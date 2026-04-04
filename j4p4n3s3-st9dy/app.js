// ============================================
// Japanese Career Coach v3
// Bilingual TTS + JLPT N5 Test + History
// ============================================

// --- State ---
let apiKey = localStorage.getItem("jcoach_apikey") || "";
let model = localStorage.getItem("jcoach_model") || "gpt-4o-mini";
let currentMode = "conversation";
let conversationHistory = [];
let isRecording = false;
let recognition = null;

// --- N5 Level Tracker ---
const N5_TOTAL = 800;
const N5_GRAMMAR = 80;
let learnedWords = JSON.parse(localStorage.getItem("jcoach_words") || "{}");
let learnedGrammar = JSON.parse(localStorage.getItem("jcoach_grammar") || "{}");
let xp = parseInt(localStorage.getItem("jcoach_xp") || "0");
let sessionHistory = JSON.parse(localStorage.getItem("jcoach_history") || "[]");
let jlptTestResults = JSON.parse(localStorage.getItem("jcoach_jlpt_results") || "[]");
let readingProgress = JSON.parse(localStorage.getItem("jcoach_reading") || "{}");
let writingProgress = JSON.parse(localStorage.getItem("jcoach_writing") || "{}");
let userNotes = JSON.parse(localStorage.getItem("jcoach_notes") || "{}");

// Current session tracking
let sessionStart = Date.now();
let sessionWordsLearned = 0;
let sessionMessages = 0;

function saveProgress() {
    localStorage.setItem("jcoach_words", JSON.stringify(learnedWords));
    localStorage.setItem("jcoach_grammar", JSON.stringify(learnedGrammar));
    localStorage.setItem("jcoach_xp", xp.toString());
    localStorage.setItem("jcoach_history", JSON.stringify(sessionHistory));
    localStorage.setItem("jcoach_jlpt_results", JSON.stringify(jlptTestResults));
    localStorage.setItem("jcoach_reading", JSON.stringify(readingProgress));
    localStorage.setItem("jcoach_writing", JSON.stringify(writingProgress));
    localStorage.setItem("jcoach_notes", JSON.stringify(userNotes));
    updateLevelUI();
}

function logSession() {
    if (sessionMessages < 1) return;
    sessionHistory.push({
        date: new Date(sessionStart).toISOString(),
        duration: Math.round((Date.now() - sessionStart) / 60000),
        wordsLearned: sessionWordsLearned,
        messages: sessionMessages,
        mode: currentMode,
        totalWords: Object.keys(learnedWords).length,
        totalGrammar: Object.keys(learnedGrammar).length,
        xp: xp
    });
    // Keep last 100 sessions
    if (sessionHistory.length > 100) sessionHistory = sessionHistory.slice(-100);
    saveProgress();
}

function trackWord(word, reading, meaning) {
    const key = word.trim();
    if (!key) return;
    if (!learnedWords[key]) {
        learnedWords[key] = { reading, meaning, seen: 0, correct: 0, added: Date.now() };
        xp += 5;
        sessionWordsLearned++;
    }
    learnedWords[key].seen++;
    learnedWords[key].lastSeen = Date.now();
    saveProgress();
}

function trackGrammar(point) {
    if (!point) return;
    if (!learnedGrammar[point]) {
        learnedGrammar[point] = { seen: 0, added: Date.now() };
        xp += 10;
    }
    learnedGrammar[point].seen++;
    saveProgress();
}

// --- Progress Calculators ---
// Returns 0-1 representing how much of reading material is learned
// Uses partial credit: each item contributes min(correct, 3) / 3
function getReadingPct() {
    if (typeof KANA_DATA === "undefined") return 0;
    const cats = ["hiragana", "katakana", "kanji", "dailyWords"];
    let totalItems = 0, totalScore = 0;
    cats.forEach(key => {
        const groups = KANA_DATA[key].groups;
        groups.forEach(g => {
            (g.chars || g.words || []).forEach(item => {
                const ch = item.char || item.word;
                totalItems++;
                const p = readingProgress[ch];
                if (p) totalScore += Math.min(p.correct, 3) / 3;
            });
        });
    });
    // Grammar patterns
    KANA_DATA.grammar.patterns.forEach(p => {
        totalItems++;
        const rp = readingProgress[p.pattern];
        if (rp) totalScore += Math.min(rp.correct, 3) / 3;
    });
    return totalItems > 0 ? totalScore / totalItems : 0;
}

function getWritingPct() {
    if (typeof KANA_DATA === "undefined") return 0;
    const cats = ["hiragana", "katakana", "kanji", "dailyWords"];
    let totalItems = 0, totalScore = 0;
    cats.forEach(key => {
        const groups = KANA_DATA[key].groups;
        groups.forEach(g => {
            (g.chars || g.words || []).forEach(item => {
                const ch = item.char || item.word;
                totalItems++;
                const p = writingProgress[ch];
                if (p) totalScore += Math.min(p.correct, 3) / 3;
            });
        });
    });
    KANA_DATA.grammar.patterns.forEach(p => {
        totalItems++;
        const wp = writingProgress[p.pattern];
        if (wp) totalScore += Math.min(wp.correct, 3) / 3;
    });
    return totalItems > 0 ? totalScore / totalItems : 0;
}

function getConversationPct() {
    const wordPct = Math.min(Object.keys(learnedWords).length / N5_TOTAL, 1);
    const gramPct = Math.min(Object.keys(learnedGrammar).length / N5_GRAMMAR, 1);
    return wordPct * 0.6 + gramPct * 0.4;
}

function getLevel() {
    const readPct = getReadingPct();     // 0-1
    const writePct = getWritingPct();    // 0-1
    const convPct = getConversationPct(); // 0-1
    // Weighted: reading 35%, writing 35%, conversation 30%
    const totalPct = (readPct * 0.35 + writePct * 0.35 + convPct * 0.30) * 100;
    if (totalPct >= 90) return { label: "N5 Ready!", sublevel: "N5", pct: totalPct, readPct: readPct * 100, writePct: writePct * 100, convPct: convPct * 100, color: "#4caf50" };
    if (totalPct >= 70) return { label: "N5-", sublevel: "Almost N5", pct: totalPct, readPct: readPct * 100, writePct: writePct * 100, convPct: convPct * 100, color: "#8bc34a" };
    if (totalPct >= 50) return { label: "Pre-N5", sublevel: "Intermediate Beginner", pct: totalPct, readPct: readPct * 100, writePct: writePct * 100, convPct: convPct * 100, color: "#ff9800" };
    if (totalPct >= 25) return { label: "N5--", sublevel: "Elementary", pct: totalPct, readPct: readPct * 100, writePct: writePct * 100, convPct: convPct * 100, color: "#ff5722" };
    return { label: "Beginner", sublevel: "Just Started", pct: totalPct, readPct: readPct * 100, writePct: writePct * 100, convPct: convPct * 100, color: "#f44336" };
}

function updateLevelUI() {
    const lvl = getLevel();
    const bar = document.getElementById("levelBar");
    const label = document.getElementById("levelLabel");
    const stats = document.getElementById("levelStats");
    if (!bar || !label) return;
    bar.style.width = `${Math.max(lvl.pct, 2)}%`;
    bar.style.background = lvl.color;
    label.textContent = `${lvl.label} (${lvl.pct.toFixed(1)}%)`;
    label.style.color = lvl.color;
    if (stats) stats.textContent = `R:${Math.round(lvl.readPct)}% W:${Math.round(lvl.writePct)}% C:${Math.round(lvl.convPct)}% | ${xp} XP`;
}

// --- Word-by-word format instruction for AI ---
const WORD_FORMAT_INSTRUCTION = `
CRITICAL OUTPUT FORMAT: For EVERY Japanese sentence you produce, you MUST include a word-by-word breakdown table IMMEDIATELY after it, using this EXACT format:

[BREAKDOWN]
word1 | reading1 | meaning1 | grammar_note1
word2 | reading2 | meaning2 | grammar_note2
[/BREAKDOWN]

Example:
**品質管理のデジタル化に興味があります。**
(Hinshitsu kanri no dijitaru-ka ni kyoumi ga arimasu.)
= I am interested in QC digitalization.

[BREAKDOWN]
品質管理 | hinshitsu kanri | quality control | compound noun
の | no | possessive particle ('of') | particle
デジタル化 | dijitaru-ka | digitalization | noun + 化(ka)='-ization'
に | ni | to/in (target) | particle
興味 | kyoumi | interest | noun
が | ga | subject marker | particle
あります | arimasu | exists/have | polite form of ある(aru)
[/BREAKDOWN]

Rules for breakdown:
- Every word/particle gets its own row
- grammar_note must explain: particle function, verb form, conjugation, or construction pattern
- Keep grammar notes SHORT (5-10 words max)
- Always include particles (は、が、の、に、で、を、と、も、へ)
- For verbs, note the form (polite/casual/te-form/past/etc.)
`;

const CORRECTION_FORMAT_INSTRUCTION = `
CRITICAL: Whenever the student sends a message (English OR Japanese), you MUST include a correction block BEFORE your main response using this EXACT format:

[CORRECTION]
original: (exactly what the student wrote)
corrected_en: (grammatically correct English version)
corrected_jp: (natural Japanese equivalent with kanji + furigana reading)
romaji: (romaji of the corrected Japanese)
note: (brief explanation of what was wrong or improved, max 15 words)
[/CORRECTION]

Rules for correction:
- ALWAYS include this block, even if the student's message is already correct
- If correct, set note to "Perfect! No correction needed."
- corrected_jp must be NATURAL Japanese, not word-for-word translation
- Include polite form (です/ます) by default
- This block comes FIRST, before your actual teaching response
`;

// --- System Prompts ---
// Helper: check if student has passed N5 (final test with score >= 60%)
function hasPassedN5() {
    return jlptTestResults.some(r => r.isFinal && r.score >= 60);
}

// Helper: get summary of learned words for AI context
function getLearnedWordsSummary() {
    const words = [];
    if (typeof KANA_DATA !== 'undefined') {
        ['hiragana', 'katakana', 'dailyWords'].forEach(cat => {
            const groups = KANA_DATA[cat].groups;
            groups.forEach(g => {
                (g.chars || g.words || []).forEach(item => {
                    const ch = item.char || item.word;
                    const rp = readingProgress[ch];
                    const wp = writingProgress[ch];
                    if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                        words.push(`${ch}(${item.romaji})=${item.meaning || item.hint || ''}`);
                    }
                });
            });
        });
        KANA_DATA.kanji.groups.forEach(g => {
            g.chars.forEach(item => {
                const rp = readingProgress[item.char];
                const wp = writingProgress[item.char];
                if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                    words.push(`${item.char}(${item.romaji})=${item.meaning}`);
                }
            });
        });
    }
    if (typeof WORD_FIRST_DATA !== 'undefined') {
        WORD_FIRST_DATA.forEach(lvl => {
            lvl.words.forEach(w => {
                const rp = readingProgress[w.word];
                const wp = writingProgress[w.word];
                if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                    if (!words.includes(`${w.word}(${w.romaji})=${w.meaning}`)) {
                        words.push(`${w.word}(${w.romaji})=${w.meaning}`);
                    }
                }
            });
        });
    }
    return words;
}

const SYSTEM_PROMPTS = {
    conversation: `You are Reyza's personal Japanese language career coach. Strict but encouraging sensei personality. Help him learn Japanese for a QC Digitalization interview at PT. NSK Bearings Manufacturing Indonesia.

You operate in TWO modes that adapt automatically:
1. FREE TALK: When the student initiates conversation, respond naturally, correct mistakes, and teach vocabulary in context.
2. VOCAB DRILL: When the student says "drill", "practice", "quiz me", or similar, switch to drilling mode — present ONE word/phrase at a time, wait for answer, confirm, give sample sentence WITH breakdown, then next word. After 5 correct, increase difficulty.

IMPORTANT: Prioritize vocabulary from the student's learned word list (provided below). Build on words they already know from Reading/Writing practice. Introduce new related words gradually. Focus on: QC terms, workplace phrases, greetings, daily life, and interview expressions.

${CORRECTION_FORMAT_INSTRUCTION}

${WORD_FORMAT_INSTRUCTION}

Additional rules:
- Mix Japanese and English naturally. Start simple, increase difficulty based on responses.
- Correct mistakes firmly but kindly. Always show the correct form.
- Use QC/manufacturing vocabulary when relevant.
- Keep responses concise (2-4 sentences of Japanese max per turn).
- Encourage with "Yoku dekimashita!" or "Mou sukoshi!" (almost!).
- If he speaks English, teach the Japanese equivalent.

Reyza's background: D3 Mechatronics, 4+ years QC & full-stack dev at PT Dharma Polimetal. Applying to NSK.`,

    interview: `You are a senior Japanese manager at NSK Bearings Manufacturing Indonesia conducting a mock interview for QC Digitalization Staff.

${CORRECTION_FORMAT_INSTRUCTION}

${WORD_FORMAT_INSTRUCTION}

Rules:
- Start with formal Japanese greeting.
- Ask about: self-intro, motivation, experience, QC, technical skills, teamwork, goals.
- Start simple Japanese, gradually increase.
- After each answer: 💡 **[Coach]**: feedback + better Japanese way with breakdown.
- Include cultural tips. Be realistic, firm but fair.
- Format: 🎯 **[Interviewer]**: question`,

    jlpt: `You are a JLPT N5 exam administrator. Generate authentic N5-level test questions.

When asked to generate a test, produce EXACTLY this format:

[JLPT_TEST]
SECTION: Vocabulary (もじ・ごい)
Q1: ＿＿の ことばは どう よみますか。「学生」
A) がくせい
B) がくしょう  
C) がっせい
D) がくせ
ANSWER: A
---
Q2: (next question same format)
ANSWER: X
---
(continue for 5 vocabulary questions)

SECTION: Grammar (ぶんぽう)
Q6: わたしは まいにち コーヒー＿＿ のみます。
A) が
B) を
C) に
D) で
ANSWER: B
---
(continue for 5 grammar questions)

SECTION: Reading (どっかい)
Q11: (short passage followed by question)
A) ...
B) ...
C) ...
D) ...
ANSWER: X
---
(continue for 5 reading questions)
[/JLPT_TEST]

Rules:
- Generate 15 questions: 5 vocabulary, 5 grammar, 5 reading comprehension.
- All content must be genuine N5 level (JLPT standard).
- Vocabulary: kanji reading, word meaning, correct usage.
- Grammar: particles, verb conjugation, sentence patterns, counters.
- Reading: short passages (2-3 sentences) with comprehension questions.
- Vary difficulty within N5 range. Include some tricky distractors.
- Always use the exact format above with [JLPT_TEST] tags.`
};

// --- DOM Elements ---
const $ = (sel) => document.querySelector(sel);
const apiKeyModal = $("#apiKeyModal");
const apiKeyInput = $("#apiKeyInput");
const modelSelect = $("#modelSelect");
const saveKeyBtn = $("#saveKeyBtn");
const settingsBtn = $("#settingsBtn");
const app = $("#app");
const messagesEl = $("#messages");
const textInput = $("#textInput");
const sendBtn = $("#sendBtn");
const micBtn = $("#micBtn");
const voiceStatus = $("#voiceStatus");
const autoSpeak = $("#autoSpeak");
const japaneseVoice = $("#japaneseVoice");
const phraseBook = $("#phraseBook");
const phraseList = $("#phraseList");
const chatArea = $("#chatArea");
const inputArea = $("#inputArea");

// --- Init ---
function init() {
    if (apiKey) showApp();

    saveKeyBtn.addEventListener("click", saveSettings);
    settingsBtn.addEventListener("click", () => {
        apiKeyInput.value = apiKey;
        modelSelect.value = model;
        apiKeyModal.classList.remove("hidden");
    });
    sendBtn.addEventListener("click", sendMessage);
    textInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
    micBtn.addEventListener("click", toggleRecording);

    document.querySelectorAll(".mode-btn").forEach((btn) => {
        btn.addEventListener("click", () => switchMode(btn.dataset.mode));
    });

    initSpeechRecognition();
    updateLevelUI();

    // Close popups on outside click
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".word-popup") && !e.target.closest(".clickable-word")) {
            document.querySelectorAll(".word-popup").forEach((p) => p.remove());
        }
    });

    // Log session on page unload
    window.addEventListener("beforeunload", () => logSession());
}

function saveSettings() {
    const key = apiKeyInput.value.trim();
    if (!key) { apiKeyInput.style.borderColor = "#f44336"; return; }
    apiKey = key;
    model = modelSelect.value;
    localStorage.setItem("jcoach_apikey", apiKey);
    localStorage.setItem("jcoach_model", model);
    showApp();
}

function showApp() {
    apiKeyModal.classList.add("hidden");
    app.classList.remove("hidden");
    addSystemMessage(getModeWelcome(currentMode));
    updateLevelUI();
}

function getModeWelcome(mode) {
    return ({
        conversation: "💬 Practice — Free talk + vocab drill in one! Say \"drill me\" for quiz mode, or just chat freely. Content adapts to your learned words!",
        interview: "🎯 Interview Prep — NSK mock interview, sensei-style!",
        phrases: "📋 My Vocabulary — Words you've learned from Reading & Writing practice.",
        jlpt: "📝 JLPT N5 Mock Test — 15 questions: Vocab, Grammar, Reading. Standard format!",
        history: "📊 Your learning history and progress over time.",
        reading: "📚 Reading Practice — Hiragana → Katakana → Kanji → Words → Grammar. Progressive!",
        writing: "✍️ Writing Practice — Type the correct Japanese from prompts. Build muscle memory!",
        studyplan: "📅 Study Plan — 30-day guided curriculum with Leitner SRS!"
    })[mode] || "";
}

// --- Modes ---
function switchMode(mode) {
    currentMode = mode;
    document.querySelectorAll(".mode-btn").forEach((b) => b.classList.remove("active"));
    const btn = document.querySelector(`[data-mode="${mode}"]`);
    if (btn) btn.classList.add("active");

    // Hide all panels
    chatArea.classList.add("hidden");
    phraseBook.classList.add("hidden");
    inputArea.classList.add("hidden");
    const historyPanel = document.getElementById("historyPanel");
    if (historyPanel) historyPanel.classList.add("hidden");
    const jlptPanel = document.getElementById("jlptPanel");
    if (jlptPanel) jlptPanel.classList.add("hidden");
    const readingPanel = document.getElementById("readingPanel");
    if (readingPanel) readingPanel.classList.add("hidden");
    const writingPanel = document.getElementById("writingPanel");
    if (writingPanel) writingPanel.classList.add("hidden");
    const studyPlanPanel = document.getElementById("studyPlanPanel");
    if (studyPlanPanel) studyPlanPanel.classList.add("hidden");

    if (mode === "studyplan") {
        if (studyPlanPanel) { studyPlanPanel.classList.remove("hidden"); renderStudyPlanPanel(); }
    } else if (mode === "phrases") {
        phraseBook.classList.remove("hidden");
        renderMyVocabulary();
    } else if (mode === "history") {
        if (historyPanel) { historyPanel.classList.remove("hidden"); renderHistory(); }
    } else if (mode === "reading") {
        if (readingPanel) { readingPanel.classList.remove("hidden"); renderReadingPanel(); }
    } else if (mode === "writing") {
        if (writingPanel) { writingPanel.classList.remove("hidden"); renderWritingPanel(); }
    } else if (mode === "interview") {
        if (!hasPassedN5()) {
            // Show locked message
            phraseBook.classList.remove("hidden");
            phraseBook.innerHTML = `<div class="interview-locked">
                <div class="interview-locked-icon">🔒</div>
                <h3>Interview Prep Locked</h3>
                <p>Pass the <strong>JLPT N5 Final Test</strong> to unlock Interview Prep mode.</p>
                <p class="interview-locked-hint">Go to 📝 N5 Test → take the Final Exam and score ≥ 60%</p>
                <button class="btn-primary" style="max-width:200px;margin-top:12px" onclick="switchMode('jlpt')">📝 Go to N5 Test</button>
            </div>`;
            return;
        }
        chatArea.classList.remove("hidden");
        inputArea.classList.remove("hidden");
        conversationHistory = [];
        messagesEl.innerHTML = "";
        addSystemMessage(getModeWelcome(mode));
        sendToAI("Let's begin!");
    } else if (mode === "jlpt") {
        if (jlptPanel) { jlptPanel.classList.remove("hidden"); }
        chatArea.classList.remove("hidden");
        inputArea.classList.remove("hidden");
        conversationHistory = [];
        messagesEl.innerHTML = "";
        addSystemMessage(getModeWelcome(mode));
        renderJLPTStart();
    } else {
        // conversation (practice) mode
        chatArea.classList.remove("hidden");
        inputArea.classList.remove("hidden");
        conversationHistory = [];
        messagesEl.innerHTML = "";
        addSystemMessage(getModeWelcome(mode));
    }
}

// --- JLPT N5 Mock Test ---
let jlptCurrentTest = null;
let jlptAnswers = {};
let jlptIsFinal = false;

