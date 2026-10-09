extends Control
## Interactive stylised map of the archipelago: region status, completion,
## discovered landmarks and fast travel between them.

const REGION_ANCHORS := {
	"prologue": Vector2(120, 300),
	"sumatra": Vector2(168, 176),
	"java": Vector2(392, 366),
	"kalimantan": Vector2(430, 168),
	"kalimantan_east": Vector2(500, 150),
	"sulawesi": Vector2(620, 196),
	"papua": Vector2(828, 262),
}

var canvas: Control
var info_box: VBoxContainer
var region_buttons: HBoxContainer
var selected_region := "sumatra"
var selected_map_id := ""
var view_mode := "archipelago"


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := TextureRect.new()
	bg.texture = UITheme.texture(UITheme.PANEL_PARCHMENT)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.stretch_mode = TextureRect.STRETCH_TILE
	bg.modulate = Color(0.45, 0.52, 0.6)
	add_child(bg)

	var title := UITheme.heading("Nusantara", 32)
	title.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title.position = Vector2(0, 14)
	add_child(title)

	canvas = Control.new()
	canvas.position = Vector2(28, 60)
	canvas.custom_minimum_size = Vector2(900, 600)
	canvas.mouse_filter = Control.MOUSE_FILTER_PASS
	canvas.draw.connect(_draw_map)
	canvas.gui_input.connect(_on_canvas_input)
	add_child(canvas)

	var right := PanelContainer.new()
	right.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_DARK))
	right.position = Vector2(946, 60)
	right.custom_minimum_size = Vector2(304, 600)
	add_child(right)
	var info_scroll := ScrollContainer.new()
	info_scroll.custom_minimum_size = Vector2(284, 580)
	info_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	info_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right.add_child(info_scroll)
	info_box = VBoxContainer.new()
	info_box.custom_minimum_size = Vector2(270, 0)
	info_box.add_theme_constant_override("separation", 5)
	info_scroll.add_child(info_box)

	region_buttons = HBoxContainer.new()
	region_buttons.position = Vector2(28, 664)
	region_buttons.add_theme_constant_override("separation", 6)
	add_child(region_buttons)


func on_open() -> void:
	view_mode = "archipelago"
	if Game.current_region != "" and Data.get_region(Game.current_region).size() > 0:
		selected_region = Game.current_region
	else:
		selected_region = "prologue"
	var maps := Data.maps_of(selected_region)
	if maps.has(World.current_map_id):
		selected_map_id = World.current_map_id
	else:
		selected_map_id = str(maps[0]) if not maps.is_empty() else ""
	_build_buttons()
	_refresh_info()
	canvas.queue_redraw()


func _map_region_ids() -> Array:
	var ids: Array = ["prologue"]
	for region_id in Data.region_order:
		if not ids.has(str(region_id)):
			ids.append(str(region_id))
	return ids


func _build_buttons() -> void:
	for child in region_buttons.get_children():
		child.queue_free()
	var group := ButtonGroup.new()
	for region_id in _map_region_ids():
		var rid := str(region_id)
		var def := Data.get_region(rid)
		var btn := Button.new()
		btn.toggle_mode = true
		btn.button_group = group
		btn.button_pressed = rid == selected_region
		var state := Game.region_state(rid)
		btn.text = str(def.get("name", rid))
		if state == "locked":
			btn.text += "  (locked · preview)"
		btn.tooltip_text = "Open the schematic route map for %s. Locked regions are view-only." % [
			str(def.get("name", rid))]
		UITheme.apply_button(btn, 13)
		btn.custom_minimum_size = Vector2(138, 34)
		btn.pressed.connect(func(): _select_region(rid))
		region_buttons.add_child(btn)


func _select_region(region_id: String) -> void:
	selected_region = region_id
	var maps := Data.maps_of(selected_region)
	if not maps.has(selected_map_id):
		selected_map_id = str(maps[0]) if not maps.is_empty() else ""
	_refresh_info()
	canvas.queue_redraw()
	Audio.ui_click()


func _region_center(region_id: String) -> Vector2:
	if REGION_ANCHORS.has(region_id):
		return REGION_ANCHORS[region_id]
	return Vector2(400, 300)


