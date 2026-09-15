"""Build the portfolio site in English and Indonesian.

English content lives in this file; Indonesian translations live in i18n_id.py, keyed by
the exact English text. Edit both, then run from the repo root:

    python site-src/build.py

Writes the English pages into the repo root and the Indonesian pages into id/.
The build lists any English string that has no Indonesian translation yet.
Every figure traces to a Verified evidence item (IDs listed per case) or to the
PowerSync git history. Keep it that way: do not add a number you cannot show.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_id import ID  # noqa: E402
import powersync_page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://reyzasagara.github.io/nicetomeetyou/"
CV_PDF = "assets/Reyza-Agung-Gunawan-CV.pdf"

E = html.escape

LANG = "en"
P = ""  # path prefix back to the repo root ("" for English, "../" for Indonesian)
MISSING = set()


def t(s):
    """Translate an English string for the current language."""
    if LANG == "en":
        return s
    value = ID.get(s)
    if value is None:
        if re.search(r"[A-Za-z]{2,}", s) and not re.fullmatch(r"BA\d\d-E\d\d", s):
            MISSING.add(s)
        return s
    return value


def T(s):
    return E(t(s))


PERSON = {
    "name": "Reyza Agung Gunawan",
    "location": "Cikarang, Bekasi, Indonesia",
    "email": "reyzacomm@gmail.com",
    "linkedin": "https://www.linkedin.com/in/reyzaag/",
    "github": "https://github.com/Reyzasagara",
}

LEVELS = {
    1: "Foundation",
    2: "Working knowledge",
    3: "Independent",
    4: "Advanced",
    5: "Lead-capable",
}

# --------------------------------------------------------------------------- domains

DOMAINS = [
    {
        "id": "ba",
        "slug": "business-analysis",
        "name": "Business Analysis",
        "role": "Core",
        "summary": "Turning how work really happens into requirements a system can enforce.",
        "overview": "I start with how the work really happens: the paper form, the WhatsApp message, the spreadsheet only one admin understands. Then I turn it into requirements, rules and data a system can enforce.",
        "competencies": [
            ("Process mapping, as-is to to-be", 4, "Drew before-and-after swimlanes of the faktur request in the Dec 2024 proposal, then mapped number control, PO-to-delivery and claims.", "powersync-dealer"),
            ("Requirements and traceability", 4, "Kept a traceability matrix that links 16 requirements to SRS items, UAT scenarios and evidence.", "powersync-dealer"),
            ("Business rules and controls", 4, "Layered checks on engine and frame numbers cut off-format numbers from 101 to 25.", "powersync-mes"),
            ("Adoption and change", 3, "15 of 22 dealers were active in May–Jun 2026, and one admin now handles the whole faktur workload.", "powersync-dealer"),
            ("Changing course based on evidence", 3, "Tried bulk faktur processing on 38 requests and dropped it after two weeks.", "powersync-dealer"),
            ("Funnel and CRM gap analysis", 3, "Found that 54 of 328 WhatsApp conversations in one week never got a reply.", "digital-growth"),
        ],
        "tools": [
            ("BPMN 2.0 and swimlane flowcharts", "Drawing processes.", "I draw the current process from real forms first, then the new one, so every requirement points to a step that changes."),
            ("Requirements traceability matrix", "Linking requirement, specification, test and evidence.", "I use it to show a feature is done using real system data."),
            ("MySQL Workbench and XMind", "Data models and scope maps.", "Mind maps for scope and status lifecycles, then an ERD the build follows."),
            ("Laravel", "The framework PowerSync runs on.", "I build and adjust the workflows myself, so requirements and delivery stay in the same loop."),
        ],
        "steps": [
            "Understand what the business needs",
            "Talk to the people doing the work",
            "Map the current process from real documents",
            "Find where errors and delays start",
            "Design the new workflow",
            "Turn it into requirements and rules",
            "Get business and tech teams on the same page",
            "Test with UAT and real system data",
            "Measure adoption and results",
            "Keep improving, including removing what doesn't work",
        ],
        "primary": "powersync-dealer",
        "supporting": ["powersync-mes", "digital-growth"],
        "related": ["ops", "ai", "mkt"],
    },
    {
        "id": "ai",
        "slug": "ai-orchestration",
        "name": "AI Orchestration",
        "role": "What sets me apart",
        "summary": "Putting AI where rules fall short, with a person making the final call.",
        "overview": "I use AI where fixed rules can't cope, like handwriting, free-text chats or messy evidence, and I keep a person at the point where decisions are made. Most of this is recent, so I show it as a lab and say honestly where each project stands.",
        "competencies": [
            ("Human-in-the-loop design", 3, "The AI sales assistant writes the draft; a person approves it before any customer sees it.", "lab"),
            ("Working when AI is off", 3, "Production keeps running when AI is switched off or its quota runs out.", "lab"),
            ("Grounding claims in evidence", 3, "Checked 53 evidence items against the source files and dropped every claim the files didn't support.", "lab"),
            ("AI-assisted development", 3, "Built PowerSync with an AI pair programmer: 1,043 commits between Oct 2025 and Sep 2026.", "powersync-mes"),
            ("Governing AI use", 2, "One control point that switches on, switches off and meters AI use for every module.", "lab"),
        ],
        "tools": [
            ("Claude Code and MCP tools", "Agent-based coding and tool orchestration.", "I plan the change, let the agent do the work, and review every diff and every claim before it goes in."),
            ("Vision and speech models", "Reading images and voice.", "They turn handwritten QC forms and spoken findings into structured problem lists."),
            ("Knowledge base and persona prompts", "Context for a chat assistant.", "Product facts and tone for the sales assistant, rehearsed before it talks to a customer."),
            ("Supabase with row-level security", "The data layer for FinAI.", "Keeps each user's financial data private from day one."),
        ],
        "steps": [
            "Find work that rules alone can't handle",
            "Split fixed steps from AI steps",
            "Decide what context and sources the AI gets",
            "Design the agent and tool workflow",
            "Add human approval where mistakes are expensive",
            "Decide how to judge the output",
            "Make sure the process still works when AI is off",
            "Tune cost, speed and reliability",
        ],
        "primary": "lab",
        "supporting": ["powersync-mes", "digital-growth"],
        "related": ["ba", "ops"],
    },
    {
        "id": "ops",
        "slug": "operations-digitalization",
        "name": "Operations Digitalization",
        "role": "Strong support",
        "summary": "Capturing data once, at the post where it's created.",
        "overview": "Most unit data starts on the factory floor. I design the posts, kiosks and labels that record it once, at the source, so nobody has to correct it later.",
        "competencies": [
            ("Traceability design", 4, "99.9% of units ordered through PowerSync link to a PO, and 95% of sold units link to a customer.", "powersync-dealer"),
            ("Checking data at the source", 4, "0 mismatches across 217 planned vs stamped number pairs, and 635 units checked by photo.", "powersync-mes"),
            ("Shop-floor kiosks and labels", 3, "Assembly and repair kiosks, with planned numbers printed on QR labels.", "powersync-mes"),
            ("Digital quality workflow", 3, "780 QC inspections recorded against each unit, with NG units sent to the repair post.", "powersync-mes"),
            ("PPIC planning and recap", 3, "PPIC sets parameters and creates a production recap from a phone.", "powersync-mes"),
        ],
        "tools": [
            ("Laravel and MySQL", "Application and data layer.", "Production, QC, repair and delivery records all share one unit identity."),
            ("QR labels and photo capture", "Capturing data at the post.", "The label carries the planned number; the photo proves what was actually stamped."),
            ("Tablet kiosks", "The operator's screen.", "Pick-from-a-list screens, so operators tap instead of type."),
            ("Power BI", "Monitoring.", "Dashboards and weekly KPI notes for management."),
        ],
        "steps": [
            "Walk the line and follow one unit",
            "List every record that gets created or re-typed",
            "Find the post where each value is born",
            "Design the capture: label, photo, scan or list",
            "Add checks at that post",
            "Link every record to one unit identity",
            "Give PPIC and QC a live view",
            "Fix whatever operators keep working around",
        ],
        "primary": "powersync-mes",
        "supporting": ["powersync-dealer", "ev-type-approval"],
        "related": ["ba", "ee", "ai"],
    },
    {
        "id": "mkt",
        "slug": "market-research-data",
        "name": "Market Research & Data Analysis",
        "role": "Supporting",
        "summary": "Finding where demand actually is before we spend money chasing it.",
        "overview": "Before building anything, I want to know where demand actually is. I combine sales, registration, public and search data into models a sales team can act on.",
        "competencies": [
            ("Competitor and regional analysis", 4, "Showed that the market leader sold 75.4% of its units in Java (2022–Aug 2024).", "market-intel"),
            ("Market sizing with stated assumptions", 3, "Built two sizing scenarios for the Strategic Renewal proposal (Sep–Dec 2024).", "market-intel"),
            ("Collecting public data", 3, "BPS regional statistics through a scraper, plus Google Trends and local surveys.", "market-intel"),
            ("BI dashboards", 3, "Power BI dashboards for the three-wheeler market and sales performance.", "market-intel"),
            ("Customer research", 3, "A 349-response survey, focus groups, car clinics and a customer journey map.", "market-intel"),
            ("Search and campaign analysis", 3, "A click-to-WhatsApp campaign that brought 344 conversations at about IDR 4,200 each.", "digital-growth"),
        ],
        "tools": [
            ("Power BI", "Business intelligence and charts.", "I model market, dealer and sales data into dashboards used for planning."),
            ("Excel and SQL", "Cleaning and joining data.", "Registration, sales and public data get joined by region before any chart is drawn."),
            ("Python scraper", "Collecting public data.", "Pulled BPS regional statistics to score areas."),
            ("GA4, Search Console, Meta Ads", "Digital performance.", "I follow traffic, search queries and campaign cost all the way to conversations."),
        ],
        "steps": [
            "Write down the business question",
            "List the sources and where they came from",
            "Clean and join by region and period",
            "Build the model and state the assumptions",
            "Check the conclusion holds in both scenarios",
            "Turn the insight into a recommendation",
            "Hand it to someone who owns the program",
            "Check what changed",
        ],
        "primary": "market-intel",
        "supporting": ["digital-growth"],
        "related": ["ba", "ee"],
    },
    {
        "id": "ee",
        "slug": "electrical-engineering",
        "name": "Electrical Engineering / R&D",
        "role": "Where I started",
        "summary": "Electrical design, testing and type approval for an electric vehicle.",
        "overview": "This is where I started: the electrical design of an electric three-wheeler, its testing and its type approval. I learned how electrical systems fail in real use, and that passing a test doesn't mean the product fits the market.",
        "competencies": [
            ("Type approval preparation", 4, "Prepared the test package and filed the second type test in-house; the SUT certificate was issued in Sep 2023.", "ev-type-approval"),
            ("Validation testing", 3, "25% slope at 800 kg, a 270 mm water test, charging time and range.", "ev-type-approval"),
            ("Wiring harness drawings", 3, "Drew the EV wiring harness for mass production (Jul 2024) and revised it in 2025.", "ev-type-approval"),
            ("Controller commissioning", 3, "Compared Votol, Fardriver and Arduino-based controllers and set up commissioning in the field.", "ev-type-approval"),
            ("Fault investigation", 3, "Pre-test NG findings, a gear indicator fault and electric ATV tests.", "ev-type-approval"),
        ],
        "tools": [
            ("AutoCAD and KiCad", "Harness drawings and schematics.", "Wiring harness drawings and electrical schematics for production."),
            ("Controller software (Votol)", "Motor controller settings.", "Throttle response, current and speed limits tuned to each test result."),
            ("Google Earth elevation profiles", "Planning test routes.", "Picked gradient routes up to 47% before we drove them."),
            ("QC checklists", "Self-checks before the official test.", "Caught NG items before the government test did."),
        ],
        "steps": [
            "Read the regulation and the test items",
            "Test ourselves before the official test",
            "Log every NG and its cause",
            "Fix, retest, document",
            "Submit the test package",
            "Validate on real roads with real loads",
            "Hand the harness drawings to production",
            "Feed field findings back into the design",
        ],
        "primary": "ev-type-approval",
        "supporting": ["powersync-mes"],
        "related": ["ops", "mkt"],
    },
]

DOMAIN = {d["id"]: d for d in DOMAINS}

# --------------------------------------------------------------------------- cases

CASES = [
    {
        "id": "powersync-dealer",
        "domain": "ba",
        "title": "PowerSync: Integrated Dealer Management Platform",
        "short": "PowerSync dealer platform",
        "period": "Proposed Dec 2024 · built from Oct 2025 · live in 2026",
        "role": "Business analyst and delivery lead",
        "tools": "Laravel, MySQL, Power Apps (prototype), Power BI, BPMN 2.0, XMind",
        "xyz": "I connected dealer orders, production, delivery, vehicle registration and claims in one platform that 15 of 22 dealers now use. I got there by mapping the real paper and Excel processes into requirements, rules and data.",
        "figure": ("15/22", "dealers active, May–Jun 2026"),
        "plates": [
            ("15/22", "dealers active on the platform, May–Jun 2026"),
            ("4,818", "unit records, each with its own identity"),
            ("99.9%", "of units ordered through PowerSync linked to a PO"),
            ("1 admin", "handles the whole faktur workload, with peaks of 60–68 a day"),
        ],
        "situation": [
            "PT Dharma Polimetal moved from supplying components to selling its own three-wheelers through dealers. SAP ran the factory, but not the retail side.",
            "Dealer purchase orders, vehicle registration (faktur) requests, free-service coupons and warranty claims lived on paper, in WhatsApp and in personal Excel files. Two admins and a support staff member re-typed the same data, and nobody could trace a unit from order to customer.",
        ],
        "task": "Replace the scattered retail paperwork with one system of record that dealers and internal teams would actually use, and that could trace every unit.",
        "actions": [
            "Proposed a Power Platform pilot covering 12 dealer processes (Dec 2024), with before-and-after flowcharts of the faktur request.",
            "Prototyped the key screens in Power Apps (Jan 2025), then moved to Laravel to get full control of data and permissions.",
            "Mapped the current process from real documents: faktur spreadsheets, paper coupons and warranty forms, dealer PO letters, the production report and the PDI checklist.",
            "Kept a traceability matrix linking 16 requirements to SRS items, UAT scenarios and evidence.",
            "Designed roles and permissions, then tracked adoption every week after go-live.",
            "Tried bulk faktur processing on 38 requests and removed it after two weeks, so each request gets checked before the paid registration step.",
        ],
        "flows": [
            ("Before", "before", ["Dealer fills in Excel", "Sent by email or WhatsApp", "Admin re-types it", "Paper documents", "Report built by hand"]),
            ("After", "after", ["Dealer submits in the portal", "Checked on entry", "Admin approves", "Documents issued", "Live dashboard"]),
        ],
        "results": [
            "15 of 22 dealers were active in May–Jun 2026, and 55 of 73 accounts were active in the last three months.",
            "By Sep 2026 the platform held 141 POs (1,685 units), 4,818 unit records, 442 faktur requests, 175 free-service claims and 780 QC inspections.",
            "One Sales Admin now handles the whole faktur workload, including peaks of 60–68 requests a day.",
            "99.9% of units ordered through PowerSync link to a PO, and 95% of sold units link to a customer record.",
        ],
        "not_claimed": [
            "A percentage of paper removed. There's no paper-versus-digital count to back it.",
            "Time saved per faktur. The proposal's 15 min → 3 min was an estimate, not a measurement.",
            "That older factory records are fully linked to dealer orders.",
        ],
        "lessons": [
            "Most of the gain came from linking order, unit and customer records, which is what lets us trace a unit from PO to buyer.",
            "I removed bulk faktur processing after two weeks because it let wrong data reach the paid registration step. Taking that feature out was the right call.",
        ],
        "evidence": ["BA01-E01", "BA01-E02", "BA01-E03", "BA01-E08", "BA01-E10", "BA01-E11", "BA01-E12", "BA01-E13", "BA01-E14"],
    },
    {
        "id": "powersync-mes",
        "domain": "ops",
        "title": "PowerSync: Manufacturing, PPIC & Shop-Floor Traceability",
        "short": "Manufacturing & traceability",
        "period": "2026",
        "role": "Business analyst and builder",
        "tools": "Laravel, MySQL, QR labels, tablet kiosks, photo capture, vision and speech models",
        "xyz": "Every unit can now be traced from its planned engine and frame number through QC to delivery, with 0 mismatches across 217 planned vs stamped pairs. I designed the kiosks, QR labels and layered number checks that made it work.",
        "figure": ("0/217", "number mismatches, planned vs stamped"),
        "plates": [
            ("101→25", "off-format engine and frame numbers after the checks"),
            ("0/217", "mismatches between planned and stamped numbers"),
            ("635", "units checked by photo at the post"),
            ("780", "QC inspections recorded against the unit"),
        ],
        "situation": [
            "Engine (NOSIN) and frame (NOKA) numbers were planned in spreadsheets, stamped by hand and often found wrong too late: on invoices, on registration documents or after delivery. Across 4,818 unit records, 103 shared 51 engine numbers.",
            "Production reports and PDI checklists were on paper, so PPIC and QC saw the line a day late.",
        ],
        "task": "Catch number errors at the post where they happen, and give PPIC and QC a live view of the line.",
        "actions": [
            "Planned frame numbers at recap time, skipping numbers already used.",
            "Designed kiosks for the assembly and repair posts: a photo of the stamped number, and problem lists to pick from instead of typing.",
            "Added format checks plus a normalised duplicate check (O vs 0, spacing) that catches duplicates exact matching misses.",
            "Printed the planned numbers on QR labels for the line.",
            "Moved QC from a paper checklist to inspections recorded against each unit, with NG units sent through the repair post.",
            "Let PPIC set parameters and create a production recap from a phone. Later added AI that reads handwritten QC forms, while production carries on if the AI is off.",
        ],
        "flows": [
            ("Unit flow", "after", ["Plan numbers", "Stamp at the post", "Kiosk photo and format check", "Duplicate re-check", "QC inspection", "Repair post if NG", "Delivery linked to PO"]),
        ],
        "results": [
            "Off-format numbers dropped from 101 to 25 in one scan, with no exact duplicates left.",
            "0 mismatches across 217 planned vs stamped pairs, and 635 units checked by photo.",
            "780 QC inspections recorded; the production report and PDI checklist are no longer on paper.",
            "A split PO stays one record: a 4-unit PO shipped on two delivery reports three weeks apart still shows partial delivery against each unit.",
        ],
        "not_claimed": [
            "Uniqueness enforced by the database. Engine numbers are still only checked in the application.",
            "A shorter cycle time. It hasn't been measured yet.",
            "Accuracy figures for the AI form reading.",
        ],
        "lessons": [
            "A check at the kiosk takes a few seconds. The same wrong number found at registration means a reissued document and a customer left waiting.",
            "I built the AI steps so production keeps running when the AI is off or out of quota. The line can't stop and wait for a model.",
        ],
        "evidence": ["BA01-E05", "BA01-E06", "BA01-E07", "BA01-E09", "BA01-E14", "PowerSync git history, Aug–Sep 2026"],
    },
    {
        "id": "digital-growth",
        "domain": "mkt",
        "title": "PowerAce Digital Growth System",
        "short": "Digital growth system",
        "period": "Jul–Sep 2026",
        "role": "Started it, analysed it and built it",
        "tools": "Next.js, Laravel API, CI security scanning, OWASP ZAP, GTM, GA4, Search Console, Meta Ads",
        "xyz": "I took a vendor-built website with serious security flaws and made it a company-controlled, measurable source of leads, raising our self-assessed security score from 28 to 78/100. That meant auditing, rebuilding and instrumenting the site, then mapping the path from ad to dealer.",
        "figure": ("28→78", "self-assessed security score"),
        "plates": [
            ("28→78", "self-assessed security score, weighted by OWASP"),
            ("85", "redirects that brought search traffic back after the move"),
            ("344", "WhatsApp conversations from IDR 1.44 million"),
            ("54/328", "conversations in one week that never got a reply"),
        ],
        "situation": [
            "A vendor built and controlled the company website. It ran on an end-of-life framework with debug mode on and an unsafe upload path, and it showed signs of spam abuse.",
            "Marketing couldn't see which visits turned into conversations, or what happened to those conversations afterwards.",
        ],
        "task": "Bring the site in-house, make it secure and measurable, and connect visitors to the dealers who close the sale.",
        "actions": [
            "Started the move in-house (Jul 2026) and audited the old site (OWASP ZAP: 2 High and 3 Medium alert types).",
            "Rebuilt it as a company-controlled Next.js front end with a Laravel API, documented architecture and CI security scanning, and retired the old admin login.",
            "Set up Google Tag Manager, GA4 events, Search Console and Bing verification, and brought search traffic back after the domain move with 85 redirects.",
            "Planned SEO content: a question map by search intent, a brand brief and a CMS workflow.",
            "Ran a click-to-WhatsApp campaign and mapped the path from ad to WhatsApp to dealer to PO.",
        ],
        "flows": [
            ("The system", "after", ["Audit", "Rebuild", "Measure", "Content", "Campaign", "Funnel gap", "AI follow-up design"]),
        ],
        "results": [
            "The High and Medium findings from the old scan couldn't be reproduced on the new stack; the self-assessed security score rose from 28 to 78/100.",
            "The new homepage scored 73/100 for SEO health and 0 for mobile CLS in lab tests (Aug 2026).",
            "The campaign brought in 344 conversations for IDR 1.44 million, about IDR 4,200 each.",
            "In one week, 54 of 328 conversations never got a reply and 30 were lost because no dealer covered the area. That became the brief for an AI sales follow-up with human approval.",
        ],
        "not_claimed": [
            "An external security audit. The score is a self-assessment.",
            "Ranking gains from the content plan. Not measured yet.",
            "Deals won from the campaign. The funnel isn't tracked through to closed sales.",
        ],
        "lessons": [
            "The expensive gap turned out to be 54 unanswered conversations a week. Fixing that is a sales process job, so it became the brief for the AI follow-up.",
            "I did the security fixes and the tracking setup in the same rebuild, so the traffic numbers now come from a site the company controls.",
        ],
        "evidence": ["BA02-E01", "BA02-E03", "BA02-E04", "BA02-E05", "BA02-E06", "BA02-E07", "BA02-E08", "BA02-E10", "BA02-E11", "BA02-E13"],
    },
    {
        "id": "market-intel",
        "domain": "mkt",
        "title": "3W Market Intelligence & Demand Modelling",
        "short": "Market intelligence",
        "period": "2024–2026",
        "role": "Market research analyst, alongside engineering from 2024",
        "tools": "Power BI, Excel, Python scraper, BPS data, Google Trends, surveys",
        "xyz": "I helped steer dealer expansion toward proven demand by showing that the market leader sold 75.4% of its units in Java (2022–Aug 2024). The work behind it: a market dataset, sizing scenarios and a regional whitespace score.",
        "figure": ("75.4%", "of the leader's units sold in Java"),
        "plates": [
            ("75.4%", "of the market leader's units sold in Java, 2022–Aug 2024"),
            ("~25%", "of the market was in the areas we had been expanding into"),
            ("14", "data sources, each logged with where it came from"),
            ("349", "survey responses behind the customer needs"),
        ],
        "situation": [
            "The company went into retail three-wheelers without its own market data. Dealer expansion was opportunistic, and a lot of it went to areas far from the factory.",
        ],
        "task": "Answer one question with data: where is the Indonesian three-wheeler market really, and where are the best opportunities?",
        "actions": [
            "Wrote the Strategic Renewal proposal (Sep–Dec 2024) with two market-sizing scenarios and their assumptions spelled out.",
            "Kept a register of 14 data sources, each flagged with where it came from.",
            "Collected public data (BPS regional statistics through a scraper, Google Trends and local surveys) to score pilot areas.",
            "Built a whitespace score (registration gap × regional GDP × access) and Power BI dashboards for market and sales performance.",
            "Grounded customer needs in a 349-response survey, focus groups, car clinics and a customer and dealer journey map.",
        ],
        "flows": [
            ("Analysis flow", "after", ["Business question", "Sources", "Cleaning", "Model", "Insight", "Recommendation", "Program"]),
        ],
        "results": [
            "Our expansion had targeted areas holding about 25% of the market, while the leader sold 75.4% of its units in Java.",
            "The 2025 plan adopted a Java dealer focus, an exclusive-dealer scheme and a digitalization objective.",
            "The recommendations turned into programs: events in five competitor strongholds, a dealership tier program, a sub-dealer SOP, and the digitalization objective that became PowerSync.",
        ],
        "not_claimed": [
            "Market share or sales gains from these programs. Their commercial effect hasn't been measured.",
            "A full sensitivity analysis beyond the two sizing scenarios.",
        ],
        "lessons": [
            "The Java conclusion held in both sizing scenarios, so it didn't depend on which market-size estimate turned out to be right.",
            "The analysis turned into real work once each recommendation had an owner, such as the dealer scheme and the platform.",
        ],
        "evidence": ["BA03-E01", "BA03-E02", "BA03-E03", "BA03-E04", "BA03-E05", "BA03-E06", "BA03-E07", "BA03-E08", "BA03-E09", "BA03-E10"],
    },
    {
        "id": "ev-type-approval",
        "domain": "ee",
        "title": "EV Type Approval & Validation: PowerAce TRIEX",
        "short": "EV type approval",
        "period": "2022–2024",
        "role": "Electrical design engineer",
        "tools": "Votol controller software, AutoCAD, QC checklists, Google Earth elevation profiles",
        "xyz": "I handled the electrical side of an imported electric three-wheeler prototype and prepared its type approval, which ended with a government certificate (SUT, Sep 2023). That included fixing what failed our own pre-test, putting together the test package and filing the second type test in-house.",
        "figure": ("SUT", "type approval, Sep 2023"),
        "plates": [
            ("SUT", "type-approval certificate issued 15 Sep 2023"),
            ("25%", "slope test passed with an 800 kg load"),
            ("270 mm", "water test, everything still working"),
            ("59 km", "range, with a full charge in 4 h 35 min"),
        ],
        "situation": [
            "After the company's IPO, the three-wheeler business was a way to show it could do more than supply components. There was an imported electric prototype, but it wasn't ready for production and had no type approval.",
        ],
        "task": "Get the prototype's electrical system ready and take the vehicle through government type approval.",
        "actions": [
            "Ran our own pre-test (14 Mar 2023), which found NG items (gear indicator, parking sensor, cover rubber) before the official test could.",
            "Prepared the test package: QC self-assessment, SNI 8872 battery test and specifications.",
            "Filed the second type test and paid the government fee in-house (IDR 9.7 million, Jun 2023).",
            "Compared EV controllers (Votol, Fardriver, Arduino-based) and set up commissioning in the field using the supplier's guide.",
            "Planned road tests with Google Earth gradient profiles, then ran slope, water, charging and range tests.",
            "Drew the EV wiring harness for mass production (Jul 2024).",
        ],
        "flows": [
            ("Certification path", "after", ["Prototype", "Own pre-test: NG", "Fix", "Test package", "Type test", "Certificate", "Road tests", "Harness drawing"]),
        ],
        "results": [
            "SUT type-approval certificate issued 15 Sep 2023.",
            "Passed a 25% slope test with 800 kg and a 270 mm water test with everything still working.",
            "Full charge in 4 h 35 min and a 59 km range (Jun 2024).",
            "Mass-production harness drawing released Jul 2024 and revised in 2025.",
        ],
        "not_claimed": [
            "A first-attempt pass score.",
            "Savings compared with consultant fees. The evidence shows a direct government fee.",
            "Finished tests on the 37% and 47% gradient routes. They were planned.",
            "Writing the controller commissioning guide. It's the supplier's document.",
            "The frame and body design. That was my team's work; my part was the electrical system.",
        ],
        "lessons": [
            "Passing type approval didn't mean the product fit the market. At two to four times the price of competing EVs, with a 59 km range, it didn't yet do the job most buyers needed, and that's why I moved into market research.",
        ],
        "evidence": ["BA04-E01", "BA04-E02", "BA04-E03", "BA04-E04", "BA04-E05", "BA04-E06", "BA04-E07", "BA04-E09", "BA04-E13"],
    },
]

CASE = {c["id"]: c for c in CASES}

# --------------------------------------------------------------------------- lab

LAB = [
    {
        "title": "AI on the shop floor",
        "status": ("live", "Live in PowerSync"),
        "body": "Vision AI reads handwritten QC forms and turns them into named problem lists, and QC findings can be recorded by voice. Production keeps going when AI is off or out of quota, and a single control point meters AI use for every module.",
        "note": "Shipped Aug–Sep 2026. Accuracy isn't measured yet.",
    },
    {
        "title": "AI Sales Engine",
        "status": ("build", "In build"),
        "body": "Built to close the gap of 54 unanswered conversations a week. The assistant has a persona and a product knowledge base, practises conversations before any customer sees one, and a person approves its replies.",
        "note": "Started Sep 2026. No results yet.",
    },
    {
        "title": "Career evidence assistant",
        "status": ("done", "Done for this site"),
        "body": "Turned 1,026 work records into four main case studies and 53 evidence items. Every claim was checked against source files, nothing was marked verified without my approval, and anything the files didn't support was dropped.",
        "note": "Every figure on this site went through that process.",
    },
    {
        "title": "FinAI",
        "status": ("build", "V0: ledger"),
        "body": "A personal finance system built on one rule: a human confirms, AI does the work. V0 is a manual ledger on React and Supabase with row-level security; AI categorisation comes next.",
        "note": "No AI calls yet, on purpose.",
    },
]

AI_CASE_STANDARD = [
    "The business problem",
    "Why normal automation isn't enough",
    "Which decisions need AI",
    "The context and data the AI gets",
    "Prompt, agent and tool design",
    "Where a human approves",
    "Failure handling and guardrails",
    "How the output is judged",
    "Cost, speed and accuracy",
    "A measured result",
]

TIMELINE = [
    ("Dec 2021", "Joined PT Dharma Polimetal as an electrical design engineer in the three-wheeler division", "ee"),
    ("Sep 2023", "Electric three-wheeler gets government type approval (SUT)", "ee"),
    ("Jul 2024", "Mass-production EV wiring harness drawing released", "ee"),
    ("2024", "Started market analysis alongside engineering; built Power BI market dashboards", "mkt"),
    ("Dec 2024", "Strategic Renewal proposal: market focus and the PowerSync pilot", "ba"),
    ("Jan 2025", "Prototyped PowerSync in Power Apps", "ba"),
    ("Oct 2025", "Started building PowerSync on Laravel", "ops"),
    ("2026", "Became Marketing Research Analyst, 3W division", "mkt"),
    ("May–Jun 2026", "15 of 22 dealers active on PowerSync", "ba"),
    ("Jul–Aug 2026", "Brought the company website in-house and rebuilt it", "mkt"),
    ("Sep 2026", "AI on the shop floor; AI Sales Engine in build", "ai"),
]

EVOLUTION = [
    ("2021–2023", "Electrical engineering", "How do I get the EV's electrical system working and through type approval?", "ee"),
    ("2024", "Market insight", "Who actually needs it, and where are they?", "mkt"),
    ("Dec 2024–2025", "Business analysis", "Why is everything behind a sale still on paper?", "ba"),
    ("2025–2026", "Operations digitalization", "How do we capture the facts right where they happen?", "ops"),
    ("2026", "AI orchestration", "What can AI do safely, with a person making the final call?", "ai"),
]

# --------------------------------------------------------------------------- helpers


def domain_href(d):
    return f"domain-{d['slug']}.html"


def case_href(case_id):
    if case_id == "lab":
        return "lab.html"
    return f"work-{case_id}.html"


def case_name(case_id):
    if case_id == "lab":
        return t("Portfolio Lab")
    return t(CASE[case_id]["short"])


def wire(domain_id):
    return f'<span class="wire d-{domain_id}" aria-hidden="true"></span>'


def domain_tag(d):
    return f'<span class="tag d-{d["id"]}">{wire(d["id"])}<span>{T(d["name"])}</span></span>'


def project_visual(case_id):
    """Public-safe diagrams drawn from the case evidence, never application screenshots."""
    if case_id == "powersync-dealer":
        return f'''<div class="project-visual visual-platform" role="img" aria-label="{T("PowerSync workflow: dealer order, production, delivery, customer and after-sales")}">
          <div class="mini-window"><div class="window-top"><span class="mini-brand">P<span>owerSync</span></span><span>{T("Connected operations")}</span><i></i></div>
          <div class="window-content"><div class="window-sidebar"><b>{T("Overview")}</b><span>{T("Dealer orders")}</span><span>{T("Production")}</span><span>{T("Delivery")}</span><span>{T("After-sales")}</span></div>
          <div class="window-main"><span class="visual-label">{T("ONE CONNECTED WORKFLOW")}</span><h4>{T("Order to customer in one record.")}</h4><div class="mini-stats"><div><b>15/22</b><span>{T("active dealers")}</span></div><div><b>{T("4,818")}</b><span>{T("unit records")}</span></div></div><div class="workflow-nodes"><span>{T("Order")}</span><i>→</i><span>{T("Build")}</span><i>→</i><span>{T("Deliver")}</span></div><div class="mini-rule"></div><span class="visual-caption">{T("One unit identity at every step.")}</span></div></div></div>
          <span class="visual-foot">{T("Workflow illustration")} · BA01-E01 / E02 / E08</span></div>'''
    if case_id == "powersync-mes":
        return f'''<div class="project-visual visual-production" role="img" aria-label="{T("Production check: 217 planned vs stamped pairs, zero mismatches")}"><div class="production-card"><div class="visual-label">{T("PRODUCTION · VALIDATION")}</div><h4>{t("Numbers checked<br>at the post.")}</h4><div class="production-flow"><span>{T("Plan")}</span><i>→</i><span>{T("Stamp")}</span><i>→</i><span>{T("Check")}</span></div><div class="validation"><span class="checkmark">✓</span><div><b>{T("217 pairs. 0 mismatches.")}</b><small>{T("Planned vs stamped unit numbers")}</small></div></div></div><span class="visual-foot">{T("Control summary")} · BA01-E07</span></div>'''
    if case_id == "market-intel":
        return f'''<div class="project-visual visual-market" role="img" aria-label="{T("Market leader sales, 2022 to August 2024: Java 75.4 percent, other regions 24.6 percent")}"><div class="chart-card"><span class="visual-label">{T("WHERE DEMAND IS")}</span><h4>{T("Where the market leader sells.")}</h4><div class="bar-row"><span>{T("Java")}</span><div><i style="width:75.4%"></i></div><b>{T("75.4%")}</b></div><div class="bar-row"><span>{T("Other")}</span><div><i style="width:24.6%"></i></div><b>{T("24.6%")}</b></div><small>{T("Market leader unit sales · 2022–Aug 2024")}</small></div><span class="visual-foot">{T("Evidence summary")} · BA03-E03</span></div>'''
    if case_id == "digital-growth":
        return f'''<div class="project-visual visual-growth" role="img" aria-label="{T("Digital growth path: discover, engage, then start a conversation")}"><div class="growth-card"><span class="visual-label">{T("ONE CONNECTED CUSTOMER JOURNEY")}</span><h4>{T("From ad to dealer.")}</h4><div class="growth-bars"><span>01 <b>{T("Discover")}</b><small>{T("Search & content")}</small></span><span>02 <b>{T("Engage")}</b><small>{T("Website & campaign")}</small></span><span>03 <b>{T("Converse")}</b><small>{T("WhatsApp & CRM")}</small></span></div></div><span class="visual-foot">{T("Journey illustration")} · BA02-E07 / E08</span></div>'''
    return f'''<div class="project-visual visual-engineering" role="img" aria-label="{T("EV electrical work: wiring, testing, fixes and type approval in September 2023")}"><div class="engineering-card"><span class="visual-label">{T("ELECTRICAL ENGINEERING")}</span><h4>{t("Electrical design<br>to type approval.")}</h4><div class="engineering-line"><span>{T("Wiring")}</span><i>→</i><span>{T("Test")}</span><i>→</i><span>{T("Fix")}</span></div><div class="approval-stamp"><b>SUT</b><span>{t("Type approval<br>September 2023")}</span></div></div><span class="visual-foot">{T("Lifecycle summary")} · BA04-E01 / E14</span></div>'''


def project_card(c, featured=False):
    d = DOMAIN[c["domain"]]
    return f'''<article class="project-card{' featured' if featured else ''}" data-domain="{d['id']}" style="view-transition-name:case-{c['id']}">
      <a href="{case_href(c['id'])}" aria-label="{T('Read case study')}: {T(c['short'])}">
        {project_visual(c['id'])}
        <div class="project-copy">{domain_tag(d)}<h3>{T(c['title'])}</h3><p>{T(c['xyz'])}</p>
        <div class="project-bottom"><span>{T(c['figure'][0])} <small>{T(c['figure'][1])}</small></span><span class="read">{T('Read the case study')} <span aria-hidden="true">↗</span></span></div></div>
      </a></article>'''


def level(n, domain_id):
    dots = "".join(f'<i class="{"on" if i <= n else ""}"></i>' for i in range(1, 6))
    label = E(t("Level {n} of 5, {name}").format(n=n, name=t(LEVELS[n])))
    return f'<span class="d-{domain_id}"><span class="level" role="img" aria-label="{label}">{dots}</span><span class="level-name">{n} · {T(LEVELS[n])}</span></span>'


def plate(value, label):
    return f'<div class="plate"><b>{T(value)}</b><small>{T(label)}</small></div>'


def flow(label, kind, steps, domain_id):
    items = "".join(f'<li><span class="step"><small>{i:02d}</small>{T(s)}</span></li>' for i, s in enumerate(steps, 1))
    return f'<div><p class="mono flow-label">{T(label)}</p><ol class="flow {kind} d-{domain_id}">{items}</ol></div>'


def nav(active):
    links = [
        ("index.html#work", "Work", "work"),
        ("powersync.html", "PowerSync", "powersync"),
        ("index.html#domains", "Roles", "domains"),
        ("lab.html", "Lab", "lab"),
        ("index.html#about", "About", "about"),
        ("cv.html", "CV", "cv"),
    ]
    out = []
    for href, label, key in links:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{cur}>{T(label)}</a>')
    return "".join(out)


def lang_switch(filename):
    if LANG == "en":
        en_href, id_href = filename, "id/" + filename
    else:
        en_href, id_href = "../" + filename, filename
    en_cur = ' aria-current="true"' if LANG == "en" else ""
    id_cur = ' aria-current="true"' if LANG == "id" else ""
    return (
        f'<nav class="lang-switch" aria-label="{T("Language")}">'
        f'<a href="{en_href}" hreflang="en" lang="en"{en_cur} title="Read in English">EN</a>'
        f'<a href="{id_href}" hreflang="id" lang="id"{id_cur} title="Baca dalam Bahasa Indonesia">ID</a>'
        f"</nav>"
    )


def page(filename, title, description, body, active="", extra_head="", body_class=""):
    tail = "" if filename == "index.html" else filename
    en_url = SITE_URL + tail
    id_url = SITE_URL + "id/" + tail
    canonical = en_url if LANG == "en" else id_url
    doc = f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="id" href="{id_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'en_US' if LANG == 'en' else 'id_ID'}">
<meta property="og:image" content="{SITE_URL}assets/img/og-card.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f0f1f2">
<meta name="view-transition" content="same-origin">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;650;700;750;800&display=swap">
<link rel="stylesheet" href="{P}assets/presentation.css">
{extra_head}
</head>
<body class="{body_class}">
<a class="skip" href="#main">{T("Skip to content")}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">r.</span><span>reyza<span class="brand-light">gunawan</span></span></a>
    <nav class="nav" id="main-nav" aria-label="{T('Main')}">{nav(active)}</nav>
    {lang_switch(filename)}
    <a class="header-contact" href="index.html#contact">{T("Let's talk")} <span aria-hidden="true">↗</span></a>
    <button class="icon-btn menu-btn" type="button" data-menu-toggle aria-expanded="false" aria-controls="main-nav" aria-label="{T('Open menu')}" data-label-open="{T('Open menu')}" data-label-close="{T('Close menu')}">{T("Menu")} <span aria-hidden="true">☰</span></button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 {E(PERSON['name'])}<small>{T("Professional portfolio · September 2026")}</small></span>
    <span><a href="mailto:{PERSON['email']}">{T("Email")}</a> · <a href="{PERSON['linkedin']}">LinkedIn</a> · <a href="{PERSON['github']}">GitHub</a></span>
  </div>
</footer>
<script src="{P}assets/site.js" defer></script>
</body>
</html>
"""
    out_dir = ROOT if LANG == "en" else os.path.join(ROOT, "id")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)
    print("wrote", ("" if LANG == "en" else "id/") + filename)


