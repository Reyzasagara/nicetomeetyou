# -*- coding: utf-8 -*-
"""
NSK Bearings - Technical QC Digitalization Deep Dive Report
For: Reyza Agung Gunawan - Interview Preparation (April 2026)
Purpose: Impress interviewer with end-to-end simulation system concept 
         showing deep knowledge of their manufacturing process, sensor data,
         and practical digitalization architecture using Reyza's own skillset.
"""

from fpdf import FPDF
import os

MARGIN = 15
EW = 180

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "NSK QC Digitalization - Technical Deep Dive | Reyza Agung Gunawan | April 2026", align="R")
        self.ln(5)
        self.set_draw_color(0, 90, 170)
        self.set_line_width(0.3)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Confidential - For Interview Use Only | April 2026", align="C")

    def h1(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 60, 130)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 90, 170)
        self.set_line_width(0.5)
        self.line(MARGIN, self.get_y(), MARGIN + 120, self.get_y())
        self.ln(3)

    def h2(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def h3(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "BI", 9.5)
        self.set_text_color(0, 90, 170)
        self.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

    def p(self, text):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(EW, 5, text)
        self.ln(2)

    def b(self, label, text=""):
        self.set_x(MARGIN + 3)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        if text:
            self.set_font("Helvetica", "B", 9)
            w = self.get_string_width(label + " ")
            self.cell(w, 5, label + " ")
            self.set_font("Helvetica", "", 9)
            self.multi_cell(EW - 3 - w, 5, text)
        else:
            self.multi_cell(EW - 3, 5, "  - " + label)

    def note(self, text, color=(255,153,0)):
        self.set_x(MARGIN)
        self.set_fill_color(*color)
        self.set_text_color(30, 30, 30)
        self.set_font("Helvetica", "I", 8.5)
        self.multi_cell(EW, 5, "  " + text, fill=True)
        self.ln(2)

    def th(self, cols):
        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(0, 60, 130)
        self.set_text_color(255, 255, 255)
        for label, w in cols:
            self.cell(w, 6, label, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(30, 30, 30)

    def tr(self, vals, widths, shade=False, bold_first=False):
        self.set_x(MARGIN)
        if shade:
            self.set_fill_color(240, 245, 255)
        else:
            self.set_fill_color(255, 255, 255)
        for i, (val, w) in enumerate(zip(vals, widths)):
            if bold_first and i == 0:
                self.set_font("Helvetica", "B", 8)
            else:
                self.set_font("Helvetica", "", 8)
            self.cell(w, 5.5, val, border=1, fill=True)
        self.ln()

    def space(self, needed=25):
        if self.get_y() > 297 - MARGIN - needed:
            self.add_page()

    def divider(self):
        self.ln(2)
        self.set_draw_color(200, 210, 230)
        self.set_line_width(0.2)
        self.line(MARGIN, self.get_y(), 210 - MARGIN, self.get_y())
        self.ln(3)


def build():
    pdf = PDF("P", "mm", "A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(MARGIN, MARGIN, MARGIN)

    # ======================================================
    # COVER PAGE
    # ======================================================
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 120, 200)
    pdf.cell(0, 7, "TECHNICAL DEEP DIVE REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(0, 50, 120)
    pdf.cell(0, 12, "End-to-End QC Digitalization", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "Simulation System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "PT. NSK Bearings Manufacturing Indonesia", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(0, 90, 170)
    pdf.set_line_width(0.8)
    pdf.line(55, pdf.get_y(), 155, pdf.get_y())
    pdf.ln(10)

    for line, sz in [
        ("Prepared by: Reyza Agung Gunawan", 10),
        ("D3 Mechatronics | 4+ Years Manufacturing Digitalization", 9),
        ("Date: April 2026", 9),
    ]:
        pdf.set_font("Helvetica", "", sz)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 7, line, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(14)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    sections = (
        "Sections: NSK Manufacturing Process | Estimated Machine Inventory | "
        "Sensor Data Catalog | Industrial Comm Protocols | DB Architecture | "
        "Simulation Design | Laravel + Realtime Stack | Power BI Analytics | "
        "NG Data Scenarios | NSK Supply Chain Map"
    )
    pdf.multi_cell(EW, 6, sections, align="C")

    pdf.ln(20)
    pdf.set_fill_color(240, 247, 255)
    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 60, 130)
    pdf.multi_cell(EW, 6,
        "PURPOSE: This report is designed to demonstrate to NSK interviewers that Reyza has done "
        "deep technical homework - understanding not just software development, but the actual "
        "manufacturing processes, machine types, sensor signals, and industrial protocols used in "
        "bearing production. The proposed simulation system is a portfolio-quality deliverable "
        "Reyza can present as a deployment-ready concept.",
        fill=True)

    # ======================================================
    # SECTION 1: NSK BEARING MANUFACTURING PROCESS
    # ======================================================
    pdf.add_page()
    pdf.h1("1. Bearing Manufacturing Process at NSK Indonesia")

    pdf.h2("1.1 Products at PT. NSK Bearings Manufacturing Indonesia (Cikarang)")
    pdf.p(
        "NSK Cikarang primarily manufactures rolling element bearings for automotive applications, "
        "including Deep Groove Ball Bearings (DGBB), Angular Contact Ball Bearings (ACBB), "
        "Tapered Roller Bearings (TRB), and Hub Unit Bearings (HUB). These are supplied "
        "predominantly to automotive OEMs and their Tier-1 suppliers in the JABODETABEK and "
        "Karawang-Bekasi industrial corridor."
    )

    pdf.h2("1.2 Core Manufacturing Process Flow")
    pdf.p("A standard ball bearing goes through these production stages:")

    steps = [
        ("STAGE 1", "Raw Material Receiving",
         "Steel rings (SUJ2 / AISI 52100 bearing steel) and steel balls arrive from steel mills. "
         "Incoming QC: hardness test, dimensional check, chemical composition certificate."),
        ("STAGE 2", "Turning (Lathe Process)",
         "CNC turning machines shape inner ring (IR) and outer ring (OR) from steel tube/bar stock. "
         "Critical QC: OD, ID, width, squareness. Typical tolerance: +/-0.01mm."),
        ("STAGE 3", "Heat Treatment",
         "Bearing rings undergo carburizing, quenching, and tempering in controlled atmosphere furnace. "
         "Target: 58-65 HRC hardness. Critical QC: hardness, microstructure, distortion."),
        ("STAGE 4", "Grinding (Inner/Outer Ring)",
         "CNC centerless grinding machines achieve final dimensional accuracy. Multiple sub-stages: "
         "OD grinding, face grinding, bore grinding, raceway grinding. "
         "Critical QC: roundness (<0.5 micron), surface roughness (Ra 0.1-0.3 micron), dimensions."),
        ("STAGE 5", "Superfinishing",
         "Honing/superfinishing of raceway surface. Target surface: Ra < 0.1 micron. "
         "Critical QC: surface roughness, waviness, LOB (Lobbing)."),
        ("STAGE 6", "Ball / Roller Manufacturing",
         "Steel balls made separately (may also be sourced from PT. AKS Precision Ball Indonesia, "
         "NSK's sister company at MM2100). Critical QC: diameter uniformity, roundness, surface."),
        ("STAGE 7", "Assembly",
         "Inner ring + outer ring + balls/rollers + cage + seals assembled. "
         "Critical QC: axial play, radial play, ball count, seal integrity, greasing amount."),
        ("STAGE 8", "Noise & Vibration Test",
        "Every bearing tested on noise/vibration tester (Anderonmeter or custom machine). "
         "Electric motor spins bearing at test speed; acoustic/vibration sensor measures quality. "
         "Critical QC: ABEC class compliance, Anderon level, No defect pattern in frequency spectrum."),
        ("STAGE 9", "Final Inspection & Marking",
         "100% visual inspection (manual + camera), dimensional final check on CMM or automatic gauging, "
         "laser/inkjet marking with serial number, date code, product number."),
        ("STAGE 10", "Packaging & Shipping",
         "Packaging by customer specification. Shipping documentation, PPAP documents, "
         "quality records archived. Traceability to batch and production date."),
    ]

    w_stage, w_name, w_desc = 18, 45, 117
    pdf.th([("Stage", w_stage), ("Process", w_name), ("Details & QC Points", w_desc)])
    for i, (stage, name, desc) in enumerate(steps):
        pdf.set_x(MARGIN)
        shade = (i % 2 == 0)
        fill_color = (235, 245, 255) if shade else (250, 250, 255)
        pdf.set_fill_color(*fill_color)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(w_stage, 5.5, stage, border=1, fill=True, align="C")
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(w_name, 5.5, name, border=1, fill=True)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(w_desc, 5.5, desc[:95] + ("..." if len(desc) > 95 else ""), border=1, fill=True)
        pdf.ln()

    pdf.ln(3)
    pdf.note(
        "KEY INSIGHT for Interview: Stages 3 (Heat Treatment), 4 (Grinding), and 8 (Noise/Vibration) "
        "are the three highest-defect-risk stages. Any QC digitalization system must prioritize "
        "real-time monitoring at these three stages first.",
        color=(220, 240, 255)
    )

    # ======================================================
    # SECTION 2: MACHINE INVENTORY (ESTIMATED)
    # ======================================================
    pdf.add_page()
    pdf.h1("2. Estimated Machine Inventory at NSK Cikarang")

    pdf.p(
        "Based on industry knowledge of bearing manufacturer plant layouts (NSK, JTEKT, SKF comparable "
        "plants), the following machine types are estimated to be present at PT. NSK Bearings "
        "Manufacturing Indonesia. Exact models may vary, but the sensor data types are consistent "
        "across manufacturers of this equipment category."
    )

    machines = [
        ("CNC Lathe / Turning Center", "Turning rings from bar/tube stock",
         "Citizen, Nakamura, Miyano, or NSK-proprietary", "10-30 units",
         "Spindle RPM, Feed Rate, Cutting Load, Coolant Temp, Dimensional Output (OD/ID/Width)"),
        ("CNC Cylindrical Grinder", "Grinding OD, ID, faces to final tolerance",
         "JTEKT (Toyoda), Mikrosa, DANOBAT, Kellenberger", "20-50 units",
         "Spindle Vibration, Wheel Wear, Grinding Force, Coolant Temp/Flow, Surface Roughness, Dimension"),
        ("CNC Centerless Grinder", "Grinding ball and ring OD",
         "Koyo Machine, Mikrosa, Cincinnati", "10-20 units",
         "Wheel RPM, Throughput Speed, Workpiece Diameter, Roundness, Vibration"),
        ("Superfinishing Machine", "Honing raceway surface to Ra < 0.1 micron",
         "Supfina, Peter Wolters, VALGRO", "10-20 units",
         "Stone Pressure, Oscillation Frequency/Amplitude, Ra Surface Roughness, Oil Flow"),
        ("Heat Treatment Furnace", "Carburizing, quenching, tempering",
         "Ipsen, AFC-Holcroft, Aichelin Group", "3-8 units (large batch equipment)",
         "Zone Temperature (6-12 zones), Atmosphere (CH4/CO/N2%), Quench Oil Temp, Cycle Time, Hardness Output"),
        ("CMM (Coord Measuring Machine)", "Final dimensional inspection",
         "Zeiss, Mitutoyo, Hexagon", "3-6 units",
         "Diameter, Roundness, Cylindricity, Surface Roughness, Positional Accuracy, Pass/Fail Output"),
        ("Automatic Gauging Machine", "In-line 100% dimensional check",
         "Marposs, Mahr, Renishaw", "1 per grinding line",
         "OD/ID/Width measurement, SPC data stream (Xbar-R), NG count, Cp/Cpk calculation"),
        ("Assembly Machine", "Press-fit, greasing, sealing assembly",
         "NSK-proprietary custom, Felo Automation", "5-15 units",
         "Press Force (kN), Axial Play (micron), Radial Play (micron), Grease Weight (g), Seal Seating Force"),
        ("Noise/Vibration Tester", "Final Anderon / vibration quality test",
         "NSK Anderon Meter (proprietary), STL Spectrum Analyzer", "5-15 units",
         "Anderon Level (mA), Noise Level (dB), Vibration Frequency Spectrum (FFT), RPM, Pass/Fail, Defect Class"),
        ("Washing Machine", "Cleaning rings/balls between processes",
         "LPW, Pero, MecWash", "5-10 units",
         "Water Temperature, Detergent Concentration, pH Level, Cycle Count, Chamber Pressure"),
        ("Hardness Tester", "Rockwell hardness check post heat-treat",
         "Mitutoyo, Wolpert Wilson, Buehler", "5-10 units",
         "HRC Value, Load (N), Dwell Time, Pass/Fail vs specification"),
        ("Incoming QC Station", "Chemical & dimensional check on raw material",
         "XRF Spectrometer, Hardness Tester, CMM", "2-4 stations",
         "Chemical Composition (C/Cr/Mn%), Hardness (HRC/HRB), Diameter, Certificate Verification"),
    ]

    w = [38, 28, 26, 15, 73]  # Adjusted widths for better display
    pdf.th([("Machine Type", w[0]), ("Application", w[1]), ("Likely Make/Model", w[2]),
            ("Qty Est.", w[3]), ("Key Sensor Data Points", w[4])])
    
    for i, (mtype, app, make, qty, data) in enumerate(machines):
        shade = (i % 2 == 0)
        fc = (235, 245, 255) if shade else (250, 250, 255)
        pdf.set_fill_color(*fc)
        
        # Calculate row height based on data column content
        pdf.set_font("Helvetica", "", 6.5)
        num_lines = len(pdf.multi_cell(w[4], 4, data, dry_run=True, output="LINES"))
        row_height = max(5.5, num_lines * 4)
        
        # Save Y position for border drawing
        y_start = pdf.get_y()
        x_start = MARGIN
        
        # Draw cells with proper borders
        pdf.set_xy(x_start, y_start)
        pdf.set_font("Helvetica", "B", 6.5)
        pdf.multi_cell(w[0], row_height, mtype, border=1, fill=True)
        
        pdf.set_xy(x_start + w[0], y_start)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.multi_cell(w[1], row_height, app, border=1, fill=True)
        
        pdf.set_xy(x_start + w[0] + w[1], y_start)
        pdf.multi_cell(w[2], row_height, make, border=1, fill=True)
        
        pdf.set_xy(x_start + w[0] + w[1] + w[2], y_start)
        pdf.multi_cell(w[3], row_height, qty, border=1, fill=True, align="C")
        
        pdf.set_xy(x_start + w[0] + w[1] + w[2] + w[3], y_start)
        pdf.multi_cell(w[4], 4, data, border=1, fill=True)
        
        # Move to next row
        pdf.set_xy(MARGIN, y_start + row_height)

    # ======================================================
    # SECTION 3: SENSOR DATA CATALOG
    # ======================================================
    pdf.add_page()
    pdf.h1("3. Sensor Data Catalog - By Machine Type")

    pdf.p(
        "This section details every significant data point that can be collected from each machine "
        "type. These represent the actual signals that would flow from the shop floor into the "
        "proposed digitalization system. Understanding these precisely is a key differentiator "
        "when presenting to NSK's engineering and QC teams."
    )

    sensor_sections = [

        ("3.1 CNC Grinding Machine (Raceway / OD / ID Grinding)", [
            ("Spindle Motor Current (A)", "Indirect measure of grinding force / wheel wear", "4-20mA analog", "100ms", "OPC-UA"),
            ("Spindle Vibration (mm/s)", "Bearing condition on spindle itself, imbalance detection", "Piezo accelerometer", "10ms", "OPC-UA"),
            ("Grinding Wheel RPM (rpm)", "Speed control verification, affects surface finish", "Encoder", "10ms", "OPC-UA / Modbus"),
            ("Coolant Temperature (degC)", "Too hot = thermal expansion error, burn marks", "Thermocouple (PT100)", "1s", "Modbus RTU"),
            ("Coolant Flow Rate (L/min)", "Insufficient flow = burn risk, part damage", "Flow meter (magnetic)", "1s", "Modbus RTU"),
            ("Workpiece Diameter - In Process (micron)", "Post-process gauge result (Marposs APC)", "LVDT/Air gauge", "Per cycle", "OPC-UA / RS232"),
            ("Surface Roughness Ra (micron)", "Tactile/optical profilometer reading", "Profilometer", "Per cycle", "RS232 / OPC-UA"),
            ("Roundness / Cylindricity (micron)", "CMM or in-process roundness gauge", "Air gauge / inductive", "Per cycle", "OPC-UA"),
            ("Wheel Dresser Counter", "Tracks dress frequency, predicts wheel life", "Counter in CNC PLC", "Per cycle", "OPC-UA"),
            ("Part Counter (OK / NG)", "Real-time production count from CNC PLC", "PLC register", "Per cycle", "OPC-UA / Modbus"),
        ]),

        ("3.2 Heat Treatment Furnace", [
            ("Zone Temperatures x8 (degC)", "Accuracy +/-5degC critical. NG if deviation", "Type K thermocouple", "5s", "Modbus RTU"),
            ("Carbon Potential (%C)", "Controls carburizing depth, surface hardness", "O2 probe / CO IR sensor", "30s", "Modbus RTU / 4-20mA"),
            ("Atmosphere Gas Flow N2/CH4/CO (L/min)", "Recipe compliance, safety monitoring", "Mass flow controller", "5s", "Modbus RTU"),
            ("Chamber Pressure (mbar)", "Prevents air infiltration in atmosphere furnace", "Pressure transducer", "5s", "4-20mA"),
            ("Quench Oil Temperature (degC)", "Cold oil = inconsistent martensite structure", "PT100", "5s", "Modbus RTU"),
            ("Quench Oil Agitation (Hz)", "Agitator speed affects cooling rate uniformity", "VFD feedback", "5s", "Modbus RTU"),
            ("Batch ID / Recipe ID", "Traceability: which parts, which recipe", "Manual/Barcode scanner", "Per batch", "RS232 / MQTT"),
            ("Cycle Start/End Time", "For cycle time analysis, OEE calculation", "PLC", "Per cycle", "OPC-UA"),
            ("Alarm Codes", "Furnace fault codes for rapid response", "PLC", "Event", "MQTT / OPC-UA"),
        ]),

        ("3.3 Noise / Vibration Tester (Anderon Meter)", [
            ("Anderon Level - Low Band (mA)", "Low-frequency noise: raceway defects, waviness", "Piezo sensor", "Per test", "RS232 / OPC-UA"),
            ("Anderon Level - Medium Band (mA)", "Mid-frequency: ball defects, cage noise", "Piezo sensor", "Per test", "RS232 / OPC-UA"),
            ("Anderon Level - High Band (mA)", "High-frequency: surface roughness quality", "Piezo sensor", "Per test", "RS232 / OPC-UA"),
            ("Vibration Frequency Spectrum (FFT)", "Full 0-10kHz spectrum for defect classification", "Accelerometer + DSP", "Per test", "TCP/IP JSON"),
            ("Test RPM (rpm)", "Standardized test speed, usually 1800 or 3600 rpm", "Encoder", "Per test", "OPC-UA"),
            ("Axial Load Applied (N)", "Preload during test for ABEC class compliance", "Load cell", "Per test", "OPC-UA"),
            ("Pass/Fail + Defect Class", "OK, NG-Low, NG-Medium, NG-High, NG-Impact", "PLC logic", "Per test", "OPC-UA / MQTT"),
            ("Part Serial Number", "1D/2D barcode scan for traceability", "Barcode scanner", "Per test", "TCP/IP / MQTT"),
            ("Test Duration (s)", "Cycle time KPI", "PLC timer", "Per test", "OPC-UA"),
        ]),

        ("3.4 Assembly Machine", [
            ("Press Force - Seal / Shield Install (kN)", "Detects missing seal, wrong seal, hard press", "Load cell", "Per cycle", "OPC-UA"),
            ("Press Force - IR onto shaft press (kN)", "Interference fit compliance monitoring", "Load cell", "Per cycle", "OPC-UA"),
            ("Axial Play (micron)", "Gap between IR and OR along axis, ABEC spec", "LVDT sensor", "Per cycle", "OPC-UA"),
            ("Radial Play (micron)", "Radial clearance specification compliance", "LVDT sensor", "Per cycle", "OPC-UA"),
            ("Grease Volume (g)", "Gravimetric or volumetric grease dispenser", "Load cell / dispenser", "Per cycle", "OPC-UA / 4-20mA"),
            ("Ball / Roller Count Verification", "Vision system counts rolling elements", "Camera + vision PLC", "Per cycle", "TCP/IP / OPC-UA"),
            ("Cycle Time (s)", "OEE calculation, bottleneck detection", "PLC timer", "Per cycle", "OPC-UA"),
            ("Part Counter OK / NG / Total", "Production tracking", "PLC", "Per cycle", "OPC-UA / Modbus"),
        ]),

        ("3.5 Automatic Gauging Machine (In-Line CMM / Air Gauge)", [
            ("OD Measurement (micron)", "100% outer diameter gauging", "Air gauge / LVDT", "Per part", "RS232 / OPC-UA"),
            ("ID Measurement (micron)", "100% inner diameter gauging", "Air gauge / LVDT", "Per part", "RS232 / OPC-UA"),
            ("Width / Height (micron)", "Bearing width tolerance compliance", "LVDT", "Per part", "RS232 / OPC-UA"),
            ("Roundness (micron)", "Deviation from perfect circle", "Multi-point sensor", "Per part", "OPC-UA"),
            ("Pass/Fail + Out-of-Control Signal", "Real-time SPC alert for control chart breach", "Gauging PLC", "Per part", "MQTT / OPC-UA"),
            ("SPC Data: Xbar, R, Cp, Cpk", "Statistical process control live stream", "Gauging controller", "Rolling avg", "OPC-UA / TCP/IP"),
            ("Last 100 parts moving average", "Trend detection before NG occurs", "Controller calculation", "Continuous", "OPC-UA"),
        ]),
    ]

    for title, rows in sensor_sections:
        pdf.space(40)
        pdf.h2(title)
        pdf.th([("Data Point", 55), ("Purpose / Why It Matters", 60), ("Sensor Type", 25),
                ("Freq", 15), ("Protocol", 25)])
        for i, (dp, why, sensor, freq, proto) in enumerate(rows):
            shade = (i % 2 == 0)
            fc = (238, 246, 255) if shade else (252, 252, 255)
            pdf.set_x(MARGIN)
            pdf.set_fill_color(*fc)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(55, 5, dp, border=1, fill=True)
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(60, 5, why[:58] + ("..." if len(why) > 58 else ""), border=1, fill=True)
            pdf.cell(25, 5, sensor, border=1, fill=True)
            pdf.cell(15, 5, freq, border=1, fill=True, align="C")
            pdf.set_font("Helvetica", "B", 7)
            pdf.set_text_color(0, 80, 160)
            pdf.cell(25, 5, proto, border=1, fill=True, align="C")
            pdf.set_text_color(30, 30, 30)
            pdf.ln()
        pdf.ln(2)

    # ======================================================
    # SECTION 4: INDUSTRIAL COMMUNICATION PROTOCOLS
    # ======================================================
    pdf.add_page()
    pdf.h1("4. Industrial Communication Protocols - Recommendation")

    pdf.p(
        "Choosing the right protocol for each layer of the system is critical for reliability, "
        "latency, and integration ease. The following recommendations are grounded in actual "
        "bearing manufacturing industry standards."
    )

    pdf.h2("4.1 Protocol Stack by Layer")

    protocols = [
        ("Device/Fieldbus Layer", "OPC-UA", "RECOMMENDED for modern CNC machines",
         "OPC-UA (IEC 62541) is the dominant standard for CNC-to-server communication. "
         "Most Fanuc, Siemens SINUMERIK, Mitsubishi M-series controllers support OPC-UA server built-in. "
         "Supports data modeling, security, and real-time data at 10ms polling. "
         "Most bearing manufacturers (NSK, JTEKT, SKF) use OPC-UA as primary machine data protocol.",
         (0, 150, 50)),
        ("Legacy Machine Layer", "Modbus RTU/TCP", "For older PLCs and analog devices",
         "Modbus RTU over RS-485 is universal for legacy Mitsubishi, Omron, Siemens S7-200 PLCs. "
         "Modbus TCP for Ethernet-connected older machines. "
         "Widely used for temperature controllers, VFDs, flow meters. "
         "Simple, reliable, widely supported. Polling rate: 100ms-1s typical.",
         (180, 130, 0)),
        ("IoT / Event Layer", "MQTT (v3.1.1 or v5)", "For lightweight real-time push events",
         "MQTT is ideal for alarm events, cycle completion triggers, NG part alerts. "
         "Publish/subscribe model - machine publishes on event, server subscribes. "
         "Broker: Eclipse Mosquitto (open-source, lightweight, runs on Raspberry Pi). "
         "QoS Level 1 for guaranteed delivery. Latency < 50ms. "
         "Used by smart sensors, barcode scanners, end-of-line testers that support MQTT.",
         (0, 100, 200)),
        ("Edge-to-Server Layer", "REST API over HTTPS", "Between Edge Gateway and Laravel Server",
         "Edge gateway (industrial PC or Raspberry Pi) collects OPC-UA + Modbus + MQTT data, "
         "batches it, and sends to Laravel REST API every 500ms - 5s. "
         "Stateless, scalable, easy to debug. Laravel API validates, processes, and stores. "
         "Alternative: WebSocket for sub-second real-time push from edge to browser.",
         (80, 0, 160)),
        ("Report Layer", "REST / DirectQuery", "Power BI to Database",
         "Power BI Desktop connects to MySQL (historical DB) via Power BI MySQL connector. "
         "DirectQuery mode for near-real-time analytics (30s refresh). "
         "Import mode for weekly/monthly trend reports with DAX calculations. "
         "Separate database user with READ-ONLY privilege for Power BI security.",
         (0, 128, 128)),
    ]

    for layer, proto, tagline, desc, color in protocols:
        pdf.space(35)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(*color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(EW, 6, f"  {layer}: {proto} - {tagline}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(MARGIN + 4)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(EW - 4, 5, desc)
        pdf.ln(2)

    pdf.h2("4.2 Database Architecture")

    pdf.note(
        "RECOMMENDATION: Use TWO databases optimized for different purposes. "
        "Do NOT use a single general-purpose MySQL for everything - high-frequency sensor data "
        "will kill query performance in a relational DB.",
        color=(255, 235, 200)
    )

    db_compare = [
        ("Database", "TimescaleDB (PostgreSQL ext.)", "MySQL 8.0 (or PostgreSQL)"),
        ("Purpose", "Real-time sensor data stream", "Transactional + Historical records"),
        ("Best For", "Time-series: temp, vibration, RPM etc.", "Production plans, inspection logs, NG reports"),
        ("Write Speed", "1M+ inserts/sec with hypertable compression", "10K-50K inserts/sec standard"),
        ("Query Pattern", "SELECT last 60 minutes of sensor X", "SELECT WHERE lot_no = 'A001'"),
        ("Retention Policy", "Auto-compress after 7 days, archive 90d", "Full history, auditable, backed up"),
        ("Laravel Support", "Via PostgreSQL driver (full support)", "Native Laravel MySQL driver"),
        ("Power BI Support", "Via PostgreSQL connector", "Native MySQL connector"),
        ("Open Source", "Yes (free Timescale Community)", "Yes (MySQL Community)"),
        ("Recommended Use", "ALL sensor data tables (grinding, furnace etc.)", "Inspection records, WO, NG reports, users"),
    ]

    w1, w2, w3 = 45, 65, 70
    pdf.th([("Property", w1), ("Real-Time DB: TimescaleDB", w2), ("Historical DB: MySQL", w3)])
    for i, row in enumerate(db_compare):
        shade = (i % 2 == 1)
        pdf.tr(row, [w1, w2, w3], shade=shade, bold_first=True)

    pdf.ln(3)
    pdf.h2("4.3 Message Broker + Edge Architecture")
    pdf.p(
        "Recommended edge stack running on an Industrial PC (IPC) per production line:\n"
        "  1. OPC-UA Client (Node.js 'node-opcua' or Python 'opcua' library) - polls CNC machines\n"
        "  2. Modbus TCP/RTU Client - polls PLCs, sensors, gauging machines\n"
        "  3. MQTT Broker (Mosquitto) - receives push events from smart devices\n"
        "  4. Edge Aggregator Service - collects all above, buffers, sends to Laravel REST API\n"
        "  5. Local SQLite buffer - stores 24h of data in case of network interruption\n\n"
        "WHY EDGE: Reduces load on cloud server. Enables offline operation. "
        "Provides pre-processing (unit conversion, calibration offset, alarm logic) close to source."
    )

    # ======================================================
    # SECTION 5: END-TO-END SYSTEM ARCHITECTURE
    # ======================================================
    pdf.add_page()
    pdf.h1("5. Proposed End-to-End System Architecture")

    pdf.h2("5.1 Architecture Overview (ASCII Diagram)")
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(30, 30, 30)
    diag = [
        "+------------------+   OPC-UA/Modbus/MQTT   +-------------------+",
        "| PRODUCTION FLOOR |------------------------>| EDGE GATEWAY (IPC)|",
        "| - CNC Grinders   |                         | - OPC-UA Client   |",
        "| - Furnaces       |                         | - Modbus Client   |",
        "| - Noise Testers  |                         | - MQTT Broker     |",
        "| - Gauging Mach.  |                         | - SQLite buffer   |",
        "| - Assembly Mach. |                         | - Aggregator svc  |",
        "+------------------+                         +-------------------+",
        "                                                       |",
        "                                       REST API / WebSocket (HTTPS)",
        "                                                       |",
        "                                                       v",
        "+--------------------+     MySQL      +-------------------+",
        "| TimescaleDB        |<-------------->|  LARAVEL APP      |",
        "| (Real-time sensor) |   Write/Read   |  (REST API)       |",
        "+--------------------+                | - Auth (RBAC)    |",
        "         |                             | - Production Plan |",
        "    DirectQuery                        | - Parameter Mgmt  |",
        "         |                             | - Alerting        |",
        "         v                             | - WebSocket Push  |",
        "+--------------------+                +-------------------+",
        "| POWER BI DASHBOARD |                        |",
        "| - Trend Analysis   |                    WebSocket",
        "| - SPC Charts       |                        |",
        "| - NG Pareto        |                        v",
        "| - OEE Reports      |           +-------------------------+",
        "+--------------------+           |   REALTIME DASHBOARD   |",
        "                                 |   (Vue.js or Blade)     |",
        "                                 |   Laravel + Pusher/     |",
        "                                 |   Laravel Echo          |",
        "                                 +-------------------------+",
    ]
    for line in diag:
        pdf.set_x(MARGIN + 2)
        pdf.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 9)
    pdf.h2("5.2 Manual Input Module (Production Plan & Thresholds)")
    pdf.p(
        "Not everything comes from sensors. Operators and engineers input critical planning data:"
    )
    manual_inputs = [
        ("Production Plan", "Work order number, part number, batch size, target quantity, shift, line assignment"),
        ("Quality Threshold / Spec", "OD nom/tolerance, ID nom/tolerance, Roundness limit, Ra limit per product"),
        ("Anderon Limits", "Pass/fail threshold per bearing type and ABEC class (C0/P0/P6 etc.)"),
        ("Alert Escalation Matrix", "Who gets notified at what severity: Operator > Supervisor > QC Manager"),
        ("Machine Calibration Record", "Last calibration date, next due, calibration value for gauge offset compensation"),
        ("Maintenance Schedule", "Preventive maintenance plan input, triggers pre-maintenance alert"),
        ("User / Role Management", "Operator, QC Inspector, Supervisor, Engineer, Manager roles with different data access"),
    ]

    for item, desc in manual_inputs:
        pdf.b(item + ":", desc)
    pdf.ln(2)

    pdf.h2("5.3 Laravel Application Modules")
    modules = [
        ("API Gateway", "Receives data from Edge Gateway (REST POST). Validates JWT token, validates schema, writes to TimescaleDB + MySQL."),
        ("Production Plan Module", "CRUD for work orders, schedules, target quantities. Links to machine assignment."),
        ("Quality Parameter Module", "Stores product specifications. Provides threshold values consumed by Edge Gateway for real-time alerting."),
        ("Real-Time Monitor", "Uses Laravel Echo + Pusher/Soketi to push sensor events to browser. SPC chart updates, NG alerts."),
        ("NG Management Module", "Records NG events with root cause, affected lot, action taken, disposition (scrap/rework)."),
        ("Report Module", "On-demand hourly/daily/weekly quality reports. Downloadable CSV/PDF. Can export to Power BI format."),
        ("Alert Module", "Rule-based alerting engine. Triggers when SPC rule violated, Anderon above limit, furnace deviation."),
        ("Traceability Module", "Given a part serial number, trace: machine, operator, shift, batch, all sensor readings during production."),
        ("User Auth (RBAC)", "Role-based access control. Japanese engineers = read + spec management. Operators = data input only."),
    ]
    w_m, w_d = 45, 135
    pdf.th([("Module", w_m), ("Description", w_d)])
    for i, (mod, desc) in enumerate(modules):
        shade = (i % 2 == 0)
        pdf.set_x(MARGIN)
        fc = (238, 246, 255) if shade else (252, 252, 255)
        pdf.set_fill_color(*fc)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(w_m, 5.5, mod, border=1, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(w_d, 5.5, desc, border=1, fill=True)
        pdf.ln()

    # ======================================================
    # SECTION 6: SENSOR DATA SIMULATION (NG SCENARIOS)
    # ======================================================
    pdf.add_page()
    pdf.h1("6. Sensor Data Simulation - NG Defect Scenarios")

    pdf.p(
        "Since we cannot access the real factory, we simulate realistic sensor data including "
        "NG (Not Good) scenarios. Each scenario mimics an actual defect mode observed in bearing "
        "manufacturing. The simulation generates time-series data that can be fed into the "
        "Laravel system via the same REST API as real machines - making the demo fully realistic."
    )

    pdf.h2("6.1 Normal (OK) Data Ranges per Machine")
    pdf.note(
        "These ranges are based on industry standards for precision bearing grinding. "
        "In simulation, generate random values within these ranges for 'OK' parts.",
        color=(220, 255, 220)
    )

    normal_ranges = [
        ("Grinding Machine", "Spindle Motor Current", "8.5 - 11.0 A", "Centerline ~9.8A"),
        ("Grinding Machine", "Coolant Temperature", "18 - 22 degC", "Process spec max 25degC"),
        ("Grinding Machine", "Workpiece OD", "Nominal +/- 5 micron", "e.g. 52.000 +/- 0.005mm"),
        ("Grinding Machine", "Surface Roughness Ra", "0.10 - 0.25 micron", "Spec max Ra 0.32"),
        ("Grinding Machine", "Roundness", "0.1 - 0.4 micron", "Spec max 0.5 micron"),
        ("Furnace", "Zone 1-2 Temp (Carburize)", "920 - 930 degC", "+/-5 degC allowed"),
        ("Furnace", "Zone 3-4 Temp (Diffuse)", "880 - 895 degC", "+/-5 degC allowed"),
        ("Furnace", "Carbon Potential", "0.82 - 0.88 %C", "Spec 0.80-0.90 %C"),
        ("Furnace", "Quench Oil Temp", "40 - 55 degC", "Spec 35-65 degC"),
        ("Noise/Vib Tester", "Anderon Low Band", "0 - 2.5 mA", "Spec max 3.5 mA"),
        ("Noise/Vib Tester", "Anderon Medium Band", "0 - 2.0 mA", "Spec max 3.0 mA"),
        ("Noise/Vib Tester", "Anderon High Band", "0 - 1.5 mA", "Spec max 2.5 mA"),
        ("Assembly Machine", "Axial Play", "15 - 30 micron", "Spec 10-45 micron"),
        ("Assembly Machine", "Grease Weight", "0.90 - 1.10 g", "Spec 0.85-1.15 g"),
    ]

    w = [35, 42, 40, 63]
    pdf.th([("Machine", w[0]), ("Parameter", w[1]), ("Normal Range", w[2]), ("Notes", w[3])])
    for i, row in enumerate(normal_ranges):
        shade = (i % 2 == 0)
        pdf.tr(row, w, shade=shade, bold_first=True)

    pdf.ln(3)
    pdf.h2("6.2 NG Defect Scenarios with Sensor Signature")

    scenarios = [
        {
            "id": "NG-001",
            "name": "Grinding Burn (Thermal Damage on Raceway)",
            "machine": "CNC Cylindrical / Surface Grinder",
            "cause": "Excessive grinding aggression, insufficient coolant, worn grinding wheel",
            "sensor_signature": [
                "Spindle motor current SPIKES: 11.0A -> 13.5A (sudden 20% increase)",
                "Coolant temperature RISES: 22degC -> 28-35degC over 15 minutes",
                "Surface Roughness Ra INCREASES: 0.25 -> 0.50-0.80 micron",
                "Dimension DRIFT: OD creep of +3 to +5 micron due to thermal expansion",
                "AE (Acoustic Emission) spike if sensor fitted",
            ],
            "ng_rate": "0.2 - 0.5% of parts in an affected batch",
            "detection": "In-process Ra sensor or CMM, or downstream hardness re-test",
            "simulation": "Inject current spike every 450th part, ramp up Ra from part 440 onwards",
        },
        {
            "id": "NG-002",
            "name": "Out-of-Spec Dimension (OD Oversize)",
            "machine": "CNC Grinding + Gauging Machine",
            "cause": "Wheel wear compensation not triggered, thermal expansion, gauge drift",
            "sensor_signature": [
                "Gauging machine OD measurement DRIFTS: +0.000mm -> +0.007mm over 200 parts",
                "SPC Xbar chart shows upward TREND (Western Electric Rule 2 violation)",
                "Individual parts still within spec, but trend predicts out-of-spec in 50 parts",
                "Cp value decreases: 1.67 -> 1.20 -> 0.95 (below 1.0 = process not capable)",
            ],
            "ng_rate": "5-15% of batch if undetected and uncorrected",
            "detection": "SPC real-time trend alert, auto alert when Cpk < 1.33",
            "simulation": "Linear drift model: add 0.00003mm per part to OD reading from part 100",
        },
        {
            "id": "NG-003",
            "name": "Furnace Carbon Potential Deviation (Soft Bearing)",
            "machine": "Heat Treatment Furnace",
            "cause": "O2 probe failure, gas flow problem, endothermic generator issue",
            "sensor_signature": [
                "Carbon potential DROPS: 0.85%C -> 0.70%C over 30 minutes",
                "Zone 2 temperature FLUCTUATES: +/-12degC (vs spec +/-5degC)",
                "Gas CO flow DROPS: 8 L/min -> 4 L/min",
                "Downstream hardness test FAILS: HRC 55 (spec min 58 HRC)",
                "Alarm code sequence: CP_LOW, then GAS_FLOW_LOW",
            ],
            "ng_rate": "Full batch at risk (entire furnace load = 500-5000 parts)",
            "detection": "Carbon potential sensor, with 15-minute SPC on CP trend",
            "simulation": "Sinusoidal CP drift injected at T=60min, hardness calculated as linear function of CP",
        },
        {
            "id": "NG-004",
            "name": "High Anderon Level (Noise Failure)",
            "machine": "Noise / Vibration Tester",
            "cause": "Raceway surface defect, contamination in bearing, cage damage in assembly",
            "sensor_signature": [
                "Anderon Medium Band EXCEEDS spec: 3.5 mA (spec max 3.0 mA)",
                "FFT shows abnormal peak at BPFO (Ball Pass Frequency Outer race) = inner defect",
                "Low Band and High Band remain OK - only medium band affected",
                "Visual inspection shows micro-indentation on outer raceway",
            ],
            "ng_rate": "0.01 - 0.1% in controlled production, higher if grinding issue upstream",
            "detection": "100% noise test at end of line. Automatic reject chute activated.",
            "simulation": "Random 1-in-500 parts gets Anderon Medium spike drawn from Beta(2,1.5) distribution",
        },
        {
            "id": "NG-005",
            "name": "Assembly - Wrong Grease Volume",
            "machine": "Greasing Station (Assembly)",
            "cause": "Nozzle clog, pump wear, recipe parameter error",
            "sensor_signature": [
                "Grease dispenser weight drops: 1.00g -> 0.55g (TARGET 0.90-1.10g)",
                "Alarm generated: GREASE_UNDER_FILL after 3 consecutive NG",
                "Cycle time INCREASES slightly as system retries (if equipped with retry logic)",
                "NOTE: Under-greased bearing = premature failure in customer vehicle",
            ],
            "ng_rate": "Can be 100% of output until nozzle is cleaned (minutes to hours)",
            "detection": "Gravimetric check on every cycle; stop production if 3 consecutive NG",
            "simulation": "Nozzle clog starts at part 200: grease drops exponentially from 1.0 to 0.4g over 20 parts",
        },
    ]

    for s in scenarios:
        pdf.space(45)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(0, 60, 130)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(EW, 6, f"  {s['id']} - {s['name']}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)

        info_rows = [
            ("Machine:", s["machine"]),
            ("Root Cause:", s["cause"]),
            ("NG Rate:", s["ng_rate"]),
            ("Detection Method:", s["detection"]),
            ("Simulation Logic:", s["simulation"]),
        ]
        for label, val in info_rows:
            pdf.set_x(MARGIN + 3)
            pdf.set_font("Helvetica", "B", 8.5)
            w_l = pdf.get_string_width(label + "  ")
            pdf.cell(w_l, 5, label)
            pdf.set_font("Helvetica", "", 8.5)
            pdf.multi_cell(EW - 3 - w_l, 5, val)

        pdf.set_x(MARGIN + 3)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(0, 5, "Sensor Signature:", new_x="LMARGIN", new_y="NEXT")
        for sig in s["sensor_signature"]:
            pdf.set_x(MARGIN + 6)
            pdf.set_font("Helvetica", "", 8)
            pdf.multi_cell(EW - 6, 4.5, "  > " + sig)
        pdf.ln(3)

    # ======================================================
    # SECTION 7: SIMULATION DATA SCHEMA (DATABASE TABLES)
    # ======================================================
    pdf.add_page()
    pdf.h1("7. Database Schema for Sensor Data Simulation")

    pdf.p(
        "The following schema covers both TimescaleDB (sensor time-series) and MySQL "
        "(transactional / plan data). These tables form the foundation of the simulation system."
    )

    pdf.h2("7.1 TimescaleDB: Sensor Data Tables (Real-Time DB)")

    tables_ts = [
        ("sensor_grinding", [
            ("id", "BIGINT", "Auto-increment primary key"),
            ("time", "TIMESTAMPTZ", "Hypertable partition key (required by TimescaleDB)"),
            ("machine_id", "VARCHAR(20)", "FK to machines table in MySQL"),
            ("part_serial", "VARCHAR(30)", "Part barcode scanned on entry"),
            ("spindle_current_a", "FLOAT", "Spindle motor current (Amps)"),
            ("coolant_temp_c", "FLOAT", "Coolant temperature (degC)"),
            ("workpiece_od_um", "FLOAT", "Outer diameter in micrometers (nominal = 0, deviation)"),
            ("surface_ra_um", "FLOAT", "Surface roughness Ra in microns"),
            ("roundness_um", "FLOAT", "Roundness deviation in microns"),
            ("wheel_rpm", "INT", "Grinding wheel speed"),
            ("part_result", "TINYINT", "0=OK, 1=NG (dimensional), 2=NG (surface), 3=NG (roundness)"),
            ("ng_reason", "VARCHAR(50)", "NG classification if part_result > 0"),
        ]),
        ("sensor_furnace", [
            ("id", "BIGINT", "Auto-increment primary key"),
            ("time", "TIMESTAMPTZ", "Hypertable partition key"),
            ("furnace_id", "VARCHAR(20)", "FK to machines table"),
            ("batch_id", "VARCHAR(30)", "Production batch/lot number"),
            ("zone_1_temp_c", "FLOAT", "Zone 1 temperature"),
            ("zone_2_temp_c", "FLOAT", "Zone 2 temperature"),
            ("zone_3_temp_c", "FLOAT", "Zone 3 temperature (diffuse)"),
            ("zone_4_temp_c", "FLOAT", "Zone 4 temperature (diffuse)"),
            ("carbon_potential_pct", "FLOAT", "Carbon potential %C"),
            ("quench_oil_temp_c", "FLOAT", "Quench oil temperature"),
            ("ch4_flow_lpm", "FLOAT", "Methane gas flow L/min"),
            ("alarm_code", "VARCHAR(30)", "Active alarm code from PLC (NULL if none)"),
        ]),
        ("sensor_noise_test", [
            ("id", "BIGINT", "Auto-increment primary key"),
            ("time", "TIMESTAMPTZ", "Test timestamp"),
            ("tester_id", "VARCHAR(20)", "FK to machines table"),
            ("part_serial", "VARCHAR(30)", "Part barcode linked to full production history"),
            ("anderon_low_ma", "FLOAT", "Anderon Low Band (mA)"),
            ("anderon_mid_ma", "FLOAT", "Anderon Mid Band (mA)"),
            ("anderon_high_ma", "FLOAT", "Anderon High Band (mA)"),
            ("test_rpm", "INT", "RPM during test"),
            ("test_result", "TINYINT", "0=OK, 1=NG-Low, 2=NG-Mid, 3=NG-High, 4=NG-Impact"),
            ("axial_play_um", "FLOAT", "Axial play measurement"),
            ("radial_play_um", "FLOAT", "Radial play measurement"),
        ]),
    ]

    for tname, cols in tables_ts:
        pdf.space(30)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(0, 100, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(EW, 5.5, f"  TABLE: {tname}  (TimescaleDB Hypertable)", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.th([("Column", 50), ("Data Type", 30), ("Description", 100)])
        for i, (col, dtype, desc) in enumerate(cols):
            shade = (i % 2 == 0)
            fc = (240, 255, 240) if shade else (252, 252, 252)
            pdf.set_x(MARGIN)
            pdf.set_fill_color(*fc)
            pdf.set_font("Courier", "B" if i <= 1 else "", 7.5)
            pdf.cell(50, 5, col, border=1, fill=True)
            pdf.set_font("Courier", "", 7.5)
            pdf.cell(30, 5, dtype, border=1, fill=True)
            pdf.set_font("Helvetica", "", 7.5)
            pdf.cell(100, 5, desc, border=1, fill=True)
            pdf.ln()
        pdf.ln(3)

    pdf.h2("7.2 MySQL: Transactional Tables")

    mysql_tables = [
        ("work_orders", [
            ("id / wo_number / part_number", "Work order details, part spec FK"),
            ("target_qty / produced_qty / ng_qty", "Production tracking counters"),
            ("shift / line_id / machine_id", "Which shift, line, machine assignment"),
            ("planned_start / actual_start / end_time", "Schedule vs actual"),
            ("status", "ENUM: planned, in_progress, completed, on_hold"),
        ]),
        ("quality_specs", [
            ("part_number / revision", "Product identifier"),
            ("od_nominal_mm / od_tol_plus_um / od_tol_minus_um", "OD specification"),
            ("id_nominal_mm / id_tol_plus_um / id_tol_minus_um", "ID specification"),
            ("anderon_low_max / anderon_mid_max / anderon_high_max", "Noise limits by ABEC class"),
            ("ra_max_um / roundness_max_um / axial_play_min_um / axial_play_max_um", "Surface/play specs"),
            ("heat_treat_hardness_min_hrc / carbon_potential_min_pct / max_pct", "Furnace specs"),
        ]),
        ("ng_records", [
            ("id / part_serial / wo_id / machine_id", "Traceability links"),
            ("ng_type", "ENUM: dimensional, surface, vibration, hardness, grease, visual"),
            ("ng_value / ng_spec_limit", "What was measured vs what was allowed"),
            ("detected_at / detected_by_user", "When and by whom (or which machine)"),
            ("root_cause / corrective_action / disposition", "8D fields"),
            ("status", "ENUM: open, investigating, closed"),
        ]),
        ("machines", [
            ("id / machine_code / name / type", "Machine master data"),
            ("line_id / location", "Physical location on floor"),
            ("last_maintenance / next_maintenance", "PM schedule tracking"),
            ("status", "ENUM: running, idle, maintenance, breakdown"),
            ("opc_ua_endpoint / modbus_address", "Connection config for Edge Gateway"),
        ]),
    ]

    for tname, cols in mysql_tables:
        pdf.space(25)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(130, 60, 0)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(EW, 5.5, f"  TABLE: {tname}  (MySQL)", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.th([("Key Columns", 70), ("Purpose", 110)])
        for i, (cols_text, desc) in enumerate(cols):
            shade = (i % 2 == 0)
            fc = (255, 245, 230) if shade else (252, 252, 252)
            pdf.set_x(MARGIN)
            pdf.set_fill_color(*fc)
            pdf.set_font("Courier", "", 8)
            pdf.cell(70, 5, cols_text[:40] + ("..." if len(cols_text) > 40 else ""), border=1, fill=True)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(110, 5, desc, border=1, fill=True)
            pdf.ln()
        pdf.ln(3)

    # ======================================================
    # SECTION 8: LARAVEL + REALTIME STACK IMPLEMENTATION
    # ======================================================
    pdf.add_page()
    pdf.h1("8. Laravel + Real-Time Stack Implementation Plan")

    pdf.h2("8.1 Laravel API Architecture")
    pdf.p("Recommended directory structure additions to standard Laravel (inside app/ and routes/):")

    pdf.set_font("Courier", "", 8)
    code = [
        "app/",
        "  Http/Controllers/",
        "    SensorDataController.php    <- receives POST from Edge Gateway",
        "    ProductionPlanController.php <- CRUD for work orders",
        "    QualitySpecController.php    <- manage product specifications",
        "    NGRecordController.php       <- NG record management",
        "    ReportController.php         <- generate reports",
        "    DashboardController.php      <- real-time dashboard data",
        "  Events/",
        "    SensorDataReceived.php       <- Laravel Event for WebSocket push",
        "    NGPartDetected.php           <- triggers alert broadcast",
        "    SPCAlarmTriggered.php        <- SPC rule violation event",
        "  Jobs/",
        "    ProcessSensorBatch.php       <- queued job to write to TimescaleDB",
        "    SendAlertNotification.php    <- email/SMS alert job",
        "  Services/",
        "    SPCCalculatorService.php     <- Xbar-R, Cpk calculation",
        "    NGClassificationService.php  <- classify NG type automatically",
        "routes/",
        "  api.php   <- /api/v1/sensor-data, /api/v1/ng-records etc.",
        "  web.php   <- dashboard routes, auth routes",
    ]
    for line in code:
        pdf.set_x(MARGIN + 2)
        if "<-" in line:
            pdf.set_text_color(0, 100, 0)
        else:
            pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)

    pdf.h2("8.2 Real-Time Communication Stack")
    realtime_options = [
        ("Option A (Simplest)", "Laravel Reverb (Official WebSocket)",
         "Laravel 11+ built-in WebSocket server. No external dependency. "
         "Uses Laravel Echo on frontend. Free, self-hosted. "
         "Recommended if on local server / intranet. Low latency ~ 50ms.",
         (0, 150, 60)),
        ("Option B (Scalable)", "Pusher + Laravel Echo",
         "Pusher handles WebSocket infrastructure (cloud). "
         "Laravel broadcasts to Pusher channel, Vue.js/Blade listens via Laravel Echo. "
         "Very easy to implement. Free tier: 100 connections, 200K messages/day - enough for demo. "
         "Easy swap to self-hosted Soketi (open-source Pusher-compatible).",
         (0, 100, 200)),
        ("Option C (Advanced)", "Redis Pub/Sub + Soketi",
         "Redis as message queue between Laravel and WebSocket server. "
         "Use when horizontal scaling needed (multiple Laravel instances). "
         "Soketi is self-hosted open-source Pusher replacement. "
         "Best for production when 100+ concurrent users on dashboard.",
         (100, 0, 150)),
    ]
    for opt, name, desc, color in realtime_options:
        pdf.space(25)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(*color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(EW, 5.5, f"  {opt}: {name}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(MARGIN + 3)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(EW - 3, 5, desc)
        pdf.ln(2)

    pdf.note("RECOMMENDATION: Use Laravel Reverb for the simulation demo (zero external cost, "
             "works on local development server). Present Option B (Pusher) as production path.", 
             color=(220, 255, 220))

    # ======================================================
    # SECTION 9: POWER BI ANALYTICS LAYER
    # ======================================================
    pdf.add_page()
    pdf.h1("9. Power BI Analytics Layer Design")

    pdf.p(
        "Power BI connects to MySQL (historical DB) for analytical reporting. "
        "The following reports are tailored to what a QC Manager at NSK would actually need daily."
    )

    reports = [
        ("Daily QC Dashboard", "DirectQuery + Import",
         [
             "Total Production vs Target (gauge chart per line)",
             "NG Count and NG Rate % by machine (today)",
             "Anderon failure rate trend - 7 day rolling",
             "SPC status indicator: Green/Yellow/Red per parameter",
             "Top 3 NG types (Pareto chart auto-refresh 15 min)",
         ]),
        ("Grinding Process SPC Report", "Import (refreshed hourly)",
         [
             "Xbar-R Control Chart: OD, Ra, Roundness per machine",
             "Cp / Cpk trend chart (target > 1.67)",
             "Grinder-to-grinder comparison (which machine is drifting?)",
             "Wheel life consumption: dress count vs surface quality",
             "Correlation: Coolant temp rise vs Ra increase (scatter plot)",
         ]),
        ("Furnace Quality Report", "Import (refreshed per batch)",
         [
             "Temperature profile replay per batch (line chart all 4 zones)",
             "Carbon potential compliance % by batch",
             "Hardness distribution (box plot) - batch vs batch comparison",
             "Alarm frequency by furnace ID (pareto)",
             "Correlation: CP deviation vs downstream hardness failure rate",
         ]),
        ("Noise Test Analytics", "Import (daily)",
         [
             "Anderon pass/fail rate trend by product (line chart)",
             "Defect class breakdown: Low/Mid/High/Impact (stacked bar)",
             "Top NG hours (heatmap: day x hour - when do most NGs occur?)",
             "Serial number drill-through: click NG part to see full traceability",
             "Week-on-week NG rate comparison by part number",
         ]),
        ("NG Root Cause Analysis", "Import (weekly/monthly)",
         [
             "NG Pareto by type, machine, shift, operator",
             "Mean Time Between Failures (MTBF) by machine",
             "Corrective action open/closed status tracker",
             "Cost of Quality estimation (scrap value in IDR)",
             "Repeat NG rate: same machine recurring in 30 days?",
         ]),
    ]

    for report_name, mode, bullets in reports:
        pdf.space(35)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(0, 90, 120)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(EW, 6, f"  {report_name}  [{mode}]", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        for bul in bullets:
            pdf.set_x(MARGIN + 5)
            pdf.set_font("Helvetica", "", 8.5)
            pdf.multi_cell(EW - 5, 5, "  - " + bul)
        pdf.ln(2)

    # ======================================================
    # SECTION 10: NSK SUPPLY CHAIN MAP
    # ======================================================
    pdf.add_page()
    pdf.h1("10. NSK Indonesia Supply Chain Map - Research")

    pdf.p(
        "Understanding NSK's value chain positions Reyza to connect the QC system's importance "
        "to BUSINESS IMPACT in the interview. A defect that escapes NSK reaches these customers."
    )

    pdf.h2("10.1 Estimated Key Customers (NSK Bearing Buyers in Indonesia)")
    customers = [
        ("Toyota Motor Manufacturing Indonesia", "TMMIN", "Karawang", "Tapered roller bearings, hub units, transmission bearings"),
        ("Astra Honda Motor", "AHM", "Sunter, Jakarta", "Wheel bearings, engine bearings for motorcycles"),
        ("PT. Honda Prospect Motor", "HPM", "Karawang", "Ball bearings, hub units for cars"),
        ("Suzuki Indomobil Motor", "SIM", "Cakung, Jakarta", "Bearings for Ertiga, Carry, Baleno"),
        ("Yamaha Indonesia Motor Mfg", "YIMM", "Pulogadung, Jakarta", "Motorcycle wheel & crankshaft bearings"),
        ("PT. Mitsubishi Motors KY", "MMKI", "Bekasi", "Bearings for Xpander, L300, Pajero"),
        ("PT. Krama Yudha Ratu Motor", "KYM", "Bekasi", "Mitsubishi truck bearings (Fuso)"),
        ("PT. Denso Indonesia", "DENSO", "MM2100, Cikarang", "Bearings for cooling fans, alternators"),
        ("PT. JTEKT Indonesia", "JTEKT", "MM2100, Cikarang", "OEM steering bearings (sister company relationship)"),
        ("PT. Daikin Industries Indonesia", "Daikin", "Cikarang", "Bearings for AC compressors"),
    ]

    w = [55, 18, 35, 72]
    pdf.th([("Customer", w[0]), ("Code", w[1]), ("Location", w[2]), ("Bearing Application", w[3])])
    for i, row in enumerate(customers):
        shade = (i % 2 == 0)
        pdf.tr(list(row), w, shade=shade, bold_first=True)

    pdf.ln(4)
    pdf.h2("10.2 Estimated Key Vendors / Suppliers to NSK Indonesia")
    suppliers = [
        ("Krakatau Steel / Nippon Steel", "Japan/Cilegon", "Bearing steel SUJ2 / SCM420 raw material"),
        ("Chuetsu Metal Works / Sumitomo Metal", "Japan (import)", "High-purity bearing steel tubes, blanks"),
        ("PT. AKS Precision Ball Indonesia", "MM2100, Cikarang", "Steel balls (NSK sister company, same complex)"),
        ("PT. NSK-Warner Indonesia", "MM2100, Cikarang", "Cage components (NSK group company)"),
        ("NOK Corporation (via local agent)", "Japan/Indonesia", "Rubber seals and shields"),
        ("Koyo Chemicals (JTEKT group)", "Japan/local", "Lubricants and greases for bearing packing"),
        ("3M / Loctite distributor", "Local", "Thread-locking compounds, adhesives for assembly"),
        ("Fanuc ROBOMACHINE / JTEKT Toyoda", "Japan (via agent)", "CNC Grinder and Lathe spare parts"),
        ("Marposs Indonesia", "Jakarta/import", "Gauging equipment, LVDT probes, air gauge heads"),
        ("Mitutoyo Indonesia", "Jakarta", "CMM, hardness testers, micrometers (QC instruments)"),
        ("Ipsen International", "Germany/agent", "Heat treatment furnace parts, atmosphere controllers"),
    ]

    w2 = [60, 40, 80]
    pdf.th([("Supplier / Vendor", w2[0]), ("Origin / Location", w2[1]), ("What They Supply", w2[2])])
    for i, row in enumerate(suppliers):
        shade = (i % 2 == 0)
        pdf.tr(list(row), w2, shade=shade, bold_first=True)

    pdf.ln(4)
    pdf.note(
        "INTERVIEW STRATEGY: Mentioning this supply chain in interviews shows Reyza understands "
        "the BUSINESS CONTEXT of QC digitalization - not just the technology. "
        "E.g.: 'A furnace CP deviation in your plant could create hardness failures in TMMIN's "
        "Fortuner gearbox bearings, causing a warranty claim and supply chain disruption.'",
        color=(255, 250, 200)
    )

    # ======================================================
    # SECTION 11: 30-DAY IMPLEMENTATION ROADMAP
    # ======================================================
    pdf.add_page()
    pdf.h1("11. Proposed 30-Day Implementation Roadmap (Demo-Ready)")

    pdf.p(
        "This roadmap shows how Reyza would deliver a working simulation system in 30 days "
        "- demonstrating project management skill as well as technical execution."
    )

    roadmap = [
        ("Week 1\n(Days 1-7)", "Foundation & Data Layer",
         [
             "Set up TimescaleDB + MySQL on local/cloud server",
             "Create all sensor tables and MySQL transactional tables",
             "Build data simulator (Python) generating realistic sensor streams for all 5 NG scenarios",
             "Define API contracts (JSON payload schema) for each machine type",
             "Install and configure MQTT Mosquitto broker",
         ]),
        ("Week 2\n(Days 8-14)", "Laravel API + Edge Simulation",
         [
             "Build Laravel REST API: POST /sensor-data endpoint per machine type",
             "Implement Edge Gateway simulator (Python/Node.js) pushing data to Laravel API",
             "Build Laravel Event system: SensorDataReceived, NGPartDetected events",
             "Add Redis queue for processing heavy sensor batch writes",
             "Implement SPC calculator service (Western Electric Rules)",
         ]),
        ("Week 3\n(Days 15-21)", "Real-Time Dashboard",
         [
             "Configure Laravel Reverb (or Pusher) WebSocket server",
             "Build real-time Blade/Vue dashboard: live sensor gauges, SPC chart, NG counter",
             "Implement alert broadcast: NG detected -> WebSocket push -> browser alert (toast notification)",
             "Build production plan CRUD module (work orders, product spec management)",
             "Add RBAC: Operator, QC Inspector, Supervisor, Manager roles",
         ]),
        ("Week 4\n(Days 22-30)", "Power BI + Polish + Demo",
         [
             "Connect Power BI to MySQL - build all 5 report pages (Daily QC, SPC, Furnace, Noise, RCA)",
             "Create DAX measures: NG%, Cpk, Anderon pass rate, OEE",
             "Polish dashboard UI (make it look professional for interview demo)",
             "Run full simulation: inject NG-001 through NG-005 scenarios, verify system detects all",
             "Prepare 10-minute live demo script: normal operation -> NG event -> alert -> investigation",
         ]),
    ]

    for week, title, tasks in roadmap:
        pdf.space(40)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(0, 60, 130)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(EW, 6, f"  {week.replace(chr(10), ' ')} - {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        for t in tasks:
            pdf.set_x(MARGIN + 5)
            pdf.set_font("Helvetica", "", 8.5)
            pdf.multi_cell(EW - 5, 5, "  [ ]  " + t)
        pdf.ln(2)

    # ======================================================
    # SECTION 12: INTERVIEW TALKING POINTS
    # ======================================================
    pdf.add_page()
    pdf.h1("12. Interview Talking Points (Use These!)")

    pdf.h2("12.1 When Asked: 'How would you digitalize our QC process?'")
    pdf.note(
        "Do NOT give a generic answer. Walk them through the ACTUAL 7 layers of the system "
        "using NSK-specific machine names and data points. Show the architecture diagram "
        "(Section 5.1) if possible on a printed copy.",
        color=(255, 235, 200)
    )
    talking_a = [
        "Start with the shop floor: 'I would map each critical QC checkpoint - grinding dimensional "
        "check, furnace carbon potential, and the Anderon noise test. These three stages have the "
        "highest defect risk and generate the most actionable data.'",
        "Move to communication: 'Modern CNC grinders (Toyoda, Mikrosa) support OPC-UA out of the box. "
        "For older PLCs, I would use Modbus TCP. For event-driven alerts from noise testers, "
        "MQTT with a Mosquitto broker gives sub-50ms latency.'",
        "Explain the dual database: 'I would separate real-time sensor streams into TimescaleDB "
        "(time-series optimized, 1M+ inserts/sec) from transactional records like WO and NG reports "
        "in MySQL. This keeps analytics fast and historical records auditable.'",
        "Describe the application: 'Laravel REST API as the central hub, with Laravel Reverb "
        "pushing real-time alerts to a web dashboard. When a furnace CP drops or an Anderon "
        "value spikes, the QC operator gets a browser alert within 2 seconds.'",
        "Close with Power BI: 'Historical analysis in Power BI - Anderon pass rate trend, "
        "SPC Cpk by grinder, furnace profile replay by batch. Management can see quality "
        "from their phone, engineer can drill down to individual part serial number.'",
    ]
    for i, txt in enumerate(talking_a):
        pdf.space(20)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(0, 70, 140)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(8, 5, f" {i+1}", fill=True)
        pdf.set_text_color(30, 30, 30)
        pdf.set_fill_color(235, 245, 255)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(EW - 8, 5, "  " + txt, fill=True)
        pdf.ln(1)

    pdf.ln(4)
    pdf.h2("12.2 When Asked: 'What data would you collect from a grinding machine?'")
    pdf.p(
        "Answer confidently with 8 specific data points from Section 3.1: "
        "Spindle motor current (grinding force proxy), coolant temperature, in-process OD via "
        "Marposs APC gauge, surface roughness from profilometer, roundness, wheel RPM, "
        "dress counter, and part result (OK/NG with reason code). "
        "Then add: 'These feed into SPC in real-time, so we catch process drift BEFORE "
        "parts go out-of-spec - preventing NG rather than just finding it.'"
    )

    pdf.h2("12.3 NSK-Specific Numbers to mention in interview")
    numbers = [
        ("3 million", "Bearings produced by NSK Group globally per day"),
        ("+/-0.5 micron", "Typical roundness tolerance for ABEC P5 class bearing raceway"),
        ("Ra < 0.1 micron", "Surface finish target after superfinishing - finer than human hair (0.17mm / 170,000 micron)"),
        ("58-65 HRC", "Target hardness range after heat treatment (bearing steel SUJ2)"),
        ("0.80-0.90 %C", "Carbon potential target during carburizing heat treatment"),
        ("IEC 62541", "Standard number for OPC-UA protocol"),
        ("QS-9000 / IATF 16949", "Quality management standard for automotive suppliers (NSK complies)"),
        ("6-sigma / 3.4 PPM", "NSK's target defect rate for safety-critical bearing components"),
        ("L10 life", "Bearing life rating: 90% of bearings exceed this life under stated load/speed"),
    ]

    w = [25, 155]
    pdf.th([("Number", w[0]), ("Context", w[1])])
    for i, (num, ctx) in enumerate(numbers):
        shade = (i % 2 == 0)
        pdf.tr([num, ctx], w, shade=shade, bold_first=True)

    # ======================================================
    # FINAL PAGE: QUICK REFERENCE SUMMARY
    # ======================================================
    pdf.add_page()
    pdf.h1("Quick Reference - System Architecture Summary")

    boxes = [
        ("SHOP FLOOR (Input Layer)", [
            "CNC Grinder      -> OPC-UA -> dimensional, Ra, roundness, current",
            "Heat Furnace     -> Modbus -> temps, carbon %, quench, alarms",
            "Noise Tester     -> OPC-UA -> Anderon L/M/H, FFT, pass/fail",
            "Assembly Machine -> OPC-UA -> force, axial play, grease weight",
            "Gauging Machine  -> RS232/OPC-UA -> 100% dimensional + SPC stream",
        ], (0, 80, 40)),
        ("EDGE GATEWAY (IPC per line)", [
            "OPC-UA Client    <- polls CNC, tester, assembly machines",
            "Modbus Client    <- polls furnace PLCs, flow meters",
            "MQTT Subscriber  <- receives events from smart sensors",
            "SQLite buffer    <- 24h offline storage if network drops",
            "REST POST        -> sends batch to Laravel every 500ms",
        ], (100, 50, 0)),
        ("LARAVEL APP (Central Hub)", [
            "REST API endpoint -> validates + stores sensor data",
            "MySQL (via Eloquent) -> WO, specs, NG records, users",
            "TimescaleDB (raw) -> all sensor time-series data",
            "Laravel Events + Reverb -> pushes NG alerts via WebSocket",
            "SPC Service -> calculates Xbar-R, Cpk on every write",
        ], (0, 60, 130)),
        ("ANALYTICS (Output Layer)", [
            "Real-time dashboard (Vue/Blade+Echo) -> live shop floor view",
            "Power BI (DirectQuery/Import) -> historical analytics",
            "Email/SMS alerts (Laravel Mail+Queue) -> escalation",
            "PDF reports (Laravel DomPDF) -> daily QC summary",
            "Traceability lookup -> part serial -> full history chain",
        ], (80, 0, 120)),
    ]

    for title, items, color in boxes:
        pdf.space(35)
        pdf.set_x(MARGIN)
        pdf.set_fill_color(*color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.cell(EW, 6.5, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_fill_color(245, 248, 255)
        pdf.set_text_color(20, 20, 20)
        for item in items:
            pdf.set_x(MARGIN)
            pdf.set_font("Courier", "", 8)
            pdf.cell(EW, 5.5, "   " + item, fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    pdf.ln(4)
    pdf.set_x(MARGIN)
    pdf.set_fill_color(10, 10, 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(EW, 8, "  REYZA'S UNIQUE VALUE: The whole stack uses skills he already has.", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(230, 240, 255)
    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Helvetica", "", 9)
    stack_match = [
        "Laravel + MySQL     = Already in production use at PT Dharma Polimetal (4+ years)",
        "TimescaleDB         = PostgreSQL extension, same SQL syntax, 2-day learning curve",
        "OPC-UA / MQTT       = IoT experience (Arduino Andon build) + 1 week study to apply",
        "Power BI + DAX      = Active daily use, existing QC dashboards built",
        "Real-time WebSocket = Laravel Reverb / Echo, standard Laravel 11 feature",
        "SPC Calculation     = 7 QC Tools knowledge, Cpk formula is math not magic",
    ]
    for line in stack_match:
        pdf.set_x(MARGIN)
        pdf.cell(EW, 5.5, "   " + line, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    out_path = os.path.join(os.path.dirname(__file__), "NSK_QC_Technical_Deep_Dive_Report.pdf")
    pdf.output(out_path)
    print(f"Report saved: {out_path}")
    return out_path


if __name__ == "__main__":
    build()
