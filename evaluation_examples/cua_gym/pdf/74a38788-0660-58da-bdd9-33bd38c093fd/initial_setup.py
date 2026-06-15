"""
Initial Setup: Create a 30-page PDF reference guide with multi-level bookmarks
Task ID: pdf_gf1_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_032'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/reference_guide.pdf'


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


def create_initial():
    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    # Remove toc.txt if it exists (must NOT exist in initial state)
    toc_path = f'{DOCS_DIR}/toc.txt'
    if os.path.exists(toc_path):
        os.remove(toc_path)

    doc = pymupdf.open()

    # Define the bookmark/TOC structure (16 entries)
    # [level, title, page_number (1-indexed)]
    toc = [
        [1, "Chapter 1: System Architecture Overview", 1],
        [2, "1.1 Hardware Requirements", 2],
        [2, "1.2 Software Dependencies", 4],
        [2, "1.3 Network Configuration", 6],
        [3, "1.3.1 Firewall Rules", 7],
        [1, "Chapter 2: Installation and Deployment", 8],
        [2, "2.1 Pre-Installation Checklist", 9],
        [2, "2.2 Step-by-Step Installation", 10],
        [2, "2.3 Post-Installation Verification", 13],
        [3, "2.3.1 Health Check Procedures", 14],
        [1, "Chapter 3: User Management and Security", 15],
        [2, "3.1 Role-Based Access Control", 16],
        [2, "3.2 Authentication Protocols", 18],
        [3, "3.2.1 Multi-Factor Authentication Setup", 19],
        [2, "3.3 Audit Logging", 20],
        [1, "Chapter 4: Troubleshooting and Maintenance", 22],
        [2, "4.1 Common Error Codes", 23],
        [2, "4.2 Performance Tuning", 25],
        [2, "4.3 Backup and Recovery", 27],
        [3, "4.3.1 Disaster Recovery Procedures", 28],
    ]

    # Chapter content templates for realistic pages
    chapter_content = {
        1: "This chapter provides a comprehensive overview of the system architecture, "
           "including hardware specifications, software stack components, and network topology. "
           "Understanding the architecture is essential for effective deployment and maintenance.",
        8: "This chapter covers the complete installation process from initial environment "
           "preparation through final verification. Follow each step carefully to ensure "
           "a successful deployment.",
        15: "Security is a critical component of any enterprise system. This chapter details "
            "the user management framework, authentication mechanisms, and audit capabilities "
            "built into the platform.",
        22: "When issues arise, this chapter provides systematic troubleshooting procedures, "
            "performance optimization guidelines, and data protection strategies.",
    }

    # Create 30 pages with realistic content
    for page_num in range(1, 31):
        page = doc.new_page(width=595, height=842)  # A4

        # Find if this page has a bookmark
        page_bookmarks = [b for b in toc if b[2] == page_num]

        y_pos = 72

        if page_bookmarks:
            for bm in page_bookmarks:
                level, title, _ = bm
                if level == 1:
                    # Chapter title - large bold
                    page.insert_text(
                        pymupdf.Point(72, y_pos),
                        title,
                        fontsize=20,
                        fontname="hebo",
                        color=(0.1, 0.1, 0.4),
                    )
                    y_pos += 40

                    # Chapter intro paragraph
                    if page_num in chapter_content:
                        rect = pymupdf.Rect(72, y_pos, 523, y_pos + 80)
                        page.insert_textbox(
                            rect,
                            chapter_content[page_num],
                            fontsize=11,
                            fontname="helv",
                            color=(0, 0, 0),
                        )
                        y_pos += 100

                elif level == 2:
                    page.insert_text(
                        pymupdf.Point(72, y_pos),
                        title,
                        fontsize=14,
                        fontname="hebo",
                        color=(0.2, 0.2, 0.5),
                    )
                    y_pos += 30

                elif level == 3:
                    page.insert_text(
                        pymupdf.Point(90, y_pos),
                        title,
                        fontsize=12,
                        fontname="hebi",
                        color=(0.3, 0.3, 0.6),
                    )
                    y_pos += 25

        # Add body text to every page
        body_texts = [
            "The configuration parameters described in this section are essential for optimal "
            "system performance. Each parameter has been tested across multiple deployment "
            "scenarios to ensure reliability and consistency.",
            "Refer to Appendix A for detailed specifications and compatibility matrices. "
            "All values shown represent recommended settings for production environments "
            "with standard workloads.",
            "Note: Changes to these settings require a service restart. It is recommended "
            "to schedule configuration changes during maintenance windows to minimize "
            "impact on active users.",
        ]

        for i, text in enumerate(body_texts):
            rect = pymupdf.Rect(72, y_pos + i * 60, 523, y_pos + i * 60 + 50)
            page.insert_textbox(
                rect,
                text,
                fontsize=10,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(280, 810),
            f"- {page_num} -",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Set the bookmark outline (TOC)
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
