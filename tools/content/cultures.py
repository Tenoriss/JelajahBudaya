"""Culture journal entries.

Ground rules used while writing these:
  * each entry names the community/region it belongs to;
  * nothing sacred is reproduced or described as a spectacle - motifs in the
    game stay abstract and original;
  * anything uncertain or regionally contested carries `"verify": True`, which
    the game shows as "needs verification" in the journal.
"""

CATEGORIES = [
    "Architecture", "Textiles", "Music & Instruments", "Food & Cooking",
    "Festivals & Ceremony", "Craft", "Oral Tradition", "Environment",
]

C = []
def e(cid, cat, region, name, short, text, verify=False, source=""):
    C.append({"id": cid, "category": cat, "region": region, "name": name,
              "short": short, "text": text, "verify": verify, "source": source})

# ---------------------------------------------------------------- prologue
e("nusantara_intro", "Oral Tradition", "prologue", "Nusantara",
  "The old word for the island world of Indonesia.",
  "Nusantara is an old Javanese term for the island world that later became Indonesia. "
  "It is still used today to mean the archipelago as one connected cultural region, which is "
  "why your grandmother's notebook is called a jejak budaya - a trace of culture.")
e("notebook_habit", "Oral Tradition", "prologue", "Keeping a Field Notebook",
  "Writing down what people tell you, in their own words.",
  "Travellers, teachers and researchers have long kept field notebooks: date, place, who spoke, "
  "what they said. Recording a person's own words and naming them as the source is the simplest "
  "way to respect the people you meet - and the easiest way to avoid mixing up two different "
  "communities' traditions.")
e("kampung_home", "Architecture", "prologue", "Coastal Village House",
  "A small stilt house with a shaded veranda.",
  "Along Indonesia's coasts, many houses are raised on posts - for airflow in the heat, to avoid "
  "damp and flooding, and often to keep animals out. The shaded front veranda is where guests "
  "are received, so it is usually the busiest part of the house.")

# ----------------------------------------------------------------- sumatra
e("rumah_gadang", "Architecture", "sumatra", "Rumah Gadang",
  "Minangkabau long house with a sweeping curved roof.",
  "The rumah gadang is the traditional house of the Minangkabau of West Sumatra. Its roof rises "
  "into sharp curved points (gonjong), the walls carry carved panels, and the building belongs to "
  "the women of a matrilineal clan - each rumah gadang is home to the daughters' line. "
  "Motifs in this game are original and abstract; they are not copies of any specific carving.",
  source="Minangkabau tradition, West Sumatra")
e("ulos", "Textiles", "sumatra", "Ulos",
  "Batak woven cloth given as a blessing.",
  "Ulos is hand-woven by Batak communities of North Sumatra, especially around Lake Toba. "
  "Different ulos are worn or presented at births, weddings and funerals; giving one is a way of "
  "passing on blessing and protection. Weaving is done on a backstrap loom, so the cloth is only "
  "as wide as the weaver's reach.", source="Batak tradition, North Sumatra")
e("saluang", "Music & Instruments", "sumatra", "Saluang",
  "A thin bamboo flute from the Minangkabau highlands.",
  "The saluang is a bamboo flute of the Minangkabau. It is played with a circular breathing "
  "technique: air is pushed out through the instrument while the player breathes in through the "
  "nose, so a single phrase can be held for a long time. Saluang playing is traditionally paired "
  "with sung poetry (dendang).", source="Minangkabau tradition, West Sumatra")
e("talempong", "Music & Instruments", "sumatra", "Talempong",
  "Small bronze gong-chimes struck with sticks.",
  "A talempong set is made up of small bronze or brass gongs sitting in a wooden frame. They are "
  "struck with a pair of sticks to carry melody, and usually played together with drums and a "
  "wind instrument. Unlike the Javanese gamelan, a talempong ensemble is portable - it can be "
  "carried to a wedding or a street performance.", source="Minangkabau tradition, West Sumatra")
