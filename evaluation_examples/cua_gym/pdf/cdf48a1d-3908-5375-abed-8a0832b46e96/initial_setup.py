"""
Initial Setup: Create high-resolution brochure PDF with large images
Task ID: pdf_mbc_069
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/high_res_brochure.pdf'

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

def create_high_res_image(width, height, color_base, text_label, seed=0):
    """Create a high-resolution image with gradients and patterns to simulate brochure imagery."""
    from PIL import Image, ImageDraw, ImageFont
    import random
    random.seed(seed)

    img = Image.new('RGB', (width, height), color_base)
    draw = ImageDraw.Draw(img)

    # Create gradient overlay
    for y in range(height):
        alpha = y / height
        r = int(color_base[0] * (1 - alpha * 0.3))
        g = int(color_base[1] * (1 - alpha * 0.2))
        b = int(color_base[2] * (1 - alpha * 0.1))
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add geometric patterns (circles, rectangles)
    for _ in range(30):
        x1 = random.randint(0, width - 200)
        y1 = random.randint(0, height - 200)
        x2 = x1 + random.randint(80, 200)
        y2 = y1 + random.randint(80, 200)
        fill = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        if random.random() > 0.5:
            draw.ellipse([x1, y1, x2, y2], fill=fill, outline=(255, 255, 255))
        else:
            draw.rectangle([x1, y1, x2, y2], fill=fill, outline=(255, 255, 255))

    # Add noise/texture for realism (makes images larger)
    import struct
    pixels = img.load()
    for y in range(0, height, 3):
        for x in range(0, width, 3):
            r, g, b = pixels[x, y]
            noise = random.randint(-15, 15)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise))
            )

    # Add label text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = ImageFont.load_default()
    draw.text((width // 4, height // 2 - 30), text_label, fill=(255, 255, 255), font=font)

    return img


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Remove existing file if any
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    import pymupdf

    doc = pymupdf.open()

    # Page configuration - 8 pages of brochure content
    # Using A4 size: 595 x 842 points
    # At 600 DPI, we need large images to fill pages
    # 595 pts / 72 pts per inch * 600 DPI = ~4958 pixels wide
    # 842 pts / 72 pts per inch * 600 DPI = ~7017 pixels tall

    page_configs = [
        {
            "title": "TechVista Solutions",
            "subtitle": "Annual Product Brochure 2025",
            "body": "Discover our cutting-edge technology solutions designed to transform your business operations and drive growth in the digital era.",
            "img_color": (30, 60, 120),
            "img_label": "Innovation Hub",
        },
        {
            "title": "Cloud Infrastructure Platform",
            "subtitle": "Enterprise-Grade Scalability",
            "body": "Our cloud platform delivers 99.99% uptime with automated scaling, built-in disaster recovery, and comprehensive security compliance including SOC 2 Type II and ISO 27001 certifications.",
            "img_color": (20, 100, 80),
            "img_label": "Cloud Services",
        },
        {
            "title": "AI-Powered Analytics Suite",
            "subtitle": "Real-Time Business Intelligence",
            "body": "Transform raw data into actionable insights with machine learning models that automatically detect patterns, anomalies, and trends across your entire data ecosystem.",
            "img_color": (100, 40, 90),
            "img_label": "Data Analytics",
        },
        {
            "title": "Cybersecurity Solutions",
            "subtitle": "Zero Trust Architecture",
            "body": "Protect your organization with multi-layered defense systems including endpoint detection, network monitoring, identity management, and automated incident response.",
            "img_color": (120, 30, 30),
            "img_label": "Security Shield",
        },
        {
            "title": "IoT Management Platform",
            "subtitle": "Connected Device Ecosystem",
            "body": "Manage millions of IoT devices seamlessly with our unified platform featuring device provisioning, firmware updates, real-time telemetry, and edge computing capabilities.",
            "img_color": (40, 80, 120),
            "img_label": "IoT Network",
        },
        {
            "title": "Developer Experience Tools",
            "subtitle": "Accelerate Your Development Lifecycle",
            "body": "Empower your engineering teams with integrated CI/CD pipelines, collaborative code review, automated testing frameworks, and comprehensive API management tools.",
            "img_color": (60, 100, 40),
            "img_label": "DevOps Pipeline",
        },
        {
            "title": "Customer Success Stories",
            "subtitle": "Trusted by Industry Leaders",
            "body": "Over 2,500 enterprises across 45 countries rely on TechVista Solutions. Our clients report an average 340% ROI within the first 18 months of deployment.",
            "img_color": (80, 60, 100),
            "img_label": "Success Metrics",
        },
        {
            "title": "Contact & Next Steps",
            "subtitle": "Let's Build Your Future Together",
            "body": "Schedule a personalized demo with our solutions architects. Visit techvista-solutions.com or call +1 (555) 847-2900. Headquarters: 1200 Innovation Drive, San Francisco, CA 94105.",
            "img_color": (50, 70, 110),
            "img_label": "Get Started",
        },
    ]

    for i, config in enumerate(page_configs):
        page = doc.new_page(width=595, height=842)

        # Create a high-resolution image (600 DPI equivalent)
        # Image covers roughly 70% of page area
        img_w = 3500  # ~600 DPI for roughly 5.8 inches
        img_h = 2800  # ~600 DPI for roughly 4.7 inches
        img = create_high_res_image(img_w, img_h, config["img_color"], config["img_label"], seed=i * 17)

        # Save image to bytes (PNG for maximum quality/size)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Insert image into page (top portion)
        img_rect = pymupdf.Rect(20, 20, 575, 420)
        page.insert_image(img_rect, stream=img_bytes.read())

        # Add title text
        page.insert_text(
            pymupdf.Point(40, 460),
            config["title"],
            fontsize=28,
            fontname="hebo",
            color=(0.1, 0.1, 0.3),
        )

        # Add subtitle
        page.insert_text(
            pymupdf.Point(40, 495),
            config["subtitle"],
            fontsize=16,
            fontname="heit",
            color=(0.3, 0.3, 0.5),
        )

        # Add body text in a textbox
        body_rect = pymupdf.Rect(40, 520, 555, 700)
        page.insert_textbox(
            body_rect,
            config["body"],
            fontsize=12,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Add page number footer
        page.insert_text(
            pymupdf.Point(280, 810),
            f"Page {i + 1} of 8",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Add a second smaller image on some pages for more content
        if i % 2 == 0:
            img2_w = 2400
            img2_h = 1200
            secondary_colors = [(70, 120, 90), (90, 50, 110), (110, 80, 40), (40, 90, 120)]
            img2 = create_high_res_image(img2_w, img2_h, secondary_colors[i // 2 % 4],
                                          f"Detail View {i+1}", seed=i * 31 + 7)
            img2_bytes = io.BytesIO()
            img2.save(img2_bytes, format='PNG')
            img2_bytes.seek(0)

            img2_rect = pymupdf.Rect(40, 710, 555, 790)
            page.insert_image(img2_rect, stream=img2_bytes.read())

        print(f"  Page {i+1}/8 created")

    # Set document metadata
    doc.set_metadata({
        "title": "TechVista Solutions - Annual Product Brochure 2025",
        "author": "TechVista Marketing Department",
        "subject": "Product Brochure",
        "keywords": "technology, cloud, AI, cybersecurity, IoT, enterprise",
        "creator": "TechVista Design Studio",
        "producer": "TechVista Publishing",
    })

    # Add table of contents
    toc = [
        [1, "TechVista Solutions", 1],
        [1, "Cloud Infrastructure Platform", 2],
        [1, "AI-Powered Analytics Suite", 3],
        [1, "Cybersecurity Solutions", 4],
        [1, "IoT Management Platform", 5],
        [1, "Developer Experience Tools", 6],
        [1, "Customer Success Stories", 7],
        [1, "Contact & Next Steps", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    # Check file size
    file_size = os.path.getsize(OUTPUT)
    print(f"Initial brochure created: {OUTPUT}")
    print(f"File size: {file_size / (1024*1024):.1f} MB")
    print(f"Target was ~85MB with 600 DPI images")

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
