"""Compiles every content module into the game's JSON files and validates them."""
from __future__ import annotations
import json, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from content import qb, quests_ps, quests_jk, quests_sp, npcs, mapdefs1, mapdefs2, maplinks
from content.regions import REGIONS, CHAPTERS, ENDINGS, ACHIEVEMENTS, REGION_ORDER
from content.cultures import C, CATEGORIES
from content.items_puzzles import ITEM_CATALOGUE, PZ
from content.maphelp import all_maps

DATA = os.path.join(ROOT, "data")
MAPS_DIR = os.path.join(DATA, "maps")


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    return path


def main():
    quests = {q["id"]: q for q in qb.QUESTS}
    cultures = {c["id"]: c for c in C}
    items = {i["id"]: i for i in ITEM_CATALOGUE}
    puzzles = {p["id"]: p for p in PZ}
    npc_cards = {}
    for n in npcs.NDEFS:
        card = dict(n)
        conds = qb.NPC_CONDITIONALS.get(n["id"], [])
        if conds:
            card["conditional_dialogue"] = conds
        card.pop("id", None)
        npc_cards[n["id"]] = card

    # every puzzle gets a "solved" flag so dialogue gates can test it
    for pid, p in puzzles.items():
        p["rewards"]["flag"] = p["rewards"].get("flag") or ("done_" + pid)

    regions = {"order": REGION_ORDER, "regions": REGIONS, "chapters": CHAPTERS}
    dump(os.path.join(DATA, "regions.json"), regions)
    dump(os.path.join(DATA, "quests.json"), {"quests": quests})
    dump(os.path.join(DATA, "cultures.json"), {"categories": CATEGORIES, "entries": cultures})
    dump(os.path.join(DATA, "items.json"), {"items": items})
    dump(os.path.join(DATA, "puzzles.json"), {"puzzles": puzzles})
    dump(os.path.join(DATA, "dialogues.json"), {"dialogues": qb.DIALOGUES})
    dump(os.path.join(DATA, "npcs.json"), {"npcs": npc_cards})
    dump(os.path.join(DATA, "achievements.json"), {"achievements": ACHIEVEMENTS})
    dump(os.path.join(DATA, "endings.json"), {"endings": ENDINGS})
    for m in all_maps():
        dump(os.path.join(MAPS_DIR, m["id"] + ".json"), m)

    print("quests %d | cultures %d | items %d | puzzles %d | dialogues %d | npcs %d | maps %d"
          % (len(quests), len(cultures), len(items), len(puzzles), len(qb.DIALOGUES),
             len(npc_cards), len(all_maps())))

    # ------------------------------------------------------------ validation
    problems = []
    minigame_types = set(re.findall(r'"(memory|pattern|sequence|rhythm|tile|match|logic|cooking|'
                                    r'crafting|exploration|environment|quiz|nod)":',
                                    open(os.path.join(ROOT, "scripts/core/puzzle_manager.gd")).read()))
    landmarks = {}
    for m in all_maps():
        for l in m["landmarks"]:
            landmarks[l["id"]] = m["id"]
    map_ids = {m["id"] for m in all_maps()}

    def need(cond, msg):
        if not cond:
            problems.append(msg)

    for qid, q in quests.items():
        need(q["giver"] in npc_cards, "%s: unknown giver %s" % (qid, q["giver"]))
        need(q["offer_dialogue"] in qb.DIALOGUES, "%s: missing offer dialogue" % qid)
        need(q["turn_in_dialogue"] in qb.DIALOGUES, "%s: missing turn-in dialogue" % qid)
        for rid in q["requires"]["quests"]:
            need(rid in quests, "%s: requires unknown quest %s" % (qid, rid))
        for star in [q["start"], q["complete"]]:
            if "npc" in star:
                need(star["npc"] in npc_cards, "%s: unknown npc %s" % (qid, star["npc"]))
        for obj in q["objectives"]:
            t, tgt = obj["type"], str(obj["target"])
            if t == "puzzle":
                need(tgt in puzzles, "%s: objective puzzle %s missing" % (qid, tgt))
            elif t == "collect":
                need(tgt in items, "%s: objective item %s missing" % (qid, tgt))
            elif t == "discover":
                need(tgt in cultures, "%s: objective culture %s missing" % (qid, tgt))
            elif t == "reach":
                need(tgt in map_ids, "%s: objective map %s missing" % (qid, tgt))
            elif t == "landmark":
                need(tgt in landmarks, "%s: objective landmark %s missing" % (qid, tgt))
            elif t == "minigame":
                need(tgt in minigame_types, "%s: objective minigame %s missing" % (qid, tgt))
            elif t == "talk":
                need(tgt in npc_cards or tgt.startswith("interactable:"),
                     "%s: objective npc %s missing" % (qid, tgt))
        if q["puzzle"]:
            need(q["puzzle"] in puzzles, "%s: puzzle %s missing" % (qid, q["puzzle"]))
        for cid in q["rewards"]["culture"]:
            need(cid in cultures, "%s: reward culture %s missing" % (qid, cid))
        for iid in q["rewards"]["items"]:
            need(iid in items, "%s: reward item %s missing" % (qid, iid))
        if q["rewards"].get("unlock_region"):
            need(q["rewards"]["unlock_region"] in REGIONS, "%s: unlock_region bad" % qid)
        if q["rewards"].get("unlock_map"):
            need(q["rewards"]["unlock_map"] in map_ids, "%s: unlock_map bad" % qid)

    for pid, p in puzzles.items():
        need(p["type"] in minigame_types, "%s: bad puzzle type %s" % (pid, p["type"]))
        need(len(p["hints"]) >= 1, "%s: no hints" % pid)
        for cid in p["rewards"]["culture"]:
            need(cid in cultures, "%s: reward culture %s missing" % (pid, cid))
        for iid in p["rewards"]["items"]:
            need(iid in items, "%s: reward item %s missing" % (pid, iid))

    for did, tree in qb.DIALOGUES.items():
        nodes = tree.get("nodes", {})
        need(tree.get("start", "") in nodes, "%s: bad start node" % did)
        for nid, node in nodes.items():
            sp = node.get("speaker", "")
            need(sp == "" or sp in npc_cards, "%s/%s: unknown speaker %s" % (did, nid, sp))
            if node.get("goto"):
                need(node["goto"] in nodes, "%s/%s: goto %s missing" % (did, nid, node["goto"]))
            for ch in node.get("choices", []):
                if ch.get("goto"):
                    need(ch["goto"] in nodes, "%s/%s: choice goto missing" % (did, nid))
                do = ch.get("do", {})
                if "start_quest" in do:
                    need(do["start_quest"] in quests, "%s: bad start_quest" % did)
                if "open_puzzle" in do:
                    need(do["open_puzzle"] in puzzles, "%s: bad open_puzzle %s" % (did, do["open_puzzle"]))
                if "open_minigame" in do:
                    need(do["open_minigame"] in minigame_types, "%s: bad open_minigame" % did)
            do = node.get("do", {})
            if "start_quest" in do:
                need(do["start_quest"] in quests, "%s: unknown quest %s" % (did, do["start_quest"]))
            if "open_puzzle" in do:
                need(do["open_puzzle"] in puzzles, "%s: unknown puzzle %s" % (did, do["open_puzzle"]))
            if "discover" in do:
                need(do["discover"] in cultures, "%s: unknown culture %s" % (did, do["discover"]))
            if "give_item" in do:
                need(str(do["give_item"]).split(":")[0] in items, "%s: unknown item" % did)
            if "unlock_map" in do:
                need(do["unlock_map"] in map_ids, "%s: unknown map" % did)
            if "unlock_region" in do:
                need(do["unlock_region"] in REGIONS, "%s: unknown region" % did)

    for cid, c in cultures.items():
        need(c["category"] in CATEGORIES, "%s: bad category %s" % (cid, c["category"]))
        need(c["region"] in REGIONS, "%s: bad region" % cid)
        need(c["name"] and c["short"] and c["text"], "%s: incomplete" % cid)

    for iid, it in items.items():
        need(it["category"] in ("items", "quest", "collectibles", "souvenirs"),
             "%s: bad category" % iid)
        icon_path = str(it["icon"]).replace("res://", "")
        need(os.path.exists(os.path.join(ROOT, icon_path)),
             "%s: icon missing %s" % (iid, it["icon"]))

    for m in all_maps():
        need(m["region"] in REGIONS, "%s: bad region" % m["id"])
        for e in m["exits"]:
            need(e["target"] in map_ids, "%s: exit target %s missing" % (m["id"], e["target"]))
        for it in m["interactables"]:
            k = it["kind"]
            tgt = str(it.get("target", ""))
            if k == "puzzle":
                need(tgt in puzzles, "%s/%s: puzzle %s missing" % (m["id"], it["id"], tgt))
            elif k in ("pickup", "chest"):
                ids = [tgt] if k == "pickup" else [str(x) for x in it.get("items", [])]
                for x in ids:
                    need(x in items, "%s/%s: item %s missing" % (m["id"], it["id"], x))
            elif k == "discovery":
                need(tgt in cultures, "%s/%s: culture %s missing" % (m["id"], it["id"], tgt))
            elif k == "dialogue":
                need(tgt in qb.DIALOGUES, "%s/%s: dialogue %s missing" % (m["id"], it["id"], tgt))
            elif k == "minigame":
                need(str(it.get("minigame", tgt)) in minigame_types,
                     "%s/%s: minigame %s missing" % (m["id"], it["id"], tgt))
            elif k == "door":
                need(tgt in map_ids, "%s/%s: door map %s missing" % (m["id"], it["id"], tgt))
            elif k == "landmark":
                need(tgt in landmarks, "%s/%s: landmark %s missing" % (m["id"], it["id"], tgt))
            if it.get("culture"):
                need(str(it["culture"]) in cultures, "%s/%s: culture %s missing"
                     % (m["id"], it["id"], it["culture"]))
            for x in it.get("items", []):
                need(str(x) in items, "%s/%s: item %s missing" % (m["id"], it["id"], x))
            # gates that mention quests must reference real quests
            for key, val in (it.get("if") or {}).items():
                if key in ("quest_active", "quest_done"):
                    need(str(val) in quests, "%s/%s: gate quest %s missing" % (m["id"], it["id"], val))
        for n in m["npcs"]:
            need(n["id"] in npc_cards, "%s: npc %s has no card" % (m["id"], n["id"]))
        # NPCs must sit inside the map
        for n in m["npcs"]:
            need(0 <= n["pos"][0] < m["size"][0] and 0 <= n["pos"][1] < m["size"][1],
                 "%s: npc %s outside map" % (m["id"], n["id"]))

    # quest givers must actually be placed somewhere in the world
    placed = {n["id"] for m in all_maps() for n in m["npcs"]}
    for qid, q in quests.items():
        need(q["giver"] in placed, "%s: giver %s is not placed on any map" % (qid, q["giver"]))
    # collect objectives need a pickup somewhere
    pickups = {str(it.get("target", "")) for m in all_maps() for it in m["interactables"]
               if it["kind"] == "pickup"}
    for qid, q in quests.items():
        for obj in q["objectives"]:
            if obj["type"] == "collect":
                need(str(obj["target"]) in pickups,
                     "%s: item %s has no pickup in the world" % (qid, obj["target"]))

    if problems:
        print("\n%d VALIDATION PROBLEM(S):" % len(problems))
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("validation OK")


if __name__ == "__main__":
    main()
