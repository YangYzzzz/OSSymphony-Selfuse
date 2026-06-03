"""
Initial Setup: Create a programming book PDF with top-level chapter bookmarks (no sub-bookmarks for Chapter 3).
Task ID: pdf_mbc_044
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_044'
OUTPUT = f'{WORKDIR}/Documents/programming_book.pdf'

# Chapter structure: (title, start_page_0indexed, page_count, sections)
CHAPTERS = [
    ("Chapter 1: Introduction to Programming", 0, 8, [
        "What is Programming?",
        "History of Programming Languages",
        "Setting Up Your Environment",
        "Your First Program",
        "Understanding the Command Line",
        "Choosing a Text Editor",
        "Version Control Basics",
        "Summary",
    ]),
    ("Chapter 2: Data Types and Operators", 8, 10, [
        "Primitive Data Types",
        "Integers and Floats",
        "Strings and Characters",
        "Boolean Logic",
        "Arithmetic Operators",
        "Comparison Operators",
        "Logical Operators",
        "Type Conversion",
        "Working with Collections",
        "Summary",
    ]),
    ("Chapter 3: Core Programming Concepts", 18, 15, [
        "Variables and Assignment",
        "Naming Conventions",
        "Scope and Lifetime",
        "Functions and Parameters",
        "Return Values",
        "Recursion",
        "Classes and Objects",
        "Inheritance",
        "Polymorphism",
        "Modules and Packages",
        "Import Mechanisms",
        "Standard Library Overview",
        "Error Handling Basics",
        "Debugging Techniques",
        "Summary",
    ]),
    ("Chapter 4: Control Flow", 33, 10, [
        "Conditional Statements",
        "If-Else Chains",
        "Switch/Match Statements",
        "For Loops",
        "While Loops",
        "Loop Control",
        "Iterators and Generators",
        "List Comprehensions",
        "Exception Handling",
        "Summary",
    ]),
    ("Chapter 5: Advanced Topics", 43, 10, [
        "File I/O",
        "Regular Expressions",
        "Multithreading",
        "Networking Basics",
        "Database Connectivity",
        "Testing Frameworks",
        "Design Patterns",
        "Performance Optimization",
        "Deployment Strategies",
        "Summary and Next Steps",
    ]),
]

# Some realistic paragraph texts for filling pages
BODY_TEXTS = [
    "Programming is the art and science of instructing computers to perform specific tasks. "
    "Through carefully constructed sequences of instructions, developers create software that "
    "powers everything from simple calculators to complex artificial intelligence systems.",

    "Understanding the fundamentals is crucial before diving into advanced topics. Each concept "
    "builds upon the previous one, creating a solid foundation for more complex programming "
    "challenges that you will encounter in real-world applications.",

    "Practice is essential in mastering programming concepts. While reading about theory provides "
    "the intellectual framework, it is through hands-on coding exercises that true understanding "
    "develops. Consider working through the exercises at the end of each chapter.",

    "In modern software development, collaboration and code quality are paramount. Writing clean, "
    "readable code that others can maintain is just as important as writing code that works. "
    "Following established conventions and best practices will serve you well throughout your career.",

    "The evolution of programming paradigms—from procedural to object-oriented to functional—reflects "
    "the growing complexity of software systems. Each paradigm offers unique advantages for "
    "organizing code and managing state in different contexts.",

    "Error handling is a critical aspect of robust software. Anticipating potential failures and "
    "providing graceful recovery mechanisms ensures that your applications remain stable even "
    "under unexpected conditions. Defensive programming is a valuable habit to develop.",

    "Performance optimization should be approached methodically. Premature optimization is often "
    "counterproductive; instead, focus on writing correct, readable code first, then profile "
    "and optimize the actual bottlenecks when they become apparent.",

    "The software development lifecycle encompasses requirements gathering, design, implementation, "
    "testing, deployment, and maintenance. Understanding each phase helps you contribute effectively "
    "to projects of any scale, from personal scripts to enterprise applications.",
]


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
    total_pages = 53  # enough pages for all chapters

    # Create all pages with content
    for pg_idx in range(total_pages):
        page = doc.new_page(width=595, height=842)  # A4

        # Find which chapter and section this page belongs to
        chapter_info = None
        section_name = None
        page_in_chapter = 0
        for ch_title, ch_start, ch_count, ch_sections in CHAPTERS:
            if ch_start <= pg_idx < ch_start + ch_count:
                chapter_info = ch_title
                page_in_chapter = pg_idx - ch_start
                if page_in_chapter < len(ch_sections):
                    section_name = ch_sections[page_in_chapter]
                break

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(280, 820),
            str(pg_idx + 1),
            fontsize=10,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        if chapter_info:
            # Chapter header on first page of chapter
            if page_in_chapter == 0:
                page.insert_text(
                    pymupdf.Point(72, 80),
                    chapter_info,
                    fontsize=22,
                    fontname="hebo",
                    color=(0.1, 0.1, 0.4),
                )
                # Decorative line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, 90), pymupdf.Point(523, 90))
                shape.finish(color=(0.1, 0.1, 0.4), width=2)
                shape.commit()
                y_start = 130
            else:
                y_start = 72

            # Section header
            if section_name:
                page.insert_text(
                    pymupdf.Point(72, y_start),
                    section_name,
                    fontsize=16,
                    fontname="hebo",
                    color=(0.2, 0.2, 0.5),
                )
                y_start += 30

            # Body text - fill with realistic content
            text_idx = (pg_idx * 3) % len(BODY_TEXTS)
            for i in range(3):
                body = BODY_TEXTS[(text_idx + i) % len(BODY_TEXTS)]
                rect = pymupdf.Rect(72, y_start, 523, y_start + 100)
                page.insert_textbox(
                    rect,
                    body,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                y_start += 110
                if y_start > 700:
                    break
        else:
            # Pages beyond chapter content (blank or index)
            page.insert_text(
                pymupdf.Point(72, 80),
                "Appendix",
                fontsize=18,
                fontname="hebo",
                color=(0.2, 0.2, 0.5),
            )

    # Set TOC with ONLY top-level chapter bookmarks (no sub-bookmarks for Chapter 3)
    # Page numbers in TOC are 1-indexed
    toc = [
        [1, "Chapter 1: Introduction to Programming", 1],   # page 1 (0-indexed: 0)
        [1, "Chapter 2: Data Types and Operators", 9],       # page 9 (0-indexed: 8)
        [1, "Chapter 3: Core Programming Concepts", 19],     # page 19 (0-indexed: 18) -> context says page 28
        [1, "Chapter 4: Control Flow", 34],                  # page 34 (0-indexed: 33)
        [1, "Chapter 5: Advanced Topics", 44],               # page 44 (0-indexed: 43)
    ]

    # Wait -- the task says "Chapter 3 points to page 28". Let me adjust page structure.
    # The task uses 1-indexed pages. Chapter 3 -> page 28, sub-bookmarks at pages 31, 35, 42, 48.
    # We need at least 48+ pages. Let me recalculate.
    # Chapter 1: pages 1-8 (8 pages)
    # Chapter 2: pages 9-18 (10 pages)
    # Chapter 3: pages 19-... but task says it points to page 28
    # So let me adjust the TOC to match the task description exactly.

    toc = [
        [1, "Chapter 1", 1],
        [1, "Chapter 2", 10],
        [1, "Chapter 3", 28],
        [1, "Chapter 4", 40],
        [1, "Chapter 5", 49],
    ]

    doc.set_toc(toc)
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Launch PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
