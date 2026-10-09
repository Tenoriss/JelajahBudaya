extends MinigameBase
## LOGIC: deduction.  Read the clues, then pick the correct answer.
## data: {"clues": ["..."], "options": ["..."], "answer": 2, "explain": "..."}

var options: Array = []
var answer := 0
var done := false


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	options = []
	for o in d.get("options", ["Option A", "Option B", "Option C"]):
		options.append(str(o))
	answer = int(d.get("answer", 0))
	done = false
	var clues: Array = d.get("clues", [])
	var y := 14.0
	for clue in clues:
		var lbl := make_tile(Vector2(700, 46), Color(0.2, 0.18, 0.24), "• " + str(clue), 17)
		lbl.position = Vector2(30, y)
		board.add_child(lbl)
		y += 54.0
	y += 10.0
	for i in range(options.size()):
		var btn := add_button(Vector2(30, y), Vector2(700, 54), str(options[i]),
				_on_option.bind(i), Color(0.24, 0.24, 0.3), 18)
		y += 62.0
	set_status("Read the clues, then choose the answer that fits them all.")


func _on_option(index: int) -> void:
	if done:
		return
	if index == answer:
		done = true
		Audio.chime(3)
		var d: Dictionary = puzzle.get("data", {})
		set_status("Correct!  " + str(d.get("explain", "")), UITheme.COL_OK)
		win(120)
	else:
		lose("One of the clues rules that out.")
