"""
Initial Setup: Create a large 20-page PDF presentation with high-resolution images,
embedded thumbnails, and metadata for a file-size compression task.
Task ID: pdf_cf_033
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_cf_033'
OUTPUT = f'{WORKDIR}/Documents/large_presentation.pdf'

def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def create_slide_image(width, height, base_color, slide_num):
    """Create a realistic slide image as JPEG bytes at high quality."""
    from PIL import Image, ImageDraw
    import random
    random.seed(slide_num * 37 + 7)

    img = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(img)
    r, g, b = base_color

    # Gradient background
    for y in range(height):
        f = y / height
        cr = min(255, int(r + (200 - r) * f * 0.4))
        cg = min(255, int(g + (200 - g) * f * 0.3))
        cb = min(255, int(b + (220 - b) * f * 0.2))
        draw.line([(0, y), (width, y)], fill=(cr, cg, cb))

    # Add noisy texture to prevent high JPEG compression
    import struct
    pixels = img.load()
    for y in range(0, height, 3):
        for x in range(0, width, 3):
            pr, pg2, pb = pixels[x, y]
            noise = random.randint(-15, 15)
            pixels[x, y] = (
                max(0, min(255, pr + noise)),
                max(0, min(255, pg2 + noise + random.randint(-5, 5))),
                max(0, min(255, pb + noise + random.randint(-5, 5))),
            )

    # Decorative shapes
    for _ in range(12):
        x0 = random.randint(0, width - 200)
        y0 = random.randint(0, height - 150)
        x1 = x0 + random.randint(100, 250)
        y1 = y0 + random.randint(80, 180)
        fill = (random.randint(40, 230), random.randint(40, 230), random.randint(40, 230))
        if random.random() > 0.5:
            draw.rectangle([x0, y0, x1, y1], fill=fill, outline=(20, 20, 20))
        else:
            draw.ellipse([x0, y0, x1, y1], fill=fill, outline=(20, 20, 20))

    # Chart bars
    base_y = int(height * 0.85)
    for i in range(8):
        bx = int(width * 0.08) + i * int(width * 0.11)
        bh = random.randint(int(height * 0.15), int(height * 0.5))
        bw = int(width * 0.07)
        bc = ((70 + i * 25) % 256, (110 + i * 18) % 256, (190 - i * 12) % 256)
        draw.rectangle([bx, base_y - bh, bx + bw, base_y], fill=bc, outline=(30, 30, 30))

    buf = io.BytesIO()
    # High-quality JPEG = large file with noisy content
    img.save(buf, format='JPEG', quality=98, subsampling=0)
    return buf.getvalue()

def create_initial():
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    import pymupdf

    doc = pymupdf.open()

    # Rich metadata
    doc.set_metadata({
        "title": "Global Innovation Summit 2025 - Annual Strategic Presentation",
        "author": "Dr. Elena Rodriguez, Chief Strategy Officer",
        "subject": "Annual Strategic Review and Innovation Roadmap for Meridian Corp",
        "keywords": "innovation, strategy, digital transformation, AI, sustainability, Q4 review, annual report, corporate strategy, technology roadmap, market analysis",
        "creator": "Meridian Corp Executive Presentations Suite v4.2",
        "producer": "Adobe Acrobat Pro DC 2025.001.20064",
    })

    pages_data = [
        {"title": "Global Innovation Summit 2025", "body": "Annual Strategic Presentation\nMeridian Corporation", "color": (25, 55, 109)},
        {"title": "Executive Summary", "body": "Revenue exceeding $4.2B. Digital transformation drove 23% efficiency improvement.", "color": (40, 80, 140)},
        {"title": "Market Overview", "body": "Global TAM: $187B. NA: $72B (+12%) | Europe: $54B (+8%) | APAC: $61B (+18%)", "color": (60, 100, 150)},
        {"title": "Financial Performance Q1-Q4", "body": "Revenue: $4.23B (+28%). Gross Margin: 67.2%. EBITDA: $1.14B. Net Income: $892M", "color": (45, 90, 130)},
        {"title": "Product Innovation Pipeline", "body": "Aurora: ML platform. Nexus: Quantum encryption. Helios: Sustainable computing. 14 patents.", "color": (70, 110, 160)},
        {"title": "Customer Success Metrics", "body": "NPS: 78. Retention: 96.3%. ACV: $2.4M (+15%). Enterprise clients: 847.", "color": (35, 75, 125)},
        {"title": "Technology Architecture", "body": "Microservices: 92% complete. 12 cloud regions. API latency: 23ms. Uptime: 99.997%", "color": (55, 95, 145)},
        {"title": "Talent & Organization", "body": "Headcount: 12,450. Engineering: 4,200 (+35%). Satisfaction: 4.6/5.0. Diversity +18pp.", "color": (50, 85, 135)},
        {"title": "Sustainability Report", "body": "Carbon -42%. Renewables: 78%. Waste diverted: 3,200 tons. ESG: AA rating.", "color": (30, 100, 80)},
        {"title": "Regional: Americas", "body": "Revenue: $1.89B (+31%). Fortune 100 deals. Austin TX hub. MIT partnership.", "color": (80, 60, 130)},
        {"title": "Regional: EMEA", "body": "Revenue: $1.21B (+22%). GDPR compliant. Nordic expansion. EU Digital Council.", "color": (100, 70, 120)},
        {"title": "Regional: APAC", "body": "Revenue: $1.13B (+38%). Japan $420M. New DCs: Singapore, Sydney, Mumbai.", "color": (90, 80, 140)},
        {"title": "R&D Investment", "body": "R&D: $680M (16.1%). AI/ML: $210M. Quantum partnership. 23 papers published.", "color": (65, 105, 155)},
        {"title": "Competitive Landscape", "body": "#2 globally, #1 enterprise. +4.2pp share. AI + security differentiation.", "color": (75, 95, 145)},
        {"title": "Risk Management", "body": "Cybersecurity: $145M (+40%). Zero incidents. 8 DR scenarios. 47 jurisdictions.", "color": (85, 65, 115)},
        {"title": "Strategic Partnerships", "body": "Microsoft Azure, Salesforce CRM, SAP Enterprise, AWS Advanced Partner.", "color": (55, 110, 90)},
        {"title": "2026 Roadmap", "body": "Target: $5.4B. 15 regions. 3 product lines. 2 acquisitions. Carbon neutral.", "color": (40, 100, 120)},
        {"title": "Capital Allocation", "body": "Capex: $450M. M&A: $800M. Buyback: $500M. Dividend +15%. R&D: $780M.", "color": (70, 80, 150)},
        {"title": "KPIs Dashboard", "body": "MAU: 24.7M. API: 12.3B/day. Data: 4.8PB/mo. Inference <50ms. Uptime 99.99%.", "color": (45, 105, 135)},
        {"title": "Thank You", "body": "Questions & Discussion\nstrategy@meridiancorp.com\nConfidential", "color": (25, 55, 109)},
    ]

    # 300 DPI images: main 1500x1050, secondary 900x600
    for i, pg in enumerate(pages_data):
        page = doc.new_page(width=595, height=842)

        # Main image (large, high-res)
        img_bytes = create_slide_image(1500, 1050, pg["color"], i)
        page.insert_image(pymupdf.Rect(20, 20, 575, 430), stream=img_bytes)

        # Secondary image
        sc = ((pg["color"][0]+60)%200+40, (pg["color"][1]+40)%200+40, (pg["color"][2]+80)%200+40)
        img_bytes2 = create_slide_image(900, 600, sc, i + 100)
        page.insert_image(pymupdf.Rect(50, 440, 300, 620), stream=img_bytes2)

        # Title
        page.insert_text(pymupdf.Point(72, 660), pg["title"],
                        fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

        # Body
        rect = pymupdf.Rect(72, 675, 523, 820)
        page.insert_textbox(rect, pg["body"], fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))

        # Page number
        page.insert_text(pymupdf.Point(280, 835), f"Page {i + 1} of 20",
                        fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

        print(f"  Created page {i + 1}/20: {pg['title']}")

    # Bookmarks
    toc = [[1, pg["title"], i + 1] for i, pg in enumerate(pages_data)]
    doc.set_toc(toc)

    # Save -- JPEG content means deflate won't shrink it much, keeping file large
    doc.save(OUTPUT, garbage=0, deflate=False, clean=False)
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f'\nInitial file created: {OUTPUT}')
    print(f'File size: {file_size / (1024*1024):.1f} MB')

    # Ensure compressed version does NOT exist
    compressed = f'{WORKDIR}/Documents/large_presentation_compressed.pdf'
    if os.path.exists(compressed):
        os.remove(compressed)

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