function renderJLPTStart() {
    const lvl = getLevel();
    const overallPct = lvl.pct;
    const readPct = lvl.readPct;
    const writePct = lvl.writePct;

    // Gate: unlock practice tests every 10%
    const milestone = Math.floor(overallPct / 10) * 10;
    const nextMilestone = milestone + 10;

    // Final test requires reading >= 80% AND writing >= 80% AND overall >= 90%
    const isFinalReady = readPct >= 80 && writePct >= 80 && overallPct >= 90;
    const isPracticeReady = overallPct >= 10;

    const div = document.createElement("div");
    div.className = "message system";

    let statusHTML = '';
    if (!isPracticeReady) {
        statusHTML = `<div class="jlpt-gate">
            <p>🔒 <strong>Locked</strong> — Reach 10% overall progress to unlock practice tests.</p>
            <div class="jlpt-gate-bar"><div class="jlpt-gate-fill" style="width:${overallPct}%"></div></div>
            <p style="font-size:12px;color:var(--text-dim)">Current: ${overallPct.toFixed(1)}% — Keep studying in Reading & Writing modes!</p>
        </div>`;
    } else {
        statusHTML = `<div class="jlpt-readiness">
            <h4>📊 N5 Readiness</h4>
            <div class="jlpt-ready-row"><span>📚 Reading</span><div class="jlpt-mini-bar"><div class="jlpt-mini-fill" style="width:${readPct}%;background:${readPct >= 80 ? 'var(--success)' : 'var(--accent)'}"></div></div><span>${Math.round(readPct)}%</span><span>${readPct >= 80 ? '✅' : '⬜'}</span></div>
            <div class="jlpt-ready-row"><span>✍️ Writing</span><div class="jlpt-mini-bar"><div class="jlpt-mini-fill" style="width:${writePct}%;background:${writePct >= 80 ? 'var(--success)' : 'var(--accent)'}"></div></div><span>${Math.round(writePct)}%</span><span>${writePct >= 80 ? '✅' : '⬜'}</span></div>
            <div class="jlpt-ready-row"><span>🎯 Overall</span><div class="jlpt-mini-bar"><div class="jlpt-mini-fill" style="width:${overallPct}%;background:${overallPct >= 90 ? 'var(--success)' : 'var(--accent)'}"></div></div><span>${Math.round(overallPct)}%</span><span>${overallPct >= 90 ? '✅' : '⬜'}</span></div>
        </div>
        <p>15 questions across 3 sections:</p>
        <ul>
            <li><strong>Vocabulary (もじ・ごい)</strong> — 5 questions</li>
            <li><strong>Grammar (ぶんぽう)</strong> — 5 questions</li>
            <li><strong>Reading (どっかい)</strong> — 5 questions</li>
        </ul>
        <div style="margin-top:12px">
            <button class="btn-primary" style="max-width:300px" onclick="startJLPTTest()">📝 Practice Test (milestone: ${milestone}%)</button>
        </div>
        ${!isFinalReady ? `<p style="margin-top:8px;font-size:12px;color:var(--warn)">🔒 <strong>Final Certification Test</strong> unlocks when: Reading ≥ 80%, Writing ≥ 80%, Overall ≥ 90%</p>` : `<div style="margin-top:8px"><button class="btn-primary" style="max-width:300px;background:var(--success)" onclick="startJLPTTest(true)">🏆 Final N5 Certification Test</button></div>`}
        ${jlptTestResults.length > 0 ? `<p style="margin-top:8px;font-size:12px;color:var(--text-dim)">Previous scores: ${jlptTestResults.slice(-5).map(r => (r.isFinal ? '🏆' : '') + r.score + '%').join(', ')}</p>` : ''}`;
    }

    div.innerHTML = `
        <div class="jlpt-start">
            <h3>JLPT N5 Mock Test</h3>
            ${statusHTML}
        </div>
    `;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function startJLPTTest(isFinal = false) {
    jlptCurrentTest = null;
    jlptAnswers = {};
    jlptIsFinal = isFinal;
    // Remove start button
    document.querySelector(".jlpt-start")?.closest(".message")?.remove();
    addSystemMessage("Generating your N5 test... (this takes a moment)");
    
    // Ask AI to generate test
    showTyping();
    try {
        const res = await fetch("https://api.openai.com/v1/chat/completions", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
            body: JSON.stringify({
                model: model,
                messages: [
                    { role: "system", content: SYSTEM_PROMPTS.jlpt },
                    { role: "user", content: "Generate a complete JLPT N5 mock test with 15 questions." }
                ],
                temperature: 0.9,
                max_tokens: 2000
            })
        });
        hideTyping();
        if (!res.ok) { addSystemMessage("Failed to generate test. Try again."); return; }
        const data = await res.json();
        const raw = data.choices[0].message.content;
        jlptCurrentTest = parseJLPTTest(raw);
        if (jlptCurrentTest && jlptCurrentTest.length > 0) {
            renderJLPTQuestions(jlptCurrentTest);
        } else {
            addSystemMessage("Test format error. Trying again...");
            // Fallback: show raw
            addMessage(raw, "ai");
        }
    } catch (err) {
        hideTyping();
        addSystemMessage(`Error: ${err.message}`);
    }
}

function parseJLPTTest(raw) {
    const questions = [];
    // Match questions with format: Q1: ... A) ... B) ... C) ... D) ... ANSWER: X
    const qRegex = /Q(\d+):\s*([\s\S]*?)(?=\nA\))\nA\)\s*(.*)\nB\)\s*(.*)\nC\)\s*(.*)\nD\)\s*(.*)\nANSWER:\s*([A-D])/g;
    let m;
    while ((m = qRegex.exec(raw)) !== null) {
        questions.push({
            num: parseInt(m[1]),
            question: m[2].trim(),
            options: { A: m[3].trim(), B: m[4].trim(), C: m[5].trim(), D: m[6].trim() },
            answer: m[7].trim()
        });
    }
    // Also extract sections
    const sectionRegex = /SECTION:\s*(.+)/g;
    let sections = [];
    while ((m = sectionRegex.exec(raw)) !== null) {
        sections.push(m[1].trim());
    }
    // Tag questions with sections
    questions.forEach(q => {
        if (q.num <= 5) q.section = sections[0] || "Vocabulary";
        else if (q.num <= 10) q.section = sections[1] || "Grammar";
        else q.section = sections[2] || "Reading";
    });
    return questions;
}

function renderJLPTQuestions(questions) {
    const div = document.createElement("div");
    div.className = "message ai jlpt-test-container";
    let currentSection = "";
    let html = "";

    questions.forEach(q => {
        if (q.section !== currentSection) {
            currentSection = q.section;
            html += `<div class="jlpt-section-header">${currentSection}</div>`;
        }
        html += `
            <div class="jlpt-question" id="jlpt-q${q.num}">
                <div class="jlpt-q-text">Q${q.num}: ${q.question}</div>
                <div class="jlpt-options">
                    ${['A','B','C','D'].map(letter => `
                        <button class="jlpt-option" data-q="${q.num}" data-letter="${letter}"
                                onclick="selectJLPTAnswer(${q.num}, '${letter}', this)">
                            ${letter}) ${q.options[letter]}
                        </button>
                    `).join("")}
                </div>
            </div>
        `;
    });

    html += `<button class="btn-primary" style="margin-top:16px" onclick="submitJLPTTest()">Submit Test</button>`;
    div.innerHTML = html;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function selectJLPTAnswer(qNum, letter, btn) {
    // Deselect others in same question
    document.querySelectorAll(`[data-q="${qNum}"]`).forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    jlptAnswers[qNum] = letter;
}

