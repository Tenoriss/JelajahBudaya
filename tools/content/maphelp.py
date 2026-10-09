"""Helpers that build map JSON definitions with less noise."""
MAPS = []

WATER_SOLID = ("WATER", "DEEP")


def rect(tile, x, y, w, h):
    return {"tile": tile, "rect": [x, y, w, h]}


def line(tile, x1, y1, x2, y2, width=1):
    return {"tile": tile, "from": [x1, y1], "to": [x2, y2], "width": width}


def blob(tile, cx, cy, radius):
    return {"tile": tile, "center": [cx, cy], "radius": radius}


def obj(sprite, x, y, flip=False, scale=None, collide=True):
    out = {"sprite": sprite, "pos": [x, y], "flip": flip, "collide": collide}
    if scale:
        out["scale"] = scale
    return out


def ix(iid, kind, x, y, when=None, **kw):
    """when={...} becomes the JSON gate "if": {...} (the world reads "if")."""
    out = {"id": iid, "kind": kind, "pos": [x, y]}
    out.update(kw)
    if when:
        out["if"] = when
    return out


def npc(nid, x, y, wander=False, facing="down", patrol=None):
    out = {"id": nid, "pos": [x, y], "wander": wander, "facing": facing}
    if patrol:
        out["patrol"] = patrol
    return out


def lm(lid, name, x, y, description, entry="", radius=64):
    return {"id": lid, "name": name, "pos": [x, y], "description": description,
            "entry": entry, "radius": radius}


def ex(eid, x, y, target, entry, size=(2, 2), cond=None, locked_text=""):
    out = {"id": eid, "pos": [x, y], "size": list(size), "target": target, "entry": entry}
    if cond:
        out["if"] = cond
    if locked_text:
        out["locked_text"] = locked_text
    return out


def M(mid, name, region, size, music, ambience, terrain, objects=None, npcs=None,
      interactables=None, landmarks=None, exits=None, collision=None, spawn=None):
    terrain = dict(terrain)
    collision = list(collision or [])
    # water is not walkable: give every water rect/blob a collision box
    for r in terrain.get("rects", []):
        if r["tile"] in WATER_SOLID:
            x, y, w, h = r["rect"]
            collision.append([x, y, w, h])
    for b in terrain.get("blobs", []):
        if b["tile"] in WATER_SOLID:
            cx, cy = b["center"]
            rad = b["radius"] + 0.4
            collision.append([cx - rad, cy - rad, rad * 2, rad * 2])
    if ambience and not ambience.startswith("amb_"):
        ambience = "amb_" + ambience
    m = {"id": mid, "name": name, "region": region, "size": list(size),
         "spawn": list(spawn or [size[0] // 2, size[1] - 8]),
         "music": music, "ambience": ambience, "terrain": terrain,
         "objects": list(objects or []), "npcs": list(npcs or []),
         "interactables": list(interactables or []), "landmarks": list(landmarks or []),
         "exits": list(exits or []), "collision_rects": collision}
    MAPS.append(m)
    return m


def find(mid):
    for m in MAPS:
        if m["id"] == mid:
            return m
    raise KeyError(mid)


def link(a, b, pos_a, pos_b, size=(2, 2), cond_a=None, cond_b=None,
         locked_a="", locked_b=""):
    """Two-way door between two maps (arrival points are the doors themselves)."""
    ma, mb = find(a), find(b)
    ma["exits"].append(ex("to_" + b, pos_a[0], pos_a[1], b, "to_" + a, size,
                          cond_a, locked_a))
    mb["exits"].append(ex("to_" + a, pos_b[0], pos_b[1], a, "to_" + b, size,
                          cond_b, locked_b))


def all_maps():
    return MAPS
