extends Node
## QuestManager (autoload "Quest")
##
## Data driven quests (data/quests.json).  A quest definition:
## {
##   "id", "title", "region", "chapter", "giver", "type",
##   "description", "summary",
##   "requires": {"quests": [...], "flags": [...], "level": n},
##   "start": {"type": "talk"|"auto"|"flag", "npc": "id", "flag": "story_x"},
##   "objectives": [ {"id","text","type","target","count","hidden"} ],
##   "complete": {"type": "auto"|"talk"|"flag", "npc": "...", "flag": "..."},
##   "puzzle": "puzzle_id",
##   "rewards": {"culture_points": 100, "items": ["x"], "culture": ["entry"],
##               "unlock_region": "java", "unlock_map": "x", "flag": "y"},
##   "hints": ["...", "...", "..."]
## }
##
## Objective types:
##   talk    -- talk to a NPC (target = npc id, count = 1)
##   reach   -- enter a map (target = map id)
##   collect -- own N of an item (target = item id, count = N)
##   puzzle  -- solve a puzzle (target = puzzle id)
##   flag    -- a story flag must be set (target = flag)
##   discover-- discover a culture entry (target = culture id)
##   minigame-- finish a mini game (target = minigame id)
##   landmark-- discover a landmark (target = landmark id)

signal quest_state_changed(quest_id: String, state: String)
signal objective_updated(quest_id: String, objective_id: String)
signal quest_available(quest_id: String)
signal quest_completed(quest_id: String)
signal tracked_changed(quest_id: String)

enum State { LOCKED, AVAILABLE, ACTIVE, COMPLETED }

const STATE_NAMES := ["Locked", "Available", "Active", "Completed"]

var states: Dictionary = {}        # quest_id -> int
var progress: Dictionary = {}      # quest_id -> { objective_id: count }
var tracked := ""
var _completion_queue: Array = []


func reset() -> void:
	states.clear()
	progress.clear()
	tracked = ""
	_completion_queue.clear()


# ------------------------------------------------------------------ queries
func state_of(quest_id: String) -> int:
	return int(states.get(quest_id, State.LOCKED))


func state_name(quest_id: String) -> String:
	return STATE_NAMES[state_of(quest_id)]


func is_active(quest_id: String) -> bool:
	return state_of(quest_id) == State.ACTIVE


func is_completed(quest_id: String) -> bool:
	return state_of(quest_id) == State.COMPLETED


func active_quests() -> Array:
	return _ids_with_state(State.ACTIVE)


func available_quests() -> Array:
	return _ids_with_state(State.AVAILABLE)


func completed_quests() -> Array:
	return _ids_with_state(State.COMPLETED)


func _ids_with_state(state: int) -> Array:
	var out: Array = []
	for qid in Data.quests.keys():
		if state_of(qid) == state:
			out.append(qid)
	out.sort()
	return out


func quests_for_region(region: String) -> Array:
	return Data.get_quests_in_region(region)


func progress_text(quest_id: String) -> String:
	var def := Data.get_quest(quest_id)
	if def.is_empty():
		return ""
	var lines: Array = []
	for obj in def.get("objectives", []):
		if bool(obj.get("hidden", false)):
			continue
		var current := objective_progress(quest_id, str(obj.get("id", "")))
		var need := int(obj.get("count", 1))
		var mark := "[x]" if current >= need else "[ ]"
		lines.append("%s %s" % [mark, obj.get("text", "")])
	return "\n".join(lines)


func objective_progress(quest_id: String, objective_id: String) -> int:
	return int(progress.get(quest_id, {}).get(objective_id, 0))


func objective_text(quest_id: String, objective_id: String) -> String:
	for obj in Data.get_quest(quest_id).get("objectives", []):
		if str(obj.get("id", "")) == objective_id:
			return str(obj.get("text", ""))
	return ""


func tracked_quest() -> String:
	if tracked != "" and is_active(tracked):
		return tracked
	var act := active_quests()
	return act[0] if act.size() > 0 else ""


func set_tracked(quest_id: String) -> void:
	tracked = quest_id
	tracked_changed.emit(quest_id)


# --------------------------------------------------------------- evaluation
## Recomputes LOCKED / AVAILABLE / ACTIVE / COMPLETED for every quest.
func refresh_availability(silent := false) -> void:
	for qid in Data.quests.keys():
		var state := state_of(qid)
		if state == State.ACTIVE or state == State.COMPLETED:
			_check_completion(qid)
			continue
		if not _requirements_met(qid):
			if state != State.LOCKED:
				_set_state(qid, State.LOCKED)
			continue
		var start: Dictionary = Data.get_quest(qid).get("start", {})
		var stype := str(start.get("type", "talk"))
		if stype == "auto" or stype == "flag":
			var ok := true
			if stype == "flag":
				ok = Game.has_flag(str(start.get("flag", "")))
			if ok:
				if state != State.ACTIVE:
					start_quest(qid)
			continue
		if state == State.LOCKED:
			_set_state(qid, State.AVAILABLE)
			if not silent:
				quest_available.emit(qid)


