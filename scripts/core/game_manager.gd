extends Node
## GameManager (autoload "Game")
##
## Holds the run state (which region is unlocked, story chapter, culture points,
## world flags) and emits the events the rest of the game listens to.
## All mutable state lives here so SaveManager has a single source of truth.

signal state_changed(kind: String, data: Dictionary)
signal region_unlocked(region_id: String)
signal chapter_changed(index: int)
signal culture_points_changed(total: int)
signal flag_changed(flag: String, value)
signal game_started(is_new: bool)
signal story_finished()

const SAVE_VERSION := 3
const CP_CULTURE := 25
const CP_QUEST := 60
const CP_PUZZLE := 30
const CP_LANDMARK := 15
const CP_HIDDEN := 40
const CP_MINIGAME := 35
const CP_HINT_PENALTY := 5

var started := false             # a run is in progress
var current_region := "prologue"
var current_map := "desa_awal"
var last_position := Vector2.ZERO
var unlocked_regions: Array = ["prologue"]
var visited_regions: Array = []
var unlocked_maps: Array = []
var culture_points := 0
var play_time := 0.0
var story_chapter := 1
var flags: Dictionary = {}        # arbitrary story flags
var map_player_pos: Dictionary = {}   # map_id -> [x, y]
var stats := {
	"quests_completed": 0,
	"puzzles_completed": 0,
	"puzzles_attempted": 0,
	"minigames_completed": 0,
	"landmarks_found": 0,
	"hidden_areas_found": 0,
	"npcs_talked": 0,
	"hints_used": 0,
	"steps_taken": 0,
	"fast_travels": 0,
	"deaths": 0,
}
var landmarks: Array = []         # discovered landmark ids
var hidden_areas: Array = []
var talked_npcs: Array = []


func _process(delta: float) -> void:
	if started and not get_tree().paused:
		play_time += delta


# ------------------------------------------------------------------ new run
func new_game() -> void:
	current_region = "prologue"
	current_map = "desa_awal"
	last_position = Vector2.ZERO
	unlocked_regions = ["prologue"]
	visited_regions = []
	unlocked_maps = ["desa_awal"]
	culture_points = 0
	play_time = 0.0
	story_chapter = 1
	flags.clear()
	map_player_pos.clear()
	landmarks.clear()
	hidden_areas.clear()
	talked_npcs.clear()
	for key in stats.keys():
		stats[key] = 0
	started = true
	Items.reset()
	Quest.reset()
	Culture.reset()
	Achievements.reset()
	game_started.emit(true)
	state_changed.emit("new_game", {})


func mark_started(is_new: bool) -> void:
	started = true
	game_started.emit(is_new)


# ------------------------------------------------------------------- region
func is_region_unlocked(region_id: String) -> bool:
	if region_id == "prologue":
		return true
	# regions may require the previous one to be far enough along
	var def := Data.get_region(region_id)
	var requires: String = def.get("requires", "")
	if requires == "":
		return unlocked_regions.has(region_id)
	return unlocked_regions.has(region_id) and is_region_complete_enough(requires, float(def.get("requires_percent", 55.0)))


func unlock_region(region_id: String, silent := false) -> void:
	if unlocked_regions.has(region_id):
		return
	unlocked_regions.append(region_id)
	if not silent:
		region_unlocked.emit(region_id)
		Notify.achievement_banner("REGION UNLOCKED", Data.get_region(region_id).get("name", region_id))
	state_changed.emit("region_unlocked", {"region": region_id})


func enter_region(region_id: String) -> void:
	current_region = region_id
	if not visited_regions.has(region_id):
		visited_regions.append(region_id)
		Culture.discover_implicit_entries(region_id)
		state_changed.emit("region_visited", {"region": region_id})
		Achievements.check_all()


func is_region_complete_enough(region_id: String, percent: float) -> bool:
	return region_progress_percent(region_id) >= percent


func region_progress_percent(region_id: String) -> float:
	var quest_ids := Data.get_quests_in_region(region_id)
	var region_map_ids := Data.maps_of(region_id)
	var total := quest_ids.size() + region_map_ids.size() + landmarks_in_region(region_id).size()
	if total == 0:
		return 0.0
	var done := 0
	for qid in quest_ids:
		if Quest.is_completed(qid):
			done += 1
	for mid in region_map_ids:
		if unlocked_maps.has(mid):
			done += 1
	for lm in landmarks_in_region(region_id):
		if landmarks.has(lm["id"]):
			done += 1
	return clampf(float(done) / float(total) * 100.0, 0.0, 100.0)


func landmarks_in_region(region_id: String) -> Array:
	var out: Array = []
	for mid in Data.maps_of(region_id):
		var m: Dictionary = Data.get_map(mid)
		for lm in m.get("landmarks", []):
			if not out.any(func(e): return e["id"] == lm["id"]):
				out.append(lm)
	return out


