extends Control
## Full-screen host for puzzles and mini-games.  Keeps the world frozen while a
## puzzle runs and shows the shared puzzle chrome (title, hints, controls).

var content: Control
var title_label: Label


func on_setup() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.04, 0.07, 0.88)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	content = Control.new()
	content.set_anchors_preset(Control.PRESET_FULL_RECT)
	content.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(content)
	title_label = Label.new()
	UITheme.apply_label(title_label, 24, UITheme.COL_GOLD)
	title_label.position = Vector2(24, 16)
	add_child(title_label)


func attach(instance: Node) -> void:
	for child in content.get_children():
		child.queue_free()
	content.add_child(instance)
	if instance is Control:
		(instance as Control).set_anchors_preset(Control.PRESET_FULL_RECT)
	title_label.text = str(instance.get("puzzle_title")) if "puzzle_title" in instance else ""
	visible = true


func detach() -> void:
	for child in content.get_children():
		child.queue_free()
	visible = false
