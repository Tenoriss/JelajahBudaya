class_name WorldBuilder
extends RefCounted
## Turns a data driven map definition (data/maps/*.json) into a live scene.
##
## Map definition format
## ---------------------
## {
##   "id": "sumatra_desa", "name": "Kampung Danau", "region": "sumatra",
##   "size": [64, 48],                       # in tiles
##   "spawn": [32, 40], "music": "sumatra", "ambience": "stream",
##   "terrain": {                            # painted with a tiny brush DSL
##      "default": "GRASS",
##      "rects": [ {"tile": "WATER", "rect": [20,14,10,6]} ],
##      "lines": [ {"tile": "PATH", "from": [4,40], "to": [60,40], "width": 2} ],
##      "blobs": [ {"tile": "JUNGLE", "center": [10,10], "radius": 6} ]
##   },
##   "objects": [ {"sprite": "rumah_gadang", "pos": [20,24]} ],
##   "npcs":   [ {"id": "npc_aminah", "pos": [24,30]} ],
##   "interactables": [
##       {"id": "x", "kind": "pickup|sign|chest|puzzle|npc|landmark|hidden|door|item",
##        "pos": [x,y], "sprite": "crate", "text": "...", "target": "...", ...} ],
##   "landmarks": [ {"id": "lk", "name": "N", "pos": [x,y]} ],
##   "exits":  [ {"id": "e", "pos": [x,y], "target": "other_map", "entry": "e2"} ],
##   "collision_rects": [ [x,y,w,h] ]        # extra invisible walls (tiles)
## }

const TILE := 32