# --------------------------------------------------------------------------- home


def build_home():
    hero = f"""
<section class="hero wrap paper" aria-labelledby="hero-name">
  <div class="hero-copy">
    <span class="eyebrow"><span class="tiny-line"></span> Reyza Agung Gunawan · {T("Portfolio 2026")}</span>
    <h1 id="hero-name">{t("I turn paper processes<br><span>into working systems.</span>")}</h1>
    <p class="hero-role">{T("A business analyst who also builds.")}</p>
    <p class="lede">{T("I've worked at PT Dharma Polimetal in Cikarang for more than four years. I started on the electrical design and type approval of an electric three-wheeler. Now I lead PowerSync, the platform that replaced the paper and spreadsheets behind our dealers and production line.")}</p>
    <div class="btn-row">
      <a class="btn btn--solid" href="#work">{T("See my work")} <span aria-hidden="true">↗</span></a>
      <a class="text-link" href="{P}{CV_PDF}">{T("Download CV")} <span aria-hidden="true">↓</span></a>
    </div>
    <p class="hero-location"><span aria-hidden="true">◎</span> {T("Based in Cikarang, Indonesia")}</p>
  </div>
  <figure class="hero-art hero-art--team">
    <span class="art-index">{T("The five roles I work across")}</span>
    <img class="hero-team" src="{P}assets/img/hero-five-personas.jpg" width="1437" height="1073" alt="{T('Illustration of Reyza in five outfits, one for each role: electrical engineer, data analyst, business analyst, AI orchestrator and digital marketing.')}" fetchpriority="high">
    <figcaption><span class="caption-icon" aria-hidden="true">↗</span><span><strong>{T("Business analysis at the core")}</strong><small>{T("Plus AI, operations, market research and electrical engineering.")}</small></span></figcaption>
  </figure>
</section>"""

    proof = f"""
<section class="wrap home-proof" aria-label="{T('Selected results')}">
  <p class="proof-intro">{t("A few numbers<br><strong>I can back up.</strong>")}</p><div class="plates">
    {plate("15/22", "dealers active on PowerSync, May–Jun 2026")}
    {plate("0/217", "mismatches between planned and stamped unit numbers")}
    {plate("SUT", "electric three-wheeler type approval, Sep 2023")}
  </div>
</section>"""

    evo_items = "".join(
        f'<li class="d-{d}"><span class="yr">{T(yr)}</span><h3>{T(stage)}</h3><p>{T(q)}</p></li>'
        for yr, stage, q, d in EVOLUTION
    )
    evolution = f"""
<section class="section evolution-section" aria-labelledby="evo-h">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">04 / {T("How I got here")}</span>
      <h2 id="evo-h">{T("How my work changed")}</h2>
      <p>{T("Each stage started with a problem the stage before it couldn't solve.")}</p>
    </div>
    <ol class="evolution">{evo_items}</ol>
  </div>
</section>"""

    rows = [project_card(c, i == 0) for i, c in enumerate(CASES)]
    work = f"""
<section class="section" id="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="section-head split-head">
      <div><span class="eyebrow">02 / {T("Selected work")}</span><h2 id="work-h">{T("Selected projects")}</h2></div>
      <p>{T("Each case study covers the problem, my part, the results and what I don't claim.")}</p>
    </div>
    <div class="work-filters" role="group" aria-label="{T('Filter selected work')}" hidden>
      <button type="button" data-filter="all" aria-pressed="true">{T("All work")} <span>05</span></button>
      <button type="button" data-filter="ba" aria-pressed="false">{T("Business analysis")}</button>
      <button type="button" data-filter="ops" aria-pressed="false">{T("Operations")}</button>
      <button type="button" data-filter="mkt" aria-pressed="false">{T("Market & growth")}</button>
      <button type="button" data-filter="ee" aria-pressed="false">{T("Engineering")}</button>
    </div>
    <p class="sr-only" data-filter-status data-one="{T('1 case study shown.')}" data-many="{T('{n} case studies shown.')}" aria-live="polite"></p>
    <div class="project-grid">{''.join(rows)}</div>
  </div>
</section>"""

    drows = []
    for i, d in enumerate(DOMAINS, 1):
        drows.append(f"""
      <li class="domain-card d-{d['id']}">
        <a href="{domain_href(d)}">
          <div class="domain-portrait"><span class="domain-number">0{i}</span><img src="{P}assets/img/avatar-{d['id']}.jpg" width="620" height="1000" alt="{E(t("Reyza as {name}").format(name=t(d['name'])))}" loading="lazy"></div>
          <div class="domain-copy"><span class="eyebrow">{T(d['role'])}</span><h3>{T(d['name'])}</h3><p>{T(d['summary'])}</p><span class="read">{T("See this role")} <span aria-hidden="true">↗</span></span></div>
        </a>
      </li>""")
    domains = f"""
<section class="section" id="domains" aria-labelledby="dom-h">
  <div class="wrap">
    <div class="section-head split-head">
      <div><span class="eyebrow">01 / {T("What I do")}</span><h2 id="dom-h">{T("The roles I work in")}</h2></div>
      <p>{T("Business analysis is the core. AI is where I'm heading. Operations, data and engineering are where I learned the job.")}</p>
    </div>
    <ul class="domain-grid">{''.join(drows)}</ul>
  </div>
</section>"""

    lab_items = "".join(
        f"""<article class="lab-item"><div class="lab-top"><h3>{T(x['title'])}</h3><span class="chip chip--{x['status'][0]}">{T(x['status'][1])}</span></div><p>{T(x['body'])}</p></article>"""
        for x in LAB[:2]
    )
    lab = f"""
<section class="section lab-section" aria-labelledby="lab-h">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">03 / {T("Lab")}</span>
      <h2 id="lab-h">{T("AI projects in progress")}</h2>
      <p>{T("AI projects in progress. Each one shows where it stands and what I haven't measured yet.")}</p>
    </div>
    <div class="lab-grid">{lab_items}</div>
    <p style="margin-top:1.5rem"><a class="btn" href="lab.html">{T("See all lab projects")} <span aria-hidden="true">→</span></a></p>
  </div>
</section>"""

    tl = "".join(
        f'<li class="d-{d}" style="--w:var(--w-{d})"><span class="yr">{T(y)}</span><span>{T(x)}</span></li>' for y, x, d in TIMELINE
    )
    about = f"""
<section class="section" id="about" aria-labelledby="about-h">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">05 / {T("About")}</span>
      <h2 id="about-h">{T("Engineer by training, analyst by habit")}</h2>
    </div>
    <div class="about">
      <div>
        <div class="prose">
          <p>{T("I studied mechatronics and joined PT Dharma Polimetal in 2021 as an electrical design engineer. My early work was the electrical side of an electric three-wheeler: wiring, controllers, testing and getting it through government type approval.")}</p>
          <p>{T("Along the way I kept running into problems outside engineering. We didn't know where demand really was, and a lot of the business still ran on paper and re-typed spreadsheets. In 2024 I started market analysis alongside my engineering job, proposed a platform to connect the retail process, and went on to lead PowerSync from requirements to a system that dealers, admins and the production floor use every day.")}</p>
          <p>{T("Today I work as a business analyst who also builds. I map the process, write the rules and ship the workflow. I use AI where it helps, and a person still makes the final call.")}</p>
        </div>
        <dl class="facts">
          <dt>{T("Now")}</dt><dd>{T("Marketing Research Analyst, 3W division, PT Dharma Polimetal Tbk (2026 – present)")}</dd>
          <dt>{T("Before")}</dt><dd>{T("Electrical Design Engineer, 3W R&D (Dec 2021 – 2026)")}</dd>
          <dt>{T("Education")}</dt><dd>{T("Diploma III (D3), Mechatronics Engineering, Politeknik Manufaktur Bandung")}</dd>
          <dt>{T("Certificate")}</dt><dd>{T("Google Data Analytics Professional Certificate (2024)")}</dd>
          <dt>{T("Industry")}</dt><dd>{T("Automotive manufacturing · three-wheelers and EVs · dealer retail")}</dd>
          <dt>{T("Based in")}</dt><dd>{E(PERSON['location'])}</dd>
        </dl>
      </div>
      <div>
        <p class="mono" style="margin-bottom:1rem">{T("Timeline")}</p>
        <ol class="timeline">{tl}</ol>
      </div>
    </div>
  </div>
</section>"""

    contact = f"""
<section class="section" id="contact" aria-labelledby="contact-h">
  <div class="wrap contact">
    <span class="eyebrow">06 / {T("Contact")}</span>
    <h2 id="contact-h">{T("Get in touch")}</h2>
    <p>{T("I'm open to business analyst, digital transformation and product roles.")}</p>
    <a class="big" href="mailto:{PERSON['email']}">{E(PERSON['email'])} <span aria-hidden="true">↗</span></a>
    <div class="btn-row">
      <a class="btn" href="{PERSON['linkedin']}">LinkedIn</a>
      <a class="btn" href="{PERSON['github']}">GitHub</a>
      <a class="btn btn--solid" href="{P}{CV_PDF}">{T("Download CV (PDF)")}</a>
    </div>
  </div>
</section>"""

    person_ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": PERSON["name"],
        "jobTitle": "Business Analyst",
        "url": SITE_URL,
        "image": SITE_URL + "assets/img/reyza-portrait.jpg",
        "email": "mailto:" + PERSON["email"],
        "address": {"@type": "PostalAddress", "addressLocality": "Cikarang", "addressRegion": "West Java", "addressCountry": "ID"},
        "alumniOf": "Politeknik Manufaktur Bandung",
        "worksFor": {"@type": "Organization", "name": "PT Dharma Polimetal Tbk"},
        "sameAs": [PERSON["linkedin"], PERSON["github"]],
    }
    extra = f'<script type="application/ld+json">{json.dumps(person_ld)}</script>'

    page(
        "index.html",
        "Reyza Agung Gunawan",
        t("Business analyst from Cikarang who also builds: a dealer and factory platform, market research, digital growth and EV type approval, with evidence behind every number."),
        hero + proof + domains + work + lab + evolution + about + contact,
        extra_head=extra,
    )