function submitJLPTTest() {
    if (!jlptCurrentTest) return;
    let correct = 0;
    let total = jlptCurrentTest.length;
    let sectionScores = { vocab: 0, grammar: 0, reading: 0 };
    let sectionTotals = { vocab: 0, grammar: 0, reading: 0 };

    jlptCurrentTest.forEach(q => {
        const userAnswer = jlptAnswers[q.num];
        const isCorrect = userAnswer === q.answer;
        const qEl = document.getElementById(`jlpt-q${q.num}`);

        // Categorize
        let cat = q.num <= 5 ? "vocab" : q.num <= 10 ? "grammar" : "reading";
        sectionTotals[cat]++;
        if (isCorrect) { correct++; sectionScores[cat]++; }

        // Visual feedback
        if (qEl) {
            qEl.classList.add(isCorrect ? "correct" : "wrong");
            // Highlight correct answer
            qEl.querySelectorAll(".jlpt-option").forEach(btn => {
                const l = btn.dataset.letter;
                if (l === q.answer) btn.classList.add("correct-answer");
                if (l === userAnswer && !isCorrect) btn.classList.add("wrong-answer");
                btn.disabled = true;
            });
        }

        // Track words from questions
        if (isCorrect) xp += 15;
    });

    const score = Math.round((correct / total) * 100);

    // Save result
    jlptTestResults.push({
        date: new Date().toISOString(),
        score,
        correct,
        total,
        isFinal: jlptIsFinal,
        sections: { vocab: sectionScores.vocab, grammar: sectionScores.grammar, reading: sectionScores.reading }
    });
    xp += 50; // Bonus for completing test
    saveProgress();

    // Remove submit button, show result
    document.querySelector(".jlpt-test-container .btn-primary")?.remove();
    const resultDiv = document.createElement("div");
    resultDiv.className = "message system jlpt-result";
    const passed = score >= 60;
    resultDiv.innerHTML = `
        <div class="jlpt-result-card ${passed ? 'pass' : 'fail'}">
            <h3>${passed ? '合格 (PASSED)' : '不合格 (NOT YET)'}</h3>
            <div class="jlpt-score">${score}%</div>
            <div class="jlpt-detail">
                ${correct}/${total} correct | Pass mark: 60%
            </div>
            <div class="jlpt-sections">
                <span>Vocab: ${sectionScores.vocab}/${sectionTotals.vocab}</span>
                <span>Grammar: ${sectionScores.grammar}/${sectionTotals.grammar}</span>
                <span>Reading: ${sectionScores.reading}/${sectionTotals.reading}</span>
            </div>
            <button class="btn-primary" style="margin-top:12px;max-width:200px" onclick="switchMode('jlpt')">Try Again</button>
        </div>
    `;
    messagesEl.appendChild(resultDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

// --- History Panel ---
function renderHistory() {
    const panel = document.getElementById("historyPanel");
    if (!panel) return;

    const wordsArr = Object.entries(learnedWords).sort((a, b) => (b[1].lastSeen || 0) - (a[1].lastSeen || 0));
    const gramArr = Object.entries(learnedGrammar).sort((a, b) => (b[1].seen || 0) - (a[1].seen || 0));
    const lvl = getLevel();

    // Words learned per day (last 14 days)
    const dayMap = {};
    wordsArr.forEach(([, data]) => {
        const day = new Date(data.added).toLocaleDateString();
        dayMap[day] = (dayMap[day] || 0) + 1;
    });

    const last14 = [];
    for (let i = 13; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const key = d.toLocaleDateString();
        last14.push({ day: d.toLocaleDateString("en", { month: "short", day: "numeric" }), count: dayMap[key] || 0 });
    }
    const maxCount = Math.max(...last14.map(d => d.count), 1);

    panel.innerHTML = `
        <div class="history-content">
            <!-- Summary Card -->
            <div class="history-card">
                <h3>Learning Summary</h3>
                <div class="history-stats-grid">
                    <div class="stat-box">
                        <span class="stat-num">${Object.keys(learnedWords).length}</span>
                        <span class="stat-label">Words</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-num">${Object.keys(learnedGrammar).length}</span>
                        <span class="stat-label">Grammar</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-num">${xp}</span>
                        <span class="stat-label">Total XP</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-num" style="color:${lvl.color}">${lvl.label}</span>
                        <span class="stat-label">Level</span>
                    </div>
                </div>
            </div>

            <!-- Activity Chart -->
            <div class="history-card">
                <h3>Words Learned (Last 14 Days)</h3>
                <div class="mini-chart">
                    ${last14.map(d => `
                        <div class="chart-col">
                            <div class="chart-bar" style="height:${Math.max((d.count / maxCount) * 60, 2)}px"></div>
                            <span class="chart-label">${d.day.split(' ')[1]}</span>
                            ${d.count > 0 ? `<span class="chart-val">${d.count}</span>` : ''}
                        </div>
                    `).join("")}
                </div>
            </div>

            <!-- JLPT Test History -->
            <div class="history-card">
                <h3>JLPT N5 Test Results</h3>
                ${jlptTestResults.length === 0 ? '<p style="color:var(--text-dim);font-size:13px">No tests taken yet. Go to JLPT Test mode!</p>' :
                `<div class="test-history-list">
                    ${jlptTestResults.slice(-10).reverse().map(r => {
                        const d = new Date(r.date);
                        const passed = r.score >= 60;
                        return `<div class="test-history-row ${passed ? 'pass' : 'fail'}">
                            <span class="thr-date">${d.toLocaleDateString("en", { month: "short", day: "numeric" })}</span>
                            <span class="thr-score" style="color:${passed ? '#4caf50' : '#f44336'}">${r.score}%</span>
                            <span class="thr-detail">V:${r.sections?.vocab || '?'} G:${r.sections?.grammar || '?'} R:${r.sections?.reading || '?'}</span>
                            <span class="thr-badge">${passed ? '合格' : '不合格'}</span>
                        </div>`;
                    }).join("")}
                </div>`}
            </div>

            <!-- Session History -->
            <div class="history-card">
                <h3>Recent Sessions</h3>
                ${sessionHistory.length === 0 ? '<p style="color:var(--text-dim);font-size:13px">Sessions will be logged when you study.</p>' :
                `<div class="session-list">
                    ${sessionHistory.slice(-10).reverse().map(s => {
                        const d = new Date(s.date);
                        return `<div class="session-row">
                            <span>${d.toLocaleDateString("en", { month: "short", day: "numeric" })} ${d.toLocaleTimeString("en", { hour: "2-digit", minute: "2-digit" })}</span>
                            <span>${s.mode || 'talk'}</span>
                            <span>${s.duration || 0}min</span>
                            <span>+${s.wordsLearned || 0} words</span>
                            <span>${s.messages || 0} msgs</span>
                        </div>`;
                    }).join("")}
                </div>`}
            </div>

            <!-- Word List -->
            <div class="history-card">
                <h3>All Learned Words (${wordsArr.length})</h3>
                <div class="word-list-scroll">
                    ${wordsArr.length === 0 ? '<p style="color:var(--text-dim);font-size:13px">Start learning to see words here!</p>' :
                    wordsArr.slice(0, 50).map(([word, data]) => `
                        <div class="word-list-item">
                            <span class="wli-word">${word}</span>
                            <span class="wli-reading">${data.reading || ''}</span>
                            <span class="wli-meaning">${data.meaning || ''}</span>
                            <span class="wli-seen">x${data.seen}</span>
                        </div>
                    `).join("")}
                    ${wordsArr.length > 50 ? `<p style="color:var(--text-dim);font-size:12px;text-align:center">...and ${wordsArr.length - 50} more</p>` : ''}
                </div>
            </div>

            <!-- Grammar Points -->
            <div class="history-card">
                <h3>Grammar Points (${gramArr.length})</h3>
                <div class="word-list-scroll">
                    ${gramArr.length === 0 ? '<p style="color:var(--text-dim);font-size:13px">Grammar will be tracked from breakdowns!</p>' :
                    gramArr.slice(0, 30).map(([point, data]) => `
                        <div class="word-list-item">
                            <span class="wli-word" style="flex:2">${point}</span>
                            <span class="wli-seen">x${data.seen}</span>
                        </div>
                    `).join("")}
                </div>
            </div>

            <!-- Save / Load Profile -->
            <div class="history-card" style="border-color:var(--accent)">
                <h3 style="color:var(--accent)">💾 Save & Load Progress</h3>
                <p style="font-size:12px;color:var(--text-dim);margin-bottom:4px">
                    Your progress is saved in <strong>this browser only</strong>. Use Save/Load to backup or transfer between devices.
                </p>
                <p style="font-size:11px;color:var(--text-dim);margin-bottom:12px">
                    Last saved: <strong id="lastSaveTime">${localStorage.getItem('jcoach_last_save') ? new Date(localStorage.getItem('jcoach_last_save')).toLocaleString() : 'Never'}</strong>
                </p>
                <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
                    <button class="btn-primary" style="max-width:200px;background:#4a9eff" onclick="exportProgress()">
                        ⬇️ Save to File
                    </button>
                    <button class="btn-primary" style="max-width:200px;background:#2ecc71" onclick="document.getElementById('importFile').click()">
                        ⬆️ Load from File
                    </button>
                    <input type="file" id="importFile" accept=".json" style="display:none" onchange="importProgress(event)">
                </div>
                <div id="saveLoadStatus" style="font-size:12px;display:none;padding:8px 12px;border-radius:8px;margin-bottom:8px"></div>
            </div>

            <!-- Danger Zone -->
            <div class="history-card" style="border-color:#f44336">
                <h3 style="color:#f44336">⚠️ Reset Progress</h3>
                <p style="font-size:12px;color:var(--text-dim);margin-bottom:8px">This will clear all words, grammar, XP, history, and test results.</p>
                <button class="btn-primary" style="background:#f44336;max-width:200px" onclick="if(confirm('Reset ALL progress? This cannot be undone.')){localStorage.clear();location.reload();}">Reset Everything</button>
            </div>
        </div>
    `;
}

// ============================================
// SAVE / LOAD PROGRESS (Export/Import JSON)
// ============================================
const SAVE_KEYS = [
    'jcoach_words', 'jcoach_grammar', 'jcoach_xp', 'jcoach_history',
    'jcoach_jlpt_results', 'jcoach_reading', 'jcoach_writing', 'jcoach_notes',
    'jcoach_srs', 'jcoach_studyplan', 'jcoach_sp_completed',
    'jcoach_wr', 'jcoach_kb_size'
];

function showSaveLoadStatus(msg, isError) {
    const el = document.getElementById('saveLoadStatus');
    if (!el) return;
    el.style.display = 'block';
    el.style.background = isError ? 'rgba(244,67,54,0.15)' : 'rgba(46,204,113,0.15)';
    el.style.color = isError ? '#f44336' : '#2ecc71';
    el.textContent = msg;
    setTimeout(() => { el.style.display = 'none'; }, 4000);
}

function exportProgress() {
    const data = { _meta: { app: 'JapaneseCoach', version: 3, exported: new Date().toISOString() } };
    SAVE_KEYS.forEach(key => {
        const val = localStorage.getItem(key);
        if (val !== null) data[key] = val;
    });
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const d = new Date();
    a.href = url;
    a.download = `jcoach_save_${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    localStorage.setItem('jcoach_last_save', new Date().toISOString());
    showSaveLoadStatus('✅ Progress saved to file!', false);
    const ts = document.getElementById('lastSaveTime');
    if (ts) ts.textContent = new Date().toLocaleString();
}

function importProgress(event) {
    const file = event.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.json')) {
        showSaveLoadStatus('❌ Please select a .json file', true);
        event.target.value = '';
        return;
    }
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            // Validate it's a JapaneseCoach save
            if (!data._meta || data._meta.app !== 'JapaneseCoach') {
                showSaveLoadStatus('❌ Invalid save file. Not a Japanese Coach backup.', true);
                return;
            }
            // Count what we're loading
            let loaded = 0;
            SAVE_KEYS.forEach(key => {
                if (data[key] !== undefined) {
                    localStorage.setItem(key, data[key]);
                    loaded++;
                }
            });
            showSaveLoadStatus(`✅ Loaded ${loaded} data entries. Reloading...`, false);
            setTimeout(() => location.reload(), 1500);
        } catch (err) {
            showSaveLoadStatus('❌ Error reading file: ' + err.message, true);
        }
    };
    reader.readAsText(file);
    event.target.value = '';
}

// ============================================
// READING PRACTICE MODE
// Progressive: Hiragana → Katakana → Kanji → Words → Grammar
// ============================================
let readingQuiz = { items: [], current: 0, correct: 0, category: "", group: "" };

function getReadingMastery(char) {
    return readingProgress[char] || { correct: 0, seen: 0, mastered: false };
}

function markReadingResult(char, isCorrect) {
    if (!readingProgress[char]) readingProgress[char] = { correct: 0, seen: 0, mastered: false };
    readingProgress[char].seen++;
    if (isCorrect) {
        readingProgress[char].correct++;
        xp += 3;
    }
    if (readingProgress[char].correct >= 3) readingProgress[char].mastered = true;
    saveProgress();
}

function renderReadingPanel(scrollToLevel) {
    const panel = document.getElementById("readingPanel");
    if (!panel || typeof KANA_DATA === "undefined") { panel.innerHTML = "<p>Loading data...</p>"; return; }

    // Determine which sections should be open
    const openSections = JSON.parse(localStorage.getItem('jcoach_rp_open') || '{"hiragana":true,"katakana":true,"kanji":true,"traditional":false}');

    let html = `<div class="rw-content"><h2 class="rw-title">📚 Reading Practice</h2>
        <p class="rw-subtitle">Step 1: Learn individual characters with mnemonics. Step 2: Apply to real words.</p>`;

    // === STEP 1: Traditional Character Recognition ===
    const tradOpen = openSections.traditional !== false;
    html += `<details class="rw-collapsible" ${tradOpen ? 'open' : ''} data-section="traditional">
        <summary class="wr-section-header wr-script-header wr-traditional">
            <span class="wr-script-label">🎯 Step 1 — Character Recognition</span>
            <span class="wr-script-pct">Master each character first</span>
            <span class="wr-collapse-icon"></span>
        </summary>
        <div class="rw-collapsible-body">`;

    const categories = [
        { key: "hiragana", data: KANA_DATA.hiragana, icon: "あ" },
        { key: "katakana", data: KANA_DATA.katakana, icon: "ア" },
        { key: "kanji", data: KANA_DATA.kanji, icon: "漢" },
        { key: "dailyWords", data: KANA_DATA.dailyWords, icon: "語" },
        { key: "grammar", data: KANA_DATA.grammar, icon: "文" },
    ];

    categories.forEach(cat => {
        const groups = cat.key === "grammar" ? [{ name: "All Patterns", chars: cat.data.patterns.map(p => ({ char: p.pattern, romaji: p.id })) }] : cat.data.groups;
        const allChars = groups.flatMap(g => (g.chars || g.words || []).map(c => c.char || c.word));
        const learned = allChars.filter(c => readingProgress[c] && readingProgress[c].correct > 0).length;
        const pct = allChars.length > 0 ? Math.round((learned / allChars.length) * 100) : 0;
        const catOpen = openSections[cat.key] !== false;

        html += `<details class="rw-collapsible" ${catOpen ? 'open' : ''} data-section="${cat.key}">
            <summary class="rw-cat-header rw-collapsible-header">
                <span class="rw-cat-icon">${cat.icon}</span>
                <div class="rw-cat-info"><h3>${cat.data.label}</h3><p>${cat.data.desc}</p></div>
                <div class="rw-cat-progress"><span class="rw-cat-pct">${pct}%</span><span class="rw-cat-count">${learned}/${allChars.length}</span></div>
                <span class="wr-collapse-icon"></span>
            </summary>
            <div class="rw-progress-bar"><div class="rw-progress-fill" style="width:${pct}%"></div></div>
            <div class="rw-groups">`;
        if (cat.key === "grammar") {
            html += `<div class="rw-group-row">
                <button class="rw-study-btn" onclick="startReadingStudy('grammar','patterns')">📖 Study</button>
                <button class="rw-quiz-btn" onclick="startReadingQuiz('grammar','patterns')">🧠 Quiz</button>
            </div>`;
        } else {
            groups.forEach((g, idx) => {
                const gChars = (g.chars || g.words || []).map(c => c.char || c.word);
                const gLearned = gChars.filter(c => readingProgress[c] && readingProgress[c].correct > 0).length;
                const prevBtn = idx > 0 ? `<button class="wr-nav-btn" onclick="document.querySelectorAll('[data-section=\\'${cat.key}\\'] .rw-group-row')[${idx - 1}].scrollIntoView({behavior:'smooth',block:'center'})">◀ Prev</button>` : '<span></span>';
                const nextBtn = idx < groups.length - 1 ? `<button class="wr-nav-btn" onclick="document.querySelectorAll('[data-section=\\'${cat.key}\\'] .rw-group-row')[${idx + 1}].scrollIntoView({behavior:'smooth',block:'center'})">Next ▶</button>` : '<span></span>';
                html += `<div class="rw-group-row" id="trad-${cat.key}-${idx}">
                    <span class="rw-group-name">${g.name} (${idx + 1}/${groups.length})</span>
                    <span class="rw-group-stat">${gLearned}/${gChars.length}</span>
                    <button class="rw-study-btn" onclick="startReadingStudy('${cat.key}','${g.name}')">📖 Study</button>
                    <button class="rw-quiz-btn" onclick="startReadingQuiz('${cat.key}','${g.name}')">🧠 Quiz</button>
                    <div class="wr-nav-row" style="margin-top:8px">${prevBtn} ${nextBtn}</div>
                </div>`;
            });
        }
        html += `</div></details>`;
    });

    html += `</div></details>`;

    // === STEP 2: Word-First Practice ===
    html += `<h3 class="wr-section-header" style="margin-top:32px; font-size:18px; color:var(--accent)">📚 Step 2 — Word Practice Methods</h3>
        <p style="text-align:center; color:var(--text-dim); font-size:14px; margin-bottom:16px">Apply your character knowledge to real words!</p>`;

    // === Word-First Levels ===
    if (typeof WORD_FIRST_DATA !== "undefined") {
        // Auto-unlock first level of each script section
        [1, 17, 27].forEach(lv => {
            if (!wrProgress[lv]) wrProgress[lv] = { unlocked: true, bestSpeed: null, wordsLearned: 0, speedClears: 0 };
            else if (!wrProgress[lv].unlocked) wrProgress[lv].unlocked = true;
        });

        const sections = [
            { key: 'hiragana', label: 'ひらがな Hiragana', cls: 'wr-hiragana', startLvl: 1, endLvl: 16, stepHeaders: {1: '🔤 Step 1 — Learn Through Words', 10: '👁️ Step 2 — Visual Groups', 14: '📚 Step 3 — Mini Vocabulary'} },
            { key: 'katakana', label: 'カタカナ Katakana', cls: 'wr-katakana', startLvl: 17, endLvl: 26, stepHeaders: {17: '� Step 1 — Sound Conversion Method', 23: '👁️ Step 2 — Visual Confusion Pairs', 25: '💼 Step 3 — Workplace Sound Conversion'} },
            { key: 'kanji', label: '漢字 Kanji', cls: 'wr-kanji', startLvl: 27, endLvl: 34, stepHeaders: {27: '🧩 Step 1 — Radical + Meaning Method', 31: '🌿 Step 2 — Radical Decoding', 34: '🏢 Step 3 — Workplace Radicals'} },
        ];

        sections.forEach(sec => {
            const secLevels = WORD_FIRST_DATA.filter(l => l.level >= sec.startLvl && l.level <= sec.endLvl);
            const totalWords = secLevels.reduce((s, l) => s + l.words.length, 0);
            const learnedWords = secLevels.reduce((s, l) => { const p = getWRLevel(l.level); return s + Math.min(p.wordsLearned || 0, l.words.length); }, 0);
            const secPct = totalWords > 0 ? Math.round((learnedWords / totalWords) * 100) : 0;
            const isOpen = scrollToLevel >= sec.startLvl && scrollToLevel <= sec.endLvl ? true : openSections[sec.key] !== false;

            html += `<details class="rw-collapsible" ${isOpen ? 'open' : ''} data-section="${sec.key}">
                <summary class="wr-section-header wr-script-header ${sec.cls}">
                    <span class="wr-script-label">${sec.label}</span>
                    <span class="wr-script-pct">${secPct}%</span>
                    <span class="wr-collapse-icon"></span>
                </summary>
                <div class="rw-collapsible-body">`;

            secLevels.forEach(lvl => {
                const prog = getWRLevel(lvl.level);
                const isUnlocked = prog.unlocked;
                const wCount = lvl.words.length;
                const pct = wCount > 0 ? Math.round((Math.min(prog.wordsLearned, wCount) / wCount) * 100) : 0;
                const isComplete = pct >= 100;

                if (sec.stepHeaders[lvl.level]) html += `<h4 class="wr-step-header">${sec.stepHeaders[lvl.level]}</h4>`;

                const scriptClass = lvl.script === 'katakana' ? 'wr-card-katakana' : lvl.script === 'kanji' ? 'wr-card-kanji' : '';
                html += `<div class="rw-category-card ${scriptClass} ${!isUnlocked ? 'wr-locked-card' : ''} ${isComplete ? 'wr-complete-card' : ''}" id="wf-level-${lvl.level}">
                    <div class="rw-cat-header">
                        <span class="rw-cat-icon">${lvl.focus.length ? lvl.focus[0] : '📝'}</span>
                        <div class="rw-cat-info"><h3>${lvl.title}</h3><p>${lvl.subtitle}</p></div>
                        ${lvl.focus.length ? `<div class="wr-level-chars">${lvl.focus.join(' ')}</div>` : ''}
                        <div class="rw-cat-progress"><span class="rw-cat-pct">${pct}%</span></div>
                    </div>
                    <div class="rw-progress-bar"><div class="rw-progress-fill" style="width:${Math.min(pct, 100)}%"></div></div>
                    ${isUnlocked ? `<div class="rw-groups"><div class="rw-group-row">
                        <button class="rw-study-btn" onclick="startWFReadLearn(${lvl.level})">📖 Learn</button>
                        <button class="rw-quiz-btn" onclick="startWFReadQuiz(${lvl.level})">🧠 Quiz</button>
                        ${prog.bestSpeed ? `<span class="wr-best-time">🏆 ${(prog.bestSpeed / 1000).toFixed(1)}s</span>` : ''}
                    </div></div>` : `<div class="wr-level-locked">🔒 Complete previous level first</div>`}
                </div>`;
            });
            html += `</div></details>`;
        });

        // Speed challenge
        const totalLearned = Object.values(wrProgress).reduce((s, p) => s + (p.wordsLearned || 0), 0);
        if (totalLearned >= 6) {
            html += `<h3 class="wr-section-header">⚡ Speed Challenge</h3>
                <div class="rw-category-card">
                    <div class="rw-cat-header">
                        <span class="rw-cat-icon">⚡</span>
                        <div class="rw-cat-info"><h3>Speed Recognition</h3><p>Read ALL learned words instantly</p></div>
                    </div>
                    <div class="rw-groups"><div class="rw-group-row">
                        <button class="rw-quiz-btn" onclick="startWFReadChallenge()">🔥 ${totalLearned} words — GO!</button>
                    </div></div>
                </div>`;
        }
    }

    html += `</div>`;
    panel.innerHTML = html;

    // Attach collapsible toggle persistence
    panel.querySelectorAll('.rw-collapsible[data-section]').forEach(d => d.addEventListener('toggle', () => {
        const o = {}; panel.querySelectorAll('.rw-collapsible[data-section]').forEach(el => o[el.dataset.section] = el.open);
        localStorage.setItem('jcoach_rp_open', JSON.stringify(o));
    }));

    // Scroll to target level if specified
    if (scrollToLevel) {
        requestAnimationFrame(() => {
            const el = document.getElementById(`wf-level-${scrollToLevel}`);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
}

function getGroupItems(category, groupName) {
    if (category === "grammar") {
        return KANA_DATA.grammar.patterns.map(p => ({
            char: p.pattern, romaji: p.id, meaning: p.meaning,
            example: p.example, exampleEn: p.exampleEn
        }));
    }
    const catData = KANA_DATA[category];
    const group = catData.groups.find(g => g.name === groupName);
    if (!group) return [];
    return (group.chars || group.words || []).map(item => ({
        char: item.char || item.word,
        romaji: item.romaji,
        meaning: item.meaning || "",
        hint: item.hint || "",
        onyomi: item.onyomi || "",
        kunyomi: item.kunyomi || "",
    }));
}

function getNextGroup(category, currentGroupName) {
    if (category === "grammar") return null;
    const catData = KANA_DATA[category];
    if (!catData || !catData.groups) return null;
    const groups = catData.groups;
    const currentIdx = groups.findIndex(g => g.name === currentGroupName);
    if (currentIdx === -1 || currentIdx >= groups.length - 1) return null;
    return groups[currentIdx + 1].name;
}

function getPrevGroup(category, currentGroupName) {
    if (category === "grammar") return null;
    const catData = KANA_DATA[category];
    if (!catData || !catData.groups) return null;
    const groups = catData.groups;
    const currentIdx = groups.findIndex(g => g.name === currentGroupName);
    if (currentIdx <= 0) return null;
    return groups[currentIdx - 1].name;
}

function startReadingStudy(category, groupName) {
    const items = getGroupItems(category, groupName);
    if (!items.length) return;
    const panel = document.getElementById("readingPanel");
    let idx = 0;
    let cardPhase = "front"; // front → mnemonic → back

    function getMnemonic(char) {
        return (typeof MNEMONICS !== "undefined" && MNEMONICS[char]) || null;
    }

    function renderCard() {
        const item = items[idx];
        const mastery = getReadingMastery(item.char);
        const isKanji = category === "kanji";
        const isGrammar = category === "grammar";
        const mn = getMnemonic(item.char);
        cardPhase = "front";

        panel.innerHTML = `<div class="rw-content">
            <div class="rw-study-header">
                <button class="rw-back-btn" onclick="renderReadingPanel()">← Back</button>
                <span>${idx + 1} / ${items.length}</span>
                <span>${groupName}</span>
            </div>
            <div class="rw-flashcard" id="studyCard">
                <div class="rw-card-front" id="cardFront">
                    <span class="rw-big-char">${item.char}</span>
                    <span class="rw-tap-hint">tap to see memory aid →</span>
                </div>
                <div class="rw-card-mnemonic" id="cardMnemonic" style="display:none">
                    ${mn ? `
                        <div class="mn-visual">${mn.visual}</div>
                        <div class="mn-char">${item.char} = ${item.romaji}</div>
                        <div class="mn-story">${mn.story}</div>
                        ${isKanji && item.meaning ? `<div class="mn-meaning">"${item.meaning}"</div>` : ""}
                    ` : `
                        <div class="mn-char">${item.char} = ${item.romaji}</div>
                        ${item.meaning ? `<div class="mn-meaning">"${item.meaning}"</div>` : ""}
                        ${item.hint ? `<div class="mn-story">${item.hint}</div>` : ""}
                    `}
                    <div class="mn-note-container">
                        <label class="mn-note-label">✏️ My memory trick:</label>
                        <textarea class="mn-note-area" id="mnNoteInput" placeholder="Write your own way to remember this...">${(userNotes[item.char] || "").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</textarea>
                        <span class="mn-note-saved" id="mnNoteSaved"></span>
                    </div>
                    <span class="rw-tap-hint">tap for full details →</span>
                </div>
                <div class="rw-card-back" id="cardBack" style="display:none">
                    <span class="rw-romaji">${item.romaji}</span>
                    ${item.meaning ? `<span class="rw-meaning">${item.meaning}</span>` : ""}
                    ${mn ? `<div class="mn-story-small">💡 ${mn.story}</div>` : ""}
                    <div class="mn-user-note" id="cardBackNote"${userNotes[item.char] ? "" : " style='display:none'"}>${userNotes[item.char] ? `✏️ &quot;${(userNotes[item.char]).replace(/</g, "&lt;").replace(/>/g, "&gt;")}&quot;` : ""}</div>
                    ${item.hint ? `<span class="rw-hint">${item.hint}</span>` : ""}
                    ${isKanji ? `<span class="rw-readings">ON: ${item.onyomi || "—"} | KUN: ${item.kunyomi || "—"}</span>` : ""}
                    ${isGrammar && item.example ? `<div class="rw-example">${item.example}<br><span style="color:var(--text-dim)">${item.exampleEn || ""}</span></div>` : ""}
                    <span class="rw-mastery ${mastery.mastered ? 'done' : ''}">${mastery.mastered ? '✅ Mastered' : `${mastery.correct}/3 correct`}</span>
                </div>
            </div>
            <div class="rw-nav-row">
                <button class="rw-nav-btn" onclick="void(0)" id="rw-prev" ${idx === 0 ? 'disabled' : ''}>◀ Prev</button>
                <button class="rw-speak-btn" onclick="speakJapanese('${item.char.replace(/'/g, "\\'")}')">🔊</button>
                <button class="rw-nav-btn" onclick="void(0)" id="rw-next">${idx === items.length - 1 ? 'Done ✓' : 'Next ▶'}</button>
            </div>
        </div>`;

        // Note save listener
        const noteInput = document.getElementById("mnNoteInput");
        if (noteInput) {
            let _noteTimer = null;
            noteInput.addEventListener("input", () => {
                userNotes[item.char] = noteInput.value;
                saveProgress();
                const savedEl = document.getElementById("mnNoteSaved");
                if (savedEl) {
                    savedEl.textContent = "✓ Saved";
                    savedEl.classList.add("visible");
                    clearTimeout(_noteTimer);
                    _noteTimer = setTimeout(() => savedEl.classList.remove("visible"), 1500);
                }
            });
        }

        // Three-phase card flip: front → mnemonic → back
        document.getElementById("studyCard").onclick = (e) => {
            if (e.target.closest(".mn-note-container")) return; // don't flip while editing note
            if (cardPhase === "front") {
                document.getElementById("cardFront").style.display = "none";
                document.getElementById("cardMnemonic").style.display = "flex";
                cardPhase = "mnemonic";
            } else if (cardPhase === "mnemonic") {
                // Sync latest note to back phase before showing it
                const note = userNotes[item.char];
                const noteEl = document.getElementById("cardBackNote");
                if (noteEl) {
                    if (note) {
                        noteEl.innerHTML = `✏️ &quot;${note.replace(/</g, "&lt;").replace(/>/g, "&gt;")}&quot;`;
                        noteEl.style.display = "";
                    } else {
                        noteEl.style.display = "none";
                    }
                }
                document.getElementById("cardMnemonic").style.display = "none";
                document.getElementById("cardBack").style.display = "flex";
                cardPhase = "back";
            } else {
                document.getElementById("cardBack").style.display = "none";
                document.getElementById("cardFront").style.display = "flex";
                cardPhase = "front";
            }
        };
        document.getElementById("rw-prev").onclick = () => { if (idx > 0) { idx--; renderCard(); } };
        document.getElementById("rw-next").onclick = () => {
            if (idx < items.length - 1) { idx++; renderCard(); }
            else {
                // Study complete - show completion screen with navigation
                const prevGrp = getPrevGroup(category, groupName);
                const nextGrp = getNextGroup(category, groupName);
                panel.innerHTML = `<div class="rw-content">
                    <div class="rw-quiz-result">
                        <h3>✅ Study Complete!</h3>
                        <div class="rw-score">You studied ${items.length} characters</div>
                        <div class="rw-quiz-actions">
                            <button class="btn-primary" style="max-width:200px" onclick="startReadingQuiz('${category}','${groupName}')">📝 Take Quiz</button>
                            ${prevGrp ? `<button class="rw-nav-btn" onclick="startReadingStudy('${category}','${prevGrp}')" style="margin-top:8px">◀ Prev Group</button>` : ''}
                            ${nextGrp ? `<button class="rw-nav-btn" onclick="startReadingStudy('${category}','${nextGrp}')" style="margin-top:8px">Next Group ▶</button>` : ''}
                            <button class="rw-back-btn" onclick="renderReadingPanel()" style="margin-top:8px">← Back to Reading</button>
                        </div>
                    </div>
                </div>`;
            }
        };
    }
    renderCard();
}

function startReadingQuiz(category, groupName) {
    const items = getGroupItems(category, groupName);
    if (items.length < 2) return;
    // Shuffle and take up to 10
    const shuffled = [...items].sort(() => Math.random() - 0.5).slice(0, 10);
    readingQuiz = { items: shuffled, current: 0, correct: 0, category, group: groupName, allItems: items };
    renderReadingQuestion();
}

function renderReadingQuestion() {
    const panel = document.getElementById("readingPanel");
    const q = readingQuiz;
    if (q.current >= q.items.length) {
        // Quiz complete
        const pct = Math.round((q.correct / q.items.length) * 100);
        xp += q.correct * 5;
        saveProgress();
        const nextGrp = getNextGroup(q.category, q.group);
        const prevGrp = getPrevGroup(q.category, q.group);
        panel.innerHTML = `<div class="rw-content">
            <div class="rw-quiz-result">
                <h3>${pct >= 80 ? '🎉 Excellent!' : pct >= 60 ? '👍 Good job!' : '💪 Keep practicing!'}</h3>
                <div class="rw-score">${q.correct}/${q.items.length} correct (${pct}%)</div>
                <div class="rw-quiz-actions">
                    <button class="btn-primary" style="max-width:200px" onclick="startReadingQuiz('${q.category}','${q.group}')">🔄 Try Again</button>
                    ${nextGrp ? `<button class="btn-primary" style="max-width:200px; margin-top:8px" onclick="startReadingStudy('${q.category}','${nextGrp}')">📖 Next Group ▶</button>` : ''}
                    ${prevGrp ? `<button class="rw-nav-btn" onclick="startReadingStudy('${q.category}','${prevGrp}')" style="margin-top:8px">◀ Prev Group</button>` : ''}
                    <button class="rw-back-btn" onclick="renderReadingPanel()" style="margin-top:8px">← Back to Reading</button>
                </div>
            </div>
        </div>`;
        return;
    }

    const item = q.items[q.current];
    const isKanji = q.category === "kanji";
    const isGrammar = q.category === "grammar";
    const isWords = q.category === "dailyWords";

    // Generate wrong options from same category
    const others = q.allItems.filter(i => i.char !== item.char);
    const wrongPool = others.sort(() => Math.random() - 0.5).slice(0, 3);
    let options;

    if (isKanji || isGrammar || isWords) {
        // Show char, pick meaning
        options = [{ text: item.meaning || item.romaji, correct: true }];
        wrongPool.forEach(w => options.push({ text: w.meaning || w.romaji, correct: false }));
    } else {
        // Show char, pick romaji
        options = [{ text: item.romaji, correct: true }];
        wrongPool.forEach(w => options.push({ text: w.romaji, correct: false }));
    }
    options.sort(() => Math.random() - 0.5);

    panel.innerHTML = `<div class="rw-content">
        <div class="rw-study-header">
            <button class="rw-back-btn" onclick="renderReadingPanel()">← Back</button>
            <span>Q${q.current + 1} / ${q.items.length}</span>
            <span>✓ ${q.correct}</span>
        </div>
        <div class="rw-quiz-card">
            <span class="rw-quiz-prompt">${item.char}</span>
            ${isKanji || isGrammar ? `<span class="rw-quiz-sub">${isKanji ? 'What does this kanji mean?' : 'What does this pattern mean?'}</span>` : ''}
            ${isWords ? `<span class="rw-quiz-sub">What does this word mean?</span>` : ''}
            <div class="rw-quiz-options" id="rw-options">
                ${options.map((o, i) => `
                    <button class="rw-quiz-option" data-correct="${o.correct}" onclick="handleReadingAnswer(this, ${o.correct}, '${item.char.replace(/'/g, "\\'")}')">
                        ${o.text}
                    </button>
                `).join("")}
            </div>
        </div>
    </div>`;
}

function handleReadingAnswer(btn, isCorrect, char) {
    // Disable all buttons
    document.querySelectorAll(".rw-quiz-option").forEach(b => {
        b.disabled = true;
        if (b.dataset.correct === "true") b.classList.add("correct-answer");
        if (b === btn && !isCorrect) b.classList.add("wrong-answer");
    });
    if (isCorrect) readingQuiz.correct++;
    markReadingResult(char, isCorrect);

    // Show mnemonic hint after answering (especially on wrong answers)
    const mn = (typeof MNEMONICS !== "undefined" && MNEMONICS[char]) || null;
    const personalNote = userNotes[char] || "";
    if (!isCorrect && (mn || personalNote)) {
        const hintEl = document.createElement("div");
        hintEl.className = "mn-quiz-hint";
        let hintHtml = "";
        if (mn) hintHtml += `<span class="mn-quiz-visual">${mn.visual}</span> <span class="mn-quiz-story">${mn.story}</span>`;
        if (personalNote) hintHtml += `<div class="mn-personal-note">✏️ &quot;${personalNote.replace(/</g, "&lt;").replace(/>/g, "&gt;")}&quot;</div>`;
        hintEl.innerHTML = hintHtml;
        document.querySelector(".rw-quiz-card")?.appendChild(hintEl);
    }

    setTimeout(() => {
        readingQuiz.current++;
        renderReadingQuestion();
    }, !isCorrect && (mn || personalNote) ? 2500 : 1200);
}

// ============================================
// WORD-FIRST READING LEARN / QUIZ / CHALLENGE
// Merged into reading panel from Word Recognition
// ============================================

function startWFReadLearn(level) {
    const lvlData = WORD_FIRST_DATA.find(l => l.level === level);
    if (!lvlData) return;
    const panel = document.getElementById("readingPanel");
    const words = lvlData.words;
    let idx = 0;
    let phase = "word";

    function buildHiraganaDetail(w) {
        const mn = typeof MNEMONICS !== "undefined" ? MNEMONICS : {};
        const chars = [...w.word];
        const breakdownHTML = chars.map(c => {
            const m = mn[c] || null;
            let charRomaji = "";
            let charMeaning = "";
            ["hiragana", "katakana"].forEach(type => {
                if (typeof KANA_DATA !== "undefined") {
                    KANA_DATA[type].groups.forEach(g => {
                        (g.chars || []).forEach(ch => { if (ch.char === c) charRomaji = ch.romaji; });
                    });
                }
            });
            if (!charRomaji && typeof KANA_DATA !== "undefined" && KANA_DATA.kanji) {
                KANA_DATA.kanji.groups.forEach(g => {
                    (g.chars || []).forEach(ch => {
                        if (ch.char === c) { charRomaji = ch.romaji; charMeaning = ch.meaning || ""; }
                    });
                });
            }
            return `<div class="wr-char-cell">
                <span class="wr-char-big">${c}</span>
                <span class="wr-char-romaji">${charRomaji}</span>
                ${charMeaning ? `<span class="wr-char-meaning">${charMeaning}</span>` : ''}
                ${m ? `<span class="wr-char-mnemonic">${m.visual}</span>` : ''}
            </div>`;
        }).join('');
        const tipHTML = w.tip ? `<div class="wr-tip">${w.tip}</div>` : '';
        return `<span class="wr-detail-word">${w.word}</span>
            <span class="wr-detail-romaji">${w.romaji}</span>
            <span class="wr-detail-meaning">${w.emoji} ${w.meaning}</span>
            <div class="wr-breakdown">${breakdownHTML}</div>
            ${tipHTML}`;
    }

    function buildKatakanaDetail(w) {
        const steps = w.soundSteps || [];
        const stepsHTML = steps.length >= 2
            ? `<div class="wr-sound-steps">
                <div class="wr-sound-step wr-sound-en"><span class="wr-sound-label">English</span><span class="wr-sound-val">${w.english || ''}</span></div>
                <div class="wr-sound-arrow">▼</div>
                <div class="wr-sound-step wr-sound-convert"><span class="wr-sound-label">Sound</span><span class="wr-sound-val">${steps[0]}</span></div>
                <div class="wr-sound-arrow">▼</div>
                <div class="wr-sound-step wr-sound-kata"><span class="wr-sound-label">カタカナ</span><span class="wr-sound-val">${steps[1]}</span></div>
              </div>` : '';
        const ruleHTML = w.rule ? `<div class="wr-sound-rule">📏 <strong>Rule:</strong> ${w.rule}</div>` : '';
        const tipHTML = w.tip ? `<div class="wr-tip">${w.tip}</div>` : '';
        return `<span class="wr-detail-word">${w.word}</span>
            <span class="wr-detail-romaji">${w.romaji}</span>
            <span class="wr-detail-meaning">${w.emoji} ${w.meaning}</span>
            ${stepsHTML}
            ${ruleHTML}
            ${tipHTML}`;
    }

    function buildKanjiDetail(w) {
        const rads = w.radicals || [];
        const radHTML = rads.map(r => {
            const partsHTML = (r.parts || []).map(p => `<span class="wr-radical-part">${p}</span>`).join('');
            const logicHTML = r.logic ? `<div class="wr-radical-logic">→ ${r.logic}</div>` : '';
            return `<div class="wr-radical-card">
                <span class="wr-radical-char">${r.char}</span>
                <span class="wr-radical-meaning">${r.meaning || ''}</span>
                <div class="wr-radical-parts">${partsHTML}</div>
                ${logicHTML}
            </div>`;
        }).join('');
        const tipHTML = w.tip ? `<div class="wr-tip">${w.tip}</div>` : '';
        return `<span class="wr-detail-word">${w.word}</span>
            <span class="wr-detail-romaji">${w.romaji}</span>
            <span class="wr-detail-meaning">${w.emoji} ${w.meaning}</span>
            <div class="wr-radicals">${radHTML}</div>
            ${tipHTML}`;
    }

    function renderLearnCard() {
        const w = words[idx];
        phase = "word";
        const script = lvlData.script;
        let frontHint = "tap to reveal ↓";
        let detailHTML = "";
        if (script === "katakana") {
            frontHint = "How does this sound in Japanese? ↓";
            detailHTML = buildKatakanaDetail(w);
        } else if (script === "kanji") {
            frontHint = "What do the parts mean? ↓";
            detailHTML = buildKanjiDetail(w);
        } else {
            detailHTML = buildHiraganaDetail(w);
        }
        const frontWord = (script === "katakana" && w.english) ? w.english : w.word;
        const frontLabel = script === "katakana" ? `<span class="wr-word-sub">${w.word}</span>` : '';

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="unlockNextWR(${level});renderReadingPanel(${level})">← Back</button>
                <span>${idx + 1} / ${words.length}</span>
                <span>${lvlData.title}</span>
            </div>
            <div class="wr-card ${script ? 'wr-card-' + script : ''}" id="wrCard">
                <div class="wr-card-word" id="wrWordFace">
                    <span class="wr-word-emoji">${w.emoji}</span>
                    <span class="wr-word-big">${frontWord}</span>
                    ${frontLabel}
                    <span class="wr-word-hint">${frontHint}</span>
                </div>
                <div class="wr-card-detail" id="wrDetailFace" style="display:none">
                    ${detailHTML}
                </div>
            </div>
            <div class="wr-nav-row">
                <button class="rw-speak-btn" onclick="speakJapanese('${w.word.replace(/'/g, "\\'")}')">🔊</button>
                ${idx > 0 ? `<button class="wr-nav-btn" onclick="wfReadPrev()">◀ Prev</button>` : '<span></span>'}
                <button class="wr-nav-btn wr-nav-next" onclick="wfReadNext()">${idx < words.length - 1 ? 'Next ▶' : '✅ Done'}</button>
            </div>
        </div>`;

        document.getElementById("wrCard").onclick = (e) => {
            if (e.target.closest(".wr-nav-row") || e.target.closest("button")) return;
            if (phase === "word") {
                document.getElementById("wrWordFace").style.display = "none";
                document.getElementById("wrDetailFace").style.display = "flex";
                phase = "detail";
            }
        };
    }

    window.wfReadPrev = function() { if (idx > 0) { idx--; renderLearnCard(); } };
    window.wfReadNext = function() {
        const prog = getWRLevel(level);
        prog.wordsLearned = Math.max(prog.wordsLearned, idx + 1);
        prog.unlocked = true;
        setWRLevel(level, prog);
        const w = words[idx];
        trackWord(w.word, w.romaji, w.meaning);
        [...w.word].forEach(c => { markReadingResult(c, true); });
        idx++;
        if (idx < words.length) { renderLearnCard(); }
        else {
            unlockNextWR(level);
            xp += 15;
            saveProgress();
            const nextLvl = WORD_FIRST_DATA.find(l => l.level === level + 1);
            const hasNext = nextLvl && getWRLevel(level + 1).unlocked;
            panel.innerHTML = `<div class="wr-content">
                <div class="wr-complete">
                    <h3>🎉 Level ${level} Complete!</h3>
                    <p>You learned ${words.length} words. Try the <strong>🧠 Quiz</strong> or continue to the next level!</p>
                    <div class="wr-complete-actions">
                        <button class="wr-speed-btn" onclick="startWFReadQuiz(${level})">🧠 Quiz</button>
                        ${hasNext ? `<button class="btn-primary" onclick="startWFReadLearn(${level + 1})">▶ Next Level</button>` : ''}
                        <button class="rw-back-btn" onclick="renderReadingPanel(${level})">← Back to Reading</button>
                    </div>
                </div>
            </div>`;
        }
    };
    renderLearnCard();
}

function startWFReadQuiz(level) {
    const lvlData = WORD_FIRST_DATA.find(l => l.level === level);
    if (!lvlData) return;
    const panel = document.getElementById("readingPanel");
    const words = [...lvlData.words].sort(() => Math.random() - 0.5);
    let idx = 0, correct = 0, startTime = Date.now();

    function renderQuizCard() {
        if (idx >= words.length) {
            const elapsed = Date.now() - startTime;
            const pct = Math.round((correct / words.length) * 100);
            const avgMs = Math.round(elapsed / words.length);
            const prog = getWRLevel(level);
            if (pct >= 80 && (!prog.bestSpeed || elapsed < prog.bestSpeed)) prog.bestSpeed = elapsed;
            prog.speedClears = (prog.speedClears || 0) + 1;
            setWRLevel(level, prog);
            xp += correct * 3; saveProgress();
            panel.innerHTML = `<div class="wr-content"><div class="wr-complete">
                <h3>${pct >= 90 ? '🔥 Lightning Fast!' : pct >= 70 ? '⚡ Great Speed!' : '💪 Keep Practicing!'}</h3>
                <div class="wr-speed-stats">
                    <div class="wr-stat"><span class="wr-stat-num">${correct}/${words.length}</span><span>correct</span></div>
                    <div class="wr-stat"><span class="wr-stat-num">${(elapsed / 1000).toFixed(1)}s</span><span>total time</span></div>
                    <div class="wr-stat"><span class="wr-stat-num">${avgMs}ms</span><span>per word</span></div>
                </div>
                ${pct < 80 ? `<p class="wr-speed-tip">💡 Goal: Read each word <strong>instantly</strong> — not い…ぬ…maybe… but いぬ = dog! 🐕</p>` : ''}
                <div class="wr-complete-actions">
                    <button class="wr-speed-btn" onclick="startWFReadQuiz(${level})">🔄 Try Again</button>
                    ${WORD_FIRST_DATA.find(l => l.level === level + 1) && getWRLevel(level + 1).unlocked ? `<button class="btn-primary" onclick="startWFReadLearn(${level + 1})">▶ Next Level</button>` : ''}
                    <button class="rw-back-btn" onclick="renderReadingPanel(${level})">← Back</button>
                </div>
            </div></div>`;
            return;
        }
        const w = words[idx];
        let wrongPool = [];
        WORD_FIRST_DATA.forEach(l => {
            if (Math.abs(l.level - level) <= 2) l.words.forEach(ww => { if (ww.word !== w.word) wrongPool.push(ww); });
        });
        wrongPool = wrongPool.sort(() => Math.random() - 0.5).slice(0, 3);
        let options = [{ text: `${w.emoji} ${w.meaning}`, correct: true }];
        wrongPool.forEach(ww => options.push({ text: `${ww.emoji} ${ww.meaning}`, correct: false }));
        options = options.sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="renderReadingPanel(${level})">← Back</button>
                <span>${idx + 1}/${words.length}</span>
                <span class="wr-timer" id="wrTimer">0.0s</span>
            </div>
            <div class="wr-speed-card">
                <span class="wr-speed-word">${w.word}</span>
                <div class="wr-speed-options" id="wrReadOpts">
                    ${options.map(o => `<button class="wr-speed-option" data-correct="${o.correct}"
                        onclick="wfReadQuizAnswer(this, ${o.correct})">${o.text}</button>`).join('')}
                </div>
            </div>
        </div>`;
        const timerEl = document.getElementById("wrTimer");
        const ti = setInterval(() => {
            if (timerEl && document.contains(timerEl)) timerEl.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
            else clearInterval(ti);
        }, 100);
    }

    window.wfReadQuizAnswer = function(btn, isCorrect) {
        document.querySelectorAll("#wrReadOpts .wr-speed-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !isCorrect) b.classList.add("wrong-answer");
        });
        if (isCorrect) correct++;
        const w = words[idx];
        [...w.word].forEach(c => { markReadingResult(c, isCorrect); });
        setTimeout(() => { idx++; renderQuizCard(); }, isCorrect ? 400 : 1200);
    };
    renderQuizCard();
}

function startWFReadChallenge() {
    const panel = document.getElementById("readingPanel");
    let allWords = [];
    WORD_FIRST_DATA.forEach(lvl => {
        const prog = getWRLevel(lvl.level);
        if (prog.unlocked && prog.wordsLearned > 0) lvl.words.slice(0, prog.wordsLearned).forEach(w => allWords.push(w));
    });
    if (allWords.length < 4) { renderReadingPanel(); return; }
    allWords = allWords.sort(() => Math.random() - 0.5).slice(0, 20);
    let idx = 0, correct = 0, startTime = Date.now();

    function renderCCard() {
        if (idx >= allWords.length) {
            const elapsed = Date.now() - startTime;
            const pct = Math.round((correct / allWords.length) * 100);
            const avgMs = Math.round(elapsed / allWords.length);
            xp += correct * 5; saveProgress();
            panel.innerHTML = `<div class="wr-content"><div class="wr-complete">
                <h3>${pct >= 95 ? '🏆 PERFECT!' : pct >= 80 ? '🔥 Impressive!' : pct >= 60 ? '⚡ Good!' : '💪 Keep Going!'}</h3>
                <div class="wr-speed-stats">
                    <div class="wr-stat"><span class="wr-stat-num">${correct}/${allWords.length}</span><span>correct</span></div>
                    <div class="wr-stat"><span class="wr-stat-num">${(elapsed / 1000).toFixed(1)}s</span><span>total</span></div>
                    <div class="wr-stat"><span class="wr-stat-num">${avgMs}ms</span><span>avg/word</span></div>
                </div>
                <div class="wr-complete-actions">
                    <button class="wr-speed-btn" onclick="startWFReadChallenge()">🔄 Again</button>
                    <button class="rw-back-btn" onclick="renderReadingPanel()">← Back</button>
                </div>
            </div></div>`;
            return;
        }
        const w = allWords[idx];
        let wrongPool = allWords.filter(ww => ww.word !== w.word).sort(() => Math.random() - 0.5).slice(0, 3);
        if (wrongPool.length < 3) {
            WORD_FIRST_DATA.forEach(l => { l.words.forEach(ww => { if (ww.word !== w.word && wrongPool.length < 3) wrongPool.push(ww); }); });
        }
        let options = [{ text: `${w.emoji} ${w.meaning}`, correct: true }];
        wrongPool.slice(0, 3).forEach(ww => options.push({ text: `${ww.emoji} ${ww.meaning}`, correct: false }));
        options = options.sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="renderReadingPanel()">← Back</button>
                <span>${idx + 1}/${allWords.length}</span>
                <span class="wr-timer" id="wrTimer">0.0s</span>
            </div>
            <div class="wr-speed-card wr-challenge-card">
                <span class="wr-speed-word">${w.word}</span>
                <div class="wr-speed-options" id="wrChalOpts">
                    ${options.map(o => `<button class="wr-speed-option" data-correct="${o.correct}"
                        onclick="wfReadChalAnswer(this, ${o.correct})">${o.text}</button>`).join('')}
                </div>
            </div>
        </div>`;
        const timerEl = document.getElementById("wrTimer");
        const ti = setInterval(() => {
            if (timerEl && document.contains(timerEl)) timerEl.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
            else clearInterval(ti);
        }, 100);
    }

    window.wfReadChalAnswer = function(btn, isCorrect) {
        document.querySelectorAll("#wrChalOpts .wr-speed-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !isCorrect) b.classList.add("wrong-answer");
        });
        if (isCorrect) correct++;
        setTimeout(() => { idx++; renderCCard(); }, isCorrect ? 400 : 1200);
    };
    renderCCard();
}

