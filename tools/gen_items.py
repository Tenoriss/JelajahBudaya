"""gen_items.py -- draws the item / collectible / souvenir icon set (32x32).

Original pixel art written for "Nusantara: Jejak Budaya"; no external assets.
Every icon is built from simple geometric shapes: vessels, plants, cloth folds,
blades, instruments and abstract collectible tokens.
"""
from __future__ import annotations
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artlib import Canvas, P

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "ui", "items")
S = 32


def base(col_bg=None):
    cv = Canvas(S, S)
    return cv


def leaf_shape(cv, x, y, sx=1.0, col=P["leaf"], dark=P["grass_dark"]):
    cv.ellipse(x - 6 * sx, y - 3, x + 6 * sx, y + 3, col)
    cv.line([(x - 6 * sx, y), (x + 6 * sx, y)], dark)


def icon_rice(cv):
    cv.poly([(10, 28), (22, 28), (19, 12), (13, 12)], (196, 168, 92, 255))
    for i, x in enumerate((8, 12, 16, 20, 24)):
        top = 4 + (i % 2) * 3
        cv.line([(x, 28), (x, top + 2)], (150, 178, 96, 255), 2)
        cv.ellipse(x - 3, top, x + 3, top + 9, (232, 208, 118, 255))
        cv.ellipse(x - 2, top + 1, x + 2, top + 8, (250, 232, 152, 255))
        cv.px(x, top + 3, (186, 152, 74, 255))
    cv.rect(9, 18, 23, 21, (168, 118, 66, 255))
    cv.line([(10, 19), (22, 19)], (206, 156, 96, 255))

def icon_chilli(cv):
    cv.line([(8, 4), (13, 9)], (86, 140, 70, 255), 3)
    cv.poly([(11, 8), (16, 9), (26, 27), (17, 29), (8, 16)], (188, 48, 40, 255))
    cv.poly([(13, 10), (16, 11), (23, 25), (19, 26)], (226, 84, 60, 255))
    cv.line([(14, 12), (19, 22)], (250, 190, 170, 255))

def icon_fish(cv):
    cv.ellipse(5, 9, 25, 27, (96, 164, 200, 255))
    cv.ellipse(7, 11, 23, 25, (128, 190, 222, 255))
    cv.poly([(24, 18), (31, 10), (31, 26)], (74, 138, 176, 255))
    cv.poly([(12, 11), (18, 5), (21, 12)], (108, 176, 210, 255))
    cv.ellipse(8, 14, 12, 18, (250, 250, 250, 255))
    cv.ellipse(9, 15, 11, 17, (34, 32, 44, 255))
    for i in range(3):
        cv.line([(12 + i * 4, 20), (15 + i * 4, 20)], (206, 232, 244, 255))

def icon_coconut(cv):
    cv.ellipse(8, 8, 24, 25, (140, 96, 60, 255))
    cv.ellipse(11, 11, 21, 22, (168, 118, 72, 255))
    cv.px(13, 13, (220, 190, 150, 255))
    cv.px(18, 15, (220, 190, 150, 255))
    cv.px(15, 18, (220, 190, 150, 255))


def icon_coffee(cv):
    cv.ellipse(6, 12, 20, 26, (120, 74, 48, 255))
    cv.ellipse(9, 15, 17, 23, (86, 52, 34, 255))
    cv.ellipse(14, 9, 26, 20, (140, 92, 58, 255))
    cv.line([(15, 13), (24, 15)], (196, 148, 96, 255))
    cv.line([(15, 16), (24, 18)], (196, 148, 96, 255))


def icon_spices(cv):
    cv.ellipse(6, 16, 26, 28, (150, 118, 88, 255))
    cv.ellipse(8, 8, 15, 15, (198, 146, 60, 255))
    cv.ellipse(16, 6, 23, 13, (168, 96, 52, 255))
    cv.ellipse(13, 12, 18, 17, (226, 200, 140, 255))
    cv.px(20, 9, (232, 176, 96, 255))


def icon_sago(cv):
    cv.poly([(10, 26), (22, 26), (20, 10), (12, 10)], (206, 190, 160, 255))
    cv.ellipse(9, 19, 23, 27, (240, 236, 226, 255))
    cv.ellipse(12, 21, 20, 25, (252, 250, 246, 255))
    cv.line([(12, 12), (20, 12)], (176, 158, 130, 255))


def icon_banana(cv):
    cv.poly([(7, 9), (10, 10), (24, 21), (22, 26), (9, 15)], (232, 206, 76, 255))
    cv.poly([(9, 10), (22, 22), (23, 23), (10, 13)], (248, 226, 110, 255))
    cv.line([(21, 23), (25, 27)], (150, 122, 60, 255))