func _draw_map() -> void:
	var c := canvas
	if view_mode == "regional":
		_draw_region_route(c)
		return
	# sea
	c.draw_rect(Rect2(Vector2.ZERO, canvas.custom_minimum_size), Color(0.22, 0.35, 0.5, 0.35), true)
	for i in range(0, 900, 40):
		c.draw_line(Vector2(i, 0), Vector2(i - 120, 600), Color(1, 1, 1, 0.03), 6)
	# island shapes (stylised silhouettes)
	_draw_island(c, "sumatra", [
		Vector2(96, 96), Vector2(150, 130), Vector2(196, 210), Vector2(224, 300),
		Vector2(196, 392), Vector2(150, 430), Vector2(120, 380), Vector2(120, 300),
		Vector2(100, 210),
	])
	_draw_island(c, "java", [
		Vector2(300, 380), Vector2(392, 348), Vector2(520, 372), Vector2(600, 400),
		Vector2(520, 420), Vector2(392, 404), Vector2(320, 406),
	])
	_draw_island(c, "kalimantan", [
		Vector2(330, 190), Vector2(392, 120), Vector2(500, 96), Vector2(560, 150),
		Vector2(560, 250), Vector2(500, 300), Vector2(420, 296), Vector2(360, 252),
	])
	_draw_island(c, "sulawesi", [
		Vector2(586, 130), Vector2(620, 160), Vector2(600, 200), Vector2(660, 240),
		Vector2(700, 300), Vector2(668, 320), Vector2(620, 260), Vector2(590, 230),
		Vector2(566, 180),
	])
	_draw_island(c, "papua", [
		Vector2(740, 180), Vector2(830, 160), Vector2(896, 210), Vector2(896, 300),
		Vector2(820, 340), Vector2(756, 300), Vector2(736, 240),
	])
	# landmarks
	for entry in World.all_landmarks(""):
		if not entry.get("discovered", false):
			continue
		var region := str(entry.get("region", ""))
		var base := _region_center(region)
		var map := Data.get_map(str(entry.get("map", "")))
		var size_arr: Array = map.get("size", [40, 30])
		var pos: Array = entry.get("pos", [0, 0])
		var offset := Vector2((float(pos[0]) / maxf(1.0, float(size_arr[0]))) - 0.5,
				(float(pos[1]) / maxf(1.0, float(size_arr[1]))) - 0.5) * Vector2(96, 76)
		var p := base + offset
		c.draw_circle(p, 5.5, UITheme.COL_GOLD)
		c.draw_circle(p, 3.0, Color(0.2, 0.14, 0.1))
		var font := ThemeDB.fallback_font
		c.draw_string(font, p + Vector2(9, 5), str(entry.get("name", "")),
				HORIZONTAL_ALIGNMENT_LEFT, -1, 13, UITheme.COL_TEXT)
	# region labels + completion
	for region_id in Data.region_order:
		var def := Data.get_region(str(region_id))
		var state := Game.region_state(str(region_id))
		var center := _region_center(str(region_id))
		var colour := Color(0.5, 0.45, 0.42)
		match state:
			"unlocked":
				colour = UITheme.COL_TEAL
			"in_progress":
				colour = UITheme.COL_GOLD
			"completed":
				colour = UITheme.COL_OK
		var label_pos := center + Vector2(-40, -96)
		var font := ThemeDB.fallback_font
		c.draw_string(font, label_pos, str(def.get("name", region_id)),
				HORIZONTAL_ALIGNMENT_LEFT, -1, 22, colour)
		var progress := Game.region_progress_percent(str(region_id))
		c.draw_string(font, label_pos + Vector2(0, 18), "%d%% complete" % int(progress),
				HORIZONTAL_ALIGNMENT_LEFT, -1, 14, colour)
	# player position marker
	if World.current_map_id != "":
		var region := Game.current_region
		if REGION_ANCHORS.has(region):
			c.draw_circle(_region_center(region) + Vector2(0, 0), 7.0, Color(1, 0.4, 0.35, 0.8))
			c.draw_circle(_region_center(region), 4.0, Color(1, 0.95, 0.85))


