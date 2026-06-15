"""
Initial Setup: Create linked_doc.pdf with 15 pages and no link annotations
Task ID: pdf_adv_190
Domain: pdf

Creates ~/Documents/linked_doc.pdf with 15 pages and no link annotations.
The agent will then add:
  - A GoTo link on page 1 at rect (72, 750, 200, 765) pointing to page 10
  - A URI link on page 1 at rect (72, 730, 300, 745) pointing to 'https://www.example.com/resources'
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_190'
OUTPUT_FILE = f'{WORKDIR}/Documents/linked_doc.pdf'
NUM_PAGES = 15


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, NUM_PAGES + 1):
        page = doc.new_page(width=595, height=842)

        # Header bar
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 60))
        shape.finish(color=(0.15, 0.35, 0.65), fill=(0.15, 0.35, 0.65))
        shape.commit()

        # Title text
        page.insert_text(
            pymupdf.Point(40, 40),
            f"Document Title — Page {page_num}",
            fontsize=16,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Body content
        page.insert_text(
            pymupdf.Point(72, 100),
            f"Section {page_num}: Overview",
            fontsize=13,
            fontname="hebo",
            color=(0.1, 0.1, 0.1),
        )

        body_lines = [
            f"This is page {page_num} of the document.",
            "It contains sample text content to simulate a real document.",
            "The document spans 15 pages covering various topics.",
            "",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
        ]

        y = 130
        for line in body_lines:
            if line:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
            y += 18

        # Placeholder text where links will be added (page 1 only)
        if page_num == 1:
            page.insert_text(
                pymupdf.Point(72, 720),
                "Reference Links:",
                fontsize=11,
                fontname="hebo",
                color=(0.3, 0.3, 0.3),
            )
            # Area where URI link will go (72, 730, 300, 745)
            page.insert_text(
                pymupdf.Point(72, 742),
                "External Resources",
                fontsize=10,
                fontname="helv",
                color=(0.2, 0.2, 0.8),
            )
            # Area where GoTo link will go (72, 750, 200, 765)
            page.insert_text(
                pymupdf.Point(72, 762),
                "Go to Chapter 10",
                fontsize=10,
                fontname="helv",
                color=(0.2, 0.2, 0.8),
            )

        # Footer
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, 810), pymupdf.Point(523, 810))
        shape2.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape2.commit()

        page.insert_text(
            pymupdf.Point(72, 825),
            f"Page {page_num} of {NUM_PAGES}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT_FILE)
    doc.close()

    size = os.path.getsize(OUTPUT_FILE)
    print(f"Created: {OUTPUT_FILE} ({NUM_PAGES} pages, {size} bytes)")

    # Verify no links in the initial state
    doc_check = pymupdf.open(OUTPUT_FILE)
    page1_links = doc_check[0].get_links()
    doc_check.close()
    assert len(page1_links) == 0, f"Expected 0 links on page 1, found {len(page1_links)}"
    print(f"Verified: page 1 has {len(page1_links)} link annotations (expected: 0)")

    print(f"\nInitial state ready: {OUTPUT_FILE}")
    print(f"  - {NUM_PAGES} pages")
    print(f"  - No link annotations on any page")
    print(f"  - Agent must add: GoTo link at (72,750,200,765) → page 10")
    print(f"  - Agent must add: URI link at (72,730,300,745) → https://www.example.com/resources")

    launch_gui(f'evince "{OUTPUT_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with linked_doc.pdf using DISPLAY=:0')


create_initial()
