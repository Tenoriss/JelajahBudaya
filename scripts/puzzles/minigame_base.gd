class_name MinigameBase
extends Control
## Shared chrome and behaviour for every puzzle / mini-game.
##
## Subclasses implement:
##   _build()                      create the board inside `board`
##   _check_success() -> bool      (optional) auto-complete check
## and call `win()` / `lose()`.
##
## Every puzzle always offers: retry (R), hint (H), exit (ESC) - the player can
## never get permanently stuck.

signal finished(success: bool, score: int)
signal hint_requested(level: int)

var puzzle: Dictionary = {}
var puzzle_id := ""
var puzzle_title := ""
var manager: Node = null
var context: Dictionary = {}

var board: Control
var hint_label: Label
var status_label: Label
var hint_level := 0
var attempts := 0
var solved := false
var started_at := 0

const BG := Color(0.08, 0.07, 0.1, 0.92)


func setup(def: Dictionary, mgr: Node, ctx := {}) -> void:
	puzzle = def
	puzzle_id = str(def.get("id", ""))
	puzzle_title = str(def.get("title", "Puzzle"))
	manager = mgr
	context = ctx
	attempts = manager.attempts_of(puzzle_id) if manager != null else 1
	hint_level = manager.hints_used_of(puzzle_id) if manager != null else 0
	started_at = Time.get_ticks_msec()
	_build_chrome()
	_build()
	if has_method("_restore_state"):
		pass


func _build_chrome() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new()
	bg.color = BG
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var header := PanelContainer.new()
	header.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_BANNER, 8))
	header.position = Vector2(240, 18)
	header.custom_minimum_size = Vector2(800, 0)
	add_child(header)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 2)
	header.add_child(col)
	var title := Label.new()
	UITheme.apply_label(title, 26, UITheme.COL_GOLD)
	title.text = puzzle_title
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	col.add_child(title)
	var desc := Label.new()
	UITheme.apply_label(desc, 16, UITheme.COL_PANEL_TEXT)
	desc.text = str(puzzle.get("description", ""))
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc.custom_minimum_size = Vector2(760, 0)
	col.add_child(desc)

	board = Control.new()
	board.position = Vector2(240, 130)
	board.custom_minimum_size = Vector2(800, 470)
	board.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(board)

	status_label = Label.new()
	UITheme.apply_label(status_label, 19, UITheme.COL_TEAL)
	status_label.position = Vector2(244, 606)
	status_label.custom_minimum_size = Vector2(790, 0)
	status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(status_label)

	hint_label = Label.new()
	UITheme.apply_label(hint_label, 18, UITheme.COL_GOLD)
	hint_label.position = Vector2(244, 646)
	hint_label.custom_minimum_size = Vector2(790, 0)
	hint_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(hint_label)

	var buttons := HBoxContainer.new()
	buttons.position = Vector2(244, 682)
	buttons.add_theme_constant_override("separation", 8)
	add_child(buttons)

	var hint_btn := Button.new()
	hint_btn.text = "Hint  [H]"
	UITheme.apply_button(hint_btn, 17)
	hint_btn.pressed.connect(use_hint)
	buttons.add_child(hint_btn)

	var retry := Button.new()
	retry.text = "Reset  [R]"
	UITheme.apply_button(retry, 17)
	retry.pressed.connect(reset_puzzle)
	buttons.add_child(retry)

	var exit_btn := Button.new()
	exit_btn.text = "Leave  [ESC]"
	UITheme.apply_button(exit_btn, 17)
	exit_btn.pressed.connect(func(): manager.close_current())
	buttons.add_child(exit_btn)

	var progress := Label.new()
	UITheme.apply_label(progress, 15, UITheme.COL_DIM)
	progress.text = "Attempt %d" % attempts
	progress.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	progress.position = Vector2(-220, 26)
	progress.custom_minimum_size = Vector2(200, 0)
	progress.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	add_child(progress)

	_show_hints_available()


func _show_hints_available() -> void:
	var hints: Array = puzzle.get("hints", [])
	if hints.is_empty():
		hint_label.text = ""
		return
	if hint_level > 0:
		hint_label.text = "Hint %d: %s" % [hint_level, str(hints[mini(hint_level - 1, hints.size() - 1)])]
	else:
		hint_label.text = "Press [H] if you want a nudge (small Culture Point cost)."


# -------------------------------------------------------------- subclass API
func _build() -> void:
	pass