def icon_rattan(cv):
    for i, y in enumerate(range(8, 26, 5)):
        cv.ellipse(5, y, 27, y + 5, (196, 160, 96, 255))
        cv.line([(6, y + 2), (26, y + 2)], (160, 124, 68, 255))
        cv.px(9 + i * 4, y + 1, (224, 196, 130, 255))


def icon_wood(cv):
    cv.rect(4, 9, 28, 25, (146, 100, 60, 255))
    cv.rect(4, 9, 28, 12, (186, 138, 88, 255))
    cv.ellipse(17, 12, 28, 23, (206, 162, 104, 255))
    cv.ellipse(19, 14, 26, 21, (166, 118, 74, 255))
    cv.ellipse(21, 16, 24, 19, (206, 162, 104, 255))
    for i in range(3):
        cv.line([(6, 16 + i * 3), (13, 16 + i * 3)], (112, 74, 44, 255))

def icon_cloth(cv):
    cv.poly([(4, 7), (28, 5), (28, 27), (4, 29)], (186, 66, 58, 255))
    cv.rect(7, 9, 25, 25, (206, 92, 74, 255))
    cv.ellipse(11, 12, 16, 17, (240, 206, 132, 255))
    cv.ellipse(18, 18, 23, 23, (240, 206, 132, 255))
    cv.line([(9, 22), (23, 22)], (150, 48, 44, 255))
    cv.line([(9, 12), (23, 12)], (150, 48, 44, 255))
    cv.line([(16, 8), (16, 26)], (232, 176, 104, 255))

def icon_silk(cv):
    for i in range(5):
        cv.ellipse(4, 6 + i * 4, 28, 11 + i * 4, (120, 190, 170, 255) if i % 2 == 0 else (96, 168, 154, 255))
    cv.line([(6, 22), (26, 22)], (200, 240, 226, 255))


def icon_beads(cv):
    positions = [(10, 8), (16, 10), (22, 12), (12, 15), (18, 17), (24, 19), (14, 22), (20, 24), (26, 26)]
    cols = [(196, 70, 60, 255), (230, 180, 70, 255), (90, 150, 200, 255), (120, 190, 120, 255)]
    for i, (x, y) in enumerate(positions):
        cv.ellipse(x - 3, y - 3, x + 3, y + 3, cols[i % len(cols)])
        cv.px(x - 1, y - 1, (255, 250, 240, 255))


def icon_blade(cv):
    cv.poly([(7, 25), (9, 27), (25, 11), (22, 8)], (200, 206, 214, 255))
    cv.poly([(9, 25), (23, 11), (25, 11), (11, 26)], (238, 242, 248, 255))
    cv.rect(5, 23, 9, 28, (110, 78, 48, 255))
    cv.px(8, 26, (222, 190, 120, 255))


def icon_flute(cv):
    cv.rect(4, 14, 28, 18, (214, 186, 120, 255))
    cv.rect(4, 14, 28, 15, (238, 214, 156, 255))
    for x in (9, 14, 19, 24):
        cv.px(x, 16, (110, 84, 48, 255))
        cv.px(x, 17, (110, 84, 48, 255))
    cv.line([(6, 19), (26, 19)], (176, 146, 92, 255))


def icon_drum(cv):
    cv.ellipse(4, 4, 28, 15, (234, 216, 184, 255))
    cv.ellipse(7, 7, 25, 12, (250, 240, 216, 255))
    cv.poly([(4, 9), (28, 9), (24, 29), (8, 29)], (172, 108, 62, 255))
    cv.poly([(8, 24), (24, 24), (24, 28), (8, 28)], (138, 82, 48, 255))
    for i in range(3):
        cv.line([(9, 13 + i * 4), (23, 13 + i * 4)], (222, 178, 122, 255))
    cv.line([(14, 10), (18, 10)], (120, 68, 40, 255))

def icon_gong(cv):
    cv.ellipse(4, 6, 28, 27, (198, 154, 70, 255))
    cv.ellipse(8, 10, 24, 23, (232, 190, 96, 255))
    cv.ellipse(13, 14, 19, 19, (170, 124, 56, 255))
    cv.px(16, 16, (250, 232, 170, 255))


def icon_pot(cv):
    cv.poly([(7, 12), (25, 12), (22, 27), (10, 27)], (108, 108, 116, 255))
    cv.line([(8, 14), (24, 14)], (150, 150, 158, 255))
    cv.ellipse(5, 8, 12, 14, (108, 108, 116, 255))
    cv.ellipse(20, 8, 27, 14, (108, 108, 116, 255))
    for y in (17, 21, 25):
        cv.line([(11, y), (21, y)], (84, 84, 92, 255))