static func build(def: Dictionary) -> Node2D:
	var map_id := str(def.get("id", "map"))
	var region := str(def.get("region", "prologue"))
	var root := Node2D.new()
	root.name = "Map_" + map_id
	root.set_script(load("res://scripts/world/world_map.gd"))
	root.map_def = def
	root.region = region
	root.map_id = map_id
	root.setup_nodes()

	var tileset: Dictionary = Data.tilesets.get(region, Data.tilesets.get("sumatra", {}))
	var size_arr: Array = def.get("size", [48, 36])
	var w := int(size_arr[0])
	var h := int(size_arr[1])

	# ---- terrain ---------------------------------------------------------
	var legend: Dictionary = Data.tile_legend
	var grid: Array = []
	for y in range(h):
		var row: Array = []
		for x in range(w):
			row.append(str(def.get("terrain", {}).get("default", "GRASS")))
		grid.append(row)

	var terrain: Dictionary = def.get("terrain", {})
	for r in terrain.get("rects", []):
		var rect: Array = r.get("rect", [0, 0, 1, 1])
		var kind := str(r.get("tile", "GRASS"))
		for y in range(int(rect[1]), int(rect[1]) + int(rect[3])):
			for x in range(int(rect[0]), int(rect[0]) + int(rect[2])):
				if x >= 0 and y >= 0 and x < w and y < h:
					grid[y][x] = kind
	for line in terrain.get("lines", []):
		var kind2 := str(line.get("tile", "PATH"))
		var from: Array = line.get("from", [0, 0])
		var to: Array = line.get("to", [0, 0])
		var width := int(line.get("width", 1))
		var steps := maxi(absi(int(to[0]) - int(from[0])), absi(int(to[1]) - int(from[1]))) + 1
		for i in range(steps):
			var t := float(i) / maxf(1.0, float(steps - 1))
			var cx := int(round(float(from[0]) + (float(to[0]) - float(from[0])) * t))
			var cy := int(round(float(from[1]) + (float(to[1]) - float(from[1])) * t))
			for dy in range(-((width - 1) / 2), (width / 2) + 1):
				for dx in range(-((width - 1) / 2), (width / 2) + 1):
					var px := cx + dx
					var py := cy + dy
					if px >= 0 and py >= 0 and px < w and py < h:
						grid[py][px] = kind2
	for blob in terrain.get("blobs", []):
		var kind3 := str(blob.get("tile", "JUNGLE"))
		var center: Array = blob.get("center", [0, 0])
		var radius := float(blob.get("radius", 4))
		for y in range(h):
			for x in range(w):
				var d := Vector2(float(x) - float(center[0]), float(y) - float(center[1])).length()
				if d <= radius:
					grid[y][x] = kind3

	# ---- build the tile layer -------------------------------------------
	var layer: TileMapLayer = root.ground
	layer.tile_set = _build_tileset(tileset, legend)

	var tile_size := int(tileset.get("tile_size", TILE))
	var atlas_cols := int(tileset.get("columns", 10))
	var tiles: Dictionary = tileset.get("tiles", {})
	var source_id := 0

	var rng := RandomNumberGenerator.new()
	rng.seed = hash(map_id)
	var anim_groups: Dictionary = tileset.get("animations", {})
	var anim_lookup := {}
	for group_name in anim_groups.keys():
		for idx in range(anim_groups[group_name].size()):
			anim_lookup[str(anim_groups[group_name][idx])] = {"group": group_name, "index": idx}

	for y in range(h):
		for x in range(w):
			var kind: String = grid[y][x]
			var names: Array = legend.get(kind, legend.get("GRASS", ["grass0"]))
			var tile_name := str(
				names[rng.randi_range(0, names.size() - 1)] if names.size() > 1 else names[0])
			if not tiles.has(tile_name):
				tile_name = str(tiles.keys()[0])
			var info: Dictionary = tiles[tile_name]
			var at: Array = info.get("atlas", [0, 0])
			layer.set_cell(Vector2i(x, y), source_id, Vector2i(int(at[0]), int(at[1])))
			if anim_lookup.has(tile_name):
				root.register_anim_cell(Vector2i(x, y), str(anim_lookup[tile_name]["group"]),
						int(anim_lookup[tile_name]["index"]))
			if bool(info.get("solid", false)):
				root.add_solid_rect(Rect2(x * tile_size, y * tile_size, tile_size, tile_size))

	root.setup_bounds(Vector2(w * tile_size, h * tile_size))

	# ---- extra collision -------------------------------------------------
	for rect in def.get("collision_rects", []):
		root.add_solid_rect(Rect2(float(rect[0]) * tile_size, float(rect[1]) * tile_size,
				float(rect[2]) * tile_size, float(rect[3]) * tile_size))

	# ---- objects ---------------------------------------------------------
	for obj in def.get("objects", []):
		var pos: Array = obj.get("pos", [0, 0])
		var px := float(pos[0]) * tile_size + tile_size * 0.5
		var py := float(pos[1]) * tile_size + tile_size
		root.spawn_object(str(obj.get("sprite", "")), Vector2(px, py), obj)
	# objects placed on the half tile (for props that need pixel precision)
	for obj in def.get("objects_px", []):
		var pos2: Array = obj.get("pos", [0, 0])
		root.spawn_object(str(obj.get("sprite", "")), Vector2(float(pos2[0]), float(pos2[1])), obj)

	# ---- landmarks -------------------------------------------------------
	for lm in def.get("landmarks", []):
		var pos: Array = lm.get("pos", [0, 0])
		root.spawn_landmark(lm, Vector2(float(pos[0]) * tile_size + tile_size * 0.5,
				float(pos[1]) * tile_size + tile_size * 0.5))

	# ---- interactables ---------------------------------------------------
	for it in def.get("interactables", []):
		var pos: Array = it.get("pos", [0, 0])
		var p := Vector2(
				float(pos[0]) * tile_size + tile_size * 0.5,
				float(pos[1]) * tile_size + tile_size * 0.5)
		root.spawn_interactable(it, p)

	# ---- npcs ------------------------------------------------------------
	for npc in def.get("npcs", []):
		var pos: Array = npc.get("pos", [0, 0])
		var p2 := Vector2(
				float(pos[0]) * tile_size + tile_size * 0.5,
				float(pos[1]) * tile_size + tile_size * 0.5)
		root.spawn_npc(npc, p2)

	# ---- exits -----------------------------------------------------------
	for ex in def.get("exits", []):
		var pos: Array = ex.get("pos", [0, 0])
		var p3 := Vector2(
				float(pos[0]) * tile_size + tile_size * 0.5,
				float(pos[1]) * tile_size + tile_size * 0.5)
		root.spawn_exit(ex, p3)

	# Every placed scenery prop gets a repeatable, non-destructive examine action.
	# A prop with its own authored action reuses that richer interaction instead.
	var prop_index := 0
	for obj in def.get("objects", []):
		var object_pos: Array = obj.get("pos", [0, 0])
		var world_pos := Vector2(float(object_pos[0]) * tile_size + tile_size * 0.5,
				float(object_pos[1]) * tile_size + tile_size)
		_spawn_prop_interaction(root, def, map_id, obj, world_pos, prop_index, tile_size)
		prop_index += 1
	for obj in def.get("objects_px", []):
		var object_pos: Array = obj.get("pos", [0, 0])
		var world_pos := Vector2(float(object_pos[0]), float(object_pos[1]))
		_spawn_prop_interaction(root, def, map_id, obj, world_pos, prop_index, tile_size)
		prop_index += 1

	root.finish_setup()
	return root