// ============================================
// JAPANESE ON-SCREEN KEYBOARD + WRITING MODE
// Gojuuon layout — tap hiragana/katakana to write
// Word-first approach with keyboard input
// ============================================

const JP_KB_HIRAGANA = [
    ["あ","い","う","え","お","か","き","く","け","こ"],
    ["さ","し","す","せ","そ","た","ち","つ","て","と"],
    ["な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ"],
    ["ま","み","む","め","も","や","ゆ","よ","わ","ん"],
    ["ら","り","る","れ","ろ","を","っ","ー","゛","゜"],
];
const JP_KB_KATA = [
    ["ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ"],
    ["サ","シ","ス","セ","ソ","タ","チ","ツ","テ","ト"],
    ["ナ","ニ","ヌ","ネ","ノ","ハ","ヒ","フ","ヘ","ホ"],
    ["マ","ミ","ム","メ","モ","ヤ","ユ","ヨ","ワ","ン"],
    ["ラ","リ","ル","レ","ロ","ヲ","ッ","ー","゛","゜"],
];
const DAKUTEN_MAP = {
    "か":"が","き":"ぎ","く":"ぐ","け":"げ","こ":"ご",
    "さ":"ざ","し":"じ","す":"ず","せ":"ぜ","そ":"ぞ",
    "た":"だ","ち":"ぢ","つ":"づ","て":"で","と":"ど",
    "は":"ば","ひ":"び","ふ":"ぶ","へ":"べ","ほ":"ぼ",
    "カ":"ガ","キ":"ギ","ク":"グ","ケ":"ゲ","コ":"ゴ",
    "サ":"ザ","シ":"ジ","ス":"ズ","セ":"ゼ","ソ":"ゾ",
    "タ":"ダ","チ":"ヂ","ツ":"ヅ","テ":"デ","ト":"ド",
    "ハ":"バ","ヒ":"ビ","フ":"ブ","ヘ":"ベ","ホ":"ボ",
};
const HANDAKUTEN_MAP = {
    "は":"ぱ","ひ":"ぴ","ふ":"ぷ","へ":"ぺ","ほ":"ぽ",
    "ハ":"パ","ヒ":"ピ","フ":"プ","ヘ":"ペ","ホ":"ポ",
};

let kbInput = [];
let kbExpected = "";
let kbType = "hiragana";
let kbSize = localStorage.getItem("jcoach_kb_size") || "medium";
let kbOnComplete = null;
let kbOnSkip = null;

function kbSetSize(size) {
    kbSize = size;
    localStorage.setItem("jcoach_kb_size", size);
    const el = document.getElementById("jpKeyboard");
    if (el) el.innerHTML = getKBRowsHTML();
}

function getKBRowsHTML() {
    const rows = kbType === "katakana" ? JP_KB_KATA : JP_KB_HIRAGANA;
    const sizeClass = `jpkb-${kbSize}`;
    return `<div class="jpkb-size-selector">
        <button class="jpkb-size-btn ${kbSize === 'small' ? 'active' : ''}" onclick="kbSetSize('small')">S</button>
        <button class="jpkb-size-btn ${kbSize === 'medium' ? 'active' : ''}" onclick="kbSetSize('medium')">M</button>
        <button class="jpkb-size-btn ${kbSize === 'large' ? 'active' : ''}" onclick="kbSetSize('large')">L</button>
    </div>
    <div class="jpkb-keys ${sizeClass}">${rows.map(row => `<div class="jpkb-row">${row.map(k =>
        `<button class="jpkb-key${k === '゛' || k === '゜' ? ' jpkb-mod' : ''}" data-char="${k}" onclick="kbPress('${k}')">${k}</button>`
    ).join('')}</div>`).join('')}
    <div class="jpkb-row jpkb-bottom">
        <button class="jpkb-key jpkb-fn" onclick="kbPress('⌫')">⌫</button>
        <button class="jpkb-key jpkb-fn" onclick="kbSwitchType()">${kbType === 'hiragana' ? 'カナ' : 'かな'}</button>
    </div></div>`;
}

function kbSwitchType() {
    kbType = kbType === "hiragana" ? "katakana" : "hiragana";
    const el = document.getElementById("jpKeyboard");
    if (el) el.innerHTML = getKBRowsHTML();
}

function kbPress(key) {
    const expectedChars = [...kbExpected];
    if (key === '⌫') { kbInput.pop(); kbUpdateDisplay(); return; }
    if (key === '゛' || key === '゜') {
        if (kbInput.length === 0) return;
        const last = kbInput[kbInput.length - 1];
        const map = key === '゛' ? DAKUTEN_MAP : HANDAKUTEN_MAP;
        if (map[last]) {
            kbInput[kbInput.length - 1] = map[last];
            kbUpdateDisplay();
            if (kbInput.length === expectedChars.length && kbInput.join('') === kbExpected) {
                if (kbOnComplete) kbOnComplete(true);
            }
        }
        return;
    }
    const pos = kbInput.length;
    if (pos >= expectedChars.length) return;
    const expected = expectedChars[pos];
    // Direct match
    if (key === expected) {
        kbInput.push(key);
        kbUpdateDisplay();
        if (kbInput.length === expectedChars.length) { if (kbOnComplete) kbOnComplete(true); }
        return;
    }
    // Base char for dakuten/handakuten — accept tentatively
    if (DAKUTEN_MAP[key] === expected || HANDAKUTEN_MAP[key] === expected) {
        kbInput.push(key);
        kbUpdateDisplay();
        return;
    }
    // Wrong — flash the key
    kbFlashWrong(key);
}

function kbUpdateDisplay() {
    const el = document.getElementById("kbDisplay");
    if (!el) return;
    const expectedChars = [...kbExpected];
    let html = '';
    expectedChars.forEach((c, i) => {
        if (i < kbInput.length) {
            const typed = kbInput[i];
            if (typed === c) html += `<span class="kbd-c kbd-ok">${typed}</span>`;
            else if (DAKUTEN_MAP[typed] === c || HANDAKUTEN_MAP[typed] === c)
                html += `<span class="kbd-c kbd-pending">${typed}<small>+゛</small></span>`;
            else html += `<span class="kbd-c kbd-err">${typed}</span>`;
        } else if (i === kbInput.length) {
            html += `<span class="kbd-c kbd-cursor">_</span>`;
        } else {
            html += `<span class="kbd-c kbd-empty">_</span>`;
        }
    });
    el.innerHTML = html;
}

