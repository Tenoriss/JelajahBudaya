extends Area2D
## Walking into this area moves the player to another map (data driven exits).

var exit_data: Dictionary = {}
var map: Node = null
var _busy := false


func _ready() -> void:
	collision_layer = 0
	collision_mask = 2
	body_entered.connect(_on_body_entered)
	if exit_data.has("if"):
		visible = true


func _on_body_entered(body: Node2D) -> void:
	if _busy or body.name != "Player":
		return
	if not _conditions_met():
		return
	var target := str(exit_data.get("target", ""))
	if target == "":
		return
	_busy = true
	Audio.sfx("ui_open", -10.0)
	# remember where the player came from so we can walk back
	if map != null and map.map_id != "":
		Game.map_player_pos[map.map_id] = [global_position.x, global_position.y + 40]
	await World.change_map(target, Vector2.INF, str(exit_data.get("entry", "")))
	await get_tree().create_timer(0.8).timeout
	_busy = false


func _conditions_met() -> bool:
	var cond: Dictionary = exit_data.get("if", {})
	for key in cond.keys():
		match key:
			"flag":
				if not Game.has_flag(str(cond[key])):
					_denied(str(exit_data.get("locked_text", "The way is closed for now.")))
					return false
			"no_flag":
				if Game.has_flag(str(cond[key])):
					_denied(str(exit_data.get("locked_text", "You have no reason to go back yet.")))
					return false
			"quest_done":
				if not Quest.is_completed(str(cond[key])):
					_denied(str(exit_data.get("locked_text", "Not yet.")))
					return false
			_:
				pass
	return true


func _denied(text: String) -> void:
	if _busy:
		return
	_busy = true
	Audio.ui_error()
	Notify.toast(text)
	await get_tree().create_timer(1.2).timeout
	_busy = false
