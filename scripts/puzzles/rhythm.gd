extends MinigameBase
## RHYTHM: hit the marked beats as the notes reach the line.
## data: {"beats": [1.0, 1.5, 2.0, 3.0, ...] (seconds), "tempo_hint": "..."}

var beats: Array = []
var notes: Array = []
var hit := 0
var missed := 0
var speed := 180.0
var song_time := 0.0
var running := false
var hit_line_x := 150.0
var note_y := 150.0


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	beats = []
	for b in d.get("beats", [1.0, 1.4, 1.8, 2.4, 2.8, 3.4, 3.8, 4.4]):
		beats.append(float(b))
	speed = float(d.get("speed", 180.0))
	notes.clear()
	hit = 0
	missed = 0
	song_time = -1.2            # lead-in
	running = true
	note_y = 150.0
	hit_line_x = 150.0
	# track
	var track := make_tile(Vector2(700, 90), Color(0.16, 0.15, 0.2))
	track.position = Vector2(40, note_y - 24)
	board.add_child(track)
	var line := make_tile(Vector2(8, 120), UITheme.COL_GOLD)
	line.position = Vector2(hit_line_x - 4, note_y - 40)
	board.add_child(line)
	set_status("Press [SPACE] or click when a note crosses the gold line.")


func _process(delta: float) -> void:
	if not running or solved:
		return
	song_time += delta
	# spawn notes
	for b in beats:
		var key := int(b * 1000.0)
		if not puzzle.get("_spawned", {}).has(key) and song_time >= b - 2.2:
			if not puzzle.has("_spawned"):
				puzzle["_spawned"] = {}
			puzzle["_spawned"][key] = true
			var btn := add_button(Vector2(700, note_y + 12), Vector2(30, 30), "", func(): pass,
					UITheme.COL_TEAL, 14)
			btn.disabled = true
			notes.append({"btn": btn, "t": b, "done": false})
	# move notes
	for note in notes:
		if note["done"]:
			continue
		var x: float = (float(note["t"]) - song_time) * speed
		if x < -60.0:
			note["done"] = true
			note["btn"].visible = false
			missed += 1
			set_status("Missed one. Keep the beat!", UITheme.COL_ACCENT)
			continue
		note["btn"].position = Vector2(hit_line_x + x, note_y + 12)
	if song_time > 1.0 and hit + missed >= beats.size():
		_finish()


func _input(event: InputEvent) -> void:
	if not running or solved:
		return
	var pressed := false
	if event.is_action_pressed("interact") or event.is_action_pressed("ui_accept"):
		pressed = true
	if event is InputEventMouseButton and event.pressed:
		pressed = true
	if not pressed:
		return
	# nearest note to the line
	var best: Dictionary = {}
	var best_d := 1e9
	for note in notes:
		if note["done"]:
			continue
		var x: float = (float(note["t"]) - song_time) * speed
		var d := absf(x)
		if d < best_d:
			best_d = d
			best = note
	if best.is_empty() or best_d > 46.0:
		return
	best["done"] = true
	best["btn"].visible = false
	hit += 1
	Audio.tone(mini(5, hit - 1))
	set_status("Nice!  %d / %d" % [hit, beats.size()], UITheme.COL_OK)


func _finish() -> void:
	running = false
	if hit >= int(ceil(beats.size() * 0.6)):
		win(100 + hit * 5)
	else:
		lose("You hit %d of %d notes." % [hit, beats.size()])
		await get_tree().create_timer(1.4).timeout
		if not solved:
			reset_puzzle()