static func _spawn_prop_interaction(root: Node, def: Dictionary, map_id: String, obj: Dictionary,
		world_pos: Vector2, prop_index: int, tile_size: int) -> void:
	var sprite_name := str(obj.get("sprite", ""))
	if sprite_name == "" or _has_authored_object_action(def, sprite_name, world_pos, tile_size):
		return
	var sprite_def := Data.get_object(sprite_name)
	var names: Dictionary = sprite_def.get("inspect_name", {})
	var fallback_name := sprite_name.replace("_", " ").capitalize()
	var name_en := str(names.get("en", fallback_name))
	var name_id := str(names.get("id", fallback_name))
	var inspect_data := {
		"id": "prop_%s_%03d" % [map_id, prop_index],
		"kind": "inspect",
		"target": sprite_name,
		"title_en": name_en,
		"title_id": name_id,
		"text_en": ("Observe the shape and details of %s. Notice its place in the " +
				"surrounding environment.") % name_en,
		"text_id": ("Amati bentuk dan detail %s ini, lalu perhatikan letaknya " +
				"di lingkungan sekitar.") % name_id,
		"radius": 58.0,
	}
	root.call("spawn_interactable", inspect_data, world_pos)


static func _has_authored_object_action(
		def: Dictionary, sprite_name: String, object_pos: Vector2, tile_size: int) -> bool:
	for entry in def.get("interactables", []):
		if str(entry.get("sprite", "")) != sprite_name:
			continue
		var tile_pos: Array = entry.get("pos", [0, 0])
		var target_pos := Vector2(float(tile_pos[0]) * tile_size + tile_size * 0.5,
				float(tile_pos[1]) * tile_size + tile_size * 0.5)
		if object_pos.distance_to(target_pos) <= float(tile_size) * 0.6:
			return true
	return false


static func _build_tileset(tileset: Dictionary, _legend: Dictionary) -> TileSet:
	var ts := TileSet.new()
	var tile_size := int(tileset.get("tile_size", TILE))
	ts.tile_size = Vector2i(tile_size, tile_size)
	var atlas := TileSetAtlasSource.new()
	var region_name := str(tileset.get("region", "sumatra"))
	var tex_path := "res://assets/environments/tilesets/terrain_%s.png" % region_name
	if ResourceLoader.exists(tex_path):
		atlas.texture = load(tex_path)
	else:
		var fallback := Image.create(tile_size, tile_size, false, Image.FORMAT_RGBA8)
		fallback.fill(Color(0.5, 0.5, 0.5))
		atlas.texture = ImageTexture.create_from_image(fallback)
	atlas.texture_region_size = Vector2i(tile_size, tile_size)
	var cols := int(tileset.get("columns", 10))
	var tile_count := int(tileset.get("tiles", {}).size())
	if atlas.texture != null:
		var tex_w := atlas.texture.get_width()
		var tex_h := atlas.texture.get_height()
		for i in range(tile_count):
			var cx := i % cols
			var cy := i / cols
			if (cx + 1) * tile_size <= tex_w and (cy + 1) * tile_size <= tex_h:
				atlas.create_tile(Vector2i(cx, cy))
	ts.add_source(atlas, 0)
	return ts
