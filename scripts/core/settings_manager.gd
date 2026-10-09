extends Node
## SettingsManager (autoload "Settings") -- user preferences + localisation hook.

signal changed

const PATH := "user://settings.json"

var music_volume := 0.7
var sfx_volume := 0.85
var text_speed := 45.0          # characters per second (0 = instant)
var fullscreen := false
var resolution := Vector2i(1280, 720)
var language := "en"
var show_hints_button := true
var screenshake := true
var minimap_enabled := true


func _ready() -> void:
	load_settings()


func apply() -> void:
	Audio.apply_volumes()
	if fullscreen:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	if not fullscreen:
		DisplayServer.window_set_size(resolution)
	TranslationServer.set_locale(language)
	changed.emit()


func to_dict() -> Dictionary:
	return {
		"music_volume": music_volume,
		"sfx_volume": sfx_volume,
		"text_speed": text_speed,
		"fullscreen": fullscreen,
		"resolution": [resolution.x, resolution.y],
		"language": language,
		"show_hints_button": show_hints_button,
		"screenshake": screenshake,
		"minimap_enabled": minimap_enabled,
	}


func from_dict(d: Dictionary) -> void:
	music_volume = clampf(float(d.get("music_volume", 0.7)), 0.0, 1.0)
	sfx_volume = clampf(float(d.get("sfx_volume", 0.85)), 0.0, 1.0)
	text_speed = clampf(float(d.get("text_speed", 45.0)), 0.0, 200.0)
	fullscreen = bool(d.get("fullscreen", false))
	var res = d.get("resolution", [1280, 720])
	resolution = Vector2i(int(res[0]), int(res[1]))
	language = str(d.get("language", "en"))
	show_hints_button = bool(d.get("show_hints_button", true))
	screenshake = bool(d.get("screenshake", true))
	minimap_enabled = bool(d.get("minimap_enabled", true))


func save_settings() -> void:
	var f := FileAccess.open(PATH, FileAccess.WRITE)
	if f == null:
		return
	f.store_string(JSON.stringify(to_dict(), "\t"))
	f.close()


func load_settings() -> void:
	if not FileAccess.file_exists(PATH):
		return
	var f := FileAccess.open(PATH, FileAccess.READ)
	if f == null:
		return
	var parsed = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) == TYPE_DICTIONARY:
		from_dict(parsed)
	else:
		push_warning("settings.json corrupted -- using defaults")