func _requirements_met(qid: String) -> bool:
	var def := Data.get_quest(qid)
	var req: Dictionary = def.get("requires", {})
	for other in req.get("quests", []):
		if not is_completed(str(other)):
			return false
	for flag in req.get("flags", []):
		if not Game.has_flag(str(flag)):
			return false
	var forbid: Array = def.get("forbid_flags", [])
	for flag in forbid:
		if Game.has_flag(str(flag)):
			return false
	var region := str(def.get("region", ""))
	if region != "" and region != "prologue" and not Game.unlocked_regions.has(region):
		return false
	return true


func _set_state(qid: String, state: int) -> void:
	states[qid] = state
	quest_state_changed.emit(qid, STATE_NAMES[state])


# ------------------------------------------------------------------ actions
func start_quest(qid: String, announce := true) -> void:
	if qid == "" or not Data.quests.has(qid):
		return
	var state := state_of(qid)
	if state == State.ACTIVE:
		return
	if state == State.COMPLETED:
		return
	_set_state(qid, State.ACTIVE)
	if not progress.has(qid):
		progress[qid] = {}
	for obj in Data.get_quest(qid).get("objectives", []):
		var oid := str(obj.get("id", ""))
		if not progress[qid].has(oid):
			progress[qid][oid] = 0
	if tracked == "" or not is_active(tracked):
		set_tracked(qid)
	if announce:
		var def := Data.get_quest(qid)
		Audio.sfx("ui_confirm", -4.0)
		Notify.banner("New Quest", str(def.get("title", qid)), str(def.get("region", "")).capitalize())
	_refresh_objectives(qid)
	_check_completion(qid)
	Game.state_changed.emit("quest_started", {"quest": qid})


func set_objective(quest_id: String, objective_id: String, value: int) -> void:
	if not is_active(quest_id):
		return
	if not progress.has(quest_id):
		progress[quest_id] = {}
	progress[quest_id][objective_id] = value
	objective_updated.emit(quest_id, objective_id)
	_check_completion(quest_id)


func add_objective(quest_id: String, objective_id: String, amount := 1) -> void:
	var obj := _find_objective(quest_id, objective_id)
	var need := int(obj.get("count", 1))
	var cur := objective_progress(quest_id, objective_id)
	if cur >= need:
		return
	var next := mini(need, cur + amount)
	set_objective(quest_id, objective_id, next)
	if next < need:
		var text := str(obj.get("text", ""))
		Notify.toast("%s  (%d/%d)" % [text, next, need], Color(0.85, 1.0, 0.9))


func _find_objective(quest_id: String, objective_id: String) -> Dictionary:
	for obj in Data.get_quest(quest_id).get("objectives", []):
		if str(obj.get("id", "")) == objective_id:
			return obj
	return {}


## Called by the world whenever something happens: gates every objective.
func notify_event(kind: String, target: String, amount := 1) -> void:
	for qid in active_quests():
		for obj in Data.get_quest(qid).get("objectives", []):
			if str(obj.get("type", "")) != kind:
				continue
			var obj_target := str(obj.get("target", ""))
			if obj_target != target:
				continue
			var oid := str(obj.get("id", ""))
			match kind:
				"talk", "reach", "landmark", "minigame", "puzzle", "discover":
					set_objective(qid, oid, int(obj.get("count", 1)))
				_:
					add_objective(qid, oid, amount)
	_refresh_objectives("")


func _refresh_objectives(quest_id: String) -> void:
	# collect / flag objectives are derived from the world state every time
	var targets := [quest_id] if quest_id != "" else active_quests()
	for qid in targets:
		if not is_active(qid):
			continue
		for obj in Data.get_quest(qid).get("objectives", []):
			var otype := str(obj.get("type", ""))
			var oid := str(obj.get("id", ""))
			var target := str(obj.get("target", ""))
			match otype:
				"collect":
					var have := Items.count(target)
					if have != objective_progress(qid, oid):
						set_objective(qid, oid, mini(have, int(obj.get("count", 1))))
				"flag":
					if Game.has_flag(target) and objective_progress(qid, oid) < int(obj.get("count", 1)):
						set_objective(qid, oid, int(obj.get("count", 1)))


