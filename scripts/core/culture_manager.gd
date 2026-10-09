extends Node
## CultureManager (autoload "Culture")
##
## The Culture Journal: entries are discovered through gameplay and stored here.
## Entries flagged "verify": true in data/cultures.json are shown with a
## "needs verification" note in the journal instead of being stated as fact.

signal discovered(entry: Dictionary)
signal changed

var discovered_ids: Array = []
var pending_card_queue: Array = []
var _showing_card := false


func reset() -> void:
	discovered_ids.clear()
	pending_card_queue.clear()
	changed.emit()


func is_discovered(id: String) -> bool:
	return discovered_ids.has(id)


func discover(id: String, show_card := true, silent := false) -> bool:
	if id == "" or is_discovered(id):
		return false
	var entry := Data.get_culture(id)
	if entry.is_empty():
		push_warning("Unknown culture entry: " + id)
		return false
	discovered_ids.append(id)
	if not silent:
		Game.add_culture_points(Game.CP_CULTURE, "culture:" + id)
		Audio.culture_discovered()
		if show_card:
			_queue_card(entry)
		else:
			Notify.toast("Journal: " + str(entry.get("name", id)), Color(0.8, 0.95, 1.0))
	discovered.emit(entry)
	changed.emit()
	Quest.notify_event("discover", id)
	Achievements.check_all()
	return true


func _queue_card(entry: Dictionary) -> void:
	pending_card_queue.append(entry)
	if not _showing_card:
		_show_next_card()


func _show_next_card() -> void:
	if pending_card_queue.is_empty():
		_showing_card = false
		return
	_showing_card = true
	var entry: Dictionary = pending_card_queue.pop_front()
	Notify.show_culture_card(entry)


func on_card_closed() -> void:
	Audio.ui_confirm()
	_show_next_card()


## Entries with "implicit": true are granted when the player first enters a region.
func discover_implicit_entries(region: String) -> void:
	for id in Data.cultures_for(region):
		var entry := Data.get_culture(id)
		if bool(entry.get("implicit", false)) and not is_discovered(id):
			discover(id, false, true)


func entries_in_category(cat: String) -> Array:
	var out: Array = []
	for id in Data.cultures.keys():
		var e: Dictionary = Data.cultures[id]
		if str(e.get("category", "")) == cat and is_discovered(id):
			out.append(id)
	out.sort()
	return out


func all_categories() -> Array:
	var cats: Array = []
	for id in Data.cultures.keys():
		var c := str(Data.cultures[id].get("category", "Other"))
		if not cats.has(c):
			cats.append(c)
	cats.sort()
	return cats


func region_progress(region: String) -> Dictionary:
	var ids := Data.cultures_for(region)
	var found := 0
	for id in ids:
		if is_discovered(id):
			found += 1
	return {"found": found, "total": ids.size(),
			"percent": (float(found) / max(1, ids.size())) * 100.0}


func total_found() -> int:
	return discovered_ids.size()


func to_dict() -> Dictionary:
	return {"discovered": discovered_ids.duplicate()}


func from_dict(d: Dictionary) -> void:
	discovered_ids = []
	for id in d.get("discovered", []):
		discovered_ids.append(str(id))
	changed.emit()
