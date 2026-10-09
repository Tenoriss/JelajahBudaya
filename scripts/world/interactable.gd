extends Area2D
## A generic world interaction point driven by data.
##
## kind:
##   inspect     - examine a placed scenery prop (repeatable)
##   sign        - read a short note            (text)
##   pickup      - collect an item              (target=item id)
##   chest       - collect several items        (items=[..], once=true)
##   puzzle      - open a puzzle                (target=puzzle id)
##   minigame    - open a mini-game             (target=minigame id)
##   door        - travel to another map        (target=map id, entry=entry id)
##   discovery   - discover a culture entry     (target=culture id)
##   landmark    - register a landmark          (target/name/description)
##   hidden      - hidden area discovery        (name, hint, rewards)
##   dialogue    - start a dialogue tree        (target=dialogue id)
##   flag        - set a story flag             (target=flag)
##   save        - save point
##   note        - long readable document       (title, text)

const INTERACT_LAYER := 4      # areas the player's interact zone can see

var data: Dictionary = {}
var map: Node = null
var used := false
var prompt := ""

func _ready() -> void:
	# the player's InteractZone polls get_overlapping_areas(), so this area has to
	# live on the interaction layer and be monitorable (but it never monitors itself)
	collision_layer = INTERACT_LAYER
	collision_mask = 0
	monitoring = false
	monitorable = true
	_apply_visible_state()
	add_to_group("interactable")


func _apply_visible_state() -> void:
	if _is_consumed():
		used = true
	if bool(data.get("hidden", false)):
		visible = Game.has_flag("reveal_" + _id())
	_sync_children_visible()


func _sync_children_visible() -> void:
	for child in get_children():
		if child is Sprite2D or child is Node2D:
			child.visible = visible


func _is_consumed() -> bool:
	if bool(data.get("once", false)) and Game.has_flag("used_" + _id()):
		return true
	if data.has("once_flag") and Game.has_flag(str(data["once_flag"])):
		return true
	return false


func _id() -> String:
	return str(data.get("id", name))


func display_name() -> String:
	if _is_consumed() or not _conditions_met():
		return ""
	var kind := str(data.get("kind", "sign"))
	var label := "Interact"
	match kind:
		"inspect":
			var examine := "Periksa " if Settings.language.begins_with("id") else "Examine "
			label = examine + _inspection_name()
		"sign", "note":
			label = "Read"
		"pickup":
			label = "Pick up " + str(Data.get_item(str(data.get("target", ""))).get("name", "item"))
		"chest":
			label = "Open"
		"puzzle", "discovery":
			label = "Examine"
		"minigame":
			label = str(data.get("prompt", "Try it"))
		"door":
			label = str(data.get("prompt", "Enter"))
		"landmark":
			label = "Look around"
		"hidden":
			label = "Search"
		"dialogue":
			label = "Talk"
		"flag":
			label = str(data.get("prompt", "Interact"))
		"save":
			label = "Rest (save)"
	return label


func _conditions_met() -> bool:
	var cond: Dictionary = data.get("if", {})
	var conditions_ok := true
	for key in cond.keys():
		match key:
			"flag":
				conditions_ok = Game.has_flag(str(cond[key]))
			"no_flag":
				conditions_ok = not Game.has_flag(str(cond[key]))
			"quest_active":
				conditions_ok = Quest.is_active(str(cond[key]))
			"quest_done":
				conditions_ok = Quest.is_completed(str(cond[key]))
			"has_item":
				var parts := str(cond[key]).split(":")
				var need := int(parts[1]) if parts.size() > 1 else 1
				conditions_ok = Items.has(parts[0], need)
			"puzzle_solved":
				conditions_ok = Puzzle.is_solved(str(cond[key]))
			"puzzle_unsolved":
				conditions_ok = not Puzzle.is_solved(str(cond[key]))
			"chapter":
				conditions_ok = Game.story_chapter >= int(cond[key])
			"time":
				conditions_ok = World.time_name().to_lower() == str(cond[key]).to_lower()
		if not conditions_ok:
			break
	return conditions_ok


