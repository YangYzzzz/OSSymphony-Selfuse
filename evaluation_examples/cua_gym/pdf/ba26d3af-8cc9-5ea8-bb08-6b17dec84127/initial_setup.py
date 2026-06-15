"""
Initial Setup: Create a 14-page combined tax forms PDF bundle
Task ID: pdf_fin_074
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_074'
FINANCE_DIR = f'{WORKDIR}/finance'
FORMS_DIR = f'{FINANCE_DIR}/forms'
OUTPUT = f'{FINANCE_DIR}/tax_forms_bundle.pdf'

LETTER_W, LETTER_H = 612, 792  # US Letter in points


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


def add_page_header(page, title, page_num_label):
    """Add a header bar and page label to a page."""
    shape = page.new_shape()
    # Header background
    header_rect = pymupdf.Rect(0, 0, LETTER_W, 50)
    shape.draw_rect(header_rect)
    shape.finish(color=(0, 0, 0.4), fill=(0, 0, 0.4))
    shape.commit()
    page.insert_text(pymupdf.Point(30, 35), title,
                     fontsize=16, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(LETTER_W - 80, 35), page_num_label,
                     fontsize=10, fontname="helv", color=(1, 1, 1))


def add_form_field_line(page, y, label, value):
    """Add a labeled field line."""
    page.insert_text(pymupdf.Point(50, y), label,
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(220, y), value,
                     fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(218, y + 3), pymupdf.Point(550, y + 3))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()


def create_w2_pages(doc):
    """Pages 1-4: Form W-2 Wage and Tax Statement."""
    # Page 1 - Employee info
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form W-2 - Wage and Tax Statement", "Page 1 of 4")
    p.insert_text(pymupdf.Point(50, 90), "Tax Year 2025",
                  fontsize=12, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(50, 110), "Department of the Treasury - Internal Revenue Service",
                  fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    y = 150
    fields = [
        ("Employer (EIN):", "74-3829156  Meridian Technologies Inc."),
        ("Employer Address:", "2850 Westlake Blvd, Suite 400, Austin, TX 78746"),
        ("Employee SSN:", "***-**-8294"),
        ("Employee Name:", "Rebecca A. Thornton"),
        ("Employee Address:", "1437 Magnolia Drive, Austin, TX 78703"),
        ("Wages, tips, other:", "$127,450.00"),
        ("Federal tax withheld:", "$28,438.50"),
        ("Social Security wages:", "$127,450.00"),
        ("Social Security tax:", "$7,902.00"),
        ("Medicare wages:", "$127,450.00"),
        ("Medicare tax:", "$1,848.03"),
    ]
    for label, val in fields:
        add_form_field_line(p, y, label, val)
        y += 28

    # Page 2 - State and local
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form W-2 - State and Local Tax Information", "Page 2 of 4")
    y = 90
    fields2 = [
        ("State:", "TX"),
        ("State wages:", "$127,450.00"),
        ("State income tax:", "$0.00"),
        ("Local wages:", "$127,450.00"),
        ("Local income tax:", "$0.00"),
        ("Control number:", "W2-2025-RTH-004892"),
        ("Retirement plan:", "Yes - 401(k)"),
        ("Third-party sick pay:", "No"),
        ("Statutory employee:", "No"),
    ]
    for label, val in fields2:
        add_form_field_line(p, y, label, val)
        y += 28
    p.insert_text(pymupdf.Point(50, y + 30),
                  "Box 12 Codes: D - $19,500.00 (401k elective deferrals)",
                  fontsize=9, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(50, y + 50),
                  "Box 12 Codes: DD - $8,250.00 (Employer health coverage cost)",
                  fontsize=9, fontname="helv", color=(0, 0, 0))

    # Page 3 - Instructions Copy B
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form W-2 - Copy B: Employee's Records", "Page 3 of 4")
    instructions = (
        "This copy is for your records. You should keep this form with your tax "
        "records for at least 4 years after the date your return was due or filed, "
        "whichever is later. This information is being furnished to the Internal "
        "Revenue Service. If you are required to file a tax return, a negligence "
        "penalty or other sanction may be imposed on you if this income is taxable "
        "and you fail to report it."
    )
    p.insert_textbox(pymupdf.Rect(50, 80, 560, 250), instructions,
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(50, 280),
                  "IMPORTANT: Attach Copy B to your federal tax return (Form 1040).",
                  fontsize=10, fontname="hebo", color=(0.6, 0, 0))

    # Page 4 - Copy C employer
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form W-2 - Copy C: Employer's Records", "Page 4 of 4")
    p.insert_textbox(pymupdf.Rect(50, 80, 560, 200),
                     "This copy is for the employer's records. Retain for at least "
                     "4 years. Employer: Meridian Technologies Inc. EIN: 74-3829156. "
                     "Prepared by: Payroll Department, Contact: payroll@meridiantech.com",
                     fontsize=10, fontname="helv", color=(0, 0, 0))


def create_1099_pages(doc):
    """Pages 5-6: Form 1099-INT Interest Income."""
    # Page 5
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1099-INT - Interest Income", "Page 1 of 2")
    p.insert_text(pymupdf.Point(50, 90), "Tax Year 2025",
                  fontsize=12, fontname="hebo", color=(0, 0, 0))
    y = 130
    fields = [
        ("Payer's Name:", "First National Savings Bank"),
        ("Payer's TIN:", "36-4821097"),
        ("Payer's Address:", "900 Commerce Street, Dallas, TX 75201"),
        ("Recipient's TIN:", "***-**-8294"),
        ("Recipient:", "Rebecca A. Thornton"),
        ("1. Interest income:", "$3,842.67"),
        ("2. Early withdrawal penalty:", "$0.00"),
        ("3. Interest on U.S. bonds:", "$0.00"),
        ("4. Federal tax withheld:", "$576.40"),
        ("5. Investment expenses:", "$0.00"),
        ("6. Foreign tax paid:", "$0.00"),
    ]
    for label, val in fields:
        add_form_field_line(p, y, label, val)
        y += 26

    # Page 6 - Instructions
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1099-INT - Instructions for Recipient", "Page 2 of 2")
    text = (
        "The amount shown in Box 1 is taxable interest income that must be "
        "reported on your tax return. If this amount exceeds $1,500, you must "
        "complete Schedule B (Form 1040). Box 4 shows backup withholding. "
        "Include this amount on your income tax return as a payment. Account "
        "Type: High-Yield Savings, Account No: ****4738, Interest Rate: 4.85% APY."
    )
    p.insert_textbox(pymupdf.Rect(50, 80, 560, 280), text,
                     fontsize=10, fontname="helv", color=(0, 0, 0))


def create_1040_pages(doc):
    """Pages 7-10: Form 1040 Individual Income Tax Return."""
    # Page 7 - Personal info
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1040 - U.S. Individual Income Tax Return", "Page 1 of 4")
    p.insert_text(pymupdf.Point(50, 90), "For Tax Year January 1 - December 31, 2025",
                  fontsize=11, fontname="hebo", color=(0, 0, 0))
    y = 130
    fields = [
        ("Filing Status:", "Single"),
        ("First name and initial:", "Rebecca A."),
        ("Last name:", "Thornton"),
        ("SSN:", "***-**-8294"),
        ("Address:", "1437 Magnolia Drive"),
        ("City, State, ZIP:", "Austin, TX 78703"),
        ("Digital assets (Yes/No):", "No"),
        ("Standard deduction:", "Yes"),
        ("Age 65 or older:", "No"),
        ("Blind:", "No"),
    ]
    for label, val in fields:
        add_form_field_line(p, y, label, val)
        y += 26

    # Page 8 - Income
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1040 - Income", "Page 2 of 4")
    y = 90
    income_fields = [
        ("1. Wages (from W-2):", "$127,450.00"),
        ("2a. Tax-exempt interest:", "$0.00"),
        ("2b. Taxable interest:", "$3,842.67"),
        ("3a. Qualified dividends:", "$1,205.00"),
        ("3b. Ordinary dividends:", "$1,205.00"),
        ("4a. IRA distributions:", "$0.00"),
        ("4b. Taxable amount:", "$0.00"),
        ("5a. Pensions:", "$0.00"),
        ("5b. Taxable amount:", "$0.00"),
        ("6. Social Security:", "$0.00"),
        ("7. Capital gain/loss:", "$2,340.00"),
        ("8. Other income:", "$48,720.00"),
        ("9. Total income:", "$183,557.67"),
        ("10. Adjustments:", "$19,500.00"),
        ("11. Adjusted gross income:", "$164,057.67"),
    ]
    for label, val in income_fields:
        add_form_field_line(p, y, label, val)
        y += 24

    # Page 9 - Deductions and tax
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1040 - Tax and Credits", "Page 3 of 4")
    y = 90
    tax_fields = [
        ("12. Standard deduction:", "$14,600.00"),
        ("13. Qualified business:", "$0.00"),
        ("14. Total deductions:", "$14,600.00"),
        ("15. Taxable income:", "$149,457.67"),
        ("16. Tax:", "$30,766.53"),
        ("17. Amount from Sch 2:", "$0.00"),
        ("18. Total tax before credits:", "$30,766.53"),
        ("19. Child tax credit:", "$0.00"),
        ("20. Other credits:", "$0.00"),
        ("21. Total credits:", "$0.00"),
        ("22. Tax after credits:", "$30,766.53"),
    ]
    for label, val in tax_fields:
        add_form_field_line(p, y, label, val)
        y += 26

    # Page 10 - Payments and refund
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Form 1040 - Payments and Refund", "Page 4 of 4")
    y = 90
    payment_fields = [
        ("24. Federal tax withheld:", "$29,014.90"),
        ("25. Estimated tax payments:", "$0.00"),
        ("26. Earned income credit:", "$0.00"),
        ("27. Additional child credit:", "$0.00"),
        ("28. Other payments:", "$0.00"),
        ("29. Total payments:", "$29,014.90"),
        ("30. Tax after credits:", "$30,766.53"),
        ("31. Amount owed:", "$1,751.63"),
        ("32. Estimated tax penalty:", "$0.00"),
    ]
    for label, val in payment_fields:
        add_form_field_line(p, y, label, val)
        y += 28
    p.insert_text(pymupdf.Point(50, y + 30),
                  "Under penalties of perjury, I declare that I have examined this return "
                  "and to the best of my knowledge and belief, it is true and correct.",
                  fontsize=8, fontname="heit", color=(0.3, 0.3, 0.3))


def create_schedule_c_pages(doc):
    """Pages 11-14: Schedule C - Profit or Loss From Business."""
    # Page 11 - Business info
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Schedule C - Profit or Loss From Business", "Page 1 of 4")
    p.insert_text(pymupdf.Point(50, 90), "Tax Year 2025",
                  fontsize=12, fontname="hebo", color=(0, 0, 0))
    y = 130
    fields = [
        ("Name of proprietor:", "Rebecca A. Thornton"),
        ("SSN:", "***-**-8294"),
        ("Business name:", "Thornton Digital Consulting"),
        ("Business address:", "1437 Magnolia Drive, Austin, TX 78703"),
        ("EIN:", "84-6203571"),
        ("Principal business code:", "541512 - Computer Systems Design"),
        ("Accounting method:", "Cash"),
        ("Did you start business in 2025?:", "No"),
        ("Payments requiring 1099s?:", "Yes"),
        ("Did you file all 1099s?:", "Yes"),
    ]
    for label, val in fields:
        add_form_field_line(p, y, label, val)
        y += 26

    # Page 12 - Income section
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Schedule C - Part I: Income", "Page 2 of 4")
    y = 90
    income = [
        ("1. Gross receipts:", "$84,600.00"),
        ("2. Returns and allowances:", "$0.00"),
        ("3. Net receipts (1 - 2):", "$84,600.00"),
        ("4. Cost of goods sold:", "$0.00"),
        ("5. Gross profit (3 - 4):", "$84,600.00"),
        ("6. Other income:", "$0.00"),
        ("7. Gross income (5 + 6):", "$84,600.00"),
    ]
    for label, val in income:
        add_form_field_line(p, y, label, val)
        y += 30
    p.insert_text(pymupdf.Point(50, y + 20),
                  "Income Sources: Cloudbridge Corp ($32,000), Apex Ventures ($28,400), "
                  "Nexgen Solutions ($14,200), Various small clients ($10,000)",
                  fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))

    # Page 13 - Expenses
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Schedule C - Part II: Expenses", "Page 3 of 4")
    y = 90
    expenses = [
        ("8. Advertising:", "$2,400.00"),
        ("9. Car and truck expenses:", "$3,150.00"),
        ("10. Commissions and fees:", "$850.00"),
        ("11. Contract labor:", "$6,200.00"),
        ("12. Insurance:", "$2,880.00"),
        ("13. Interest (mortgage):", "$0.00"),
        ("14. Interest (other):", "$0.00"),
        ("15. Legal/professional:", "$1,500.00"),
        ("16. Office expense:", "$2,340.00"),
        ("17. Rent (vehicles/equip):", "$0.00"),
        ("18. Rent (other):", "$4,800.00"),
        ("19. Repairs and maintenance:", "$680.00"),
        ("20. Supplies:", "$1,920.00"),
        ("21. Taxes and licenses:", "$450.00"),
        ("22. Travel:", "$3,860.00"),
        ("23. Meals (50%):", "$1,250.00"),
        ("24. Utilities:", "$1,600.00"),
        ("25. Other expenses:", "$2,000.00"),
    ]
    for label, val in expenses:
        add_form_field_line(p, y, label, val)
        y += 22

    # Page 14 - Net profit
    p = doc.new_page(width=LETTER_W, height=LETTER_H)
    add_page_header(p, "Schedule C - Part II (cont.) and Net Profit", "Page 4 of 4")
    y = 90
    summary = [
        ("26. Total expenses:", "$35,880.00"),
        ("27. Tentative profit (7 - 26):", "$48,720.00"),
        ("28. Home office deduction:", "$0.00"),
        ("29. Net profit (27 - 28):", "$48,720.00"),
    ]
    for label, val in summary:
        add_form_field_line(p, y, label, val)
        y += 30
    p.insert_text(pymupdf.Point(50, y + 20),
                  "If a profit, enter on Form 1040 line 8. If a loss, you must check "
                  "the box that describes your investment in this activity.",
                  fontsize=9, fontname="helv", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(50, y + 50),
                  "Part III: Cost of Goods Sold - Not applicable (service business)",
                  fontsize=10, fontname="hebo", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(50, y + 80),
                  "Part IV: Vehicle Information - Standard mileage rate used, "
                  "12,600 miles driven for business in 2025.",
                  fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)
    os.makedirs(FORMS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Pages 1-4: W-2
    create_w2_pages(doc)
    # Pages 5-6: 1099-INT
    create_1099_pages(doc)
    # Pages 7-10: 1040
    create_1040_pages(doc)
    # Pages 11-14: Schedule C
    create_schedule_c_pages(doc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 14')
    print(f'Forms directory exists: {os.path.isdir(FORMS_DIR)}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
