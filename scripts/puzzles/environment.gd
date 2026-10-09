extends MinigameBase
## ENVIRONMENT: rotate channel pieces so water flows from the source to the
## field/garden.  data: {"size": 4, "kind": "water_redirect",
##   "source": [0,0], "target": [3,3], "grid": [[piece types]]}
## Piece types: 0 straight, 1 elbow, plus rotations.

enum { STRAIGHT, ELBOW, TEE }
# connections per rotation: [up, right, down, left]
const SHAPES := {
	0: [[1, 0, 1, 0], [0, 1, 0, 1]],                    # straight: vertical, horizontal
	1: [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]],   # elbow
	2: [[1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]],   # tee
}

var size_n := 4
var kinds: Array = []
var rots: Array = []
var source := Vector2i(0, 0)
var target := Vector2i(3, 3)
var cells: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	size_n = int(d.get("size", 4))
	var grid: Array = d.get("grid", [])
	kinds = []
	rots = []
	for y in range(size_n):
		for x in range(size_n):
			if grid.size() > y and (grid[y] as Array).size() > x:
				var piece: Array = grid[y][x]
				kinds.append(int(piece[0]))
				rots.append(int(piece[1]))
			else:
				kinds.append(STRAIGHT)
				rots.append(0)
	var s: Array = d.get("source", [0, 0])
	var t: Array = d.get("target", [size_n - 1, size_n - 1])
	source = Vector2i(int(s[0]), int(s[1]))
	target = Vector2i(int(t[0]), int(t[1]))
	cells.clear()
	_render()


func _render() -> void:
	for child in board.get_children():
		child.queue_free()
	cells.clear()
	var cell := 96.0
	var gap := 8.0
	var total := size_n * cell + (size_n - 1) * gap
	var start := Vector2((board.custom_minimum_size.x - total) * 0.5, 20)
	var flow := _flow()
	for y in range(size_n):
		for x in range(size_n):
			var idx := y * size_n + x
			var label := _glyph(int(kinds[idx]), int(rots[idx]))
			var colour := Color(0.22, 0.3, 0.24)
			if flow.has(Vector2i(x, y)):
				colour = Color(0.2, 0.42, 0.55)
			if Vector2i(x, y) == source:
				colour = Color(0.35, 0.5, 0.3)
			if Vector2i(x, y) == target:
				colour = Color(0.45, 0.38, 0.24)
			var btn := add_button(start + Vector2(x * (cell + gap), y * (cell + gap)),
					Vector2(cell, cell), label, _on_tile.bind(idx), colour, 30)
			cells.append(btn)
	var lbl := make_label_center("Water must reach the marked plot (bottom right).",
			17, UITheme.COL_TEXT)
	lbl.position = Vector2(start.x, start.y + total + 14)
	lbl.custom_minimum_size = Vector2(total, 0)
	board.add_child(lbl)
	set_status("Click a channel to rotate it. Water flows from the spring.")


func _glyph(kind: int, rot: int) -> String:
	if kind == STRAIGHT:
		return "|" if rot % 2 == 0 else "-"
	if kind == ELBOW:
		return ["r", "n", "l", "u"][rot % 4]
	return "+"


func _connections(x: int, y: int) -> Array:
	var idx := y * size_n + x
	var kind := int(kinds[idx])
	var rot := int(rots[idx]) % 4
	if kind == STRAIGHT:
		return SHAPES[0][rot % 2]
	return SHAPES[kind][rot]


func _flow() -> Dictionary:
	## flood fill of water from the source through matching connections
	var out: Dictionary = {}
	var queue: Array = [source]
	out[source] = true
	var dirs := [Vector2i(0, -1), Vector2i(1, 0), Vector2i(0, 1), Vector2i(-1, 0)]
	while queue.size() > 0:
		var cur: Vector2i = queue.pop_front()
		var conn := _connections(cur.x, cur.y)
		for d in range(4):
			if not bool(conn[d]):
				continue
			var nxt: Vector2i = cur + dirs[d]
			if nxt.x < 0 or nxt.y < 0 or nxt.x >= size_n or nxt.y >= size_n:
				continue
			if out.has(nxt):
				continue
			var opposite := (d + 2) % 4
			var nconn := _connections(nxt.x, nxt.y)
			if bool(nconn[opposite]):
				out[nxt] = true
				queue.append(nxt)
	return out


func _on_tile(index: int) -> void:
	rots[index] = (int(rots[index]) + 1) % 4
	Audio.sfx("water_splash", -12.0)
	_render()
	var flow := _flow()
	if flow.has(target):
		set_status("The water reaches the plot!", UITheme.COL_OK)
		win(130)
