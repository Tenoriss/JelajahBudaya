class_name UITheme
extends RefCounted
## Central look and feel for the whole UI: colours, fonts, panel styles.
## Everything is generated art (assets/ui/*.png) + built-in fonts, so the game
## has no external dependencies.

const COL_TEXT := Color(0.97, 0.93, 0.84)
const COL_DIM := Color(0.76, 0.70, 0.60)
const COL_GOLD := Color(0.94, 0.78, 0.40)
const COL_ACCENT := Color(0.95, 0.62, 0.42)
const COL_OK := Color(0.56, 0.86, 0.55)
const COL_BAD := Color(0.88, 0.42, 0.38)
const COL_TEAL := Color(0.55, 0.86, 0.88)
const COL_PANEL_TEXT := Color(0.99, 0.96, 0.90)

enum Panel { DARK, SOFT, BANNER, DIALOGUE, PARCHMENT, NONE }

const PANEL_DARK := Panel.DARK
const PANEL_SOFT := Panel.SOFT
const PANEL_BANNER := Panel.BANNER
const PANEL_DIALOGUE := Panel.DIALOGUE
const PANEL_PARCHMENT := Panel.PARCHMENT

const TEX := {
	Panel.DARK: "res://assets/ui/panel_dark.png",
	Panel.SOFT: "res://assets/ui/panel_soft.png",
	Panel.BANNER: "res://assets/ui/panel_banner.png",
	Panel.DIALOGUE: "res://assets/ui/panel_dialogue.png",
	Panel.PARCHMENT: "res://assets/ui/parchment.png",
}

const MARGINS := {
	Panel.DARK: 10,
	Panel.SOFT: 9,
	Panel.BANNER: 12,
	Panel.DIALOGUE: 12,
	Panel.PARCHMENT: 12,
}


static func texture(panel: int) -> Texture2D:
	var path: String = TEX.get(panel, TEX[Panel.DARK])
	if ResourceLoader.exists(path):
		return load(path)
	return null


static func panel_style(panel: int = Panel.DARK, margin := -1) -> StyleBox:
	var tex := texture(panel)
	var m: float = float(MARGINS.get(panel, 10)) if margin < 0 else float(margin)
	if tex == null:
		var flat := StyleBoxFlat.new()
		flat.bg_color = Color(0.16, 0.12, 0.16, 0.92)
		flat.border_color = COL_GOLD
		flat.set_border_width_all(2)
		flat.set_corner_radius_all(6)
		flat.set_content_margin_all(m)
		return flat
	var sb := StyleBoxTexture.new()
	sb.texture = tex
	sb.set_texture_margin_all(6)
	sb.set_content_margin_all(m + 4)
	return sb


static func button_style(state := "normal") -> StyleBox:
	var path := "res://assets/ui/button_%s.png" % state
	if not ResourceLoader.exists(path):
		var flat := StyleBoxFlat.new()
		flat.bg_color = Color(0.3, 0.22, 0.28)
		flat.set_content_margin_all(8)
		flat.set_corner_radius_all(4)
		return flat
	var sb := StyleBoxTexture.new()
	sb.texture = load(path)
	sb.set_texture_margin_all(7)
	sb.set_content_margin_all(12)
	return sb


static func apply_button(btn: Button, font_size := 20) -> void:
	btn.add_theme_stylebox_override("normal", button_style("normal"))
	btn.add_theme_stylebox_override("hover", button_style("hover"))
	btn.add_theme_stylebox_override("pressed", button_style("pressed"))
	btn.add_theme_stylebox_override("disabled", button_style("disabled"))
	btn.add_theme_stylebox_override("focus", button_style("hover"))
	btn.add_theme_font_size_override("font_size", font_size)
	btn.add_theme_color_override("font_color", COL_TEXT)
	btn.add_theme_color_override("font_hover_color", Color(1, 0.98, 0.9))
	btn.add_theme_color_override("font_pressed_color", COL_GOLD)
	btn.add_theme_color_override("font_disabled_color", Color(0.6, 0.55, 0.5))
	btn.mouse_entered.connect(func(): Audio.ui_hover())
	btn.pressed.connect(func(): Audio.ui_click())
	if not btn.focus_entered.is_connected(_on_focus):
		btn.focus_entered.connect(_on_focus)


static func _on_focus() -> void:
	pass


static func apply_label(lbl: Label, size := 18, color := COL_TEXT) -> void:
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	lbl.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
	lbl.add_theme_constant_override("shadow_offset_x", 1)
	lbl.add_theme_constant_override("shadow_offset_y", 2)


static func heading(text: String, size := 30) -> Label:
	var lbl := Label.new()
	lbl.text = text
	apply_label(lbl, size, COL_GOLD)
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return lbl


static func hline() -> HSeparator:
	var sep := HSeparator.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(COL_GOLD.r, COL_GOLD.g, COL_GOLD.b, 0.45)
	sb.content_margin_top = 1
	sb.content_margin_bottom = 1
	sep.add_theme_stylebox_override("separator", sb)
	return sep


static func make_panel(panel: int = Panel.DARK) -> PanelContainer:
	var pc := PanelContainer.new()
	pc.add_theme_stylebox_override("panel", panel_style(panel))
	return pc


static func progress_bar(value: float, maxv: float, colour := COL_GOLD, width := 140.0) -> ProgressBar:
	var bar := ProgressBar.new()
	bar.max_value = maxf(0.01, maxv)
	bar.value = value
	bar.show_percentage = false
	bar.custom_minimum_size = Vector2(width, 12)
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color(0.12, 0.1, 0.13, 0.85)
	bg.border_color = Color(COL_GOLD.r, COL_GOLD.g, COL_GOLD.b, 0.6)
	bg.set_border_width_all(1)
	bg.set_corner_radius_all(3)
	var fill := StyleBoxFlat.new()
	fill.bg_color = colour
	fill.set_corner_radius_all(3)
	bar.add_theme_stylebox_override("background", bg)
	bar.add_theme_stylebox_override("fill", fill)
	return bar


static func icon(name: String) -> Texture2D:
	var path := "res://assets/ui/icon_%s.png" % name
	if ResourceLoader.exists(path):
		return load(path)
	return null
