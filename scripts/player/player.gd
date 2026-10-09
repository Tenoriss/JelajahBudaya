extends CharacterBody2D
## The player character: 8-way movement, animated sprite sharing, interaction
## detection, footstep audio and a smooth follow camera.

const SPEED := 132.0
const SPRINT_SPEED := 196.0
const ACCEL := 1100.0
const FRICTION := 1400.0

var facing := "down"
var moving := false
var locked := false                 # set while dialogue / puzzle / menu is open
var spawn_position := Vector2.ZERO
var sprite: AnimatedSprite2D
var anim_frames: SpriteFrames
var interact_zone: Area2D
var camera: Camera2D
var _anim_time := 0.0
var _step_timer := 0.0
var _current_target: Node = null
var _bob := 0.0


func _ready() -> void:
	name = "Player"
	collision_layer = 2
	collision_mask = 1
	var shape := CollisionShape2D.new()
	var capsule := CapsuleShape2D.new()
	capsule.radius = 7.0
	capsule.height = 16.0
	shape.shape = capsule
	shape.position = Vector2(0, 8)
	add_child(shape)

	sprite = AnimatedSprite2D.new()
	sprite.name = "Sprite"
	sprite.sprite_frames = _build_frames()
	sprite.animation = "idle_down"
	sprite.centered = true
	sprite.offset = Vector2(0, -8)      # feet at the node origin
	sprite.play()
	add_child(sprite)

	interact_zone = Area2D.new()
	interact_zone.name = "InteractZone"
	interact_zone.collision_layer = 0
	interact_zone.collision_mask = 4      # sees interactables + NPC talk zones
	var iz := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = 34.0
	iz.shape = circle
	iz.position = Vector2(0, 8)
	interact_zone.add_child(iz)
	add_child(interact_zone)

	camera = Camera2D.new()
	camera.name = "Camera2D"
	camera.position = Vector2(0, -8)
	camera.zoom = Vector2(2.0, 2.0)
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 6.0
	camera.drag_horizontal_enabled = true
	camera.drag_vertical_enabled = true
	camera.drag_left_margin = 0.14
	camera.drag_right_margin = 0.14
	camera.drag_top_margin = 0.14
	camera.drag_bottom_margin = 0.14
	add_child(camera)
	camera.make_current()

	Quest.refresh_availability()


func _build_frames() -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	var sheet_info: Dictionary = Data.get_character("player")
	var tex_path: String = str(sheet_info.get("sheet", "res://assets/characters/player.png"))
	var tex: Texture2D = load(tex_path) if ResourceLoader.exists(tex_path) else null
	if tex == null:
		var img := Image.create(32, 48, false, Image.FORMAT_RGBA8)
		img.fill(Color(0.3, 0.7, 0.8))
		tex = ImageTexture.create_from_image(img)
	var fw := int(sheet_info.get("frame_w", 32))
	var fh := int(sheet_info.get("frame_h", 48))
	var idle: Array = sheet_info.get("idle_frames", [0, 1])
	var walk: Array = sheet_info.get("walk_frames", [2, 3, 4, 5])
	var dirs: Array = sheet_info.get("directions", ["down", "left", "right", "up"])
	for row in range(dirs.size()):
		var dir := str(dirs[row])
		var idle_name := "idle_" + dir
		var walk_name := "walk_" + dir
		frames.add_animation(idle_name)
		frames.set_animation_speed(idle_name, 3.0)
		frames.set_animation_loop(idle_name, true)
		for i in idle:
			frames.add_frame(idle_name, _atlas(tex, fw, fh, int(i), row))
		frames.add_animation(walk_name)
		frames.set_animation_speed(walk_name, 9.0)
		frames.set_animation_loop(walk_name, true)
		for i in walk:
			frames.add_frame(walk_name, _atlas(tex, fw, fh, int(i), row))
	return frames


func _atlas(tex: Texture2D, fw: int, fh: int, col: int, row: int) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = tex
	at.region = Rect2(col * fw, row * fh, fw, fh)
	return at


func _physics_process(delta: float) -> void:
	if locked or not Game.started:
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		move_and_slide()
		_update_animation(Vector2.ZERO)
		return
	var input := Vector2(
		Input.get_axis("move_left", "move_right"),
		Input.get_axis("move_up", "move_down"))
	input = input.limit_length(1.0)
	var speed := SPRINT_SPEED if Input.is_action_pressed("sprint") else SPEED
	if input.length() > 0.01:
		velocity = velocity.move_toward(input * speed, ACCEL * delta)
		facing = _dir_from_vector(input)
	else:
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
	move_and_slide()
	_update_animation(input)
	_update_footsteps(delta, input)
	Game.map_player_pos[World.current_map_id] = [position.x, position.y]
	_check_interactables()