# --------------------------------------------------------------------------- case pages


def build_case(i, c):
    d = DOMAIN[c["domain"]]
    plates = "".join(plate(v, l) for v, l in c["plates"])
    flows = "".join(flow(label, kind, steps, d["id"]) for label, kind, steps in c["flows"])
    situation = "".join(f"<p>{T(p)}</p>" for p in c["situation"])
    actions = "".join(f"<li>{T(a)}</li>" for a in c["actions"])
    results = "".join(f"<li>{T(r)}</li>" for r in c["results"])
    not_claimed = "".join(f"<li>{T(n)}</li>" for n in c["not_claimed"])
    lessons = "".join(f"<p>{T(p)}</p>" for p in c["lessons"])
    codes = "".join(f'<span class="code">{T(x)}</span>' for x in c["evidence"])
    related = [x for x in DOMAINS if x["id"] != d["id"] and (c["id"] == x["primary"] or c["id"] in x["supporting"])]
    related_links = " · ".join(f'<a href="{domain_href(x)}">{T(x["name"])}</a>' for x in [d] + related)
    prev_c = CASES[(i - 1) % len(CASES)]
    next_c = CASES[(i + 1) % len(CASES)]
    ps_link = (
        f'<p class="ps-cta"><a class="btn btn--solid" href="powersync.html">{T("Explore every PowerSync module")} <span aria-hidden="true">↗</span></a></p>'
        if c["id"].startswith("powersync")
        else ""
    )

    body = f"""
<div class="wrap">
  <p class="crumbs"><a href="index.html#work">{T("Work")}</a> / {T(d['name'])}</p>
  <header class="case-head" style="view-transition-name:case-{c['id']}">
    <div>
      {domain_tag(d)}
      <h1>{T(c['title'])}</h1>
      <p class="xyz">{T(c['xyz'])}</p>
    </div>
    <dl class="case-facts">
      <div><dt>{T("Role")}</dt><dd>{T(c['role'])}</dd></div>
      <div><dt>{T("Period")}</dt><dd>{T(c['period'])}</dd></div>
      <div><dt>{T("Tools")}</dt><dd>{T(c['tools'])}</dd></div>
      <div><dt>{T("Roles involved")}</dt><dd>{related_links}</dd></div>
    </dl>
  </header>
  <section aria-label="{T('Key results')}" class="plates" style="margin-bottom:clamp(2.5rem,6vw,4rem)">{plates}</section>
  <section class="case-body section" style="padding-top:clamp(2rem,5vw,3rem)">
    <h2>{T("The situation")}</h2><div>{situation}</div>
    <h2>{T("The goal")}</h2><div><p>{T(c['task'])}</p></div>
    <h2>{T("What I did")}</h2><div><ol>{actions}</ol></div>
    <h2>{T("How it flows")}</h2><div class="flow-group">{project_visual(c['id'])}{flows}</div>
    <h2>{T("What changed")}</h2><div><ul>{results}</ul></div>
    <h2>{T("What I don't claim")}</h2><div><div class="not-claimed"><span class="mono">{T("And why")}</span><ul>{not_claimed}</ul></div></div>
    <h2>{T("What I learned")}</h2><div>{lessons}</div>
    <h2>{T("Evidence")}</h2><div><p style="color:var(--ink-2);margin-bottom:.8rem">{T("Every claim on this page traces to a verified evidence item. The source files are internal company documents, and I'm happy to walk through them in an interview.")}</p><div class="codes">{codes}</div></div>
  </section>
  {ps_link}
  <nav class="pager" aria-label="{T('More case studies')}">
    <a href="{case_href(prev_c['id'])}"><span class="mono">← {T("Previous case")}</span><strong>{T(prev_c['title'])}</strong></a>
    <a href="{case_href(next_c['id'])}"><span class="mono">{T("Next case")} →</span><strong>{T(next_c['title'])}</strong></a>
  </nav>
</div>"""
    page(case_href(c["id"]), t(c["title"]) + " · Reyza Agung Gunawan", t(c["xyz"]), body, active="work")


