"""gen_ui.py -- original UI art: ornamental panels, buttons, bars, map parchment.

Outputs to assets/ui/.  Panels are 9-slice friendly (uniform, symmetric borders).

Run: python3 tools/gen_ui.py
"""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artlib import Canvas, c, shade  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "ui")


def panel(w, h, fill, border, border2, ornament=None, corner=10):
    cv = Canvas(w, h)
    cv.rect(0, 0, w - 1, h - 1, border2)
    cv.rect(1, 1, w - 2, h - 2, border)
    cv.rect(2, 2, w - 3, h - 3, fill)
    # inner shading
    cv.rect(2, 2, w - 3, 4, shade(fill, 0.10))
    cv.rect(2, h - 5, w - 3, h - 3, shade(fill, -0.16))
    cv.rect(2, 2, 4, h - 3, shade(fill, 0.06))
    cv.rect(w - 5, 2, w - 3, h - 3, shade(fill, -0.12))
    if ornament:
        # small gold corner brackets (drawn so 9-slice keeps them tidy)
        for (cx, cy, dx, dy) in ((5, 5, 1, 1), (w - 6, 5, -1, 1), (5, h - 6, 1, -1), (w - 6, h - 6, -1, -1)):
            for k in range(6):
                cv.px(cx + dx * k, cy, ornament)
                cv.px(cx, cy + dy * k, ornament)
            cv.px(cx + dx * 2, cy + dy * 2, shade(ornament, -0.2))
    return cv


def ornament_line(w, col="#e8c060"):
    cv = Canvas(w, 8)
    for x in range(w):
        t = x / max(1, w - 1)
        vy = int(2 + 3 * abs(math.sin(t * math.pi * 5)))
        cv.px(x, vy, col)
        cv.px(x, vy + 1, shade(col, -0.25))
    return cv


