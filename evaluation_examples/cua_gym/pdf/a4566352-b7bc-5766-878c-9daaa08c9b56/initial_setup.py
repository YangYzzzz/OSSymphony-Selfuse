"""
Initial Setup: Build a document classification pipeline
Task ID: pdf_gf3_036
Domain: pdf

Creates 30 PDFs of mixed types (invoice, contract, report, receipt) in /home/user/classify/
with subdirectories for each type. No classifier script or classifications.json yet.
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_036'
CLASSIFY_DIR = f'{WORKDIR}/classify'
SCRIPTS_DIR = f'{WORKDIR}/scripts'

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


def create_invoice_pdf(filepath, inv_num, vendor, items, total, date_str):
    """Create a realistic invoice PDF (1-2 pages)."""
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)

    # Header
    page.insert_text(pymupdf.Point(72, 50), vendor, fontsize=18, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 75), f"INVOICE #{inv_num}", fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 95), f"Date: {date_str}", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 110), f"Payment Terms: Net 30", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 125), f"Amount Due: ${total:,.2f}", fontsize=12, fontname="hebo", color=(0.8, 0, 0))

    # Bill To section
    page.insert_text(pymupdf.Point(72, 160), "Bill To:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 175), "Meridian Corp", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 190), "1200 Market Street, Suite 400", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 205), "San Francisco, CA 94103", fontsize=10, fontname="helv")

    # Line separator
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 225), pymupdf.Point(540, 225))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    # Table header
    y = 245
    page.insert_text(pymupdf.Point(72, y), "Item", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(280, y), "Qty", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(350, y), "Unit Price", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(460, y), "Amount", fontsize=10, fontname="hebo")

    y += 20
    for item_name, qty, price in items:
        page.insert_text(pymupdf.Point(72, y), item_name, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(280, y), str(qty), fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(350, y), f"${price:,.2f}", fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(460, y), f"${qty * price:,.2f}", fontsize=9, fontname="helv")
        y += 18

    # Total line
    y += 10
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(350, y), pymupdf.Point(540, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    y += 15
    page.insert_text(pymupdf.Point(350, y), "Total:", fontsize=11, fontname="hebo")
    page.insert_text(pymupdf.Point(460, y), f"${total:,.2f}", fontsize=11, fontname="hebo")

    # Payment instructions
    y += 40
    page.insert_text(pymupdf.Point(72, y), "Payment Instructions:", fontsize=10, fontname="hebo")
    y += 15
    page.insert_text(pymupdf.Point(72, y), "Please remit payment within 30 days.", fontsize=9, fontname="helv")
    y += 15
    page.insert_text(pymupdf.Point(72, y), "Bank: First National Bank | Account: 8827-4451-0093", fontsize=9, fontname="helv")

    doc.save(filepath)
    doc.close()


def create_contract_pdf(filepath, title, parties, date_str, num_pages):
    """Create a realistic contract PDF (5+ pages)."""
    import pymupdf
    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(150, 200), title, fontsize=22, fontname="hebo", color=(0, 0, 0.4))
    page.insert_text(pymupdf.Point(150, 240), f"Effective Date: {date_str}", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(150, 270), f"Between: {parties[0]}", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(150, 290), f"And: {parties[1]}", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(150, 330), "CONFIDENTIAL", fontsize=14, fontname="hebo", color=(0.7, 0, 0))

    # Contract body pages
    sections = [
        ("1. DEFINITIONS AND INTERPRETATION",
         "In this Agreement, unless the context otherwise requires, the following terms shall have "
         "the meanings set forth below. 'Agreement' means this contract including all schedules and "
         "amendments. 'Effective Date' means the date first written above. 'Services' means the "
         "professional services described in Schedule A. 'Confidential Information' means any "
         "proprietary data, trade secrets, or business information disclosed by either party. "
         "The obligations under this section shall survive termination of the agreement for a "
         "period of five (5) years."),
        ("2. SCOPE OF SERVICES",
         "The Service Provider agrees to perform the services described in Schedule A attached "
         "hereto and incorporated by reference. The scope includes but is not limited to consulting, "
         "technical implementation, training, and ongoing support. All deliverables shall meet the "
         "quality standards specified in Section 4. Any changes to the scope of services must be "
         "agreed upon in writing by both parties through a formal change order process."),
        ("3. TERM AND TERMINATION",
         "This Agreement shall commence on the Effective Date and continue for a period of "
         "twenty-four (24) months unless terminated earlier in accordance with this section. "
         "Either party may terminate this Agreement for cause upon thirty (30) days written notice "
         "if the other party materially breaches any obligation hereunder and fails to cure such "
         "breach within the notice period. Upon termination, all outstanding invoices become "
         "immediately due and payable."),
        ("4. COMPENSATION AND PAYMENT",
         "Client agrees to pay Service Provider the fees set forth in Schedule B. Payment shall "
         "be due within thirty (30) days of receipt of invoice. Late payments shall accrue interest "
         "at the rate of 1.5% per month. All fees are exclusive of applicable taxes. Service Provider "
         "shall submit monthly invoices detailing the services performed and hours expended."),
        ("5. INTELLECTUAL PROPERTY",
         "All intellectual property developed under this Agreement shall be owned by the Client upon "
         "full payment. Service Provider retains rights to pre-existing materials and general "
         "know-how. Each party grants the other a limited license to use its trademarks solely "
         "for the purpose of performing obligations under this Agreement."),
        ("6. CONFIDENTIALITY",
         "Each party agrees to maintain the confidentiality of all Confidential Information "
         "received from the other party. Confidential Information shall not be disclosed to any "
         "third party without the prior written consent of the disclosing party. This obligation "
         "shall not apply to information that is publicly available, independently developed, or "
         "required to be disclosed by law or regulation."),
        ("7. LIABILITY AND INDEMNIFICATION",
         "Neither party shall be liable for any indirect, incidental, special, or consequential "
         "damages arising out of this Agreement. The total aggregate liability of either party "
         "shall not exceed the total fees paid or payable under this Agreement in the twelve (12) "
         "months preceding the claim. Each party agrees to indemnify and hold harmless the other "
         "party from any claims arising from its negligence or willful misconduct."),
        ("8. GOVERNING LAW AND DISPUTE RESOLUTION",
         "This Agreement shall be governed by and construed in accordance with the laws of the "
         "State of Delaware, without regard to its conflict of laws principles. Any disputes arising "
         "under this Agreement shall first be submitted to mediation. If mediation fails, disputes "
         "shall be resolved by binding arbitration in accordance with the rules of the American "
         "Arbitration Association."),
    ]

    section_idx = 0
    for pg in range(num_pages - 1):
        page = doc.new_page(width=612, height=792)
        y = 72
        page.insert_text(pymupdf.Point(72, y), f"Page {pg + 2}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
        y += 30
        # Add 2 sections per page
        for _ in range(2):
            if section_idx < len(sections):
                heading, body = sections[section_idx]
                page.insert_text(pymupdf.Point(72, y), heading, fontsize=12, fontname="hebo")
                y += 20
                rect = pymupdf.Rect(72, y, 540, y + 200)
                page.insert_textbox(rect, body, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y += 220
                section_idx += 1

    doc.save(filepath)
    doc.close()


def create_report_pdf(filepath, title, dept, date_str, num_pages):
    """Create a realistic report PDF (3-6 pages)."""
    import pymupdf
    doc = pymupdf.open()

    # Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(100, 250), title, fontsize=24, fontname="hebo", color=(0, 0.2, 0.5))
    page.insert_text(pymupdf.Point(100, 290), f"Department: {dept}", fontsize=14, fontname="helv")
    page.insert_text(pymupdf.Point(100, 315), f"Report Date: {date_str}", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(100, 340), "Classification: Internal Use Only", fontsize=10, fontname="heit", color=(0.5, 0.5, 0.5))

    report_sections = [
        ("Executive Summary",
         "This report presents an analysis of key performance indicators and operational metrics "
         "for the current reporting period. Overall performance has shown improvement across most "
         "dimensions, with notable gains in efficiency and customer satisfaction. The data suggests "
         "continued positive trends with some areas requiring attention and further investment."),
        ("Methodology",
         "Data was collected from multiple internal systems including the CRM platform, financial "
         "reporting tools, and operational dashboards. Statistical analysis was performed using "
         "standard regression models and time-series decomposition. Survey data was collected from "
         "a representative sample of 450 respondents with a 95% confidence interval."),
        ("Key Findings",
         "Revenue increased by 12.3% year-over-year, driven primarily by expansion in the "
         "enterprise segment. Customer acquisition costs decreased by 8.7% due to improved "
         "targeting algorithms. Employee productivity metrics showed a 15% improvement following "
         "the implementation of new workflow automation tools. Net Promoter Score rose from 42 to 58."),
        ("Financial Analysis",
         "Total revenue for the period was $14.2 million, against a target of $13.8 million. "
         "Operating expenses were $9.1 million, resulting in an operating margin of 35.9%. "
         "Capital expenditure totaled $2.3 million, primarily allocated to infrastructure upgrades "
         "and technology investments. Cash flow from operations was positive at $4.8 million."),
        ("Recommendations",
         "Based on the findings, we recommend: (1) Increase investment in digital marketing by "
         "20% to capitalize on the lower customer acquisition costs; (2) Expand the automation "
         "initiative to additional departments; (3) Establish a dedicated customer success team "
         "to maintain and improve the NPS trajectory; (4) Conduct a detailed review of underperforming "
         "product lines with a view to rationalization."),
        ("Appendix: Data Tables",
         "Detailed quarterly breakdowns, regional performance comparisons, and full survey results "
         "are available in the supplementary data package. All figures in this report are subject "
         "to standard rounding conventions and may not sum to totals."),
    ]

    sec_idx = 0
    for pg in range(num_pages - 1):
        page = doc.new_page(width=612, height=792)
        y = 72
        for _ in range(2):
            if sec_idx < len(report_sections):
                heading, body = report_sections[sec_idx]
                page.insert_text(pymupdf.Point(72, y), heading, fontsize=14, fontname="hebo", color=(0, 0.2, 0.5))
                y += 25
                rect = pymupdf.Rect(72, y, 540, y + 200)
                page.insert_textbox(rect, body, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y += 220
                sec_idx += 1

    doc.save(filepath)
    doc.close()


def create_receipt_pdf(filepath, store, items, total, date_str, receipt_num):
    """Create a realistic receipt PDF (1 page, small format)."""
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page(width=300, height=500)  # Smaller receipt format

    y = 30
    page.insert_text(pymupdf.Point(50, y), store, fontsize=12, fontname="hebo")
    y += 18
    page.insert_text(pymupdf.Point(50, y), f"Receipt #{receipt_num}", fontsize=8, fontname="helv")
    y += 14
    page.insert_text(pymupdf.Point(50, y), f"Date: {date_str}", fontsize=8, fontname="helv")
    y += 14
    page.insert_text(pymupdf.Point(50, y), "----------------------------", fontsize=8, fontname="cour")
    y += 14

    for item_name, price in items:
        page.insert_text(pymupdf.Point(50, y), item_name, fontsize=8, fontname="helv")
        page.insert_text(pymupdf.Point(220, y), f"${price:.2f}", fontsize=8, fontname="helv")
        y += 14

    y += 5
    page.insert_text(pymupdf.Point(50, y), "----------------------------", fontsize=8, fontname="cour")
    y += 14
    tax = round(total * 0.0875, 2)
    page.insert_text(pymupdf.Point(50, y), "Subtotal:", fontsize=8, fontname="helv")
    page.insert_text(pymupdf.Point(220, y), f"${total:.2f}", fontsize=8, fontname="helv")
    y += 14
    page.insert_text(pymupdf.Point(50, y), "Tax (8.75%):", fontsize=8, fontname="helv")
    page.insert_text(pymupdf.Point(220, y), f"${tax:.2f}", fontsize=8, fontname="helv")
    y += 14
    page.insert_text(pymupdf.Point(50, y), "TOTAL:", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(220, y), f"${total + tax:.2f}", fontsize=9, fontname="hebo")
    y += 20
    page.insert_text(pymupdf.Point(50, y), "Payment: Visa ***4821", fontsize=8, fontname="helv")
    y += 14
    page.insert_text(pymupdf.Point(50, y), "Thank you for your purchase!", fontsize=8, fontname="heit")

    doc.save(filepath)
    doc.close()


def create_initial():
    # Create directories
    os.makedirs(CLASSIFY_DIR, exist_ok=True)
    os.makedirs(f'{CLASSIFY_DIR}/invoices', exist_ok=True)
    os.makedirs(f'{CLASSIFY_DIR}/contracts', exist_ok=True)
    os.makedirs(f'{CLASSIFY_DIR}/reports', exist_ok=True)
    os.makedirs(f'{CLASSIFY_DIR}/receipts', exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # --- INVOICES (8 files) ---
    invoices = [
        ("inv_techsupply_2024.pdf", "INV-2024-0871", "TechSupply Solutions Inc.",
         [("Dell Latitude 5540 Laptop", 5, 1249.00), ("USB-C Docking Station", 5, 189.99), ("Wireless Mouse Kit", 10, 34.95)],
         7974.45, "2024-11-15"),
        ("inv_cloudservices_q4.pdf", "INV-2024-1102", "CloudBridge Services LLC",
         [("Enterprise Cloud Hosting (Monthly)", 3, 2500.00), ("API Gateway License", 1, 890.00), ("Support Package Premium", 1, 450.00)],
         8840.00, "2024-12-01"),
        ("inv_officesupply_nov.pdf", "INV-78432", "National Office Products",
         [("A4 Copy Paper (Case)", 20, 42.50), ("Toner Cartridge HP 26A", 8, 78.90), ("Stapler Heavy Duty", 3, 24.99)],
         1556.17, "2024-11-20"),
        ("inv_consulting_strategic.pdf", "INV-SC-0045", "Pinnacle Strategy Group",
         [("Strategic Consulting Hours", 40, 275.00), ("Market Research Report", 1, 3500.00), ("Presentation Materials", 1, 750.00)],
         15250.00, "2024-10-31"),
        ("inv_maintenance_annual.pdf", "INV-2024-MAI-003", "BuildRight Facilities Inc.",
         [("HVAC Quarterly Service", 4, 850.00), ("Fire Safety Inspection", 1, 1200.00), ("Elevator Maintenance", 4, 625.00)],
         5900.00, "2024-09-15"),
        ("inv_marketing_digital.pdf", "INV-DM-2024-089", "PixelWave Digital Agency",
         [("SEO Campaign (Monthly)", 3, 1800.00), ("Social Media Management", 3, 1200.00), ("PPC Ad Spend", 1, 5000.00)],
         14000.00, "2024-11-30"),
        ("inv_catering_event.pdf", "INV-CAT-4421", "Gourmet Events Catering Co.",
         [("Corporate Lunch Package (50 pax)", 1, 1250.00), ("Beverage Service", 1, 375.00), ("Setup & Cleanup", 1, 200.00)],
         1825.00, "2024-12-05"),
        ("inv_software_licenses.pdf", "INV-SL-20241108", "CodeForge Software Ltd.",
         [("IDE Pro License (Annual)", 15, 299.00), ("CI/CD Pipeline License", 1, 2400.00), ("Code Review Tool", 10, 120.00)],
         8085.00, "2024-11-08"),
    ]

    for fname, inv_num, vendor, items, total, date_str in invoices:
        create_invoice_pdf(f'{CLASSIFY_DIR}/{fname}', inv_num, vendor, items, total, date_str)

    # --- CONTRACTS (7 files) ---
    contracts = [
        ("contract_saas_agreement.pdf", "SaaS Service Agreement", ("Meridian Corp", "CloudBridge Services LLC"), "2024-01-15", 7),
        ("contract_nda_bilateral.pdf", "Bilateral Non-Disclosure Agreement", ("Meridian Corp", "Pinnacle Strategy Group"), "2024-03-01", 5),
        ("contract_employment_senior.pdf", "Senior Engineer Employment Contract", ("Meridian Corp", "Alexandra Petrov"), "2024-06-15", 8),
        ("contract_lease_office.pdf", "Commercial Office Lease Agreement", ("Meridian Corp", "Westfield Properties LLC"), "2024-02-01", 10),
        ("contract_vendor_master.pdf", "Master Vendor Services Agreement", ("Meridian Corp", "National Office Products"), "2024-04-10", 6),
        ("contract_partnership_jv.pdf", "Joint Venture Partnership Agreement", ("Meridian Corp", "Apex Innovations Ltd."), "2024-07-22", 9),
        ("contract_maintenance_sla.pdf", "Service Level Agreement - IT Maintenance", ("Meridian Corp", "TechSupply Solutions Inc."), "2024-05-01", 6),
    ]

    for fname, title, parties, date_str, pages in contracts:
        create_contract_pdf(f'{CLASSIFY_DIR}/{fname}', title, parties, date_str, pages)

    # --- REPORTS (8 files) ---
    reports = [
        ("report_q3_financial.pdf", "Q3 2024 Financial Performance Report", "Finance", "2024-10-15", 5),
        ("report_market_analysis.pdf", "Market Analysis: Enterprise SaaS Trends 2024", "Strategy", "2024-09-20", 4),
        ("report_employee_engagement.pdf", "Annual Employee Engagement Survey Results", "Human Resources", "2024-08-30", 6),
        ("report_cybersecurity_audit.pdf", "Information Security Audit Report", "IT Security", "2024-11-01", 5),
        ("report_sustainability_esg.pdf", "ESG & Sustainability Progress Report", "Corporate Affairs", "2024-07-15", 4),
        ("report_product_roadmap.pdf", "Product Roadmap Review - H2 2024", "Product Management", "2024-06-28", 3),
        ("report_customer_satisfaction.pdf", "Customer Satisfaction Analysis Report", "Customer Success", "2024-10-05", 5),
        ("report_operational_efficiency.pdf", "Operational Efficiency Improvement Report", "Operations", "2024-11-12", 4),
    ]

    for fname, title, dept, date_str, pages in reports:
        create_report_pdf(f'{CLASSIFY_DIR}/{fname}', title, dept, date_str, pages)

    # --- RECEIPTS (7 files) ---
    receipts = [
        ("receipt_staples_office.pdf", "Staples Office Supply",
         [("Ballpoint Pens (12pk)", 4.99), ("Sticky Notes 3x3", 3.49), ("File Folders (50pk)", 12.99), ("Binder Clips Lg", 5.79)],
         27.26, "2024-11-18", "R-884210"),
        ("receipt_amazon_tech.pdf", "Amazon.com",
         [("USB-C Cable 6ft", 12.99), ("Webcam 1080p", 49.99), ("Mouse Pad XL", 15.99)],
         78.97, "2024-11-22", "113-4928571"),
        ("receipt_uber_ride.pdf", "Uber Technologies",
         [("UberX: Downtown to Airport", 34.50), ("Toll Fee", 2.75)],
         37.25, "2024-12-01", "UBER-9X8K2"),
        ("receipt_lunch_meeting.pdf", "The Capital Grille",
         [("Dry-Aged Steak", 52.00), ("Caesar Salad", 16.00), ("Sparkling Water", 8.00), ("Espresso x2", 12.00)],
         88.00, "2024-11-25", "TBL-3847"),
        ("receipt_parking_monthly.pdf", "CityPark Garage",
         [("Monthly Parking Pass - December 2024", 285.00)],
         285.00, "2024-12-01", "PKG-20241201"),
        ("receipt_fedex_shipping.pdf", "FedEx Office",
         [("Priority Overnight (5 lbs)", 45.80), ("Packaging Supplies", 3.25)],
         49.05, "2024-11-28", "FX-770842199"),
        ("receipt_hotel_travel.pdf", "Marriott Downtown",
         [("Standard Room (2 nights)", 358.00), ("Room Service", 42.50), ("Parking", 30.00)],
         430.50, "2024-11-14", "CONF-8827441"),
    ]

    for fname, store, items, total, date_str, rnum in receipts:
        create_receipt_pdf(f'{CLASSIFY_DIR}/{fname}', store, items, total, date_str, rnum)

    # Verify count
    pdfs = [f for f in os.listdir(CLASSIFY_DIR) if f.endswith('.pdf')]
    print(f'Created {len(pdfs)} PDFs in {CLASSIFY_DIR}')
    for f in sorted(pdfs):
        print(f'  {f}')

    # Verify subdirectories are empty
    for subdir in ['invoices', 'contracts', 'reports', 'receipts']:
        contents = os.listdir(f'{CLASSIFY_DIR}/{subdir}')
        print(f'  {subdir}/: {len(contents)} files (should be 0)')

    print(f'Scripts dir exists: {os.path.isdir(SCRIPTS_DIR)}')

    # Open file manager showing classify directory
    launch_gui(f'nautilus "{CLASSIFY_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
