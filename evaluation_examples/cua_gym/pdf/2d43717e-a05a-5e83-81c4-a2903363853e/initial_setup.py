"""
Initial Setup: Create a 10-page annual report PDF with 18 embedded images
Task ID: pdf_gf3_006
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_006'
REPORTS_DIR = f'{WORKDIR}/reports'
OUTPUT = f'{REPORTS_DIR}/annual_report.pdf'


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


def create_chart_image(width, height, title, chart_type, colors):
    """Create a simple chart-like image using Pillow."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient-like fill
    for y in range(height):
        r = int(245 + (255 - 245) * y / height)
        g = int(248 + (255 - 248) * y / height)
        b = int(252 + (255 - 252) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Title
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font = ImageFont.load_default()
        small_font = font

    draw.text((10, 8), title, fill=(33, 37, 41), font=font)

    if chart_type == 'bar':
        # Bar chart
        num_bars = len(colors)
        bar_width = (width - 80) // num_bars
        max_h = height - 80
        import random
        random.seed(hash(title) % 10000)
        values = [random.randint(30, 95) for _ in range(num_bars)]
        labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'][:num_bars]
        for i, (val, color) in enumerate(zip(values, colors)):
            x0 = 40 + i * bar_width + 5
            bar_h = int(val / 100 * (max_h - 40))
            y0 = height - 40 - bar_h
            draw.rectangle([x0, y0, x0 + bar_width - 10, height - 40], fill=color)
            draw.text((x0 + 5, height - 35), labels[i], fill=(80, 80, 80), font=small_font)

    elif chart_type == 'pie':
        # Pie chart
        cx, cy = width // 2, height // 2 + 10
        radius = min(width, height) // 3
        import random
        random.seed(hash(title) % 10000)
        slices = [random.randint(10, 40) for _ in range(len(colors))]
        total = sum(slices)
        start = 0
        for s, color in zip(slices, colors):
            end = start + (s / total) * 360
            draw.pieslice([cx - radius, cy - radius, cx + radius, cy + radius],
                          start=start, end=end, fill=color, outline=(255, 255, 255))
            start = end

    elif chart_type == 'line':
        # Line chart
        import random
        random.seed(hash(title) % 10000)
        points = [(40 + i * ((width - 80) // 9), height - 50 - random.randint(20, height - 100))
                  for i in range(10)]
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=colors[0], width=3)
        for pt in points:
            draw.ellipse([pt[0] - 4, pt[1] - 4, pt[0] + 4, pt[1] + 4], fill=colors[0])

    elif chart_type == 'photo':
        # Simulate a photo with colored rectangles and shapes
        import random
        random.seed(hash(title) % 10000)
        for _ in range(15):
            x0 = random.randint(10, width - 60)
            y0 = random.randint(40, height - 60)
            x1 = x0 + random.randint(20, 80)
            y1 = y0 + random.randint(20, 60)
            color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
            draw.rectangle([x0, y0, x1, y1], fill=color, outline=(30, 30, 30))

    # Border
    draw.rectangle([0, 0, width - 1, height - 1], outline=(200, 200, 200), width=1)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.read()


def create_initial():
    import pymupdf

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Make sure extracted_images does NOT exist
    extracted_dir = f'{REPORTS_DIR}/extracted_images'
    if os.path.exists(extracted_dir):
        import shutil
        shutil.rmtree(extracted_dir)

    doc = pymupdf.open()

    # Define image distribution across 10 pages (total 18 images)
    # Page 1: 3 images (cover page charts)
    # Page 2: 2 images
    # Page 3: 2 images
    # Page 4: 1 image
    # Page 5: 3 images
    # Page 6: 0 images (text-only page)
    # Page 7: 2 images
    # Page 8: 2 images
    # Page 9: 0 images (text-only page)
    # Page 10: 3 images
    # Total: 3+2+2+1+3+0+2+2+0+3 = 18

    image_specs = {
        0: [  # Page 1 - 3 images (smaller heights to fit)
            (400, 180, "Revenue Growth 2024", "bar", [(41, 128, 185), (52, 152, 219), (93, 173, 226), (163, 204, 233)]),
            (350, 160, "Market Share Distribution", "pie", [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15)]),
            (380, 170, "Annual Profit Trends", "line", [(155, 89, 182)]),
        ],
        1: [  # Page 2 - 2 images
            (420, 240, "Department Headcount", "bar", [(39, 174, 96), (46, 204, 113), (88, 214, 141)]),
            (350, 230, "Employee Satisfaction Survey", "pie", [(52, 152, 219), (231, 76, 60), (241, 196, 15), (46, 204, 113), (155, 89, 182)]),
        ],
        2: [  # Page 3 - 2 images
            (400, 240, "Quarterly Sales by Region", "bar", [(192, 57, 43), (211, 84, 0), (41, 128, 185), (39, 174, 96)]),
            (360, 230, "Customer Acquisition Cost", "line", [(231, 76, 60)]),
        ],
        3: [  # Page 4 - 1 image
            (440, 320, "Office Headquarters", "photo", []),
        ],
        4: [  # Page 5 - 3 images (smaller heights to fit)
            (380, 170, "Product Revenue Breakdown", "pie", [(52, 152, 219), (155, 89, 182), (241, 196, 15), (231, 76, 60), (46, 204, 113), (243, 156, 18)]),
            (400, 180, "Monthly Active Users", "line", [(41, 128, 185)]),
            (350, 160, "Support Ticket Volume", "bar", [(211, 84, 0), (243, 156, 18), (241, 196, 15), (248, 196, 113)]),
        ],
        5: [],  # Page 6 - no images
        6: [  # Page 7 - 2 images
            (400, 240, "R&D Investment Allocation", "pie", [(41, 128, 185), (39, 174, 96), (231, 76, 60), (155, 89, 182)]),
            (420, 240, "Patent Applications by Year", "bar", [(52, 73, 94), (93, 109, 126), (149, 165, 180)]),
        ],
        7: [  # Page 8 - 2 images
            (380, 230, "Cloud Infrastructure Costs", "line", [(243, 156, 18)]),
            (400, 240, "Team Photo - Engineering Retreat", "photo", []),
        ],
        8: [],  # Page 9 - no images
        9: [  # Page 10 - 3 images (smaller heights to fit)
            (420, 180, "2025 Revenue Projections", "bar", [(39, 174, 96), (46, 204, 113), (88, 214, 141), (163, 228, 182)]),
            (350, 170, "Strategic Priority Allocation", "pie", [(52, 152, 219), (231, 76, 60), (241, 196, 15), (46, 204, 113)]),
            (380, 170, "ESG Score Progression", "line", [(39, 174, 96)]),
        ],
    }

    page_titles = [
        "Meridian Technologies Inc. — Annual Report 2024",
        "Chapter 1: Human Resources Overview",
        "Chapter 2: Sales Performance Analysis",
        "Chapter 3: Corporate Culture & Facilities",
        "Chapter 4: Product & Technology Metrics",
        "Chapter 5: Governance & Compliance",
        "Chapter 6: Research & Development",
        "Chapter 7: Infrastructure & Operations",
        "Chapter 8: Sustainability & Social Impact",
        "Chapter 9: Forward-Looking Statements & Projections",
    ]

    page_texts = [
        "Meridian Technologies Inc. is pleased to present our Annual Report for fiscal year 2024. "
        "This year marked significant milestones across all business units, with consolidated revenue reaching "
        "$4.2 billion, representing a 15.3% year-over-year increase. Our commitment to innovation, "
        "sustainability, and employee well-being continues to drive our strategic objectives forward.",

        "Our workforce expanded to 12,847 employees across 23 global offices. Employee retention improved "
        "to 91.2%, up from 87.5% in 2023. The Learning & Development team delivered over 45,000 training "
        "hours, with particular emphasis on AI literacy and leadership development programs.",

        "Global sales performance exceeded targets by 8.2% in 2024. The Asia-Pacific region emerged as "
        "our fastest-growing market, with 28% revenue growth driven by enterprise cloud solutions. "
        "North American operations maintained steady performance with 12% growth in recurring revenue.",

        "Our new Silicon Valley campus, completed in March 2024, features state-of-the-art collaborative "
        "workspaces, an on-site wellness center, and LEED Platinum certification. The facility supports "
        "our hybrid work model, accommodating 3,500 employees with 60% average daily occupancy.",

        "The product portfolio generated $2.8 billion in subscription revenue, up 22% from the prior year. "
        "Monthly active users surpassed 15 million for the first time, while customer support response "
        "times improved by 35% following the deployment of our AI-assisted support platform.",

        "The Board of Directors maintained robust governance standards throughout 2024. Key activities "
        "included the adoption of enhanced cybersecurity protocols, updated whistleblower protection "
        "policies, and comprehensive third-party risk management frameworks. Regulatory compliance "
        "achieved 99.7% adherence across all jurisdictions.",

        "R&D investment totaled $680 million in 2024, representing 16.2% of total revenue. The team "
        "filed 127 new patent applications, bringing our total active patent portfolio to 1,842. Key "
        "breakthroughs included advances in federated learning, quantum-safe encryption, and edge "
        "computing architectures.",

        "Cloud infrastructure spending was optimized through a multi-cloud strategy, reducing per-unit "
        "compute costs by 18%. Data center operations achieved 99.99% uptime, with carbon-neutral "
        "operations across all three primary data centers. The engineering retreat brought together "
        "400 engineers for a week of innovation sprints and team building.",

        "Meridian's ESG score improved from 72 to 81 (out of 100) in 2024. Carbon emissions decreased "
        "by 23% through renewable energy procurement and operational efficiency. Community engagement "
        "programs contributed $12.5 million in grants and volunteer hours equivalent. Diversity metrics "
        "showed meaningful progress, with women representing 38% of leadership positions, up from 33%.",

        "Looking ahead to 2025, we project consolidated revenue of $4.8-5.1 billion, driven by expansion "
        "into healthcare AI, autonomous systems, and green technology markets. Strategic priorities include "
        "completing the European market expansion, launching three new product lines, and achieving carbon "
        "neutrality across our entire supply chain by Q4 2025.",
    ]

    for page_idx in range(10):
        page = doc.new_page(width=595, height=842)  # A4

        # Page header
        page.insert_text(
            pymupdf.Point(72, 50),
            page_titles[page_idx],
            fontsize=16 if page_idx == 0 else 13,
            fontname="hebo",
            color=(0.16, 0.24, 0.36),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(523, 58))
        shape.finish(color=(0.16, 0.24, 0.36), width=1.5)
        shape.commit()

        # Page body text
        text_rect = pymupdf.Rect(72, 70, 523, 200)
        page.insert_textbox(
            text_rect,
            page_texts[page_idx],
            fontsize=10,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Insert images for this page
        images = image_specs.get(page_idx, [])
        y_offset = 210
        for img_idx, (w, h, title, chart_type, colors) in enumerate(images):
            img_data = create_chart_image(w, h, title, chart_type, colors)

            # Calculate placement
            img_width = min(w, 450)
            scale = img_width / w
            img_height = int(h * scale)

            x0 = 72
            y0 = y_offset
            x1 = x0 + img_width
            y1 = y0 + img_height

            # If image would go off page, clamp
            if y1 > 800:
                y1 = 800
                img_height = y1 - y0

            # Skip if rect is degenerate
            if img_height < 10 or y0 >= y1:
                y_offset = y1 + 15
                continue

            img_rect = pymupdf.Rect(x0, y0, x1, y1)
            page.insert_image(img_rect, stream=img_data)

            y_offset = y1 + 15

        # Page number footer
        page.insert_text(
            pymupdf.Point(285, 830),
            f"— {page_idx + 1} —",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Technologies Inc. — Annual Report 2024",
        "author": "Meridian Technologies Inc.",
        "subject": "Annual Report",
        "keywords": "annual report, 2024, Meridian Technologies, financial, corporate",
        "creator": "Meridian Technologies Document Services",
    })

    # Add table of contents
    toc = [
        [1, "Annual Report 2024", 1],
        [1, "Human Resources Overview", 2],
        [1, "Sales Performance Analysis", 3],
        [1, "Corporate Culture & Facilities", 4],
        [1, "Product & Technology Metrics", 5],
        [1, "Governance & Compliance", 6],
        [1, "Research & Development", 7],
        [1, "Infrastructure & Operations", 8],
        [1, "Sustainability & Social Impact", 9],
        [1, "Forward-Looking Statements & Projections", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify image count
    verify_doc = pymupdf.open(OUTPUT)
    total_images = 0
    for i in range(verify_doc.page_count):
        imgs = verify_doc[i].get_images()
        total_images += len(imgs)
        print(f'  Page {i+1}: {len(imgs)} images')
    verify_doc.close()
    print(f'Total images embedded: {total_images}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
