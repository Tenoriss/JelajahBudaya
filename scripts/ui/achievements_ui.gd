extends Control
## Achievement list with progress.

var list: VBoxContainer
var summary: Label


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.06, 0.85)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var title := UITheme.heading("Achievements", 30)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 16)
	add_child(title)
	summary = Label.new()
	UITheme.apply_label(summary, 17, UITheme.COL_TEAL)
	summary.set_anchors_preset(Control.PRESET_TOP_WIDE)
	summary.position = Vector2(0, 58)
	summary.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(summary)
	var panel := UITheme.make_panel(UITheme.PANEL_DARK)
	panel.position = Vector2(180, 92)
	panel.custom_minimum_size = Vector2(920, 560)
	add_child(panel)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(890, 530)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel.add_child(scroll)
	list = VBoxContainer.new()
	list.add_theme_constant_override("separation", 4)
	scroll.add_child(list)


func on_open() -> void:
	for child in list.get_children():
		child.queue_free()
	var ids: Array = Data.achievements.keys()
	ids.sort()
	var unlocked := 0
	for id in ids:
		var def: Dictionary = Data.achievements[id]
		var got := Achievements.is_unlocked(str(id))
		if got:
			unlocked += 1
		var row := PanelContainer.new()
		row.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT, 6))
		var hb := HBoxContainer.new()
		hb.add_theme_constant_override("separation", 10)
		row.add_child(hb)
		var icon := TextureRect.new()
		icon.texture = UITheme.icon("trophy" if got else "lock")
		icon.custom_minimum_size = Vector2(36, 36)
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		hb.add_child(icon)
		var col := VBoxContainer.new()
		col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		hb.add_child(col)
		var name_lbl := Label.new()
		UITheme.apply_label(name_lbl, 19, UITheme.COL_GOLD if got else UITheme.COL_DIM)
		name_lbl.text = str(def.get("name", id))
		col.add_child(name_lbl)
		var desc := Label.new()
		UITheme.apply_label(desc, 15, UITheme.COL_TEXT if got else Color(0.55, 0.5, 0.48))
		desc.text = str(def.get("description", ""))
		desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		desc.custom_minimum_size = Vector2(760, 0)
		col.add_child(desc)
		if got and def.has("unlock_text"):
			var extra := Label.new()
			UITheme.apply_label(extra, 14, UITheme.COL_TEAL)
			extra.text = str(def["unlock_text"])
			col.add_child(extra)
		list.add_child(row)
	summary.text = "%d / %d  ·  %.0f%% complete" % [unlocked, ids.size(), Achievements.progress_percent()]


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("achievements")
		get_viewport().set_input_as_handled()