e("tari_piring", "Festivals & Ceremony", "sumatra", "Tari Piring",
  "A plate dance with fast, careful steps.",
  "Tari Piring comes from Solok in West Sumatra. Dancers hold small plates in each hand and step "
  "quickly between them, sometimes on broken glass, ending by stepping on the plates. It began as "
  "a harvest offering to give thanks for the rice crop, and many groups still perform it at "
  "harvest festivals.", source="Minangkabau tradition, West Sumatra")
e("rendang", "Food & Cooking", "sumatra", "Rendang",
  "Meat slow-cooked in coconut milk and spices until nearly dry.",
  "Rendang is a Minangkabau dish of beef simmered for hours with coconut milk, chilli, ginger, "
  "turmeric, galangal and other aromatics until almost all the liquid is gone. Because it is "
  "cooked so dry it keeps for days without refrigeration, which is why it travels well and is "
  "served at celebrations. The whole spice mix is usually pounded or ground first.",
  source="Minangkabau tradition, West Sumatra")
e("rumah_limas", "Architecture", "sumatra", "Rumah Limas",
  "A South Sumatran stilt house with a tiered roof.",
  "In and around Palembang, the rumah limas is a raised wooden house whose roof steps up in "
  "tiers. The main room is a wide open space used for family gatherings, with the private rooms "
  "behind. Its posts and panels are often carved, and the height of the house above ground keeps "
  "the living space clear of river floods.", source="Palembang Malay tradition, South Sumatra")
e("songket_palembang", "Textiles", "sumatra", "Songket",
  "Cloth with gold or silver thread woven through it.",
  "Songket is woven with an extra weft of metallic thread that floats over the surface, giving "
  "the cloth a shimmer and a raised pattern. Palembang songket is one of the best-known styles in "
  "Sumatra; the work is slow because the metallic thread has to be placed by hand, row by row. "
  "It is worn at weddings and formal ceremonies.", source="Malay tradition, Palembang")
e("danau_toba", "Environment", "sumatra", "Lake Toba",
  "The largest volcanic lake in the world.",
  "Lake Toba fills a huge volcanic caldera in North Sumatra and is ringed by steep highland "
  "slopes where coffee, rice and vegetables are grown. The surrounding highlands are the Batak "
  "homelands. The lake is deep, cool and often misted over in the mornings, and the roads around "
  "it climb sharply away from the water.", source="Geography, North Sumatra")
e("tari_saman", "Oral Tradition", "sumatra", "Tari Saman",
  "Sitting dancers clap and chant in perfect time.",
  "Tari Saman is performed by a line of seated dancers from the Gayo highlands of Aceh. They "
  "clap their hands, slap their chests and thighs, and sing verses together, speeding up until "
  "the whole line moves like one body. The verses mix praise, advice and religious teaching, so "
  "the dance is also a way of passing on words.", source="Gayo tradition, Aceh", verify=True)

# -------------------------------------------------------------------- java
e("gamelan", "Music & Instruments", "java", "Gamelan",
  "A bronze orchestra that is tuned as one set.",
  "A gamelan is an ensemble of metallophones, gongs, drums and flutes - mainly bronze. Each set "
  "is tuned to suit itself and is usually tuned to one of two note systems, slendro (five notes "
  "to the octave) or pelog (seven, of which a five-note subset is used). Because the whole set is "
  "tuned together, instruments from two different gamelans are normally not mixed.",
  source="Javanese tradition")
e("batik", "Textiles", "java", "Batik",
  "Cloth patterned with hot wax and dye.",
  "In batik, wax is drawn or stamped onto cloth and the cloth is dyed; the waxed areas resist the "
  "dye and stay light, and repeating the process builds up the pattern. Named motifs such as "
  "parang or kawung carry meanings, and in Java certain patterns are traditionally associated with "
  "particular occasions. Batik of Indonesia was added to UNESCO's intangible cultural heritage "
  "list in 2009.", source="Javanese tradition; UNESCO 2009")
