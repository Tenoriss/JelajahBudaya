extends Control
## Shop / trader screen.
##
## The trader's stock is data driven: every souvenir and everyday item whose
## "region" is the region the player is standing in (or the shared "prologue"
## goods) can be bought with Culture Points.  Buying spends points and adds the
## item to the satchel; there is no way to lose progress here.

var title_label: Label
var points_label: Label
var list_box: VBoxContainer
var detail_box: VBoxContainer
var status_label: Label

var stock: Array = []
var selected := ""


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false

	var bg := ColorRect.new()
	bg.color = Color(0.06, 0.05, 0.08, 0.86)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var panel := UITheme.make_panel(UITheme.PANEL_DARK)
	panel.position = Vector2(120, 60)
	panel.size = Vector2(1040, 600)
	add_child(panel)

	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 8)
	panel.add_child(col)

	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 12)
	col.add_child(head)
	title_label = Label.new()
	UITheme.apply_label(title_label, 26, UITheme.COL_GOLD)
	title_label.text = "Trading Post"
	head.add_child(title_label)
	points_label = Label.new()
	UITheme.apply_label(points_label, 20, UITheme.COL_TEAL)
	points_label.text = ""
	head.add_child(points_label)
	col.add_child(UITheme.hline())

	var body := HBoxContainer.new()
	body.add_theme_constant_override("separation", 14)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	col.add_child(body)

	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(600, 420)
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(scroll)
	list_box = VBoxContainer.new()
	list_box.add_theme_constant_override("separation", 6)
	list_box.custom_minimum_size = Vector2(580, 0)
	scroll.add_child(list_box)

	detail_box = VBoxContainer.new()
	detail_box.add_theme_constant_override("separation", 8)
	detail_box.custom_minimum_size = Vector2(390, 0)
	detail_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(detail_box)

	status_label = Label.new()
	UITheme.apply_label(status_label, 17, UITheme.COL_DIM)
	col.add_child(status_label)

	var buttons := HBoxContainer.new()
	buttons.add_theme_constant_override("separation", 10)
	col.add_child(buttons)
	var buy := Button.new()
	buy.text = "Buy selected  [SPACE]"
	UITheme.apply_button(buy, 18)
	buy.pressed.connect(_buy_selected)
	buttons.add_child(buy)
	var leave := Button.new()
	leave.text = "Leave  [ESC]"
	UITheme.apply_button(leave, 18)
	leave.pressed.connect(func(): UI.close("shop"))
	buttons.add_child(leave)


func on_open() -> void:
	_build_stock()
	_refresh()


func on_close() -> void:
	status_label.text = ""


func _build_stock() -> void:
	stock.clear()
	var region := Game.current_region
	for id in Data.items.keys():
		var def: Dictionary = Data.items[id]
		var cat := str(def.get("category", ""))
		if cat != "souvenirs" and cat != "items":
			continue
		var item_region := str(def.get("region", ""))
		if item_region != region and item_region != "prologue":
			continue
		if int(def.get("value", 0)) <= 0:
			continue
		stock.append(id)
	stock.sort_custom(func(a, b):
		return int(Data.items[a].get("value", 0)) < int(Data.items[b].get("value", 0)))


func _refresh() -> void:
	for child in list_box.get_children():
		child.queue_free()
	points_label.text = "Culture Points: %d" % Game.culture_points
	title_label.text = "Trading Post  ·  %s" % str(Data.get_region(Game.current_region).get("name", ""))
	if stock.is_empty():
		var empty := Label.new()
		UITheme.apply_label(empty, 18, UITheme.COL_DIM)
		empty.text = "Nothing for sale here today."
		list_box.add_child(empty)
		return
	for id in stock:
		var def: Dictionary = Data.items[id]
		var price := int(def.get("value", 0))
		var row := Button.new()
		var owned := Items.count(id)
		row.text = "%s   ·   %d CP%s" % [str(def.get("name", id)), price,
			("   (you have %d)" % owned) if owned > 0 else ""]
		UITheme.apply_button(row, 18)
		if id == selected:
			row.add_theme_color_override("font_color", UITheme.COL_GOLD)
		row.pressed.connect(func(): _select(id))
		row.mouse_entered.connect(func(): Audio.ui_hover())
		list_box.add_child(row)
	_show_detail()


func _select(id: String) -> void:
	selected = id
	Audio.ui_click()
	_refresh()


func _show_detail() -> void:
	for child in detail_box.get_children():
		child.queue_free()
	if selected == "" or not Data.items.has(selected):
		var hint := Label.new()
		UITheme.apply_label(hint, 18, UITheme.COL_DIM)
		hint.text = "Choose something from the list to look at it."
		hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		hint.custom_minimum_size = Vector2(380, 0)
		detail_box.add_child(hint)
		return
	var def: Dictionary = Data.items[selected]
	var icon := TextureRect.new()
	var icon_path := str(def.get("icon", ""))
	if icon_path != "" and ResourceLoader.exists(icon_path):
		icon.texture = load(icon_path)
	icon.custom_minimum_size = Vector2(96, 96)
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	detail_box.add_child(icon)

	var name_label := Label.new()
	UITheme.apply_label(name_label, 22, UITheme.COL_GOLD)
	name_label.text = str(def.get("name", selected))
	name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_label.custom_minimum_size = Vector2(380, 0)
	detail_box.add_child(name_label)

	var info := Label.new()
	UITheme.apply_label(info, 16, UITheme.COL_TEAL)
	info.text = "%s · %s · %d CP" % [str(def.get("category", "")), str(def.get("rarity", "common")),
		int(def.get("value", 0))]
	detail_box.add_child(info)

	var text := Label.new()
	UITheme.apply_label(text, 17, UITheme.COL_TEXT)
	text.text = str(def.get("description", ""))
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.custom_minimum_size = Vector2(380, 0)
	detail_box.add_child(text)


func _buy_selected() -> void:
	if selected == "" or not Data.items.has(selected):
		status_label.text = "Pick something first."
		Audio.ui_error()
		return
	var def: Dictionary = Data.items[selected]
	var price := int(def.get("value", 0))
	if Game.culture_points < price:
		status_label.text = "Not enough Culture Points for that yet (%d needed)." % price
		Audio.ui_error()
		return
	if not Game.spend_culture_points(price):
		status_label.text = "Not enough Culture Points."
		Audio.ui_error()
		return
	Items.add(selected, 1)
	Audio.coin()
	status_label.text = "Bought %s for %d Culture Points." % [str(def.get("name", selected)), price]
	_refresh()


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_ESCAPE:
				UI.close("shop")
			KEY_SPACE, KEY_ENTER:
				_buy_selected()
