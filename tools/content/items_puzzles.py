"""Item catalogue and puzzle/mini-game definitions."""

# ------------------------------------------------------------------ items
# fields: name, category, region, icon, rarity, value, description, stack
I = []
def item(iid, name, category, region, icon, desc, rarity="common", value=5, stack=99):
    I.append({"id": iid, "name": name, "category": category, "region": region,
              "icon": "res://assets/ui/items/%s.png" % icon, "description": desc,
              "rarity": rarity, "value": value, "stack": stack})

# --- quest items -----------------------------------------------------------
item("jurnal_nenek", "Grandmother's Notebook", "quest", "prologue", "notebook",
     "A cloth-bound notebook with a few pages already written in a careful hand. "
     "Whoever carries it is expected to fill the rest.", "rare", 0, 1)
item("surat_izin", "Village Travel Letter", "quest", "prologue", "notebook",
     "A short letter with a stamp and a signature, asking the next village to receive you.", "uncommon", 0, 1)
item("benang_jaring", "Net Twine", "quest", "prologue", "thread",
     "A roll of tough twine for mending fishing nets.", "common", 4)
item("keranjang_kosong", "Empty Basket", "quest", "prologue", "rattan",
     "A plain woven basket, useful for carrying anything the village sends with you.", "common", 4)
item("keranjang_isi", "Basket of Village Gifts", "quest", "prologue", "rattan",
     "The basket now holds salt, coffee and dried fish - the village's gift to the road ahead.", "uncommon", 0, 1)
item("bibit_padi", "Rice Seedlings", "quest", "java", "seed",
     "Bundles of young rice plants ready to be pressed into the mud of a wet field.", "common", 6)
item("lilin_batik", "Batik Wax", "quest", "java", "pot",
     "A block of wax that smells faintly of resin; it melts clear and holds a line on cloth.", "common", 8)
item("canting", "Wax Pen", "quest", "java", "flute",
     "A small copper pen with a bamboo handle, used to draw fine lines of hot wax onto cloth.", "uncommon", 12)
item("tabuh", "Gamelan Mallet", "quest", "java", "drum",
     "A padded wooden mallet. The padding is what keeps the bronze sounding soft rather than sharp.", "common", 8)
item("naskah_wayang", "Wayang Story Note", "quest", "java", "notebook",
     "A page of cues and jokes in cramped handwriting, prepared for a night-long performance.", "uncommon", 10)
item("bumbu_tumpeng", "Tumpeng Ingredients", "quest", "java", "spices",
     "Turmeric, coconut, and the aromatics for a celebration cone of yellow rice.", "common", 8)
item("ukiran_kayu", "Carved Wood Panel", "quest", "sumatra", "carving",
     "An original abstract panel cut with a small knife. Its curves were invented for this game, "
     "not copied from any specific carving.", "uncommon", 15)
item("benang_songket", "Gold Thread", "quest", "sumatra", "thread",
     "A spool of shiny thread that is laid over the cloth instead of woven through it.", "uncommon", 18)
item("kain_ulos", "Woven Cloth", "quest", "sumatra", "cloth",
     "A warm, hand-woven cloth in deep reds and blacks, given as a blessing rather than sold.", "uncommon", 20)
item("bambu_saluang", "Bamboo Flute Blank", "quest", "sumatra", "flute",
     "A thin bamboo tube, cut to length and waiting for its finger holes.", "rare", 16)
item("piring_tari", "Dance Plates", "quest", "sumatra", "stone",
     "Two small ceramic plates, held in the palms during a harvest dance.", "rare", 14)
item("biji_kopi", "Highland Coffee Beans", "quest", "sumatra", "coffee",
     "Green coffee beans from the slopes around the lake, still smelling of the drying yard.", "common", 10)
item("bumbu_rendang", "Rendang Spice Bundle", "quest", "sumatra", "spices",
     "Chilli, ginger, turmeric, galangal and lemongrass, bundled in a banana leaf.", "common", 12)
item("mentega_kelapa", "Coconut Milk", "quest", "sumatra", "coconut",
     "Thick milk squeezed from grated coconut - the liquid that carries all the spice.", "common", 8)
item("rumpun_rotan", "Rattan Bundle", "quest", "kalimantan", "rattan",
     "Long flexible canes, still with their outer skin, ready to be split and soaked.", "common", 10)
item("getah_kemenyan", "Aromatic Resin", "quest", "kalimantan", "honey",
     "Lumps of tree resin that smell of smoke and sweetness when they burn.", "common", 14)
item("kayu_ukiran", "Carved House Post", "quest", "kalimantan", "totem",
     "A short post carved with original hooking scrolls - invented for this game, not copied.", "rare", 30)
item("benang_sasirangan", "Dye Thread", "quest", "kalimantan", "thread",
     "Strong thread used to tie cloth tightly before it goes into the dye bath.", "common", 10)
item("bibit_padi_ladang", "Dry Field Seed", "quest", "kalimantan", "seed",
     "A handful of seed rice kept for the dry fields, where the water comes only from the sky.", "common", 10)
item("papan_phinisi", "Ship Planking", "quest", "sulawesi", "wood",
     "A long board already shaped by hand and eye, ready to be fitted to a hull curve.", "uncommon", 22)
item("pasak_kayu", "Wooden Pegs", "quest", "sulawesi", "wood",
     "Hard wooden pins. A wooden ship is held together with these instead of iron nails.", "common", 12)
item("layar_kain", "Sail Cloth", "quest", "sulawesi", "cloth",
     "Heavy cloth, stitched and reinforced at the corners where the wind pulls hardest.", "common", 16)
item("batang_kolintang", "Kolintang Bar", "quest", "sulawesi", "gong",
     "One wooden bar of a tuned set; each bar rings a note when it is struck with a mallet.", "uncommon", 18)
