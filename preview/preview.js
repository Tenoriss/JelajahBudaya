/*
 * Browser showcase for the Godot project. The scene uses the same compiled
 * map data, atlas sheets, character sprites, object art, dialogue and journal.
 * Movement and this small interaction layer are intentionally lightweight;
 * the full game systems remain in the Godot project.
 */
(() => {
  'use strict';

  const TILE = 32;
  const DIRECTIONS = ['down', 'left', 'right', 'up', 'down_left', 'down_right', 'up_left', 'up_right'];
  const REGION_ORDER = ['prologue', 'sumatra', 'java', 'kalimantan', 'sulawesi', 'papua'];
  const REGION_SHORT = {
    prologue: 'Prologue', sumatra: 'Sumatra', java: 'Java',
    kalimantan: 'Kalimantan', sulawesi: 'Sulawesi', papua: 'Papua'
  };
  const PREFERRED_MAP = {
    prologue: 'desa_awal', sumatra: 'sumatra_desa', java: 'java_desa',
    kalimantan: 'kalimantan_desa', sulawesi: 'sulawesi_desa', papua: 'papua_desa'
  };
  const WEATHER = {
    prologue: 'Soft sea breeze', sumatra: 'Highland mist', java: 'Warm field breeze',
    kalimantan: 'Rainforest air', sulawesi: 'Salt in the wind', papua: 'Mountain haze'
  };
  const TIME_STATES = [
    { key: 'morning', tint: 'rgba(245, 203, 132, .045)' },
    { key: 'daylight', tint: '' },
    { key: 'evening', tint: 'rgba(206, 119, 83, .11)' },
    { key: 'night', tint: 'rgba(45, 62, 111, .26)' }
  ];
  const REGION_SHORT_ID = {
    prologue: 'Pengantar', sumatra: 'Sumatra', java: 'Jawa',
    kalimantan: 'Kalimantan', sulawesi: 'Sulawesi', papua: 'Papua'
  };
  const REGION_TAGLINES_ID = {
    prologue: 'Kampung pesisir kecil tempat perjalanan dimulai.',
    sumatra: 'Dataran tinggi, rumah panjang, dan bunyi saluang.',
    java: 'Teras sawah, gamelan, dan batu candi.',
    kalimantan: 'Sungai, hutan hujan, dan rumah panjang.',
    sulawesi: 'Atap pelana dan kehidupan pesisir.',
    papua: 'Danau pegunungan, noken, dan suara tifa.'
  };
  const COPY = {
    en: {
      journeyBadge: 'FIELD JOURNAL · CHAPTER 01', mapButton: 'Map', journalButton: 'Journal',
      fullscreenEnter: 'Full screen', fullscreenExit: 'Exit full screen',
      fullscreenEnterAria: 'Enter full screen', fullscreenExitAria: 'Exit full screen',
      chapterMark: 'THE FIRST<br>NOTE', move: 'Move', interact: 'Talk / examine', hurry: 'Hurry',
      previewNote: 'INTERACTIVE BROWSER PREVIEW', coordinatesLabel: 'FIELD NOTES', travelerLog: "TRAVELER'S LOG", travelerName: 'The Storyteller',
      travelerSubline: 'A new page is waiting.', storyThread: 'STORY THREAD', questReady: 'READY TO BEGIN',
      questLog: 'Quest log', cultureJournal: 'CULTURE JOURNAL', journalStamp: 'FIELD<br>NOTE 001',
      journalTitle: 'Listening comes first', journalExcerpt: 'Write down what people tell you, in their own words.',
      openJournal: 'Open the journal', archipelago: 'THE ARCHIPELAGO', trailTitle: 'Six stops on the trail',
      previewRoute: 'PREVIEW ROUTE', culturePoints: 'CULTURE POINTS', satchel: 'Satchel',
      nowExploring: 'NOW EXPLORING', morning: 'MORNING', daylight: 'DAYLIGHT', evening: 'EVENING', night: 'NIGHT',
      soundOn: 'Sound on', soundOff: 'Sound off', audioPlaying: 'ORIGINAL AUDIO PLAYING', audioAvailable: 'AMBIENCE AVAILABLE',
      questActive: 'IN PROGRESS', questComplete: 'COMPLETED', freeExploration: 'FREE EXPLORATION',
      noQuestTitle: 'A new page is waiting', noQuestSummary: 'Explore each region, meet its people, and collect the stories you hear.',
      chooseRegion: 'Choose a region from the trail', meetNpc: 'Meet {name}', followingStory: 'Following a story thread.',
      fieldSteps: 'field steps', readyToBegin: 'READY TO BEGIN', storyComplete: 'Story thread complete — keep exploring.',
      meetLocalGuide: 'Meet the local guide',
      mapEyebrow: 'WORLD MAP · PREVIEW ROUTE', mapTitle: 'Across the archipelago',
      mapSubtitle: 'Choose a place to explore. Every region is open in this preview.', locationsIn: 'LOCATIONS IN {name}',
      mapRouteLabel: 'REGIONAL ROUTE MAP', mapRouteNote: 'Schematic game route — locations and paths are for gameplay, not geographic scale.',
      mapNodeOpen: 'Open location', mapNodeCurrent: 'Current location', regionStatsLine: '{maps} locations · {quests} quests',
      openLocation: 'Open preview location', noLocations: 'No preview locations in this region yet.',
      questFilterLabel: 'QUESTS BY REGION', questCountShort: '{count} quests',
      previewTravelNote: 'Preview travel is open across all five cultural regions. The Godot game retains its story progression and unlock rules.',
      journalEyebrow: "THE STORYTELLER'S NOTEBOOK · {region}", journalModalTitle: 'Culture Journal',
      journalSubtitle: 'A living record of places, practices, and the people who share them. Notes marked for checking are not presented as settled fact.',
      sourceNeedsChecking: 'Source details to be confirmed', verifySource: 'CHECK SOURCE', noJournalEntries: 'No notes for this region yet.',
      languageNote: 'All preview text—including NPC interaction prompts and dialogue, quests and objectives, journal entries and source notes, inventory, map and travel labels, notices, and sample puzzles—switches between English and Indonesian. Proper cultural names and formal source titles retain their original wording.',
      questsEyebrow: 'FIELD JOURNAL · STORY THREADS', questsTitle: 'Quest log', questsDescription: '{count} authored story threads for {region}. Each major quest includes an interactive challenge.',
      statusCompleted: 'COMPLETED', statusTracking: 'TRACKING', statusAvailable: 'AVAILABLE IN GAME', trackQuest: 'Track in preview', trackingQuest: 'Currently tracking',
      noQuestThreads: 'There are no story threads in this region.',
      satchelEyebrow: "TRAVELER'S SATCHEL", inventoryTitle: 'Collected along the way',
      inventorySubtitle: 'Keepsakes, useful items, and the small things that help carry a story forward.',
      satchelEmpty: 'Your satchel is light for now.<br>Explore nearby and talk to the people you meet.',
      itemsLocal: 'Items in this browser preview are local to this session.',
      fieldInteraction: 'FIELD INTERACTION', journalFieldNote: 'CULTURE JOURNAL · FIELD NOTE', conversationLabel: 'FIELD CONVERSATION',
      continueLabel: 'Continue', recordedMoment: 'Recorded as a moment of listening on this journey.',
      puzzleEyebrow: '{type} · FIELD CHALLENGE', puzzlePairs: '{matched} / {total} pairs · {moves} turns',
      askHint: 'Ask for a hint', hintsRevealed: 'Hints revealed', revealHint: 'Reveal a hint',
      returnTrail: 'Return to the trail', sequencePrompt: 'Place the steps in a thoughtful order.',
      checkSequence: 'Check sequence', sequenceStep: 'Sequence step',
      previewChallengeNote: 'This browser preview provides playable memory and sequence samples; other puzzle systems run in the Godot project.',
      regionSpecific: 'REGION-SPECIFIC', observeChallenge: 'Observe the details and try the challenge.',
      puzzleFallback: 'Look closely at the setting. The full Godot game runs the authored version of this challenge.',
      challengeComplete: 'Challenge complete.', recordedMemory: 'The memory is recorded in your field journal.',
      turnTo: 'Talk to {name}', inspect: 'Examine', readNote: 'Read field note', readSign: 'Read sign',
      collectItem: 'Collect item', saveCheckpoint: 'Save checkpoint', openChallenge: 'Try the challenge', travelTo: 'Travel · {name}',
      discovered: 'Field discovery', nearbyChallenge: 'A challenge is nearby', puzzleNotFoundText: 'This location points to a game puzzle. Check the quest log and explore the Godot game for the full challenge.',
      puzzleAlreadyDone: 'You have already completed this challenge in the current preview session.',
      previewCouldNotLoad: 'Preview could not load', previewLoadHelp: 'Use the preview server from the repository root so the game data and art are available.',
      previewServerHelp: 'Data could not be loaded. Open the preview through tools/preview_server.py.',
      questStarted: 'Story thread started: {title}', questFinished: 'Story thread complete · +{points} Culture Points', trackingToast: 'Tracking: {title}',
      nowExploringToast: 'Now exploring {name}', collected: 'Collected {name}', keepsakeFound: 'You found a keepsake.', clueNoted: 'A new clue has been noted.',
      saved: 'A field note was saved in this browser.', saveFailed: 'This browser could not store a checkpoint.',
      audioAriaOn: 'Turn ambience off', audioAriaOff: 'Turn ambience on', languageAria: 'Switch interface language', languageChanged: 'Language: English',
      openMapAria: 'Open world map', openJournalAria: 'Open culture journal', closeAria: 'Close', regionAria: 'Travel to {name}',
      metaDescription: 'An interactive preview of Nusantara: Jejak Budaya, a cultural adventure across Indonesia.',
      homeAria: 'Nusantara: Jejak Budaya home', chooseRegionAria: 'Choose a region', gameWorldAria: 'Game world',
      zoomOutAria: 'Zoom out', zoomInAria: 'Zoom in', closeConversationAria: 'Close conversation', journeyDetailsAria: 'Journey details',
      travelerPortraitAlt: 'Traveler portrait', openSatchelAria: 'Open satchel', switchLanguageTitle: 'Switch language',
      questNotebookTitle: 'The Notebook in the Store Room', questPackTitle: 'What to Carry', questNetTitle: 'The Mended Net',
      questNotebookSummary: "Find the loose pages and begin your grandmother's field journal.",
      questPackSummary: "Pack provisions with the traveller's help.", questNetSummary: "Mend the fishing net and earn the village's travel letter.",
      questNotebookObjective: 'Match the six loose pages', questNotebookReport: 'Show the notebook to Pak Penjaga',
      questMeetKeeper: 'Speak with the village keeper', journalEntryNusantara: 'Nusantara',
      journalNusantaraShort: 'An old word for the island world of Indonesia.',
      journalNusantaraText: 'Nusantara is an old Javanese term for the island world that later became Indonesia. It is still used today to mean the archipelago as one connected cultural region, which is why your grandmother\'s notebook is called a jejak budaya — a trace of culture.'
    },
    id: {
      journeyBadge: 'JURNAL PERJALANAN · BAB 01', mapButton: 'Peta', journalButton: 'Jurnal',
      fullscreenEnter: 'Layar penuh', fullscreenExit: 'Keluar layar penuh',
      fullscreenEnterAria: 'Masuk ke layar penuh', fullscreenExitAria: 'Keluar dari layar penuh',
      chapterMark: 'CATATAN<br>PERTAMA', move: 'Bergerak', interact: 'Bicara / periksa', hurry: 'Berlari',
      previewNote: 'PRATINJAU INTERAKTIF BROWSER', coordinatesLabel: 'CATATAN LAPANGAN', travelerLog: 'CATATAN PENJELAJAH', travelerName: 'Sang Pencerita',
      travelerSubline: 'Halaman baru menanti.', storyThread: 'ALUR CERITA', questReady: 'SIAP DIMULAI',
      questLog: 'Daftar misi', cultureJournal: 'JURNAL BUDAYA', journalStamp: 'CATATAN<br>LAPANGAN 001',
      journalTitle: 'Mendengarkan adalah awal', journalExcerpt: 'Catat apa yang disampaikan orang, dengan kata-kata mereka sendiri.',
      openJournal: 'Buka jurnal', archipelago: 'KEPULAUAN NUSANTARA', trailTitle: 'Enam persinggahan',
      previewRoute: 'RUTE PRATINJAU', culturePoints: 'POIN BUDAYA', satchel: 'Tas',
      nowExploring: 'SEDANG MENJELAJAHI', morning: 'PAGI', daylight: 'SIANG', evening: 'SORE', night: 'MALAM',
      soundOn: 'Suara nyala', soundOff: 'Suara mati', audioPlaying: 'AUDIO ASLI DIPUTAR', audioAvailable: 'SUASANA TERSEDIA',
      questActive: 'SEDANG BERJALAN', questComplete: 'SELESAI', freeExploration: 'JELAJAH BEBAS',
      noQuestTitle: 'Halaman baru menanti', noQuestSummary: 'Jelajahi setiap wilayah, temui warganya, dan kumpulkan cerita yang kamu dengar.',
      chooseRegion: 'Pilih wilayah dari jalur perjalanan', meetNpc: 'Temui {name}', followingStory: 'Mengikuti alur cerita.',
      fieldSteps: 'tahap perjalanan', readyToBegin: 'SIAP DIMULAI', storyComplete: 'Alur ini selesai — lanjutkan penjelajahan.',
      meetLocalGuide: 'Temui pemandu setempat',
      mapEyebrow: 'PETA DUNIA · RUTE PRATINJAU', mapTitle: 'Menjelajahi Nusantara',
      mapSubtitle: 'Pilih tempat untuk dijelajahi. Semua wilayah terbuka dalam pratinjau ini.', locationsIn: 'LOKASI DI {name}',
      mapRouteLabel: 'PETA RUTE WILAYAH', mapRouteNote: 'Peta skematis rute permainan — lokasi dan jalur dibuat untuk gameplay, bukan skala geografis.',
      mapNodeOpen: 'Buka lokasi', mapNodeCurrent: 'Lokasi saat ini', regionStatsLine: '{maps} lokasi · {quests} misi',
      openLocation: 'Buka lokasi pratinjau', noLocations: 'Belum ada lokasi pratinjau di wilayah ini.',
      questFilterLabel: 'MISI PER WILAYAH', questCountShort: '{count} misi',
      previewTravelNote: 'Perjalanan pratinjau terbuka di lima wilayah budaya. Progres cerita dan aturan pembukaan wilayah tetap berlaku di game Godot.',
      journalEyebrow: 'BUKU CATATAN SANG PENCERITA · {region}', journalModalTitle: 'Jurnal Budaya',
      journalSubtitle: 'Catatan yang terus bertambah tentang tempat, praktik, dan orang-orang yang membagikannya. Catatan yang perlu diperiksa tidak disajikan sebagai fakta pasti.',
      sourceNeedsChecking: 'Rincian sumber perlu dikonfirmasi', verifySource: 'PERIKSA SUMBER', noJournalEntries: 'Belum ada catatan untuk wilayah ini.',
      languageNote: 'Seluruh teks pratinjau—termasuk petunjuk interaksi NPC dan dialog, misi dan tujuan, jurnal dan catatan sumber, inventaris, label peta dan perjalanan, notifikasi, serta contoh teka-teki—beralih antara bahasa Inggris dan Indonesia. Nama budaya dan judul sumber resmi tetap mengikuti bentuk aslinya.',
      questsEyebrow: 'JURNAL PERJALANAN · ALUR CERITA', questsTitle: 'Daftar misi', questsDescription: '{count} alur cerita tersedia untuk {region}. Setiap misi utama memuat tantangan interaktif.',
      statusCompleted: 'SELESAI', statusTracking: 'DIIKUTI', statusAvailable: 'TERSEDIA DI GAME', trackQuest: 'Ikuti di pratinjau', trackingQuest: 'Sedang diikuti',
      noQuestThreads: 'Belum ada alur cerita di wilayah ini.',
      satchelEyebrow: 'TAS PENJELAJAH', inventoryTitle: 'Temuan sepanjang perjalanan',
      inventorySubtitle: 'Kenang-kenangan, barang berguna, dan benda kecil yang membantu meneruskan sebuah cerita.',
      satchelEmpty: 'Tasmu masih ringan.<br>Jelajahi sekitar dan berbicaralah dengan orang yang kamu temui.',
      itemsLocal: 'Barang di pratinjau browser ini hanya tersimpan selama sesi ini.',
      fieldInteraction: 'INTERAKSI LAPANGAN', journalFieldNote: 'JURNAL BUDAYA · CATATAN LAPANGAN', conversationLabel: 'PERCAKAPAN LAPANGAN',
      continueLabel: 'Lanjutkan', recordedMoment: 'Momen mendengarkan ini tercatat dalam perjalananmu.',
      puzzleEyebrow: '{type} · TANTANGAN LAPANGAN', puzzlePairs: '{matched} / {total} pasangan · {moves} giliran',
      askHint: 'Minta petunjuk', hintsRevealed: 'Petunjuk ditampilkan', revealHint: 'Lihat petunjuk',
      returnTrail: 'Kembali ke perjalanan', sequencePrompt: 'Susun langkah-langkahnya dengan urutan yang tepat.',
      checkSequence: 'Periksa urutan', sequenceStep: 'Langkah urutan',
      previewChallengeNote: 'Pratinjau browser menyediakan contoh permainan ingatan dan urutan. Sistem teka-teki lainnya berjalan di proyek Godot.',
      regionSpecific: 'KHUSUS WILAYAH', observeChallenge: 'Amati petunjuk di sekitarmu, lalu coba tantangannya.',
      puzzleFallback: 'Perhatikan suasananya. Versi lengkap tantangan ini tersedia di game Godot.',
      challengeComplete: 'Tantangan selesai.', recordedMemory: 'Kenangan ini tercatat dalam jurnal perjalananmu.',
      turnTo: 'Bicara dengan {name}', inspect: 'Periksa', readNote: 'Baca catatan', readSign: 'Baca papan informasi',
      collectItem: 'Ambil barang', saveCheckpoint: 'Simpan progres', openChallenge: 'Coba tantangan', travelTo: 'Pergi ke · {name}',
      discovered: 'Temuan lapangan', nearbyChallenge: 'Ada tantangan di dekat sini', puzzleNotFoundText: 'Lokasi ini terhubung dengan teka-teki. Lihat daftar misi dan jelajahi game Godot untuk mencoba tantangan lengkapnya.',
      puzzleAlreadyDone: 'Tantangan ini sudah kamu selesaikan dalam sesi pratinjau ini.',
      previewCouldNotLoad: 'Pratinjau tidak dapat dimuat', previewLoadHelp: 'Jalankan server pratinjau dari folder utama agar data dan ilustrasi game dapat diakses.',
      previewServerHelp: 'Data tidak dapat dimuat. Buka pratinjau melalui tools/preview_server.py.',
      questStarted: 'Alur cerita dimulai: {title}', questFinished: 'Alur cerita selesai · +{points} Poin Budaya', trackingToast: 'Mengikuti: {title}',
      nowExploringToast: 'Sekarang menjelajahi {name}', collected: 'Mendapatkan {name}', keepsakeFound: 'Kamu menemukan sebuah kenang-kenangan.', clueNoted: 'Petunjuk baru telah dicatat.',
      saved: 'Catatan lapangan tersimpan di browser ini.', saveFailed: 'Browser ini tidak dapat menyimpan titik simpan.',
      audioAriaOn: 'Matikan suara suasana', audioAriaOff: 'Nyalakan suara suasana', languageAria: 'Ganti bahasa antarmuka', languageChanged: 'Bahasa: Indonesia',
      openMapAria: 'Buka peta dunia', openJournalAria: 'Buka jurnal budaya', closeAria: 'Tutup', regionAria: 'Jelajahi {name}',
      metaDescription: 'Pratinjau interaktif Nusantara: Jejak Budaya, petualangan budaya di Indonesia.',
      homeAria: 'Nusantara: Jejak Budaya beranda', chooseRegionAria: 'Pilih wilayah', gameWorldAria: 'Dunia permainan',
      zoomOutAria: 'Perkecil tampilan', zoomInAria: 'Perbesar tampilan', closeConversationAria: 'Tutup percakapan', journeyDetailsAria: 'Rincian perjalanan',
      travelerPortraitAlt: 'Potret penjelajah', openSatchelAria: 'Buka tas', switchLanguageTitle: 'Ganti bahasa',
      questNotebookTitle: 'Buku Catatan di Ruang Penyimpanan', questPackTitle: 'Bekal Perjalanan', questNetTitle: 'Jaring yang Diperbaiki',
      questNotebookSummary: 'Temukan halaman-halaman yang terlepas dan mulailah jurnal perjalanan nenekmu.',
      questPackSummary: 'Siapkan perbekalan dengan bantuan seorang pengembara.', questNetSummary: 'Perbaiki jaring ikan dan dapatkan surat jalan dari kampung.',
      questNotebookObjective: 'Cocokkan enam halaman yang terlepas', questNotebookReport: 'Tunjukkan buku catatan kepada Pak Penjaga',
      questMeetKeeper: 'Bicaralah dengan penjaga kampung', journalEntryNusantara: 'Nusantara',
      journalNusantaraShort: 'Sebutan lama untuk gugusan pulau yang kini menjadi Indonesia.',
      journalNusantaraText: 'Nusantara adalah istilah Jawa Kuno untuk wilayah kepulauan yang kemudian menjadi Indonesia. Istilah ini masih digunakan untuk menyebut kepulauan sebagai kawasan budaya yang saling terhubung. Karena itu, buku nenekmu disebut jejak budaya — rekam jejak kebudayaan.'
    }
  };
  let locale = 'id';
  try {
    const savedLocale = localStorage.getItem('jelajah-preview-language');
    if (savedLocale === 'en' || savedLocale === 'id') locale = savedLocale;
  } catch (_) { /* private browsing may disable local storage */ }

  const DIALOGUE_ID = {
    intro_arrival: {
      n1: ['Kamu berhasil melewati jalan pesisir. Bagus — angin bertiup berlawanan arah sepanjang pagi.', 'Ini Kampung Awal. Hanya ada satu jalan, satu dermaga, dan ruang penyimpananku yang penuh kenangan orang-orang.'],
      n2: ['Nenekmu menitipkan sesuatu kepadaku bertahun-tahun lalu. Sebuah buku catatan berbalut kain, dengan banyak halaman kosong.', 'Temui aku di dekat sumur, lalu kita cari bersama.', 'Gunakan W A S D atau tombol panah untuk bergerak. Tekan E untuk berbicara dan memeriksa benda. M membuka peta, I tas, J jurnal, dan ESC menu.']
    },
    dlg_pg_01_notebook_offer: {
      n1: ['Ah — kamu datang untuk mengambil barang-barang nenekmu?', 'Ia menyimpan sebuah buku catatan dan selalu berkata bahwa isinya belum selesai.', 'Buku itu ada di ruang penyimpanan sejak ia berhenti bepergian. Halaman-halamannya berserakan.'],
      yes: ['Baik. Luangkan waktumu, lalu catat apa yang kamu pelajari.'],
      no: ['Kembalilah jika sudah siap — semuanya akan tetap tersimpan.']
    },
    idle_npc_penjaga: {
      n1: ['Sebuah kampung menyimpan cerita dengan tiga cara: melalui tulisan, ingatan orang-orang, dan jejak di tanah.', 'Mintalah izin sebelum mencatat. Tak ada yang keberatan dengan buku catatan yang bertanya lebih dahulu.']
    },
    dlg_pg_01_notebook_task: {
      n1: ['Halaman-halaman itu ada di ruang penyimpanan — ruangan itu berada di rumah besar sebelah utara lapangan.', 'Susun berdasarkan gambar yang ada di setiap halaman.']
    },
    dlg_pg_01_notebook_turnin: {
      n1: ['Kamu berhasil mencocokkan keenamnya. Tulisan tangan nenekmu masih ada di halaman pertama.', 'Kalau begitu, sudah diputuskan: buku itu akan kembali bepergian, dan kamulah yang membawanya.', 'Catat apa yang orang-orang ceritakan — kata-kata, nama, dan tempat mereka.']
    }
  };
  const DIALOGUE_CHOICES_ID = {
    dlg_pg_01_notebook_offer: { n1: ['Aku akan membantu.', 'Belum sekarang, nanti aku kembali.'] }
  };
  const CONTENT_TRANSLATIONS_ID = {
    'Grandmother\'s first page': 'Halaman pertama Nenek',
    'It is not one culture, and it is not a hundred separate ones either. Write down what people tell you, in their own words.': 'Ini bukan satu budaya, tetapi juga bukan seratus budaya yang terpisah. Catat apa yang orang sampaikan kepadamu, dengan kata-kata mereka sendiri.',
    'Village board': 'Papan informasi kampung',
    'Kampung Awal. Jetty to the west, rice field east, road inland north.': 'Kampung Awal. Dermaga berada di barat, sawah di timur, dan jalan menuju pedalaman di utara.',
    'Stone notice': 'Prasasti batu',
    'Examine the relief panels': 'Amati panel relief',
    'Look at the map': 'Lihat peta',
    'Speak with the village keeper': 'Bicaralah dengan penjaga kampung',
    'Match the six loose pages': 'Cocokkan enam halaman yang terlepas',
    'Show the notebook to Pak Penjaga': 'Tunjukkan buku catatan kepada Pak Penjaga',
    'A quiet doorway': 'Ambang pintu yang sunyi',
    'This doorway leads somewhere else on the trail.': 'Pintu ini menuju ke tempat lain di sepanjang perjalanan.',
    'Field discovery': 'Temuan lapangan',
    'A detail worth remembering for the journal.': 'Detail yang layak dicatat dalam jurnal.',
    'A landmark recorded in the field journal.': 'Tengara yang tercatat dalam jurnal perjalanan.',
    'Field note': 'Catatan lapangan',
    'You pause to take in the details around you.': 'Kamu berhenti sejenak untuk mengamati detail di sekitarmu.',
    'Examine': 'Periksa',
    'Collect item': 'Ambil barang',
    'Villager': 'Warga',
    'Challenge': 'Tantangan'
  };
  const CATEGORY_TRANSLATIONS_ID = {
    'Culture': 'Budaya', 'FIELD NOTE': 'CATATAN LAPANGAN', 'Architecture': 'Arsitektur', 'Textiles': 'Tekstil', 'Music & Instruments': 'Musik & Alat Musik',
    'Food & Cooking': 'Makanan & Memasak', 'Festivals & Ceremony': 'Festival & Upacara',
    'Craft': 'Kerajinan', 'Oral Tradition': 'Tradisi Lisan', 'Environment': 'Lingkungan'
  };
  const ITEM_CATEGORY_ID = { quest: 'Misi', collectible: 'Koleksi', collectibles: 'Koleksi', souvenir: 'Cendera mata', souvenirs: 'Cendera mata', items: 'Barang', keepsake: 'Kenang-kenangan', food: 'Makanan', tool: 'Peralatan', material: 'Bahan' };
  const PUZZLE_TYPE_ID = { memory: 'Ingatan', sequence: 'Urutan', crafting: 'Merakit', cooking: 'Memasak', rhythm: 'Irama', pattern: 'Pola', match: 'Mencocokkan', matching: 'Mencocokkan', logic: 'Logika', tile: 'Ubin', quiz: 'Kuis', environment: 'Lingkungan', exploration: 'Penjelajahan', challenge: 'Tantangan' };
  const PUZZLE_TEXT_ID = {
    pz_notebook_pages: {
      symbols: ['Halaman depan', 'Sketsa sungai', 'Daun sawo', 'Daftar kampung', 'Cap lama', 'Catatan garam'],
      hints: ['Pasangan halaman berada berdampingan di meja, bukan saling berseberangan.', 'Dua halaman menyimpan daun yang sama di dalamnya.', 'Sketsa sungai berpasangan dengan halaman yang memiliki dua garis bergelombang.']
    }
  };

  const $ = (id) => document.getElementById(id);
  const canvas = $('worldCanvas');
  const ctx = canvas.getContext('2d', { alpha: false });
  const rootModal = $('modalRoot');
  const interactHint = $('interactHint');
  const hintText = $('interactText');
  const dialoguePanel = $('dialoguePanel');
  const toastEl = $('toast');

  let data = null;
  let dialogueTranslationsID = {};
  let previewContentTranslationsID = {};
  let mapNamesEN = {};
  let routeMapLayouts = {};
  let mapIndex = [];
  let mapCache = new Map();
  let mapDef = null;
  let tileset = null;
  let terrainGrid = [];
  let tileRegion = 'sumatra';
  let canvasWidth = 0;
  let canvasHeight = 0;
  let pixelRatio = 1;
  let zoom = 1.58;
  let lastFrame = 0;
  let startedAt = performance.now();
  let lastTimeState = -1;
  let toastTimer = 0;
  let currentTarget = null;
  let dialogueState = null;
  let modalState = null;
  let soundEnabled = false;
  let ambientAudio = null;
  let musicAudio = null;
  const keys = new Set();
  const imageCache = new Map();
  const state = {
    activeQuestId: null,
    completedNoteQuestId: null,
    completedQuestIds: new Set(),
    completedPuzzleIds: new Set(),
    completedObjectives: new Set(),
    discoveredCultureIds: new Set(),
    inventory: [],
    culturePoints: 0
  };
  const player = {
    x: 0, y: 0, facing: 'down', moving: false, animTime: 0,
    walkCycle: 0, speed: 132, lastInteract: 0
  };

  function assetUrl(path) {
    if (!path) return '';
    const clean = String(path).replace(/^res:\/\//, '').replace(/^\/+/, '');
    return `../${clean}`;
  }

  function getImage(path) {
    const url = assetUrl(path);
    if (!url) return null;
    if (!imageCache.has(url)) {
      const img = new Image();
      img.decoding = 'async';
      img.src = url;
      img.addEventListener('load', () => {});
      imageCache.set(url, img);
    }
    return imageCache.get(url);
  }

  async function fetchJSON(path) {
    const response = await fetch(path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
    return response.json();
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[char]));
  }

  function t(key, values = {}) {
    let text = COPY[locale]?.[key] ?? COPY.en[key] ?? key;
    for (const [name, value] of Object.entries(values)) text = text.replaceAll(`{${name}}`, String(value));
    return text;
  }

  function shortRegion(regionId) {
    return locale === 'id' ? (REGION_SHORT_ID[regionId] || REGION_SHORT[regionId] || regionId) : (REGION_SHORT[regionId] || regionId);
  }

  function localizedQuestTitle(quest) {
    if (locale === 'id' && quest?.title_id) return quest.title_id;
    if (locale === 'id') {
      const keys = { pg_01_notebook: 'questNotebookTitle', pg_02_keberangkatan: 'questPackTitle', pg_03_net_mend: 'questNetTitle' };
      if (keys[quest?.id]) return t(keys[quest.id]);
    }
    return localizedInline(quest?.title || '');
  }

  function localizedQuestSummary(quest) {
    if (locale === 'id' && quest?.summary_id) return quest.summary_id;
    if (locale === 'id') {
      const keys = { pg_01_notebook: 'questNotebookSummary', pg_02_keberangkatan: 'questPackSummary', pg_03_net_mend: 'questNetSummary' };
      if (keys[quest?.id]) return t(keys[quest.id]);
    }
    return localizedInline(quest?.summary || quest?.description || '');
  }

  function localizedObjectiveText(quest, objective) {
    if (locale === 'id' && objective?.text_id) return objective.text_id;
    if (locale === 'id' && quest?.id === 'pg_01_notebook') {
      if (objective?.target === 'pz_notebook_pages') return t('questNotebookObjective');
      if (objective?.target === 'npc_penjaga') return t('questNotebookReport');
    }
    const source = objective?.text || '';
    return localizedInline(source);
  }

  function localizedInline(text) {
    const source = String(text || '');
    if (locale !== 'id') return source;
    return CONTENT_TRANSLATIONS_ID[source] || previewContentTranslationsID[source] || dialogueTranslationsID[source] || source;
  }

  function localizedDialogue(dialogueId, source) {
    if (locale !== 'id' || !source) return source;
    const copy = JSON.parse(JSON.stringify(source));
    const translatedNodes = DIALOGUE_ID[dialogueId] || {};
    const translatedChoices = DIALOGUE_CHOICES_ID[dialogueId] || {};
    for (const [nodeId, node] of Object.entries(copy.nodes || {})) {
      const explicitLines = translatedNodes[nodeId];
      if (Array.isArray(explicitLines)) {
        node.lines = explicitLines;
      } else if (Array.isArray(node.lines)) {
        node.lines = node.lines.map((line) => dialogueTranslationsID[line] || line);
      }
      const explicitChoices = translatedChoices[nodeId] || [];
      if (Array.isArray(node.choices)) {
        node.choices = node.choices.map((choice, index) => ({
          ...choice,
          text: explicitChoices[index] || dialogueTranslationsID[choice.text] || choice.text
        }));
      }
    }
    return copy;
  }

  function dialogueFallback(speakerNpcId) {
    const npc = npcDef(speakerNpcId);
    const line = locale === 'id'
      ? `${npc.name || 'Warga'} tersenyum dan berbagi sedikit cerita tentang jalan di depan.`
      : (npc.name ? `${npc.name} shares a smile and a few words about the road ahead.` : 'You make a note of this moment.');
    return { start: 'n1', nodes: { n1: { speaker: speakerNpcId, lines: [line] } } };
  }

  function localizedCulture(entry, field) {
    if (!entry) return '';
    if (locale === 'id' && entry.id === 'nusantara_intro') {
      if (field === 'name') return t('journalEntryNusantara');
      if (field === 'short') return t('journalNusantaraShort');
      if (field === 'text') return t('journalNusantaraText');
    }
    const source = entry[field] || '';
    return locale === 'id' ? localizedInline(source) : source;
  }

  function localizedCategory(category) {
    return locale === 'id' ? (CATEGORY_TRANSLATIONS_ID[category] || category) : category;
  }

  function localizedPuzzleType(type) {
    return locale === 'id' ? (PUZZLE_TYPE_ID[type] || titleCase(type)) : titleCase(type);
  }

  function localizedPuzzleTitle(puzzle) {
    if (locale === 'id' && puzzle?.id === 'pz_notebook_pages') return 'Halaman-Halaman Buku Nenek';
    return localizedInline(puzzle?.title || '');
  }

  function localizedPuzzleDescription(puzzle) {
    if (locale === 'id' && puzzle?.id === 'pz_notebook_pages') return 'Rapikan halaman-halaman yang terlepas dengan mencocokkan setiap pasangan.';
    return localizedInline(puzzle?.description || '');
  }

  function localizedPuzzleSymbols(puzzle) {
    if (locale === 'id' && PUZZLE_TEXT_ID[puzzle?.id]?.symbols) return PUZZLE_TEXT_ID[puzzle.id].symbols;
    const symbols = puzzle?.data?.symbols || [];
    return locale === 'id' ? symbols.map(localizedInline) : symbols;
  }

  function localizedPuzzleItems(puzzle) {
    const items = puzzle?.data?.items || [];
    return locale === 'id' ? items.map(localizedInline) : items;
  }

  function localizedPuzzleHint(puzzle, index) {
    if (locale === 'id' && PUZZLE_TEXT_ID[puzzle?.id]?.hints?.[index]) return PUZZLE_TEXT_ID[puzzle.id].hints[index];
    const hint = puzzle?.hints?.[index] || '';
    return locale === 'id' ? localizedInline(hint) : hint;
  }

  function isFullscreenActive() {
    const appShell = document.querySelector('.app-shell');
    const fullscreenElement = document.fullscreenElement || document.webkitFullscreenElement;
    return Boolean(appShell && (fullscreenElement === appShell || appShell.classList.contains('fullscreen-fallback')));
  }

  function syncFullscreenButton() {
    const button = $('fullscreenButton');
    if (!button) return;
    const active = isFullscreenActive();
    const label = active ? 'fullscreenExit' : 'fullscreenEnter';
    const ariaLabel = active ? 'fullscreenExitAria' : 'fullscreenEnterAria';
    button.setAttribute('aria-label', t(ariaLabel));
    button.setAttribute('aria-pressed', active ? 'true' : 'false');
    button.title = `${t(label)} (F)`;
    button.classList.toggle('active', active);
    if ($('fullscreenLabel')) $('fullscreenLabel').textContent = t(label);
  }

  async function toggleFullscreen() {
    const appShell = document.querySelector('.app-shell');
    if (!appShell) return;
    const fullscreenElement = document.fullscreenElement || document.webkitFullscreenElement;
    if (fullscreenElement) {
      try {
        if (document.exitFullscreen) await document.exitFullscreen();
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
      } catch (_) { /* the browser may already have exited fullscreen */ }
    } else if (appShell.classList.contains('fullscreen-fallback')) {
      appShell.classList.remove('fullscreen-fallback');
    } else {
      const request = appShell.requestFullscreen || appShell.webkitRequestFullscreen;
      if (request) {
        try {
          await request.call(appShell, { navigationUI: 'hide' });
        } catch (_) {
          appShell.classList.add('fullscreen-fallback');
        }
      } else {
        appShell.classList.add('fullscreen-fallback');
      }
    }
    syncFullscreenButton();
    resizeCanvas();
  }

  function applyStaticLocale() {
    document.documentElement.lang = locale;
    document.title = locale === 'id' ? 'Nusantara: Jejak Budaya — Pratinjau' : 'Nusantara: Jejak Budaya — Preview';
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) metaDescription.content = t('metaDescription');
    const setAria = (selector, key) => document.querySelector(selector)?.setAttribute('aria-label', t(key));
    setAria('.brand', 'homeAria');
    setAria('#regionNav', 'chooseRegionAria');
    setAria('.explorer', 'gameWorldAria');
    setAria('#worldCanvas', 'gameWorldAria');
    setAria('#zoomOut', 'zoomOutAria');
    setAria('#zoomIn', 'zoomInAria');
    setAria('#dialogueClose', 'closeConversationAria');
    setAria('.field-rail', 'journeyDetailsAria');
    setAria('#satchelButton', 'openSatchelAria');
    setAria('#travelButton', 'openMapAria');
    const travelerPortrait = document.querySelector('.traveller-avatar img');
    if (travelerPortrait) travelerPortrait.alt = t('travelerPortraitAlt');
    document.querySelectorAll('[data-i18n]').forEach((node) => {
      const key = node.dataset.i18n;
      if (COPY[locale]?.[key]) node.textContent = t(key);
    });
    document.querySelectorAll('[data-i18n-html]').forEach((node) => {
      const key = node.dataset.i18nHtml;
      if (COPY[locale]?.[key]) node.innerHTML = t(key);
    });
    document.querySelectorAll('[data-language-label]').forEach((node) => {
      const selected = node.dataset.languageLabel === locale;
      node.classList.toggle('active', selected);
      node.setAttribute('aria-pressed', selected ? 'true' : 'false');
    });
    if ($('languageToggle')) {
      $('languageToggle').setAttribute('aria-label', t('languageAria'));
      $('languageToggle').title = t('switchLanguageTitle');
    }
    if ($('mapButton')) $('mapButton').title = `${t('openMapAria')} (M)`;
    if ($('journalButton')) $('journalButton').title = `${t('openJournalAria')} (J)`;
    if ($('satchelButton')) $('satchelButton').title = t('openSatchelAria');
    if ($('soundButton')) {
      $('soundButton').classList.toggle('active', soundEnabled);
      $('soundButton').setAttribute('aria-label', soundEnabled ? t('audioAriaOn') : t('audioAriaOff'));
      $('soundLabel').textContent = t(soundEnabled ? 'soundOn' : 'soundOff');
      $('audioCaption').innerHTML = `<span class="audio-bars"><i></i><i></i><i></i></span> ${t(soundEnabled ? 'audioPlaying' : 'audioAvailable')}`;
    }
    syncFullscreenButton();
    if (!data) return;
    updateLocationUI();
    updateQuestUI();
    renderTrail();
    updateInteractionTarget();
    if (dialogueState) {
      const source = data.dialogues.dialogues[dialogueState.dialogueId];
      dialogueState.dialogue = source
        ? localizedDialogue(dialogueState.dialogueId, source)
        : dialogueFallback(dialogueState.speakerNpcId);
      renderDialogue();
    }
    if (modalState) {
      if (modalState.type === 'map') renderMapModal();
      else if (modalState.type === 'journal') openJournalModal();
      else if (modalState.type === 'quests') renderQuestModal();
      else if (modalState.type === 'inventory') openInventoryModal();
      else if (modalState.type === 'puzzle') {
        const puzzle = puzzleDef(modalState.puzzleId);
        if (puzzle?.type === 'memory' && modalState.cards.length) {
          const symbols = localizedPuzzleSymbols(puzzle);
          modalState.cards = modalState.cards.map((card) => ({ ...card, label: symbols[Number(card.key) % symbols.length] || card.label }));
        }
        renderPuzzleModal();
      } else if (modalState.type === 'text') renderTextModal();
    }
  }

  function setLocale(nextLocale) {
    if (nextLocale !== 'en' && nextLocale !== 'id') return;
    if (locale === nextLocale) return;
    locale = nextLocale;
    try { localStorage.setItem('jelajah-preview-language', locale); } catch (_) { /* storage is optional */ }
    applyStaticLocale();
    setToast(t('languageChanged'));
  }

  function titleRegion(regionId) {
    if (regionId === 'prologue') return locale === 'id' ? 'Kampung Awal' : 'Starting Village';
    if (locale === 'id' && regionId === 'java') return 'Jawa';
    return data?.regions?.regions?.[regionId]?.name || shortRegion(regionId) || regionId;
  }

  function titleCase(value) {
    return String(value || '').replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function localizedMapName(mapOrId) {
    const entry = typeof mapOrId === 'string' ? mapMeta(mapOrId) : mapOrId;
    if (!entry) return typeof mapOrId === 'string' ? titleCase(mapOrId) : '';
    if (locale === 'en') return mapNamesEN[entry.id] || entry.name || entry.id || '';
    return localizedInline(entry.name || entry.id || '');
  }

  function setToast(message) {
    toastEl.textContent = message;
    toastEl.hidden = false;
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => { toastEl.hidden = true; }, 2600);
  }

  function mapMeta(mapId) { return mapIndex.find((entry) => entry.id === mapId) || null; }
  function questDefs() { return Object.values(data?.quests?.quests || {}); }
  function cultureDefs() { return Object.values(data?.cultures?.entries || {}); }
  function itemDef(itemId) { return data?.items?.[itemId] || null; }
  function puzzleDef(puzzleId) { return data?.puzzles?.puzzles?.[puzzleId] || null; }
  function npcDef(npcId) { return data?.npcs?.npcs?.[npcId] || {}; }

  function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    canvasWidth = rect.width;
    canvasHeight = rect.height;
    const width = Math.round(rect.width * pixelRatio);
    const height = Math.round(rect.height * pixelRatio);
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    ctx.imageSmoothingEnabled = false;
  }

  function seededHash(x, y, seed) {
    let value = (x * 73856093) ^ (y * 19349663) ^ seed;
    value = Math.imul(value ^ (value >>> 13), 1274126177);
    return (value ^ (value >>> 16)) >>> 0;
  }

  function stringHash(text) {
    let hash = 2166136261;
    for (let i = 0; i < text.length; i += 1) {
      hash ^= text.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function buildTerrain(def) {
    const [width, height] = def.size || [48, 36];
    const terrain = def.terrain || {};
    const grid = Array.from({ length: height }, () => Array(width).fill(terrain.default || 'GRASS'));
    const paint = (x, y, kind) => {
      if (x >= 0 && x < width && y >= 0 && y < height) grid[y][x] = kind;
    };
    for (const entry of terrain.rects || []) {
      const [x, y, w, h] = entry.rect || [0, 0, 0, 0];
      for (let py = y; py < y + h; py += 1) {
        for (let px = x; px < x + w; px += 1) paint(px, py, entry.tile || 'GRASS');
      }
    }
    for (const line of terrain.lines || []) {
      const [x1, y1] = line.from || [0, 0];
      const [x2, y2] = line.to || [0, 0];
      const widthBrush = Math.max(1, Number(line.width || 1));
      const steps = Math.max(Math.abs(x2 - x1), Math.abs(y2 - y1)) + 1;
      for (let index = 0; index < steps; index += 1) {
        const t = steps <= 1 ? 0 : index / (steps - 1);
        const cx = Math.round(x1 + (x2 - x1) * t);
        const cy = Math.round(y1 + (y2 - y1) * t);
        const min = -Math.floor((widthBrush - 1) / 2);
        const max = Math.floor(widthBrush / 2);
        for (let dy = min; dy <= max; dy += 1) {
          for (let dx = min; dx <= max; dx += 1) paint(cx + dx, cy + dy, line.tile || 'PATH');
        }
      }
    }
    for (const blob of terrain.blobs || []) {
      const [cx, cy] = blob.center || [0, 0];
      const radius = Number(blob.radius || 4);
      const minX = Math.max(0, Math.floor(cx - radius));
      const maxX = Math.min(width - 1, Math.ceil(cx + radius));
      const minY = Math.max(0, Math.floor(cy - radius));
      const maxY = Math.min(height - 1, Math.ceil(cy + radius));
      for (let y = minY; y <= maxY; y += 1) {
        for (let x = minX; x <= maxX; x += 1) {
          if (Math.hypot(x - cx, y - cy) <= radius) paint(x, y, blob.tile || 'JUNGLE');
        }
      }
    }
    return grid;
  }

  function regionTileset(regionId) {
    const key = data.tilesets[regionId] ? regionId : 'sumatra';
    return { key, atlas: data.tilesets[key] };
  }

  async function loadMap(mapId, announce = true) {
    let loaded = mapCache.get(mapId);
    if (!loaded) {
      loaded = await fetchJSON(`../data/maps/${encodeURIComponent(mapId)}.json`);
      mapCache.set(mapId, loaded);
    }
    mapDef = loaded;
    const chosen = regionTileset(mapDef.region);
    tileRegion = chosen.key;
    tileset = chosen.atlas;
    terrainGrid = buildTerrain(mapDef);
    const spawn = mapDef.spawn || [4, 4];
    player.x = spawn[0] * TILE + TILE / 2;
    player.y = spawn[1] * TILE + TILE / 2;
    player.facing = 'down';
    player.moving = false;
    keys.clear();
    currentTarget = null;
    interactHint.hidden = true;
    closeDialogue();
    closeModal();
    updateLocationUI();
    updateQuestUI();
    renderTrail();
    preloadMapArt();
    if (soundEnabled) syncAudio();
    if (announce) setToast(t('nowExploringToast', { name: localizedMapName(mapDef) }));
  }

  function preloadMapArt() {
    getImage(`assets/environments/tilesets/terrain_${tileRegion}.png`);
    for (const obj of [...(mapDef.objects || []), ...(mapDef.objects_px || [])]) {
      const info = data.objects[obj.sprite];
      if (info) getImage(info.file);
    }
    for (const item of mapDef.interactables || []) {
      const info = data.objects[item.sprite];
      if (info) getImage(info.file);
    }
    for (const entry of mapDef.npcs || []) {
      const character = data.characters[npcDef(entry.id).character || entry.id];
      if (character) getImage(character.sheet);
    }
    getImage(data.characters.player.sheet);
  }

  function updateLocationUI() {
    const region = mapDef.region || 'prologue';
    const regionName = titleRegion(region);
    const regionShort = shortRegion(region);
    const regionInfo = data.regions.regions[region] || {};
    const mapName = localizedMapName(mapDef);
    $('mapTitle').textContent = mapName;
    $('mapTagline').textContent = locale === 'id'
      ? (REGION_TAGLINES_ID[region] || 'Jelajahi jalur dan dengarkan kisah yang dibagikan di sepanjang perjalanan.')
      : (regionInfo.tagline || regionInfo.intro || 'Follow the paths and listen to the stories along the way.');
    $('regionEyebrow').textContent = `${t('nowExploring')} · ${regionName.toLocaleUpperCase(locale)}`;
    $('sceneMapName').textContent = mapName.toLocaleUpperCase(locale);
    $('sceneRegionName').textContent = regionShort.toLocaleUpperCase(locale);
    $('weatherLabel').textContent = locale === 'id'
      ? ({ prologue: 'Angin laut sepoi-sepoi', sumatra: 'Kabut dataran tinggi', java: 'Angin hangat di persawahan', kalimantan: 'Udara hutan hujan', sulawesi: 'Angin asin dari laut', papua: 'Kabut pegunungan' }[region] || 'Hari yang tenang di perjalanan')
      : (WEATHER[region] || 'A quiet day on the trail');
    document.querySelectorAll('.region-tab').forEach((button) => {
      const label = button.querySelector('[data-region-label]');
      if (label) label.textContent = shortRegion(button.dataset.regionId);
      button.classList.toggle('active', button.dataset.regionId === region);
      button.setAttribute('aria-pressed', button.dataset.regionId === region ? 'true' : 'false');
    });
    const mapPosition = REGION_ORDER.indexOf(region);
    $('regionCount').textContent = String(Math.max(1, mapPosition + 1)).padStart(2, '0');
    const timeState = TIME_STATES[Math.floor((performance.now() - startedAt) / 26000) % TIME_STATES.length];
    $('timeLabel').textContent = t(timeState.key);
  }

  function buildRegionNav() {
    const nav = $('regionNav');
    nav.innerHTML = REGION_ORDER.map((region) => {
      const label = shortRegion(region);
      return `<button class="region-tab" type="button" data-region-id="${region}" aria-pressed="false"><span data-region-label>${escapeHtml(label)}</span></button>`;
    }).join('');
    nav.addEventListener('click', (event) => {
      const button = event.target.closest('[data-region-id]');
      if (!button) return;
      const mapId = PREFERRED_MAP[button.dataset.regionId] || mapIndex.find((entry) => entry.region === button.dataset.regionId)?.id;
      if (mapId) loadMap(mapId);
    });
  }

  function renderTrail() {
    const trail = $('trailLine');
    const currentRegion = mapDef?.region || 'prologue';
    trail.innerHTML = REGION_ORDER.map((region) => {
      const label = titleRegion(region);
      return `<button class="trail-stop ${region === currentRegion ? 'active' : ''}" type="button" data-trail-region="${region}" aria-label="${escapeHtml(t('regionAria', { name: label }))}" title="${escapeHtml(label)}"></button>`;
    }).join('');
  }

  function objectiveKey(questId, objectiveId) { return `${questId}:${objectiveId}`; }

  function getCurrentQuest() {
    const all = questDefs();
    const region = mapDef?.region || 'prologue';
    const completedNote = all.find((quest) => quest.id === state.completedNoteQuestId);
    if (completedNote?.region === region && state.completedQuestIds.has(completedNote.id)) return completedNote;
    const active = all.find((quest) => quest.id === state.activeQuestId);
    if (active?.region === region) return active;
    const local = all.filter((quest) => quest.region === region);
    const sortByChapter = (a, b) => (a.chapter - b.chapter) || a.id.localeCompare(b.id);
    const unfinished = local.filter((quest) => !state.completedQuestIds.has(quest.id)).sort(sortByChapter);
    if (unfinished.length) return unfinished[0];
    const completed = local.filter((quest) => state.completedQuestIds.has(quest.id)).sort(sortByChapter);
    return completed[completed.length - 1] || null;
  }

  function objectiveDone(quest, objective) {
    if (state.completedObjectives.has(objectiveKey(quest.id, objective.id))) return true;
    if (objective.type === 'puzzle' && state.completedPuzzleIds.has(objective.target)) return true;
    return false;
  }

  function updateQuestUI() {
    if (!data) return;
    const quest = getCurrentQuest();
    const questCard = $('questTitle').closest('.quest-card');
    if (!quest) {
      if (questCard) questCard.hidden = true;
      questCard?.classList.remove('is-complete');
      $('questTitle').textContent = t('noQuestTitle');
      $('questSummary').textContent = t('noQuestSummary');
      $('questStatus').textContent = t('freeExploration');
      $('objectiveText').textContent = t('chooseRegion');
      $('questProgressLabel').textContent = t('readyToBegin');
      $('questProgressFill').style.width = '0%';
      return;
    }
    if (questCard) questCard.hidden = false;
    const isActive = state.activeQuestId === quest.id;
    const isComplete = state.completedQuestIds.has(quest.id);
    $('questTitle').closest('.quest-card')?.classList.toggle('is-complete', isComplete);
    const objectives = quest.objectives || [];
    const doneCount = objectives.filter((objective) => objectiveDone(quest, objective)).length;
    const firstOpen = objectives.find((objective) => !objectiveDone(quest, objective));
    $('questTitle').textContent = localizedQuestTitle(quest);
    $('questSummary').textContent = localizedQuestSummary(quest);
    $('questChapter').textContent = shortRegion(quest.region).toLocaleUpperCase(locale);
    $('questStatus').textContent = isComplete ? t('questComplete') : isActive ? t('questActive') : t('questReady');
    const npcName = npcDef(quest.start?.npc).name || t('meetLocalGuide');
    const startObjective = locale === 'id' && quest.id === 'pg_01_notebook'
      ? t('questMeetKeeper')
      : `${t('meetNpc', { name: npcName })}`;
    $('objectiveText').textContent = isComplete ? t('questComplete') :
      (isActive && firstOpen ? localizedObjectiveText(quest, firstOpen) : startObjective);
    $('objectiveCheck').textContent = isComplete ? '✓' : isActive && doneCount > 0 ? '◐' : '○';
    $('questProgressLabel').textContent = `${doneCount} / ${Math.max(1, objectives.length)} ${t('fieldSteps')}`;
    $('questProgressFill').style.width = `${objectives.length ? Math.round(doneCount / objectives.length * 100) : 0}%`;
    $('travellerSubline').textContent = isActive ? t('followingStory') : t('travelerSubline');
    $('cpCount').textContent = String(state.culturePoints).padStart(3, '0');
  }

  function positionForTile(tilePos, offsetY = 16) {
    return { x: Number(tilePos?.[0] || 0) * TILE + TILE / 2, y: Number(tilePos?.[1] || 0) * TILE + offsetY };
  }

  function getRenderables() {
    const entities = [];
    for (const obj of mapDef.objects || []) {
      const pos = obj.pos || [0, 0];
      entities.push({ kind: 'object', id: obj.sprite, obj, info: data.objects[obj.sprite],
        x: pos[0] * TILE + TILE / 2, y: pos[1] * TILE + TILE, orderY: pos[1] * TILE + TILE + 1 });
    }
    for (const obj of mapDef.objects_px || []) {
      const pos = obj.pos || [0, 0];
      entities.push({ kind: 'object', id: obj.sprite, obj, info: data.objects[obj.sprite],
        x: pos[0], y: pos[1], orderY: pos[1] + 1 });
    }
    for (const item of mapDef.interactables || []) {
      if (!item.sprite) continue;
      const pos = positionForTile(item.pos, 16);
      entities.push({ kind: 'interactable-sprite', id: item.id, item, info: data.objects[item.sprite],
        x: pos.x, y: pos.y, orderY: pos.y + 1 });
    }
    for (const npc of mapDef.npcs || []) {
      const pos = positionForTile(npc.pos, 16);
      entities.push({ kind: 'npc', npc, x: pos.x, y: pos.y, orderY: pos.y + 15 });
    }
    for (const landmark of mapDef.landmarks || []) {
      const pos = positionForTile(landmark.pos, 16);
      entities.push({ kind: 'landmark', landmark, x: pos.x, y: pos.y, orderY: pos.y + 3 });
    }
    for (const exit of mapDef.exits || []) {
      const pos = positionForTile(exit.pos, 16);
      entities.push({ kind: 'exit', exit, x: pos.x, y: pos.y, orderY: pos.y + 2 });
    }
    entities.push({ kind: 'player', x: player.x, y: player.y, orderY: player.y + 15 });
    return entities.sort((a, b) => a.orderY - b.orderY);
  }

  function tileVariantName(kind, x, y, elapsed) {
    const legend = data.tilesets._legend || {};
    const names = legend[kind] || legend.GRASS || ['grass0'];
    const value = names.length > 1 ? seededHash(x, y, stringHash(mapDef.id)) % names.length : 0;
    if (kind === 'WATER' || kind === 'DEEP') {
      const animated = Math.floor(elapsed / 470) % names.length;
      return names[(animated + value) % names.length];
    }
    return names[value];
  }

  function drawTerrain(cameraX, cameraY, elapsed) {
    const [mapTilesWide, mapTilesHigh] = mapDef.size || [48, 36];
    const worldW = mapTilesWide * TILE;
    const worldH = mapTilesHigh * TILE;
    const visibleW = canvasWidth / zoom;
    const visibleH = canvasHeight / zoom;
    const startX = Math.max(0, Math.floor((cameraX - visibleW / 2) / TILE) - 1);
    const endX = Math.min(mapTilesWide, Math.ceil((cameraX + visibleW / 2) / TILE) + 1);
    const startY = Math.max(0, Math.floor((cameraY - visibleH / 2) / TILE) - 1);
    const endY = Math.min(mapTilesHigh, Math.ceil((cameraY + visibleH / 2) / TILE) + 1);
    const texture = getImage(`assets/environments/tilesets/terrain_${tileRegion}.png`);
    if (!texture || !texture.complete || !texture.naturalWidth) {
      ctx.fillStyle = '#4f744c'; ctx.fillRect(0, 0, worldW, worldH); return;
    }
    const tiles = tileset.tiles || {};
    for (let y = startY; y < endY; y += 1) {
      for (let x = startX; x < endX; x += 1) {
        const tileName = tileVariantName(terrainGrid[y]?.[x] || 'GRASS', x, y, elapsed);
        const tileData = tiles[tileName] || tiles.grass0;
        const atlas = tileData?.atlas || [0, 0];
        ctx.drawImage(texture, atlas[0] * TILE, atlas[1] * TILE, TILE, TILE, x * TILE, y * TILE, TILE, TILE);
      }
    }
  }

  function drawEntity(entity, elapsed) {
    if (entity.kind === 'object' || entity.kind === 'interactable-sprite') {
      const info = entity.info;
      if (!info) return;
      const texture = getImage(info.file);
      if (!texture || !texture.complete || !texture.naturalWidth) return;
      const size = info.size || [texture.naturalWidth, texture.naturalHeight];
      const scale = Number(entity.obj?.scale || 1);
      const width = Number(size[0]) * scale;
      const height = Number(size[1]) * scale;
      ctx.save();
      if (entity.obj?.flip) {
        ctx.translate(entity.x, 0); ctx.scale(-1, 1); ctx.translate(-entity.x, 0);
      }
      if (entity.kind === 'interactable-sprite') {
        ctx.drawImage(texture, entity.x - width / 2, entity.y - height, width, height);
      } else {
        ctx.drawImage(texture, entity.x - width / 2, entity.y - height, width, height);
      }
      ctx.restore();
      return;
    }
    if (entity.kind === 'npc') {
      drawCharacter(entity.x, entity.y, entity.npc.id, entity.npc.facing || npcDef(entity.npc.id).facing || 'down', false, elapsed);
      return;
    }
    if (entity.kind === 'player') {
      drawCharacter(entity.x, entity.y, 'player', player.facing, player.moving, elapsed);
      return;
    }
    if (entity.kind === 'landmark') {
      const active = currentTarget?.kind === 'landmark' && currentTarget.landmark.id === entity.landmark.id;
      drawWorldGlyph(entity.x, entity.y - 19, active ? '✦' : '·', active ? '#f0d98e' : 'rgba(240,223,161,.7)', active ? 15 : 12);
      return;
    }
    if (entity.kind === 'exit') {
      const active = currentTarget?.kind === 'exit' && currentTarget.exit.id === entity.exit.id;
      drawWorldGlyph(entity.x, entity.y - 14, '⌁', active ? '#eee0a0' : 'rgba(220,230,198,.75)', active ? 19 : 16);
      return;
    }
  }

  function drawCharacter(x, feetY, characterId, facing, moving, elapsed) {
    const definition = data.characters[characterId] || data.characters.player;
    const texture = getImage(definition.sheet);
    if (!texture || !texture.complete || !texture.naturalWidth) return;
    const frameW = Number(definition.frame_w || 32);
    const frameH = Number(definition.frame_h || 48);
    const directions = definition.directions || DIRECTIONS.slice(0, 4);
    let row = directions.indexOf(facing);
    if (row < 0) row = directions.indexOf('down');
    if (row < 0) row = 0;
    const frames = moving ? (definition.walk_frames || [2, 3, 4, 5]) : (definition.idle_frames || [0, 1]);
    const frameIndex = moving ? Math.floor(elapsed / 115) % frames.length : Math.floor(elapsed / 650) % frames.length;
    const col = Number(frames[frameIndex] || 0);
    ctx.save();
    ctx.fillStyle = 'rgba(20,31,20,.3)';
    ctx.beginPath(); ctx.ellipse(x, feetY + 10, 8, 3, 0, 0, Math.PI * 2); ctx.fill();
    ctx.drawImage(texture, col * frameW, row * frameH, frameW, frameH, x - frameW / 2, feetY - frameH + 16, frameW, frameH);
    ctx.restore();
  }

  function drawWorldGlyph(x, y, text, color, size) {
    ctx.save();
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = `700 ${size}px Georgia, serif`;
    ctx.shadowColor = 'rgba(23,31,19,.65)'; ctx.shadowBlur = 5;
    ctx.fillStyle = color; ctx.fillText(text, x, y);
    ctx.restore();
  }

  function getCamera() {
    const [w, h] = mapDef.size || [48, 36];
    const mapW = w * TILE;
    const mapH = h * TILE;
    const halfW = canvasWidth / zoom / 2;
    const halfH = canvasHeight / zoom / 2;
    const x = mapW <= halfW * 2 ? mapW / 2 : Math.max(halfW, Math.min(mapW - halfW, player.x));
    const y = mapH <= halfH * 2 ? mapH / 2 : Math.max(halfH, Math.min(mapH - halfH, player.y));
    return { x, y };
  }

  function drawWorld(now) {
    if (!canvasWidth || !mapDef || !data) return;
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    ctx.imageSmoothingEnabled = false;
    ctx.fillStyle = '#33513a';
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
    const camera = getCamera();
    const elapsed = now - startedAt;
    const timeIndex = Math.floor(elapsed / 26000) % TIME_STATES.length;
    if (timeIndex !== lastTimeState) {
      lastTimeState = timeIndex;
      $('timeLabel').textContent = t(TIME_STATES[timeIndex].key);
    }
    ctx.save();
    ctx.translate(canvasWidth / 2 - camera.x * zoom, canvasHeight / 2 - camera.y * zoom);
    ctx.scale(zoom, zoom);
    drawTerrain(camera.x, camera.y, elapsed);
    for (const entity of getRenderables()) drawEntity(entity, elapsed);
    if (currentTarget) {
      const pos = targetWorldPosition(currentTarget);
      if (pos) {
        ctx.save();
        ctx.strokeStyle = 'rgba(239, 224, 160, .72)';
        ctx.lineWidth = 1.1 / zoom;
        ctx.setLineDash([3 / zoom, 3 / zoom]);
        ctx.beginPath(); ctx.arc(pos.x, pos.y, 13, 0, Math.PI * 2); ctx.stroke();
        ctx.setLineDash([]);
        ctx.restore();
      }
    }
    const tint = TIME_STATES[timeIndex].tint;
    if (tint) {
      const [w, h] = mapDef.size || [48, 36];
      ctx.fillStyle = tint;
      ctx.fillRect(0, 0, w * TILE, h * TILE);
    }
    ctx.restore();
    updateInteractionTarget();
    const tileX = Math.max(0, Math.floor(player.x / TILE));
    const tileY = Math.max(0, Math.floor(player.y / TILE));
    $('coordinates').innerHTML = `${String(tileX).padStart(2, '0')}° · ${String(tileY).padStart(2, '0')}° <span>${escapeHtml(t('coordinatesLabel'))}</span>`;
  }

  function localizedObjectName(sprite) {
    const names = data.objects[sprite]?.inspect_name || {};
    return String(names[locale] || titleCase(String(sprite).replaceAll('_', ' ')));
  }

  function targetWorldPosition(target) {
    if (!target) return null;
    if (target.kind === 'npc') return positionForTile(target.entry.pos, 16);
    if (target.kind === 'interactable') return positionForTile(target.entry.pos, 16);
    if (target.kind === 'landmark') return positionForTile(target.landmark.pos, 16);
    if (target.kind === 'exit') return positionForTile(target.exit.pos, 16);
    if (target.kind === 'prop') return target.pos;
    return null;
  }

  function getTargets() {
    const targets = [];
    for (const entry of mapDef.npcs || []) {
      const definition = npcDef(entry.id);
      const personName = definition.name || (locale === 'id' ? 'Warga' : 'Villager');
      const pos = positionForTile(entry.pos, 16);
      targets.push({ kind: 'npc', entry, id: entry.id, name: locale === 'id' ? t('turnTo', { name: personName }) : `Talk to ${personName}`, pos, radius: 61 });
    }
    for (const entry of mapDef.interactables || []) {
      const pos = positionForTile(entry.pos, 16);
      let label = entry.prompt || entry.title || (entry.kind === 'pickup' ? 'Collect item' : 'Examine');
      const actionKeys = { puzzle: 'openChallenge', pickup: 'collectItem', save: 'saveCheckpoint', note: 'readNote', sign: 'readSign', discovery: 'discovered', landmark: 'discovered' };
      if (entry.kind === 'save') label = t('saveCheckpoint');
      else if (locale === 'id') label = actionKeys[entry.kind] ? t(actionKeys[entry.kind]) : localizedInline(label);
      targets.push({ kind: 'interactable', entry, id: entry.id, name: label, pos, radius: 56 });
    }
    for (const landmark of mapDef.landmarks || []) {
      const pos = positionForTile(landmark.pos, 16);
      targets.push({ kind: 'landmark', landmark, id: landmark.id, name: `${locale === 'id' ? 'Temukan' : 'Discover'} ${localizedInline(landmark.name)}`, pos, radius: 61 });
    }
    for (const exit of mapDef.exits || []) {
      const pos = positionForTile(exit.pos, 16);
      const destination = localizedMapName(mapMeta(exit.target)) || titleCase(exit.target);
      targets.push({ kind: 'exit', exit, id: exit.id, name: t('travelTo', { name: destination }), pos, radius: 47 });
    }
    const props = [
      ...(mapDef.objects || []).map((obj) => ({ obj, pos: {
        x: Number(obj.pos?.[0] || 0) * TILE + TILE / 2,
        y: Number(obj.pos?.[1] || 0) * TILE + TILE
      } })),
      ...(mapDef.objects_px || []).map((obj) => ({ obj, pos: {
        x: Number(obj.pos?.[0] || 0), y: Number(obj.pos?.[1] || 0)
      } }))
    ];
    props.forEach(({ obj, pos }, index) => {
      const sprite = String(obj.sprite || '');
      if (!sprite || !data.objects[sprite]) return;
      const hasAuthoredAction = (mapDef.interactables || []).some((entry) => {
        if (entry.sprite !== sprite) return false;
        const other = positionForTile(entry.pos, 16);
        return Math.hypot(other.x - pos.x, other.y - pos.y) <= TILE * 0.6;
      });
      if (hasAuthoredAction) return;
      const objectName = localizedObjectName(sprite);
      targets.push({ kind: 'prop', obj, id: `prop_${mapDef.id}_${index}`, name: `${t('inspect')} ${objectName}`, pos, radius: 58 });
    });
    return targets;
  }

  function updateInteractionTarget() {
    if (dialogueState || modalState) {
      currentTarget = null;
      interactHint.hidden = true;
      return;
    }
    let closest = null;
    let best = Infinity;
    for (const target of getTargets()) {
      const distance = Math.hypot(player.x - target.pos.x, player.y - target.pos.y);
      if (distance <= target.radius && distance < best) { closest = target; best = distance; }
    }
    currentTarget = closest;
    if (!closest) {
      interactHint.hidden = true;
      return;
    }
    hintText.textContent = closest.name;
    interactHint.hidden = false;
  }

  function hasSolidTileAt(x, y) {
    const tileX = Math.floor(x / TILE);
    const tileY = Math.floor(y / TILE);
    const tileName = terrainGrid[tileY]?.[tileX];
    if (!tileName) return true;
    const names = data.tilesets._legend?.[tileName] || [];
    return names.some((name) => Boolean(tileset.tiles?.[name]?.solid));
  }

  function circleHitsRect(x, y, radius, rect) {
    const nearestX = Math.max(rect.x, Math.min(x, rect.x + rect.w));
    const nearestY = Math.max(rect.y, Math.min(y, rect.y + rect.h));
    return (x - nearestX) ** 2 + (y - nearestY) ** 2 < radius ** 2;
  }

  function isWalkable(x, y) {
    const [tilesWide, tilesHigh] = mapDef.size || [48, 36];
    if (x < 9 || y < 1 || x > tilesWide * TILE - 9 || y > tilesHigh * TILE - 10) return false;
    const bodyY = y + 8;
    const radius = 6;
    if (hasSolidTileAt(x - radius, bodyY) || hasSolidTileAt(x + radius, bodyY) ||
        hasSolidTileAt(x, bodyY - 7) || hasSolidTileAt(x, bodyY + 7)) return false;
    for (const raw of mapDef.collision_rects || []) {
      const rect = { x: raw[0] * TILE, y: raw[1] * TILE, w: raw[2] * TILE, h: raw[3] * TILE };
      if (circleHitsRect(x, bodyY, radius, rect)) return false;
    }
    for (const obj of [...(mapDef.objects || []), ...(mapDef.objects_px || [])]) {
      if (obj.collide === false) continue;
      const info = data.objects[obj.sprite];
      const col = info?.collision;
      if (!col) continue;
      const pos = obj.pos || [0, 0];
      const size = info.size || [32, 32];
      const px = mapDef.objects_px?.includes(obj);
      const centerX = px ? pos[0] : pos[0] * TILE + TILE / 2;
      const baseY = px ? pos[1] : pos[1] * TILE + TILE;
      const scale = Number(obj.scale || 1);
      const rect = {
        x: centerX - size[0] * scale / 2 + Number(col[0]) * scale,
        y: baseY - size[1] * scale + Number(col[1]) * scale,
        w: Number(col[2]) * scale, h: Number(col[3]) * scale
      };
      if (circleHitsRect(x, bodyY, radius, rect)) return false;
    }
    return true;
  }

  function directionFromVector(x, y) {
    const angle = Math.atan2(y, x);
    if (angle >= -Math.PI / 8 && angle < Math.PI / 8) return 'right';
    if (angle >= Math.PI / 8 && angle < 3 * Math.PI / 8) return 'down_right';
    if (angle >= 3 * Math.PI / 8 && angle < 5 * Math.PI / 8) return 'down';
    if (angle >= 5 * Math.PI / 8 && angle < 7 * Math.PI / 8) return 'down_left';
    if (angle >= -3 * Math.PI / 8 && angle < -Math.PI / 8) return 'up_right';
    if (angle >= -5 * Math.PI / 8 && angle < -3 * Math.PI / 8) return 'up';
    if (angle >= -7 * Math.PI / 8 && angle < -5 * Math.PI / 8) return 'up_left';
    return 'left';
  }

  function updatePlayer(delta) {
    const blocked = dialogueState || modalState;
    if (blocked) { player.moving = false; return; }
    let dx = 0; let dy = 0;
    if (keys.has('KeyA') || keys.has('ArrowLeft')) dx -= 1;
    if (keys.has('KeyD') || keys.has('ArrowRight')) dx += 1;
    if (keys.has('KeyW') || keys.has('ArrowUp')) dy -= 1;
    if (keys.has('KeyS') || keys.has('ArrowDown')) dy += 1;
    const length = Math.hypot(dx, dy);
    player.moving = length > 0;
    if (length) {
      dx /= length; dy /= length;
      player.facing = directionFromVector(dx, dy);
      const speed = keys.has('ShiftLeft') || keys.has('ShiftRight') ? 192 : player.speed;
      const step = speed * delta;
      if (isWalkable(player.x + dx * step, player.y)) player.x += dx * step;
      if (isWalkable(player.x, player.y + dy * step)) player.y += dy * step;
      player.walkCycle += delta;
    }
  }

  function triggerTarget(target) {
    if (!target) return;
    if (target.kind === 'npc') { interactWithNPC(target.entry); return; }
    if (target.kind === 'exit') {
      if (mapMeta(target.exit.target)) loadMap(target.exit.target);
      return;
    }
    if (target.kind === 'landmark') { interactWithLandmark(target.landmark); return; }
    if (target.kind === 'interactable') { interactWithObject(target.entry); return; }
    if (target.kind === 'prop') { interactWithProp(target); }
  }

  function findQuestForNpc(npcId) {
    const candidates = questDefs().filter((quest) => quest.giver === npcId && !state.completedQuestIds.has(quest.id));
    return candidates.sort((a, b) => (a.chapter - b.chapter) || a.id.localeCompare(b.id))[0] || null;
  }

  function interactWithNPC(entry) {
    const npcId = entry.id;
    const npc = npcDef(npcId);
    let dialogueId = npc.idle_dialogue || '';
    let offerQuest = null;
    let turnInQuest = null;

    if (state.activeQuestId) {
      const active = questDefs().find((quest) => quest.id === state.activeQuestId);
      if (active?.giver === npcId) {
        const puzzleObjectives = (active.objectives || []).filter((objective) => objective.type === 'puzzle');
        const allPuzzlesDone = puzzleObjectives.every((objective) => state.completedPuzzleIds.has(objective.target));
        if (puzzleObjectives.length && allPuzzlesDone) {
          turnInQuest = active;
          dialogueId = active.turn_in_dialogue || dialogueId;
          completeQuest(active);
        } else {
          const conditional = (npc.conditional_dialogue || []).find((item) => item.if?.quest_active === active.id);
          if (conditional) dialogueId = conditional.dialogue;
        }
      }
    } else {
      const available = findQuestForNpc(npcId);
      if (available && available.region === (mapDef.region || 'prologue')) {
        offerQuest = available;
        dialogueId = available.offer_dialogue || dialogueId;
      }
    }
    player.facing = directionFromVector(entry.pos[0] * TILE + TILE / 2 - player.x, entry.pos[1] * TILE + TILE / 2 - player.y);
    startDialogue(dialogueId, npcId, offerQuest, turnInQuest);
  }

  function interactWithObject(entry) {
    const kind = entry.kind || 'note';
    if (kind === 'puzzle') { openPuzzle(entry.target); return; }
    if (kind === 'pickup') {
      const item = itemDef(entry.target);
      if (item && !state.inventory.some((owned) => owned.id === item.id)) state.inventory.push(item);
      setToast(item ? t('collected', { name: localizedInline(item.name) }) : t('keepsakeFound'));
      updateQuestUI();
      if (entry.target) markObjectiveTarget('collect', entry.target);
      return;
    }
    if (kind === 'door' || kind === 'exit') {
      if (entry.target && mapMeta(entry.target)) loadMap(entry.target);
      else openTextModal(entry.title || entry.prompt || 'A quiet doorway', entry.text || 'This doorway leads somewhere else on the trail.');
      return;
    }
    if (kind === 'landmark' || kind === 'discovery') {
      const culture = data.cultures.entries[entry.target] || null;
      if (culture) state.discoveredCultureIds.add(culture.id);
      openTextModal(entry.title || culture?.name || 'Field discovery', entry.text || culture?.text || entry.description || 'A detail worth remembering for the journal.', true, culture);
      return;
    }
    if (kind === 'save') {
      try {
        localStorage.setItem('jelajah-preview-save', JSON.stringify({ map: mapDef.id, x: player.x, y: player.y }));
        setToast(t('saved'));
      } catch (_) { setToast(t('saveFailed')); }
      return;
    }
    if (kind === 'dialogue' && entry.target) { startDialogue(entry.target, npcIdFromTarget(entry)); return; }
    if (kind === 'flag') { setToast(locale === 'id' ? t('clueNoted') : (entry.prompt || t('clueNoted'))); return; }
    openTextModal(entry.title || entry.prompt || 'Field note', entry.text || entry.description || 'You pause to take in the details around you.');
    if (kind === 'note' || kind === 'sign') markObjectiveTarget('inspect', entry.id);
  }

  function npcIdFromTarget(entry) {
    return String(entry.target || '');
  }

  function interactWithProp(target) {
    const name = localizedObjectName(target.obj.sprite);
    const text = locale === 'id'
      ? `Amati bentuk dan detail ${name} ini, lalu perhatikan letaknya di lingkungan sekitar.`
      : `Observe the shape and details of ${name}. Notice its place in the surrounding environment.`;
    openTextModal(name, text);
  }

  function interactWithLandmark(landmark) {
    const entry = cultureDefs().find((item) => item.region === mapDef.region &&
      (item.name.toLowerCase().includes(landmark.name.toLowerCase()) || landmark.id.includes(item.id)));
    if (entry) state.discoveredCultureIds.add(entry.id);
    openTextModal(landmark.name, landmark.description || 'A landmark recorded in the field journal.', true, entry || null);
  }

  function markObjectiveTarget(type, targetId) {
    if (!state.activeQuestId) return;
    const quest = questDefs().find((entry) => entry.id === state.activeQuestId);
    if (!quest) return;
    const objective = (quest.objectives || []).find((item) => item.type === type && item.target === targetId);
    if (objective) state.completedObjectives.add(objectiveKey(quest.id, objective.id));
    updateQuestUI();
  }

  function startDialogue(dialogueId, speakerNpcId, offerQuest = null, turnInQuest = null) {
    const source = data.dialogues.dialogues[dialogueId];
    const dialogue = source ? localizedDialogue(dialogueId, source) : dialogueFallback(speakerNpcId);
    dialogueState = { dialogue, nodeId: dialogue.start || 'n1', lineIndex: 0, speakerNpcId, offerQuest, turnInQuest, dialogueId };
    dialoguePanel.hidden = false;
    renderDialogue();
  }

  function renderDialogue() {
    if (!dialogueState) return;
    const node = dialogueState.dialogue.nodes?.[dialogueState.nodeId] || {};
    const lines = node.lines || [];
    const speakerId = node.speaker || dialogueState.speakerNpcId;
    const definition = npcDef(speakerId);
    const charId = definition.character || speakerId;
    const character = data.characters[charId];
    $('dialogueSpeaker').textContent = definition.name || (speakerId ? titleCase(speakerId) : (locale === 'id' ? 'Pengembara' : 'Traveler'));
    const portrait = $('dialoguePortrait');
    const portraitPath = character?.portrait || 'assets/portraits/player.png';
    portrait.src = assetUrl(portraitPath);
    portrait.alt = definition.name
      ? `${definition.name}, ${locale === 'id' ? 'sedang berbicara' : 'speaking'}`
      : (locale === 'id' ? 'Potret percakapan' : 'Conversation portrait');
    $('dialogueText').textContent = lines[dialogueState.lineIndex] || '';
    const actions = $('dialogueActions');
    actions.innerHTML = '';
    if (dialogueState.lineIndex < lines.length - 1) {
      actions.innerHTML = `<button class="dialogue-action primary" type="button" data-dialogue-next>${escapeHtml(t('continueLabel'))} <span>→</span></button>`;
      return;
    }
    if (lines.length && dialogueState.lineIndex === lines.length - 1) {
      if (Array.isArray(node.choices) && node.choices.length) {
        actions.innerHTML = node.choices.map((choice, index) => `<button class="dialogue-action ${index === 0 ? 'primary' : ''}" type="button" data-dialogue-choice="${index}">${escapeHtml(choice.text)}</button>`).join('');
      } else if (node.goto) {
        actions.innerHTML = `<button class="dialogue-action primary" type="button" data-dialogue-next>${escapeHtml(t('continueLabel'))} <span>→</span></button>`;
      } else {
        actions.innerHTML = `<button class="dialogue-action primary" type="button" data-dialogue-close>${escapeHtml(t('returnTrail'))} <span>↗</span></button>`;
      }
      return;
    }
    if (Array.isArray(node.choices) && node.choices.length) {
      actions.innerHTML = node.choices.map((choice, index) => `<button class="dialogue-action ${index === 0 ? 'primary' : ''}" type="button" data-dialogue-choice="${index}">${escapeHtml(choice.text)}</button>`).join('');
    } else if (node.goto) {
      actions.innerHTML = `<button class="dialogue-action primary" type="button" data-dialogue-next>${escapeHtml(t('continueLabel'))} <span>→</span></button>`;
    } else {
      actions.innerHTML = `<button class="dialogue-action primary" type="button" data-dialogue-close>${escapeHtml(t('returnTrail'))} <span>↗</span></button>`;
    }
  }

  function advanceDialogue() {
    if (!dialogueState) return;
    const node = dialogueState.dialogue.nodes?.[dialogueState.nodeId] || {};
    const lines = node.lines || [];
    if (dialogueState.lineIndex < lines.length - 1) {
      dialogueState.lineIndex += 1;
      renderDialogue();
      return;
    }
    if (node.goto) {
      dialogueState.nodeId = node.goto;
      dialogueState.lineIndex = 0;
      renderDialogue();
      return;
    }
    if (Array.isArray(node.choices) && node.choices.length) return;
    closeDialogue();
  }

  function chooseDialogueOption(index) {
    if (!dialogueState) return;
    const node = dialogueState.dialogue.nodes?.[dialogueState.nodeId] || {};
    const choice = node.choices?.[index];
    if (!choice) return;
    if (dialogueState.offerQuest && choice.goto === 'yes') {
      state.completedNoteQuestId = null;
      state.activeQuestId = dialogueState.offerQuest.id;
      state.completedObjectives.delete(objectiveKey(dialogueState.offerQuest.id, ''));
      updateQuestUI();
      setToast(t('questStarted', { title: localizedQuestTitle(dialogueState.offerQuest) }));
    }
    if (choice.goto) {
      dialogueState.nodeId = choice.goto;
      dialogueState.lineIndex = 0;
      renderDialogue();
    } else closeDialogue();
  }

  function closeDialogue() {
    dialogueState = null;
    dialoguePanel.hidden = true;
  }

  function completeQuest(quest) {
    if (!quest || state.completedQuestIds.has(quest.id)) return;
    state.completedNoteQuestId = quest.id;
    state.completedQuestIds.add(quest.id);
    state.activeQuestId = null;
    const rewards = quest.rewards || {};
    state.culturePoints += Number(rewards.culture_points || 0);
    for (const id of rewards.items || []) {
      const item = itemDef(id);
      if (item && !state.inventory.some((owned) => owned.id === id)) state.inventory.push(item);
    }
    for (const id of rewards.culture || []) state.discoveredCultureIds.add(id);
    for (const objective of quest.objectives || []) state.completedObjectives.add(objectiveKey(quest.id, objective.id));
    updateQuestUI();
    setToast(t('questFinished', { points: rewards.culture_points || 0 }));
  }

  function openTextModal(title, text, paper = false, culture = null, localization = {}) {
    modalState = { type: 'text', title, text, paper, culture, ...localization };
    renderTextModal();
  }

  function renderTextModal() {
    if (!modalState || modalState.type !== 'text') return;
    const { title, text, paper, culture } = modalState;
    const shownTitle = modalState.titleKey
      ? t(modalState.titleKey)
      : modalState.puzzleTitleId
        ? localizedPuzzleTitle(puzzleDef(modalState.puzzleTitleId))
        : localizedInline(title);
    const sourceText = modalState.textKey ? t(modalState.textKey) : text;
    const shownText = locale === 'id' ? localizedInline(sourceText) : sourceText;
    const cultureText = culture ? localizedCulture(culture, 'text') || localizedCulture(culture, 'short') : '';
    const category = culture ? localizedCategory(culture.category || 'FIELD NOTE') : '';
    const extra = culture ? `<div class="entry-card" style="margin-top:15px"><div class="entry-card-top">${escapeHtml(category)} · ${escapeHtml(titleRegion(culture.region))}${culture.verify ? `<span class="source-verify">${escapeHtml(t('verifySource'))}</span>` : ''}</div><p>${escapeHtml(cultureText)}</p>${culture.source ? `<div class="source">${escapeHtml(locale === 'id' ? 'Sumber:' : 'Source:')} ${escapeHtml(localizedInline(culture.source))}</div>` : ''}</div>` : '';
    rootModal.innerHTML = `<div class="modal-card ${paper ? 'paper' : ''}" role="dialog" aria-modal="true" aria-label="${escapeHtml(shownTitle)}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t(paper ? 'journalFieldNote' : 'fieldInteraction'))}</p><h2 class="modal-title">${escapeHtml(shownTitle)}</h2></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body"><p class="modal-subtitle">${escapeHtml(shownText)}</p>${extra}<p class="modal-footer-note">${escapeHtml(t('recordedMoment'))}</p></div></div>`;
  }

  function openMapModal(selectedRegion = mapDef?.region || 'prologue') {
    modalState = { type: 'map', selectedRegion };
    renderMapModal();
  }

  function renderRegionRouteMap(region, maps, questCount) {
    const routeLayout = routeMapLayouts[region] || {};
    const positions = new Map();
    maps.forEach((entry) => {
      const point = routeLayout[entry.id]?.position || [500, 180];
      positions.set(entry.id, [Number(point[0]) || 500, Number(point[1]) || 180]);
    });
    const edgeKeys = new Set();
    const paths = [];
    for (const entry of maps) {
      const from = positions.get(entry.id);
      for (const targetId of routeLayout[entry.id]?.connections || []) {
        const to = positions.get(targetId);
        if (!to) continue;
        const key = [entry.id, targetId].sort().join('|');
        if (edgeKeys.has(key)) continue;
        edgeKeys.add(key);
        const midX = Math.round((from[0] + to[0]) / 2);
        paths.push(`<path d="M ${from[0]} ${from[1]} C ${midX} ${from[1]}, ${midX} ${to[1]}, ${to[0]} ${to[1]}"/>`);
      }
    }
    const nodes = maps.map((entry, index) => {
      const point = positions.get(entry.id);
      const current = mapDef?.id === entry.id;
      const left = point[0] / 10;
      const top = point[1] / 3.6;
      const label = localizedMapName(entry);
      const state = current ? t('mapNodeCurrent') : t('mapNodeOpen');
      return `<button class="regional-map-node ${current ? 'is-current' : ''}" type="button" data-map-id="${escapeHtml(entry.id)}" aria-label="${escapeHtml(`${label} · ${state}`)}" aria-current="${current ? 'location' : 'false'}" style="left:${left}%;top:${top}%"><span class="regional-map-node-index">${String(index + 1).padStart(2, '0')}</span><strong>${escapeHtml(label)}</strong><small>${escapeHtml(state)}</small></button>`;
    }).join('');
    return `<section class="regional-map-panel" aria-label="${escapeHtml(`${t('mapRouteLabel')} · ${titleRegion(region)}`)}"><div class="regional-map-heading"><span>${escapeHtml(t('mapRouteLabel'))}</span><small>${escapeHtml(t('regionStatsLine', { maps: maps.length, quests: questCount }))}</small></div><p class="regional-map-note">${escapeHtml(t('mapRouteNote'))}</p><div class="regional-map-stage"><svg viewBox="0 0 1000 360" preserveAspectRatio="none" aria-hidden="true"><g>${paths.join('')}</g></svg>${nodes}</div></section>`;
  }

  function renderMapModal() {
    if (!modalState || modalState.type !== 'map') return;
    const selected = modalState.selectedRegion;
    const info = data.regions.regions[selected] || {};
    const regions = REGION_ORDER.map((region, index) => {
      const name = titleRegion(region);
      const tagline = locale === 'id'
        ? (REGION_TAGLINES_ID[region] || '')
        : (data.regions.regions[region]?.tagline || data.regions.regions[region]?.intro || '');
      const mapCount = mapIndex.filter((entry) => entry.region === region).length;
      const questCount = questDefs().filter((quest) => quest.region === region).length;
      return `<button class="region-card ${region === selected ? 'active' : ''}" type="button" data-modal-region="${region}" aria-pressed="${region === selected}"><span class="region-number">${String(index + 1).padStart(2, '0')}</span><strong>${escapeHtml(name)}</strong><span>${escapeHtml(tagline.slice(0, 105))}${tagline.length > 105 ? '…' : ''}</span><small class="region-card-stats">${escapeHtml(t('regionStatsLine', { maps: mapCount, quests: questCount }))}</small></button>`;
    }).join('');
    const maps = mapIndex.filter((entry) => entry.region === selected);
    const regionQuestCount = questDefs().filter((quest) => quest.region === selected).length;
    const routeMap = renderRegionRouteMap(selected, maps, regionQuestCount);
    const mapRows = maps.map((entry, index) => `<button class="list-card" type="button" data-map-id="${escapeHtml(entry.id)}"><span class="list-index">${String(index + 1).padStart(2, '0')}</span><div><strong>${escapeHtml(localizedMapName(entry))}</strong><span>${escapeHtml(titleRegion(entry.region))} · ${escapeHtml(t('openLocation'))}</span></div><b>↗</b></button>`).join('');
    const intro = locale === 'id' ? (REGION_TAGLINES_ID[selected] || t('mapSubtitle')) : (info.tagline || t('mapSubtitle'));
    rootModal.innerHTML = `<div class="modal-card" role="dialog" aria-modal="true" aria-label="${escapeHtml(t('mapTitle'))}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t('mapEyebrow'))}</p><h2 class="modal-title">${escapeHtml(t('mapTitle'))}</h2><p class="modal-subtitle">${escapeHtml(intro)}</p></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body"><div class="modal-grid">${regions}</div>${routeMap}<p class="modal-eyebrow" style="margin-top:22px">${escapeHtml(t('locationsIn', { name: titleRegion(selected).toLocaleUpperCase(locale) }))}</p><div class="map-list">${mapRows || `<div class="empty-state">${escapeHtml(t('noLocations'))}</div>`}</div><p class="modal-footer-note">${escapeHtml(t('previewTravelNote'))}</p></div></div>`;
  }

  function openJournalModal() {
    modalState = { type: 'journal' };
    const current = mapDef?.region || 'prologue';
    const entries = cultureDefs().filter((entry) => entry.region === current);
    const shown = entries.length ? entries : cultureDefs();
    const cards = shown.slice(0, 18).map((entry) => {
      const verify = entry.verify ? `<span class="source-verify">${escapeHtml(t('verifySource'))}</span>` : '';
      const source = entry.source
        ? `<div class="source">${escapeHtml(locale === 'id' ? 'Sumber:' : 'Source:')} ${escapeHtml(localizedInline(entry.source))}</div>`
        : `<div class="source">${escapeHtml(t('sourceNeedsChecking'))}</div>`;
      return `<article class="entry-card"><div class="entry-card-top">${escapeHtml(localizedCategory(entry.category || 'Culture'))} · ${escapeHtml(titleRegion(entry.region))}${verify}</div><h3>${escapeHtml(localizedCulture(entry, 'name'))}</h3><p>${escapeHtml(localizedCulture(entry, 'short') || localizedCulture(entry, 'text'))}</p>${source}</article>`;
    }).join('');
    rootModal.innerHTML = `<div class="modal-card paper" role="dialog" aria-modal="true" aria-label="${escapeHtml(t('journalModalTitle'))}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t('journalEyebrow', { region: titleRegion(current).toLocaleUpperCase(locale) }))}</p><h2 class="modal-title">${escapeHtml(t('journalModalTitle'))}</h2><p class="modal-subtitle">${escapeHtml(t('journalSubtitle'))}</p></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body"><div class="journal-list">${cards || `<div class="empty-state">${escapeHtml(t('noJournalEntries'))}</div>`}</div><p class="modal-footer-note">${escapeHtml(t('languageNote'))}</p></div></div></div>`;
  }

  function openQuestModal(selectedRegion = mapDef?.region || 'prologue') {
    modalState = { type: 'quests', selectedRegion };
    renderQuestModal();
  }

  function renderQuestModal() {
    if (!modalState || modalState.type !== 'quests') return;
    const current = modalState.selectedRegion || mapDef?.region || 'prologue';
    const regionTabs = REGION_ORDER.map((region) => {
      const name = titleRegion(region);
      const count = questDefs().filter((quest) => quest.region === region).length;
      return `<button class="quest-region-tab ${region === current ? 'active' : ''}" type="button" data-quest-region="${region}" aria-label="${escapeHtml(name)} · ${escapeHtml(t('questCountShort', { count }))}" aria-pressed="${region === current}"><strong>${escapeHtml(name)}</strong><small>${escapeHtml(t('questCountShort', { count }))}</small></button>`;
    }).join('');
    const sorted = questDefs().filter((quest) => quest.region === current).sort((a, b) => (a.chapter - b.chapter) || a.id.localeCompare(b.id));
    const cards = sorted.map((quest, index) => {
      const complete = state.completedQuestIds.has(quest.id);
      const active = state.activeQuestId === quest.id;
      const status = complete ? t('statusCompleted') : active ? t('statusTracking') : t('statusAvailable');
      return `<article class="quest-list-item ${complete ? 'is-complete' : ''}"><span class="quest-list-num">${String(index + 1).padStart(2, '0')}</span><div><h3>${escapeHtml(localizedQuestTitle(quest))}</h3><p>${escapeHtml(localizedQuestSummary(quest))}</p><button class="text-link" type="button" data-track-quest="${escapeHtml(quest.id)}">${escapeHtml(t(active ? 'trackingQuest' : 'trackQuest'))} <span>↗</span></button></div><span class="quest-list-status">${escapeHtml(status)}</span></article>`;
    }).join('');
    rootModal.innerHTML = `<div class="modal-card" role="dialog" aria-modal="true" aria-label="${escapeHtml(t('questsTitle'))}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t('questsEyebrow'))}</p><h2 class="modal-title">${escapeHtml(t('questsTitle'))}</h2><p class="modal-subtitle">${escapeHtml(t('questsDescription', { count: sorted.length, region: titleRegion(current) }))}</p></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body"><p class="modal-eyebrow quest-region-label">${escapeHtml(t('questFilterLabel'))}</p><div class="quest-region-tabs" role="group" aria-label="${escapeHtml(t('questFilterLabel'))}">${regionTabs}</div><div class="quests-list">${cards || `<div class="empty-state">${escapeHtml(t('noQuestThreads'))}</div>`}</div><p class="modal-footer-note">${escapeHtml(t('languageNote'))}</p></div></div></div>`;
  }

  function openInventoryModal() {
    modalState = { type: 'inventory' };
    const cards = state.inventory.map((item) => `<article class="inventory-item"><img src="${escapeHtml(assetUrl(item.icon))}" alt=""><strong>${escapeHtml(localizedInline(item.name))}</strong><small>${escapeHtml(locale === 'id' ? (ITEM_CATEGORY_ID[item.category] || titleCase(item.category || 'keepsake')) : titleCase(item.category || 'keepsake'))}</small></article>`).join('');
    rootModal.innerHTML = `<div class="modal-card" role="dialog" aria-modal="true" aria-label="${escapeHtml(t('satchel'))}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t('satchelEyebrow'))}</p><h2 class="modal-title">${escapeHtml(t('inventoryTitle'))}</h2><p class="modal-subtitle">${escapeHtml(t('inventorySubtitle'))}</p></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body">${cards ? `<div class="inventory-grid">${cards}</div>` : `<div class="empty-state">${t('satchelEmpty')}</div>`}<p class="modal-footer-note">${locale === 'id' ? 'Poin Budaya' : 'Culture Points'}: ${state.culturePoints}. ${escapeHtml(t('itemsLocal'))}</p></div></div>`;
  }

  function openPuzzle(puzzleId) {
    const puzzle = puzzleDef(puzzleId);
    if (!puzzle) {
      openTextModal('', '', false, null, { titleKey: 'nearbyChallenge', textKey: 'puzzleNotFoundText' });
      return;
    }
    if (state.completedPuzzleIds.has(puzzleId)) {
      openTextModal('', '', false, null, { puzzleTitleId: puzzleId, textKey: 'puzzleAlreadyDone' });
      return;
    }
    const puzzleState = { type: 'puzzle', puzzleId, hintLevel: 0, moves: 0, success: false, revealed: [], matched: [], cards: [], sequence: [] };
    if (puzzle.type === 'memory' && Array.isArray(puzzle.data?.symbols)) {
      const symbols = localizedPuzzleSymbols(puzzle);
      const cards = [...symbols, ...symbols].map((label, index) => ({ label, key: `${index}` }));
      let seed = stringHash(puzzleId);
      for (let i = cards.length - 1; i > 0; i -= 1) {
        seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
        const j = seed % (i + 1);
        [cards[i], cards[j]] = [cards[j], cards[i]];
      }
      puzzleState.cards = cards;
    } else if (Array.isArray(puzzle.data?.items) && Array.isArray(puzzle.data?.order)) {
      puzzleState.sequence = puzzle.data.items.map((_, index) => index).reverse();
    }
    modalState = puzzleState;
    renderPuzzleModal();
  }

  function renderPuzzleModal() {
    if (!modalState || modalState.type !== 'puzzle') return;
    const puzzle = puzzleDef(modalState.puzzleId);
    const hints = puzzle?.hints || [];
    const hintRows = hints.slice(0, modalState.hintLevel).map((_, index) =>
      `<div class="hint-row"><b>${index + 1}</b><span>${escapeHtml(localizedPuzzleHint(puzzle, index))}</span></div>`).join('');
    const puzzleTitle = localizedPuzzleTitle(puzzle);
    const puzzleDescription = localizedPuzzleDescription(puzzle);
    const typeName = localizedPuzzleType(puzzle.type || 'challenge');
    let puzzleContent = '';
    if (modalState.success) {
      puzzleContent = `<div class="empty-state"><span style="color:#cfbd7e;font-size:24px">✦</span><br>${escapeHtml(t('challengeComplete'))}<br><button class="puzzle-button" type="button" data-action="finish-puzzle">${escapeHtml(t('returnTrail'))}</button></div>`;
    } else if (puzzle.type === 'memory' && modalState.cards.length) {
      const tiles = modalState.cards.map((card, index) => {
        const revealed = modalState.revealed.includes(index) || modalState.matched.includes(index);
        const matched = modalState.matched.includes(index);
        return `<button class="memory-tile ${revealed ? 'revealed' : ''} ${matched ? 'matched' : ''}" type="button" data-memory-index="${index}" ${matched ? 'disabled' : ''}>${revealed ? escapeHtml(card.label) : '✦'}</button>`;
      }).join('');
      puzzleContent = `<div class="memory-grid">${tiles}</div><div class="puzzle-actions"><span class="puzzle-count">${escapeHtml(t('puzzlePairs', { matched: modalState.matched.length / 2, total: modalState.cards.length / 2, moves: modalState.moves }))}</span><button class="puzzle-button" type="button" data-action="show-hint">${escapeHtml(t(modalState.hintLevel < hints.length ? 'askHint' : 'hintsRevealed'))}</button></div>${modalState.hintLevel ? `<div class="hint-stack">${hintRows}</div>` : ''}`;
    } else if (modalState.sequence.length && Array.isArray(puzzle.data?.order)) {
      const items = localizedPuzzleItems(puzzle);
      const rows = modalState.sequence.map((itemIndex, index) => `<div class="list-card"><span class="list-index">${index + 1}</span><div><strong>${escapeHtml(items[itemIndex] || '')}</strong><span>${escapeHtml(t('sequenceStep'))}</span></div><button class="puzzle-button" data-sequence-move="${index}" data-direction="up" type="button" aria-label="${locale === 'id' ? 'Naikkan urutan' : 'Move up'}" ${index === 0 ? 'disabled' : ''}>↑</button><button class="puzzle-button" data-sequence-move="${index}" data-direction="down" type="button" aria-label="${locale === 'id' ? 'Turunkan urutan' : 'Move down'}" ${index === modalState.sequence.length - 1 ? 'disabled' : ''}>↓</button></div>`).join('');
      puzzleContent = `<div class="map-list">${rows}</div><div class="puzzle-actions"><span class="puzzle-count">${escapeHtml(t('sequencePrompt'))}</span><button class="puzzle-button" type="button" data-action="check-sequence">${escapeHtml(t('checkSequence'))}</button></div>`;
      if (modalState.hintLevel) puzzleContent += `<div class="hint-stack">${hintRows}</div>`;
    } else {
      puzzleContent = `<div class="puzzle-feature"><span class="puzzle-feature-label">${escapeHtml(typeName)} · ${escapeHtml(t('regionSpecific'))}</span><p>${escapeHtml(puzzleDescription || t('observeChallenge'))}</p><div class="hint-stack">${hintRows || `<div class="hint-row"><b>✦</b><span>${escapeHtml(t('puzzleFallback'))}</span></div>`}</div><button class="puzzle-button" type="button" data-action="show-hint">${escapeHtml(t(modalState.hintLevel < hints.length ? 'revealHint' : 'returnTrail'))}</button></div><p class="modal-footer-note">${escapeHtml(t('previewChallengeNote'))}</p>`;
    }
    rootModal.innerHTML = `<div class="modal-card" role="dialog" aria-modal="true" aria-label="${escapeHtml(puzzleTitle)}"><div class="modal-head"><div><p class="modal-eyebrow">${escapeHtml(t('puzzleEyebrow', { type: typeName }))}</p><h2 class="modal-title">${escapeHtml(puzzleTitle)}</h2><p class="modal-subtitle">${escapeHtml(puzzleDescription)}</p></div><button class="modal-close" type="button" data-close aria-label="${escapeHtml(t('closeAria'))}">×</button></div><div class="modal-body">${puzzleContent}</div></div>`;
  }

  function registerPuzzleSuccess() {
    if (!modalState || modalState.type !== 'puzzle') return;
    const puzzleId = modalState.puzzleId;
    state.completedPuzzleIds.add(puzzleId);
    if (state.activeQuestId) {
      const quest = questDefs().find((entry) => entry.id === state.activeQuestId);
      for (const objective of quest?.objectives || []) {
        if (objective.type === 'puzzle' && objective.target === puzzleId) state.completedObjectives.add(objectiveKey(quest.id, objective.id));
      }
    }
    modalState.success = true;
    updateQuestUI();
    renderPuzzleModal();
  }

  function handleModalClick(event) {
    if (event.target === rootModal || event.target.closest('[data-close]')) { closeModal(); return; }
    const regionButton = event.target.closest('[data-modal-region]');
    if (regionButton && modalState?.type === 'map') {
      modalState.selectedRegion = regionButton.dataset.modalRegion;
      renderMapModal();
      return;
    }
    const questRegionButton = event.target.closest('[data-quest-region]');
    if (questRegionButton && modalState?.type === 'quests') {
      modalState.selectedRegion = questRegionButton.dataset.questRegion;
      renderQuestModal();
      return;
    }
    const mapButton = event.target.closest('[data-map-id]');
    if (mapButton) { loadMap(mapButton.dataset.mapId); return; }
    const trackButton = event.target.closest('[data-track-quest]');
    if (trackButton) {
      const quest = questDefs().find((entry) => entry.id === trackButton.dataset.trackQuest);
      if (quest) {
        state.completedNoteQuestId = null;
        state.activeQuestId = quest.id;
        updateQuestUI();
        closeModal();
        setToast(t('trackingToast', { title: localizedQuestTitle(quest) }));
      }
      return;
    }
    const memoryButton = event.target.closest('[data-memory-index]');
    if (memoryButton) { selectMemoryCard(Number(memoryButton.dataset.memoryIndex)); return; }
    const sequenceMove = event.target.closest('[data-sequence-move]');
    if (sequenceMove) { moveSequenceItem(Number(sequenceMove.dataset.sequenceMove), sequenceMove.dataset.direction); return; }
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (!action) return;
    if (action === 'show-hint') {
      if (modalState?.type === 'puzzle') {
        const hints = puzzleDef(modalState.puzzleId)?.hints || [];
        if (modalState.hintLevel < hints.length) modalState.hintLevel += 1;
        renderPuzzleModal();
      }
    } else if (action === 'check-sequence') {
      const puzzle = puzzleDef(modalState?.puzzleId);
      const desired = puzzle?.data?.order || [];
      if (desired.length && desired.every((value, index) => modalState.sequence[index] === value)) registerPuzzleSuccess();
      else { modalState.hintLevel = Math.min((puzzle?.hints || []).length, modalState.hintLevel + 1); renderPuzzleModal(); }
    } else if (action === 'finish-puzzle') {
      closeModal();
      setToast(t('recordedMemory'));
    }
  }

  function selectMemoryCard(index) {
    if (!modalState || modalState.type !== 'puzzle' || modalState.success) return;
    if (modalState.revealed.length >= 2 || modalState.matched.includes(index) || modalState.revealed.includes(index)) return;
    modalState.revealed.push(index);
    renderPuzzleModal();
    if (modalState.revealed.length === 2) {
      modalState.moves += 1;
      const [first, second] = modalState.revealed;
      if (modalState.cards[first].label === modalState.cards[second].label) {
        window.setTimeout(() => {
          if (!modalState || modalState.type !== 'puzzle') return;
          modalState.matched.push(first, second);
          modalState.revealed = [];
          if (modalState.matched.length === modalState.cards.length) registerPuzzleSuccess();
          else renderPuzzleModal();
        }, 340);
      } else {
        window.setTimeout(() => {
          if (!modalState || modalState.type !== 'puzzle') return;
          modalState.revealed = [];
          renderPuzzleModal();
        }, 780);
      }
    }
  }

  function moveSequenceItem(index, direction) {
    if (!modalState || modalState.type !== 'puzzle') return;
    const next = direction === 'up' ? index - 1 : index + 1;
    if (next < 0 || next >= modalState.sequence.length) return;
    [modalState.sequence[index], modalState.sequence[next]] = [modalState.sequence[next], modalState.sequence[index]];
    renderPuzzleModal();
  }

  function closeModal() {
    modalState = null;
    rootModal.replaceChildren();
  }

  function toggleAudio() {
    soundEnabled = !soundEnabled;
    $('soundButton').classList.toggle('active', soundEnabled);
    $('soundButton').setAttribute('aria-label', soundEnabled ? t('audioAriaOn') : t('audioAriaOff'));
    $('soundLabel').textContent = t(soundEnabled ? 'soundOn' : 'soundOff');
    $('audioCaption').innerHTML = `<span class="audio-bars"><i></i><i></i><i></i></span> ${t(soundEnabled ? 'audioPlaying' : 'audioAvailable')}`;
    if (soundEnabled) syncAudio();
    else {
      if (ambientAudio) ambientAudio.pause();
      if (musicAudio) musicAudio.pause();
    }
  }

  function syncAudio() {
    if (!mapDef) return;
    const ambientPath = assetUrl(`assets/audio/sfx/${mapDef.ambience || 'amb_village'}.ogg`);
    const musicPath = assetUrl(`assets/audio/music/${mapDef.music || mapDef.region || 'prologue'}.ogg`);
    if (!ambientAudio) { ambientAudio = new Audio(); ambientAudio.loop = true; ambientAudio.volume = 0.20; }
    if (!musicAudio) { musicAudio = new Audio(); musicAudio.loop = true; musicAudio.volume = 0.10; }
    if (ambientAudio.src !== new URL(ambientPath, document.baseURI).href) { ambientAudio.src = ambientPath; }
    if (musicAudio.src !== new URL(musicPath, document.baseURI).href) { musicAudio.src = musicPath; }
    ambientAudio.play().catch(() => {});
    musicAudio.play().catch(() => {});
  }

  function handleKeyDown(event) {
    const key = event.code;
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(key)) event.preventDefault();
    if (event.repeat) { keys.add(key); return; }
    if (key === 'Escape') {
      if (modalState) closeModal();
      else if (dialogueState) closeDialogue();
      else if (document.querySelector('.app-shell')?.classList.contains('fullscreen-fallback')) {
        document.querySelector('.app-shell').classList.remove('fullscreen-fallback');
        syncFullscreenButton();
        resizeCanvas();
      }
      keys.clear();
      return;
    }
    if (key === 'KeyF' && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      toggleFullscreen();
      return;
    }
    if (modalState) return;
    if (dialogueState) {
      if (key === 'KeyE' || key === 'Enter' || key === 'Space') advanceDialogue();
      if (/^Digit[1-9]$/.test(key)) chooseDialogueOption(Number(key.slice(-1)) - 1);
      return;
    }
    if (key === 'KeyE' || key === 'Enter') { triggerTarget(currentTarget); return; }
    if (key === 'KeyM') { openMapModal(); return; }
    if (key === 'KeyJ') { openJournalModal(); return; }
    if (key === 'KeyQ') { openQuestModal(); return; }
    if (key === 'KeyI') { openInventoryModal(); return; }
    if (key === 'Equal' || key === 'NumpadAdd') { zoom = Math.min(2.05, zoom + .12); return; }
    if (key === 'Minus' || key === 'NumpadSubtract') { zoom = Math.max(1.15, zoom - .12); return; }
    keys.add(key);
  }

  function bindUI() {
    window.addEventListener('resize', resizeCanvas);
    if ('ResizeObserver' in window) new ResizeObserver(resizeCanvas).observe($('worldFrame'));
    const onFullscreenChange = () => { syncFullscreenButton(); resizeCanvas(); };
    document.addEventListener('fullscreenchange', onFullscreenChange);
    document.addEventListener('webkitfullscreenchange', onFullscreenChange);
    $('fullscreenButton').addEventListener('click', toggleFullscreen);
    $('languageToggle').addEventListener('click', (event) => {
      const option = event.target.closest('[data-language-label]');
      if (option) setLocale(option.dataset.languageLabel);
    });
    $('mapButton').addEventListener('click', () => openMapModal());
    $('journalButton').addEventListener('click', openJournalModal);
    $('journalCardButton').addEventListener('click', openJournalModal);
    $('questButton').addEventListener('click', openQuestModal);
    $('questQuickButton').addEventListener('click', openQuestModal);
    $('travelButton').addEventListener('click', () => openMapModal());
    $('satchelButton').addEventListener('click', openInventoryModal);
    $('inventoryButton').addEventListener('click', openInventoryModal);
    $('soundButton').addEventListener('click', toggleAudio);
    $('zoomIn').addEventListener('click', () => { zoom = Math.min(2.05, zoom + .12); });
    $('zoomOut').addEventListener('click', () => { zoom = Math.max(1.15, zoom - .12); });
    $('interactHint').addEventListener('click', () => triggerTarget(currentTarget));
    $('dialogueClose').addEventListener('click', closeDialogue);
    $('dialogueActions').addEventListener('click', (event) => {
      if (event.target.closest('[data-dialogue-next]')) advanceDialogue();
      const choice = event.target.closest('[data-dialogue-choice]');
      if (choice) chooseDialogueOption(Number(choice.dataset.dialogueChoice));
      if (event.target.closest('[data-dialogue-close]')) closeDialogue();
    });
    $('trailLine').addEventListener('click', (event) => {
      const button = event.target.closest('[data-trail-region]');
      if (!button) return;
      const mapId = PREFERRED_MAP[button.dataset.trailRegion] || mapIndex.find((entry) => entry.region === button.dataset.trailRegion)?.id;
      if (mapId) loadMap(mapId);
    });
    rootModal.addEventListener('click', handleModalClick);
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', (event) => keys.delete(event.code));
    window.addEventListener('blur', () => keys.clear());
  }

  function animate(now) {
    const delta = Math.min(.05, Math.max(0, (now - (lastFrame || now)) / 1000));
    lastFrame = now;
    updatePlayer(delta);
    drawWorld(now);
    requestAnimationFrame(animate);
  }

  async function init() {
    bindUI();
    applyStaticLocale();
    resizeCanvas();
    try {
      const [regions, tilesets, objects, characters, npcs, quests, dialogues, items, cultures, puzzles, mapList, dialoguesId, contentId, routeMapData] = await Promise.all([
        fetchJSON('../data/regions.json'), fetchJSON('../data/tilesets.json'), fetchJSON('../data/objects.json'),
        fetchJSON('../data/characters.json'), fetchJSON('../data/npcs.json'), fetchJSON('../data/quests.json'),
        fetchJSON('../data/dialogues.json'), fetchJSON('../data/items.json'), fetchJSON('../data/cultures.json'),
        fetchJSON('../data/puzzles.json'), fetchJSON('./maps.json'), fetchJSON('./dialogues_id.json'),
        fetchJSON('./content_id.json'), fetchJSON('../data/route_maps.json')
      ]);
      dialogueTranslationsID = dialoguesId;
      previewContentTranslationsID = contentId.texts || {};
      mapNamesEN = contentId.map_names_en || {};
      routeMapLayouts = routeMapData.maps || {};
      data = { regions, tilesets, objects, characters, npcs, quests, dialogues, items, cultures, puzzles };
      mapIndex = mapList;
      buildRegionNav();
      renderTrail();
      await loadMap('desa_awal', false);
      resizeCanvas();
      requestAnimationFrame(animate);
    } catch (error) {
      console.error(error);
      $('mapTitle').textContent = t('previewCouldNotLoad');
      $('mapTagline').textContent = t('previewLoadHelp');
      ctx.fillStyle = '#263a30'; ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#eee9d7'; ctx.font = '16px system-ui';
      ctx.fillText(t('previewServerHelp'), 28, 48);
    }
  }

  init();
})();
