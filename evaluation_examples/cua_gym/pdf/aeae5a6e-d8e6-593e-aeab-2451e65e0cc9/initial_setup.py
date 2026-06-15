"""
Initial Setup: Create a large discovery production PDF with high-res scanned images
Task ID: pdf_legal_081
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_081'
PROD_DIR = f'{WORKDIR}/legal/production'
OUTPUT = f'{PROD_DIR}/large_production.pdf'


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


def create_high_res_image(width=1700, height=2200, seed=0):
    """Create a high-resolution image simulating a scanned document page.
    1700x2200 at ~200 DPI = 8.5x11 inches. Uses random gradient/block
    patterns that compress poorly as PNG but well as JPEG."""
    from PIL import Image, ImageDraw
    import random
    random.seed(seed)

    # Start with off-white background
    bg = (random.randint(238, 248), random.randint(236, 246), random.randint(233, 243))
    img = Image.new('RGB', (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Add many small colored rectangles to create noise that resists PNG compression
    # These simulate scan artifacts, paper texture, faint stains, etc.
    for _ in range(5000):
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = x1 + random.randint(1, 20)
        y2 = y1 + random.randint(1, 20)
        # Slight color variations
        r = random.randint(220, 255)
        g = random.randint(218, 253)
        b = random.randint(215, 250)
        draw.rectangle([x1, y1, x2, y2], fill=(r, g, b))

    # Add horizontal scan line artifacts
    for _ in range(20):
        y = random.randint(0, height - 1)
        gray = random.randint(225, 245)
        draw.line([(0, y), (width, y)], fill=(gray, gray, gray), width=1)

    # Add some darker spots (simulating ink bleed, dust)
    for _ in range(200):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r = random.randint(2, 6)
        gray = random.randint(150, 200)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(gray, gray, gray))

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=False, compress_level=1)
    return buf.getvalue()


def create_initial():
    import pymupdf

    os.makedirs(PROD_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Legal document content templates
    legal_headings = [
        "EXHIBIT", "DEPOSITION TRANSCRIPT", "INTERROGATORY RESPONSE",
        "PRODUCTION REQUEST", "PRIVILEGE LOG ENTRY", "COURT ORDER",
        "MEMORANDUM OF LAW", "AFFIDAVIT", "DECLARATION",
        "NOTICE OF MOTION", "STIPULATION", "SUBPOENA DUCES TECUM"
    ]

    parties = [
        "Westfield Holdings, LLC", "Pacific Coast Industries, Inc.",
        "Morrison & Associates", "Chen Technology Group",
        "Harrison Real Estate Partners", "Meridian Capital Fund III"
    ]

    attorneys = [
        "Sarah J. Morrison, Esq.", "David R. Blackwell, Esq.",
        "Jennifer L. Torres, Esq.", "Michael K. Okonkwo, Esq.",
        "Patricia A. Yamamoto, Esq.", "Robert S. Fitzgerald, Esq."
    ]

    case_number = "2024-CV-08174-RJM"
    court = "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF CALIFORNIA"

    # Paragraph text templates for body content
    body_paragraphs = [
        "Pursuant to Federal Rule of Civil Procedure 34, the undersigned counsel hereby "
        "produces the following documents in response to Plaintiff's First Set of Requests "
        "for Production of Documents, dated March 15, 2025.",

        "COMES NOW the Defendant, by and through undersigned counsel, and respectfully "
        "submits this Memorandum of Law in Opposition to Plaintiff's Motion for Summary "
        "Judgment, and in support thereof states as follows:",

        "The deponent, having been first duly sworn, was examined and testified as follows "
        "on the record. The examination was conducted pursuant to the Federal Rules of "
        "Civil Procedure and the applicable local rules of this Court.",

        "This document is being produced subject to and without waiver of any objections, "
        "including but not limited to objections based on attorney-client privilege, work "
        "product doctrine, and the joint defense privilege.",

        "Upon information and belief, the transactions described herein occurred between "
        "January 2023 and December 2024, involving multiple wire transfers between the "
        "accounts identified in Schedule A attached hereto.",

        "The witness testified that the meeting took place on or about September 14, 2024, "
        "at the corporate offices located at 1250 Pacific Highway, Suite 4200, San Diego, "
        "California 92101, and lasted approximately three hours.",

        "Respondent objects to this request as overly broad, unduly burdensome, and not "
        "proportional to the needs of the case. Subject to and without waiving said "
        "objections, Respondent responds as follows:",

        "FURTHER AFFIANT SAYETH NOT. Executed this day under penalty of perjury pursuant "
        "to 28 U.S.C. Section 1746, in the County of San Diego, State of California.",
    ]

    print(f"Creating {500}-page production document with high-res images...")

    # Generate 50 unique images, reuse across pages
    # More unique images = less deduplication = larger file
    NUM_IMAGES = 50
    print(f"Generating {NUM_IMAGES} high-resolution scanned images...")
    image_cache = []
    for i in range(NUM_IMAGES):
        img_bytes = create_high_res_image(seed=i)
        image_cache.append(img_bytes)
        if (i + 1) % 10 == 0:
            print(f"  Images {i+1}/{NUM_IMAGES} generated ({len(img_bytes)} bytes)")

    import random
    random.seed(42)

    for page_num in range(500):
        # A4-ish page: Letter size in points
        page = doc.new_page(width=612, height=792)

        # Every page gets a scanned image background (simulating scanned docs)
        # This is what makes the file large
        img_data = image_cache[page_num % NUM_IMAGES]
        img_rect = pymupdf.Rect(0, 0, 612, 792)
        page.insert_image(img_rect, stream=img_data)

        # Overlay text content on top
        heading_idx = page_num % len(legal_headings)
        heading = legal_headings[heading_idx]

        # Bates stamp number
        bates_num = f"WH-PROD-{page_num + 1:06d}"

        # Page header
        page.insert_text(
            pymupdf.Point(72, 40),
            f"Case No. {case_number}",
            fontsize=8,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

        # Document heading
        exhibit_num = (page_num // 20) + 1
        page.insert_text(
            pymupdf.Point(200, 80),
            f"{heading} {exhibit_num}",
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Court info (on first page of each "document section")
        if page_num % 20 == 0:
            page.insert_text(
                pymupdf.Point(170, 110),
                court,
                fontsize=10,
                fontname="hebo",
                color=(0, 0, 0),
            )
            party1 = parties[page_num % len(parties)]
            party2 = parties[(page_num + 1) % len(parties)]
            page.insert_text(
                pymupdf.Point(72, 160),
                f"{party1}, Plaintiff,\n    v.\n{party2}, Defendant.",
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
            )

        # Body text
        y_pos = 220 if page_num % 20 == 0 else 120
        for para_idx in range(3):
            para = body_paragraphs[(page_num + para_idx) % len(body_paragraphs)]
            rect = pymupdf.Rect(72, y_pos, 540, y_pos + 120)
            page.insert_textbox(
                rect,
                f"    {para}",
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            y_pos += 130

        # Attorney signature block (on some pages)
        if page_num % 20 == 19:
            attorney = attorneys[page_num % len(attorneys)]
            page.insert_text(
                pymupdf.Point(72, 680),
                f"Respectfully submitted,\n\n\n_________________________\n{attorney}\n"
                f"Counsel for Defendant",
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
            )

        # Bates stamp at bottom
        page.insert_text(
            pymupdf.Point(480, 770),
            bates_num,
            fontsize=8,
            fontname="cour",
            color=(0.4, 0.4, 0.4),
        )

        # Footer page number
        page.insert_text(
            pymupdf.Point(290, 780),
            f"Page {page_num + 1} of 500",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        if (page_num + 1) % 50 == 0:
            print(f"  Created page {page_num + 1}/500")

    # Set metadata
    doc.set_metadata({
        "title": f"Production Documents - Case {case_number}",
        "author": "Morrison & Associates",
        "subject": "Discovery Production - Westfield Holdings v. Pacific Coast Industries",
        "keywords": "legal, production, discovery, litigation",
        "creator": "Document Scanner v4.2",
        "producer": "Legal Document Management System",
    })

    doc.save(OUTPUT, deflate=False, deflate_images=False, garbage=0)  # No compression to keep size large
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f"Initial file created: {OUTPUT}")
    print(f"File size: {file_size / (1024*1024):.1f} MB")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
