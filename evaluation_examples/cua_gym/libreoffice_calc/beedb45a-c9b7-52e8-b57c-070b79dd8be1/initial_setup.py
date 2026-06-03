"""
Initial Setup: Create ebook.pdf with specific metadata fields
Task ID: pdf_mbc_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_030'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT_PDF = f'{DOCUMENTS}/ebook.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    import pymupdf

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(150, 200),
        "The Art of Programming",
        fontsize=28,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )
    page.insert_text(
        pymupdf.Point(200, 260),
        "by Jane Developer",
        fontsize=16,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(170, 320),
        "A Comprehensive Guide to",
        fontsize=12,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(130, 340),
        "Programming, Algorithms, and Data Structures",
        fontsize=12,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # --- Page 2: Table of Contents ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=20, fontname="hebo", color=(0, 0, 0))

    toc_entries = [
        ("Chapter 1: Foundations of Programming", 3),
        ("Chapter 2: Control Flow and Logic", 15),
        ("Chapter 3: Data Structures", 42),
        ("Chapter 4: Algorithm Design", 78),
        ("Chapter 5: Sorting and Searching", 110),
        ("Chapter 6: Graph Algorithms", 145),
        ("Chapter 7: Dynamic Programming", 180),
        ("Chapter 8: Complexity Analysis", 210),
        ("Chapter 9: Best Practices", 240),
        ("Chapter 10: Advanced Topics", 265),
    ]
    y = 120
    for title, pg in toc_entries:
        page2.insert_text(pymupdf.Point(90, y), title, fontsize=11, fontname="helv", color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(480, y), str(pg), fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 24

    # --- Page 3: Chapter 1 ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(pymupdf.Point(72, 72), "Chapter 1: Foundations of Programming", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))

    ch1_text = (
        "Programming is both an art and a science. At its core, it involves the systematic "
        "approach to solving problems through computational thinking. This chapter introduces "
        "the fundamental concepts that every programmer must master.\n\n"
        "Variables and data types form the building blocks of any program. Whether we are "
        "working with integers, floating-point numbers, strings, or boolean values, understanding "
        "how data is stored and manipulated is essential.\n\n"
        "Functions allow us to encapsulate logic into reusable units. By breaking complex problems "
        "into smaller, manageable pieces, we can write code that is both maintainable and testable. "
        "The concept of abstraction lets us focus on what a function does rather than how it works."
    )
    rect = pymupdf.Rect(72, 100, 523, 780)
    page3.insert_textbox(rect, ch1_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 4: Chapter 2 ---
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(pymupdf.Point(72, 72), "Chapter 2: Control Flow and Logic", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))

    ch2_text = (
        "Control flow determines the order in which statements are executed within a program. "
        "Conditional statements, loops, and branching mechanisms give programmers the power to "
        "create dynamic and responsive software.\n\n"
        "The if-else construct is perhaps the most fundamental control structure. It allows "
        "programs to make decisions based on conditions evaluated at runtime. Combined with "
        "boolean logic operators such as AND, OR, and NOT, conditions can express complex "
        "decision criteria.\n\n"
        "Loops provide the ability to repeat blocks of code. The for loop is ideal when the "
        "number of iterations is known in advance, while the while loop continues execution "
        "as long as a condition remains true. Understanding when to use each type of loop "
        "is a key skill for writing efficient algorithms."
    )
    rect = pymupdf.Rect(72, 100, 523, 780)
    page4.insert_textbox(rect, ch2_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 5: Chapter 3 ---
    page5 = doc.new_page(width=595, height=842)
    page5.insert_text(pymupdf.Point(72, 72), "Chapter 3: Data Structures", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))

    ch3_text = (
        "Data structures are specialized formats for organizing and storing data. The choice "
        "of data structure can dramatically affect the performance of an algorithm.\n\n"
        "Arrays provide constant-time access to elements by index, making them ideal for "
        "situations where random access is frequent. However, inserting or deleting elements "
        "in the middle of an array requires shifting subsequent elements, resulting in O(n) "
        "time complexity.\n\n"
        "Linked lists solve the insertion problem by storing elements as nodes with pointers "
        "to the next node. While traversal is sequential, insertions and deletions at known "
        "positions take constant time. Trees, hash tables, and graphs build upon these basic "
        "structures to enable more complex operations and relationships between data elements."
    )
    rect = pymupdf.Rect(72, 100, 523, 780)
    page5.insert_textbox(rect, ch3_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Set metadata as specified in the task context
    doc.set_metadata({
        "title": "The Art of Programming",
        "author": "Jane Developer",
        "subject": "Computer Science",
        "keywords": "programming, algorithms, data structures",
        "creator": "LaTeX",
        "producer": "pdfTeX-1.40.25",
        "creationDate": "D:20240701",
    })

    # Set TOC bookmarks
    toc = [
        [1, "Chapter 1: Foundations of Programming", 3],
        [1, "Chapter 2: Control Flow and Logic", 4],
        [1, "Chapter 3: Data Structures", 5],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Initial file created: {OUTPUT_PDF}')

    # Ensure ebook_metadata.json does NOT exist (task output)
    metadata_json = f'{DOCUMENTS}/ebook_metadata.json'
    if os.path.exists(metadata_json):
        os.remove(metadata_json)

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
