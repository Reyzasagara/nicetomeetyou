"""Documentation page: real screenshots behind the case studies.

Company figures, customer names, dealer names and the competitor's identity are blurred
before an image goes into assets/img/docs (blur pipeline: Carrer_assistant/runs/
grab-operations-analytics-assistant-manager/_build). Public statistics stay readable.
Each item gives what it is and its impact in Google's X-Y-Z form.
"""

GROUPS = [
    ("PowerSync platform", "The system I lead: database, screens and the dashboards built on it.", [
        dict(title="PowerSync database (EER diagram)", tool="MySQL", imgs=["erd"],
             what="The PowerSync database, opened in MySQL Workbench.",
             xyz="Built one data model for the whole dealer-to-factory flow, measured by 210 tables and 4,818 unit records traceable from order to customer (99.9% linked to a PO), by designing the Laravel and MySQL schema myself as analyst and developer.",
             src="MySQL Workbench, 2026. Schema only, no business figures."),
        dict(title="PowerSync home screen", tool="Laravel", imgs=["ui"],
             what="The home screen, with menus for dealers, sales, spare parts, marketing and production.",
             xyz="Moved dealer orders, vehicle registration (faktur), free-service coupons, claims and QC off paper and Excel, measured by 15 of 22 dealers (68.2%) active in May–Jun 2026, by designing one web platform around each team's daily tasks.",
             src="PowerSync, Oct 2026."),
        dict(title="Production board", tool="Laravel", imgs=["production"],
             what="Hourly output for every post on the line, live since Aug 2026.",
             xyz="Replaced the paper daily production report with a live board, measured by hourly output against target for every post, an end-of-shift forecast and downtime by cause (Man, Machine, Method, Material), by building a kiosk-fed production module in PowerSync.",
             src="PowerSync, Sep 2026. Customer name and figures blurred."),
        dict(title="Warranty and claims", tool="Laravel", imgs=["warranty"],
             what="Claim trend, claim type and the monthly warranty ratio.",
             xyz="Made warranty quality measurable every month, measured by a warranty ratio (claimed units ÷ units in operation) over 12 months with a drill-down per month, by linking each claim to the sold unit's record in PowerSync.",
             src="PowerSync, Oct 2026. Figures blurred."),
        dict(title="Director overview", tool="Laravel", imgs=["director"],
             what="Orders, revenue, spare parts, QC pass rate and deliveries on one screen.",
             xyz="Gave directors one live summary instead of separate reports, measured by orders, revenue, spare parts, QC pass rate, deliveries and order-status flow, filterable by year, quarter and month, by building it on the data dealers and staff already enter in PowerSync.",
             src="PowerSync, Oct 2026. Figures blurred."),
    ]),
    ("Power BI dashboards", "Reports I built for production meetings, inventory and market analysis.", [
        dict(title="Asakai 2W monthly summary", tool="Power BI", imgs=["asakai"],
             what="Monthly executive summary for the 2W frame and component morning meeting (asakai).",
             xyz="Gave the asakai one monthly view of production, measured by achievement rate, target-vs-actual gap and problem count for every line plus overtime by shift and line, by building the Power BI model (date table, line master, trend parameter).",
             src="Power BI, Jan 2026. Figures blurred."),
        dict(title="4W production performance (prototype)", tool="Power BI", imgs=["prod4w"],
             what="A prototype dashboard for the 4W lines, May 2025.",
             xyz="Made line performance visible hour by hour, measured by OEE split into availability, performance and quality per line plus line-stop minutes per hour, by modelling cycle time, planning, production report and reject tables in Power BI.",
             src="Power BI prototype, May 2025. Figures blurred."),
        dict(title="Material readiness for production orders", tool="Power BI", imgs=["inventory"],
             what="Supply and allocation status of material for each production order (PRO).",
             xyz="Showed which production orders were held up by missing material, measured by readiness, allocation and supply % per order and product group plus lacking lines per material, by building a star schema on SAP COOIS and MPS exports in Power BI.",
             src="Power BI, data as of Jul 2026. Logo, codes and figures blurred."),
        dict(title="Market leader sales analysis", tool="Power BI", imgs=["market"],
             what="Where the market leader sold its three-wheelers, 2022 to Aug 2024.",
             xyz="Found that 75.4% of the market leader's units sold in Java (2022–Aug 2024), the finding behind the 2025 Java dealer focus, by modelling its sales by month, model, dealer and regency in Power BI.",
             src="Power BI, Nov 2024. Dealer names, models and figures blurred."),
    ]),
    ("Python and HTML analytics", "Scripts and analysis decks I write when a spreadsheet is not enough.", [
        dict(title="Python scripts I use at work", tool="Python", imgs=["python"],
             what="A selection of my scripts for market data, QC inspection data and costing.",
             xyz="Automated data collection, cleaning and reporting, measured by 39 scripts (about 13,600 lines) covering BPS statistics, PDI inspection records, costing models and report decks, by writing Python with pandas, openpyxl, requests and LLM APIs.",
             src="Script folder, Oct 2026."),
        dict(title="Brebes market intelligence report", tool="Python + AI", imgs=["brebes-cover", "brebes-pareto"],
             what="A report on selling 3W cargo vehicles to shallot farmers in Brebes, May 2026.",
             xyz="Turned public statistics into a sales plan for one district, measured by a 12-page report covering production by sub-district, prices and the harvest calendar with every figure sourced, by writing an open-data scraper and an LLM-assisted analyst agent in Python.",
             src="Report and code, May 2026. Public statistics, left readable."),
        dict(title="Pilot area selection", tool="HTML", imgs=["pilot"],
             what="Why three pilot areas were chosen for the 2026 market-share pilot.",
             xyz="Chose 3 pilot areas out of 5 Java candidates, measured against the market leader's volume per area and whether we already had a dealer there, by building a treemap from Power BI sales data and ruling out 2 areas for structural reasons (multibrand dealers, government-tender sales).",
             src="Analysis deck, Jun 2026. Names and figures blurred."),
        dict(title="QC defect analysis", tool="Python + HTML", imgs=["quality"],
             what="Defect findings from pre-delivery inspection, Jun to Sep 2026.",
             xyz="Pointed QC at the few defect types that matter, measured by a Pareto of findings by defect type and by area of the unit, by cleaning PDI inspection records in Python and generating an interactive HTML deck.",
             src="Analysis deck, Oct 2026. Figures blurred."),
        dict(title="Customer journey Sankey", tool="HTML", imgs=["journey"],
             what="How prospects moved from seeing an ad to starting a WhatsApp chat, Sep 2026.",
             xyz="Showed where ad-driven prospects drop out, measured stage by stage from reach to ad click to WhatsApp chat, by joining Meta Ads and Qontak chat data with PowerSync in one journey view.",
             src="Analysis deck, Sep 2026. Figures blurred."),
        dict(title="Lead lifecycle funnel", tool="HTML", imgs=["funnel"],
             what="Lead status from New to Delivered, with a required reason code for every lost lead.",
             xyz="Found that about 44% of lost leads came from three internal causes that need no extra ad budget, measured with a reason code at each funnel status, by defining the funnel from New to Delivered with a definition of done for every step.",
             src="Analysis deck, Sep 2026. Figures blurred."),
    ]),
]


