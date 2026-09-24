"""Evidence decks: one full-screen deck per case, built in English and Indonesian.

A deck shows the result of a piece of work and the method behind it, in the same
presentation format I use at work. Text is bilingual inline as (english, indonesian),
the same convention powersync_page.py uses.

Every figure here also appears on the case study page it links to, and traces to a
verified evidence item. Where nothing was measured the deck says so instead of
estimating: the blind zone is part of the story.

Output: deck-<slug>.html in the repo root and id/deck-<slug>.html, plus the shared
assets/deck.css and assets/deck.js.
"""
import html
import json
import os

E = html.escape

# --------------------------------------------------------------------------- data

DIGITAL_GROWTH = {
    "slug": "digital-growth",
    "case": "work-digital-growth.html",
    "product": ("PowerAce Digital Growth", "PowerAce Digital Growth"),
    "period": ("Jul–Sep 2026", "Jul–Sep 2026"),
    "title": (
        "Our adverts brought people in. What happened next was <em>ours to fix</em>.",
        "Iklan kami mendatangkan orang. Yang terjadi setelahnya <em>ada di tangan kami</em>.",
    ),
    "lead": (
        "I ran a click-to-WhatsApp campaign, then read one full week of conversations one by one "
        "to find out where they stopped.",
        "Saya menjalankan kampanye click-to-WhatsApp, lalu membaca percakapan selama satu pekan penuh "
        "satu per satu untuk tahu di mana percakapan berhenti.",
    ),
    "slides": (
        ["Result", "Journey", "Method", "Not tracked"],
        ["Hasil", "Journey", "Metode", "Belum terlacak"],
    ),
    # one tracked week, from the case study
    "week": {"total": 328, "continued": 244, "no_reply": 54, "no_dealer": 30},
}


# --------------------------------------------------------------------------- render