func region_state(region_id: String) -> String:
	if region_id == "prologue" or unlocked_regions.has(region_id):
		var p := region_progress_percent(region_id)
		if p >= 100.0 and visited_regions.has(region_id):
			return "completed"
		if visited_regions.has(region_id):
			return "in_progress"
		return "unlocked"
	return "locked"


# ------------------------------------------------------------------ chapter
func set_chapter(index: int) -> void:
	if index == story_chapter and flags.get("chapter_started_" + str(index), false):
		return
	story_chapter = index
	flags["chapter_started_" + str(index)] = true
	chapter_changed.emit(index)
	state_changed.emit("chapter", {"index": index})


# ------------------------------------------------------------------- points
func add_culture_points(amount: int, reason := "") -> void:
	if amount == 0:
		return
	culture_points = maxi(0, culture_points + amount)
	culture_points_changed.emit(culture_points)
	state_changed.emit("cp", {"amount": amount, "total": culture_points, "reason": reason})


func spend_culture_points(amount: int) -> bool:
	if culture_points < amount:
		return false
	add_culture_points(-amount, "spend")
	return true


# -------------------------------------------------------------------- flags
func set_flag(flag: String, value := true) -> void:
	if flags.get(flag, null) == value:
		return
	flags[flag] = value
	flag_changed.emit(flag, value)
	state_changed.emit("flag", {"flag": flag, "value": value})
	Quest.on_flag_changed(flag, value)
	Achievements.check_all()


func get_flag(flag: String, default = false):
	return flags.get(flag, default)


func has_flag(flag: String) -> bool:
	return bool(flags.get(flag, false))


# -------------------------------------------------------------------- stats
func bump(stat: String, amount := 1) -> void:
	stats[stat] = int(stats.get(stat, 0)) + amount
	state_changed.emit("stat", {"stat": stat, "value": stats[stat]})
	Achievements.check_all()


func discover_landmark(id: String, title: String, subtitle := "") -> void:
	if landmarks.has(id):
		return
	landmarks.append(id)
	bump("landmarks_found")
	add_culture_points(CP_LANDMARK, "landmark")
	Notify.banner("Landmark Discovered", title, subtitle)
	state_changed.emit("landmark", {"id": id})
	Achievements.check_all()


func discover_hidden_area(id: String, title: String, hint := "") -> void:
	if hidden_areas.has(id):
		return
	hidden_areas.append(id)
	bump("hidden_areas_found")
	add_culture_points(CP_HIDDEN, "hidden")
	Notify.banner("Hidden Area Found", title, hint)
	state_changed.emit("hidden", {"id": id})
	Achievements.check_all()


func note_npc_talked(npc_id: String) -> void:
	if talked_npcs.has(npc_id):
		return
	talked_npcs.append(npc_id)
	bump("npcs_talked")


# ------------------------------------------------------------- serialisation
func to_dict() -> Dictionary:
	return {
		"version": SAVE_VERSION,
		"current_region": current_region,
		"current_map": current_map,
		"last_position": [last_position.x, last_position.y],
		"unlocked_regions": unlocked_regions.duplicate(),
		"visited_regions": visited_regions.duplicate(),
		"unlocked_maps": unlocked_maps.duplicate(),
		"culture_points": culture_points,
		"play_time": play_time,
		"story_chapter": story_chapter,
		"flags": flags.duplicate(true),
		"map_player_pos": map_player_pos.duplicate(true),
		"stats": stats.duplicate(),
		"landmarks": landmarks.duplicate(),
		"hidden_areas": hidden_areas.duplicate(),
		"talked_npcs": talked_npcs.duplicate(),
	}


func from_dict(d: Dictionary) -> void:
	current_region = str(d.get("current_region", "prologue"))
	current_map = str(d.get("current_map", "desa_awal"))
	var lp = d.get("last_position", [0, 0])
	last_position = Vector2(float(lp[0]), float(lp[1]))
	unlocked_regions = _arr(d.get("unlocked_regions", ["prologue"]))
	visited_regions = _arr(d.get("visited_regions", []))
	unlocked_maps = _arr(d.get("unlocked_maps", ["desa_awal"]))
	culture_points = int(d.get("culture_points", 0))
	play_time = float(d.get("play_time", 0.0))
	story_chapter = int(d.get("story_chapter", 1))
	flags = d.get("flags", {}).duplicate(true)
	map_player_pos = d.get("map_player_pos", {}).duplicate(true)
	stats = d.get("stats", {}).duplicate()
	for key in stats.keys():
		stats[key] = int(stats[key])
	landmarks = _arr(d.get("landmarks", []))
	hidden_areas = _arr(d.get("hidden_areas", []))
	talked_npcs = _arr(d.get("talked_npcs", []))
	started = true


func _arr(value) -> Array:
	var out: Array = []
	if value is Array:
		for v in value:
			out.append(str(v))
	return out


func play_time_string() -> String:
	var t := int(play_time)
	return "%02d:%02d:%02d" % [t / 3600, (t % 3600) / 60, t % 60]


func current_map_def() -> Dictionary:
	return Data.get_map(current_map)