e("borobudur", "Architecture", "java", "Borobudur",
  "A ninth-century temple built as a stepped mountain.",
  "Borobudur in Central Java is a huge Buddhist temple shaped like a stepped pyramid: pilgrims "
  "walk up through galleries of carved relief panels before coming out on open terraces with "
  "bell-shaped stupas. It was built in the eighth to ninth centuries and is a UNESCO World "
  "Heritage Site. Visitors walk clockwise, with the temple's shape as the story.",
  source="UNESCO World Heritage Site, Central Java")
e("angklung", "Music & Instruments", "java", "Angklung",
  "Bamboo tubes that ring when the frame is shaken.",
  "An angklung is a frame holding tuned bamboo tubes; shaking the frame makes the tubes knock "
  "against their slot and sound. Each instrument makes one note or chord, so the music only works "
  "when many people play together - which is why angklung playing is taught in groups. Sundanese "
  "in West Java developed the traditions around it; UNESCO recognised it in 2010.",
  source="Sundanese tradition, West Java; UNESCO 2010")
e("wayang_kulit", "Oral Tradition", "java", "Wayang Kulit",
  "Shadow puppets and a night-long story.",
  "In wayang kulit the puppeteer (dalang) sits behind a lit screen and moves flat leather puppets "
  "so their shadows fall on the screen for the audience on the other side. The dalang voices every "
  "character, leads the musicians and improvises jokes out of the old epics. Wayang was recognised "
  "by UNESCO in 2003.", source="Javanese tradition; UNESCO 2003")
e("tumpeng", "Food & Cooking", "java", "Tumpeng",
  "A cone of yellow rice with dishes arranged around it.",
  "Tumpeng is a cone of rice, often coloured yellow with turmeric, sitting in the middle of a "
  "platter with side dishes laid around it. The cone shape follows the slope of a mountain, and "
  "the cutting of the tip is a formal part of the gathering. It is served for syukuran - "
  "thanksgiving celebrations - rather than as everyday food.", source="Javanese tradition")
e("rumah_joglo", "Architecture", "java", "Rumah Joglo",
  "A Javanese house with a tall, heavy roof.",
  "The joglo is a traditional Javanese house whose roof rises in the middle to a high peak held "
  "up by four main posts. The open central room under that peak is the pendopo, used to receive "
  "guests and to hold gamelan rehearsals and performances. The bigger and taller the joglo, the "
  "more important the house.", source="Javanese tradition")
e("sawah", "Environment", "java", "Sawah",
  "Terraced wet-rice fields.",
  "Sawah are wet-rice fields kept flooded by a network of small channels, terraces and shared "
  "gates. Water is managed by the community rather than by one household, and the irrigation "
  "schedule is usually agreed together - an old form of cooperation called gotong royong, helping "
  "each other. Terraced sawah also slow the water down so it soaks into the soil instead of "
  "washing it away.", source="Rice cultivation, Java")
e("warung", "Food & Cooking", "java", "Warung",
  "A small neighbourhood food stall.",
  "A warung is a small shop or food stall - sometimes a permanent little building, sometimes a "
  "cart that opens in the evening. It sells coffee, snacks, cigarettes, and simple cooked dishes "
  "like nasi goreng or satay, and it is where the neighbourhood meets. Prices are low and the "
  "owner usually knows every customer.", source="Everyday life across Indonesia")
e("pasar_tradisional", "Environment", "java", "Pasar Tradisional",
  "A morning market where the village trades.",
  "Traditional markets usually run from before sunrise until mid-morning. Farmers and fishers "
  "bring what they have, and buyers come early for the best. The market is also where news "
  "travels: whoever is at the stalls in the morning knows what happened in the village the night "
  "before.", source="Everyday life across Indonesia")