def build(b, deck=DIGITAL_GROWTH):
    lang = b.LANG
    P = b.P

    def L(pair):
        return pair[0] if lang == "en" else pair[1]

    def LE(pair):
        return E(L(pair))

    w = deck["week"]
    pct = lambda n: str(round(100 * n / w["total"])) + "%"

    # ------------------------------------------------------------- shared pieces
    sep = "," if lang == "en" else "."

    def num(value, prefix="", suffix=""):
        """A figure that counts up when its slide opens."""
        return (f'<span data-count="{value}" data-sep="{sep}"'
                f'{f" data-prefix={prefix!r}" if prefix else ""}'
                f'{f" data-suffix={suffix!r}" if suffix else ""}>0</span>')

    def title(text, note, audience, step):
        dots = "".join(
            f'<span class="{"on" if i <= step else ""}"></span>' for i in range(4)
        )
        return f"""<div class="d-title d-rv">
    <div>
      <div class="d-audience"><i></i>{LE(audience)}<span class="d-depth">{dots}</span></div>
      <h2 style="margin-top:9px">{L(text)}</h2>
    </div>
    <p>{LE(note)}</p>
  </div>"""

    # ------------------------------------------------------------- slide 1
    xyz = [
        (("X", "X"), ("What I did", "Yang saya kerjakan"),
         ("Took the company website back from the vendor and connected our adverts to "
          "<b>real conversations with dealers</b>.",
          "Mengambil alih website perusahaan dari vendor dan menghubungkan iklan kami ke "
          "<b>percakapan nyata dengan dealer</b>.")),
        (("Y", "Y"), ("Measured by", "Diukur dengan"),
         ("<b>344 conversations</b> for IDR 1.44 million — about <b>IDR 4,200 each</b> — and in one "
          "tracked week <b>84 of every 100</b> conversations got an answer.",
          "<b>344 percakapan</b> dengan biaya Rp1,44 juta — sekitar <b>Rp4.200 per percakapan</b> — dan "
          "dalam satu pekan terlacak <b>84 dari 100</b> percakapan mendapat jawaban.")),
        (("Z", "Z"), ("By doing", "Dengan cara"),
         ("Rebuilding the site in-house, tagging every click, then <b>reading a full week of "
          "conversations one by one</b> to see where they stopped.",
          "Membangun ulang website secara internal, menandai setiap klik, lalu <b>membaca percakapan "
          "satu pekan penuh satu per satu</b> untuk melihat di mana berhentinya.")),
    ]
    xyz_html = "".join(
        f"""<div class="d-xyz-line"><div class="d-xyz-tag"><b>{LE(letter)}</b><span>{LE(tag)}</span></div>
      <p>{L(body)}</p></div>"""
        for letter, tag, body in xyz
    )

    figures = [
        (num(344), ("conversations with buyers", "percakapan dengan calon pembeli"),
         ("from the advert campaign", "dari kampanye iklan")),
        (num(4200, prefix="IDR " if lang == "en" else "Rp"),
         ("spent per conversation", "biaya per percakapan"),
         ("IDR 1.44 million in total", "total Rp1,44 juta")),
        (num(84, suffix="%"), ("of them got an answer", "di antaranya mendapat jawaban"),
         ("in the week I checked", "pada pekan yang saya periksa")),
    ]
    figure_html = "".join(
        f"""<div style="display:flex;align-items:baseline;gap:14px">
      <div class="d-big" style="font-size:44px;min-width:170px">{value}</div>
      <div><p style="font-size:15px;font-weight:700;letter-spacing:-.02em">{LE(label)}</p>
      <p class="d-sub" style="font-size:12.5px">{LE(sub)}</p></div>
    </div>"""
        for value, label, sub in figures
    )

    platform_html = "".join(
        f'<div><div class="d-big" style="font-size:26px">{LE(v)}</div>'
        f'<p class="d-sub" style="font-size:12px">{LE(l)}</p></div>'
        for v, l in [
            (("28 → 78", "28 → 78"), ("security score, checked by me", "skor keamanan, saya nilai sendiri")),
            (("85", "85"), ("redirects kept visitors", "redirect menjaga pengunjung")),
            (("73/100", "73/100"), ("SEO health, new homepage", "skor SEO homepage baru")),
            (("2 + 3", "2 + 3"), ("High and Medium alerts on the old site",
                                  "peringatan High dan Medium di website lama")),
        ]
    )

    slide1 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1.45fr) minmax(0,.78fr)">
  {title(deck['title'], deck['lead'], ("The short version · for anyone", "Versi singkat · untuk siapa saja"), 0)}
  <div class="d-card d-rv" style="--d:80;grid-column:span 8">
    <div class="d-head"><div><div class="d-kk">{LE(("Result, in one sentence", "Hasil, dalam satu kalimat"))}</div>
      <h3>{LE(("Adverts in, answered conversations out", "Iklan masuk, percakapan terjawab keluar"))}</h3></div>
      <div class="d-chips"><span class="d-chip bl">{LE(("Jul–Sep 2026", "Jul–Sep 2026"))}</span></div></div>
    <div class="d-xyz">{xyz_html}</div>
  </div>
  <div class="d-card d-rv" style="--d:220;grid-column:span 4;justify-content:space-evenly">{figure_html}</div>
  <div class="d-card d-rv" style="--d:320;grid-column:span 8">
    <div class="d-kk">{LE(("In plain terms", "Dengan kata sederhana"))}</div>
    <p class="d-plain">{L((
      "Adverts brought people to WhatsApp. <b>I checked what happened to every one of them for a week</b> — "
      "who got an answer, who was ignored, and who lived where we had no dealer. "
      "The next slides show that week, how I worked through it, and what I still cannot prove.",
      "Iklan membawa orang ke WhatsApp. <b>Saya memeriksa apa yang terjadi pada setiap orang selama sepekan</b> — "
      "siapa yang dijawab, siapa yang diabaikan, dan siapa yang tinggal di area tanpa dealer kami. "
      "Slide berikutnya menunjukkan pekan itu, cara saya mengerjakannya, dan apa yang belum bisa saya buktikan."))}</p>
  </div>
  <div class="d-card d-rv" style="--d:400;grid-column:span 4">
    <div class="d-kk">{LE(("Before any of that could be measured", "Sebelum semua itu bisa diukur"))}</div>
    <div class="d-split" style="flex-wrap:wrap;gap:14px 20px">{platform_html}</div>
    <p class="d-note">{LE((
      "A vendor held the old site. We rebuilt it in-house, and those alerts no longer appear on the new stack.",
      "Website lama dipegang vendor. Kami bangun ulang sendiri, dan peringatan itu tidak lagi muncul di sistem baru."))}</p>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 2 (sankey)
    scale, top, gap = 1.2, 46, 18
    h_cont, h_nore, h_node = (round(w[k] * scale) for k in ("continued", "no_reply", "no_dealer"))
    spec = {
        "width": 1430, "height": 520, "nodeWidth": 13, "scale": scale, "minHeight": 5,
        "colors": {"in": "#355c7d", "ok": "#4a7d63", "leak": "#9a5a4a"},
        "labelColors": {"in": "#20272d", "ok": "#20272d", "leak": "#9a5a4a", "blind": "#8a949d"},
        "linkOpacity": 0.38,
        "nodes": [
            {"id": "all", "type": "in", "x": 210, "y": top, "value": w["total"], "side": "left",
             "big": 34, "label": L(("conversations", "percakapan")),
             "sub": L(("one tracked week", "satu pekan terlacak"))},
            {"id": "cont", "type": "ok", "x": 700, "y": top, "value": w["continued"],
             "label": L(("answered and kept talking", "dijawab dan percakapan berlanjut")),
             "sub": pct(w["continued"])},
            {"id": "nore", "type": "leak", "x": 700, "y": top + h_cont + gap, "value": w["no_reply"],
             "label": L(("nobody ever replied to them", "tidak pernah dibalas siapa pun")),
             "sub": pct(w["no_reply"]) + L((" · internal", " · internal"))},
            {"id": "node", "type": "leak", "x": 700, "y": top + h_cont + h_nore + 2 * gap, "value": w["no_dealer"],
             "label": L(("live where we have no dealer", "tinggal di area tanpa dealer kami")),
             "sub": pct(w["no_dealer"]) + L((" · coverage gap", " · celah coverage"))},
            {"id": "spk", "type": "blind", "x": 1150, "y": top, "value": w["continued"], "display": "?",
             "big": 34, "label": L(("did they buy?", "apakah mereka membeli?")),
             "sub": L(("nobody tracked this yet", "belum ada yang melacaknya"))},
        ],
        "notes": [{"x": 975, "y": 150, "size": 14,
                   "text": L(("nothing measured past the hand-off",
                              "tak ada yang terukur setelah serah terima"))}],
        "dotRadius": 3,
        "links": [
            {"s": "all", "t": "cont", "value": w["continued"], "flow": 9},
            {"s": "all", "t": "nore", "value": w["no_reply"], "flow": 3},
            {"s": "all", "t": "node", "value": w["no_dealer"], "flow": 2},
            {"s": "cont", "t": "spk", "value": w["continued"], "blind": True},
        ],
    }

    slide2 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr)">
  {title(("The journey stops where <em>we</em> stop it", "Journey berhenti di tempat <em>kami</em> menghentikannya"),
         ("Each ribbon is a group of real conversations. The wider the ribbon, the more people it holds.",
          "Setiap pita adalah sekelompok percakapan nyata. Makin lebar pita, makin banyak orangnya."),
         ("What actually happened · one week, all 328", "Apa yang sebenarnya terjadi · satu pekan, 328 percakapan"), 1)}
  <div class="d-card d-rv" style="--d:120;grid-column:span 12">
    <div class="d-head"><div><div class="d-kk">{LE(("Customer journey · one tracked week", "Customer journey · satu pekan terlacak"))}</div>
      <h3>{LE(("From conversation to the edge of the data", "Dari percakapan sampai batas data"))}</h3></div>
      <div class="d-chips"><span class="d-chip bl">{LE(("84% answered", "84% dibalas"))}</span>
        <span class="d-chip wn">{LE(("26% lost before a dealer", "26% hilang sebelum dealer"))}</span>
        <span class="d-chip">{LE(("hatched = no data", "arsir = tidak ada data"))}</span></div></div>
    <div class="d-sankey" data-sankey="{E(json.dumps(spec), quote=True)}"></div>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 3 (method)
    outputs = [
        ("One week of conversations, joined to spend and area",
         "Satu pekan percakapan, digabung dengan biaya dan area"),
        ("Four leak types, counted, not guessed",
         "Empat tipe kebocoran, dihitung, bukan ditebak"),
        ("A requirement, a brief, and an honest list of gaps",
         "Sebuah requirement, sebuah brief, dan daftar jujur yang belum ada"),
    ]
    method = [
        (("Collect", "Kumpulkan"), ("What the funnel is made of", "Bahan baku funnel"), [
            ("Tag every WhatsApp click with GTM and GA4 events", "Tandai setiap klik WhatsApp dengan event GTM dan GA4"),
            ("Export ad spend and reach per post from Meta Ads", "Ekspor biaya dan jangkauan iklan per post dari Meta Ads"),
            ("Export the WhatsApp conversations for the same period", "Ekspor percakapan WhatsApp untuk periode yang sama"),
            ("List which areas an active dealer actually covers", "Daftar area yang benar-benar dicakup dealer aktif"),
        ]),
        (("Read", "Baca"), ("One week, conversation by conversation", "Satu pekan, percakapan per percakapan"), [
            ("Read all 328 conversations instead of sampling", "Baca seluruh 328 percakapan, bukan sampling"),
            ("Tag each one with what stopped it", "Tandai setiap percakapan dengan penyebab berhentinya"),
            ("Group the tags into leak types that repeat", "Kelompokkan tag jadi tipe kebocoran yang berulang"),
            ("Separate what we control from what we don't", "Pisahkan yang kami kendalikan dari yang tidak"),
        ]),
        (("Hand over", "Serahkan"), ("So it becomes someone's job", "Supaya jadi tanggung jawab seseorang"), [
            ("Write each leak type as a requirement with a rule", "Tulis tiap tipe kebocoran jadi requirement dengan aturannya"),
            ("Brief an AI follow-up draft that a person approves", "Susun brief draft follow-up AI yang tetap disetujui manusia"),
            ("Make dealer coverage a check before ad spend", "Jadikan coverage dealer syarat sebelum belanja iklan"),
            ("State plainly what is still not tracked", "Nyatakan terus terang apa yang masih belum terlacak"),
        ]),
    ]
    method_cards = "".join(
        f"""<div class="d-card d-rv" style="--d:{120 + i * 90};grid-column:span 4">
      <div class="d-head"><div><div class="d-kk">{LE(("Step", "Langkah"))} {i + 1}</div><h3>{LE(name)}</h3></div></div>
      <p class="d-sub">{LE(sub)}</p>
      <ul class="d-steps">{''.join(f'<li><b>{n + 1:02d}</b><span>{LE(s)}</span></li>' for n, s in enumerate(steps))}</ul>
      <p class="d-note" style="margin-top:auto;border-top:1px solid var(--d-line);padding-top:11px">
        <b>{LE(("Output", "Hasil"))}:</b> {LE(outputs[i])}</p>
    </div>"""
        for i, (name, sub, steps) in enumerate(method)
    )

    domains = [
        (True, ("Business analysis", "Business analysis"), ("Core", "Inti"),
         ("Turn the leaks into requirements and rules a system can apply.",
          "Ubah kebocoran jadi requirement dan aturan yang bisa dijalankan sistem.")),
        (False, ("Market research & data", "Market research & data"), ("Support", "Pendukung"),
         ("Collect the funnel data and read it without sampling.",
          "Kumpulkan data funnel dan baca tanpa sampling.")),
        (False, ("AI orchestration", "AI orchestration"), ("Support", "Pendukung"),
         ("Draft the follow-up; a person still approves every reply.",
          "Susun draft follow-up; setiap balasan tetap disetujui manusia.")),
        (False, ("Operations digitalization", "Operations digitalization"), ("Support", "Pendukung"),
         ("The dealer side of the funnel runs in PowerSync.",
          "Sisi dealer dari funnel berjalan di PowerSync.")),
    ]
    domain_html = "".join(
        f"""<div class="d-domain{' core' if core else ''}"><span>{LE(role)}</span>
      <strong>{LE(name)}</strong><em>{LE(note)}</em></div>"""
        for core, name, role, note in domains
    )

    slide3 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr) auto">
  {title(("How I deliver it: <em>collect, read, hand over</em>", "Cara saya mengerjakannya: <em>kumpulkan, baca, serahkan</em>"),
         ("The same three steps on every project. The reading step is the one people skip.",
          "Tiga langkah yang sama di setiap project. Langkah membaca adalah yang biasanya dilewati."),
         ("How I work · the method", "Cara saya bekerja · metodenya"), 2)}
  {method_cards}
  <div class="d-card d-rv" style="--d:420;grid-column:span 12;padding:18px 20px">
    <div class="d-head"><div class="d-kk">{LE(("Which part of my work does what", "Bagian mana dari pekerjaan saya yang berperan"))}</div></div>
    <div class="d-domains">{domain_html}</div>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 4
    blind = [
        (("SPK and closing", "SPK dan closing"),
         ("No pipeline stage exists yet, so no conversation is followed to a sale.",
          "Belum ada tahap pipeline-nya, jadi tidak ada percakapan yang diikuti sampai penjualan.")),
        (("Cost per SPK", "Biaya per SPK"),
         ("Cost per conversation is known; cost per sale cannot be derived from it.",
          "Biaya per percakapan diketahui; biaya per penjualan tidak bisa diturunkan dari situ.")),
        (("Ranking gains from the content plan", "Kenaikan ranking dari rencana konten"),
         ("The plan shipped in Aug 2026. Nothing has been measured yet.",
          "Rencananya rilis Agu 2026. Belum ada yang diukur.")),
        (("Deals won from the campaign", "Deal yang menang dari kampanye"),
         ("The funnel is not tracked through to a closed sale.",
          "Funnel belum terlacak sampai penjualan yang tutup.")),
    ]
    blind_html = "".join(
        f'<li><code>{LE(("no data", "tidak ada data"))}</code><span><b>{LE(name)}</b> — {LE(note)}</span></li>'
        for name, note in blind
    )
    nexts = [
        ("Add conversation, qualified lead, dealer hand-off and SPK as stages in PowerSync",
         "Tambahkan percakapan, lead terkualifikasi, serah terima dealer, dan SPK sebagai tahap di PowerSync"),
        ("Give every stage one owner and one response target",
         "Beri setiap tahap satu penanggung jawab dan satu target respons"),
        ("Review the leak types weekly, with the same tags",
         "Tinjau tipe kebocoran setiap pekan, dengan tag yang sama"),
        ("Only then report a cost per sale",
         "Baru setelah itu laporkan biaya per penjualan"),
    ]
    supported = [
        (("344", "344"), ("conversations, IDR 1.44m spent", "percakapan, biaya Rp1,44 juta")),
        (("328", "328"), ("read one by one in one week", "dibaca satu per satu dalam sepekan")),
        (("84", "84"), ("of the 328 got a reply", "dari 328 itu mendapat balasan")),
    ]
    supported_html = "".join(
        f'<div><div class="d-big" style="font-size:26px">{LE(v)}{"%" if v[0] == "84" else ""}</div>'
        f'<p class="d-sub" style="font-size:12.5px">{LE(l)}</p></div>'
        for v, l in supported
    )
    codes = ["BA02-E01", "BA02-E03", "BA02-E04", "BA02-E05", "BA02-E06",
             "BA02-E07", "BA02-E08", "BA02-E10", "BA02-E11", "BA02-E13"]

    slide4 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr)">
  {title(("What I <em>don't</em> claim, and what I'd build next", "Yang <em>tidak</em> saya klaim, dan yang akan saya bangun berikutnya"),
         ("A funnel deck is easy to inflate. These are the figures that do not exist yet.",
          "Deck funnel mudah dilebih-lebihkan. Ini angka-angka yang memang belum ada."),
         ("What I don't claim · the fine print", "Yang tidak saya klaim · catatan jujurnya"), 3)}
  <div class="d-card d-rv" style="--d:120;grid-column:span 7">
    <div class="d-head"><div><div class="d-kk">{LE(("Blind zone", "Zona buta"))}</div>
      <h3>{LE(("Measured nowhere, so claimed nowhere", "Tidak terukur di mana pun, jadi tidak diklaim di mana pun"))}</h3></div></div>
    <ul class="d-list">{blind_html}</ul>
    <div style="border-top:1px solid var(--d-line);padding-top:14px;margin-top:auto">
      <div class="d-kk" style="margin-bottom:9px">{LE(("What the data does support", "Yang didukung data"))}</div>
      <div class="d-split">{supported_html}</div>
    </div>
  </div>
  <div style="grid-column:span 5;display:flex;flex-direction:column;gap:16px;min-height:0">
    <div class="d-card dark d-rv" style="--d:200;flex:1">
      <div class="d-kk">{LE(("Next", "Berikutnya"))}</div>
      <h3>{LE(("Build the pipeline before buying more reach", "Bangun pipeline sebelum membeli lebih banyak jangkauan"))}</h3>
      <ul class="d-steps" style="margin-top:2px">
        {''.join(f'<li style="background:#2b3d4d;color:#fff"><b style="color:#9fc0dd">{i + 1:02d}</b><span>{LE(s)}</span></li>' for i, s in enumerate(nexts))}
      </ul>
      <p class="d-note" style="color:#9fc0dd;margin-top:auto">{LE((
        "Reach is easy to buy. A pipeline is what turns it into a number worth reporting.",
        "Jangkauan mudah dibeli. Pipeline-lah yang mengubahnya jadi angka yang layak dilaporkan."))}</p>
    </div>
    <div class="d-card d-rv" style="--d:280">
      <div class="d-kk">{LE(("Evidence behind every figure", "Bukti di balik setiap angka"))}</div>
      <div class="d-codes">{''.join(f'<span>{c}</span>' for c in codes)}</div>
      <p class="d-note">{LE((
        "Internal company files. I walk through a sanitized version in an interview.",
        "Dokumen internal perusahaan. Saya menjelaskan versi yang disamarkan saat wawancara."))}</p>
      <a class="d-cta" href="{P}{deck['case']}">{LE(("Read the full case study", "Baca studi kasus lengkapnya"))} <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</div>"""

    slides = [slide1, slide2, slide3, slide4]
    names = L(deck["slides"])
    nav = "".join(f"<button type=\"button\">{E(n)}</button>" for n in names)
    slide_html = "".join(
        f'<section class="deck-slide" aria-label="{E(names[i])}">{s}</section>'
        for i, s in enumerate(slides)
    )

    # ------------------------------------------------------------- small screens
    flow_xyz = "".join(
        f"""<div class="d-xyz-line"><div class="d-xyz-tag" style="width:84px"><b>{LE(letter)}</b>
      <span>{LE(tag)}</span></div><p style="font-size:15.5px">{L(body)}</p></div>"""
        for letter, tag, body in xyz
    )
    week_rows = [
        (("Answered and kept talking", "Dijawab dan percakapan berlanjut"), w["continued"], ""),
        (("Nobody ever replied", "Tidak pernah dibalas"), w["no_reply"], "wn"),
        (("No dealer covering the area", "Tidak ada dealer di area itu"), w["no_dealer"], "wn"),
    ]
    flow_rows = "".join(
        f'<div class="d-row"><span style="flex:1">{LE(label)}</span>'
        f'<span class="num">{n}</span><span class="d-chip {"wn" if cls else "ok"}">{pct(n)}</span></div>'
        for label, n, cls in week_rows
    )
    flow_method = "".join(
        f"<h3 style=\"font-size:15px;font-weight:750;margin-top:6px\">{i + 1}. {LE(name)}</h3>"
        f"<ul class=\"d-steps\">{''.join(f'<li><b>{n + 1:02d}</b><span>{LE(s)}</span></li>' for n, s in enumerate(steps))}</ul>"
        for i, (name, sub, steps) in enumerate(method)
    )
    flow = f"""
