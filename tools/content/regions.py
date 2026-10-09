"""Region, chapter, ending and achievement definitions."""

REGION_ORDER = ["prologue", "sumatra", "java", "kalimantan", "sulawesi", "papua"]

REGIONS = {
    "prologue": {
        "id": "prologue", "name": "Kampung Awal", "music": "prologue",
        "tagline": "The journey begins at home",
        "intro": "A small coastal village where the storyteller's satchel has been kept for "
                 "years. Your grandmother's notebook is waiting to be filled.",
        "requires": "", "requires_percent": 0,
    },
    "sumatra": {
        "id": "sumatra", "name": "Sumatra", "music": "sumatra",
        "tagline": "Highlands, long houses and the sound of the saluang",
        "intro": "Volcanic highlands, rainforest rivers and villages of carved timber. The "
                 "island is home to many communities - Minangkabau, Batak, Aceh, Lampung, "
                 "Palembang and many more - each with their own houses, cloths and songs.",
        "requires": "prologue", "requires_percent": 40,
    },
    "java": {
        "id": "java", "name": "Java", "music": "java",
        "tagline": "Rice terraces, gamelan and temple stone",
        "intro": "Terraced rice fields, market towns and the quiet bronze voices of the "
                 "gamelan. Javanese, Sundanese, Betawi and Tengger communities share this "
                 "island with nine-hundred-year-old temples.",
        "requires": "sumatra", "requires_percent": 45,
    },
    "kalimantan": {
        "id": "kalimantan", "name": "Kalimantan", "music": "kalimantan",
        "tagline": "Rivers, rainforest and longhouses",
        "intro": "Great rivers cut through the rainforest, and villages sit on stilts above "
                 "the water. Dayak communities, Banjar river towns and coastal Malay villages "
                 "each keep their own crafts and stories.",
        "requires": "java", "requires_percent": 45,
    },
    "sulawesi": {
        "id": "sulawesi", "name": "Sulawesi", "music": "sulawesi",
        "tagline": "Saddle roofs and the sea",
        "intro": "A shapeshifting island of mountains and deep bays. Toraja highlands, Bugis "
                 "and Makassar harbours, Minahasa gardens and Bajo stilt villages all face "
                 "the sea in their own way.",
        "requires": "kalimantan", "requires_percent": 45,
    },
    "papua": {
        "id": "papua", "name": "Papua", "music": "papua",
        "tagline": "Mountains, rivers and a thousand languages",
        "intro": "Highland valleys ringed by mountains, wide rivers and coastal villages. "
                 "Papua is home to hundreds of communities - Dani, Asmat, Sentani, Biak and "
                 "many others - each with their own language and traditions.",
        "requires": "sulawesi", "requires_percent": 45,
    },
}

CHAPTERS = [
    {"index": 1, "title": "Awal Perjalanan", "subtitle": "The notebook opens",
     "text": "Your grandmother left one request: travel, and write down what people tell you.",
     "region": "prologue"},
    {"index": 2, "title": "Jejak Sumatra", "subtitle": "Highlands and rivers",
     "text": "The highland road leads to carved houses and a festival that must not be late.",
     "region": "sumatra"},
    {"index": 3, "title": "Tanah Jawa", "subtitle": "Bronze and rice",
     "text": "In the shadow of the temples, an old melody waits to be played again.",
     "region": "java"},
    {"index": 4, "title": "Di Antara Sungai dan Hutan", "subtitle": "Down the great river",
     "text": "The river keeps what it takes - unless someone knows how to read it.",
     "region": "kalimantan"},
    {"index": 5, "title": "Tanah yang Menghadap Laut", "subtitle": "Sails and saddle roofs",
     "text": "Harbour towns and hill villages trade more than goods: they trade stories.",
     "region": "sulawesi"},
    {"index": 6, "title": "Timur Nusantara", "subtitle": "Mountain and coast",
     "text": "To the east, the notebook finds the oldest stories of all.",
     "region": "papua"},
    {"index": 7, "title": "Jejak yang Menyatukan", "subtitle": "One archipelago",
     "text": "Every page written so far points to the same thing: none of it is separate.",
     "region": "papua"},
]