def build():
    os.makedirs(OUT, exist_ok=True)
    gold = "#e0b45c"
    gold_d = "#8f6a2a"
    dark = "#3c2c34"

    # ---- panels --------------------------------------------------------
    panel(48, 48, "#4a3742", gold, dark, gold, 0).save(os.path.join(OUT, "panel_dark.png"))
    panel(40, 40, "#5c4650", gold, dark, None).save(os.path.join(OUT, "panel_soft.png"))
    panel(64, 64, "#6a4a52", gold, dark, gold).save(os.path.join(OUT, "panel_banner.png"))
    panel(48, 48, "#2f2530", gold, dark, None).save(os.path.join(OUT, "panel_dialogue.png"))
    panel(40, 40, "#453242", gold, dark, None).save(os.path.join(OUT, "slot_cell.png"))
    panel(40, 40, "#7a5a2a", "#f0d070", "#5c4018", gold).save(os.path.join(OUT, "slot_selected.png"))

    # ---- parchment (world map / journal pages) -------------------------
    pw, ph = 96, 96
    cv = Canvas(pw, ph)
    rng = random.Random(5)
    cv.rect(0, 0, pw - 1, ph - 1, "#d9c49a")
    for y in range(ph):
        for x in range(pw):
            v = rng.random()
            if v < 0.10:
                cv.px(x, y, "#cdb68c")
            elif v > 0.93:
                cv.px(x, y, "#e5d3ac")
    for _ in range(70):     # fibre speckles
        x, y = rng.randrange(pw), rng.randrange(ph)
        cv.px(x, y, "#b9a077")
    # burnt / aged edges
    for i in range(6):
        a = int(40 - i * 6)
        cv.rect(i, i, pw - 1 - i, ph - 1 - i, (150, 120, 80, a), fill=False)
    cv.rect(0, 0, pw - 1, ph - 1, "#a88a5c")
    cv.rect(1, 1, pw - 2, ph - 2, "#c0a273")
    cv.save(os.path.join(OUT, "parchment.png"))

    # ---- buttons -------------------------------------------------------
    def button(fill, border, label=None):
        w, h = 48, 32
        cv = Canvas(w, h)
        cv.rect(1, 0, w - 2, h - 1, border)
        cv.rect(2, 1, w - 3, h - 2, fill)
        cv.rect(2, 1, w - 3, 3, shade(fill, 0.22))
        cv.rect(2, h - 4, w - 3, h - 2, shade(fill, -0.25))
        cv.rect(1, 0, 1, h - 1, shade(border, 0.2))
        cv.rect(w - 2, 0, w - 2, h - 1, shade(border, -0.2))
        for k in range(4):
            cv.px(4 + k, 3 + k // 2, shade(border, 0.35))
            cv.px(w - 5 - k, h - 4 - k // 2, shade(border, 0.35))
        return cv

    button("#5c4250", gold).save(os.path.join(OUT, "button_normal.png"))
    button("#7a5a68", "#f7d488").save(os.path.join(OUT, "button_hover.png"))
    button("#3f2c38", "#a8823a").save(os.path.join(OUT, "button_pressed.png"))
    button("#3a3038", "#6a5a48").save(os.path.join(OUT, "button_disabled.png"))

    # ---- bars ----------------------------------------------------------
    bar_bg = Canvas(64, 14)
    bar_bg.rect(0, 0, 63, 13, "#d8b060")
    bar_bg.rect(1, 1, 62, 12, "#2f2530")
    bar_bg.rect(2, 2, 61, 11, "#3f3440")
    bar_bg.save(os.path.join(OUT, "bar_bg.png"))

    fill = Canvas(32, 12)
    for y in range(12):
        t = y / 11.0
        fill.rect(0, y, 31, y, shade("#e8a03c", 0.25 - t * 0.45))
    fill.rect(0, 0, 31, 1, "#ffe0a0")
    fill.save(os.path.join(OUT, "bar_fill.png"))

    fill_cp = Canvas(32, 12)
    for y in range(12):
        t = y / 11.0
        fill_cp.rect(0, y, 31, y, shade("#6ac0d8", 0.3 - t * 0.4))
    fill_cp.save(os.path.join(OUT, "bar_fill_cp.png"))

    # ---- misc icons ----------------------------------------------------
    def icon(name, drawer, size=24):
        cv = Canvas(size, size)
        drawer(cv, size)
        cv.save(os.path.join(OUT, name + ".png"))

    def i_coin(cv, s):
        cv.ellipse(3, 3, s - 4, s - 4, "#8f6a2a")
        cv.ellipse(4, 4, s - 5, s - 5, "#e8c060")
        cv.ellipse(6, 6, s - 7, s - 7, "#f7dc94")
        cv.rect(10, 7, 13, 17, "#c9a244")
        cv.rect(11, 8, 12, 16, "#8f6a2a")

    def i_quest(cv, s):
        cv.rect(4, 3, s - 5, s - 4, "#e8dcc0")
        cv.rect(5, 4, s - 6, s - 5, "#f4ecd8")
        for k in range(4):
            cv.rect(7, 7 + k * 4, s - 8 - (k % 2) * 3, 8 + k * 4, "#8a7a5a")

    def i_journal(cv, s):
        cv.rect(3, 4, s - 4, s - 3, "#6a4a2a")
        cv.rect(4, 5, s - 5, s - 4, "#8a5f36")
        cv.rect(11, 5, 13, s - 4, "#e8c060")
        cv.rect(5, 5, 11, s - 4, "#b8834f")
        cv.rect(14, 5, s - 5, s - 4, "#b8834f")

    def i_map(cv, s):
        cv.poly([(2, 6), (9, 3), (15, 6), (21, 3), (21, 18), (15, 21), (9, 18), (2, 21)], "#e0cfa0")
        cv.poly([(2, 6), (9, 3), (9, 18), (2, 21)], "#cdb889")
        cv.line([(9, 3), (9, 18)], "#8a7a5a", 1)
        cv.line([(15, 6), (15, 21)], "#8a7a5a", 1)
        cv.px(6, 10, "#c05040")
        cv.px(17, 12, "#c05040")

    def i_bag(cv, s):
        cv.rect(4, 8, s - 5, s - 4, "#8a5f36")
        cv.rect(5, 9, s - 6, s - 5, "#a8763e")
        cv.rect(8, 5, s - 9, 9, "#6a4a2a")
        cv.rect(4, 14, s - 5, 16, "#6a4a2a")
        cv.rect(11, 13, 13, 16, "#e8c060")

    def i_star(cv, s):
        cx, cy, R, r = s / 2, s / 2, 10, 4.5
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = R if i % 2 == 0 else r
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        cv.poly(pts, "#e8c060")
        cv.poly([(p[0], p[1]) for p in pts], "#f7dc94")
        cv.rect(int(cx) - 1, int(cy) - 1, int(cx) + 1, int(cy) + 1, "#8f6a2a")

    def i_flag(cv, s):
        cv.rect(5, 3, 7, s - 3, "#8a6440")
        cv.poly([(8, 4), (20, 6), (20, 13), (8, 11)], "#c05040")
        cv.poly([(8, 4), (20, 6), (20, 8), (8, 7)], "#e05a4a")

    def i_gear(cv, s):
        cv.ellipse(6, 6, s - 7, s - 7, "#c9c4bc")
        cv.ellipse(9, 9, s - 10, s - 10, "#4a4048")
        for i in range(8):
            a = i * math.pi / 4
            x = s / 2 + 9.5 * math.cos(a)
            y = s / 2 + 9.5 * math.sin(a)
            cv.ellipse(x - 2, y - 2, x + 2, y + 2, "#c9c4bc")

    def i_trophy(cv, s):
        cv.poly([(6, 4), (18, 4), (16, 12), (8, 12)], "#e8c060")
        cv.poly([(8, 12), (16, 12), (13, 17), (11, 17)], "#c9a244")
        cv.rect(8, 17, 16, 20, "#a8823a")
        cv.ellipse(2, 4, 7, 11, "#c9a244", fill=False)
        cv.ellipse(17, 4, 23, 11, "#c9a244", fill=False)

    def i_lock(cv, s):
        cv.rect(5, 11, s - 6, s - 4, "#b8934a")
        cv.rect(6, 12, s - 7, s - 5, "#e8c060")
        cv.ellipse(8, 4, s - 9, 14, "#c9a244", fill=False)
        cv.ellipse(8, 4, s - 9, 14, "#c9a244", fill=False)
        cv.rect(11, 15, 13, 19, "#6a4a2a")

    def i_puzzle(cv, s):
        cv.rect(3, 3, 11, 11, "#c05070")
        cv.rect(13, 3, 21, 11, "#e8c060")
        cv.rect(3, 13, 11, 21, "#6ac0d8")
        cv.rect(13, 13, 21, 21, "#7ac078")
        cv.rect(10, 3, 14, 11, "#c05070")
        cv.rect(13, 10, 21, 14, "#e8c060")
        cv.rect(10, 13, 14, 21, "#6ac0d8")

    def i_heart(cv, s):
        cv.ellipse(3, 5, 13, 15, "#d05060")
        cv.ellipse(11, 5, 21, 15, "#d05060")
        cv.poly([(3, 12), (21, 12), (12, 21)], "#d05060")
        cv.ellipse(6, 7, 11, 11, "#e87a86")

    for nm, fn in (("icon_coin", i_coin), ("icon_quest", i_quest), ("icon_journal", i_journal),
                   ("icon_map", i_map), ("icon_bag", i_bag), ("icon_star", i_star),
                   ("icon_flag", i_flag), ("icon_gear", i_gear), ("icon_trophy", i_trophy),
                   ("icon_lock", i_lock), ("icon_puzzle", i_puzzle), ("icon_heart", i_heart)):
        icon(nm, fn)

    # ---- game icon -----------------------------------------------------
    ic = Canvas(128, 128)
    for y in range(128):
        t = y / 127.0
        ic.rect(0, y, 127, y, shade("#2f4a6a", -0.25 + 0.5 * t))
    ic.ellipse(20, 18, 108, 106, "#e8b45c")
    ic.ellipse(24, 22, 104, 100, "#f7d488")
    # stylised island silhouette + pin
    ic.poly([(34, 78), (46, 62), (60, 70), (74, 58), (92, 74), (86, 92), (58, 96)], "#4a8a4a")
    ic.poly([(34, 78), (46, 62), (60, 70), (58, 96), (44, 90)], "#3f7a42")
    ic.poly([(58, 30), (74, 52), (58, 74), (42, 52)], "#c05040")
    ic.ellipse(52, 44, 64, 56, "#f4ecd8")
    ic.px(58, 50, "#c05040")
    ic.outline("#2b2026", alpha_test=70)
    ic.save(os.path.join(OUT, "icon.png"))
    # project icon needs to be a plain png at res://icon source too
    ic.save(os.path.join(ROOT, "assets", "ui", "icon.png"))
    print("wrote UI art ->", OUT)


if __name__ == "__main__":
    build()
