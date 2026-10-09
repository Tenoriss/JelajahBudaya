extends MinigameBase
## TILE: rotate stone/wood pieces so every edge lines up (pattern reconstruction).
## data: {"size": 3, "start": [[0,1,...]] , "goal": [[...]]}  -- directions 0..3

var size_n := 3
var rot: Array = []
var goal: Array = []
var cells: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	size_n = int(d.get("size", 3))
	rot = []
	goal = []
	for y in range(size_n):
		var row_start: Array = d.get("start", [])
		var row_goal: Array = d.get("goal", [])
		for x in range(size_n):
			rot.append(int(row_start[y][x]) if row_start.size() > y else 0)
			goal.append(int(row_goal[y][x]) if row_goal.size() > y else 0)
	if goal.is_empty() or goal.size() == 0:
		goal = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	cells.clear()
	set_status("Click a piece to rotate it until every piece faces as it should.")
	_render()


func _render() -> void:
	for child in board.get_children():
		child.queue_free()
	cells.clear()
	var cell := 120.0
	var gap := 14.0
	var total := size_n * cell + (size_n - 1) * gap
	var start := Vector2((board.custom_minimum_size.x - total) * 0.5, 50)
	for y in range(size_n):
		for x in range(size_n):
			var idx := y * size_n + x
			var pos := start + Vector2(x * (cell + gap), y * (cell + gap))
			var arrow := ["^", ">", "v", "<"][int(rot[idx]) % 4]
			var matched := int(rot[idx]) % 4 == int(goal[idx]) % 4
			var colour := Color(0.24, 0.34, 0.26) if matched else Color(0.32, 0.26, 0.22)
			var btn := add_button(pos, Vector2(cell, cell), arrow, _on_tile.bind(idx), colour, 44)
			cells.append(btn)
	var aligned := 0
	for i in range(rot.size()):
		if int(rot[i]) % 4 == int(goal[i]) % 4:
			aligned += 1
	set_status("%d of %d pieces aligned." % [aligned, rot.size()])


func _on_tile(index: int) -> void:
	rot[index] = (int(rot[index]) + 1) % 4
	Audio.impact("wood")
	_render()
	var aligned := 0
	for i in range(rot.size()):
		if int(rot[i]) % 4 == int(goal[i]) % 4:
			aligned += 1
	if aligned >= rot.size():
		win(110)
