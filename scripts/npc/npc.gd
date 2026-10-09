extends CharacterBody2D
## An NPC: animated sprite built from data/characters.json, optional wandering,
## an interaction prompt and dialogue dispatch (quest offer / turn-in / idle).

const SPEED := 42.0
const WANDER_RADIUS := 46.0

var npc_id := "npc_anak"
var dialogue_id := ""
var idle_dialogue := ""
var wander := false
var facing := "down"
var patrol: Array = []

var sprite: AnimatedSprite2D
var interact_zone: Area2D
var home := Vector2.ZERO
var _target := Vector2.ZERO
var _wait := 0.0
var _patrol_index := 0
var _facing_locked := false


func _ready() -> void:
	var def := Data.get_npc(npc_id)
	if def.has("name") and def.get("name", "") != "":
		name = "NPC_" + str(def.get("name", npc_id)).replace(" ", "_")
	else:
		name = "NPC_" + npc_id
	home = position
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
	sprite.sprite_frames = _build_frames()
	sprite.centered = true
	sprite.offset = Vector2(0, -8)
	sprite.play("idle_" + facing)
	add_child(sprite)

	interact_zone = Area2D.new()
	interact_zone.collision_layer = 4     # player's interact zone finds this
	interact_zone.collision_mask = 0
	interact_zone.monitoring = false
	interact_zone.monitorable = true
	var iz := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = float(def.get("talk_radius", 30))
	iz.shape = circle
	iz.position = Vector2(0, 6)
	interact_zone.add_child(iz)
	add_child(interact_zone)

	add_to_group("interactable")
	add_to_group("npc")
	collision_layer = 2
	_target = home
	if def.has("wander"):
		wander = bool(def["wander"])
	if def.has("facing"):
		facing = str(def["facing"])
	if def.has("dialogue") and dialogue_id == "":
		dialogue_id = str(def["dialogue"])


func set_patrol(points: Array) -> void:
	patrol = points
	if patrol.size() > 0:
		wander = false
		_target = _patrol_point(0)


func _patrol_point(i: int) -> Vector2:
	var p: Array = patrol[i % patrol.size()]
	return Vector2(float(p[0]) * 32.0 + 16.0, float(p[1]) * 32.0 + 16.0)


func _build_frames() -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	var def := Data.get_npc(npc_id)
	var char_id := str(def.get("character", npc_id))
	var info: Dictionary = Data.get_character(char_id)
	if info.is_empty():
		info = Data.get_character("npc_anak")
	var path: String = str(info.get("sheet", "res://assets/npcs/anak.png"))
	var tex: Texture2D = load(path) if ResourceLoader.exists(path) else null
	if tex == null:
		var img := Image.create(32, 48, false, Image.FORMAT_RGBA8)
		img.fill(Color(0.6, 0.5, 0.7))
		tex = ImageTexture.create_from_image(img)
	var fw := int(info.get("frame_w", 32))
	var fh := int(info.get("frame_h", 48))
	var idle: Array = info.get("idle_frames", [0, 1])
	var walk: Array = info.get("walk_frames", [2, 3, 4, 5])
	for row in range(4):
		var dir := ["down", "left", "right", "up"][row]
		frames.add_animation("idle_" + dir)
		frames.set_animation_speed("idle_" + dir, 2.6)
		for i in idle:
			frames.add_frame("idle_" + dir, _atlas(tex, fw, fh, int(i), row))
		frames.add_animation("walk_" + dir)
		frames.set_animation_speed("walk_" + dir, 7.0)
		for i in walk:
			frames.add_frame("walk_" + dir, _atlas(tex, fw, fh, int(i), row))
	return frames


func _atlas(tex: Texture2D, fw: int, fh: int, col: int, row: int) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = tex
	at.region = Rect2(col * fw, row * fh, fw, fh)
	return at


func _physics_process(delta: float) -> void:
	if not Game.started or UI.is_blocking():
		velocity = Vector2.ZERO
		move_and_slide()
		return
	if _wait > 0.0:
		_wait -= delta
		velocity = velocity.move_toward(Vector2.ZERO, 400.0 * delta)
		move_and_slide()
		_play_idle()
		return
	if bool(Data.get_npc(npc_id).get("schedule_night", false)) and World.time_of_day() == World.TimeOfDay.NIGHT:
		# walk home / stand still at night
		if position.distance_to(home) < 6.0:
			velocity = Vector2.ZERO
			move_and_slide()
			_play_idle()
			return
		_target = home
	if not wander and patrol.is_empty():
		velocity = Vector2.ZERO
		move_and_slide()
		_play_idle()
		return
	var to := _target - position
	if to.length() < 6.0:
		_wait = randf_range(1.2, 3.4)
		_pick_next_target()
		return
	var dir := to.normalized()
	velocity = dir * SPEED
	move_and_slide()
	facing = _dir_from_vector(dir)
	_play_walk()


