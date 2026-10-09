extends Node
## NotifyManager (autoload "Notify")
##
## Floating toasts, banner announcements and the full-screen "Culture
## Discovered" card.  Creates its own CanvasLayer so it works in every scene.

signal toast_finished

const LAYER := 90

var _layer: CanvasLayer
var _toast_box: VBoxContainer
var _banner: Control
var _banner_label: Label
var _banner_sub: Label
var _banner_timer: Timer
var _card: Control
var _queue: Array = []
var _busy := false


func _ready() -> void:
	_layer = CanvasLayer.new()
	_layer.layer = LAYER
	add_child(_layer)

	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_layer.add_child(root)

	_toast_box = VBoxContainer.new()
	_toast_box.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_toast_box.position = Vector2(-360, 96)
	_toast_box.custom_minimum_size = Vector2(340, 0)
	_toast_box.alignment = BoxContainer.ALIGNMENT_BEGIN
	_toast_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_toast_box)

	_banner = _build_banner()
	root.add_child(_banner)
	_card = null
	_card = load("res://scenes/ui/culture_card.tscn").instantiate() if ResourceLoader.exists("res://scenes/ui/culture_card.tscn") else null
	if _card:
		root.add_child(_card)
		_card.card_closed.connect(_on_card_closed)


# ------------------------------------------------------------------ toasts
func toast(text: String, color := Color(1, 0.95, 0.85)) -> void:
	_toast_box.add_child(_make_toast(text, color))
	toast_finished.emit()


func _make_toast(text: String, color: Color) -> Control:
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_SOFT))
	var lbl := Label.new()
	lbl.text = text
	lbl.add_theme_font_size_override("font_size", 18)
	lbl.add_theme_color_override("font_color", color)
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lbl.custom_minimum_size = Vector2(320, 0)
	panel.add_child(lbl)
	panel.modulate.a = 0.0
	panel.position.x = 60
	var tw := create_tween()
	tw.tween_property(panel, "modulate:a", 1.0, 0.22)
	tw.parallel().tween_property(panel, "position:x", 0.0, 0.26).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.tween_interval(2.4)
	tw.tween_property(panel, "modulate:a", 0.0, 0.4)
	tw.tween_callback(panel.queue_free)
	# keep at most 5 toasts on screen
	while _toast_box.get_child_count() > 5:
		_toast_box.get_child(0).queue_free()
	return panel


# ------------------------------------------------------------------ banner
func _build_banner() -> Control:
	var holder := Control.new()
	holder.set_anchors_preset(Control.PRESET_CENTER_TOP)
	holder.position = Vector2(-260, 120)
	holder.custom_minimum_size = Vector2(520, 120)
	holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	holder.modulate.a = 0.0

	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", UITheme.panel_style(UITheme.PANEL_BANNER))
	panel.custom_minimum_size = Vector2(520, 0)
	holder.add_child(panel)

	var vb := VBoxContainer.new()
	vb.alignment = BoxContainer.ALIGNMENT_CENTER
	vb.add_theme_constant_override("separation", 2)
	panel.add_child(vb)

	_banner_label = Label.new()
	_banner_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_banner_label.add_theme_font_size_override("font_size", 30)
	_banner_label.add_theme_color_override("font_color", UITheme.COL_GOLD)
	vb.add_child(_banner_label)

	_banner_sub = Label.new()
	_banner_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_banner_sub.add_theme_font_size_override("font_size", 18)
	_banner_sub.add_theme_color_override("font_color", UITheme.COL_TEXT)
	vb.add_child(_banner_sub)

	_banner_timer = Timer.new()
	_banner_timer.one_shot = true
	_banner_timer.wait_time = 2.6
	_banner_timer.timeout.connect(_hide_banner)
	holder.add_child(_banner_timer)
	return holder


func banner(title: String, text: String, sub := "", duration := 2.6) -> void:
	_banner_label.text = title
	var body := text
	if sub != "":
		body += "  ·  " + sub
	_banner_sub.text = body
	_banner_timer.wait_time = duration
	var tw := create_tween()
	tw.tween_property(_banner, "modulate:a", 1.0, 0.25)
	tw.parallel().tween_property(_banner, "position:y", 130.0, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_banner_timer.start()
	if _banner.get("position").y > 200:
		_banner.position.y = 100


func _hide_banner() -> void:
	var tw := create_tween()
	tw.tween_property(_banner, "modulate:a", 0.0, 0.4)


func achievement_banner(title: String, text: String) -> void:
	banner(title, text, "", 3.0)


# -------------------------------------------------------------------- cards
func show_culture_card(entry: Dictionary) -> void:
	if _card == null:
		banner("Culture discovered!", entry.get("name", ""))
		return
	_card.show_entry(entry)


func _on_card_closed() -> void:
	pass


func show_region_card(region: Dictionary) -> void:
	if _card == null:
		banner("Region discovered", region.get("name", ""))
		return
	_card.show_region(region)