# -------------------------------------------------------------- kalimantan
e("rumah_panjang", "Architecture", "kalimantan", "Rumah Panjang (Betang)",
  "A Dayak longhouse built as a row of family rooms.",
  "The rumah panjang, also called betang, is a Dayak longhouse raised on posts. Instead of one "
  "family, it holds many in a row of apartments off one long covered gallery that runs the length "
  "of the building. That gallery is the shared space - for weaving, mending, meetings and "
  "festivals - and the length of the house shows how many households belong to it.",
  source="Dayak tradition, Kalimantan")
e("mandau", "Craft", "kalimantan", "Mandau",
  "The Dayak work-knife and sword.",
  "The mandau is a traditional Dayak blade with a long slightly curved blade, carried in a carved "
  "wooden sheath that often hangs with a smaller utility knife. In daily use it clears brush, "
  "splits rattan and cuts wood; it also belongs to ceremonial dress. Bladesmiths are respected "
  "craftspeople, and a good blade is passed down rather than bought.",
  source="Dayak tradition, Kalimantan")
e("sasirangan", "Textiles", "kalimantan", "Sasirangan",
  "Banjar cloth tied and dyed with patterns.",
  "Sasirangan is a tie-dye cloth from the Banjar community of South Kalimantan. The cloth is "
  "gathered and tied or sewn tightly before dyeing, so the tied parts stay light and the dyed "
  "parts go dark, leaving a pattern. Modern sasirangan is also machine-stitched and worn as "
  "everyday clothing, not only for ceremonies.", source="Banjar tradition, South Kalimantan")
e("karungut", "Oral Tradition", "kalimantan", "Karungut",
  "Dayak Ngaju sung poetry with a story inside it.",
  "Karungut is a sung oral art of the Dayak Ngaju in Central Kalimantan. A singer delivers verses "
  "in a melodic, rhythmic style - usually with a simple instrumental accompaniment - carrying "
  "advice, praise, or the history of a place. Because the words are sung in a fixed style, a "
  "karungut performer must remember long texts.", source="Dayak Ngaju tradition, Central Kalimantan")
e("tari_gantar", "Festivals & Ceremony", "kalimantan", "Tari Gantar",
  "A planting dance with a bamboo pole and rice seeds.",
  "Tari Gantar is a Dayak dance from East Kalimantan performed with a long bamboo pole and a "
  "container of rice seed. The pole represents the dibble stick used to make holes in the soil, "
  "and the dance mimes planting - the dancers strike the ground in rhythm as the seed is "
  "scattered. It is danced at planting season and at welcoming ceremonies.",
  source="Dayak Kutai tradition, East Kalimantan")
e("pasar_terapung", "Environment", "kalimantan", "Pasar Terapung",
  "A floating market where boats do the trading.",
  "In the Banjar river towns of South Kalimantan, trade happens from small wooden boats: sellers "
  "and buyers pull alongside each other, and the whole market comes and goes with the tide and "
  "the daylight. It starts before sunrise, because produce has to reach the buyers while it is "
  "still fresh, and it disperses within a few hours.",
  source="Banjar tradition, South Kalimantan")
e("kuliner_kalimantan", "Food & Cooking", "kalimantan", "Soto Banjar",
  "A clear, fragrant chicken soup.",
  "Soto Banjar is a Banjar chicken soup - clear broth with chicken, rice cake or potato, boiled "
  "egg, and a fragrant spice mix that usually includes cinnamon, star anise and clove. It is "
  "finished with lime and fried shallots, and eaten with rice cake (ketupat). The spices show how "
  "long South Kalimantan's river ports have been part of the spice trade.",
  source="Banjar tradition, South Kalimantan")
e("hutan_kalimantan", "Environment", "kalimantan", "Rainforest River",
  "A river that carries the forest with it.",
  "Kalimantan's big rivers run from the interior mountains to the sea, turning brown with "
  "sediment in the rainy season. People travel on them by small motorboat and long wooden boat, "
  "and whole villages sit on stilts above the bank. The forest along the river supplies rattan, "
  "resin, fruit and timber, and the river is the road.",
  source="Geography, Kalimantan")
