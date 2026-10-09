extends Node2D
## Runtime map: owns the tilemap, objects, NPCs, interactables, landmarks and
## the player.  Built by WorldBuilder from a data/maps/*.json definition.

const TILE := 32

var map_def: Dictionary = {}
var map_id := ""
var region := ""
var bounds := Vector2(1600, 1200)

var player: Node2D = null
var ground: TileMapLayer = null
var decor: Node2D = null
var entities: Node2D = null
var solids: StaticBody2D = null

var _anim_cells: Array = []          # [{cell, group, index}]
var _anim_time := 0.0
var _anim_frame := 0
var _entry_points: Dictionary = {}


# ------------------------------------------------------------------ setup
func setup_nodes() -> void:
	ground = TileMapLayer.new()
	ground.name = "Ground"
	ground.z_index = -20
	add_child(ground)

	decor = Node2D.new()
	decor.name = "Decor"
	decor.y_sort_enabled = true
	add_child(decor)

	entities = Node2D.new()
	entities.name = "Entities"
	entities.y_sort_enabled = true
	add_child(entities)

	solids = StaticBody2D.new()
	solids.name = "Solids"
	solids.collision_layer = 1
	solids.collision_mask = 0
	add_child(solids)


func add_solid_rect(rect: Rect2) -> void:
	if solids == null:
		setup_nodes()
	var shape := CollisionShape2D.new()
	var box := RectangleShape2D.new()
	box.size = rect.size
	shape.shape = box
	shape.position = rect.position + rect.size * 0.5
	solids.add_child(shape)


func register_anim_cell(cell: Vector2i, group: String, index: int) -> void:
	_anim_cells.append({"cell": cell, "group": group, "index": index})


func setup_bounds(size: Vector2) -> void:
	bounds = size


func finish_setup() -> void:
	var scene := load("res://scenes/player/player.tscn") as PackedScene
	player = scene.instantiate()
	player.position = _spawn_position()
	add_child(player)
	World.register_player(player)
	var cam := player.get_node_or_null("Camera2D") as Camera2D
	if cam:
		cam.limit_left = 0
		cam.limit_top = 0
		cam.limit_right = int(bounds.x)
		cam.limit_bottom = int(bounds.y)
		cam.reset_smoothing()
	Game.map_player_pos[map_id] = [player.position.x, player.position.y]
	UI.notify_map_ready(self)
	Quest.notify_event("reach", map_id)


func _spawn_position() -> Vector2:
	var spawn = map_def.get("spawn", [4, 4])
	var pos := Vector2(float(spawn[0]) * TILE + TILE * 0.5, float(spawn[1]) * TILE + TILE * 0.5)
	if Game.map_player_pos.has(map_id):
		var p = Game.map_player_pos[map_id]
		var saved := Vector2(float(p[0]), float(p[1]))
		if saved != Vector2.ZERO:
			pos = saved
	return pos


func entry_point(entry_id: String) -> Vector2:
	if entry_id != "" and _entry_points.has(entry_id):
		return _entry_points[entry_id] + Vector2(0, 26)
	return _spawn_position()


# ------------------------------------------------------------------ runtime
func _process(delta: float) -> void:
	if _anim_cells.is_empty():
		return
	_anim_time += delta
	if _anim_time < 0.28:
		return
	_anim_time = 0.0
	_anim_frame += 1
	var tiles: Dictionary = Data.tilesets.get(region, {}).get("tiles", {})
	var groups: Dictionary = Data.tilesets.get(region, {}).get("animations", {})
	for entry in _anim_cells:
		var names: Array = groups.get(entry["group"], [])
		if names.is_empty():
			continue
		var idx := (int(entry["index"]) + _anim_frame) % names.size()
		var info: Dictionary = tiles.get(str(names[idx]), {})
		if info.is_empty():
			continue
		var at: Array = info["atlas"]
		ground.set_cell(entry["cell"], 0, Vector2i(int(at[0]), int(at[1])))