function kbFlashWrong(key) {
    const el = document.getElementById("jpKeyboard");
    if (!el) return;
    const btn = el.querySelector(`[data-char="${key}"]`);
    if (btn) { btn.classList.add('jpkb-flash'); setTimeout(() => btn.classList.remove('jpkb-flash'), 400); }
    // Also shake display
    const disp = document.getElementById("kbDisplay");
    if (disp) { disp.classList.add('kbd-shake'); setTimeout(() => disp.classList.remove('kbd-shake'), 400); }
}

// --- Writing practice state ---
let writingQuiz = { items: [], current: 0, correct: 0, category: "", group: "" };

function getWritingMastery(char) {
    return writingProgress[char] || { correct: 0, seen: 0, mastered: false };
}

function markWritingResult(char, isCorrect) {
    if (!writingProgress[char]) writingProgress[char] = { correct: 0, seen: 0, mastered: false };
    writingProgress[char].seen++;
    if (isCorrect) { writingProgress[char].correct++; xp += 4; }
    if (writingProgress[char].correct >= 3) writingProgress[char].mastered = true;
    saveProgress();
}

function renderWritingPanel() {
    const panel = document.getElementById("writingPanel");
    if (!panel || typeof KANA_DATA === "undefined") { panel.innerHTML = "<p>Loading data...</p>"; return; }

    let html = `<div class="rw-content"><h2 class="rw-title">✍️ Writing Practice</h2>
        <p class="rw-subtitle">See romaji → tap the correct hiragana on the keyboard. Word-first approach!</p>`;

    // Word-First levels
    if (typeof WORD_FIRST_DATA !== "undefined") {
        html += `<h3 class="wr-section-header">🔤 Word-First Writing</h3>`;
        WORD_FIRST_DATA.forEach(lvl => {
            const prog = getWRLevel(lvl.level);
            const isUnlocked = prog.unlocked;
            const wCount = lvl.words.length;
            let wLearned = 0;
            lvl.words.forEach(w => { if (writingProgress[w.word] && writingProgress[w.word].correct > 0) wLearned++; });
            const pct = wCount > 0 ? Math.round((wLearned / wCount) * 100) : 0;

            if (lvl.level === 10) html += `<h3 class="wr-section-header">👁️ Visual Groups Writing</h3>`;
            if (lvl.level === 14) html += `<h3 class="wr-section-header">📚 Vocabulary Writing</h3>`;

            html += `<div class="rw-category-card ${!isUnlocked ? 'wr-locked-card' : ''}">
                <div class="rw-cat-header">
                    <span class="rw-cat-icon">${lvl.focus.length ? lvl.focus[0] : '📝'}</span>
                    <div class="rw-cat-info"><h3>${lvl.title}</h3><p>${lvl.subtitle}</p></div>
                    <div class="rw-cat-progress"><span class="rw-cat-pct">${pct}%</span><span class="rw-cat-count">${wLearned}/${wCount}</span></div>
                </div>
                <div class="rw-progress-bar"><div class="rw-progress-fill" style="width:${pct}%"></div></div>
                ${isUnlocked ? `<div class="rw-groups"><div class="rw-group-row">
                    <button class="rw-quiz-btn" onclick="startKeyboardWriting(${lvl.level})">⌨️ Write</button>
                </div></div>` : `<div class="wr-level-locked">🔒 Complete level ${lvl.level - 1} first</div>`}
            </div>`;
        });
    }

    // Traditional categories (kanji, words, grammar — text input)
    html += `<h3 class="wr-section-header" style="margin-top:24px">📊 Advanced Writing</h3>`;
    const categories = [
        { key: "hiragana", data: KANA_DATA.hiragana, icon: "あ", desc: "Write hiragana characters with keyboard" },
        { key: "katakana", data: KANA_DATA.katakana, icon: "ア", desc: "Write katakana characters with keyboard" },
        { key: "kanji", data: KANA_DATA.kanji, icon: "漢", desc: "Type kanji reading (romaji)" },
        { key: "dailyWords", data: KANA_DATA.dailyWords, icon: "語", desc: "Type Japanese words with keyboard" },
        { key: "grammar", data: KANA_DATA.grammar, icon: "文", desc: "Type grammar patterns" },
    ];

    categories.forEach(cat => {
        const groups = cat.key === "grammar" ? [{ name: "All Patterns", chars: cat.data.patterns.map(p => ({ char: p.pattern, romaji: p.id })) }] : cat.data.groups;
        const allChars = groups.flatMap(g => (g.chars || g.words || []).map(c => c.char || c.word));
        let totalScore = 0;
        allChars.forEach(c => { const p = writingProgress[c]; if (p) totalScore += Math.min(p.correct, 3) / 3; });
        const pct = allChars.length > 0 ? Math.round((totalScore / allChars.length) * 100) : 0;
        const learned = allChars.filter(c => writingProgress[c] && writingProgress[c].correct > 0).length;
        const useKB = cat.key === "hiragana" || cat.key === "katakana" || cat.key === "dailyWords";

        html += `<div class="rw-category-card">
            <div class="rw-cat-header">
                <span class="rw-cat-icon">${cat.icon}</span>
                <div class="rw-cat-info"><h3>${cat.data.label}</h3><p>${cat.desc}</p></div>
                <div class="rw-cat-progress"><span class="rw-cat-pct">${pct}%</span><span class="rw-cat-count">${learned}/${allChars.length}</span></div>
            </div>
            <div class="rw-progress-bar"><div class="rw-progress-fill" style="width:${pct}%"></div></div>
            <div class="rw-groups">`;
        if (cat.key === "grammar") {
            html += `<div class="rw-group-row"><button class="rw-quiz-btn" onclick="startTextWritingQuiz('grammar','patterns')">✍️ Practice</button></div>`;
        } else {
            groups.forEach(g => {
                const gChars = (g.chars || g.words || []).map(c => c.char || c.word);
                const gLearned = gChars.filter(c => writingProgress[c] && writingProgress[c].correct > 0).length;
                html += `<div class="rw-group-row">
                    <span class="rw-group-name">${g.name}</span>
                    <span class="rw-group-stat">${gLearned}/${gChars.length}</span>
                    <button class="rw-quiz-btn" onclick="${useKB ? `startKBGroupWriting('${cat.key}','${g.name}')` : `startTextWritingQuiz('${cat.key}','${g.name}')`}">⌨️ Write</button>
                </div>`;
            });
        }
        html += `</div></div>`;
    });

    html += `</div>`;
    panel.innerHTML = html;
}

// --- Keyboard writing for Word-First levels ---
function startKeyboardWriting(level) {
    const lvlData = WORD_FIRST_DATA.find(l => l.level === level);
    if (!lvlData) return;
    const panel = document.getElementById("writingPanel");
    const words = [...lvlData.words];
    let idx = 0;
    let correctCount = 0;

    function renderKBQ() {
        if (idx >= words.length) {
            const pct = Math.round((correctCount / words.length) * 100);
            xp += correctCount * 5;
            unlockNextWR(level);
            saveProgress();
            panel.innerHTML = `<div class="rw-content"><div class="rw-quiz-result">
                <h3>${pct >= 80 ? '🎉 Excellent!' : pct >= 60 ? '👍 Good job!' : '💪 Keep practicing!'}</h3>
                <div class="rw-score">${correctCount}/${words.length} correct</div>
                <div class="rw-quiz-actions">
                    <button class="btn-primary" style="max-width:200px" onclick="startKeyboardWriting(${level})">Try Again</button>
                    <button class="rw-back-btn" onclick="renderWritingPanel()" style="margin-top:8px">← Back</button>
                </div></div></div>`;
            return;
        }
        const w = words[idx];
        kbInput = [];
        kbExpected = w.word;
        kbType = "hiragana";
        kbOnComplete = () => {
            correctCount++;
            markWritingResult(w.word, true);
            [...w.word].forEach(c => markWritingResult(c, true));
            const el = document.getElementById("kbDisplay");
            if (el) el.classList.add('kbd-success');
            setTimeout(() => { idx++; renderKBQ(); }, 800);
        };
        panel.innerHTML = `<div class="rw-content">
            <div class="rw-study-header">
                <button class="rw-back-btn" onclick="renderWritingPanel()">← Back</button>
                <span>${idx + 1} / ${words.length}</span>
                <span>✓ ${correctCount}</span>
            </div>
            <div class="kb-prompt">
                <span class="kb-prompt-emoji">${w.emoji}</span>
                <span class="kb-prompt-romaji">${w.romaji}</span>
                <span class="kb-prompt-meaning">${w.meaning}</span>
            </div>
            <div class="kb-display" id="kbDisplay"></div>
            <div class="kb-hint-row">
                <button class="rw-speak-btn" onclick="speakJapanese('${w.word.replace(/'/g, "\\'")}')" title="Listen">🔊</button>
                <button class="kb-skip-btn" onclick="kbDoSkip()">Skip →</button>
            </div>
            <div class="jpkb" id="jpKeyboard">${getKBRowsHTML()}</div>
        </div>`;
        kbUpdateDisplay();
    }
    window.kbDoSkip = function() { markWritingResult(words[idx].word, false); idx++; renderKBQ(); };
    renderKBQ();
}

// --- Keyboard writing for traditional hiragana/katakana/dailyWords groups ---
function startKBGroupWriting(category, groupName) {
    const items = getGroupItems(category, groupName);
    if (!items.length) return;
    const panel = document.getElementById("writingPanel");
    const shuffled = [...items].sort(() => Math.random() - 0.5).slice(0, 10);
    let idx = 0;
    let correctCount = 0;

    function renderKBGQ() {
        if (idx >= shuffled.length) {
            const pct = Math.round((correctCount / shuffled.length) * 100);
            xp += correctCount * 5;
            saveProgress();
            panel.innerHTML = `<div class="rw-content"><div class="rw-quiz-result">
                <h3>${pct >= 80 ? '🎉 Excellent!' : pct >= 60 ? '👍 Good job!' : '💪 Keep practicing!'}</h3>
                <div class="rw-score">${correctCount}/${shuffled.length} correct</div>
                <div class="rw-quiz-actions">
                    <button class="btn-primary" style="max-width:200px" onclick="startKBGroupWriting('${category}','${groupName}')">Try Again</button>
                    <button class="rw-back-btn" onclick="renderWritingPanel()" style="margin-top:8px">← Back</button>
                </div></div></div>`;
            return;
        }
        const item = shuffled[idx];
        const isKana = category === "hiragana" || category === "katakana";
        kbInput = [];
        kbExpected = item.char;
        kbType = category === "katakana" ? "katakana" : "hiragana";
        const prompt = isKana ? item.romaji : (item.meaning || item.romaji);
        const hint = isKana ? `Write: ${item.romaji}` : `Write: ${item.char}`;
        kbOnComplete = () => {
            correctCount++;
            markWritingResult(item.char, true);
            const el = document.getElementById("kbDisplay");
            if (el) el.classList.add('kbd-success');
            setTimeout(() => { idx++; renderKBGQ(); }, 800);
        };
        panel.innerHTML = `<div class="rw-content">
            <div class="rw-study-header">
                <button class="rw-back-btn" onclick="renderWritingPanel()">← Back</button>
                <span>${idx + 1} / ${shuffled.length}</span>
                <span>✓ ${correctCount}</span>
            </div>
            <div class="kb-prompt">
                <span class="kb-prompt-romaji">${prompt}</span>
                ${!isKana && item.meaning ? `<span class="kb-prompt-meaning">${item.meaning}</span>` : ''}
            </div>
            <div class="kb-display" id="kbDisplay"></div>
            <div class="kb-hint-row">
                <button class="rw-speak-btn" onclick="speakJapanese('${item.char.replace(/'/g, "\\'")}')" title="Listen">🔊</button>
                <button class="kb-skip-btn" onclick="kbDoGroupSkip()">Skip →</button>
            </div>
            <div class="jpkb" id="jpKeyboard">${getKBRowsHTML()}</div>
        </div>`;
        kbUpdateDisplay();
    }
    window.kbDoGroupSkip = function() { markWritingResult(shuffled[idx].char, false); idx++; renderKBGQ(); };
    renderKBGQ();
}

// --- Text-input writing for kanji/grammar (keep original approach) ---
function startTextWritingQuiz(category, groupName) {
    const items = getGroupItems(category, groupName);
    if (!items.length) return;
    const shuffled = [...items].sort(() => Math.random() - 0.5).slice(0, 10);
    writingQuiz = { items: shuffled, current: 0, correct: 0, category, group: groupName };
    renderTextWritingQ();
}

function renderTextWritingQ() {
    const panel = document.getElementById("writingPanel");
    const q = writingQuiz;
    if (q.current >= q.items.length) {
        const pct = Math.round((q.correct / q.items.length) * 100);
        xp += q.correct * 5; saveProgress();
        panel.innerHTML = `<div class="rw-content"><div class="rw-quiz-result">
            <h3>${pct >= 80 ? '🎉 Excellent!' : pct >= 60 ? '👍 Good job!' : '💪 Keep practicing!'}</h3>
            <div class="rw-score">${q.correct}/${q.items.length} correct (${pct}%)</div>
            <div class="rw-quiz-actions">
                <button class="btn-primary" style="max-width:200px" onclick="startTextWritingQuiz('${q.category}','${q.group}')">Try Again</button>
                <button class="rw-back-btn" onclick="renderWritingPanel()" style="margin-top:8px">← Back</button>
            </div></div></div>`;
        return;
    }
    const item = q.items[q.current];
    const isKanji = q.category === "kanji";
    const isWords = q.category === "dailyWords";
    const isGrammar = q.category === "grammar";
    let prompt, hint, expectedAnswers;
    if (isKanji) { prompt = item.char; hint = `Type the reading (romaji)`; expectedAnswers = item.romaji.includes("/") ? item.romaji.split("/").map(r => r.trim()) : [item.romaji]; }
    else if (isWords) { prompt = item.meaning; hint = `Type the Japanese word`; expectedAnswers = [item.char, item.romaji]; }
    else if (isGrammar) { prompt = item.meaning; hint = `Type the grammar pattern`; expectedAnswers = [item.char, item.romaji]; }
    else { prompt = item.romaji; hint = `Type the character`; expectedAnswers = [item.char]; }
    panel.innerHTML = `<div class="rw-content">
        <div class="rw-study-header">
            <button class="rw-back-btn" onclick="renderWritingPanel()">← Back</button>
            <span>Q${q.current + 1} / ${q.items.length}</span><span>✓ ${q.correct}</span>
        </div>
        <div class="rw-writing-card">
            <span class="rw-writing-prompt">${prompt}</span>
            <span class="rw-writing-hint">${hint}</span>
            <div class="rw-writing-input-row">
                <input type="text" class="rw-writing-input" id="writingInput" placeholder="Type here..." autocomplete="off" autofocus>
                <button class="rw-submit-btn" id="writingSubmit">Check</button>
            </div>
            <div class="rw-writing-feedback" id="writingFeedback"></div>
        </div></div>`;
    const input = document.getElementById("writingInput");
    const submitBtn = document.getElementById("writingSubmit");
    input.focus();
    function checkAnswer() {
        const answer = input.value.trim().toLowerCase();
        if (!answer) return;
        const correct = expectedAnswers.some(exp => answer === exp.toLowerCase() || answer === exp);
        const isCorrect = correct || answer === item.char;
        const fb = document.getElementById("writingFeedback");
        if (isCorrect) {
            fb.innerHTML = `<span class="rw-fb-correct">✅ Correct! ${item.char} = ${item.romaji}${item.meaning ? ' (' + item.meaning + ')' : ''}</span>`;
            writingQuiz.correct++;
        } else {
            fb.innerHTML = `<span class="rw-fb-wrong">❌ Answer: <strong>${item.char}</strong> (${item.romaji})${item.meaning ? ' = ' + item.meaning : ''}</span>`;
        }
        markWritingResult(item.char, isCorrect);
        input.disabled = true; submitBtn.disabled = true;
        setTimeout(() => { writingQuiz.current++; renderTextWritingQ(); }, 1800);
    }
    submitBtn.onclick = checkAnswer;
    input.onkeydown = (e) => { if (e.key === "Enter") checkAnswer(); };
}

