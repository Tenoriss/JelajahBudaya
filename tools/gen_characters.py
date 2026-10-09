"""gen_characters.py -- original character sprite sheets + dialogue portraits.

Style: chibi top-down 3/4-view pixel characters, 32x48 sprites, 8 directions x
6 frames (2 idle breathing + 4 walk).  The four diagonals are drawn as turned
3/4 views built on top of the cardinal body.  All designs are original game art; they
use abstract geometric textile motifs rather than reproducing any specific
community's sacred patterns.

Outputs:
  assets/characters/player.png
  assets/npcs/<id>.png
  assets/portraits/<id>.png
  data/characters.json
"""
from __future__ import annotations

import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artlib import Canvas, P, c, shade  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CH = os.path.join(ROOT, "assets", "characters")
OUT_NPC = os.path.join(ROOT, "assets", "npcs")
OUT_PORT = os.path.join(ROOT, "assets", "portraits")
OUT_DATA = os.path.join(ROOT, "data")

CW, CH = 32, 48
DIRS = ["down", "left", "right", "up",
        "down_left", "down_right", "up_left", "up_right"]
CARDINAL = ("down", "left", "right", "up")
FRAMES = 6          # 0,1 idle | 2,3,4,5 walk

# --------------------------------------------------------------------------
# character definitions
# --------------------------------------------------------------------------
CHARS = {
    "player": dict(
        skin="#e8b98a", hair="#33262c", hairstyle="short", shirt="#3f8f8a",
        shirt_alt="#2f6f6c", pants="#7a5a3a", shoes="#5e4028", accent="#d95f4a",
        accessory="scarf", hat=None, pattern=None, backpack=True, gender="m",
    ),
    # ---- Sumatra ---------------------------------------------------------
    "npc_aminah": dict(skin="#e0b184", hair="#3a2a2a", hairstyle="bun", shirt="#c05040",
                       shirt_alt="#a03c33", pants="#3a4a6a", shoes="#5e4028", accent="#e8c060",
                       accessory="shoulder_cloth", pattern="diamond", hat=None, gender="f"),
    "npc_datuak": dict(skin="#c99a6e", hair="#dedad2", hairstyle="long", shirt="#5a4a3a",
                       shirt_alt="#42362a", pants="#3a3028", shoes="#3a2c22", accent="#c9a06a",
                       accessory="sash", pattern="stripe", hat="ulos_cap", gender="m"),
    "npc_sari": dict(skin="#e8bd92", hair="#2f2425", hairstyle="ponytail", shirt="#e0803c",
                     shirt_alt="#c0652c", pants="#4a5a3a", shoes="#5e4028", accent="#f0d060",
                     accessory="apron", pattern=None, hat="straw", gender="f"),
    "npc_bujang": dict(skin="#d8a878", hair="#33262c", hairstyle="short", shirt="#7a4a8a",
                       shirt_alt="#5e3868", pants="#3a3a4a", shoes="#4a3020", accent="#e8c060",
                       accessory="instrument", pattern=None, hat=None, gender="m"),
    "npc_ida": dict(skin="#e8c29c", hair="#3a2c28", hairstyle="bun", shirt="#3a7a8a",
                    shirt_alt="#2c6070", pants="#6a4a3a", shoes="#5e4028", accent="#f0e0b0",
                    accessory="tray", pattern="dot", hat=None, gender="f"),
    # ---- Java ------------------------------------------------------------
    "npc_ki_bagus": dict(skin="#d2a274", hair="#e8e4dc", hairstyle="long", shirt="#6a4a2a",
                         shirt_alt="#4e3620", pants="#3a2c22", shoes="#3a2c22", accent="#c05040",
                         accessory="sash", pattern="batik", hat="blangkon", gender="m"),
    "npc_dewi": dict(skin="#e8bd92", hair="#2a2024", hairstyle="bun", shirt="#8a3a6a",
                     shirt_alt="#6c2c52", pants="#5a4a6a", shoes="#4a3020", accent="#e8c060",
                     accessory="selendang", pattern="batik", hat=None, gender="f"),
    "npc_pak_tarno": dict(skin="#cfa070", hair="#2f2a26", hairstyle="short", shirt="#6a7a4a",
                          shirt_alt="#505e36", pants="#4a3a2a", shoes="#3a2c22", accent="#d8c060",
                          accessory="apron", pattern=None, hat="straw", gender="m"),
    "npc_rara": dict(skin="#eabd8e", hair="#38262a", hairstyle="ponytail", shirt="#e8a03c",
                     shirt_alt="#c27f2a", pants="#4a4a5a", shoes="#4a3020", accent="#c05040",
                     accessory="none", pattern=None, hat=None, gender="f", child=True),
    "npc_mbah_karto": dict(skin="#c99a6e", hair="#d8d4cc", hairstyle="short", shirt="#4a4a5a",
                           shirt_alt="#383846", pants="#3a3028", shoes="#3a2c22", accent="#a89c84",
                           accessory="sash", pattern="batik", hat=None, gender="m", elder=True),
    # ---- Kalimantan ------------------------------------------------------
    "npc_lasan": dict(skin="#e0b184", hair="#2f2425", hairstyle="long", shirt="#3f7a5a",
                      shirt_alt="#2f5e44", pants="#5e4028", shoes="#3a2c22", accent="#e8d060",
                      accessory="beads", pattern="stripe", hat="feather", gender="m"),
    "npc_rini": dict(skin="#e8bd92", hair="#33262c", hairstyle="bun", shirt="#c96a3a",
                     shirt_alt="#a4532c", pants="#3a4a3a", shoes="#4a3020", accent="#e8c060",
                     accessory="basket", pattern="zigzag", hat=None, gender="f"),
    "npc_bapa_udi": dict(skin="#c99a6e", hair="#3a2f2a", hairstyle="short", shirt="#5a6a4a",
                         shirt_alt="#45543a", pants="#4a3a2a", shoes="#3a2c22", accent="#c9a06a",
                         accessory="paddle", pattern=None, hat="woven", gender="m"),
    "npc_tina": dict(skin="#e8c29c", hair="#2a2024", hairstyle="ponytail", shirt="#d96a8a",
                     shirt_alt="#b8506c", pants="#4a4a5a", shoes="#4a3020", accent="#f0e0b0",
                     accessory="none", pattern=None, hat=None, gender="f", child=True),
    # ---- Sulawesi --------------------------------------------------------
    "npc_rambu": dict(skin="#d8a878", hair="#33262c", hairstyle="long", shirt="#8a3a3a",
                      shirt_alt="#6c2c2c", pants="#3a3a4a", shoes="#3a2c22", accent="#e8c060",
                      accessory="sash", pattern="geometric", hat="headband", gender="f"),
    "npc_puang": dict(skin="#c99a6e", hair="#dedad2", hairstyle="short", shirt="#4a3a5a",
                      shirt_alt="#382c46", pants="#3a3028", shoes="#3a2c22", accent="#c05040",
                      accessory="staff", pattern=None, hat=None, gender="m", elder=True),
    "npc_dg_naba": dict(skin="#d8a878", hair="#2f2425", hairstyle="short", shirt="#3a6a8a",
                        shirt_alt="#2c5068", pants="#5e4a3a", shoes="#3a2c22", accent="#e8d060",
                        accessory="apron", pattern=None, hat="woven", gender="m"),
    "npc_yuliana": dict(skin="#e8bd92", hair="#3a2c28", hairstyle="bun", shirt="#e08a4a",
                        shirt_alt="#bc6c34", pants="#4a4a5a", shoes="#4a3020", accent="#c05040",
                        accessory="tray", pattern="zigzag", hat=None, gender="f"),
    # ---- Papua -----------------------------------------------------------
    "npc_yosia": dict(skin="#b07a4e", hair="#2a1f1e", hairstyle="curly", shirt="#c9762c",
                      shirt_alt="#a45c20", pants="#6a5a3a", shoes="#4a3020", accent="#e8d060",
                      accessory="beads", pattern="geometric", hat=None, gender="f"),
    "npc_petrus": dict(skin="#a8703f", hair="#241b1a", hairstyle="curly", shirt="#3f7a5a",
                       shirt_alt="#2f5e44", pants="#5e4a2a", shoes="#3a2c22", accent="#c05040",
                       accessory="spear", pattern="stripe", hat="feather", gender="m"),
    "npc_mama_lena": dict(skin="#b07a4e", hair="#2a1f1e", hairstyle="curly", shirt="#d96a3a",
                          shirt_alt="#b4522c", pants="#4a4a3a", shoes="#4a3020", accent="#e8c060",
                          accessory="basket", pattern="zigzag", hat=None, gender="f"),
    "npc_tomas": dict(skin="#a8703f", hair="#241b1a", hairstyle="curly", shirt="#5a6a8a",
                      shirt_alt="#44526c", pants="#5a5a4a", shoes="#3a2c22", accent="#e8d060",
                      accessory="none", pattern=None, hat=None, gender="m", child=True),
    # ---- wanderers / extras ---------------------------------------------
    "npc_pedagang": dict(skin="#d8a878", hair="#33262c", hairstyle="short", shirt="#e0b04a",
                         shirt_alt="#bc8f34", pants="#4a3a2a", shoes="#3a2c22", accent="#c05040",
                         accessory="basket", pattern=None, hat="straw", gender="m"),
    "npc_pengembara": dict(skin="#e0b184", hair="#4a3628", hairstyle="ponytail", shirt="#4a6a8a",
                           shirt_alt="#38506c", pants="#4a4a3a", shoes="#3a2c22", accent="#e8c060",
                           accessory="backpack", pattern=None, hat="hat", gender="f"),
    "npc_anak": dict(skin="#e8c29c", hair="#33262c", hairstyle="short", shirt="#7ac0d0",
                     shirt_alt="#5c9cae", pants="#5a4a3a", shoes="#4a3020", accent="#e8c060",
                     accessory="none", pattern=None, hat=None, gender="m", child=True),
    "npc_penjaga": dict(skin="#cfa070", hair="#2f2a26", hairstyle="short", shirt="#8a5a3a",
                        shirt_alt="#6c4229", pants="#3a3028", shoes="#3a2c22", accent="#c9a06a",
                        accessory="sash", pattern="stripe", hat="headband", gender="m"),
    "npc_guru": dict(skin="#e8c29c", hair="#d8d4cc", hairstyle="bun", shirt="#5a7a8a",
                     shirt_alt="#44606e", pants="#3a3a4a", shoes="#3a2c22", accent="#e8c060",
                     accessory="book", pattern="dot", hat=None, gender="f", elder=True),
    "npc_nelayan": dict(skin="#c99a6e", hair="#2f2a26", hairstyle="short", shirt="#3a6a6a",
                        shirt_alt="#2c5252", pants="#5a4a3a", shoes="#3a2c22", accent="#e8d060",
                        accessory="net", pattern=None, hat="woven", gender="m"),
    "npc_penari": dict(skin="#e8bd92", hair="#2a2024", hairstyle="bun", shirt="#c0507a",
                       shirt_alt="#9c3c5e", pants="#6a4a6a", shoes="#4a3020", accent="#e8c060",
                       accessory="selendang", pattern="batik", hat="headband", gender="f"),
    "npc_pengrajin": dict(skin="#d8a878", hair="#33262c", hairstyle="short", shirt="#6a5a4a",
                          shirt_alt="#524336", pants="#4a3a2a", shoes="#3a2c22", accent="#e8c060",
                          accessory="apron", pattern="geometric", hat=None, gender="m"),
    "npc_koki": dict(skin="#e8bd92", hair="#3a2c28", hairstyle="bun", shirt="#f0e0d0",
                     shirt_alt="#d8c4b0", pants="#4a4a5a", shoes="#4a3020", accent="#c05040",
                     accessory="apron", pattern=None, hat="bandana", gender="f"),
}


