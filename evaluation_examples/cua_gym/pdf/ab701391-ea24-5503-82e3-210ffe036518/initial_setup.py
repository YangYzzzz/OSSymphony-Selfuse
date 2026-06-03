"""
Initial Setup: Create unencrypted 5-page tax return PDF
Task ID: pdf_gf3_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_010'
PRIVATE_DIR = f'{WORKDIR}/private'
OUTPUT = f'{PRIVATE_DIR}/tax_return.pdf'


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
    os.makedirs(PRIVATE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # === Page 1: Cover Page ===
    page = doc.new_page(width=612, height=792)  # Letter size
    # Title
    page.insert_text(pymupdf.Point(72, 80), "UNITED STATES", fontsize=14, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 100), "INDIVIDUAL INCOME TAX RETURN", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 120), "Form 1040 — Tax Year 2023", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))

    # Separator line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 135), pymupdf.Point(540, 135))
    shape.finish(color=(0, 0, 0.5), width=1.5)
    shape.commit()

    # Taxpayer info
    y = 170
    fields = [
        ("Taxpayer Name:", "Margaret R. Whitfield"),
        ("Social Security Number:", "***-**-4829"),
        ("Spouse Name:", "Thomas J. Whitfield"),
        ("Spouse SSN:", "***-**-7163"),
        ("Filing Status:", "Married Filing Jointly"),
        ("Address:", "1247 Oakwood Drive, Apt 3B"),
        ("City, State, ZIP:", "Portland, OR 97205"),
        ("Occupation (Taxpayer):", "Senior Software Architect"),
        ("Occupation (Spouse):", "Clinical Psychologist"),
        ("Tax Preparer:", "Henderson & Associates, CPA"),
        ("Preparer TIN:", "P01234567"),
        ("Date Prepared:", "March 28, 2024"),
    ]
    for label, value in fields:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(250, y), value, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(72, y + 30), "CONFIDENTIAL — FOR AUTHORIZED USE ONLY",
                     fontsize=9, fontname="heit", color=(0.6, 0, 0))

    # === Page 2: Income Summary ===
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 60), "Schedule 1 — Income Summary", fontsize=14, fontname="hebo", color=(0, 0, 0.5))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape2.finish(color=(0, 0, 0.5), width=1)
    shape2.commit()

    income_items = [
        ("1a.", "Wages, salaries, tips (W-2)", "$142,800.00"),
        ("1b.", "Spouse wages, salaries, tips (W-2)", "$118,500.00"),
        ("2a.", "Tax-exempt interest", "$1,245.00"),
        ("2b.", "Taxable interest", "$3,872.50"),
        ("3a.", "Qualified dividends", "$6,420.00"),
        ("3b.", "Ordinary dividends", "$8,915.30"),
        ("4a.", "IRA distributions", "$0.00"),
        ("4b.", "Taxable IRA distributions", "$0.00"),
        ("5a.", "Pensions and annuities", "$0.00"),
        ("5b.", "Taxable pensions", "$0.00"),
        ("6.", "Social Security benefits", "$0.00"),
        ("7.", "Capital gain or (loss) — Schedule D", "$12,340.75"),
        ("8.", "Other income (Schedule 1, line 10)", "$4,500.00"),
        ("9.", "Total income (add lines 1 through 8)", "$298,593.55"),
        ("10.", "Adjustments to income", "$18,750.00"),
        ("11.", "Adjusted gross income", "$279,843.55"),
    ]

    y = 100
    for line_num, desc, amount in income_items:
        page2.insert_text(pymupdf.Point(72, y), line_num, fontsize=9, fontname="hebo", color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(100, y), desc, fontsize=9, fontname="helv", color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(480, y), amount, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 20

    # === Page 3: Deductions ===
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 60), "Schedule A — Itemized Deductions", fontsize=14, fontname="hebo", color=(0, 0, 0.5))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape3.finish(color=(0, 0, 0.5), width=1)
    shape3.commit()

    deductions = [
        ("Medical and Dental Expenses", ""),
        ("  1. Medical/dental expenses", "$14,230.00"),
        ("  2. AGI threshold (7.5%)", "$20,988.27"),
        ("  3. Allowable medical deduction", "$0.00"),
        ("", ""),
        ("Taxes You Paid", ""),
        ("  4. State and local income taxes", "$10,000.00"),
        ("  5. Real estate taxes", "$6,840.00"),
        ("  6. Personal property taxes", "$485.00"),
        ("  7. Total taxes (limited to $10,000)", "$10,000.00"),
        ("", ""),
        ("Interest You Paid", ""),
        ("  8. Home mortgage interest", "$18,432.60"),
        ("  9. Investment interest", "$1,200.00"),
        ("", ""),
        ("Gifts to Charity", ""),
        ("  10. Cash contributions", "$8,500.00"),
        ("  11. Noncash contributions", "$2,750.00"),
        ("", ""),
        ("Other Deductions", ""),
        ("  12. Casualty/theft losses", "$0.00"),
        ("  13. Other itemized deductions", "$3,420.00"),
        ("", ""),
        ("  14. Total Itemized Deductions", "$44,302.60"),
    ]

    y = 100
    for desc, amount in deductions:
        if desc and not desc.startswith(" "):
            page3.insert_text(pymupdf.Point(72, y), desc, fontsize=10, fontname="hebo", color=(0, 0, 0))
        elif desc:
            page3.insert_text(pymupdf.Point(72, y), desc, fontsize=9, fontname="helv", color=(0, 0, 0))
        if amount:
            page3.insert_text(pymupdf.Point(480, y), amount, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 18

    # === Page 4: Tax Calculation ===
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 60), "Tax Computation Worksheet", fontsize=14, fontname="hebo", color=(0, 0, 0.5))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape4.finish(color=(0, 0, 0.5), width=1)
    shape4.commit()

    tax_calc = [
        ("15.", "Adjusted gross income", "$279,843.55"),
        ("16.", "Itemized deductions", "$44,302.60"),
        ("17.", "Qualified business income deduction", "$0.00"),
        ("18.", "Total deductions (line 16 + 17)", "$44,302.60"),
        ("19.", "Taxable income (line 15 - 18)", "$235,540.95"),
        ("", "", ""),
        ("20.", "Tax (from Tax Table / Schedule)", "$46,282.14"),
        ("21.", "Alternative minimum tax", "$0.00"),
        ("22.", "Excess advance PTC repayment", "$0.00"),
        ("23.", "Total tax before credits (20+21+22)", "$46,282.14"),
        ("", "", ""),
        ("24.", "Child tax credit", "$4,000.00"),
        ("25.", "Education credits", "$0.00"),
        ("26.", "Retirement savings credit", "$0.00"),
        ("27.", "Residential energy credit", "$1,800.00"),
        ("28.", "Other credits", "$0.00"),
        ("29.", "Total credits (24 through 28)", "$5,800.00"),
        ("", "", ""),
        ("30.", "Tax after credits (23 - 29)", "$40,482.14"),
        ("31.", "Self-employment tax", "$636.30"),
        ("32.", "Additional Medicare tax", "$1,038.44"),
        ("33.", "Net investment income tax", "$1,462.31"),
        ("34.", "Total tax", "$43,619.19"),
        ("", "", ""),
        ("35.", "Federal income tax withheld", "$48,250.00"),
        ("36.", "Estimated tax payments", "$4,000.00"),
        ("37.", "Total payments", "$52,250.00"),
        ("", "", ""),
        ("38.", "Overpayment (37 - 34)", "$8,630.81"),
        ("39.", "Amount to be refunded", "$6,630.81"),
        ("40.", "Applied to next year's estimated tax", "$2,000.00"),
    ]

    y = 100
    for line_num, desc, amount in tax_calc:
        if line_num:
            page4.insert_text(pymupdf.Point(72, y), line_num, fontsize=9, fontname="hebo", color=(0, 0, 0))
            page4.insert_text(pymupdf.Point(100, y), desc, fontsize=9, fontname="helv", color=(0, 0, 0))
        if amount:
            page4.insert_text(pymupdf.Point(480, y), amount, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 18

    # === Page 5: Declaration / Signature ===
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(pymupdf.Point(72, 60), "Declaration and Signatures", fontsize=14, fontname="hebo", color=(0, 0, 0.5))

    shape5 = page5.new_shape()
    shape5.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape5.finish(color=(0, 0, 0.5), width=1)
    shape5.commit()

    declaration = (
        "Under penalties of perjury, I declare that I have examined this return and "
        "accompanying schedules and statements, and to the best of my knowledge and belief, "
        "they are true, correct, and complete. Declaration of preparer (other than taxpayer) "
        "is based on all information of which preparer has any knowledge."
    )

    rect = pymupdf.Rect(72, 90, 540, 180)
    page5.insert_textbox(rect, declaration, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Signature lines
    y = 220
    sig_fields = [
        ("Taxpayer Signature:", "Margaret R. Whitfield", "03/28/2024"),
        ("Spouse Signature:", "Thomas J. Whitfield", "03/28/2024"),
        ("Preparer Signature:", "David A. Henderson, CPA", "03/28/2024"),
    ]
    for label, name, date in sig_fields:
        page5.insert_text(pymupdf.Point(72, y), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        # Signature line
        shape5b = page5.new_shape()
        shape5b.draw_line(pymupdf.Point(200, y + 3), pymupdf.Point(400, y + 3))
        shape5b.finish(color=(0, 0, 0), width=0.5)
        shape5b.commit()
        page5.insert_text(pymupdf.Point(205, y), name, fontsize=10, fontname="heit", color=(0.2, 0.2, 0.2))
        page5.insert_text(pymupdf.Point(420, y), f"Date: {date}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 40

    # Firm info
    y += 20
    page5.insert_text(pymupdf.Point(72, y), "Preparer's Firm:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(200, y), "Henderson & Associates, CPA", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page5.insert_text(pymupdf.Point(72, y), "Firm Address:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(200, y), "890 NW Everett Street, Suite 400, Portland, OR 97209", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page5.insert_text(pymupdf.Point(72, y), "Firm EIN:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(200, y), "93-1234567", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 20
    page5.insert_text(pymupdf.Point(72, y), "Phone:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(200, y), "(503) 555-0147", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Footer on each page
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(pymupdf.Point(250, 775), f"Page {i+1} of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
        p.insert_text(pymupdf.Point(72, 775), "Form 1040 — Tax Year 2023", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
