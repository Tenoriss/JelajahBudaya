extends Control
## Pause menu: navigation hub for every screen, save/load and settings.

var panel: PanelContainer
var stats_label: Label


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.03, 0.02, 0.04, 0.78)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	panel = UITheme.make_panel(UITheme.PANEL_DARK)
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.position = Vector2(-230, -280)
	panel.custom_minimum_size = Vector2(460, 560)
	add_child(panel)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 7)
	panel.add_child(col)

	var title := Label.new()
	UITheme.apply_label(title, 30, UITheme.COL_GOLD)
	title.text = "Paused"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(title)
	col.add_child(UITheme.hline())

	var entries := [
		["Resume", func(): UI.close("pause")],
		["Quest Journal", func(): UI.open("quests")],
		["Culture Journal", func(): UI.open("journal")],
		["Satchel", func(): UI.open("inventory")],
		["World Map", func(): UI.open("worldmap")],
		["Achievements", func(): UI.open("achievements")],
		["Save / Load", func(): UI.open("savemenu")],
		["Settings", func(): UI.open("settings")],
		["Return to Main Menu", func(): _to_main_menu()],
	]
	for entry in entries:
		var btn := Button.new()
		btn.text = str(entry[0])
		UITheme.apply_button(btn, 20)
		btn.custom_minimum_size = Vector2(400, 0)
		btn.pressed.connect(entry[1])
		col.add_child(btn)

	col.add_child(UITheme.hline())
	stats_label = Label.new()
	UITheme.apply_label(stats_label, 15, UITheme.COL_DIM)
	stats_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	stats_label.custom_minimum_size = Vector2(400, 0)
	col.add_child(stats_label)


func on_open() -> void:
	stats_label.text = _stats_text()


func _stats_text() -> String:
	return ("Play time %s  ·  Chapter %d\nCulture Points %d  ·  Quests %d  ·  Puzzles %d\nJournal %d/%d  ·  Landmarks %d  ·  Steps %d" % [
		Game.play_time_string(), Game.story_chapter, Game.culture_points,
		Game.stats.get("quests_completed", 0), Game.stats.get("puzzles_completed", 0),
		Culture.total_found(), Data.total_culture_entries(),
		Game.landmarks.size(), Game.stats.get("steps_taken", 0)])


func _to_main_menu() -> void:
	Save.save_slot(Save.AUTOSAVE_SLOT, true)
	Audio.stop_all()
	get_tree().paused = false
	Game.started = false
	UI.close_all()
	get_tree().change_scene_to_file("res://scenes/main/main_menu.tscn")


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("pause") or event.is_action_pressed("ui_cancel"):
		UI.close("pause")
		get_viewport().set_input_as_handled()