<div class="deck-flow">
  <div class="f-head">
    <div class="d-kk">{LE(deck['product'])} · {LE(deck['period'])}</div>
    <h1>{L(deck['title'])}</h1>
    <p class="lead">{LE(deck['lead'])}</p>
  </div>
  <section>
    <h2>{LE(("The result", "Hasilnya"))}</h2>
    <div class="d-xyz">{flow_xyz}</div>
  </section>
  <section>
    <h2>{LE(("Where one tracked week went", "Ke mana satu pekan terlacak pergi"))}</h2>
    <p class="d-plain">{L((
      "Adverts brought people to WhatsApp. <b>I checked what happened to every one of them for a week.</b>",
      "Iklan membawa orang ke WhatsApp. <b>Saya memeriksa apa yang terjadi pada setiap orang selama sepekan.</b>"))}</p>
    <div class="d-rows">{flow_rows}</div>
    <p class="d-note">{LE((
      "Both losses are internal: how fast we answer, and where we placed dealers.",
      "Kedua kehilangan ini internal: secepat apa kami membalas, dan di mana dealer ditempatkan."))}</p>
  </section>
  <section>
    <h2>{LE(("How I deliver it", "Cara saya mengerjakannya"))}</h2>
    {flow_method}
  </section>
  <section>
    <h2>{LE(("Which part of my work does what", "Bagian mana dari pekerjaan saya yang berperan"))}</h2>
    <div class="d-domains" style="flex-direction:column">{domain_html}</div>
  </section>
  <section>
    <h2>{LE(("What I don't claim", "Yang tidak saya klaim"))}</h2>
    <ul class="d-list">{blind_html}</ul>
    <div class="d-codes">{''.join(f'<span>{c}</span>' for c in codes)}</div>
    <a class="d-cta" href="{P}{deck['case']}">{LE(("Read the full case study", "Baca studi kasus lengkapnya"))} <span aria-hidden="true">↗</span></a>
  </section>
  <footer>{LE((
    "This deck is built for a wide screen. On a phone you are reading the same figures in plain order.",
    "Deck ini dibuat untuk layar lebar. Di ponsel Anda membaca angka yang sama dalam urutan biasa."))}
    <a href="{P}index.html">{LE(("Back to the portfolio", "Kembali ke portofolio"))}</a></footer>
