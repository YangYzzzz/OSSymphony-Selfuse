"""
Initial Setup: Create a 5-page income statement PDF with no annotations
Task ID: pdf_fin_017
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_017'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/income_statement_2023.pdf'


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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page dimensions ----
    W, H = 612, 792  # US Letter

    # ================================================================
    # PAGE 1: Cover Page
    # ================================================================
    page1 = doc.new_page(width=W, height=H)

    # Company logo area - blue header bar
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, W, 100))
    shape.finish(fill=(0.12, 0.24, 0.45))  # dark navy blue
    shape.commit()

    page1.insert_text(pymupdf.Point(72, 65), "MERIDIAN GLOBAL HOLDINGS, INC.",
                      fontsize=20, fontname="hebo", color=(1, 1, 1))

    page1.insert_text(pymupdf.Point(72, 200), "CONSOLIDATED INCOME STATEMENT",
                      fontsize=24, fontname="hebo", color=(0.12, 0.24, 0.45))

    page1.insert_text(pymupdf.Point(72, 240), "For the Fiscal Year Ended December 31, 2023",
                      fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))

    page1.insert_text(pymupdf.Point(72, 290), "Prepared in accordance with U.S. GAAP",
                      fontsize=11, fontname="tiit", color=(0.4, 0.4, 0.4))

    page1.insert_text(pymupdf.Point(72, 330), "Audited by Thornton & Associates LLP",
                      fontsize=11, fontname="tiit", color=(0.4, 0.4, 0.4))

    # Footer
    page1.insert_text(pymupdf.Point(72, 720), "Confidential — For Internal Use Only",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    page1.insert_text(pymupdf.Point(72, 740), "Filed: March 15, 2024",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ================================================================
    # PAGE 2: Revenue & Cost of Goods Sold
    # ================================================================
    page2 = doc.new_page(width=W, height=H)

    # Header
    page2.insert_text(pymupdf.Point(72, 50), "Meridian Global Holdings, Inc.",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page2.insert_text(pymupdf.Point(72, 68), "Consolidated Income Statement — Revenue & COGS",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Draw header line
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape2.finish(color=(0.12, 0.24, 0.45), width=1.5)
    shape2.commit()

    # Column headers
    y = 110
    page2.insert_text(pymupdf.Point(72, y), "Description",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(350, y), "FY 2023",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(460, y), "FY 2022",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))

    # Revenue section
    revenue_data = [
        ("REVENUE", "", "", True),
        ("  Product Sales — North America", "$284,750,000", "$261,430,000", False),
        ("  Product Sales — Europe", "$198,320,000", "$185,610,000", False),
        ("  Product Sales — Asia Pacific", "$142,880,000", "$128,970,000", False),
        ("  Service Revenue", "$87,650,000", "$79,420,000", False),
        ("  Licensing & Royalties", "$34,210,000", "$31,580,000", False),
        ("  Other Revenue", "$12,190,000", "$10,840,000", False),
        ("", "", "", False),
        ("Total Revenue", "$760,000,000", "$697,850,000", True),
    ]

    y = 140
    for desc, fy23, fy22, bold in revenue_data:
        font = "hebo" if bold else "helv"
        page2.insert_text(pymupdf.Point(72, y), desc, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy23:
            page2.insert_text(pymupdf.Point(350, y), fy23, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy22:
            page2.insert_text(pymupdf.Point(460, y), fy22, fontsize=10, fontname=font, color=(0, 0, 0))
        y += 20

    # The "Total Revenue" line is at y=140 + 8*20 = 300 area
    # This matches the rect (100,300,500,320) specified in the task

    # Draw line under Total Revenue
    shape2b = page2.new_shape()
    shape2b.draw_line(pymupdf.Point(72, y - 8), pymupdf.Point(540, y - 8))
    shape2b.finish(color=(0, 0, 0), width=0.8)
    shape2b.commit()

    # COGS section
    y += 10
    cogs_data = [
        ("COST OF GOODS SOLD", "", "", True),
        ("  Raw Materials", "$198,450,000", "$186,230,000", False),
        ("  Direct Labor", "$112,680,000", "$104,520,000", False),
        ("  Manufacturing Overhead", "$67,340,000", "$62,180,000", False),
        ("  Freight & Distribution", "$28,910,000", "$26,740,000", False),
        ("  Warranty & Returns", "$8,620,000", "$7,980,000", False),
        ("", "", "", False),
        ("Total COGS", "$416,000,000", "$387,650,000", True),
    ]

    for desc, fy23, fy22, bold in cogs_data:
        font = "hebo" if bold else "helv"
        page2.insert_text(pymupdf.Point(72, y), desc, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy23:
            page2.insert_text(pymupdf.Point(350, y), fy23, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy22:
            page2.insert_text(pymupdf.Point(460, y), fy22, fontsize=10, fontname=font, color=(0, 0, 0))
        y += 20

    # Gross Profit
    y += 10
    shape2c = page2.new_shape()
    shape2c.draw_line(pymupdf.Point(72, y - 8), pymupdf.Point(540, y - 8))
    shape2c.finish(color=(0, 0, 0), width=1.2)
    shape2c.commit()

    page2.insert_text(pymupdf.Point(72, y + 5), "GROSS PROFIT",
                      fontsize=11, fontname="hebo", color=(0.12, 0.24, 0.45))
    page2.insert_text(pymupdf.Point(350, y + 5), "$344,000,000",
                      fontsize=11, fontname="hebo", color=(0.12, 0.24, 0.45))
    page2.insert_text(pymupdf.Point(460, y + 5), "$310,200,000",
                      fontsize=11, fontname="hebo", color=(0.12, 0.24, 0.45))

    # Page number
    page2.insert_text(pymupdf.Point(290, 770), "— 2 —",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ================================================================
    # PAGE 3: Operating Expenses & EBITDA
    # ================================================================
    page3 = doc.new_page(width=W, height=H)

    # Header
    page3.insert_text(pymupdf.Point(72, 50), "Meridian Global Holdings, Inc.",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page3.insert_text(pymupdf.Point(72, 68), "Consolidated Income Statement — Operating Expenses & EBITDA",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape3.finish(color=(0.12, 0.24, 0.45), width=1.5)
    shape3.commit()

    # Column headers
    y = 110
    page3.insert_text(pymupdf.Point(72, y), "Description",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(350, y), "FY 2023",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(460, y), "FY 2022",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))

    y = 140
    opex_data = [
        ("OPERATING EXPENSES", "", "", True),
        ("  Selling, General & Administrative", "$89,400,000", "$82,150,000", False),
        ("  Research & Development", "$52,300,000", "$47,600,000", False),
        ("  Marketing & Advertising", "$38,700,000", "$35,280,000", False),
        ("  Employee Benefits & Compensation", "$31,250,000", "$28,940,000", False),
        ("  Rent & Facilities", "$18,600,000", "$17,420,000", False),
        ("  Professional & Legal Fees", "$12,450,000", "$11,380,000", False),
        ("  Technology & Infrastructure", "$9,800,000", "$8,730,000", False),
        ("  Insurance", "$5,200,000", "$4,850,000", False),
        ("  Travel & Entertainment", "$4,300,000", "$3,960,000", False),
        ("  Other Operating Expenses", "$6,000,000", "$5,490,000", False),
        ("", "", "", False),
        ("Total Operating Expenses", "$268,000,000", "$245,800,000", True),
    ]

    for desc, fy23, fy22, bold in opex_data:
        font = "hebo" if bold else "helv"
        page3.insert_text(pymupdf.Point(72, y), desc, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy23:
            page3.insert_text(pymupdf.Point(350, y), fy23, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy22:
            page3.insert_text(pymupdf.Point(460, y), fy22, fontsize=10, fontname=font, color=(0, 0, 0))
        y += 20

    # Operating Income
    y += 5
    shape3b = page3.new_shape()
    shape3b.draw_line(pymupdf.Point(72, y - 5), pymupdf.Point(540, y - 5))
    shape3b.finish(color=(0, 0, 0), width=0.8)
    shape3b.commit()

    page3.insert_text(pymupdf.Point(72, y + 5), "OPERATING INCOME (EBIT)",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(350, y + 5), "$76,000,000",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(460, y + 5), "$64,400,000",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))

    y += 30
    # D&A section
    page3.insert_text(pymupdf.Point(72, y), "Add: Depreciation & Amortization",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(350, y), "$22,500,000",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(460, y), "$20,800,000",
                      fontsize=10, fontname="helv", color=(0, 0, 0))

    # EBITDA line - should be around y=450 area to match rect (200,450,400,470)
    y += 30
    shape3c = page3.new_shape()
    shape3c.draw_line(pymupdf.Point(72, y - 5), pymupdf.Point(540, y - 5))
    shape3c.finish(color=(0.12, 0.24, 0.45), width=1.2)
    shape3c.commit()

    # Place EBITDA at y ~ 458 to be within (200,450,400,470)
    page3.insert_text(pymupdf.Point(72, 458), "EBITDA",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page3.insert_text(pymupdf.Point(350, 458), "$98,500,000",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page3.insert_text(pymupdf.Point(460, 458), "$85,200,000",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))

    # EBITDA Margin
    page3.insert_text(pymupdf.Point(72, 490), "EBITDA Margin",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page3.insert_text(pymupdf.Point(350, 490), "12.96%",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page3.insert_text(pymupdf.Point(460, 490), "12.21%",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Page number
    page3.insert_text(pymupdf.Point(290, 770), "— 3 —",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ================================================================
    # PAGE 4: Net Income
    # ================================================================
    page4 = doc.new_page(width=W, height=H)

    page4.insert_text(pymupdf.Point(72, 50), "Meridian Global Holdings, Inc.",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page4.insert_text(pymupdf.Point(72, 68), "Consolidated Income Statement — Net Income",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape4.finish(color=(0.12, 0.24, 0.45), width=1.5)
    shape4.commit()

    y = 110
    page4.insert_text(pymupdf.Point(72, y), "Description",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(350, y), "FY 2023",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(460, y), "FY 2022",
                      fontsize=10, fontname="hebo", color=(0, 0, 0))

    y = 140
    net_data = [
        ("Operating Income (EBIT)", "$76,000,000", "$64,400,000", True),
        ("", "", "", False),
        ("OTHER INCOME / (EXPENSES)", "", "", True),
        ("  Interest Income", "$3,200,000", "$2,850,000", False),
        ("  Interest Expense", "($8,400,000)", "($9,100,000)", False),
        ("  Foreign Exchange Gain / (Loss)", "($1,800,000)", "$950,000", False),
        ("  Gain on Sale of Assets", "$2,150,000", "$680,000", False),
        ("  Investment Income", "$4,600,000", "$3,720,000", False),
        ("", "", "", False),
        ("Total Other Income / (Expenses)", "($250,000)", "($900,000)", True),
        ("", "", "", False),
        ("INCOME BEFORE TAX", "$75,750,000", "$63,500,000", True),
        ("", "", "", False),
        ("  Income Tax Expense (Effective Rate: 23.1%)", "($17,498,000)", "($14,605,000)", False),
        ("", "", "", False),
        ("NET INCOME", "$58,252,000", "$48,895,000", True),
    ]

    for desc, fy23, fy22, bold in net_data:
        font = "hebo" if bold else "helv"
        page4.insert_text(pymupdf.Point(72, y), desc, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy23:
            page4.insert_text(pymupdf.Point(350, y), fy23, fontsize=10, fontname=font, color=(0, 0, 0))
        if fy22:
            page4.insert_text(pymupdf.Point(460, y), fy22, fontsize=10, fontname=font, color=(0, 0, 0))
        y += 20

    # Double line under Net Income
    shape4b = page4.new_shape()
    shape4b.draw_line(pymupdf.Point(72, y - 8), pymupdf.Point(540, y - 8))
    shape4b.finish(color=(0, 0, 0), width=1.5)
    shape4b.draw_line(pymupdf.Point(72, y - 4), pymupdf.Point(540, y - 4))
    shape4b.finish(color=(0, 0, 0), width=1.5)
    shape4b.commit()

    # EPS section
    y += 20
    page4.insert_text(pymupdf.Point(72, y), "Earnings Per Share (Basic)",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(350, y), "$4.85",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(460, y), "$4.07",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page4.insert_text(pymupdf.Point(72, y), "Earnings Per Share (Diluted)",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(350, y), "$4.72",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(460, y), "$3.95",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page4.insert_text(pymupdf.Point(72, y), "Weighted Avg. Shares Outstanding (M)",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(350, y), "12.01",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(460, y), "12.01",
                      fontsize=10, fontname="helv", color=(0, 0, 0))

    # Page number
    page4.insert_text(pymupdf.Point(290, 770), "— 4 —",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ================================================================
    # PAGE 5: Notes & Assumptions
    # ================================================================
    page5 = doc.new_page(width=W, height=H)

    page5.insert_text(pymupdf.Point(72, 50), "Meridian Global Holdings, Inc.",
                      fontsize=12, fontname="hebo", color=(0.12, 0.24, 0.45))
    page5.insert_text(pymupdf.Point(72, 68), "Notes to the Income Statement",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape5 = page5.new_shape()
    shape5.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape5.finish(color=(0.12, 0.24, 0.45), width=1.5)
    shape5.commit()

    notes = [
        ("1. Revenue Recognition",
         "Revenue is recognized in accordance with ASC 606, Revenue from Contracts with Customers. "
         "Product revenue is recognized at the point of transfer of control to the customer. "
         "Service revenue is recognized over time as services are delivered."),
        ("2. Cost Allocation",
         "Manufacturing overhead is allocated based on direct labor hours. Corporate overhead is "
         "allocated to segments based on revenue contribution percentages."),
        ("3. Foreign Currency",
         "Foreign currency transactions are translated at the exchange rate prevailing at the date "
         "of the transaction. Monetary assets and liabilities denominated in foreign currencies are "
         "re-measured at period-end exchange rates."),
        ("4. Income Taxes",
         "The effective tax rate of 23.1% reflects the blended impact of federal (21%), state (3.8%), "
         "and international tax obligations, net of R&D tax credits of approximately $2.4 million."),
        ("5. Significant Estimates",
         "Management has made significant estimates related to warranty reserves ($8.6M), "
         "allowance for doubtful accounts ($3.2M), and inventory obsolescence ($5.1M). "
         "Actual results may differ from these estimates."),
    ]

    y = 110
    for title, body in notes:
        page5.insert_text(pymupdf.Point(72, y), title,
                          fontsize=10, fontname="hebo", color=(0, 0, 0))
        y += 18
        # Wrap body text in textbox
        rect = pymupdf.Rect(72, y, 540, y + 60)
        page5.insert_textbox(rect, body, fontsize=9, fontname="helv",
                             color=(0.2, 0.2, 0.2), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 70

    # Page number
    page5.insert_text(pymupdf.Point(290, 770), "— 5 —",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