// --- My Vocabulary (replaces old Phrase Book) ---
// Shows words learned from Reading & Writing, grouped by category
function renderMyVocabulary() {
    const panel = phraseBook;
    if (!panel || typeof KANA_DATA === 'undefined') return;

    // Gather all learned items from reading + writing progress
    const sections = [];

    // Word-First levels
    if (typeof WORD_FIRST_DATA !== 'undefined') {
        const wfWords = [];
        WORD_FIRST_DATA.forEach(lvl => {
            lvl.words.forEach(w => {
                const rp = readingProgress[w.word];
                const wp = writingProgress[w.word];
                if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                    wfWords.push({ jp: w.word, romaji: w.romaji, en: w.meaning, emoji: w.emoji,
                        rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
                }
            });
        });
        if (wfWords.length > 0) sections.push({ title: '🔤 Word-First Words', items: wfWords });
    }

    // Hiragana characters
    const hiraItems = [];
    KANA_DATA.hiragana.groups.forEach(g => {
        g.chars.forEach(c => {
            const rp = readingProgress[c.char];
            const wp = writingProgress[c.char];
            if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                hiraItems.push({ jp: c.char, romaji: c.romaji, en: c.hint || c.romaji,
                    rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
            }
        });
    });
    if (hiraItems.length > 0) sections.push({ title: 'あ Hiragana', items: hiraItems });

    // Katakana characters
    const kataItems = [];
    KANA_DATA.katakana.groups.forEach(g => {
        g.chars.forEach(c => {
            const rp = readingProgress[c.char];
            const wp = writingProgress[c.char];
            if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                kataItems.push({ jp: c.char, romaji: c.romaji, en: c.hint || c.romaji,
                    rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
            }
        });
    });
    if (kataItems.length > 0) sections.push({ title: 'ア Katakana', items: kataItems });

    // Kanji
    const kanjiItems = [];
    KANA_DATA.kanji.groups.forEach(g => {
        g.chars.forEach(c => {
            const rp = readingProgress[c.char];
            const wp = writingProgress[c.char];
            if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                kanjiItems.push({ jp: c.char, romaji: c.romaji, en: c.meaning,
                    rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
            }
        });
    });
    if (kanjiItems.length > 0) sections.push({ title: '漢 Kanji', items: kanjiItems });

    // Daily Words
    const dwItems = [];
    KANA_DATA.dailyWords.groups.forEach(g => {
        (g.words || []).forEach(w => {
            const rp = readingProgress[w.word];
            const wp = writingProgress[w.word];
            if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
                dwItems.push({ jp: w.word, romaji: w.romaji, en: w.meaning,
                    rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
            }
        });
    });
    if (dwItems.length > 0) sections.push({ title: '語 Daily Words', items: dwItems });

    // Grammar patterns
    const gramItems = [];
    KANA_DATA.grammar.patterns.forEach(p => {
        const rp = readingProgress[p.pattern];
        const wp = writingProgress[p.pattern];
        if ((rp && rp.correct > 0) || (wp && wp.correct > 0)) {
            gramItems.push({ jp: p.pattern, romaji: p.id, en: p.meaning,
                example: p.example, exampleEn: p.exampleEn,
                rScore: rp ? rp.correct : 0, wScore: wp ? wp.correct : 0 });
        }
    });
    if (gramItems.length > 0) sections.push({ title: '文 Grammar', items: gramItems, isGrammar: true });

    // Total count
    const totalLearned = sections.reduce((s, sec) => s + sec.items.length, 0);

    let html = `<div class="myvocab-content">
        <h2 class="myvocab-title">📋 My Vocabulary</h2>
        <p class="myvocab-subtitle">Words & characters you've learned from Reading & Writing practice.</p>
        <div class="myvocab-stats">
            <span class="myvocab-stat">${totalLearned} items learned</span>
            <span class="myvocab-stat">R: ${Math.round(getReadingPct() * 100)}%</span>
            <span class="myvocab-stat">W: ${Math.round(getWritingPct() * 100)}%</span>
        </div>`;

    if (totalLearned === 0) {
        html += `<div class="myvocab-empty">
            <div class="myvocab-empty-icon">📚</div>
            <h3>No words yet!</h3>
            <p>Start learning in <strong>📚 Reading</strong> or <strong>✍️ Writing</strong> mode to build your vocabulary here.</p>
            <div style="display:flex;gap:8px;justify-content:center;margin-top:12px">
                <button class="btn-primary" style="max-width:140px" onclick="switchMode('reading')">📚 Reading</button>
                <button class="btn-primary" style="max-width:140px" onclick="switchMode('writing')">✍️ Writing</button>
            </div>
        </div>`;
    } else {
        sections.forEach(sec => {
            html += `<div class="myvocab-section">
                <h3 class="myvocab-section-title">${sec.title} <span class="myvocab-section-count">${sec.items.length}</span></h3>
                <div class="myvocab-list">`;
            sec.items.forEach(item => {
                const totalScore = item.rScore + item.wScore;
                const mastery = Math.min(totalScore, 6);
                const masteryClass = mastery >= 6 ? 'mastered' : mastery >= 3 ? 'learning' : 'new';
                const masteryLabel = mastery >= 6 ? 'Mastered' : mastery >= 3 ? 'Learning' : 'New';
                const progressPct = Math.round((mastery / 6) * 100);
                
                html += `<div class="myvocab-card myvocab-${masteryClass}">
                    <div class="myvocab-card-main">
                        <span class="myvocab-jp">${item.emoji ? item.emoji + ' ' : ''}${item.jp}</span>
                        <span class="myvocab-romaji">${item.romaji}</span>
                        <span class="myvocab-en">${item.en}</span>
                    </div>
                    <div class="myvocab-card-meta">
                        <div class="myvocab-progress-bar">
                            <div class="myvocab-progress-fill ${masteryClass}" style="width: ${progressPct}%"></div>
                        </div>
                        <span class="myvocab-mastery-badge ${masteryClass}">${masteryLabel}</span>
                        <span class="myvocab-scores" title="Reading: ${item.rScore} correct | Writing: ${item.wScore} correct">📖${item.rScore} ✍${item.wScore}</span>
                        <button class="play-btn" onclick="speakJapanese('${item.jp.replace(/'/g, "\\\\'")}')" title="Listen">🔊</button>
                    </div>
                    ${sec.isGrammar && item.example ? `<div class="myvocab-example">
                        <span class="myvocab-example-jp">${item.example}</span>
                        <span class="myvocab-example-en">${item.exampleEn}</span>
                    </div>` : ''}
                </div>`;
            });
            html += `</div></div>`;
        });
    }

    html += `</div>`;
    panel.innerHTML = html;
}

// Keep old renderPhrases for backward compat but redirect
function renderPhrases(category) {
    renderMyVocabulary();
}

// --- Parse [CORRECTION] block ---
function parseCorrectionBlock(text) {
    const regex = /\[CORRECTION\]\n?([\s\S]*?)\n?\[\/CORRECTION\]/;
    const match = regex.exec(text);
    if (!match) return { correction: null, remaining: text };

    const block = match[1].trim();
    const fields = {};
    block.split("\n").forEach(line => {
        const idx = line.indexOf(":");
        if (idx > 0) {
            const key = line.substring(0, idx).trim().toLowerCase().replace(/\s+/g, "_");
            fields[key] = line.substring(idx + 1).trim();
        }
    });

    const correction = {
        original: fields.original || "",
        correctedEn: fields.corrected_en || "",
        correctedJp: fields.corrected_jp || "",
        romaji: fields.romaji || "",
        note: fields.note || ""
    };

    const remaining = text.replace(match[0], "").trim();
    return { correction, remaining };
}

function renderCorrectionHTML(correction) {
    const isPerfect = correction.note.toLowerCase().includes("perfect") || correction.note.toLowerCase().includes("no correction");
    return `<div class="correction-block ${isPerfect ? 'perfect' : 'has-fix'}">
        <div class="corr-header">${isPerfect ? '✅ Your message' : '📝 Correction'}</div>
        <div class="corr-row">
            <span class="corr-label">You said:</span>
            <span class="corr-value corr-original">${correction.original}</span>
        </div>
        <div class="corr-row">
            <span class="corr-label">English:</span>
            <span class="corr-value corr-en">${correction.correctedEn}</span>
        </div>
        <div class="corr-row">
            <span class="corr-label">Japanese:</span>
            <span class="corr-value corr-jp">${correction.correctedJp}</span>
        </div>
        ${correction.romaji ? `<div class="corr-row">
            <span class="corr-label">Romaji:</span>
            <span class="corr-value corr-romaji">${correction.romaji}</span>
        </div>` : ''}
        <div class="corr-note">${isPerfect ? '👍 ' : '💡 '}${correction.note}</div>
        <button class="corr-speak" onclick="speakJapanese('${correction.correctedJp.replace(/'/g, "\\'")}')">🔊 Hear correct Japanese</button>
    </div>`;
}

// --- Parse AI response with [CORRECTION] and [BREAKDOWN] blocks ---
function parseAIResponse(text) {
    // First extract correction block
    const { correction, remaining } = parseCorrectionBlock(text);

    const parts = [];
    if (correction) parts.push({ type: "correction", data: correction });

    // Then parse breakdowns from remaining text
    const regex = /\[BREAKDOWN\]\n?([\s\S]*?)\n?\[\/BREAKDOWN\]/g;
    let match;
    let lastIndex = 0;

    while ((match = regex.exec(remaining)) !== null) {
        if (match.index > lastIndex) {
            parts.push({ type: "text", content: remaining.substring(lastIndex, match.index) });
        }
        const rows = match[1].trim().split("\n").filter(r => r.trim()).map(row => {
            const cols = row.split("|").map(c => c.trim());
            return { word: cols[0] || "", reading: cols[1] || "", meaning: cols[2] || "", grammar: cols[3] || "" };
        });
        parts.push({ type: "breakdown", rows });
        rows.forEach(r => {
            if (r.word && r.meaning) {
                trackWord(r.word, r.reading, r.meaning);
                if (r.grammar) trackGrammar(r.grammar);
            }
        });
        lastIndex = match.index + match[0].length;
    }
    if (lastIndex < remaining.length) parts.push({ type: "text", content: remaining.substring(lastIndex) });
    if (parts.length === 0) parts.push({ type: "text", content: remaining });
    return parts;
}

function renderBreakdownHTML(rows) {
    return `<div class="breakdown-table">
        <div class="breakdown-header">
            <span>Word</span><span>Reading</span><span>Meaning</span><span>Grammar</span>
        </div>
        ${rows.map(r => `
            <div class="breakdown-row">
                <span class="clickable-word" data-word="${encodeURIComponent(r.word)}"
                      data-reading="${encodeURIComponent(r.reading)}"
                      data-meaning="${encodeURIComponent(r.meaning)}"
                      data-grammar="${encodeURIComponent(r.grammar)}">${r.word}</span>
                <span class="br-reading">${r.reading}</span>
                <span class="br-meaning">${r.meaning}</span>
                <span class="br-grammar">${r.grammar}</span>
            </div>
        `).join("")}
    </div>`;
}

// --- Chat ---
function addMessage(text, role) {
    const div = document.createElement("div");
    div.className = `message ${role}`;

    if (role === "ai") {
        const parts = parseAIResponse(text);
        let html = "";
        parts.forEach(part => {
            if (part.type === "correction") {
                html += renderCorrectionHTML(part.data);
            } else if (part.type === "text") {
                html += part.content
                    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
                    .replace(/\n/g, "<br>");
            } else if (part.type === "breakdown") {
                html += renderBreakdownHTML(part.rows);
            }
        });
        div.innerHTML = html;

        const speakBtn = document.createElement("button");
        speakBtn.className = "speak-btn";
        speakBtn.textContent = "🔊";
        speakBtn.onclick = () => speakText(text);
        div.appendChild(speakBtn);

        setTimeout(() => {
            div.querySelectorAll(".clickable-word").forEach(el => {
                el.addEventListener("click", (e) => { e.stopPropagation(); showWordPopup(el, e); });
            });
        }, 0);
    } else {
        div.innerHTML = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");
    }

    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showWordPopup(el, event) {
    document.querySelectorAll(".word-popup").forEach(p => p.remove());
    const word = decodeURIComponent(el.dataset.word);
    const reading = decodeURIComponent(el.dataset.reading);
    const meaning = decodeURIComponent(el.dataset.meaning);
    const grammar = decodeURIComponent(el.dataset.grammar);
    const stored = learnedWords[word];
    const seenCount = stored ? stored.seen : 1;

    const popup = document.createElement("div");
    popup.className = "word-popup";
    popup.innerHTML = `
        <div class="wp-header">
            <span class="wp-word">${word}</span>
            <button class="wp-speak" onclick="speakJapanese('${word.replace(/'/g, "\\'")}')">🔊</button>
            <button class="wp-close">&times;</button>
        </div>
        <div class="wp-reading">${reading}</div>
        <div class="wp-meaning">${meaning}</div>
        <div class="wp-divider"></div>
        <div class="wp-section-title">Grammar Note</div>
        <div class="wp-grammar">${grammar || "No grammar note"}</div>
        <div class="wp-divider"></div>
        <div class="wp-section-title">Usage</div>
        <div class="wp-usage">Loading...</div>
        <div class="wp-meta">Seen ${seenCount}x</div>
        <button class="wp-ask-btn">Ask AI for examples</button>
    `;

    document.body.appendChild(popup);
    const rect = el.getBoundingClientRect();
    let top = rect.bottom + 8;
    let left = rect.left;
    if (top + 300 > window.innerHeight) top = rect.top - 310;
    if (left + 280 > window.innerWidth) left = window.innerWidth - 290;
    if (left < 10) left = 10;
    popup.style.top = `${top}px`;
    popup.style.left = `${left}px`;

    loadQuickUsage(word, popup.querySelector(".wp-usage"));
    popup.querySelector(".wp-close").onclick = () => popup.remove();
    popup.querySelector(".wp-ask-btn").onclick = () => {
        popup.remove();
        textInput.value = `Explain "${word}" (${reading}). Show 3 example sentences with breakdowns, collocations, and related words.`;
        sendMessage();
    };
}

function loadQuickUsage(word, container) {
    const examples = [];
    Object.values(PHRASES).flat().forEach(p => {
        if (p.jp.includes(word)) examples.push(`${p.jp} (${p.romaji}) = ${p.en}`);
    });
    container.innerHTML = examples.length > 0
        ? examples.slice(0, 3).map(e => `<div class="wp-example">${e}</div>`).join("")
        : `<div class="wp-example" style="color:var(--text-dim)">No examples in phrase book. Click "Ask AI" below.</div>`;
}

function addSystemMessage(text) {
    const div = document.createElement("div");
    div.className = "message system";
    div.textContent = text;
    messagesEl.appendChild(div);
}

function showTyping() {
    const div = document.createElement("div");
    div.className = "typing";
    div.id = "typingIndicator";
    div.innerHTML = "<span>.</span><span>.</span><span>.</span> sensei is thinking";
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById("typingIndicator");
    if (el) el.remove();
}

// --- Send Message ---
function sendMessage() {
    const text = textInput.value.trim();
    if (!text) return;
    textInput.value = "";
    addMessage(text, "user");
    xp += 2;
    sessionMessages++;
    saveProgress();
    sendToAI(text);
}

async function sendToAI(userText) {
    conversationHistory.push({ role: "user", content: userText });
    showTyping();

    const lvl = getLevel();
    const levelCtx = `\n[Student level: ${lvl.label} (${lvl.pct.toFixed(0)}% N5). Words: ${Object.keys(learnedWords).length}. Adjust difficulty.]`;
    const sysPrompt = currentMode === "jlpt" ? SYSTEM_PROMPTS.jlpt : (SYSTEM_PROMPTS[currentMode] || SYSTEM_PROMPTS.conversation);

    // Inject learned words for practice mode so AI can drill relevant vocabulary
    let learnedCtx = "";
    if (currentMode === "conversation") {
        const learned = getLearnedWordsSummary();
        if (learned.length > 0) {
            learnedCtx = `\n[Student's learned words (${learned.length} total): ${learned.slice(0, 60).join(', ')}${learned.length > 60 ? '...' : ''}. Use these in drills and conversation. Build on what they know.]`;
        } else {
            learnedCtx = `\n[Student has not practiced Reading/Writing yet. Start with basic greetings and simple words.]`;
        }
    }

    const messages = [
        { role: "system", content: sysPrompt + levelCtx + learnedCtx },
        ...conversationHistory.slice(-20)
    ];

    try {
        const res = await fetch("https://api.openai.com/v1/chat/completions", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
            body: JSON.stringify({ model, messages, temperature: 0.8, max_tokens: 800 })
        });
        hideTyping();
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            addSystemMessage(res.status === 401 ? "Invalid API key. Click gear to update." : `API error: ${err.error?.message || res.statusText}`);
            return;
        }
        const data = await res.json();
        const reply = data.choices[0].message.content;
        conversationHistory.push({ role: "assistant", content: reply });
        addMessage(reply, "ai");
        if (autoSpeak.checked) speakText(reply);
    } catch (err) {
        hideTyping();
        addSystemMessage(`Connection error: ${err.message}`);
    }
}

// --- Speech Recognition (STT) ---
function initSpeechRecognition() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { voiceStatus.textContent = "Voice not supported. Use Chrome."; micBtn.disabled = true; return; }
    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.onstart = () => { isRecording = true; micBtn.classList.add("recording"); voiceStatus.textContent = "Listening..."; };
    recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) transcript += event.results[i][0].transcript;
        textInput.value = transcript;
        if (event.results[event.results.length - 1].isFinal) voiceStatus.textContent = "Got it!";
    };
    recognition.onerror = (event) => { voiceStatus.textContent = `Voice error: ${event.error}`; stopRecording(); };
    recognition.onend = () => { if (isRecording) { stopRecording(); if (textInput.value.trim()) sendMessage(); } };
}

function toggleRecording() {
    if (isRecording) { recognition.stop(); }
    else { recognition.lang = japaneseVoice.checked ? "ja-JP" : "en-US"; try { recognition.start(); } catch(e) { voiceStatus.textContent = "Mic busy."; } }
}
function stopRecording() { isRecording = false; micBtn.classList.remove("recording"); voiceStatus.textContent = "Click 🎤 to speak"; }

// ===========================================
// BILINGUAL TTS - Japanese voice for JP text,
// English voice for EN text. No double-reading.
// ===========================================
const JP_REGEX = /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]/;

function getPreferredJapaneseVoice() {
    const voices = speechSynthesis.getVoices();
    const jpVoices = voices.filter(v => v.lang.startsWith("ja"));
    const maleKw = ["male", "ichiro", "takumi", "kenji", "keitaro", "daichi"];
    const femaleKw = ["female", "ayumi", "hanako", "kyoko", "nanami", "haruka"];
    let best = null, bestScore = -1;
    for (const v of jpVoices) {
        const name = v.name.toLowerCase();
        let score = 1;
        if (maleKw.some(k => name.includes(k))) score += 10;
        if (femaleKw.some(k => name.includes(k))) score -= 10;
        if (v.localService) score += 2;
        if (name.includes("microsoft")) score += 3;
        if (score > bestScore) { bestScore = score; best = v; }
    }
    return best || jpVoices[0] || null;
}

function getEnglishVoice() {
    const voices = speechSynthesis.getVoices();
    const enVoices = voices.filter(v => v.lang.startsWith("en"));
    // Prefer male English voice too for consistency
    const maleKw = ["male", "david", "mark", "james", "guy", "daniel"];
    let best = null, bestScore = -1;
    for (const v of enVoices) {
        const name = v.name.toLowerCase();
        let score = 1;
        if (maleKw.some(k => name.includes(k))) score += 10;
        if (v.localService) score += 2;
        if (name.includes("microsoft")) score += 3;
        if (score > bestScore) { bestScore = score; best = v; }
    }
    return best || enVoices[0] || null;
}

/**
 * Split text into segments of Japanese and non-Japanese.
 * Each segment: { lang: "ja"|"en", text: "..." }
 * Punctuation/spaces inherit the language of surrounding text.
 */
function splitByLanguage(text) {
    // First pass: classify each character
    const JP_CHARS = /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]/;
    const NEUTRAL = /[\s.,!?;:'"。、！？・…―ー\-\d\u200b]/;  // space, punctuation, numbers = neutral

    const chars = [...text];
    const tagged = chars.map(ch => {
        if (JP_CHARS.test(ch)) return "ja";
        if (NEUTRAL.test(ch)) return "neutral";
        return "en";
    });

    // Resolve neutrals: inherit from nearest non-neutral neighbor (prefer left)
    for (let i = 0; i < tagged.length; i++) {
        if (tagged[i] === "neutral") {
            // Look left for nearest non-neutral
            let left = null;
            for (let j = i - 1; j >= 0; j--) { if (tagged[j] !== "neutral") { left = tagged[j]; break; } }
            // Look right for nearest non-neutral
            let right = null;
            for (let j = i + 1; j < tagged.length; j++) { if (tagged[j] !== "neutral") { right = tagged[j]; break; } }
            tagged[i] = left || right || "en";
        }
    }

    // Build segments
    const segments = [];
    let current = "";
    let currentLang = tagged[0] || "en";

    for (let i = 0; i < chars.length; i++) {
        if (tagged[i] === currentLang) {
            current += chars[i];
        } else {
            if (current.trim()) segments.push({ lang: currentLang, text: current.trim() });
            currentLang = tagged[i];
            current = chars[i];
        }
    }
    if (current.trim()) segments.push({ lang: currentLang, text: current.trim() });

    // Merge adjacent same-language & absorb tiny EN segments (< 4 real chars) between JP
    const merged = [];
    for (const seg of segments) {
        if (merged.length > 0 && merged[merged.length - 1].lang === seg.lang) {
            merged[merged.length - 1].text += " " + seg.text;
        } else {
            merged.push({ ...seg });
        }
    }

    // Second merge: tiny EN segments between JP segments → absorb into JP (likely punctuation/numbers)
    const final = [];
    for (let i = 0; i < merged.length; i++) {
        const seg = merged[i];
        if (seg.lang === "en" && seg.text.replace(/\s/g, "").length < 4) {
            const prevJP = final.length > 0 && final[final.length - 1].lang === "ja";
            const nextJP = i + 1 < merged.length && merged[i + 1].lang === "ja";
            if (prevJP && nextJP) {
                final[final.length - 1].text += " " + seg.text;
                continue;
            }
        }
        if (final.length > 0 && final[final.length - 1].lang === seg.lang) {
            final[final.length - 1].text += " " + seg.text;
        } else {
            final.push({ ...seg });
        }
    }

    // Filter out segments with no real content
    return final.filter(s => s.text.replace(/[.,!?;:\s]+/g, "").length > 0);
}

function speakText(text) {
    // Clean: strip all structured blocks, markdown, romaji, translations
    let clean = text
        .replace(/\[CORRECTION\][\s\S]*?\[\/CORRECTION\]/g, "")  // Strip correction blocks (avoid double JP reading)
        .replace(/\[BREAKDOWN\][\s\S]*?\[\/BREAKDOWN\]/g, "")    // Strip breakdown tables
        .replace(/\[JLPT_TEST\][\s\S]*?\[\/JLPT_TEST\]/g, "")   // Strip test blocks
        .replace(/\*\*/g, "")                                      // Strip bold markdown
        .replace(/[📝🎯💡💬📖📋📊✅👍❌]/g, "")                    // Strip emojis
        .replace(/\([^)]*\)/g, "")                                 // Strip ALL parenthesized text (romaji, notes)
        .replace(/^=\s*.+$/gm, "")                                 // Strip "= English translation" lines
        .replace(/\[Coach\]:?/g, "")                               // Strip [Coach] labels
        .replace(/\[Interviewer\]:?/g, "")                         // Strip [Interviewer] labels
        .replace(/\n+/g, " ")
        .replace(/\s+/g, " ")
        .trim();

    if (!clean) return;
    speechSynthesis.cancel();

    const segments = splitByLanguage(clean);
    speakSegmentsSequentially(segments, 0);
}

function speakSegmentsSequentially(segments, index) {
    if (index >= segments.length) return;
    const seg = segments[index];
    const utterance = new SpeechSynthesisUtterance(seg.text);

    if (seg.lang === "ja") {
        utterance.lang = "ja-JP";
        utterance.rate = 0.75;
        utterance.pitch = 0.85;
        const v = getPreferredJapaneseVoice();
        if (v) utterance.voice = v;
    } else {
        utterance.lang = "en-US";
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        const v = getEnglishVoice();
        if (v) utterance.voice = v;
    }

    utterance.onend = () => speakSegmentsSequentially(segments, index + 1);
    utterance.onerror = () => speakSegmentsSequentially(segments, index + 1);
    speechSynthesis.speak(utterance);
}

function speakJapanese(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ja-JP";
    utterance.rate = 0.75;
    utterance.pitch = 0.85;
    const v = getPreferredJapaneseVoice();
    if (v) utterance.voice = v;
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
}

// Preload voices
speechSynthesis.onvoiceschanged = () => {
    const jp = getPreferredJapaneseVoice();
    const en = getEnglishVoice();
    if (jp) console.log("JP voice:", jp.name);
    if (en) console.log("EN voice:", en.name);
};

// ============================================
// WORD RECOGNITION MODE — Word-First Learning
// Step 1: Learn characters through real words
// Step 2: Visual grouping with word context
// Step 3: Mini vocabulary for pattern repetition
// Step 4: Speed recognition drills
// ============================================

let wrProgress = JSON.parse(localStorage.getItem("jcoach_wr") || "{}");

function saveWR() {
    localStorage.setItem("jcoach_wr", JSON.stringify(wrProgress));
}

function getWRLevel(level) {
    return wrProgress[level] || { unlocked: level <= 1, bestSpeed: null, wordsLearned: 0, speedClears: 0 };
}

function setWRLevel(level, data) {
    wrProgress[level] = data;
    saveWR();
}

function renderWordRecogPanel() {
    const panel = document.getElementById("wordRecogPanel");
    if (!panel || typeof WORD_FIRST_DATA === "undefined") { if (panel) panel.innerHTML = "<p>Loading...</p>"; return; }

    // Ensure level 1 is unlocked
    if (!wrProgress[1]) wrProgress[1] = { unlocked: true, bestSpeed: null, wordsLearned: 0, speedClears: 0 };

    let html = `<div class="wr-content">
        <h2 class="wr-title">🔤 Word-First Recognition</h2>
        <p class="wr-subtitle">Learn characters through real words — not isolation. Your brain sees <strong>patterns</strong>, not symbols.</p>

        <div class="wr-method-cards">
            <div class="wr-method"><span class="wr-method-num">1</span><span>Learn characters <strong>inside real words</strong></span></div>
            <div class="wr-method"><span class="wr-method-num">2</span><span>Visual grouping — <strong>similar shapes, different words</strong></span></div>
            <div class="wr-method"><span class="wr-method-num">3</span><span>High-frequency <strong>mini vocabulary</strong></span></div>
            <div class="wr-method"><span class="wr-method-num">4</span><span>Speed drill — <strong>instant recognition</strong>, not slow recall</span></div>
        </div>

        <div class="wr-levels">`;

    WORD_FIRST_DATA.forEach((lvl, i) => {
        const prog = getWRLevel(lvl.level);
        const isUnlocked = prog.unlocked;
        const pct = lvl.words.length > 0 ? Math.round((prog.wordsLearned / lvl.words.length) * 100) : 0;
        const isComplete = pct >= 100;
        const isCurrent = isUnlocked && !isComplete;
        const section = lvl.level <= 9 ? "step1" : lvl.level <= 13 ? "step2" : "step3";

        // Add section headers
        if (lvl.level === 1) html += `<h3 class="wr-section-header">📝 Step 1 — Real Words</h3>`;
        if (lvl.level === 10) html += `<h3 class="wr-section-header">👁️ Step 2 — Visual Groups</h3>`;
        if (lvl.level === 14) html += `<h3 class="wr-section-header">📚 Step 3 — Mini Vocabulary</h3>`;

        html += `<div class="wr-level-card ${isUnlocked ? '' : 'locked'} ${isCurrent ? 'current' : ''} ${isComplete ? 'complete' : ''}">
            <div class="wr-level-info">
                <div class="wr-level-badge">${isComplete ? '✅' : isUnlocked ? lvl.level : '🔒'}</div>
                <div class="wr-level-text">
                    <strong>${lvl.title}</strong>
                    <span>${lvl.subtitle}</span>
                </div>
                ${lvl.focus.length ? `<div class="wr-level-chars">${lvl.focus.join(' ')}</div>` : ''}
            </div>
            ${isUnlocked ? `
                <div class="wr-level-bar"><div class="wr-level-fill" style="width:${Math.min(pct, 100)}%"></div></div>
                <div class="wr-level-actions">
                    <button class="wr-learn-btn" onclick="startWRLearn(${lvl.level})">📖 Learn</button>
                    <button class="wr-speed-btn" onclick="startWRSpeed(${lvl.level})">⚡ Speed</button>
                    ${prog.bestSpeed ? `<span class="wr-best-time">🏆 ${(prog.bestSpeed / 1000).toFixed(1)}s</span>` : ''}
                </div>
            ` : `<div class="wr-level-locked">Complete level ${lvl.level - 1} to unlock</div>`}
        </div>`;
    });

    // Speed challenge across all learned words
    const totalLearned = Object.values(wrProgress).reduce((s, p) => s + (p.wordsLearned || 0), 0);
    if (totalLearned >= 6) {
        html += `<h3 class="wr-section-header">⚡ Step 4 — Speed Challenge</h3>
            <div class="wr-level-card current">
                <div class="wr-level-info">
                    <div class="wr-level-badge">⚡</div>
                    <div class="wr-level-text">
                        <strong>Speed Recognition Challenge</strong>
                        <span>Can you read ALL learned words instantly?</span>
                    </div>
                </div>
                <div class="wr-level-actions">
                    <button class="wr-speed-btn wr-challenge-btn" onclick="startWRChallenge()">🔥 ${totalLearned} words — GO!</button>
                </div>
            </div>`;
    }

    html += `</div></div>`;
    panel.innerHTML = html;
}

