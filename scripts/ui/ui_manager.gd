extends Node
## UIManager (autoload "UI")
##
## Owns every screen that can appear above the world: HUD, dialogue box,
## notes, inventory, culture journal, world map, quest log, pause menu,
## achievements, settings and the puzzle host.  Screens live in
## res://scenes/ui/ and are instantiated on demand and cached.

signal map_ready(map_node: Node)

const SCENES := {
	"hud": "res://scenes/ui/hud.tscn",
	"dialogue": "res://scenes/ui/dialogue_box.tscn",
	"note": "res://scenes/ui/note_panel.tscn",
	"inventory": "res://scenes/ui/inventory_ui.tscn",
	"journal": "res://scenes/ui/journal_ui.tscn",
	"worldmap": "res://scenes/ui/world_map_ui.tscn",
	"quests": "res://scenes/ui/quest_log_ui.tscn",
	"pause": "res://scenes/ui/pause_menu.tscn",
	"achievements": "res://scenes/ui/achievements_ui.tscn",
	"settings": "res://scenes/ui/settings_ui.tscn",
	"savemenu": "res://scenes/ui/save_menu.tscn",
	"shop": "res://scenes/ui/shop_ui.tscn",
	"puzzle_host": "res://scenes/ui/puzzle_host.tscn",
}

var layer: CanvasLayer
var screens: Dictionary = {}           # name -> Control
var open_screens: Array = []           # stack of open screen names
var world: Node = null                 # the running map
var hud: Control = null
var _puzzle_host: Control = null
var _interaction_target: Node = null


func _ready() -> void:
	layer = CanvasLayer.new()
	layer.name = "UILayer"
	layer.layer = 10
	add_child(layer)
	process_mode = Node.PROCESS_MODE_ALWAYS


# ------------------------------------------------------------------ helpers
func screen(name: String) -> Control:
	if screens.has(name) and is_instance_valid(screens[name]):
		return screens[name]
	var path: String = SCENES.get(name, "")
	if path == "" or not ResourceLoader.exists(path):
		return null
	var node := (load(path) as PackedScene).instantiate()
	layer.add_child(node)
	screens[name] = node
	if node.has_method("on_setup"):
		node.on_setup()
	return node


func show_only(name: String) -> void:
	close_all()
	open(name)


func open(name: String) -> void:
	var node := screen(name)
	if node == null:
		return
	node.visible = true
	if not open_screens.has(name):
		open_screens.append(name)
	if node.has_method("on_open"):
		node.on_open()
	_update_pause_state()
	Audio.ui_open()


func close(name: String) -> void:
	if screens.has(name) and is_instance_valid(screens[name]):
		var node: Control = screens[name]
		if node.has_method("on_close"):
			node.on_close()
		node.visible = false
	open_screens.erase(name)
	_update_pause_state()


func close_all() -> void:
	for name in open_screens.duplicate():
		close(name)


func toggle(name: String) -> void:
	if open_screens.has(name):
		close(name)
	else:
		open(name)


func _update_pause_state() -> void:
	var blocking := is_blocking()
	get_tree().paused = blocking
	if world != null and is_instance_valid(world):
		var player := world.get("player")
		if player != null and is_instance_valid(player):
			player.lock_input(blocking)


func is_blocking() -> bool:
	for name in open_screens:
		if name in ["inventory", "journal", "worldmap", "quests", "pause", "note", "dialogue", "settings", "achievements", "savemenu", "shop"]:
			return true
	return false


# -------------------------------------------------------------- interaction
func set_interaction_target(target: Node) -> void:
	_interaction_target = target
	if hud != null and is_instance_valid(hud) and hud.has_method("set_prompt"):
		var text := ""
		if target != null and target.has_method("display_name"):
			text = str(target.display_name())
		hud.set_prompt(text)


func perform_interaction() -> void:
	if Dialogue.active or is_blocking():
		return
	if world == null or not is_instance_valid(world):
		return
	var player := world.get("player")
	if player != null and player.has_method("interact"):
		player.interact()


# ---------------------------------------------------------------- map hooks
func on_map_loaded(map_def: Dictionary) -> void:
	world = null
	if hud != null and is_instance_valid(hud):
		hud.on_map_loaded(map_def)


func notify_map_ready(map_node: Node) -> void:
	world = map_node
	if hud == null:
		hud = screen("hud")
	if hud != null:
		hud.on_map_loaded(map_node.map_def)
	map_ready.emit(map_node)
	# region music handled by World; region card handled there too


# ----------------------------------------------------------------- dialogue
func open_dialogue_node(dialogue_id: String, node: Dictionary, context: Dictionary) -> void:
	var box := screen("dialogue")
	if box == null:
		return
	if not open_screens.has("dialogue"):
		open_screens.append("dialogue")
	box.visible = true
	box.show_node(dialogue_id, node, context)
	_update_pause_state()


func show_dialogue_choices(choices: Array) -> void:
	var box := screen("dialogue")
	if box != null:
		box.show_choices(choices)


func close_dialogue() -> void:
	if screens.has("dialogue") and is_instance_valid(screens["dialogue"]):
		screens["dialogue"].visible = false
	open_screens.erase("dialogue")
	_update_pause_state()


# -------------------------------------------------------------------- notes
func show_note(title: String, text: String) -> void:
	var note := screen("note")
	if note == null:
		Notify.toast(text)
		return
	note.show_note(title, text)
	open("note")


# ------------------------------------------------------------------ puzzles
func attach_puzzle(instance: Node) -> void:
	if _puzzle_host == null:
		_puzzle_host = screen("puzzle_host")
	if _puzzle_host == null:
		# fall back: put the puzzle straight into the UI layer
		layer.add_child(instance)
		instance.tree_exited.connect(func(): _update_pause_state())
		get_tree().paused = true
		return
	_puzzle_host.attach(instance)
	get_tree().paused = false          # minigames animate, world stays frozen
	if world != null and is_instance_valid(world):
		var p := world.get("player")
		if p != null:
			p.lock_input(true)
	_puzzle_host.visible = true


func detach_puzzle() -> void:
	if _puzzle_host != null:
		_puzzle_host.detach()
		_puzzle_host.visible = false
	_update_pause_state()


func puzzle_host_active() -> bool:
	return _puzzle_host != null and _puzzle_host.visible


# ----------------------------------------------------------------- minigame
func open_minigame(name: String) -> void:
	Puzzle.start_minigame(name, {})


# --------------------------------------------------------------------- misc
func toast(text: String) -> void:
	Notify.toast(text)
