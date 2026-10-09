extends Node2D
## Root game scene: holds the world holder and boots a new journey or save.
## Also owns the light of day (a CanvasModulate tint) and a light weather layer.

@onready var world_holder: Node2D = $WorldHolder

var _boot_done := false
var _tint: CanvasModulate
var _weather: Node2D
var _weather_kind := ""

# --- opening tutorial ---------------------------------------------------
# A few short, skippable nudges shown in the corner of the screen.  They only
# teach the controls; nothing here blocks play and nothing is required for the
# story.  Everything is driven by the same inputs the game already uses.
const TUTORIAL_STEPS: Array = [
	"Move around: W A S D or the arrow keys  (hold Shift to hurry)",
	"Talk to people: walk close and press E",
	"Your notebook: press J to read the Culture Journal",
	"Travel: press M for the World Map, then pick a region",
]
var _tutorial := true
var _tutorial_step := 0
var _tutorial_moved := 0.0
var _tutorial_dialogues := 0
var _tutorial_label: Label
var _tutorial_panel: PanelContainer

const DAY_TINTS := {
	"Morning": Color(1.0, 0.97, 0.90),
	"Day": Color(1.0, 1.0, 1.0),
	"Evening": Color(0.99, 0.86, 0.72),
	"Night": Color(0.62, 0.66, 0.86),
}


func _ready() -> void:
	randomize()
	_tint = CanvasModulate.new()
	_tint.name = "DaylightTint"
	_tint.color = DAY_TINTS["Morning"]
	add_child(_tint)
	_weather = Node2D.new()
	_weather.name = "Weather"
	_weather.z_index = 40
	add_child(_weather)
	World.map_loaded.connect(_on_map_loaded)
	Dialogue.started.connect(_on_dialogue_started)
	_build_tutorial()
	print("[JelajahBudaya] data: %d regions, %d maps, %d quests, %d cultures, %d items, %d puzzles" % [
		Data.region_order.size(), Data.maps.size(), Data.quests.size(),
		Data.cultures.size(), Data.items.size(), Data.puzzles.size()])
	if Data.errors.size() > 0:
		print("[JelajahBudaya] data warnings: ", Data.errors)
	if not Game.started:
		Game.new_game()
	_boot_done = true
	call_deferred("_boot")


func _boot() -> void:
	await World.fade_out(0.01)
	World.load_map(Game.current_map if Game.current_map != "" else "desa_awal")
	await get_tree().process_frame
	await World.fade_in(0.6)
	Game.mark_started(true)
	if Game.story_chapter == 1 and not Game.has_flag("opening_done"):
		Game.set_flag("opening_done", true)
		await get_tree().create_timer(0.5).timeout
		Dialogue.start("intro_arrival", {})


func _process(_delta: float) -> void:
	if _tint != null:
		var want: Color = DAY_TINTS.get(World.time_name(), DAY_TINTS["Day"])
		_tint.color = _tint.color.lerp(want, 0.06)
	_process_tutorial(_delta)


# ---------------------------------------------------------------- tutorial
func _build_tutorial() -> void:
	if Game.has_flag("tutorial_done"):
		_tutorial = false
		return
	var layer := CanvasLayer.new()
	layer.name = "TutorialLayer"
	layer.layer = 5
	add_child(layer)
	var box := VBoxContainer.new()
	box.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	box.offset_left = 16
	box.offset_right = -16
	box.offset_top = 14
	box.alignment = BoxContainer.ALIGNMENT_CENTER
	layer.add_child(box)
	_tutorial_panel = PanelContainer.new()
	_tutorial_panel.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_DIALOGUE, 8))
	box.add_child(_tutorial_panel)
	_tutorial_label = Label.new()
	_tutorial_label.add_theme_font_size_override("font_size", 17)
	UITheme.apply_label(_tutorial_label, 17, UITheme.COL_PANEL_TEXT)
	_tutorial_panel.add_child(_tutorial_label)
	_update_tutorial_text()


func _update_tutorial_text() -> void:
	if _tutorial_label == null:
		return
	if _tutorial_step >= TUTORIAL_STEPS.size():
		_tutorial_label.text = ""
		_tutorial_panel.visible = false
		return
	_tutorial_label.text = "%s   [%d/%d]" % [str(TUTORIAL_STEPS[_tutorial_step]),
		_tutorial_step + 1, TUTORIAL_STEPS.size()]


