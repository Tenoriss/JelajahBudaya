"""gen_terrain.py -- generates the terrain tileset atlases (one per region).

Output:
  assets/environments/tilesets/terrain_<region>.png
  data/tilesets.json

Run:  python3 tools/gen_terrain.py
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artlib import Canvas, P, c, grass_tile, noise_tile, themed_palette, water_frame  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_IMG = os.path.join(ROOT, "assets", "environments", "tilesets")
OUT_DATA = os.path.join(ROOT, "data")

TS = 32          # tile size
COLS = 10        # atlas columns

# tile name -> (solid, speed, anim_group)
TILE_DEFS = [
    ("grass0", False, 1.0, None),
    ("grass1", False, 1.0, None),
    ("grass2", False, 1.0, None),
    ("grass_flower", False, 1.0, None),
    ("path", False, 1.15, None),
    ("dirt", False, 1.0, None),
    ("sand", False, 0.9, None),
    ("water", False, 0.72, "water"),
    ("deep", True, 0.0, "deep"),
    ("rice0", False, 0.85, None),
    ("rice1", False, 0.85, None),
    ("farm", False, 0.95, None),
    ("jungle_floor", False, 1.0, None),
    ("mud", False, 0.8, None),
    ("stone_floor", False, 1.0, None),
    ("cliff", True, 0.0, None),
    ("plank", False, 1.1, None),
    ("bamboo_floor", False, 1.05, None),
    ("temple_stone", False, 1.0, None),
    ("paving", False, 1.15, None),
    ("highland", False, 1.0, None),
    ("tall_grass", False, 0.9, None),
    ("reed", False, 0.9, None),
    ("ash", False, 1.0, None),
    ("volcanic", True, 0.0, None),
    ("carpet", False, 1.2, None),
]
# animated tiles add extra frames right after their base tile
ANIM_FRAMES = 3


def tile_row_extras():
    """Row list where animated tiles occupy ANIM_FRAMES slots."""
    rows = []
    for name, solid, speed, anim in TILE_DEFS:
        rows.append((name, solid, speed, anim))
    return rows


def draw_tile(name: str, theme: dict, rng: random.Random) -> Canvas:
    g_dark = theme["grass_dark"]
    g_light = theme["grass_light"]
    t = {
        "grass": theme["grass"],
        "grass_dark": g_dark,
        "grass_light": g_light,
    }
    if name.startswith("grass"):
        if name == "grass_flower":
            cv = grass_tile(t, 1, TS)
            for _ in range(7):
                x = rng.randrange(2, TS - 3)
                y = rng.randrange(2, TS - 3)
                col = rng.choice(["#f2e6a0", "#e8a0b4", "#f0f0f0", "#e0c060"])
                cv.px(x, y, col)
                cv.px(x + 1, y, col)
                cv.px(x, y + 1, shade_hex(col))
            return cv
        return grass_tile(t, int(name[-1]), TS)

    if name == "path":
        cv = noise_tile([theme["path"][0], theme["path"][1], "#d8bd93"], TS, seed=21, density=0.85, clump=2)
        for _ in range(10):  # pebbles
            x, y = rng.randrange(TS), rng.randrange(TS)
            cv.px(x, y, "#e8dcc0")
        return cv
    if name == "dirt":
        return noise_tile([theme["dirt"][0], theme["dirt"][1], "#c49a6c"], TS, seed=22, density=0.8, clump=2)
    if name == "sand":
        cv = noise_tile([theme["sand"][0], theme["sand"][1], "#f0dfae"], TS, seed=23, density=0.6, clump=2)
        for _ in range(5):
            x, y = rng.randrange(TS), rng.randrange(TS)
            cv.px(x, y, "#d8c48a")
        return cv
    if name == "water":
        return water_frame(theme, 0)
    if name == "deep":
        return water_frame(theme, 0, deep=True)
    if name in ("rice0", "rice1"):
        soil = "#7fae52" if name == "rice0" else "#8fbc5c"
        cv = Canvas(TS, TS, c("#6f9c46"))
        # flooded terrace bands
        for i in range(4):
            y = i * 8
            cv.rect(0, y, TS - 1, y + 4, "#8cbb58" if i % 2 else soil)
            cv.rect(0, y + 5, TS - 1, y + 5, "#cbb06a")
        # rice sprouts
        for i in range(4):
            y = i * 8
            for x in range(1, TS - 1, 4):
                cv.px(x + (i % 2) * 2, y + 1, "#5c8a3c")
                cv.px(x + (i % 2) * 2, y + 2, "#74a84a")
                cv.px(x + (i % 2) * 2, y + 3, "#4c7a34")
        cv.rect(0, TS - 2, TS - 1, TS - 1, "#a68f52")
        return cv

    if name == "farm":
        cv = Canvas(TS, TS, c("#8c6c44"))
        for x in range(2, TS, 7):
            cv.rect(x, 0, x + 3, TS - 1, "#77512f")   # tilled furrow
            cv.rect(x + 4, 0, x + 5, TS - 1, "#9c7a4c")
            for y in range(3, TS - 2, 6):              # young crops
                cv.px(x + 1, y, "#5f9440")
                cv.px(x + 1, y - 1, "#74ac52")
                cv.px(x + 2, y, "#4c7c36")
        for _ in range(14):
            cv.px(rng.randrange(TS), rng.randrange(TS), "#6f4c2c")
        return cv

    if name == "jungle_floor":
        cv = Canvas(TS, TS, c("#3c6238"))
        n = None
        try:
            from artlib import value_noise
            n = value_noise(TS, 6, seed=88)
        except Exception:
            pass
        if n:
            for y in range(TS):
                for x in range(TS):
                    v = n(x, y)
                    if v < 0.36:
                        cv.px(x, y, "#2f5230")
                    elif v > 0.66:
                        cv.px(x, y, "#4a7a42")
        # broad tropical leaves lying on the ground
        for _ in range(9):
            x, y = rng.randrange(2, TS - 8), rng.randrange(2, TS - 6)
            col = rng.choice(["#548c46", "#437a3c", "#638f4a", "#3a6a38"])
            cv.ellipse(x, y, x + 6, y + 3, col)
            cv.px(x + 3, y + 1, "#7aa85a")
        for _ in range(7):   # twigs + litter
            x, y = rng.randrange(TS - 3), rng.randrange(TS - 3)
            cv.px(x, y, "#8a7440")
            cv.px(x + 1, y + 1, "#6f5c34")
        return cv

    if name == "mud":
        cv = noise_tile(["#54432f", "#463726", "#66513a"], TS, seed=24, density=0.8, clump=2)
        for _ in range(4):
            x, y = rng.randrange(TS - 3), rng.randrange(TS - 3)
            cv.ellipse(x, y, x + 2, y + 1, "#7a614a")
        return cv
    if name == "stone_floor":
        cv = Canvas(TS, TS, c(theme["stone"][0]))
        for y in range(0, TS, 8):
            for x in range(0, TS, 8):
                off = 4 if (y // 8) % 2 else 0
                cv.rect(x + off, y, x + off + 7, y + 7, theme["stone"][1], fill=False)
        cv.speckle(["#b0aeae", "#8c8a8a"], 0.06, rng)
        return cv
    if name == "cliff":
        cv = Canvas(TS, TS, c("#6d6156"))
        # strata bands
        for i, col in enumerate(["#7d7162", "#645a4e", "#8a7d6a", "#5c5248"]):
            y = i * 8
            cv.rect(0, y, TS - 1, y + 6, col)
            cv.rect(0, y + 7, TS - 1, y + 7, "#463e36")
        for _ in range(26):  # cracks
            x, y = rng.randrange(TS), rng.randrange(TS)
            cv.px(x, y, "#4a4238")
            if rng.random() < 0.5:
                cv.px(x + 1, y + 1, "#4a4238")
        cv.rect(0, 0, TS - 1, 1, "#948674")
        return cv

    if name == "plank":
        cv = Canvas(TS, TS, c("#a87448"))
        for i in range(0, TS, 8):
            cv.rect(0, i, TS - 1, i + 6, "#b8834f")
            cv.rect(0, i + 7, TS - 1, i + 7, "#7d5432")
        for _ in range(12):
            cv.px(rng.randrange(TS), rng.randrange(TS), "#8f6440")
        return cv
    if name == "bamboo_floor":
        cv = Canvas(TS, TS, c("#c8b062"))
        for x in range(0, TS, 6):
            cv.rect(x, 0, x + 4, TS - 1, "#d6c078")
            cv.rect(x + 5, 0, x + 5, TS - 1, "#a08c48")
        for y in range(0, TS, 11):
            cv.rect(0, y, TS - 1, y, "#8f7c40")
        return cv
    if name == "temple_stone":
        cv = Canvas(TS, TS, c("#8e8a80"))
        cv.rect(0, 0, TS - 1, TS - 1, "#a8a496", fill=False)
        for y in range(2, TS - 2, 6):
            for x in range(2, TS - 2, 6):
                cv.rect(x, y, x + 2, y + 2, "#c8b48a")
        cv.speckle(["#78746c", "#b8b4a4"], 0.08, rng)
        return cv
    if name == "paving":
        cv = Canvas(TS, TS, c("#b8a284"))
        for y in range(0, TS, 8):
            for x in range(0, TS, 8):
                cv.rect(x, y, x + 7, y + 7, "#a68f70", fill=False)
                cv.px(x + 3, y + 3, "#8f7a5e")
        return cv
    if name == "highland":
        cv = noise_tile(["#7d9c62", "#6c8c54", "#94b072"], TS, seed=30, density=0.7, clump=2)
        for _ in range(6):
            x, y = rng.randrange(TS), rng.randrange(TS)
            cv.px(x, y, "#c8d8b0")
        return cv
    if name == "tall_grass":
        cv = Canvas(TS, TS, c("#4b7a3a"))
        from artlib import value_noise
        n = value_noise(TS, 5, seed=55)
        for y in range(TS):
            for x in range(TS):
                v = n(x, y)
                cv.px(x, y, "#5d8f46" if v > 0.5 else "#3f6b34")
        for _ in range(30):
            x, y = rng.randrange(1, TS - 2), rng.randrange(3, TS - 3)
            col = rng.choice(["#6ba64e", "#7cba5c", "#548a40"])
            cv.px(x, y, col)
            cv.px(x, y + 1, col)
            cv.px(x, y + 2, col)
            if rng.random() < 0.4:
                cv.px(x + 1, y + 2, col)
        return cv

    if name == "reed":
        cv = Canvas(TS, TS, c("#4a7a52"))
        for _ in range(16):
            x, y = rng.randrange(TS), rng.randrange(TS - 8, TS)
            cv.px(x, y, "#6a9c5c")
            cv.px(x, y - 1, "#7fae68")
            cv.px(x, y - 2, "#5c8a4c")
        cv.rect(0, TS - 6, TS - 1, TS - 1, "#3c6a48")
        return cv
    if name == "ash":
        return noise_tile(["#8a827a", "#7a726c", "#9a928a"], TS, seed=31, density=0.7, clump=2)
    if name == "volcanic":
        cv = noise_tile(["#4a423e", "#3c3632", "#5a504a"], TS, seed=32, density=0.8, clump=2)
        for _ in range(5):
            x, y = rng.randrange(TS), rng.randrange(TS)
            cv.ellipse(x, y, x + 2, y + 2, "#2c2622")
        return cv
    if name == "carpet":
        cv = Canvas(TS, TS, c("#8a3c3c"))
        cv.rect(4, 4, TS - 5, TS - 5, "#a85050", fill=False)
        cv.rect(9, 9, TS - 10, TS - 10, "#d8b070", fill=False)
        for _ in range(8):
            cv.px(rng.randrange(6, TS - 6), rng.randrange(6, TS - 6), "#e8d090")
        return cv
    return Canvas(TS, TS, c("#ff00ff"))


def shade_hex(hexcol: str) -> str:
    h = hexcol.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#%02x%02x%02x" % (max(0, r - 40), max(0, g - 40), max(0, b - 30))


def build_region(region: str) -> dict:
    theme = themed_palette(region)
    rng = random.Random(hash(region) & 0xFFFF)

    # build ordered list of (tile_name, canvas) including animation frames
    entries = []
    for name, solid, speed, anim in TILE_DEFS:
        if anim:
            for f in range(ANIM_FRAMES):
                deep = anim == "deep"
                cv = water_frame(theme, f, TS, deep=deep)
                entries.append((f"{name}{f}", solid, speed, anim, f, cv))
        else:
            entries.append((name, solid, speed, anim, 0, draw_tile(name, theme, rng)))

    rows = (len(entries) + COLS - 1) // COLS
    atlas = Canvas(COLS * TS, rows * TS, (0, 0, 0, 0))
    tile_info = {}
    anim_groups = {}
    for i, (name, solid, speed, anim, frame, cv) in enumerate(entries):
        col, row = i % COLS, i // COLS
        atlas.paste(cv, col * TS, row * TS)
        tile_info[name] = {"atlas": [col, row], "solid": solid, "speed": speed, "region": region}
        if anim:
            anim_groups.setdefault(anim, []).append(name)

    os.makedirs(OUT_IMG, exist_ok=True)
    atlas.save(os.path.join(OUT_IMG, f"terrain_{region}.png"))
    return {"tile_size": TS, "columns": COLS, "tiles": tile_info, "animations": anim_groups}


def main():
    data = {}
    for region in ["sumatra", "java", "kalimantan", "sulawesi", "papua"]:
        data[region] = build_region(region)
        print(f"  terrain_{region}.png  ({len(data[region]['tiles'])} tiles)")

    # single shared tile semantics table (used by the region builder for defaults)
    data["_legend"] = {
        "GRASS": ["grass0", "grass1", "grass2", "grass_flower"],
        "PATH": ["path"],
        "DIRT": ["dirt"],
        "SAND": ["sand"],
        "WATER": ["water0", "water1", "water2"],
        "DEEP": ["deep0", "deep1", "deep2"],
        "RICE": ["rice0", "rice1"],
        "FARM": ["farm"],
        "JUNGLE": ["jungle_floor"],
        "MUD": ["mud"],
        "STONE": ["stone_floor"],
        "CLIFF": ["cliff"],
        "PLANK": ["plank"],
        "BAMBOO": ["bamboo_floor"],
        "TEMPLE": ["temple_stone"],
        "PAVING": ["paving"],
        "HIGHLAND": ["highland"],
        "TALLGRASS": ["tall_grass"],
        "REED": ["reed"],
        "ASH": ["ash"],
        "VOLCANIC": ["volcanic"],
        "CARPET": ["carpet"],
    }
    os.makedirs(OUT_DATA, exist_ok=True)
    with open(os.path.join(OUT_DATA, "tilesets.json"), "w") as fh:
        json.dump(data, fh, indent=1)
    print("wrote data/tilesets.json")


if __name__ == "__main__":
    main()
