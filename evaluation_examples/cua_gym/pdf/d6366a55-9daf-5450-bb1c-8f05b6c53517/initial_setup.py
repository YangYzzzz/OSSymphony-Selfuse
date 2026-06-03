"""
Initial Setup: Create a 6-page financial report PDF with tables on multiple pages
Task ID: pdf_cr_051
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_051'
PDF_PATH = f'{WORKDIR}/Desktop/financial.pdf'

# Page constants
W, H = 595, 842  # A4

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


def draw_table(page, x0, y0, headers, rows, col_widths, fontsize=9):
    """Draw a table with borders on a page. Returns y position after table."""
    shape = page.new_shape()
    row_height = 18
    total_width = sum(col_widths)
    num_rows = len(rows) + 1  # +1 for header

    # Draw header background
    header_rect = pymupdf.Rect(x0, y0, x0 + total_width, y0 + row_height)
    shape.draw_rect(header_rect)
    shape.finish(color=(0, 0, 0), fill=(0.2, 0.3, 0.5), width=0.5)

    # Draw header text
    cx = x0
    for i, hdr in enumerate(headers):
        page.insert_text(
            pymupdf.Point(cx + 4, y0 + 13),
            hdr,
            fontsize=fontsize,
            fontname="hebo",
            color=(1, 1, 1),
        )
        cx += col_widths[i]

    # Draw data rows
    for r_idx, row in enumerate(rows):
        ry = y0 + row_height * (r_idx + 1)
        # Alternating row background
        if r_idx % 2 == 0:
            bg_rect = pymupdf.Rect(x0, ry, x0 + total_width, ry + row_height)
            shape.draw_rect(bg_rect)
            shape.finish(color=None, fill=(0.93, 0.93, 0.96), width=0)

        cx = x0
        for c_idx, cell in enumerate(row):
            page.insert_text(
                pymupdf.Point(cx + 4, ry + 13),
                str(cell),
                fontsize=fontsize,
                fontname="helv",
                color=(0, 0, 0),
            )
            cx += col_widths[c_idx]

    # Draw grid lines
    total_h = row_height * num_rows
    # Horizontal lines
    for i in range(num_rows + 1):
        ly = y0 + row_height * i
        shape.draw_line(pymupdf.Point(x0, ly), pymupdf.Point(x0 + total_width, ly))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
    # Vertical lines
    cx = x0
    for i in range(len(col_widths) + 1):
        shape.draw_line(pymupdf.Point(cx, y0), pymupdf.Point(cx, y0 + total_h))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
        if i < len(col_widths):
            cx += col_widths[i]

    shape.commit()
    return y0 + total_h + 10


def create_initial():
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)
    doc = pymupdf.open()

    # ======== PAGE 1: Executive Summary with Revenue Table ========
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Meridian Financial Group", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Annual Financial Report - FY2025", fontsize=14, fontname="heit", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(523, 95))
    shape.finish(color=(0.1, 0.2, 0.4), width=1.5)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 120), "1. Revenue Summary", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    rect = pymupdf.Rect(72, 130, 523, 185)
    page.insert_textbox(rect,
        "The following table presents Meridian Financial Group's revenue breakdown by division "
        "for the fiscal year ending December 31, 2025. Total consolidated revenue reached $187.4M, "
        "representing a 12.3% year-over-year increase driven by strong performance in the Technology "
        "Solutions and Advisory Services divisions.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Table 1: Revenue by Division
    headers1 = ["Division", "Q1 Revenue", "Q2 Revenue", "Q3 Revenue", "Q4 Revenue", "Total"]
    rows1 = [
        ["Technology Solutions", "$12.8M", "$13.5M", "$14.2M", "$15.1M", "$55.6M"],
        ["Advisory Services", "$9.4M", "$10.1M", "$10.8M", "$11.3M", "$41.6M"],
        ["Wealth Management", "$8.2M", "$8.5M", "$8.9M", "$9.1M", "$34.7M"],
        ["Capital Markets", "$7.6M", "$8.0M", "$8.4M", "$8.8M", "$32.8M"],
        ["Insurance Products", "$5.1M", "$5.3M", "$5.6M", "$6.7M", "$22.7M"],
    ]
    col_widths1 = [110, 72, 72, 72, 72, 72]
    y_after = draw_table(page, 72, 195, headers1, rows1, col_widths1)

    rect2 = pymupdf.Rect(72, y_after + 10, 523, y_after + 80)
    page.insert_textbox(rect2,
        "Technology Solutions led all divisions with $55.6M in annual revenue, buoyed by the "
        "successful launch of the CloudVault enterprise platform in Q2. Advisory Services showed "
        "consistent growth each quarter, reflecting increased M&A activity in the mid-market segment.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Footer
    page.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(500, H - 40), "Page 1", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======== PAGE 2: Market Analysis (no table) ========
    page2 = doc.new_page(width=W, height=H)
    page2.insert_text(pymupdf.Point(72, 60), "2. Market Analysis & Strategic Outlook", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    paragraphs = [
        ("The global financial services landscape continued to evolve rapidly throughout 2025, "
         "shaped by rising interest rates, increasing regulatory scrutiny, and accelerating digital "
         "transformation across all market segments. Meridian Financial Group navigated these "
         "challenges effectively, leveraging its diversified business model and strategic technology "
         "investments to capture growth opportunities in both established and emerging markets."),
        ("In the technology sector, the proliferation of AI-driven analytics tools created significant "
         "demand for Meridian's CloudVault platform, particularly among mid-tier banks and regional "
         "insurance carriers seeking to modernize their data infrastructure. The platform's modular "
         "architecture and compliance-first design philosophy resonated strongly with risk-averse "
         "institutional buyers who had previously hesitated to adopt cloud-based solutions."),
        ("The advisory services division benefited from a resurgence in cross-border M&A activity, "
         "with notable transactions including the $2.3B acquisition of Nordic Insurance Holdings by "
         "Pacific Capital Partners, which Meridian advised on exclusively. The firm's deep sector "
         "expertise in financial technology and insurance proved decisive in winning several "
         "competitive mandates during the second half of the year."),
        ("Looking ahead to FY2026, management expects continued momentum in Technology Solutions "
         "and Advisory Services, with targeted growth initiatives in the Asia-Pacific region. The "
         "firm's strategic partnership with Harbin Digital, announced in Q4, is projected to "
         "contribute an incremental $8-12M in revenue through joint go-to-market activities in "
         "the Greater China and Southeast Asian markets."),
        ("Risk factors for the coming year include potential regulatory changes under the proposed "
         "Digital Markets Act amendments, which could impact revenue recognition timing for "
         "multi-year platform licensing agreements. Additionally, competitive pressure from "
         "fintech startups continues to compress margins in the wealth management segment."),
    ]

    y = 80
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, 523, y + 85)
        excess = page2.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                      color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 90

    page2.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(500, H - 40), "Page 2", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======== PAGE 3: Expense Breakdown with Table ========
    page3 = doc.new_page(width=W, height=H)
    page3.insert_text(pymupdf.Point(72, 60), "3. Operating Expenses", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    rect = pymupdf.Rect(72, 75, 523, 130)
    page3.insert_textbox(rect,
        "Operating expenses for FY2025 totaled $142.1M, a 9.8% increase over the prior year. "
        "Personnel costs remain the largest expense category at 58% of total operating expenses, "
        "reflecting strategic investments in talent acquisition across all divisions. Technology "
        "infrastructure spending increased 18% year-over-year as the firm continued its multi-year "
        "cloud migration initiative.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Table 2: Expense Breakdown
    headers2 = ["Category", "FY2024", "FY2025", "Change", "% of Total"]
    rows2 = [
        ["Personnel & Compensation", "$73.8M", "$82.4M", "+11.7%", "58.0%"],
        ["Technology Infrastructure", "$16.2M", "$19.1M", "+17.9%", "13.4%"],
        ["Office & Facilities", "$12.5M", "$12.9M", "+3.2%", "9.1%"],
        ["Professional Services", "$8.7M", "$9.4M", "+8.0%", "6.6%"],
        ["Marketing & BD", "$6.3M", "$7.2M", "+14.3%", "5.1%"],
        ["Regulatory & Compliance", "$4.9M", "$5.3M", "+8.2%", "3.7%"],
        ["Travel & Entertainment", "$3.1M", "$3.4M", "+9.7%", "2.4%"],
        ["Depreciation & Amort.", "$2.0M", "$2.4M", "+20.0%", "1.7%"],
    ]
    col_widths2 = [140, 70, 70, 65, 70]
    y_after3 = draw_table(page3, 72, 140, headers2, rows2, col_widths2)

    rect3 = pymupdf.Rect(72, y_after3 + 10, 523, y_after3 + 80)
    page3.insert_textbox(rect3,
        "The increase in depreciation and amortization expense (+20.0%) reflects the accelerated "
        "write-down of legacy on-premise infrastructure as the firm transitions workloads to "
        "cloud environments. Management anticipates this category will decline beginning in "
        "FY2027 as the migration completes.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page3.insert_text(pymupdf.Point(500, H - 40), "Page 3", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======== PAGE 4: Risk Assessment (no table) ========
    page4 = doc.new_page(width=W, height=H)
    page4.insert_text(pymupdf.Point(72, 60), "4. Risk Assessment & Governance", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    risk_paragraphs = [
        ("Meridian's Enterprise Risk Management framework was strengthened in FY2025 with the "
         "appointment of Dr. Elena Vasquez as Chief Risk Officer and the establishment of a "
         "dedicated Model Risk Governance committee. The firm's risk appetite statement was "
         "updated to reflect evolving market conditions and regulatory expectations, with "
         "particular emphasis on cybersecurity and operational resilience requirements."),
        ("Credit risk exposure remained well-controlled throughout the year, with the firm's "
         "capital markets division maintaining a weighted-average credit quality of A- across "
         "its fixed income portfolio. Counterparty risk is actively monitored through daily "
         "mark-to-market processes and stress testing scenarios that incorporate both historical "
         "and hypothetical tail risk events."),
        ("Operational risk incidents decreased 23% year-over-year, attributable to enhanced "
         "automated monitoring systems deployed in Q1 and comprehensive staff training programs "
         "covering cybersecurity awareness, data handling protocols, and business continuity "
         "procedures. The firm successfully passed its annual SOC 2 Type II audit with zero "
         "material findings for the third consecutive year."),
        ("Regulatory risk remains elevated given the pending Digital Markets Act amendments and "
         "proposed changes to capital adequacy requirements for non-bank financial institutions. "
         "Meridian's Government Affairs team continues to engage constructively with policymakers "
         "and industry groups to ensure the firm's perspective is represented in the rulemaking "
         "process. Legal reserves of $4.2M have been established for ongoing regulatory inquiries."),
    ]

    y = 80
    for para in risk_paragraphs:
        rect = pymupdf.Rect(72, y, 523, y + 90)
        page4.insert_textbox(rect, para, fontsize=10, fontname="helv",
                             color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 95

    page4.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page4.insert_text(pymupdf.Point(500, H - 40), "Page 4", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======== PAGE 5: Performance Metrics with Table ========
    page5 = doc.new_page(width=W, height=H)
    page5.insert_text(pymupdf.Point(72, 60), "5. Key Performance Indicators", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    rect = pymupdf.Rect(72, 75, 523, 125)
    page5.insert_textbox(rect,
        "The table below presents selected key performance indicators tracked by the Board of "
        "Directors on a quarterly basis. All metrics reflect consolidated group results and are "
        "presented in accordance with the firm's performance measurement framework.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Table 3: KPI Metrics
    headers3 = ["Metric", "FY2024", "FY2025", "Target", "Status"]
    rows3 = [
        ["Revenue Growth", "8.7%", "12.3%", "10.0%", "Exceeded"],
        ["Operating Margin", "24.1%", "24.2%", "23.0%", "Exceeded"],
        ["Client Retention Rate", "91.4%", "93.8%", "92.0%", "Exceeded"],
        ["Employee Satisfaction", "78/100", "82/100", "80/100", "Exceeded"],
        ["Net Promoter Score", "47", "52", "50", "Exceeded"],
        ["Regulatory Compliance", "98.2%", "99.1%", "99.0%", "Met"],
        ["Digital Adoption Rate", "64.3%", "78.9%", "75.0%", "Exceeded"],
        ["Incident Response Time", "4.2 hrs", "2.8 hrs", "3.0 hrs", "Exceeded"],
        ["Cost-to-Income Ratio", "76.2%", "75.8%", "76.0%", "Met"],
    ]
    col_widths3 = [130, 65, 65, 65, 70]
    y_after5 = draw_table(page5, 72, 135, headers3, rows3, col_widths3)

    rect5 = pymupdf.Rect(72, y_after5 + 10, 523, y_after5 + 65)
    page5.insert_textbox(rect5,
        "The firm exceeded targets on 7 of 9 tracked KPIs and met the remaining 2. Notably, "
        "digital adoption rate surged from 64.3% to 78.9%, exceeding the ambitious 75% target "
        "set by the Digital Transformation Steering Committee.",
        fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page5.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page5.insert_text(pymupdf.Point(500, H - 40), "Page 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ======== PAGE 6: Conclusion (no table) ========
    page6 = doc.new_page(width=W, height=H)
    page6.insert_text(pymupdf.Point(72, 60), "6. Forward Outlook & Strategic Priorities", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    conclusion_paragraphs = [
        ("FY2025 represented a year of strong execution and strategic progress for Meridian "
         "Financial Group. The firm delivered record revenue of $187.4M while maintaining "
         "disciplined cost management, resulting in an operating margin of 24.2% that exceeded "
         "the Board's target of 23.0%. These results demonstrate the effectiveness of the "
         "diversified business model and the ongoing investments in technology and talent."),
        ("Looking ahead to FY2026, the firm's strategic priorities center on three key pillars: "
         "(1) accelerating international expansion through the Harbin Digital partnership and "
         "targeted organic growth in Asia-Pacific markets; (2) deepening the CloudVault platform's "
         "capabilities with AI-powered analytics and automated compliance monitoring features; and "
         "(3) expanding the advisory services franchise into adjacent sectors including healthcare "
         "and clean energy infrastructure."),
        ("The Board of Directors has approved a capital allocation plan that includes $25M in "
         "technology infrastructure investment, $15M earmarked for strategic acquisitions in the "
         "insurtech and regtech spaces, and a 15% increase in the quarterly dividend reflecting "
         "confidence in the firm's earnings trajectory and capital position."),
        ("Management remains cautiously optimistic about the macroeconomic outlook while "
         "maintaining robust contingency plans for adverse scenarios. The firm's strong balance "
         "sheet, diversified revenue streams, and talented workforce position it well to navigate "
         "uncertainty and capitalize on opportunities in the evolving financial services landscape."),
    ]

    y = 80
    for para in conclusion_paragraphs:
        rect = pymupdf.Rect(72, y, 523, y + 85)
        page6.insert_textbox(rect, para, fontsize=10, fontname="helv",
                             color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 90

    # Signature block
    y += 20
    page6.insert_text(pymupdf.Point(72, y), "Prepared by:", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.4))
    page6.insert_text(pymupdf.Point(72, y + 18), "Jonathan R. Whitfield, CFA", fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))
    page6.insert_text(pymupdf.Point(72, y + 33), "Chief Financial Officer", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    page6.insert_text(pymupdf.Point(72, y + 48), "March 15, 2026", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    page6.insert_text(pymupdf.Point(72, H - 40), "Meridian Financial Group  |  Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page6.insert_text(pymupdf.Point(500, H - 40), "Page 6", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Save
    doc.save(PDF_PATH)
    doc.close()
    print(f'Initial file created: {PDF_PATH}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
