"""
Initial Setup: Create a 10-page presentation PDF with images embedded on various pages.
Task ID: pdf_cr_052
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_052'
PDF_OUTPUT = f'{WORKDIR}/Desktop/presentation.pdf'


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


def create_colored_image(width, height, color_rgb, filename):
    """Create a simple colored image with some variation for realism."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (width, height), color_rgb)
    draw = ImageDraw.Draw(img)
    # Add some shapes for visual interest
    for i in range(3):
        x0 = int(width * (0.1 + i * 0.25))
        y0 = int(height * 0.2)
        x1 = x0 + int(width * 0.15)
        y1 = y0 + int(height * 0.3)
        shade = tuple(max(0, c - 40 - i * 20) for c in color_rgb)
        draw.rectangle([x0, y0, x1, y1], fill=shade)
    img.save(filename)
    return filename


def create_grayscale_image(width, height, filename):
    """Create a grayscale image."""
    from PIL import Image, ImageDraw
    img = Image.new("L", (width, height), 180)
    draw = ImageDraw.Draw(img)
    # Add gradient-like rectangles
    for i in range(5):
        shade = 40 + i * 40
        x0 = int(width * i / 5)
        draw.rectangle([x0, 0, x0 + int(width / 5), height], fill=shade)
    img.save(filename)
    return filename


