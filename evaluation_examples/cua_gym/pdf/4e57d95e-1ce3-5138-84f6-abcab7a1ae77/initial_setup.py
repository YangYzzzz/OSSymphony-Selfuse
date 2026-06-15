"""
Initial Setup: Create an unencrypted 12-page tax return PDF document.
Task ID: pdf_mbc_022
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_022'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/tax_return_2024.pdf'

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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN_L = 72
    MARGIN_R = 540
    MARGIN_T = 72

    # ---- Page 1: Cover Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(200, 120), "FORM 1040", fontsize=24, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(150, 160), "U.S. Individual Income Tax Return", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(220, 200), "Tax Year 2024", fontsize=14, fontname="helv", color=(0, 0, 0))

    # Taxpayer info
    y = 280
    info_lines = [
        ("Name:", "Margaret L. Chen"),
        ("Social Security Number:", "***-**-4829"),
        ("Filing Status:", "Single"),
        ("Address:", "1847 Oakwood Drive, Apt 12B"),
        ("City, State, ZIP:", "Portland, OR 97205"),
        ("Occupation:", "Senior Software Engineer"),
        ("Employer:", "Cascade Technologies Inc."),
    ]
    for label, value in info_lines:
        page.insert_text(pymupdf.Point(MARGIN_L, y), label, fontsize=11, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(250, y), value, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 24

    page.insert_text(pymupdf.Point(MARGIN_L, 700), "Prepared by: Greenfield Tax Associates, LLC", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(MARGIN_L, 716), "Date Prepared: March 15, 2025", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # ---- Page 2: Income Summary ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Schedule 1 - Income Summary", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    income_items = [
        ("1a", "Wages, salaries, tips (W-2)", "$142,850.00"),
        ("1b", "Tax-exempt interest", "$0.00"),
        ("2a", "Ordinary dividends", "$3,247.50"),
        ("2b", "Qualified dividends", "$2,891.25"),
        ("3a", "Capital gain distributions", "$1,125.00"),
        ("3b", "Net capital gain (Schedule D)", "$8,432.18"),
        ("4a", "IRA distributions", "$0.00"),
        ("4b", "Taxable IRA distributions", "$0.00"),
        ("5a", "Pensions and annuities", "$0.00"),
        ("5b", "Taxable pensions", "$0.00"),
        ("6",  "Social Security benefits", "$0.00"),
        ("7",  "Other income (Schedule 1)", "$2,150.00"),
        ("8",  "Total income", "$157,804.68"),
    ]
    y = 120
    for line_no, desc, amount in income_items:
        page.insert_text(pymupdf.Point(MARGIN_L, y), f"Line {line_no}.", fontsize=10, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(130, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 3: Deductions ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Schedule A - Itemized Deductions", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    deductions = [
        ("Medical and dental expenses", "$4,215.00"),
        ("State and local taxes (SALT)", "$10,000.00"),
        ("Property taxes", "$3,847.00"),
        ("Mortgage interest", "$12,456.00"),
        ("Charitable contributions - cash", "$5,200.00"),
        ("Charitable contributions - noncash", "$1,850.00"),
        ("Investment interest expense", "$0.00"),
        ("Casualty and theft losses", "$0.00"),
        ("Other itemized deductions", "$750.00"),
        ("Total itemized deductions", "$38,318.00"),
    ]
    y = 120
    for desc, amount in deductions:
        page.insert_text(pymupdf.Point(MARGIN_L, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Standard deduction comparison: $14,600 (Single filer)", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(MARGIN_L, y + 36), "Taxpayer elected itemized deductions as they exceed the standard deduction.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))

    # ---- Page 4: Tax Computation ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Tax Computation Worksheet", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    computations = [
        ("Adjusted Gross Income (AGI)", "$157,804.68"),
        ("Less: Itemized Deductions", "-$38,318.00"),
        ("Taxable Income", "$119,486.68"),
        ("", ""),
        ("Tax bracket calculation:", ""),
        ("  10% on first $11,600", "$1,160.00"),
        ("  12% on $11,601 - $47,150", "$4,266.00"),
        ("  22% on $47,151 - $100,525", "$11,742.50"),
        ("  24% on $100,526 - $119,486.68", "$4,550.60"),
        ("", ""),
        ("Total Federal Income Tax", "$21,719.10"),
        ("Less: Tax Credits", "-$0.00"),
        ("Net Tax Liability", "$21,719.10"),
    ]
    y = 120
    for desc, amount in computations:
        if desc == "":
            y += 12
            continue
        page.insert_text(pymupdf.Point(MARGIN_L, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        if amount:
            page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 5: Schedule B - Interest and Dividends ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Schedule B - Interest and Ordinary Dividends", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "Part I - Interest Income", fontsize=12, fontname="hebo", color=(0, 0, 0))
    interest_items = [
        ("First National Bank - Savings", "$847.32"),
        ("Vanguard Federal Money Market", "$1,203.65"),
        ("Treasury Direct - T-Bills", "$1,196.53"),
        ("Total Interest Income", "$3,247.50"),
    ]
    y = 150
    for desc, amount in interest_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Part II - Ordinary Dividends", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 50
    dividend_items = [
        ("Vanguard Total Stock Market ETF (VTI)", "$1,432.75"),
        ("iShares Core S&P 500 (IVV)", "$892.50"),
        ("Schwab US Dividend Equity (SCHD)", "$566.00"),
        ("Total Ordinary Dividends", "$2,891.25"),
    ]
    for desc, amount in dividend_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 6: Schedule C - Business Income ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Schedule C - Profit or Loss from Business", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "Business Name: MLChen Consulting", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, 140), "Principal Business: Software Development Consulting", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, 160), "Business Code: 541511", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, 180), "EIN: 93-XXXXXXX", fontsize=10, fontname="helv", color=(0, 0, 0))

    biz_items = [
        ("Gross receipts", "$8,500.00"),
        ("Cost of goods sold", "$0.00"),
        ("Gross profit", "$8,500.00"),
        ("Advertising", "-$250.00"),
        ("Insurance", "-$1,200.00"),
        ("Office expenses", "-$480.00"),
        ("Supplies", "-$320.00"),
        ("Software subscriptions", "-$2,100.00"),
        ("Internet (50% business use)", "-$600.00"),
        ("Professional development", "-$1,400.00"),
        ("Net profit (loss)", "$2,150.00"),
    ]
    y = 220
    for desc, amount in biz_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 7: Schedule D - Capital Gains ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Schedule D - Capital Gains and Losses", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "Part I - Short-Term Capital Gains (held 1 year or less)", fontsize=11, fontname="hebo", color=(0, 0, 0))

    short_term = [
        ("NVDA - 50 shares sold 03/12/2024", "Proceeds: $12,450.00", "Basis: $9,875.00", "Gain: $2,575.00"),
        ("AAPL - 25 shares sold 06/08/2024", "Proceeds: $5,237.50", "Basis: $4,812.50", "Gain: $425.00"),
    ]
    y = 150
    for item in short_term:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), item[0], fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 16
        page.insert_text(pymupdf.Point(MARGIN_L + 40, y), f"{item[1]}   {item[2]}   {item[3]}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 10), "Part II - Long-Term Capital Gains (held more than 1 year)", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 40

    long_term = [
        ("MSFT - 30 shares sold 09/15/2024", "Proceeds: $12,630.00", "Basis: $8,340.00", "Gain: $4,290.00"),
        ("VTI - 40 shares sold 11/20/2024", "Proceeds: $10,480.00", "Basis: $9,337.82", "Gain: $1,142.18"),
    ]
    for item in long_term:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), item[0], fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 16
        page.insert_text(pymupdf.Point(MARGIN_L + 40, y), f"{item[1]}   {item[2]}   {item[3]}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Net Short-Term Capital Gain: $3,000.00", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, y + 40), "Net Long-Term Capital Gain: $5,432.18", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, y + 60), "Total Net Capital Gain: $8,432.18", fontsize=10, fontname="hebo", color=(0, 0, 0))

    # ---- Page 8: W-2 Summary ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "W-2 Wage and Tax Statement Summary", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "Employer: Cascade Technologies Inc.", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN_L, 140), "EIN: 91-XXXXXXX", fontsize=10, fontname="helv", color=(0, 0, 0))

    w2_items = [
        ("Box 1 - Wages, tips, other compensation", "$142,850.00"),
        ("Box 2 - Federal income tax withheld", "$28,570.00"),
        ("Box 3 - Social Security wages", "$142,850.00"),
        ("Box 4 - Social Security tax withheld", "$8,856.70"),
        ("Box 5 - Medicare wages and tips", "$142,850.00"),
        ("Box 6 - Medicare tax withheld", "$2,071.33"),
        ("Box 12a - 401(k) contributions (Code D)", "$23,000.00"),
        ("Box 12b - Health savings account (Code W)", "$4,150.00"),
        ("Box 14 - State income tax withheld", "$9,142.40"),
    ]
    y = 170
    for desc, amount in w2_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 9: 1099 Forms Summary ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "1099 Forms Summary", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "1099-INT (Interest Income)", fontsize=12, fontname="hebo", color=(0, 0, 0))
    int_items = [
        ("First National Bank", "$847.32"),
        ("Vanguard Federal Money Market", "$1,203.65"),
        ("Treasury Direct", "$1,196.53"),
    ]
    y = 150
    for desc, amount in int_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "1099-DIV (Dividend Income)", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 50
    div_items = [
        ("Vanguard Brokerage - Ordinary dividends", "$2,891.25"),
        ("Vanguard Brokerage - Qualified dividends", "$2,891.25"),
        ("Capital gain distributions", "$1,125.00"),
    ]
    for desc, amount in div_items:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "1099-B (Brokerage Proceeds)", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 50
    page.insert_text(pymupdf.Point(MARGIN_L + 20, y), "Total proceeds from broker transactions", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(460, y), "$40,797.50", fontsize=10, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(MARGIN_L, y + 40), "1099-NEC (Nonemployee Compensation)", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 70
    page.insert_text(pymupdf.Point(MARGIN_L + 20, y), "MLChen Consulting - Contract work", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(460, y), "$8,500.00", fontsize=10, fontname="helv", color=(0, 0, 0))

    # ---- Page 10: Tax Credits and Payments ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Credits and Payments Summary", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(MARGIN_L, 120), "Tax Credits", fontsize=12, fontname="hebo", color=(0, 0, 0))
    credits = [
        ("Child Tax Credit", "$0.00"),
        ("Education Credits (Lifetime Learning)", "$0.00"),
        ("Retirement Savings Credit", "$0.00"),
        ("Energy Efficient Home Credit", "$0.00"),
        ("Total Credits", "$0.00"),
    ]
    y = 150
    for desc, amount in credits:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 20), "Payments and Withholdings", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 50
    payments = [
        ("Federal income tax withheld (W-2)", "$28,570.00"),
        ("Estimated tax payments (Q1-Q4)", "$3,200.00"),
        ("Self-employment tax (Schedule SE)", "$1,212.75"),
        ("Total payments", "$31,770.00"),
    ]
    for desc, amount in payments:
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    page.insert_text(pymupdf.Point(MARGIN_L, y + 30), "Refund / Amount Owed Calculation:", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 60
    page.insert_text(pymupdf.Point(MARGIN_L + 20, y), "Total tax liability", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(460, y), "$22,931.85", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 22
    page.insert_text(pymupdf.Point(MARGIN_L + 20, y), "Total payments and credits", fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(460, y), "$31,770.00", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 22
    page.insert_text(pymupdf.Point(MARGIN_L + 20, y), "REFUND DUE", fontsize=12, fontname="hebo", color=(0, 0.4, 0))
    page.insert_text(pymupdf.Point(460, y), "$8,838.15", fontsize=12, fontname="hebo", color=(0, 0.4, 0))

    # ---- Page 11: State Tax Return - Oregon ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Oregon Form 40 - Individual Income Tax Return", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    or_items = [
        ("Federal AGI", "$157,804.68"),
        ("Oregon additions", "$0.00"),
        ("Oregon subtractions", "-$7,050.00"),
        ("Oregon taxable income", "$150,754.68"),
        ("", ""),
        ("Oregon income tax", "$13,567.92"),
        ("Oregon standard credit", "-$236.00"),
        ("Net Oregon tax", "$13,331.92"),
        ("Oregon tax withheld (W-2 Box 17)", "$9,142.40"),
        ("Oregon estimated payments", "$2,400.00"),
        ("Total Oregon payments", "$11,542.40"),
        ("Oregon tax owed", "$1,789.52"),
    ]
    y = 120
    for desc, amount in or_items:
        if desc == "":
            y += 12
            continue
        page.insert_text(pymupdf.Point(MARGIN_L + 20, y), desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # ---- Page 12: Signature and Declaration ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_L, 80), "Declaration and Signature", fontsize=16, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, 90), pymupdf.Point(MARGIN_R, 90))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    declaration = (
        "Under penalties of perjury, I declare that I have examined this return and "
        "accompanying schedules and statements, and to the best of my knowledge and "
        "belief, they are true, correct, and complete. Declaration of preparer (other "
        "than taxpayer) is based on all information of which preparer has any knowledge."
    )
    rect = pymupdf.Rect(MARGIN_L, 110, MARGIN_R, 200)
    page.insert_textbox(rect, declaration, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y = 240
    sig_fields = [
        ("Taxpayer Signature:", "Margaret L. Chen"),
        ("Date:", "March 15, 2025"),
        ("Taxpayer Phone:", "(503) 555-0147"),
        ("Email:", "m.chen@cascadetech.example.com"),
        ("", ""),
        ("Preparer Signature:", "David R. Greenfield, CPA"),
        ("Preparer Firm:", "Greenfield Tax Associates, LLC"),
        ("Preparer PTIN:", "P01234567"),
        ("Firm EIN:", "93-XXXXXXX"),
        ("Firm Address:", "2200 SW Morrison St, Suite 400, Portland, OR 97205"),
        ("Preparer Phone:", "(503) 555-0283"),
        ("Date:", "March 15, 2025"),
    ]
    for label, value in sig_fields:
        if label == "":
            y += 20
            continue
        page.insert_text(pymupdf.Point(MARGIN_L, y), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(230, y), value, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 24

    # Add footer to all pages
    for i in range(len(doc)):
        p = doc[i]
        p.insert_text(
            pymupdf.Point(MARGIN_L, H - 30),
            f"Tax Return 2024 - Margaret L. Chen - Page {i+1} of 12",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