func _draw_region_route(c: Control) -> void:
	var draw_size := canvas.size
	if draw_size.x <= 0.0 or draw_size.y <= 0.0:
		draw_size = canvas.custom_minimum_size
	c.draw_rect(Rect2(Vector2.ZERO, draw_size), Color(0.13, 0.22, 0.26, 0.92), true)
	for x in range(24, int(draw_size.x), 48):
		c.draw_line(Vector2(x, 62), Vector2(x, draw_size.y - 18), Color(0.75, 0.86, 0.8, 0.035), 1.0)
	for y in range(72, int(draw_size.y), 48):
		c.draw_line(Vector2(24, y), Vector2(draw_size.x - 24, y), Color(0.75, 0.86, 0.8, 0.035), 1.0)
	var font := ThemeDB.fallback_font
	var region_def := Data.get_region(selected_region)
	c.draw_string(font, Vector2(24, 30), str(region_def.get("name", selected_region)) + " — ROUTE MAP",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 22, UITheme.COL_GOLD)
	c.draw_string(font, Vector2(24, 50),
			"Schematic gameplay route · not geographic scale · select a node to inspect",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 13, UITheme.COL_PANEL_TEXT)
	var map_ids := Data.maps_of(selected_region)
	var route_layout: Dictionary = Data.route_maps.get(selected_region, {})
	if map_ids.is_empty():
		c.draw_string(font, Vector2(32, 110), "No local map locations are available yet.",
				HORIZONTAL_ALIGNMENT_LEFT, -1, 16, UITheme.COL_DIM)
		return
	var points: Dictionary = {}
	for map_value in map_ids:
		var map_id := str(map_value)
		var entry: Dictionary = route_layout.get(map_id, {})
		var raw_position: Array = entry.get("position", [500, 180])
		var raw_x := float(raw_position[0]) if raw_position.size() > 0 else 500.0
		var raw_y := float(raw_position[1]) if raw_position.size() > 1 else 180.0
		var x_span := maxf(300.0, draw_size.x - 110.0)
		var y_span := maxf(220.0, draw_size.y - 160.0)
		points[map_id] = Vector2(
			55.0 + raw_x / 1000.0 * x_span,
			76.0 + raw_y / 360.0 * y_span)
	var drawn_edges: Dictionary = {}
	for map_value in map_ids:
		var map_id := str(map_value)
		var from: Vector2 = points[map_id]
		var entry: Dictionary = route_layout.get(map_id, {})
		for target_value in entry.get("connections", []):
			var target_id := str(target_value)
			if not points.has(target_id):
				continue
			var edge_start := map_id if map_id < target_id else target_id
			var edge_end := target_id if map_id < target_id else map_id
			var key := edge_start + "|" + edge_end
			if drawn_edges.has(key):
				continue
			drawn_edges[key] = true
			c.draw_line(from, points[target_id], Color(0.67, 0.78, 0.58, 0.72),
					3.0, true)
	var quest_targets := _tracked_quest_map_targets(map_ids)
	for map_value in map_ids:
		var map_id := str(map_value)
		var point: Vector2 = points[map_id]
		var map_def := Data.get_map(map_id)
		var is_current := World.current_map_id == map_id
		var is_selected := selected_map_id == map_id
		var is_quest_target := quest_targets.has(map_id)
		if is_quest_target:
			c.draw_arc(point, 28.0, 0.0, TAU, 40, Color(0.88, 0.61, 0.33, 0.9), 2.5, true)
		if is_current:
			c.draw_circle(point, 22.0, Color(0.84, 0.71, 0.36, 0.28))
		elif is_selected:
			c.draw_circle(point, 21.0, Color(0.31, 0.7, 0.68, 0.26))
		c.draw_circle(point, 15.0, UITheme.COL_PANEL_DARK)
		var node_outline := UITheme.COL_GOLD if is_current else UITheme.COL_TEXT
		if is_selected and not is_current:
			node_outline = UITheme.COL_TEAL
		c.draw_arc(point, 15.0, 0.0, TAU, 40, node_outline, 2.0, true)
		var state_color := UITheme.COL_GOLD if is_current else UITheme.COL_TEXT
		var location_name := str(map_def.get("name", map_id))
		c.draw_string(font, point + Vector2(-118, 38), location_name,
				HORIZONTAL_ALIGNMENT_CENTER, 236, 15, state_color)
		if is_current:
			c.draw_string(font, point + Vector2(-65, -24), "YOU ARE HERE",
					HORIZONTAL_ALIGNMENT_CENTER, 130, 10, UITheme.COL_GOLD)
		elif is_quest_target:
			c.draw_string(font, point + Vector2(-66, -24), "TRACKED QUEST",
					HORIZONTAL_ALIGNMENT_CENTER, 132, 10, Color(0.96, 0.72, 0.44))


