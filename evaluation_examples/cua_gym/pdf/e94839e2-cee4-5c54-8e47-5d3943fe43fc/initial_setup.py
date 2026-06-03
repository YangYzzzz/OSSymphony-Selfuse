"""
Initial Setup: Create a 20-page vendor contracts PDF with phone numbers and dollar amounts
Task ID: pdf_pw_019
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_019'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/vendor_contracts.pdf'


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


# Vendor data for realistic content
VENDORS = [
    {
        "name": "Apex Supply Co.",
        "contact": "Sarah Chen",
        "phone": "(555) 234-8901",
        "address": "1420 Industrial Blvd, Suite 200, Portland, OR 97201",
        "services": "Industrial cleaning supplies and janitorial equipment",
    },
    {
        "name": "BlueLine Logistics LLC",
        "contact": "Marcus Johnson",
        "phone": "(555) 678-3412",
        "address": "890 Commerce Way, Dallas, TX 75201",
        "services": "Freight transportation and warehousing solutions",
    },
    {
        "name": "CrestView IT Solutions",
        "contact": "Priya Patel",
        "phone": "(555) 901-2345",
        "address": "3300 Tech Park Drive, San Jose, CA 95134",
        "services": "Managed IT services, cloud infrastructure, and cybersecurity",
    },
    {
        "name": "Dawson & Partners Consulting",
        "contact": "Robert Dawson",
        "phone": "(555) 456-7890",
        "address": "55 Financial Center, 12th Floor, Chicago, IL 60601",
        "services": "Strategic consulting, market analysis, and business development",
    },
    {
        "name": "EverGreen Facilities Management",
        "contact": "Linda Torres",
        "phone": "(555) 123-4567",
        "address": "700 Park Avenue, Denver, CO 80202",
        "services": "Building maintenance, HVAC servicing, and landscaping",
    },
    {
        "name": "Frontier Digital Marketing",
        "contact": "James O'Brien",
        "phone": "(555) 345-6789",
        "address": "2100 Creative Blvd, Austin, TX 78701",
        "services": "SEO, PPC campaigns, social media management, and content strategy",
    },
    {
        "name": "GoldStar Catering Services",
        "contact": "Maria Gonzalez",
        "phone": "(555) 567-8901",
        "address": "445 Culinary Lane, Miami, FL 33101",
        "services": "Corporate catering, event planning, and food service management",
    },
    {
        "name": "Harbor Security Systems",
        "contact": "David Kim",
        "phone": "(555) 789-0123",
        "address": "1600 Security Way, Seattle, WA 98101",
        "services": "Access control, surveillance systems, and security personnel",
    },
    {
        "name": "Ironclad Legal Services",
        "contact": "Catherine Wright",
        "phone": "(555) 012-3456",
        "address": "800 Justice Blvd, Suite 500, Boston, MA 02101",
        "services": "Contract review, compliance auditing, and corporate legal counsel",
    },
    {
        "name": "JetStream Courier Inc.",
        "contact": "Thomas Rivera",
        "phone": "(555) 890-1234",
        "address": "320 Express Drive, Atlanta, GA 30301",
        "services": "Same-day delivery, overnight shipping, and document courier services",
    },
]

# Dollar amounts to embed across the document
AMOUNTS = [
    "$1,500.00", "$25,000.00", "$750.00", "$12,350.00", "$8,900.00",
    "$45,000.00", "$3,200.00", "$67,500.00", "$2,100.00", "$18,750.00",
    "$5,400.00", "$32,000.00", "$950.00", "$15,600.00", "$42,800.00",
    "$7,250.00", "$28,900.00", "$4,375.00",
]

# Additional phone numbers beyond vendor contacts (to reach ~12 total)
EXTRA_PHONES = [
    "(555) 432-1098",
    "(555) 654-3210",
]

PAGE_W, PAGE_H = 612, 792  # US Letter


def add_header_footer(page, page_num, total_pages):
    """Add consistent header and footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, 50), pymupdf.Point(558, 50))
    shape.finish(color=(0.2, 0.2, 0.5), width=1.5)
    shape.commit()
    page.insert_text(pymupdf.Point(54, 45), "CONFIDENTIAL - Vendor Contract Compendium",
                     fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(440, 45), "Fiscal Year 2025-2026",
                     fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    # Footer
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(54, 755), pymupdf.Point(558, 755))
    shape2.finish(color=(0.2, 0.2, 0.5), width=0.5)
    shape2.commit()
    page.insert_text(pymupdf.Point(54, 770), "Meridian Holdings Corp.",
                     fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(480, 770), f"Page {page_num} of {total_pages}",
                     fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5))


