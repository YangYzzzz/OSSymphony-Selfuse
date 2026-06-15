"""
Initial Setup: Expense report PDF with 7 embedded receipt images
Task ID: pdf_fin_067
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_067'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/expense_with_receipts.pdf'


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


def create_receipt_image(receipt_data):
    """Create a realistic receipt image using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = receipt_data['width'], receipt_data['height']
    img = Image.new('RGB', (width, height), color=(255, 252, 245))
    draw = ImageDraw.Draw(img)

    try:
        font_regular = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except OSError:
        font_regular = ImageFont.load_default()
        font_bold = font_regular
        font_small = font_regular
        font_title = font_regular

    # Draw border
    draw.rectangle([(2, 2), (width - 3, height - 3)], outline=(180, 180, 180), width=1)

    y = 15
    # Store name
    draw.text((width // 2 - 60, y), receipt_data['store'], fill=(30, 30, 30), font=font_title)
    y += 30
    # Address
    draw.text((width // 2 - 80, y), receipt_data['address'], fill=(100, 100, 100), font=font_small)
    y += 20
    # Date and time
    draw.text((15, y), receipt_data['datetime'], fill=(60, 60, 60), font=font_small)
    y += 20
    # Separator
    draw.line([(10, y), (width - 10, y)], fill=(180, 180, 180), width=1)
    y += 10

    # Items
    for item_name, item_price in receipt_data['items']:
        draw.text((15, y), item_name, fill=(40, 40, 40), font=font_regular)
        draw.text((width - 80, y), item_price, fill=(40, 40, 40), font=font_regular)
        y += 22

    # Separator
    y += 5
    draw.line([(10, y), (width - 10, y)], fill=(180, 180, 180), width=1)
    y += 10

    # Subtotal, tax, total
    draw.text((15, y), "Subtotal:", fill=(60, 60, 60), font=font_regular)
    draw.text((width - 80, y), receipt_data['subtotal'], fill=(60, 60, 60), font=font_regular)
    y += 22
    draw.text((15, y), "Tax:", fill=(60, 60, 60), font=font_regular)
    draw.text((width - 80, y), receipt_data['tax'], fill=(60, 60, 60), font=font_regular)
    y += 22
    draw.text((15, y), "TOTAL:", fill=(20, 20, 20), font=font_bold)
    draw.text((width - 80, y), receipt_data['total'], fill=(20, 20, 20), font=font_bold)
    y += 30

    # Payment method
    draw.text((15, y), receipt_data['payment'], fill=(100, 100, 100), font=font_small)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.read()


def create_initial():
    import pymupdf

    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Define 7 realistic receipts
    receipts = [
        {
            'store': 'Marriott Hotel',
            'address': '1200 Pacific Ave, San Francisco, CA',
            'datetime': '2025-11-04  14:32',
            'items': [
                ('Deluxe Room (2 nights)', '$478.00'),
                ('Room Service - Dinner', '$67.50'),
                ('Parking (2 days)', '$56.00'),
            ],
            'subtotal': '$601.50',
            'tax': '$54.14',
            'total': '$655.64',
            'payment': 'Visa ending 4821',
            'width': 320, 'height': 340,
        },
        {
            'store': 'Delta Airlines',
            'address': 'SFO Terminal 2, Gate B14',
            'datetime': '2025-11-03  06:15',
            'items': [
                ('SFO -> ORD Economy', '$342.00'),
                ('Seat Upgrade 14A', '$45.00'),
                ('Checked Bag', '$35.00'),
            ],
            'subtotal': '$422.00',
            'tax': '$37.98',
            'total': '$459.98',
            'payment': 'Corp Amex ending 1190',
            'width': 310, 'height': 330,
        },
        {
            'store': 'The Capital Grille',
            'address': '87 E Wacker Dr, Chicago, IL',
            'datetime': '2025-11-04  19:45',
            'items': [
                ('Dry-Aged NY Strip', '$62.00'),
                ('Caesar Salad', '$18.00'),
                ('Lobster Bisque', '$22.00'),
                ('Sparkling Water (2)', '$14.00'),
                ('Espresso', '$6.50'),
            ],
            'subtotal': '$122.50',
            'tax': '$12.25',
            'total': '$134.75',
            'payment': 'Corp Amex ending 1190',
            'width': 300, 'height': 380,
        },
        {
            'store': 'Yellow Cab Co.',
            'address': 'Chicago, IL',
            'datetime': '2025-11-04  08:22',
            'items': [
                ('ORD Airport -> Downtown', '$52.00'),
                ('Toll charges', '$4.50'),
            ],
            'subtotal': '$56.50',
            'tax': '$0.00',
            'total': '$56.50',
            'payment': 'Visa ending 4821',
            'width': 280, 'height': 260,
        },
        {
            'store': 'Office Depot',
            'address': '440 N Michigan Ave, Chicago, IL',
            'datetime': '2025-11-05  10:30',
            'items': [
                ('USB-C Hub Adapter', '$45.99'),
                ('Presentation Pointer', '$32.99'),
                ('Legal Pads (3-pack)', '$12.49'),
                ('Ballpoint Pens (12)', '$8.99'),
            ],
            'subtotal': '$100.46',
            'tax': '$10.35',
            'total': '$110.81',
            'payment': 'Corp Amex ending 1190',
            'width': 310, 'height': 350,
        },
        {
            'store': 'Starbucks',
            'address': '233 S Wacker Dr, Chicago, IL',
            'datetime': '2025-11-05  07:50',
            'items': [
                ('Grande Americano', '$4.95'),
                ('Blueberry Muffin', '$3.75'),
            ],
            'subtotal': '$8.70',
            'tax': '$0.91',
            'total': '$9.61',
            'payment': 'Visa ending 4821',
            'width': 270, 'height': 250,
        },
        {
            'store': 'Hertz Car Rental',
            'address': "O'Hare Airport, Chicago, IL",
            'datetime': '2025-11-05  16:00',
            'items': [
                ('Midsize Sedan (1 day)', '$89.00'),
                ('Insurance Waiver', '$24.00'),
                ('Fuel Prepay', '$42.00'),
            ],
            'subtotal': '$155.00',
            'tax': '$16.28',
            'total': '$171.28',
            'payment': 'Corp Amex ending 1190',
            'width': 310, 'height': 330,
        },
    ]

    # Generate receipt images
    receipt_images = []
    for r in receipts:
        img_bytes = create_receipt_image(r)
        receipt_images.append(img_bytes)

    # Create the 10-page expense report PDF
    doc = pymupdf.open()

    PAGE_W, PAGE_H = 612, 792  # Letter size
    MARGIN = 72

    # --- Page 1: Cover / Title ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 120), "EXPENSE REPORT", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(MARGIN, 165), "Business Trip: Chicago Client Meeting", fontsize=16, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(MARGIN, 210), "Employee: Rachel Nguyen", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 230), "Department: Business Development", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 250), "Employee ID: EMP-20847", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 270), "Travel Period: November 3-5, 2025", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 290), "Report Date: November 10, 2025", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 310), "Approver: James Whitfield (VP Sales)", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(MARGIN, 360), "Total Claimed: $1,598.57", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))

    # --- Page 2: Expense Summary Table ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "Expense Summary", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))

    # Draw table header
    y = 90
    headers = ["Date", "Category", "Vendor", "Amount"]
    col_x = [MARGIN, MARGIN + 90, MARGIN + 200, MARGIN + 400]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y), h, fontsize=11, fontname="hebo")
    y += 5
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN, y), pymupdf.Point(PAGE_W - MARGIN, y))
    shape.finish(color=(0.3, 0.3, 0.3), width=1)
    shape.commit()

    expenses = [
        ("2025-11-03", "Airfare", "Delta Airlines", "$459.98"),
        ("2025-11-04", "Lodging", "Marriott Hotel", "$655.64"),
        ("2025-11-04", "Meals", "The Capital Grille", "$134.75"),
        ("2025-11-04", "Transport", "Yellow Cab Co.", "$56.50"),
        ("2025-11-05", "Supplies", "Office Depot", "$110.81"),
        ("2025-11-05", "Meals", "Starbucks", "$9.61"),
        ("2025-11-05", "Transport", "Hertz Car Rental", "$171.28"),
    ]
    y += 20
    for row in expenses:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=10, fontname="helv")
        y += 18

    y += 10
    page.insert_text(pymupdf.Point(col_x[2], y), "Grand Total:", fontsize=11, fontname="hebo")
    page.insert_text(pymupdf.Point(col_x[3], y), "$1,598.57", fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))

    # --- Page 3: Travel & Airfare with Receipt 1 (Delta) ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "1. Airfare - Delta Airlines", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 160),
        "Round-trip economy flight from San Francisco (SFO) to Chicago O'Hare (ORD) on "
        "November 3, 2025. Seat upgraded to 14A for additional legroom. One checked bag "
        "for presentation materials and client gifts. Flight departed on time at 7:15 AM PST.",
        fontsize=11, fontname="helv",
    )
    # Embed receipt image (Delta)
    page.insert_text(pymupdf.Point(MARGIN, 175), "Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 190, MARGIN + 20 + 310, 190 + 330), stream=receipt_images[1])

    # --- Page 4: Hotel with Receipt 2 (Marriott) ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "2. Lodging - Marriott Hotel", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 150),
        "Two-night stay at the San Francisco Marriott Marquis, November 3-5. Deluxe room "
        "selected per company travel policy for trips exceeding 2 days. Room service dinner "
        "on arrival night due to late check-in. Hotel parking for rental vehicle.",
        fontsize=11, fontname="helv",
    )
    page.insert_text(pymupdf.Point(MARGIN, 165), "Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 180, MARGIN + 20 + 320, 180 + 340), stream=receipt_images[0])

    # --- Page 5: Client Dinner with Receipt 3 (Capital Grille) ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "3. Client Dinner - The Capital Grille", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 160),
        "Dinner meeting with Apex Solutions team (Sarah Kim, VP Engineering; David Park, "
        "CTO) to discuss Q1 2026 partnership proposal. Discussed product integration timeline "
        "and pricing structure. Meal for one (client expenses covered by Apex).",
        fontsize=11, fontname="helv",
    )
    page.insert_text(pymupdf.Point(MARGIN, 175), "Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 190, MARGIN + 20 + 300, 190 + 380), stream=receipt_images[2])

    # --- Page 6: Transportation with Receipts 4 & 5 (Cab + Hertz) ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "4. Ground Transportation", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 130),
        "Taxi from O'Hare to downtown Chicago hotel on arrival. Rental car from Hertz on "
        "departure day for client site visit in suburban Naperville before return flight.",
        fontsize=11, fontname="helv",
    )
    page.insert_text(pymupdf.Point(MARGIN, 145), "Taxi Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 160, MARGIN + 20 + 280, 160 + 260), stream=receipt_images[3])

    page.insert_text(pymupdf.Point(MARGIN, 440), "Car Rental Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 455, MARGIN + 20 + 310, 455 + 330), stream=receipt_images[6])

    # --- Page 7: Office Supplies with Receipt 6 (Office Depot) ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "5. Office Supplies - Office Depot", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 150),
        "Purchased USB-C hub adapter and wireless presentation pointer for client demo. "
        "Also picked up legal pads and pens for meeting notes. All items were necessary "
        "for the client presentation at Apex Solutions headquarters.",
        fontsize=11, fontname="helv",
    )
    page.insert_text(pymupdf.Point(MARGIN, 165), "Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 180, MARGIN + 20 + 310, 180 + 350), stream=receipt_images[4])

    # --- Page 8: Meals - Starbucks with Receipt 7 ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "6. Meals - Starbucks", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 80, PAGE_W - MARGIN, 130),
        "Breakfast on November 5 before the client presentation. Coffee and muffin at the "
        "Starbucks near Willis Tower, walking distance from the hotel.",
        fontsize=11, fontname="helv",
    )
    page.insert_text(pymupdf.Point(MARGIN, 145), "Receipt:", fontsize=11, fontname="hebo")
    page.insert_image(pymupdf.Rect(MARGIN + 20, 160, MARGIN + 20 + 270, 160 + 250), stream=receipt_images[5])

    # --- Page 9: Policy Compliance Notes ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "Policy Compliance Notes", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(MARGIN, 85, PAGE_W - MARGIN, 400),
        "All expenses comply with the company travel policy (Rev. 3.2, effective July 2025):\n\n"
        "- Airfare: Economy class booked 14 days in advance per Section 4.1.\n"
        "- Lodging: Rate within approved per-diem for San Francisco ($350/night). "
        "Two-night stay approved by manager for trips exceeding one business day.\n"
        "- Meals: Client dinner within $150 single-meal cap (Section 6.3). "
        "Breakfast within $25 daily meal allowance.\n"
        "- Ground Transport: Taxi and rental car approved for airport transfers and client "
        "site visits per Section 5.2. Rental was midsize category as required.\n"
        "- Supplies: Business-related purchases under $200 pre-approved per Section 8.1.\n\n"
        "All original receipts are attached as images within this report.\n\n"
        "Submitted electronically via the company expense portal.",
        fontsize=11, fontname="helv",
    )

    # --- Page 10: Approval / Signatures ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(MARGIN, 60), "Approval", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(MARGIN, 100), "Employee Signature:", fontsize=12, fontname="helv")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN + 150, 105), pymupdf.Point(PAGE_W - MARGIN, 105))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(MARGIN, 125), "Rachel Nguyen", fontsize=12, fontname="heit")
    page.insert_text(pymupdf.Point(MARGIN, 145), "Date: November 10, 2025", fontsize=11, fontname="helv")

    page.insert_text(pymupdf.Point(MARGIN, 200), "Manager Approval:", fontsize=12, fontname="helv")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN + 150, 205), pymupdf.Point(PAGE_W - MARGIN, 205))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(MARGIN, 225), "James Whitfield, VP Sales", fontsize=12, fontname="heit")
    page.insert_text(pymupdf.Point(MARGIN, 245), "Date: _______________", fontsize=11, fontname="helv")

    page.insert_text(pymupdf.Point(MARGIN, 310), "Finance Department:", fontsize=12, fontname="helv")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN + 150, 315), pymupdf.Point(PAGE_W - MARGIN, 315))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(MARGIN, 340), "Date: _______________", fontsize=11, fontname="helv")

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Pages: 10, Embedded receipts: 7')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
