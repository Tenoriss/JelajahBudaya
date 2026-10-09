extends Node
## InventoryManager (autoload "Items")
##
## Grid inventory with categories.  Items are defined in data/items.json:
##   { name, category, description, icon, stack, region, rarity, value, note }

signal changed
signal item_added(item_id: String, count: int)
signal item_removed(item_id: String, count: int)

const CATEGORIES := ["items", "quest", "collectibles", "souvenirs"]
const CATEGORY_LABELS := {
	"items": "Items",
	"quest": "Quest Items",
	"collectibles": "Collectibles",
	"souvenirs": "Souvenirs",
}

var stacks: Dictionary = {}       # item_id -> count
var unlocked_items: Dictionary = {}   # item_id -> true (has ever been found)


func reset() -> void:
	stacks.clear()
	unlocked_items.clear()
	changed.emit()


func category_of(item_id: String) -> String:
	var def := Data.get_item(item_id)
	var cat: String = def.get("category", "items")
	return cat if CATEGORIES.has(cat) else "items"


func add(item_id: String, count := 1, silent := false) -> void:
	if item_id == "" or count <= 0:
		return
	var def := Data.get_item(item_id)
	if def.is_empty():
		push_warning("Unknown item: " + item_id)
		return
	var stack_max := int(def.get("stack", 99))
	stacks[item_id] = mini(stack_max, int(stacks.get(item_id, 0)) + count)
	var first := not unlocked_items.has(item_id)
	unlocked_items[item_id] = true
	if not silent:
		Audio.collect()
		var label: String = def.get("name", item_id)
		if category_of(item_id) == "collectibles":
			Notify.toast("* %s  ·  collected" % label, Color(1, 0.9, 0.6))
		else:
			Notify.toast("+ %s x%d" % [label, count])
	if first and category_of(item_id) == "collectibles":
		Game.bump("collectibles_found")
	changed.emit()
	item_added.emit(item_id, count)


func remove(item_id: String, count := 1) -> bool:
	var have := int(stacks.get(item_id, 0))
	if have < count:
		return false
	var left := have - count
	if left <= 0:
		stacks.erase(item_id)
	else:
		stacks[item_id] = left
	changed.emit()
	item_removed.emit(item_id, count)
	return true


func has(item_id: String, count := 1) -> bool:
	return int(stacks.get(item_id, 0)) >= count


func count(item_id: String) -> int:
	return int(stacks.get(item_id, 0))


func items_in_category(cat: String) -> Array:
	var out: Array = []
	for id in stacks.keys():
		if category_of(id) == cat:
			out.append(id)
	out.sort_custom(func(a, b): return str(Data.get_item(a).get("name", a)) < str(Data.get_item(b).get("name", b)))
	return out


func total_collectibles() -> int:
	return items_in_category("collectibles").size()


func to_dict() -> Dictionary:
	return {"stacks": stacks.duplicate(), "unlocked": unlocked_items.keys()}


func from_dict(d: Dictionary) -> void:
	stacks = {}
	var raw: Dictionary = d.get("stacks", {})
	for k in raw.keys():
		stacks[str(k)] = int(raw[k])
	unlocked_items = {}
	for k in d.get("unlocked", []):
		unlocked_items[str(k)] = true
	changed.emit()
