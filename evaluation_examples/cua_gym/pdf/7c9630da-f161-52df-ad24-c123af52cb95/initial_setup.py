"""
Initial Setup: Create a 50-page unencrypted user manual PDF
Task ID: pdf_mbc_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_015'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/shared_manual.pdf'


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


# Chapter structure for a realistic 50-page user manual
# 10 chapters + 38 sections = 48 content pages + 2 front matter = 50 pages
CHAPTERS = [
    ("Chapter 1: Introduction", [
        "1.1 Purpose of This Manual",
        "1.2 System Requirements",
        "1.3 Getting Started",
        "1.4 Support and Resources",
    ]),
    ("Chapter 2: Installation", [
        "2.1 Download and Setup",
        "2.2 Configuration Wizard",
        "2.3 License Activation",
        "2.4 Verifying Installation",
    ]),
    ("Chapter 3: User Interface Overview", [
        "3.1 Dashboard Layout",
        "3.2 Navigation Panel",
        "3.3 Toolbar Reference",
        "3.4 Status Bar Indicators",
    ]),
    ("Chapter 4: Data Management", [
        "4.1 Importing Data",
        "4.2 Exporting Reports",
        "4.3 Database Connections",
        "4.4 Backup and Recovery",
    ]),
    ("Chapter 5: Advanced Features", [
        "5.1 Scripting and Automation",
        "5.2 Custom Workflows",
        "5.3 API Integration",
        "5.4 Plugin Management",
    ]),
    ("Chapter 6: User Administration", [
        "6.1 Role-Based Access Control",
        "6.2 Creating User Accounts",
        "6.3 Permission Templates",
        "6.4 Audit Logging",
    ]),
    ("Chapter 7: Troubleshooting", [
        "7.1 Common Error Messages",
        "7.2 Performance Optimization",
        "7.3 Network Diagnostics",
        "7.4 Log File Analysis",
    ]),
    ("Chapter 8: Security Configuration", [
        "8.1 Encryption Settings",
        "8.2 Two-Factor Authentication",
        "8.3 SSL Certificate Management",
    ]),
    ("Chapter 9: Reporting and Analytics", [
        "9.1 Built-in Report Templates",
        "9.2 Custom Report Builder",
        "9.3 Scheduling Reports",
    ]),
    ("Chapter 10: Appendices", [
        "10.1 Glossary of Terms",
        "10.2 Compliance Standards",
        "10.3 Contact Information",
    ]),
]

# Realistic paragraph content for sections
SECTION_PARAGRAPHS = [
    "This section provides detailed guidance on configuring and managing the system "
    "components. Administrators should review these settings carefully before deploying "
    "to production environments. All configuration changes are logged automatically and "
    "can be audited through the management console.",

    "The platform supports integration with third-party services through a standardized "
    "REST API. Authentication tokens can be generated from the Security Settings panel. "
    "Rate limiting is enforced at 1000 requests per minute per API key to ensure fair "
    "usage across all connected applications.",

    "When working with large datasets, it is recommended to use the batch processing "
    "mode. This optimizes memory usage and reduces the total processing time by up to "
    "60%. Batch jobs can be scheduled during off-peak hours using the built-in task "
    "scheduler available under Tools > Batch Processing.",

    "Users with administrative privileges can create custom workflows using the visual "
    "workflow designer. Each workflow consists of triggers, conditions, and actions that "
    "execute automatically based on predefined criteria. Workflows can be exported as "
    "JSON templates and shared across different installations.",

    "For optimal performance, ensure that the server meets the minimum hardware "
    "requirements: 8 GB RAM, 4-core CPU, and 50 GB available disk space. SSD storage "
    "is strongly recommended for database operations. Network bandwidth should be at "
    "least 100 Mbps for multi-user environments.",

    "The reporting engine supports multiple output formats including PDF, Excel, CSV, "
    "and HTML. Reports can be parameterized with date ranges, department filters, and "
    "custom grouping options. Scheduled reports are delivered via email with optional "
    "encryption using the organization's PGP keys.",

    "Security compliance is maintained through regular automated scans. The system "
    "generates compliance reports aligned with SOC 2, GDPR, and HIPAA standards. "
    "Vulnerability assessments run weekly and results are available in the Security "
    "Dashboard under the Compliance tab.",

    "Data retention policies can be configured per data category. By default, "
    "transaction logs are retained for 7 years, user activity logs for 2 years, "
    "and temporary files for 30 days. Custom retention rules can be defined through "
    "the Data Governance settings panel.",

    "The notification system supports email, SMS, and in-app alerts. Notification "
    "rules can be configured based on event severity levels: Critical, Warning, "
    "Informational, and Debug. Each user can customize their notification preferences "
    "through the Profile Settings page.",

    "Backup procedures should be established before the system goes live. Full backups "
    "are recommended weekly, with incremental backups running daily. The built-in "
    "backup verification tool confirms data integrity after each backup cycle and "
    "sends a summary report to designated administrators.",
]


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    CONTENT_RECT = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT, MARGIN_BOTTOM)

    page_count = 0
    para_idx = 0

    # -- Title Page --
    page = doc.new_page(width=W, height=H)
    page_count += 1

    page.insert_text(
        pymupdf.Point(W / 2 - 150, 250),
        "DataFlow Pro",
        fontsize=36,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 120, 310),
        "User Manual",
        fontsize=28,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 80, 370),
        "Version 4.2.1",
        fontsize=16,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 130, 420),
        "Meridian Software Inc.",
        fontsize=14,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 80, 460),
        "March 2025",
        fontsize=12,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Draw a decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 330), pymupdf.Point(462, 330))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    # -- Table of Contents Page --
    page = doc.new_page(width=W, height=H)
    page_count += 1
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 30),
        "Table of Contents",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.2, 0.5),
    )
    y = MARGIN_TOP + 70
    toc_page = 3  # chapters start at page 3
    for ch_title, sections in CHAPTERS:
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, y),
            f"{ch_title}",
            fontsize=12,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y += 18
        for sec in sections:
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT + 20, y),
                sec,
                fontsize=10,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            y += 15
        y += 8
        toc_page += len(sections) + 1
        if y > MARGIN_BOTTOM - 30:
            # Overflow to next page if needed
            page = doc.new_page(width=W, height=H)
            page_count += 1
            y = MARGIN_TOP + 30

    # -- Chapter Pages --
    for ch_idx, (ch_title, sections) in enumerate(CHAPTERS):
        # Chapter title page
        page = doc.new_page(width=W, height=H)
        page_count += 1

        # Chapter header
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 40),
            ch_title,
            fontsize=24,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )

        # Decorative line under chapter title
        shape = page.new_shape()
        shape.draw_line(
            pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 50),
            pymupdf.Point(MARGIN_RIGHT, MARGIN_TOP + 50),
        )
        shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
        shape.commit()

        # Chapter overview paragraph
        overview_text = SECTION_PARAGRAPHS[para_idx % len(SECTION_PARAGRAPHS)]
        para_idx += 1
        page.insert_textbox(
            pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 70, MARGIN_RIGHT, MARGIN_TOP + 160),
            overview_text,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Section pages within the chapter
        for sec_idx, sec_title in enumerate(sections):
            page = doc.new_page(width=W, height=H)
            page_count += 1

            # Section header
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 25),
                sec_title,
                fontsize=16,
                fontname="hebo",
                color=(0.15, 0.25, 0.45),
            )

            # Section content - multiple paragraphs
            y_offset = MARGIN_TOP + 55
            for p in range(3):
                text = SECTION_PARAGRAPHS[(para_idx + p) % len(SECTION_PARAGRAPHS)]
                para_idx += 1
                rect = pymupdf.Rect(MARGIN_LEFT, y_offset, MARGIN_RIGHT, y_offset + 90)
                page.insert_textbox(
                    rect,
                    text,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                y_offset += 100

            # Add a note box on some pages
            if sec_idx % 2 == 0:
                note_rect = pymupdf.Rect(MARGIN_LEFT + 20, y_offset + 10,
                                         MARGIN_RIGHT - 20, y_offset + 70)
                shape = page.new_shape()
                shape.draw_rect(note_rect)
                shape.finish(color=(0.6, 0.6, 0.6), fill=(0.95, 0.95, 0.98), width=0.5)
                shape.commit()
                page.insert_textbox(
                    pymupdf.Rect(note_rect.x0 + 10, note_rect.y0 + 8,
                                 note_rect.x1 - 10, note_rect.y1 - 8),
                    "Note: For additional details on this topic, refer to the online "
                    "knowledge base at https://docs.meridian-software.com or contact "
                    "technical support at support@meridian-software.com.",
                    fontsize=9,
                    fontname="tiit",
                    color=(0.3, 0.3, 0.3),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )

    # Pad to exactly 50 pages if needed
    while page_count < 50:
        page = doc.new_page(width=W, height=H)
        page_count += 1
        appendix_num = page_count - 48
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 25),
            f"Appendix {chr(64 + appendix_num)}: Additional Reference Material",
            fontsize=16,
            fontname="hebo",
            color=(0.15, 0.25, 0.45),
        )
        text = SECTION_PARAGRAPHS[para_idx % len(SECTION_PARAGRAPHS)]
        para_idx += 1
        page.insert_textbox(
            pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 55, MARGIN_RIGHT, MARGIN_BOTTOM),
            (text + " ") * 4,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Add page numbers as footer on all pages (except title page)
    for i in range(1, doc.page_count):
        pg = doc[i]
        pg.insert_text(
            pymupdf.Point(W / 2 - 10, H - 30),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Set TOC bookmarks
    toc = [[1, "Title Page", 1], [1, "Table of Contents", 2]]
    pg_num = 3
    for ch_title, sections in CHAPTERS:
        toc.append([1, ch_title, pg_num])
        pg_num += 1
        for sec in sections:
            toc.append([2, sec, pg_num])
            pg_num += 1
            if pg_num > 50:
                break
        if pg_num > 50:
            break
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_count}')

    # Launch PDF viewer
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
