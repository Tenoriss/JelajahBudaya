"""NPC roster: names, roles and idle conversations."""
from content.qb import DIALOGUES

NDEFS = []
def N(nid, name, role, region, idle, wander=False, radius=30, facing="down", sheet=None,
      shop=False):
    NDEFS.append({"id": nid, "name": name, "role": role, "region": region,
                  "character": sheet or nid, "idle_dialogue": "idle_" + nid,
                  "wander": wander, "talk_radius": radius, "facing": facing})
    node = {"speaker": nid, "lines": idle, "goto": ""}
    nodes = {"n1": node}
    if shop:
        node["choices"] = [{"text": "What do you have for sale?",
                            "goto": "shop"},
                           {"text": "Just passing by.", "goto": ""}]
        nodes["shop"] = {"speaker": nid,
                         "lines": ["Take a look. Prices are in Culture Points - "
                                   "that is how we count favours on this journey."],
                         "do": {"open_shop": True}}
    DIALOGUES["idle_" + nid] = {"start": "n1", "nodes": nodes}

# --------------------------------------------------------------- sumatra
N("npc_aminah", "Aminah", "keeper of the ancestral house", "sumatra",
  ["The house is old, but the wall was renewed twice. Nothing here is frozen.",
   "If you sit on the veranda long enough, somebody always comes by with news."], wander=True)
N("npc_datuak", "Datuak", "elder", "sumatra",
  ["Bronze gongs like ours are carried to the wedding in a basket - front and back, like a boat.",
   "When you write down what we say, write our names beside it. Then people will know who spoke."])
N("npc_sari", "Sari", "weaver", "sumatra",
  ["A backstrap loom can only make cloth as wide as my arms are long. That is why our cloths are narrow.",
   "Red, black and white. Those are the colours you will see on a woman's cloth at a wedding."])
N("npc_bujang", "Bujang", "flute player", "sumatra",
  ["Listen - that is the wind in the bamboo, not music. It is a good day when the two agree.",
   "A flute is cheap to make and impossible to make well. Cut one yourself and you will see."], wander=True)
N("npc_ida", "Ida", "cook", "sumatra",
  ["Everything here starts with coconut. Milk, oil, sugar - the same tree, three different things.",
   "Eat with your right hand if you are eating with your hand. And wash first, always."])

# ------------------------------------------------------------------ java
N("npc_ki_bagus", "Ki Bagus", "gamelan player", "java",
  ["Sit anywhere you like. The instruments do not belong to anyone in particular except the set.",
   "You can hear the difference between two gamelans in a single note. Each set finds its own pitch."])
N("npc_dewi", "Dewi", "museum copyist", "java",
  ["We do not restore the reliefs. We copy them, and we write down what condition they are in.",
   "The stone has been repaired more than once, and each repair is part of the building's history."])
N("npc_pak_tarno", "Pak Tarno", "farmer", "java",
  ["Rice will stand in water for weeks and then want to be dry for cutting. Two moods, one plant.",
   "The ducks come after the harvest, and they eat what we would have to clear. That is the trade."], wander=True)
N("npc_rara", "Rara", "angklung teacher", "java",
  ["Thirty children, thirty instruments, one tune. It is the easiest lesson and the hardest.",
   "One tube per note. Nothing here is decoration - the length of the tube makes the pitch."])
N("npc_mbah_karto", "Mbah Karto", "puppeteer", "java",
  ["A performance can run to morning. I have fallen asleep twice, and both times the puppets survived.",
   "The stories are old, but the jokes are new every night. That is how the crowd stays."])

# ------------------------------------------------------------ kalimantan
N("npc_lasan", "Lasan", "longhouse repairer", "kalimantan",
  ["The gallery belongs to everyone, so we repair it together and nobody writes down who paid.",
   "Up here the roof is our biggest worry. Down at the coast their worry is the tide."], wander=True)
N("npc_tina", "Tina", "singer", "kalimantan",
  ["A sung story can carry advice, praise or grief. The tune decides how far the words travel.",
   "My grandmother sang for an hour without repeating herself. I manage four verses."])
N("npc_bapa_udi", "Bapa Udi", "boatman", "kalimantan",
  ["In the wet season the river takes the road. Then we travel on the water and forget the road exists.",
   "Never swim after rain. The current under a brown surface is not what it looks like from the bank."])
N("npc_rini", "Rini", "dyer", "kalimantan",
  ["Tie it tight and it stays light. Tie it loose and the dye creeps in. That is the whole pattern.",
   "Combed cotton came here by trade. Our own fibre is bark and rattan, and that goes the other way."])