# --------------------------------------------------------------------------
# drawing
# --------------------------------------------------------------------------
def limb(cv, x0, y0, x1, y1, col, w=3):
    cv.line([(x0, y0), (x1, y1)], col, w)


def draw_char(spec: dict, direction: str, frame: int, seed=0) -> Canvas:
    """One 32x48 frame.  Chibi 3/4 view, readable at 2-4x zoom."""
    cv = Canvas(CW, CH)
    diagonal = ""
    if direction not in CARDINAL:
        # diagonals reuse the cardinal body of their horizontal side, then get a
        # turned head so the character clearly faces the diagonal
        diagonal = direction
        direction = "left" if direction.endswith("left") else "right"
    skin = spec["skin"]
    skin_d = shade(skin, -0.2)
    hair = spec["hair"]
    shirt = spec["shirt"]
    shirt_d = spec.get("shirt_alt") or shade(shirt, -0.22)
    shirt_l = shade(shirt, 0.2)
    pants = spec["pants"]
    pants_d = shade(pants, -0.18)
    shoes = spec["shoes"]
    accent = spec.get("accent", "#e8c060")
    child = spec.get("child", False)
    elder = spec.get("elder", False)

    # vertical layout (sprite is 32x48)
    head_r = 8 if not child else 7
    ground = CH - 2
    if child:
        body_bot = ground - 12
    else:
        body_bot = ground - 11
    body_top = body_bot - 15
    head_cy = body_top - head_r + 1
    hx = 16

    # ---- walk cycle -----------------------------------------------------
    if frame < 2:
        bob = frame                      # 0 or 1
        step = 0
        swing = 0
    else:
        cyc = (frame - 2) % 4
        bob = [0, 1, 0, 1][cyc]
        step = [1, 0, -1, 0][cyc]
        swing = [1, 0, -1, 0][cyc]
    head_cy -= bob
    body_top -= bob
    body_bot -= bob

    # ---- shadow ---------------------------------------------------------
    cv.ellipse(hx - 9, ground - 3, hx + 9, ground + 1, (40, 32, 40, 70))

    # ---- legs -----------------------------------------------------------
    leg_top = body_bot - 2
    leg_bot = ground - 3
    lx, rx = 12, 19
    if direction in ("left", "right"):
        fwd = 1 if direction == "right" else -1
        cv.rect(lx + step * fwd - 2, leg_top, lx + step * fwd + 1, leg_bot, pants)
        cv.rect(rx - step * fwd - 2, leg_top, rx - step * fwd + 1, leg_bot, pants_d)
        cv.rect(lx + step * fwd - 3, leg_bot, lx + step * fwd + 2, leg_bot + 2, shoes)
        cv.rect(rx - step * fwd - 3, leg_bot, rx - step * fwd + 2, leg_bot + 2, shade(shoes, -0.15))
    else:
        lo = abs(step)
        cv.rect(lx - 2, leg_top, lx + 1, leg_bot - lo, pants)
        cv.rect(rx - 2, leg_top, rx + 1, leg_bot - (1 if step else 0), pants_d)
        cv.rect(lx - 3, leg_bot - lo, lx + 2, leg_bot + 2 - lo, shoes)
        cv.rect(rx - 3, leg_bot - (1 if step else 0), rx + 2, leg_bot + 2 - (1 if step else 0),
                shade(shoes, -0.15))

    # ---- arms (drawn behind torso for up / at sides otherwise) ----------
    arm_top = body_top + 2
    arm_bot = body_bot - 1
    for side, ax in ((0, 9), (1, 22)):
        sw = swing * (1 if side == 0 else -1)
        if direction == "up":
            cv.rect(ax - 2, arm_top, ax + 1, arm_bot, shade(shirt, -0.15))
        else:
            cv.rect(ax - 2, arm_top + abs(sw) * 0, ax + 1, arm_bot + sw, shirt_d if side else shade(shirt, -0.05))
            cv.rect(ax - 2, arm_bot + sw - 1, ax + 1, arm_bot + sw + 2, skin)

    # ---- torso ----------------------------------------------------------
    cv.rect(10, body_top, 21, body_bot, shirt)
    cv.rect(10, body_top, 21, body_top + 1, shirt_l)
    cv.rect(10, body_bot - 2, 21, body_bot, shirt_d)
    cv.rect(10, body_top, 10, body_bot, shirt_l)
    cv.rect(21, body_top, 21, body_bot, shirt_d)

    # cloth pattern (abstract geometric motifs -- original game art)
    pat = spec.get("pattern")
    if pat == "batik":
        for i in range(3):
            for k in range(3):
                cv.px(12 + k * 4, body_top + 3 + i * 4, accent)
                cv.px(13 + k * 4, body_top + 4 + i * 4, accent)
    elif pat == "stripe":
        for i in range(4):
            cv.rect(11, body_top + 2 + i * 3, 20, body_top + 2 + i * 3, shade(shirt, -0.28))
    elif pat == "diamond":
        for i in range(2):
            for k in range(2):
                x, y = 12 + k * 6, body_top + 4 + i * 6
                cv.px(x + 1, y, accent)
                cv.px(x, y + 1, accent)
                cv.px(x + 2, y + 1, accent)
                cv.px(x + 1, y + 2, accent)
    elif pat == "zigzag":
        for i in range(3):
            y = body_top + 3 + i * 5
            for k in range(4):
                cv.px(11 + k * 3 + (i % 2), y + (k % 2), accent)
    elif pat == "geometric":
        for i in range(3):
            cv.rect(11, body_top + 3 + i * 5, 20, body_top + 4 + i * 5, accent)
            cv.rect(13, body_top + 5 + i * 5, 18, body_top + 5 + i * 5, accent)
    elif pat == "dot":
        for i in range(3):
            for k in range(3):
                cv.px(11 + k * 4, body_top + 3 + i * 4, accent)

    # ---- accessory ------------------------------------------------------
    acc = spec.get("accessory")
    if acc == "sash":
        cv.line([(11, body_top + 1), (20, body_bot - 1)], accent, 2)
    elif acc == "shoulder_cloth":
        cv.rect(9, body_top - 1, 22, body_top + 2, accent)
        for k in range(4):
            cv.px(11 + k * 3, body_top + 1, shade(accent, -0.4))
        cv.rect(9, body_top + 2, 12, body_top + 9, accent)
        for k in range(3):
            cv.px(10, body_top + 3 + k * 2, shade(accent, -0.3))
    elif acc == "selendang":
        cv.rect(8, body_top - 1, 23, body_top + 1, accent)
        cv.rect(8, body_top + 1, 10, body_bot - 2, accent)
        cv.rect(21, body_top + 1, 23, body_bot, accent)
    elif acc == "apron":
        cv.rect(12, body_top + 5, 19, body_bot, "#e0d0b0")
        cv.rect(12, body_top + 5, 19, body_top + 6, "#f0e6cc")
        cv.rect(14, body_top + 8, 17, body_bot - 2, "#f0e6cc")
    elif acc == "scarf":
        cv.rect(10, body_top, 21, body_top + 2, accent)
        cv.rect(18, body_top + 2, 21, body_top + 7, accent)
        cv.rect(18, body_top + 2, 19, body_top + 7, shade(accent, 0.25))
    elif acc == "beads":
        for k in range(6):
            cv.px(11 + k * 2, body_top + 1, "#f0e8d8" if k % 2 else accent)
    elif acc == "basket":
        cv.rect(22, body_top + 3, 27, body_bot - 2, "#c9a06a")
        for k in range(3):
            cv.rect(22, body_top + 4 + k * 3, 27, body_top + 5 + k * 3, "#a87f52")
    elif acc == "tray":
        cv.rect(4, body_bot - 3, 9, body_bot, "#c9a06a")
        cv.ellipse(4, body_bot - 6, 8, body_bot - 2, "#d8634a")
    elif acc == "instrument":
        cv.rect(23, body_top + 2, 28, body_top + 14, "#a8763e")
        cv.ellipse(24, body_top, 28, body_top + 4, "#d8b060")
    elif acc == "book":
        cv.rect(22, body_top + 4, 27, body_top + 10, "#8a5a3a")
        cv.rect(23, body_top + 5, 26, body_top + 9, "#e8dcc0")
    elif acc == "net":
        for k in range(4):
            cv.line([(6, body_top + 2 + k * 2), (11, body_top + 4 + k * 2)], "#d8d0c0", 1)
    elif acc == "paddle":
        cv.line([(25, body_top + 1), (28, body_bot + 3)], "#a8763e", 2)
        cv.poly([(26, body_bot + 1), (30, body_bot + 7), (25, body_bot + 7)], "#c9a06a")
    elif acc == "staff":
        cv.rect(24, body_top - 5, 25, body_bot + 2, "#8a6440")
        cv.ellipse(22, body_top - 8, 27, body_top - 3, accent)
    elif acc == "spear":
        cv.rect(24, body_top - 8, 25, body_bot + 1, "#8a6440")
        cv.poly([(23, body_top - 8), (26, body_top - 8), (24, body_top - 13)], "#c8c8c0")

    if spec.get("backpack"):
        cv.rect(8, body_top + 1, 10, body_bot - 2, "#8a5a3a")
        cv.rect(9, body_top + 4, 10, body_top + 8, "#c9a06a")

    # ---- head -----------------------------------------------------------
    cv.ellipse(hx - head_r, head_cy - head_r, hx + head_r - 1, head_cy + head_r, skin)
    cv.ellipse(hx - head_r + 1, head_cy - head_r, hx + head_r - 2, head_cy + head_r - 2, skin)

    # ears
    if direction == "left":
        cv.ellipse(hx - head_r - 1, head_cy - 1, hx - head_r + 1, head_cy + 3, skin_d)
    elif direction == "right":
        cv.ellipse(hx + head_r - 1, head_cy - 1, hx + head_r + 1, head_cy + 3, skin_d)
    elif direction == "down":
        cv.ellipse(hx - head_r - 1, head_cy - 1, hx - head_r + 1, head_cy + 3, skin_d)
        cv.ellipse(hx + head_r - 1, head_cy - 1, hx + head_r + 1, head_cy + 3, skin_d)

    # ---- hair -----------------------------------------------------------
    style = spec.get("hairstyle", "short")
    if style == "curly":
        cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 1, hair)
        for i in range(13):
            a = math.pi + i * (math.pi / 12)
            px = hx + int((head_r + 1) * math.cos(a))
            py = head_cy - 1 + int((head_r + 1) * math.sin(a) * 0.95)
            cv.ellipse(px - 2, py - 2, px + 2, py + 2, hair if i % 2 else shade(hair, 0.18))
        cv.ellipse(hx - head_r - 1, head_cy - 4, hx - head_r + 2, head_cy + 4, hair)
        cv.ellipse(hx + head_r - 2, head_cy - 4, hx + head_r + 1, head_cy + 4, hair)
        cv.rect(hx - head_r - 1, head_cy - head_r - 3, hx + head_r, head_cy - head_r - 1, hair)
    elif style == "long":
        cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 2, hair)
        cv.rect(hx - head_r - 1, head_cy - 2, hx - head_r + 1, head_cy + 9, hair)
        cv.rect(hx + head_r - 2, head_cy - 2, hx + head_r, head_cy + 9, hair)
        cv.rect(hx - head_r - 1, head_cy + 7, hx + head_r, head_cy + 9, hair)
        cv.ellipse(hx - 7, head_cy - head_r - 3, hx + 6, head_cy - 2, shade(hair, 0.14))
    elif style == "bun":
        cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 2, hair)
        cv.ellipse(hx - 4, head_cy - head_r - 6, hx + 4, head_cy - head_r + 1, hair)
        cv.ellipse(hx - 3, head_cy - head_r - 5, hx + 2, head_cy - head_r - 1, shade(hair, 0.16))
        cv.rect(hx - head_r - 1, head_cy - 2, hx - head_r + 1, head_cy + 4, hair)
        cv.rect(hx + head_r - 2, head_cy - 2, hx + head_r, head_cy + 4, hair)
        cv.ellipse(hx - 7, head_cy - head_r - 3, hx + 6, head_cy - 2, shade(hair, 0.14))
    elif style == "ponytail":
        cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 2, hair)
        cv.rect(hx - head_r - 1, head_cy - 2, hx - head_r + 1, head_cy + 4, hair)
        cv.rect(hx + head_r - 2, head_cy - 2, hx + head_r, head_cy + 4, hair)
        cv.rect(hx + head_r, head_cy - 5, hx + head_r + 3, head_cy + 6, hair)
        cv.ellipse(hx + head_r, head_cy + 4, hx + head_r + 3, head_cy + 9, hair)
        cv.ellipse(hx - 7, head_cy - head_r - 3, hx + 6, head_cy - 2, shade(hair, 0.14))
    else:  # short
        cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 2, hair)
        cv.rect(hx - head_r - 1, head_cy - 3, hx - head_r + 1, head_cy + 2, hair)
        cv.rect(hx + head_r - 2, head_cy - 3, hx + head_r, head_cy + 2, hair)
        cv.ellipse(hx - 7, head_cy - head_r - 3, hx + 6, head_cy - 2, shade(hair, 0.16))

    # side fringe strands over the forehead
    if style not in ("curly",):
        for k in range(3):
            fx = hx - head_r + 1 + k * 5
            cv.px(fx, head_cy - 2, hair)
            cv.px(fx + 1, head_cy - 2, hair)
    if elder:
        cv.rect(hx - head_r - 1, head_cy - head_r - 1, hx + head_r, head_cy - head_r, hair)

    # ---- face -----------------------------------------------------------
    eye = "#33262c"
    if direction == "down":
        cv.rect(hx - 4, head_cy, hx - 3, head_cy + 2, eye)
        cv.rect(hx + 3, head_cy, hx + 4, head_cy + 2, eye)
        cv.px(hx - 4, head_cy, "#ffffff")
        cv.px(hx + 3, head_cy, "#ffffff")
        cv.rect(hx - 1, head_cy + 4, hx + 1, head_cy + 4, shade(skin, -0.35))
        if elder:
            cv.ellipse(hx - 5, head_cy + 3, hx + 4, head_cy + 8, hair)
        cv.px(hx - 6, head_cy + 3, shade(skin, -0.08))
        cv.px(hx + 6, head_cy + 3, shade(skin, -0.08))
    elif direction == "left":
        cv.rect(hx - 6, head_cy, hx - 4, head_cy + 2, eye)
        cv.px(hx - 6, head_cy, "#ffffff")
        cv.rect(hx - head_r - 2, head_cy + 2, hx - head_r - 1, head_cy + 3, skin_d)
        cv.rect(hx - 2, head_cy + 4, hx, head_cy + 4, shade(skin, -0.3))
    elif direction == "right":
        cv.rect(hx + 3, head_cy, hx + 5, head_cy + 2, eye)
        cv.px(hx + 5, head_cy, "#ffffff")
        cv.rect(hx + head_r, head_cy + 2, hx + head_r + 1, head_cy + 3, skin_d)
        cv.rect(hx - 1, head_cy + 4, hx + 1, head_cy + 4, shade(skin, -0.3))
    else:  # up -> back of head, no face
        cv.ellipse(hx - head_r, head_cy - head_r + 1, hx + head_r - 1, head_cy + head_r - 2, hair)
        cv.ellipse(hx - 6, head_cy - head_r, hx + 5, head_cy + 3, shade(hair, 0.14))

    if diagonal != "":
        # 3/4-view head: turned towards the diagonal, both eyes visible
        look_up = diagonal.startswith("up")
        turn = -1 if diagonal.endswith("left") else 1
        cv.ellipse(hx - head_r, head_cy - head_r, hx + head_r - 1, head_cy + head_r, skin)
        cv.ellipse(hx - 6, head_cy + 3, hx + 5, head_cy + 7, shade(skin, -0.06))
        if look_up:
            # away from the camera: mostly hair, a sliver of cheek on the near side
            cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy + head_r - 3, hair)
            cv.ellipse(hx - 6, head_cy - head_r + 1, hx + 5, head_cy + 1, shade(hair, 0.15))
            cv.ellipse(hx + turn * 4 - 2, head_cy + 2, hx + turn * 4 + 2, head_cy + 5, skin)
            cv.rect(hx - head_r - 1, head_cy - head_r - 1, hx + head_r, head_cy - head_r + 1, hair)
        else:
            cv.ellipse(hx - head_r - 1, head_cy - head_r - 2, hx + head_r, head_cy - 3, hair)
            cv.rect(hx + head_r - 2, head_cy - 3, hx + head_r, head_cy + 2, hair)
            cv.rect(hx - head_r - 1, head_cy - 3, hx - head_r + 1, head_cy + 3, hair)
            if elder:
                cv.ellipse(hx - 5, head_cy + 4, hx + 4, head_cy + 8, hair)
            # eyes: near eye open and low, far eye smaller
            ex_near = hx + turn * 3
            ex_far = hx - turn * 3
            cv.rect(ex_near - 1, head_cy, ex_near + 1, head_cy + 2, "#33262c")
            cv.px(ex_near - 1, head_cy, "#ffffff")
            cv.rect(ex_far - 1, head_cy + 1, ex_far, head_cy + 2, "#33262c")
            cv.rect(hx - 1, head_cy + 4, hx + 1, head_cy + 4, shade(skin, -0.32))
            cv.px(hx - turn * 6, head_cy + 3, shade(skin, -0.08))

    # ---- hat ------------------------------------------------------------
    hat = spec.get("hat")
    if hat and direction != "up":
        if hat == "straw":
            cv.ellipse(hx - 12, head_cy - head_r - 1, hx + 12, head_cy - head_r + 5, "#c9a860")
            cv.ellipse(hx - 12, head_cy - head_r - 1, hx + 12, head_cy - head_r + 2, "#dcbe74")
            cv.ellipse(hx - 6, head_cy - head_r - 6, hx + 6, head_cy - head_r + 1, "#c9a860")
            cv.ellipse(hx - 6, head_cy - head_r - 6, hx + 6, head_cy - head_r - 2, "#dcbe74")
        elif hat == "woven":
            cv.ellipse(hx - 10, head_cy - head_r - 2, hx + 10, head_cy - head_r + 4, "#b8a068")
            cv.ellipse(hx - 5, head_cy - head_r - 6, hx + 5, head_cy - head_r + 1, "#c9b078")
            for k in range(4):
                cv.px(hx - 3 + k * 2, head_cy - head_r - 4, "#a08a58")
        elif hat == "blangkon":
            cv.ellipse(hx - 9, head_cy - head_r - 2, hx + 9, head_cy - head_r + 4, "#6a4a2a")
            cv.ellipse(hx - 7, head_cy - head_r - 4, hx + 7, head_cy - head_r + 1, "#7d5a36")
            cv.ellipse(hx + 4, head_cy - head_r - 6, hx + 10, head_cy - head_r - 1, "#7d5a36")
            cv.rect(hx - 9, head_cy - head_r, hx + 9, head_cy - head_r + 1, "#5a3e22")
        elif hat == "headband":
            cv.rect(hx - head_r, head_cy - head_r + 1, hx + head_r - 1, head_cy - head_r + 3, accent)
            cv.rect(hx - head_r, head_cy - head_r + 2, hx + head_r - 1, head_cy - head_r + 2, shade(accent, -0.3))
        elif hat == "feather":
            cv.rect(hx - head_r, head_cy - head_r + 1, hx + head_r - 1, head_cy - head_r + 3, accent)
            cv.poly([(hx + 2, head_cy - head_r), (hx + 5, head_cy - head_r - 9), (hx + 8, head_cy - head_r - 1)], "#e8e0d0")
            cv.poly([(hx + 3, head_cy - head_r - 1), (hx + 5, head_cy - head_r - 7), (hx + 7, head_cy - head_r - 1)], "#c05040")
            cv.poly([(hx - 3, head_cy - head_r), (hx - 6, head_cy - head_r - 8), (hx - 8, head_cy - head_r - 1)], "#e8e0d0")
        elif hat == "bandana":
            cv.rect(hx - head_r, head_cy - head_r + 1, hx + head_r - 1, head_cy - head_r + 3, "#c05040")
            cv.rect(hx - head_r, head_cy - head_r + 1, hx + head_r - 1, head_cy - head_r + 2, "#d9685a")
        elif hat == "ulos_cap":
            cv.ellipse(hx - 9, head_cy - head_r - 2, hx + 9, head_cy - head_r + 3, "#3a3a4a")
            for k in range(4):
                cv.px(hx - 6 + k * 4, head_cy - head_r + 1, accent)
        elif hat == "hat":
            cv.ellipse(hx - 11, head_cy - head_r - 1, hx + 11, head_cy - head_r + 4, "#8a6a44")
            cv.ellipse(hx - 6, head_cy - head_r - 6, hx + 6, head_cy - head_r + 1, "#a8834f")
            cv.rect(hx - 7, head_cy - head_r - 3, hx + 7, head_cy - head_r - 2, "#c9a06a")
        elif hat == "bandana_top":
            pass

    cv.outline("#2b2026", alpha_test=70)
    return cv