func _tracked_quest_map_targets(map_ids: Array) -> Array:
	var targets: Array = []
	var quest_id := Quest.tracked_quest()
	if quest_id == "":
		return targets
	var quest_def := Data.get_quest(quest_id)
	for map_value in map_ids:
		var map_id := str(map_value)
		var map_def := Data.get_map(map_id)
		var belongs := false
		for objective in quest_def.get("objectives", []):
			var objective_type := str(objective.get("type", ""))
			var target := str(objective.get("target", ""))
			if objective_type == "reach" and target == map_id:
				belongs = true
				break
			for list_name in ["npcs", "landmarks", "interactables"]:
				for record in map_def.get(list_name, []):
					if str(record.get("id", "")) == target or str(record.get("target", "")) == target:
						belongs = true
						break
				if belongs:
					break
			if belongs:
				break
		if not belongs:
			var start_npc := str(quest_def.get("start", {}).get("npc", ""))
			var finish_npc := str(quest_def.get("complete", {}).get("npc", ""))
			for npc in map_def.get("npcs", []):
				if str(npc.get("id", "")) == start_npc or str(npc.get("id", "")) == finish_npc:
					belongs = true
					break
		if belongs:
			targets.append(map_id)
	return targets


func _draw_island(c: Control, region_id: String, points: Array) -> void:
	var state := Game.region_state(region_id)
	var fill := Color(0.35, 0.42, 0.3, 0.85)
	var outline := Color(0.2, 0.24, 0.18)
	if state == "locked":
		fill = Color(0.3, 0.3, 0.33, 0.7)
		outline = Color(0.2, 0.2, 0.22)
	elif state == "in_progress":
		fill = Color(0.42, 0.5, 0.3, 0.9)
	c.draw_colored_polygon(PackedVector2Array(points), fill)
	var closed := PackedVector2Array(points)
	closed.append(points[0])
	c.draw_polyline(closed, outline, 3.0)
	if state == "locked":
		var center := Vector2.ZERO
		for p in points:
			center += p
		center /= float(points.size())
		c.draw_string(ThemeDB.fallback_font, center + Vector2(-24, 4), "LOCKED",
				HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color(0.85, 0.8, 0.75, 0.8))


func _refresh_info() -> void:
	for child in info_box.get_children():
		child.queue_free()
	var def := Data.get_region(selected_region)
	var name_lbl := Label.new()
	UITheme.apply_label(name_lbl, 24, UITheme.COL_GOLD)
	name_lbl.text = str(def.get("name", selected_region))
	name_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_lbl.custom_minimum_size = Vector2(260, 0)
	info_box.add_child(name_lbl)
	var state_lbl := Label.new()
	UITheme.apply_label(state_lbl, 16, UITheme.COL_TEAL)
	state_lbl.text = "Status: " + Game.region_state(selected_region).replace("_", " ").capitalize()
	info_box.add_child(state_lbl)
	var intro := Label.new()
	UITheme.apply_label(intro, 14, UITheme.COL_PANEL_TEXT)
	intro.text = str(def.get("intro", ""))
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	intro.custom_minimum_size = Vector2(260, 0)
	info_box.add_child(intro)
	info_box.add_child(UITheme.hline())
	var qstats := Quest.region_stats(selected_region)
	var cstats := Culture.region_progress(selected_region)
	var map_count := Data.maps_of(selected_region).size()
	var landmark_count := _landmark_count(selected_region)
	var lines: Array = [
		"Quests: %d/%d" % [qstats["completed"], qstats["total"]],
		"Journal: %d/%d" % [cstats["found"], cstats["total"]],
		"Locations: %d · Landmarks found: %d" % [map_count, landmark_count],
	]
	for line in lines:
		var lbl := Label.new()
		UITheme.apply_label(lbl, 14, UITheme.COL_TEXT)
		lbl.text = line
		info_box.add_child(lbl)
	info_box.add_child(UITheme.progress_bar(Game.region_progress_percent(selected_region), 100.0,
			UITheme.COL_GOLD, 260))
	var mode_button := Button.new()
	mode_button.text = "Back to archipelago" if view_mode == "regional" else "Open island route map"
	UITheme.apply_button(mode_button, 15)
	mode_button.custom_minimum_size = Vector2(260, 38)
	mode_button.pressed.connect(func():
		if view_mode == "regional":
			view_mode = "archipelago"
		else:
			view_mode = "regional"
			var local_maps := Data.maps_of(selected_region)
			if local_maps.has(World.current_map_id):
				selected_map_id = World.current_map_id
			else:
				selected_map_id = str(local_maps[0]) if not local_maps.is_empty() else ""
		_refresh_info()
		canvas.queue_redraw())
	info_box.add_child(mode_button)
	info_box.add_child(UITheme.hline())
	if view_mode == "regional":
		_add_regional_map_details()
	else:
		_add_fast_travel_details()


