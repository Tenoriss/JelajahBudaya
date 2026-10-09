extends Control
## HUD: region banner, culture points, active quest tracker, mini-map,
## interaction prompt and day/night indicator.

var prompt_label: Label
var region_label: Label
var cp_label: Label
var quest_note_panel: PanelContainer
var quest_box: VBoxContainer
var quest_title: RichTextLabel
var quest_objective: RichTextLabel
var time_label: Label
var minimap: Control
var hint_label: Label
var _map_def: Dictionary = {}
var _map_node: Node = null
var _completed_note_id := ""
var _refresh_timer := 0.0


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

	# ---- top left: player / region / points --------------------------
	var top_left := VBoxContainer.new()
	top_left.position = Vector2(14, 10)
	top_left.add_theme_constant_override("separation", 2)
	add_child(top_left)

	var region_panel := UITheme.make_panel(UITheme.PANEL_SOFT)
	region_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top_left.add_child(region_panel)
	var rv := VBoxContainer.new()
	region_panel.add_child(rv)
	region_label = Label.new()
	UITheme.apply_label(region_label, 20, UITheme.COL_GOLD)
	rv.add_child(region_label)
	time_label = Label.new()
	UITheme.apply_label(time_label, 14, UITheme.COL_DIM)
	rv.add_child(time_label)

	var cp_row := HBoxContainer.new()
	cp_row.add_theme_constant_override("separation", 6)
	top_left.add_child(cp_row)
	var cp_icon := TextureRect.new()
	cp_icon.texture = UITheme.icon("coin")
	cp_icon.custom_minimum_size = Vector2(22, 22)
	cp_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	cp_row.add_child(cp_icon)
	cp_label = Label.new()
	UITheme.apply_label(cp_label, 18, UITheme.COL_GOLD)
	cp_row.add_child(cp_label)

	# ---- top right: mini map ----------------------------------------
	minimap = Control.new()
	minimap.name = "MiniMap"
	minimap.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	minimap.position = Vector2(-176, 12)
	minimap.custom_minimum_size = Vector2(164, 164)
	minimap.mouse_filter = Control.MOUSE_FILTER_IGNORE
	minimap.draw.connect(_draw_minimap)
	add_child(minimap)

	var map_hint := Label.new()
	UITheme.apply_label(map_hint, 12, UITheme.COL_DIM)
	map_hint.text = "[M] map   [J] journal   [I] bag"
	map_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	map_hint.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	map_hint.position = Vector2(-280, 180)
	map_hint.custom_minimum_size = Vector2(268, 0)
	add_child(map_hint)

	# ---- bottom: interaction prompt ---------------------------------
	var prompt_panel := UITheme.make_panel(UITheme.PANEL_SOFT)
	prompt_panel.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	prompt_panel.position = Vector2(-150, -118)
	prompt_panel.custom_minimum_size = Vector2(300, 0)
	prompt_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(prompt_panel)
	prompt_label = Label.new()
	UITheme.apply_label(prompt_label, 18, UITheme.COL_TEXT)
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.custom_minimum_size = Vector2(282, 0)
	prompt_panel.add_child(prompt_label)

	# ---- top left: compact quest-only note -----------------------------
	quest_note_panel = UITheme.make_panel(UITheme.PANEL_PARCHMENT)
	quest_note_panel.position = Vector2(14, 98)
	quest_note_panel.custom_minimum_size = Vector2(200, 0)
	quest_note_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(quest_note_panel)
	quest_box = VBoxContainer.new()
	quest_box.add_theme_constant_override("separation", 2)
	quest_note_panel.add_child(quest_box)
	quest_title = RichTextLabel.new()
	quest_title.fit_content = true
	quest_title.scroll_active = false
	quest_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	quest_title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	quest_title.custom_minimum_size = Vector2(168, 0)
	quest_title.add_theme_font_size_override("normal_font_size", 12)
	quest_title.add_theme_color_override("default_color", Color(0.18, 0.22, 0.18))
	quest_box.add_child(quest_title)
	quest_objective = RichTextLabel.new()
	quest_objective.fit_content = true
	quest_objective.scroll_active = false
	quest_objective.mouse_filter = Control.MOUSE_FILTER_IGNORE
	quest_objective.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	quest_objective.custom_minimum_size = Vector2(168, 0)
	quest_objective.add_theme_font_size_override("normal_font_size", 9)
	quest_objective.add_theme_color_override("default_color", Color(0.29, 0.31, 0.27))
	quest_box.add_child(quest_objective)

	hint_label = Label.new()
	UITheme.apply_label(hint_label, 14, UITheme.COL_TEAL)
	hint_label.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	hint_label.position = Vector2(-320, -74)
	hint_label.custom_minimum_size = Vector2(300, 0)
	hint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	add_child(hint_label)

	Game.culture_points_changed.connect(func(_v): _refresh_top())
	Game.state_changed.connect(_on_game_state)
	Quest.tracked_changed.connect(_on_tracked_quest_changed)
	Quest.quest_state_changed.connect(_on_quest_state_changed)
	Quest.quest_completed.connect(_on_quest_completed)
	Quest.objective_updated.connect(func(_q, _o): _refresh_quest())
	Settings.changed.connect(func(): _refresh_quest())
	_notify_ready()