# --------------------------------------------------------------------------- domain pages


def build_domain(d):
    rows = "".join(
        f"""<tr><td><strong>{T(name)}</strong></td><td>{level(n, d['id'])}</td><td class="muted">{T(ev)}</td><td><a href="{case_href(cid)}">{E(case_name(cid))}</a></td></tr>"""
        for name, n, ev, cid in d["competencies"]
    )
    tools = "".join(
        f'<div class="tool"><h3>{T(x)}</h3><p><strong>{T("Used for:")}</strong> {T(fn)}</p><p><strong>{T("How I use it:")}</strong> {T(how)}</p></div>'
        for x, fn, how in d["tools"]
    )
    steps = "".join(f"<li>{T(s)}</li>" for s in d["steps"])

    def project_row(cid, label):
        if cid == "lab":
            return f'<li class="case-row d-ai"><a href="lab.html"><div class="meta"><span class="mono">{T(label)}</span></div><div><h3>{T("Portfolio Lab")}</h3><p>{T("AI projects with their real status: live, in build or done.")}</p></div><div class="figure"><b>4</b><small>{T("lab projects")}</small></div></a></li>'
        c = CASE[cid]
        v, l = c["figure"]
        cd = DOMAIN[c["domain"]]
        return f'<li class="case-row d-{cd["id"]}"><a href="{case_href(cid)}"><div class="meta"><span class="mono">{T(label)}</span>{domain_tag(cd)}</div><div><h3>{T(c["title"])}</h3><p>{T(c["xyz"])}</p></div><div class="figure"><b>{T(v)}</b><small>{T(l)}</small></div></a></li>'

    projects = project_row(d["primary"], "Main") + "".join(project_row(s, "Supporting") for s in d["supporting"])
    related = " · ".join(f'<a href="{domain_href(DOMAIN[r])}">{T(DOMAIN[r]["name"])}</a>' for r in d["related"])
    scale = " · ".join(f"{n} {t(LEVELS[n])}" for n in range(1, 6))

    body = f"""
<div class="wrap">
  <p class="crumbs"><a href="index.html#domains">{T("Roles")}</a> / {T(d['name'])}</p>
  <header class="case-head domain-head d-{d['id']}">
    <div class="domain-intro">
      <span class="tag d-{d['id']}">{wire(d['id'])}<span>{T(d['role'])}</span></span>
      <h1>{T(d['name'])}</h1>
      <p class="xyz">{T(d['overview'])}</p>
      <a class="btn btn--solid" href="{case_href(d['primary'])}">{T("See the main project")} <span aria-hidden="true">↗</span></a>
    </div>
    <figure class="domain-hero-art"><img src="{P}assets/img/avatar-{d['id']}.jpg" width="620" height="1000" alt="{E(t("Reyza as {name}").format(name=t(d['name'])))}" fetchpriority="high"><figcaption>{T(d['name'])}</figcaption></figure>
  </header>
    <dl class="case-facts domain-facts">
      <div><dt>{T("Main project")}</dt><dd><a href="{case_href(d['primary'])}">{E(case_name(d['primary']))}</a></dd></div>
      <div><dt>{T("Related roles")}</dt><dd>{related}</dd></div>
      <div><dt>{T("Rating scale")}</dt><dd>{E(scale)}</dd></div>
    </dl>
  <section class="section" aria-labelledby="comp-h">
    <div class="section-head"><span class="eyebrow">{T("Skills map")}</span><h2 id="comp-h">{T("Skills and evidence")}</h2></div>
    <div class="table-wrap"><table>
      <thead><tr><th>{T("Skill")}</th><th>{T("Level")}</th><th>{T("Evidence")}</th><th>{T("Project")}</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </section>

  <section class="section" aria-labelledby="tools-h">
    <div class="section-head"><span class="eyebrow">{T("Tools")}</span><h2 id="tools-h">{T("Tools I use")}</h2></div>
    <div class="tools">{tools}</div>
  </section>

  <section class="section" aria-labelledby="team-h">
    <div class="section-head"><span class="eyebrow">{T("On a team")}</span><h2 id="team-h">{T("How I work with a team")}</h2><p>{T("The order I usually work in, from the first conversation to the next round of changes.")}</p></div>
    <ol class="steps">{steps}</ol>
  </section>

  <section class="section" aria-labelledby="proj-h">
    <div class="section-head"><span class="eyebrow">{T("Projects")}</span><h2 id="proj-h">{T("Related projects")}</h2></div>
    <ul class="case-list">{projects}</ul>
  </section>
</div>"""
    page(domain_href(d), t(d["name"]) + " · Reyza Agung Gunawan", t(d["overview"]), body, active="domains")


