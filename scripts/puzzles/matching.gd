extends MinigameBase
## MATCHING: connect each left card with the right one (object -> region,
## instrument -> category, food -> region ...).  data: {"pairs": [[L,R], ...]}

var left_items: Array = []
var right_items: Array = []
var selected_left := -1
var pairs: Dictionary = {}
var solved_pairs := 0
var left_buttons: Array = []
var right_buttons: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	pairs.clear()
	left_items.clear()
	right_items.clear()
	for pair in d.get("pairs", [["Rumah Gadang", "Sumatra"], ["Tongkonan", "Sulawesi"]]):
		left_items.append(str(pair[0]))
		right_items.append(str(pair[1]))
		pairs[str(pair[0])] = str(pair[1])
	solved_pairs = 0
	selected_left = -1
	left_buttons.clear()
	right_buttons.clear()
	right_items.shuffle()
	var y := 30.0
	for i in range(left_items.size()):
		var btn := add_button(Vector2(60, y), Vector2(320, 56), "  " + str(left_items[i]),
				_on_left.bind(i), Color(0.24, 0.22, 0.3), 18)
		left_buttons.append(btn)
		y += 66
	y = 30.0
	for j in range(right_items.size()):
		var btn2 := add_button(Vector2(430, y), Vector2(300, 56), "  " + str(right_items[j]),
				_on_right.bind(j), Color(0.22, 0.27, 0.3), 18)
		right_buttons.append(btn2)
		y += 66
	set_status("Pick a card on the left, then its match on the right.")


func _on_left(index: int) -> void:
	selected_left = index
	for i in range(left_buttons.size()):
		paint(left_buttons[i], Color(0.4, 0.34, 0.2) if i == index else Color(0.24, 0.22, 0.3))
	Audio.ui_hover()


func _on_right(index: int) -> void:
	if selected_left < 0:
		set_status("Choose a card on the left first.", UITheme.COL_ACCENT)
		return
	var left_name := str(left_items[selected_left])
	var right_name := str(right_items[index])
	if pairs.get(left_name, "") == right_name:
		solved_pairs += 1
		paint(left_buttons[selected_left], Color(0.22, 0.38, 0.26))
		paint(right_buttons[index], Color(0.22, 0.38, 0.26))
		left_buttons[selected_left].disabled = true
		right_buttons[index].disabled = true
		selected_left = -1
		Audio.collect()
		set_status("Matched!  %d / %d" % [solved_pairs, left_items.size()])
		if solved_pairs >= left_items.size():
			win(115)
	else:
		Audio.puzzle_wrong()
		paint(right_buttons[index], Color(0.42, 0.22, 0.22))
		set_status("That is not the match for “%s”." % left_name, UITheme.COL_ACCENT)
		await get_tree().create_timer(0.7).timeout
		if is_instance_valid(right_buttons[index]):
			paint(right_buttons[index], Color(0.22, 0.27, 0.3))
