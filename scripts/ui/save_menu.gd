extends Control
## Save / load slots.  Slot 0 is the autosave.

var row_box: VBoxContainer


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.06, 0.88)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)
	var title := UITheme.heading("Save / Load", 30)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 16)
	add_child(title)
	var panel := UITheme.make_panel(UITheme.PANEL_DARK)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(-380, -250)
	panel.custom_minimum_size = Vector2(760, 500)
	add_child(panel)
	row_box = VBoxContainer.new()
	row_box.add_theme_constant_override("separation", 8)
	panel.add_child(row_box)


func on_open() -> void:
	_refresh()


func _refresh() -> void:
	for child in row_box.get_children():
		child.queue_free()
	for slot in range(0, Save.SLOT_COUNT + 1):
		var info := Save.slot_info(slot)
		var row := PanelContainer.new()
		row.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT, 6))
		var hb := HBoxContainer.new()
		hb.add_theme_constant_override("separation", 10)
		row.add_child(hb)
		var col := VBoxContainer.new()
		col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		hb.add_child(col)
		var name_lbl := Label.new()
		UITheme.apply_label(name_lbl, 19, UITheme.COL_GOLD)
		name_lbl.text = "Autosave" if slot == 0 else "Slot %d" % slot
		col.add_child(name_lbl)
		var detail := Label.new()
		UITheme.apply_label(detail, 15, UITheme.COL_TEXT)
		if info.is_empty():
			detail.text = "(empty)"
			detail.add_theme_color_override("font_color", UITheme.COL_DIM)
		elif info.get("corrupted", false):
			detail.text = "Corrupted save file - ignored"
			detail.add_theme_color_override("font_color", UITheme.COL_BAD)
		else:
			detail.text = "%s  ·  %s  ·  Chapter %d  ·  %d quests  ·  %d CP  ·  play %s" % [
				info["region"], info["date"], info["chapter"], info["quests"], info["cp"], info["time"]]
		col.add_child(detail)
		if slot != 0:
			var save_btn := Button.new()
			save_btn.text = "Save"
			UITheme.apply_button(save_btn, 16)
			var s := slot
			save_btn.pressed.connect(func():
				Save.save_slot(s)
				_refresh())
			hb.add_child(save_btn)
		var load_btn := Button.new()
		load_btn.text = "Load"
		load_btn.disabled = info.is_empty()
		UITheme.apply_button(load_btn, 16)
		var s2 := slot
		load_btn.pressed.connect(func(): _load(s2))
		hb.add_child(load_btn)
		row_box.add_child(row)
	var back := Button.new()
	back.text = "Back"
	UITheme.apply_button(back, 19)
	back.pressed.connect(func(): UI.close("savemenu"))
	row_box.add_child(back)


func _load(slot: int) -> void:
	if not Save.load_slot(slot):
		Audio.ui_error()
		Notify.toast(Save.last_error)
		return
	UI.close_all()
	Audio.ui_confirm()
	get_tree().paused = false
	await World.fade_out(0.35)
	World.load_map(Game.current_map)
	await get_tree().process_frame
	await World.fade_in(0.35)
	var player = World.world_root.player if World.world_root != null else null
	if player != null and player.has_method("teleport"):
		player.teleport(Game.last_position if Game.last_position != Vector2.ZERO else player.position)
	Notify.banner("Loaded", "Slot %d" % slot, World.time_name(), 2.0)


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("savemenu")
		get_viewport().set_input_as_handled()
