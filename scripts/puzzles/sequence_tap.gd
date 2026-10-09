extends MinigameBase
## SEQUENCE: put the steps in the right order (craft steps, ceremony order,
## recipe stages...).  data: {"items": ["...", ...], "order": [2,0,3,1]}

var items: Array = []
var order: Array = []
var picked: Array = []


func _build() -> void:
	var d: Dictionary = puzzle.get("data", {})
	items = []
	for v in d.get("items", ["Step A", "Step B", "Step C", "Step D"]):
		items.append(str(v))
	order = []
	for v in d.get("order", []):
		order.append(int(v))
	if order.is_empty():
		for i in range(items.size()):
			order.append(i)
	picked.clear()
	set_status("Click the steps in the correct order.")
	_render()


func _render() -> void:
	for child in board.get_children():
		child.queue_free()
	var y := 30.0
	for i in range(items.size()):
		var pos := Vector2(60, y)
		var is_picked := picked.has(i)
		var label := "%d. %s" % [picked.find(i) + 1, items[i]] if is_picked else str(items[i])
		var colour := Color(0.22, 0.32, 0.24) if is_picked else Color(0.24, 0.2, 0.26)
		var btn := add_button(pos, Vector2(680, 62), label, _on_item.bind(i), colour, 19)
		btn.disabled = is_picked
		y += 72


func _on_item(index: int) -> void:
	if picked.has(index):
		return
	var expected := order[picked.size()]
	picked.append(index)
	if index != expected:
		lose("The order needs another look.")
		await get_tree().create_timer(1.1).timeout
		if not solved:
			picked.clear()
			_render()
		return
	Audio.tone(mini(5, picked.size() - 1))
	set_status("Step %d correct." % picked.size())
	_render()
	if picked.size() >= order.size():
		win(120)