# --------------------------------------------------------------------------- lab page


def build_lab():
    items = "".join(
        f"""<article class="lab-item"><div class="lab-top"><h3>{T(x['title'])}</h3><span class="chip chip--{x['status'][0]}">{T(x['status'][1])}</span></div><p>{T(x['body'])}</p><p class="note">{T(x['note'])}</p></article>"""
        for x in LAB
    )
    standard = "".join(f"<li>{T(s)}</li>" for s in AI_CASE_STANDARD)
    body = f"""
<div class="wrap">
  <p class="crumbs"><a href="index.html">{T("Home")}</a> / {T("Portfolio Lab")}</p>
  <header class="case-head">
    <div>
      <span class="tag d-ai">{wire('ai')}<span>{T("AI Orchestration")}</span></span>
      <h1>{T("Portfolio Lab")}</h1>
      <p class="xyz">{T("AI projects shown as they really stand. None of them counts as a finished case study until it has a measured result.")}</p>
    </div>
    <dl class="case-facts">
      <div><dt>{T("Principle")}</dt><dd>{T("AI does the work where rules can't. A person signs off wherever a mistake costs money.")}</dd></div>
      <div><dt>{T("Role page")}</dt><dd><a href="domain-ai-orchestration.html">{T("AI Orchestration")}</a></dd></div>
    </dl>
  </header>
  <section class="section" aria-label="{T('Lab projects')}"><div class="lab-grid">{items}</div></section>
  <section class="section" aria-labelledby="std-h">
    <div class="section-head">
      <span class="eyebrow">{T("The bar for a finished AI case")}</span>
      <h2 id="std-h">{T("What a lab project needs before it graduates")}</h2>
      <p>{T("The first project that covers all ten, including a measured result, becomes a full case study.")}</p>
    </div>
    <ol class="steps">{standard}</ol>
  </section>
</div>"""
    page("lab.html", t("Portfolio Lab") + " · Reyza Agung Gunawan", t("AI projects by Reyza Agung Gunawan, shown with their real status: shop-floor AI, an AI sales engine, a career evidence assistant and FinAI."), body, active="lab")