func _process_tutorial(delta: float) -> void:
	if not _tutorial:
		return
	if World.player != null:
		var vel: Variant = World.player.get("velocity")
		if vel is Vector2:
			_tutorial_moved += (vel as Vector2).length() * delta
	match _tutorial_step:
		0:
			if _tutorial_moved > 90.0:
				_advance_tutorial()
		1:
			if _tutorial_dialogues >= 1:
				_advance_tutorial()
		2:
			if UI.open_screens.has("journal") or Game.has_flag("journal_seen"):
				Game.set_flag("journal_seen", true)
				_advance_tutorial()
		3:
			if UI.open_screens.has("worldmap"):
				_advance_tutorial()


func _advance_tutorial() -> void:
	_tutorial_step += 1
	if _tutorial_step >= TUTORIAL_STEPS.size():
		_tutorial = false
		Game.set_flag("tutorial_done", true)
		Notify.toast("Tutorial complete - explore, talk and travel freely!")
	_update_tutorial_text()


func _on_dialogue_started(_id: String) -> void:
	_tutorial_dialogues += 1


## Rain in the wet regions, mist in the mountains - a light, low cost weather layer.
func _on_map_loaded(map_id: String) -> void:
	var region := str(Data.get_map(map_id).get("region", ""))
	var kind := World.weather_particles_for(region)
	if kind == _weather_kind:
		return
	_weather_kind = kind
	for child in _weather.get_children():
		child.queue_free()
	if kind == "none":
		return
	var particles := GPUParticles2D.new()
	particles.amount = 90 if kind == "rain_light" else 40
	particles.lifetime = 1.6
	particles.position = Vector2(640, -40)
	particles.local_coords = false
	particles.preprocess = 1.0
	var mat := ParticleProcessMaterial.new()
	mat.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	mat.emission_box_extents = Vector3(760, 4, 1)
	if kind == "rain_light":
		mat.direction = Vector3(0.25, 1, 0)
		mat.spread = 4.0
		mat.initial_velocity_min = 320.0
		mat.initial_velocity_max = 420.0
		mat.color = Color(0.72, 0.82, 0.95, 0.55)
		particles.amount = 120
	else:
		mat.direction = Vector3(1, 0, 0)
		mat.spread = 20.0
		mat.initial_velocity_min = 8.0
		mat.initial_velocity_max = 20.0
		mat.color = Color(0.92, 0.95, 1.0, 0.22)
	particles.process_material = mat
	particles.texture = _weather_texture(kind)
	_weather.add_child(particles)


func _weather_texture(kind: String) -> Texture2D:
	var img := Image.create(4 if kind == "rain_light" else 24, 14, false, Image.FORMAT_RGBA8)
	if kind == "rain_light":
		for y in range(14):
			img.set_pixel(1, y, Color(1, 1, 1, 0.85))
			img.set_pixel(2, y, Color(1, 1, 1, 0.55))
	else:
		for y in range(14):
			for x in range(24):
				var d := absf(float(y) - 6.5) / 7.0
				if x + y % 3 < 24 - int(d * 8.0):
					img.set_pixel(x, y, Color(1, 1, 1, 0.35 * (1.0 - d)))
	return ImageTexture.create_from_image(img)


func _unhandled_input(event: InputEvent) -> void:
	if not _boot_done:
		return
	if Dialogue.active or UI.is_blocking() or UI.puzzle_host_active():
		return
	var handled := true
	if event.is_action_pressed("open_map"):
		UI.open("worldmap")
	elif event.is_action_pressed("open_inventory"):
		UI.open("inventory")
	elif event.is_action_pressed("open_journal"):
		UI.open("journal")
	elif event.is_action_pressed("pause"):
		UI.open("pause")
	elif event.is_action_pressed("hint"):
		if Puzzle.current_id != "" and Puzzle._instance != null and Puzzle._instance.has_method("use_hint"):
			Puzzle._instance.use_hint()
		else:
			UI.open("quests")
	else:
		handled = false
	if handled:
		get_viewport().set_input_as_handled()