func _pick_next_target() -> void:
	if patrol.size() > 0:
		_patrol_index = (_patrol_index + 1) % patrol.size()
		_target = _patrol_point(_patrol_index)
		return
	var angle := randf() * TAU
	var dist := randf_range(18.0, WANDER_RADIUS)
	_target = home + Vector2(cos(angle), sin(angle) * 0.7) * dist


func _dir_from_vector(v: Vector2) -> String:
	if absf(v.x) > absf(v.y):
		return "right" if v.x > 0 else "left"
	return "down" if v.y > 0 else "up"


func _play_idle() -> void:
	var anim := "idle_" + facing
	if sprite.animation != anim:
		sprite.play(anim)


func _play_walk() -> void:
	var anim := "walk_" + facing
	if sprite.animation != anim:
		sprite.play(anim)


# ---------------------------------------------------------------- interaction
func display_name() -> String:
	return "Talk to " + str(Data.get_npc(npc_id).get("name", "villager"))


func can_interact() -> bool:
	return true


func interact(player: Node) -> void:
	if Dialogue.active or UI.is_blocking():
		return
	# face the player
	if player:
		var d := player.global_position - global_position
		facing = _dir_from_vector(d)
		_facing_locked = true
		_play_idle()
	var resolved := _resolve_dialogue()
	if resolved == "":
		Audio.ui_error()
		Notify.toast(str(Data.get_npc(npc_id).get("name", "They")) + " has nothing to say right now.")
		return
	Game.note_npc_talked(npc_id)
	Quest.notify_event("talk", npc_id)
	Dialogue.finished.connect(_on_dialogue_finished, CONNECT_ONE_SHOT)
	Dialogue.start(resolved, {"npc": npc_id, "npc_name": Data.get_npc(npc_id).get("name", ""),
			"portrait": _portrait_path()})


func _portrait_path() -> String:
	var def := Data.get_npc(npc_id)
	var char_id := str(def.get("character", npc_id))
	var info: Dictionary = Data.get_character(char_id)
	return str(info.get("portrait", ""))


## Dialogue priority: turn in a finished quest -> offer a new quest -> idle chat.
func _resolve_dialogue() -> String:
	var waiting := Quest.active_quests_of(npc_id)
	if waiting.size() > 0:
		var qid := str(waiting[0])
		var def := Data.get_quest(qid)
		var complete: Dictionary = def.get("complete", {})
		if str(complete.get("type", "")) == "talk" and Game.has_flag("_ready_" + qid):
			Game.set_flag("_ready_" + qid, false)
			Quest.complete_quest(qid)
			return str(def.get("turn_in_dialogue", def.get("dialogue_after", dialogue_id)))
	var offered := Quest.quests_offered_by(npc_id)
	if offered.size() > 0:
		var qid2 := str(offered[0])
		var qdef := Data.get_quest(qid2)
		var offer_dialogue := str(qdef.get("offer_dialogue", ""))
		if offer_dialogue != "":
			return offer_dialogue
		Quest.start_quest(qid2)
	var npc_def := Data.get_npc(npc_id)
	# context dialogues: a "conditional" list lets an NPC mention quest progress
	for entry in npc_def.get("conditional_dialogue", []):
		if _dialogue_condition(entry.get("if", {})):
			return str(entry.get("dialogue", ""))
	if Dialogue.is_dialogue_available(npc_id).get("type", "") == "turn_in":
		return str(npc_def.get("turn_in_dialogue", dialogue_id))
	if idle_dialogue != "":
		return idle_dialogue
	if dialogue_id != "":
		return dialogue_id
	return str(npc_def.get("idle_dialogue", ""))


func _dialogue_condition(cond: Dictionary) -> bool:
	for key in cond.keys():
		match key:
			"flag":
				if not Game.has_flag(str(cond[key])):
					return false
			"no_flag":
				if Game.has_flag(str(cond[key])):
					return false
			"quest_active":
				if not Quest.is_active(str(cond[key])):
					return false
			"quest_done":
				if not Quest.is_completed(str(cond[key])):
					return false
			"region":
				if Game.current_region != str(cond[key]):
					return false
			_:
				pass
	return true


func _on_dialogue_finished(_id: String) -> void:
	_facing_locked = false
	Quest.refresh_availability()
