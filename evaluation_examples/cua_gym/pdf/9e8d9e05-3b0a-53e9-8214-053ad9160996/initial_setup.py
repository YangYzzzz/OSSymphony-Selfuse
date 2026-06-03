"""
Initial Setup: Create 8 scanned PDFs (image-only, no text layer) in /home/user/scans/batch/
Task ID: pdf_gf2_047
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_047'
BATCH_DIR = f'{WORKDIR}/scans/batch'

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

# Install dependencies on VM
subprocess.run(['pip3', 'install', 'PyMuPDF', 'Pillow', 'pytesseract'],
               capture_output=True, timeout=120)
# Install tesseract binary (needed by agent for OCR task)
subprocess.run('echo "password" | sudo -S apt-get install -y -qq tesseract-ocr 2>/dev/null',
               shell=True, capture_output=True, timeout=120)

def create_scan_image(width, height, lines, fontsize=20):
    """Create a PIL image that looks like a scanned document page."""
    from PIL import Image, ImageDraw, ImageFont

    # Create slightly off-white background to simulate scan
    bg_r = random.randint(240, 250)
    bg_g = random.randint(238, 248)
    bg_b = random.randint(235, 245)
    img = Image.new('RGB', (width, height), (bg_r, bg_g, bg_b))
    draw = ImageDraw.Draw(img)

    # Try to use a decent font
    font = None
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, fontsize)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    y_pos = 60
    for line in lines:
        # Slight random offset to simulate scan imperfection
        x_offset = random.randint(-2, 2)
        # Slightly varying text color (dark gray/black) to simulate scan
        c = random.randint(10, 40)
        draw.text((50 + x_offset, y_pos), line, fill=(c, c, c), font=font)
        y_pos += fontsize + random.randint(8, 16)
        if y_pos > height - 80:
            break

    # Add some noise speckles to simulate scan artifacts
    for _ in range(random.randint(20, 60)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        gray = random.randint(150, 200)
        draw.point((x, y), fill=(gray, gray, gray))

    return img


# Document content for 8 different scanned documents
documents = {
    'scan_a': {
        'pages': [
            [
                "MEMORANDUM",
                "",
                "TO: Regional Sales Managers",
                "FROM: Patricia Whitfield, VP Sales",
                "DATE: March 15, 2024",
                "RE: Q1 Revenue Targets Update",
                "",
                "This memo provides an update on our Q1 2024",
                "revenue targets across all regions. The Southeast",
                "division exceeded projections by 12 percent while",
                "the Northwest region fell short by approximately",
                "8 percent due to supply chain disruptions.",
                "",
                "Key performance highlights:",
                "- Total revenue: $4.2M (target: $3.9M)",
                "- New accounts acquired: 47",
                "- Client retention rate: 94.3%",
                "",
                "Please review the attached regional breakdown",
                "and submit your Q2 forecasts by April 5, 2024.",
            ],
            [
                "REGIONAL BREAKDOWN - Q1 2024",
                "",
                "SOUTHEAST REGION",
                "  Revenue: $1,340,000",
                "  Growth: +12.4%",
                "  Key Account: Meridian Healthcare",
                "",
                "NORTHEAST REGION",
                "  Revenue: $1,120,000",
                "  Growth: +6.8%",
                "  Key Account: Atlantic Financial Group",
                "",
                "NORTHWEST REGION",
                "  Revenue: $890,000",
                "  Growth: -8.1%",
                "  Key Account: Pacific Lumber Co",
                "",
                "SOUTHWEST REGION",
                "  Revenue: $850,000",
                "  Growth: +3.2%",
                "  Key Account: Desert Sun Energy",
            ],
        ]
    },
    'scan_b': {
        'pages': [
            [
                "INVOICE #INV-2024-0389",
                "",
                "Greenfield Construction Services LLC",
                "4521 Industrial Boulevard",
                "Portland, OR 97201",
                "",
                "Bill To: Summit Properties Inc",
                "         890 Commerce Drive",
                "         Seattle, WA 98101",
                "",
                "Date: February 28, 2024",
                "Due Date: March 30, 2024",
                "",
                "Description          Qty    Rate     Amount",
                "Foundation Work       1    $45,000   $45,000",
                "Framing (Phase 1)     1    $32,500   $32,500",
                "Electrical Rough-In   1    $18,750   $18,750",
                "Plumbing Installation  1   $22,300   $22,300",
                "",
                "Subtotal:                           $118,550",
                "Tax (8.5%):                          $10,077",
                "TOTAL DUE:                          $128,627",
            ],
        ]
    },
    'scan_c': {
        'pages': [
            [
                "PATIENT DISCHARGE SUMMARY",
                "",
                "Riverside Medical Center",
                "Department of Internal Medicine",
                "",
                "Patient: Eleanor M. Vasquez",
                "MRN: 7842901",
                "Admission Date: January 22, 2024",
                "Discharge Date: January 29, 2024",
                "",
                "DIAGNOSIS:",
                "  Primary: Community-acquired pneumonia",
                "  Secondary: Type 2 diabetes mellitus",
                "",
                "TREATMENT SUMMARY:",
                "  IV antibiotics (Ceftriaxone 1g daily)",
                "  Supplemental oxygen therapy",
                "  Blood glucose monitoring and insulin",
                "  adjustment per endocrinology consult",
            ],
            [
                "DISCHARGE MEDICATIONS:",
                "",
                "1. Amoxicillin 500mg TID x 7 days",
                "2. Metformin 1000mg BID (continue)",
                "3. Lisinopril 10mg daily (continue)",
                "4. Albuterol inhaler PRN",
                "",
                "FOLLOW-UP INSTRUCTIONS:",
                "- PCP visit within 7 days",
                "- Chest X-ray in 4 weeks",
                "- HbA1c in 3 months",
                "",
                "Attending Physician: Dr. James K. Thornton",
                "Resident: Dr. Aisha Patel",
                "",
                "Signed electronically on 01/29/2024",
            ],
            [
                "LABORATORY RESULTS SUMMARY",
                "",
                "Date: January 22, 2024 (Admission)",
                "",
                "CBC:",
                "  WBC: 14.2 x10^3/uL (H)",
                "  RBC: 4.1 x10^6/uL",
                "  Hemoglobin: 12.8 g/dL",
                "  Hematocrit: 38.2%",
                "  Platelets: 245 x10^3/uL",
                "",
                "CHEMISTRY:",
                "  Glucose: 186 mg/dL (H)",
                "  BUN: 22 mg/dL",
                "  Creatinine: 0.9 mg/dL",
                "  Sodium: 139 mEq/L",
                "  Potassium: 4.1 mEq/L",
                "",
                "HbA1c: 7.8% (H)",
            ],
        ]
    },
    'scan_d': {
        'pages': [
            [
                "RENTAL AGREEMENT",
                "",
                "This Residential Lease Agreement is entered",
                "into this 1st day of March 2024 between:",
                "",
                "LANDLORD: Pinnacle Property Management LLC",
                "ADDRESS: 1200 Main Street, Suite 400",
                "         Denver, CO 80202",
                "",
                "TENANT: Robert J. Nakamura",
                "UNIT: Apartment 7B",
                "       3845 Elm Creek Drive",
                "       Denver, CO 80220",
                "",
                "LEASE TERM: 12 months",
                "START DATE: April 1, 2024",
                "END DATE: March 31, 2025",
                "",
                "MONTHLY RENT: $1,850.00",
                "SECURITY DEPOSIT: $1,850.00",
                "PET DEPOSIT: $300.00",
            ],
            [
                "TERMS AND CONDITIONS (continued)",
                "",
                "Section 3: Utilities",
                "Tenant is responsible for electricity, gas,",
                "internet, and cable. Water and trash removal",
                "are included in the monthly rent.",
                "",
                "Section 4: Maintenance",
                "Tenant shall maintain the premises in clean",
                "condition. Landlord is responsible for major",
                "repairs and structural maintenance.",
                "",
                "Section 5: Termination",
                "Either party may terminate with 60 days",
                "written notice. Early termination fee of",
                "two months rent applies.",
                "",
                "Section 6: Pets",
                "One pet under 35 lbs allowed with deposit.",
                "Breed restrictions apply per building policy.",
            ],
            [
                "Section 7: Insurance",
                "Tenant must maintain renters insurance with",
                "minimum liability coverage of $100,000.",
                "",
                "Section 8: Alterations",
                "No structural modifications without written",
                "consent from Landlord. Minor cosmetic changes",
                "permitted with prior approval.",
                "",
                "SIGNATURES:",
                "",
                "Landlord: _________________________",
                "          Pinnacle Property Mgmt LLC",
                "          Date: March 1, 2024",
                "",
                "Tenant:  _________________________",
                "         Robert J. Nakamura",
                "         Date: March 1, 2024",
            ],
            [
                "ADDENDUM A: MOVE-IN INSPECTION CHECKLIST",
                "",
                "Unit 7B - 3845 Elm Creek Drive",
                "Inspection Date: March 28, 2024",
                "",
                "KITCHEN:",
                "  Countertops: Good condition",
                "  Appliances: All functional",
                "  Cabinets: Minor wear on handles",
                "  Floor: Small scratch near island",
                "",
                "LIVING ROOM:",
                "  Walls: Good condition, freshly painted",
                "  Carpet: Professional cleaned",
                "  Windows: All operational",
                "",
                "BEDROOM:",
                "  Closet doors: Track slightly bent",
                "  Ceiling fan: Operational",
                "  Walls: Good condition",
                "",
                "Inspector: Maria Gonzalez",
            ],
        ]
    },
    'scan_e': {
        'pages': [
            [
                "RESEARCH ABSTRACT",
                "",
                "Title: Effects of Urban Green Spaces on",
                "Air Quality in Metropolitan Areas",
                "",
                "Authors: Dr. Liang Chen, Dr. Sarah Mitchell,",
                "         Prof. Henrik Johansson",
                "Institution: University of California, Davis",
                "Published: Environmental Science Journal, 2024",
                "",
                "Abstract:",
                "This study examines the relationship between",
                "urban green space coverage and particulate",
                "matter concentrations across 45 metropolitan",
                "areas in the United States. Using satellite",
                "imagery and EPA monitoring data from 2019 to",
                "2023, we developed regression models showing",
                "a significant inverse correlation between",
                "tree canopy coverage and PM2.5 levels.",
                "Results suggest that a 10 percent increase in",
                "green space reduces PM2.5 by 2.3 ug/m3.",
            ],
            [
                "METHODOLOGY",
                "",
                "Data Sources:",
                "- MODIS satellite imagery (NASA)",
                "- EPA Air Quality System (AQS) database",
                "- US Census Bureau urban boundary data",
                "",
                "Statistical Methods:",
                "- Multivariate linear regression",
                "- Geographically weighted regression (GWR)",
                "- Spatial autocorrelation analysis",
                "",
                "Study Period: January 2019 - December 2023",
                "Sample Size: 45 metropolitan statistical areas",
                "",
                "Control Variables:",
                "- Population density",
                "- Industrial emissions index",
                "- Transportation infrastructure density",
                "- Seasonal temperature variations",
                "- Wind speed and precipitation patterns",
            ],
        ]
    },
    'scan_f': {
        'pages': [
            [
                "MEETING MINUTES",
                "",
                "Board of Directors Meeting",
                "Cascade Valley Water District",
                "Date: March 12, 2024",
                "Location: District Office, Conference Room A",
                "",
                "ATTENDEES:",
                "  Chair: Dorothy Flanagan",
                "  Vice Chair: Thomas Reeves",
                "  Directors: Maria Santos, Kevin Park,",
                "             William Okafor",
                "  General Manager: Richard Huang",
                "  District Counsel: Pamela Frost, Esq.",
                "",
                "Meeting called to order at 6:02 PM",
                "",
                "AGENDA ITEM 1: Approval of Minutes",
                "Motion to approve Feb 2024 minutes by",
                "Director Santos, seconded by Director Park.",
                "APPROVED unanimously (5-0).",
            ],
        ]
    },
    'scan_g': {
        'pages': [
            [
                "PRODUCT SPECIFICATION SHEET",
                "",
                "Product: ThermoGuard Pro 5000",
                "Category: Industrial Temperature Controller",
                "Manufacturer: Apex Controls International",
                "Part Number: TGP-5000-A1",
                "",
                "ELECTRICAL SPECIFICATIONS:",
                "  Input Voltage: 100-240 VAC, 50/60 Hz",
                "  Power Consumption: 45W max",
                "  Control Output: 4-20mA / 0-10VDC",
                "  Relay Output: 2x SPDT, 5A 250VAC",
                "",
                "TEMPERATURE RANGE:",
                "  Measurement: -200C to +1800C",
                "  Accuracy: +/- 0.1C",
                "  Response Time: < 100ms",
                "",
                "PHYSICAL:",
                "  Dimensions: 96 x 96 x 110 mm (DIN)",
                "  Weight: 0.45 kg",
                "  Protection: IP65 front panel",
            ],
            [
                "COMMUNICATION INTERFACES:",
                "  RS-485 Modbus RTU",
                "  Ethernet (optional module)",
                "  USB for configuration",
                "",
                "CERTIFICATIONS:",
                "  UL Listed (UL 61010-1)",
                "  CE Marked",
                "  CSA Approved",
                "  RoHS Compliant",
                "",
                "ORDERING INFORMATION:",
                "  TGP-5000-A1   Base unit, relay output",
                "  TGP-5000-A2   With analog output",
                "  TGP-5000-A3   With Ethernet module",
                "  TGP-5000-KIT  Mounting kit + manual",
                "",
                "WARRANTY: 3 years parts and labor",
                "LEAD TIME: 2-4 weeks standard",
                "",
                "Apex Controls International",
                "Technical Support: 1-800-555-APEX",
            ],
        ]
    },
    'scan_h': {
        'pages': [
            [
                "TRAVEL ITINERARY",
                "",
                "Prepared for: Jessica and Mark Thompson",
                "Trip: Mediterranean Cruise 2024",
                "Travel Dates: June 8-22, 2024",
                "Booking Ref: MED-2024-77432",
                "",
                "DAY 1 - June 8 (Saturday)",
                "  Flight: AA 4521 Denver to Rome",
                "  Depart: 5:45 PM MDT",
                "  Arrive: 11:30 AM +1 (June 9) CEST",
                "",
                "DAY 2 - June 9 (Sunday)",
                "  Transfer to Civitavecchia Port",
                "  Embarkation: 2:00 PM - 5:00 PM",
                "  Ship: MS Adriatic Jewel, Cabin 8214",
                "  Dinner: 7:30 PM Main Dining Room",
            ],
            [
                "DAY 3 - June 10 (Monday)",
                "  Port: Naples, Italy",
                "  Excursion: Pompeii Guided Tour",
                "  Depart Ship: 8:30 AM",
                "  Return: 2:00 PM",
                "  Evening: Onboard entertainment",
                "",
                "DAY 4 - June 11 (Tuesday)",
                "  At Sea",
                "  Spa appointment: 10:00 AM",
                "  Cooking class: 2:00 PM (Deck 12)",
                "",
                "DAY 5 - June 12 (Wednesday)",
                "  Port: Santorini, Greece",
                "  Excursion: Oia Village Walking Tour",
                "  Free time for shopping in Fira",
                "  Sunset dinner reservation at Ambrosia",
                "",
                "DAY 6 - June 13 (Thursday)",
                "  Port: Mykonos, Greece",
                "  Beach day at Paradise Beach",
                "  Return to ship by 5:00 PM",
            ],
            [
                "DAY 7-8 - June 14-15",
                "  Port: Istanbul, Turkey (overnight)",
                "  Excursion Day 1: Blue Mosque, Hagia Sophia",
                "  Excursion Day 2: Grand Bazaar, Spice Market",
                "  Dinner: Rooftop restaurant (booked)",
                "",
                "DAY 9 - June 16 (Sunday)",
                "  Port: Athens (Piraeus), Greece",
                "  Excursion: Acropolis and Plaka District",
                "  Return by 4:00 PM",
                "",
                "DAY 10-12 - June 17-19",
                "  Ports: Dubrovnik, Split, Venice",
                "  Walking tours booked for each city",
                "",
                "DAY 13 - June 20",
                "  Disembarkation in Barcelona",
                "  Hotel: Hotel Arts Barcelona (2 nights)",
                "",
                "DAY 14-15 - June 21-22",
                "  Free days in Barcelona",
                "  Flight: BA 1498 Barcelona to Denver",
                "  Depart: 6:15 PM CEST (June 22)",
            ],
        ]
    },
}


def create_scanned_pdfs():
    """Create 8 image-only PDFs that simulate scanned documents."""
    import pymupdf
    from PIL import Image, ImageDraw, ImageFont
    import io

    os.makedirs(BATCH_DIR, exist_ok=True)

    for name, doc_info in documents.items():
        pdf_doc = pymupdf.open()

        for page_lines in doc_info['pages']:
            # Create scan image with Pillow
            # Letter size at 150 DPI = 1275 x 1650 pixels
            img = create_scan_image(1275, 1650, page_lines, fontsize=22)

            # Convert PIL image to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            # Create a new page and insert the image as a full-page image
            page = pdf_doc.new_page(width=612, height=792)  # Letter size in points
            page.insert_image(
                pymupdf.Rect(0, 0, 612, 792),
                stream=img_bytes,
            )

        output_path = f'{BATCH_DIR}/{name}.pdf'
        pdf_doc.save(output_path)
        pdf_doc.close()
        print(f'Created: {output_path} ({len(doc_info["pages"])} pages)')

    print(f'\nAll 8 scanned PDFs created in {BATCH_DIR}')

    # Verify no text layer exists
    import pymupdf as fitz
    for name in documents:
        doc = fitz.open(f'{BATCH_DIR}/{name}.pdf')
        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                print(f'WARNING: {name}.pdf page {i} has text layer: "{text[:50]}"')
        doc.close()

    print('Verification: confirmed image-only PDFs (no text layer)')


create_scanned_pdfs()

# Open file manager to show the batch directory
launch_gui(f'nautilus "{BATCH_DIR}"', delay_sec=2.0)
print('GUI_READY: launched file manager with DISPLAY=:0')
