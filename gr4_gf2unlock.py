#!/usr/bin/env python3
"""GR4-GF2Unlock: GF-2 Flash Mode for the RICOH GR IV (firmware 1.11).

Adds "GF-2 Flash Mode" as a fifth Flash Mode option, the distance-based flash exposure
mode RICOH gave the GR III in firmware 2.10. With it selected, the camera fires the flash
at a fixed power and sets aperture, ISO and shutter speed from the focus distance and the
flash's guide number: the GF-2's (3) by default, or your own flash's with --gn. Turns the
official RICOH firmware file you downloaded yourself into the GF-2 Flash Mode version. A
file is written only if every check passes.

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

VERSION = '1.2.0'

OFFICIAL_SHA256 = 'a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f'
OFFICIAL_BYTES = 38648776

UNLOCKED_SHA256 = '225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22'

# Other known GR IV 1.11 builds that this tool should not be fed (identified by `check`).
OTHER_KNOWN = {
    '660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75': 'GR4-GF2Unlock 1.1.0 (GF-2 Flash Mode, guide number 3)',
    '45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c': 'GR4-GF2Unlock 1.0.0 (GF-2 Flash Mode, GF-2 only)',
    '4c04b48c65897f2edd028df0f5e04666ca241488c81502bae0f34e040ee454eb': 'GR4-MonoUnlock 1.0.0 (monochrome looks unlocked)',
    'fa2c67d1b67e16675a0c75b98d58c519b803f049a00e40e34103e54ca9a6a6c7': 'GR4-XPanUnlock 1.0.0 (16:9 replaced by XPan, letterboxed live view)',
    '4534d44297b69bb6d305bac2ad62fef98b0caf7a6558d6da36c049dbb88f80c8': 'GR4-XPanUnlock 1.1.0 (16:9 replaced by XPan)',
    'aa9ac5dbb05d0e362019b78c678ac322fe9b6786d980cafe1846bf191f739cb0': 'GR4-XPanUnlock 2.0.0 (XPan added next to 16:9)',
}

# The guide number GF-2 Flash Mode plans with: one word in the added code, 16*log2(GN) with GN
# at ISO 100 in metres. The change data below sets the GR III's constant, 25 (GN 2.95); --gn
# writes another value there and nothing else.
GN_OFFSET = 0x1a568
GN_DEFAULT = 25
GN_CODES = range(0, 105)            # GN 1 .. 90, the range checked offline
# Decoded contents of the reference firmware (default GN), to recognise other GN builds.
REFERENCE_PAYLOAD_SHA256 = 'cfe81cdeaa129fe3cb43ff2bd721d9b1879eccad640ac28935c48a4a754c6081'

# The GF-2 Flash Mode changes, applied to the official file.
PATCH_SHA256 = '71a04cf3d2fa214edc4132525cbfa626c1203b922fdd73e92d7735342266584a'
PATCH_DATA = (
    'eNrtVv9vU1UUP++1Xbv3xnrnJo4OxgM0mV+Q8kUczsgbX5RYlMJCIHPGMpYwjJFuky8/gCm1qBsu'
    'gC4xQSaXGAzyi0U0TOKyt2wjhhgzk/1klvBer6/Dhd50CI4YYz33bcgk8w8w2U26c/o5957zOV/u'
    '7UD6tAsg7wLMrJk1s2bWzJpZ/4flhjB7CKDNZ3TYwwPDtgx1rBggAFmNTf0I+2tol9CuCjuec6MU'
    '+HfGsOUyNqbEWcROuoFaJYOhVGlj5/UC47Q9N7fEyhP7UYexUyMVC6FmxciuGhE/u2nxr+7Bl1K+'
    'o4szpULqx2345CvuJsdtQtrtOUpHhgSNm6sCHRlDGee9gXF+Ro1yd9mYI1vVCNfV25z8Mcatx69l'
    'UmXXMvXqLV5flX1ZYJGq7I87qm459h2oM7WbG+odbla1cFB/RzvaFOLYkftVCYjIQYlMnpEwRwli'
    'qXyAUQj9xUGjDAhlDXftGrgkAmtlDUyZHLYk0M0SaLeJbtwMIHfjmXHeWrWT61UTHOvxXH1ogtvO'
    'EHILTXJD/RfBrewOt8re4pGy/+BVNoVXeJKXeo/XP/b7eYV1syuSzyqQ066d69lK7IkbeT6K34Xu'
    'Q33tpH6KDtkQpdarjwzZCU+HnSwZwry2oP92e3upzKB4PYPYCVsia1JFp/dYBRrmG9sgi5mYjRwP'
    'zQqzOPbh0Cy6KPZtPiMK8NkX1zMd635GjfEqjKEfTfJKUNhsF/pSkzyImMBB/Z6P+EMp0VdTveTg'
    'htLNSYBwELlijiXQaXu0980v6qkFUMtIkqc1jOsOdtqlUcpkrdosiHXaLUYu3RTMpT97+rDZEuxJ'
    '90VfMJtQ6rCN6VG6SIIaVhqFPq8WNzUtnmpGm0/rtJu1nrQMNZZLoxcOIuaCLVY5wHlZ22iKvc3R'
    'CR8V2Jc8Sq11ZjyF9WLLkJ8X4k5sMQf7j+fSD+PsRMM96VdgK3sA99eFsU+wnRVh/5qgJ+3FmhUi'
    '7oVqc34l2nzvmLI3zD6f9C3yVdDvOvO9lPNd5GdQC+/saAJ9JsJ0kdgjoU9h9xPTlQ9HTQ/Gx7k1'
    'Q6Jm0YmYpf49VrOWS5MouDZgP/M04Q+W04V0gTgvR2iRqK3wkzDxTAQ/Yq6Q837kWQpw+YAWSjWH'
    'c+mz2+LmXsxrIExxdrYyn7j3uO/PJX6Rz6i427HEk72Tstp5bPRjejPmPFhojQDWSfiO4ndNWmNG'
    'kddeyKWp4686FSU9aYDNDOf7RTzJqH8TU30xU2+kluG/YsWkiEV3UGtQ+nKEIDcSgT6JVKSyfj/z'
    'khMWJI9CIRwxC0jczCPVZhQ5i1gJ3JsIQ58H3jObiOjtZpyhkCkFaa8L69WCPdMjsRSpBd4F+QzO'
    'f8134YzqShdvWxJLSZcvc4I1cvqiaFxtC/INSpIvc+Z0nO/D2ZHKbt57m/AeCN3Euy3uM+AsYU4/'
    'i374xTtKnnd4+DBX1cFrhVT2kVzaqSPBWQr2sjcwHs4km0vAJSNnmdCfvGiP4j4Pyux8P5PIu+gr'
    'J+pmIX5FoqLvmy1yUsL3gl6Axy5xcRcBKKsOdHEDc1ICC7jIQw4s5aoS5CuUROaptkRmZSCRiZzt'
    't3d7+u3X8VM62I5vdPcNN8rsse7rMrSawr+Yc5w5vJNizv9d4zqUdWG4WJvLjbZnvqHjV5LPJfsH'
    '8d2pE30NgEFZst+wfMagDRO/HYHhgQmdXIVCnHM2PGDYASWWKRdvA645MK88gdKDPzLFsgf/uGDe'
    'ggOIeMOVSnHjcn8Dit9W+2DeE3emQ5eumA6NTLv3SN39kVoPTrfvg2l9Hrs+HUorpkHL38wimo+R'
    'mEhURHMUF5THGtEihRtQ+wE1F55yTpzz3cXPVU7FDXoXN4am4KtaIgKHI7CqTex3S1q8+HYuF4DV'
    'hzqE5UEXrH5bF1qRF3Y3POv8bzB2+uPOwvRJ2P2h4+uGFz5ypyG+bsjxJf8NrYJAAg=='
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


def payload_gn(payload):
    """The GN code of a GF-2 Flash Mode payload made by this version, else None."""
    if len(payload) < GN_OFFSET + 8:
        return None
    code = struct.unpack_from('<i', payload, GN_OFFSET)[0]
    buf = bytearray(payload)
    struct.pack_into('<i', buf, GN_OFFSET, GN_DEFAULT)
    return code if sha256(rezero(bytes(buf))) == REFERENCE_PAYLOAD_SHA256 else None


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
    code = payload_gn(payload) if payload is not None and digest not in names else None
    if code is not None:
        default = ', the default' if code == GN_DEFAULT else ''
        names[digest] = (f'GR4-GF2Unlock {VERSION} (GF-2 Flash Mode added, '
                         f'guide number {gn_value(code):.2f}{default})')
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
