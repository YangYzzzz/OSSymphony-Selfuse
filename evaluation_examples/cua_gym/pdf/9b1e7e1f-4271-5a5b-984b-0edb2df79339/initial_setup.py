"""
Initial Setup: Create a 5-page scanned contract PDF with no selectable text
Task ID: pdf_gf2_013
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_013'
SCAN_DIR = f'{WORKDIR}/scans'
OUTPUT = f'{SCAN_DIR}/contract_scan.pdf'

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

# Contract text for each page - realistic service contract content
PAGE_TEXTS = [
    # Page 1 - Title and Introduction
    """SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of March 15, 2025,
by and between Meridian Technology Solutions Inc., a Delaware corporation
with principal offices at 4200 Westfield Boulevard, Suite 800, Indianapolis,
IN 46205 ("Service Provider"), and Cascade Healthcare Systems LLC, a
California limited liability company with principal offices at 1750 Pacific
Coast Highway, Suite 400, Redondo Beach, CA 90277 ("Client").

RECITALS

WHEREAS, Service Provider is engaged in the business of providing information
technology consulting, software development, and managed infrastructure
services to healthcare organizations; and

WHEREAS, Client desires to engage Service Provider to perform certain
technology services as described herein, and Service Provider desires to
provide such services subject to the terms and conditions set forth in this
Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, and for other good and valuable consideration, the receipt
and sufficiency of which are hereby acknowledged, the parties agree as
follows:""",

    # Page 2 - Scope of Services
    """ARTICLE 1: SCOPE OF SERVICES

1.1 Services. Service Provider shall provide the following services to Client
during the Term of this Agreement (collectively, the "Services"):

(a) Electronic Health Records (EHR) System Migration: Complete migration of
Client's existing patient records database from Legacy MedTrack v4.2 to the
CloudMed Enterprise Platform, including data mapping, validation, and
integrity verification for approximately 2.4 million patient records.

(b) Network Infrastructure Upgrade: Design and implementation of redundant
fiber-optic network backbone across Client's three primary hospital campuses
located in Redondo Beach, Torrance, and Long Beach, California.

(c) Cybersecurity Assessment and Remediation: Comprehensive security audit
of Client's existing IT infrastructure, including penetration testing,
vulnerability assessment, and implementation of HIPAA-compliant security
protocols and encryption standards.

(d) Staff Training Program: Development and delivery of technology training
curriculum for approximately 850 clinical and administrative staff members
across all Client facilities.

1.2 Service Standards. All Services shall be performed in a professional and
workmanlike manner, consistent with industry best practices and applicable
regulatory requirements, including but not limited to HIPAA, HITECH Act, and
California Consumer Privacy Act (CCPA) standards.""",

    # Page 3 - Compensation and Payment
    """ARTICLE 2: COMPENSATION AND PAYMENT TERMS

2.1 Service Fees. Client shall pay Service Provider the following fees for
the Services rendered under this Agreement:

(a) EHR Migration Services: A fixed fee of $1,875,000.00 (One Million Eight
Hundred Seventy-Five Thousand Dollars), payable in four equal quarterly
installments of $468,750.00 each, with the first installment due upon
execution of this Agreement.

(b) Network Infrastructure: A fixed fee of $2,340,000.00 (Two Million Three
Hundred Forty Thousand Dollars), payable upon completion of designated
milestones as set forth in Exhibit B attached hereto.

(c) Cybersecurity Services: A monthly retainer of $45,000.00 (Forty-Five
Thousand Dollars) for ongoing monitoring and maintenance, plus a one-time
assessment fee of $185,000.00 (One Hundred Eighty-Five Thousand Dollars).

(d) Training Program: A fixed fee of $225,000.00 (Two Hundred Twenty-Five
Thousand Dollars), payable in two installments of $112,500.00 each.

2.2 Expenses. Client shall reimburse Service Provider for all reasonable and
pre-approved out-of-pocket expenses incurred in connection with the
performance of Services, including travel, lodging, and equipment costs,
provided that any single expense exceeding $5,000.00 requires prior written
approval from Client.

2.3 Payment Terms. All invoices shall be due and payable within thirty (30)
calendar days of receipt. Late payments shall accrue interest at the rate of
1.5% per month or the maximum rate permitted by applicable law, whichever
is less.""",

    # Page 4 - Term and Termination
    """ARTICLE 3: TERM AND TERMINATION

3.1 Term. This Agreement shall commence on the Effective Date and shall
continue for an initial term of thirty-six (36) months (the "Initial Term"),
unless earlier terminated in accordance with the provisions hereof. Upon
expiration of the Initial Term, this Agreement shall automatically renew for
successive twelve (12) month periods (each a "Renewal Term"), unless either
party provides written notice of non-renewal at least ninety (90) days prior
to the expiration of the then-current term.

3.2 Termination for Cause. Either party may terminate this Agreement upon
sixty (60) days written notice if the other party materially breaches any
provision of this Agreement and fails to cure such breach within thirty (30)
days after receipt of written notice specifying the nature of the breach.

3.3 Termination for Convenience. Client may terminate this Agreement for
convenience upon one hundred twenty (120) days prior written notice to
Service Provider, subject to payment of all fees earned through the effective
date of termination plus a termination fee equal to fifteen percent (15%)
of the remaining contract value.