ENDINGS = {
    "ending_nusantara": {
        "title": "Jejak yang Menyatukan",
        "dialogue": "ending_finale",
        "text": "The notebook is full, and the last page says what the whole journey has been "
                "showing: Indonesia is not one culture, and it is not a hundred separate ones "
                "either. It is people who have always traded, borrowed, argued and celebrated "
                "together across the water.",
    }
}

ACHIEVEMENTS = {
    "first_step": {"name": "First Step", "description": "Complete your first quest.",
                   "condition": {"quests_completed": 1}, "icon": "flag"},
    "curious_traveler": {"name": "Curious Traveller", "description": "Discover 10 journal entries.",
                         "condition": {"culture_discovered": 10}, "icon": "journal"},
    "student_of_stories": {"name": "Student of Stories", "description": "Discover 30 journal entries.",
                           "condition": {"culture_discovered": 30}, "icon": "journal"},
    "nusantara_explorer": {"name": "Nusantara Explorer", "description": "Visit all five regions.",
                           "condition": {"regions_visited": 5}, "icon": "map"},
    "collector": {"name": "Collector", "description": "Find 15 collectibles.",
                  "condition": {"collectibles": 15}, "icon": "bag"},
    "puzzle_master": {"name": "Puzzle Master", "description": "Solve 20 puzzles.",
                      "condition": {"puzzles_completed": 20}, "icon": "puzzle"},
    "puzzler": {"name": "Puzzler", "description": "Solve your first puzzle.",
                "condition": {"puzzles_completed": 1}, "icon": "puzzle"},
    "pathfinder": {"name": "Pathfinder", "description": "Discover 10 landmarks.",
                   "condition": {"landmarks": 10}, "icon": "star"},
    "hidden_paths": {"name": "Hidden Paths", "description": "Find 5 hidden places.",
                     "condition": {"hidden_areas": 5}, "icon": "map"},
    "festival_goer": {"name": "Festival Goer", "description": "Finish 5 mini-games.",
                      "condition": {"minigames": 5}, "icon": "trophy"},
    "good_neighbour": {"name": "Good Neighbour", "description": "Talk to 20 people.",
                       "condition": {"npcs_talked": 20}, "icon": "heart"},
    "story_complete": {"name": "Cultural Journey", "description": "Complete the main story.",
                       "condition": {"flag": "story_complete"}, "icon": "trophy"},
    "sumatra_friend": {"name": "Highland Friend", "description": "Complete 6 quests in Sumatra.",
                       "condition": {"region_complete": "sumatra:70"}, "icon": "star"},
    "java_friend": {"name": "Gamelan Friend", "description": "Complete 6 quests in Java.",
                    "condition": {"region_complete": "java:70"}, "icon": "star"},
    "kalimantan_friend": {"name": "River Friend", "description": "Complete 6 quests in Kalimantan.",
                          "condition": {"region_complete": "kalimantan:70"}, "icon": "star"},
    "sulawesi_friend": {"name": "Harbour Friend", "description": "Complete 6 quests in Sulawesi.",
                        "condition": {"region_complete": "sulawesi:70"}, "icon": "star"},
    "papua_friend": {"name": "Mountain Friend", "description": "Complete 6 quests in Papua.",
                     "condition": {"region_complete": "papua:70"}, "icon": "star"},
    "journal_keeper": {"name": "Journal Keeper", "description": "Fill a journal category with "
                                                                "at least 3 entries.",
                       "condition": {"journal_category_full": "Food"}, "icon": "journal"},
    "quiz_champion": {"name": "Culture Quiz Champion", "description": "Pass a village culture quiz.",
                      "condition": {"flag": "quiz_passed"}, "icon": "trophy"},
    "minigame_all": {"name": "Jack of All Trades", "description": "Complete 15 mini-games.",
                     "condition": {"minigames": 15}, "icon": "trophy"},
}
