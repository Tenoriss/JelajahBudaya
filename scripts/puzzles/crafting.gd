extends MinigameBase
## CRAFTING: choose the right materials, then lay out an abstract motif pattern
## on the weaving/plaiting grid to match the target.
## data: {"materials": [...], "wrong": [...], "size": 5, "target": [cells]}

var stage := 0
var materials: Array = []
var wrong: Array = []
var chosen: Array = []
var size_n := 5
var target: Array = []
var grid: Array = []
var cells: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	materials = []
	for m in d.get("materials", ["Cotton", "Natural dye", "Loom"]):
		materials.append(str(m))
	wrong = []
	for m in d.get("wrong", ["Plastic sheet"]):
		wrong.append(str(m))
	size_n = int(d.get("size", 5))
	target = []
	for v in d.get("target", []):
		target.append(int(v))
	if target.is_empty():
		for y in range(size_n):
			for x in range(size_n):
				target.append(1 if (x + y) % 3 == 0 else 0)
	grid = []
	for i in range(size_n * size_n):
		grid.append(0)
	chosen.clear()
	cells.clear()
	stage = 0
	_render()


func _render() -> void:
	for child in board.get_children():
		child.queue_free()
	cells.clear()
	match stage:
		0:
			set_status("Stage 1 - gather only the materials this craft needs.")
			var all: Array = materials.duplicate()
			for w in wrong:
				all.append(str(w))
			all.shuffle()
			var x := 30.0
			var y := 20.0
			for i in range(all.size()):
				if i % 3 == 0 and i > 0:
					x = 30.0
					y += 70.0
				var name := str(all[i])
				var picked := chosen.has(name)
				var btn := add_button(Vector2(x, y), Vector2(220, 58), name,
						_on_material.bind(name), Color(0.26, 0.32, 0.24) if picked else Color(0.26, 0.22, 0.26), 18)
				x += 236.0
			add_button(Vector2(30, y + 84), Vector2(240, 54), "Start weaving", _confirm_materials,
					Color(0.3, 0.26, 0.36), 19)
		1:
			set_status("Stage 2 - click the grid to copy the pattern shown on the right.")
			var cell := 76.0
			var gap := 8.0
			var total := size_n * cell + (size_n - 1) * gap
			var start := Vector2((board.custom_minimum_size.x - total) * 0.5 - 120, 40)
			for y in range(size_n):
				for x in range(size_n):
					var idx := y * size_n + x
					var on := int(grid[idx]) == 1
					var btn := add_button(start + Vector2(x * (cell + gap), y * (cell + gap)),
							Vector2(cell, cell), "", _on_cell.bind(idx),
							Color(0.5, 0.36, 0.24) if on else Color(0.2, 0.2, 0.24))
					cells.append(btn)
			# target preview
			var prev_cell := 40.0
			var prev_gap := 5.0
			var prev_start := Vector2(start.x + total + 60, 60)
			var lbl := make_label_center("Target", 16, UITheme.COL_GOLD)
			lbl.position = prev_start + Vector2(-10, -30)
			lbl.custom_minimum_size = Vector2(200, 0)
			board.add_child(lbl)
			for y in range(size_n):
				for x in range(size_n):
					var idx2 := y * size_n + x
					var on2 := int(target[idx2]) == 1
					var tile := make_tile(Vector2(prev_cell, prev_cell),
							Color(0.55, 0.4, 0.26) if on2 else Color(0.22, 0.21, 0.24))
					tile.position = prev_start + Vector2(x * (prev_cell + prev_gap), y * (prev_cell + prev_gap))
					board.add_child(tile)
			add_button(Vector2(30, 470), Vector2(240, 50), "Finish the craft", _confirm_pattern,
					Color(0.3, 0.26, 0.36), 19)


func _on_material(name: String) -> void:
	if chosen.has(name):
		chosen.erase(name)
	else:
		chosen.append(name)
	Audio.ui_hover()
	_render()


func _confirm_materials() -> void:
	for w in wrong:
		if chosen.has(w):
			lose("“%s” is not used for this craft." % w)
			chosen.clear()
			_render()
			return
	for m in materials:
		if not chosen.has(m):
			set_status("Still needed: %s" % m, UITheme.COL_ACCENT)
			return
	stage = 1
	Audio.chime(2)
	_render()


func _on_cell(index: int) -> void:
	grid[index] = 0 if int(grid[index]) == 1 else 1
	Audio.impact("wood")
	_render()


func _confirm_pattern() -> void:
	var matches := true
	for i in range(target.size()):
		if int(target[i]) != int(grid[i]):
			matches = false
			break
	if matches:
		win(150)
	else:
		lose("The motif does not match the reference yet.")
