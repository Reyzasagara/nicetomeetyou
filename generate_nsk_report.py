# -*- coding: utf-8 -*-
"""
NSK Bearings QC Digitalization - Application Intelligence Report
Generated for: Reyza Agung Gunawan
"""

from fpdf import FPDF
import os

# Page: A4 (210x297), margins 15mm each side => effective width = 180mm
MARGIN = 15
EW = 180  # effective width

class ReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "NSK QC Digitalization - Application Intelligence Report | Reyza Agung Gunawan", align="R")
        self.ln(6)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.4)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Confidential | April 2026", align="C")

    def section_title(self, title):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 70, 140)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 204)
        self.line(MARGIN, self.get_y(), 110, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def txt(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(EW, 5, text)
        self.ln(2)

    def bul(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(EW, 5, "  - " + text)

    def bbul(self, label, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(EW, 5, "  - " + label + " " + text)

    def table_header(self, cols):
        """cols = list of (label, width). Sum of widths must be <= EW."""
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(0, 70, 140)
        self.set_text_color(255, 255, 255)
        for label, w in cols:
            self.cell(w, 6, label, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(30, 30, 30)

    def table_row(self, cells, widths, bold=False):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B" if bold else "", 8.5)
        for val, w in zip(cells, widths):
            self.cell(w, 5.5, val, border=1, align="C")
        self.ln()

    def ensure_space(self, h=30):
        if self.get_y() > 297 - MARGIN - h:
            self.add_page()


def build():
    pdf = ReportPDF("P", "mm", "A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(MARGIN, MARGIN, MARGIN)

    # ========== COVER ==========
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(0, 70, 140)
    pdf.cell(0, 14, "Application Intelligence Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 15)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 9, "QC Staff for Digitalization Project", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 9, "PT. NSK Bearings Manufacturing Indonesia", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(0.7)
    pdf.line(65, pdf.get_y(), 145, pdf.get_y())
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    for line in [
        "Prepared for: Reyza Agung Gunawan",
        "Date: April 2026",
        "Document Type: Career Strategy & Research",
    ]:
        pdf.cell(0, 7, line, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "Contents: Company Research | Qualification Match | Salary Benchmark", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Application Answers | Japanese Crash Plan | Interview Strategy | Upskilling", align="C", new_x="LMARGIN", new_y="NEXT")

    # ========== 1. COMPANY OVERVIEW ==========
    pdf.add_page()
    pdf.section_title("1. Company Overview - NSK Bearings Manufacturing Indonesia")

    pdf.sub_title("About NSK Group (Global)")
    pdf.txt(
        "NSK Ltd. is a Japanese multinational headquartered in Tokyo, established November 8, 1916. "
        "One of the world's largest bearing manufacturers with annual net sales of JPY 796.7 billion (~USD 5.3B) "
        "and ~24,057 employees globally (March 2025). Main businesses: industrial bearings, ball screws, "
        "precision machinery, automotive bearings, steering systems, and automatic transmission products. "
        "Operations in 30+ countries. President & CEO: Akitoshi Ichii."
    )

    pdf.sub_title("NSK Indonesia Operations")
    pdf.txt(
        "PT. NSK Indonesia incorporated January 14, 2003. Indonesia has 4 entities:\n"
        "1) PT. NSK Indonesia (HQ) - Summitmas II 4th Floor, Jl. Sudirman Kav. 61-62, Jakarta\n"
        "2) PT. NSK Bearings Manufacturing Indonesia - Kawasan MM.2100 Blok M-4, Cikarang Barat, Bekasi 17520\n"
        "3) PT. NSK-Warner Indonesia - Block DD-12 MM2100, Cikarang Barat, Bekasi\n"
        "4) PT. AKS Precision Ball Indonesia - Blok N-8 MM2100, Cikarang Barat, Bekasi\n\n"
        "KEY INSIGHT: The manufacturing plant is in MM2100 Cikarang - same industrial corridor as PT Dharma Polimetal. "
        "No relocation needed. This is a significant practical advantage."
    )

    pdf.sub_title("NSK Vision 2026")
    pdf.txt(
        "'We bring motion to life, to enrich lifestyles, and to build a brighter future.' "
        "The MTP emphasizes: operational efficiency through digitalization, IoT integration, and "
        "data-driven quality management - directly aligned with this QC Digitalization role."
    )

    pdf.sub_title("Strategic Implications for Your Application")
    pdf.bul("Japanese MNC = structured environment, strong documentation culture, process-oriented")
    pdf.bul("Bearings = precision products requiring strict QC (micron-level tolerances)")
    pdf.bul("Camera & Laser Profiling = advanced automated inspection infrastructure already in use")
    pdf.bul("Same industrial area (MM2100 Cikarang) = zero relocation cost/effort")
    pdf.bul("Active digitalization investment = budget and management support for this project")
    pdf.bul("Japanese language listed as 'big plus' not mandatory = English + tech compensates")
    pdf.ln(2)

    # ========== 2. QUALIFICATION MATCH ==========
    pdf.add_page()
    pdf.section_title("2. Qualification Match Analysis")
    pdf.sub_title("Overall Match Score: 85-90%")
    pdf.txt(
        "Your profile is an exceptionally strong match. You meet or exceed almost every requirement. "
        "The only gaps are Japanese language (nice-to-have) and Node.js (learnable quickly)."
    )

    # Match table: 55 + 20 + 105 = 180
    pdf.table_header([("Requirement", 55), ("Status", 20), ("Your Evidence", 105)])

    match_data = [
        ("D3/S1 Teknik", "MATCH", "D3 Mekatronika Polman Bandung - exact match"),
        ("Laravel Full Stack", "STRONG", "4+ yrs Laravel. Built production app w/ MySQL, RBAC, REST API"),
        ("Node.js", "PARTIAL", "JS ecosystem knowledge. Node learnable in 2-4 weeks"),
        ("MySQL / SQL Server", "STRONG", "Expert: schema design, query optimization, data modeling"),
        ("REST API & Data Flow", "STRONG", "Built REST endpoints for multi-system integration"),
        ("IoT & Auto Inspection", "MATCH", "Built IoT Andon system w/ Arduino. Sensor integration"),
        ("AI / Image Processing", "PARTIAL", "Conceptual understanding. Recommend upskilling OpenCV"),
        ("Japanese Language", "GAP", "Not yet. Listed as bonus. Basic greetings recommended"),
        ("Analytical Skills", "STRONG", "Power BI, Python, 7 QC Tools, SPC, RCA. Google cert."),
        ("Production Floor Exp", "STRONG", "4+ yrs on floor. Warranty claims -70-80%. 24h SLA"),
        ("Cross-functional Collab", "STRONG", "Operators, engineers, IT, management. UAT coordination"),
        ("Production Dynamics", "STRONG", "Andon system built ON floor. Not an office-only dev"),
    ]

    for req, status, note in match_data:
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "", 8)
        if "STRONG" in status or "MATCH" in status:
            c = (0, 100, 0)
        elif "PARTIAL" in status:
            c = (180, 130, 0)
        else:
            c = (200, 0, 0)
        pdf.cell(55, 5, req, border=1)
        pdf.set_text_color(*c)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(20, 5, status, border=1, align="C")
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(105, 5, note, border=1)
        pdf.ln()

    pdf.ln(4)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 128, 0)
    pdf.cell(0, 6, "STRENGTHS (10/12 requirements = strong match):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.bul("Laravel full-stack with production-proven deployment")
    pdf.bul("MySQL/SQL Server at advanced level (daily use)")
    pdf.bul("REST API + system integration (exactly their need)")
    pdf.bul("IoT hardware (Arduino Andon) - rare for a developer")
    pdf.bul("Production floor native - not a pure desk developer")
    pdf.bul("Power BI dashboards + 7 QC Tools = QC domain knowledge")

    pdf.ln(2)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(200, 150, 0)
    pdf.cell(0, 6, "GAPS TO ADDRESS:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.bul("Node.js: Learn Express.js + Socket.io basics (2-4 weeks). Your JS foundation makes this fast.")
    pdf.bul("AI/Image Processing: Study OpenCV concepts, camera inspection pipeline (1-2 weeks conceptual).")

    # ========== 3. SALARY ==========
    pdf.add_page()
    pdf.section_title("3. Salary Benchmark & Negotiation")

    pdf.sub_title("Estimate: QC Staff (Digitalization) at Japanese MNC, Cikarang")
    pdf.txt(
        "Based on: Japanese MNC tier in Bekasi/Cikarang, D3 + 4+ yrs experience, "
        "QC + IT hybrid skillset. Sources: Robert Walters/Kelly Services 2025 surveys, "
        "JobStreet/Glints comparable roles, MNC manufacturing benchmarks."
    )

    # Salary table: 40 + 45 + 35 + 60 = 180
    pdf.table_header([("Level", 40), ("Monthly (IDR)", 45), ("Monthly (USD)", 35), ("Annual 13x (IDR)", 60)])
    pdf.table_row(["Low", "Rp 7,000,000", "~$430", "Rp 91,000,000"], [40, 45, 35, 60])
    pdf.table_row(["Mid (Target)", "Rp 9,000,000", "~$555", "Rp 117,000,000"], [40, 45, 35, 60], bold=True)
    pdf.table_row(["High", "Rp 12,000,000", "~$740", "Rp 156,000,000"], [40, 45, 35, 60])

    pdf.ln(3)
    pdf.sub_title("Adjustment Factors")
    pdf.bbul("D3 vs S1:", "-5 to -10% vs S1 holders. But 4+ yrs experience compensates.")
    pdf.bbul("Rare hybrid skill:", "+10-15% premium. Full-stack + QC + IoT + floor exp is uncommon.")
    pdf.bbul("Japanese MNC:", "Typically 10-20% above local companies. Structured benefits.")
    pdf.bbul("Location:", "Cikarang UMK 2026 ~Rp 5.3-5.5M. Role should be well above UMK.")

    pdf.ln(2)
    pdf.sub_title("Total Compensation (Japanese MNC Typical)")
    pdf.bul("THR: Mandatory 1x monthly salary (13th month)")
    pdf.bul("Bonus: 1-3 months typical for Japanese MNCs (performance-based)")
    pdf.bul("BPJS Kesehatan + Ketenagakerjaan: Employer contribution")
    pdf.bul("Transport/meal allowance: Rp 500K-1.5M/month common")
    pdf.bul("Overtime: Production-area roles often have OT")
    pdf.bul("Language bonus: Some NSK subsidiaries offer Japanese language allowance")

    pdf.ln(2)
    pdf.sub_title("Negotiation Script")
    pdf.txt(
        'When asked salary expectation:\n\n'
        '"Berdasarkan riset pasar untuk posisi kombinasi full-stack development, database management, '
        'dan pengalaman QC di perusahaan manufaktur Jepang area Cikarang, serta pengalaman 4+ tahun saya, '
        'saya mengharapkan range Rp 8.000.000 - Rp 11.000.000/bulan. Terbuka diskusi total package."\n\n'
        'If countered below range, negotiate for: performance review at 6 months, '
        'training budget, Japanese language course sponsorship, transport allowance.'
    )

    # ========== 4. APPLICATION ANSWERS ==========
    pdf.add_page()
    pdf.section_title("4. Application Question Answers")

    qa = [
        ("Q1: Berapa gaji bulanan yang kamu inginkan?",
         "Rp 8.000.000 - Rp 11.000.000/bulan (negotiable based on total package). "
         "Justification: 4+ yrs combining full-stack (Laravel, MySQL, REST API) with QC/production floor experience."),

        ("Q2: Kualifikasi mana yang kamu miliki?",
         "D3 Mekatronika (Polman Bandung), Full Stack Dev (Laravel), DB Management (MySQL/SQL Server), "
         "REST API Development, IoT & Sensor Integration, Data Analytics (Power BI, Python), "
         "7 QC Tools/SPC/RCA, Google Data Analytics Certificate 2024, Fluent ID + EN."),

        ("Q3: Berapa tahun pengalaman sebagai Staf Quality Control?",
         "4+ tahun (Dec 2021 - Present). Meliputi: RCA, defect analysis (7 QC Tools), IoT Andon system, "
         "quality dashboard (Power BI), warranty claims reduction 70-80%."),

        ("Q4: Berapa lama notice period ke perusahaan saat ini?",
         "30 hari (1 bulan) - standar notice period. Handover proper dijamin."),

        ("Q5: Bahasa yang fasih?",
         "Bahasa Indonesia (native), Bahasa Inggris (fasih written & verbal). "
         "Bahasa Jepang: sedang dalam proses belajar dasar."),

        ("Q6: Pengalaman sebagai desainer web?",
         "2+ tahun. UX/UI design untuk aplikasi internal Laravel, portfolio website responsive, "
         "collaborative design melalui UAT process."),

        ("Q7: Pengalaman sebagai pengembang web?",
         "2+ tahun full-stack. Laravel + MySQL backend, REST API, RBAC, database schema design, "
         "deployment aplikasi produksi untuk cross-functional team."),
    ]

    for q, a in qa:
        pdf.ensure_space(35)
        pdf.sub_title(q)
        pdf.txt(a)

    # ========== 5. JAPANESE CRASH PLAN ==========
    pdf.add_page()
    pdf.section_title("5. Japanese Language Crash Plan (2 Weeks)")

    pdf.txt("Japanese is 'nilai tambah yang besar'. Even basic phrases differentiate you and show cultural awareness.")

    pdf.sub_title("Week 1: Essential Greetings")
    # 80 + 100 = 180
    pdf.table_header([("Romaji", 80), ("Meaning", 100)])
    w1 = [
        ("Ohayou gozaimasu", "Good morning (polite)"),
        ("Konnichiwa", "Good afternoon / Hello"),
        ("Hajimemashite", "Nice to meet you (first time)"),
        ("Watashi wa Reyza desu", "My name is Reyza"),
        ("Yoroshiku onegaishimasu", "Please take care of me"),
        ("Arigatou gozaimasu", "Thank you very much"),
        ("Sumimasen", "Excuse me / Sorry"),
        ("Wakarimashita", "I understand"),
        ("Mou ichido onegaishimasu", "Once more please"),
        ("Nihongo wa benkyou-chuu desu", "I'm still studying Japanese"),
        ("Ganbarimasu", "I will do my best"),
    ]
    for r, m in w1:
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(80, 5, r, border=1)
        pdf.cell(100, 5, m, border=1)
        pdf.ln()

    pdf.ln(3)
    pdf.sub_title("Week 2: Workplace & QC Vocabulary")
    pdf.table_header([("Romaji", 80), ("Meaning", 100)])
    w2 = [
        ("Hinshitsu kanri", "Quality control (QC)"),
        ("Kensa", "Inspection"),
        ("Furyou / Furyouhin", "Defect / Defective product"),
        ("Kaizen", "Continuous improvement"),
        ("Seisan", "Production"),
        ("Deeta", "Data"),
        ("Houkoku", "Report"),
        ("Mondai", "Problem"),
        ("Taisaku", "Countermeasure"),
        ("Genba", "Shop floor / Production site"),
        ("Jidouka", "Automation (with human touch)"),
    ]
    for r, m in w2:
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(80, 5, r, border=1)
        pdf.cell(100, 5, m, border=1)
        pdf.ln()

    pdf.ln(3)
    pdf.sub_title("Interview Power Phrase (Memorize This)")
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(0, 70, 140)
    pdf.multi_cell(EW, 6,
        '"Hajimemashite. Watashi wa Reyza desu. Hinshitsu kanri no dijitaru-ka ni kyoumi ga arimasu. '
        'Yoroshiku onegaishimasu."')
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(EW, 5,
        '= "Nice to meet you. I am Reyza. I am interested in QC digitalization. Please take care of me."')

    pdf.set_text_color(30, 30, 30)
    pdf.ln(3)
    pdf.sub_title("Cultural Tips for Japanese Company Interview")
    pdf.bul("Bow slightly (15-30 degrees) when greeting")
    pdf.bul("Both hands when giving/receiving documents")
    pdf.bul("Arrive 10-15 minutes early - punctuality is critical")
    pdf.bul("Use 'We achieved...' not 'I achieved...' - teamwork valued")
    pdf.bul("Mention 'kaizen' mindset naturally")
    pdf.bul("Basic Japanese greeting to Japanese interviewer = major impression")

    pdf.ln(2)
    pdf.sub_title("Free Learning Resources")
    pdf.bul("Duolingo Japanese - 15 min/day")
    pdf.bul("JapanesePod101 (YouTube) - beginner lessons")
    pdf.bul("NHK World Easy Japanese - structured course")
    pdf.bul("Anki flashcards - memorize the phrases above")

    # ========== 6. INTERVIEW STRATEGY ==========
    pdf.add_page()
    pdf.section_title("6. Interview Strategy")

    pdf.sub_title("Expected Format (Japanese MNC)")
    pdf.bul("Round 1: HR screening - behavioral, motivation, salary")
    pdf.bul("Round 2: Technical - coding/system design, QC knowledge, SQL")
    pdf.bul("Round 3: Manager/Director - culture fit, project discussion")
    pdf.bul("Possible: Practical test - build small app or write SQL queries")

    pdf.ln(2)
    pdf.sub_title("Key Messages to Deliver in Every Answer")
    pdf.bul("PRODUCTION FLOOR DEVELOPER: 'I build systems ON and FOR the production floor, not just from an office.'")
    pdf.bul("FULL-STACK + QC HYBRID: 'I speak both developer and quality engineer language.'")
    pdf.bul("PROVEN DEPLOYMENT: 'I already built and deployed a Laravel platform reducing workload 50-70%.'")
    pdf.bul("DATA-DRIVEN QUALITY: 'My dashboards reduced reporting by 60% and informed company strategy.'")

    pdf.ln(2)
    pdf.sub_title("Anticipated Technical Questions & Strategies")
    tech = [
        ("Explain your Laravel app architecture",
         "MVC pattern, MySQL backend, role-based access, REST API endpoints, data flow from floor to dashboard."),
        ("How would you integrate IoT sensors with a database?",
         "Arduino sensors > data collection > API endpoint > MySQL > dashboard. Real-time vs batch trade-offs."),
        ("Write a SQL query for defect analysis",
         "GROUP BY defect_type, production_line, date. Mention indexing for large datasets. Show real examples."),
        ("How do you optimize slow database queries?",
         "EXPLAIN/ANALYZE, indexing, query restructuring, denormalization, caching. Give real production example."),
        ("What do you know about automated visual inspection?",
         "Camera > preprocess > feature extract > classify > report. Understand pipeline, eager to learn NSK specifics."),
        ("Build a real-time quality monitoring dashboard?",
         "Sensors > API ingestion > DB > backend > WebSocket/polling > frontend charts + alerts. Reference Power BI exp."),
    ]
    for q, s in tech:
        pdf.ensure_space(20)
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(0, 70, 140)
        pdf.multi_cell(EW, 5, "Q: " + q)
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(EW, 5, "Strategy: " + s)
        pdf.ln(2)

    # ========== 7. UPSKILLING ==========
    pdf.add_page()
    pdf.section_title("7. Upskilling Roadmap")

    pdf.sub_title("A. Node.js (2-4 Week Plan)")
    pdf.txt("Required for real-time middleware alongside Laravel. Your JS foundation makes this a fast learn:")
    pdf.bul("Week 1: Node.js fundamentals - npm, modules, async/await, event loop")
    pdf.bul("Week 1: Express.js basics - routing, middleware, REST API creation")
    pdf.bul("Week 2: Real-time with Socket.io - WebSocket connections, event broadcasting")
    pdf.bul("Week 2: Connect Node.js to MySQL (mysql2 package) - familiar territory")
    pdf.bul("Week 3: Mini project - real-time quality alert system (Node + Socket.io + MySQL)")
    pdf.bul("Week 4: Integration pattern - Laravel main app, Node.js real-time middleware")
    pdf.txt("Resources: freeCodeCamp Node.js (free), Socket.io docs, The Odin Project.")

    pdf.sub_title("B. AI/Image Processing (1-2 Weeks Conceptual)")
    pdf.txt("NSK uses Camera & Laser Profiling. You need conceptual understanding, not deep expertise:")
    pdf.bul("Pipeline: capture > preprocess > feature extract > classify > report")
    pdf.bul("OpenCV basics in Python: image loading, filtering, edge detection (3-4 hours)")
    pdf.bul("'Laser Profiling' = surface defect detection for bearings")
    pdf.bul("Key: analyze defect data FROM the inspection system, not build the AI model")
    pdf.txt("Resources: OpenCV-Python tutorial, YouTube 'bearing surface defect detection'.")

    pdf.sub_title("C. Japanese Language (Ongoing)")
    pdf.bul("JLPT N5 target (6-12 months) - basic certification")
    pdf.bul("If hired, request company-sponsored Japanese language training")
    pdf.bul("Many Japanese MNCs in Indonesia offer internal language courses")
    pdf.bul("Even N5 level significantly boosts career growth in Japanese companies")

    # ========== 8. ACTION PLAN ==========
    pdf.add_page()
    pdf.section_title("8. Action Plan & Timeline")

    pdf.sub_title("Immediate (This Week)")
    pdf.bul("Submit application with tailored CV (cv_qc_specialist.tex)")
    pdf.bul("Send application email (email_nsk_qc_digitalization.txt)")
    pdf.bul("Start memorizing Japanese greetings (Section 5)")
    pdf.bul("Begin Node.js crash course (Express.js basics)")

    pdf.ln(2)
    pdf.sub_title("Week 1-2 (While Waiting)")
    pdf.bul("Complete Node.js + Express.js fundamentals")
    pdf.bul("Build mini real-time monitoring demo")
    pdf.bul("Study OpenCV basics (2-3 hours)")
    pdf.bul("Research bearing manufacturing QC processes")
    pdf.bul("Practice Japanese daily (10-15 min)")

    pdf.ln(2)
    pdf.sub_title("Week 2-3 (Interview Prep)")
    pdf.bul("Practice technical questions from Section 6")
    pdf.bul("Prepare STAR-method stories for behavioral questions")
    pdf.bul("Portfolio demos ready: Laravel app, Power BI dashboards, Andon system")
    pdf.bul("Practice Japanese self-introduction")

    pdf.ln(2)
    pdf.sub_title("Interview Day Checklist")
    pdf.bul("Arrive 15 minutes early")
    pdf.bul("Printed CV (2 copies)")
    pdf.bul("Laptop with portfolio demos if applicable")
    pdf.bul("Open with Japanese greeting if Japanese interviewer present")
    pdf.bul("Salary range ready: Rp 8-11M (flexible for total package)")
    pdf.bul("Questions to ask interviewer:")
    pdf.txt(
        '  "What inspection systems are currently in use?"\n'
        '  "What is the current tech stack for internal apps?"\n'
        '  "How does the digi team collaborate with production?"\n'
        '  "Is there Japanese language training opportunity?"'
    )

    # ========== 9. RISK ASSESSMENT ==========
    pdf.ensure_space(60)
    pdf.section_title("9. Risk Assessment")
    # 50 + 25 + 105 = 180
    pdf.table_header([("Risk", 50), ("Likelihood", 25), ("Mitigation", 105)])
    risks = [
        ("Node.js test", "Medium", "Start learning now. Express.js demo shows initiative."),
        ("Japanese filter", "Low", "Listed as bonus. Basic greeting shows awareness."),
        ("S1 preference", "Low-Med", "4+ yrs exp + Google cert + proven deployment."),
        ("Salary below target", "Medium", "Walk-away: Rp 7M min. Negotiate total package."),
        ("Overqualified concern", "Low", "Frame as growth into QC digitalization specialty."),
    ]
    for risk, lik, mit in risks:
        pdf.set_x(MARGIN)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(50, 5, risk, border=1)
        pdf.cell(25, 5, lik, border=1, align="C")
        pdf.cell(105, 5, mit, border=1)
        pdf.ln()

    # Save
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "NSK_QC_Digitalization_Report.pdf")
    pdf.output(out_path)
    print(f"Report saved: {out_path}")


if __name__ == "__main__":
    build()
