"""
Initial Setup: Create a 100-page textbook PDF with no bookmarks
Task ID: pdf_fm_035
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_035'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/textbook.pdf'

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


# Content structure for a realistic textbook
PARTS = {
    1: {"title": "Part I: Foundations", "start": 1, "chapters": {
        1: {"title": "Chapter 1: Introduction to Data Science", "start": 3, "end": 24},
        2: {"title": "Chapter 2: Statistical Fundamentals", "start": 25, "end": 49},
    }},
    2: {"title": "Part II: Advanced Topics", "start": 50, "chapters": {
        3: {"title": "Chapter 3: Machine Learning Models", "start": 52, "end": 77},
        4: {"title": "Chapter 4: Deep Learning Architectures", "start": 78, "end": 100},
    }},
}

SECTION_CONTENT = {
    "Chapter 1": [
        "Data science is an interdisciplinary field that combines statistical analysis, machine learning, and domain expertise to extract meaningful insights from structured and unstructured data.",
        "The modern data science workflow typically involves data collection, cleaning, exploratory analysis, feature engineering, model building, and deployment.",
        "Key tools in the data science ecosystem include Python, R, SQL, and various cloud computing platforms that enable scalable data processing.",
    ],
    "Chapter 2": [
        "Statistical fundamentals form the backbone of data analysis. Understanding probability distributions, hypothesis testing, and regression analysis is essential for any data scientist.",
        "Bayesian statistics provides a framework for updating beliefs as new evidence becomes available, complementing traditional frequentist approaches.",
        "Experimental design and A/B testing methodologies enable organizations to make data-driven decisions with quantified uncertainty.",
    ],
    "Chapter 3": [
        "Machine learning models can be broadly categorized into supervised learning, unsupervised learning, and reinforcement learning paradigms.",
        "Decision trees, random forests, and gradient boosting machines represent powerful ensemble methods that achieve state-of-the-art performance on tabular data.",
        "Model evaluation requires careful consideration of metrics such as accuracy, precision, recall, F1-score, and area under the ROC curve.",
    ],
    "Chapter 4": [
        "Deep learning architectures have revolutionized fields such as computer vision, natural language processing, and speech recognition.",
        "Convolutional neural networks exploit spatial hierarchies in image data through learnable filters and pooling operations.",
        "Transformer architectures, built on self-attention mechanisms, have become the foundation for large language models and multimodal AI systems.",
    ],
}


def get_chapter_for_page(page_num):
    """Return chapter info for a given 1-indexed page number."""
    for part in PARTS.values():
        for ch_num, ch in part["chapters"].items():
            if ch["start"] <= page_num <= ch["end"]:
                return ch_num, ch
    return None, None


def create_initial():
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, 101):
        page = doc.new_page(width=595, height=842)  # A4

        ch_num, ch_info = get_chapter_for_page(page_num)

        if page_num == 1:
            # Title page
            page.insert_text(
                pymupdf.Point(297 - 120, 300),
                "Data Science:",
                fontsize=28,
                fontname="hebo",
                color=(0, 0, 0),
            )
            page.insert_text(
                pymupdf.Point(297 - 160, 345),
                "Theory and Practice",
                fontsize=28,
                fontname="hebo",
                color=(0, 0, 0),
            )
            page.insert_text(
                pymupdf.Point(297 - 80, 420),
                "Dr. Elena Vasquez",
                fontsize=16,
                fontname="tiit",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(297 - 100, 450),
                "Stanford University Press",
                fontsize=12,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
            page.insert_text(
                pymupdf.Point(297 - 30, 480),
                "2024",
                fontsize=12,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
        elif page_num == 2:
            # Copyright page
            page.insert_text(pymupdf.Point(72, 600), "Copyright (c) 2024 Elena Vasquez", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 620), "All rights reserved.", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 640), "ISBN: 978-1-234567-89-0", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        elif page_num in [p["start"] for p in PARTS.values()]:
            # Part title page
            for part in PARTS.values():
                if part["start"] == page_num:
                    page.insert_text(
                        pymupdf.Point(297 - 120, 380),
                        part["title"],
                        fontsize=24,
                        fontname="hebo",
                        color=(0, 0, 0),
                    )
                    # Horizontal rule
                    shape = page.new_shape()
                    shape.draw_line(pymupdf.Point(150, 400), pymupdf.Point(445, 400))
                    shape.finish(color=(0.5, 0.5, 0.5), width=1)
                    shape.commit()
                    break
        elif ch_info and page_num == ch_info["start"]:
            # Chapter start page
            page.insert_text(
                pymupdf.Point(72, 100),
                ch_info["title"],
                fontsize=20,
                fontname="hebo",
                color=(0, 0, 0),
            )
            # Horizontal rule under chapter title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 110), pymupdf.Point(523, 110))
            shape.finish(color=(0, 0, 0), width=0.5)
            shape.commit()

            # Chapter intro text
            ch_key = f"Chapter {ch_num}"
            if ch_key in SECTION_CONTENT:
                y = 150
                for para in SECTION_CONTENT[ch_key]:
                    rect = pymupdf.Rect(72, y, 523, y + 80)
                    page.insert_textbox(rect, para, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    y += 85
        else:
            # Regular content page
            if ch_info:
                # Header with chapter name
                page.insert_text(
                    pymupdf.Point(72, 50),
                    ch_info["title"],
                    fontsize=8,
                    fontname="heit",
                    color=(0.5, 0.5, 0.5),
                )
                # Thin rule under header
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, 55), pymupdf.Point(523, 55))
                shape.finish(color=(0.8, 0.8, 0.8), width=0.3)
                shape.commit()

            # Body text placeholder for regular pages
            section_num = (page_num % 5) + 1
            paragraphs = [
                f"Section {page_num - (ch_info['start'] if ch_info else 0)}.{section_num} continues the discussion of core concepts introduced earlier in this chapter. "
                "The theoretical framework presented here builds upon established principles in the field, "
                "incorporating recent advances and empirical findings from leading research institutions.",

                "Empirical validation of these methods has been conducted across multiple datasets, "
                "demonstrating consistent improvements in both accuracy and computational efficiency. "
                "The results presented in Table {0}.{1} summarize the key performance metrics.".format(
                    ch_num if ch_num else 1, section_num
                ),

                "Furthermore, the integration of domain-specific knowledge with automated feature extraction "
                "pipelines has shown promising results in reducing the time-to-insight for complex analytical tasks. "
                "These findings align with recent industry benchmarks published by major technology companies.",
            ]

            y = 80
            for para in paragraphs:
                rect = pymupdf.Rect(72, y, 523, y + 80)
                page.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y += 90

        # Page number (centered at bottom, except title page)
        if page_num > 1:
            page.insert_text(
                pymupdf.Point(285, 810),
                str(page_num),
                fontsize=9,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

    # Ensure NO bookmarks/TOC
    doc.set_toc([])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify no bookmarks
    verify_doc = pymupdf.open(OUTPUT)
    toc = verify_doc.get_toc()
    print(f'Verification - Page count: {verify_doc.page_count}, TOC entries: {len(toc)}')
    verify_doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
