extends Control
## Grid inventory: category tabs, item cells and a detail pane.

var grid: GridContainer
var detail_icon: TextureRect
var detail_name: Label
var detail_meta: Label
var detail_text: Label
var tabs: HBoxContainer
var current_category := "collectibles"
var selected := ""


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.03, 0.06, 0.82)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	var title := UITheme.heading("Satchel", 30)
	title.position = Vector2(0, 18)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	add_child(title)

	tabs = HBoxContainer.new()
	tabs.position = Vector2(60, 62)
	tabs.add_theme_constant_override("separation", 8)
	add_child(tabs)
	for cat in Items.CATEGORIES:
		var btn := Button.new()
		btn.text = Items.CATEGORY_LABELS[cat]
		UITheme.apply_button(btn, 17)
		var c := cat
		btn.pressed.connect(func(): _select_category(c))
		tabs.add_child(btn)

	var list_panel := UITheme.make_panel(UITheme.PANEL_DARK)
	list_panel.position = Vector2(48, 106)
	list_panel.custom_minimum_size = Vector2(700, 540)
	add_child(list_panel)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(670, 510)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	list_panel.add_child(scroll)
	grid = GridContainer.new()
	grid.columns = 6
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	scroll.add_child(grid)

	var detail_panel := UITheme.make_panel(UITheme.PANEL_SOFT)
	detail_panel.position = Vector2(772, 106)
	detail_panel.custom_minimum_size = Vector2(460, 540)
	add_child(detail_panel)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 8)
	detail_panel.add_child(col)
	detail_icon = TextureRect.new()
	detail_icon.custom_minimum_size = Vector2(84, 84)
	detail_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	col.add_child(detail_icon)
	detail_name = Label.new()
	UITheme.apply_label(detail_name, 24, UITheme.COL_GOLD)
	detail_name.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	detail_name.custom_minimum_size = Vector2(420, 0)
	col.add_child(detail_name)
	detail_meta = Label.new()
	UITheme.apply_label(detail_meta, 16, UITheme.COL_TEAL)
	col.add_child(detail_meta)
	col.add_child(UITheme.hline())
	detail_text = Label.new()
	UITheme.apply_label(detail_text, 17, UITheme.COL_PANEL_TEXT)
	detail_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	detail_text.custom_minimum_size = Vector2(420, 250)
	detail_text.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	col.add_child(detail_text)

	var footer := Label.new()
	UITheme.apply_label(footer, 15, UITheme.COL_DIM)
	footer.text = "Arrow keys / mouse to browse  ·  [I] or [ESC] to close"
	footer.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	footer.position = Vector2(0, -34)
	footer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(footer)
	Items.changed.connect(_refresh)


func on_open() -> void:
	_select_category(current_category)


func _select_category(cat: String) -> void:
	current_category = cat
	for i in range(tabs.get_child_count()):
		var btn := tabs.get_child(i) as Button
		btn.disabled = false
		if Items.CATEGORIES[i] == cat:
			btn.add_theme_color_override("font_color", UITheme.COL_GOLD)
		else:
			btn.add_theme_color_override("font_color", UITheme.COL_TEXT)
	_refresh()


func _refresh() -> void:
	if grid == null:
		return
	for child in grid.get_children():
		child.queue_free()
	var ids := Items.items_in_category(current_category)
	if ids.is_empty():
		var empty := Label.new()
		UITheme.apply_label(empty, 17, UITheme.COL_DIM)
		empty.text = "Nothing here yet. Explore the islands!"
		grid.add_child(empty)
		_show_detail("")
		return
	for id in ids:
		var def := Data.get_item(id)
		var cell := PanelContainer.new()
		cell.custom_minimum_size = Vector2(102, 102)
		cell.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT, 6))
		var vb := VBoxContainer.new()
		vb.alignment = BoxContainer.ALIGNMENT_CENTER
		cell.add_child(vb)
		var rect := TextureRect.new()
		var icon_path := str(def.get("icon", ""))
		if icon_path != "" and ResourceLoader.exists(icon_path):
			rect.texture = load(icon_path)
		else:
			rect.texture = UITheme.icon("star")
		rect.custom_minimum_size = Vector2(56, 56)
		rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		vb.add_child(rect)
		var lbl := Label.new()
		UITheme.apply_label(lbl, 11, UITheme.COL_TEXT)
		lbl.text = str(def.get("name", id))
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lbl.custom_minimum_size = Vector2(94, 0)
		vb.add_child(lbl)
		var count := Items.count(id)
		if count > 1:
			var badge := Label.new()
			UITheme.apply_label(badge, 12, UITheme.COL_GOLD)
			badge.text = "x%d" % count
			vb.add_child(badge)
		var btn := Button.new()
		btn.flat = true
		btn.set_anchors_preset(Control.PRESET_FULL_RECT)
		var item_id := str(id)
		btn.pressed.connect(func(): _show_detail(item_id))
		btn.mouse_entered.connect(func(): Audio.ui_hover())
		cell.add_child(btn)
		grid.add_child(cell)
	if selected == "" or not ids.has(selected):
		selected = str(ids[0])
	_show_detail(selected)


func _show_detail(id: String) -> void:
	selected = id
	if id == "":
		detail_name.text = ""
		detail_meta.text = ""
		detail_text.text = ""
		detail_icon.texture = null
		return
	var def := Data.get_item(id)
	detail_name.text = str(def.get("name", id))
	var region := str(def.get("region", ""))
	detail_meta.text = "%s  ·  %s" % [
		str(def.get("category", "")).capitalize(),
		Data.get_region(region).get("name", region.capitalize()) if region != "" else "—"]
	if def.has("rarity"):
		detail_meta.text += "  ·  " + str(def["rarity"]).capitalize()
	detail_text.text = str(def.get("description", ""))
	if def.has("note"):
		detail_text.text += "\n\n" + str(def["note"])
	var icon_path := str(def.get("icon", ""))
	detail_icon.texture = load(icon_path) if icon_path != "" and ResourceLoader.exists(icon_path) else UITheme.icon("star")
	Audio.ui_hover()


func on_close() -> void:
	pass


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("open_inventory") or event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("inventory")
		get_viewport().set_input_as_handled()