e("ukiran_dayak", "Craft", "kalimantan", "Carved Wood and Beadwork",
  "Patterns cut into posts, shields and tools.",
  "Dayak woodcarving covers house posts, doors, shields, containers and tool handles, and is "
  "usually paired with beadwork in red, black, yellow and white. Motifs are often abstract "
  "curves, spirals and hooking shapes rather than pictures of animals or people. A carver works "
  "with a small adze and knife, following the grain of the wood.",
  source="Dayak tradition, Kalimantan")
e("tenun_ikat", "Textiles", "kalimantan", "Ikat Weaving",
  "Threads tied and dyed before weaving.",
  "In ikat weaving, bundles of thread are tied tightly before dyeing; the tied parts resist the "
  "colour, so when the threads are finally woven the pattern appears where the ties were. Ikat "
  "is found in many parts of Indonesia, and Dayak ikat work in Kalimantan is known for its "
  "dark red, black and white palette.", source="Ikat traditions, Kalimantan")

# ---------------------------------------------------------------- sulawesi
e("tongkonan", "Architecture", "sulawesi", "Tongkonan",
  "Toraja ancestral house with a saddle-shaped roof.",
  "A tongkonan is the ancestral house of a Toraja family in the highlands of South Sulawesi. Its "
  "roof sweeps up at both ends like a saddle, and the front normally faces north. It belongs to a "
  "family line rather than an individual and is where the family's heirlooms are kept, so "
  "building or restoring a tongkonan is a matter for the whole kin group.",
  source="Toraja tradition, South Sulawesi")
e("phinisi", "Craft", "sulawesi", "Pinisi",
  "A wooden sailing ship built without nails or blueprints.",
  "The pinisi is a two-masted wooden sailing ship of the Bugis and Makassar peoples of South "
  "Sulawesi, traditionally built plank by plank at shipyards such as Tanaberu. The hull planks "
  "are shaped and joined by hand, the design is held in the builder's head rather than on paper, "
  "and the ship is launched by rolling it into the water. UNESCO recognised Indonesian "
  "boatbuilding traditions of South Sulawesi in 2017.",
  source="Bugis-Makassar tradition; UNESCO 2017")
e("kolintang", "Music & Instruments", "sulawesi", "Kolintang",
  "Wooden bars struck with mallets.",
  "A kolintang is a set of wooden bars of increasing length laid in a wooden frame; the player "
  "strikes them with padded mallets. Because each bar rings a note, a group of players covers the "
  "melody, the middle voice and the bass together. Kolintang ensembles are a Minahasa tradition "
  "from North Sulawesi and are often played at weddings and church festivals.",
  source="Minahasa tradition, North Sulawesi")
e("sutra_sengkang", "Textiles", "sulawesi", "Sengkang Silk",
  "Fine woven cloth with floral or geometric patterns.",
  "Around Sengkang in Wajo, South Sulawesi, silk is reeled, dyed and woven on hand looms. Bugis "
  "weavers produce fine sarong cloth with floral or geometric patterns, and the mulberry silk "
  "work supports many households in the area. Worn for weddings and formal occasions, the cloth "
  "is a Bugis asset passed down through families.",
  source="Bugis tradition, South Sulawesi")
e("coto_makassar", "Food & Cooking", "sulawesi", "Coto Makassar",
  "Beef soup thickened with ground peanuts.",
  "Coto Makassar is a beef soup from Makassar in South Sulawesi. Beef and offal are simmered with "
  "a spice mixture that includes coriander, cumin and lemongrass, then ground roasted peanuts are "
  "added to give the broth its thickness. It is eaten with rice cake (ketupat) and a spoonful of "
  "chilli sambal.", source="Makassar tradition, South Sulawesi")
e("tari_pakarena", "Festivals & Ceremony", "sulawesi", "Tari Pakarena",
  "A Makassar dance of fans and slowing drums.",
  "Tari Pakarena is a Makassar dance in which dancers move slowly with hand fans, following the "
  "drum rather than a counted beat. Steps are small and controlled, with the eyes and hands "
  "carrying much of the expression. It is performed at welcomes and celebrations, and takes a "
  "long time to learn because the pace is so deliberate.",
  source="Makassar tradition, South Sulawesi")
