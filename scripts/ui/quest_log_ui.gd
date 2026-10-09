extends Control
## Quest log: active + completed quests, objectives and the hint system.

var list: VBoxContainer
var detail_title: Label
var detail_body: RichTextLabel
var hint_box: VBoxContainer
var region_bar: HBoxContainer
var selected := ""
var selected_region := ""
var requested_region := ""


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.06, 0.85)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	var title := UITheme.heading("Quest Journal", 30)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 16)
	add_child(title)

	selected_region = Game.current_region if Game.current_region != "" else "prologue"
	region_bar = HBoxContainer.new()
	region_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	region_bar.position = Vector2(40, 52)
	region_bar.custom_minimum_size = Vector2(1200, 34)
	region_bar.add_theme_constant_override("separation", 6)
	add_child(region_bar)
	_build_region_tabs()

	var left := PanelContainer.new()
	left.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_DARK))
	left.position = Vector2(40, 94)
	left.custom_minimum_size = Vector2(460, 570)
	add_child(left)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(436, 540)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	left.add_child(scroll)
	list = VBoxContainer.new()
	list.add_theme_constant_override("separation", 3)
	scroll.add_child(list)

	var right := PanelContainer.new()
	right.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT))
	right.position = Vector2(516, 94)
	right.custom_minimum_size = Vector2(716, 570)
	add_child(right)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 6)
	right.add_child(col)
	detail_title = Label.new()
	UITheme.apply_label(detail_title, 26, UITheme.COL_GOLD)
	detail_title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	detail_title.custom_minimum_size = Vector2(670, 0)
	col.add_child(detail_title)
	col.add_child(UITheme.hline())
	detail_body = RichTextLabel.new()
	detail_body.bbcode_enabled = true
	detail_body.custom_minimum_size = Vector2(670, 300)
	detail_body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	detail_body.add_theme_font_size_override("normal_font_size", 18)
	detail_body.add_theme_color_override("default_color", UITheme.COL_PANEL_TEXT)
	col.add_child(detail_body)
	hint_box = VBoxContainer.new()
	hint_box.add_theme_constant_override("separation", 4)
	col.add_child(hint_box)

	var footer := Label.new()
	UITheme.apply_label(footer, 15, UITheme.COL_DIM)
	footer.text = "Press [T] to track a quest  ·  [ESC] to close"
	footer.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	footer.position = Vector2(0, -32)
	footer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(footer)


func on_open() -> void:
	if requested_region != "" and Data.get_region(requested_region).size() > 0:
		selected_region = requested_region
		requested_region = ""
	elif Game.current_region != "" and Data.get_region(Game.current_region).size() > 0:
		selected_region = Game.current_region
	_update_region_tabs()
	_refresh()


func request_region(region_id: String) -> void:
	if Data.get_region(region_id).size() > 0:
		requested_region = region_id


func _region_ids() -> Array:
	var ids: Array = ["prologue"]
	for region_id in Data.region_order:
		if not ids.has(str(region_id)):
			ids.append(str(region_id))
	return ids


func _build_region_tabs() -> void:
	var group := ButtonGroup.new()
	for region_id in _region_ids():
		var rid := str(region_id)
		var def := Data.get_region(rid)
		var btn := Button.new()
		btn.toggle_mode = true
		btn.button_group = group
		btn.button_pressed = rid == selected_region
		btn.set_meta("region_id", rid)
		var quest_count := Data.get_quests_in_region(rid).size()
		btn.text = "%s  ·  %d" % [str(def.get("name", rid.capitalize())), quest_count]
		UITheme.apply_button(btn, 13)
		btn.custom_minimum_size = Vector2(190, 34)
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.pressed.connect(func(): _select_region(rid))
		region_bar.add_child(btn)


func _update_region_tabs() -> void:
	if region_bar == null:
		return
	for button in region_bar.get_children():
		if button is Button:
			button.button_pressed = str(button.get_meta("region_id", "")) == selected_region


func _select_region(region_id: String) -> void:
	if not Data.region_order.has(region_id) and region_id != "prologue":
		return
	selected_region = region_id
	selected = ""
	_update_region_tabs()
	_refresh()


