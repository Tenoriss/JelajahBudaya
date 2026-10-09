extends MinigameBase
## EXPLORATION: read the clues, then mark where the thing is hidden on the board.
## data: {"clues": ["..."], "answer": [x, y] (0..1 relative), "tolerance": 0.1,
##        "board": "map"|"forest"}

var clues: Array = []
var answer := Vector2(0.5, 0.5)
var tolerance := 0.1
var marks: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	clues = []
	for c in d.get("clues", ["Look near the old tree."]):
		clues.append(str(c))
	var ans: Array = d.get("answer", [0.5, 0.5])
	answer = Vector2(float(ans[0]), float(ans[1]))
	tolerance = float(d.get("tolerance", 0.12))
	marks.clear()
	var y := 10.0
	for c in clues:
		var lbl := make_tile(Vector2(330, 76), Color(0.2, 0.19, 0.24), "• " + str(c), 15)
		lbl.position = Vector2(10, y)
		board.add_child(lbl)
		y += 84.0
	# the search board
	var field := add_button(Vector2(370, 20), Vector2(410, 420), "", _on_board,
			Color(0.18, 0.28, 0.2), 16)
	field.tooltip_text = "Click the spot the clues point to."
	var hint := make_label_center("Click the place on the land where you would search.",
			16, UITheme.COL_TEXT)
	hint.position = Vector2(370, 450)
	hint.custom_minimum_size = Vector2(410, 0)
	board.add_child(hint)
	set_status("Use the clues to work out where to look, then click that spot.")


func _on_board() -> void:
	var field := board.get_child(board.get_child_count() - 1)
	var mouse := board.get_local_mouse_position()
	var rel := Vector2((mouse.x - 370.0) / 410.0, (mouse.y - 20.0) / 420.0)
	var marker := make_tile(Vector2(18, 18), UITheme.COL_GOLD)
	marker.position = Vector2(370 + rel.x * 410 - 9, 20 + rel.y * 420 - 9)
	board.add_child(marker)
	marks.append(rel)
	if rel.distance_to(answer) <= tolerance:
		set_status("You found it!", UITheme.COL_OK)
		win(130)
	else:
		lose("Nothing there. Re-read the clues and search again.")
