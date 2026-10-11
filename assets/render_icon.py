"""Icon "Stop ladder": a RICOH GF-2 throwing its beam across an 18% grey card. The light falls off with the square
of the distance and is drawn in whole stops: each band reaches √2 times farther than the one before and gets half
the light, the same √2 ladder as the f-numbers. Six bands, one for each full stop from f/2.8 to f/16, the GR IV's
range in GF-2 Flash Mode. Same card and tile as the GR4-LUTSmith icon.

Writes assets/icon-<size>.png. Needs numpy and Pillow (only for this script; the tool itself needs neither):
  python3 assets/render_icon.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent
SIZES = (128, 256, 1024)                             # README (1x, 2x) and a master

CARD = '#777777'                                     # 18% grey, L* 50
BODY = '#1E1F22'                                     # the GF-2's black housing
XENON = '#F4F7FF'                                    # flash window
BEAM = '#DCE6FF'                                     # its light: xenon is a little cooler than the card's ambient
SS = 4                                               # supersampling


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float) / 255


def to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def cov(sdf, px):
    return np.clip(0.5 - sdf / px, 0, 1)


def tile_sdf(u, v, ext=0.344, n=3.3):
    """Rounded square with continuous corners like the macOS icon shape (as in GR4-LUTSmith)."""
    x, y = np.abs(u - 0.5), np.abs(v - 0.5)
    c = 0.5 - ext
    cx, cy = np.clip(x - c, 0, None) + 1e-9, np.clip(y - c, 0, None) + 1e-9
    r = (cx ** n + cy ** n) ** (1 / n)
    g = np.hypot((cx / r) ** (n - 1), (cy / r) ** (n - 1))
    corner = (x > c) & (y > c)
    return np.where(corner, (r - ext) / g, np.maximum(x, y) - 0.5)


def rect_sdf(u, v, x0, y0, x1, y1, r=0.0):
    cx, cy, hx, hy = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    qx, qy = np.abs(u - cx) - hx, np.abs(v - cy) - hy
    return np.hypot(np.clip(qx, 0, None), np.clip(qy, 0, None)) + np.minimum(np.maximum(qx, qy), 0) - r


def box(a, w, axis):
    r = w // 2
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode='edge'), axis=axis)
    n = a.shape[axis]
    return (np.take(c, np.arange(w, w + n), axis=axis) - np.take(c, np.arange(n), axis=axis)) / w


def blur(a, sigma):
    if sigma < 0.35:
        return a
    w = int(round(np.sqrt(4 * sigma ** 2 + 1)))
    w += 1 - w % 2
    for _ in range(3):
        a = box(box(a, w, 0), w, 1)
    return a


def shift(a, dx, dy):
    out = np.zeros_like(a)
    h, w = a.shape
    out[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = a[max(-dy, 0):h - max(dy, 0), max(-dx, 0):w - max(dx, 0)]
    return out


def params(size):
    return dict(body=round(size * 824 / 1024),
                bands=6,
                gain=6.0,                         # flash light in the first band, in units of the ambient light
                half=np.radians(22),
                r0=0.085,                         # first band edge, measured from the flash window
                head=(0.105, 0.438, 0.235, 0.563))


def render(size):
    p = params(size)
    S = size * SS
    B = p['body'] * SS
    o = (S - B) / 2
    ys, xs = np.mgrid[0:S, 0:S] + 0.5
    u, v, px = (xs - o) / B, (ys - o) / B, 1 / B

    tsdf = tile_sdf(u, v)
    tile = cov(tsdf, px)

    # ambient: the grey card, lit softly from above
    amb = to_lin(hex_rgb(CARD)) * (1 + 0.10 * (0.5 - v))[..., None]

    # the GF-2, seen from the side: black housing on a hot-shoe foot, xenon window facing the subject
    hx0, hy0, hx1, hy1 = p['head']
    hh = hy1 - hy0
    wy0, wy1 = hy0 + 0.16 * hh, hy1 - 0.16 * hh
    wx, wy = hx1, (wy0 + wy1) / 2

    # the beam leaves the window and spreads; its light falls off in whole stops with the distance from the window
    ax = wx - (wy1 - wy0) / 2 / np.tan(p['half'])  # wedge apex behind the window, so the beam is window-high there
    ang = np.arctan2(v - wy, u - ax)
    in_wedge = cov((np.abs(ang) - p['half']) * np.hypot(u - ax, v - wy), px) * (u > wx - 0.01)
    r = np.hypot(u - wx, v - wy)
    stop = np.floor(np.log(np.maximum(r, 1e-6) / p['r0']) / np.log(np.sqrt(2)))
    stop = np.clip(stop, 0, None)
    fin = cov(r - p['r0'] * np.sqrt(2) ** p['bands'], px)       # the beam ends after the last stop
    flash = p['gain'] * 0.5 ** stop * in_wedge * fin
    rgb = amb * (1 + flash[..., None] * to_lin(hex_rgb(BEAM)))

    hsdf = rect_sdf(u, v, hx0, hy0, hx1, hy1, 0.016)
    foot = rect_sdf(u, v, hx0 + 0.25 * (hx1 - hx0), hy1 - 0.01, hx1 - 0.25 * (hx1 - hx0), hy1 + 0.032, 0.004)
    head = cov(np.minimum(hsdf, foot), px)
    sh = blur(shift(head, 0, round(0.020 * B)), 0.022 * B) * 0.45
    sh *= 1 - np.clip(flash / p['gain'], 0, 1)                    # the beam washes the shadow out
    rgb = rgb * (1 - sh[..., None])
    body = to_lin(hex_rgb(BODY)) * (1 + 0.7 * np.clip((hy1 - v) / hh, 0, 1.3))[..., None]
    win = cov(rect_sdf(u, v, hx1 - 0.03, wy0, hx1 + 0.004, wy1, 0.005), px) * head
    glow = to_lin(hex_rgb(XENON))
    rgb = rgb * (1 - head[..., None]) + body * head[..., None]
    rgb = rgb * (1 - win[..., None]) + glow * win[..., None]

    rgb = to_srgb(rgb)

    # tile edge: light rim at the top, faint dark rim all round (as in GR4-LUTSmith)
    rim_w = max(px, 0.0035)
    ring = tile - cov(tsdf + rim_w, px)
    rgb += (1 - rgb) * (0.20 * ring * np.clip(1.2 - 2.2 * v, 0, 1))[..., None]
    dark = tile - cov(tsdf + max(px * 0.8, 0.0015), px)
    rgb *= 1 - 0.14 * dark[..., None]

    k = S / 1024
    drop = blur(shift(tile, 0, max(1, round(10 * k))), max(0.5, 9 * k)) * 0.30
    alpha = tile + drop * (1 - tile)
    out = np.where(alpha[..., None] > 0, rgb * tile[..., None] / np.maximum(alpha, 1e-6)[..., None], 0)
    big = np.dstack([out * alpha[..., None], alpha])           # premultiplied for a clean downsample
    small = big.reshape(size, SS, size, SS, 4).mean((1, 3))
    a = small[..., 3:]
    small[..., :3] = np.where(a > 0, small[..., :3] / np.maximum(a, 1e-6), 0)
    return Image.fromarray(np.round(np.clip(small, 0, 1) * 255).astype(np.uint8), 'RGBA')


def main():
    for s in SIZES:
        render(s).save(OUT / f'icon-{s}.png')
    print('written', ', '.join(f'icon-{s}.png' for s in SIZES))


if __name__ == '__main__':
    main()
