extends Control
## Title screen with an animated archipelago backdrop (drawn in code).

var _t := 0.0
var _clouds: Array = []


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_build()
	Audio.play_music("prologue")


func _build() -> void:
	var bg := Control.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bg.draw.connect(_draw_backdrop.bind(bg))
	add_child(bg)

	for i in range(6):
		var cloud := Control.new()
		cloud.custom_minimum_size = Vector2(180, 70)
		cloud.mouse_filter = Control.MOUSE_FILTER_IGNORE
		cloud.draw.connect(_draw_cloud.bind(cloud))
		cloud.position = Vector2(randf() * 1280, randf_range(50, 300))
		add_child(cloud)
		_clouds.append({"node": cloud, "speed": randf_range(6.0, 18.0)})

	var title := Label.new()
	title.text = "NUSANTARA"
	title.add_theme_font_size_override("font_size", 74)
	title.add_theme_color_override("font_color", Color(0.99, 0.92, 0.72))
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.75))
	title.add_theme_constant_override("shadow_offset_x", 3)
	title.add_theme_constant_override("shadow_offset_y", 4)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 88)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var sub := Label.new()
	sub.text = "JEJAK BUDAYA   ·   a journey through the cultures of Indonesia"
	sub.add_theme_font_size_override("font_size", 21)
	sub.add_theme_color_override("font_color", Color(0.93, 0.82, 0.58))
	sub.set_anchors_preset(Control.PRESET_TOP_WIDE)
	sub.position = Vector2(0, 178)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(sub)

	var menu := VBoxContainer.new()
	menu.set_anchors_preset(Control.PRESET_CENTER)
	menu.position = Vector2(-140, 30)
	menu.custom_minimum_size = Vector2(280, 0)
	menu.add_theme_constant_override("separation", 7)
	add_child(menu)

	var entries := [
		["New Journey", Callable(self, "_new_game"), true],
		["Continue", Callable(self, "_continue"), Save.has_save(Save.AUTOSAVE_SLOT) or _has_any_save()],
		["Load Game", Callable(self, "_load_game"), _has_any_save()],
		["Culture Journal", Callable(self, "_open_journal"), true],
		["Achievements", Callable(self, "_open_achievements"), true],
		["Settings", Callable(self, "_open_settings"), true],
		["Quit", Callable(self, "_quit"), true],
	]
	for entry in entries:
		var btn := Button.new()
		btn.text = str(entry[0])
		UITheme.apply_button(btn, 22)
		btn.custom_minimum_size = Vector2(280, 0)
		btn.disabled = not bool(entry[2])
		btn.pressed.connect(entry[1])
		menu.add_child(btn)

	var hint := Label.new()
	UITheme.apply_label(hint, 14, Color(0.82, 0.8, 0.72))
	hint.text = "Original artwork, music and story created for this project · Cultural entries flagged “verify” still need source checking"
	hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	hint.position = Vector2(0, -52)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(hint)


func _draw_backdrop(host: Control) -> void:
	var s := host.size
	var water_y := s.y * 0.60
	host.draw_rect(Rect2(0, 0, s.x, water_y), Color(0.11, 0.16, 0.27), true)
	host.draw_circle(Vector2(s.x * 0.78, s.y * 0.24), 68.0, Color(0.95, 0.76, 0.44, 0.9))
	host.draw_circle(Vector2(s.x * 0.78, s.y * 0.24), 50.0, Color(1.0, 0.9, 0.66, 0.9))
	host.draw_rect(Rect2(0, water_y, s.x, s.y - water_y), Color(0.12, 0.25, 0.33), true)
	for i in range(-2, int(s.x / 28.0) + 2):
		var x := i * 28.0 + fmod(_t * 12.0, 28.0)
		host.draw_line(Vector2(x, water_y + 14), Vector2(x + 16, water_y + 20),
				Color(0.75, 0.88, 0.92, 0.10), 2.0)
		host.draw_line(Vector2(x + 8, water_y + 52), Vector2(x + 24, water_y + 58),
				Color(0.75, 0.88, 0.92, 0.07), 2.0)
	var islands := [
		[0.15, 1.0], [0.37, 0.78], [0.55, 1.15], [0.72, 0.72], [0.88, 0.9],
	]
	for isl in islands:
		var cx: float = float(isl[0]) * s.x
		var sc: float = float(isl[1])
		var y := water_y + 18
		var pts := PackedVector2Array([
			Vector2(cx - 120 * sc, y), Vector2(cx - 74 * sc, y - 36 * sc),
			Vector2(cx - 18 * sc, y - 56 * sc), Vector2(cx + 34 * sc, y - 44 * sc),
			Vector2(cx + 96 * sc, y - 20 * sc), Vector2(cx + 120 * sc, y)])
		host.draw_colored_polygon(pts, Color(0.15, 0.29, 0.2))
		host.draw_line(Vector2(cx - 8 * sc, y - 40 * sc), Vector2(cx - 22 * sc, y - 78 * sc),
				Color(0.14, 0.21, 0.15), 5.0)
		host.draw_circle(Vector2(cx - 24 * sc, y - 82 * sc), 15 * sc, Color(0.16, 0.3, 0.2))
		host.draw_circle(Vector2(cx + 2 * sc, y - 76 * sc), 12 * sc, Color(0.14, 0.27, 0.18))


func _draw_cloud(host: Control) -> void:
	host.draw_circle(Vector2(46, 36), 26, Color(1, 1, 1, 0.09))
	host.draw_circle(Vector2(90, 30), 32, Color(1, 1, 1, 0.08))
	host.draw_circle(Vector2(132, 38), 22, Color(1, 1, 1, 0.07))


func _process(delta: float) -> void:
	_t += delta
	for c in _clouds:
		var node: Control = c["node"]
		node.position.x += float(c["speed"]) * delta
		if node.position.x > 1400:
			node.position.x = -240
			node.position.y = randf_range(50, 300)


func _has_any_save() -> bool:
	for slot in range(1, Save.SLOT_COUNT + 1):
		if Save.has_save(slot):
			return true
	return false


func _new_game() -> void:
	Game.new_game()
	_start_game()


func _continue() -> void:
	if Save.load_slot(Save.AUTOSAVE_SLOT):
		_start_game()


func _load_game() -> void:
	UI.open("savemenu")


func _open_journal() -> void:
	UI.open("journal")


func _open_achievements() -> void:
	UI.open("achievements")


func _open_settings() -> void:
	UI.open("settings")


func _quit() -> void:
	get_tree().quit()


func _start_game() -> void:
	Audio.ui_confirm()
	UI.close_all()
	await World.fade_out(0.45)
	get_tree().change_scene_to_file("res://scenes/main/game.tscn")