e("lontara", "Oral Tradition", "sulawesi", "Lontara Script",
  "The old Bugis-Makassar writing system.",
  "Lontara is an Indic-derived script once used to write Bugis, Makassar and related languages. "
  "It was written on strips of palm leaf, and the word lontara can refer to the leaf, the script "
  "or a written record. Old lontara records kept genealogies, laws and diaries, which makes them "
  "important sources for local history.", source="Bugis-Makassar tradition, South Sulawesi")
e("bajo_village", "Architecture", "sulawesi", "Bajo Stilt Village",
  "Houses on posts standing over the water.",
  "Bajo communities live in villages built on stilts directly over the sea or tidal flats, "
  "connected by wooden walkways. They are known across the region as boat-builders and freedivers, "
  "with a long history of moving between coasts and islands. Living above the water keeps houses "
  "cool and close to the boats.", source="Bajo tradition, Sulawesi and eastern Indonesia")
e("benteng_rotterdam", "Architecture", "sulawesi", "Harbour Forts",
  "Stone defences built by kingdoms and traders.",
  "Makassar grew as a trading harbour where ships from many nations met, and the old kingdom "
  "built stone forts such as Fort Rotterdam to control the port. The forts now serve as museums "
  "and archives. Their presence shows that the island's history is a history of sea trade, not "
  "isolation.", source="History, Makassar, South Sulawesi")
e("sagu_maluku", "Food & Cooking", "sulawesi", "Sago as Staple",
  "Starch washed out of the sago palm.",
  "Sago is starch extracted from the trunk of the sago palm: the pith is rasped, washed and "
  "sieved, and the starch settles out of the water. In Maluku, parts of Papua, Sulawesi and "
  "Kalimantan it is a staple food, cooked into a thick porridge (papeda) or baked into flat "
  "cakes. Sago palms grow in wet ground where rice does not.",
  source="Eastern Indonesia food traditions")

# ------------------------------------------------------------------- papua
e("honai", "Architecture", "papua", "Honai",
  "A round Dani house with a conical thatched roof.",
  "In the Baliem Valley of the highlands of Papua, the Dani build honai: small round houses with "
  "a conical roof of thatch reaching almost to the ground, entered through a low doorway. Inside, "
  "a central hearth keeps the house warm in the cold highland nights. Larger houses serve as "
  "meeting places for men, and separate ones serve as homes for women and children.",
  source="Dani tradition, Baliem Valley, Papua")
e("noken", "Craft", "papua", "Noken",
  "A bag knotted or woven from bark fibre.",
  "Noken is a bag from Papua made by knotting or weaving fibres from bark, leaves or roots into a "
  "loose net. It stretches to carry heavy loads - sweet potato from the garden, firewood, a baby "
  "- and is hung from the head or shoulder with the weight on the back. UNESCO added noken to its "
  "intangible cultural heritage list in 2012.", source="Papuan tradition; UNESCO 2012")
e("papeda", "Food & Cooking", "papua", "Papeda",
  "Sago porridge eaten with fish soup.",
  "Papeda is a thick, gluey porridge of sago starch, made by stirring sago into boiling water "
  "until it turns clear and stretchy. It is eaten by wrapping a strand of it around a wooden fork "
  "and dipping it in yellow fish soup, usually made with turmeric and lime. It is a staple in "
  "lowland Papua and parts of Maluku.",
  source="Papuan and Maluku food traditions")
e("tifa", "Music & Instruments", "papua", "Tifa",
  "A hand drum with an animal-skin head.",
  "The tifa is a Papuan hand drum, a wooden cylinder with one end covered by animal skin and "
  "often carved along the body. It marks the beat for songs and dances and is usually played "
  "sitting down, with the drum resting on the player's lap or on the ground. Different areas "
  "shape and decorate their drums differently.",
  source="Papuan tradition")