def create_title_page(doc):
    """Page 1: Title page."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    # Title block
    page.insert_text(pymupdf.Point(130, 250), "VENDOR CONTRACT", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(165, 285), "COMPENDIUM", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(195, 330), "Fiscal Year 2025-2026", fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 345), pymupdf.Point(462, 345))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(175, 390), "Prepared by: Procurement Division", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(175, 410), "Meridian Holdings Corp.", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(175, 430), "Date: January 15, 2025", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(175, 450), f"Main Office: {EXTRA_PHONES[0]}", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(175, 470), f"Total Contract Value: {AMOUNTS[0]}", fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    add_header_footer(page, 1, 20)
    return page


def create_toc_page(doc):
    """Page 2: Table of Contents."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(54, 90), "TABLE OF CONTENTS", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    y = 130
    for i, v in enumerate(VENDORS):
        page.insert_text(pymupdf.Point(72, y), f"{i+1}. {v['name']}", fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(430, y), f"...... Page {i*2 + 3}", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 22
    y += 20
    page.insert_text(pymupdf.Point(72, y), "For procurement inquiries, contact:", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 16
    page.insert_text(pymupdf.Point(72, y), f"Procurement Hotline: {EXTRA_PHONES[1]}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    add_header_footer(page, 2, 20)
    return page


def create_vendor_pages(doc, vendor_idx):
    """Create 2 pages per vendor (vendor agreement + financial terms)."""
    v = VENDORS[vendor_idx]
    page_start = vendor_idx * 2 + 3
    amt_start = vendor_idx * 2 if vendor_idx * 2 < len(AMOUNTS) else vendor_idx % len(AMOUNTS)

    # --- Page A: Vendor Agreement ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 80
    page.insert_text(pymupdf.Point(54, y), f"VENDOR AGREEMENT: {v['name'].upper()}", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 10
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, y), pymupdf.Point(558, y))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    y += 20

    page.insert_text(pymupdf.Point(54, y), "Section 1: Vendor Information", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    info_lines = [
        f"Company Name: {v['name']}",
        f"Primary Contact: {v['contact']}",
        f"Contact Phone: {v['phone']}",
        f"Business Address: {v['address']}",
        f"Services Provided: {v['services']}",
        f"Vendor Registration ID: VR-2025-{1000 + vendor_idx * 111}",
    ]
    for line in info_lines:
        page.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 12
    page.insert_text(pymupdf.Point(54, y), "Section 2: Agreement Terms", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20

    terms_text = (
        f"This Vendor Agreement (\"Agreement\") is entered into as of January 15, 2025, "
        f"by and between Meridian Holdings Corp. (\"Client\") and {v['name']} (\"Vendor\"). "
        f"The Vendor agrees to provide the services described herein for a base annual fee of "
        f"{AMOUNTS[amt_start % len(AMOUNTS)]}. The initial term of this Agreement shall be "
        f"twelve (12) months commencing on February 1, 2025. Either party may terminate this "
        f"Agreement with thirty (30) days written notice. Early termination fees of "
        f"{AMOUNTS[(amt_start + 1) % len(AMOUNTS)]} may apply as outlined in Appendix B."
    )
    rect = pymupdf.Rect(72, y, 545, y + 120)
    page.insert_textbox(rect, terms_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 130

    page.insert_text(pymupdf.Point(54, y), "Section 3: Performance Standards", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    perf_text = (
        f"The Vendor shall maintain a minimum service level agreement (SLA) uptime of 99.5%. "
        f"Failure to meet this threshold will result in a penalty of {AMOUNTS[(amt_start + 2) % len(AMOUNTS)]} per incident. "
        f"All service requests shall be acknowledged within 4 business hours. "
        f"For urgent matters outside business hours, the Vendor's emergency line at {v['phone']} "
        f"shall be available 24/7."
    )
    rect2 = pymupdf.Rect(72, y, 545, y + 90)
    page.insert_textbox(rect2, perf_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    add_header_footer(page, page_start, 20)

    # --- Page B: Financial Terms ---
    page2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 80
    page2.insert_text(pymupdf.Point(54, y), f"FINANCIAL TERMS: {v['name'].upper()}", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 10
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(54, y), pymupdf.Point(558, y))
    shape2.finish(color=(0.1, 0.1, 0.4), width=1)
    shape2.commit()
    y += 20

    page2.insert_text(pymupdf.Point(54, y), "Section 4: Payment Schedule", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20

    # Use different amounts for different vendors to spread them across pages
    a1 = AMOUNTS[(amt_start + 3) % len(AMOUNTS)]
    a2 = AMOUNTS[(amt_start + 4) % len(AMOUNTS)]

    payment_text = (
        f"Payment shall be made in quarterly installments. The quarterly fee is {a1}, "
        f"due on the first business day of each quarter. Late payments shall incur a "
        f"1.5% monthly interest charge. An additional setup and onboarding fee of {a2} "
        f"is due upon execution of this Agreement."
    )
    rect3 = pymupdf.Rect(72, y, 545, y + 80)
    page2.insert_textbox(rect3, payment_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 95

    page2.insert_text(pymupdf.Point(54, y), "Section 5: Insurance & Liability", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    insurance_text = (
        f"The Vendor shall maintain commercial general liability insurance with minimum "
        f"coverage of {AMOUNTS[(amt_start + 5) % len(AMOUNTS)]} per occurrence. "
        f"Certificates of insurance must be provided within 10 business days of Agreement execution. "
        f"The Vendor's insurance coordinator can be reached at {v['phone']}."
    )
    rect4 = pymupdf.Rect(72, y, 545, y + 75)
    page2.insert_textbox(rect4, insurance_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 90

    page2.insert_text(pymupdf.Point(54, y), "Section 6: Authorized Signatories", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 25
    page2.insert_text(pymupdf.Point(72, y), "For Meridian Holdings Corp.:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 18
    page2.insert_text(pymupdf.Point(72, y), "Name: Eleanor Whitfield, VP of Procurement", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page2.insert_text(pymupdf.Point(72, y), "Signature: _______________________________  Date: __________", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 28
    page2.insert_text(pymupdf.Point(72, y), f"For {v['name']}:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 18
    page2.insert_text(pymupdf.Point(72, y), f"Name: {v['contact']}, Account Manager", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page2.insert_text(pymupdf.Point(72, y), "Signature: _______________________________  Date: __________", fontsize=10, fontname="helv", color=(0, 0, 0))

    add_header_footer(page2, page_start + 1, 20)


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page 1: Title
    create_title_page(doc)

    # Page 2: Table of Contents
    create_toc_page(doc)

    # Pages 3-20: 10 vendors x 2 pages each = 20 pages total (but we have pages 1-2 already)
    # We need 18 more pages for 10 vendors = 20 pages total? 2 + 10*2 = 22. Let's use 9 vendors for 2 pages each.
    # Actually: 2 intro pages + 9 vendors * 2 pages = 20 pages. Use first 9 vendors.
    for i in range(9):
        create_vendor_pages(doc, i)

    # Verify page count
    assert doc.page_count == 20, f"Expected 20 pages, got {doc.page_count}"

    # Set TOC
    toc = [
        [1, "Title Page", 1],
        [1, "Table of Contents", 2],
    ]
    for i in range(9):
        toc.append([1, f"Vendor Agreement: {VENDORS[i]['name']}", i * 2 + 3])
        toc.append([2, f"Financial Terms: {VENDORS[i]['name']}", i * 2 + 4])
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Vendor Contract Compendium - Fiscal Year 2025-2026",
        "author": "Meridian Holdings Corp. - Procurement Division",
        "subject": "Vendor Agreements and Financial Terms",
        "keywords": "vendor, contracts, procurement, agreements",
        "creator": "Meridian Procurement System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify content
    doc = pymupdf.open(OUTPUT)
    all_text = ""
    for page in doc:
        all_text += page.get_text("text")
    doc.close()

    import re
    phone_matches = re.findall(r'\(\d{3}\) \d{3}-\d{4}', all_text)
    dollar_matches = re.findall(r'\$[\d,]+\.\d{2}', all_text)
    print(f"Phone numbers found: {len(phone_matches)}")
    print(f"Dollar amounts found: {len(dollar_matches)}")
    print(f"Phone numbers: {phone_matches}")
    print(f"Dollar amounts: {dollar_matches}")

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
