"""qb.py -- tiny DSL that turns compact Python specs into quest + dialogue JSON."""

QUESTS = []
DIALOGUES = {}
NPC_CONDITIONALS = {}      # npc_id -> [ {if: {...}, dialogue: id} ]
ACHIEVEMENTS_EXTRA = {}


def o(oid, text, typ, target="", count=1, hidden=False):
    return {"id": oid, "text": text, "type": typ, "target": target,
            "count": count, "hidden": hidden}


def Q(qid, region, chapter, giver, title, description, summary, objectives,
      complete, hints, offer, turnin, requires=(), puzzle="", rewards=None,
      accept="I will help.", decline="Not yet, but I will come back.",
      accept_lines=(), turnin_do=None, unlock_region="", unlock_map="",
      requires_flags=(), offer_do=None, closing="", interlude=()):
    """Builds one quest plus its four dialogue trees (offer, puzzle, turn-in, done)."""
    rewards = rewards or {}
    rw = {"culture_points": rewards.get("cp", 60),
          "items": list(rewards.get("items", [])),
          "culture": list(rewards.get("culture", [])),
          "flags": list(rewards.get("flags", []))}
    if unlock_region:
        rw["unlock_region"] = unlock_region
    if unlock_map:
        rw["unlock_map"] = unlock_map
    req = {"quests": list(requires), "flags": list(requires_flags)}
    quest = {
        "id": qid, "title": title, "region": region, "chapter": chapter,
        "giver": giver, "type": "main", "description": description,
        "summary": summary, "requires": req,
        "start": {"type": "talk", "npc": giver},
        "objectives": objectives,
        "complete": complete,
        "puzzle": puzzle,
        "rewards": rw,
        "hints": list(hints),
    }
    offer_id = "dlg_%s_offer" % qid
    turnin_id = "dlg_%s_turnin" % qid
    quest["offer_dialogue"] = offer_id
    quest["turn_in_dialogue"] = turnin_id
    QUESTS.append(quest)

    # ---- offer tree (choice: accept / decline) --------------------------
    accept_effects = {}
    if offer_do:
        accept_effects.update(offer_do)
    nodes = {
        "n1": {"speaker": giver, "lines": list(offer),
               "choices": [{"text": accept, "goto": "yes"},
                           {"text": decline, "goto": "no"}]},
        "yes": {"speaker": giver, "lines": list(accept_lines) or
                ["Good. Take your time, and write down what you learn."],
                "do": accept_effects},
        "no": {"speaker": giver,
               "lines": ["Then come back when you are ready - it will keep."],
               "goto": ""},
    }
    DIALOGUES[offer_id] = {"start": "n1", "nodes": nodes}

    # ---- turn-in tree ---------------------------------------------------
    tdo = dict(turnin_do or {})
    tnodes = {"n1": {"speaker": giver, "lines": list(turnin)}}
    if closing:
        tnodes["n1"]["goto"] = "n2"
        tnodes["n2"] = {"speaker": giver, "lines": [closing], "do": tdo}
    elif tdo:
        tnodes["n1"]["do"] = tdo
    DIALOGUES[turnin_id] = {"start": "n1", "nodes": tnodes}

    # ---- "let me try the task" interlude (opens the puzzle) --------------
    if interlude:
        inter_id = "dlg_%s_task" % qid
        condition = {"quest_active": qid}
        if puzzle != "":
            condition["no_flag"] = "done_" + puzzle
        idlg = {"start": "n1", "nodes": {
            "n1": {"speaker": giver, "lines": list(interlude),
                   "do": {"open_puzzle": puzzle} if puzzle != "" else {}}}}
        DIALOGUES[inter_id] = idlg
        NPC_CONDITIONALS.setdefault(giver, []).insert(0, {"if": condition, "dialogue": inter_id})
    return quest
