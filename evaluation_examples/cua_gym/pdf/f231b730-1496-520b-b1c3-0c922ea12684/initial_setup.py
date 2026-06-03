"""
Initial Setup: Create a large 100-page PDF report with high-resolution images
Task ID: pdf_aw_020
Domain: pdf

Creates /home/user/web/large_report.pdf — a non-linearized, ~85MB document
with 300+ DPI images, suitable for the web optimization task.
"""

import os
import shlex
import subprocess
import time
import io
import struct
import zlib

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_020'
OUTPUT_DIR = f'{WORKDIR}/web'
OUTPUT = f'{OUTPUT_DIR}/large_report.pdf'


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


def create_high_res_png(width, height, seed):
    """Create a high-resolution PNG image in memory with varied content.
    Returns PNG bytes. Uses raw Python (no PIL dependency needed)."""
    import random
    random.seed(seed)

    # Create pixel data with gradients and patterns for visual variety
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # filter byte: None
        for x in range(width):
            # Create a gradient/pattern based on seed for visual variety
            r = int((x / width) * 200 + random.randint(0, 55)) % 256
            g = int((y / height) * 180 + (seed * 37) % 76) % 256
            b = int(((x + y) / (width + height)) * 220 + (seed * 53) % 36) % 256
            raw_data.extend([r, g, b])

    # Build PNG file
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + chunk + crc

    png = b'\x89PNG\r\n\x1a\n'
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png += make_chunk(b'IHDR', ihdr_data)
    # IDAT
    compressed = zlib.compress(bytes(raw_data), 1)  # low compression for larger size
    png += make_chunk(b'IDAT', compressed)
    # IEND
    png += make_chunk(b'IEND', b'')
    return png


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    doc = pymupdf.open()

    # Report content sections for realistic variety
    chapters = [
        ("Executive Summary", [
            "This comprehensive annual report presents the financial performance, strategic initiatives, and operational achievements of Meridian Global Holdings for the fiscal year ending December 31, 2025.",
            "Total revenue reached $4.87 billion, representing a 12.3% increase year-over-year. Operating margins improved to 18.7%, driven by efficiency gains across all business segments.",
            "Key highlights include the successful integration of the Apex Technologies acquisition, expansion into three new international markets, and the launch of our next-generation product platform.",
        ]),
        ("Financial Performance", [
            "Revenue Analysis: The company reported consolidated revenues of $4,872 million for the fiscal year, compared to $4,338 million in the prior year. This growth was primarily driven by strong performance in the Enterprise Solutions segment (+15.2%) and Digital Services segment (+18.9%).",
            "Cost of revenues increased to $3,145 million from $2,890 million, reflecting higher input costs and investments in delivery capabilities. Gross profit margin improved to 35.4% from 33.4%.",
            "Operating expenses were $1,285 million, including $342 million in research and development expenditures. SG&A expenses were managed at $943 million, demonstrating cost discipline.",
        ]),
        ("Market Analysis", [
            "The global technology services market grew at an estimated 8.5% CAGR during the period. Meridian outpaced market growth in all key segments, gaining 1.2 percentage points of market share.",
            "Regional performance: North America contributed 52% of total revenue ($2,533M), Europe accounted for 28% ($1,364M), and Asia-Pacific represented 20% ($975M).",
            "Competitive positioning improved significantly with the launch of MeridianOne platform, which achieved 2,400 enterprise client deployments within the first nine months.",
        ]),
        ("Operations Review", [
            "Global headcount increased to 34,500 employees across 42 countries. Employee retention rate improved to 91.3%, above industry benchmark of 85.7%.",
            "Infrastructure investments totaled $567 million, including new data centers in Singapore, Frankfurt, and Sao Paulo. Network uptime achieved 99.97% across all facilities.",
            "Supply chain optimization initiatives reduced procurement costs by $89 million while improving delivery timelines by an average of 2.3 business days.",
        ]),
        ("Technology & Innovation", [
            "R&D investment of $342 million funded 47 active research programs across artificial intelligence, quantum computing, edge processing, and cybersecurity domains.",
            "Patent portfolio expanded to 3,847 active patents globally, with 312 new patents granted during the fiscal year. Licensing revenue from intellectual property reached $127 million.",
            "The MeridianLabs division launched 14 new products and 23 major feature updates, maintaining a product release cadence that exceeded planned targets by 18%.",
        ]),
        ("Sustainability Report", [
            "Carbon emissions reduced by 23% year-over-year, achieving 67% of our 2030 net-zero commitment. Renewable energy now powers 78% of global operations.",
            "Water usage efficiency improved by 15% through closed-loop cooling systems in data centers. Total water consumption decreased to 2.1 million cubic meters.",
            "Diversity metrics: Women represent 38% of leadership positions (up from 34%), and underrepresented minorities comprise 27% of the US workforce.",
        ]),
        ("Risk Management", [
            "Enterprise risk framework was enhanced with real-time monitoring capabilities. 94 risk scenarios are actively tracked across cybersecurity, regulatory, operational, and financial categories.",
            "Cybersecurity posture: Zero critical breaches recorded. Mean time to detect threats reduced to 4.2 minutes. Security operations center processes 2.7 billion events daily.",
            "Regulatory compliance maintained across all 42 operating jurisdictions. No material regulatory actions or penalties during the reporting period.",
        ]),
        ("Corporate Governance", [
            "Board of Directors comprises 11 members, with 9 independent directors. Three new board members were appointed, bringing expertise in AI governance, international trade, and sustainability.",
            "Executive compensation was restructured to align 60% of variable pay with long-term performance metrics including ESG targets, customer satisfaction, and innovation benchmarks.",
            "Shareholder engagement: Management conducted 187 investor meetings during the year. Annual General Meeting attendance reached 72% of outstanding shares.",
        ]),
        ("Outlook & Strategy", [
            "For fiscal year 2026, the company projects revenue growth of 10-13%, driven by continued momentum in Enterprise Solutions and anticipated contributions from new product launches.",
            "Strategic priorities include: (1) Accelerate AI integration across all product lines, (2) Expand presence in emerging markets, (3) Achieve 50% recurring revenue mix, (4) Advance sustainability targets.",
            "Capital allocation plan includes $400M in R&D investment, $350M in infrastructure, and $600M in shareholder returns through dividends and share repurchases.",
        ]),
        ("Appendix & Data Tables", [
            "This section contains detailed financial statements, segment breakdowns, regional performance data, and supplementary disclosures as required by applicable accounting standards.",
            "All figures are presented in US dollars unless otherwise noted. Prior period comparatives have been restated where applicable to reflect current period presentation.",
            "Independent auditor Ernst & Young LLP has issued an unqualified opinion on the consolidated financial statements for the year ended December 31, 2025.",
        ]),
    ]

    # Generate high-res images (300 DPI equivalent)
    # At 300 DPI, a 4x3 inch image = 1200x900 pixels
    # We create several large images that will be reused across pages to build up file size
    print("Generating high-resolution images...")
    image_cache = []
    for i in range(10):
        # Create 1200x900 pixel images (300 DPI at ~4x3 inches)
        png_bytes = create_high_res_png(1200, 900, seed=i * 42 + 7)
        image_cache.append(png_bytes)
        print(f"  Image {i+1}/10: {len(png_bytes)} bytes")

    print("Building 100-page PDF document...")

    for page_idx in range(100):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Determine chapter and section
        chapter_idx = page_idx // 10
        section_in_chapter = page_idx % 10

        if chapter_idx < len(chapters):
            chapter_title, paragraphs = chapters[chapter_idx]
        else:
            chapter_title = f"Supplementary Data Section {chapter_idx - len(chapters) + 1}"
            paragraphs = [
                f"This section contains additional data tables and analysis for reference period Q{(page_idx % 4) + 1} 2025.",
                f"Regional breakdown shows performance metrics across {42 + page_idx % 15} operational territories with detailed variance analysis.",
                f"Year-over-year comparison demonstrates consistent improvement in key performance indicators tracked by the executive leadership team.",
            ]

        y_pos = 72  # Start 1 inch from top

        # Page header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(540, 50))
        shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
        shape.commit()

        page.insert_text(
            pymupdf.Point(72, 45),
            "MERIDIAN GLOBAL HOLDINGS — ANNUAL REPORT 2025",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )
        page.insert_text(
            pymupdf.Point(480, 45),
            f"Page {page_idx + 1}",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Chapter title on first page of each chapter
        if section_in_chapter == 0:
            page.insert_text(
                pymupdf.Point(72, y_pos + 20),
                f"Chapter {chapter_idx + 1}",
                fontsize=12,
                fontname="helv",
                color=(0.3, 0.3, 0.7),
            )
            y_pos += 30
            page.insert_text(
                pymupdf.Point(72, y_pos + 20),
                chapter_title,
                fontsize=22,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y_pos += 45

            # Decorative line under title
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(72, y_pos), pymupdf.Point(300, y_pos))
            shape2.finish(color=(0.2, 0.4, 0.8), width=2)
            shape2.commit()
            y_pos += 15
        else:
            # Section subtitle
            page.insert_text(
                pymupdf.Point(72, y_pos + 15),
                f"{chapter_title} — Section {section_in_chapter + 1}",
                fontsize=14,
                fontname="hebo",
                color=(0.2, 0.2, 0.5),
            )
            y_pos += 35

        # Insert high-resolution image on most pages
        if section_in_chapter < 8:  # 80% of pages get an image
            img_idx = (page_idx * 3 + section_in_chapter) % len(image_cache)
            img_rect = pymupdf.Rect(72, y_pos, 540, y_pos + 180)
            page.insert_image(img_rect, stream=image_cache[img_idx])
            y_pos += 195

        # Text content
        for p_idx, para in enumerate(paragraphs):
            if y_pos > 700:
                break
            text_rect = pymupdf.Rect(72, y_pos, 540, y_pos + 80)
            excess = page.insert_textbox(
                text_rect,
                para,
                fontsize=10,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            y_pos += 85

        # Add some data table content on specific pages
        if section_in_chapter in [2, 5, 8]:
            if y_pos < 620:
                # Simple table header
                page.insert_text(
                    pymupdf.Point(72, y_pos + 12),
                    "Performance Metrics Summary",
                    fontsize=11,
                    fontname="hebo",
                    color=(0.1, 0.1, 0.3),
                )
                y_pos += 25

                # Table data
                table_data = [
                    ["Metric", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"],
                    ["Revenue ($M)", "1,142", "1,198", "1,243", "1,289"],
                    ["EBITDA ($M)", "213", "228", "241", "256"],
                    ["Margin (%)", "18.7%", "19.0%", "19.4%", "19.9%"],
                    ["Headcount", "33,200", "33,800", "34,100", "34,500"],
                ]
                for row_idx, row in enumerate(table_data):
                    for col_idx, cell in enumerate(row):
                        x = 72 + col_idx * 94
                        fontname = "hebo" if row_idx == 0 else "helv"
                        color = (1, 1, 1) if row_idx == 0 else (0.1, 0.1, 0.1)

                        if row_idx == 0:
                            # Header background
                            shape3 = page.new_shape()
                            shape3.draw_rect(pymupdf.Rect(x - 2, y_pos - 2, x + 92, y_pos + 14))
                            shape3.finish(fill=(0.2, 0.3, 0.6))
                            shape3.commit()

                        page.insert_text(
                            pymupdf.Point(x, y_pos + 10),
                            cell,
                            fontsize=9,
                            fontname=fontname,
                            color=color,
                        )
                    y_pos += 16

        # Footer
        shape4 = page.new_shape()
        shape4.draw_line(pymupdf.Point(72, 755), pymupdf.Point(540, 755))
        shape4.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape4.commit()
        page.insert_text(
            pymupdf.Point(72, 770),
            "Confidential — Meridian Global Holdings, Inc. All rights reserved.",
            fontsize=7,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

        if (page_idx + 1) % 10 == 0:
            print(f"  Built page {page_idx + 1}/100")

    # Add table of contents / bookmarks
    toc = []
    for i, (title, _) in enumerate(chapters):
        toc.append([1, f"Chapter {i+1}: {title}", i * 10 + 1])
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Global Holdings Annual Report 2025",
        "author": "Meridian Global Holdings, Inc.",
        "subject": "Annual Financial and Operational Report",
        "keywords": "annual report, financial, 2025, meridian, holdings",
        "creator": "Meridian Report Generator",
        "producer": "PyMuPDF",
    })

    # Save WITHOUT linearization (the task is to linearize it)
    doc.save(OUTPUT, deflate=False)  # No compression deflation for larger file
    doc.close()

    file_size = os.path.getsize(OUTPUT)
    print(f"Initial file created: {OUTPUT}")
    print(f"File size: {file_size / (1024*1024):.1f} MB")
    print(f"Pages: 100")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
