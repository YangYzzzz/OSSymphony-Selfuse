"""
Initial Setup: Create encyclopedia.pdf with complex bookmark hierarchy
Task ID: pdf_mbc_051
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_051'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/encyclopedia.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Remove bookmark_count.txt if it exists (must NOT be present in initial state)
    count_file = f'{DOCS_DIR}/bookmark_count.txt'
    if os.path.exists(count_file):
        os.remove(count_file)

    doc = pymupdf.open()

    # We need a PDF with enough pages and a complex bookmark hierarchy:
    # 8 top-level, 24 second-level (3 per top-level), 12 third-level (scattered)
    # Total: 8 + 24 + 12 = 44 bookmarks

    # Define the encyclopedia structure
    chapters = [
        {
            "title": "Chapter 1: Ancient Civilizations",
            "sections": [
                {"title": "1.1 Mesopotamia", "subsections": ["1.1.1 Sumerian Culture", "1.1.2 Babylonian Empire"]},
                {"title": "1.2 Ancient Egypt", "subsections": ["1.2.1 The Pharaohs"]},
                {"title": "1.3 Indus Valley", "subsections": []},
            ]
        },
        {
            "title": "Chapter 2: Classical Antiquity",
            "sections": [
                {"title": "2.1 Ancient Greece", "subsections": ["2.1.1 Athenian Democracy"]},
                {"title": "2.2 Roman Republic", "subsections": ["2.2.1 Roman Law"]},
                {"title": "2.3 Persian Empire", "subsections": []},
            ]
        },
        {
            "title": "Chapter 3: Medieval Period",
            "sections": [
                {"title": "3.1 Byzantine Empire", "subsections": []},
                {"title": "3.2 Islamic Golden Age", "subsections": ["3.2.1 Advances in Mathematics"]},
                {"title": "3.3 European Feudalism", "subsections": ["3.3.1 The Crusades"]},
            ]
        },
        {
            "title": "Chapter 4: Renaissance and Reformation",
            "sections": [
                {"title": "4.1 Italian Renaissance", "subsections": ["4.1.1 Art and Architecture"]},
                {"title": "4.2 Scientific Revolution", "subsections": []},
                {"title": "4.3 Protestant Reformation", "subsections": []},
            ]
        },
        {
            "title": "Chapter 5: Age of Exploration",
            "sections": [
                {"title": "5.1 Maritime Routes", "subsections": []},
                {"title": "5.2 Colonial Empires", "subsections": ["5.2.1 Spanish Conquests"]},
                {"title": "5.3 Cultural Exchange", "subsections": []},
            ]
        },
        {
            "title": "Chapter 6: Industrial Revolution",
            "sections": [
                {"title": "6.1 Mechanization", "subsections": []},
                {"title": "6.2 Urbanization", "subsections": ["6.2.1 Factory Systems"]},
                {"title": "6.3 Social Reforms", "subsections": []},
            ]
        },
        {
            "title": "Chapter 7: Modern Era",
            "sections": [
                {"title": "7.1 World War I", "subsections": []},
                {"title": "7.2 World War II", "subsections": ["7.2.1 The Holocaust"]},
                {"title": "7.3 Cold War", "subsections": []},
            ]
        },
        {
            "title": "Chapter 8: Contemporary World",
            "sections": [
                {"title": "8.1 Globalization", "subsections": ["8.1.1 International Trade"]},
                {"title": "8.2 Digital Revolution", "subsections": []},
                {"title": "8.3 Climate Change", "subsections": []},
            ]
        },
    ]

    # Verify bookmark counts
    top_count = len(chapters)  # 8
    sec_count = sum(len(ch["sections"]) for ch in chapters)  # 24
    sub_count = sum(
        len(sec["subsections"])
        for ch in chapters
        for sec in ch["sections"]
    )  # 12
    total = top_count + sec_count + sub_count
    assert total == 44, f"Expected 44 bookmarks, got {total}"

    # Create pages with content (one page per chapter, plus a title page)
    # Title page
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(150, 200),
        "The World Encyclopedia",
        fontsize=28,
        fontname="hebo",
        color=(0, 0, 0.5),
    )
    page.insert_text(
        pymupdf.Point(160, 260),
        "A Comprehensive History",
        fontsize=18,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(200, 340),
        "Third Edition, 2025",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Build TOC and create pages
    toc = []
    page_num = 2  # start at page 2 (page 1 is title)

    for ch in chapters:
        # Create chapter page
        p = doc.new_page(width=595, height=842)
        p.insert_text(
            pymupdf.Point(72, 80),
            ch["title"],
            fontsize=22,
            fontname="hebo",
            color=(0, 0, 0.4),
        )

        # Add some body text
        body_text = (
            "This chapter provides an in-depth examination of the historical period "
            "and its lasting impact on subsequent developments in human civilization. "
            "The analysis covers political, social, economic, and cultural dimensions "
            "that shaped the trajectory of societies across different regions."
        )
        p.insert_textbox(
            pymupdf.Rect(72, 110, 523, 250),
            body_text,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Top-level bookmark
        toc.append([1, ch["title"], page_num])

        y_pos = 280
        for sec in ch["sections"]:
            # Add section heading on the same page
            p.insert_text(
                pymupdf.Point(90, y_pos),
                sec["title"],
                fontsize=16,
                fontname="tibo",
                color=(0.1, 0.1, 0.1),
            )
            y_pos += 30

            # Section body
            sec_text = (
                "Detailed coverage of key events, figures, and developments "
                "that defined this particular era and region."
            )
            p.insert_textbox(
                pymupdf.Rect(90, y_pos, 523, y_pos + 40),
                sec_text,
                fontsize=10,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            y_pos += 55

            # Second-level bookmark
            toc.append([2, sec["title"], page_num])

            for sub in sec["subsections"]:
                # Add subsection text
                p.insert_text(
                    pymupdf.Point(110, y_pos),
                    sub,
                    fontsize=13,
                    fontname="tiit",
                    color=(0.2, 0.2, 0.3),
                )
                y_pos += 25

                # Third-level bookmark
                toc.append([3, sub, page_num])

        page_num += 1

    # Set the table of contents (bookmarks)
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    verify_toc = verify_doc.get_toc()
    verify_doc.close()
    print(f"Initial file created: {OUTPUT}")
    print(f"Total bookmarks: {len(verify_toc)}")
    assert len(verify_toc) == 44, f"Expected 44 bookmarks, got {len(verify_toc)}"

    # Open PDF in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
