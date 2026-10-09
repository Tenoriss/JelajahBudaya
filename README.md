# Nusantara: Jejak Budaya

A 2D top-down cultural adventure through Indonesia, built with **Godot 4.x**.
You carry your grandmother's half-empty notebook across five regions, meet
people, help them with real work, and write down what you learn.

```
explore  ->  meet NPCs  ->  clues  ->  quest  ->  puzzle / challenge
        ->  culture discovery  ->  reward  ->  journal  ->  unlock area  ->  travel
```

## Browser preview

A lightweight, playable browser showcase uses the project's compiled maps, original pixel art, NPC portraits, dialogue, journal entries and audio. It includes walking, interactions, preview travel across all regions, sample memory/sequence challenges, and an **EN / ID language toggle** (Bahasa Indonesia is the default and the choice is remembered in the browser). The map modal has a region selector and a schematic route diagram with openable local destinations. The quest log filters by island, and a compact top-left quest-only note follows the current island, showing the quest title and the next clear action; completed quests are automatically struck through. Every placed scenery prop can also be examined with **E**, alongside the authored NPC, puzzle, note, pickup, landmark, save, and travel interactions. All preview text—including NPC interaction prompts and dialogue, quests and objectives, journal entries and source notes, inventory, regional-map labels, travel labels, notices, and sample puzzles—switches between English and Indonesian. Proper cultural names and formal source titles retain their original wording. This is a showcase rather than a Godot web export; the complete game systems run in the native Godot project.

From the repository root:

```bash
python3 tools/preview_server.py
```

Open `http://localhost:4173/` (the server redirects to the preview). Use the **EN / ID** toggle to switch languages. Use **WASD / arrows** to walk, **E** to talk or examine, **M** for the preview map, **J** for the journal, **Q** for the quest log, **I** for the satchel, **F** to toggle full screen, and **Shift** to hurry. Press **Esc** to leave full screen (or close an open dialog first). Click **Sound off / Suara mati** to hear the original region ambience and music.

## Running the game

1. Install **Godot 4.3 or newer** (standard build, no C# needed).
2. Open the project folder in the Godot editor (`project.godot` is in the root).
3. Press **F5** (or *Play*). The configured main scene is `res://scenes/main/game.tscn`.
4. To ship it: *Project → Export → Linux/Windows/macOS*. No plugins, no external
   dependencies and no network access are used.

The project runs in the `gl_compatibility` renderer with a fixed 1280×720
`canvas_items` stretch, so it behaves the same on a laptop iGPU.

## Controls

| Action | Keys |
| --- | --- |
| Walk | `W A S D` / arrow keys |
| Talk / examine / confirm | `E` or `Enter` |
| World map | `M` |
| Satchel (inventory) | `I` |
| Culture journal | `J` |
| Quest log / hint while in a puzzle | `H` |
| Pause menu | `Esc` |
| Sprint | `Shift` |
| Puzzle: hint / reset / leave | `H` / `R` / `Esc` |
| Dialogue: skip typing / advance | `E`, `Space` or click |

## What is in the game

* **22 hand-authored maps** across a prologue village and five regions —
  Sumatra, Java, Kalimantan, Sulawesi and Papua — with villages, markets,
  forests, lakes, rice terraces, rivers, a temple, a stilt village and a harbour.
* **44 quests** (8 per region plus a 3-part prologue), every one of them built
  around an interactive mechanic: you cook, weave, plait, carve, tune, tutor,
  irrigate, search, deduce and perform.
* **44 puzzles across 13 mechanics** — memory pairs, pattern copy, sequence,
  rhythm, rotating tiles, matching, logic deduction, cooking, crafting,
  exploration/clue boards, environmental flow, culture quiz and a timed festival
  game — with a 3-step hint system that costs a little Culture Points but never
  blocks progress, and a reset that never punishes.
* **55 journal entries** in 8 categories (Architecture, Textiles, Music,
  Food, Festivals, Craft, Oral Tradition, Environment), each naming the
  community it belongs to.
* **84 items**: quest items, collectibles (4 per region), souvenirs and everyday
  goods, all with original pixel-art icons.
* **31 NPCs** with names, roles, idle conversations, conditional dialogue,
  quest offers, turn-ins and a trader shop.
* Culture Points economy, a world map with per-region completion, openable
  island route maps and region-filtered quests, landmark discovery, fast travel,
  hidden areas, achievements, 3 save slots + autosave
  with corruption handling, day/night tint, weather in the wet regions, ambient
  audio beds, original music for every region, and a full 7-chapter story that
  ends at a festival back in the first village.

## Project layout

```
assets/        original art (tilesets, objects, characters, UI, item icons)
audio/         original music, ambience and sfx (generated, OGG)
data/          all content as JSON: regions, maps, route-map layouts, quests,
               dialogues, cultures, items, puzzles, npcs, achievements, endings
scenes/        main, player, npc, ui and minigame scenes (code-driven)
scripts/
  core/        Autoload managers (Data, Settings, Audio, Notify, Game, Save,
               Items, Culture, Quest, Achievements, Dialogue, Puzzle, World)
  ui/          screens: hud, dialogue, notes, inventory, journal, world map,
               quest log, pause, achievements, settings, saves, shop, cards
  world/       world builder, runtime map, interactables, landmarks, exits
  player/ npc/ player controller, NPC framework
  puzzles/     MinigameBase + 13 puzzle implementations
  main/        game root scene, title screen
tools/         Python generators for every asset + the content compiler
```

Everything the game shows comes from `data/*.json`, so new regions, quests,
maps, items or puzzles can be added without touching the engine-side code.
`tools/build_data.py` compiles the authoring modules in `tools/content/` into
those JSON files and validates every cross-reference (quest → NPC → map →
puzzle → item → culture) before writing.

## Regenerating assets and content

```bash
python3 tools/gen_terrain.py     # 5 region tilesets
python3 tools/gen_objects.py     # 78 environment objects
python3 tools/gen_characters.py  # player + 31 NPCs + portraits
python3 tools/gen_ui.py          # UI plates, buttons, icons
python3 tools/gen_items.py       # 34 item icons
python3 tools/gen_audio.py       # music + sfx (writes WAV)
python3 tools/to_ogg.py          # WAV -> OGG (soundfile)
python3 tools/build_data.py      # content modules -> data/*.json + validation
```

All art and audio in this repository is generated by these scripts: no external,
copied or placeholder assets, and no sampled or copyrighted music.

## Cultural notes

* Facts are attributed to the community they belong to (for example *ulos* is
  described as a Batak cloth, *noken* as Papuan, *tongkonan* as Toraja).
* Carvings, motifs, songs and patterns shown in the game are **original,
  abstract designs made for this game**. No specific sacred carving, motif or
  design is reproduced.
* Three journal entries carry `"verify": true` and are shown in the journal as
  *needs verification* — they are the ones a human should double-check against a
  published source before the game is used for teaching.
* The adventure story is fictional; the cultural information is written to be
  grounded, respectful and non-stereotyped.

## Known limitations

* No voice acting; dialogue is text only (with a typewriter speed setting).
* The archipelago and per-region route maps are schematic gameplay diagrams, not geographically accurate maps or surveys.
* Region boundaries are gameplay abstractions: one map per region stands in for
  the whole region, and communities are represented by shared, generic
  buildings rather than exact architecture.
* The shop trades items for Culture Points only; there is no currency duel or
  haggling mechanic.
* Weather is cosmetic (rain in the wet regions, mist in the highlands).
* Human review is still wanted for: the three `verify` journal entries, the
  Indonesian-language names and place spellings, and a full playtest pass on
  real hardware for difficulty balance.
