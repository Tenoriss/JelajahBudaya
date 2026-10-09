extends Node
## WorldManager (autoload "World")
##
## Region / map loading, transitions, fast travel and the day-night cycle.
## The actual world scene is created here and handed to the running game scene
## through a signal so the game scene stays tiny.

signal map_loaded(map_id: String)
signal map_unloaded(map_id: String)
signal transition_started(kind: String)
signal transition_finished(kind: String)

const WORLD_HOLDER := "/root/Game/WorldHolder"

enum TimeOfDay { MORNING, DAY, EVENING, NIGHT }

var day_time := 8.5                # 0..24
var time_scale := 0.06             # in-game minutes per real second
var paused_time := false
var current_map_id := ""
var world_root: Node2D = null
var player: Node2D = null          # registered by the world scene
var transition: ColorRect = null
var weather := "clear"


func _ready() -> void:
	set_process(false)


func _process(delta: float) -> void:
	if paused_time or not Game.started:
		return
	var before := time_of_day()
	day_time = fmod(day_time + delta * time_scale * 60.0 / 60.0, 24.0)
	if time_of_day() != before:
		Game.state_changed.emit("time_of_day", {"phase": time_of_day()})


func time_of_day() -> int:
	if day_time < 6.0:
		return TimeOfDay.NIGHT
	if day_time < 11.0:
		return TimeOfDay.MORNING
	if day_time < 17.0:
		return TimeOfDay.DAY
	if day_time < 20.0:
		return TimeOfDay.EVENING
	return TimeOfDay.NIGHT


func time_name() -> String:
	return ["Morning", "Day", "Evening", "Night"][time_of_day()]


func time_string() -> String:
	return "%02d:%02d" % [int(day_time), int(fmod(day_time * 60.0, 60.0))]


# ------------------------------------------------------------------- loading
func load_map(map_id: String, spawn: Vector2 = Vector2.INF, entry_id := "") -> void:
	var def := Data.get_map(map_id)
	if def.is_empty():
		push_error("Unknown map: " + map_id)
		return
	if world_root != null:
		map_unloaded.emit(current_map_id)
		world_root.queue_free()
		world_root = null
	var holder := _holder()
	if holder == null:
		push_error("WorldHolder not found; cannot load map")
		return
	var scene := WorldBuilder.build(def)
	if scene == null:
		push_error("WorldBuilder failed for " + map_id)
		return
	world_root = scene
	holder.add_child(world_root)
	current_map_id = map_id
	Game.current_map = map_id
	unlock_map(map_id)
	Game.enter_region(str(def.get("region", "prologue")))
	# entering a region opens its roads: every map of the region becomes reachable
	for mid in Data.maps_of(str(def.get("region", "prologue"))):
		unlock_map(str(mid))
	var region := Data.get_region(str(def.get("region", "")))
	if region.size() > 0 and not Game.has_flag("regioncard_" + str(def.get("region", ""))):
		Game.set_flag("regioncard_" + str(def.get("region", "")), true)
		Notify.show_region_card(region)
		Audio.play_music(str(region.get("music", "prologue")))
	else:
		Audio.play_music(str(def.get("music", region.get("music", "prologue"))))
	if def.has("ambience"):
		Audio.play_ambience(str(def["ambience"]))
	# where does the player come out?  an explicit spot (fast travel / load game),
	# the door they walked out of (entry id), or wherever the fresh player spawned.
	var spawn_pos := spawn
	if spawn_pos == Vector2.INF:
		if entry_id != "" and world_root.has_method("entry_point"):
			spawn_pos = world_root.entry_point(entry_id)
		elif world_root != null and world_root.get("player") != null:
			spawn_pos = world_root.player.position
		else:
			spawn_pos = _default_spawn()
	if world_root != null and world_root.get("player") != null and is_instance_valid(world_root.player):
		world_root.player.position = spawn_pos
	UI.on_map_loaded(def)
	map_loaded.emit(map_id)
	Game.state_changed.emit("map_loaded", {"map": map_id})
	Game.map_player_pos[map_id] = [spawn_pos.x, spawn_pos.y]
	Achievements.check_all()


## Registered by the world scene so transitions can remember the player spot.
func register_player(node: Node2D) -> void:
	player = node


func player_position() -> Vector2:
	if player != null and is_instance_valid(player):
		return player.global_position
	return Vector2.ZERO


func _default_spawn() -> Vector2:
	if Game.map_player_pos.has(current_map_id):
		var p = Game.map_player_pos[current_map_id]
		return Vector2(float(p[0]), float(p[1]))
	var map := Data.get_map(current_map_id)
	var spawn = map.get("spawn", [400, 400])
	return Vector2(float(spawn[0]), float(spawn[1]))