def draw_sheet(spec: dict, cid: str) -> Canvas:
    sheet = Canvas(CW * FRAMES, CH * len(DIRS))
    for row, d in enumerate(DIRS):
        for f in range(FRAMES):
            frame = draw_char(spec, d, f, seed=row * 10 + f)
            sheet.paste(frame, f * CW, row * CH)
    return sheet


def draw_portrait(spec: dict, size=72) -> Canvas:
    """Dialogue bust portrait: clear face, expressive eyes, per-character hair."""
    cv = Canvas(size, size)
    skin = spec["skin"]
    skin_d = shade(skin, -0.22)
    skin_l = shade(skin, 0.12)
    hair = spec["hair"]
    shirt = spec["shirt"]
    accent = spec.get("accent", "#e8c060")
    elder = spec.get("elder", False)
    child = spec.get("child", False)

    # ---- background plate (warm, subtle batik-ish corner ornaments) -----
    for y in range(size):
        t = y / size
        cv.rect(0, y, size - 1, y, shade("#6a4a4e", -0.18 + 0.30 * t))
    for i in range(0, size, 6):
        cv.rect(i, 0, i, size - 1, shade("#6a4a4e", 0.04))
    for (ox, oy) in ((6, 6), (size - 20, 6), (6, size - 20), (size - 20, size - 20)):
        for k in range(3):
            cv.px(ox + k * 5, oy + 5, shade(accent, -0.25))
            cv.px(ox + 5, oy + k * 5, shade(accent, -0.25))
    cv.rect(0, 0, size - 1, size - 1, "#3a2c32")
    cv.rect(1, 1, size - 2, size - 2, "#d8b060")
    cv.rect(2, 2, size - 3, size - 3, "#3a2c32")

    head_r = 18 if not child else 16
    hx = size // 2
    hy = size // 2 - 6

    # ---- shoulders / torso ---------------------------------------------
    cv.ellipse(hx - 28, hy + 22, hx + 28, size + 16, shirt)
    cv.ellipse(hx - 26, hy + 25, hx + 26, size + 14, shade(shirt, 0.06))
    # collar
    cv.poly([(hx - 13, hy + 19), (hx, hy + 27), (hx + 13, hy + 19)], shade(shirt, -0.18))
    cv.poly([(hx - 11, hy + 19), (hx, hy + 25), (hx + 11, hy + 19)], shade(shirt, 0.22))
    # accessory hint on the shoulders
    acc = spec.get("accessory")
    if acc in ("selendang", "shoulder_cloth", "sash"):
        cv.poly([(hx - 26, hy + 26), (hx - 18, hy + 22), (hx - 16, size - 2), (hx - 27, size - 2)], accent)
        cv.poly([(hx + 18, hy + 22), (hx + 26, hy + 26), (hx + 27, size - 2), (hx + 16, size - 2)], accent)
        for k in range(3):
            cv.px(hx - 22 + k, hy + 30 + k * 2, shade(accent, -0.3))
            cv.px(hx + 22 - k, hy + 30 + k * 2, shade(accent, -0.3))

    # ---- neck -----------------------------------------------------------
    cv.rect(hx - 6, hy + 10, hx + 6, hy + 22, shade(skin, -0.1))
    cv.rect(hx - 6, hy + 18, hx + 6, hy + 22, shade(skin, -0.22))

    # ---- head -----------------------------------------------------------
    cv.ellipse(hx - head_r, hy - head_r - 1, hx + head_r, hy + head_r + 1, skin)
    cv.ellipse(hx - head_r + 1, hy - head_r, hx + head_r - 1, hy + head_r, skin)
    cv.ellipse(hx - head_r + 2, hy - head_r + 2, hx - head_r + 6, hy + 2, skin_l)   # cheek light
    # ears
    cv.ellipse(hx - head_r - 2, hy - 2, hx - head_r + 2, hy + 6, skin_d)
    cv.ellipse(hx + head_r - 2, hy - 2, hx + head_r + 2, hy + 6, skin_d)

    # ---- hair -----------------------------------------------------------
    style = spec.get("hairstyle", "short")
    if style == "curly":
        cv.ellipse(hx - head_r - 2, hy - head_r - 4, hx + head_r + 2, hy + 2, hair)
        for i in range(16):
            a = math.pi + i * (math.pi / 15)
            px = hx + int((head_r + 2) * math.cos(a))
            py = hy - 3 + int((head_r + 2) * math.sin(a) * 0.95)
            cv.ellipse(px - 4, py - 4, px + 4, py + 4, hair if i % 2 else shade(hair, 0.2))
        cv.ellipse(hx - head_r - 2, hy - 6, hx - head_r + 4, hy + 6, hair)
        cv.ellipse(hx + head_r - 4, hy - 6, hx + head_r + 2, hy + 6, hair)
    elif style == "long":
        cv.ellipse(hx - head_r - 3, hy - head_r - 5, hx + head_r + 3, hy + 2, hair)
        cv.rect(hx - head_r - 3, hy - 4, hx - head_r + 3, hy + 24, hair)
        cv.rect(hx + head_r - 2, hy - 4, hx + head_r + 3, hy + 24, hair)
        cv.ellipse(hx - head_r - 1, hy - head_r - 3, hx + head_r - 1, hy - 4, shade(hair, 0.16))
    elif style == "bun":
        cv.ellipse(hx - head_r - 3, hy - head_r - 5, hx + head_r + 3, hy + 2, hair)
        cv.ellipse(hx - 9, hy - head_r - 14, hx + 9, hy - head_r + 3, hair)
        cv.ellipse(hx - 7, hy - head_r - 12, hx + 4, hy - head_r - 1, shade(hair, 0.18))
        cv.ellipse(hx - head_r - 1, hy - head_r - 3, hx + head_r - 1, hy - 4, shade(hair, 0.16))
    elif style == "ponytail":
        cv.ellipse(hx - head_r - 3, hy - head_r - 5, hx + head_r + 3, hy + 2, hair)
        cv.rect(hx + head_r - 2, hy - 8, hx + head_r + 6, hy + 18, hair)
        cv.ellipse(hx + head_r - 1, hy + 14, hx + head_r + 6, hy + 24, hair)
        cv.ellipse(hx - head_r - 1, hy - head_r - 3, hx + head_r - 1, hy - 4, shade(hair, 0.16))
    else:
        cv.ellipse(hx - head_r - 3, hy - head_r - 5, hx + head_r + 3, hy + 1, hair)
        cv.rect(hx - head_r - 3, hy - 6, hx - head_r + 4, hy + 4, hair)
        cv.rect(hx + head_r - 3, hy - 6, hx + head_r + 3, hy + 4, hair)
        cv.ellipse(hx - 10, hy - head_r - 5, hx + 9, hy - 4, shade(hair, 0.16))
    # fringe
    if style != "curly":
        cv.ellipse(hx - head_r, hy - head_r + 2, hx - 2, hy - 1, hair)
        cv.ellipse(hx + 1, hy - head_r + 1, hx + head_r, hy - 2, hair)

    # ---- eyes -----------------------------------------------------------
    ex = 7
    eye_y = hy - 1
    for sx in (-1, 1):
        cx = hx + sx * ex
        cv.ellipse(cx - 4, eye_y - 4, cx + 4, eye_y + 3, "#f6f1e6")
        cv.ellipse(cx - 3, eye_y - 3, cx + 3, eye_y + 2, "#5c6a78")
        cv.rect(cx - 2, eye_y - 2, cx + 2, eye_y + 1, shade(hair, -0.06))
        cv.px(cx - 2, eye_y - 2, "#ffffff")
        cv.px(cx - 1, eye_y - 1, "#ffffff")
        cv.rect(cx - 4, eye_y - 4, cx + 4, eye_y - 3, shade(hair, 0.05))   # upper lid
        # eyebrow
        cv.rect(cx - 4, eye_y - 7, cx + 3, eye_y - 6, shade(hair, -0.12))
        if elder:
            cv.px(cx - 5, eye_y - 6, shade(hair, 0.3))
            cv.px(cx + 4, eye_y - 6, shade(hair, 0.3))
    # nose + mouth
    cv.rect(hx, eye_y + 5, hx + 1, eye_y + 7, shade(skin, -0.22))
    cv.rect(hx - 2, eye_y + 10, hx + 2, eye_y + 10, shade(skin, -0.45))
    cv.px(hx - 3, eye_y + 9, shade(skin, -0.35))
    cv.px(hx + 3, eye_y + 9, shade(skin, -0.35))
    # cheeks
    cv.ellipse(hx - 13, eye_y + 4, hx - 8, eye_y + 8, shade(skin, -0.1))
    cv.ellipse(hx + 8, eye_y + 4, hx + 13, eye_y + 8, shade(skin, -0.1))

    if elder:
        cv.ellipse(hx - 9, eye_y + 8, hx + 9, hy + 20, hair)
        cv.ellipse(hx - 7, eye_y + 9, hx + 7, hy + 18, shade(hair, 0.18))
        cv.rect(hx - 7, eye_y + 11, hx + 7, eye_y + 12, shade(hair, -0.2))
        cv.rect(hx - 4, eye_y + 10, hx + 4, eye_y + 10, shade(skin, -0.3))
        for k in range(3):  # wrinkles
            cv.px(hx - 12, eye_y + 1 + k * 2, shade(skin, -0.18))
            cv.px(hx + 12, eye_y + 1 + k * 2, shade(skin, -0.18))
    if child:
        cv.ellipse(hx - 13, eye_y + 3, hx - 9, eye_y + 6, shade(skin, -0.06))
        cv.ellipse(hx + 9, eye_y + 3, hx + 13, eye_y + 6, shade(skin, -0.06))

    # ---- hat / headband --------------------------------------------------
    hat = spec.get("hat")
    if hat in ("headband", "feather"):
        cv.rect(hx - head_r - 1, hy - head_r, hx + head_r + 1, hy - head_r + 3, accent)
        cv.rect(hx - head_r - 1, hy - head_r + 2, hx + head_r + 1, hy - head_r + 3, shade(accent, -0.3))
        if hat == "feather":
            cv.poly([(hx + 4, hy - head_r), (hx + 12, hy - head_r - 18), (hx + 16, hy - head_r + 1)], "#e8e0d0")
            cv.poly([(hx + 6, hy - head_r), (hx + 12, hy - head_r - 13), (hx + 14, hy - head_r)], "#c05040")
            cv.poly([(hx - 5, hy - head_r), (hx - 10, hy - head_r - 12), (hx - 13, hy - head_r + 1)], "#e8e0d0")
    elif hat == "bandana":
        cv.rect(hx - head_r - 1, hy - head_r, hx + head_r + 1, hy - head_r + 4, "#c05040")
        cv.rect(hx - head_r - 1, hy - head_r, hx + head_r + 1, hy - head_r + 2, "#d9685a")
    elif hat == "blangkon":
        cv.ellipse(hx - head_r - 2, hy - head_r - 5, hx + head_r + 2, hy - head_r + 4, "#6a4a2a")
        cv.ellipse(hx - head_r, hy - head_r - 6, hx + head_r - 2, hy - head_r + 1, "#7d5a36")
        cv.ellipse(hx + 6, hy - head_r - 9, hx + head_r + 4, hy - head_r - 1, "#7d5a36")
    elif hat == "straw":
        cv.ellipse(hx - 24, hy - head_r - 2, hx + 24, hy - head_r + 6, "#c9a860")
        cv.ellipse(hx - 24, hy - head_r - 2, hx + 24, hy - head_r + 3, "#dcbe74")
        cv.ellipse(hx - 13, hy - head_r - 9, hx + 13, hy - head_r + 2, "#c9a860")
        cv.ellipse(hx - 13, hy - head_r - 9, hx + 13, hy - head_r - 3, "#dcbe74")
    elif hat == "woven":
        cv.ellipse(hx - 19, hy - head_r - 3, hx + 19, hy - head_r + 5, "#b8a068")
        cv.ellipse(hx - 11, hy - head_r - 9, hx + 11, hy - head_r + 2, "#c9b078")
        for k in range(5):
            cv.px(hx - 7 + k * 4, hy - head_r - 6, "#a08a58")
    elif hat == "ulos_cap":
        cv.ellipse(hx - 18, hy - head_r - 4, hx + 18, hy - head_r + 4, "#3a3a4a")
        for k in range(5):
            cv.px(hx - 10 + k * 5, hy - head_r, accent)
    elif hat == "hat":
        cv.ellipse(hx - 22, hy - head_r - 2, hx + 22, hy - head_r + 5, "#8a6a44")
        cv.ellipse(hx - 12, hy - head_r - 9, hx + 12, hy - head_r + 2, "#a8834f")
        cv.rect(hx - 13, hy - head_r - 4, hx + 13, hy - head_r - 2, "#c9a06a")

    cv.outline("#2b2026", alpha_test=70)
    return cv


def build():
    os.makedirs(OUT_CH, exist_ok=True)
    os.makedirs(OUT_NPC, exist_ok=True)
    os.makedirs(OUT_PORT, exist_ok=True)
    data = {}
    for cid, spec in CHARS.items():
        sheet = draw_sheet(spec, cid)
        port = draw_portrait(spec)
        folder = OUT_CH if cid == "player" else OUT_NPC
        name = "player" if cid == "player" else cid.replace("npc_", "")
        sheet.save(os.path.join(folder, name + ".png"))
        port.save(os.path.join(OUT_PORT, name + ".png"))
        data[cid] = {
            "sheet": f"assets/{'characters' if cid=='player' else 'npcs'}/{name}.png",
            "portrait": f"assets/portraits/{name}.png",
            "frame_w": CW, "frame_h": CH, "columns": FRAMES, "rows": len(DIRS),
            "directions": DIRS,
            "idle_frames": [0, 1],
            "walk_frames": [2, 3, 4, 5],
        }
    with open(os.path.join(OUT_DATA, "characters.json"), "w") as fh:
        json.dump(data, fh, indent=1)
    print(f"wrote {len(data)} characters + portraits + data/characters.json")


if __name__ == "__main__":
    build()
