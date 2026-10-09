extends MinigameBase
## PATTERN: watch a pattern light up, then reproduce it.
## data: {"size": 4, "pattern": [0,5,6,10], "preview_time": 2.2}

var size_n := 4
var target: Array = []
var selected: Array = []
var cells: Array = []
var showing := true
var preview_time := 2.2


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	size_n = int(d.get("size", 4))
	target = []
	for v in d.get("pattern", [0, 5, 6, 10]):
		target.append(int(v))
	preview_time = float(d.get("preview_time", 2.2))
	selected.clear()
	cells.clear()
	showing = true
	var cell := float(d.get("cell", 90))
	var gap := 10.0
	var total := size_n * cell + (size_n - 1) * gap
	var start := Vector2((board.custom_minimum_size.x - total) * 0.5, 40)
	for y in range(size_n):
		for x in range(size_n):
			var idx := y * size_n + x
			var pos := start + Vector2(x * (cell + gap), y * (cell + gap))
			var btn := add_button(pos, Vector2(cell, cell), "", _on_cell.bind(idx), Color(0.22, 0.19, 0.26))
			cells.append(btn)
	set_status("Memorise the pattern...")
	_show_pattern()


func _show_pattern() -> void:
	await get_tree().create_timer(preview_time).timeout
	if solved:
		return
	showing = false
	for btn in cells:
		paint(btn, Color(0.22, 0.19, 0.26))
	set_status("Now click the tiles that were lit, in any order.")


func _on_cell(index: int) -> void:
	if showing:
		return
	if selected.has(index):
		return
	selected.append(index)
	Audio.chime(mini(3, selected.size()))
	if not target.has(index):
		lose("That tile was not lit.")
		await get_tree().create_timer(1.1).timeout
		if not solved:
			reset_puzzle()
		return
	paint(cells[index], Color(0.35, 0.55, 0.34))
	set_status("%d of %d tiles found." % [selected.size(), target.size()])
	if selected.size() >= target.size():
		win(110)


func reset_puzzle() -> void:
	super.reset_puzzle()