func _notify_ready() -> void:
	_refresh_top()
	_refresh_quest()


func on_map_loaded(map_def: Dictionary) -> void:
	_map_def = map_def
	_map_node = UI.world
	var region := Data.get_region(str(map_def.get("region", "")))
	var rname := str(region.get("name", str(map_def.get("region", "")).capitalize()))
	region_label.text = "%s  ·  %s" % [rname, str(map_def.get("name", ""))]
	_refresh_top()
	_refresh_quest()


func _on_game_state(kind: String, _data: Dictionary) -> void:
	match kind:
		"cp":
			_refresh_top()
		"quest_started", "quest_completed", "region_unlocked", "map_loaded", "quest_available":
			_refresh_quest()
		"time_of_day":
			_refresh_top()


func _process(delta: float) -> void:
	_refresh_timer -= delta
	if _refresh_timer <= 0.0:
		_refresh_timer = 0.5
		time_label.text = "%s  %s" % [World.time_string(), World.time_name()]
		if minimap != null:
			minimap.queue_redraw()


func _refresh_top() -> void:
	cp_label.text = "%d  Culture Points" % Game.culture_points
	var region := Data.get_region(Game.current_region)
	if region.size() > 0 and region_label.text == "":
		region_label.text = str(region.get("name", ""))


func set_prompt(text: String) -> void:
	if prompt_label == null:
		return
	if text == "":
		prompt_label.text = ""
	else:
		prompt_label.text = "[E]  %s" % text
	var panel := prompt_label.get_parent() as Control
	if panel:
		panel.visible = text != ""


func _on_tracked_quest_changed(quest_id: String) -> void:
	if quest_id != "" and quest_id != _completed_note_id:
		if str(Data.get_quest(quest_id).get("region", "")) == Game.current_region:
			_completed_note_id = ""
	_refresh_quest()


func _on_quest_state_changed(quest_id: String, state_name: String) -> void:
	if state_name == "Active" and quest_id != _completed_note_id:
		var def := Data.get_quest(quest_id)
		if str(def.get("region", "")) == Game.current_region:
			_completed_note_id = ""
	_refresh_quest()


func _on_quest_completed(quest_id: String) -> void:
	var def := Data.get_quest(quest_id)
	if str(def.get("region", "")) == Game.current_region:
		_completed_note_id = quest_id
		_refresh_quest()