# --------------------------------------------------------------- sulawesi
N("npc_rambu", "Rambu", "kolintang player", "sulawesi",
  ["Wooden bars, padded sticks, three players. The bass player is the one who never seems busy.",
   "In the villages here, the music group is also the church choir. Same people, different chairs."])
N("npc_puang", "Puang", "head of the family line", "sulawesi",
  ["The house is not mine. It belongs to the line - I merely keep the door open.",
   "When the family gathers, we sleep on the gallery and the grandchildren go to the rice store."])
N("npc_dg_naba", "Daeng Naba", "shipwright", "sulawesi",
  ["I do not draw hulls. I have built twelve, and the thirteenth will be slightly better than the twelfth.",
   "The timber is bought three years before it is cut. Wet wood fights the builder."])
N("npc_yuliana", "Yuliana", "gardener", "sulawesi",
  ["In the highlands the soil is thin and the rain is heavy. We plant along the slope, not across it.",
   "Nutmeg, clove, coconut - a garden here is also a spice shop."], wander=True)

# ----------------------------------------------------------------- papua
N("npc_yosia", "Yosia", "builder", "papua",
  ["The roof has to be three fingers thick or the rain finds a way through.",
   "We build in a circle here. In the villages down at the coast, the houses are long and rectangular."])
N("npc_petrus", "Petrus", "canoe owner", "papua",
  ["The lake is calm in the morning and dishonest in the afternoon. Cross early.",
   "A canoe has a name and a family. If it is gone, we know who to ask first."])
N("npc_mama_lena", "Mama Lena", "basket maker", "papua",
  ["Pull the knot tight and the bag stretches. It hangs from my head, so my hands stay free.",
   "I do not sell other families' patterns. What I make, I was given the right to make."])
N("npc_tomas", "Tomas", "drum carver", "papua",
  ["One piece of wood, one skin. If the wood has a crack in it, the drum will always answer badly.",
   "You play sitting down. Standing up turns a drum into a noise."])

# ---------------------------------------------------------------- helpers
N("npc_penjaga", "Pak Hasan", "village keeper", "prologue",
  ["A village keeps records in three ways: in writing, in what people remember, and in the ground.",
   "Ask before you write. Nobody minds a notebook that asks first."])
N("npc_pengembara", "Samsul", "traveller", "prologue",
  ["I have walked from the eastern islands to the western ones. Twice, in fact. My knees are not friends with me.",
   "Carry less than you think, and something to give away. That is the whole of travelling."])
N("npc_anak", "Ari", "child", "prologue",
  ["Did you see the boat? It had a red sail! I saw it first!",
   "My cousin says there are islands that are all mountains. Is that true?"], wander=True, radius=34)
N("npc_nelayan", "Pak Amir", "fisher", "prologue",
  ["The tide here runs hard on the full moon. Everybody plans around that, not around the clock.",
   "Mend the net before it tears. A mend costs an hour; a tear costs a morning."], shop=True)
N("npc_guru", "Bu Ratna", "teacher", "prologue",
  ["There are over seven hundred languages in this country. Every one of them carries something.",
   "A class of thirty children here may speak two languages at home. That is not a problem, it is a library."])
N("npc_penari", "Nur", "dancer", "prologue",
  ["Dance first, then talk. The body explains it faster than I can.",
   "Every region's dance is built differently because the story it tells is different."])
N("npc_pengrajin", "Bu Wati", "craftsperson", "prologue",
  ["A good craftsperson is a good listener. The material tells you what it wants to become.",
   "If I cannot make it twice, I have not finished learning it."], shop=True)
N("npc_koki", "Bu Siti", "cook", "prologue",
  ["A recipe is not a set of instructions. It is a description of the last time somebody made it.",
   "Serve from the outside in, always. The middle of the platter is for sharing."], shop=True)
N("npc_pedagang", "Umar", "trader", "prologue",
  ["Prices change with the tide, the harvest and the week. I write them down, which is the only advantage I have.",
   "Everything sells twice: once at the market, once as a story about where it came from."],
  wander=True, shop=True)


# ------------------------------------------------------------- opening scene
DIALOGUES["intro_arrival"] = {"start": "n1", "nodes": {
    "n1": {"speaker": "npc_penjaga",
           "lines": ["You made it up the coast road. Good - the wind was against you all morning.",
                     "This is Kampung Awal. One street, one jetty, and my store room full of "
                     + "other people's memories."],
           "goto": "n2"},
    "n2": {"speaker": "npc_penjaga",
           "lines": ["Your grandmother left something with me years ago. A notebook, cloth bound, "
                     + "half empty.",
                     "Come and talk to me by the well and we will go and find it.",
                     "Walk with W A S D or the arrow keys. Press E to talk to people and to look "
                     + "at things. M opens the map, I your bag, J your journal, ESC the menu."],
           "goto": ""},
}}
