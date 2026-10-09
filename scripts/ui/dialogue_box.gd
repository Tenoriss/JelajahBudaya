extends Control
## Dialogue box: portrait, speaker name, typewriter text and choice buttons.

var portrait_rect: TextureRect
var name_label: Label
var text_label: Label
var continue_icon: Label
var choice_box: VBoxContainer
var panel: PanelContainer

var _lines: Array = []
var _line_index := 0
var _visible_chars := 0.0
var _typing := false
var _context: Dictionary = {}
var _pending_choices: Array = []


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	visible = false

	var dim := ColorRect.new()
	dim.color = Color(0.05, 0.04, 0.06, 0.25)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(dim)

	panel = UITheme.make_panel(UITheme.PANEL_DIALOGUE)
	panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	panel.position = Vector2(24, -206)
	panel.custom_minimum_size = Vector2(1232, 190)
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(panel)

	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 14)
	panel.add_child(row)

	var portrait_frame := PanelContainer.new()
	portrait_frame.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT, 6))
	portrait_frame.custom_minimum_size = Vector2(112, 112)
	row.add_child(portrait_frame)
	portrait_rect = TextureRect.new()
	portrait_rect.custom_minimum_size = Vector2(96, 96)
	portrait_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	portrait_frame.add_child(portrait_rect)

	var col := VBoxContainer.new()
	col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	col.add_theme_constant_override("separation", 4)
	row.add_child(col)

	name_label = Label.new()
	UITheme.apply_label(name_label, 22, UITheme.COL_GOLD)
	col.add_child(name_label)
	col.add_child(UITheme.hline())
	text_label = Label.new()
	UITheme.apply_label(text_label, 20, UITheme.COL_PANEL_TEXT)
	text_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text_label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	text_label.custom_minimum_size = Vector2(1000, 78)
	text_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	col.add_child(text_label)
	continue_icon = Label.new()
	UITheme.apply_label(continue_icon, 16, UITheme.COL_GOLD)
	continue_icon.text = "[E] continue      [1-4] choose"
	continue_icon.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	col.add_child(continue_icon)

	choice_box = VBoxContainer.new()
	choice_box.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	choice_box.position = Vector2(-470, -320)
	choice_box.custom_minimum_size = Vector2(440, 0)
	choice_box.add_theme_constant_override("separation", 6)
	choice_box.visible = false
	add_child(choice_box)

	set_process(true)


func show_node(dialogue_id: String, node: Dictionary, context: Dictionary) -> void:
	_context = context
	_lines = []
	for line in node.get("lines", []):
		_lines.append(str(line))
	if _lines.is_empty():
		_lines = ["..."]
	_line_index = 0
	_pending_choices = []
	choice_box.visible = false
	var speaker := str(node.get("speaker", context.get("npc", "")))
	var npc_def := Data.get_npc(speaker)
	name_label.text = str(npc_def.get("name", context.get("npc_name", speaker.capitalize())))
	var portrait_path := str(context.get("portrait", ""))
	if portrait_path == "":
		portrait_path = str(Data.get_character(str(npc_def.get("character", speaker))).get("portrait", ""))
	if portrait_path != "" and ResourceLoader.exists(portrait_path):
		portrait_rect.texture = load(portrait_path)
	else:
		var icon := UITheme.icon("star")
		portrait_rect.texture = icon
	_apply_line()


func _apply_line() -> void:
	if _line_index >= _lines.size():
		_finish_lines()
		return
	text_label.text = _lines[_line_index]
	_visible_chars = 0.0
	_typing = true
	text_label.visible_characters = 0
	continue_icon.text = ""


func _process(delta: float) -> void:
	if not visible:
		return
	if _typing:
		var speed := Settings.text_speed
		_visible_chars += delta * (speed if speed > 0.0 else 1000.0)
		var total := text_label.text.length()
		text_label.visible_characters = int(_visible_chars)
		if int(_visible_chars) >= total:
			_typing = false
			text_label.visible_characters = -1
			continue_icon.text = "[E] continue" if _line_index < _lines.size() - 1 else "[E] done"


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("interact") or event.is_action_pressed("ui_accept"):
		clicked()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed("pause") and not _typing:
		# ESC ends the conversation politely (no permanent consequence)
		Dialogue.finish()
		get_viewport().set_input_as_handled()
	elif event is InputEventKey and event.pressed and not _typing:
		var kc: int = event.keycode
		if kc >= KEY_1 and kc <= KEY_4:
			var idx := kc - KEY_1
			if idx < _pending_choices.size():
				Dialogue.choose(idx)
				choice_box.visible = false
				_pending_choices = []
				get_viewport().set_input_as_handled()


func clicked() -> void:
	if _typing:
		_typing = false
		text_label.visible_characters = -1
		continue_icon.text = "[E] continue"
		return
	if _pending_choices.size() > 0:
		return
	_line_index += 1
	if _line_index >= _lines.size():
		_finish_lines()
	else:
		_apply_line()


func _finish_lines() -> void:
	Dialogue.advance()


func show_choices(choices: Array) -> void:
	_pending_choices = choices
	for child in choice_box.get_children():
		child.queue_free()
	choice_box.visible = true
	for i in range(choices.size()):
		var choice: Dictionary = choices[i]
		var btn := Button.new()
		btn.text = "%d. %s" % [i + 1, str(choice.get("text", "..."))]
		UITheme.apply_button(btn, 17)
		btn.custom_minimum_size = Vector2(430, 0)
		var index := i
		btn.pressed.connect(func():
			choice_box.visible = false
			_pending_choices = []
			Dialogue.choose(index))
		choice_box.add_child(btn)