3.4 Effect of Termination. Upon termination or expiration of this Agreement:

(a) Service Provider shall promptly deliver to Client all work product,
documentation, and Client data in its possession;

(b) Client shall pay all outstanding fees and expenses incurred through the
effective date of termination;

(c) Sections 4 (Confidentiality), 5 (Intellectual Property), 6 (Limitation
of Liability), and 7 (Indemnification) shall survive termination.""",

    # Page 5 - General Provisions and Signatures
    """ARTICLE 4: CONFIDENTIALITY AND DATA PROTECTION

4.1 Confidential Information. Each party agrees to maintain in strict
confidence all proprietary and confidential information received from the
other party during the term of this Agreement. Confidential Information
shall include, but not be limited to, trade secrets, business plans,
financial data, patient health information (PHI), technical specifications,
and software source code.

ARTICLE 5: LIMITATION OF LIABILITY

5.1 Limitation. IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY UNDER
THIS AGREEMENT EXCEED THE TOTAL FEES PAID OR PAYABLE TO SERVICE PROVIDER
DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING
RISE TO THE CLAIM.

ARTICLE 6: GENERAL PROVISIONS

6.1 Governing Law. This Agreement shall be governed by and construed in
accordance with the laws of the State of California.

6.2 Entire Agreement. This Agreement constitutes the entire agreement
between the parties and supersedes all prior negotiations and agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the
date first written above.

MERIDIAN TECHNOLOGY SOLUTIONS INC.

By: ___________________________________
Name: Victoria R. Blackwell
Title: Chief Executive Officer
Date: March 15, 2025

CASCADE HEALTHCARE SYSTEMS LLC

By: ___________________________________
Name: Dr. Jonathan M. Reeves
Title: President and Chief Operating Officer
Date: March 15, 2025"""
]


def create_scanned_pdf():
    """Create a PDF with text rendered as images (simulating scanned document)."""
    from PIL import Image, ImageDraw, ImageFont
    import pymupdf

    os.makedirs(SCAN_DIR, exist_ok=True)

    # Render each page's text as an image, then embed in PDF
    page_images = []
    for i, text in enumerate(PAGE_TEXTS):
        # Create high-res image simulating a scanned page
        # A4 at 200 DPI: ~1654 x 2339 pixels
        img_w, img_h = 1654, 2339
        img = Image.new('RGB', (img_w, img_h), color=(252, 250, 245))  # slightly off-white like scan

        draw = ImageDraw.Draw(img)

        # Try to use a reasonable font
        font_size = 28
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font_size)
                font_bold = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
                font_bold = font

        # Draw text line by line
        margin_x = 120
        margin_y = 140
        line_height = 38
        max_width = img_w - 2 * margin_x

        y = margin_y
        lines = text.strip().split('\n')
        for line in lines:
            line = line.rstrip()
            if not line:
                y += line_height // 2
                continue

            # Simple word wrapping
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                try:
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    tw = bbox[2] - bbox[0]
                except:
                    tw = len(test_line) * (font_size * 0.6)

                if tw > max_width and current_line:
                    # Check if this is a title line (all caps, short)
                    use_font = font_bold if current_line.isupper() and len(current_line) < 60 else font
                    draw.text((margin_x, y), current_line, fill=(25, 25, 30), font=use_font)
                    y += line_height
                    current_line = word
                else:
                    current_line = test_line

            if current_line:
                use_font = font_bold if current_line.isupper() and len(current_line) < 60 else font
                draw.text((margin_x, y), current_line, fill=(25, 25, 30), font=use_font)
                y += line_height

        # Add slight noise/grain to simulate scan quality
        import random
        random.seed(42 + i)
        pixels = img.load()
        for _ in range(5000):
            rx = random.randint(0, img_w - 1)
            ry = random.randint(0, img_h - 1)
            r, g, b = pixels[rx, ry]
            noise = random.randint(-15, 15)
            pixels[rx, ry] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )

        # Save page image temporarily
        page_img_path = f'/tmp/pdf_gf2_013_page_{i}.png'
        img.save(page_img_path, 'PNG')
        page_images.append(page_img_path)

    # Create PDF from images (no text layer - simulating scanned document)
    doc = pymupdf.open()
    for img_path in page_images:
        img = pymupdf.open(img_path)
        # Convert image to single-page PDF and insert
        pdfbytes = img.convert_to_pdf()
        img.close()
        img_pdf = pymupdf.open("pdf", pdfbytes)
        doc.insert_pdf(img_pdf)
        img_pdf.close()

    doc.save(OUTPUT)
    doc.close()

    # Clean up temp images
    for img_path in page_images:
        os.remove(img_path)

    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 5')

    # Verify no selectable text
    verify_doc = pymupdf.open(OUTPUT)
    for i in range(verify_doc.page_count):
        text = verify_doc[i].get_text("text").strip()
        if text:
            print(f'WARNING: Page {i+1} has selectable text: {text[:50]}...')
        else:
            print(f'Page {i+1}: No selectable text (OK - scanned image)')
    verify_doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_scanned_pdf()