def icon_boat(cv):
    cv.poly([(4, 18), (28, 18), (24, 27), (8, 27)], (144, 96, 58, 255))
    cv.line([(5, 19), (27, 19)], (186, 140, 92, 255))
    cv.rect(15, 4, 17, 18, (110, 74, 44, 255))
    cv.poly([(17, 5), (26, 13), (17, 13)], (232, 224, 200, 255))
    cv.poly([(15, 7), (7, 14), (15, 14)], (216, 208, 186, 255))


def icon_lantern(cv):
    cv.rect(12, 3, 20, 6, (96, 70, 44, 255))
    cv.poly([(9, 8), (23, 8), (25, 23), (7, 23)], (222, 160, 82, 255))
    cv.poly([(12, 9), (20, 9), (21, 22), (11, 22)], (250, 226, 140, 255))
    cv.line([(10, 25), (22, 25)], (96, 70, 44, 255))


def icon_feather(cv):
    cv.line([(6, 29), (24, 6)], (152, 148, 156, 255), 3)
    cv.poly([(23, 3), (29, 9), (14, 27), (9, 22)], (232, 176, 56, 255))
    cv.poly([(23, 3), (26, 8), (13, 25), (10, 22)], (252, 216, 112, 255))
    for i in range(6):
        cv.line([(11 + i * 2, 23 - i * 3), (19 + i * 2, 18 - i * 3)], (186, 130, 36, 255))
    cv.px(6, 29, (96, 74, 44, 255))

def icon_notebook(cv):
    cv.rect(6, 5, 26, 28, (150, 108, 66, 255))
    cv.rect(9, 5, 26, 28, (240, 232, 210, 255))
    cv.rect(6, 5, 9, 28, (120, 84, 52, 255))
    for i in range(5):
        cv.line([(12, 10 + i * 4), (24, 10 + i * 4)], (170, 156, 132, 255))
    cv.rect(7, 3, 11, 6, (214, 176, 96, 255))


def icon_mask(cv):
    cv.poly([(8, 5), (24, 5), (24, 20), (16, 28), (8, 20)], (196, 150, 92, 255))
    cv.poly([(11, 9), (21, 9), (21, 18), (16, 24), (11, 18)], (226, 186, 120, 255))
    cv.rect(11, 12, 14, 15, (60, 44, 40, 255))
    cv.rect(18, 12, 21, 15, (60, 44, 40, 255))
    cv.line([(13, 19), (19, 19)], (150, 96, 60, 255))


def icon_totem(cv):
    cv.rect(11, 3, 21, 29, (170, 122, 78, 255))
    cv.rect(12, 4, 20, 12, (206, 162, 104, 255))
    cv.rect(12, 16, 20, 28, (150, 106, 66, 255))
    cv.rect(13, 7, 16, 10, (58, 42, 38, 255))
    cv.rect(18, 7, 20, 10, (58, 42, 38, 255))
    cv.rect(14, 19, 19, 22, (58, 42, 38, 255))
    cv.line([(12, 14), (20, 14)], (96, 66, 42, 255))


def icon_stone(cv):
    cv.poly([(7, 25), (8, 12), (16, 5), (25, 12), (24, 25)], (150, 148, 148, 255))
    cv.poly([(10, 23), (11, 14), (16, 9), (18, 14)], (186, 184, 182, 255))
    cv.line([(12, 20), (20, 20)], (108, 106, 112, 255))
    cv.line([(14, 24), (21, 17)], (108, 106, 112, 255))


def icon_carving(cv):
    cv.rect(6, 6, 26, 26, (176, 128, 82, 255))
    cv.rect(8, 8, 24, 24, (208, 162, 108, 255))
    for i in range(3):
        cv.ellipse(10, 9 + i * 6, 22, 15 + i * 6, (156, 106, 66, 255))
        cv.rect(13, 10 + i * 6, 19, 13 + i * 6, (72, 50, 40, 255))


def icon_puzzle(cv):
    cv.rect(5, 5, 17, 17, (200, 168, 96, 255))
    cv.rect(17, 5, 27, 15, (94, 164, 196, 255))
    cv.rect(5, 17, 15, 27, (188, 110, 96, 255))
    cv.rect(17, 17, 27, 27, (140, 176, 118, 255))
    cv.rect(12, 11, 20, 19, (44, 36, 44, 255))
    cv.rect(9, 8, 15, 14, (44, 36, 44, 255))
    cv.rect(17, 18, 24, 25, (44, 36, 44, 255))