func _regional_quest_id() -> String:
	var region_id := Game.current_region
	if region_id == "" and not _map_def.is_empty():
		region_id = str(_map_def.get("region", "prologue"))
	var quest_ids := Data.get_quests_in_region(region_id)
	quest_ids.sort_custom(func(a, b):
		var chapter_a := int(Data.get_quest(str(a)).get("chapter", 0))
		var chapter_b := int(Data.get_quest(str(b)).get("chapter", 0))
		return chapter_a < chapter_b if chapter_a != chapter_b else str(a) < str(b))
	if quest_ids.is_empty():
		return ""
	var show_completed_note := _completed_note_id != "" and quest_ids.has(_completed_note_id)
	if show_completed_note and Quest.is_completed(_completed_note_id):
		return _completed_note_id
	var tracked_id := Quest.tracked_quest()
	if tracked_id != "" and str(Data.get_quest(tracked_id).get("region", "")) == region_id:
		return tracked_id
	for desired_state in ["Active", "Available", "Locked"]:
		for quest_id in quest_ids:
			if Quest.state_name(str(quest_id)) == desired_state:
				return str(quest_id)
	for index in range(quest_ids.size() - 1, -1, -1):
		var quest_id := str(quest_ids[index])
		if Quest.state_name(quest_id) == "Completed":
			return quest_id
	return ""


func _set_note_text(label: RichTextLabel, value: String, crossed_out: bool) -> void:
	label.clear()
	if crossed_out:
		label.push_strikethrough()
	label.add_text(value)
	if crossed_out:
		label.pop()


func _localized_quest_field(def: Dictionary, field: String) -> String:
	var key := field + "_id" if Settings.language.begins_with("id") else field
	return str(def.get(key, def.get(field, "")))


func _quest_note_objective(quest_id: String, def: Dictionary, state_name: String) -> String:
	var indonesian := Settings.language.begins_with("id")
	var note_text := ""
	match state_name:
		"Completed":
			note_text = "Misi selesai" if indonesian else "Quest completed"
		"Available":
			var start: Dictionary = def.get("start", {})
			var start_npc_id := str(start.get("npc", def.get("giver", "")))
			var start_npc_name := str(Data.get_npc(start_npc_id).get("name", "the local guide"))
			var start_action := "Bicara dengan %s untuk memulai" if indonesian else "Talk to %s to begin"
			note_text = start_action % start_npc_name
		"Active":
			var found_objective := false
			for objective in def.get("objectives", []):
				if bool(objective.get("hidden", false)):
					continue
				var objective_id := str(objective.get("id", ""))
				var needed := int(objective.get("count", 1))
				if Quest.objective_progress(quest_id, objective_id) < needed:
					var field := "text_id" if indonesian else "text"
					note_text = str(objective.get(field, objective.get("text", "Continue the quest.")))
					found_objective = true
					break
			if not found_objective:
				var complete: Dictionary = def.get("complete", {})
				var return_npc_id := str(complete.get("npc", def.get("giver", "")))
				var return_npc_name := str(Data.get_npc(return_npc_id).get("name", "the quest giver"))
				var report_action := "Kembali bicara dengan %s" if indonesian else "Report back to %s"
				note_text = report_action % return_npc_name
		_:
			var requirements: Dictionary = def.get("requires", {})
			var prerequisite_quests: Array = requirements.get("quests", [])
			if not prerequisite_quests.is_empty():
				var previous := Data.get_quest(str(prerequisite_quests[0]))
				var previous_title := _localized_quest_field(previous, "title")
				var prerequisite_action := "Complete %s first"
				if indonesian:
					prerequisite_action = "Selesaikan %s terlebih dahulu"
				note_text = prerequisite_action % previous_title
			elif indonesian:
				note_text = "Selesaikan misi sebelumnya terlebih dahulu"
			else:
				note_text = "Complete earlier quests to unlock this one"
	return note_text


