extends MinigameBase
## MEMORY: flip cards to find matching pairs of cultural items.
## data: {"pairs": [["A","B"], ...]}  -- each inner list is the two card labels,
## or {"symbols": ["A","B","C","D"]} to match identical symbols.

var cards: Array = []
var flipped: Array = []
var matched := 0
var busy := false
var symbols: Array = []


func _build() -> void:
	cards.clear()
	flipped.clear()
	matched = 0
	busy = false
	symbols = []
	var d: Dictionary = puzzle.get("data", {})
	if d.has("pairs"):
		for pair in d["pairs"]:
			symbols.append(str(pair[0]))
			symbols.append(str(pair[1]))
	else:
		var base: Array = d.get("symbols", ["Rumah Gadang", "Ulos", "Gamelan", "Batik",
				"Rumah Panjang", "Tongkonan", "Honai", "Sasando"])
		for s in base:
			symbols.append(str(s))
			symbols.append(str(s))
	symbols.shuffle()
	var cols := int(d.get("columns", 4))
	var cell := float(d.get("cell", 150))
	var gap := 16.0
	var total_w := cols * cell + (cols - 1) * gap
	var start_x := (board.custom_minimum_size.x - total_w) * 0.5
	for i in range(symbols.size()):
		var row := i / cols
		var col := i % cols
		var pos := Vector2(start_x + col * (cell + gap), 40 + row * (cell * 0.62 + gap))
		var btn := add_button(pos, Vector2(cell, cell * 0.62), "?", _on_card.bind(i), Color(0.26, 0.2, 0.3), 22)
		cards.append({"btn": btn, "symbol": symbols[i], "face_up": false})
	set_status("Find every matching pair.  %d pairs." % (symbols.size() / 2))


func _on_card(index: int) -> void:
	if busy or index >= cards.size():
		return
	var card: Dictionary = cards[index]
	if card["face_up"]:
		return
	_flip(index, true)
	flipped.append(index)
	Audio.chime(1)
	if flipped.size() < 2:
		return
	busy = true
	await get_tree().create_timer(0.45).timeout
	var a: Dictionary = cards[flipped[0]]
	var b: Dictionary = cards[flipped[1]]
	if a["symbol"] == b["symbol"]:
		matched += 1
		Audio.collect()
		for idx in flipped:
			var btn: Button = cards[idx]["btn"]
			paint(btn, Color(0.22, 0.38, 0.26))
			btn.disabled = true
		flipped.clear()
		busy = false
		set_status("Matched!  %d of %d pairs." % [matched, symbols.size() / 2])
		if matched >= symbols.size() / 2:
			win(120)
	else:
		for idx in flipped:
			_flip(idx, false)
		flipped.clear()
		busy = false
		set_status("Not a pair. Keep looking.", UITheme.COL_ACCENT)


func _flip(index: int, face_up: bool) -> void:
	var card: Dictionary = cards[index]
	var btn: Button = card["btn"]
	card["face_up"] = face_up
	if face_up:
		btn.text = str(card["symbol"])
		paint(btn, Color(0.36, 0.28, 0.2))
	else:
		btn.text = "?"
		paint(btn, Color(0.26, 0.2, 0.3))
