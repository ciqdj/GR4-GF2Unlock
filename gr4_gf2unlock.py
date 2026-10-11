#!/usr/bin/env python3
"""GR4-GF2Unlock: GF-2 Flash Mode for the RICOH GR IV (firmware 1.11).

Adds "GF-2 Flash Mode" as a fifth Flash Mode option, the distance-based flash exposure
mode RICOH gave the GR III in firmware 2.10. With the RICOH GF-2 flash attached, the
camera fires the flash at a fixed power and sets aperture, ISO and shutter speed from the
focus distance. Turns the official RICOH firmware file you downloaded yourself into the
GF-2 Flash Mode version. A file is written only if every check passes.

Usage
  python3 gr4_gf2unlock.py patch  OFFICIAL_fwdc248b.bin  [-o OUTPUT_DIR]
  python3 gr4_gf2unlock.py check  ANY_fwdc248b.bin

Python 3.8 or newer, no extra packages.
"""
import argparse
import base64
import hashlib
import struct
import sys
import zlib
from pathlib import Path

VERSION = '1.0.0'

OFFICIAL_SHA256 = 'a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f'
OFFICIAL_BYTES = 38648776

UNLOCKED_SHA256 = '45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c'

# Other known GR IV 1.11 builds that this tool should not be fed (identified by `check`).
OTHER_KNOWN = {
    '4c04b48c65897f2edd028df0f5e04666ca241488c81502bae0f34e040ee454eb': 'GR4-MonoUnlock 1.0.0 (monochrome looks unlocked)',
    'fa2c67d1b67e16675a0c75b98d58c519b803f049a00e40e34103e54ca9a6a6c7': 'GR4-XPanUnlock 1.0.0 (16:9 replaced by XPan, letterboxed live view)',
    '4534d44297b69bb6d305bac2ad62fef98b0caf7a6558d6da36c049dbb88f80c8': 'GR4-XPanUnlock 1.1.0 (16:9 replaced by XPan)',
    'aa9ac5dbb05d0e362019b78c678ac322fe9b6786d980cafe1846bf191f739cb0': 'GR4-XPanUnlock 2.0.0 (XPan added next to 16:9)',
}

# The GF-2 Flash Mode changes, applied to the official file.
PATCH_SHA256 = '6a1fe047c906fef68e1e0f916f8683107b81c734312c313d806acd9b1b6cafad'
PATCH_DATA = (
    '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'
)

HEADER, MAGIC, FOOTER_MAGIC = 128, b'RICOH\0\0\0', b'\xa5\x5a\x5a\xa5'
MAX_DISTANCE = 0x2000
LITERAL_CHUNK = 0x6000


class Refused(Exception):
    pass


INVALID = 'not a valid RICOH firmware file'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def word_sum(data):
    if len(data) % 4:
        raise Refused(INVALID)
    return sum(w for (w,) in struct.iter_unpack('<I', data)) & 0xffffffff


