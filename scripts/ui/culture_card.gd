extends Control
## "CULTURE DISCOVERED!" card shown when a journal entry is unlocked.

signal card_closed

var title_label: Label
var name_label: Label
var region_label: Label
var category_label: Label
var body: RichTextLabel
var fact_label: Label
var verify_label: Label
var panel: PanelContainer
var _queue_shown := false


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.05, 0.6)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	panel = UITheme.make_panel(UITheme.PANEL_BANNER)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(-320, -190)
	panel.custom_minimum_size = Vector2(640, 380)
	add_child(panel)

	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 6)
	panel.add_child(col)
	title_label = Label.new()
	UITheme.apply_label(title_label, 26, UITheme.COL_GOLD)
	title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_label.text = "CULTURE DISCOVERED!"
	col.add_child(title_label)
	name_label = Label.new()
	UITheme.apply_label(name_label, 30, Color(1, 0.98, 0.9))
	name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(name_label)
	var meta := HBoxContainer.new()
	meta.alignment = BoxContainer.ALIGNMENT_CENTER
	meta.add_theme_constant_override("separation", 10)
	col.add_child(meta)
	region_label = Label.new()
	UITheme.apply_label(region_label, 17, UITheme.COL_TEAL)
	meta.add_child(region_label)
	category_label = Label.new()
	UITheme.apply_label(category_label, 17, UITheme.COL_ACCENT)
	meta.add_child(category_label)
	col.add_child(UITheme.hline())
	body = RichTextLabel.new()
	body.bbcode_enabled = true
	body.fit_content = false
	body.custom_minimum_size = Vector2(590, 150)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_theme_font_size_override("normal_font_size", 18)
	body.add_theme_color_override("default_color", UITheme.COL_PANEL_TEXT)
	col.add_child(body)
	fact_label = Label.new()
	UITheme.apply_label(fact_label, 17, UITheme.COL_GOLD)
	fact_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	fact_label.custom_minimum_size = Vector2(590, 0)
	col.add_child(fact_label)
	verify_label = Label.new()
	UITheme.apply_label(verify_label, 15, Color(1, 0.75, 0.55))
	verify_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	verify_label.custom_minimum_size = Vector2(590, 0)
	verify_label.visible = false
	verify_label.text = "(This detail is marked for verification in the journal.)"
	col.add_child(verify_label)
	var close := Button.new()
	close.text = "Add to journal  [E]"
	UITheme.apply_button(close, 19)
	close.pressed.connect(close_card)
	col.add_child(close)


func show_entry(entry: Dictionary) -> void:
	name_label.text = str(entry.get("name", ""))
	region_label.text = str(Data.get_region(str(entry.get("region", ""))).get("name", str(entry.get("region", "")).capitalize()))
	category_label.text = str(entry.get("category", ""))
	var text := str(entry.get("text", entry.get("description", "")))
	var source := str(entry.get("source", ""))
	if source != "":
		text += "\n\n[Source: " + source + "]"
	body.text = text
	fact_label.text = "In short:  " + str(entry.get("short", entry.get("fact", "")))
	verify_label.visible = bool(entry.get("verify", false))
	visible = true
	modulate.a = 0.0
	var tw := create_tween()
	tw.tween_property(self, "modulate:a", 1.0, 0.28)
	panel.scale = Vector2(0.94, 0.94)
	panel.pivot_offset = panel.custom_minimum_size * 0.5
	var tw2 := create_tween()
	tw2.tween_property(panel, "scale", Vector2.ONE, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	Audio.culture_discovered()


func show_region(region: Dictionary) -> void:
	name_label.text = str(region.get("name", ""))
	region_label.text = "New region discovered"
	category_label.text = ""
	body.text = str(region.get("intro", ""))
	fact_label.text = str(region.get("tagline", ""))
	verify_label.visible = false
	title_label.text = "REGION DISCOVERED!"
	visible = true
	Audio.unlock()


func close_card() -> void:
	if not visible:
		return
	visible = false
	title_label.text = "CULTURE DISCOVERED!"
	Audio.ui_confirm()
	card_closed.emit()
	Culture.on_card_closed()


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("interact") or event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		close_card()
		get_viewport().set_input_as_handled()
