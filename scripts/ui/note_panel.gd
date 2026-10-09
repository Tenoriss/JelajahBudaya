extends Control
## A parchment panel for readable notes, signs and found documents.

var title_label: Label
var body: RichTextLabel
var panel: PanelContainer


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.45)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	panel = UITheme.make_panel(UITheme.PANEL_PARCHMENT)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(-330, -200)
	panel.custom_minimum_size = Vector2(660, 400)
	add_child(panel)

	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 8)
	panel.add_child(col)
	title_label = Label.new()
	title_label.add_theme_font_size_override("font_size", 26)
	title_label.add_theme_color_override("font_color", Color(0.32, 0.21, 0.12))
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(title_label)
	body = RichTextLabel.new()
	body.bbcode_enabled = true
	body.fit_content = false
	body.scroll_active = true
	body.custom_minimum_size = Vector2(600, 300)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_theme_font_size_override("normal_font_size", 19)
	body.add_theme_color_override("default_color", Color(0.26, 0.18, 0.1))
	col.add_child(body)
	var close := Button.new()
	close.text = "Close  [E]"
	UITheme.apply_button(close, 18)
	close.pressed.connect(close_panel)
	col.add_child(close)


func show_note(title: String, text: String) -> void:
	title_label.text = title
	body.text = text


func close_panel() -> void:
	UI.close("note")


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("interact") or event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		close_panel()
		get_viewport().set_input_as_handled()