func _refresh_quest() -> void:
	var qid := _regional_quest_id()
	if qid == "":
		quest_note_panel.visible = false
		_set_note_text(quest_title, "", false)
		_set_note_text(quest_objective, "", false)
		hint_label.text = ""
		return
	var def := Data.get_quest(qid)
	var quest_state := Quest.state_name(qid)
	var is_completed := quest_state == "Completed"
	quest_note_panel.visible = true
	_set_note_text(quest_title, _localized_quest_field(def, "title"), is_completed)
	_set_note_text(quest_objective, _quest_note_objective(qid, def, quest_state), is_completed)
	hint_label.text = str(def.get("hint_short", "")) if quest_state == "Active" else ""


static func _draw_map_icon(_canvas: Control, _pos: Vector2, _kind: String) -> void:
	pass


func _draw_minimap() -> void:
	if not Settings.minimap_enabled or _map_node == null or not is_instance_valid(_map_node):
		return
	var size := minimap.custom_minimum_size
	var rect := Rect2(Vector2.ZERO, size)
	# frame
	minimap.draw_rect(Rect2(Vector2.ZERO, size), Color(0.1, 0.08, 0.11, 0.75), true)
	minimap.draw_rect(Rect2(Vector2.ZERO, size), UITheme.COL_GOLD, false, 2.0)
	var inner := Rect2(4, 4, size.x - 8, size.y - 8)
	var bounds: Vector2 = _map_node.bounds if "bounds" in _map_node else Vector2(1600, 1200)
	var scale := Vector2(inner.size.x / bounds.x, inner.size.y / bounds.y)
	var ground = _map_node.ground
	if ground != null:
		# draw a coarse version of the terrain
		var used: Array = ground.get_used_cells()
		var tiles: Dictionary = Data.tilesets.get(str(_map_node.region), {}).get("tiles", {})
		var step := 2
		for cell in used:
			if cell.x % step != 0 or cell.y % step != 0:
				continue
			var atlas: Vector2i = ground.get_cell_atlas_coords(cell)
			var col := Color(0.3, 0.45, 0.3)
			for tile_name in tiles.keys():
				var at: Array = tiles[tile_name]["atlas"]
				if int(at[0]) == atlas.x and int(at[1]) == atlas.y:
					var n := str(tile_name)
					if n.begins_with("water") or n.begins_with("deep"):
						col = Color(0.24, 0.42, 0.6)
					elif n.begins_with("sand"):
						col = Color(0.72, 0.65, 0.45)
					elif n.begins_with("path") or n.begins_with("dirt"):
						col = Color(0.55, 0.45, 0.32)
					elif n.begins_with("grass") or n.begins_with("rice") or n.begins_with("farm"):
						col = Color(0.34, 0.5, 0.3)
					elif n.begins_with("jungle") or n.begins_with("tall"):
						col = Color(0.22, 0.38, 0.24)
					elif (n.begins_with("plank") or n.begins_with("stone")
						or n.begins_with("temple") or n.begins_with("paving")):
						col = Color(0.5, 0.48, 0.45)
					break
			var p := inner.position + Vector2(cell.x * 32, cell.y * 32) * scale
			minimap.draw_rect(Rect2(p, Vector2(32, 32) * scale * step + Vector2(1, 1)), col, true)
	# landmarks
	for lm in _map_def.get("landmarks", []):
		var p := Vector2(float(lm["pos"][0]) * 32, float(lm["pos"][1]) * 32) * scale + inner.position
		var discovered: bool = Game.landmarks.has(str(lm.get("id", "")))
		minimap.draw_circle(p, 3.5, UITheme.COL_GOLD if discovered else Color(0.5, 0.45, 0.4))
	# NPCs
	for npc in _map_node.entities.get_children():
		if npc.is_in_group("npc"):
			var p := npc.position * scale + inner.position
			minimap.draw_circle(p, 2.0, Color(0.4, 0.9, 0.6, 0.9))
	# player
	var player = _map_node.player
	if player != null and is_instance_valid(player):
		var p: Vector2 = player.position * scale + inner.position
		minimap.draw_circle(p, 3.2, Color(1.0, 0.95, 0.8))
		minimap.draw_circle(p, 5.0, Color(1.0, 0.9, 0.6, 0.35))
