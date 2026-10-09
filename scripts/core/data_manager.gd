extends Node
## DataManager (autoload "Data")
##
## Loads every content file from res://data/ once and exposes it to the rest of
## the game.  Everything the game shows is data driven so that new regions,
## quests, cultures, items or puzzles can be added without touching code.

const DATA_DIR := "res://data"

var regions: Dictionary = {}          # region_id -> region definition
var region_order: Array = []          # ["sumatra", "java", ...]
var maps: Dictionary = {}             # map_id -> map definition (generated maps)
var map_regions: Dictionary = {}      # region_id -> [map_id, ...]
var route_maps: Dictionary = {}       # region_id -> map layout/connection data
var quests: Dictionary = {}           # quest_id -> quest
var cultures: Dictionary = {}         # entry_id -> culture journal entry
var culture_by_region: Dictionary = {}# region_id -> [entry_id]
var items: Dictionary = {}            # item_id -> item
var puzzles: Dictionary = {}          # puzzle_id -> puzzle definition
var dialogues: Dictionary = {}        # dialogue_id -> dialogue tree
var achievements: Dictionary = {}
var npcs: Dictionary = {}             # npc_id -> npc definition (id cards)
var characters: Dictionary = {}       # character_id -> sprite sheet info
var objects: Dictionary = {}          # object sprite_name -> sprite/reg info
var tilesets: Dictionary = {}         # region_id -> tileset atlas info
var chapters: Array = []
var endings: Dictionary = {}
var tile_legend: Dictionary = {}      # 'G' -> ["grass0", ...] tile names

var loaded := false
var errors: Array[String] = []


func _ready() -> void:
	reload()


func reload() -> void:
	errors.clear()
	regions = _load_json("regions.json", {})
	chapters = regions.get("chapters", [])
	region_order = regions.get("order", [])
	route_maps = _load_json("route_maps.json", {}).get("maps", {})
	quests = _load_json("quests.json", {}).get("quests", {})
	cultures = _load_json("cultures.json", {}).get("entries", {})
	items = _load_json("items.json", {}).get("items", {})
	puzzles = _load_json("puzzles.json", {}).get("puzzles", {})
	achievements = _load_json("achievements.json", {}).get("achievements", {})
	dialogues = _load_json("dialogues.json", {}).get("dialogues", {})
	npcs = _load_json("npcs.json", {}).get("npcs", {})
	endings = _load_json("endings.json", {})
	characters = _load_json("characters.json", {})
	objects = _load_json("objects.json", {})
	tilesets = _load_json("tilesets.json", {})
	tile_legend = tilesets.get("_legend", {})

	culture_by_region.clear()
	for entry_id in cultures.keys():
		var region: String = cultures[entry_id].get("region", "")
		if not culture_by_region.has(region):
			culture_by_region[region] = []
		culture_by_region[region].append(entry_id)

	maps.clear()
	map_regions.clear()
	var map_dir := DirAccess.open(DATA_DIR + "/maps")
	if map_dir:
		map_dir.list_dir_begin()
		var file := map_dir.get_next()
		while file != "":
			if file.ends_with(".json"):
				var data: Dictionary = _load_json_raw(DATA_DIR + "/maps/" + file)
				if data.has("id"):
					var mid: String = data["id"]
					maps[mid] = data
					var reg: String = data.get("region", "prologue")
					if not map_regions.has(reg):
						map_regions[reg] = []
					map_regions[reg].append(mid)
			file = map_dir.get_next()
		map_dir.list_dir_end()
	else:
		errors.append("Cannot open res://data/maps")

	for reg in map_regions.keys():
		map_regions[reg].sort()
	loaded = true
	if errors.size() > 0:
		push_warning("DataManager loaded with %d warning(s): %s" % [errors.size(), ", ".join(errors)])


# ---------------------------------------------------------------- accessors
func get_region(id: String) -> Dictionary:
	return regions.get("regions", {}).get(id, {})


func get_map(id: String) -> Dictionary:
	return maps.get(id, {})


func get_quest(id: String) -> Dictionary:
	return quests.get(id, {})


func get_quests_in_region(region: String) -> Array:
	var out: Array = []
	for qid in quests.keys():
		if quests[qid].get("region", "") == region:
			out.append(qid)
	out.sort()
	return out


func get_culture(id: String) -> Dictionary:
	return cultures.get(id, {})


func get_item(id: String) -> Dictionary:
	return items.get(id, {})


func get_puzzle(id: String) -> Dictionary:
	return puzzles.get(id, {})


func get_npc(id: String) -> Dictionary:
	return npcs.get(id, {})


func get_dialogue(id: String) -> Dictionary:
	return dialogues.get(id, {})


func get_achievement(id: String) -> Dictionary:
	return achievements.get(id, {})


func get_character(id: String) -> Dictionary:
	return characters.get(id, {})


func get_object(sprite: String) -> Dictionary:
	return objects.get(sprite, {})


func cultures_for(region: String) -> Array:
	return culture_by_region.get(region, [])


func maps_of(region: String) -> Array:
	return map_regions.get(region, [])


func get_chapter(index: int) -> Dictionary:
	for ch in chapters:
		if int(ch.get("index", -1)) == index:
			return ch
	return {}


func total_culture_entries() -> int:
	return cultures.size()


func all_quest_ids() -> Array:
	var out: Array = quests.keys()
	out.sort()
	return out


# ------------------------------------------------------------------ loading
func _load_json(file_name: String, fallback: Dictionary) -> Dictionary:
	var data: Dictionary = _load_json_raw(DATA_DIR + "/" + file_name)
	if data.is_empty():
		errors.append("Missing or empty: " + file_name)
		return fallback
	return data


func _load_json_raw(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		errors.append("No such file: " + path)
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		errors.append("Cannot open: " + path)
		return {}
	var text := f.get_as_text()
	f.close()
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		errors.append("Bad JSON: " + path)
		return {}
	return parsed
