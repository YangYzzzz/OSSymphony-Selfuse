"""
Initial Setup: Create a large 20-page PDF report with redundant objects and uncompressed streams.
Task ID: pdf_gf1_019
Domain: pdf
"""

import os
import io
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_019'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/large_report.pdf'


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


def create_large_image(width=800, height=600, color_seed=0):
    """Create a large uncompressed BMP-style image to inflate file size."""
    from PIL import Image, ImageDraw, ImageFont
    import random
    random.seed(color_seed)

    img = Image.new('RGB', (width, height),
                     (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)))
    draw = ImageDraw.Draw(img)

    # Draw random shapes to create visual complexity
    for _ in range(50):
        x1 = random.randint(0, width - 100)
        y1 = random.randint(0, height - 100)
        x2 = x1 + random.randint(20, 100)
        y2 = y1 + random.randint(20, 100)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        shape_type = random.choice(['rect', 'ellipse', 'line'])
        if shape_type == 'rect':
            draw.rectangle([x1, y1, x2, y2], fill=color, outline='black')
        elif shape_type == 'ellipse':
            draw.ellipse([x1, y1, x2, y2], fill=color, outline='black')
        else:
            draw.line([x1, y1, x2, y2], fill=color, width=3)

    # Add text overlay
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    draw.text((50, 50), f"Report Image #{color_seed + 1}", fill='black', font=font)

    # Return as uncompressed BMP bytes to maximize size
    buf = io.BytesIO()
    img.save(buf, format='BMP')
    buf.seek(0)
    return buf.read(), img