def create_initial():
    import pymupdf
    from PIL import Image
    import tempfile

    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)
    tmp_dir = tempfile.mkdtemp()

    doc = pymupdf.open()

    # --- Page layouts ---
    # We'll create 10 pages. Images on pages 1, 2, 3, 5, 6, 8, 10 (0-indexed: 0,1,2,4,5,7,9)
    # Varying image sizes, colorspaces, and counts per page

    page_titles = [
        "TechVision 2026 - Annual Strategy Overview",
        "Market Analysis & Growth Trends",
        "Product Portfolio Review",
        "Financial Performance Summary",
        "Customer Engagement Metrics",
        "Research & Development Pipeline",
        "Global Expansion Roadmap",
        "Team & Organizational Updates",
        "Sustainability & ESG Initiatives",
        "Key Takeaways & Next Steps",
    ]

    # Define images to embed: (page_idx, width, height, color_mode, color/None, rect)
    # color_mode: "RGB" or "L" (grayscale)
    images_spec = [
        # Page 0 (title slide): 1 large banner image
        (0, 480, 200, "RGB", (45, 85, 140), pymupdf.Rect(57, 200, 538, 420)),
        # Page 1: 2 images - charts
        (1, 320, 240, "RGB", (60, 130, 80), pymupdf.Rect(57, 250, 290, 500)),
        (1, 280, 200, "RGB", (180, 70, 50), pymupdf.Rect(300, 280, 538, 480)),
        # Page 2: 1 product image
        (2, 400, 300, "RGB", (100, 60, 140), pymupdf.Rect(100, 300, 500, 600)),
        # Page 3 (no images - text only)
        # Page 4: 2 images - metrics dashboards
        (4, 250, 180, "RGB", (30, 100, 150), pymupdf.Rect(57, 250, 280, 430)),
        (4, 200, 150, "L", None, pymupdf.Rect(310, 270, 510, 430)),
        # Page 5: 3 images - R&D photos
        (5, 160, 120, "RGB", (200, 160, 50), pymupdf.Rect(57, 250, 200, 370)),
        (5, 160, 120, "RGB", (50, 160, 200), pymupdf.Rect(220, 250, 363, 370)),
        (5, 160, 120, "RGB", (160, 50, 120), pymupdf.Rect(383, 250, 526, 370)),
        # Page 6 (no images - map placeholder text)
        # Page 7: 1 team photo (grayscale)
        (7, 500, 280, "L", None, pymupdf.Rect(57, 300, 538, 600)),
        # Page 8: 2 images
        (8, 220, 180, "RGB", (40, 140, 100), pymupdf.Rect(57, 280, 270, 460)),
        (8, 220, 180, "RGB", (90, 90, 170), pymupdf.Rect(290, 280, 520, 460)),
        # Page 9: 1 summary graphic
        (9, 350, 200, "RGB", (70, 70, 70), pymupdf.Rect(120, 350, 475, 560)),
    ]

    # Create all image files first
    img_files = []
    for idx, (page_idx, w, h, mode, color, rect) in enumerate(images_spec):
        fname = os.path.join(tmp_dir, f"img_{idx}.png")
        if mode == "RGB":
            create_colored_image(w, h, color, fname)
        else:
            create_grayscale_image(w, h, fname)
        img_files.append(fname)

    # Create pages and insert text and images
    for page_idx in range(10):
        page = doc.new_page(width=595, height=842)  # A4

        # Title bar background
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 80))
        shape.finish(fill=(0.15, 0.25, 0.45), color=(0.15, 0.25, 0.45))
        shape.commit()

        # Page title
        page.insert_text(
            pymupdf.Point(57, 50),
            page_titles[page_idx],
            fontsize=20,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Page number
        page.insert_text(
            pymupdf.Point(520, 820),
            f"{page_idx + 1}/10",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Subtitle / body text per page
        body_texts = {
            0: "Welcome to TechVision's annual strategy meeting. This presentation covers our key achievements, market position, and strategic priorities for the coming year.",
            1: "Our market analysis indicates strong growth across all segments. Revenue increased by 23% YoY while maintaining healthy profit margins above industry average.",
            2: "The product portfolio has expanded to include 15 active product lines serving enterprise, SMB, and consumer segments across North America, Europe, and Asia-Pacific.",
            3: "Q1: $12.4M revenue, 18% margin | Q2: $14.1M revenue, 21% margin | Q3: $15.8M revenue, 22% margin | Q4: $18.2M revenue, 25% margin. Total FY: $60.5M, Net Profit: $13.1M.",
            4: "Customer satisfaction scores reached 4.6/5.0 with NPS of 72. Active user base grew to 2.3M monthly users, up from 1.6M at the start of the year.",
            5: "R&D investment totaled $8.2M across three major initiatives: AI-powered analytics engine, next-gen mobile platform, and enterprise security framework.",
            6: "Expansion into Southeast Asia and Latin America is on track. Singapore office opened Q2, Sao Paulo office planned for Q1 next year. Partnership with Meridian Corp signed.",
            7: "Headcount grew from 340 to 485 employees. Key hires include VP of Engineering (Dr. Lisa Park), Head of APAC Sales (Rajesh Kumar), and Chief Data Officer (Maria Santos).",
            8: "Carbon footprint reduced by 15%. Achieved ISO 14001 certification. Launched employee volunteer program with 2,400 hours contributed. Published first ESG report.",
            9: "Key priorities for next year: 1) Scale AI platform to 5M users, 2) Achieve $80M revenue target, 3) Complete APAC expansion, 4) Launch v3.0 product suite.",
        }

        text_y = 110 if page_idx != 3 else 110
        page.insert_textbox(
            pymupdf.Rect(57, text_y, 538, 230),
            body_texts[page_idx],
            fontsize=11,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # Now insert images
    for idx, (page_idx, w, h, mode, color, rect) in enumerate(images_spec):
        page = doc[page_idx]
        page.insert_image(rect, filename=img_files[idx])

    # Set metadata
    doc.set_metadata({
        "title": "TechVision 2026 - Annual Strategy Overview",
        "author": "TechVision Strategic Planning Team",
        "subject": "Annual Strategy Presentation",
        "keywords": "strategy, annual, techvision, 2026",
        "creator": "TechVision Presentations",
    })

    doc.save(PDF_OUTPUT)
    doc.close()
    print(f'Initial file created: {PDF_OUTPUT}')

    # Clean up temp images
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
