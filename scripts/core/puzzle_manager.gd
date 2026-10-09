extends Node
## PuzzleManager (autoload "Puzzle")
##
## Owns the puzzle / mini-game framework:
##   * opens the right mini-game scene for a puzzle definition
##   * feeds it its data (state is kept in the save file so puzzles survive a
##     reload)
##   * applies rewards, runs the 3-step hint system and never lets a player get
##     permanently stuck (every puzzle can be reset or exited).

signal puzzle_started(puzzle_id: String)
signal puzzle_finished(puzzle_id: String, success: bool, score: int)
signal hint_used(puzzle_id: String, level: int)

const SCENES := {
	"memory": "res://scenes/minigames/memory_match.tscn",
	"pattern": "res://scenes/minigames/pattern_copy.tscn",
	"sequence": "res://scenes/minigames/sequence_tap.tscn",
	"rhythm": "res://scenes/minigames/rhythm.tscn",
	"tile": "res://scenes/minigames/tile_rotate.tscn",
	"match": "res://scenes/minigames/matching.tscn",
	"logic": "res://scenes/minigames/logic_flow.tscn",
	"cooking": "res://scenes/minigames/cooking.tscn",
	"crafting": "res://scenes/minigames/crafting.tscn",
	"exploration": "res://scenes/minigames/clue_board.tscn",
	"environment": "res://scenes/minigames/environment.tscn",
	"quiz": "res://scenes/minigames/quiz.tscn",
	"nod": "res://scenes/minigames/nod.tscn",
}

var states: Dictionary = {}          # puzzle_id -> arbitrary saved state
var solved: Array = []
var attempts: Dictionary = {}        # puzzle_id -> int
var hints_used: Dictionary = {}      # puzzle_id -> int
var current_id := ""
var _instance: Node = null


# ------------------------------------------------------------------ queries
func is_solved(id: String) -> bool:
	return solved.has(id)


func attempts_of(id: String) -> int:
	return int(attempts.get(id, 0))


func hints_used_of(id: String) -> int:
	return int(hints_used.get(id, 0))


func save_state(id: String, state: Dictionary) -> void:
	states[id] = state.duplicate(true)


func load_state(id: String) -> Dictionary:
	return states.get(id, {})


func clear_state(id: String) -> void:
	states.erase(id)


func hints_for(id: String) -> Array:
	return Data.get_puzzle(id).get("hints", [])


# ------------------------------------------------------------------- opening
func request(puzzle_id: String, context := "") -> void:
	open(puzzle_id, {"source": context})


func open(puzzle_id: String, context := {}) -> bool:
	if _instance != null:
		return false
	var def := Data.get_puzzle(puzzle_id)
	if def.is_empty():
		push_warning("Unknown puzzle: " + puzzle_id)
		return false
	var type := str(def.get("type", "logic"))
	if not SCENES.has(type):
		push_warning("No scene for puzzle type: " + type)
		return false
	if not ResourceLoader.exists(SCENES[type]):
		# fall back to the generic flow puzzle so the quest never soft-locks
		if not ResourceLoader.exists(SCENES["logic"]):
			push_warning("Puzzle scene missing: " + str(SCENES[type]))
			complete_puzzle(puzzle_id, 0)
			return false
		type = "logic"
	current_id = puzzle_id
	attempts[puzzle_id] = attempts_of(puzzle_id) + 1
	Game.bump("puzzles_attempted")
	var scene := load(SCENES[type]) as PackedScene
	_instance = scene.instantiate()
	_instance.name = "Puzzle_" + puzzle_id
	UI.attach_puzzle(_instance)
	if _instance.has_method("setup"):
		_instance.setup(def, self, context)
	if _instance.has_signal("finished"):
		_instance.finished.connect(_on_puzzle_finished)
	if _instance.has_signal("hint_requested"):
		_instance.hint_requested.connect(_on_hint_requested)
	puzzle_started.emit(puzzle_id)
	Game.state_changed.emit("puzzle_started", {"puzzle": puzzle_id})
	return true


func _on_puzzle_finished(success: bool, score: int) -> void:
	var puzzle_id := current_id
	_close_instance()
	if success:
		complete_puzzle(puzzle_id, score)
	else:
		Audio.puzzle_wrong()
		Notify.toast("Not quite - press H for a hint or R to reset.", Color(1, 0.85, 0.7))
	puzzle_finished.emit(puzzle_id, success, score)


