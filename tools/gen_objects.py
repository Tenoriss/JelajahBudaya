"""gen_objects.py -- original top-down / 3-4 view pixel art objects & buildings.

Outputs PNGs + data/objects.json (sprite size, collision box, anchor, shadow).

Run: python3 tools/gen_objects.py
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artlib import Canvas, P, c, mix, shade  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "objects")
OUT_DATA = os.path.join(ROOT, "data")

REGISTRY = {}


def scale_canvas(cv: Canvas, factor: float) -> Canvas:
    """Nearest-neighbour whole-sprite scale (keeps the pixel look)."""
    from PIL import Image
    img = cv.img.resize((max(1, int(cv.w * factor)), max(1, int(cv.h * factor))), Image.NEAREST)
    out = Canvas(1, 1)
    out.w, out.h = img.width, img.height
    out.img = img
    from PIL import ImageDraw
    out.d = ImageDraw.Draw(img)
    return out


def reg(name, cv: Canvas, collision=None, anchor="bottom", shadow=True, sway=False, tag="prop"):
    os.makedirs(OUT, exist_ok=True)
    cv.save(os.path.join(OUT, name + ".png"))
    REGISTRY[name] = {
        "file": f"assets/objects/{name}.png",
        "size": [cv.w, cv.h],
        "collision": collision,      # [x, y, w, h] relative to sprite top-left, or None
        "anchor": anchor,
        "shadow": shadow,
        "sway": sway,
        "tag": tag,
    }


# ==========================================================================
#  NATURE
# ==========================================================================
def tree_tropical(seed=1, palette=("jungle", "jungle2", "jungle3"), fruits=None, h=88, w=64):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    cx = w // 2
    trunk_top = h - 24
    # trunk
    for y in range(trunk_top, h):
        tw = 5 - (y - trunk_top) // 12
        cv.rect(cx - tw // 2, y, cx + tw // 2, y, shade("#8a6440", -0.1))
        cv.px(cx - tw // 2, y, shade("#8a6440", -0.3))
        cv.px(cx + tw // 2, y, shade("#6d4c30", -0.1))
    # roots
    for dx in (-6, 6):
        cv.line([(cx, h - 2), (cx + dx, h - 1)], "#5e4229", 2)
    # canopy: layered blobs
    layers = [
        (h - 72, 26, palette[1]),
        (h - 62, 30, palette[0]),
        (h - 50, 26, palette[2]),
        (h - 40, 20, palette[0]),
    ]
    for cy, rad, col in layers:
        for i in range(9):
            a = i / 9 * 6.28318
            bx = cx + int((rad - 4) * 0.72 * (1 + 0.35 * rng.random()) * (1 if i % 2 else 0.8) * (1 if abs(a - 3.14) < 1.6 else 0.55)) * (1 if a < 3.14 else -1)
            by = cy + int((rad - 6) * 0.34 * (rng.random() - 0.5) * 2)
            r = rng.randint(8, 13)
            cv.ellipse(bx - r, by - r + 2, bx + r, by + r, col)
    # highlight pass
    for _ in range(26):
        x = cx + rng.randint(-24, 24)
        y = h - 70 + rng.randint(-10, 26)
        d = abs(x - cx) / 24 + abs(y - (h - 58)) / 30
        if d < 1.1:
            cv.ellipse(x, y, x + rng.randint(2, 4), y + rng.randint(1, 3), shade(palette[2], 0.18))
    if fruits:
        for _ in range(5):
            x = cx + rng.randint(-20, 20)
            y = h - 60 + rng.randint(-8, 22)
            cv.ellipse(x, y, x + 3, y + 3, fruits)
            cv.px(x + 1, y + 1, shade(fruits, 0.35))
    cv.outline("#241c22", alpha_test=60)
    return cv


def tree_palm(seed=2, h=84, w=56):
    """Leaning coconut palm with fronds radiating from the crown."""
    import math
    rng = random.Random(seed)
    cv = Canvas(w, h)
    cx = w // 2
    # curved trunk made of stacked segments
    seg = []
    for y in range(24, h):
        t = (y - 24) / max(1, (h - 24))
        x = cx + int(t * t * 8)
        seg.append((x, y))
    for i, (x, y) in enumerate(seg):
        t = i / max(1, len(seg) - 1)
        wdt = max(2, 5 - int(t * 3))
        col = "#b8903f" if i % 7 else "#a07d34"
        cv.rect(x - wdt // 2, y, x + wdt // 2, y, col)
        cv.rect(x - wdt // 2, y, x - wdt // 2, y, "#87672b")
        # ring marks
        if i % 6 == 0:
            cv.rect(x - wdt // 2, y, x + wdt // 2, y, "#7d5f28")
    cx_top, cy_top = seg[0]
    # fronds
    n = 9
    for i in range(n):
        a = -math.pi * 0.98 + i * (math.pi * 1.96 / (n - 1))
        L = rng.randint(20, 27)
        ex = cx_top + int(L * math.cos(a))
        ey = cy_top + int(L * math.sin(a) * 0.52)
        col = "#4f9c46" if i % 2 else "#3d7c3a"
        mid = ((cx_top + ex) // 2, (cy_top + ey) // 2 - 5)
        cv.line([(cx_top, cy_top), mid, (ex, ey)], col, 3)
        cv.line([(cx_top, cy_top - 1), (mid[0], mid[1] - 2), (ex, ey - 2)], shade(col, 0.22), 1)
        # leaflets
        for k in range(1, 6):
            t = k / 6
            lx = int(cx_top + (ex - cx_top) * t)
            ly = int(cy_top + (ey - cy_top) * t - (4 if abs(a) < 2 else 2))
            cv.px(lx, ly - 2, shade(col, 0.1))
            cv.px(lx, ly + 2, shade(col, -0.15))
    cv.ellipse(cx_top - 5, cy_top - 5, cx_top + 5, cy_top + 5, "#2f5c30")
    # coconuts
    for k in range(3):
        cv.ellipse(cx_top - 4 + k * 4, cy_top + 1, cx_top + k * 4, cy_top + 6, "#c08a3a")
        cv.px(cx_top - 3 + k * 4, cy_top + 2, "#d8a44c")
    cv.outline("#241c22", alpha_test=60)
    return cv


def tree_pine(seed=3, h=76, w=44):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    cx = w // 2
    cv.rect(cx - 2, h - 14, cx + 2, h - 1, "#7a5a3c")
    for i, (cy, rad, col) in enumerate([(h - 16, 19, "#2f5c44"), (h - 28, 16, "#356a4c"),
                                        (h - 39, 13, "#3f7a54"), (h - 49, 9, "#4a8a5e")]):
        for k in range(7):
            x = cx - rad + int(k * (2 * rad) / 6)
            cv.line([(cx, cy - 10), (x, cy + 6)], col, 4)
        cv.line([(cx, cy - 12), (cx, cy + 8)], shade(col, 0.18), 2)
    cv.outline("#241c22", alpha_test=60)
    return cv


def bamboo_cluster(seed=4, h=70, w=48):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    for i in range(5):
        x = 10 + i * 7 + rng.randint(-2, 2)
        top = 8 + rng.randint(0, 12)
        col = "#93b24a" if i % 2 else "#7fa03c"
        cv.rect(x, top, x + 3, h - 2, col)
        cv.rect(x, top, x, h - 2, shade(col, 0.22))
        cv.rect(x + 3, top, x + 3, h - 2, shade(col, -0.22))
        for y in range(top + 5, h - 4, 10):  # nodes
            cv.rect(x, y, x + 3, y, shade(col, -0.35))
        # leaves
        for k in range(4):
            ly = top + 6 + k * 7
            lx = x + (6 if k % 2 == 0 else -6)
            cv.line([(x, ly), (lx, ly - 3), (lx + (5 if k % 2 == 0 else -5), ly - 1)], "#4f8a3c", 2)
    cv.outline("#241c22", alpha_test=60)
    return cv


def bush(seed=5, w=40, h=28, flower=None, col="#4a8a44"):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    for _ in range(14):
        x = rng.randrange(4, w - 8)
        y = rng.randrange(6, h - 6)
        r = rng.randint(5, 9)
        cv.ellipse(x, y, x + r, y + r - 2, col)
    for _ in range(10):
        x = rng.randrange(4, w - 8)
        y = rng.randrange(4, h - 10)
        cv.ellipse(x, y, x + 4, y + 3, shade(col, 0.22))
    if flower:
        for _ in range(5):
            x = rng.randrange(6, w - 8)
            y = rng.randrange(6, h - 8)
            cv.px(x, y, flower)
            cv.px(x + 1, y, shade(flower, 0.3))
            cv.px(x, y + 1, shade(flower, -0.2))
    cv.outline("#241c22", alpha_test=60)
    return cv


def fern(seed=6, w=42, h=34):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    cx = w // 2
    for i in range(6):
        a = -2.6 + i * 0.75
        import math
        L = rng.randint(14, 19)
        ex, ey = cx + int(L * math.cos(a)), h - 4 + int(L * math.sin(a) * 0.55)
        cv.line([(cx, h - 3), (cx + (ex - cx) // 2, h - 8), (ex, ey)], "#3f7a3c", 2)
        for k in range(3):
            t = 0.35 + k * 0.25
            px, py = int(cx + (ex - cx) * t), int(h - 3 + (ey - (h - 3)) * t)
            cv.px(px, py - 1, "#66a04e")
            cv.px(px + 1, py - 2, "#66a04e")
    cv.outline("#241c22", alpha_test=60)
    return cv


def rock(seed=7, w=34, h=26, big=False):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    pts = []
    n = 9
    for i in range(n):
        a = i / n * 6.28318
        r = (w // 2 - 2) * (0.7 + rng.random() * 0.4) if not big else (w // 2 - 1)
        pts.append((w // 2 + int(r * __import__("math").cos(a)), h - 6 + int((h * 0.42) * __import__("math").sin(a))))
    cv.poly(pts, "#8c8880")
    for i in range(0, n, 2):  # top highlight
        x, y = pts[i]
        cv.line([(x, y), (x - 3, y + 4)], shade("#8c8880", 0.25), 2)
    for _ in range(8):
        cv.px(rng.randrange(6, w - 6), rng.randrange(6, h - 8), shade("#8c8880", -0.25))
    cv.ellipse(w // 2 - 6, h - 9, w // 2 + 6, h - 4, "#6d6a64")
    cv.outline("#241c22", alpha_test=60)
    return cv


def stump(seed=8):
    cv = Canvas(28, 20)
    cv.ellipse(4, 8, 24, 19, "#7a5a3a")
    cv.ellipse(6, 3, 22, 14, "#966f45")
    cv.ellipse(9, 6, 19, 12, "#a87f52")
    cv.ellipse(11, 7, 15, 10, "#8c6a44")
    cv.outline("#241c22", alpha_test=60)
    return cv


def flower_patch(seed=9, w=26, h=20, colors=("#e0728a", "#f0d060", "#e8e8e8")):
    rng = random.Random(seed)
    cv = Canvas(w, h)
    for _ in range(7):
        x, y = rng.randrange(2, w - 3), rng.randrange(4, h - 4)
        col = rng.choice(colors)
        cv.px(x, y, col)
        cv.px(x + 1, y, col)
        cv.px(x, y + 1, shade(col, -0.15))
        cv.px(x + 1, y + 2, "#4a8a3c")
    cv.outline("#241c22", alpha_test=60)
    return cv


def mushroom(seed=10):
    cv = Canvas(20, 18)
    cv.rect(8, 10, 11, 16, "#e8dcc0")
    cv.ellipse(3, 2, 16, 12, "#c05040")
    cv.ellipse(5, 3, 14, 9, "#d86050")
    for x, y in [(7, 5), (11, 7), (9, 4)]:
        cv.ellipse(x, y, x + 2, y + 1, "#f0e8d0")
    cv.outline("#241c22", alpha_test=60)
    return cv


def log(seed=11):
    cv = Canvas(46, 22)
    cv.rect(4, 6, 41, 17, "#8a6240")
    cv.rect(4, 6, 41, 8, "#a2764c")
    cv.rect(4, 15, 41, 17, "#6d4c30")
    cv.ellipse(2, 6, 12, 18, "#9c7448")
    cv.ellipse(5, 9, 9, 15, "#7a5a38")
    for x in range(14, 40, 6):
        cv.rect(x, 6, x, 17, "#7a5a38")
    cv.outline("#241c22", alpha_test=60)
    return cv


def reed_clump(seed=12):
    rng = random.Random(seed)
    cv = Canvas(34, 34)
    for i in range(9):
        x = 3 + i * 3 + rng.randint(-1, 1)
        top = 4 + rng.randint(0, 8)
        cv.line([(x, 32), (x + rng.randint(-2, 2), top)], "#6f9c52", 2)
        cv.px(x, 32, "#4f7a3c")
    cv.outline("#241c22", alpha_test=60)
    return cv


def lily_pad(seed=13):
    cv = Canvas(26, 18)
    cv.ellipse(2, 4, 22, 16, "#3f8a4a")
    cv.ellipse(4, 5, 20, 13, "#4f9c56")
    cv.poly([(12, 10), (16, 6), (16, 13)], (0, 0, 0, 0))
    cv.ellipse(11, 3, 17, 9, "#e07a9a")
    cv.ellipse(12, 4, 16, 7, "#f0a0b8")
    cv.outline("#241c22", alpha_test=60)
    return cv


# ==========================================================================
#  BUILDINGS
# ==========================================================================
def _stilts(cv, x0, x1, y, n=4, col="#6d4c30"):
    for i in range(n):
        sx = x0 + int((x1 - x0) * (i + 0.5) / n)
        cv.rect(sx - 1, y, sx + 1, y + 7, col)


def rumah_gadang(seed=20):
    """Rumah Gadang inspired: long stilt house, upswept horn roof (gonjong)."""
    w, h = 176, 128
    cv = Canvas(w, h)
    body_y0, body_y1 = 62, 96
    wall = "#d8b483"
    wall_d = "#b8945f"
    wood = "#7a4c34"
    roof = "#3a2a2e"
    roof_hi = "#54403f"
    # plinth / posts
    _stilts(cv, 14, w - 14, 96, n=7, col="#5e4229")
    cv.rect(10, 96, w - 10, 100, "#6d4c30")
    # long facade
    cv.rect(12, body_y0, w - 13, body_y1, wall)
    cv.rect(12, body_y0, w - 13, body_y0 + 3, wall_d)
    cv.rect(12, body_y1 - 6, w - 13, body_y1, wall_d)
    # carved panels (batik-ish motif rows)
    for i in range(11):
        px0 = 20 + i * 13
        cv.rect(px0, body_y0 + 8, px0 + 9, body_y1 - 8, "#c9a370")
        cv.rect(px0 + 2, body_y0 + 11, px0 + 7, body_y1 - 11, "#8a5a3a")
        for k in range(3):
            cv.px(px0 + 4, body_y0 + 14 + k * 6, "#e0c08c")
            cv.px(px0 + 3, body_y0 + 15 + k * 6, "#e0c08c")
            cv.px(px0 + 5, body_y0 + 15 + k * 6, "#e0c08c")
    # central door + windows
    cv.rect(80, body_y0 + 6, 96, body_y1, "#5e3624")
    cv.rect(83, body_y0 + 10, 93, body_y1 - 4, "#7a4c34")
    cv.rect(86, body_y0 + 16, 87, body_y1 - 6, "#c9a06a")
    for wx in (34, 58, 118, 142):
        cv.rect(wx, body_y0 + 12, wx + 10, body_y0 + 30, "#4a2c22")
        cv.rect(wx + 2, body_y0 + 14, wx + 8, body_y0 + 28, "#8fb0c0")
        cv.rect(wx + 4, body_y0 + 14, wx + 6, body_y0 + 28, "#b8d4e0")
    # roof: upswept "gonjong" horns (two-sided gable with rising ends)
    top_y = 20
    pts = [
        (6, 66), (16, 54), (34, 44), (52, 38), (74, 34), (88, 22),
        (100, 34), (122, 38), (140, 44), (160, 54), (170, 66), (168, 70),
        (150, 60), (128, 52), (108, 46), (88, 34), (68, 46), (48, 52), (26, 60), (8, 70),
    ]
    cv.poly(pts, roof)
    # roof ridge shading + thatch lines
    for i in range(24):
        t = i / 23
        x0 = int(10 + t * 156)
        y0 = int(66 - 40 * (1 - abs(t - 0.5) * 1.7) if 0.15 < t < 0.85 else 66 - 14 * (1 - abs(t - 0.5)))
        cv.px(x0, max(22, y0), roof_hi)
    cv.line([(8, 68), (86, 21)], roof_hi, 2)
    cv.line([(168, 68), (90, 21)], roof_hi, 2)
    cv.line([(88, 22), (88, 34)], "#2a1e22", 2)
    # buffalo-horn tips
    for hx, dirx in ((4, -1), (172, 1)):
        cv.line([(hx, 66), (hx + 5 * dirx, 58), (hx + 9 * dirx, 50)], "#54403f", 3)
        cv.line([(hx + 2 * dirx, 60), (hx + 10 * dirx, 46)], "#3a2a2e", 2)
    # front steps
    cv.rect(74, 100, 102, 106, "#6d4c30")
    cv.rect(78, 106, 98, 112, "#5e4229")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def joglo_house(seed=21, scale=1.0):
    """Joglo: two-tier pyramidal tile roof on pillars, wide overhang."""
    w, h = 132, 122
    cv = Canvas(w, h)
    body_y0, body_y1 = 74, 104
    # pillars
    for px in (16, 44, 88, 116):
        if px < w:
            cv.rect(px, 68, px + 5, body_y1, "#6b4630")
            cv.rect(px, 68, px, body_y1, "#83573a")
    cv.rect(10, 100, w - 11, body_y1, "#a88354")     # base platform
    cv.rect(14, body_y0, w - 15, body_y1 - 4, "#e0c79a")  # wall
    cv.rect(14, body_y0, w - 15, body_y0 + 3, "#c9ab7c")
    # wall panels
    for i in range(6):
        x = 20 + i * 16
        cv.rect(x, body_y0 + 20, x + 12, body_y1 - 8, "#d3b587")
        cv.rect(x + 3, body_y0 + 23, x + 9, body_y1 - 11, "#f0dcae")
    # door
    cv.rect(w // 2 - 12, body_y0 + 6, w // 2 + 12, body_y1, "#5e3624")
    cv.rect(w // 2 - 9, body_y0 + 10, w // 2 + 9, body_y1 - 3, "#8a5a34")
    cv.rect(w // 2 - 1, body_y0 + 12, w // 2 + 1, body_y1 - 5, "#c9a06a")
    for wx in (26, 100):
        cv.rect(wx, body_y0 + 24, wx + 12, body_y0 + 40, "#4a2c22")
        cv.rect(wx + 2, body_y0 + 26, wx + 10, body_y0 + 38, "#96b8c8")
    # roof tier 1 (wide)
    cv.poly([(2, 76), (w - 3, 76), (w - 26, 50), (26, 50)], "#9c4436")
    for y in range(50, 77, 3):
        cv.line([(int(w * 0.06) + (y - 50) * 0, y), (int(w * 0.94), y)], "#8a3a30", 1)
    cv.poly([(2, 76), (w - 3, 76), (w - 3, 72), (2, 72)], "#7d3226")
    cv.poly([(2, 76), (w - 3, 76), (w - 3, 79), (2, 79)], "#b85a44")
    # roof tier 2 (pyramid top)
    cv.poly([(30, 52), (w - 31, 52), (w // 2 + 12, 26), (w // 2 - 12, 26)], "#a84c3a")
    cv.poly([(w // 2 - 12, 26), (w // 2 + 12, 26), (w // 2 + 8, 18), (w // 2 - 8, 18)], "#8a3a30")
    cv.line([(w // 2, 18), (w // 2, 52)], "#7d3226", 1)
    for i in range(5):
        x = 34 + i * 14
        cv.line([(x, 52), (w // 2 - 6 + i * 3, 28)], "#c2664a", 1)
    # ridge ornament
    cv.rect(w // 2 - 2, 12, w // 2 + 1, 18, "#d8b060")
    cv.ellipse(w // 2 - 3, 8, w // 2 + 2, 14, "#e8c878")
    # front steps
    cv.rect(w // 2 - 14, 104, w // 2 + 14, 110, "#a88354")
    cv.rect(w // 2 - 10, 110, w // 2 + 10, 116, "#8f6f46")
    cv.outline("#2b2026", alpha_test=70)
    if scale != 1.0:
        cv = scale_canvas(cv, scale)
    return cv


def rumah_panjang(seed=22):
    """Betang / longhouse: very long stilt house with gable roof and totems."""
    w, h = 224, 124
    cv = Canvas(w, h)
    body_y0, body_y1 = 62, 96
    _stilts(cv, 12, w - 12, 96, n=9, col="#5a4028")
    cv.rect(8, 94, w - 8, 100, "#6b4a2e")
    # body
    cv.rect(10, body_y0, w - 11, body_y1, "#b07a48")
    cv.rect(10, body_y0, w - 11, body_y0 + 4, "#c68f56")
    cv.rect(10, body_y1 - 8, w - 11, body_y1, "#8f6238")
    # carved / painted band
    cv.rect(10, body_y0 + 6, w - 11, body_y0 + 14, "#3c2c30")
    for i in range(17):
        x = 14 + i * 12
        cv.px(x + 3, body_y0 + 10, "#e8c060")
        cv.px(x + 4, body_y0 + 9, "#e8c060")
        cv.px(x + 5, body_y0 + 10, "#e8c060")
        cv.px(x + 4, body_y0 + 11, "#c05040")
    # doors along the long side
    for i in range(5):
        dx = 22 + i * 44
        cv.rect(dx, body_y0 + 16, dx + 18, body_y1, "#5e3624")
        cv.rect(dx + 2, body_y0 + 19, dx + 16, body_y1 - 2, "#7d4f2e")
        cv.rect(dx + 8, body_y0 + 20, dx + 10, body_y1 - 4, "#c9a06a")
        # small windows either side
        cv.rect(dx - 10, body_y0 + 22, dx - 4, body_y0 + 34, "#43281e")
        cv.rect(dx + 24, body_y0 + 22, dx + 30, body_y0 + 34, "#43281e")
    # gable roof
    cv.poly([(-2, 66), (w + 2, 66), (w - 34, 26), (34, 26)], "#4a3a30")
    cv.poly([(-2, 66), (w + 2, 66), (w + 2, 61), (-2, 61)], "#382c24")
    cv.poly([(-2, 66), (w + 2, 66), (w + 2, 70), (-2, 70)], "#5e4a3c")
    for x in range(10, w, 12):
        cv.line([(x, 65), (int(x * 0.78) + 30, 28)], "#5e4a3c", 1)
    cv.line([(0, 66), (w, 66)], "#2f2620", 2)
    # roof ridge with carved finial at both ends
    cv.rect(28, 24, w - 28, 28, "#6b5240")
    for fx, dirx in ((26, -1), (w - 27, 1)):
        cv.line([(fx, 26), (fx + 8 * dirx, 18), (fx + 14 * dirx, 12)], "#8a6440", 3)
        cv.line([(fx + 2 * dirx, 22), (fx + 12 * dirx, 8)], "#a87f52", 2)
    # entrance ladder
    cv.rect(100, 100, 122, 120, "#7a5a3a")
    for y in range(102, 120, 5):
        cv.rect(102, y, 120, y + 1, "#966f45")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def tongkonan(seed=23):
    """Tongkonan: stilt house with the iconic sweeping saddle-shaped roof."""
    w, h = 150, 134
    cv = Canvas(w, h)
    body_y0, body_y1 = 74, 104
    # stilts (tall, on posts)
    for px in (24, 50, 78, 106, 128):
        cv.rect(px, 96, px + 5, 120, "#6b4a2e")
        cv.rect(px, 96, px, 120, "#835a38")
    cv.rect(14, 100, w - 15, 106, "#8f6238")
    # facade - black/red/white carved panels (buffalo + rooster motifs, abstracted)
    cv.rect(16, body_y0, w - 17, body_y1, "#3a2c28")
    cv.rect(16, body_y0, w - 17, body_y0 + 4, "#5a443a")
    for i in range(5):
        x = 22 + i * 22
        cv.rect(x, body_y0 + 6, x + 16, body_y1 - 6, "#4a362e")
        cv.rect(x + 1, body_y0 + 7, x + 15, body_y0 + 9, "#e8dcc0")
        cv.rect(x + 1, body_y1 - 9, x + 15, body_y1 - 7, "#c05040")
        # abstract geometric motif (game-art abstraction, not a copy of any specific carving)
        for k in range(3):
            cv.px(x + 4 + k * 4, body_y0 + 16, "#e8c060")
            cv.px(x + 5 + k * 4, body_y0 + 17, "#c05040")
            cv.px(x + 6 + k * 4, body_y0 + 16, "#e8c060")
    # door
    cv.rect(w // 2 - 9, body_y0 + 10, w // 2 + 9, body_y1, "#1f1614")
    cv.rect(w // 2 - 6, body_y0 + 13, w // 2 + 6, body_y1 - 3, "#33241f")
    # saddle roof: front rises high, rear slopes down (classic boat shape)
    pts = [
        (4, 76), (10, 62), (22, 44), (40, 28), (60, 18), (74, 14),
        (86, 20), (96, 34), (110, 48), (128, 58), (146, 66), (148, 74),
        (140, 78), (124, 70), (106, 60), (92, 46), (80, 34), (70, 26),
        (56, 32), (40, 44), (26, 58), (14, 74),
    ]
    cv.poly(pts, "#3f2f2a")
    cv.line([(8, 72), (70, 15)], "#5d463a", 2)
    cv.line([(146, 70), (84, 19)], "#5d463a", 2)
    cv.line([(6, 74), (146, 72)], "#2a1f1c", 2)
    for i in range(7):  # bamboo roof texture
        t = i / 6
        cv.line([(10 + int(t * 130), 74 - int(46 * (1 - t) if t < 0.5 else 20 * t))], "#00000000", 0)
    # upward horn tip
    cv.line([(6, 74), (2, 56), (6, 44)], "#5d463a", 3)
    cv.line([(148, 72), (150, 60), (146, 52)], "#5d463a", 2)
    # front gable panel with geometric art
    cv.poly([(30, 70), (120, 70), (86, 26), (64, 26)], "#2f2420")
    for i in range(4):
        cv.line([(44 + i * 4, 68), (68 + i * 3, 30)], "#c05040", 1)
        cv.line([(106 - i * 4, 68), (82 - i * 3, 30)], "#e8c060", 1)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def honai(seed=24, big=False):
    """Honai-style round thatched hut with conical roof (Papua highlands)."""
    w, h = (104, 108) if big else (78, 84)
    cv = Canvas(w, h)
    cx = w // 2
    # body (cylindrical, woven/plastered)
    bw = int(w * 0.62)
    body_top = int(h * 0.5)
    cv.ellipse(cx - bw // 2, body_top - 12, cx + bw // 2, h - 4, "#b8a06a")
    cv.rect(cx - bw // 2, body_top - 6, cx + bw // 2, h - 10, "#c4ab74")
    if big:
        cv.ellipse(cx - bw // 2, h - 22, cx + bw // 2, h - 2, "#b09864")
    # texture: woven fibres
    for y in range(body_top - 6, h - 10, 4):
        for x in range(cx - bw // 2 + 2, cx + bw // 2 - 2, 3):
            cv.px(x + (y // 4 % 2), y, "#a08a5a")
    # conical thatch roof (stacked rings)
    roof_h = int(h * 0.52)
    for i in range(roof_h):
        t = i / roof_h
        half = int((bw // 2 + 3) * (1 - t) + 2)
        y = body_top - 6 - i
        col = "#7f6a3c" if i % 5 else "#6b5830"
        if i % 7 == 0:
            col = "#8f7a44"
        cv.rect(cx - half, y, cx + half, y, col)
    # ridge cap
    cv.ellipse(cx - 5, body_top - 6 - roof_h - 2, cx + 5, body_top - 6 - roof_h + 4, "#5d4c28")
    cv.rect(cx - 1, body_top - 6 - roof_h - 8, cx + 1, body_top - 6 - roof_h, "#6b5830")
    # small door
    cv.rect(cx - 7, h - 26, cx + 7, h - 5, "#3c2c24")
    cv.rect(cx - 5, h - 23, cx + 5, h - 5, "#54413a")
    if big:
        cv.rect(cx - 2, h - 24, cx + 2, h - 6, "#6b5240")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def hut_papua_coastal(seed=25):
    """Stilt hut with palm roof (Papua coastal / lowland village)."""
    w, h = 96, 88
    cv = Canvas(w, h)
    for px in (18, 44, 70):
        cv.rect(px, 58, px + 4, 80, "#6d4c30")
    cv.rect(12, 62, w - 13, 68, "#966f45")
    cv.rect(14, 40, w - 15, 62, "#b07a48")
    cv.rect(14, 40, w - 15, 44, "#c68f56")
    for i in range(4):
        cv.rect(20 + i * 18, 46, 32 + i * 18, 60, "#a06c3c")
    cv.rect(w // 2 - 8, 44, w // 2 + 8, 62, "#4a3020")
    # palm-leaf roof
    cv.poly([(4, 44), (w - 5, 44), (w - 22, 14), (22, 14)], "#8a7a3c")
    cv.poly([(4, 44), (w - 5, 44), (w - 5, 39), (4, 39)], "#6f6230")
    for i in range(12):
        x = 10 + i * 7
        cv.line([(x, 43), (14 + int(x * 0.7), 15)], "#9c8a48", 1)
    cv.rect(20, 12, w - 21, 16, "#7a6a34")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def lumbung(seed=26):
    """Rice barn on stilts with a curved roof (common across the archipelago)."""
    w, h = 84, 96
    cv = Canvas(w, h)
    for px in (20, 40, 60):
        cv.rect(px, 62, px + 4, 84, "#6d4c30")
    cv.rect(14, 58, w - 15, 64, "#966f45")
    cv.rect(18, 32, w - 19, 58, "#c9a06a")
    cv.rect(18, 32, w - 19, 36, "#dcb47e")
    for i in range(3):
        cv.rect(24 + i * 14, 40, 34 + i * 14, 56, "#b08a54")
    cv.rect(w // 2 - 6, 36, w // 2 + 6, 58, "#5e3624")
    # curved roof
    cv.poly([(6, 34), (w - 7, 34), (w - 24, 12), (24, 12)], "#8a5a3a")
    cv.poly([(6, 34), (w - 7, 34), (w - 7, 30), (6, 30)], "#6f4630")
    for i in range(8):
        cv.line([(10 + i * 9, 33), (26 + i * 4, 13)], "#a2734a", 1)
    cv.line([(8, 32), (20, 8)], "#a2734a", 2)
    cv.line([(w - 9, 32), (w - 22, 8)], "#a2734a", 2)
    cv.rect(22, 10, w - 23, 14, "#7a5a3a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def warung(seed=27, roof_col="#8a3a30"):
    """Small food stall / shop with awning and wares."""
    w, h = 76, 68
    cv = Canvas(w, h)
    cv.rect(6, 40, w - 7, 62, "#b08a54")
    cv.rect(6, 40, w - 7, 44, "#c69c62")
    cv.rect(10, 48, w - 11, 60, "#8f6a3c")
    # counter with goods
    for i in range(5):
        x = 12 + i * 10
        col = ["#d8634a", "#e0b04a", "#7aa84a", "#c06a9a", "#e0d060"][i]
        cv.rect(x, 44, x + 6, 52, col)
        cv.rect(x, 44, x + 6, 45, shade(col, 0.25))
    # awning roof
    cv.poly([(0, 40), (w - 1, 40), (w - 10, 18), (9, 18)], roof_col)
    cv.poly([(0, 40), (w - 1, 40), (w - 1, 36), (0, 36)], shade(roof_col, -0.25))
    for i in range(6):
        x = 4 + i * 12
        cv.line([(x, 39), (12 + int(x * 0.8), 19)], shade(roof_col, 0.25), 1)
    cv.rect(9, 16, w - 10, 20, "#5e3624")
    # hanging lantern + sign
    cv.rect(6, 46, 7, 58, "#5e3624")
    cv.ellipse(2, 52, 10, 60, "#e8c060")
    cv.rect(52, 24, 70, 32, "#e8dcc0")
    cv.rect(53, 25, 69, 31, "#c9a06a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def food_stall(seed=28):
    """Open-air food stall with stools and steaming pots."""
    w, h = 88, 60
    cv = Canvas(w, h)
    # cart/stall body
    cv.rect(14, 26, 74, 48, "#a8763e")
    cv.rect(14, 26, 74, 30, "#c08d4c")
    cv.rect(14, 44, 74, 48, "#8a5f30")
    # pots + steam
    for i, x in enumerate((22, 38, 54)):
        cv.ellipse(x, 20, x + 14, 30, "#4a4a52")
        cv.ellipse(x + 1, 19, x + 13, 27, "#5c5c66")
        cv.ellipse(x + 2, 18, x + 12, 22, "#3c3c44")
        for k in range(3):
            cv.px(x + 5 + k * 2, 14 - k, "#d8d8e0")
            cv.px(x + 6 + k * 2, 12 - k, "#e8e8f0")
    # canopy posts + cloth
    cv.rect(12, 6, 15, 30, "#6d4c30")
    cv.rect(73, 6, 76, 30, "#6d4c30")
    cv.rect(10, 4, 78, 9, "#c05040")
    cv.rect(10, 4, 78, 6, "#d8664a")
    # stools
    for x in (0, 80):
        cv.rect(x + 2, 40, x + 8, 48, "#8f6238")
        cv.rect(x + 1, 38, x + 9, 41, "#b08a54")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def workshop(seed=29, accent="#7a4c34"):
    """Craft workshop with tools, open front."""
    w, h = 92, 76
    cv = Canvas(w, h)
    cv.rect(6, 34, w - 7, 68, "#c9a06a")
    cv.rect(6, 34, w - 7, 38, "#dcb47e")
    cv.rect(10, 42, w - 11, 66, accent)
    cv.rect(12, 44, w - 13, 64, "#5e4028")
    # workbench + tools
    cv.rect(16, 50, 60, 56, "#8f6238")
    for x, col in ((20, "#9c9c9c"), (30, "#b0b0b0"), (40, "#8a8a8a")):
        cv.rect(x, 44, x + 3, 50, col)
        cv.rect(x - 1, 42, x + 4, 44, "#6d4c30")
    # roof
    cv.poly([(0, 36), (w - 1, 36), (w - 12, 12), (11, 12)], "#6d4c30")
    cv.poly([(0, 36), (w - 1, 36), (w - 1, 32), (0, 32)], "#523a26")
    for i in range(7):
        x = 4 + i * 12
        cv.line([(x, 35), (14 + int(x * 0.8), 13)], "#8a6440", 1)
    # hanging sign + finished craft on the sill
    cv.rect(30, 18, 62, 28, "#e8dcc0")
    cv.rect(31, 19, 61, 27, "#d8c9a0")
    cv.rect(42, 21, 50, 25, "#8a5a3a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def cultural_center(seed=30, roof="#8a5a3a", banner="#c05040"):
    """Village cultural hall / mini museum with banner and entrance."""
    w, h = 128, 100
    cv = Canvas(w, h)
    cv.rect(8, 44, w - 9, 92, "#dcb47e")
    cv.rect(8, 44, w - 9, 49, "#c9a06a")
    cv.rect(8, 86, w - 9, 92, "#b08a54")
    # windows
    for x in (20, 44, 84, 108):
        cv.rect(x, 56, x + 14, 72, "#4a2c22")
        cv.rect(x + 2, 58, x + 12, 70, "#9cc0cc")
        cv.rect(x + 6, 58, x + 8, 70, "#3c2c24")
    # columns
    for x in (10, 116):
        cv.rect(x, 46, x + 5, 92, "#c9a06a")
        cv.rect(x, 46, x + 1, 92, "#e0c79a")
    # double door
    cv.rect(w // 2 - 18, 52, w // 2 + 18, 92, "#5e3624")
    cv.rect(w // 2 - 15, 55, w // 2 - 2, 92, "#8a5a34")
    cv.rect(w // 2 + 2, 55, w // 2 + 15, 92, "#7d4f2e")
    cv.rect(w // 2 - 1, 55, w // 2 + 1, 92, "#c9a06a")
    # carved top band
    cv.rect(8, 44, w - 9, 52, "#8a5a3a")
    for i in range(11):
        x = 14 + i * 10
        cv.px(x + 3, 48, "#e8c060")
        cv.px(x + 4, 47, "#e8c060")
        cv.px(x + 5, 48, "#e8c060")
    # hipped roof
    cv.poly([(0, 46), (w - 1, 46), (w - 22, 16), (21, 16)], roof)
    cv.poly([(0, 46), (w - 1, 46), (w - 1, 41), (0, 41)], shade(roof, -0.25))
    cv.poly([(21, 16), (w - 22, 16), (w // 2 + 8, 6), (w // 2 - 8, 6)], shade(roof, 0.12))
    for i in range(10):
        x = 6 + i * 12
        cv.line([(x, 45), (24 + int(x * 0.78), 17)], shade(roof, 0.2), 1)
    # banners
    for x in (16, 104):
        cv.rect(x, 48, x + 8, 76, banner)
        cv.rect(x + 1, 50, x + 7, 74, shade(banner, 0.18))
        cv.rect(x - 1, 46, x + 9, 49, "#e8c060")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def candi(seed=31):
    """Temple-inspired stone structure (stylised, not a copy of any specific temple)."""
    w, h = 118, 140
    cv = Canvas(w, h)
    stone = "#8e8a7e"
    stone_d = "#75716a"
    stone_l = "#a8a496"
    # stepped base
    for i, (inset, col) in enumerate([(0, stone_d), (6, stone), (12, stone_l), (18, stone)]):
        cv.rect(4 + inset, 108 + i * 8, w - 5 - inset, 116 + i * 8, col)
    cv.rect(4, 116, w - 5, 120, "#6a6660")
    # body
    cv.rect(26, 62, w - 27, 110, stone)
    cv.rect(26, 62, w - 27, 66, stone_l)
    cv.rect(26, 104, w - 27, 110, stone_d)
    for x in range(30, w - 30, 8):  # relief bands
        cv.rect(x, 70, x + 5, 78, "#c8b48a")
        cv.rect(x, 84, x + 5, 92, "#c8b48a")
    # doorway with kala-ish stylised head above
    cv.rect(w // 2 - 12, 74, w // 2 + 12, 110, "#4a4640")
    cv.rect(w // 2 - 9, 78, w // 2 + 9, 110, "#332f2c")
    cv.poly([(w // 2 - 16, 74), (w // 2 + 16, 74), (w // 2 + 10, 64), (w // 2 - 10, 64)], "#c8b48a")
    cv.rect(w // 2 - 6, 68, w // 2 + 6, 71, "#5e5a52")
    # roof: tiered pyramid
    tiers = [(40, 56), (34, 46), (28, 36), (20, 26), (12, 18)]
    for i, (half, y) in enumerate(tiers):
        cv.rect(w // 2 - half, y, w // 2 + half, y + 9, stone_l if i % 2 == 0 else stone)
        cv.rect(w // 2 - half, y + 8, w // 2 + half, y + 9, stone_d)
        for x in range(w // 2 - half + 3, w // 2 + half - 2, 6):
            cv.rect(x, y + 2, x + 3, y + 6, stone_d)
    cv.rect(w // 2 - 6, 10, w // 2 + 6, 18, stone_l)
    cv.poly([(w // 2 - 5, 10), (w // 2 + 5, 10), (w // 2, 2)], "#b8b4a4")
    # staircase
    for i in range(5):
        cv.rect(w // 2 - 14 + i, 116 + i * 4, w // 2 + 14 - i, 120 + i * 4, "#b0aa9a" if i % 2 else stone)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def gate_keraton(seed=32):
    """Split gate (candi bentar inspired) with steps."""
    w, h = 126, 118
    cv = Canvas(w, h)
    stone = "#a89c84"
    stone_d = "#8a7f6a"
    for side in (0, 1):
        half = []
        base_x = 4 if side == 0 else w - 5
        dirx = 1 if side == 0 else -1
        for i in range(7):
            bw = 20 - i * 2
            y = 112 - i * 9
            x0 = base_x
            x1 = base_x + dirx * bw
            half.append((min(x0, x1), y, max(x0, x1), y + 8))
        for x0, y, x1, y1 in half:
            cv.rect(x0, y, x1, y1, stone if (y // 9) % 2 else stone_d)
        # top ornament
        tip_x = base_x + dirx * 8
        cv.poly([(tip_x - 3, 40), (tip_x + 3, 40), (tip_x, 30)], "#c8b48a")
        cv.rect(tip_x - 2, 40, tip_x + 2, 48, stone)
    for i in range(6):
        cv.rect(52 + i * 2, 104 + i * 3, 74 - i * 2, 107 + i * 3, "#b8ae96" if i % 2 else "#9a8f78")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def clock_tower(seed=33):
    """Jam Gadang inspired clock tower (landmark, Sumatran highlands)."""
    w, h = 74, 152
    cv = Canvas(w, h)
    cv.rect(10, 120, w - 11, 148, "#d8ccb0")
    cv.rect(6, 140, w - 7, 150, "#b8ac90")
    cv.rect(16, 62, w - 17, 122, "#e8dcc0")
    cv.rect(16, 62, w - 17, 66, "#f4ecd8")
    # windows
    for y in (72, 86, 100):
        cv.rect(w // 2 - 8, y, w // 2 + 8, y + 10, "#6a6058")
        cv.rect(w // 2 - 6, y + 1, w // 2 + 6, y + 9, "#a8c0cc")
    # clock faces on two sides
    cv.ellipse(w // 2 - 11, 104, w // 2 + 11, 124, "#f4ecd8")
    cv.ellipse(w // 2 - 9, 106, w // 2 + 9, 122, "#5c5048")
    cv.line([(w // 2, 114), (w // 2, 109)], "#f0e8d8", 2)
    cv.line([(w // 2, 114), (w // 2 + 5, 114)], "#f0e8d8", 2)
    cv.px(w // 2, 114, "#d8c060")
    # tiered roof with upswept tips
    cv.poly([(6, 62), (w - 7, 62), (w - 22, 34), (21, 34)], "#8a3a30")
    cv.poly([(6, 62), (w - 7, 62), (w - 7, 57), (6, 57)], "#6f2c26")
    cv.poly([(18, 36), (w - 19, 36), (w // 2 + 6, 18), (w // 2 - 6, 18)], "#9c4436")
    cv.poly([(w // 2 - 6, 18), (w // 2 + 6, 18), (w // 2, 6)], "#8a3a30")
    cv.line([(4, 62), (0, 52)], "#6f2c26", 3)
    cv.line([(w - 5, 62), (w - 1, 52)], "#6f2c26", 3)
    for i in range(8):
        cv.line([(8 + i * 9, 61), (24 + i * 4, 35)], "#b8564a", 1)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def lookout_tower(seed=34, wood="#8a6440"):
    """Wooden lookout / signal tower (coastal + highland landmarks)."""
    w, h = 92, 132
    cv = Canvas(w, h)
    # legs
    cv.line([(22, 126), (32, 46)], wood, 4)
    cv.line([(70, 126), (60, 46)], wood, 4)
    cv.line([(30, 128), (34, 50)], shade(wood, -0.2), 3)
    cv.line([(64, 128), (58, 50)], shade(wood, -0.2), 3)
    for y in range(56, 122, 16):  # braces
        cv.line([(26 + (122 - y) // 8, y), (66 - (122 - y) // 8, y)], shade(wood, -0.15), 2)
    cv.line([(30, 96), (64, 76)], shade(wood, -0.15), 2)
    cv.line([(62, 96), (30, 76)], shade(wood, -0.15), 2)
    # platform
    cv.rect(20, 40, 74, 48, shade(wood, 0.15))
    cv.rect(20, 46, 74, 49, shade(wood, -0.25))
    # railing
    for x in (22, 34, 46, 58, 70):
        cv.rect(x, 28, x + 2, 42, shade(wood, 0.05))
    cv.rect(20, 26, 74, 29, shade(wood, 0.2))
    # roof
    cv.poly([(12, 30), (82, 30), (66, 8), (28, 8)], "#6f5a34")
    cv.poly([(12, 30), (82, 30), (82, 26), (12, 26)], "#584526")
    cv.rect(28, 6, 66, 10, "#7a6438")
    # ladder
    cv.rect(38, 46, 40, 126, "#9c7448")
    cv.rect(52, 46, 54, 126, "#9c7448")
    for y in range(50, 126, 8):
        cv.rect(38, y, 54, y + 1, "#b08a54")
    cv.outline("#2b2026", alpha_test=70)
    return cv


# ==========================================================================
#  PROPS
# ==========================================================================
def fence(seed=35, w=64, h=30, col="#a8823f"):
    cv = Canvas(w, h)
    cv.rect(2, 10, w - 3, 13, col)
    cv.rect(2, 20, w - 3, 23, col)
    cv.rect(2, 10, w - 3, 11, shade(col, 0.22))
    for x in range(3, w - 3, 12):
        cv.rect(x, 4, x + 3, 28, shade(col, -0.12))
        cv.rect(x, 4, x, 28, shade(col, 0.1))
        cv.poly([(x, 4), (x + 3, 4), (x + 1, 1)], shade(col, -0.2))
    cv.outline("#2b2026", alpha_test=70)
    return cv


def signpost(seed=36, text_hint="village"):
    cv = Canvas(34, 46)
    cv.rect(15, 20, 19, 44, "#7a5a3a")
    cv.rect(15, 20, 15, 44, "#966f45")
    cv.rect(3, 6, 32, 22, "#c9a06a")
    cv.rect(3, 6, 32, 9, "#dcb47e")
    cv.rect(4, 7, 31, 21, "#c9a06a", fill=False)
    for i in range(3):        # abstract "writing" marks
        cv.rect(7 + i * 8, 12, 11 + i * 8, 13, "#7a5a3a")
        cv.rect(7 + i * 8, 15, 12 + i * 8, 16, "#7a5a3a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def lantern(seed=37):
    cv = Canvas(26, 40)
    cv.rect(11, 22, 14, 38, "#6d4c30")
    cv.rect(8, 6, 18, 24, "#e8c060")
    cv.rect(9, 7, 17, 23, "#f4dc94")
    cv.rect(8, 6, 18, 8, "#b8934a")
    cv.rect(8, 22, 18, 24, "#b8934a")
    cv.rect(6, 2, 20, 7, "#8a5a3a")
    cv.px(13, 15, "#fff0c0")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def brazier(seed=38):
    cv = Canvas(28, 34)
    cv.rect(4, 16, 24, 24, "#6d5a4a")
    cv.rect(4, 16, 24, 18, "#8a7460")
    cv.rect(6, 24, 9, 32, "#4a3c32")
    cv.rect(19, 24, 22, 32, "#4a3c32")
    for i in range(6):
        cv.poly([(9 + i * 2, 16), (12 + i * 2, 6 + (i % 3) * 3), (15 + i * 2, 16)],
                ["#e8722c", "#f4a03c", "#f8d060"][i % 3])
    cv.outline("#2b2026", alpha_test=70)
    return cv


def well(seed=39):
    cv = Canvas(46, 50)
    cv.ellipse(6, 24, 40, 44, "#8a8a86")
    cv.ellipse(10, 26, 36, 40, "#5a5a58")
    cv.ellipse(12, 28, 34, 38, "#3c4a58")
    cv.rect(8, 22, 38, 28, "#9c9c96")
    cv.rect(6, 22, 12, 30, "#a8a8a0")
    cv.rect(34, 22, 40, 30, "#a8a8a0")
    cv.rect(10, 6, 13, 24, "#7a5a3a")
    cv.rect(33, 6, 36, 24, "#7a5a3a")
    cv.poly([(4, 10), (42, 10), (36, 2), (10, 2)], "#8a5a3a")
    cv.rect(20, 10, 26, 16, "#6d4c30")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def bridge_plank(seed=40):
    cv = Canvas(64, 38)
    cv.rect(0, 12, 63, 30, "#a8763e")
    for x in range(0, 64, 8):
        cv.rect(x, 12, x + 6, 30, "#b8834f")
        cv.rect(x + 7, 12, x + 7, 30, "#7d5432")
    cv.rect(0, 12, 63, 14, "#c99a5c")
    cv.rect(0, 28, 63, 30, "#6d4a2c")
    cv.rect(-1, 8, 3, 32, "#8a6440")
    cv.rect(61, 8, 65, 32, "#8a6440")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def canoe(seed=41):
    cv = Canvas(64, 26)
    cv.poly([(2, 12), (62, 12), (52, 22), (12, 22)], "#8a6440")
    cv.poly([(4, 13), (60, 13), (52, 18), (12, 18)], "#a8763e")
    cv.rect(6, 10, 58, 12, "#6d4c30")
    cv.line([(8, 12), (14, 4), (20, 12)], "#9c7448", 2)
    cv.rect(30, 6, 34, 12, "#7a5a3a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def dock(seed=42):
    cv = Canvas(96, 46)
    cv.rect(0, 14, 95, 40, "#9c6f42")
    for x in range(0, 96, 10):
        cv.rect(x, 14, x + 8, 40, "#ab7c4c")
        cv.rect(x + 9, 14, x + 9, 40, "#7a5432")
    cv.rect(0, 14, 95, 16, "#c09460")
    for x in (8, 40, 72):
        cv.rect(x, 40, x + 4, 45, "#6d4a2c")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def pot_plant(seed=43):
    cv = Canvas(24, 30)
    cv.poly([(6, 18), (18, 18), (16, 28), (8, 28)], "#b8694a")
    cv.rect(5, 16, 19, 20, "#c9785a")
    cv.rect(5, 16, 19, 17, "#d98a68")
    for i in range(5):
        cv.line([(12, 16), (6 + i * 3, 4 + (i % 2) * 4)], "#4f8a3c", 2)
        cv.px(6 + i * 3, 4 + (i % 2) * 4, "#68a850")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def basket(seed=44):
    cv = Canvas(26, 24)
    cv.poly([(4, 10), (22, 10), (19, 22), (7, 22)], "#c9a06a")
    for y in range(11, 22, 3):
        cv.line([(5, y), (21, y)], "#a87f52", 1)
    cv.rect(4, 8, 22, 11, "#dcb47e")
    cv.line([(8, 8), (12, 2), (18, 8)], "#a87f52", 2)
    cv.poly([(9, 2), (13, 2), (12, 6), (10, 6)], "#6f9c52")
    cv.poly([(12, 3), (17, 3), (15, 7), (12, 6)], "#8ab060")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def drying_rack(seed=45, col="#c05040"):
    """Fish / crop drying rack with hanging produce."""
    cv = Canvas(58, 44)
    cv.rect(6, 8, 9, 42, "#8a6440")
    cv.rect(48, 8, 51, 42, "#8a6440")
    cv.rect(4, 6, 53, 10, "#a8763e")
    for i in range(5):
        x = 10 + i * 9
        cv.rect(x, 10, x + 6, 22, col)
        cv.rect(x + 1, 11, x + 5, 21, shade(col, 0.18))
        cv.rect(x + 2, 8, x + 4, 11, "#8a6440")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def gamelan_set(seed=46):
    """Gamelan-inspired instrument rack (stylised: gongs + metallophone)."""
    cv = Canvas(78, 54)
    # frame
    cv.rect(4, 14, 74, 18, "#7a3a2a")
    cv.rect(4, 40, 74, 48, "#7a3a2a")
    cv.rect(4, 14, 8, 48, "#8f4a34")
    cv.rect(70, 14, 74, 48, "#8f4a34")
    # hanging gongs
    for i, x in enumerate((16, 32, 48, 62)):
        r = 8 - i
        cv.ellipse(x - r, 18 - r // 2, x + r, 18 + r + r // 2, "#c8a24a")
        cv.ellipse(x - r + 2, 20 - r // 2, x + r - 2, 16 + r + r // 2, "#e0bc62")
        cv.ellipse(x - 2, 22, x + 2, 26, "#8a6a2a")
    # metallophone bars
    for i in range(6):
        x = 8 + i * 11
        cv.rect(x, 30, x + 8, 34, "#d8b060")
        cv.rect(x, 30, x + 8, 31, "#f0d08a")
        cv.rect(x + 3, 34, x + 5, 40, "#8a6a2a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def angklung_stand(seed=47):
    """Angklung-inspired bamboo instrument stand."""
    cv = Canvas(60, 62)
    cv.rect(6, 12, 10, 58, "#8a6440")
    cv.rect(50, 12, 54, 58, "#8a6440")
    for i in range(3):
        x = 14 + i * 13
        cv.rect(x, 14, x + 10, 18, "#7a5a3a")
        for k in range(3):     # bamboo tubes of decreasing length
            cv.rect(x + 1 + k * 3, 18, x + 3 + k * 3, 18 + 26 - k * 6, "#c8b062")
            cv.rect(x + 1 + k * 3, 18, x + 1 + k * 3, 18 + 26 - k * 6, "#dcc878")
            cv.rect(x + 1 + k * 3, 18 + 26 - k * 6, x + 3 + k * 3, 18 + 26 - k * 6, "#9c8840")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def loom(seed=48):
    """Weaving loom with a half-finished textile."""
    cv = Canvas(66, 58)
    cv.rect(6, 12, 10, 54, "#8a6440")
    cv.rect(56, 12, 60, 54, "#8a6440")
    cv.rect(4, 8, 62, 14, "#a8763e")
    cv.rect(4, 46, 62, 52, "#a8763e")
    cv.rect(10, 20, 56, 22, "#c9a06a")
    cv.rect(10, 22, 56, 44, "#7a4a6a")     # textile in progress
    for i in range(6):
        cv.rect(12 + i * 7, 22, 14 + i * 7, 44, "#c05070")
        cv.rect(15 + i * 7, 24, 17 + i * 7, 42, "#e8b060")
    cv.rect(10, 42, 56, 46, "#5e3624")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def cooking_fire(seed=49):
    cv = Canvas(40, 36)
    for x in (4, 34):
        cv.rect(x, 20, x + 2, 32, "#5e4028")
    cv.poly([(2, 32), (38, 32), (20, 20)], "#5e4028")
    cv.poly([(6, 32), (34, 32), (20, 22)], "#7a5a3a")
    for i in range(5):
        cv.poly([(10 + i * 4, 24), (13 + i * 4, 8 + (i % 3) * 4), (16 + i * 4, 24)],
                ["#e8722c", "#f4a03c", "#f8d060", "#f4a03c", "#e8722c"][i])
    cv.px(18, 20, "#fff0c0")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def shrine(seed=50, stone="#a89c84", accent="#e8c060"):
    """Small wayside shrine / offering stone (variant per region via colours)."""
    cv = Canvas(34, 48)
    cv.rect(6, 32, 28, 44, "#8a8a82")
    cv.rect(4, 40, 30, 46, "#9c9c94")
    cv.rect(8, 28, 26, 34, stone)
    cv.poly([(6, 28), (28, 28), (24, 16), (10, 16)], stone)
    cv.rect(14, 10, 20, 16, accent)
    cv.poly([(12, 10), (22, 10), (17, 2)], accent)
    cv.px(17, 20, "#e8722c")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def market_stall(seed=51, cloth="#c05040"):
    """Market stall with striped awning and produce crates."""
    w, h = 84, 72
    cv = Canvas(w, h)
    cv.rect(6, 38, w - 7, 66, "#a8763e")
    cv.rect(6, 38, w - 7, 42, "#c08d4c")
    cv.rect(10, 46, w - 11, 64, "#8a5f30")
    # crates
    for i, (x, col) in enumerate(((12, "#d8634a"), (30, "#e0b04a"), (48, "#7aa84a"), (64, "#d88a4a"))):
        cv.rect(x, 40, x + 14, 54, "#8f6238")
        cv.rect(x + 1, 39, x + 13, 44, col)
        cv.rect(x + 1, 40, x + 13, 41, shade(col, 0.3))
    # awning
    cv.poly([(0, 40), (w - 1, 40), (w - 10, 16), (9, 16)], cloth)
    cv.poly([(0, 40), (w - 1, 40), (w - 1, 36), (0, 36)], shade(cloth, -0.25))
    for i in range(4):
        x = 8 + i * 20
        cv.rect(x, 17, x + 10, 39, shade(cloth, 0.18))
    cv.rect(9, 14, w - 10, 18, "#6d4c30")
    cv.rect(16, 4, 21, 16, "#6d4c30")
    cv.rect(w - 22, 4, w - 17, 16, "#6d4c30")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def stage(seed=52, cloth="#7a3a6a"):
    """Performance stage / pendopo for dances and music."""
    w, h = 140, 96
    cv = Canvas(w, h)
    # platform
    cv.rect(6, 62, w - 7, 86, "#a8763e")
    cv.rect(6, 62, w - 7, 66, "#c08d4c")
    cv.rect(6, 80, w - 7, 86, "#7d5432")
    # pillars
    for x in (10, w - 16):
        cv.rect(x, 24, x + 6, 64, "#8f6238")
        cv.rect(x, 24, x + 1, 64, "#b08a54")
    # roof
    cv.poly([(2, 26), (w - 3, 26), (w - 20, 6), (19, 6)], "#6d4c30")
    cv.poly([(2, 26), (w - 3, 26), (w - 3, 22), (2, 22)], "#523a26")
    # backdrop cloth with motif
    cv.rect(20, 30, w - 21, 62, cloth)
    cv.rect(20, 30, w - 21, 34, shade(cloth, 0.2))
    for i in range(9):
        x = 26 + i * 12
        cv.px(x, 44, "#e8c060")
        cv.px(x + 1, 43, "#e8c060")
        cv.px(x + 2, 44, "#e8c060")
        cv.px(x + 1, 45, "#e8c060")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def statue(seed=53, stone="#9c9c94"):
    """Village guardian statue (generic, respectful, non-specific)."""
    cv = Canvas(34, 56)
    cv.rect(4, 42, 30, 52, "#8a8a82")
    cv.rect(6, 38, 28, 44, "#9c9c94")
    cv.rect(10, 20, 24, 40, stone)
    cv.ellipse(11, 8, 23, 22, stone)
    cv.rect(13, 12, 16, 15, "#4a4640")
    cv.rect(18, 12, 21, 15, "#4a4640")
    cv.rect(15, 17, 19, 19, "#6a6660")
    cv.poly([(8, 8), (26, 8), (17, 0)], stone)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def totem(seed=54, base="#8a6440", accent="#e8c060"):
    """Carved wooden ancestral post.  Decorative game art (abstract motifs),
    not a reproduction of any specific community's carving."""
    cv = Canvas(34, 80)
    # base block
    cv.rect(6, 68, 28, 78, "#6d4c30")
    cv.rect(6, 68, 28, 70, "#8a6440")
    cv.rect(13, 58, 21, 70, shade(base, -0.15))
    # stacked carved faces (alternating direction, like a totem pole)
    for i in range(4):
        y = 12 + i * 12
        flip = i % 2 == 1
        cv.rect(4, y, 30, y + 11, shade(base, 0.1 if flip else 0.0))
        cv.rect(4, y, 30, y + 1, shade(base, -0.25))
        # face plate
        cv.rect(8, y + 2, 26, y + 10, shade(base, 0.22))
        # eyes
        cv.rect(11, y + 4, 14, y + 6, accent)
        cv.rect(20, y + 4, 23, y + 6, accent)
        cv.px(12, y + 5, "#2b2026")
        cv.px(21, y + 5, "#2b2026")
        # beak / mouth
        cv.poly([(15, y + 7), (19, y + 7), (17, y + 10 if flip else y + 11)], "#c05040")
        cv.rect(9, y + 8, 25, y + 9, "#5e4028")
        # wing flourishes on the sides
        for dirx in (-1, 1):
            sx = 4 if dirx < 0 else 30
            cv.line([(sx, y + 3), (sx + 7 * dirx, y + 1), (sx + 11 * dirx, y + 6)], shade(base, 0.3), 2)
    # crest
    cv.poly([(4, 12), (30, 12), (17, 0)], accent)
    cv.px(17, 6, "#c05040")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def tribal_shield(seed=55):
    cv = Canvas(24, 40)
    cv.poly([(4, 6), (20, 6), (20, 30), (12, 38), (4, 30)], "#b08a54")
    for i in range(3):
        cv.line([(6, 10 + i * 8), (18, 12 + i * 8)], "#7a4c34", 2)
    cv.line([(12, 6), (12, 36)], "#8a5a3a", 2)
    for i in range(3):
        cv.px(9, 12 + i * 8, "#e8c060")
        cv.px(15, 12 + i * 8, "#c05040")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def drum(seed=56):
    """Kendang-inspired two-headed drum."""
    cv = Canvas(34, 42)
    cv.ellipse(6, 4, 28, 14, "#b8834f")
    cv.ellipse(8, 5, 26, 12, "#d8b088")
    cv.rect(6, 10, 28, 32, "#a8763e")
    for x in range(7, 28, 5):
        cv.rect(x, 10, x + 1, 32, "#8a5f30")
    cv.ellipse(6, 28, 28, 38, "#b8834f")
    cv.ellipse(8, 29, 26, 36, "#e0c0a0")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def flute_rack(seed=57):
    cv = Canvas(46, 34)
    cv.rect(4, 14, 42, 18, "#8a6440")
    cv.rect(4, 18, 8, 32, "#8a6440")
    cv.rect(38, 18, 42, 32, "#8a6440")
    for i in range(4):
        x = 10 + i * 8
        cv.rect(x, 4, x + 3, 15, "#c8b062")
        cv.rect(x, 4, x, 15, "#dcc878")
        cv.px(x + 1, 8, "#7a6a34")
        cv.px(x + 2, 11, "#7a6a34")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def textile_rack(seed=58, cloth="#3a4a8a"):
    """Ulos / songket style textile hung on a rack (abstract pattern)."""
    cv = Canvas(58, 52)
    cv.rect(4, 6, 7, 50, "#8a6440")
    cv.rect(51, 6, 54, 50, "#8a6440")
    cv.rect(2, 4, 56, 8, "#a8763e")
    cv.rect(8, 10, 50, 46, cloth)
    cv.rect(8, 10, 50, 13, shade(cloth, 0.25))
    for i in range(5):
        y = 16 + i * 6
        col = "#e8c060" if i % 2 == 0 else "#e8e0d0"
        for x in range(11, 47, 6):
            cv.px(x, y, col)
            cv.px(x + 1, y + 1, col)
            cv.px(x + 2, y, col)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def crate(seed=59, col="#a8763e"):
    cv = Canvas(30, 28)
    cv.rect(3, 6, 27, 26, col)
    cv.rect(3, 6, 27, 10, shade(col, 0.2))
    cv.rect(3, 22, 27, 26, shade(col, -0.2))
    cv.rect(3, 6, 27, 26, shade(col, -0.35), fill=False)
    cv.line([(3, 6), (27, 26)], shade(col, -0.25), 1)
    cv.line([(27, 6), (3, 26)], shade(col, -0.25), 1)
    cv.outline("#2b2026", alpha_test=70)
    return cv


