extends Control
## Settings: audio, text speed, display, controls reference.

var music_slider: HSlider
var sfx_slider: HSlider
var text_slider: HSlider
var fullscreen_check: CheckBox
var minimap_check: CheckBox
var shake_check: CheckBox
var res_option: OptionButton


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.06, 0.88)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var title := UITheme.heading("Settings", 30)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 16)
	add_child(title)

	var panel := UITheme.make_panel(UITheme.PANEL_DARK)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(-360, -300)
	panel.custom_minimum_size = Vector2(720, 600)
	add_child(panel)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 10)
	panel.add_child(col)

	col.add_child(_slider_row("Music volume", 0.0, 1.0, Settings.music_volume,
			func(v): Settings.music_volume = v; Audio.apply_volumes()))
	music_slider = col.get_child(col.get_child_count() - 1).get_meta("slider")
	col.add_child(_slider_row("Sound volume", 0.0, 1.0, Settings.sfx_volume,
			func(v): Settings.sfx_volume = v; Audio.apply_volumes(); Audio.ui_hover()))
	sfx_slider = col.get_child(col.get_child_count() - 1).get_meta("slider")
	col.add_child(_slider_row("Text speed (chars/sec, 0 = instant)", 0.0, 160.0, Settings.text_speed,
			func(v): Settings.text_speed = v))
	text_slider = col.get_child(col.get_child_count() - 1).get_meta("slider")

	var fs := CheckBox.new()
	fs.text = "Fullscreen"
	UITheme.apply_button(fs, 17)
	fs.button_pressed = Settings.fullscreen
	fs.toggled.connect(func(v): Settings.fullscreen = v; Settings.apply(); Settings.save_settings())
	col.add_child(fs)
	fullscreen_check = fs

	var mini := CheckBox.new()
	mini.text = "Show mini-map"
	UITheme.apply_button(mini, 17)
	mini.button_pressed = Settings.minimap_enabled
	mini.toggled.connect(func(v): Settings.minimap_enabled = v; Settings.save_settings())
	col.add_child(mini)
	minimap_check = mini

	var shake := CheckBox.new()
	shake.text = "Screen shake"
	UITheme.apply_button(shake, 17)
	shake.button_pressed = Settings.screenshake
	shake.toggled.connect(func(v): Settings.screenshake = v; Settings.save_settings())
	col.add_child(shake)
	shake_check = shake

	var res_row := HBoxContainer.new()
	res_row.add_theme_constant_override("separation", 8)
	col.add_child(res_row)
	var rl := Label.new()
	UITheme.apply_label(rl, 17, UITheme.COL_TEXT)
	rl.text = "Resolution"
	res_row.add_child(rl)
	res_option = OptionButton.new()
	UITheme.apply_button(res_option, 16)
	var sizes := [Vector2i(1280, 720), Vector2i(1366, 768), Vector2i(1600, 900), Vector2i(1920, 1080)]
	for i in range(sizes.size()):
		res_option.add_item("%dx%d" % [sizes[i].x, sizes[i].y], i)
		if sizes[i] == Settings.resolution:
			res_option.select(i)
	res_option.item_selected.connect(func(i):
		Settings.resolution = sizes[i]
		Settings.apply()
		Settings.save_settings())
	res_row.add_child(res_option)

	col.add_child(UITheme.hline())
	var controls := Label.new()
	UITheme.apply_label(controls, 15, UITheme.COL_DIM)
	controls.text = "WASD / Arrow keys  move\nE  interact / advance dialogue\nM  world map      I  satchel      J  journal\nH  hint during a puzzle      ESC  pause\nShift  run"
	controls.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	controls.custom_minimum_size = Vector2(660, 0)
	col.add_child(controls)

	var close := Button.new()
	close.text = "Back"
	UITheme.apply_button(close, 19)
	close.pressed.connect(func():
		Settings.save_settings()
		UI.close("settings"))
	col.add_child(close)


func _slider_row(label_text: String, minv: float, maxv: float, value: float, cb: Callable) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 8)
	var lbl := Label.new()
	UITheme.apply_label(lbl, 17, UITheme.COL_TEXT)
	lbl.text = label_text
	lbl.custom_minimum_size = Vector2(330, 0)
	row.add_child(lbl)
	var slider := HSlider.new()
	slider.min_value = minv
	slider.max_value = maxv
	slider.step = 0.01 if maxv <= 1.0 else 1.0
	slider.value = value
	slider.custom_minimum_size = Vector2(270, 24)
	slider.value_changed.connect(cb)
	row.add_child(slider)
	row.set_meta("slider", slider)
	return row


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		Settings.save_settings()
		UI.close("settings")
		get_viewport().set_input_as_handled()