def icon_coin(cv):
    cv.ellipse(6, 6, 26, 26, (214, 168, 70, 255))
    cv.ellipse(8, 8, 24, 24, (246, 208, 108, 255))
    cv.ellipse(12, 12, 20, 20, (214, 168, 70, 255))
    cv.rect(15, 12, 17, 20, (150, 108, 44, 255))


def icon_thread(cv):
    cv.rect(8, 6, 24, 27, (196, 108, 122, 255))
    cv.rect(10, 8, 22, 25, (238, 162, 172, 255))
    cv.rect(6, 4, 26, 9, (140, 78, 92, 255))
    cv.rect(6, 24, 26, 29, (140, 78, 92, 255))
    cv.line([(11, 11), (21, 11)], (196, 108, 122, 255))
    cv.line([(11, 15), (21, 15)], (196, 108, 122, 255))
    cv.poly([(24, 8), (30, 3), (31, 5), (26, 11)], (238, 162, 172, 255))

def icon_water(cv):
    cv.poly([(16, 3), (26, 18), (16, 29), (6, 18)], (86, 158, 208, 255))
    cv.poly([(16, 7), (23, 18), (16, 26), (9, 18)], (140, 200, 232, 255))
    cv.px(13, 15, (232, 246, 252, 255))


def icon_seed(cv):
    cv.ellipse(8, 10, 22, 26, (150, 106, 64, 255))
    cv.ellipse(11, 13, 19, 23, (204, 158, 96, 255))
    cv.line([(16, 12), (16, 6)], (110, 158, 78, 255), 2)
    cv.ellipse(11, 2, 22, 11, (124, 176, 84, 255))
    cv.line([(12, 7), (21, 6)], (86, 134, 62, 255))

def icon_honey(cv):
    cv.poly([(8, 7), (24, 7), (27, 28), (5, 28)], (198, 150, 70, 255))
    cv.poly([(11, 10), (21, 10), (23, 26), (9, 26)], (246, 200, 104, 255))
    cv.poly([(11, 17), (21, 17), (23, 26), (9, 26)], (232, 176, 78, 255))
    cv.rect(10, 4, 22, 8, (146, 96, 52, 255))
    cv.line([(12, 6), (20, 6)], (196, 148, 92, 255))
    cv.line([(10, 14), (22, 14)], (172, 118, 56, 255))

def icon_shell(cv):
    cv.poly([(16, 26), (6, 12), (11, 6), (16, 12), (21, 6), (26, 12)], (240, 214, 186, 255))
    for x in (10, 13, 16, 19, 22):
        cv.line([(x, 10), (16, 25)], (206, 174, 148, 255))
    cv.line([(6, 12), (26, 12)], (176, 142, 120, 255))


def icon_leaf(cv):
    cv.poly([(16, 4), (27, 12), (16, 28), (5, 12)], (108, 176, 84, 255))
    cv.poly([(16, 7), (24, 13), (16, 25), (8, 13)], (140, 200, 104, 255))
    cv.line([(16, 8), (16, 25)], (74, 132, 62, 255))
    for i in range(3):
        cv.line([(16, 12 + i * 4), (11 + i, 10 + i * 4)], (74, 132, 62, 255))
        cv.line([(16, 12 + i * 4), (21 - i, 10 + i * 4)], (74, 132, 62, 255))


ICONS = {
    "rice": icon_rice, "chilli": icon_chilli, "fish": icon_fish, "coconut": icon_coconut,
    "coffee": icon_coffee, "spices": icon_spices, "sago": icon_sago, "banana": icon_banana,
    "rattan": icon_rattan, "wood": icon_wood, "cloth": icon_cloth, "silk": icon_silk,
    "beads": icon_beads, "blade": icon_blade, "flute": icon_flute, "drum": icon_drum,
    "gong": icon_gong, "pot": icon_pot, "boat": icon_boat, "lantern": icon_lantern,
    "feather": icon_feather, "notebook": icon_notebook, "mask": icon_mask, "totem": icon_totem,
    "stone": icon_stone, "carving": icon_carving, "puzzle": icon_puzzle, "coin": icon_coin,
    "thread": icon_thread, "water": icon_water, "seed": icon_seed, "honey": icon_honey,
    "shell": icon_shell, "leaf": icon_leaf,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in ICONS.items():
        cv = base()
        fn(cv)
        cv.outline((36, 26, 38, 255))
        cv.save(os.path.join(OUT, name + ".png"))
    print(f"wrote {len(ICONS)} item icons to {OUT}")


if __name__ == "__main__":
    main()