def barrel(seed=60, col="#8a5f30"):
    cv = Canvas(26, 30)
    cv.rect(4, 6, 22, 28, col)
    cv.rect(4, 6, 22, 8, shade(col, 0.25))
    cv.ellipse(4, 4, 22, 12, shade(col, 0.12))
    cv.rect(3, 12, 23, 14, "#6d5a3a")
    cv.rect(3, 22, 23, 24, "#6d5a3a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def easel_board(seed=61):
    """Notice board used for puzzles / village announcements."""
    cv = Canvas(46, 52)
    cv.rect(20, 26, 23, 50, "#7a5a3a")
    cv.rect(6, 4, 40, 30, "#8a6440")
    cv.rect(8, 6, 38, 28, "#e8dcc0")
    cv.rect(8, 6, 38, 28, "#c9a06a", fill=False)
    for i in range(4):
        cv.rect(11, 10 + i * 5, 30 - i * 3, 11 + i * 5, "#8a7a5a")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def boat_dock_house(seed=62):
    """River house on stilts with a small jetty (Kalimantan style)."""
    w, h = 118, 104
    cv = Canvas(w, h)
    for px in (18, 44, 70, 96):
        cv.rect(px, 70, px + 4, 96, "#6d4c30")
    cv.rect(10, 66, w - 11, 74, "#966f45")
    cv.rect(14, 42, w - 15, 68, "#b07a48")
    cv.rect(14, 42, w - 15, 46, "#c68f56")
    for i in range(3):
        cv.rect(20 + i * 26, 50, 40 + i * 26, 64, "#a06c3c")
        cv.rect(22 + i * 26, 52, 38 + i * 26, 62, "#8f6234")
    cv.rect(w // 2 - 8, 46, w // 2 + 8, 68, "#4a3020")
    cv.poly([(6, 44), (w - 7, 44), (w - 26, 16), (25, 16)], "#7a4a34")
    cv.poly([(6, 44), (w - 7, 44), (w - 7, 39), (6, 39)], "#5e3a28")
    for i in range(9):
        cv.line([(10 + i * 12, 43), (28 + int(i * 8), 17)], "#96624a", 1)
    cv.rect(25, 14, w - 26, 18, "#5e3a28")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def mountain_rock(seed=63):
    w, h = 96, 84
    cv = Canvas(w, h)
    cv.poly([(2, 82), (20, 40), (34, 22), (48, 8), (62, 24), (76, 44), (94, 82)], "#7a7268")
    cv.poly([(48, 8), (62, 24), (76, 44), (94, 82), (54, 82)], "#6a6258")
    cv.poly([(34, 22), (48, 8), (54, 82), (30, 82)], "#8a8278")
    cv.poly([(40, 26), (48, 10), (56, 26), (48, 34)], "#b8b2a8")
    for _ in range(20):
        rng = random.Random(seed + _)
        cv.px(rng.randrange(10, 86), rng.randrange(30, 80), "#5e564e")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def waterfall(seed=64):
    w, h = 96, 120
    cv = Canvas(w, h)
    cv.poly([(0, 30), (30, 10), (66, 14), (95, 34), (95, 118), (0, 118)], "#6a6258")
    cv.rect(30, 18, 66, 118, "#5a94b8")
    cv.rect(34, 18, 62, 118, "#78b0d0")
    for y in range(22, 118, 8):
        cv.rect(36, y, 44, y + 3, "#a8d4e8")
        cv.rect(50, y + 4, 58, y + 7, "#a8d4e8")
    cv.ellipse(24, 104, 72, 122, "#cfeaf8")
    cv.rect(26, 108, 70, 118, "#e8f6fc")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def cave_mouth(seed=65):
    w, h = 120, 96
    cv = Canvas(w, h)
    cv.poly([(0, 94), (10, 40), (40, 12), (80, 12), (110, 40), (119, 94)], "#6a6258")
    cv.ellipse(28, 40, 92, 96, "#241f1e")
    cv.ellipse(34, 46, 86, 92, "#161314")
    for i in range(7):   # stalactites
        x = 38 + i * 7
        cv.poly([(x, 46), (x + 5, 46), (x + 2, 56 + (i % 3) * 5)], "#3c3634")
    cv.rect(26, 88, 94, 96, "#4a4440")
    cv.outline("#2b2026", alpha_test=70)
    return cv


def rice_terrace_edge(seed=66):
    cv = Canvas(96, 40)
    cv.rect(0, 0, 95, 12, "#7fae52")
    for i in range(3):
        cv.rect(0, 12 + i * 9, 95, 20 + i * 9, "#8a6c44" if i % 2 else "#77512f")
    cv.rect(0, 36, 95, 39, "#6f9c46")
    cv.outline("#2b2026", alpha_test=70)
    return cv


# ==========================================================================
#  BUILD
# ==========================================================================
def build():
    # ---- nature -------------------------------------------------------
    reg("tree_tropical", tree_tropical(1), [-20, 62, 40, 24], sway=True)
    reg("tree_tropical2", tree_tropical(2, palette=("jungle2", "jungle", "jungle3")), [-20, 62, 40, 24], sway=True)
    reg("tree_fruit", tree_tropical(3, fruits="#e05a4a"), [-20, 62, 40, 24], sway=True)
    reg("tree_palm", tree_palm(4), [-16, 58, 32, 24], sway=True)
    reg("tree_palm2", tree_palm(5), [-16, 58, 32, 24], sway=True)
    reg("tree_pine", tree_pine(6), [-14, 54, 28, 20], sway=True)
    reg("bamboo_cluster", bamboo_cluster(7), [-14, 48, 28, 20], sway=True)
    reg("bush_green", bush(8), [-10, 14, 20, 12])
    reg("bush_flower", bush(9, flower="#e8798f"), [-10, 14, 20, 12])
    reg("bush_dark", bush(10, col="#3f7a3c"), [-10, 14, 20, 12])
    reg("fern", fern(11), [-10, 14, 20, 12])
    reg("rock_small", rock(12), [-9, 12, 18, 10])
    reg("rock_big", rock(13, big=True), [-14, 14, 28, 12])
    reg("stump", stump(14), [-10, 12, 20, 8])
    reg("flower_patch", flower_patch(15), None)
    reg("flower_patch2", flower_patch(16, colors=("#a070d8", "#f0f0f0", "#e8c060")), None)
    reg("mushroom", mushroom(17), None)
    reg("log", log(18), [-20, 12, 40, 10])
    reg("reed_clump", reed_clump(19), None)
    reg("lily_pad", lily_pad(20), None)
    reg("mountain_rock", mountain_rock(63), [-40, 58, 80, 24])
    reg("waterfall", waterfall(64), [-30, 30, 60, 88])
    reg("cave_mouth", cave_mouth(65), None)
    reg("rice_terrace_edge", rice_terrace_edge(66), None)

    # ---- buildings ----------------------------------------------------
    reg("rumah_gadang", rumah_gadang(20), [-70, 92, 140, 26], tag="building")
    reg("joglo_house", joglo_house(21), [-52, 96, 104, 22], tag="building")
    reg("joglo_house_small", joglo_house(22, scale=0.78), [-42, 96, 84, 22], tag="building")
    reg("rumah_panjang", rumah_panjang(23), [-96, 96, 192, 26], tag="building")
    reg("tongkonan", tongkonan(24), [-56, 100, 112, 24], tag="building")
    reg("honai", honai(25), [-24, 66, 48, 18], tag="building")
    reg("honai_big", honai(26, big=True), [-34, 86, 68, 22], tag="building")
    reg("hut_coastal", hut_papua_coastal(27), [-34, 62, 68, 20], tag="building")
    reg("lumbung", lumbung(28), [-28, 60, 56, 24], tag="building")
    reg("warung", warung(29), [-30, 42, 60, 20], tag="building")
    reg("warung_green", warung(30, roof_col="#3f7a4a"), [-30, 42, 60, 20], tag="building")
    reg("food_stall", food_stall(31), [-36, 28, 72, 20], tag="building")
    reg("workshop", workshop(32), [-36, 40, 72, 26], tag="building")
    reg("workshop_java", workshop(33, accent="#8a6a3a"), [-36, 40, 72, 26], tag="building")
    reg("cultural_center", cultural_center(34), [-52, 48, 104, 44], tag="building")
    reg("cultural_center_timur", cultural_center(35, roof="#7a4a34", banner="#3a7a8a"), [-52, 48, 104, 44], tag="building")
    reg("candi", candi(36), [-52, 116, 104, 26], tag="landmark")
    reg("gate_keraton", gate_keraton(37), None, tag="landmark")
    reg("clock_tower", clock_tower(38), [-22, 138, 44, 16], tag="landmark")
    reg("lookout_tower", lookout_tower(39), [-24, 120, 48, 14], tag="landmark")
    reg("boat_dock_house", boat_dock_house(40), [-48, 68, 96, 30], tag="building")
    reg("stage", stage(41), [-60, 62, 120, 26], tag="building")

    # ---- props --------------------------------------------------------
    reg("fence", fence(42), None)
    reg("fence_wood", fence(43, col="#8a6440"), None)
    reg("signpost", signpost(44), [-8, 22, 16, 20])
    reg("lantern", lantern(45), [-6, 24, 12, 14])
    reg("brazier", brazier(46), [-10, 24, 20, 8])
    reg("well", well(47), [-14, 24, 28, 18])
    reg("bridge_plank", bridge_plank(48), None)
    reg("canoe", canoe(49), [-24, 14, 48, 10])
    reg("dock", dock(50), None)
    reg("pot_plant", pot_plant(51), [-9, 20, 18, 10])
    reg("basket", basket(52), [-10, 12, 20, 10])
    reg("drying_rack", drying_rack(53), [-20, 12, 40, 28])
    reg("drying_rack_blue", drying_rack(54, col="#3a6a9a"), [-20, 12, 40, 28])
    reg("gamelan_set", gamelan_set(55), [-32, 40, 64, 8])
    reg("angklung_stand", angklung_stand(56), [-22, 50, 44, 8])
    reg("loom", loom(57), [-24, 46, 48, 8])
    reg("cooking_fire", cooking_fire(58), [-12, 24, 24, 8])
    reg("shrine", shrine(59), [-11, 38, 22, 10])
    reg("shrine_java", shrine(60, stone="#b0a48c", accent="#d8a840"), [-11, 38, 22, 10])
    reg("market_stall", market_stall(61), [-32, 40, 64, 26], tag="building")
    reg("market_stall_blue", market_stall(62, cloth="#3a6a9a"), [-32, 40, 64, 26], tag="building")
    reg("statue", statue(63), [-12, 40, 24, 12])
    reg("totem", totem(64), [-10, 58, 20, 16])
    reg("totem_red", totem(65, accent="#c05040"), [-10, 58, 20, 16])
    reg("tribal_shield", tribal_shield(66), [-9, 12, 18, 24])
    reg("drum", drum(67), [-12, 28, 24, 12])
    reg("flute_rack", flute_rack(68), [-18, 22, 36, 10])
    reg("textile_rack", textile_rack(69), [-20, 4, 40, 44])
    reg("textile_rack_red", textile_rack(70, cloth="#8a3a3a"), [-20, 4, 40, 44])
    reg("crate", crate(71), [-12, 14, 24, 12])
    reg("barrel", barrel(72), [-11, 14, 22, 14])
    reg("easel_board", easel_board(73), [-14, 16, 28, 32])

    os.makedirs(OUT_DATA, exist_ok=True)
    with open(os.path.join(OUT_DATA, "objects.json"), "w") as fh:
        json.dump(REGISTRY, fh, indent=1)
    print(f"wrote {len(REGISTRY)} objects + data/objects.json")


if __name__ == "__main__":
    build()
