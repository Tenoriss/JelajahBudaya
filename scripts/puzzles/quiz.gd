extends MinigameBase
## QUIZ: questions drawn from cultural information the player has met.
## data: {"questions": [{"q": "...", "options": [...], "answer": 1, "fact": "..."}]}

var questions: Array = []
var index := 0
var score := 0


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	questions = d.get("questions", [])
	if questions.is_empty():
		questions = [{"q": "Which region is Rumah Gadang from?", "options": ["West Sumatra", "Papua", "Java"], "answer": 0}]
	index = 0
	score = 0
	_ask()


func _ask() -> void:
	for child in board.get_children():
		child.queue_free()
	if index >= questions.size():
		win(100 + score * 10)
		return
	var q: Dictionary = questions[index]
	var qlabel := make_tile(Vector2(700, 90), Color(0.22, 0.2, 0.28), str(q.get("q", "")), 20)
	qlabel.position = Vector2(30, 10)
	board.add_child(qlabel)
	var opts: Array = q.get("options", [])
	var y := 120.0
	for i in range(opts.size()):
		var btn := add_button(Vector2(30, y), Vector2(700, 56), str(opts[i]),
				_on_answer.bind(i), Color(0.24, 0.24, 0.3), 18)
		y += 64.0
	set_status("Question %d of %d" % [index + 1, questions.size()])


func _on_answer(choice: int) -> void:
	var q: Dictionary = questions[index]
	if choice == int(q.get("answer", 0)):
		score += 1
		Audio.collect()
		set_status("Correct!  " + str(q.get("fact", "")), UITheme.COL_OK)
	else:
		Audio.puzzle_wrong()
		set_status("Not this time.  " + str(q.get("fact", "")) + "  You can retry the quiz.", UITheme.COL_ACCENT)
		await get_tree().create_timer(0.6).timeout
		index = 0
		score = 0
		_ask()
		return
	index += 1
	await get_tree().create_timer(0.8).timeout
	_ask()