func _add_fast_travel_details() -> void:
	var head := Label.new()
	UITheme.apply_label(head, 17, UITheme.COL_GOLD)
	head.text = "Fast travel"
	info_box.add_child(head)
	var found: Array = []
	for entry in World.all_landmarks(selected_region):
		if entry.get("discovered", false):
			found.append(entry)
	if found.is_empty():
		var lbl2 := Label.new()
		UITheme.apply_label(lbl2, 14, UITheme.COL_DIM)
		lbl2.text = "No landmarks discovered here yet."
		info_box.add_child(lbl2)
	for entry in found:
		var btn := Button.new()
		btn.text = str(entry.get("name", ""))
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		UITheme.apply_button(btn, 14)
		btn.custom_minimum_size = Vector2(260, 0)
		var lm_id := str(entry.get("id", ""))
		btn.pressed.connect(func():
			UI.close("worldmap")
			World.fast_travel(lm_id))
		info_box.add_child(btn)


func _add_regional_map_details() -> void:
	var local_maps := Data.maps_of(selected_region)
	if not local_maps.has(selected_map_id):
		selected_map_id = str(local_maps[0]) if not local_maps.is_empty() else ""
	var head := Label.new()
	UITheme.apply_label(head, 17, UITheme.COL_GOLD)
	head.text = "Locations in this region"
	info_box.add_child(head)
	var group := ButtonGroup.new()
	for map_value in local_maps:
		var map_id := str(map_value)
		var map_def := Data.get_map(map_id)
		var btn := Button.new()
		btn.toggle_mode = true
		btn.button_group = group
		btn.button_pressed = map_id == selected_map_id
		btn.text = ("●  " if map_id == World.current_map_id else "○  ") + str(map_def.get("name", map_id))
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.tooltip_text = "Select this location on the regional route map."
		UITheme.apply_button(btn, 13)
		btn.custom_minimum_size = Vector2(260, 34)
		btn.pressed.connect(func(): _select_local_map(map_id))
		info_box.add_child(btn)
	if selected_map_id != "":
		var selected_def := Data.get_map(selected_map_id)
		var info := Label.new()
		UITheme.apply_label(info, 15, UITheme.COL_TEAL)
		info.text = "Selected: " + str(selected_def.get("name", selected_map_id))
		info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		info.custom_minimum_size = Vector2(260, 0)
		info_box.add_child(info)
		var route_info: Dictionary = Data.route_maps.get(selected_region, {}).get(selected_map_id, {})
		var connection_names: Array = []
		for connected_id in route_info.get("connections", []):
			connection_names.append(str(Data.get_map(str(connected_id)).get("name", connected_id)))
		var connection_label := Label.new()
		UITheme.apply_label(connection_label, 13, UITheme.COL_PANEL_TEXT)
		var connection_text := ", ".join(connection_names)
		if connection_text.is_empty():
			connection_text = "No same-region route connection listed."
		connection_label.text = "Connected route: " + connection_text
		connection_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		connection_label.custom_minimum_size = Vector2(260, 0)
		info_box.add_child(connection_label)
		var status_label := Label.new()
		UITheme.apply_label(status_label, 13, UITheme.COL_DIM)
		if World.current_map_id == selected_map_id:
			status_label.text = "You are here."
		else:
			status_label.text = "Find the connecting path in the game world."
		info_box.add_child(status_label)
	info_box.add_child(UITheme.hline())
	var quest_head := Label.new()
	UITheme.apply_label(quest_head, 17, UITheme.COL_GOLD)
	quest_head.text = "Quests for " + str(def.get("name", selected_region))
	info_box.add_child(quest_head)
	var quest_ids := Data.get_quests_in_region(selected_region)
	if quest_ids.is_empty():
		var no_quests := Label.new()
		UITheme.apply_label(no_quests, 14, UITheme.COL_DIM)
		no_quests.text = "No quests are authored for this region yet."
		info_box.add_child(no_quests)
	for quest_id in quest_ids:
		var quest_def := Data.get_quest(str(quest_id))
		var quest_label := Label.new()
		UITheme.apply_label(quest_label, 12, UITheme.COL_PANEL_TEXT)
		quest_label.text = "[%s] %s" % [
			Quest.state_name(str(quest_id)), str(quest_def.get("title", quest_id))]
		quest_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		quest_label.custom_minimum_size = Vector2(260, 0)
		info_box.add_child(quest_label)
	var quest_button := Button.new()
	quest_button.text = "Open this region's quest journal"
	UITheme.apply_button(quest_button, 13)
	quest_button.custom_minimum_size = Vector2(260, 34)
	quest_button.pressed.connect(_open_region_quest_log)
	info_box.add_child(quest_button)