e("asmat_carving", "Craft", "papua", "Asmat Carving",
  "A carving tradition tied to ancestors and community.",
  "The Asmat people of southern Papua are known for carving wood - shields, poles and figures - "
  "using adzes and shell tools, with designs connected to ancestors and to clan stories. Carving "
  "in this tradition is not decoration: specific works belong to particular families. In this "
  "game only abstract, original shapes are shown; no specific Asmat design is reproduced.",
  source="Asmat tradition, southern Papua; Museum collections")
e("danau_sentani", "Environment", "papua", "Lake Sentani",
  "A lake among hills, near the north coast.",
  "Lake Sentani lies inland from Jayapura in northern Papua, surrounded by hills and by villages "
  "that fish it and farm the surrounding land. Bark cloth and canoe traditions from the Sentani "
  "area are held in museum collections worldwide, and artists from the lake have been influential "
  "in modern Indonesian art.", source="Sentani tradition, northern Papua")
e("baliem_valley", "Environment", "papua", "Baliem Valley",
  "A highland valley of gardens and sweet potato.",
  "The Baliem Valley is a high valley in the central mountains of Papua, ringed by steep ridges "
  "and farmed with sweet potato, taro and yam. Because it is high, nights are cold and mornings "
  "are misty, and the valley supported dense communities long before roads reached it. "
  "Agriculture there is drained by a network of ditches rather than flooded like rice fields.",
  source="Geography and agriculture, highland Papua")
e("burung_cenderawasih", "Environment", "papua", "Birds of Paradise",
  "Forest birds famous for their display plumes.",
  "Birds of paradise live in the forests of New Guinea. Males of many species grow elaborate "
  "plumes and perform display dances to court females, and in colonial times the feathers were "
  "traded as far away as Europe - which is why the birds were hunted so heavily. They are now "
  "protected by Indonesian law and by international trade rules.",
  source="Wildlife of New Guinea; protected species")
e("rumah_kaki_seribu", "Architecture", "papua", "Rumah Kaki Seribu",
  "A many-posted highland house of the Arfak mountains.",
  "In the Arfak mountains of West Papua, houses are built raised on a great many short wooden "
  "posts - the name rumah kaki seribu means the house of a thousand feet. The posts lift the "
  "dwelling well above the damp ground, and the low roof and thick thatch keep out mountain rain. "
  "The posts and walls are cut and shaped with simple hand tools.",
  source="Arfak tradition, West Papua", verify=True)
e("kain_kulit_kayu", "Textiles", "papua", "Bark Cloth",
  "Cloth beaten from the inner bark of a tree.",
  "Bark cloth is made by stripping the inner bark of certain trees, soaking it, and beating it "
  "with a mallet until it spreads into a soft sheet. In Papua and in the Sentani area in "
  "particular, the cloth is painted with patterns for ceremonies and for trade, and different "
  "patterns mark different families. Beating bark cloth is hard, repetitive work that takes hours.",
  source="Papuan bark cloth traditions", verify=True)

# ------------------------------------------------------------------ shared
e("gotong_royong", "Oral Tradition", "prologue", "Gotong Royong",
  "Working together on a task the whole village needs.",
  "Gotong royong is the Indonesian idea of working together voluntarily on something a community "
  "needs - cleaning a road, building a house, preparing a feast. It appears in many local forms "
  "and under many names across the archipelago, and it is the reason a village can rebuild a "
  "bridge in a day.", source="Widely used concept across Indonesia")
e("sambal", "Food & Cooking", "prologue", "Sambal",
  "Chilli relish pounded fresh for the table.",
  "Sambal is a family of chilli relishes - different from district to district, sometimes with "
  "shrimp paste, tomato, lime or ground nuts. It is pounded in a stone mortar rather than blended, "
  "which keeps the texture rough, and eaten with almost anything: rice, fish, vegetables, grilled "
  "corn. Every cook has their own version.",
  source="Culinary tradition across Indonesia")
