extends Area2D
## A landmark: registers itself with GameManager when the player walks in and
## becomes a fast-travel destination on the world map.

var lm_id := ""
var lm_name := ""
var lm_description := ""
var lm_entry := ""
var _done := false


func _ready() -> void:
	collision_layer = 0
	collision_mask = 2          # detects the player body only
	monitoring = true
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if _done or body.name != "Player":
		return
	_done = true
	Game.discover_landmark(lm_id, lm_name, lm_description)
	if lm_entry != "":
		Culture.discover(lm_entry, true)
	Quest.notify_event("landmark", lm_id)