func _select_local_map(map_id: String) -> void:
	selected_map_id = map_id
	_refresh_info()
	canvas.queue_redraw()
	Audio.ui_click()


func _open_region_quest_log() -> void:
	var quest_screen := UI.screen("quests")
	if quest_screen != null and quest_screen.has_method("request_region"):
		quest_screen.request_region(selected_region)
	UI.open("quests")


func _landmark_count(region: String) -> int:
	var count := 0
	for entry in World.all_landmarks(region):
		if entry.get("discovered", false):
			count += 1
	return count


func _on_canvas_input(event: InputEvent) -> void:
	if not (
		event is InputEventMouseButton
		and event.pressed
		and event.button_index == MOUSE_BUTTON_LEFT
	):
		return
	var mouse: Vector2 = event.position
	if view_mode == "regional":
		var draw_size := canvas.size
		if draw_size.x <= 0.0 or draw_size.y <= 0.0:
			draw_size = canvas.custom_minimum_size
		var best_map := ""
		var best_map_dist := 38.0
		for map_value in Data.maps_of(selected_region):
			var map_id := str(map_value)
			var route_entry: Dictionary = Data.route_maps.get(selected_region, {}).get(map_id, {})
			var raw_position: Array = route_entry.get("position", [500, 180])
			var raw_x := float(raw_position[0]) if raw_position.size() > 0 else 500.0
			var raw_y := float(raw_position[1]) if raw_position.size() > 1 else 180.0
			var point := Vector2(55.0 + raw_x / 1000.0 * maxf(300.0, draw_size.x - 110.0),
					76.0 + raw_y / 360.0 * maxf(220.0, draw_size.y - 160.0))
			var distance := mouse.distance_to(point)
			if distance < best_map_dist:
				best_map_dist = distance
				best_map = map_id
		if best_map != "":
			_select_local_map(best_map)
		return
	var best_region := ""
	var best_dist := 120.0
	for region_id in Data.region_order:
		var distance := mouse.distance_to(_region_center(str(region_id)))
		if distance < best_dist:
			best_dist = distance
			best_region = str(region_id)
	if best_region != "":
		_select_region(best_region)


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if (
		event.is_action_pressed("open_map")
		or event.is_action_pressed("pause")
		or event.is_action_pressed("ui_cancel")
	):
		UI.close("worldmap")
		get_viewport().set_input_as_handled()
