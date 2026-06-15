"""
Initial Setup: Add annotations to a financial draft report PDF
Task ID: pdf_gf2_006
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_006'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/draft_report.pdf'


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

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    margin = 72
    content_width = W - 2 * margin

    # --- Page 1: Title page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 200), "FINANCIAL PROJECTIONS REPORT",
                     fontsize=24, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_text(pymupdf.Point(margin, 240), "Fiscal Year 2025-2026",
                     fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 280), "Prepared by: Strategic Finance Division",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 310), "Date: March 15, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 340), "Classification: Internal - Confidential",
                     fontsize=11, fontname="tiit", color=(0.6, 0.1, 0.1))

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "1. Executive Summary",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    summary_text = (
        "This report presents the financial projections for Meridian Technologies Inc. "
        "for fiscal years 2025-2026. Based on current market conditions and our strategic "
        "initiatives, we project a compound annual growth rate (CAGR) of 14.2% in total "
        "revenue, driven primarily by expansion in the cloud services and enterprise "
        "analytics segments.\n\n"
        "Key findings include a projected increase in gross margin from 62.3% to 67.8%, "
        "reflecting improved operational efficiency and favorable product mix shifts. "
        "Operating expenses are expected to grow at 8.5%, below revenue growth, indicating "
        "strengthening operating leverage.\n\n"
        "Capital expenditure requirements for the projection period total $42.7 million, "
        "primarily allocated to data center expansion ($28.3M) and R&D infrastructure ($14.4M). "
        "The projected free cash flow yield improves from 5.8% to 7.4% by FY2026."
    )
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 500),
                        summary_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 3: Revenue Projections (where sticky note will go) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "2. Revenue Projections",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_text(pymupdf.Point(margin, 105), "Revenue Breakdown by Segment (in $M)",
                     fontsize=12, fontname="tibo", color=(0.2, 0.2, 0.2))

    # Table header
    y = 135
    headers = ["Segment", "FY2024 Actual", "FY2025 Proj.", "FY2026 Proj.", "CAGR"]
    col_x = [margin, margin + 140, margin + 260, margin + 380, margin + 490]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    # Draw header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(margin, y + 5), pymupdf.Point(W - margin, y + 5))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    # Table rows
    rows = [
        ["Cloud Services", "$127.4", "$152.8", "$178.6", "18.4%"],
        ["Enterprise Analytics", "$84.2", "$95.6", "$110.2", "14.4%"],
        ["Consulting Services", "$56.8", "$61.3", "$65.9", "7.7%"],
        ["License Revenue", "$38.1", "$35.7", "$33.2", "-6.7%"],
        ["Support & Maintenance", "$45.6", "$49.8", "$54.3", "9.1%"],
        ["Total Revenue", "$352.1", "$395.2", "$442.2", "12.1%"],
    ]
    for r_idx, row in enumerate(rows):
        ry = y + 20 + r_idx * 18
        fn = "hebo" if r_idx == len(rows) - 1 else "helv"
        for c_idx, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[c_idx], ry), val, fontsize=10, fontname=fn, color=(0, 0, 0))

    page.insert_textbox(pymupdf.Rect(margin, 300, W - margin, 500),
        "Cloud Services continues to be the primary growth driver, with projected revenue "
        "reaching $178.6M by FY2026. The migration of legacy license customers to cloud "
        "subscriptions accounts for approximately 40% of this growth. Enterprise Analytics "
        "benefits from the launch of the DataLens Pro platform in Q3 2024, with enterprise "
        "adoption rates exceeding initial projections by 23%.\n\n"
        "License Revenue decline reflects the strategic shift toward recurring revenue models. "
        "Management expects this segment to stabilize at approximately $30M by FY2027 as the "
        "remaining on-premises customers are transitioned.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    # --- Page 4: Cost Analysis ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "3. Cost Structure & Margins",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 550),
        "Cost of goods sold is projected to decrease as a percentage of revenue from 37.7% "
        "to 32.2%, driven by economies of scale in cloud infrastructure and improved vendor "
        "negotiations. Key cost optimization initiatives include:\n\n"
        "1. Data Center Consolidation: Migrating from 12 regional centers to 5 hyper-scale "
        "facilities, reducing operational overhead by an estimated $8.2M annually.\n\n"
        "2. Automation of Tier-1 Support: Implementation of AI-driven support tools is expected "
        "to reduce support staffing costs by 22% while maintaining or improving customer "
        "satisfaction scores.\n\n"
        "3. Procurement Optimization: Renegotiated contracts with three major hardware vendors "
        "yield projected savings of $4.7M in FY2025 and $6.1M in FY2026.\n\n"
        "Research and development spending will increase from $52.4M (14.9% of revenue) to "
        "$59.8M (13.5% of revenue), reflecting continued investment in platform capabilities "
        "while achieving leverage through revenue scale.\n\n"
        "Sales and marketing expenses are projected at 18.2% of revenue in FY2025, declining "
        "to 16.8% in FY2026 as brand awareness improvements and channel partnerships reduce "
        "customer acquisition costs.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    # --- Page 5: Cash Flow (where freetext annotation will go) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "4. Cash Flow Projections",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 550),
        "Operating cash flow is projected to increase from $68.4M in FY2024 to $94.2M in "
        "FY2026, reflecting improved profitability and working capital management.\n\n"
        "Capital expenditure requirements:\n"
        "  - Data center expansion (new Phoenix facility): $28.3M over 24 months\n"
        "  - R&D lab equipment and infrastructure: $14.4M\n"
        "  - Office build-out (Austin campus Phase 2): $7.8M\n"
        "  - IT systems upgrades: $4.2M\n\n"
        "Free cash flow projections:\n"
        "  FY2024 Actual: $21.7M (6.2% of revenue)\n"
        "  FY2025 Projected: $28.9M (7.3% of revenue)\n"
        "  FY2026 Projected: $39.4M (8.9% of revenue)\n\n"
        "Dividend policy: The board has approved maintaining the current quarterly dividend "
        "of $0.18/share through FY2025, with a planned increase to $0.22/share in FY2026 "
        "pending achievement of operating margin targets.\n\n"
        "Share repurchase: $15M authorized for FY2025 under the existing buyback program. "
        "Management will evaluate an additional $20M authorization for FY2026 based on "
        "stock price levels and cash flow performance.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    # --- Page 6: Balance Sheet ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "5. Balance Sheet Projections",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 500),
        "Total assets are projected to grow from $487.2M to $562.8M, with the increase "
        "primarily in long-term assets related to data center investments and capitalized "
        "software development costs.\n\n"
        "Key balance sheet metrics:\n"
        "  Current ratio: 2.1x (FY2024) → 2.3x (FY2026)\n"
        "  Debt-to-equity: 0.42 (FY2024) → 0.38 (FY2026)\n"
        "  Book value per share: $24.67 → $29.15\n\n"
        "Long-term debt of $85M (5-year term loan at SOFR + 175bps) matures in Q2 FY2027. "
        "Management plans to refinance at favorable rates given improved credit metrics. "
        "Moody's upgraded the company outlook from stable to positive in January 2025.\n\n"
        "Goodwill and intangible assets of $124.6M relate primarily to the DataLens "
        "acquisition (2022) and are subject to annual impairment testing. No impairment "
        "indicators have been identified as of the report date.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    # --- Page 7: Risk Factors ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "6. Risk Factors & Sensitivities",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 600),
        "The following key risks could materially impact projected financial outcomes:\n\n"
        "Market Risk: A 10% decline in enterprise IT spending would reduce projected "
        "FY2026 revenue by approximately $35M and operating income by $18M.\n\n"
        "Competition Risk: Aggressive pricing by major cloud providers (AWS, Azure, GCP) "
        "could compress cloud services margins by 200-400 basis points. Mitigation: "
        "differentiated AI/ML capabilities and vertical-specific solutions.\n\n"
        "Regulatory Risk: Evolving data privacy regulations (EU AI Act, state-level privacy "
        "laws) may require additional compliance investments estimated at $3-5M annually.\n\n"
        "Talent Risk: Engineering talent retention remains challenging with a current "
        "attrition rate of 14.2%. Compensation adjustments of approximately $6M are "
        "factored into FY2025 projections.\n\n"
        "Foreign Exchange Risk: Approximately 28% of revenue is denominated in non-USD "
        "currencies. A 5% strengthening of the dollar would reduce reported revenue "
        "by approximately $5.5M.\n\n"
        "Technology Risk: Platform migration timeline extensions could delay anticipated "
        "cost savings by 2-3 quarters, impacting FY2026 margin targets.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    # --- Page 8: Appendix ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Appendix: Methodology & Assumptions",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.3))
    page.insert_textbox(pymupdf.Rect(margin, 100, W - margin, 600),
        "Projection Methodology:\n"
        "Revenue projections are built bottom-up from individual product line forecasts, "
        "validated against top-down market sizing analysis. Growth rates incorporate "
        "historical trends, pipeline analysis, and management estimates.\n\n"
        "Key Assumptions:\n"
        "  - GDP growth: 2.3% (2025), 2.1% (2026)\n"
        "  - Enterprise IT spending growth: 6.5% (2025), 7.2% (2026)\n"
        "  - Cloud market CAGR: 18% through 2027\n"
        "  - Customer churn rate: <5% annually\n"
        "  - Average revenue per enterprise customer growth: 8% annually\n"
        "  - New customer acquisition: 85-95 enterprise clients per year\n\n"
        "Data Sources:\n"
        "  - Internal financial systems (SAP S/4HANA)\n"
        "  - Gartner IT spending forecasts (January 2025)\n"
        "  - IDC Cloud Infrastructure Tracker\n"
        "  - Bureau of Economic Analysis GDP estimates\n"
        "  - Company CRM pipeline data (Salesforce)\n\n"
        "Disclaimer: These projections are forward-looking statements based on current "
        "information and assumptions. Actual results may differ materially from projections "
        "due to the factors described in the Risk Factors section.",
        fontsize=10, fontname="helv", color=(0, 0, 0))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 8')

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
