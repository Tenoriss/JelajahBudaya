extends Node
## SaveManager (autoload "Save")
##
## JSON save slots in user://saves/.  Invalid or corrupted files never crash
## the game: load_slot() reports the problem and returns false.

signal saved(slot: int)
signal loaded(slot: int)

const SAVE_DIR := "user://saves"
const SLOT_COUNT := 3
const AUTOSAVE_SLOT := 0

var last_error := ""


func _ready() -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR)
	# autosave when the game is closed from the window manager
	get_tree().auto_accept_quit = false
	get_tree().set_meta("save_on_quit", true)


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		if Game.started:
			save_slot(AUTOSAVE_SLOT, true)
		get_tree().quit()


func slot_path(slot: int) -> String:
	return "%s/slot_%d.json" % [SAVE_DIR, slot]


func has_save(slot: int) -> bool:
	return FileAccess.file_exists(slot_path(slot))


func save_slot(slot: int, silent := false) -> bool:
	last_error = ""
	var payload := {
		"version": Game.SAVE_VERSION,
		"saved_at": Time.get_datetime_string_from_system(false, true),
		"play_time": Game.play_time,
		"chapter": Game.story_chapter,
		"region": Game.current_region,
		"game": Game.to_dict(),
		"items": Items.to_dict(),
		"quests": Quest.to_dict(),
		"culture": Culture.to_dict(),
		"achievements": Achievements.to_dict(),
	}
	var f := FileAccess.open(slot_path(slot), FileAccess.WRITE)
	if f == null:
		last_error = "Cannot write save file (%s)" % error_string(FileAccess.get_open_error())
		push_error(last_error)
		return false
	f.store_string(JSON.stringify(payload, "\t"))
	f.close()
	if not silent:
		Notify.toast("Saved to slot %d" % slot if slot > 0 else "Game autosaved")
	saved.emit(slot)
	return true


func load_slot(slot: int) -> bool:
	last_error = ""
	var path := slot_path(slot)
	if not FileAccess.file_exists(path):
		last_error = "Save slot %d is empty" % slot
		return false
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		last_error = "Cannot read save file"
		return false
	var text := f.get_as_text()
	f.close()
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY or not parsed.has("game"):
		last_error = "Save file is corrupted"
		push_warning(last_error)
		return false
	var version := int(parsed.get("version", 0))
	if version > Game.SAVE_VERSION:
		last_error = "Save was created by a newer version of the game"
		return false
	Game.from_dict(parsed["game"])
	Items.from_dict(parsed.get("items", {}))
	Quest.from_dict(parsed.get("quests", {}))
	Culture.from_dict(parsed.get("culture", {}))
	Achievements.from_dict(parsed.get("achievements", {}))
	loaded.emit(slot)
	return true


func delete_slot(slot: int) -> void:
	if has_save(slot):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(slot_path(slot)))


func slot_info(slot: int) -> Dictionary:
	if not has_save(slot):
		return {}
	var f := FileAccess.open(slot_path(slot), FileAccess.READ)
	if f == null:
		return {}
	var parsed = JSON.parse_string(f.get_as_text())
	f.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		return {"corrupted": true}
	var g: Dictionary = parsed.get("game", {})
	var region: String = str(g.get("current_region", "prologue"))
	var region_name: String = Data.get_region(region).get("name", region.capitalize())
	var quests: Dictionary = parsed.get("quests", {})
	var done: int = int(quests.get("completed", []).size()) if quests.has("completed") else 0
	var t := int(float(parsed.get("play_time", 0.0)))
	return {
		"slot": slot,
		"date": str(parsed.get("saved_at", "-")),
		"time": "%02d:%02d:%02d" % [t / 3600, (t % 3600) / 60, t % 60],
		"region": region_name,
		"chapter": int(parsed.get("chapter", 1)),
		"quests": done,
		"cp": int(g.get("culture_points", 0)),
	}