def create_initial():
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    doc = pymupdf.open()

    # Report content data
    departments = [
        "Engineering", "Marketing", "Sales", "Human Resources", "Finance",
        "Operations", "Research & Development", "Customer Support",
        "Legal", "Product Management"
    ]
    employees = [
        ("Sarah Chen", "Engineering", 125000, "Senior Software Engineer"),
        ("Marcus Johnson", "Marketing", 92000, "Marketing Director"),
        ("Emily Rodriguez", "Sales", 88000, "Regional Sales Manager"),
        ("David Kim", "Finance", 115000, "Financial Analyst"),
        ("Priya Patel", "Engineering", 135000, "Principal Engineer"),
        ("James Wilson", "Operations", 78000, "Operations Coordinator"),
        ("Aisha Mohammed", "R&D", 142000, "Research Scientist"),
        ("Robert Taylor", "Customer Support", 65000, "Support Team Lead"),
        ("Lisa Chang", "Legal", 155000, "Senior Legal Counsel"),
        ("Michael O'Brien", "Product Management", 128000, "Senior Product Manager"),
        ("Fatima Al-Rashid", "Engineering", 118000, "DevOps Engineer"),
        ("Carlos Mendoza", "Sales", 95000, "Enterprise Account Executive"),
        ("Jennifer Park", "Human Resources", 82000, "HR Business Partner"),
        ("Thomas Anderson", "Finance", 98000, "Senior Accountant"),
        ("Nina Volkov", "Marketing", 87000, "Content Strategy Manager"),
    ]

    quarterly_data = {
        "Q1 2025": {"Revenue": "$4,230,000", "Expenses": "$3,180,000", "Net Income": "$1,050,000", "Headcount": 342},
        "Q2 2025": {"Revenue": "$4,850,000", "Expenses": "$3,420,000", "Net Income": "$1,430,000", "Headcount": 358},
        "Q3 2025": {"Revenue": "$5,120,000", "Expenses": "$3,650,000", "Net Income": "$1,470,000", "Headcount": 371},
        "Q4 2025": {"Revenue": "$5,680,000", "Expenses": "$3,890,000", "Net Income": "$1,790,000", "Headcount": 385},
    }

    projects = [
        ("Project Atlas", "Engineering", "In Progress", "Q2 2026", "$1.2M"),
        ("Project Beacon", "R&D", "Planning", "Q4 2026", "$800K"),
        ("Project Catalyst", "Marketing", "Completed", "Q1 2025", "$350K"),
        ("Project Delta", "Operations", "In Progress", "Q3 2025", "$550K"),
        ("Project Echo", "Engineering", "On Hold", "TBD", "$950K"),
        ("Project Frontier", "Sales", "In Progress", "Q1 2026", "$420K"),
        ("Project Genesis", "Product", "Planning", "Q3 2026", "$1.5M"),
        ("Project Horizon", "R&D", "In Progress", "Q2 2026", "$2.1M"),
    ]

    # ---- Page creation ----

    for page_idx in range(20):
        page = doc.new_page(width=612, height=792)  # US Letter

        # Add header on every page
        page.insert_text(
            pymupdf.Point(72, 40),
            "Meridian Technologies Inc. — Annual Report 2025",
            fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3)
        )
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 48), pymupdf.Point(540, 48))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()

        # Footer
        page.insert_text(
            pymupdf.Point(72, 775),
            f"Page {page_idx + 1} of 20  |  Confidential — Internal Use Only",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5)
        )

        if page_idx == 0:
            # Title page
            page.insert_text(pymupdf.Point(150, 250), "ANNUAL REPORT", fontsize=36, fontname="hebo", color=(0, 0.2, 0.5))
            page.insert_text(pymupdf.Point(200, 300), "Fiscal Year 2025", fontsize=24, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(150, 380), "Meridian Technologies Inc.", fontsize=18, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(150, 410), "1200 Innovation Drive, Suite 500", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(150, 430), "San Francisco, CA 94105", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(150, 470), "Prepared by: Office of the CFO", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(150, 490), "Date: March 15, 2026", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))

            # Decorative shapes
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(72, 200, 540, 210))
            shape.finish(color=(0, 0.2, 0.5), fill=(0, 0.2, 0.5), width=0)
            shape.draw_rect(pymupdf.Rect(72, 520, 540, 525))
            shape.finish(color=(0, 0.2, 0.5), fill=(0, 0.2, 0.5), width=0)
            shape.commit()

        elif page_idx == 1:
            # Table of Contents
            page.insert_text(pymupdf.Point(72, 80), "Table of Contents", fontsize=22, fontname="hebo", color=(0, 0.2, 0.5))
            toc_items = [
                ("1. Executive Summary", 3), ("2. Financial Overview", 4),
                ("3. Quarterly Performance", 6), ("4. Employee Directory", 8),
                ("5. Project Portfolio", 10), ("6. Department Analysis", 12),
                ("7. Risk Assessment", 14), ("8. Market Analysis", 16),
                ("9. Technology Infrastructure", 18), ("10. Appendices", 20),
            ]
            y = 120
            for title, pg in toc_items:
                page.insert_text(pymupdf.Point(90, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(480, y), f"........ {pg}", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
                y += 28

        elif page_idx == 2:
            # Executive Summary
            page.insert_text(pymupdf.Point(72, 80), "1. Executive Summary", fontsize=20, fontname="hebo", color=(0, 0.2, 0.5))
            summary_text = (
                "Meridian Technologies Inc. delivered exceptional results in fiscal year 2025, "
                "achieving record revenue of $19.88 million, representing a 23% year-over-year increase. "
                "Our strategic investments in cloud infrastructure and artificial intelligence research "
                "have positioned the company for sustained growth in the coming fiscal year.\n\n"
                "Key highlights include the successful launch of Project Atlas, which expanded our "
                "enterprise client base by 40%, and the completion of Project Catalyst, which streamlined "
                "our marketing operations and reduced customer acquisition costs by 18%.\n\n"
                "The company's headcount grew from 342 to 385 employees, a 12.6% increase, reflecting "
                "our continued investment in human capital. Employee retention rates remained strong at "
                "91%, well above the industry average of 82%.\n\n"
                "Looking ahead to FY2026, we anticipate continued momentum driven by expanding market "
                "opportunities in edge computing, sustainability-focused technology solutions, and our "
                "growing presence in the Asia-Pacific region. We have budgeted $6.5 million for R&D "
                "initiatives that will shape our product roadmap for the next three years."
            )
            rect = pymupdf.Rect(72, 100, 540, 700)
            page.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

        elif page_idx in (3, 4, 5):
            # Financial Overview / Quarterly Performance (pages 4-6)
            section_num = page_idx + 1
            if page_idx == 3:
                title = "2. Financial Overview"
            elif page_idx == 4:
                title = "2. Financial Overview (continued)"
            else:
                title = "3. Quarterly Performance"
            page.insert_text(pymupdf.Point(72, 80), title, fontsize=20, fontname="hebo", color=(0, 0.2, 0.5))

            y = 120
            for quarter, data in quarterly_data.items():
                page.insert_text(pymupdf.Point(90, y), quarter, fontsize=14, fontname="hebo", color=(0, 0, 0))
                y += 22
                for key, val in data.items():
                    page.insert_text(pymupdf.Point(110, y), f"{key}:", fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
                    page.insert_text(pymupdf.Point(250, y), str(val), fontsize=11, fontname="helv", color=(0, 0, 0))
                    y += 18
                y += 12

            # Additional filler text
            filler = (
                "The financial performance metrics presented above demonstrate consistent quarter-over-quarter "
                "improvement across all key indicators. Revenue growth was primarily driven by expansion in "
                "our enterprise software segment, which accounted for 62% of total revenue. Operating margins "
                "improved from 24.8% in Q1 to 31.5% in Q4, reflecting the scalability of our platform "
                "architecture and ongoing cost optimization initiatives across all departments."
            )
            rect = pymupdf.Rect(72, y + 10, 540, 750)
            page.insert_textbox(rect, filler, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

        elif page_idx in (6, 7, 8, 9):
            # Employee Directory (pages 7-10)
            sub = page_idx - 6
            page.insert_text(pymupdf.Point(72, 80), f"4. Employee Directory (Part {sub + 1})", fontsize=20, fontname="hebo", color=(0, 0.2, 0.5))

            # Table headers
            y = 115
            headers = ["Name", "Department", "Salary", "Title"]
            x_positions = [80, 200, 310, 390]
            for i, h in enumerate(headers):
                page.insert_text(pymupdf.Point(x_positions[i], y), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

            # Header background
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(72, y - 12, 540, y + 5))
            shape.finish(color=(0, 0.2, 0.5), fill=(0, 0.2, 0.5), width=0)
            shape.commit()

            y += 20
            start_idx = sub * 4
            for emp in employees[start_idx:start_idx + 4]:
                name, dept, salary, title = emp
                page.insert_text(pymupdf.Point(x_positions[0], y), name, fontsize=9, fontname="helv", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(x_positions[1], y), dept, fontsize=9, fontname="helv", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(x_positions[2], y), f"${salary:,}", fontsize=9, fontname="helv", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(x_positions[3], y), title, fontsize=9, fontname="helv", color=(0, 0, 0))
                y += 18

            # Add additional detail paragraphs to fill page
            detail_text = (
                f"Department performance metrics for the employees listed above show an average "
                f"productivity index of {88 + sub * 2}% for the reporting period. Training completion "
                f"rates averaged {92 + sub}%, with all listed employees meeting or exceeding their "
                f"annual professional development requirements. The department heads have submitted "
                f"positive performance evaluations for Q4 2025, noting particular strength in "
                f"cross-functional collaboration and project delivery timelines.\n\n"
                f"Compensation analysis indicates that current salary levels are competitive within "
                f"the 75th percentile of industry benchmarks for the San Francisco Bay Area market. "
                f"Total compensation including equity grants, performance bonuses, and benefits "
                f"packages positions Meridian Technologies favorably against peer companies."
            )
            rect = pymupdf.Rect(72, y + 20, 540, 750)
            page.insert_textbox(rect, detail_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

        elif page_idx in (10, 11):
            # Project Portfolio (pages 11-12)
            page.insert_text(pymupdf.Point(72, 80), f"5. Project Portfolio (Part {page_idx - 9})", fontsize=20, fontname="hebo", color=(0, 0.2, 0.5))

            y = 115
            start = (page_idx - 10) * 4
            for proj in projects[start:start + 4]:
                name, dept, status, deadline, budget = proj
                page.insert_text(pymupdf.Point(90, y), name, fontsize=13, fontname="hebo", color=(0, 0.15, 0.4))
                y += 18
                page.insert_text(pymupdf.Point(110, y), f"Department: {dept}  |  Status: {status}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 16
                page.insert_text(pymupdf.Point(110, y), f"Deadline: {deadline}  |  Budget: {budget}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 16
                desc = (
                    f"This initiative focuses on delivering strategic capabilities aligned with "
                    f"the company's long-term technology roadmap. Current progress is on track with "
                    f"key milestones being met according to the established timeline."
                )
                rect = pymupdf.Rect(110, y, 530, y + 50)
                page.insert_textbox(rect, desc, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                y += 65

        else:
            # Remaining pages: Department Analysis, Risk Assessment, Market Analysis, etc.
            section_titles = {
                12: "6. Department Analysis",
                13: "6. Department Analysis (continued)",
                14: "7. Risk Assessment",
                15: "7. Risk Assessment (continued)",
                16: "8. Market Analysis",
                17: "8. Market Analysis (continued)",
                18: "9. Technology Infrastructure",
                19: "10. Appendices",
            }
            title = section_titles.get(page_idx, f"Section {page_idx + 1}")
            page.insert_text(pymupdf.Point(72, 80), title, fontsize=20, fontname="hebo", color=(0, 0.2, 0.5))

            # Rich text content for each page
            content_blocks = {
                12: (
                    "The Engineering department continues to be the primary growth driver, with a 28% "
                    "increase in output measured by lines of code shipped, pull requests merged, and "
                    "production deployments completed. The team successfully migrated 85% of legacy "
                    "services to our new microservices architecture, reducing average deployment time "
                    "from 45 minutes to under 8 minutes.\n\n"
                    "Marketing achieved a 35% increase in qualified leads through improved content "
                    "strategy and targeted advertising campaigns. The cost per acquisition decreased "
                    "by 22% while conversion rates improved from 3.2% to 4.8%."
                ),
                13: (
                    "Sales exceeded annual targets by 15%, closing 127 enterprise deals worth a combined "
                    "$8.4 million in annual recurring revenue. The sales cycle length decreased from an "
                    "average of 68 days to 52 days, attributed to improved product demos and streamlined "
                    "procurement processes.\n\n"
                    "Human Resources implemented a new employee wellness program that reduced turnover "
                    "by 6 percentage points. The recruitment team filled 95% of open positions within "
                    "the target timeline of 45 days, with diversity hires representing 42% of new employees."
                ),
                14: (
                    "RISK ASSESSMENT MATRIX\n\n"
                    "Category: Cybersecurity\n"
                    "Severity: High | Likelihood: Medium | Mitigation: SOC 2 Type II compliance, "
                    "quarterly penetration testing, employee security awareness training\n\n"
                    "Category: Market Competition\n"
                    "Severity: Medium | Likelihood: High | Mitigation: Accelerated R&D investment, "
                    "strategic partnerships, patent portfolio expansion\n\n"
                    "Category: Regulatory Compliance\n"
                    "Severity: High | Likelihood: Low | Mitigation: Dedicated compliance team, "
                    "automated monitoring tools, external legal counsel engagement"
                ),
                15: (
                    "Category: Supply Chain Disruption\n"
                    "Severity: Medium | Likelihood: Medium | Mitigation: Multi-vendor strategy, "
                    "inventory buffer management, geographic diversification of suppliers\n\n"
                    "Category: Talent Retention\n"
                    "Severity: High | Likelihood: Medium | Mitigation: Competitive compensation "
                    "packages, career development programs, flexible work arrangements, equity refresh "
                    "grants for high performers\n\n"
                    "Category: Technology Obsolescence\n"
                    "Severity: Medium | Likelihood: Low | Mitigation: Continuous technology assessment, "
                    "modular architecture design, regular platform upgrades and migrations"
                ),
                16: (
                    "The global enterprise software market is projected to reach $650 billion by 2027, "
                    "growing at a CAGR of 11.3%. Meridian Technologies is well-positioned to capture "
                    "an increasing share of this market through our differentiated platform capabilities.\n\n"
                    "Key market trends include the acceleration of digital transformation initiatives "
                    "across all industry verticals, increasing demand for AI-powered automation tools, "
                    "and the shift toward cloud-native architectures. Our product roadmap aligns closely "
                    "with these trends, particularly in the areas of intelligent process automation "
                    "and real-time analytics."
                ),
                17: (
                    "Competitive landscape analysis reveals three primary competitors in our core market "
                    "segment. Our differentiation strategy focuses on superior integration capabilities, "
                    "enterprise-grade security features, and a developer-first platform experience.\n\n"
                    "Geographic expansion opportunities have been identified in the APAC region, "
                    "specifically in Japan, South Korea, and Australia, where enterprise software "
                    "adoption rates are growing at 15-20% annually. We plan to establish regional "
                    "offices in Tokyo and Sydney by Q3 2026."
                ),
                18: (
                    "INFRASTRUCTURE OVERVIEW\n\n"
                    "Cloud Provider: AWS (primary), Azure (secondary/DR)\n"
                    "Total compute capacity: 2,400 vCPUs across 3 regions\n"
                    "Data storage: 450 TB managed across S3, EBS, and RDS\n"
                    "Average monthly cloud spend: $185,000\n"
                    "Uptime SLA achievement: 99.97% (target: 99.95%)\n\n"
                    "Security certifications: SOC 2 Type II, ISO 27001, HIPAA\n"
                    "Disaster recovery RTO: 4 hours (actual tested: 2.5 hours)\n"
                    "Backup frequency: Continuous replication with 15-minute RPO\n\n"
                    "The technology infrastructure team completed a major upgrade cycle in Q3 2025, "
                    "migrating core services to Kubernetes-based container orchestration."
                ),
                19: (
                    "APPENDIX A: Financial Statements Detail\n"
                    "Complete audited financial statements are available upon request from the "
                    "Office of the CFO. Contact: finance@meridiantech.com\n\n"
                    "APPENDIX B: Board of Directors\n"
                    "Dr. Alexandra Whitfield (Chair), Jonathan Reeves (CEO), Maria Santos (CFO), "
                    "Dr. Kenneth Park (CTO), Rachel Goldberg (Independent), Samuel Okonkwo (Independent)\n\n"
                    "APPENDIX C: Glossary of Terms\n"
                    "ARR: Annual Recurring Revenue\n"
                    "CAGR: Compound Annual Growth Rate\n"
                    "CAC: Customer Acquisition Cost\n"
                    "LTV: Lifetime Value\n"
                    "NPS: Net Promoter Score\n"
                    "RPO: Recovery Point Objective\n"
                    "RTO: Recovery Time Objective\n"
                    "SLA: Service Level Agreement"
                ),
            }

            text = content_blocks.get(page_idx, "Additional content and analysis for this section.")
            rect = pymupdf.Rect(72, 110, 540, 750)
            page.insert_textbox(rect, text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

        # Embed a large image on selected pages to increase file size
        # We embed on most pages to reach ~15MB target
        if page_idx >= 2:
            from PIL import Image as PILImage
            bmp_data, pil_img = create_large_image(640, 480, color_seed=page_idx)
            # Convert to uncompressed PNG (larger than JPEG)
            png_buf = io.BytesIO()
            pil_img.save(png_buf, format='PNG', compress_level=0)
            png_bytes = png_buf.getvalue()

            # Place image near bottom of page
            img_rect = pymupdf.Rect(120, 580, 490, 760)
            if page_idx in (6, 7, 8, 9):
                img_rect = pymupdf.Rect(120, 550, 490, 730)
            if page_idx == 0:
                img_rect = pymupdf.Rect(150, 530, 460, 680)

            page.insert_image(img_rect, stream=png_bytes)

    # Set document metadata (deliberately verbose/redundant to add to size)
    doc.set_metadata({
        "title": "Meridian Technologies Inc. Annual Report FY2025",
        "author": "Office of the Chief Financial Officer",
        "subject": "Comprehensive Annual Financial and Operational Performance Report",
        "keywords": "meridian, technologies, annual, report, 2025, financial, performance, "
                    "revenue, employees, engineering, marketing, sales, operations, R&D, "
                    "enterprise, software, cloud, infrastructure, AI, machine learning, "
                    "digital transformation, quarterly, analysis, risk, assessment, market",
        "creator": "Meridian Report Generator v3.2.1",
        "producer": "PyMuPDF Document Services",
    })

    # Set Table of Contents / bookmarks
    toc = [
        [1, "Executive Summary", 3],
        [1, "Financial Overview", 4],
        [1, "Quarterly Performance", 6],
        [1, "Employee Directory", 7],
        [1, "Project Portfolio", 11],
        [1, "Department Analysis", 13],
        [1, "Risk Assessment", 15],
        [1, "Market Analysis", 17],
        [1, "Technology Infrastructure", 19],
        [1, "Appendices", 20],
    ]
    doc.set_toc(toc)

    # Save WITHOUT deflate compression to keep the file large
    doc.save(OUTPUT, deflate=False, garbage=0)
    doc.close()

    # Now re-open and duplicate some images / inflate further using pikepdf
    # to add redundant objects
    import pikepdf
    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)

    # Add duplicate metadata streams to inflate file size
    # Add redundant XMP metadata
    with pdf.open_metadata() as meta:
        meta["dc:title"] = "Meridian Technologies Inc. Annual Report FY2025"
        meta["dc:creator"] = ["Office of the Chief Financial Officer"]
        meta["dc:description"] = (
            "Comprehensive annual report covering financial performance, operational metrics, "
            "employee statistics, project portfolio status, risk assessment, market analysis, "
            "and technology infrastructure review for Meridian Technologies Inc. fiscal year 2025. "
            "This document contains confidential business information intended for internal "
            "distribution only. Unauthorized reproduction or distribution is prohibited."
        )
        meta["dc:subject"] = ["Annual Report", "Financial", "Technology", "Enterprise"]
        meta["xmp:CreatorTool"] = "Meridian Report Generator v3.2.1"
        meta["pdf:Producer"] = "pikepdf/PyMuPDF Dual Pipeline"
        meta["pdf:Keywords"] = (
            "meridian technologies annual report 2025 financial performance revenue "
            "engineering marketing sales operations research development enterprise "
            "software cloud infrastructure artificial intelligence machine learning"
        )

    # Save without compression to maintain large file size
    pdf.save(OUTPUT, compress_streams=False, object_stream_mode=pikepdf.ObjectStreamMode.disable)

    file_size = os.path.getsize(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'File size: {file_size / (1024*1024):.2f} MB')
    print(f'Target: ~15 MB')

    # Open the PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
