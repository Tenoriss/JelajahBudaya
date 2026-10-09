"""artlib.py -- tiny pixel-art toolkit used by the JelajahBudaya asset generators.

Everything in this file is original procedural art code written for the game
"Nusantara: Jejak Budaya".  No external art assets are used.

The helpers deliberately work in *pixel* space (no anti-aliasing) so that the
output keeps a crisp, cohesive retro/2D-adventure look.
"""
from __future__ import annotations

import math
import random
from PIL import Image, ImageDraw, ImageFilter

# --------------------------------------------------------------------------
# Palette (warm, Indonesian-adventure inspired, deliberately cohesive)
# --------------------------------------------------------------------------
P = {
    # generic
    "outline": (38, 28, 40, 255),
    "outline_soft": (58, 44, 62, 255),
    "shadow": (52, 44, 70, 90),
    "white": (255, 250, 240, 255),
    "cream": (243, 226, 190, 255),
    "paper": (232, 209, 166, 255),
    "paper_dark": (203, 172, 126, 255),
    # greens
    "grass": (104, 168, 76, 255),
    "grass2": (86, 148, 66, 255),
    "grass3": (124, 186, 88, 255),
    "grass_dark": (66, 118, 56, 255),
    "jungle": (58, 112, 58, 255),
    "jungle2": (44, 90, 50, 255),
    "jungle3": (78, 134, 66, 255),
    "moss": (96, 128, 64, 255),
    "leaf": (74, 158, 82, 255),
    # earth
    "dirt": (170, 128, 84, 255),
    "dirt2": (148, 108, 70, 255),
    "dirt3": (190, 150, 104, 255),
    "sand": (226, 200, 140, 255),
    "sand2": (205, 178, 120, 255),
    "mud": (104, 84, 62, 255),
    "mud2": (84, 66, 50, 255),
    "stone": (150, 148, 148, 255),
    "stone2": (122, 120, 124, 255),
    "stone3": (176, 174, 172, 255),
    "rock": (110, 106, 112, 255),
    "cliff": (128, 112, 100, 255),
    # water
    "water": (74, 152, 196, 255),
    "water2": (60, 128, 178, 255),
    "water3": (110, 186, 220, 255),
    "deep": (44, 96, 150, 255),
    "deep2": (34, 78, 128, 255),
    "foam": (222, 244, 250, 255),
    # wood / building
    "wood": (168, 116, 72, 255),
    "wood2": (140, 94, 58, 255),
    "wood3": (196, 148, 98, 255),
    "bamboo": (196, 176, 96, 255),
    "bamboo2": (166, 148, 74, 255),
    "thatch": (206, 168, 96, 255),
    "thatch2": (172, 134, 74, 255),
    "roof_red": (176, 74, 62, 255),
    "roof_red2": (142, 54, 48, 255),
    "roof_dark": (86, 62, 58, 255),
    "roof_black": (62, 50, 52, 255),
    "roof_gold": (206, 166, 78, 255),
    "tile_blue": (74, 106, 132, 255),
    # culture accents
    "batik_brown": (120, 74, 46, 255),
    "batik_indigo": (58, 72, 124, 255),
    "batik_gold": (220, 176, 84, 255),
    "red": (196, 68, 62, 255),
    "red2": (158, 48, 46, 255),
    "yellow": (238, 196, 84, 255),
    "gold": (232, 186, 92, 255),
    "orange": (226, 132, 60, 255),
    "teal": (66, 158, 152, 255),
    "purple": (124, 84, 148, 255),
    "pink": (226, 140, 158, 255),
    # skin tones (respectful variety)
    "skin1": (240, 202, 160, 255),
    "skin2": (222, 174, 126, 255),
    "skin3": (198, 146, 100, 255),
    "skin4": (168, 118, 80, 255),
    "skin5": (136, 92, 62, 255),
    # hair
    "hair_black": (48, 38, 44, 255),
    "hair_brown": (86, 56, 42, 255),
    "hair_grey": (176, 172, 168, 255),
    "hair_white": (226, 222, 214, 255),
    "hair_red": (140, 62, 48, 255),
    # ui
    "ui_bg": (44, 32, 48, 240),
    "ui_bg2": (62, 44, 62, 245),
    "ui_panel": (86, 58, 62, 250),
    "ui_panel_light": (112, 78, 78, 255),
    "ui_border": (226, 186, 106, 255),
    "ui_border2": (150, 104, 62, 255),
    "ui_text": (248, 236, 210, 255),
    "ui_dim": (196, 172, 140, 255),
    "ui_ok": (128, 196, 118, 255),
    "ui_bad": (208, 92, 84, 255),
    "ui_hl": (252, 226, 154, 255),
}


