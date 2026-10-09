extends Node
## AchievementManager (autoload "Achievements")
##
## Declarative achievements from data/achievements.json.  Each entry may combine
## several conditions; every condition must be satisfied.

signal unlocked(achievement_id: String)

var unlocked_ids: Array = []


func reset() -> void:
	unlocked_ids.clear()


func is_unlocked(id: String) -> bool:
	return unlocked_ids.has(id)


func check_all() -> void:
	for id in Data.achievements.keys():
		if is_unlocked(id):
			continue
		if _conditions_met(Data.achievements[id]):
			unlock(id)


func unlock(id: String) -> void:
	if is_unlocked(id):
		return
	var def := Data.get_achievement(id)
	if def.is_empty():
		return
	unlocked_ids.append(id)
	Audio.unlock()
	Notify.banner("Achievement: " + str(def.get("name", id)),
			str(def.get("description", "")), "", 3.2)
	unlocked.emit(id)
	Game.state_changed.emit("achievement", {"id": id})


func _conditions_met(def: Dictionary) -> bool:
	var cond: Dictionary = def.get("condition", {})
	for key in cond.keys():
		var value = cond[key]
		match key:
			"quests_completed":
				if int(Game.stats.get("quests_completed", 0)) < int(value):
					return false
			"puzzles_completed":
				if int(Game.stats.get("puzzles_completed", 0)) < int(value):
					return false
			"regions_visited":
				if Game.visited_regions.size() < int(value):
					return false
			"regions_unlocked":
				if Game.unlocked_regions.size() < int(value):
					return false
			"culture_discovered":
				if Culture.discovered_ids.size() < int(value):
					return false
			"collectibles":
				if Items.total_collectibles() < int(value):
					return false
			"landmarks":
				if Game.landmarks.size() < int(value):
					return false
			"hidden_areas":
				if Game.hidden_areas.size() < int(value):
					return false
			"minigames":
				if int(Game.stats.get("minigames_completed", 0)) < int(value):
					return false
			"culture_points":
				if Game.culture_points < int(value):
					return false
			"npcs_talked":
				if int(Game.stats.get("npcs_talked", 0)) < int(value):
					return false
			"flag":
				if not Game.has_flag(str(value)):
					return false
			"region_complete":
				var entry := str(value).split(":")
				if entry.size() == 2:
					if Game.region_progress_percent(entry[0]) < float(entry[1]):
						return false
			"journal_category_full":
				var found := 0
				for id in Data.cultures.keys():
					if str(Data.cultures[id].get("category", "")) == str(value) and Culture.is_discovered(id):
						found += 1
				if found < 3:
					return false
			_:
				pass
	return true


func progress_percent() -> float:
	if Data.achievements.is_empty():
		return 0.0
	return float(unlocked_ids.size()) / float(Data.achievements.size()) * 100.0


func to_dict() -> Dictionary:
	return {"unlocked": unlocked_ids.duplicate()}


func from_dict(d: Dictionary) -> void:
	unlocked_ids = []
	for id in d.get("unlocked", []):
		unlocked_ids.append(str(id))