item("benang_sutra", "Silk Yarn", "quest", "sulawesi", "silk",
     "Fine, strong yarn reeled by hand and dyed before it goes on the loom.", "uncommon", 24)
item("bumbu_coto", "Coto Spice Mix", "quest", "sulawesi", "spices",
     "Coriander, cumin, lemongrass and roasted peanut - the base of a thick beef soup.", "common", 14)
item("naskah_lontara", "Palm Leaf Note", "quest", "sulawesi", "notebook",
     "A palm-leaf strip with a line of old script scratched into it. Kept in the village archive.", "rare", 26)
item("serat_noken", "Bark Fibre", "quest", "papua", "thread",
     "Rough fibre stripped from inner bark, softened by soaking and beating.", "common", 10)
item("bibit_ubi", "Sweet Potato Cuttings", "quest", "papua", "seed",
     "Vine cuttings to be pushed into the dark soil of a highland garden bed.", "common", 10)
item("anyaman_tifa", "Drum Skin", "quest", "papua", "drum",
     "A stretched skin, scraped thin and warm to the touch, waiting for a drum body.", "common", 16)
item("gaung_papeda", "Papeda Fork", "quest", "papua", "wood",
     "A wooden fork cut with two prongs, used to lift sago porridge out of the bowl.", "common", 8)
item("serat_kulit_kayu", "Bark Cloth Square", "quest", "papua", "cloth",
     "A soft sheet beaten out of inner bark, with an original geometric pattern painted on it.", "uncommon", 20)
item("sagu_kering", "Dried Sago", "quest", "papua", "sago",
     "Dried sago starch in a leaf wrapper. Sago comes from the palm, not from a field.", "common", 8)
item("ikan_kuning", "Fish for Soup", "quest", "papua", "fish",
     "Fresh fish, ready to be simmered with turmeric and lime for papeda.", "common", 8)

# --- collectibles (4 per region, region sets) ------------------------------
item("col_ukiran_kecil", "Carved Motif Token", "collectibles", "sumatra", "carving",
     "A small wooden token cut with an abstract curve. One of four highland keepsakes.", "uncommon", 12)
item("col_benang_emas", "Gold Thread Skein", "collectibles", "sumatra", "thread",
     "A finger-sized skein of metallic thread, wrapped round a bamboo core.", "uncommon", 12)
item("col_talempong_chip", "Bronze Ding", "collectibles", "sumatra", "gong",
     "A little bronze disc that still rings faintly when it is tapped.", "rare", 18)
item("col_kopi_liar", "Wild Coffee Bean", "collectibles", "sumatra", "coffee",
     "A single roasted bean, dark and glossy, from a coffee tree that grows by itself.", "uncommon", 12)
item("col_lilin", "Wax Curl", "collectibles", "java", "pot",
     "A curl of batik wax, translucent at the thin edge.", "common", 10)
item("col_keping_gamelan", "Bronze Key Plate", "collectibles", "java", "gong",
     "A small bronze plate from a gong-chime, tuned to a note you cannot quite sing.", "rare", 20)
item("col_batu_candi", "Temple Stone Chip", "collectibles", "java", "stone",
     "A chip of grey stone with one corner of an abstract repeating pattern on it.", "uncommon", 14)
item("col_boneka_lidi", "Lidi Puppet", "collectibles", "java", "mask",
     "A little puppet cut from a palm rib and painted - an original design, not a wayang figure.", "uncommon", 14)
item("col_manik_dayak", "Bead", "collectibles", "kalimantan", "beads",
     "A single glass bead in red and white, the kind traded upriver for centuries.", "common", 10)
item("col_gelang_rotan", "Rattan Ring", "collectibles", "kalimantan", "rattan",
     "A bracelet of split rattan, sprung and worn smooth.", "common", 10)
item("col_damar", "Resin Lump", "collectibles", "kalimantan", "honey",
     "Hardened tree resin that smells of the forest when it is warmed in the hand.", "uncommon", 14)
item("col_ukiran_kecil_kl", "Carved Handle Piece", "collectibles", "kalimantan", "totem",
     "A small carved piece from a tool handle, cut with original hooking shapes.", "uncommon", 14)
item("col_keping_kolintang", "Kolintang Key", "collectibles", "sulawesi", "gong",
     "A short wooden bar; tap it and the note sits somewhere between two of your own.", "uncommon", 14)
item("col_serat_sutra", "Silk Thread", "collectibles", "sulawesi", "silk",
     "A metre of raw silk thread, strong enough to cut your fingers if you pull it fast.", "uncommon", 14)
item("col_kerang", "Harbour Shell", "collectibles", "sulawesi", "shell",
     "A ridged shell from the shallows, worn pale by sand and salt.", "common", 10)
item("col_kulit_lontara", "Script Fragment", "collectibles", "sulawesi", "notebook",
     "A scrap of palm leaf with three marks of old script on it.", "rare", 20)
item("col_noken_kecil", "Small Noken", "collectibles", "papua", "rattan",
     "A knotted bag the size of your fist, made for carrying small things.", "uncommon", 14)
item("col_serat_sagu_kol", "Sago Fibre Bundle", "collectibles", "papua", "sago",
     "A bundle of pale fibres left over after the starch has been washed out.", "common", 10)
item("col_batu_lukis", "Painted Stone", "collectibles", "papua", "stone",
     "A smooth river stone painted with an original geometric pattern in earth colours.", "uncommon", 14)
item("col_bulu_molt", "Moulted Plume", "collectibles", "papua", "feather",
     "A plume found on the forest floor, moulted naturally and picked up without disturbing "
     "any bird - protected species are never collected in this game.", "rare", 18)