func _close_instance() -> void:
	if _instance != null:
		_instance.queue_free()
		_instance = null
	current_id = ""
	UI.detach_puzzle()
	Quest.refresh_availability()


func close_current() -> void:
	if _instance != null:
		if _instance.has_method("can_exit") and not _instance.can_exit():
			return
		_close_instance()
		Audio.ui_click()


func complete_puzzle(puzzle_id: String, score := 100) -> void:
	if is_solved(puzzle_id):
		return
	solved.append(puzzle_id)
	Game.bump("puzzles_completed")
	Game.add_culture_points(Game.CP_PUZZLE, "puzzle:" + puzzle_id)
	Game.state_changed.emit("puzzle_solved", {"puzzle": puzzle_id})
	Audio.puzzle_solved()
	var def := Data.get_puzzle(puzzle_id)
	for entry_id in def.get("rewards", {}).get("culture", []):
		Culture.discover(str(entry_id), true)
	for item_id in def.get("rewards", {}).get("items", []):
		Items.add(str(item_id), 1)
	if def.get("rewards", {}).has("flag"):
		Game.set_flag(str(def["rewards"]["flag"]), true)
	Quest.notify_event("puzzle", puzzle_id)
	Quest.refresh_availability()
	Achievements.check_all()


func _on_hint_requested(level: int) -> void:
	if current_id == "":
		return
	var before := hints_used_of(current_id)
	hints_used[current_id] = maxi(before, level + 1)
	if level + 1 > before:
		Game.bump("hints_used")
		# hints cost a small amount of Culture Points but never block progress
		if Game.culture_points >= Game.CP_HINT_PENALTY:
			Game.add_culture_points(-Game.CP_HINT_PENALTY, "hint")
		hint_used.emit(current_id, level + 1)


# --------------------------------------------------------------- mini-games
func start_minigame(name: String, context := {}) -> void:
	var def := {
		"id": "minigame_" + name,
		"type": name,
		"title": context.get("title", name.capitalize()),
		"description": context.get("description", ""),
		"hints": context.get("hints", []),
		"reward_cp": int(context.get("reward_cp", Game.CP_MINIGAME)),
		"data": context.get("data", {}),
	}
	var id := str(def["id"])
	if not Data.puzzles.has(id):
		Data.puzzles[id] = def
	current_id = id
	attempts[id] = attempts_of(id) + 1
	var scene_path: String = SCENES.get(name, SCENES["logic"])
	if not ResourceLoader.exists(scene_path):
		scene_path = SCENES["logic"]
	var scene := load(scene_path) as PackedScene
	_instance = scene.instantiate()
	_instance.name = "Minigame_" + name
	UI.attach_puzzle(_instance)
	if _instance.has_method("setup"):
		_instance.setup(def, self, context)
	if _instance.has_signal("finished"):
		_instance.finished.connect(_on_minigame_finished)
	if _instance.has_signal("hint_requested"):
		_instance.hint_requested.connect(_on_hint_requested)
	puzzle_started.emit(id)


func _on_minigame_finished(success: bool, score: int) -> void:
	var id := current_id
	_close_instance()
	if success:
		Game.bump("minigames_completed")
		Game.add_culture_points(Game.CP_MINIGAME, "minigame")
		Audio.puzzle_solved()
		Quest.notify_event("minigame", id.replace("minigame_", ""))
		Quest.notify_event("minigame", id)
		Achievements.check_all()
	else:
		Audio.puzzle_wrong()
	puzzle_finished.emit(id, success, score)


# ------------------------------------------------------------- serialisation
func to_dict() -> Dictionary:
	return {"states": states.duplicate(true), "solved": solved.duplicate(),
			"attempts": attempts.duplicate(), "hints": hints_used.duplicate()}


func from_dict(d: Dictionary) -> void:
	states = d.get("states", {}).duplicate(true)
	solved = []
	for id in d.get("solved", []):
		solved.append(str(id))
	attempts = {}
	var raw: Dictionary = d.get("attempts", {})
	for k in raw.keys():
		attempts[str(k)] = int(raw[k])
	hints_used = {}
	var raw2: Dictionary = d.get("hints", {})
	for k in raw2.keys():
		hints_used[str(k)] = int(raw2[k])