def c(name: str) -> tuple:
    """Colour lookup by name, ``#rrggbb`` or rgba tuple."""
    if isinstance(name, tuple):
        return name
    if name.startswith("#"):
        h = name.lstrip("#")
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    return P[name]


def shade(col, amount: float):
    """Lighten (amount>0) or darken (amount<0) an RGBA colour."""
    col = c(col) if not isinstance(col, tuple) else col
    r, g, b = col[0], col[1], col[2]
    a = col[3] if len(col) > 3 else 255
    if amount >= 0:
        r = int(r + (255 - r) * amount)
        g = int(g + (255 - g) * amount)
        b = int(b + (255 - b) * amount)
    else:
        r = int(r * (1 + amount))
        g = int(g * (1 + amount))
        b = int(b * (1 + amount))
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), a)


def mix(a, b, t: float):
    a, b = c(a), c(b)
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
        255,
    )


# --------------------------------------------------------------------------
# Canvas
# --------------------------------------------------------------------------
class Canvas:
    """Thin wrapper around a Pillow RGBA image with pixel helpers."""

    def __init__(self, w: int, h: int, bg=(0, 0, 0, 0)):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), bg)
        self.d = ImageDraw.Draw(self.img)

    # -- primitives -------------------------------------------------------
    def px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((int(x), int(y)), c(col))

    def rect(self, x0, y0, x1, y1, col, fill=True):
        col = c(col)
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if fill:
            self.d.rectangle([x0, y0, x1, y1], fill=col)
        else:
            self.d.rectangle([x0, y0, x1, y1], outline=col)

    def ellipse(self, x0, y0, x1, y1, col, fill=True):
        col = c(col)
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if fill:
            self.d.ellipse([x0, y0, x1, y1], fill=col)
        else:
            self.d.ellipse([x0, y0, x1, y1], outline=col)

    def line(self, pts, col, width=1):
        self.d.line(pts, fill=c(col), width=width, joint="curve")

    def poly(self, pts, col, fill=True):
        col = c(col)
        if fill:
            self.d.polygon(pts, fill=col)
        else:
            self.d.polygon(pts, outline=col)

    def paste(self, other, x, y):
        self.img.alpha_composite(other.img if isinstance(other, Canvas) else other, (int(x), int(y)))

    # -- texture helpers --------------------------------------------------
    def speckle(self, col_list, density=0.10, rng=None, region=None, mask_fn=None):
        rng = rng or random.Random(1234)
        x0, y0, x1, y1 = region or (0, 0, self.w, self.h)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if mask_fn and not mask_fn(x, y):
                    continue
                if rng.random() < density:
                    self.px(x, y, rng.choice(col_list))

    def blobs(self, col, count=6, rmin=1, rmax=3, rng=None, mask_fn=None):
        rng = rng or random.Random(99)
        for _ in range(count):
            x = rng.randrange(self.w)
            y = rng.randrange(self.h)
            if mask_fn and not mask_fn(x, y):
                continue
            r = rng.randint(rmin, rmax)
            self.ellipse(x - r, y - r, x + r, y + r, col)

    def dither(self, col, mask_fn, rng=None, density=0.5):
        rng = rng or random.Random(7)
        for y in range(self.h):
            for x in range(self.w):
                if mask_fn(x, y) and rng.random() < density:
                    self.px(x, y, col)

    # -- composition ------------------------------------------------------
    def outline(self, col=None, alpha_test=40, diagonal=True, only_shrink=False):
        """Add a 1px outline around opaque pixels (classic sprite outline)."""
        col = c(col or "outline")
        src = self.img.copy()
        px = src.load()
        w, h = self.w, self.h
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            offsets += [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for y in range(h):
            for x in range(w):
                if px[x, y][3] > alpha_test:
                    continue
                near = False
                for dx, dy in offsets:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] > alpha_test:
                        near = True
                        break
                if near:
                    self.px(x, y, col)

    def drop_shadow(self, dx=0, dy=2, alpha=70):
        shadow = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        alpha = self.img.split()[3]
        shadow.putalpha(alpha.point(lambda a: min(alpha_, alpha) if a > 40 else 0) if False else alpha.point(lambda a: int(a * 0.28) if a > 40 else 0))
        shadow = shadow.filter(ImageFilter.GaussianBlur(0.6))
        base = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        base.alpha_composite(shadow, (max(0, dx), max(0, dy)))
        base.alpha_composite(self.img)
        self.img = base
        self.d = ImageDraw.Draw(self.img)

    def save(self, path):
        self.img.save(path)
        return path