# --- souvenirs (buy / gift items) -----------------------------------------
item("sou_mini_rumah", "Miniature Gadang House", "souvenirs", "sumatra", "carving",
     "A palm-sized model carved from soft wood with its roof sweeping into two points.", "uncommon", 40)
item("sou_kain_songket", "Songket Scarf", "souvenirs", "sumatra", "cloth",
     "A short scarf with metallic thread worked through it.", "uncommon", 55)
item("sou_kopi_pak", "Packet of Highland Coffee", "souvenirs", "sumatra", "coffee",
     "Ground coffee folded into paper, ready to give as a gift.", "common", 20)
item("sou_angklung_mini", "Small Angklung", "souvenirs", "java", "gong",
     "A two-tube bamboo shaker that plays one chord and no more.", "uncommon", 45)
item("sou_batik_syal", "Batik Cloth Square", "souvenirs", "java", "cloth",
     "A square of batik with an original pattern, folded and tied with string.", "uncommon", 50)
item("sou_gamelan_mini", "Miniature Gamelan", "souvenirs", "java", "gong",
     "A tiny bronze-look plate and mallet mounted on a wooden stand.", "rare", 70)
item("sou_tas_rotan", "Rattan Bag", "souvenirs", "kalimantan", "rattan",
     "A stiff little bag plaited from split cane, with a shoulder strap.", "uncommon", 45)
item("sou_sasirangan", "Tie-dye Cloth", "souvenirs", "kalimantan", "cloth",
     "A square of cloth dyed in rings and streaks where it was tied.", "uncommon", 50)
item("sou_topi_anyaman", "Wide Woven Hat", "souvenirs", "kalimantan", "rattan",
     "A broad hat that keeps both sun and rain off; it folds flat for the boat.", "common", 30)
item("sou_perahu_mini", "Model Sailing Ship", "souvenirs", "sulawesi", "boat",
     "A model of a two-masted wooden ship, pegged together the way the real hulls are.", "rare", 80)
item("sou_sutra_kecil", "Silk Sash", "souvenirs", "sulawesi", "silk",
     "A narrow hand-woven sash in deep colour, light enough to carry anywhere.", "uncommon", 60)
item("sou_kolintang_mini", "Pocket Kolintang", "souvenirs", "sulawesi", "gong",
     "Four wooden bars on a frame small enough to fit in a bag.", "uncommon", 55)
item("sou_noken_tas", "Knotted Noken", "souvenirs", "papua", "rattan",
     "A stretchy knotted bag; hang it from your head and the load rides on your back.", "uncommon", 50)
item("sou_ukiran_papua", "Abstract Carved Plaque", "souvenirs", "papua", "totem",
     "A small plaque carved with original curving shapes invented for this game.", "uncommon", 55)
item("sou_tifa_mini", "Small Drum", "souvenirs", "papua", "drum",
     "A hand-sized drum with a skin head, quiet enough for a hut but not for a festival.", "uncommon", 45)

# --- everyday items -------------------------------------------------------
item("bekal_jalan", "Travel Provisions", "items", "prologue", "rice",
     "Cooked rice, salted fish and a little sambal wrapped in banana leaf. Eat it before it spoils.", "common", 6)
item("air_minum", "Water Flask", "items", "prologue", "water",
     "A gourd of clean water. The highlands get cold; the lowlands get very hot.", "common", 4)
item("sambal_botol", "Bottle of Sambal", "items", "prologue", "chilli",
     "Pounded chilli relish in a small bottle. Dangerous in large amounts.", "common", 8)
item("lampu_minyak", "Oil Lamp", "items", "prologue", "lantern",
     "A small lamp with a clay body and a rag wick; it burns low but it burns all night.", "common", 10)
item("tali_tambang", "Coil of Rope", "items", "prologue", "rattan",
     "Twisted rope long enough to cross a stream or tie down a load.", "common", 12)
item("peta_lipat", "Folded Map", "items", "prologue", "notebook",
     "A hand-copied map of river mouths and roads, with one corner chewed by a rat.", "uncommon", 15)
item("obat_herbal", "Herbal Remedy", "items", "prologue", "leaf",
     "Bitter leaves and root boiled down. Tastes awful; works well enough.", "common", 10)
item("keranjang_bahu", "Shoulder Basket", "items", "prologue", "rattan",
     "A woven basket with a strap, for carrying things that do not fit in a bag.", "common", 14)
item("pisau_serbaguna", "Utility Knife", "items", "prologue", "blade",
     "A short straight blade in a wooden sheath, used for everything from peeling to sharpening pegs.", "common", 18)
item("pipa_bambu", "Water Bamboo", "items", "prologue", "water",
     "A length of bamboo cut between the joints and used for carrying water.", "common", 6)
item("kain_merah", "Red Cloth", "items", "prologue", "cloth",
     "A plain square of red cloth, useful for wrapping, carrying or signalling.", "common", 10)

ITEM_CATALOGUE = I


# ----------------------------------------------------------------- puzzles
# type must be one of Puzzle.SCENES keys:
#   memory pattern sequence rhythm tile match logic cooking crafting
#   exploration environment quiz nod
PZ = []
def puzzle(pid, ptype, title, desc, data, hints, culture=None, items=None, flag="", cp=None):
    PZ.append({"id": pid, "type": ptype, "title": title, "description": desc,
               "data": data, "hints": hints,
               "rewards": {"culture": culture or [], "items": items or [], "flag": flag}})