// --- Word Learn Mode: Show word cards with character breakdown ---
function startWRLearn(level) {
    const lvlData = WORD_FIRST_DATA.find(l => l.level === level);
    if (!lvlData) return;
    const panel = document.getElementById("wordRecogPanel");
    const words = lvlData.words;
    let idx = 0;
    let phase = "word"; // word → breakdown → next

    function renderLearnCard() {
        const w = words[idx];
        const mn = typeof MNEMONICS !== "undefined" ? MNEMONICS : {};
        phase = "word";

        // Break word into individual characters for breakdown display
        const chars = [...w.word];
        const breakdownHTML = chars.map(c => {
            const m = mn[c] || null;
            // Find this char's romaji from KANA_DATA
            let charRomaji = "";
            ["hiragana", "katakana"].forEach(type => {
                if (typeof KANA_DATA !== "undefined") {
                    KANA_DATA[type].groups.forEach(g => {
                        (g.chars || []).forEach(ch => { if (ch.char === c) charRomaji = ch.romaji; });
                    });
                }
            });
            return `<div class="wr-char-cell">
                <span class="wr-char-big">${c}</span>
                <span class="wr-char-romaji">${charRomaji}</span>
                ${m ? `<span class="wr-char-mnemonic">${m.visual}</span>` : ''}
            </div>`;
        }).join('');

        const tipHTML = w.tip ? `<div class="wr-tip">${w.tip}</div>` : '';

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="unlockNextWR(${level});renderWordRecogPanel()">← Back</button>
                <span>${idx + 1} / ${words.length}</span>
                <span>${lvlData.title}</span>
            </div>
            <div class="wr-card" id="wrCard">
                <div class="wr-card-word" id="wrWordFace">
                    <span class="wr-word-emoji">${w.emoji}</span>
                    <span class="wr-word-big">${w.word}</span>
                    <span class="wr-word-hint">tap to reveal ↓</span>
                </div>
                <div class="wr-card-detail" id="wrDetailFace" style="display:none">
                    <span class="wr-detail-word">${w.word}</span>
                    <span class="wr-detail-romaji">${w.romaji}</span>
                    <span class="wr-detail-meaning">${w.emoji} ${w.meaning}</span>
                    <div class="wr-breakdown">${breakdownHTML}</div>
                    ${tipHTML}
                </div>
            </div>
            <div class="wr-nav-row">
                <button class="rw-speak-btn" onclick="speakJapanese('${w.word.replace(/'/g, "\\'")}')">🔊</button>
                ${idx > 0 ? `<button class="wr-nav-btn" onclick="wrPrev()">◀ Prev</button>` : '<span></span>'}
                <button class="wr-nav-btn wr-nav-next" onclick="wrNext()">${idx < words.length - 1 ? 'Next ▶' : '✅ Done'}</button>
            </div>
        </div>`;

        document.getElementById("wrCard").onclick = (e) => {
            if (e.target.closest(".wr-nav-row") || e.target.closest("button")) return;
            if (phase === "word") {
                document.getElementById("wrWordFace").style.display = "none";
                document.getElementById("wrDetailFace").style.display = "flex";
                phase = "detail";
            }
        };
    }

    window.wrPrev = function() { if (idx > 0) { idx--; renderLearnCard(); } };
    window.wrNext = function() {
        // Mark word as learned
        const prog = getWRLevel(level);
        prog.wordsLearned = Math.max(prog.wordsLearned, idx + 1);
        prog.unlocked = true;
        setWRLevel(level, prog);

        // Track in main progress system
        const w = words[idx];
        trackWord(w.word, w.romaji, w.meaning);
        // Track individual characters in reading progress
        [...w.word].forEach(c => { markReadingResult(c, true); });

        idx++;
        if (idx < words.length) { renderLearnCard(); }
        else {
            unlockNextWR(level);
            xp += 15;
            saveProgress();
            panel.innerHTML = `<div class="wr-content">
                <div class="wr-complete">
                    <h3>🎉 Level ${level} Complete!</h3>
                    <p>You learned ${words.length} words. Now try the <strong>⚡ Speed Drill</strong> to build instant recognition!</p>
                    <div class="wr-complete-actions">
                        <button class="wr-speed-btn" onclick="startWRSpeed(${level})">⚡ Speed Drill</button>
                        <button class="btn-primary" onclick="renderWordRecogPanel()">← Back to Levels</button>
                    </div>
                </div>
            </div>`;
        }
    };

    renderLearnCard();
}

function unlockNextWR(currentLevel) {
    const nextLevel = currentLevel + 1;
    const nextData = WORD_FIRST_DATA.find(l => l.level === nextLevel);
    if (nextData) {
        const prog = getWRLevel(nextLevel);
        prog.unlocked = true;
        setWRLevel(nextLevel, prog);
    }
}

// --- Speed Drill: Timed word recognition ---
function startWRSpeed(level) {
    const lvlData = WORD_FIRST_DATA.find(l => l.level === level);
    if (!lvlData) return;
    const panel = document.getElementById("wordRecogPanel");
    const words = [...lvlData.words].sort(() => Math.random() - 0.5);
    let idx = 0;
    let correct = 0;
    let startTime = Date.now();

    function renderSpeedCard() {
        if (idx >= words.length) {
            const elapsed = Date.now() - startTime;
            const pct = Math.round((correct / words.length) * 100);
            const avgMs = Math.round(elapsed / words.length);

            // Update best time
            const prog = getWRLevel(level);
            if (pct >= 80 && (!prog.bestSpeed || elapsed < prog.bestSpeed)) {
                prog.bestSpeed = elapsed;
            }
            prog.speedClears = (prog.speedClears || 0) + 1;
            setWRLevel(level, prog);
            xp += correct * 3;
            saveProgress();

            panel.innerHTML = `<div class="wr-content">
                <div class="wr-complete">
                    <h3>${pct >= 90 ? '🔥 Lightning Fast!' : pct >= 70 ? '⚡ Great Speed!' : '💪 Keep Practicing!'}</h3>
                    <div class="wr-speed-stats">
                        <div class="wr-stat"><span class="wr-stat-num">${correct}/${words.length}</span><span>correct</span></div>
                        <div class="wr-stat"><span class="wr-stat-num">${(elapsed / 1000).toFixed(1)}s</span><span>total time</span></div>
                        <div class="wr-stat"><span class="wr-stat-num">${avgMs}ms</span><span>per word</span></div>
                    </div>
                    ${pct < 80 ? `<p class="wr-speed-tip">💡 Goal: Read each word <strong>instantly</strong> — not い…ぬ…maybe… but いぬ = dog! 🐕</p>` : ''}
                    <div class="wr-complete-actions">
                        <button class="wr-speed-btn" onclick="startWRSpeed(${level})">🔄 Try Again</button>
                        <button class="btn-primary" onclick="renderWordRecogPanel()">← Back</button>
                    </div>
                </div>
            </div>`;
            return;
        }

        const w = words[idx];
        // Generate options: 1 correct + 3 wrong from same level or adjacent levels
        let wrongPool = [];
        WORD_FIRST_DATA.forEach(l => {
            if (Math.abs(l.level - level) <= 2) {
                l.words.forEach(ww => { if (ww.word !== w.word) wrongPool.push(ww); });
            }
        });
        wrongPool = wrongPool.sort(() => Math.random() - 0.5).slice(0, 3);
        let options = [{ text: `${w.emoji} ${w.meaning}`, correct: true }];
        wrongPool.forEach(ww => options.push({ text: `${ww.emoji} ${ww.meaning}`, correct: false }));
        options = options.sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="renderWordRecogPanel()">← Back</button>
                <span>${idx + 1}/${words.length}</span>
                <span class="wr-timer" id="wrTimer">0.0s</span>
            </div>
            <div class="wr-speed-card">
                <span class="wr-speed-word">${w.word}</span>
                <div class="wr-speed-options" id="wrSpeedOpts">
                    ${options.map(o => `
                        <button class="wr-speed-option" data-correct="${o.correct}"
                                onclick="wrSpeedAnswer(this, ${o.correct})">
                            ${o.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        </div>`;

        // Update timer
        const timerEl = document.getElementById("wrTimer");
        const timerInterval = setInterval(() => {
            if (timerEl && document.contains(timerEl)) {
                timerEl.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
            } else { clearInterval(timerInterval); }
        }, 100);
    }

    window.wrSpeedAnswer = function(btn, isCorrect) {
        document.querySelectorAll("#wrSpeedOpts .wr-speed-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !isCorrect) b.classList.add("wrong-answer");
        });
        if (isCorrect) correct++;
        const w = words[idx];
        [...w.word].forEach(c => { markReadingResult(c, isCorrect); });
        setTimeout(() => { idx++; renderSpeedCard(); }, isCorrect ? 400 : 1200);
    };

    renderSpeedCard();
}

// --- Grand Speed Challenge: All learned words ---
function startWRChallenge() {
    const panel = document.getElementById("wordRecogPanel");
    // Collect all words from unlocked levels
    let allWords = [];
    WORD_FIRST_DATA.forEach(lvl => {
        const prog = getWRLevel(lvl.level);
        if (prog.unlocked && prog.wordsLearned > 0) {
            lvl.words.slice(0, prog.wordsLearned).forEach(w => allWords.push(w));
        }
    });
    if (allWords.length < 4) { renderWordRecogPanel(); return; }
    allWords = allWords.sort(() => Math.random() - 0.5).slice(0, 20);

    let idx = 0;
    let correct = 0;
    let startTime = Date.now();

    function renderChallengeCard() {
        if (idx >= allWords.length) {
            const elapsed = Date.now() - startTime;
            const pct = Math.round((correct / allWords.length) * 100);
            const avgMs = Math.round(elapsed / allWords.length);
            xp += correct * 5;
            saveProgress();
            panel.innerHTML = `<div class="wr-content">
                <div class="wr-complete">
                    <h3>${pct >= 95 ? '🏆 PERFECT RECOGNITION!' : pct >= 80 ? '🔥 Impressive!' : pct >= 60 ? '⚡ Good Progress!' : '💪 Keep Training!'}</h3>
                    <div class="wr-speed-stats">
                        <div class="wr-stat"><span class="wr-stat-num">${correct}/${allWords.length}</span><span>correct</span></div>
                        <div class="wr-stat"><span class="wr-stat-num">${(elapsed / 1000).toFixed(1)}s</span><span>total</span></div>
                        <div class="wr-stat"><span class="wr-stat-num">${avgMs}ms</span><span>avg/word</span></div>
                    </div>
                    <p class="wr-speed-tip">${avgMs < 2000 ? '🧠 Near-instant recognition — すごい！' : '💡 Target: under 2 seconds per word for fluent reading.'}</p>
                    <div class="wr-complete-actions">
                        <button class="wr-speed-btn" onclick="startWRChallenge()">🔄 Again</button>
                        <button class="btn-primary" onclick="renderWordRecogPanel()">← Back</button>
                    </div>
                </div>
            </div>`;
            return;
        }

        const w = allWords[idx];
        let wrongPool = allWords.filter(ww => ww.word !== w.word).sort(() => Math.random() - 0.5).slice(0, 3);
        if (wrongPool.length < 3) {
            WORD_FIRST_DATA.forEach(l => {
                l.words.forEach(ww => { if (ww.word !== w.word && wrongPool.length < 3) wrongPool.push(ww); });
            });
        }
        let options = [{ text: `${w.emoji} ${w.meaning}`, correct: true }];
        wrongPool.slice(0, 3).forEach(ww => options.push({ text: `${ww.emoji} ${ww.meaning}`, correct: false }));
        options = options.sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="wr-content">
            <div class="wr-learn-header">
                <button class="rw-back-btn" onclick="renderWordRecogPanel()">← Back</button>
                <span>${idx + 1}/${allWords.length}</span>
                <span class="wr-timer" id="wrTimer">0.0s</span>
            </div>
            <div class="wr-speed-card wr-challenge-card">
                <span class="wr-speed-word">${w.word}</span>
                <div class="wr-speed-options" id="wrChallengeOpts">
                    ${options.map(o => `
                        <button class="wr-speed-option" data-correct="${o.correct}"
                                onclick="wrChallengeAnswer(this, ${o.correct})">
                            ${o.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        </div>`;

        const timerEl = document.getElementById("wrTimer");
        const timerInterval = setInterval(() => {
            if (timerEl && document.contains(timerEl)) {
                timerEl.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
            } else { clearInterval(timerInterval); }
        }, 100);
    }

    window.wrChallengeAnswer = function(btn, isCorrect) {
        document.querySelectorAll("#wrChallengeOpts .wr-speed-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !isCorrect) b.classList.add("wrong-answer");
        });
        if (isCorrect) correct++;
        setTimeout(() => { idx++; renderChallengeCard(); }, isCorrect ? 400 : 1200);
    };

    renderChallengeCard();
}

// ============================================
// STUDY PLAN MODE — Research-Based 1-Month N5
// Implements: Leitner Box SRS, Daily Curriculum,
// Interleaving, Active Recall, Spaced Repetition
// ============================================

// --- Leitner Box SRS Engine ---
// Box 1: review every session (new/hard)
// Box 2: review every 2 days
// Box 3: review every 4 days
// Box 4: review every 7 days
// Box 5: review every 14 days (mastered)
const SRS_INTERVALS = [0, 1, 2, 4, 7, 14]; // days per box (box 0 = immediate, box 1..5)

let srsData = JSON.parse(localStorage.getItem("jcoach_srs") || "{}");
let studyPlanState = JSON.parse(localStorage.getItem("jcoach_studyplan") || '{"startDate":null,"currentDay":1}');

function saveSRS() {
    localStorage.setItem("jcoach_srs", JSON.stringify(srsData));
    localStorage.setItem("jcoach_studyplan", JSON.stringify(studyPlanState));
}

function getSRSCard(char) {
    if (!srsData[char]) {
        srsData[char] = { box: 0, lastReview: null, nextReview: null, correct: 0, wrong: 0 };
    }
    return srsData[char];
}

function srsPromote(char) {
    const card = getSRSCard(char);
    card.box = Math.min(card.box + 1, 5);
    card.correct++;
    card.lastReview = Date.now();
    card.nextReview = Date.now() + SRS_INTERVALS[card.box] * 86400000;
    saveSRS();
}

function srsDemote(char) {
    const card = getSRSCard(char);
    card.box = Math.max(card.box - 1, 0);
    card.wrong++;
    card.lastReview = Date.now();
    card.nextReview = Date.now() + SRS_INTERVALS[card.box] * 86400000;
    saveSRS();
}

function isDueForReview(char) {
    const card = getSRSCard(char);
    if (card.box === 0) return true; // New or Box 0 = always due
    if (!card.nextReview) return true;
    return Date.now() >= card.nextReview;
}

// --- 30-Day Curriculum ---
// Week 1 (Days 1-7): Hiragana — 5 chars/day + review
// Week 2 (Days 8-14): Hiragana dakuten/combo + Katakana start
// Week 3 (Days 15-21): Katakana complete + N5 Kanji start
// Week 4 (Days 22-30): Kanji + Vocabulary + Grammar
const STUDY_CURRICULUM = [
    // Week 1: Hiragana Foundation
    { day: 1,  label: "Vowels あいうえお",          new: { cat: "hiragana", group: "Vowels" },         review: [],                                                  tip: "Start with the 5 vowels — the building blocks of Japanese!" },
    { day: 2,  label: "K-row かきくけこ",            new: { cat: "hiragana", group: "K-row" },           review: ["hiragana:Vowels"],                                  tip: "Review yesterday's vowels first, then learn K-row." },
    { day: 3,  label: "S-row さしすせそ",            new: { cat: "hiragana", group: "S-row" },           review: ["hiragana:Vowels", "hiragana:K-row"],                tip: "し is 'shi' not 'si' — remember the fishhook! 🎣" },
    { day: 4,  label: "T-row たちつてと",            new: { cat: "hiragana", group: "T-row" },           review: ["hiragana:S-row"],                                   tip: "ち='chi', つ='tsu' — the irregular ones. Tsunami wave! 🌊" },
    { day: 5,  label: "N-row なにぬねの",            new: { cat: "hiragana", group: "N-row" },           review: ["hiragana:T-row", "hiragana:K-row"],                 tip: "Halfway through basic hiragana! がんばって！" },
    { day: 6,  label: "H-row はひふへほ",            new: { cat: "hiragana", group: "H-row" },           review: ["hiragana:N-row", "hiragana:S-row"],                 tip: "ふ='fu' (not 'hu'). Mt. Fuji! 🗻" },
    { day: 7,  label: "Review Day — Rows あ to は",  new: null,                                          review: ["hiragana:Vowels","hiragana:K-row","hiragana:S-row","hiragana:T-row","hiragana:N-row","hiragana:H-row"], tip: "No new characters today — deep review only. SRS at work!" },

    // Week 2: Complete Hiragana + Start Katakana
    { day: 8,  label: "M-row まみむめも",            new: { cat: "hiragana", group: "M-row" },           review: ["hiragana:H-row"],                                   tip: "め='me' means eye! 👁️ Look at the shape." },
    { day: 9,  label: "Y-row やゆよ + R-row",        new: { cat: "hiragana", group: "Y-row" },           review: ["hiragana:M-row", "hiragana:Vowels"],                tip: "Only 3 Y-row chars. Use spare time for R-row preview." },
    { day: 10, label: "R-row らりるれろ",            new: { cat: "hiragana", group: "R-row" },           review: ["hiragana:Y-row", "hiragana:T-row"],                 tip: "Japanese 'r' sounds between 'l' and 'r'. Practice aloud!" },
    { day: 11, label: "W-row + N わをん",            new: { cat: "hiragana", group: "W-row + N" },       review: ["hiragana:R-row", "hiragana:N-row"],                 tip: "All 46 basic hiragana complete after today! 🎉" },
    { day: 12, label: "Dakuten G-row がぎぐげご",    new: { cat: "hiragana", group: "Dakuten (G)" },     review: ["hiragana:W-row + N", "hiragana:K-row"],             tip: "Dakuten ゛ makes K→G. か→が, き→ぎ. Easy pattern!" },
    { day: 13, label: "Dakuten Z/D ざじずぜぞ etc",  new: { cat: "hiragana", group: "Dakuten (Z)" },     review: ["hiragana:Dakuten (G)", "hiragana:S-row"],           tip: "S→Z with dakuten, T→D with dakuten. Pattern!" },
    { day: 14, label: "Full Hiragana Review",         new: null,                                          review: ["hiragana:Vowels","hiragana:K-row","hiragana:S-row","hiragana:T-row","hiragana:N-row","hiragana:H-row","hiragana:M-row","hiragana:Y-row","hiragana:R-row","hiragana:W-row + N","hiragana:Dakuten (G)","hiragana:Dakuten (Z)"], tip: "Major milestone review! You should know all hiragana by now." },

    // Week 3: Katakana + Early Kanji
    { day: 15, label: "Katakana Vowels アイウエオ",   new: { cat: "katakana", group: "Vowels" },          review: ["hiragana:Dakuten (B)", "hiragana:Handakuten (P)"],  tip: "Same sounds as hiragana, sharper strokes. あ↔ア" },
    { day: 16, label: "Katakana K+S row",             new: { cat: "katakana", group: "K-row" },           review: ["katakana:Vowels", "hiragana:Dakuten (D)"],          tip: "カ vs か — katakana is angular, hiragana is curvy." },
    { day: 17, label: "Katakana T+N row",             new: { cat: "katakana", group: "T-row" },           review: ["katakana:K-row"],                                   tip: "Watch out: シ vs ツ, ソ vs ン — the infamous pairs!" },
    { day: 18, label: "Katakana H+M row",             new: { cat: "katakana", group: "H-row" },           review: ["katakana:T-row", "katakana:Vowels"],                tip: "フ='fu' — same sound as ふ but different shape." },
    { day: 19, label: "Katakana Y+R+W row",           new: { cat: "katakana", group: "R-row" },           review: ["katakana:H-row"],                                   tip: "Almost done with katakana! ラリルレロ" },
    { day: 20, label: "N5 Kanji: Numbers 1-10",       new: { cat: "kanji", group: "Numbers" },            review: ["katakana:R-row", "katakana:K-row"],                 tip: "一二三 = 1,2,3 — the simplest kanji! Start strong." },
    { day: 21, label: "Review: Katakana + Numbers",    new: null,                                          review: ["katakana:Vowels","katakana:K-row","katakana:T-row","katakana:H-row","katakana:R-row","kanji:Numbers"], tip: "Interleaving review: mix katakana and kanji together!" },

    // Week 4: Kanji + Grammar + Vocabulary
    { day: 22, label: "Kanji: Time & Calendar",       new: { cat: "kanji", group: "Time & Calendar" },    review: ["kanji:Numbers"],                                     tip: "日月火水木金土 = days of the week! Very useful." },
    { day: 23, label: "Kanji: People & Body",         new: { cat: "kanji", group: "People & Body" },      review: ["kanji:Time & Calendar"],                             tip: "人=person, 男=man, 女=woman. Essential kanji!" },
    { day: 24, label: "Grammar: です/は/か/の",        new: { cat: "grammar", group: "patterns" },          review: ["kanji:People & Body", "kanji:Numbers"],              tip: "Core grammar particles — the glue of Japanese!" },
    { day: 25, label: "Vocab: Greetings & Daily",     new: { cat: "dailyWords", group: "Greetings" },     review: ["kanji:Time & Calendar"],                             tip: "おはようございます! Real words you'll use at NSK." },
    { day: 26, label: "Vocab: Common Verbs",          new: { cat: "dailyWords", group: "Common Verbs" },  review: ["kanji:People & Body"],                               tip: "たべます, のみます, いきます — daily action words!" },
    { day: 27, label: "Vocab: Time & Adjectives",     new: { cat: "dailyWords", group: "Time & Frequency" }, review: ["kanji:Numbers", "kanji:Time & Calendar"],         tip: "きょう, あした, いま — time words for daily life." },
    { day: 28, label: "Mixed Review: All Kanji",      new: null,                                          review: ["kanji:Numbers","kanji:Time & Calendar","kanji:People & Body"], tip: "Interleaved kanji review — the research says this works best!" },
    { day: 29, label: "Final Review: Hiragana+Kata",  new: null,                                          review: ["hiragana:Vowels","hiragana:K-row","hiragana:S-row","hiragana:T-row","hiragana:N-row","hiragana:H-row","hiragana:M-row","katakana:Vowels","katakana:K-row","katakana:T-row"], tip: "One month almost done! Deep review of everything." },
    { day: 30, label: "Month 1 Final Assessment",     new: null,                                          review: [],                                                    tip: "Take the N5 Practice Test to measure your progress! 🏆", isTest: true },
];

function getStudyDay() {
    if (!studyPlanState.startDate) return 0;
    const start = new Date(studyPlanState.startDate);
    start.setHours(0, 0, 0, 0);
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    return Math.floor((now - start) / 86400000) + 1;
}

function startStudyPlan() {
    studyPlanState.startDate = new Date().toISOString();
    studyPlanState.currentDay = 1;
    saveSRS();
    renderStudyPlanPanel();
}

function getDueItems() {
    const due = [];
    Object.entries(srsData).forEach(([char, card]) => {
        if (isDueForReview(char)) due.push({ char, ...card });
    });
    return due.sort((a, b) => a.box - b.box); // Prioritize lower boxes
}

function getItemsForGroup(cat, groupName) {
    if (cat === "grammar") {
        return KANA_DATA.grammar.patterns.map(p => ({
            char: p.pattern, romaji: p.id, meaning: p.meaning,
            example: p.example, exampleEn: p.exampleEn
        }));
    }
    const catData = KANA_DATA[cat];
    if (!catData) return [];
    const group = catData.groups.find(g => g.name === groupName);
    if (!group) return [];
    return (group.chars || group.words || []).map(item => ({
        char: item.char || item.word,
        romaji: item.romaji,
        meaning: item.meaning || "",
        hint: item.hint || "",
        onyomi: item.onyomi || "",
        kunyomi: item.kunyomi || "",
    }));
}

function renderStudyPlanPanel() {
    const panel = document.getElementById("studyPlanPanel");
    if (!panel) return;

    // Not started yet
    if (!studyPlanState.startDate) {
        panel.innerHTML = `<div class="sp-content">
            <div class="sp-hero">
                <h2>📅 1-Month N5 Study Plan</h2>
                <p class="sp-subtitle">A research-based 30-day curriculum using proven methods:</p>
                <div class="sp-methods">
                    <div class="sp-method-card">
                        <span class="sp-method-icon">📦</span>
                        <strong>Leitner Box SRS</strong>
                        <span>5-box spaced repetition — review at expanding intervals</span>
                    </div>
                    <div class="sp-method-card">
                        <span class="sp-method-icon">🧠</span>
                        <strong>Active Recall</strong>
                        <span>Quiz yourself before seeing answers — struggle = memory</span>
                    </div>
                    <div class="sp-method-card">
                        <span class="sp-method-icon">🔀</span>
                        <strong>Interleaving</strong>
                        <span>Mix reading, writing & grammar in each session</span>
                    </div>
                    <div class="sp-method-card">
                        <span class="sp-method-icon">🎭</span>
                        <strong>Mnemonics</strong>
                        <span>Visual stories for each character — Heisig-inspired</span>
                    </div>
                    <div class="sp-method-card">
                        <span class="sp-method-icon">📈</span>
                        <strong>i+1 Progression</strong>
                        <span>Each day builds on previous knowledge (Krashen)</span>
                    </div>
                    <div class="sp-method-card">
                        <span class="sp-method-icon">5️⃣</span>
                        <strong>Rule of 5</strong>
                        <span>See each character in 5 contexts before it sticks</span>
                    </div>
                </div>
                <div class="sp-plan-preview">
                    <h3>30-Day Roadmap</h3>
                    <div class="sp-roadmap">
                        <div class="sp-week"><strong>Week 1</strong> Hiragana basics (あ→は rows)</div>
                        <div class="sp-week"><strong>Week 2</strong> Hiragana complete + dakuten</div>
                        <div class="sp-week"><strong>Week 3</strong> Katakana + first kanji</div>
                        <div class="sp-week"><strong>Week 4</strong> Kanji + grammar + vocabulary</div>
                    </div>
                    <p class="sp-time">⏱️ ~20-30 minutes per day</p>
                </div>
                <button class="btn-primary sp-start-btn" onclick="startStudyPlan()">🚀 Start 30-Day Plan</button>
            </div>
        </div>`;
        return;
    }

    const today = getStudyDay();
    const dayData = STUDY_CURRICULUM.find(d => d.day === Math.min(today, 30)) || STUDY_CURRICULUM[STUDY_CURRICULUM.length - 1];

    // Calculate SRS stats
    const totalCards = Object.keys(srsData).length;
    const boxCounts = [0, 0, 0, 0, 0, 0];
    Object.values(srsData).forEach(c => boxCounts[c.box]++);
    const dueCount = getDueItems().length;
    const masteredCount = boxCounts[4] + boxCounts[5];

    // Completion status per day
    const completedDays = JSON.parse(localStorage.getItem("jcoach_sp_completed") || "[]");

    panel.innerHTML = `<div class="sp-content">
        <h2 class="sp-title">📅 Day ${Math.min(today, 30)} of 30</h2>
        <p class="sp-day-label">${dayData.label}</p>

        <!-- SRS Box Visualization -->
        <div class="sp-srs-boxes">
            <h3>Leitner Boxes</h3>
            <div class="sp-boxes-row">
                ${boxCounts.map((count, i) => `
                    <div class="sp-box ${i === 0 ? 'box-new' : ''} ${i >= 4 ? 'box-mastered' : ''}">
                        <span class="sp-box-num">${count}</span>
                        <span class="sp-box-label">${['New','1d','2d','4d','7d','14d'][i]}</span>
                    </div>
                `).join("")}
            </div>
            <div class="sp-srs-summary">
                <span>${totalCards} total cards</span>
                <span class="sp-due">${dueCount} due for review</span>
                <span>${masteredCount} mastered</span>
            </div>
        </div>

        <!-- Today's Tip -->
        <div class="sp-tip">
            <span class="sp-tip-icon">💡</span>
            <span>${dayData.tip}</span>
        </div>

        <!-- Today's Actions -->
        <div class="sp-actions">
            ${dayData.isTest ? `
                <button class="btn-primary sp-action-btn" onclick="switchMode('jlpt')">
                    🏆 Take N5 Practice Test
                </button>
            ` : `
                ${dayData.new ? `
                    <button class="btn-primary sp-action-btn sp-new-btn" onclick="startSRSLearn('${dayData.new.cat}','${dayData.new.group}')">
                        📖 Learn New: ${dayData.new.group}
                    </button>
                ` : ''}
                ${dueCount > 0 ? `
                    <button class="btn-primary sp-action-btn sp-review-btn" onclick="startSRSReview()">
                        🧠 Review Due Cards (${dueCount})
                    </button>
                ` : '<p class="sp-all-clear">✅ No cards due for review right now! Come back later.</p>'}
                ${dayData.review.length > 0 ? `
                    <button class="sp-action-btn sp-drill-btn" onclick="startSRSDayReview(${dayData.day})">
                        🔀 Today's Mixed Drill
                    </button>
                ` : ''}
            `}
        </div>

        <!-- Week Progress -->
        <div class="sp-week-progress">
            <h3>30-Day Progress</h3>
            <div class="sp-calendar">
                ${STUDY_CURRICULUM.map(d => {
                    const isDone = completedDays.includes(d.day);
                    const isToday = d.day === Math.min(today, 30);
                    const isPast = d.day < today;
                    const weekNum = Math.ceil(d.day / 7);
                    return `<div class="sp-cal-day ${isToday ? 'today' : ''} ${isDone ? 'done' : ''} ${isPast && !isDone ? 'missed' : ''}"
                                 title="Day ${d.day}: ${d.label}">
                        <span>${d.day}</span>
                    </div>`;
                }).join("")}
            </div>
        </div>

        <!-- Reset -->
        <div class="sp-reset">
            <button class="sp-reset-btn" onclick="if(confirm('Reset study plan? SRS data will be kept.')){studyPlanState={startDate:null,currentDay:1};localStorage.removeItem('jcoach_sp_completed');saveSRS();renderStudyPlanPanel();}">
                Reset Plan
            </button>
        </div>
    </div>`;
}

// --- SRS Learn: Teach new items with flashcards + auto-add to SRS ---
function startSRSLearn(cat, groupName) {
    const items = getItemsForGroup(cat, groupName);
    if (!items.length) return;
    const panel = document.getElementById("studyPlanPanel");
    let idx = 0;
    let phase = "front";

    // Add all items to SRS as Box 0 (new)
    items.forEach(item => {
        if (!srsData[item.char]) {
            srsData[item.char] = { box: 0, lastReview: null, nextReview: null, correct: 0, wrong: 0, cat, group: groupName };
        }
    });
    saveSRS();

    function renderLearnCard() {
        const item = items[idx];
        const card = getSRSCard(item.char);
        const mn = (typeof MNEMONICS !== "undefined" && MNEMONICS[item.char]) || null;
        const isKanji = cat === "kanji";
        phase = "front";

        panel.innerHTML = `<div class="sp-content">
            <div class="sp-learn-header">
                <button class="rw-back-btn" onclick="markDayComplete();renderStudyPlanPanel()">← Back</button>
                <span>Learning ${idx + 1}/${items.length}</span>
                <span class="sp-box-badge">Box ${card.box}</span>
            </div>
            <div class="rw-flashcard sp-flashcard" id="srsCard">
                <div id="srsCardFront" class="rw-card-front">
                    <span class="rw-big-char">${item.char}</span>
                    <span class="rw-tap-hint">tap to reveal →</span>
                </div>
                <div id="srsCardBack" class="rw-card-back" style="display:none">
                    <span class="rw-romaji">${item.romaji}</span>
                    ${item.meaning ? `<span class="rw-meaning">${item.meaning}</span>` : ""}
                    ${mn ? `<div class="mn-story-small">💡 ${mn.visual} ${mn.story}</div>` : ""}
                    ${item.hint ? `<span class="rw-hint">${item.hint}</span>` : ""}
                    ${isKanji ? `<span class="rw-readings">ON: ${item.onyomi || "—"} | KUN: ${item.kunyomi || "—"}</span>` : ""}
                    <div class="sp-srs-buttons">
                        <button class="sp-srs-wrong" onclick="srsAnswerLearn('${item.char.replace(/'/g, "\\'")}', false)">❌ Hard</button>
                        <button class="sp-srs-right" onclick="srsAnswerLearn('${item.char.replace(/'/g, "\\'")}', true)">✅ Got it!</button>
                    </div>
                </div>
            </div>
            <div class="rw-nav-row">
                <button class="rw-speak-btn" onclick="speakJapanese('${item.char.replace(/'/g, "\\'")}')">🔊</button>
            </div>
        </div>`;

        document.getElementById("srsCard").onclick = (e) => {
            if (e.target.closest(".sp-srs-buttons")) return;
            if (phase === "front") {
                document.getElementById("srsCardFront").style.display = "none";
                document.getElementById("srsCardBack").style.display = "flex";
                phase = "back";
            }
        };
    }

    window.srsAnswerLearn = function(char, correct) {
        if (correct) { srsPromote(char); xp += 3; }
        else { srsDemote(char); }
        // Also update reading progress for integration
        markReadingResult(char, correct);
        saveProgress();
        idx++;
        if (idx < items.length) renderLearnCard();
        else {
            markDayComplete();
            panel.innerHTML = `<div class="sp-content">
                <div class="sp-learn-done">
                    <h3>🎉 New items learned!</h3>
                    <p>${items.length} characters added to your SRS. They'll appear in future reviews.</p>
                    <button class="btn-primary" onclick="renderStudyPlanPanel()">← Back to Plan</button>
                </div>
            </div>`;
        }
    };

    renderLearnCard();
}

// --- SRS Review: Quiz due cards using Active Recall ---
function startSRSReview() {
    const due = getDueItems();
    if (!due.length) { renderStudyPlanPanel(); return; }
    const panel = document.getElementById("studyPlanPanel");
    let idx = 0;
    let items = due.slice(0, 20); // Max 20 per session

    function renderReviewCard() {
        if (idx >= items.length) {
            markDayComplete();
            panel.innerHTML = `<div class="sp-content">
                <div class="sp-learn-done">
                    <h3>✅ Review complete!</h3>
                    <p>Reviewed ${items.length} cards. Come back when more are due!</p>
                    <button class="btn-primary" onclick="renderStudyPlanPanel()">← Back to Plan</button>
                </div>
            </div>`;
            return;
        }
        const item = items[idx];
        const allItems = getAllSRSItemData();
        const itemData = allItems.find(i => i.char === item.char) || { char: item.char, romaji: "?", meaning: "" };
        const mn = (typeof MNEMONICS !== "undefined" && MNEMONICS[item.char]) || null;
        const isKanji = itemData.onyomi || itemData.kunyomi;

        // Generate wrong options for multiple choice
        const others = allItems.filter(i => i.char !== item.char && i.romaji);
        const wrongPool = others.sort(() => Math.random() - 0.5).slice(0, 3);

        let options;
        if (isKanji || itemData.meaning) {
            options = [{ text: itemData.meaning || itemData.romaji, correct: true }];
            wrongPool.forEach(w => options.push({ text: w.meaning || w.romaji, correct: false }));
        } else {
            options = [{ text: itemData.romaji, correct: true }];
            wrongPool.forEach(w => options.push({ text: w.romaji, correct: false }));
        }
        options = options.slice(0, 4).sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="sp-content">
            <div class="sp-learn-header">
                <button class="rw-back-btn" onclick="renderStudyPlanPanel()">← Back</button>
                <span>Review ${idx + 1}/${items.length}</span>
                <span class="sp-box-badge">Box ${item.box}</span>
            </div>
            <div class="rw-quiz-card sp-quiz-card">
                <span class="rw-quiz-prompt">${item.char}</span>
                <div class="rw-quiz-options" id="srs-options">
                    ${options.map(o => `
                        <button class="rw-quiz-option" data-correct="${o.correct}"
                                onclick="srsReviewAnswer(this, ${o.correct}, '${item.char.replace(/'/g, "\\'")}')">
                            ${o.text}
                        </button>
                    `).join("")}
                </div>
                <div class="sp-review-hint" id="srsHint" style="display:none"></div>
            </div>
        </div>`;
    }

    window.srsReviewAnswer = function(btn, correct, char) {
        document.querySelectorAll("#srs-options .rw-quiz-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !correct) b.classList.add("wrong-answer");
        });

        const mn = (typeof MNEMONICS !== "undefined" && MNEMONICS[char]) || null;
        const hint = document.getElementById("srsHint");
        if (!correct && mn && hint) {
            hint.innerHTML = `<span class="mn-quiz-visual">${mn.visual}</span> ${mn.story}`;
            hint.style.display = "block";
        }

        if (correct) { srsPromote(char); xp += 5; markReadingResult(char, true); }
        else { srsDemote(char); markReadingResult(char, false); }
        saveProgress();

        setTimeout(() => { idx++; renderReviewCard(); }, correct ? 800 : 2000);
    };

    renderReviewCard();
}

