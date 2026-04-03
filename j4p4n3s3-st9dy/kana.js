// ============================================
// Japanese Reading & Writing Data
// Hiragana, Katakana, N5 Kanji, Daily Words, Grammar
// ============================================

const KANA_DATA = {

// --- HIRAGANA (46 basic + dakuten/combo) ---
hiragana: {
    label: "Hiragana (ひらがな)",
    desc: "Basic Japanese alphabet. Master this first!",
    groups: [
        { name: "Vowels", chars: [
            { char: "あ", romaji: "a", hint: "Like 'ah'" },
            { char: "い", romaji: "i", hint: "Like 'ee'" },
            { char: "う", romaji: "u", hint: "Like 'oo'" },
            { char: "え", romaji: "e", hint: "Like 'eh'" },
            { char: "お", romaji: "o", hint: "Like 'oh'" },
        ]},
        { name: "K-row", chars: [
            { char: "か", romaji: "ka" }, { char: "き", romaji: "ki" },
            { char: "く", romaji: "ku" }, { char: "け", romaji: "ke" }, { char: "こ", romaji: "ko" },
        ]},
        { name: "S-row", chars: [
            { char: "さ", romaji: "sa" }, { char: "し", romaji: "shi" },
            { char: "す", romaji: "su" }, { char: "せ", romaji: "se" }, { char: "そ", romaji: "so" },
        ]},
        { name: "T-row", chars: [
            { char: "た", romaji: "ta" }, { char: "ち", romaji: "chi" },
            { char: "つ", romaji: "tsu" }, { char: "て", romaji: "te" }, { char: "と", romaji: "to" },
        ]},
        { name: "N-row", chars: [
            { char: "な", romaji: "na" }, { char: "に", romaji: "ni" },
            { char: "ぬ", romaji: "nu" }, { char: "ね", romaji: "ne" }, { char: "の", romaji: "no" },
        ]},
        { name: "H-row", chars: [
            { char: "は", romaji: "ha" }, { char: "ひ", romaji: "hi" },
            { char: "ふ", romaji: "fu" }, { char: "へ", romaji: "he" }, { char: "ほ", romaji: "ho" },
        ]},
        { name: "M-row", chars: [
            { char: "ま", romaji: "ma" }, { char: "み", romaji: "mi" },
            { char: "む", romaji: "mu" }, { char: "め", romaji: "me" }, { char: "も", romaji: "mo" },
        ]},
        { name: "Y-row", chars: [
            { char: "や", romaji: "ya" }, { char: "ゆ", romaji: "yu" }, { char: "よ", romaji: "yo" },
        ]},
        { name: "R-row", chars: [
            { char: "ら", romaji: "ra" }, { char: "り", romaji: "ri" },
            { char: "る", romaji: "ru" }, { char: "れ", romaji: "re" }, { char: "ろ", romaji: "ro" },
        ]},
        { name: "W-row + N", chars: [
            { char: "わ", romaji: "wa" }, { char: "を", romaji: "wo" }, { char: "ん", romaji: "n" },
        ]},
        { name: "Dakuten (G)", chars: [
            { char: "が", romaji: "ga" }, { char: "ぎ", romaji: "gi" },
            { char: "ぐ", romaji: "gu" }, { char: "げ", romaji: "ge" }, { char: "ご", romaji: "go" },
        ]},
        { name: "Dakuten (Z)", chars: [
            { char: "ざ", romaji: "za" }, { char: "じ", romaji: "ji" },
            { char: "ず", romaji: "zu" }, { char: "ぜ", romaji: "ze" }, { char: "ぞ", romaji: "zo" },
        ]},
        { name: "Dakuten (D)", chars: [
            { char: "だ", romaji: "da" }, { char: "ぢ", romaji: "di/ji" },
            { char: "づ", romaji: "du/zu" }, { char: "で", romaji: "de" }, { char: "ど", romaji: "do" },
        ]},
        { name: "Dakuten (B)", chars: [
            { char: "ば", romaji: "ba" }, { char: "び", romaji: "bi" },
            { char: "ぶ", romaji: "bu" }, { char: "べ", romaji: "be" }, { char: "ぼ", romaji: "bo" },
        ]},
        { name: "Handakuten (P)", chars: [
            { char: "ぱ", romaji: "pa" }, { char: "ぴ", romaji: "pi" },
            { char: "ぷ", romaji: "pu" }, { char: "ぺ", romaji: "pe" }, { char: "ぽ", romaji: "po" },
        ]},
    ]
},

// --- KATAKANA (46 basic + dakuten) ---
katakana: {
    label: "Katakana (カタカナ)",
    desc: "Used for foreign words, company names, tech terms.",
    groups: [
        { name: "Vowels", chars: [
            { char: "ア", romaji: "a" }, { char: "イ", romaji: "i" },
            { char: "ウ", romaji: "u" }, { char: "エ", romaji: "e" }, { char: "オ", romaji: "o" },
        ]},
        { name: "K-row", chars: [
            { char: "カ", romaji: "ka" }, { char: "キ", romaji: "ki" },
            { char: "ク", romaji: "ku" }, { char: "ケ", romaji: "ke" }, { char: "コ", romaji: "ko" },
        ]},
        { name: "S-row", chars: [
            { char: "サ", romaji: "sa" }, { char: "シ", romaji: "shi" },
            { char: "ス", romaji: "su" }, { char: "セ", romaji: "se" }, { char: "ソ", romaji: "so" },
        ]},
        { name: "T-row", chars: [
            { char: "タ", romaji: "ta" }, { char: "チ", romaji: "chi" },
            { char: "ツ", romaji: "tsu" }, { char: "テ", romaji: "te" }, { char: "ト", romaji: "to" },
        ]},
        { name: "N-row", chars: [
            { char: "ナ", romaji: "na" }, { char: "ニ", romaji: "ni" },
            { char: "ヌ", romaji: "nu" }, { char: "ネ", romaji: "ne" }, { char: "ノ", romaji: "no" },
        ]},
        { name: "H-row", chars: [
            { char: "ハ", romaji: "ha" }, { char: "ヒ", romaji: "hi" },
            { char: "フ", romaji: "fu" }, { char: "ヘ", romaji: "he" }, { char: "ホ", romaji: "ho" },
        ]},
        { name: "M-row", chars: [
            { char: "マ", romaji: "ma" }, { char: "ミ", romaji: "mi" },
            { char: "ム", romaji: "mu" }, { char: "メ", romaji: "me" }, { char: "モ", romaji: "mo" },
        ]},
        { name: "Y-row", chars: [
            { char: "ヤ", romaji: "ya" }, { char: "ユ", romaji: "yu" }, { char: "ヨ", romaji: "yo" },
        ]},
        { name: "R-row", chars: [
            { char: "ラ", romaji: "ra" }, { char: "リ", romaji: "ri" },
            { char: "ル", romaji: "ru" }, { char: "レ", romaji: "re" }, { char: "ロ", romaji: "ro" },
        ]},
        { name: "W-row + N", chars: [
            { char: "ワ", romaji: "wa" }, { char: "ヲ", romaji: "wo" }, { char: "ン", romaji: "n" },
        ]},
        { name: "Dakuten (G)", chars: [
            { char: "ガ", romaji: "ga" }, { char: "ギ", romaji: "gi" },
            { char: "グ", romaji: "gu" }, { char: "ゲ", romaji: "ge" }, { char: "ゴ", romaji: "go" },
        ]},
        { name: "Dakuten (Z)", chars: [
            { char: "ザ", romaji: "za" }, { char: "ジ", romaji: "ji" },
            { char: "ズ", romaji: "zu" }, { char: "ゼ", romaji: "ze" }, { char: "ゾ", romaji: "zo" },
        ]},
        { name: "Dakuten (D)", chars: [
            { char: "ダ", romaji: "da" }, { char: "ヂ", romaji: "di/ji" },
            { char: "ヅ", romaji: "du/zu" }, { char: "デ", romaji: "de" }, { char: "ド", romaji: "do" },
        ]},
        { name: "Dakuten (B)", chars: [
            { char: "バ", romaji: "ba" }, { char: "ビ", romaji: "bi" },
            { char: "ブ", romaji: "bu" }, { char: "ベ", romaji: "be" }, { char: "ボ", romaji: "bo" },
        ]},
        { name: "Handakuten (P)", chars: [
            { char: "パ", romaji: "pa" }, { char: "ピ", romaji: "pi" },
            { char: "プ", romaji: "pu" }, { char: "ペ", romaji: "pe" }, { char: "ポ", romaji: "po" },
        ]},
    ]
},

// --- N5 KANJI (103 essential kanji) ---
kanji: {
    label: "N5 Kanji (漢字)",
    desc: "103 kanji required for JLPT N5.",
    groups: [
        { name: "Numbers", chars: [
            { char: "一", romaji: "ichi", meaning: "one", onyomi: "イチ", kunyomi: "ひと" },
            { char: "二", romaji: "ni", meaning: "two", onyomi: "ニ", kunyomi: "ふた" },
            { char: "三", romaji: "san", meaning: "three", onyomi: "サン", kunyomi: "み" },
            { char: "四", romaji: "shi/yon", meaning: "four", onyomi: "シ", kunyomi: "よ" },
            { char: "五", romaji: "go", meaning: "five", onyomi: "ゴ", kunyomi: "いつ" },
            { char: "六", romaji: "roku", meaning: "six", onyomi: "ロク", kunyomi: "む" },
            { char: "七", romaji: "shichi/nana", meaning: "seven", onyomi: "シチ", kunyomi: "なな" },
            { char: "八", romaji: "hachi", meaning: "eight", onyomi: "ハチ", kunyomi: "や" },
            { char: "九", romaji: "ku/kyuu", meaning: "nine", onyomi: "キュウ", kunyomi: "ここの" },
            { char: "十", romaji: "juu", meaning: "ten", onyomi: "ジュウ", kunyomi: "とお" },
            { char: "百", romaji: "hyaku", meaning: "hundred", onyomi: "ヒャク" },
            { char: "千", romaji: "sen", meaning: "thousand", onyomi: "セン", kunyomi: "ち" },
            { char: "万", romaji: "man", meaning: "ten thousand", onyomi: "マン" },
            { char: "円", romaji: "en", meaning: "yen/circle", onyomi: "エン", kunyomi: "まる" },
        ]},
        { name: "Time & Calendar", chars: [
            { char: "日", romaji: "nichi/hi", meaning: "day/sun", onyomi: "ニチ", kunyomi: "ひ" },
            { char: "月", romaji: "getsu/tsuki", meaning: "month/moon", onyomi: "ゲツ", kunyomi: "つき" },
            { char: "火", romaji: "ka/hi", meaning: "fire/Tuesday", onyomi: "カ", kunyomi: "ひ" },
            { char: "水", romaji: "sui/mizu", meaning: "water/Wednesday", onyomi: "スイ", kunyomi: "みず" },
            { char: "木", romaji: "moku/ki", meaning: "tree/Thursday", onyomi: "モク", kunyomi: "き" },
            { char: "金", romaji: "kin/kane", meaning: "gold/Friday", onyomi: "キン", kunyomi: "かね" },
            { char: "土", romaji: "do/tsuchi", meaning: "earth/Saturday", onyomi: "ド", kunyomi: "つち" },
            { char: "年", romaji: "nen/toshi", meaning: "year", onyomi: "ネン", kunyomi: "とし" },
            { char: "時", romaji: "ji/toki", meaning: "time/hour", onyomi: "ジ", kunyomi: "とき" },
            { char: "分", romaji: "fun/bun", meaning: "minute/part", onyomi: "フン", kunyomi: "わ" },
            { char: "半", romaji: "han", meaning: "half", onyomi: "ハン" },
            { char: "毎", romaji: "mai", meaning: "every", onyomi: "マイ" },
            { char: "今", romaji: "kon/ima", meaning: "now", onyomi: "コン", kunyomi: "いま" },
            { char: "先", romaji: "sen/saki", meaning: "previous/ahead", onyomi: "セン", kunyomi: "さき" },
            { char: "来", romaji: "rai/ku", meaning: "come/next", onyomi: "ライ", kunyomi: "く" },
            { char: "前", romaji: "zen/mae", meaning: "before/front", onyomi: "ゼン", kunyomi: "まえ" },
            { char: "後", romaji: "go/ato", meaning: "after/behind", onyomi: "ゴ", kunyomi: "あと" },
            { char: "午", romaji: "go", meaning: "noon", onyomi: "ゴ" },
            { char: "間", romaji: "kan/aida", meaning: "interval/between", onyomi: "カン", kunyomi: "あいだ" },
            { char: "週", romaji: "shuu", meaning: "week", onyomi: "シュウ" },
        ]},
        { name: "People & Body", chars: [
            { char: "人", romaji: "jin/hito", meaning: "person", onyomi: "ジン", kunyomi: "ひと" },
            { char: "男", romaji: "dan/otoko", meaning: "man", onyomi: "ダン", kunyomi: "おとこ" },
            { char: "女", romaji: "jo/onna", meaning: "woman", onyomi: "ジョ", kunyomi: "おんな" },
            { char: "子", romaji: "shi/ko", meaning: "child", onyomi: "シ", kunyomi: "こ" },
            { char: "母", romaji: "bo/haha", meaning: "mother", onyomi: "ボ", kunyomi: "はは" },
            { char: "父", romaji: "fu/chichi", meaning: "father", onyomi: "フ", kunyomi: "ちち" },
            { char: "友", romaji: "yuu/tomo", meaning: "friend", onyomi: "ユウ", kunyomi: "とも" },
            { char: "目", romaji: "moku/me", meaning: "eye", onyomi: "モク", kunyomi: "め" },
            { char: "耳", romaji: "ji/mimi", meaning: "ear", onyomi: "ジ", kunyomi: "みみ" },
            { char: "口", romaji: "kou/kuchi", meaning: "mouth", onyomi: "コウ", kunyomi: "くち" },
            { char: "手", romaji: "shu/te", meaning: "hand", onyomi: "シュ", kunyomi: "て" },
            { char: "足", romaji: "soku/ashi", meaning: "foot/leg", onyomi: "ソク", kunyomi: "あし" },
        ]},
        { name: "Places & Directions", chars: [
            { char: "国", romaji: "koku/kuni", meaning: "country", onyomi: "コク", kunyomi: "くに" },
            { char: "外", romaji: "gai/soto", meaning: "outside", onyomi: "ガイ", kunyomi: "そと" },
            { char: "中", romaji: "chuu/naka", meaning: "inside/middle", onyomi: "チュウ", kunyomi: "なか" },
            { char: "上", romaji: "jou/ue", meaning: "up/above", onyomi: "ジョウ", kunyomi: "うえ" },
            { char: "下", romaji: "ka/shita", meaning: "down/below", onyomi: "カ", kunyomi: "した" },
            { char: "右", romaji: "u/migi", meaning: "right", onyomi: "ウ", kunyomi: "みぎ" },
            { char: "左", romaji: "sa/hidari", meaning: "left", onyomi: "サ", kunyomi: "ひだり" },
            { char: "北", romaji: "hoku/kita", meaning: "north", onyomi: "ホク", kunyomi: "きた" },
            { char: "南", romaji: "nan/minami", meaning: "south", onyomi: "ナン", kunyomi: "みなみ" },
            { char: "東", romaji: "tou/higashi", meaning: "east", onyomi: "トウ", kunyomi: "ひがし" },
            { char: "西", romaji: "sei/nishi", meaning: "west", onyomi: "セイ", kunyomi: "にし" },
            { char: "山", romaji: "san/yama", meaning: "mountain", onyomi: "サン", kunyomi: "やま" },
            { char: "川", romaji: "sen/kawa", meaning: "river", onyomi: "セン", kunyomi: "かわ" },
            { char: "天", romaji: "ten/ame", meaning: "heaven/sky", onyomi: "テン", kunyomi: "あめ" },
            { char: "気", romaji: "ki", meaning: "spirit/energy", onyomi: "キ" },
            { char: "雨", romaji: "u/ame", meaning: "rain", onyomi: "ウ", kunyomi: "あめ" },
            { char: "電", romaji: "den", meaning: "electricity", onyomi: "デン" },
            { char: "車", romaji: "sha/kuruma", meaning: "car", onyomi: "シャ", kunyomi: "くるま" },
            { char: "駅", romaji: "eki", meaning: "station", onyomi: "エキ" },
            { char: "道", romaji: "dou/michi", meaning: "road/way", onyomi: "ドウ", kunyomi: "みち" },
        ]},
        { name: "Actions & Common", chars: [
            { char: "食", romaji: "shoku/ta", meaning: "eat", onyomi: "ショク", kunyomi: "た" },
            { char: "飲", romaji: "in/no", meaning: "drink", onyomi: "イン", kunyomi: "の" },
            { char: "見", romaji: "ken/mi", meaning: "see/look", onyomi: "ケン", kunyomi: "み" },
            { char: "聞", romaji: "bun/ki", meaning: "hear/ask", onyomi: "ブン", kunyomi: "き" },
            { char: "読", romaji: "doku/yo", meaning: "read", onyomi: "ドク", kunyomi: "よ" },
            { char: "書", romaji: "sho/ka", meaning: "write", onyomi: "ショ", kunyomi: "か" },
            { char: "話", romaji: "wa/hanashi", meaning: "talk/story", onyomi: "ワ", kunyomi: "はなし" },
            { char: "言", romaji: "gen/i", meaning: "say", onyomi: "ゲン", kunyomi: "い" },
            { char: "行", romaji: "kou/i", meaning: "go", onyomi: "コウ", kunyomi: "い" },
            { char: "出", romaji: "shutsu/de", meaning: "exit/go out", onyomi: "シュツ", kunyomi: "で" },
            { char: "入", romaji: "nyuu/hai", meaning: "enter", onyomi: "ニュウ", kunyomi: "はい" },
            { char: "立", romaji: "ritsu/ta", meaning: "stand", onyomi: "リツ", kunyomi: "た" },
            { char: "休", romaji: "kyuu/yasu", meaning: "rest", onyomi: "キュウ", kunyomi: "やす" },
            { char: "買", romaji: "bai/ka", meaning: "buy", onyomi: "バイ", kunyomi: "か" },
            { char: "会", romaji: "kai/a", meaning: "meet", onyomi: "カイ", kunyomi: "あ" },
            { char: "生", romaji: "sei/i", meaning: "life/live", onyomi: "セイ", kunyomi: "い" },
        ]},
        { name: "Size & Quality", chars: [
            { char: "大", romaji: "dai/oo", meaning: "big", onyomi: "ダイ", kunyomi: "おお" },
            { char: "小", romaji: "shou/chii", meaning: "small", onyomi: "ショウ", kunyomi: "ちい" },
            { char: "多", romaji: "ta/oo", meaning: "many", onyomi: "タ", kunyomi: "おお" },
            { char: "少", romaji: "shou/suku", meaning: "few/little", onyomi: "ショウ", kunyomi: "すく" },
            { char: "新", romaji: "shin/atara", meaning: "new", onyomi: "シン", kunyomi: "あたら" },
            { char: "古", romaji: "ko/furu", meaning: "old", onyomi: "コ", kunyomi: "ふる" },
            { char: "高", romaji: "kou/taka", meaning: "high/expensive", onyomi: "コウ", kunyomi: "たか" },
            { char: "安", romaji: "an/yasu", meaning: "cheap/safe", onyomi: "アン", kunyomi: "やす" },
            { char: "長", romaji: "chou/naga", meaning: "long", onyomi: "チョウ", kunyomi: "なが" },
            { char: "白", romaji: "haku/shiro", meaning: "white", onyomi: "ハク", kunyomi: "しろ" },
        ]},
        { name: "School & Study", chars: [
            { char: "学", romaji: "gaku/mana", meaning: "study/learn", onyomi: "ガク", kunyomi: "まな" },
            { char: "校", romaji: "kou", meaning: "school", onyomi: "コウ" },
            { char: "語", romaji: "go", meaning: "language", onyomi: "ゴ" },
            { char: "何", romaji: "ka/nani", meaning: "what", onyomi: "カ", kunyomi: "なに" },
            { char: "名", romaji: "mei/na", meaning: "name", onyomi: "メイ", kunyomi: "な" },
            { char: "花", romaji: "ka/hana", meaning: "flower", onyomi: "カ", kunyomi: "はな" },
            { char: "本", romaji: "hon", meaning: "book/origin", onyomi: "ホン" },
            { char: "店", romaji: "ten/mise", meaning: "shop", onyomi: "テン", kunyomi: "みせ" },
            { char: "社", romaji: "sha", meaning: "company/shrine", onyomi: "シャ" },
        ]},
    ]
},

// --- N5 DAILY WORDS (grouped by topic) ---
dailyWords: {
    label: "Daily Words (ことば)",
    desc: "Essential N5 vocabulary for daily life.",
    groups: [
        { name: "Greetings", words: [
            { word: "おはようございます", romaji: "ohayou gozaimasu", meaning: "good morning (polite)" },
            { word: "こんにちは", romaji: "konnichiwa", meaning: "hello/good afternoon" },
            { word: "こんばんは", romaji: "konbanwa", meaning: "good evening" },
            { word: "さようなら", romaji: "sayounara", meaning: "goodbye" },
            { word: "ありがとうございます", romaji: "arigatou gozaimasu", meaning: "thank you (polite)" },
            { word: "すみません", romaji: "sumimasen", meaning: "excuse me/sorry" },
            { word: "おねがいします", romaji: "onegai shimasu", meaning: "please" },
            { word: "はじめまして", romaji: "hajimemashite", meaning: "nice to meet you" },
        ]},
        { name: "Pronouns & People", words: [
            { word: "わたし", romaji: "watashi", meaning: "I/me" },
            { word: "あなた", romaji: "anata", meaning: "you" },
            { word: "かれ", romaji: "kare", meaning: "he/him" },
            { word: "かのじょ", romaji: "kanojo", meaning: "she/her" },
            { word: "せんせい", romaji: "sensei", meaning: "teacher" },
            { word: "がくせい", romaji: "gakusei", meaning: "student" },
            { word: "ともだち", romaji: "tomodachi", meaning: "friend" },
            { word: "かぞく", romaji: "kazoku", meaning: "family" },
        ]},
        { name: "QC & Work", words: [
            { word: "しごと", romaji: "shigoto", meaning: "work/job" },
            { word: "かいしゃ", romaji: "kaisha", meaning: "company" },
            { word: "ひんしつ", romaji: "hinshitsu", meaning: "quality" },
            { word: "けんさ", romaji: "kensa", meaning: "inspection" },
            { word: "せいひん", romaji: "seihin", meaning: "product" },
            { word: "こうじょう", romaji: "koujou", meaning: "factory" },
            { word: "もんだい", romaji: "mondai", meaning: "problem" },
            { word: "かいぜん", romaji: "kaizen", meaning: "improvement" },
            { word: "データ", romaji: "deeta", meaning: "data" },
            { word: "システム", romaji: "shisutemu", meaning: "system" },
        ]},
        { name: "Time & Frequency", words: [
            { word: "きょう", romaji: "kyou", meaning: "today" },
            { word: "あした", romaji: "ashita", meaning: "tomorrow" },
            { word: "きのう", romaji: "kinou", meaning: "yesterday" },
            { word: "いま", romaji: "ima", meaning: "now" },
            { word: "あさ", romaji: "asa", meaning: "morning" },
            { word: "ひる", romaji: "hiru", meaning: "noon/daytime" },
            { word: "よる", romaji: "yoru", meaning: "night" },
            { word: "まいにち", romaji: "mainichi", meaning: "every day" },
            { word: "いつも", romaji: "itsumo", meaning: "always" },
        ]},
        { name: "Common Verbs", words: [
            { word: "たべます", romaji: "tabemasu", meaning: "eat" },
            { word: "のみます", romaji: "nomimasu", meaning: "drink" },
            { word: "いきます", romaji: "ikimasu", meaning: "go" },
            { word: "きます", romaji: "kimasu", meaning: "come" },
            { word: "します", romaji: "shimasu", meaning: "do" },
            { word: "みます", romaji: "mimasu", meaning: "see/watch" },
            { word: "ききます", romaji: "kikimasu", meaning: "listen/ask" },
            { word: "よみます", romaji: "yomimasu", meaning: "read" },
            { word: "かきます", romaji: "kakimasu", meaning: "write" },
            { word: "はなします", romaji: "hanashimasu", meaning: "speak" },
            { word: "わかります", romaji: "wakarimasu", meaning: "understand" },
            { word: "あります", romaji: "arimasu", meaning: "exist (things)" },
            { word: "います", romaji: "imasu", meaning: "exist (living)" },
        ]},
        { name: "Common Adjectives", words: [
            { word: "おおきい", romaji: "ookii", meaning: "big" },
            { word: "ちいさい", romaji: "chiisai", meaning: "small" },
            { word: "たかい", romaji: "takai", meaning: "expensive/tall" },
            { word: "やすい", romaji: "yasui", meaning: "cheap" },
            { word: "あたらしい", romaji: "atarashii", meaning: "new" },
            { word: "ふるい", romaji: "furui", meaning: "old (things)" },
            { word: "いい", romaji: "ii", meaning: "good" },
            { word: "わるい", romaji: "warui", meaning: "bad" },
            { word: "むずかしい", romaji: "muzukashii", meaning: "difficult" },
            { word: "やさしい", romaji: "yasashii", meaning: "easy/kind" },
        ]},
    ]
},

// --- N5 GRAMMAR PATTERNS ---
grammar: {
    label: "N5 Grammar (ぶんぽう)",
    desc: "Essential grammar patterns for JLPT N5.",
    patterns: [
        { id: "desu", pattern: "〜です", meaning: "is/am/are (polite)", example: "がくせいです。", exampleEn: "I am a student.", level: 1 },
        { id: "wa", pattern: "〜は", meaning: "topic marker", example: "わたしは リーです。", exampleEn: "I am Lee.", level: 1 },
        { id: "ka", pattern: "〜か", meaning: "question marker", example: "がくせいですか。", exampleEn: "Are you a student?", level: 1 },
        { id: "no", pattern: "〜の", meaning: "possessive/of", example: "わたしの ほんです。", exampleEn: "It's my book.", level: 1 },
        { id: "ga", pattern: "〜が", meaning: "subject marker", example: "ねこが います。", exampleEn: "There is a cat.", level: 2 },
        { id: "wo", pattern: "〜を", meaning: "object marker", example: "パンを たべます。", exampleEn: "I eat bread.", level: 2 },
        { id: "ni-time", pattern: "〜に (time)", meaning: "at (time)", example: "7じに おきます。", exampleEn: "I wake up at 7.", level: 2 },
        { id: "ni-place", pattern: "〜に (place)", meaning: "to/in (destination)", example: "がっこうに いきます。", exampleEn: "I go to school.", level: 2 },
        { id: "de-place", pattern: "〜で (place)", meaning: "at (location of action)", example: "うちで たべます。", exampleEn: "I eat at home.", level: 2 },
        { id: "de-means", pattern: "〜で (means)", meaning: "by/with (tool/means)", example: "バスで いきます。", exampleEn: "I go by bus.", level: 2 },
        { id: "to", pattern: "〜と", meaning: "and/with", example: "ともだちと いきます。", exampleEn: "I go with a friend.", level: 2 },
        { id: "mo", pattern: "〜も", meaning: "also/too", example: "わたしも がくせいです。", exampleEn: "I am also a student.", level: 2 },
        { id: "kara-made", pattern: "〜から〜まで", meaning: "from...to...", example: "9じから 5じまで", exampleEn: "From 9 to 5.", level: 3 },
        { id: "masu", pattern: "〜ます", meaning: "polite verb ending", example: "たべます。", exampleEn: "I eat.", level: 1 },
        { id: "masen", pattern: "〜ません", meaning: "polite negative", example: "たべません。", exampleEn: "I don't eat.", level: 2 },
        { id: "mashita", pattern: "〜ました", meaning: "polite past", example: "たべました。", exampleEn: "I ate.", level: 2 },
        { id: "masendeshita", pattern: "〜ませんでした", meaning: "polite negative past", example: "たべませんでした。", exampleEn: "I didn't eat.", level: 2 },
        { id: "tai", pattern: "〜たい", meaning: "want to", example: "たべたいです。", exampleEn: "I want to eat.", level: 3 },
        { id: "te-kudasai", pattern: "〜てください", meaning: "please do~", example: "みてください。", exampleEn: "Please look.", level: 3 },
        { id: "te-imasu", pattern: "〜ています", meaning: "doing/state", example: "たべています。", exampleEn: "I am eating.", level: 3 },
        { id: "nai", pattern: "〜ない", meaning: "casual negative", example: "たべない。", exampleEn: "I don't eat.", level: 3 },
        { id: "i-adj", pattern: "い-adjective", meaning: "adjective ending い", example: "たかいです。", exampleEn: "It is expensive.", level: 2 },
        { id: "na-adj", pattern: "な-adjective", meaning: "adjective + な + noun", example: "しずかな ところ", exampleEn: "A quiet place.", level: 2 },
        { id: "sugiru", pattern: "〜すぎる", meaning: "too much", example: "たかすぎます。", exampleEn: "It's too expensive.", level: 3 },
        { id: "hou-ga-ii", pattern: "〜ほうがいい", meaning: "should/better to", example: "やすんだほうがいい。", exampleEn: "You should rest.", level: 3 },
    ]
}
};