func _refresh() -> void:
	for child in list.get_children():
		child.queue_free()
	var region_quests := Data.get_quests_in_region(selected_region)
	region_quests.sort_custom(func(a, b):
		var chapter_a := int(Data.get_quest(str(a)).get("chapter", 0))
		var chapter_b := int(Data.get_quest(str(b)).get("chapter", 0))
		return chapter_a < chapter_b if chapter_a != chapter_b else str(a) < str(b))
	var act: Array = []
	var avail: Array = []
	var done: Array = []
	var locked: Array = []
	for quest_id in region_quests:
		match Quest.state_name(str(quest_id)):
			"Active": act.append(quest_id)
			"Available": avail.append(quest_id)
			"Completed": done.append(quest_id)
			_: locked.append(quest_id)
	_add_section("Active", act, UITheme.COL_GOLD)
	_add_section("Available", avail, UITheme.COL_TEAL)
	_add_section("Completed", done, UITheme.COL_DIM)
	_add_section("Locked", locked, UITheme.COL_DIM)
	if region_quests.is_empty():
		var lbl := Label.new()
		UITheme.apply_label(lbl, 16, UITheme.COL_DIM)
		lbl.text = "No quests authored for this region yet."
		list.add_child(lbl)
	if not region_quests.has(selected):
		selected = ""
		for candidates in [act, avail, done, locked]:
			if not candidates.is_empty():
				selected = str(candidates[0])
				break
	_show(selected)


func _add_section(title: String, ids: Array, colour: Color) -> void:
	if ids.is_empty():
		return
	var head := Label.new()
	UITheme.apply_label(head, 17, colour)
	head.text = title
	list.add_child(head)
	for id in ids:
		var def := Data.get_quest(str(id))
		var btn := Button.new()
		var mark := ">" if Quest.tracked_quest() == str(id) else " "
		btn.text = "%s %s" % [mark, str(def.get("title", id))]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		UITheme.apply_button(btn, 17)
		btn.custom_minimum_size = Vector2(420, 0)
		var qid := str(id)
		btn.pressed.connect(func(): _show(qid))
		list.add_child(btn)


func _show(id: String) -> void:
	selected = id
	for child in hint_box.get_children():
		child.queue_free()
	if id == "" or not Data.quests.has(id):
		detail_title.text = ""
		detail_body.text = ""
		return
	var def: Dictionary = Data.quests[id]
	detail_title.text = str(def.get("title", id))
	var region := str(def.get("region", ""))
	var text := "[b]%s[/b]  ·  %s\n\n%s" % [
		Data.get_region(region).get("name", region.capitalize()),
		Quest.state_name(id),
		str(def.get("description", ""))]
	if Quest.is_active(id):
		text += "\n\n[b]Objectives[/b]\n" + Quest.progress_text(id)
	if Quest.is_completed(id):
		text += "\n\n[i]Completed.[/i]"
	if def.has("reward_text"):
		text += "\n\n[b]Reward:[/b] " + str(def["reward_text"])
	detail_body.text = text
	if Quest.is_active(id):
		var track := Button.new()
		track.text = "Track this quest"
		UITheme.apply_button(track, 17)
		var qid := str(id)
		track.pressed.connect(func(): Quest.set_tracked(qid); _refresh())
		hint_box.add_child(track)
		_add_hints(str(id))


func _add_hints(id: String) -> void:
	var hints: Array = Data.get_quest(id).get("hints", [])
	if hints.is_empty():
		return
	var lbl := Label.new()
	UITheme.apply_label(lbl, 15, UITheme.COL_TEAL)
	lbl.text = "Hints (revealing one costs a few Culture Points)"
	hint_box.add_child(lbl)
	for i in range(hints.size()):
		var row := HBoxContainer.new()
		var revealed := Quest.objective_progress(id, "_hint_%d" % i) > 0
		revealed = revealed or Game.has_flag("hint_%d_%s" % [i, id])
		var btn := Button.new()
		btn.text = "Hint %d" % (i + 1) if not revealed else "Hint %d shown" % (i + 1)
		UITheme.apply_button(btn, 16)
		btn.disabled = revealed
		var idx := i
		var qid := str(id)
		btn.pressed.connect(func():
			Game.set_flag("hint_%d_%s" % [idx, qid], true)
			if Game.culture_points >= Game.CP_HINT_PENALTY:
				Game.add_culture_points(-Game.CP_HINT_PENALTY, "hint")
			_refresh())
		row.add_child(btn)
		var text := Label.new()
		UITheme.apply_label(text, 16, UITheme.COL_TEXT)
		text.text = str(hints[i]) if revealed else "..."
		text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		text.custom_minimum_size = Vector2(520, 0)
		row.add_child(text)
		hint_box.add_child(row)


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventKey and event.pressed and event.keycode == KEY_T:
		if selected != "":
			Quest.set_tracked(selected)
			_refresh()
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("quests")
		get_viewport().set_input_as_handled()