# --------------------------------------------------------------------------
# Reusable drawing routines
# --------------------------------------------------------------------------
def value_noise(size: int, cell: int, seed: int):
    """Tiny value-noise grid (smooth-ish) used for organic tile texture."""
    rng = random.Random(seed)
    gw = size // cell + 2
    grid = [[rng.random() for _ in range(gw)] for _ in range(gw)]

    def sample(sx, sy):
        gx, gy = sx / cell, sy / cell
        x0, y0 = int(gx), int(gy)
        fx, fy = gx - x0, gy - y0
        # smoothstep
        fx = fx * fx * (3 - 2 * fx)
        fy = fy * fy * (3 - 2 * fy)
        a = grid[y0][x0] * (1 - fx) + grid[y0][x0 + 1] * fx
        b = grid[y0 + 1][x0] * (1 - fx) + grid[y0 + 1][x0 + 1] * fx
        return a * (1 - fy) + b * fy

    return sample


def grass_tile(theme: dict, variant: int, size=32) -> Canvas:
    """Grass tile: value-noise clumps + blades + details."""
    base = theme["grass"][variant % len(theme["grass"])]
    cv = Canvas(size, size, c(base))
    rng = random.Random(4000 + variant)

    n1 = value_noise(size, 7, seed=100 + variant)
    n2 = value_noise(size, 3, seed=200 + variant)
    dark = theme["grass_dark"][0]
    dark2 = theme["grass_dark"][-1]
    light = theme["grass_light"][-1]
    light2 = theme["grass_light"][0]
    for y in range(size):
        for x in range(size):
            v = n1(x, y) * 0.65 + n2(x, y) * 0.35
            if v < 0.36:
                cv.px(x, y, dark)
            elif v < 0.44:
                cv.px(x, y, dark2)
            elif v > 0.72:
                cv.px(x, y, light)
            elif v > 0.63:
                cv.px(x, y, light2)

    # blades of grass (little vertical tufts)
    for _ in range(int(size * 0.7)):
        x = rng.randrange(1, size - 2)
        y = rng.randrange(2, size - 3)
        col = rng.choice([light, light2, dark2])
        cv.px(x, y, col)
        cv.px(x, y + 1, col)
        if rng.random() < 0.35:
            cv.px(x + 1, y + 1, col)
    # darker outer wisps so tiles read as a lawn rather than a grid
    for _ in range(5):
        x = rng.randrange(0, size - 2)
        y = rng.randrange(0, size - 2)
        cv.px(x, y, dark)
        cv.px(x + 1, y, dark)
    return cv


def noise_tile(colors, size=32, seed=0, density=0.5, clump=3):
    cv = Canvas(size, size, c(colors[0]))
    rng = random.Random(seed)
    for _ in range(int(size * size * density / clump)):
        x = rng.randrange(size)
        y = rng.randrange(size)
        col = rng.choice(colors[1:])
        r = rng.randint(0, 1)
        cv.ellipse(x - r, y - r, x + r, y + r, col)
    return cv


def water_frame(theme: dict, frame: int, size=32, deep=False) -> Canvas:
    """Animated water tile: 3 shade bands + drifting crests + sparkles."""
    cols = theme["deep"] if deep else theme["water"]
    cv = Canvas(size, size, c(cols[0]))
    n = value_noise(size, 6, seed=33 if deep else 11)
    for y in range(size):
        for x in range(size):
            v = n(x, y)
            if v > 0.68:
                cv.px(x, y, cols[1])
            elif v < 0.32:
                cv.px(x, y, cols[2])
    # drifting wave crests (shift with the frame so the loop reads as motion)
    rng = random.Random(frame * 31 + (5 if deep else 2))
    for i in range(3 if not deep else 2):
        y = (rng.randrange(size) + frame * 3) % size
        x0 = (rng.randrange(size) + frame * 5) % size
        length = rng.randint(5, 11)
        for k in range(length):
            xx = x0 + k
            if xx >= size:
                xx -= size
            yy = y
            cv.px(xx, yy, cols[3])
            if k % 3 == 1 and yy + 1 < size:
                cv.px(xx, yy + 1, shade(cols[0], 0.18))
    for _ in range(4):
        x = (rng.randrange(size - 3) + frame * 7) % (size - 2)
        y = (rng.randrange(size - 2) + frame * 2) % (size - 1)
        cv.px(x, y, cols[3])
    return cv