# ---- prologue -------------------------------------------------------------
puzzle("pz_notebook_pages", "memory",
       "Grandmother's Notebook",
       "Sort through the loose pages and match each pair that belongs together.",
       {"columns": 4, "cell": 140,
        "symbols": ["Front page", "River sketch", "Sawo leaf", "Village list",
                    "Old stamp", "Salt note"]},
       ["Pairs sit next to each other on the table, not across it.",
        "Two pages carry the same leaf pressed inside.",
        "The river sketch matches the page with two wavy lines."])

puzzle("pz_gotong_royong", "sequence",
       "Raising the Shed Together",
       "Put the steps of a village work-day in the right order.",
       {"items": ["Measure and mark the posts", "Cut and sharpen the posts",
                  "Raise the posts together", "Tie the cross beams",
                  "Lay the roof thatch", "Sweep the ground"],
        "order": [0, 1, 2, 3, 4, 5]},
       ["Nothing can be tied before the posts stand.",
        "The thatch goes on after the frame is tied.",
        "The sweep is always last."])

puzzle("pz_net_mend", "crafting",
       "Mending the Net",
       "Choose the right materials, then lay the mesh on the grid to match the pattern.",
       {"materials": ["Net twine", "Wooden shuttle", "Bamboo needle"],
        "wrong": ["Iron nail", "Batik wax", "Gold thread"],
        "size": 5,
        "target": [1,1,0,1,1, 1,0,1,0,1, 0,1,0,1,0, 1,0,1,0,1, 1,1,0,1,1]},
       ["Twine is tied with a shuttle, not nailed.",
        "The pattern is symmetrical left to right.",
        "The middle row has fewer holes than the rows above and below."])

# ---- sumatra --------------------------------------------------------------
puzzle("pz_carving_memory", "memory",
       "The Carved Wall",
       "Match the pairs of carved panels on the wall of the house.",
       {"columns": 4, "cell": 140,
        "symbols": ["Curved horn", "Spiral", "Leaf row", "Double wave",
                    "Crossed stick", "Rope line"]},
       ["The panels are paired by motif, not by size.",
        "Two of them follow the same curve as the roof edge.",
        "The crossed stick and the rope line are partners."])

puzzle("pz_rendang", "cooking",
       "Cooking Rendang",
       "Pick the right ingredients, put the steps in order, then watch the fire.",
       {"ingredients": ["Beef", "Coconut milk", "Chilli", "Ginger", "Turmeric", "Lemongrass"],
        "bad": ["Chocolate", "Sweet soy sauce"],
        "steps": ["Pound the spices", "Simmer the meat with the spice paste",
                  "Add the coconut milk", "Cook until the sauce is nearly dry"],
        "order": [0, 1, 2, 3],
        "timing": {"width": 0.22, "speed": 250}},
       ["Six things belong in the pot and two do not.",
        "The spice paste goes in before the coconut milk.",
        "When the marker stays in the golden band the sauce is right."],
       culture=["rendang"], items=["bekal_jalan"])

puzzle("pz_saluang_song", "rhythm",
       "The Saluang Song",
       "An old melody for the bamboo flute: keep the beat as the notes pass the golden line.",
       {"beats": [0.8, 1.2, 1.6, 2.2, 2.6, 3.0, 3.6, 4.0, 4.4, 5.0, 5.4, 5.8],
        "speed": 170},
       ["Press space (or click) exactly as a note reaches the gold line.",
        "The melody starts slowly and speeds up in the middle.",
        "You only need to hit most of the notes, not every one."],
       culture=["saluang"], items=["bambu_saluang"])

puzzle("pz_ulos_pattern", "crafting",
       "Weaving the Cloth",
       "Gather the loom materials, then copy the abstract weaving pattern.",
       {"materials": ["Cotton yarn", "Backstrap loom", "Shuttle"],
        "wrong": ["Plastic sheet", "Nail polish"],
        "size": 5,
        "target": [0,1,0,1,0, 1,1,0,1,1, 0,0,1,0,0, 1,1,0,1,1, 0,1,0,1,0]},
       ["Thread is woven; plastic has no place on a loom.",
        "The pattern is mirrored top and bottom.",
        "The middle row is a single line of light."],
       culture=["ulos"], items=["kain_ulos"])

puzzle("pz_talempong_pattern", "pattern",
       "The Talempong Set",
       "Watch which gongs are struck, then strike the same ones.",
       {"size": 4, "pattern": [1, 6, 9, 12, 15], "preview_time": 2.4, "cell": 88},
       ["The lit gongs form a diagonal line.",
        "There are five of them, from top left to bottom right.",
        "You may strike them in any order once you remember them."],
       culture=["talempong"])

puzzle("pz_danau_search", "exploration",
       "Where Did the Cargo Go?",
       "Read the clues and mark the spot on the lakeside where the cargo drifted ashore.",
       {"clues": ["The boy saw the basket pass the reed bed on the north side.",
                  "It did not reach the rocks - those are in the south.",
                  "The cake seller's stall is east of the landing.",
                  "It was pulled out just west of the cake stall."],
        "answer": [0.42, 0.3], "tolerance": 0.14},
       ["North is towards the top of the picture.",
        "Reeds grow where the water is shallow.",
        "Start from the stall and walk west."],
       culture=["danau_toba"])

puzzle("pz_piring_steps", "sequence",
       "The Plate Dance",
       "Arrange the dance steps in the order they are performed.",
       {"items": ["Bow to the musicians", "Step the first pattern",
                  "Turn with the plates lifted", "Quick steps between the plates",
                  "Step onto the plates", "Bow again to close"],
        "order": [0, 1, 2, 3, 4, 5]},
       ["A performance opens with respect and closes with it.",
        "The fast steps come before the final, most difficult part.",
        "The plates are stepped on last, never first."],
       culture=["tari_piring"])

