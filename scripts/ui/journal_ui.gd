extends Control
## Culture Journal: entries grouped by category, with per-region progress bars
## and a detail page for each discovered entry.

var cat_list: VBoxContainer
var entry_list: VBoxContainer
var detail_title: Label
var detail_meta: Label
var detail_body: RichTextLabel
var progress_box: VBoxContainer
var current_category := ""


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := TextureRect.new()
	bg.texture = UITheme.texture(UITheme.PANEL_PARCHMENT)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.stretch_mode = TextureRect.STRETCH_TILE
	bg.modulate = Color(0.55, 0.5, 0.55)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	var title := UITheme.heading("Culture Journal", 32)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 16)
	title.add_theme_color_override("font_color", UITheme.COL_GOLD)
	add_child(title)

	var left := PanelContainer.new()
	left.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_DARK))
	left.position = Vector2(30, 70)
	left.custom_minimum_size = Vector2(290, 600)
	add_child(left)
	var lscroll := ScrollContainer.new()
	lscroll.custom_minimum_size = Vector2(266, 570)
	lscroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	left.add_child(lscroll)
	var lcol := VBoxContainer.new()
	lcol.add_theme_constant_override("separation", 4)
	lscroll.add_child(lcol)
	cat_list = VBoxContainer.new()
	cat_list.add_theme_constant_override("separation", 3)
	lcol.add_child(cat_list)
	lcol.add_child(UITheme.hline())
	progress_box = VBoxContainer.new()
	progress_box.add_theme_constant_override("separation", 3)
	lcol.add_child(progress_box)

	var mid := PanelContainer.new()
	mid.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_DARK))
	mid.position = Vector2(336, 70)
	mid.custom_minimum_size = Vector2(380, 600)
	add_child(mid)
	var mscroll := ScrollContainer.new()
	mscroll.custom_minimum_size = Vector2(356, 570)
	mscroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	mid.add_child(mscroll)
	entry_list = VBoxContainer.new()
	entry_list.add_theme_constant_override("separation", 2)
	mscroll.add_child(entry_list)

	var right := PanelContainer.new()
	right.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_PARCHMENT))
	right.position = Vector2(732, 70)
	right.custom_minimum_size = Vector2(500, 600)
	add_child(right)
	var rcol := VBoxContainer.new()
	rcol.add_theme_constant_override("separation", 6)
	right.add_child(rcol)
	detail_title = Label.new()
	detail_title.add_theme_font_size_override("font_size", 26)
	detail_title.add_theme_color_override("font_color", Color(0.3, 0.19, 0.1))
	detail_title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	detail_title.custom_minimum_size = Vector2(460, 0)
	rcol.add_child(detail_title)
	detail_meta = Label.new()
	detail_meta.add_theme_font_size_override("font_size", 16)
	detail_meta.add_theme_color_override("font_color", Color(0.45, 0.3, 0.16))
	rcol.add_child(detail_meta)
	detail_body = RichTextLabel.new()
	detail_body.bbcode_enabled = true
	detail_body.custom_minimum_size = Vector2(460, 480)
	detail_body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	detail_body.add_theme_font_size_override("normal_font_size", 17)
	detail_body.add_theme_color_override("default_color", Color(0.24, 0.16, 0.09))
	rcol.add_child(detail_body)

	var footer := Label.new()
	UITheme.apply_label(footer, 15, UITheme.COL_TEXT)
	footer.text = "[J] or [ESC] to close  ·  Entries marked (verify) need source checking"
	footer.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	footer.position = Vector2(0, -34)
	footer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(footer)


func on_open() -> void:
	_build_categories()
	_build_progress()


func _build_categories() -> void:
	for child in cat_list.get_children():
		child.queue_free()
	var cats := Culture.all_categories()
	if cats.is_empty():
		var lbl := Label.new()
		UITheme.apply_label(lbl, 16, UITheme.COL_DIM)
		lbl.text = "No categories"
		cat_list.add_child(lbl)
		return
	if current_category == "" or not cats.has(current_category):
		current_category = str(cats[0])
	for cat in cats:
		var ids := Culture.entries_in_category(str(cat))
		var total := 0
		for id in Data.cultures.keys():
			if str(Data.cultures[id].get("category", "")) == str(cat):
				total += 1
		var btn := Button.new()
		btn.text = "%s  (%d/%d)" % [str(cat), ids.size(), total]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		UITheme.apply_button(btn, 16)
		btn.custom_minimum_size = Vector2(256, 0)
		var c := str(cat)
		btn.pressed.connect(func(): _select_category(c))
		cat_list.add_child(btn)
	_select_category(current_category)


func _select_category(cat: String) -> void:
	current_category = cat
	for child in entry_list.get_children():
		child.queue_free()
	var ids := Culture.entries_in_category(cat)
	if ids.is_empty():
		var lbl := Label.new()
		UITheme.apply_label(lbl, 16, UITheme.COL_DIM)
		lbl.text = "Nothing discovered in this category yet."
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lbl.custom_minimum_size = Vector2(340, 0)
		entry_list.add_child(lbl)
		_show_entry("")
		return
	for id in ids:
		var entry: Dictionary = Data.cultures[id]
		var btn := Button.new()
		btn.text = str(entry.get("name", id))
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		UITheme.apply_button(btn, 17)
		btn.custom_minimum_size = Vector2(346, 0)
		var eid := str(id)
		btn.pressed.connect(func(): _show_entry(eid))
		entry_list.add_child(btn)
	_show_entry(str(ids[0]))


func _show_entry(id: String) -> void:
	if id == "" or not Data.cultures.has(id):
		detail_title.text = ""
		detail_meta.text = ""
		detail_body.text = ""
		return
	var entry: Dictionary = Data.cultures[id]
	detail_title.text = str(entry.get("name", ""))
	var region := str(entry.get("region", ""))
	detail_meta.text = "%s  ·  %s%s" % [
		Data.get_region(region).get("name", region.capitalize()),
		str(entry.get("category", "")),
		"  ·  needs verification" if bool(entry.get("verify", false)) else ""]
	var text := str(entry.get("description", ""))
	if entry.has("context"):
		text += "\n\n[b]Community / context:[/b] " + str(entry["context"])
	if entry.has("fact"):
		text += "\n\n[b]Short fact:[/b] " + str(entry["fact"])
	if bool(entry.get("verify", false)):
		text += "\n\n[i]This entry is marked for verification.[/i]"
	detail_body.text = text


func _build_progress() -> void:
	for child in progress_box.get_children():
		child.queue_free()
	var lbl := Label.new()
	UITheme.apply_label(lbl, 16, UITheme.COL_GOLD)
	lbl.text = "Culture collection"
	progress_box.add_child(lbl)
	for region_id in Data.region_order:
		var progress := Culture.region_progress(region_id)
		var row := VBoxContainer.new()
		row.add_theme_constant_override("separation", 0)
		var name_lbl := Label.new()
		UITheme.apply_label(name_lbl, 14, UITheme.COL_TEXT)
		name_lbl.text = "%s  %d/%d" % [Data.get_region(region_id).get("name", region_id),
				progress["found"], progress["total"]]
		row.add_child(name_lbl)
		row.add_child(UITheme.progress_bar(progress["found"], maxf(1.0, progress["total"]),
				UITheme.COL_TEAL, 250))
		progress_box.add_child(row)


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("open_journal") or event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("journal")
		get_viewport().set_input_as_handled()