func _dir_from_vector(v: Vector2) -> String:
	# eight-way facing: the sheet has a dedicated row for each diagonal
	if v.length() < 0.01:
		return facing
	var ang := atan2(v.y, v.x)          # -PI..PI, 0 = right, +PI/2 = down
	if ang >= -PI / 8.0 and ang < PI / 8.0:
		return "right"
	if ang >= PI / 8.0 and ang < 3.0 * PI / 8.0:
		return "down_right"
	if ang >= 3.0 * PI / 8.0 and ang < 5.0 * PI / 8.0:
		return "down"
	if ang >= 5.0 * PI / 8.0 and ang < 7.0 * PI / 8.0:
		return "down_left"
	if ang >= -3.0 * PI / 8.0 and ang < -PI / 8.0:
		return "up_right"
	if ang >= -5.0 * PI / 8.0 and ang < -3.0 * PI / 8.0:
		return "up"
	if ang >= -7.0 * PI / 8.0 and ang < -5.0 * PI / 8.0:
		return "up_left"
	return "left"


func _update_animation(input: Vector2) -> void:
	var speed_now := velocity.length()
	moving = speed_now > 8.0
	if not moving:
		_facing_idle()
	else:
		var dir := facing
		if input.length() > 0.01:
			dir = _dir_from_vector(input)
			facing = dir
		var anim := "walk_" + dir
		if sprite.animation != anim:
			sprite.play(anim)
		sprite.speed_scale = clampf(speed_now / SPEED, 0.7, 1.5)


func _facing_idle() -> void:
	# play the idle animation for whichever of the eight facings is current
	var anim := "idle_" + facing
	if sprite.animation != anim:
		sprite.play(anim)
	sprite.speed_scale = 1.0


func _update_footsteps(delta: float, input: Vector2) -> void:
	if input.length() < 0.1:
		_step_timer = 0.0
		return
	_step_timer -= delta
	if _step_timer <= 0.0:
		_step_timer = 0.30 if not Input.is_action_pressed("sprint") else 0.22
		Audio.footstep(_surface_under_player())
		Game.bump("steps_taken")


func _surface_under_player() -> String:
	var map_node := get_parent()
	if map_node == null or not "ground" in map_node or map_node.ground == null:
		return "grass"
	var cell: Vector2i = map_node.ground.local_to_map(map_node.ground.to_local(global_position + Vector2(0, 10)))
	var src := map_node.ground.get_cell_source_id(cell)
	if src < 0:
		return "grass"
	var atlas: Vector2i = map_node.ground.get_cell_atlas_coords(cell)
	var region: String = str(map_node.region)
	var tiles: Dictionary = Data.tilesets.get(region, {}).get("tiles", {})
	for tile_name in tiles.keys():
		var at: Array = tiles[tile_name]["atlas"]
		if int(at[0]) == atlas.x and int(at[1]) == atlas.y:
			var n := str(tile_name)
			if n.begins_with("water") or n.begins_with("deep"):
				return "water"
			if n.begins_with("grass") or n.begins_with("tall"):
				return "grass"
			if n.begins_with("sand"):
				return "sand"
			if n.begins_with("plank") or n.begins_with("stone") or n.begins_with("temple") or n.begins_with("paving"):
				return "stone"
			return "dirt"
	return "grass"


# ---------------------------------------------------------------- interaction
func _check_interactables() -> void:
	var best: Node = null
	var best_dist := 1e9
	for area in interact_zone.get_overlapping_areas():
		if not area.is_in_group("interactable"):
			continue
		if area.has_method("can_interact") and not area.can_interact():
			continue
		var d := global_position.distance_to(area.global_position)
		if d < best_dist:
			best_dist = d
			best = area
	if best != _current_target:
		_current_target = best
		UI.set_interaction_target(best)


func current_target() -> Node:
	return _current_target


func interact() -> void:
	if _current_target == null or not is_instance_valid(_current_target):
		return
	if _current_target.has_method("interact"):
		_current_target.interact(self)


func lock_input(value: bool) -> void:
	locked = value
	if value:
		velocity = Vector2.ZERO
	UI.set_interaction_target(null if value else _current_target)


func teleport(pos: Vector2) -> void:
	global_position = pos
	velocity = Vector2.ZERO
	if camera:
		camera.reset_smoothing()


func face_and_walk(dir: String) -> void:
	facing = dir
	_facing_idle()


func shake(amount := 3.0) -> void:
	if not Settings.screenshake or camera == null:
		return
	var tw := create_tween()
	tw.tween_property(camera, "offset", Vector2(randf_range(-amount, amount), randf_range(-amount, amount)), 0.05)
	tw.tween_property(camera, "offset", Vector2.ZERO, 0.12)
