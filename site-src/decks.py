"""Evidence decks: one full-screen deck per case, built in English and Indonesian.

A deck shows the result of a piece of work and the method behind it, in the same
presentation format I use at work. Text is bilingual inline as (english, indonesian),
the same convention powersync_page.py uses.

Source for this deck: the internal customer-journey analysis of the 4-22 Sep 2026
click-to-WhatsApp campaign, plus the journey-layers systems map. Figures are the ones
in those decks. Deliberately left out: customer names, the dealers behind each failure,
and the vacancy detail of the internal org chart. Where nothing was measured the deck
says so instead of estimating: the blind zone is part of the story.

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
    "period": ("4–22 Sep 2026", "4–22 Sep 2026"),
    "title": (
        "697 people asked about our vehicle. <em>210 were lost by us</em>, not by the budget.",
        "697 orang bertanya tentang kendaraan kami. <em>210 hilang karena kami</em>, bukan karena budget.",
    ),
    "lead": (
        "I ran the September advert campaign, then read and classified every one of the 697 "
        "WhatsApp conversations it produced.",
        "Saya menjalankan kampanye iklan September, lalu membaca dan mengklasifikasi seluruh 697 "
        "percakapan WhatsApp yang dihasilkannya.",
    ),
    "slides": (
        ["Result", "Journey", "Campaign", "Leaks", "Systems", "Next"],
        ["Hasil", "Journey", "Kampanye", "Kebocoran", "Sistem", "Berikutnya"],
    ),
    "funnel": {
        "chats": 697, "qualified": 365, "hot": 105, "to_dealer": 56,
        "drop_qualify": 332, "drop_intent": 260, "drop_forward": 49,
    },
}


# --------------------------------------------------------------------------- render


def build(b, deck=DIGITAL_GROWTH):
    lang = b.LANG
    P = b.P

    def L(pair):
        return pair[0] if lang == "en" else pair[1]

    def LE(pair):
        return E(L(pair))

    f = deck["funnel"]
    names = L(deck["slides"])
    total = len(names)
    sep = "," if lang == "en" else "."
    rp = "IDR " if lang == "en" else "Rp"

    def money(value):
        return rp + format(value, ",").replace(",", sep)

    def num(value, prefix="", suffix=""):
        """A figure that counts up when its slide opens."""
        return (f'<span data-count="{value}" data-sep="{sep}"'
                f'{f" data-prefix={prefix!r}" if prefix else ""}'
                f'{f" data-suffix={suffix!r}" if suffix else ""}>0</span>')

    def title(text, note, audience, step):
        dots = "".join(
            f'<span class="{"on" if i <= step else ""}"></span>' for i in range(total)
        )
        return f"""<div class="d-title d-rv">
    <div>
      <div class="d-audience"><i></i>{LE(audience)}<span class="d-depth">{dots}</span></div>
      <h2 style="margin-top:9px">{L(text)}</h2>
    </div>
    <p>{LE(note)}</p>
  </div>"""

    def figure(value, label, sub, size=44):
        return f"""<div style="display:flex;align-items:baseline;gap:14px">
      <div class="d-big" style="font-size:{size}px;min-width:150px">{value}</div>
      <div><p style="font-size:15px;font-weight:700;letter-spacing:-.02em">{LE(label)}</p>
      <p class="d-sub" style="font-size:12.5px">{LE(sub)}</p></div>
    </div>"""

    def steps(items):
        return "".join(
            f'<li><b>{i + 1:02d}</b><span>{LE(x)}</span></li>' for i, x in enumerate(items)
        )

    # ------------------------------------------------------------- slide 1 · result
    xyz = [
        (("X", "X"), ("What I did", "Yang saya kerjakan"),
         ("Ran the September advert campaign and followed <b>every conversation it produced</b>, "
          "from the advert to the dealer.",
          "Menjalankan kampanye iklan September dan mengikuti <b>setiap percakapan yang dihasilkan</b>, "
          "dari iklan sampai ke dealer.")),
        (("Y", "Y"), ("Measured by", "Diukur dengan"),
         ("<b>697 conversations</b> for IDR 1.92 million — about <b>IDR 2,760 each</b> — and "
          "<b>105 buyers ready to buy</b>, of whom only 56 ever reached a dealer.",
          "<b>697 percakapan</b> dengan biaya Rp1,92 juta — sekitar <b>Rp2.760 per percakapan</b> — dan "
          "<b>105 calon pembeli siap beli</b>, tetapi hanya 56 yang sampai ke dealer.")),
        (("Z", "Z"), ("By doing", "Dengan cara"),
         ("Reading all 697 conversations, sorting them into <b>six failure types that repeat</b>, "
          "and mapping the 11 systems this journey needs against the 5 we have.",
          "Membaca seluruh 697 percakapan, memilahnya jadi <b>enam tipe kegagalan yang berulang</b>, "
          "dan memetakan 11 sistem yang dibutuhkan journey ini terhadap 5 yang kami punya.")),
    ]
    xyz_html = "".join(
        f"""<div class="d-xyz-line"><div class="d-xyz-tag"><b>{LE(letter)}</b><span>{LE(tag)}</span></div>
      <p>{L(body)}</p></div>"""
        for letter, tag, body in xyz
    )

    headline_figures = "".join([
        figure(num(697), ("conversations with buyers", "percakapan dengan calon pembeli"),
               ("19 days of adverts, IDR 1.92 million", "19 hari iklan, Rp1,92 juta")),
        figure(num(2760, prefix=rp), ("spent per conversation", "biaya per percakapan"),
               ("a ready-to-buy lead cost IDR 18,320", "lead siap beli berbiaya Rp18.320")),
        figure(num(210), ("lost inside our own process", "hilang di dalam proses kami sendiri"),
               ("30% of every conversation we paid for", "30% dari percakapan yang kami bayar")),
    ])

    jobs = [
        ("bl", ("Growth", "Growth"), ("ran the adverts", "menjalankan iklan")),
        ("bl", ("Data", "Data"), ("classified all 697 conversations", "mengklasifikasi 697 percakapan")),
        ("dk", ("Business analysis", "Business analysis"),
         ("turned it into systems and rules", "mengubahnya jadi sistem dan aturan")),
    ]
    jobs_html = "".join(
        f"""<div class="d-row" style="gap:10px"><span class="d-chip {cls}" style="min-width:128px;text-align:center">{LE(tag)}</span>
      <span style="flex:1;font-weight:600;font-size:13.5px">{LE(work)}</span></div>"""
        for cls, tag, work in jobs
    )

    slide1 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1.45fr) minmax(0,.78fr)">
  {title(deck['title'], deck['lead'], ("The short version · for anyone", "Versi singkat · untuk siapa saja"), 0)}
  <div class="d-card d-rv" style="--d:80;grid-column:span 8">
    <div class="d-head"><div><div class="d-kk">{LE(("Result, in one sentence", "Hasil, dalam satu kalimat"))}</div>
      <h3>{LE(("The adverts worked. The handling behind them did not.", "Iklannya berhasil. Penanganan di belakangnya tidak."))}</h3></div>
      <div class="d-chips"><span class="d-chip bl">{LE(deck['period'])}</span></div></div>
    <div class="d-xyz">{xyz_html}</div>
  </div>
  <div class="d-card d-rv" style="--d:220;grid-column:span 4;justify-content:space-evenly">{headline_figures}</div>
  <div class="d-card d-rv" style="--d:320;grid-column:span 8">
    <div class="d-kk">{LE(("In plain terms", "Dengan kata sederhana"))}</div>
    <p class="d-plain">{L((
      "Adverts brought 697 people to WhatsApp in 19 days. <b>116 of them were never answered at all.</b> "
      "204 were answered, but nobody asked the one question that decides which dealer they belong to. "
      "And 49 of the people most ready to buy never reached a dealer. None of that needed more budget.",
      "Iklan membawa 697 orang ke WhatsApp dalam 19 hari. <b>116 di antaranya sama sekali tidak pernah dibalas.</b> "
      "204 dibalas, tetapi tidak ada yang menanyakan satu hal yang menentukan dealer mana yang menanganinya. "
      "Dan 49 orang yang paling siap membeli tidak pernah sampai ke dealer. Semua itu tidak butuh tambahan budget."))}</p>
  </div>
  <div class="d-card d-rv" style="--d:400;grid-column:span 4">
    <div class="d-kk">{LE(("Three jobs inside one piece of work", "Tiga peran dalam satu pekerjaan"))}</div>
    <div style="display:flex;flex-direction:column;gap:9px">{jobs_html}</div>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 2 · journey
    # Ribbons are drawn to scale, but each label block needs about 70px of clear
    # space, so the gap under a stage grows as that stage's ribbon gets thinner.
    scale, top = 0.62, 40
    h = {k: round(v * scale) for k, v in f.items()}
    spec = {
        "width": 1600, "height": 600, "nodeWidth": 13, "scale": scale, "minHeight": 6,
        "colors": {"in": "#355c7d", "ok": "#4a7d63", "leak": "#9a5a4a", "drop": "#9aa5ae"},
        "labelColors": {"in": "#20272d", "ok": "#20272d", "leak": "#9a5a4a",
                        "drop": "#66737e", "blind": "#8a949d"},
        "linkOpacity": 0.36, "dotRadius": 3,
        "nodes": [
            {"id": "chats", "type": "in", "x": 150, "y": top, "value": f["chats"], "side": "left",
             "big": 32, "label": L(("conversations", "percakapan")),
             "sub": L(("4–22 Sep 2026", "4–22 Sep 2026"))},
            {"id": "qual", "type": "ok", "x": 470, "y": top, "value": f["qualified"], "big": 26,
             "label": L(("told us where they live", "memberi tahu lokasinya")),
             "sub": L(("52% · a lead we can route", "52% · lead yang bisa diarahkan"))},
            {"id": "dropq", "type": "leak", "x": 470, "y": top + h["qualified"] + 70,
             "value": f["drop_qualify"], "big": 24,
             "label": L(("dropped before that", "gugur sebelum itu")),
             "sub": L(("116 never answered · 204 never asked", "116 tak dibalas · 204 tak ditanya"))},
            {"id": "hot", "type": "ok", "x": 790, "y": top, "value": f["hot"], "big": 26,
             "label": L(("ready to buy", "siap membeli")),
             "sub": L(("15% · IDR 18,320 each", "15% · Rp18.320 per lead"))},
            {"id": "dropi", "type": "drop", "x": 790, "y": top + h["hot"] + 80,
             "value": f["drop_intent"], "big": 22,
             "label": L(("still deciding, or out of reach", "masih menimbang, atau tak terjangkau")),
             "sub": L(("45 live where we have no dealer", "45 tinggal di area tanpa dealer"))},
            {"id": "dealer", "type": "ok", "x": 1090, "y": top, "value": f["to_dealer"], "big": 24,
             "label": L(("reached a dealer", "sampai ke dealer")),
             "sub": L(("8% of everyone who wrote in", "8% dari semua yang menghubungi"))},
            {"id": "dropf", "type": "leak", "x": 1090, "y": top + h["to_dealer"] + 85,
             "value": f["drop_forward"], "big": 22,
             "label": L(("ready to buy, never forwarded", "siap beli, tidak diteruskan")),
             "sub": L(("47% of the hottest leads", "47% dari lead terpanas"))},
            {"id": "blind", "type": "blind", "x": 1360, "y": top, "value": f["to_dealer"],
             "display": "?", "big": 30, "label": L(("did they buy?", "apakah mereka membeli?")),
             "sub": L(("nobody tracked this yet", "belum ada yang melacaknya"))},
        ],
        "notes": [{"x": 1235, "y": 108, "size": 13,
                   "text": L(("no data past the dealer", "tak ada data setelah dealer"))}],
        "links": [
            {"s": "chats", "t": "qual", "value": f["qualified"], "flow": 8},
            {"s": "chats", "t": "dropq", "value": f["drop_qualify"], "flow": 5},
            {"s": "qual", "t": "hot", "value": f["hot"], "flow": 4},
            {"s": "qual", "t": "dropi", "value": f["drop_intent"], "flow": 3},
            {"s": "hot", "t": "dealer", "value": f["to_dealer"], "flow": 2},
            {"s": "hot", "t": "dropf", "value": f["drop_forward"], "flow": 2},
            {"s": "dealer", "t": "blind", "value": f["to_dealer"], "blind": True},
        ],
    }

    slide2 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr)">
  {title(("Every stage is narrower — and the last one is <em>dark</em>",
          "Setiap tahap makin sempit — dan tahap terakhir <em>gelap</em>"),
         ("Ribbon width is the number of people. Red is a loss we caused; grey is the market deciding.",
          "Lebar pita adalah jumlah orang. Merah adalah kehilangan karena kami; abu-abu adalah pasar yang memutuskan."),
         ("What actually happened · the funnel", "Apa yang sebenarnya terjadi · funnel-nya"), 1)}
  <div class="d-card d-rv" style="--d:120;grid-column:span 12">
    <div class="d-head"><div><div class="d-kk">{LE(("Customer journey · 697 conversations", "Customer journey · 697 percakapan"))}</div>
      <h3>{LE(("From advert to dealer, in four steps", "Dari iklan ke dealer, dalam empat langkah"))}</h3></div>
      <div class="d-chips"><span class="d-chip wn">{LE(("210 lost by us", "210 hilang karena kami"))}</span>
        <span class="d-chip">{LE(("hatched = no data", "arsir = tidak ada data"))}</span></div></div>
    <div class="d-sankey" data-sankey="{E(json.dumps(spec), quote=True)}"></div>
    <p class="d-note">{LE((
      "Each drop is the difference between two stages, and its caption names the biggest cause inside it. "
      "Exact counts per cause are on the Leaks slide.",
      "Setiap penurunan adalah selisih antara dua tahap, dan keterangannya menyebut penyebab terbesar di dalamnya. "
      "Jumlah persis per penyebab ada di slide Kebocoran."))}</p>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 3 · campaign
    creative = [
        (("Opens WhatsApp straight away", "Langsung membuka WhatsApp"), 377, 1442, "ok"),
        (("Sends people to a page first", "Mengarahkan ke halaman dulu"), 238, 5798, "wn"),
        (("Found us without an advert", "Menemukan kami tanpa iklan"), 82, None, ""),
    ]
    creative_rows = "".join(
        f"""<div class="d-row"><span style="min-width:236px">{LE(label)}</span>
      <span class="bar"><i class="{cls}" data-w="{round(100 * n / 377)}"></i></span>
      <span class="num">{n}</span>
      <span class="d-chip {'ok' if cls == 'ok' else ('wn' if cls else 'bl')}"
        style="min-width:92px;text-align:center">{money(cost) if cost else LE(("organic", "organik"))}</span></div>"""
        for label, n, cost, cls in creative
    )

    ladder = [
        (("Per conversation", "Per percakapan"), 2760, 15),
        (("Per lead we can route", "Per lead yang bisa diarahkan"), 5260, 29),
        (("Per buyer ready to buy", "Per calon pembeli siap beli"), 18320, 100),
        (("Per vehicle sold", "Per unit terjual"), None, 100),
    ]
    ladder_rows = "".join(
        f"""<div class="d-row"><span style="min-width:206px">{LE(label)}</span>
      <span class="bar"><i data-w="{w}"{'' if cost else ' style="background:repeating-linear-gradient(135deg,#c9d1d7 0 4px,#eef1f3 4px 8px)"'}></i></span>
      <span class="num" style="min-width:98px">{money(cost) if cost else rp + " ?"}</span></div>"""
        for label, cost, w in ladder
    )

    reach = "".join([
        figure(num(63156), ("people saw the adverts", "orang melihat iklannya"),
               ("358,018 views · about 5.7 each", "358.018 tayangan · sekitar 5,7 kali per orang"), 34),
        figure(num(4.3, suffix="%"), ("of them clicked", "di antaranya mengklik"),
               ("99.8% were not following us", "99,8% belum mengikuti akun kami"), 34),
    ])

    slide3 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr) minmax(0,1fr)">
  {title(("One advert format cost <em>4× less</em> per conversation",
          "Satu format iklan berbiaya <em>4× lebih murah</em> per percakapan"),
         ("The campaign side: what the money bought, and which decision changed the price.",
          "Sisi kampanye: apa yang dibeli uangnya, dan keputusan mana yang mengubah harganya."),
         ("Growth · what the adverts did", "Growth · hasil kerja iklannya"), 2)}
  <div class="d-card d-rv" style="--d:80;grid-column:span 4;justify-content:space-evenly">
    <div class="d-kk">{LE(("Reach · 19 days · 3 adverts", "Jangkauan · 19 hari · 3 iklan"))}</div>
    {reach}
  </div>
  <div class="d-card d-rv" style="--d:180;grid-column:span 8">
    <div class="d-head"><div><div class="d-kk">{LE(("Where the 697 conversations came from", "Dari mana 697 percakapan itu datang"))}</div>
      <h3>{LE(("Same budget, very different price", "Budget sama, harga sangat berbeda"))}</h3></div></div>
    <div class="d-rows">{creative_rows}</div>
    <p class="d-note">{LE((
      "The format that opens a chat straight away brought the most conversations at IDR 1,442 each. "
      "The one that sends people to a page first cost IDR 5,798 for every conversation it produced.",
      "Format yang langsung membuka chat menghasilkan percakapan terbanyak dengan biaya Rp1.442. "
      "Format yang mengarahkan ke halaman dulu menghabiskan Rp5.798 untuk setiap percakapan."))}</p>
  </div>
  <div class="d-card d-rv" style="--d:280;grid-column:span 7">
    <div class="d-head"><div><div class="d-kk">{LE(("The cost ladder", "Tangga biaya"))}</div>
      <h3>{LE(("Each step deeper costs more — then stops being countable",
                "Tiap langkah lebih dalam makin mahal — lalu tak bisa dihitung"))}</h3></div></div>
    <div class="d-rows">{ladder_rows}</div>
  </div>
  <div class="d-card d-rv" style="--d:360;grid-column:span 5">
    <div class="d-kk">{LE(("Two decisions I took to the team", "Dua keputusan yang saya bawa ke tim"))}</div>
    <ul class="d-steps">
      <li><b>01</b><span>{LE((
        "Stop advertising in provinces where no dealer can serve the buyer — 45 conversations came from there.",
        "Hentikan iklan di provinsi yang belum punya dealer — 45 percakapan datang dari sana."))}</span></li>
      <li><b>02</b><span>{LE((
        "Make one promo wording true everywhere; three buyers were told at the dealer that the advert's offer did not apply.",
        "Samakan satu kalimat promo di semua tempat; tiga pembeli diberi tahu di dealer bahwa penawaran iklan tidak berlaku."))}</span></li>
    </ul>
    <p class="d-note">{LE((
      "Both cost nothing to fix, and both stayed invisible until the conversations were read.",
      "Keduanya tidak butuh biaya untuk diperbaiki, dan keduanya tak terlihat sebelum percakapan dibaca."))}</p>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 4 · leaks
    leaks = [
        ("L1", ("Never answered at all", "Sama sekali tidak dibalas"), 116, "16.6%",
         ("Worst on weekends and on the busiest advert days.",
          "Terparah di akhir pekan dan di hari iklan tersibuk."),
         ("Reply target under 15 minutes, with cover at night and weekends.",
          "Target balas di bawah 15 menit, dengan jaga malam dan akhir pekan.")),
        ("L2", ("Answered, but never asked where they live", "Dibalas, tapi tidak ditanya lokasinya"), 204, "29.3%",
         ("Nearly half of those chats closed themselves before anyone asked.",
          "Hampir separuh chat itu tertutup sendiri sebelum sempat ditanya."),
         ("Ask the area in the first message, with province buttons.",
          "Tanyakan area di pesan pertama, dengan tombol pilihan provinsi.")),
        ("L3", ("Told us where — and we have no dealer there", "Memberi tahu lokasinya — dan kami tak punya dealer di sana"), 45, "6.5%",
         ("Paid adverts were running in provinces with no dealer at all.",
          "Iklan berbayar berjalan di provinsi yang sama sekali belum punya dealer."),
         ("Remove those areas from targeting until a dealer covers them.",
          "Keluarkan area itu dari targeting sampai ada dealer yang menanganinya.")),
        ("L4", ("Stuck on the down-payment question", "Tertahan di pertanyaan uang muka"), 135, "31%",
         ("Of 215 interested buyers, 135 were still waiting on an answer about instalments.",
          "Dari 215 peminat, 135 masih menunggu jawaban soal cicilan."),
         ("One standard instalment table, and the same promo status at every dealer.",
          "Satu tabel cicilan baku, dan status promo yang sama di semua dealer.")),
        ("L5", ("Ready to buy, never forwarded", "Siap beli, tidak pernah diteruskan"), 49, "47%",
         ("The most expensive leads we buy stopped at the front desk.",
          "Lead termahal yang kami beli berhenti di meja depan."),
         ("Forward within the hour, and make the hand-off a required field.",
          "Teruskan dalam satu jam, dan jadikan serah terima kolom wajib.")),
        ("L6", ("Forwarded, then silence", "Diteruskan, lalu senyap"), None, "?",
         ("No dealer sends a status back, so nobody knows what happened next.",
          "Tidak ada dealer yang mengirim status balik, jadi tak ada yang tahu kelanjutannya."),
         ("A status update per lead within 48 hours, tied to one Lead ID.",
          "Update status per lead dalam 48 jam, terhubung ke satu Lead ID.")),
    ]
    leak_rows = "".join(
        f"""<tr>
      <td><span class="d-chip {'gy' if n is None else 'wn'}" style="min-width:34px;text-align:center;padding:5px 8px">{lid}</span></td>
      <td><div class="tt">{LE(name)}</div><div class="te">{LE(note)}</div></td>
      <td style="text-align:right"><div class="tn">{n if n else "?"}</div>
        <div class="d-sub" style="font-size:11.5px">{E(pct)}</div></td>
      <td class="tf">{LE(fix)}</td>
    </tr>"""
        for lid, name, n, pct, note, fix in leaks
    )

    slide4 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr)">
  {title(("Six failure types — <em>none are the customer's fault</em>",
          "Enam tipe kegagalan — <em>tak satu pun salah pelanggan</em>"),
         ("I read all 697 conversations and tagged what stopped each one. The tags became six types that repeat.",
          "Saya membaca seluruh 697 percakapan dan menandai apa yang menghentikannya. Tanda itu menjadi enam tipe yang berulang."),
         ("Data · all 697 conversations, classified", "Data · 697 percakapan, diklasifikasi"), 3)}
  <div class="d-card d-rv" style="--d:100;grid-column:span 9;padding-top:14px">
    <table class="tx"><thead><tr>
      <th style="width:58px">{LE(("Type", "Tipe"))}</th>
      <th>{LE(("What stopped the conversation", "Apa yang menghentikan percakapan"))}</th>
      <th style="text-align:right;width:88px">{LE(("People", "Orang"))}</th>
      <th style="width:300px">{LE(("The fix I proposed", "Perbaikan yang saya usulkan"))}</th>
    </tr></thead><tbody>{leak_rows}</tbody></table>
    <p class="d-note" style="margin-top:auto">{LE((
      "L1, L3 and L5 are ours alone — 210 conversations. L2 and L4 are process gaps we share with the dealers, and L6 is the missing feedback loop that hides everything after the hand-off.",
      "L1, L3, dan L5 murni milik kami — 210 percakapan. L2 dan L4 adalah celah proses bersama dealer, dan L6 adalah lingkaran umpan balik yang hilang sehingga semua setelah serah terima tak terlihat."))}</p>
  </div>
  <div style="grid-column:span 3;display:flex;flex-direction:column;gap:16px;min-height:0">
    <div class="d-card dark d-rv" style="--d:200;flex:1;justify-content:center">
      <div class="d-kk">{LE(("Cost of the ones we control", "Biaya dari yang kami kendalikan"))}</div>
      <div class="d-big" style="font-size:38px">{num(580, prefix=rp, suffix="k")}</div>
      <p class="d-sub" style="color:#a9b6c2">{LE((
        "of the IDR 1.92 million spent went on conversations our own process dropped.",
        "dari Rp1,92 juta yang dibelanjakan terpakai untuk percakapan yang gugur oleh proses kami sendiri."))}</p>
    </div>
    <div class="d-card d-rv" style="--d:260;flex:1">
      <div class="d-kk">{LE(("How the tagging worked", "Cara penandaannya"))}</div>
      <ul class="d-steps" style="gap:7px">{steps([
        ("Export every conversation for the period", "Ekspor seluruh percakapan pada periode itu"),
        ("Read each one, tag what stopped it", "Baca satu per satu, tandai penyebab berhentinya"),
        ("Group repeating tags into types", "Kelompokkan tanda yang berulang jadi tipe"),
        ("Price each type at the blended cost", "Hitung biaya tiap tipe pada biaya rata-rata"),
      ])}</ul>
    </div>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 5 · systems
    today = [
        ("Advert figures read off a screenshot", "Angka iklan dibaca dari screenshot"),
        ("Chat history exported into Excel", "Riwayat chat diekspor ke Excel"),
        ("Classified by hand, by one analyst", "Diklasifikasi manual, oleh satu analis"),
        ("Ends its life as a slide deck", "Berakhir sebagai deck slide"),
    ]
    target = [
        ("Advert data arrives through the API", "Data iklan masuk lewat API"),
        ("Area and intent become required fields in the chat", "Area dan minat jadi kolom wajib di chat"),
        ("One Lead ID is created in PowerSync", "Satu Lead ID dibuat di PowerSync"),
        ("The dealer returns a status against that ID", "Dealer mengembalikan status untuk ID itu"),
        ("Sale, financing and service link to the same ID", "Penjualan, leasing, dan servis terhubung ke ID yang sama"),
    ]
    domains = [
        (True, ("Business analysis & delivery", "Business analysis & delivery"), ("Core", "Inti"),
         ("Turned six failure types into reply targets, required fields and a Lead ID — then built them in PowerSync.",
          "Mengubah enam tipe kegagalan jadi target balas, kolom wajib, dan Lead ID — lalu membangunnya di PowerSync.")),
        (False, ("Data analysis", "Data analysis"), ("Support", "Pendukung"),
         ("Read and classified 697 conversations, then priced every stage of the funnel.",
          "Membaca dan mengklasifikasi 697 percakapan, lalu menghitung biaya tiap tahap funnel.")),
        (False, ("Digital marketing & growth", "Digital marketing & growth"), ("Support", "Pendukung"),
         ("Ran the adverts: reach, cost per conversation by format, and where we should not advertise.",
          "Menjalankan iklan: jangkauan, biaya per percakapan tiap format, dan di mana kami tidak boleh beriklan.")),
        (False, ("AI orchestration", "AI orchestration"), ("Support", "Pendukung"),
         ("Drafts the follow-up for the leads we were dropping; a person still approves every reply.",
          "Menyusun draft follow-up untuk lead yang terlewat; setiap balasan tetap disetujui manusia.")),
    ]
    domain_html = "".join(
        f"""<div class="d-domain{' core' if core else ''}"><span>{LE(role)}</span>
      <strong>{LE(name)}</strong><em>{LE(note)}</em></div>"""
        for core, name, role, note in domains
    )

    slide5 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr) auto">
  {title(("The real problem is <em>plumbing</em>, not effort",
          "Masalah sebenarnya ada di <em>pipa datanya</em>, bukan usaha"),
         ("Eleven systems are needed to see this journey end to end. Five exist, and every one is pulled by hand.",
          "Sebelas sistem dibutuhkan untuk melihat journey ini ujung ke ujung. Lima yang ada, dan semuanya ditarik manual."),
         ("Systems · what the business needs to build", "Sistem · yang perlu dibangun perusahaan"), 4)}
  <div class="d-card d-rv" style="--d:80;grid-column:span 4;justify-content:space-evenly">
    {figure(num(5) + '<span style="font-size:.5em;color:#66737e"> / 11</span>',
            ("systems actually in place", "sistem yang benar-benar ada"),
            ("and all five are pulled by hand", "dan kelimanya ditarik manual"), 38)}
    {figure(num(3) + '<span style="font-size:.5em;color:#66737e"> / 5</span>',
            ("stage targets cannot be measured", "target per tahap tidak bisa diukur"),
            ("the last three stages have no data at all", "tiga tahap terakhir sama sekali tanpa data"), 38)}
    <p class="d-note">{LE((
      "Ownership fades the further a buyer gets from the advert: the hand-off, after-sales and loyalty have no clear owner today.",
      "Kepemilikan makin kabur makin jauh pembeli dari iklan: serah terima, after-sales, dan loyalty belum punya pemilik yang jelas."))}</p>
  </div>
  <div class="d-card d-rv" style="--d:180;grid-column:span 4">
    <div class="d-head"><div><div class="d-kk">{LE(("Today", "Hari ini"))}</div>
      <h3>{LE(("Held together by one analyst", "Ditopang oleh satu analis"))}</h3></div></div>
    <ul class="d-steps">{steps(today)}</ul>
    <p class="d-note">{LE((
      "There is no shared ID, so nothing can be followed past the hand-off.",
      "Tidak ada ID bersama, jadi tak ada yang bisa diikuti setelah serah terima."))}</p>
  </div>
  <div class="d-card dark d-rv" style="--d:260;grid-column:span 4">
    <div class="d-kk">{LE(("What I specified instead", "Yang saya spesifikasikan sebagai gantinya"))}</div>
    <h3>{LE(("One Lead ID, carried the whole way", "Satu Lead ID, dibawa sepanjang jalan"))}</h3>
    <ul class="d-steps">{steps(target)}</ul>
  </div>
  <div class="d-card d-rv" style="--d:340;grid-column:span 12;padding:18px 20px">
    <div class="d-head"><div class="d-kk">{LE(("Which part of my work does what", "Bagian mana dari pekerjaan saya yang berperan"))}</div></div>
    <div class="d-domains">{domain_html}</div>
  </div>
</div>"""

    # ------------------------------------------------------------- slide 6 · next
    blind = [
        (("Did any of them buy", "Apakah ada yang membeli"),
         ("No dealer returns a status, so not one of the 56 can be followed to a sale.",
          "Tidak ada dealer yang mengembalikan status, jadi tak satu pun dari 56 bisa diikuti sampai penjualan.")),
        (("Cost per vehicle sold", "Biaya per unit terjual"),
         ("Cost per conversation and per hot lead are known; cost per sale cannot be derived from them.",
          "Biaya per percakapan dan per hot lead diketahui; biaya per penjualan tidak bisa diturunkan dari situ.")),
        (("Whether the fixes worked", "Apakah perbaikannya berhasil"),
         ("The six fixes were proposed in Sep 2026. Their effect has not been measured yet.",
          "Enam perbaikan diusulkan pada Sep 2026. Efeknya belum diukur.")),
        (("The ownership proposal", "Usulan kepemilikan peran"),
         ("A proposed split of responsibilities, not an approved one.",
          "Usulan pembagian tanggung jawab, belum disetujui.")),
    ]
    blind_html = "".join(
        f'<li><code>{LE(("no data", "tidak ada data"))}</code><span><b>{LE(name)}</b> — {LE(note)}</span></li>'
        for name, note in blind
    )
    nexts = [
        ("Create the Lead ID in PowerSync and stamp it on every conversation",
         "Buat Lead ID di PowerSync dan tempelkan ke setiap percakapan"),
        ("Give the dealer a two-field status form, due within 48 hours",
         "Beri dealer form status dua kolom, wajib dalam 48 jam"),
        ("Hold the reply target, and report the six types every week",
         "Jaga target balas, dan laporkan enam tipe itu setiap pekan"),
        ("Only then report a cost per vehicle sold",
         "Baru setelah itu laporkan biaya per unit terjual"),
    ]
    supported = [
        (("697", "697"), ("conversations, all read", "percakapan, semuanya dibaca")),
        (("IDR 1.92m", "Rp1,92 jt"), ("advert spend, 19 days", "belanja iklan, 19 hari")),
        (("105", "105"), ("buyers ready to buy", "calon pembeli siap beli")),
    ]
    supported_html = "".join(
        f'<div><div class="d-big" style="font-size:24px">{LE(v)}</div>'
        f'<p class="d-sub" style="font-size:12px">{LE(l)}</p></div>'
        for v, l in supported
    )
    codes = ["BA02-E01", "BA02-E03", "BA02-E04", "BA02-E05", "BA02-E06",
             "BA02-E07", "BA02-E08", "BA02-E10", "BA02-E11", "BA02-E13"]

    slide6 = f"""
<div class="d-grid" style="grid-template-rows:auto minmax(0,1fr)">
  {title(("What I <em>don't</em> claim, and what I'd build next",
          "Yang <em>tidak</em> saya klaim, dan yang akan saya bangun berikutnya"),
         ("A funnel deck is easy to inflate. These are the figures that do not exist yet.",
          "Deck funnel mudah dilebih-lebihkan. Ini angka-angka yang memang belum ada."),
         ("What I don't claim · the fine print", "Yang tidak saya klaim · catatan jujurnya"), 5)}
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
      <h3>{LE(("Close the loop before buying more reach", "Tutup lingkarannya sebelum membeli jangkauan lagi"))}</h3>
      <ul class="d-steps" style="margin-top:2px">{steps(nexts)}</ul>
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

    slides = [slide1, slide2, slide3, slide4, slide5, slide6]
    nav = "".join(f'<button type="button">{E(n)}</button>' for n in names)
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
    stages = [
        (("Asked about the vehicle", "Bertanya tentang kendaraan"), f["chats"], ""),
        (("Told us where they live", "Memberi tahu lokasinya"), f["qualified"], ""),
        (("Ready to buy", "Siap membeli"), f["hot"], ""),
        (("Reached a dealer", "Sampai ke dealer"), f["to_dealer"], "wn"),
    ]
    flow_stages = "".join(
        f'<div class="d-row"><span style="flex:1">{LE(label)}</span>'
        f'<span class="num">{n}</span>'
        f'<span class="d-chip {"wn" if cls else "ok"}">{round(100 * n / f["chats"])}%</span></div>'
        for label, n, cls in stages
    )
    flow_leaks = "".join(
        f'<li><code>{lid}</code><span><b>{LE(name)}</b> — {n if n else "?"} '
        f'{LE(("people", "orang"))}. {LE(fix)}</span></li>'
        for lid, name, n, pct, note, fix in leaks
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
    <h2>{LE(("The funnel, stage by stage", "Funnel-nya, tahap demi tahap"))}</h2>
    <p class="d-plain">{L((
      "Adverts brought 697 people to WhatsApp in 19 days. <b>I read every one of those conversations.</b>",
      "Iklan membawa 697 orang ke WhatsApp dalam 19 hari. <b>Saya membaca setiap percakapan itu.</b>"))}</p>
    <div class="d-rows">{flow_stages}</div>
  </section>
  <section>
    <h2>{LE(("Six failure types", "Enam tipe kegagalan"))}</h2>
    <ul class="d-list">{flow_leaks}</ul>
  </section>
  <section>
    <h2>{LE(("What the business needs to build", "Yang perlu dibangun perusahaan"))}</h2>
    <p class="d-sub">{LE((
      "Eleven systems are needed to see this journey end to end. Five exist, all pulled by hand.",
      "Sebelas sistem dibutuhkan untuk melihat journey ini ujung ke ujung. Lima yang ada, semuanya manual."))}</p>
    <ul class="d-steps">{steps(target)}</ul>
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
    title_text = L(("From advert to dealer: 697 conversations, mapped",
                    "Dari iklan ke dealer: 697 percakapan, dipetakan"))
    description = L(deck["lead"])
    en_url = b.SITE_URL + filename
    id_url = b.SITE_URL + "id/" + filename
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title_text)} · {E(b.PERSON['name'])}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{en_url if lang == 'en' else id_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="id" href="{id_url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(title_text)}">
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
        <span class="d-chip dk">{LE(("Internal evidence", "Bukti internal"))}</span>
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