# --------------------------------------------------------------------------- CV page (printed to PDF; the CV itself stays in English)


def build_cv():
    body = f"""
<article class="cv">
  <div class="cv-actions">
    <a class="btn btn--solid" href="{P}{CV_PDF}">{T("Download PDF")}</a>
    <a class="btn" href="index.html">{T("Back to portfolio")}</a>
  </div>
  <h1>{E(PERSON['name'])}</h1>
  <p class="cv-role">Business Analyst · Digital Transformation · EV electrical R&amp;D background</p>
  <p class="cv-contact">{E(PERSON['location'])} · {E(PERSON['email'])} · linkedin.com/in/reyzaag · github.com/Reyzasagara · reyzasagara.github.io/nicetomeetyou</p>

  <h2>Summary</h2>
  <p>Business analyst with 4+ years at PT Dharma Polimetal, moving from EV electrical R&amp;D into market analysis and cross-functional digitalization. Led analysis and delivery of PowerSync, a dealer-to-factory platform used by 15 of 22 active dealers and holding 4,818 unit records. Initiated moving the company website in-house and rebuilt it with security, analytics and SEO in place.</p>

  <h2>Experience</h2>
  <h3>Marketing Research Analyst, 3W Division, PT Dharma Polimetal Tbk <span>2026 – Present</span></h3>
  <h4>PowerSync: dealer, production and after-sales digitalization</h4>
  <ul>
    <li>Led business analysis and delivery of PowerSync, a Laravel platform covering retail steps SAP did not handle; by Sep 2026 it held 141 POs (1,685 units), 4,818 unit records, 442 faktur requests and 780 QC inspections.</li>
    <li>Reached 68.2% dealer adoption (15 of 22 dealers) in May–Jun 2026; 55 of 73 accounts active in the last three months.</li>
    <li>Replaced paper and Excel forms for POs, faktur requests, free-service coupons, warranty claims, PDI checks and production reports; one Sales Admin now handles the full faktur workload, including peaks of 60–68 requests a day.</li>
    <li>Designed layered engine and frame number controls (format checks, normalised duplicate detection and photo validation), cutting off-format numbers from 101 to 25, with 0 mismatches across 217 planned-vs-stamped pairs.</li>
    <li>Built unit traceability from PO to production, delivery and customer: 99.9% of PowerSync-ordered units link to a PO; 95% of sold units link to a customer.</li>
    <li>Mapped AS-IS processes from real forms, kept a requirements traceability matrix (16 requirements → SRS → UAT) and ran weekly post-go-live KPI reporting.</li>
  </ul>
  <h4>Website security and digital growth</h4>
  <ul>
    <li>Initiated moving the vendor-built company website in-house (Jul 2026); audited it (OWASP ZAP: 2 High, 3 Medium) and rebuilt it on Next.js and a Laravel API with CI security scanning, raising the self-assessed security score from 28 to 78/100.</li>
    <li>Set up Google Tag Manager, GA4 events and Search Console; restored search traffic after the domain move with 85 redirects.</li>
    <li>Ran a click-to-WhatsApp campaign: 344 conversations for IDR 1.44 million (about IDR 4,200 each); found 54 of 328 weekly conversations unanswered, the basis for an AI sales follow-up with human approval.</li>
  </ul>

  <h3>Electrical Design Engineer, 3W R&amp;D, PT Dharma Polimetal Tbk <span>Dec 2021 – 2026</span></h3>
  <h4>EV product development</h4>
  <ul>
    <li>Took the PowerAce TRIEX electric three-wheeler through type approval: prepared the test package (pre-test QC self-assessment, SNI 8872 battery test), filed and paid the second type test in-house and obtained the SUT certificate (Sep 2023).</li>
    <li>Drew the mass-production EV wiring harness (Jul 2024) and revised it in 2025.</li>
    <li>Planned road validation with gradient profiles; passed the 25% slope test at 800 kg and a 270 mm water test, with a 4 h 35 min full charge and 59 km range.</li>
    <li>Compared EV controllers (Votol, Fardriver, Arduino-based) and set up field controller commissioning.</li>
  </ul>
  <h4>Market analysis alongside engineering (from 2024)</h4>
  <ul>
    <li>Wrote the Strategic Renewal proposal (Sep–Dec 2024): two stated-assumption market-sizing scenarios; showed expansion had targeted areas holding ~25% of demand; recommended a Java focus, multi-tier dealers, a digital marketing plan and a central data platform.</li>
    <li>Found that 75.4% of the market leader's units sold in Java (2022–Aug 2024), which shaped the 2025 plan.</li>
    <li>Built a 14-source data register, BPS and Google Trends collection, a regional whitespace score and Power BI dashboards.</li>
    <li>Proposed PowerSync as a Power Platform pilot covering 12 dealer processes and prototyped it in Power Apps (Jan 2025) before the Laravel build.</li>
  </ul>

  <h2>Skills</h2>
  <ul>
    <li><strong>Business analysis:</strong> requirements and traceability, process mapping (AS-IS/TO-BE, BPMN 2.0), UAT, KPI reporting, adoption tracking</li>
    <li><strong>Data:</strong> Power BI, Excel, SQL/MySQL, Power Apps, public-data collection, market sizing models</li>
    <li><strong>Digital and AI:</strong> Laravel, Next.js, GA4, Google Tag Manager, Search Console, Meta Ads, OWASP ZAP, CI security scanning, AI-assisted development (Claude Code)</li>
    <li><strong>Engineering:</strong> EV electrical systems, wiring harness design, motor controller commissioning, vehicle type approval (SUT)</li>
  </ul>

  <h2>Education</h2>
  <p>Diploma III (D3) Mechatronics Engineering, Politeknik Manufaktur Bandung, Indonesia</p>
  <p style="margin-top:.4rem">Google Data Analytics Professional Certificate, Google Career Certificates, 2024</p>
</article>"""
    page("cv.html", "CV · Reyza Agung Gunawan", t("CV of Reyza Agung Gunawan, a business analyst with a background in EV electrical R&D."), body, active="cv")


def build_all():
    build_home()
    for i, c in enumerate(CASES):
        build_case(i, c)
    for d in DOMAINS:
        build_domain(d)
    build_lab()
    build_cv()
    powersync_page.build(sys.modules[__name__])


if __name__ == "__main__":
    for lang, prefix in (("en", ""), ("id", "../")):
        LANG, P = lang, prefix
        build_all()
    if MISSING:
        print(f"\n{len(MISSING)} string(s) without an Indonesian translation:")
        for s in sorted(MISSING):
            print("  -", s)
    else:
        print("\nAll strings translated.")