def decode(data, limit=256 * 1024 * 1024):
    if len(data) < 160 or data[:8] != MAGIC:
        raise Refused(INVALID)
    out = bytearray()
    frames = []
    cursor = HEADER
    while True:
        start = cursor
        if cursor + 2 > len(data):
            raise Refused(INVALID)
        descriptor = int.from_bytes(data[cursor:cursor + 2], 'big')
        cursor += 2
        if descriptor == 0:
            return bytes(out), frames, cursor
        size = descriptor & 0x7fff
        end = cursor + size
        if not size or end > len(data):
            raise Refused(INVALID)
        output_start = len(out)
        if descriptor & 0x8000:
            out += data[cursor:end]
            cursor = end
        else:
            while cursor < end:
                if cursor + 2 > end:
                    raise Refused(INVALID)
                flags = int.from_bytes(data[cursor:cursor + 2], 'big')
                cursor += 2
                for bit in range(15, -1, -1):
                    if cursor == end:
                        break
                    if not flags & (1 << bit):
                        out.append(data[cursor])
                        cursor += 1
                        continue
                    if cursor + 2 > end:
                        raise Refused(INVALID)
                    a, b = data[cursor], data[cursor + 1]
                    cursor += 2
                    distance = ((a >> 3) << 8) | b
                    length = a & 7
                    if length == 7:
                        while True:
                            if cursor >= end:
                                raise Refused(INVALID)
                            extension = data[cursor]
                            cursor += 1
                            length += extension
                            if extension != 255:
                                break
                    if distance == 0:
                        break
                    if distance > len(out):
                        raise Refused(INVALID)
                    count = length + 3
                    if distance >= count:
                        out += out[-distance:len(out) - distance + count]
                    else:
                        pattern = bytes(out[-distance:])
                        out += (pattern * ((count + distance - 1) // distance))[:count]
                if len(out) > limit:
                    raise Refused(INVALID)
        frames.append((start, end, output_start, len(out)))


def check_container(data, payload=None, consumed=None):
    if payload is None:
        payload, _, consumed = decode(data)
    if data[-20:-16] != FOOTER_MAGIC:
        raise Refused(INVALID)
    enc, dec = struct.unpack_from('<II', data, len(data) - 12)
    if enc != consumed - HEADER or dec != len(payload):
        raise Refused(INVALID)
    if word_sum(data) or word_sum(payload):
        raise Refused(INVALID)
    return payload


def sections(payload):
    out, pos = [], 0
    while pos + 16 <= len(payload):
        tag = payload[pos:pos + 8].rstrip(b'\0')
        if not tag or not tag.isalnum() or not tag.isupper():
            break
        size = struct.unpack_from('<I', payload, pos + 12)[0]
        if pos + 16 + size > len(payload):
            break
        out.append((tag.decode(), pos + 16, pos + 16 + size))
        pos += 16 + size
    return out


def differences(a, b, block=1 << 16):
    if len(a) != len(b):
        raise Refused(INVALID)
    out = []
    for pos in range(0, len(a), block):
        x, y = a[pos:pos + block], b[pos:pos + block]
        if x != y:
            out += [pos + i for i in range(len(x)) if x[i] != y[i]]
    return out


def rezero(payload):
    buf = bytearray(payload)
    last = struct.unpack_from('<I', buf, len(buf) - 4)[0]
    struct.pack_into('<I', buf, len(buf) - 4, (last - word_sum(buf)) & 0xffffffff)
    return bytes(buf)


def literal_frames(data):
    out = bytearray()
    for pos in range(0, len(data), LITERAL_CHUNK):
        chunk = data[pos:pos + LITERAL_CHUNK]
        out += struct.pack('>H', 0x8000 | len(chunk)) + chunk
    return bytes(out)


def rebuild(source, frames, consumed, patched, changed):
    body = bytearray()
    reemitted = 0
    for (c0, c1, d0, d1) in frames:
        if any(d0 <= c < d1 or c < d0 < c + MAX_DISTANCE for c in changed):
            body += literal_frames(patched[d0:d1])
            reemitted += 1
        else:
            body += source[c0:c1]
    body += b'\0\0'
    trailer = bytearray(source[consumed:])
    struct.pack_into('<II', trailer, len(trailer) - 12, len(body), len(patched))
    struct.pack_into('<I', trailer, len(trailer) - 4, 0)
    padding = bytes((-HEADER - len(body) - len(trailer)) % 4)
    out = bytearray(source[:HEADER] + body + padding + trailer)
    struct.pack_into('<I', out, len(out) - 4, (-word_sum(out)) & 0xffffffff)
    return bytes(out), reemitted


def patch(source, log=print):
    digest = sha256(source)
    if digest != OFFICIAL_SHA256 or len(source) != OFFICIAL_BYTES:
        if digest == UNLOCKED_SHA256:
            raise Refused('this file already has GF-2 Flash Mode; use the official RICOH file')
        if digest in OTHER_KNOWN:
            raise Refused(f'this file is {OTHER_KNOWN[digest]}; use the official RICOH file')
        raise Refused('input is not the official RICOH GR IV 1.11 fwdc248b.bin '
                      f'(SHA-256 {digest}, expected {OFFICIAL_SHA256})')
    log('input: official RICOH GR IV 1.11 firmware (SHA-256 verified)')

    log('reading the firmware ...')
    payload, frames, consumed = decode(source)
    check_container(source, payload, consumed)
    secs = sections(payload)

    log('adding GF-2 Flash Mode ...')
    raw = zlib.decompress(base64.b64decode(''.join(PATCH_DATA)))
    if sha256(raw) != PATCH_SHA256:
        raise Refused('the change data in this tool is damaged; download the tool again')
    buf = bytearray(payload)
    allowed = set()
    pos = 0
    while pos < len(raw):
        off, n = struct.unpack_from('>II', raw, pos)
        old, new = raw[pos + 8:pos + 8 + n], raw[pos + 8 + n:pos + 8 + 2 * n]
        pos += 8 + 2 * n
        if bytes(buf[off:off + n]) != old or not any(a <= off and off + n <= b for _, a, b in secs):
            raise Refused('the firmware does not have the expected contents')
        buf[off:off + n] = new
        allowed |= set(range(off, off + n))
    patched = rezero(bytes(buf))

    log('writing the new firmware ...')
    changed = differences(payload, patched)
    out, _ = rebuild(source, frames, consumed, patched, changed)

    log('verifying result ...')
    again, _, used = decode(out)
    if again != patched:
        raise Refused('verification failed: the new file does not read back correctly')
    check_container(out, again, used)
    allowed |= set(range(len(payload) - 4, len(payload)))
    if out[:HEADER] != source[:HEADER] or [i for i in changed if i not in allowed] or \
            sections(again) != secs:
        raise Refused('verification failed: unexpected changes')
    if sha256(out) != UNLOCKED_SHA256:
        raise Refused('verification failed: the result differs from the camera-tested firmware')
    log('verified: the result matches the camera-tested firmware exactly')
    return out


def write_atomic(data, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / 'fwdc248b.bin'
    if target.exists():
        raise Refused(f'{target} already exists; choose another output directory or remove it')
    tmp = target.with_name('.fwdc248b.bin.tmp')
    tmp.write_bytes(data)
    if sha256(tmp.read_bytes()) != sha256(data):
        tmp.unlink()
        raise Refused('write verification failed')
    tmp.rename(target)
    return target


def identify(data, log=print):
    digest = sha256(data)
    names = {OFFICIAL_SHA256: 'official RICOH GR IV 1.11 (unmodified)',
             UNLOCKED_SHA256: f'GR4-GF2Unlock {VERSION} (GF-2 Flash Mode added)', **OTHER_KNOWN}
    log(f'SHA-256  {digest}')
    log(f'bytes    {len(data)}')
    log(f'file     {names.get(digest, "unknown - not produced by this tool and not the official 1.11 file")}')
    try:
        check_container(data)
        log('file: valid firmware file')
    except Refused as exc:
        log(f'file: INVALID - {exc}')
        return 2
    return 0 if digest in names else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog='gr4_gf2unlock.py', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', action='version', version=VERSION)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('patch', help='make the GF-2 Flash Mode firmware from the official file')
    p.add_argument('input', type=Path, help='official RICOH fwdc248b.bin (GR IV 1.11)')
    p.add_argument('-o', '--output-dir', type=Path, default=Path('output'),
                   help='directory for the result (default: ./output); the file is named fwdc248b.bin')
    c = sub.add_parser('check', help='identify a fwdc248b.bin and validate its container')
    c.add_argument('input', type=Path)
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)
    if sys.version_info < (3, 8):
        print('Python 3.8 or newer is required', file=sys.stderr)
        return 2
    try:
        data = a.input.read_bytes()
        if a.cmd == 'check':
            return identify(data)
        if (a.output_dir / 'fwdc248b.bin').exists():
            raise Refused(f'{a.output_dir / "fwdc248b.bin"} already exists; '
                          'choose another output directory or remove it')
        print(f'GR4-GF2Unlock {VERSION}')
        out = patch(data)
        target = write_atomic(out, a.output_dir)
        print(f'wrote {target}  (SHA-256 {sha256(out)})')
        print('Copy this file to the root of the SD card and run the camera\'s firmware update.')
        return 0
    except Refused as exc:
        print(f'refused: {exc}', file=sys.stderr)
        print('nothing was written.', file=sys.stderr)
        return 1
    except OSError as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