puzzle("pz_pasar_match", "match",
       "Market Day",
       "Match each good with the stall that sells it.",
       {"pairs": [["Gold thread", "Weaving stall"], ["Chilli", "Spice stall"],
                  ["Coffee beans", "Drying yard"], ["Woven cloth", "Cloth stall"],
                  ["Bronze ding", "Music stall"]]},
       ["Each good belongs with the trade that makes it.",
        "Thread goes where something is being woven.",
        "Bronze belongs with music."],
       culture=["songket_palembang"], items=["sou_kain_songket", "col_benang_emas"],
       flag="sumatra_market_done")

# ---- java -----------------------------------------------------------------
puzzle("pz_tumpeng", "cooking",
       "The Celebration Rice",
       "Choose the ingredients for a cone of yellow rice, then finish it on the fire.",
       {"ingredients": ["Rice", "Turmeric", "Coconut milk", "Lemongrass", "Fried shallots"],
        "bad": ["Chocolate bar", "Cheese slice"],
        "steps": ["Wash the rice", "Steam the rice with turmeric and coconut milk",
                  "Shape the cone", "Arrange the side dishes around it"],
        "order": [0, 1, 2, 3],
        "timing": {"width": 0.2, "speed": 280}},
       ["Turmeric is what makes the rice yellow.",
        "Rice steams before it is shaped; it cannot hold a cone while wet and loose.",
        "Side dishes are arranged after the cone is standing."],
       culture=["tumpeng"], items=["bumbu_tumpeng"])

puzzle("pz_batik", "crafting",
       "Drawing with Wax",
       "Gather the batik tools, then match the pattern on the cloth.",
       {"materials": ["Cotton cloth", "Batik wax", "Wax pen"],
        "wrong": ["Spray paint", "Stapler"],
        "size": 5,
        "target": [1,0,1,0,1, 0,1,1,1,0, 1,1,0,1,1, 0,1,1,1,0, 1,0,1,0,1]},
       ["Wax resists dye, so waxed areas stay light.",
        "This pattern repeats diagonally.",
        "Every corner of the grid is waxed."],
       culture=["batik"], items=["lilin_batik", "canting"])

puzzle("pz_gamelan", "rhythm",
       "Gamelan Rehearsal",
       "Follow the drum: strike as each note crosses the line.",
       {"beats": [1.0, 1.45, 1.9, 2.35, 2.9, 3.4, 3.9, 4.4, 5.0, 5.5, 6.0, 6.5, 7.0],
        "speed": 175},
       ["Watch the drum, not your hands.",
        "The notes come in groups of four.",
        "Missing one note will not stop the rehearsal."],
       culture=["gamelan"], items=["tabuh"])

puzzle("pz_sawah_water", "environment",
       "Water for the Terrace",
       "Rotate the channels so water runs from the spring to the lowest field.",
       {"size": 4, "source": [0, 0], "target": [3, 3],
        "grid": [[[0, 0], [0, 1], [1, 3], [0, 1]],
                 [[1, 1], [1, 0], [0, 1], [1, 2]],
                 [[0, 1], [1, 3], [1, 0], [0, 0]],
                 [[1, 0], [0, 1], [1, 2], [1, 3]]]},
       ["Two pieces have to join the spring before anything else flows.",
        "Water only moves where two connections meet.",
        "The lowest field is the bottom right corner."],
       culture=["sawah"], items=["bibit_padi"])

puzzle("pz_wayang_quiz", "quiz",
       "Stories Behind the Screen",
       "Answer the questions the puppeteer asks about the stories you have recorded.",
       {"questions": [
           {"q": "What is the puppeteer of a wayang kulit performance called?",
            "options": ["Dalang", "Dukun", "Pawang"], "answer": 0,
            "fact": "The dalang voices every character and leads the musicians."},
           {"q": "Where does the audience of a wayang kulit watch the story?",
            "options": ["On the same side as the puppets", "On the shadow side of the screen",
                        "Outside the building"], "answer": 1,
            "fact": "The puppets cast shadows onto a lit screen for the audience."},
           {"q": "How long can a wayang performance last?",
            "options": ["About ten minutes", "One hour", "All night"], "answer": 2,
            "fact": "Performances traditionally run through the night."}]},
       ["Think about where the light is.",
        "The screen is lit from behind the puppeteer.",
        "A night performance is the traditional form."],
       culture=["wayang_kulit"], items=["naskah_wayang"])

puzzle("pz_angklung_order", "sequence",
       "Assembling the Angklung",
       "Put the steps of playing in a group in the right order.",
       {"items": ["Check that every tube is in its frame", "Agree the beat with a nod",
                  "Shake on your turn only", "Hold the note while others play",
                  "Stop together at the signal"],
        "order": [0, 1, 2, 3, 4]},
       ["Nothing can be played before the instruments are checked.",
        "One shake, one note - the timing has to be agreed first.",
        "Everyone stops together, not one by one."],
       culture=["angklung"], items=["sou_angklung_mini"])

