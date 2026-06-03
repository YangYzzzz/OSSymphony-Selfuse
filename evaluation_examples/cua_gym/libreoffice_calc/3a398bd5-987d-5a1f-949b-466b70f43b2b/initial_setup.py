"""
Initial Setup: Create a 15-page PDF financial report with empty metadata
Task ID: pdf_ro_025
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_025'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/report.pdf'


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

    # Page dimensions (A4)
    W, H = 595, 842

    # ---- Page 1: Cover Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(150, 200), "Q4 Financial Report", fontsize=28, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_text(pymupdf.Point(180, 260), "Fiscal Year 2025", fontsize=18, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(150, 340), "Prepared by: Finance Department", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(150, 365), "Date: December 31, 2025", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(150, 390), "Classification: Internal Use Only", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 300), pymupdf.Point(523, 300))
    shape.finish(color=(0.1, 0.15, 0.35), width=2)
    shape.commit()

    # ---- Page 2: Table of Contents ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Revenue Analysis", "4"),
        ("3. Expense Breakdown", "5"),
        ("4. Profit & Loss Statement", "6"),
        ("5. Balance Sheet Overview", "7"),
        ("6. Cash Flow Analysis", "8"),
        ("7. Regional Performance", "9"),
        ("8. Product Line Performance", "10"),
        ("9. Key Performance Indicators", "11"),
        ("10. Risk Assessment", "12"),
        ("11. Forecast & Projections", "13"),
        ("12. Capital Expenditures", "14"),
        ("13. Appendix", "15"),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(90, y), title, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), pg, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 3: Executive Summary ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    summary_text = (
        "The fourth quarter of fiscal year 2025 demonstrated strong financial performance across all business "
        "segments. Total revenue reached $48.7 million, representing a 12.3% increase compared to Q4 2024. "
        "Operating expenses were managed effectively at $31.2 million, resulting in an operating margin of 35.9%. "
        "Net income for the quarter was $13.1 million, exceeding analyst expectations by $1.4 million. "
        "Key growth drivers included our cloud services division, which saw 28% year-over-year growth, and the "
        "enterprise solutions segment, which secured 14 new contracts valued at over $500K each. The APAC region "
        "continued its strong trajectory with 18% revenue growth, while EMEA stabilized after restructuring. "
        "Looking ahead, we maintain our full-year guidance and expect continued momentum into Q1 2026."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 4: Revenue Analysis ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Revenue Analysis", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_text(pymupdf.Point(72, 110), "Quarterly Revenue Breakdown (in $ millions)", fontsize=12, fontname="hebo", color=(0, 0, 0))
    rev_data = [
        ["Segment", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"],
        ["Cloud Services", "8.2", "9.1", "10.4", "12.8"],
        ["Enterprise Solutions", "6.5", "6.8", "7.2", "8.4"],
        ["Consumer Products", "4.1", "4.3", "4.5", "5.2"],
        ["Professional Services", "3.8", "4.0", "4.2", "4.6"],
        ["Licensing & Royalties", "2.9", "3.1", "3.3", "3.5"],
        ["Support & Maintenance", "10.2", "10.8", "11.5", "14.2"],
    ]
    y = 140
    for i, row in enumerate(rev_data):
        x = 72
        for j, cell in enumerate(row):
            fn = "hebo" if i == 0 else "helv"
            page.insert_text(pymupdf.Point(x, y), cell, fontsize=10, fontname=fn, color=(0, 0, 0))
            x += 95
        y += 18
    page.insert_text(pymupdf.Point(72, y + 20), "Total Q4 Revenue: $48.7M (+12.3% YoY)", fontsize=11, fontname="hebo", color=(0.1, 0.5, 0.1))

    # ---- Page 5: Expense Breakdown ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. Expense Breakdown", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    expenses = [
        ("Cost of Revenue", "$14.6M", "29.9%"),
        ("Research & Development", "$6.8M", "14.0%"),
        ("Sales & Marketing", "$5.2M", "10.7%"),
        ("General & Administrative", "$3.1M", "6.4%"),
        ("Depreciation & Amortization", "$1.5M", "3.1%"),
    ]
    y = 120
    page.insert_text(pymupdf.Point(72, y), "Category", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(280, y), "Amount", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(400, y), "% of Revenue", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    for cat, amt, pct in expenses:
        page.insert_text(pymupdf.Point(72, y), cat, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(280, y), amt, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(400, y), pct, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18
    page.insert_text(pymupdf.Point(72, y + 15), "Total Operating Expenses: $31.2M (64.1% of revenue)", fontsize=11, fontname="hebo", color=(0.6, 0.1, 0.1))

    # ---- Page 6: Profit & Loss Statement ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. Profit & Loss Statement", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    pnl_items = [
        ("Revenue", "$48,700,000"),
        ("Cost of Revenue", "($14,600,000)"),
        ("Gross Profit", "$34,100,000"),
        ("Operating Expenses", "($16,600,000)"),
        ("Operating Income", "$17,500,000"),
        ("Interest Expense", "($1,200,000)"),
        ("Other Income", "$340,000"),
        ("Income Before Tax", "$16,640,000"),
        ("Income Tax", "($3,540,000)"),
        ("Net Income", "$13,100,000"),
    ]
    y = 120
    for item, val in pnl_items:
        fn = "hebo" if item in ("Gross Profit", "Operating Income", "Net Income") else "helv"
        page.insert_text(pymupdf.Point(90, y), item, fontsize=11, fontname=fn, color=(0, 0, 0))
        page.insert_text(pymupdf.Point(380, y), val, fontsize=11, fontname=fn, color=(0, 0, 0))
        y += 22

    # ---- Page 7: Balance Sheet Overview ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. Balance Sheet Overview", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    bal_text = (
        "Total Assets as of December 31, 2025 stood at $215.4 million, an increase of $28.6 million from the "
        "prior quarter. Current assets totaled $89.2 million, including cash and equivalents of $42.1 million. "
        "Non-current assets of $126.2 million include property, plant and equipment ($68.4M), intangible assets "
        "($35.8M), and goodwill ($22.0M). Total liabilities were $98.7 million, with current liabilities of "
        "$45.3 million and long-term debt of $53.4 million. Shareholders equity reached $116.7 million."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 400), bal_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 8: Cash Flow Analysis ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6. Cash Flow Analysis", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    cf_items = [
        ("Operating Activities", "+$18,200,000"),
        ("Investing Activities", "-$7,400,000"),
        ("Financing Activities", "-$4,300,000"),
        ("Net Change in Cash", "+$6,500,000"),
        ("Beginning Cash Balance", "$35,600,000"),
        ("Ending Cash Balance", "$42,100,000"),
    ]
    y = 120
    for item, val in cf_items:
        page.insert_text(pymupdf.Point(90, y), item, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(380, y), val, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 9: Regional Performance ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. Regional Performance", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    regions = [
        ("North America", "$22.4M", "46.0%", "+9.8%"),
        ("Europe (EMEA)", "$12.1M", "24.8%", "+4.2%"),
        ("Asia Pacific", "$9.8M", "20.1%", "+18.3%"),
        ("Latin America", "$2.9M", "6.0%", "+11.5%"),
        ("Middle East & Africa", "$1.5M", "3.1%", "+7.2%"),
    ]
    y = 120
    headers = ["Region", "Revenue", "Share", "YoY Growth"]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(72 + i * 120, y), h, fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    for region, rev, share, growth in regions:
        page.insert_text(pymupdf.Point(72, y), region, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(192, y), rev, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(312, y), share, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(432, y), growth, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # ---- Page 10: Product Line Performance ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "8. Product Line Performance", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    products = [
        ("CloudSync Pro", "Enterprise cloud storage", "$8.4M", "+32%"),
        ("DataVault Enterprise", "Data management suite", "$6.2M", "+15%"),
        ("SecureGate", "Cybersecurity platform", "$5.8M", "+22%"),
        ("AnalyticsPro", "Business intelligence", "$4.1M", "+18%"),
        ("CollabSpace", "Team collaboration", "$3.7M", "+25%"),
        ("DevOps Toolkit", "CI/CD platform", "$3.2M", "+28%"),
    ]
    y = 120
    for name, desc, rev, growth in products:
        page.insert_text(pymupdf.Point(90, y), name, fontsize=11, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(90, y + 15), f"{desc} | Revenue: {rev} | Growth: {growth}", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 40

    # ---- Page 11: Key Performance Indicators ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "9. Key Performance Indicators", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    kpis = [
        ("Revenue Growth (YoY)", "12.3%", "10.0%", "Exceeded"),
        ("Gross Margin", "70.0%", "68.0%", "Exceeded"),
        ("Operating Margin", "35.9%", "33.0%", "Exceeded"),
        ("Net Profit Margin", "26.9%", "25.0%", "Exceeded"),
        ("Customer Retention", "94.2%", "92.0%", "Exceeded"),
        ("New Customer Acquisition", "847", "750", "Exceeded"),
        ("Employee Satisfaction", "4.3/5.0", "4.0/5.0", "Exceeded"),
        ("NPS Score", "72", "65", "Exceeded"),
    ]
    y = 120
    page.insert_text(pymupdf.Point(72, y), "KPI", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(250, y), "Actual", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(340, y), "Target", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(430, y), "Status", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    for kpi, actual, target, status in kpis:
        page.insert_text(pymupdf.Point(72, y), kpi, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(250, y), actual, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(340, y), target, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(430, y), status, fontsize=10, fontname="helv", color=(0, 0.5, 0))
        y += 18

    # ---- Page 12: Risk Assessment ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "10. Risk Assessment", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    risk_text = (
        "Market Risk: Global economic uncertainty and potential recession indicators in key markets pose moderate "
        "risk to revenue projections. Mitigation: Diversified geographic presence and recurring revenue base. "
        "\n\nCurrency Risk: Approximately 45% of revenue is denominated in non-USD currencies. A 5% adverse "
        "movement could impact revenue by approximately $1.1M per quarter. Mitigation: Natural hedging through "
        "local cost structures and selective forward contracts. "
        "\n\nTechnology Risk: Rapid evolution in AI and cloud computing requires sustained R&D investment. "
        "Failure to adapt could erode competitive positioning. Mitigation: Increased R&D budget allocation to 14% "
        "of revenue and strategic partnerships with leading technology providers. "
        "\n\nRegulatory Risk: Evolving data privacy regulations (GDPR, CCPA, new APAC regulations) require "
        "ongoing compliance investment. Mitigation: Dedicated compliance team and proactive regulatory engagement."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 600), risk_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 13: Forecast & Projections ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "11. Forecast & Projections", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    forecasts = [
        ("Q1 2026", "$50.2M", "$32.8M", "$13.4M"),
        ("Q2 2026", "$52.5M", "$34.1M", "$14.1M"),
        ("Q3 2026", "$55.0M", "$35.5M", "$15.0M"),
        ("Q4 2026", "$58.3M", "$37.2M", "$16.2M"),
        ("FY 2026 Total", "$216.0M", "$139.6M", "$58.7M"),
    ]
    y = 120
    page.insert_text(pymupdf.Point(72, y), "Period", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, y), "Revenue", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(310, y), "Expenses", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(420, y), "Net Income", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    for period, rev, exp, ni in forecasts:
        fn = "hebo" if "Total" in period else "helv"
        page.insert_text(pymupdf.Point(72, y), period, fontsize=10, fontname=fn, color=(0, 0, 0))
        page.insert_text(pymupdf.Point(200, y), rev, fontsize=10, fontname=fn, color=(0, 0, 0))
        page.insert_text(pymupdf.Point(310, y), exp, fontsize=10, fontname=fn, color=(0, 0, 0))
        page.insert_text(pymupdf.Point(420, y), ni, fontsize=10, fontname=fn, color=(0, 0, 0))
        y += 18

    # ---- Page 14: Capital Expenditures ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "12. Capital Expenditures", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    capex_items = [
        ("Data Center Expansion (Virginia)", "$3.2M", "Q1-Q2 2026"),
        ("Cloud Infrastructure Upgrade", "$2.8M", "Q2 2026"),
        ("Office Renovation (Singapore HQ)", "$1.5M", "Q3 2026"),
        ("Security Systems Upgrade", "$0.9M", "Q1 2026"),
        ("New Development Lab (Austin)", "$2.1M", "Q2-Q3 2026"),
        ("ERP System Migration", "$1.8M", "FY 2026"),
    ]
    y = 120
    page.insert_text(pymupdf.Point(72, y), "Project", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(310, y), "Budget", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(410, y), "Timeline", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    for proj, budget, timeline in capex_items:
        page.insert_text(pymupdf.Point(72, y), proj, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(310, y), budget, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(410, y), timeline, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18
    page.insert_text(pymupdf.Point(72, y + 20), "Total Planned CapEx: $12.3M", fontsize=11, fontname="hebo", color=(0.1, 0.15, 0.35))

    # ---- Page 15: Appendix ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "13. Appendix", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    appendix_text = (
        "Appendix A: Detailed Revenue by Product\n"
        "Appendix B: Employee Headcount by Department\n"
        "Appendix C: Customer Satisfaction Survey Results\n"
        "Appendix D: Competitive Landscape Analysis\n"
        "Appendix E: Regulatory Compliance Status\n"
        "\n"
        "Note: Detailed supporting documentation for each appendix item is available upon request from the "
        "Finance Department. Contact: finance@company.com\n"
        "\n"
        "Disclaimer: This report contains forward-looking statements that involve risks and uncertainties. "
        "Actual results may differ materially from those projected. Past performance is not indicative of "
        "future results. This document is intended for internal use only and should not be distributed to "
        "external parties without prior authorization from the Chief Financial Officer."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 600), appendix_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Ensure metadata is empty/minimal
    doc.set_metadata({
        "title": "",
        "author": "",
        "subject": "",
        "keywords": "",
        "creator": "",
        "producer": "",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 15')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