</div>"""

    filename = f"deck-{deck['slug']}.html"
    title = L(("Ad to dealer: where the funnel leaks", "Dari iklan ke dealer: di mana funnel bocor"))
    description = L(deck["lead"])
    en_url = b.SITE_URL + filename
    id_url = b.SITE_URL + "id/" + filename
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} · {E(b.PERSON['name'])}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{en_url if lang == 'en' else id_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="id" href="{id_url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:image" content="{b.SITE_URL}assets/img/og-card.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#dcdfe2">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;650;700;750;800&display=swap">
<link rel="stylesheet" href="{P}assets/deck.css">
</head>
<body class="deck-body">
<a class="deck-skip" href="#deck-main">{LE(("Skip to the deck", "Lompat ke deck"))}</a>
<div class="deck-progress"></div>
<div class="deck-count">1 / {len(slides)}</div>
<div class="deck-viewport" id="deck-main">
  <div class="deck-stage" id="stage">
    <div class="deck-topbar">
      <a class="deck-brand" href="{P}index.html"><span class="mark" aria-hidden="true">r.</span>
        <span>{E(b.PERSON['name'])}</span><small>{LE(deck['product'])}</small></a>
      <nav class="deck-nav" aria-label="{LE(("Slides", "Slide"))}">{nav}</nav>
      <div class="deck-meta">
        <span class="d-chip">{LE(deck['period'])}</span>
        <span class="d-chip dk">{LE(("Verified evidence", "Bukti terverifikasi"))}</span>
      </div>
    </div>
    {slide_html}
  </div>
</div>
{flow}
<script src="{P}assets/deck.js" defer></script>
</body>
</html>
"""
    out_dir = b.ROOT if lang == "en" else os.path.join(b.ROOT, "id")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)
    print("wrote", ("" if lang == "en" else "id/") + filename)
