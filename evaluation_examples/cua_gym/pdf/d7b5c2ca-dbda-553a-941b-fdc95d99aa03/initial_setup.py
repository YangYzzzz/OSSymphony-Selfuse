"""
Initial Setup: Create a 15-page print-ready PDF with mixed embedded/referenced fonts
Task ID: pdf_gf2_043
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_043'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/print_ready.pdf'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    import pymupdf

    doc = pymupdf.open()

    # Page dimensions (A4)
    W, H = 595, 842

    # ---- Page 1: Title page with Helvetica (built-in, always embedded subset) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "Meridian Analytics Group",
                     fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 170), "Annual Print Production Report",
                     fontsize=20, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 210), "Fiscal Year 2025 — Confidential",
                     fontsize=14, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 260), "Prepared by: Document Services Division",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 285), "Date: March 15, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    # Draw a decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 230), pymupdf.Point(523, 230))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()

    # ---- Page 2: Table of Contents with Times (built-in) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents",
                     fontsize=22, fontname="tibo", color=(0, 0, 0))
    toc_items = [
        ("1. Executive Summary", 3),
        ("2. Production Volume Overview", 4),
        ("3. Quality Metrics", 5),
        ("4. Cost Analysis", 6),
        ("5. Equipment Utilization", 7),
        ("6. Substrate Inventory Report", 8),
        ("7. Color Accuracy Assessment", 9),
        ("8. Prepress Workflow Statistics", 10),
        ("9. Bindery & Finishing Operations", 11),
        ("10. Client Satisfaction Scores", 12),
        ("11. Environmental Compliance", 13),
        ("12. Staff Training Records", 14),
        ("13. Future Outlook & Recommendations", 15),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(72, y), title,
                         fontsize=12, fontname="tiro", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y), f"...{pg}",
                         fontsize=12, fontname="tiro", color=(0.4, 0.4, 0.4))
        y += 24

    # ---- Page 3: Executive Summary (Helvetica + Courier mix) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary",
                     fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    summary_text = (
        "The fiscal year 2025 marked a significant turning point for Meridian Analytics Group's "
        "print production division. Total output reached 4.2 million impressions, representing a "
        "17% increase over the previous year. Our investment in new Heidelberg Speedmaster XL 106 "
        "press technology contributed to a 23% improvement in color consistency scores. "
        "Waste reduction initiatives brought spoilage rates down to 2.1%, well below the industry "
        "average of 3.8%. Client satisfaction surveys returned an aggregate score of 94.7 out of 100, "
        "the highest in the division's 12-year history."
    )
    rect = pymupdf.Rect(72, 100, 523, 400)
    page.insert_textbox(rect, summary_text, fontsize=11, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Add a code-style note in Courier
    page.insert_text(pymupdf.Point(72, 430), "Reference Code: MAG-FY25-RPT-001",
                     fontsize=10, fontname="cour", color=(0.3, 0.3, 0.3))

    # ---- Page 4: Production Volume (Times + Helvetica) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Production Volume Overview",
                     fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    prod_text = (
        "Monthly production volumes showed consistent growth throughout the fiscal year. "
        "January through March averaged 310,000 impressions per month. The second quarter "
        "saw an acceleration to 360,000 per month following the commissioning of Press Unit 7. "
        "Peak production occurred in October with 425,000 impressions to meet holiday catalog demand."
    )
    rect = pymupdf.Rect(72, 100, 523, 280)
    page.insert_textbox(rect, prod_text, fontsize=11, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Table header
    y = 310
    headers = ["Month", "Impressions", "Waste %", "Uptime %"]
    x_positions = [72, 180, 320, 430]
    for x, h in zip(x_positions, headers):
        page.insert_text(pymupdf.Point(x, y), h,
                         fontsize=10, fontname="hebo", color=(0.1, 0.1, 0.4))
    # Table data
    months_data = [
        ("January", "295,400", "2.8%", "91.2%"),
        ("February", "308,200", "2.5%", "93.1%"),
        ("March", "326,100", "2.3%", "94.0%"),
        ("April", "345,600", "2.1%", "94.8%"),
        ("May", "358,900", "2.0%", "95.2%"),
        ("June", "372,400", "1.9%", "95.7%"),
    ]
    y += 22
    for row in months_data:
        for x, val in zip(x_positions, row):
            page.insert_text(pymupdf.Point(x, y), val,
                             fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # ---- Pages 5-8: Use external fonts (DejaVu) for variety ----
    # These will be embedded via TextWriter
    external_font_path = None
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]:
        if os.path.exists(candidate):
            external_font_path = candidate
            break

    external_bold_path = None
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]:
        if os.path.exists(candidate):
            external_bold_path = candidate
            break

    external_serif_path = None
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ]:
        if os.path.exists(candidate):
            external_serif_path = candidate
            break

    page_contents = [
        ("3. Quality Metrics",
         "Our quality control department conducted 12,480 inspections during FY2025. "
         "Color accuracy, measured using spectrophotometric analysis against Pantone standards, "
         "achieved a Delta-E average of 1.2 — well within the acceptable tolerance of 2.0. "
         "Registration accuracy improved to +/- 0.05mm across all press units. "
         "Dot gain on coated stock averaged 14% at 50% midtone, consistent with GRACoL specifications."),
        ("4. Cost Analysis",
         "Total production costs for FY2025 were $3,847,200, broken down as follows: "
         "substrate costs at $1,423,100 (37%), ink and consumables at $578,600 (15%), "
         "labor at $1,154,400 (30%), equipment depreciation at $462,200 (12%), and "
         "overhead at $228,900 (6%). Cost per impression decreased 8.3% to $0.916."),
        ("5. Equipment Utilization",
         "Press Unit 1 (Komori Lithrone G40): 2,847 operating hours, 94.2% uptime. "
         "Press Unit 3 (HP Indigo 12000 HD): 3,102 operating hours, 97.1% uptime for digital runs. "
         "Press Unit 5 (Heidelberg Speedmaster XL 106): 2,956 operating hours, 95.8% uptime. "
         "Press Unit 7 (commissioned Q2): 1,842 operating hours, 96.3% uptime since installation."),
        ("6. Substrate Inventory Report",
         "Current substrate inventory valued at $287,400. Key stock levels: "
         "80gsm uncoated bond — 42 pallets (168,000 sheets). "
         "130gsm gloss coated — 28 pallets (84,000 sheets). "
         "250gsm card stock — 15 pallets (30,000 sheets). "
         "350gsm board for packaging — 8 pallets (12,000 sheets). "
         "Specialty stocks (metallic, textured) — 6 pallets assorted."),
    ]

    for i, (heading, body) in enumerate(page_contents):
        page = doc.new_page(width=W, height=H)
        if external_bold_path:
            font_bold = pymupdf.Font(fontfile=external_bold_path)
            tw = pymupdf.TextWriter(page.rect)
            tw.append(pymupdf.Point(72, 72), heading, font=font_bold, fontsize=18)
            tw.write_text(page, color=(0.1, 0.1, 0.4))
        else:
            page.insert_text(pymupdf.Point(72, 72), heading,
                             fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))

        if external_font_path:
            font_regular = pymupdf.Font(fontfile=external_font_path)
            tw = pymupdf.TextWriter(page.rect)
            # Write body text line by line (rough wrapping)
            words = body.split()
            line = ""
            y_pos = 110
            for word in words:
                test_line = f"{line} {word}".strip()
                if len(test_line) * 5.5 > 451:  # approximate width check
                    tw.append(pymupdf.Point(72, y_pos), line, font=font_regular, fontsize=11)
                    y_pos += 16
                    line = word
                else:
                    line = test_line
            if line:
                tw.append(pymupdf.Point(72, y_pos), line, font=font_regular, fontsize=11)
            tw.write_text(page, color=(0, 0, 0))
        else:
            rect = pymupdf.Rect(72, 100, 523, 500)
            page.insert_textbox(rect, body, fontsize=11, fontname="helv",
                                color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Pages 9-11: Use Courier and mixed fonts ----
    more_contents = [
        ("7. Color Accuracy Assessment",
         "Spectrophotometer readings were taken on 500 randomly selected sheets per press run. "
         "Results for primary process colors: Cyan averaged Delta-E 0.9, Magenta averaged 1.1, "
         "Yellow averaged 0.8, and Black averaged 0.6. Spot color matching for Pantone Reflex Blue "
         "achieved Delta-E 1.4. Overall color consistency across a 50,000 impression run showed "
         "standard deviation of Delta-E 0.3, indicating excellent press stability."),
        ("8. Prepress Workflow Statistics",
         "The prepress department processed 2,847 jobs during FY2025. Average turnaround time "
         "from file receipt to plate-ready was 3.2 hours, down from 4.1 hours the previous year. "
         "CTP (Computer-to-Plate) output totaled 18,400 plates with a remake rate of 0.8%. "
         "PDF/X-4 compliance rate for incoming files improved to 89% following client education "
         "initiatives launched in Q1."),
        ("9. Bindery & Finishing Operations",
         "Bindery throughput for FY2025: Perfect binding — 892,000 units. Saddle stitching — "
         "1,247,000 units. Die cutting — 456,000 sheets. Folding operations — 3,100,000 impressions. "
         "UV coating applications — 1,850,000 sheets. Lamination (gloss and matte) — 620,000 sheets. "
         "Foil stamping — 178,000 impressions. Average bindery turnaround: 1.4 business days."),
    ]

    for heading, body in more_contents:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), heading,
                         fontsize=18, fontname="tibo", color=(0.1, 0.1, 0.4))
        rect = pymupdf.Rect(72, 100, 523, 500)
        page.insert_textbox(rect, body, fontsize=11, fontname="cour",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # ---- Page 12: Client Satisfaction (Helvetica-BoldOblique) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "10. Client Satisfaction Scores",
                     fontsize=18, fontname="hebi", color=(0.1, 0.1, 0.4))
    satisfaction_text = (
        "Annual client satisfaction survey results (100-point scale):\n"
        "Print Quality: 96.2\nDelivery Timeliness: 93.8\n"
        "Customer Service: 95.1\nPricing Competitiveness: 91.4\n"
        "Technical Support: 94.9\nOverall Satisfaction: 94.7\n\n"
        "Net Promoter Score: 72 (up from 65 in FY2024)\n"
        "Client retention rate: 97.3%\nNew client acquisitions: 34"
    )
    rect = pymupdf.Rect(72, 100, 523, 500)
    page.insert_textbox(rect, satisfaction_text, fontsize=11, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # ---- Page 13: Environmental (mixed serif) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "11. Environmental Compliance",
                     fontsize=18, fontname="tibo", color=(0.1, 0.1, 0.4))
    env_text = (
        "FSC Chain of Custody certification maintained (FSC-C012345). "
        "Recycled substrate usage increased to 34% of total volume. "
        "VOC emissions from press operations measured at 12.4 tonnes, "
        "a 15% reduction from FY2024 following the switch to low-VOC fountain solutions. "
        "Waste paper recycling rate: 98.2%. Ink waste properly disposed: 100%. "
        "Energy consumption: 1,247,000 kWh (down 6% due to LED UV curing retrofits). "
        "Carbon offset credits purchased: 450 tonnes CO2 equivalent."
    )
    rect = pymupdf.Rect(72, 100, 523, 400)
    page.insert_textbox(rect, env_text, fontsize=11, fontname="tiit",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 14: Staff Training (Symbol + ZapfDingbats for bullet points, Helvetica for body) ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "12. Staff Training Records",
                     fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    training_items = [
        "Color Management Certification (G7 Expert) — 8 staff completed",
        "Heidelberg Press Operations Level 3 — 5 operators certified",
        "HP Indigo Digital Front End Advanced — 3 technicians trained",
        "OSHA Workplace Safety Refresher — all 47 production staff",
        "Lean Manufacturing Workshop — 12 supervisors attended",
        "Adobe Creative Suite Prepress Integration — 6 prepress staff",
        "Environmental Health & Safety Module — all 62 employees",
    ]
    y = 110
    for item in training_items:
        # Use ZapfDingbats for bullet
        page.insert_text(pymupdf.Point(72, y), "4",
                         fontsize=10, fontname="zadb", color=(0.1, 0.4, 0.1))
        page.insert_text(pymupdf.Point(90, y), item,
                         fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # Use Symbol font for a section separator
    page.insert_text(pymupdf.Point(72, y + 20), "* * *",
                     fontsize=14, fontname="symb", color=(0.5, 0.5, 0.5))

    # ---- Page 15: Future Outlook (external serif if available + Courier) ----
    page = doc.new_page(width=W, height=H)
    if external_serif_path:
        font_serif = pymupdf.Font(fontfile=external_serif_path)
        tw = pymupdf.TextWriter(page.rect)
        tw.append(pymupdf.Point(72, 72), "13. Future Outlook & Recommendations",
                  font=font_serif, fontsize=18)
        tw.write_text(page, color=(0.1, 0.1, 0.4))
    else:
        page.insert_text(pymupdf.Point(72, 72), "13. Future Outlook & Recommendations",
                         fontsize=18, fontname="tibo", color=(0.1, 0.1, 0.4))

    outlook_text = (
        "Key recommendations for FY2026:\n\n"
        "1. Invest in automated inline inspection system (est. $285,000) to reduce manual QC "
        "sampling by 60% while improving defect detection rates.\n\n"
        "2. Expand digital print capacity with second HP Indigo unit to capture growing "
        "short-run and variable data market segment.\n\n"
        "3. Implement MIS/ERP integration between Hiflex MIS and SAP to streamline job costing "
        "and reduce administrative overhead by estimated 25%.\n\n"
        "4. Pursue ISO 14001 Environmental Management certification to strengthen competitive "
        "position with environmentally conscious clients.\n\n"
        "5. Launch operator apprenticeship program to address projected 15% workforce "
        "retirement attrition over next 3 years."
    )
    rect = pymupdf.Rect(72, 100, 523, 700)
    page.insert_textbox(rect, outlook_text, fontsize=11, fontname="cour",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Set document metadata
    doc.set_metadata({
        "title": "Meridian Analytics Group — Annual Print Production Report FY2025",
        "author": "Document Services Division",
        "subject": "Print Production Annual Report",
        "keywords": "print, production, annual report, FY2025",
        "creator": "Meridian Analytics Internal Systems",
        "producer": "PyMuPDF",
    })

    # Add a table of contents (bookmarks)
    toc = [
        [1, "Executive Summary", 3],
        [1, "Production Volume Overview", 4],
        [1, "Quality Metrics", 5],
        [1, "Cost Analysis", 6],
        [1, "Equipment Utilization", 7],
        [1, "Substrate Inventory Report", 8],
        [1, "Color Accuracy Assessment", 9],
        [1, "Prepress Workflow Statistics", 10],
        [1, "Bindery & Finishing Operations", 11],
        [1, "Client Satisfaction Scores", 12],
        [1, "Environmental Compliance", 13],
        [1, "Staff Training Records", 14],
        [1, "Future Outlook & Recommendations", 15],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open the PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
