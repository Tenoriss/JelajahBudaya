extends MinigameBase
## FESTIVAL: a timing game - stop the moving marker inside the target band,
## three times, with the band moving faster each round.
## data: {"rounds": 3, "width": 90, "speed": 320, "themes": ["..."]}

var rounds := 3
var round_index := 0
var width := 90.0
var speed := 320.0
var pos := 0.0
var dir := 1.0
var band_pos := 0.3
var marker: Control
var band: Control
var track_width := 700.0
var busy := false


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	rounds = int(d.get("rounds", 3))
	width = float(d.get("width", 90.0))
	speed = float(d.get("speed", 320.0))
	round_index = 0
	pos = 0.0
	dir = 1.0
	busy = false
	_build_round()


func _build_round() -> void:
	for child in board.get_children():
		child.queue_free()
	var track := make_tile(Vector2(track_width, 52), Color(0.18, 0.16, 0.22))
	track.position = Vector2(30, 120)
	board.add_child(track)
	band_pos = randf_range(0.1, 0.8)
	band = make_tile(Vector2(width, 52), UITheme.COL_GOLD)
	band.position = Vector2(30 + track_width * band_pos, 120)
	board.add_child(band)
	marker = make_tile(Vector2(12, 66), Color(0.95, 0.8, 0.5))
	marker.position = Vector2(30, 113)
	board.add_child(marker)
	var theme := "the crowd is watching!"
	var themes: Array = puzzle.get("data", {}).get("themes", [])
	if themes.size() > round_index:
		theme = str(themes[round_index])
	var lbl := make_label_center("Round %d of %d  ·  %s" % [round_index + 1, rounds, theme],
			20, UITheme.COL_GOLD)
	lbl.position = Vector2(30, 40)
	lbl.custom_minimum_size = Vector2(track_width, 0)
	board.add_child(lbl)
	set_status("Press [SPACE] (or click) when the marker is inside the golden band.")


func _process(delta: float) -> void:
	if busy or solved or marker == null:
		return
	pos += dir * (speed + round_index * 60.0) * delta / track_width
	if pos > 1.0:
		pos = 1.0
		dir = -1.0
	elif pos < 0.0:
		pos = 0.0
		dir = 1.0
	marker.position = Vector2(30 + track_width * pos, 113)


func _input(event: InputEvent) -> void:
	if busy or solved:
		return
	var pressed := event.is_action_pressed("interact") or event.is_action_pressed("ui_accept")
	if event is InputEventMouseButton and event.pressed:
		pressed = true
	if not pressed:
		return
	if pos >= band_pos and pos <= band_pos + width / track_width:
		round_index += 1
		Audio.tone(mini(5, round_index))
		if round_index >= rounds:
			win(150)
		else:
			_build_round()
	else:
		Audio.puzzle_wrong()
		round_index = maxi(0, round_index - 1)
		busy = true
		set_status("Off the beat! The festival crowd gives you another chance...", UITheme.COL_ACCENT)
		await get_tree().create_timer(0.8).timeout
		busy = false
		_build_round()
