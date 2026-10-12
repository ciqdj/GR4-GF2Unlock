#!/usr/bin/env python3
"""GR4-GF2Unlock: GF-2 Flash Mode for the RICOH GR IV (firmware 1.11).

Adds "GF-2 Flash Mode" as a fifth Flash Mode option, the distance-based flash exposure
mode RICOH gave the GR III in firmware 2.10. With it selected, the camera sets aperture,
ISO and shutter speed from the focus distance and the flash's guide number: the GF-2's (3)
by default, or your own flash's with --gn. As on the GR III, it applies to the GF-2 and to
flashes the camera does not communicate with (manual flashes); a P-TTL flash works as
Flash On. Turns the official RICOH firmware file you downloaded yourself into the GF-2
Flash Mode version. A file is written only if every check passes.

Usage
  python3 gr4_gf2unlock.py patch  OFFICIAL_fwdc248b.bin  [--gn GN] [-o OUTPUT_DIR]
  python3 gr4_gf2unlock.py check  ANY_fwdc248b.bin

Python 3.8 or newer, no extra packages.
"""
import argparse
import base64
import hashlib
import math
import struct
import sys
import zlib
from pathlib import Path

VERSION = '1.3.0'

OFFICIAL_SHA256 = 'a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f'
OFFICIAL_BYTES = 38648776

UNLOCKED_SHA256 = '86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a'

# Other known GR IV 1.11 builds that this tool should not be fed (identified by `check`).
OTHER_KNOWN = {
    '225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22':
        'GR4-GF2Unlock 1.2.0 (GF-2 Flash Mode, guide number 2.95, the default; not for manual flashes)',
    '660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75':
        'GR4-GF2Unlock 1.1.0 (GF-2 Flash Mode, guide number 3; not for manual flashes)',
    '45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c': 'GR4-GF2Unlock 1.0.0 (GF-2 Flash Mode, GF-2 only)',
    '4c04b48c65897f2edd028df0f5e04666ca241488c81502bae0f34e040ee454eb': 'GR4-MonoUnlock 1.0.0 (monochrome looks unlocked)',
    'fa2c67d1b67e16675a0c75b98d58c519b803f049a00e40e34103e54ca9a6a6c7': 'GR4-XPanUnlock 1.0.0 (16:9 replaced by XPan, letterboxed live view)',
    '4534d44297b69bb6d305bac2ad62fef98b0caf7a6558d6da36c049dbb88f80c8': 'GR4-XPanUnlock 1.1.0 (16:9 replaced by XPan)',
    'aa9ac5dbb05d0e362019b78c678ac322fe9b6786d980cafe1846bf191f739cb0': 'GR4-XPanUnlock 2.0.0 (XPan added next to 16:9)',
}

# The guide number GF-2 Flash Mode plans with: one word in the added code, 16*log2(GN) with GN
# at ISO 100 in metres. The change data below sets the GR III's constant, 25 (GN 2.95); --gn
# writes another value there and nothing else.
GN_OFFSET = 0x1a560
GN_DEFAULT = 25
GN_CODES = range(0, 105)            # GN 1 .. 90, the range checked offline
# Decoded contents of the reference firmware (default GN), to recognise other GN builds.
REFERENCE_PAYLOAD_SHA256 = 'ef2a1fe30969eda800de7e30cc120d5c24cad875bcb0be6b37da620b3d03237b'
# Earlier versions with a GN word, so that `check` still names their --gn files:
# (version, GN offset, decoded reference with the default GN, note).
LEGACY_GN = (
    ('1.2.0', 0x1a568, 'cfe81cdeaa129fe3cb43ff2bd721d9b1879eccad640ac28935c48a4a754c6081',
     '; not for manual flashes'),
)