func win(score := 100) -> void:
	if solved:
		return
	solved = true
	status_label.add_theme_color_override("font_color", UITheme.COL_OK)
	status_label.text = "Well done!"
	Audio.puzzle_solved()
	await get_tree().create_timer(0.55).timeout
	finished.emit(true, score)


func lose(reason := "") -> void:
	if solved:
		return
	status_label.add_theme_color_override("font_color", UITheme.COL_BAD)
	status_label.text = ("Not quite. " + reason + "  Try again - no penalty!") if reason != "" else "Try again!"
	Audio.puzzle_wrong()


func set_status(text: String, colour := UITheme.COL_TEAL) -> void:
	if status_label == null:
		return
	status_label.add_theme_color_override("font_color", colour)
	status_label.text = text


# ---------------------------------------------------------------- hint/retry
func use_hint() -> void:
	var hints: Array = puzzle.get("hints", [])
	if hints.is_empty():
		set_status("This puzzle has no hints - you can always reset it.", UITheme.COL_DIM)
		return
	hint_level = mini(hints.size(), hint_level + 1)
	hint_requested.emit(hint_level - 1)
	hint_label.text = "Hint %d: %s" % [hint_level, str(hints[hint_level - 1])]
	Audio.chime(0)


func reset_puzzle() -> void:
	for child in board.get_children():
		child.queue_free()
	solved = false
	attempts += 1
	set_status("Puzzle reset. Take your time.", UITheme.COL_TEAL)
	_build()


func can_exit() -> bool:
	return true


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_H:
				use_hint()
			KEY_R:
				reset_puzzle()
			KEY_ESCAPE:
				manager.close_current()


# ------------------------------------------------------------------- helpers
## Positioned, clickable tile helper (minigames lay their boards out by hand).
func add_button(pos: Vector2, size: Vector2, text: String, on_press: Callable,
		colour := Color(0.24, 0.19, 0.24), font_size := 20) -> Button:
	var btn := Button.new()
	btn.text = text
	btn.position = pos
	btn.custom_minimum_size = size
	btn.size = size
	var sb := StyleBoxFlat.new()
	sb.bg_color = colour
	sb.border_color = Color(0.14, 0.11, 0.14, 0.9)
	sb.set_border_width_all(2)
	sb.set_corner_radius_all(8)
	sb.set_content_margin_all(6)
	btn.add_theme_stylebox_override("normal", sb)
	var hover := sb.duplicate() as StyleBoxFlat
	hover.bg_color = colour.lightened(0.16)
	btn.add_theme_stylebox_override("hover", hover)
	var pressed := sb.duplicate() as StyleBoxFlat
	pressed.bg_color = colour.darkened(0.18)
	btn.add_theme_stylebox_override("pressed", pressed)
	btn.add_theme_stylebox_override("focus", hover)
	btn.add_theme_font_size_override("font_size", font_size)
	btn.add_theme_color_override("font_color", UITheme.COL_PANEL_TEXT)
	btn.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	btn.pressed.connect(on_press)
	btn.mouse_entered.connect(func(): Audio.ui_hover())
	board.add_child(btn)
	return btn


func paint(btn: Button, colour: Color) -> void:
	var sb := btn.get_theme_stylebox("normal")
	if sb is StyleBoxFlat:
		(sb as StyleBoxFlat).bg_color = colour
		var hover := sb.duplicate() as StyleBoxFlat
		hover.bg_color = colour.lightened(0.16)
		btn.add_theme_stylebox_override("hover", hover)


func make_tile(size: Vector2, colour: Color, text := "", font_size := 20) -> PanelContainer:
	var pc := PanelContainer.new()
	pc.custom_minimum_size = size
	var sb := StyleBoxFlat.new()
	sb.bg_color = colour
	sb.border_color = Color(0.15, 0.12, 0.15, 0.9)
	sb.set_border_width_all(2)
	sb.set_corner_radius_all(8)
	sb.set_content_margin_all(6)
	pc.add_theme_stylebox_override("panel", sb)
	if text != "":
		var lbl := Label.new()
		UITheme.apply_label(lbl, font_size, UITheme.COL_PANEL_TEXT)
		lbl.text = text
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		pc.add_child(lbl)
	return pc


func make_label_center(text: String, size := 18, colour := UITheme.COL_TEXT) -> Label:
	var lbl := Label.new()
	UITheme.apply_label(lbl, size, colour)
	lbl.text = text
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return lbl