puzzle("pz_candi_relief", "tile",
       "The Stone Gallery",
       "Rotate the stone panels until every carved block faces the right way.",
       {"size": 3,
        "start": [[0, 1, 2], [3, 0, 1], [2, 3, 0]],
        "goal": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
       ["Each block only needs turning, never moving.",
        "Click a block once to turn it a quarter turn.",
        "Work row by row from the top."],
       culture=["borobudur"])

puzzle("pz_javanese_market", "match",
       "The Morning Market",
       "Match each stall with what it sells before the market packs up.",
       {"pairs": [["Turmeric rice", "Food stall"], ["Wax pen", "Batik stall"],
                  ["Padded mallet", "Gamelan stall"], ["Rice seedlings", "Seed seller"],
                  ["Fan", "Dance troupe"]]},
       ["Each object points at the trade it belongs to.",
        "The mallet is padded so the bronze rings soft.",
        "Seedlings come from whoever grows them."],
       culture=["rumah_joglo"], items=["sou_batik_syal", "col_batu_candi"],
       flag="java_market_done")

# ---- kalimantan -----------------------------------------------------------
puzzle("pz_roof_plait", "crafting",
       "Weaving the Roof Panel",
       "Choose the right materials and plait the panel to match the pattern.",
       {"materials": ["Rattan strips", "Palm leaves", "Water for soaking"],
        "wrong": ["Steel wire", "Batik wax"],
        "size": 5,
        "target": [1,1,1,1,1, 1,0,0,0,1, 1,0,1,0,1, 1,0,0,0,1, 1,1,1,1,1]},
       ["Rattan is soaked so it bends without cracking.",
        "The pattern has a hollow centre.",
        "The outer ring is completely filled."],
       culture=["rumah_panjang"], items=["rumpun_rotan"])

puzzle("pz_karungut", "rhythm",
       "A Sung Story",
       "Sing the verses in time: hit the beat as the syllables pass.",
       {"beats": [0.9, 1.3, 1.7, 2.1, 2.7, 3.1, 3.5, 3.9, 4.5, 4.9, 5.3, 5.7, 6.3],
        "speed": 165},
       ["Karungut keeps a steady pulse; listen to the drum first.",
        "The phrase groups are short, then a longer pause.",
        "You can miss a syllable and still finish the verse."],
       culture=["karungut"], items=["anyaman_tifa"])

puzzle("pz_river_flow", "environment",
       "The Blocked Channel",
       "Turn the channels so the river water reaches the village landing.",
       {"size": 4, "source": [0, 2], "target": [3, 1],
        "grid": [[[1, 0], [1, 1], [1, 2], [1, 3]],
                 [[0, 0], [1, 3], [0, 0], [1, 1]],
                 [[1, 1], [0, 1], [1, 0], [1, 0]],
                 [[1, 3], [1, 0], [1, 2], [1, 1]]]},
       ["The spring is on the left bank, halfway up.",
        "A channel that points away from the next one blocks the whole line.",
        "The landing sits just above the middle of the right edge."],
       culture=["hutan_kalimantan"], items=["peta_lipat"])

puzzle("pz_sasirangan", "pattern",
       "Tie-dye Pattern",
       "Watch the tied cloth pattern, then tie the same squares.",
       {"size": 4, "pattern": [0, 3, 5, 6, 9, 10, 12, 15], "preview_time": 2.6, "cell": 88},
       ["The ties form a ring around the middle.",
        "Two squares sit in opposite corners.",
        "Count eight ties, not six."],
       culture=["sasirangan"], items=["benang_sasirangan", "sou_sasirangan"])

puzzle("pz_mandau_tools", "memory",
       "Tools of the Workshop",
       "Match the pairs of tools on the workbench.",
       {"columns": 4, "cell": 140,
        "symbols": ["Work blade", "Sheath pin", "Sharpening stone", "Rattan strip",
                    "Oil cloth", "Wood mallet"]},
       ["Each tool has exactly one twin.",
        "The sharpening stone pairs with nothing metal.",
        "Six pairs, twelve cards."],
       culture=["mandau"], items=["pisau_serbaguna"])

puzzle("pz_soto_banjar", "cooking",
       "Soto from the River Market",
       "Choose the soup ingredients and finish the broth at the right moment.",
       {"ingredients": ["Chicken", "Cinnamon", "Star anise", "Clove", "Rice cake", "Lime"],
        "bad": ["Whipped cream", "Chocolate"],
        "steps": ["Boil the chicken for the broth", "Add the whole spices",
                  "Simmer until it smells sweet", "Serve with rice cake and lime"],
        "order": [0, 1, 2, 3],
        "timing": {"width": 0.24, "speed": 260}},
       ["The aromatic spices go in whole and come out before serving.",
        "Broth first, spices second.",
        "Lime goes in the bowl, not the pot."],
       culture=["kuliner_kalimantan"], items=["bekal_jalan"])

puzzle("pz_pasar_logic", "logic",
       "Which Boat Carries What?",
       "Read the boatmen's statements and work out which boat carries the salt.",
       {"clues": ["Three boats lie at the landing: A, B and C.",
                  "Boat A carries fruit, or so its owner says.",
                  "Boat C is moored next to the one carrying salt.",
                  "Boat B is moored at the far end, away from both others."],
        "options": ["Boat A", "Boat B", "Boat C"], "answer": 2,
        "explain": "B and A cannot both be next to the salt, and A is fruit, so C carries it."},
       ["The far end has only one neighbour.",
        "A is fruit, so the salt is not in A.",
        "Who is left moored beside A?"],
       culture=["pasar_terapung"], items=["keranjang_bahu"])

puzzle("pz_gantar_steps", "sequence",
       "Planting Dance",
       "Put the planting steps in order as the dancers do them.",
       {"items": ["Clear the ground", "Make holes with the dibble stick",
                  "Drop in the seed", "Cover the seed", "Stamp the soil firm"],
        "order": [0, 1, 2, 3, 4]},
       ["Nothing is planted before the ground is cleared.",
        "Seed goes into a hole, never on top of the soil.",
        "The last movement presses the earth down."],
       culture=["tari_gantar"], items=["bibit_padi_ladang", "col_manik_dayak"],
       flag="kalimantan_planting_done")

# ---- sulawesi -------------------------------------------------------------
puzzle("pz_tongkonan_carve", "tile",
       "Carving the Gable",
       "Turn the carved panels until the gable pattern matches.",
       {"size": 3,
        "start": [[3, 2, 1], [0, 3, 2], [1, 0, 3]],
        "goal": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
       ["Start with the top row and leave it alone once it is right.",
        "Each click is a quarter turn clockwise.",
        "The centre panel also needs turning."],
       culture=["tongkonan"], items=["ukiran_kayu"])

puzzle("pz_phinisi_hull", "crafting",
       "Laying the Hull",
       "Choose the shipbuilding materials and lay out the planks.",
       {"materials": ["Shaped planking", "Wooden pegs", "Palm fibre caulking"],
        "wrong": ["Steel nails", "Plastic sheet"],
        "size": 5,
        "target": [1,1,1,1,1, 0,1,1,1,0, 0,1,0,1,0, 0,1,0,1,0, 1,0,0,0,1]},
       ["No iron goes into a wooden hull.",
        "The pattern narrows towards the keel.",
        "The bottom row is the keel line: two separate points."],
       culture=["phinisi"], items=["papan_phinisi", "pasak_kayu"])

puzzle("pz_kolintang_tune", "pattern",
       "Tuning the Kolintang",
       "Watch which bars are struck, then strike the same ones.",
       {"size": 4, "pattern": [4, 5, 10, 11], "preview_time": 2.0, "cell": 92},
       ["The lit bars form a small square in the middle.",
        "Four bars, not three.",
        "You may strike them in any order."],
       culture=["kolintang"], items=["batang_kolintang"])

puzzle("pz_coto", "cooking",
       "Coto Makassar",
       "Pick the spices for the soup, order the steps, and stop the boil at the right moment.",
       {"ingredients": ["Beef", "Ground peanut", "Coriander", "Cumin", "Lemongrass", "Rice cake"],
        "bad": ["Vanilla extract", "Butter"],
        "steps": ["Boil the beef until tender", "Grind and add the spice mix",
                  "Stir in the ground peanut", "Serve with rice cake"],
        "order": [0, 1, 2, 3],
        "timing": {"width": 0.2, "speed": 290}},
       ["Peanut is what thickens the broth.",
        "Spices go in after the meat is tender.",
        "Stop the boil while the band is gold."],
       culture=["coto_makassar"], items=["bumbu_coto"])

puzzle("pz_pakarena", "rhythm",
       "The Fan Dance",
       "Move with the drum: hit each beat as it crosses the line.",
       {"beats": [1.0, 1.5, 2.0, 2.5, 3.2, 3.7, 4.2, 4.7, 5.4, 5.9, 6.4, 6.9],
        "speed": 160},
       ["The drum leads; the dancers follow it, not a count.",
        "The beats come in pairs with a gap between.",
        "Slow is correct here - the dance is deliberately unhurried."],
       culture=["tari_pakarena"], items=["sou_sutra_kecil"])

puzzle("pz_lontara_logic", "logic",
       "Reading the Palm Leaf",
       "Use the marks on the palm leaf to work out which line belongs to which record.",
       {"clues": ["Four records: genealogy, law, diary, land.",
                  "The leaf with the longest line is the genealogy.",
                  "The law leaf is the only one with a double mark.",
                  "The diary is shorter than the land record."],
        "options": ["Diary", "Law", "Genealogy", "Land record"], "answer": 3,
        "explain": "The land record is not the longest, not double-marked and not the shortest."},
       ["Compare the lengths before the marks.",
        "The double mark is unique to one record.",
        "Whatever is left is the land record."],
       culture=["lontara"], items=["naskah_lontara", "col_kulit_lontara"])

puzzle("pz_bajo_search", "exploration",
       "Where the Fish Are",
       "Read the boats' reports and mark the fishing ground on the map.",
       {"clues": ["The water shallows near the stilt walkway on the west side.",
                  "Fish were seen where the reef meets the deep channel.",
                  "The channel runs south of the village.",
                  "The catch was taken just north of the channel, near the reef edge."],
        "answer": [0.35, 0.62], "tolerance": 0.13},
       ["West is the left side of the map.",
        "North is up.",
        "The fishing ground sits between the village and the channel."],
       culture=["bajo_village"])

puzzle("pz_harbour_match", "match",
       "Ports and Cargo",
       "Match each cargo with the port it left from.",
       {"pairs": [["Silk sash", "Sengkang"], ["Wooden ship", "Tanaberu"],
                  ["Palm leaf record", "Makassar"], ["Sago flour", "Maluku boats"],
                  ["Coffee", "Highland road"]]},
       ["Each cargo names a place you have already visited or heard about.",
        "Silk comes from where it is woven.",
        "Sago travels by boat, never by road."],
       culture=["sutra_sengkang"], items=["sou_perahu_mini", "col_kerang"],
       flag="sulawesi_harbour_done")

# ---- papua ----------------------------------------------------------------
puzzle("pz_honai_build", "crafting",
       "Building the Honai",
       "Gather the right materials and lay out the roof thatch.",
       {"materials": ["Wooden posts", "Thatch grass", "Bark rope"],
        "wrong": ["Glass pane", "Brick"],
        "size": 5,
        "target": [0,0,1,0,0, 0,1,1,1,0, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1]},
       ["A honai roof is a cone of thatch, thick at the base.",
        "The pattern widens as it goes down.",
        "The bottom three rows are completely filled."],
       culture=["honai"], items=["col_noken_kecil"])

puzzle("pz_noken_knot", "memory",
       "Knots of the Noken",
       "Match the pairs of knots used to make the bag.",
       {"columns": 4, "cell": 140,
        "symbols": ["Loop knot", "Double knot", "Slip knot", "Square knot",
                    "Overhand knot", "Chain knot"]},
       ["Six knots, twelve cards.",
        "The slip knot is the one that comes undone with a pull.",
        "Work across the top row first."],
       culture=["noken"], items=["serat_noken"])

puzzle("pz_papeda", "cooking",
       "Papeda and Fish Soup",
       "Choose the right ingredients, stir in order, and stop the boil at the right moment.",
       {"ingredients": ["Sago starch", "Water", "Fish", "Turmeric", "Lime", "Salt"],
        "bad": ["Instant noodles", "Cream"],
        "steps": ["Boil the water", "Stir in the sago starch slowly",
                  "Keep stirring until it turns clear", "Simmer the fish soup"],
        "order": [0, 1, 2, 3],
        "timing": {"width": 0.2, "speed": 270}},
       ["Sago thickens all at once if the starch goes in too fast.",
        "Stirring is the whole trick.",
        "Stop while the marker is inside the gold band."],
       culture=["papeda"], items=["sagu_kering", "gaung_papeda"])

puzzle("pz_tifa_pattern", "pattern",
       "Drum Call",
       "Watch the drum call, then answer on the same skins.",
       {"size": 4, "pattern": [0, 2, 5, 7, 8, 13], "preview_time": 2.4, "cell": 90},
       ["The call starts at the top corner and closes at the bottom.",
        "Six strikes, not eight.",
        "You may play them in any order to answer."],
       culture=["tifa"], items=["anyaman_tifa", "sou_tifa_mini"])

puzzle("pz_valley_ditches", "environment",
       "Watering the Gardens",
       "Turn the ditches so the stream reaches the sweet potato beds.",
       {"size": 4, "source": [1, 0], "target": [2, 3],
        "grid": [[[1, 0], [0, 0], [1, 1], [0, 0]],
                 [[1, 3], [1, 1], [1, 0], [1, 0]],
                 [[0, 1], [1, 0], [1, 3], [1, 2]],
                 [[1, 0], [1, 1], [0, 1], [1, 3]]]},
       ["The stream enters near the top, one across from the corner.",
        "Highland gardens are drained, not flooded, so the ditch must keep running.",
        "The beds are in the bottom row, middle column."],
       culture=["baliem_valley"], items=["bibit_ubi"])

puzzle("pz_sentani_find", "exploration",
       "Something by the Lake",
       "Read the villagers' directions and mark the place on the lakeshore.",
       {"clues": ["The old canoe is on the north shore of the lake.",
                  "The painted stones were gathered east of the canoe.",
                  "The fish drying racks stand south of the painted stones.",
                  "The person you are looking for sits between the drying racks and the water."],
        "answer": [0.68, 0.55], "tolerance": 0.13},
       ["North is up, east is right.",
        "Move down from the painted stones to reach the racks.",
        "The lake is towards the bottom of the map."],
       culture=["danau_sentani"])

puzzle("pz_barkcloth", "sequence",
       "Making Bark Cloth",
       "Put the steps of making bark cloth in the right order.",
       {"items": ["Strip the inner bark", "Soak the bark", "Beat it with a mallet",
                  "Dry the sheet", "Paint the pattern"],
        "order": [0, 1, 2, 3, 4]},
       ["The bark is only beaten after it has been soaked.",
        "Painting comes last of all.",
        "Nothing is dried before it is flat."],
       culture=["kain_kulit_kayu"], items=["serat_kulit_kayu"])

puzzle("pz_bird_logic", "logic",
       "Watching, Not Catching",
       "From the watchers' notes, work out which bird the group is watching.",
       {"clues": ["The bird displays at dawn, not at midday.",
                  "It holds the plumes up in a fan above its head.",
                  "It is not the one that sings from the same branch all morning.",
                  "The watchers never catch or cage anything."],
        "options": ["The dawn displaying bird", "The one singing from the branch",
                    "The pale bird by the water"],
        "answer": 0,
        "explain": "Only the dawn bird folds its plumes into a fan."},
       ["Notes are about behaviour, not about catching.",
        "The display happens at dawn.",
        "Choose the bird the notes describe."],
       culture=["burung_cenderawasih"], items=["col_bulu_molt"])

puzzle("pz_quiz_festival", "quiz",
       "The Keeping of Records",
       "The last test: answer questions from across the whole journey.",
       {"questions": [
           {"q": "Which community builds the rumah gadang with its sweeping roof?",
            "options": ["Minangkabau", "Toraja", "Dani"], "answer": 0,
            "fact": "The rumah gadang is the Minangkabau house of West Sumatra."},
           {"q": "What makes batik patterns?",
            "options": ["Wax resisting dye", "Printed stickers", "Painted ink alone"],
            "answer": 0, "fact": "Wax blocks the dye, so waxed areas stay light."},
           {"q": "What is a noken made from?",
            "options": ["Plastic rope", "Bark and leaf fibre", "Cotton factory thread"],
            "answer": 1, "fact": "Noken is knotted or woven from natural fibre."},
           {"q": "A pinisi hull is fastened how?",
            "options": ["Welded steel", "Wooden pegs", "Glue"], "answer": 1,
            "fact": "Wooden pegs and caulking hold a pinisi together."},
           {"q": "Why is rendang cooked until nearly dry?",
            "options": ["So it keeps without refrigeration", "Because it looks better",
                        "To make it sweet"], "answer": 0,
            "fact": "Slow drying means it keeps for days - useful for travel and celebrations."},
           {"q": "Sago starch comes from where?",
            "options": ["A rice field", "The trunk of a sago palm", "A wheat mill"],
            "answer": 1, "fact": "Sago is washed out of the pith of a sago palm trunk."}]},
       ["Every answer is something a person told you on the road.",
        "You can retry the quiz as many times as you like.",
        "Two of these were taught by cooks, two by builders."],
       culture=["gotong_royong", "sambal"], items=["jurnal_nenek"],
       flag="quiz_passed")