func _holder() -> Node:
	var game := get_tree().root.get_node_or_null("Game")
	if game == null:
		return null
	return game.get_node_or_null("WorldHolder")


func unlock_map(map_id: String) -> void:
	if not Game.unlocked_maps.has(map_id):
		Game.unlocked_maps.append(map_id)
		Game.state_changed.emit("map_unlocked", {"map": map_id})


func is_map_unlocked(map_id: String) -> bool:
	return Game.unlocked_maps.has(map_id)


# ---------------------------------------------------------------- transitions
func change_map(map_id: String, spawn: Vector2 = Vector2.INF, entry_id := "", fade := 0.45) -> void:
	if not is_map_unlocked(map_id):
		Audio.ui_error()
		Notify.toast("That road is still closed.")
		return
	if current_map_id != "" and player != null and is_instance_valid(player) and player.is_inside_tree():
		Game.map_player_pos[current_map_id] = [player.global_position.x, player.global_position.y]
	transition_started.emit("map")
	await fade_out(fade)
	load_map(map_id, spawn, entry_id)
	await get_tree().process_frame
	await fade_in(fade)
	transition_finished.emit("map")


func fast_travel(landmark_id: String) -> void:
	var target := find_landmark(landmark_id)
	if target.is_empty():
		Audio.ui_error()
		Notify.toast("Unknown destination.")
		return
	if not is_map_unlocked(str(target["map"])):
		Audio.ui_error()
		Notify.toast("You have not discovered that place yet.")
		return
	Audio.sfx("ui_confirm", -4.0)
	Game.bump("fast_travels")
	await transition_flash()
	var p: Array = target.get("pos", [0, 0])
	load_map(str(target["map"]), Vector2(float(p[0]), float(p[1]) + 24.0))
	Notify.banner("Fast Travel", str(target.get("name", "")), "", 2.0)


func find_landmark(landmark_id: String) -> Dictionary:
	for map_id in Data.maps.keys():
		var map: Dictionary = Data.maps[map_id]
		for lm in map.get("landmarks", []):
			if str(lm.get("id", "")) == landmark_id:
				var out := lm.duplicate()
				out["map"] = map_id
				out["region"] = map.get("region", "")
				return out
	return {}


func all_landmarks(region := "") -> Array:
	var out: Array = []
	for map_id in Data.maps.keys():
		var map: Dictionary = Data.maps[map_id]
		if region != "" and str(map.get("region", "")) != region:
			continue
		for lm in map.get("landmarks", []):
			var entry := lm.duplicate()
			entry["map"] = map_id
			entry["region"] = map.get("region", "")
			entry["discovered"] = Game.landmarks.has(str(lm.get("id", "")))
			out.append(entry)
	out.sort_custom(func(a, b): return str(a.get("name", "")) < str(b.get("name", "")))
	return out


# ----------------------------------------------------------------- fade f/x
func _ensure_transition() -> bool:
	if transition != null and is_instance_valid(transition):
		return true
	var game := get_tree().root.get_node_or_null("Game")
	if game == null:
		return false
	var layer := game.get_node_or_null("Overlay") as CanvasLayer
	if layer == null:
		layer = CanvasLayer.new()
		layer.name = "Overlay"
		layer.layer = 50
		game.add_child(layer)
	transition = ColorRect.new()
	transition.color = Color(0.06, 0.05, 0.08, 0.0)
	transition.set_anchors_preset(Control.PRESET_FULL_RECT)
	transition.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(transition)
	return true


func fade_out(duration := 0.4, color := Color(0.06, 0.05, 0.08)) -> void:
	if not _ensure_transition():
		return
	transition.color = Color(color.r, color.g, color.b, 0.0)
	transition.visible = true
	var tw := create_tween()
	tw.tween_property(transition, "color:a", 1.0, duration)
	await tw.finished


func fade_in(duration := 0.4) -> void:
	if transition == null:
		return
	var tw := create_tween()
	tw.tween_property(transition, "color:a", 0.0, duration)
	await tw.finished
	transition.visible = false


func transition_flash() -> void:
	if not _ensure_transition():
		return
	transition.color = Color(0.98, 0.92, 0.8, 0.0)
	transition.visible = true
	var tw := create_tween()
	tw.tween_property(transition, "color:a", 0.85, 0.25)
	tw.tween_interval(0.1)
	tw.tween_property(transition, "color:a", 0.0, 0.35)
	await tw.finished
	transition.visible = false


func weather_particles_for(region: String) -> String:
	match region:
		"kalimantan":
			return "rain_light"
		"papua":
			return "mist"
	return "none"
