extends Node
## DialogueManager (autoload "Dialogue")
##
## Runtime for data driven dialogue trees (data/dialogues.json):
## {
##   "start": "node_id",
##   "nodes": {
##     "node_id": {
##       "speaker": "npc_id",
##       "lines": ["...", "..."],
##       "choices": [ {"text": "...", "goto": "node", "if": {...}, "do": {...}} ],
##       "goto": "next_node",
##       "do": {"start_quest": "q", "set_flag": "f", "give_item": "i",
##              "discover": "culture", "cp": 10, "unlock_region": "java",
##              "open_puzzle": "p", "open_minigame": "m", "end": true}
##     }
##   }
## }
##
## The UI (scenes/ui/dialogue_box.tscn) is intentionally dumb: it renders what
## this manager tells it to and reports back clicks.

signal started(dialogue_id: String)
signal finished(dialogue_id: String)
signal node_entered(dialogue_id: String, node_id: String)

var active := false
var dialogue_id := ""
var current_node := ""
var _context: Dictionary = {}


func start(id: String, context := {}) -> bool:
	var tree := Data.get_dialogue(id)
	if tree.is_empty():
		push_warning("Unknown dialogue: " + id)
		return false
	dialogue_id = id
	_context = context
	active = true
	var start_node := str(tree.get("start", ""))
	if start_node == "" or not tree.get("nodes", {}).has(start_node):
		active = false
		return false
	started.emit(id)
	_enter(start_node)
	return true


func _enter(node_id: String) -> void:
	if not active:
		return
	var tree := Data.get_dialogue(dialogue_id)
	var nodes: Dictionary = tree.get("nodes", {})
	if not nodes.has(node_id):
		finish()
		return
	current_node = node_id
	var node: Dictionary = nodes[node_id]
	if node.has("do"):
		_apply_effects(node["do"])
	# effects may have ended the dialogue or opened a sub screen
	if not active:
		return
	node_entered.emit(dialogue_id, node_id)
	UI.open_dialogue_node(dialogue_id, node, _context)


func choose(index: int) -> void:
	var tree := Data.get_dialogue(dialogue_id)
	var node: Dictionary = tree.get("nodes", {}).get(current_node, {})
	var choices: Array = _visible_choices(node)
	if index < 0 or index >= choices.size():
		return
	var choice: Dictionary = choices[index]
	if choice.has("do"):
		_apply_effects(choice["do"])
	if not active:
		return
	if choice.has("goto"):
		_enter(str(choice["goto"]))
	else:
		_advance()


func _visible_choices(node: Dictionary) -> Array:
	var out: Array = []
	for choice in node.get("choices", []):
		if _conditions_ok(choice.get("if", {})):
			out.append(choice)
	return out


func _conditions_ok(cond: Dictionary) -> bool:
	for key in cond.keys():
		var v = cond[key]
		match key:
			"flag":
				if not Game.has_flag(str(v)):
					return false
			"no_flag":
				if Game.has_flag(str(v)):
					return false
			"quest_active":
				if not Quest.is_active(str(v)):
					return false
			"quest_done":
				if not Quest.is_completed(str(v)):
					return false
			"quest_available":
				if Quest.state_of(str(v)) != Quest.State.AVAILABLE:
					return false
			"has_item":
				var parts := str(v).split(":")
				var need := int(parts[1]) if parts.size() > 1 else 1
				if not Items.has(parts[0], need):
					return false
			"culture":
				if not Culture.is_discovered(str(v)):
					return false
			"region_unlocked":
				if not Game.unlocked_regions.has(str(v)):
					return false
			"chapter":
				if Game.story_chapter < int(v):
					return false
			"cp":
				if Game.culture_points < int(v):
					return false
			_:
				pass
	return true


## Called by the dialogue UI when the last line has been read.
func advance() -> void:
	var tree := Data.get_dialogue(dialogue_id)
	var node: Dictionary = tree.get("nodes", {}).get(current_node, {})
	if _visible_choices(node).size() > 0:
		UI.show_dialogue_choices(_visible_choices(node))
		return
	_advance()


func _advance() -> void:
	var tree := Data.get_dialogue(dialogue_id)
	var node: Dictionary = tree.get("nodes", {}).get(current_node, {})
	if node.has("goto"):
		_enter(str(node["goto"]))
	else:
		finish()


func finish() -> void:
	if not active:
		return
	active = false
	var finished_id := dialogue_id
	dialogue_id = ""
	current_node = ""
	_context.clear()
	UI.close_dialogue()
	finished.emit(finished_id)
	Quest.refresh_availability()
	Achievements.check_all()


func _apply_effects(effects: Dictionary) -> void:
	for key in effects.keys():
		var value = effects[key]
		match key:
			"start_quest":
				Quest.start_quest(str(value))
			"complete_quest":
				Quest.complete_quest(str(value))
			"set_flag":
				Game.set_flag(str(value), true)
			"clear_flag":
				Game.set_flag(str(value), false)
			"give_item":
				var parts := str(value).split(":")
				Items.add(parts[0], int(parts[1]) if parts.size() > 1 else 1)
			"take_item":
				var parts2 := str(value).split(":")
				Items.remove(parts2[0], int(parts2[1]) if parts2.size() > 1 else 1)
			"discover":
				Culture.discover(str(value), true)
			"cp":
				Game.add_culture_points(int(value), "dialogue")
			"unlock_region":
				Game.unlock_region(str(value))
			"unlock_map":
				World.unlock_map(str(value))
			"chapter":
				Game.set_chapter(int(value))
			"open_puzzle":
				Puzzle.request(str(value), _context.get("npc", ""))
			"open_minigame":
				UI.open_minigame(str(value))
			"open_shop":
				UI.open("shop")
			"teleport":
				World.fast_travel(str(value))
			"end":
				if bool(value):
					finish()
			"sound":
				Audio.sfx(str(value), -6.0)
			_:
				push_warning("Unknown dialogue effect: " + key)


func is_dialogue_available(npc_id: String) -> Dictionary:
	## Picks the best dialogue for an NPC: report-back > quest offer > idle chat.
	var result := {}
	var quest_defs: Array = []
	for qid in Quest.active_quests_of(npc_id):
		quest_defs.append(qid)
	if quest_defs.size() > 0:
		result = {"type": "turn_in", "quest": quest_defs[0]}
	var offered := Quest.quests_offered_by(npc_id)
	if offered.size() > 0 and result.is_empty():
		result = {"type": "offer", "quest": offered[0]}
	if result.is_empty():
		result = {"type": "dialogue"}
	return result