// --- Mixed Drill for today's curriculum review groups ---
function startSRSDayReview(day) {
    const dayData = STUDY_CURRICULUM.find(d => d.day === day);
    if (!dayData || !dayData.review.length) return;

    // Collect all items from review groups
    let allItems = [];
    dayData.review.forEach(ref => {
        const [cat, group] = ref.split(":");
        const items = getItemsForGroup(cat, group);
        items.forEach(item => {
            // Only include items already in SRS
            if (srsData[item.char]) allItems.push(item);
        });
    });

    if (!allItems.length) {
        // If no SRS items yet, pull from the groups directly
        dayData.review.forEach(ref => {
            const [cat, group] = ref.split(":");
            allItems = allItems.concat(getItemsForGroup(cat, group));
        });
    }

    // Shuffle and limit
    allItems = allItems.sort(() => Math.random() - 0.5).slice(0, 15);
    if (!allItems.length) return;

    const panel = document.getElementById("studyPlanPanel");
    let idx = 0;
    let correct = 0;

    function renderDrillCard() {
        if (idx >= allItems.length) {
            markDayComplete();
            const pct = Math.round((correct / allItems.length) * 100);
            xp += correct * 3;
            saveProgress();
            panel.innerHTML = `<div class="sp-content">
                <div class="sp-learn-done">
                    <h3>${pct >= 80 ? '🎉 Excellent!' : pct >= 60 ? '👍 Good!' : '💪 Keep going!'}</h3>
                    <p>${correct}/${allItems.length} correct (${pct}%)</p>
                    <button class="btn-primary" onclick="renderStudyPlanPanel()">← Back to Plan</button>
                </div>
            </div>`;
            return;
        }

        const item = allItems[idx];
        const others = allItems.filter(i => i.char !== item.char);
        const wrongPool = others.sort(() => Math.random() - 0.5).slice(0, 3);

        let options;
        if (item.meaning) {
            options = [{ text: item.meaning, correct: true }];
            wrongPool.forEach(w => options.push({ text: w.meaning || w.romaji, correct: false }));
        } else {
            options = [{ text: item.romaji, correct: true }];
            wrongPool.forEach(w => options.push({ text: w.romaji, correct: false }));
        }
        options = options.slice(0, 4).sort(() => Math.random() - 0.5);

        panel.innerHTML = `<div class="sp-content">
            <div class="sp-learn-header">
                <button class="rw-back-btn" onclick="renderStudyPlanPanel()">← Back</button>
                <span>Drill ${idx + 1}/${allItems.length}</span>
                <span>✓ ${correct}</span>
            </div>
            <div class="rw-quiz-card sp-quiz-card">
                <span class="rw-quiz-prompt">${item.char}</span>
                <div class="rw-quiz-options" id="drill-options">
                    ${options.map(o => `
                        <button class="rw-quiz-option" data-correct="${o.correct}"
                                onclick="drillAnswer(this, ${o.correct}, '${item.char.replace(/'/g, "\\'")}')">
                            ${o.text}
                        </button>
                    `).join("")}
                </div>
            </div>
        </div>`;
    }

    window.drillAnswer = function(btn, isCorrect, char) {
        document.querySelectorAll("#drill-options .rw-quiz-option").forEach(b => {
            b.disabled = true;
            if (b.dataset.correct === "true") b.classList.add("correct-answer");
            if (b === btn && !isCorrect) b.classList.add("wrong-answer");
        });
        if (isCorrect) { correct++; srsPromote(char); }
        else { srsDemote(char); }
        markReadingResult(char, isCorrect);
        saveProgress();
        setTimeout(() => { idx++; renderDrillCard(); }, 1000);
    };

    renderDrillCard();
}

function getAllSRSItemData() {
    const all = [];
    ["hiragana", "katakana", "kanji", "dailyWords"].forEach(cat => {
        KANA_DATA[cat].groups.forEach(g => {
            (g.chars || g.words || []).forEach(item => {
                all.push({
                    char: item.char || item.word,
                    romaji: item.romaji,
                    meaning: item.meaning || "",
                    hint: item.hint || "",
                    onyomi: item.onyomi || "",
                    kunyomi: item.kunyomi || "",
                });
            });
        });
    });
    KANA_DATA.grammar.patterns.forEach(p => {
        all.push({ char: p.pattern, romaji: p.id, meaning: p.meaning });
    });
    return all;
}

function markDayComplete() {
    const today = Math.min(getStudyDay(), 30);
    let completed = JSON.parse(localStorage.getItem("jcoach_sp_completed") || "[]");
    if (!completed.includes(today)) {
        completed.push(today);
        localStorage.setItem("jcoach_sp_completed", JSON.stringify(completed));
        xp += 20; // Daily completion bonus
        saveProgress();
    }
}

// --- Start ---
document.addEventListener("DOMContentLoaded", init);