# ---------------------------------------------------------------- spawning
func spawn_object(sprite_name: String, pos: Vector2, obj: Dictionary) -> void:
	var info: Dictionary = Data.get_object(sprite_name)
	if info.is_empty():
		return
	var path: String = str(info.get("file", ""))
	if not ResourceLoader.exists(path):
		return
	var node := Node2D.new()
	node.name = "obj_" + sprite_name
	node.position = pos
	var size: Array = info.get("size", [32, 32])
	var spr := Sprite2D.new()
	spr.texture = load(path)
	spr.centered = true
	spr.offset = Vector2(0, -float(size[1]) * 0.5)
	spr.flip_h = bool(obj.get("flip", false))
	node.add_child(spr)
	if obj.has("scale"):
		node.scale = Vector2.ONE * float(obj["scale"])
	if obj.has("modulate"):
		spr.modulate = Color(str(obj["modulate"]))
	# soft shadow for bigger props
	if float(size[1]) > 56:
		var shadow := Sprite2D.new()
		shadow.texture = load(path)
		shadow.centered = true
		shadow.offset = spr.offset
		shadow.modulate = Color(0, 0, 0, 0.20)
		shadow.position = Vector2(1, 2)
		node.add_child(shadow)
		node.move_child(shadow, 0)
	# collision
	var col = info.get("collision")
	if col != null and bool(obj.get("collide", true)):
		var body := StaticBody2D.new()
		body.collision_layer = 1
		body.collision_mask = 0
		var shape := CollisionShape2D.new()
		var box := RectangleShape2D.new()
		box.size = Vector2(float(col[2]), float(col[3]))
		shape.shape = box
		shape.position = Vector2(float(col[0]) + float(col[2]) * 0.5 - float(size[0]) * 0.5,
				float(col[1]) + float(col[3]) * 0.5 - float(size[1]))
		body.add_child(shape)
		node.add_child(body)
	# foliage sway
	if bool(info.get("sway", false)):
		var tw := create_tween().set_loops()
		var amount := float(obj.get("sway_amount", 0.012))
		var dur := randf_range(1.8, 3.0)
		tw.tween_property(spr, "rotation", amount, dur).set_trans(Tween.TRANS_SINE)
		tw.tween_property(spr, "rotation", -amount, dur * 2.0).set_trans(Tween.TRANS_SINE)
		tw.tween_property(spr, "rotation", 0.0, dur).set_trans(Tween.TRANS_SINE)
	decor.add_child(node)


func spawn_landmark(lm: Dictionary, pos: Vector2) -> void:
	var area := Area2D.new()
	area.name = "landmark_" + str(lm.get("id", ""))
	area.position = pos
	area.collision_layer = 0
	area.collision_mask = 2
	var shape := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = float(lm.get("radius", 60))
	shape.shape = circle
	area.add_child(shape)
	area.set_script(load("res://scripts/world/landmark.gd"))
	area.lm_id = str(lm.get("id", ""))
	area.lm_name = str(lm.get("name", ""))
	area.lm_description = str(lm.get("description", ""))
	area.lm_entry = str(lm.get("entry", ""))
	entities.add_child(area)
	_entry_points[str(lm.get("id", ""))] = pos


func spawn_interactable(it: Dictionary, pos: Vector2) -> void:
	var area := Area2D.new()
	area.name = "int_" + str(it.get("id", "x"))
	area.position = pos
	area.collision_layer = 0
	area.collision_mask = 2
	var shape := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = float(it.get("radius", 30))
	shape.shape = circle
	area.add_child(shape)
	area.set_script(load("res://scripts/world/interactable.gd"))
	area.data = it
	area.map = self
	entities.add_child(area)
	area.add_to_group("interactable")
	if it.has("sprite"):
		var info: Dictionary = Data.get_object(str(it["sprite"]))
		if not info.is_empty():
			var spr := Sprite2D.new()
			spr.texture = load(str(info["file"]))
			spr.centered = true
			var size: Array = info.get("size", [32, 32])
			spr.offset = Vector2(0, -float(size[1]) * 0.5)
			area.add_child(spr)
			if bool(info.get("sway", false)):
				var tw := create_tween().set_loops()
				tw.tween_property(spr, "rotation", 0.02, 2.4).set_trans(Tween.TRANS_SINE)
				tw.tween_property(spr, "rotation", -0.02, 2.4).set_trans(Tween.TRANS_SINE)


func spawn_npc(npc: Dictionary, pos: Vector2) -> void:
	var scene := load("res://scenes/npc/npc.tscn") as PackedScene
	var node := scene.instantiate()
	node.npc_id = str(npc.get("id", "npc_anak"))
	node.dialogue_id = str(npc.get("dialogue", ""))
	node.wander = bool(npc.get("wander", false))
	node.facing = str(npc.get("facing", "down"))
	node.position = pos
	entities.add_child(node)
	if npc.has("patrol"):
		node.set_patrol(npc["patrol"])
	if npc.has("idle_dialogue"):
		node.idle_dialogue = str(npc["idle_dialogue"])


func spawn_exit(ex: Dictionary, pos: Vector2) -> void:
	var area := Area2D.new()
	area.position = pos
	area.collision_layer = 0
	area.collision_mask = 2
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	var size: Array = ex.get("size", [1, 1])
	rect.size = Vector2(float(size[0]) * TILE, float(size[1]) * TILE)
	shape.shape = rect
	area.add_child(shape)
	area.set_script(load("res://scripts/world/map_exit.gd"))
	area.exit_data = ex
	area.map = self
	entities.add_child(area)
	_entry_points["exit_" + str(ex.get("id", ""))] = pos


func entry_position(entry_id: String) -> Vector2:
	return entry_point(entry_id)