# The GF-2 Flash Mode changes, applied to the official file.
PATCH_SHA256 = '09a11069a717e44d4ee86ef3d2f07c43f9b41143feaebbf30d5fe84fe4730747'
PATCH_DATA = (
    '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'
    '1L5v27vtgVtH3ChvWGJjfAf3y/j9A+FzoBk='
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


def gn_code(gn):
    """Guide number (ISO 100, m) -> the GN word: 16*log2(GN), in 1/16-stop steps."""
    code = round(16 * math.log2(gn)) if 0 < gn < 1e6 else None
    if code not in GN_CODES:
        raise Refused(f'guide number {gn:g} is outside {gn_value(GN_CODES[0]):g} to {gn_value(GN_CODES[-1]):.1f}')
    return code


def gn_value(code):
    return 2 ** (code / 16)


def payload_gn(payload, offset=GN_OFFSET, reference=REFERENCE_PAYLOAD_SHA256):
    """The GN code of a GF-2 Flash Mode payload made by this version (or by the version whose
    GN offset and reference are given), else None."""
    if len(payload) < offset + 8:
        return None
    code = struct.unpack_from('<i', payload, offset)[0]
    buf = bytearray(payload)
    struct.pack_into('<i', buf, offset, GN_DEFAULT)
    return code if sha256(rezero(bytes(buf))) == reference else None


def encode(source, frames, consumed, payload, base, patched, allowed):
    """The container for `patched` (built from the official `source`, whose decoded contents
    are `payload`), read back and checked: only `allowed` offsets and the checksum word may
    differ from `base`."""
    out, _ = rebuild(source, frames, consumed, patched, differences(payload, patched))
    again, _, used = decode(out)
    if again != patched:
        raise Refused('verification failed: the new file does not read back correctly')
    check_container(out, again, used)
    allowed = allowed | set(range(len(base) - 4, len(base)))
    if out[:HEADER] != source[:HEADER] or [i for i in differences(base, patched) if i not in allowed] or \
            sections(again) != sections(base):
        raise Refused('verification failed: unexpected changes')
    return out


def patch(source, gn=GN_DEFAULT, log=print):
    """gn: the GN word (gn_code), GN_DEFAULT for the reference firmware."""
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
    out = encode(source, frames, consumed, payload, payload, patched, allowed)
    if sha256(out) != UNLOCKED_SHA256 or payload_gn(patched) != GN_DEFAULT:
        raise Refused('verification failed: the result differs from the reference firmware')
    log('verified: the result matches the reference firmware exactly')
    if gn == GN_DEFAULT:
        return out

    log(f'setting the guide number to {gn_value(gn):.2f} ...')
    buf = bytearray(patched)
    struct.pack_into('<i', buf, GN_OFFSET, gn)
    custom = rezero(bytes(buf))
    out = encode(source, frames, consumed, payload, patched, custom, set(range(GN_OFFSET, GN_OFFSET + 4)))
    if payload_gn(custom) != gn:
        raise Refused('verification failed: the guide number was not set')
    log('verified: the reference firmware with only the guide number changed')
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
    names = {OFFICIAL_SHA256: 'official RICOH GR IV 1.11 (unmodified)', **OTHER_KNOWN}
    log(f'SHA-256  {digest}')
    log(f'bytes    {len(data)}')
    try:
        payload = check_container(data)
    except Refused as exc:
        payload, error = None, exc
    if payload is not None and digest not in names:
        for version, offset, reference, note in ((VERSION, GN_OFFSET, REFERENCE_PAYLOAD_SHA256, ''),) + LEGACY_GN:
            code = payload_gn(payload, offset, reference)
            if code is not None:
                default = ', the default' if code == GN_DEFAULT else ''
                names[digest] = (f'GR4-GF2Unlock {version} (GF-2 Flash Mode added, '
                                 f'guide number {gn_value(code):.2f}{default}{note})')
                break
    log(f'file     {names.get(digest, "unknown - not produced by this tool and not the official 1.11 file")}')
    if payload is None:
        log(f'file: INVALID - {error}')
        return 2
    log('file: valid firmware file')
    return 0 if digest in names else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog='gr4_gf2unlock.py', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', action='version', version=VERSION)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('patch', help='make the GF-2 Flash Mode firmware from the official file')
    p.add_argument('input', type=Path, help='official RICOH fwdc248b.bin (GR IV 1.11)')
    p.add_argument('--gn', type=float, default=None,
                   help='guide number of your flash at ISO 100, in metres (default: 3, as on the GR III; '
                        'range 1 to 90)')
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
        code = GN_DEFAULT if a.gn is None else gn_code(a.gn)
        print(f'GR4-GF2Unlock {VERSION}')
        print(f'guide number: {gn_value(code):.2f} (ISO 100, m)' + (' - the default' if a.gn is None else ''))
        out = patch(data, code)
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
