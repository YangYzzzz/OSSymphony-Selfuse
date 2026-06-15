"""
Initial Setup: Create a large 50-page PDF report with high-resolution images
Task ID: pdf_ro_028
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/large_report.pdf'


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


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    from PIL import Image
    import numpy as np
    import pymupdf

    departments = [
        "Executive Summary", "Engineering", "Product Development",
        "Marketing & Sales", "Human Resources", "Finance & Accounting",
        "Operations", "Customer Success", "Research & Development",
        "Legal & Compliance"
    ]

    quarterly_data = [
        ("Q1 2025", "$12.4M", "+8.2%", "$9.1M", "$3.3M"),
        ("Q2 2025", "$14.1M", "+13.7%", "$10.2M", "$3.9M"),
        ("Q3 2025", "$15.8M", "+12.1%", "$11.0M", "$4.8M"),
        ("Q4 2025", "$18.2M", "+15.2%", "$12.5M", "$5.7M"),
    ]

    employee_names = [
        "Sarah Chen", "Marcus Johnson", "Elena Rodriguez", "David Kim",
        "Priya Patel", "James O'Brien", "Aisha Mohammed", "Robert Zhang",
        "Maria Santos", "William Turner", "Fatima Hassan", "Thomas Anderson",
        "Yuki Tanaka", "Carlos Mendez", "Jennifer Walsh", "Ahmed Al-Rashid",
        "Sophie Martin", "Raj Krishnamurthy", "Olivia Bennett", "Hassan Yilmaz",
    ]

    image_colors = [
        (41, 98, 164), (52, 131, 80), (178, 67, 52), (142, 96, 168),
        (189, 146, 42), (65, 140, 153), (168, 84, 118), (88, 122, 62),
        (176, 108, 52), (62, 78, 148),
    ]

    # 1400x1050 at 300 DPI = 4.7x3.5 inches
    # Use high-quality JPEG (quality=98) to still be large but more reasonable
    IMG_W, IMG_H = 1400, 1050

    print("Building PDF pages with embedded images...")
    doc = pymupdf.open()
    rng = np.random.RandomState(42)

    for page_idx in range(50):
        page = doc.new_page(width=612, height=792)

        dept = departments[page_idx % len(departments)]
        section_num = page_idx // len(departments) + 1

        # Header
        page.insert_text(
            pymupdf.Point(72, 50),
            "Nextera Technologies Inc. \u2014 Annual Report 2025",
            fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4),
        )
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(540, 58))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        if page_idx == 0:
            page.insert_text(pymupdf.Point(72, 100),
                "Annual Corporate Report \u2014 Fiscal Year 2025",
                fontsize=22, fontname="hebo", color=(0.16, 0.24, 0.45))
            page.insert_text(pymupdf.Point(72, 130),
                "Prepared by the Office of the Chief Financial Officer",
                fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 155),
                "Document Classification: Internal \u2014 Confidential",
                fontsize=10, fontname="helv", color=(0.5, 0.1, 0.1))
            y_start = 190
        else:
            page.insert_text(pymupdf.Point(72, 90),
                f"Section {section_num}: {dept} \u2014 Detailed Analysis",
                fontsize=16, fontname="hebo", color=(0.16, 0.24, 0.45))
            y_start = 120

        paragraphs = [
            f"During the fiscal year 2025, the {dept} division demonstrated significant progress across all key performance indicators. Revenue contributions increased by {8 + page_idx % 12}% compared to the prior year, driven primarily by strategic initiatives launched in Q2.",
            f"Team headcount grew from {20 + page_idx * 3} to {28 + page_idx * 3} full-time employees. Notable hires include {employee_names[page_idx % len(employee_names)]} as Senior Director and {employee_names[(page_idx + 7) % len(employee_names)]} as Principal Analyst.",
            f"Capital expenditures for the period totaled ${(1.2 + page_idx * 0.15):.1f}M, allocated across infrastructure upgrades ({40 + page_idx % 20}%), talent acquisition ({25 + page_idx % 10}%), and technology licensing ({35 - page_idx % 15}%).",
        ]

        rect_top = y_start
        for para in paragraphs:
            rect = pymupdf.Rect(72, rect_top, 540, rect_top + 60)
            page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            rect_top += 65

        # Generate image in memory as high-quality JPEG
        color = image_colors[page_idx % len(image_colors)]
        img_arr = np.zeros((IMG_H, IMG_W, 3), dtype=np.uint8)
        for c in range(3):
            base = color[c]
            gradient = np.linspace(base * 0.6, min(255, base * 1.4), IMG_W).astype(np.uint8)
            img_arr[:, :, c] = gradient[np.newaxis, :]
        v_grad = np.linspace(0.7, 1.3, IMG_H).reshape(-1, 1, 1)
        img_arr = np.clip(img_arr * v_grad, 0, 255).astype(np.uint8)
        noise = rng.randint(-15, 16, (IMG_H, IMG_W, 3), dtype=np.int16)
        img_arr = np.clip(img_arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        img = Image.fromarray(img_arr, 'RGB')
        buf = io.BytesIO()
        # Save as high-quality JPEG (DPI=300, quality=95) for large file
        img.save(buf, 'JPEG', quality=95, dpi=(300, 300))
        img_bytes = buf.getvalue()

        img_rect = pymupdf.Rect(72, rect_top + 10, 540, rect_top + 310)
        page.insert_image(img_rect, stream=img_bytes)

        caption_y = rect_top + 325
        page.insert_text(pymupdf.Point(72, caption_y),
            f"Figure {page_idx + 1}: {dept} Performance Metrics Visualization \u2014 High Resolution (300 DPI)",
            fontsize=8, fontname="heit", color=(0.3, 0.3, 0.3))

        q = quarterly_data[page_idx % 4]
        page.insert_text(pymupdf.Point(72, caption_y + 35),
            f"Period: {q[0]}  |  Revenue: {q[1]}  |  Growth: {q[2]}  |  Expenses: {q[3]}  |  Profit: {q[4]}",
            fontsize=9, fontname="cour", color=(0.2, 0.2, 0.2))

        page.insert_text(pymupdf.Point(72, 770), "Nextera Technologies Inc. \u2014 Confidential",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
        page.insert_text(pymupdf.Point(500, 770), f"Page {page_idx + 1} of 50",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

        if (page_idx + 1) % 10 == 0:
            print(f"  Built {page_idx + 1}/50 pages")

    doc.set_metadata({
        "title": "Nextera Technologies Inc. \u2014 Annual Report 2025",
        "author": "Office of the CFO",
        "subject": "Annual Corporate Report \u2014 Fiscal Year 2025",
        "keywords": "annual report, fiscal year, 2025, nextera, corporate",
        "creator": "Nextera Report Generator",
        "producer": "PyMuPDF",
    })

    toc = [[1, "Annual Corporate Report \u2014 Fiscal Year 2025", 1]]
    for i in range(1, 50):
        dept = departments[i % len(departments)]
        section_num = i // len(departments) + 1
        toc.append([2 if i % len(departments) != 0 else 1,
                     f"Section {section_num}: {dept}", i + 1])
    doc.set_toc(toc)

    doc.save(OUTPUT, garbage=0, deflate=False)
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'File size: {file_size / (1024 * 1024):.1f} MB')

    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