def build(b):
    T, t, E, P = b.T, b.t, b.E, b.P
    sections = []
    for gi, (name, intro, items) in enumerate(GROUPS):
        cards = []
        for it in items:
            imgs = "".join(
                f'<a href="{P}assets/img/docs/{k}.jpg" target="_blank" rel="noopener">'
                f'<img src="{P}assets/img/docs/{k}.jpg" alt="{E(t(it["title"]))}" loading="lazy" decoding="async"></a>'
                for k in it["imgs"])
            pair = " doc-shot--pair" if len(it["imgs"]) > 1 else ""
            cards.append(f"""<article class="doc-item">
  <div class="doc-shot{pair}">{imgs}</div>
  <div class="doc-copy">
    <div class="lab-top"><h3>{T(it['title'])}</h3><span class="chip">{E(it['tool'])}</span></div>
    <p>{T(it['what'])}</p>
    <p class="doc-impact"><span class="mono">{T("Impact (X-Y-Z)")}</span>{T(it['xyz'])}</p>
    <p class="note">{T(it['src'])}</p>
  </div>
</article>""")
        sections.append(f"""<section class="section" aria-labelledby="docs-g{gi}">
  <div class="section-head"><span class="eyebrow">{T("Documentation")} · 0{gi + 1}</span><h2 id="docs-g{gi}">{T(name)}</h2><p>{T(intro)}</p></div>
  <div class="doc-grid">{''.join(cards)}</div>
</section>""")
    body = f"""
<div class="wrap">
  <p class="crumbs"><a href="index.html">{T("Home")}</a> / {T("Documentation")}</p>
  <header class="case-head">
    <div>
      <span class="tag d-ba">{b.wire('ba')}<span>{T("Documentation")}</span></span>
      <h1>{T("The work, as it looks on screen")}</h1>
      <p class="xyz">{T("These are real screenshots of the systems, dashboards and analysis behind my case studies. I blurred company figures, customer names and competitor names. Public statistics stay readable.")}</p>
    </div>
    <dl class="case-facts">
      <div><dt>{T("How to read it")}</dt><dd>{T("Each item says what it is, then its impact in Google's X-Y-Z form: what changed, how it was measured and how I did it.")}</dd></div>
      <div><dt>{T("Tools")}</dt><dd>Laravel · MySQL · Power BI · Python · HTML</dd></div>
      <div><dt>{T("Full image")}</dt><dd>{T("Click any screenshot to open it at full size.")}</dd></div>
    </dl>
  </header>
  {''.join(sections)}
</div>"""
    b.page("docs.html", t("Documentation") + " · Reyza Agung Gunawan",
           t("Screenshots of the PowerSync platform, Power BI dashboards and Python analysis by Reyza Agung Gunawan, with company figures blurred."),
           body, active="docs")
