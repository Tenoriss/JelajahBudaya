extends MinigameBase
## COOKING: pick the right ingredients, then the right preparation order, then
## hit the cooking timing.  data: {"ingredients": [...], "bad": [...],
## "steps": [...], "order": [...], "timing": {"width": 120, "speed": 260}}

var stage := 0
var ingredients: Array = []
var bad: Array = []
var chosen: Array = []
var steps: Array = []
var order: Array = []
var step_picked: Array = []
var marker := 0.0
var dir := 1.0
var target_start := 0.4
var target_width := 0.2
var speed := 260.0
var marker_node: Control
var track_node: Control


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	ingredients = _to_str_array(d.get("ingredients", ["Rice", "Coconut", "Spices"]))
	bad = _to_str_array(d.get("bad", ["Chocolate"]))
	steps = _to_str_array(d.get("steps", ["Prepare", "Cook", "Serve"]))
	order = []
	for v in d.get("order", [0, 1, 2]):
		order.append(int(v))
	target_width = float(d.get("timing", {}).get("width", 0.2))
	speed = float(d.get("timing", {}).get("speed", 260.0))
	chosen.clear()
	step_picked.clear()
	stage = 0
	_render()


func _to_str_array(arr: Array) -> Array:
	var out: Array = []
	for v in arr:
		out.append(str(v))
	return out


func _render() -> void:
	for child in board.get_children():
		child.queue_free()
	marker_node = null
	track_node = null
	match stage:
		0:
			set_status("Stage 1 - choose only the ingredients this recipe needs.")
			var all: Array = ingredients.duplicate()
			for b in bad:
				all.append(str(b))
			all.shuffle()
			var x := 30.0
			var y := 20.0
			for i in range(all.size()):
				if i % 3 == 0 and i > 0:
					x = 30.0
					y += 70.0
				var name := str(all[i])
				var is_chosen := chosen.has(name)
				var btn := add_button(Vector2(x, y), Vector2(220, 58), name,
						_on_ingredient.bind(name), Color(0.24, 0.3, 0.24) if is_chosen else Color(0.26, 0.22, 0.26), 18)
				x += 236.0
			var confirm := add_button(Vector2(30, y + 84), Vector2(240, 54), "Start cooking",
					_confirm_ingredients, Color(0.3, 0.26, 0.36), 19)
		1:
			set_status("Stage 2 - click the preparation steps in order.")
			var yy := 20.0
			for i in range(steps.size()):
				var picked := step_picked.has(i)
				var label := "%d. %s" % [step_picked.find(i) + 1, steps[i]] if picked else str(steps[i])
				var btn2 := add_button(Vector2(30, yy), Vector2(680, 54), label,
						_on_step.bind(i), Color(0.22, 0.32, 0.24) if picked else Color(0.26, 0.22, 0.26), 18)
				btn2.disabled = picked
				yy += 62.0
		2:
			set_status("Stage 3 - press [SPACE] when the marker is inside the golden band.")
			track_node = make_tile(Vector2(700, 46), Color(0.18, 0.16, 0.2))
			track_node.position = Vector2(30, 80)
			board.add_child(track_node)
			var band := make_tile(Vector2(700 * target_width, 46), UITheme.COL_GOLD)
			band.position = Vector2(30 + 700 * target_start, 80)
			board.add_child(band)
			marker_node = make_tile(Vector2(10, 60), Color(0.95, 0.75, 0.45))
			marker_node.position = Vector2(30, 73)
			board.add_child(marker_node)
			marker = 0.0
			dir = 1.0


func _on_ingredient(name: String) -> void:
	if chosen.has(name):
		chosen.erase(name)
		Audio.ui_hover()
	else:
		chosen.append(name)
		Audio.ui_click()
	_render()


func _confirm_ingredients() -> void:
	for b in bad:
		if chosen.has(b):
			lose("“%s” does not belong in this recipe." % b)
			chosen.clear()
			_render()
			return
	for needed in ingredients:
		if not chosen.has(needed):
			set_status("You still need: %s" % needed, UITheme.COL_ACCENT)
			return
	stage = 1
	Audio.chime(2)
	_render()


func _on_step(index: int) -> void:
	if step_picked.has(index):
		return
	var expected := order[step_picked.size()] if step_picked.size() < order.size() else -1
	if index != expected:
		lose("That is not the next step.")
		step_picked.clear()
		_render()
		return
	step_picked.append(index)
	Audio.tone(mini(5, step_picked.size() - 1))
	_render()
	if step_picked.size() >= order.size():
		stage = 2
		_render()


func _process(delta: float) -> void:
	if stage != 2 or solved:
		return
	marker += dir * speed * delta / 700.0
	if marker > 1.0:
		marker = 1.0
		dir = -1.0
	elif marker < 0.0:
		marker = 0.0
		dir = 1.0
	if marker_node != null and is_instance_valid(marker_node):
		marker_node.position = Vector2(30 + 700 * marker, 73)


func _input(event: InputEvent) -> void:
	if stage != 2 or solved:
		return
	var pressed := event.is_action_pressed("interact") or event.is_action_pressed("ui_accept")
	if event is InputEventMouseButton and event.pressed:
		pressed = true
	if not pressed:
		return
	if marker >= target_start and marker <= target_start + target_width:
		set_status("Perfectly cooked!", UITheme.COL_OK)
		win(140)
	else:
		lose("It needs a little more time on the fire.")
		stage = 2
		_render()