// ============================================
// WORD-FIRST RECOGNITION DATA
// Learn characters THROUGH real words, not isolation.
// Step 1: Ultra-simple real words
// Step 2: Visual grouping with words
// Step 3: High-frequency mini vocabulary
// Step 4: Speed recognition drills
// ============================================

const WORD_FIRST_DATA = [
    // ===== STEP 1: Vowel-only words =====
    {
        level: 1,
        title: "Vowel Words",
        subtitle: "あいうえお through real words",
        focus: ["あ", "い", "う", "え", "お"],
        words: [
            { word: "あい", romaji: "ai", meaning: "love", emoji: "❤️" },
            { word: "いえ", romaji: "ie", meaning: "house", emoji: "🏠" },
            { word: "うえ", romaji: "ue", meaning: "up/above", emoji: "⬆️" },
            { word: "おい", romaji: "oi", meaning: "hey!", emoji: "👋" },
            { word: "あおい", romaji: "aoi", meaning: "blue", emoji: "🔵" },
            { word: "いう", romaji: "iu", meaning: "to say", emoji: "🗣️" },
        ]
    },
    // ===== K-row words =====
    {
        level: 2,
        title: "K-row Words",
        subtitle: "かきくけこ through real words",
        focus: ["か", "き", "く", "け", "こ"],
        words: [
            { word: "かお", romaji: "kao", meaning: "face", emoji: "😊" },
            { word: "きく", romaji: "kiku", meaning: "to listen", emoji: "👂" },
            { word: "くうき", romaji: "kuuki", meaning: "air", emoji: "🌬️" },
            { word: "いけ", romaji: "ike", meaning: "pond", emoji: "🏊" },
            { word: "ここ", romaji: "koko", meaning: "here", emoji: "📍" },
            { word: "こえ", romaji: "koe", meaning: "voice", emoji: "🎤" },
        ]
    },
    // ===== S-row words =====
    {
        level: 3,
        title: "S-row Words",
        subtitle: "さしすせそ through real words",
        focus: ["さ", "し", "す", "せ", "そ"],
        words: [
            { word: "さけ", romaji: "sake", meaning: "salmon/alcohol", emoji: "🍶" },
            { word: "すし", romaji: "sushi", meaning: "sushi", emoji: "🍣" },
            { word: "しお", romaji: "shio", meaning: "salt", emoji: "🧂" },
            { word: "せかい", romaji: "sekai", meaning: "world", emoji: "🌍" },
            { word: "そこ", romaji: "soko", meaning: "there", emoji: "👇" },
            { word: "すき", romaji: "suki", meaning: "like/love", emoji: "💕" },
        ]
    },
    // ===== T-row words =====
    {
        level: 4,
        title: "T-row Words",
        subtitle: "たちつてと through real words",
        focus: ["た", "ち", "つ", "て", "と"],
        words: [
            { word: "たこ", romaji: "tako", meaning: "octopus", emoji: "🐙" },
            { word: "ちち", romaji: "chichi", meaning: "father", emoji: "👨" },
            { word: "つき", romaji: "tsuki", meaning: "moon", emoji: "🌙" },
            { word: "て", romaji: "te", meaning: "hand", emoji: "🤚" },
            { word: "とけい", romaji: "tokei", meaning: "clock", emoji: "⏰" },
            { word: "ちかい", romaji: "chikai", meaning: "near", emoji: "📏" },
        ]
    },
    // ===== N-row words =====
    {
        level: 5,
        title: "N-row Words",
        subtitle: "なにぬねの through real words",
        focus: ["な", "に", "ぬ", "ね", "の"],
        words: [
            { word: "なつ", romaji: "natsu", meaning: "summer", emoji: "☀️" },
            { word: "にく", romaji: "niku", meaning: "meat", emoji: "🥩" },
            { word: "いぬ", romaji: "inu", meaning: "dog", emoji: "🐕" },
            { word: "ねこ", romaji: "neko", meaning: "cat", emoji: "🐱" },
            { word: "この", romaji: "kono", meaning: "this", emoji: "👉" },
            { word: "なに", romaji: "nani", meaning: "what?", emoji: "❓" },
        ]
    },
    // ===== H-row words =====
    {
        level: 6,
        title: "H-row Words",
        subtitle: "はひふへほ through real words",
        focus: ["は", "ひ", "ふ", "へ", "ほ"],
        words: [
            { word: "はな", romaji: "hana", meaning: "flower", emoji: "🌸" },
            { word: "ひと", romaji: "hito", meaning: "person", emoji: "🧑" },
            { word: "ふね", romaji: "fune", meaning: "boat", emoji: "⛵" },
            { word: "へそ", romaji: "heso", meaning: "belly button", emoji: "🔘" },
            { word: "ほし", romaji: "hoshi", meaning: "star", emoji: "⭐" },
            { word: "ひかり", romaji: "hikari", meaning: "light", emoji: "💡" },
        ]
    },
    // ===== M-row words =====
    {
        level: 7,
        title: "M-row Words",
        subtitle: "まみむめも through real words",
        focus: ["ま", "み", "む", "め", "も"],
        words: [
            { word: "まち", romaji: "machi", meaning: "town", emoji: "🏘️" },
            { word: "みず", romaji: "mizu", meaning: "water", emoji: "💧" },
            { word: "むし", romaji: "mushi", meaning: "insect", emoji: "🐛" },
            { word: "め", romaji: "me", meaning: "eye", emoji: "👁️" },
            { word: "もの", romaji: "mono", meaning: "thing", emoji: "📦" },
            { word: "みみ", romaji: "mimi", meaning: "ear", emoji: "👂" },
        ]
    },
    // ===== Y-row + R-row words =====
    {
        level: 8,
        title: "Y & R-row Words",
        subtitle: "やゆよ + らりるれろ through real words",
        focus: ["や", "ゆ", "よ", "ら", "り", "る", "れ", "ろ"],
        words: [
            { word: "やま", romaji: "yama", meaning: "mountain", emoji: "⛰️" },
            { word: "ゆき", romaji: "yuki", meaning: "snow", emoji: "❄️" },
            { word: "よる", romaji: "yoru", meaning: "night", emoji: "🌙" },
            { word: "そら", romaji: "sora", meaning: "sky", emoji: "🌤️" },
            { word: "くるま", romaji: "kuruma", meaning: "car", emoji: "🚗" },
            { word: "れいぞうこ", romaji: "reizouko", meaning: "fridge", emoji: "🧊" },
        ]
    },
    // ===== W-row + ん words =====
    {
        level: 9,
        title: "W-row + ん Words",
        subtitle: "わをん — completing the basics",
        focus: ["わ", "を", "ん"],
        words: [
            { word: "わたし", romaji: "watashi", meaning: "I/me", emoji: "🙋" },
            { word: "みかん", romaji: "mikan", meaning: "mandarin", emoji: "🍊" },
            { word: "にほん", romaji: "nihon", meaning: "Japan", emoji: "🗾" },
            { word: "パンをたべる", romaji: "pan wo taberu", meaning: "eat bread", emoji: "🍞" },
            { word: "えんぴつ", romaji: "enpitsu", meaning: "pencil", emoji: "✏️" },
            { word: "おんせん", romaji: "onsen", meaning: "hot spring", emoji: "♨️" },
        ]
    },

    // ===== STEP 2: Visual Grouping =====
    {
        level: 10,
        title: "Loop Group: め・ぬ・の",
        subtitle: "Similar shapes — learn to tell them apart",
        focus: ["め", "ぬ", "の"],
        visualGroup: true,
        words: [
            { word: "め", romaji: "me", meaning: "eye", emoji: "👁️", tip: "め = eye — see the pupil shape!" },
            { word: "いぬ", romaji: "inu", meaning: "dog", emoji: "🐕", tip: "ぬ = dog word! The loop has a tail" },
            { word: "ねこの", romaji: "neko no", meaning: "cat's", emoji: "🐱", tip: "の = super common 'of' particle" },
            { word: "ぬの", romaji: "nuno", meaning: "cloth", emoji: "🧵", tip: "ぬ (loop+tail) vs の (simple loop)" },
            { word: "めいし", romaji: "meishi", meaning: "business card", emoji: "💳", tip: "め starts the word — spot it fast!" },
        ]
    },
    {
        level: 11,
        title: "Hook Group: は・ほ・ま",
        subtitle: "Characters with vertical + crossing strokes",
        focus: ["は", "ほ", "ま"],
        visualGroup: true,
        words: [
            { word: "はは", romaji: "haha", meaning: "mother", emoji: "👩", tip: "は has two separate parts" },
            { word: "ほし", romaji: "hoshi", meaning: "star", emoji: "⭐", tip: "ほ = は but with extra stroke" },
            { word: "まま", romaji: "mama", meaning: "mama", emoji: "👩‍👧", tip: "ま has a rounder bottom loop" },
            { word: "はほ", romaji: "haho", meaning: "(practice pair)", emoji: "🔄", tip: "は vs ほ — count the strokes!" },
        ]
    },
    {
        level: 12,
        title: "Wave Group: さ・き・ち",
        subtitle: "Characters with a cross + curve",
        focus: ["さ", "き", "ち"],
        visualGroup: true,
        words: [
            { word: "さき", romaji: "saki", meaning: "ahead/future", emoji: "🔮", tip: "さ has one loop, き has two bumps" },
            { word: "ちかい", romaji: "chikai", meaning: "near", emoji: "📏", tip: "ち curves down uniquely" },
            { word: "おさけ", romaji: "osake", meaning: "alcohol", emoji: "🍶", tip: "さ in the middle — spot it!" },
            { word: "きさき", romaji: "kisaki", meaning: "queen", emoji: "👑", tip: "き vs さ side by side" },
        ]
    },
    {
        level: 13,
        title: "Angle Group: け・は・に",
        subtitle: "Characters with two vertical parts",
        focus: ["け", "は", "に"],
        visualGroup: true,
        words: [
            { word: "けいたい", romaji: "keitai", meaning: "phone", emoji: "📱", tip: "け = door + vertical flick" },
            { word: "はし", romaji: "hashi", meaning: "bridge", emoji: "🌉", tip: "は = two similar halves" },
            { word: "にく", romaji: "niku", meaning: "meat", emoji: "🥩", tip: "に = arrow pointing right" },
            { word: "にほん", romaji: "nihon", meaning: "Japan", emoji: "🗾", tip: "に appears in Japan's name!" },
        ]
    },

    // ===== STEP 3: Mini Vocabulary (high-frequency) =====
    {
        level: 14,
        title: "Nature & Objects",
        subtitle: "Daily objects for pattern recognition",
        focus: [],
        words: [
            { word: "みず", romaji: "mizu", meaning: "water", emoji: "💧" },
            { word: "くるま", romaji: "kuruma", meaning: "car", emoji: "🚗" },
            { word: "やま", romaji: "yama", meaning: "mountain", emoji: "⛰️" },
            { word: "そら", romaji: "sora", meaning: "sky", emoji: "🌤️" },
            { word: "かわ", romaji: "kawa", meaning: "river", emoji: "🏞️" },
            { word: "き", romaji: "ki", meaning: "tree", emoji: "🌳" },
            { word: "はな", romaji: "hana", meaning: "flower", emoji: "🌸" },
            { word: "ほし", romaji: "hoshi", meaning: "star", emoji: "⭐" },
        ]
    },
    {
        level: 15,
        title: "People & Basics",
        subtitle: "Essential words you'll use every day",
        focus: [],
        words: [
            { word: "わたし", romaji: "watashi", meaning: "I/me", emoji: "🙋" },
            { word: "あなた", romaji: "anata", meaning: "you", emoji: "👤" },
            { word: "ひと", romaji: "hito", meaning: "person", emoji: "🧑" },
            { word: "こども", romaji: "kodomo", meaning: "child", emoji: "👶" },
            { word: "ともだち", romaji: "tomodachi", meaning: "friend", emoji: "🤝" },
            { word: "せんせい", romaji: "sensei", meaning: "teacher", emoji: "👨‍🏫" },
            { word: "しごと", romaji: "shigoto", meaning: "work", emoji: "💼" },
            { word: "かいしゃ", romaji: "kaisha", meaning: "company", emoji: "🏢" },
        ]
    },
    {
        level: 16,
        title: "Actions & Feelings",
        subtitle: "Verbs & adjectives for real sentences",
        focus: [],
        words: [
            { word: "たべる", romaji: "taberu", meaning: "to eat", emoji: "🍽️" },
            { word: "のむ", romaji: "nomu", meaning: "to drink", emoji: "🥤" },
            { word: "みる", romaji: "miru", meaning: "to see", emoji: "👀" },
            { word: "いく", romaji: "iku", meaning: "to go", emoji: "🚶" },
            { word: "くる", romaji: "kuru", meaning: "to come", emoji: "🏃" },
            { word: "すき", romaji: "suki", meaning: "like", emoji: "💕" },
            { word: "おおきい", romaji: "ookii", meaning: "big", emoji: "🔴" },
            { word: "ちいさい", romaji: "chiisai", meaning: "small", emoji: "🔹" },
        ]
    },
];