func can_interact() -> bool:
	if _is_consumed():
		return false
	if not visible:
		return false
	return _conditions_met()


func interact(_player: Node) -> bool:
	if not can_interact():
		if not visible:
			Audio.ui_error()
			Notify.toast("Nothing here... yet.")
			return true
		if not _conditions_met():
			Audio.ui_error()
			Notify.toast(str(data.get("locked_text", "You cannot do that yet.")))
			return true
		return false
	var kind := str(data.get("kind", "sign"))
	var target := str(data.get("target", ""))
	match kind:
		"inspect":
			UI.show_note(_inspection_name(), _inspection_text())
		"sign", "note":
			UI.show_note(str(data.get("title", "")), str(data.get("text", "")))
		"pickup":
			Items.add(target, int(data.get("count", 1)))
			_mark_used()
			if data.has("text"):
				UI.show_note(str(data.get("title", "Found")), str(data["text"]))
		"chest":
			for item_id in data.get("items", []):
				Items.add(str(item_id), 1)
			if data.has("culture"):
				Culture.discover(str(data["culture"]), true)
			if data.has("text"):
				UI.show_note(str(data.get("title", "Opened")), str(data["text"]))
			_mark_used()
		"puzzle":
			Puzzle.open(target, {"source": _id()})
		"minigame":
			Puzzle.start_minigame(str(data.get("minigame", target)), {
				"title": str(data.get("title", "")),
				"description": str(data.get("text", "")),
				"reward_cp": int(data.get("reward_cp", Game.CP_MINIGAME)),
				"data": data.get("data", {}),
			})
		"door":
			if map != null:
				World.change_map(target, Vector2.INF, str(data.get("entry", "")))
		"discovery":
			if not Culture.discover(target, true):
				UI.show_note(str(data.get("title", "Nothing new")),
						str(data.get("repeat_text", "You have already recorded this.")))
			_mark_used()
		"landmark":
			Game.discover_landmark(target if target != "" else _id(),
					str(data.get("title", "")), str(data.get("text", "")))
			if data.has("culture"):
				Culture.discover(str(data["culture"]), true)
			_mark_used()
		"hidden":
			Game.discover_hidden_area(_id(), str(data.get("title", "Hidden place")),
					str(data.get("text", "")))
			for item_id in data.get("items", []):
				Items.add(str(item_id), 1)
			if data.has("culture"):
				Culture.discover(str(data["culture"]), true)
			_mark_used()
		"dialogue":
			Dialogue.start(target, {"source": _id(), "npc": str(data.get("npc", ""))})
		"flag":
			Game.set_flag(target, true)
			if data.has("text"):
				Notify.toast(str(data["text"]))
			_mark_used()
		"save":
			if Save.save_slot(Save.AUTOSAVE_SLOT, true):
				Notify.banner("Saved", "Your journey is recorded", World.time_string(), 2.2)
			Audio.chime(0)
		_:
			UI.show_note("", str(data.get("text", "")))
	Quest.notify_event("talk", "interactable:" + _id())
	return true


func _inspection_name() -> String:
	var key := "title_id" if Settings.language.begins_with("id") else "title_en"
	var fallback := str(data.get("target", "object")).replace("_", " ").capitalize()
	return str(data.get(key, fallback))


func _inspection_text() -> String:
	var key := "text_id" if Settings.language.begins_with("id") else "text_en"
	if data.has(key):
		return str(data[key])
	var name := _inspection_name()
	if Settings.language.begins_with("id"):
		return "Amati bentuk dan detail %s ini." % name
	return "Observe the shape and details of %s." % name


func _mark_used() -> void:
	used = true
	Game.set_flag("used_" + _id(), true)
	if bool(data.get("hide_when_used", true)):
		visible = false
		_sync_children_visible()
	remove_from_group("interactable")
	monitorable = false