func _check_completion(quest_id: String) -> void:
	if not is_active(quest_id):
		return
	var def := Data.get_quest(quest_id)
	var all_done := true
	for obj in def.get("objectives", []):
		var need := int(obj.get("count", 1))
		if objective_progress(quest_id, str(obj.get("id", ""))) < need:
			all_done = false
			break
	if not all_done:
		return
	var complete: Dictionary = def.get("complete", {"type": "auto"})
	match str(complete.get("type", "auto")):
		"talk":
			# wait for the player to report back to the NPC
			if not Game.has_flag("_ready_" + quest_id):
				Game.set_flag("_ready_" + quest_id, true)
				Notify.banner("Objective complete", "Report back to %s" %
					Data.get_npc(str(complete.get("npc", ""))).get("name", "the quest giver"))
			return
		"flag":
			if not Game.has_flag(str(complete.get("flag", ""))):
				return
	complete_quest(quest_id)


func complete_quest(quest_id: String) -> void:
	if is_completed(quest_id):
		return
	_set_state(quest_id, State.COMPLETED)
	var def := Data.get_quest(quest_id)
	var rewards: Dictionary = def.get("rewards", {})

	Game.bump("quests_completed")
	Game.add_culture_points(int(rewards.get("culture_points", Game.CP_QUEST)), "quest:" + quest_id)

	for item_id in rewards.get("items", []):
		Items.add(str(item_id), 1)
	for entry_id in rewards.get("culture", []):
		Culture.discover(str(entry_id), true)
	for flag in rewards.get("flags", []):
		Game.set_flag(str(flag), true)
	if rewards.has("unlock_map"):
		World.unlock_map(str(rewards["unlock_map"]))
	if rewards.has("unlock_region"):
		Game.unlock_region(str(rewards["unlock_region"]))
	Game.set_flag("quest_done_" + quest_id, true)

	Audio.quest_complete()
	Notify.banner("QUEST COMPLETE", str(def.get("title", quest_id)),
			"+%d Culture Points" % int(rewards.get("culture_points", Game.CP_QUEST)), 3.4)
	if tracked == quest_id:
		var act := active_quests()
		set_tracked(act[0] if act.size() > 0 else "")
	quest_completed.emit(quest_id)
	refresh_availability()
	Achievements.check_all()
	Game.state_changed.emit("quest_completed", {"quest": quest_id})


## Called by the dialogue system when a quest's "complete.npc" is talked to.
func try_turn_in(quest_id: String, npc_id: String) -> bool:
	if not is_active(quest_id):
		return false
	var complete: Dictionary = Data.get_quest(quest_id).get("complete", {})
	if str(complete.get("type", "")) == "talk" and str(complete.get("npc", "")) == npc_id \
			and Game.has_flag("_ready_" + quest_id):
		Game.set_flag("_ready_" + quest_id, false)
		complete_quest(quest_id)
		return true
	return false


func on_flag_changed(_flag: String, _value) -> void:
	refresh_availability()
	_refresh_objectives("")


func on_item_changed() -> void:
	_refresh_objectives("")
	refresh_availability()


## Quests the given NPC can offer right now (used by the dialogue system).
func quests_offered_by(npc_id: String) -> Array:
	var out: Array = []
	for qid in Data.quests.keys():
		var def := Data.get_quest(qid)
		if str(def.get("giver", "")) != npc_id:
			continue
		if state_of(qid) == State.AVAILABLE and _requirements_met(qid) \
				and str(def.get("start", {}).get("type", "talk")) == "talk":
			out.append(qid)
	return out


func active_quests_of(npc_id: String) -> Array:
	var out: Array = []
	for qid in active_quests():
		var def := Data.get_quest(qid)
		var complete: Dictionary = def.get("complete", {})
		if str(complete.get("npc", "")) == npc_id and Game.has_flag("_ready_" + qid):
			out.append(qid)
	return out


func region_stats(region: String) -> Dictionary:
	var ids := Data.get_quests_in_region(region)
	var done := 0
	var active := 0
	for qid in ids:
		if is_completed(qid):
			done += 1
		elif is_active(qid):
			active += 1
	return {"total": ids.size(), "completed": done, "active": active,
			"percent": (float(done) / max(1, ids.size())) * 100.0}


func to_dict() -> Dictionary:
	return {"states": states.duplicate(), "progress": progress.duplicate(true),
			"tracked": tracked}


func from_dict(d: Dictionary) -> void:
	states = {}
	var raw: Dictionary = d.get("states", {})
	for k in raw.keys():
		var v = raw[k]
		if typeof(v) == TYPE_STRING:
			# tolerate older saves storing the state name
			states[str(k)] = STATE_NAMES.find(str(v))
		else:
			states[str(k)] = int(v)
	progress = d.get("progress", {}).duplicate(true)
	for qid in progress.keys():
		progress[qid] = progress[qid].duplicate(true)
	tracked = str(d.get("tracked", ""))