def themed_palette(name: str) -> dict:
    """Region specific colour themes for terrain."""
    themes = {
        "sumatra": dict(
            grass=["#6aa84f", "#5d9a46", "#78b45a"],
            grass_dark=["#3f6b34", "#4c7d3c"],
            grass_light=["#8ec86b", "#a5d97c"],
            dirt=["#b0855a", "#9a7050"],
            sand=["#e0c88c", "#cdb277"],
            water=["#4a98c4", "#3a80b4", "#6db6dc", "#e4f4fb"],
            deep=["#2c6090", "#24507c", "#3f7cb0", "#bfe2f0"],
            stone=["#9c9a9a", "#828282"],
            path=["#c2a071", "#ab8a5e"],
            rock=["#7c6a5c", "#63544a"],
            accent="#c98a4a",
        ),
        "java": dict(
            grass=["#7cae4e", "#6ea044", "#8cbe5c"],
            grass_dark=["#4c7838", "#5c8a42"],
            grass_light=["#a0d070", "#b4e084"],
            dirt=["#a8834e", "#8e6c40"],
            sand=["#ded29a", "#c8bb84"],
            water=["#5a9fb0", "#4a889c", "#7fc0cc", "#e8f6f4"],
            deep=["#3a6e80", "#2e5c6c", "#558e9c", "#cfe8ea"],
            stone=["#a8a49c", "#8c887f"],
            path=["#cbb489", "#b09a72"],
            rock=["#8a8278", "#6d675f"],
            accent="#c9a24a",
        ),
        "kalimantan": dict(
            grass=["#4e8c46", "#437c3d", "#5c9c52"],
            grass_dark=["#2f5c2e", "#3a6a34"],
            grass_light=["#78b062", "#8cc070"],
            dirt=["#8a6a48", "#71553a"],
            sand=["#cbb27e", "#b69c68"],
            water=["#5a7c62", "#48684f", "#7f9c7e", "#d8e8dc"],
            deep=["#3c5a4c", "#2f4a40", "#567a64", "#c4dccd"],
            stone=["#8c8c84", "#74746c"],
            path=["#a8906a", "#8e7856"],
            rock=["#6c6058", "#574d46"],
            accent="#7fa05a",
        ),
        "sulawesi": dict(
            grass=["#86b055", "#78a24a", "#96c05f"],
            grass_dark=["#557c3a", "#638c44"],
            grass_light=["#aed07c", "#c0dc92"],
            dirt=["#b8945e", "#9c7a4a"],
            sand=["#e8d6a4", "#d2bd8a"],
            water=["#4590b8", "#387aa2", "#6cb4d4", "#e6f4fa"],
            deep=["#2a5c88", "#224c74", "#4a84ac", "#c6e4f2"],
            stone=["#b0aa9c", "#948e80"],
            path=["#cdb390", "#b39a76"],
            rock=["#8e8272", "#6f6558"],
            accent="#d09a52",
        ),
        "papua": dict(
            grass=["#5f9c58", "#548c4e", "#6cac62"],
            grass_dark=["#356640", "#3f7448"],
            grass_light=["#8cc074", "#a0ce86"],
            dirt=["#9c7a52", "#856342"],
            sand=["#d8c48e", "#c0ac76"],
            water=["#4a94ba", "#3b7fa6", "#72b8d6", "#e6f6fb"],
            deep=["#2e6488", "#265274", "#4c8cb0", "#c8e6f4"],
            stone=["#9a968c", "#807c74"],
            path=["#b89a70", "#9c825c"],
            rock=["#6e6a64", "#5a564f"],
            accent="#a8785a",
        ),
    }
    return themes[name]
