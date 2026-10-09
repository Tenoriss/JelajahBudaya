extends Node
## AudioManager (autoload "Audio")
##
## Music, ambience and one-shot sfx with streaming players and soft crossfades.
## All audio is original material generated for this game (see tools/gen_audio.py).

const MUSIC_DIR := "res://assets/audio/music/"
const SFX_DIR := "res://assets/audio/sfx/"

var _music_a: AudioStreamPlayer
var _music_b: AudioStreamPlayer
var _using_a := true
var _ambience: AudioStreamPlayer
var _sfx_pool: Array[AudioStreamPlayer] = []
var _sfx_players := 12
var _sfx_index := 0
var current_music := ""
var _music_bus := "Music"
var _sfx_bus := "SFX"
var _step_index := 0
var _last_sfx_time := {}


func _ready() -> void:
	_ensure_buses()
	_music_a = _make_player(_music_bus)
	_music_b = _make_player(_music_bus)
	_music_b.volume_db = -80.0
	_ambience = _make_player("Ambience")
	for i in range(_sfx_players):
		var p := _make_player(_sfx_bus)
		_sfx_pool.append(p)
	apply_volumes()


func _make_player(bus: String) -> AudioStreamPlayer:
	var p := AudioStreamPlayer.new()
	p.bus = bus
	add_child(p)
	return p


func _ensure_buses() -> void:
	for bus_name in ["Music", "SFX", "Ambience"]:
		if AudioServer.get_bus_index(bus_name) == -1:
			var idx := AudioServer.bus_count
			AudioServer.add_bus(idx)
			AudioServer.set_bus_name(idx, bus_name)
			AudioServer.set_bus_send(idx, "Master")


func apply_volumes() -> void:
	_set_bus_volume("Music", Settings.music_volume)
	_set_bus_volume("Ambience", Settings.music_volume * 0.9)
	_set_bus_volume("SFX", Settings.sfx_volume)


func _set_bus_volume(bus: String, linear: float) -> void:
	var idx := AudioServer.get_bus_index(bus)
	if idx >= 0:
		AudioServer.set_bus_mute(idx, linear <= 0.001)
		AudioServer.set_bus_volume_db(idx, linear_to_db(maxf(0.0001, linear)))


# ------------------------------------------------------------------- music
func play_music(name: String, fade := 1.2) -> void:
	if name == current_music and _active_music().playing:
		return
	var stream := _load(MUSIC_DIR + name + ".ogg")
	if stream == null:
		return
	if stream is AudioStreamOggVorbis:
		stream.loop = true
	current_music = name
	var incoming := _music_b if _using_a else _music_a
	var outgoing := _music_a if _using_a else _music_b
	incoming.stream = stream
	incoming.volume_db = -40.0
	incoming.play()
	_using_a = not _using_a
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(incoming, "volume_db", 0.0, fade)
	if outgoing.playing:
		var tw2 := create_tween()
		tw2.tween_property(outgoing, "volume_db", -40.0, fade)
		tw2.tween_callback(outgoing.stop)


func stop_music(fade := 0.8) -> void:
	current_music = ""
	for p in [_music_a, _music_b]:
		if p.playing:
			var tw := create_tween()
			tw.tween_property(p, "volume_db", -40.0, fade)
			tw.tween_callback(p.stop)


func _active_music() -> AudioStreamPlayer:
	return _music_b if _using_a else _music_a


func play_ambience(name: String, fade := 1.0) -> void:
	if name == "":
		var tw := create_tween()
		tw.tween_property(_ambience, "volume_db", -40.0, fade)
		tw.tween_callback(_ambience.stop)
		return
	var stream := _load(SFX_DIR + name + ".ogg")
	if stream == null:
		return
	if stream is AudioStreamOggVorbis:
		stream.loop = true
	_ambience.stream = stream
	_ambience.volume_db = -26.0
	_ambience.play()
	var tw := create_tween()
	tw.tween_property(_ambience, "volume_db", -14.0, fade)


func stop_all() -> void:
	stop_music(0.3)
	for p in [_ambience]:
		p.stop()
	for p in _sfx_pool:
		p.stop()


# --------------------------------------------------------------------- sfx
func sfx(name: String, volume_db := 0.0, pitch := 1.0, throttle_ms := 0) -> void:
	if throttle_ms > 0:
		var now := Time.get_ticks_msec()
		if _last_sfx_time.get(name, -9999) + throttle_ms > now:
			return
		_last_sfx_time[name] = now
	var stream := _load(SFX_DIR + name + ".ogg")
	if stream == null:
		return
	var p := _sfx_pool[_sfx_index]
	_sfx_index = (_sfx_index + 1) % _sfx_pool.size()
	p.stream = stream
	p.volume_db = volume_db
	p.pitch_scale = pitch
	p.play()


func play_sfx(name: String) -> void:  # alias used in a few places
	sfx(name)


func ui_click() -> void:
	sfx("ui_click", -6.0, 1.0, 40)


func ui_hover() -> void:
	sfx("ui_tick", -14.0, 1.0, 30)


func ui_open() -> void:
	sfx("ui_open", -8.0)


func ui_confirm() -> void:
	sfx("ui_confirm", -5.0)


func ui_error() -> void:
	sfx("ui_error", -6.0)


func footstep(surface := "grass") -> void:
	_step_index = (_step_index + 1) % 4
	var kind := "grass" if surface in ["grass", "dirt", "mud", "sand", "rice", "farm", "jungle", "highland", "tall_grass", "reed", "ash"] else "stone"
	sfx("step_%s_%d" % [kind, _step_index], -16.0, randf_range(0.94, 1.08), 90)


func culture_discovered() -> void:
	sfx("culture_discovered", -3.0)


func quest_complete() -> void:
	sfx("quest_complete", -2.0)


func puzzle_solved() -> void:
	sfx("puzzle_solved", -3.0)


func puzzle_wrong() -> void:
	sfx("puzzle_wrong", -5.0)


func collect() -> void:
	sfx("collect", -4.0)


func coin() -> void:
	sfx("coin", -3.0)


func unlock() -> void:
	sfx("unlock", -2.0)


func chime(index: int) -> void:
	sfx("chime_%d" % clampi(index, 0, 3), -4.0)


func tone(index: int) -> void:
	sfx("tone_%d" % clampi(index, 0, 5), -7.0)


func impact(kind := "wood") -> void:
	sfx("impact_" + kind, -6.0)


# ------------------------------------------------------------------ helpers
func _load(path: String) -> AudioStream:
	if ResourceLoader.exists(path):
		return load(path)
	return null
