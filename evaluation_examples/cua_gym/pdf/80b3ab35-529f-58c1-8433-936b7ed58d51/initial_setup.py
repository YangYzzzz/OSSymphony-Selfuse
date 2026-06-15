"""
Initial Setup: Create a 200-page A5 PDF book for booklet imposition task.
Task ID: pdf_fm_074
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_074'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/book.pdf'

# A5 dimensions in points (148mm x 210mm)
A5_WIDTH = 420  # ~148mm
A5_HEIGHT = 595  # ~210mm


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

    doc = pymupdf.open()

    # Chapter structure for a realistic book
    chapters = [
        (1, "Introduction to Modern Computing"),
        (12, "Chapter 1: The Digital Revolution"),
        (28, "Chapter 2: Hardware Fundamentals"),
        (45, "Chapter 3: Operating Systems"),
        (62, "Chapter 4: Networking and the Internet"),
        (80, "Chapter 5: Data Structures and Algorithms"),
        (98, "Chapter 6: Database Systems"),
        (115, "Chapter 7: Software Engineering"),
        (132, "Chapter 8: Artificial Intelligence"),
        (150, "Chapter 9: Cybersecurity"),
        (168, "Chapter 10: Cloud Computing"),
        (185, "Chapter 11: Future Trends"),
    ]

    # Paragraph snippets for realistic content
    paragraphs = [
        "The rapid evolution of technology has fundamentally transformed how we interact with information systems. From the earliest mainframes to modern distributed architectures, computing has become an integral part of daily life.",
        "Understanding the underlying principles of computation requires a solid foundation in both theoretical concepts and practical applications. This chapter explores the core mechanisms that drive modern systems.",
        "Performance optimization remains a critical concern in system design. Engineers must balance throughput, latency, and resource utilization to achieve optimal results in production environments.",
        "Security considerations must be woven into every layer of the technology stack. A defense-in-depth approach ensures that no single point of failure can compromise the entire system.",
        "The emergence of cloud-native architectures has shifted the paradigm from monolithic deployments to microservices-based systems. This transition brings both opportunities and challenges.",
        "Data-driven decision making relies on robust pipelines that can process, transform, and analyze information at scale. Modern analytics platforms leverage distributed computing frameworks.",
        "User experience design plays a crucial role in the adoption of new technologies. Intuitive interfaces reduce cognitive load and improve productivity across diverse user populations.",
        "Continuous integration and continuous deployment practices have revolutionized the software delivery lifecycle. Automated testing and monitoring ensure quality at every stage.",
    ]

    for page_num in range(200):
        page = doc.new_page(width=A5_WIDTH, height=A5_HEIGHT)

        # Determine if this is a chapter start
        chapter_title = None
        for ch_start, ch_title in chapters:
            if page_num + 1 == ch_start:
                chapter_title = ch_title
                break

        if chapter_title:
            # Chapter title page
            page.insert_text(
                pymupdf.Point(40, 180),
                chapter_title,
                fontsize=18,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            # Decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(40, 195), pymupdf.Point(A5_WIDTH - 40, 195))
            shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
            shape.commit()

            # Intro paragraph
            rect = pymupdf.Rect(40, 220, A5_WIDTH - 40, A5_HEIGHT - 60)
            page.insert_textbox(
                rect,
                paragraphs[page_num % len(paragraphs)],
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
        else:
            # Regular content page
            # Header with book title
            page.insert_text(
                pymupdf.Point(40, 30),
                "Foundations of Modern Computing",
                fontsize=7,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )
            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(40, 38), pymupdf.Point(A5_WIDTH - 40, 38))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()

            # Body text - two paragraphs
            rect = pymupdf.Rect(40, 50, A5_WIDTH - 40, A5_HEIGHT - 60)
            para1 = paragraphs[page_num % len(paragraphs)]
            para2 = paragraphs[(page_num + 3) % len(paragraphs)]
            body_text = f"{para1}\n\n{para2}"
            page.insert_textbox(
                rect,
                body_text,
                fontsize=10,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Page number at bottom center
        pn_text = str(page_num + 1)
        page.insert_text(
            pymupdf.Point(A5_WIDTH / 2 - 5, A5_HEIGHT - 30),
            pn_text,
            fontsize=9,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Foundations of Modern Computing",
        "author": "Dr. Elena Vasquez",
        "subject": "Computer Science Textbook",
        "keywords": "computing, technology, programming, algorithms",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 200')

    # Open the file in evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
