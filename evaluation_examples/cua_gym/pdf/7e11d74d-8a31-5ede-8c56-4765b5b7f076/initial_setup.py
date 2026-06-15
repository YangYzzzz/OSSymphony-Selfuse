"""
Initial Setup: Create a 10-page scanned document with pages needing rotation correction.
Task ID: pdf_gf2_018
Domain: pdf

Pages 1-4: portrait content that should be landscape (agent must rotate 90 CW)
Pages 5-6: upside-down content (agent must rotate 180)
Pages 7-10: correctly oriented (no rotation needed)
All pages start at rotation 0.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_018'
SCANS_DIR = f'{WORKDIR}/scans'
OUTPUT = f'{SCANS_DIR}/mixed_scan.pdf'


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
    os.makedirs(SCANS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Pages 1-4: Portrait pages (scanned wrong orientation) ---
    # These contain landscape-oriented content but were scanned in portrait.
    # The agent should rotate them 90 degrees clockwise.
    page_contents_1_4 = [
        {
            "title": "Q1 2025 Revenue Dashboard",
            "body": (
                "Region        | Jan      | Feb      | Mar      | Total\n"
                "North America | $142,300 | $158,700 | $167,200 | $468,200\n"
                "Europe        | $98,500  | $105,200 | $112,800 | $316,500\n"
                "Asia Pacific  | $76,400  | $82,100  | $89,300  | $247,800\n"
                "Latin America | $34,200  | $37,800  | $41,500  | $113,500\n"
                "---------------------------------------------------\n"
                "Total         | $351,400 | $383,800 | $410,800 | $1,146,000"
            ),
        },
        {
            "title": "Q2 2025 Revenue Dashboard",
            "body": (
                "Region        | Apr      | May      | Jun      | Total\n"
                "North America | $171,500 | $179,300 | $185,600 | $536,400\n"
                "Europe        | $118,400 | $124,700 | $130,200 | $373,300\n"
                "Asia Pacific  | $93,800  | $98,200  | $104,500 | $296,500\n"
                "Latin America | $44,100  | $47,600  | $51,200  | $142,900\n"
                "---------------------------------------------------\n"
                "Total         | $427,800 | $449,800 | $471,500 | $1,349,100"
            ),
        },
        {
            "title": "Employee Headcount by Department",
            "body": (
                "Department     | Full-Time | Part-Time | Contractors | Total\n"
                "Engineering    | 245       | 18        | 42          | 305\n"
                "Product        | 67        | 5         | 12          | 84\n"
                "Marketing      | 89        | 22        | 31          | 142\n"
                "Sales          | 156       | 14        | 28          | 198\n"
                "Operations     | 112       | 35        | 19          | 166\n"
                "HR & Admin     | 43        | 8         | 6           | 57\n"
                "---------------------------------------------------\n"
                "Company Total  | 712       | 102       | 138         | 952"
            ),
        },
        {
            "title": "Infrastructure Cost Breakdown - March 2025",
            "body": (
                "Service          | Monthly Cost | YoY Change | Budget Var\n"
                "Cloud Compute    | $287,450     | +12.3%     | -2.1%\n"
                "Database Storage | $94,200      | +8.7%      | +1.4%\n"
                "CDN & Network    | $56,800      | +15.1%     | -5.3%\n"
                "Monitoring       | $18,300      | -3.2%      | +0.8%\n"
                "Security Tools   | $42,700      | +22.5%     | -8.7%\n"
                "CI/CD Pipeline   | $23,100      | +6.8%      | +2.1%\n"
                "---------------------------------------------------\n"
                "Total            | $522,550     | +11.4%     | -2.8%"
            ),
        },
    ]

    for i, content in enumerate(page_contents_1_4):
        # A4 portrait page
        page = doc.new_page(width=595, height=842)
        page.insert_text(
            pymupdf.Point(72, 60),
            content["title"],
            fontsize=16,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        page.insert_text(
            pymupdf.Point(72, 80),
            f"Page {i + 1} of 10 — Scanned Document",
            fontsize=9,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )
        # Draw separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 88), pymupdf.Point(523, 88))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        rect = pymupdf.Rect(72, 100, 523, 780)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=10,
            fontname="cour",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # --- Pages 5-6: Upside-down pages (need 180 rotation) ---
    page_contents_5_6 = [
        {
            "title": "Meeting Minutes — Board of Directors",
            "body": (
                "Date: February 14, 2025\n"
                "Location: Conference Room A, 12th Floor\n"
                "Attendees: Sarah Chen (CEO), Marcus Johnson (CFO), "
                "Priya Patel (CTO), David Kim (COO), Lisa Wang (CLO)\n\n"
                "1. Call to Order\n"
                "   The meeting was called to order at 9:03 AM by Sarah Chen.\n\n"
                "2. Approval of Previous Minutes\n"
                "   Motion to approve January 2025 minutes was moved by Marcus Johnson,\n"
                "   seconded by Priya Patel. Approved unanimously.\n\n"
                "3. Financial Review\n"
                "   Marcus Johnson presented Q4 2024 results:\n"
                "   - Revenue: $4.82M (up 18% YoY)\n"
                "   - EBITDA margin: 23.4% (target was 22%)\n"
                "   - Cash reserves: $12.7M\n\n"
                "4. Technology Roadmap\n"
                "   Priya Patel outlined the 2025 engineering priorities:\n"
                "   - Platform migration to Kubernetes (Q1-Q2)\n"
                "   - AI/ML feature rollout (Q2-Q3)\n"
                "   - SOC 2 Type II compliance (Q3)\n\n"
                "5. Adjournment\n"
                "   Meeting adjourned at 11:42 AM. Next meeting: March 14, 2025."
            ),
        },
        {
            "title": "Legal Notice — Confidentiality Agreement",
            "body": (
                "CONFIDENTIALITY AND NON-DISCLOSURE AGREEMENT\n\n"
                "This Agreement is entered into as of March 1, 2025, by and between\n"
                "Nexus Analytics, Inc. ('Company') and the undersigned recipient\n"
                "('Recipient').\n\n"
                "1. DEFINITION OF CONFIDENTIAL INFORMATION\n"
                "   'Confidential Information' means any non-public information\n"
                "   disclosed by the Company, including but not limited to: trade\n"
                "   secrets, business strategies, financial data, customer lists,\n"
                "   technical specifications, and proprietary algorithms.\n\n"
                "2. OBLIGATIONS OF RECIPIENT\n"
                "   The Recipient agrees to:\n"
                "   a) Hold all Confidential Information in strict confidence\n"
                "   b) Not disclose to any third party without prior written consent\n"
                "   c) Use the information solely for the authorized purpose\n"
                "   d) Return or destroy all materials upon termination\n\n"
                "3. TERM\n"
                "   This Agreement shall remain in effect for a period of three (3)\n"
                "   years from the date of execution.\n\n"
                "4. GOVERNING LAW\n"
                "   This Agreement shall be governed by the laws of the State of\n"
                "   California, without regard to conflict of laws principles.\n\n"
                "Signature: _________________________  Date: _______________"
            ),
        },
    ]

    for i, content in enumerate(page_contents_5_6):
        page = doc.new_page(width=595, height=842)
        page.insert_text(
            pymupdf.Point(72, 60),
            content["title"],
            fontsize=14,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        page.insert_text(
            pymupdf.Point(72, 78),
            f"Page {i + 5} of 10 — Scanned Document",
            fontsize=9,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 86), pymupdf.Point(523, 86))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        rect = pymupdf.Rect(72, 100, 523, 780)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # --- Pages 7-10: Correctly oriented pages ---
    page_contents_7_10 = [
        {
            "title": "Product Specification — NX-7200 Sensor Module",
            "body": (
                "Part Number: NX-7200-REV-C\n"
                "Revision Date: January 22, 2025\n"
                "Classification: Internal Use Only\n\n"
                "PHYSICAL SPECIFICATIONS:\n"
                "  Dimensions: 42mm x 28mm x 8.5mm\n"
                "  Weight: 12.3g (without mounting bracket)\n"
                "  Operating Temperature: -20°C to +85°C\n"
                "  Storage Temperature: -40°C to +125°C\n"
                "  Ingress Protection: IP67\n\n"
                "ELECTRICAL SPECIFICATIONS:\n"
                "  Input Voltage: 3.3V DC (±5%)\n"
                "  Current Draw: 45mA typical, 120mA peak\n"
                "  Communication: SPI (up to 10 MHz), I2C (400 kHz)\n"
                "  ADC Resolution: 16-bit\n"
                "  Sampling Rate: 1 kHz to 50 kHz (configurable)\n"
            ),
        },
        {
            "title": "Quality Assurance Test Report",
            "body": (
                "Test Report ID: QA-2025-0847\n"
                "Product: NX-7200 Sensor Module (Batch #2025-B03)\n"
                "Test Date: February 28, 2025\n"
                "Inspector: Dr. Elena Volkov\n\n"
                "TEST RESULTS SUMMARY:\n\n"
                "Test ID  | Description           | Result | Notes\n"
                "T-001    | Voltage Tolerance      | PASS   | 3.14V - 3.47V range\n"
                "T-002    | Current Draw (typical)  | PASS   | 43.8mA measured\n"
                "T-003    | Current Draw (peak)     | PASS   | 117.2mA measured\n"
                "T-004    | Temperature Cycling     | PASS   | 500 cycles completed\n"
                "T-005    | Vibration Resistance    | PASS   | MIL-STD-810G Method 514\n"
                "T-006    | Water Ingress (IP67)    | PASS   | 30 min submersion\n"
                "T-007    | EMI/EMC Compliance      | PASS   | FCC Part 15 Class B\n"
                "T-008    | ADC Linearity           | PASS   | INL < 0.5 LSB\n\n"
                "OVERALL STATUS: ALL TESTS PASSED\n"
                "Batch cleared for production release."
            ),
        },
        {
            "title": "Shipping Manifest — Order #WH-2025-3391",
            "body": (
                "Warehouse: Distribution Center West (Fremont, CA)\n"
                "Ship Date: March 5, 2025\n"
                "Carrier: FedEx Ground — Tracking: 7946 2031 8847\n\n"
                "LINE ITEMS:\n\n"
                "Item # | SKU          | Description              | Qty | Weight\n"
                "1      | NX-7200-C    | Sensor Module Rev C      | 500 | 6.15 kg\n"
                "2      | NX-7200-BRK  | Mounting Bracket Kit      | 500 | 3.80 kg\n"
                "3      | NX-CAB-1M    | Shielded Cable (1m)       | 500 | 8.50 kg\n"
                "4      | NX-CAB-3M    | Shielded Cable (3m)       | 200 | 10.20 kg\n"
                "5      | NX-PWR-33    | 3.3V Power Supply Unit    | 250 | 12.75 kg\n"
                "6      | NX-DOCK-4    | 4-Port Docking Station    | 50  | 7.00 kg\n\n"
                "TOTAL PACKAGES: 12 cartons\n"
                "TOTAL WEIGHT: 48.40 kg (106.7 lbs)\n"
                "DECLARED VALUE: $87,500.00\n\n"
                "Special Instructions: Fragile — handle with care. Do not stack more\n"
                "than 3 cartons high. Keep away from extreme heat sources."
            ),
        },
        {
            "title": "Appendix A — Regulatory Compliance Certificates",
            "body": (
                "This appendix contains references to all applicable compliance\n"
                "certificates for the NX-7200 Sensor Module product line.\n\n"
                "1. FCC Certificate of Conformity\n"
                "   FCC ID: 2A5YZ-NX7200\n"
                "   Grant Date: December 15, 2024\n"
                "   Equipment Class: Unintentional Radiator (Part 15, Subpart B)\n\n"
                "2. CE Declaration of Conformity\n"
                "   Notified Body: TÜV Rheinland (NB 0197)\n"
                "   Report Number: CE-2024-NX7200-001\n"
                "   Directives: 2014/30/EU (EMC), 2011/65/EU (RoHS)\n\n"
                "3. UL Recognition\n"
                "   UL File Number: E501234\n"
                "   Standard: UL 61010-1 (Safety for Measurement Equipment)\n\n"
                "4. RoHS & REACH Compliance\n"
                "   All materials verified compliant with EU RoHS Directive\n"
                "   SVHC screening completed per REACH Article 33\n\n"
                "5. ISO 9001:2015 Certification\n"
                "   Certificate Number: QMS-2024-78543\n"
                "   Issued by: Bureau Veritas\n"
                "   Valid through: November 2027\n\n"
                "Document Control: DC-2025-0091 | Classification: PUBLIC"
            ),
        },
    ]

    for i, content in enumerate(page_contents_7_10):
        page = doc.new_page(width=595, height=842)
        page.insert_text(
            pymupdf.Point(72, 60),
            content["title"],
            fontsize=14,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        page.insert_text(
            pymupdf.Point(72, 78),
            f"Page {i + 7} of 10 — Scanned Document",
            fontsize=9,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 86), pymupdf.Point(523, 86))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        rect = pymupdf.Rect(72, 100, 523, 780)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=10,
            fontname="cour",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 10')

    # Verify all pages have rotation 0
    doc = pymupdf.open(OUTPUT)
    for i in range(doc.page_count):
        print(f'  Page {i+1}: rotation={doc[i].rotation}')
    doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
