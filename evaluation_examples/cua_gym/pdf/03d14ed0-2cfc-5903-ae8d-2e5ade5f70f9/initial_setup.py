"""
Initial Setup: Create a 120-page scanned book PDF with 50-point dark borders (scanner artifact)
Task ID: pdf_pw_044
Domain: pdf
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
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_pw_044'
OUTPUT = f'{DOCUMENTS}/scanned_book.pdf'

# Book content - realistic scanned book with chapters
CHAPTERS = [
    ("Chapter 1: The Origins of Modern Computing", [
        "The history of computing stretches back centuries, from the abacus to Charles Babbage's Analytical Engine. In the mid-twentieth century, the development of electronic computers transformed the field entirely.",
        "Alan Turing's theoretical work on computability laid the mathematical foundations for digital computing. His concept of a universal machine demonstrated that a single device could perform any computation given the right instructions.",
        "The ENIAC, completed in 1945 at the University of Pennsylvania, was one of the first general-purpose electronic computers. It weighed over 27 tons and occupied 1,800 square feet of floor space.",
        "John von Neumann's stored-program architecture, described in 1945, became the blueprint for virtually all subsequent computer designs. The idea of storing instructions in the same memory as data was revolutionary.",
        "By the 1950s, commercial computers began appearing. The UNIVAC I, delivered to the U.S. Census Bureau in 1951, marked the beginning of the commercial computing era.",
    ]),
    ("Chapter 2: The Rise of Programming Languages", [
        "Early computers were programmed using machine code, sequences of binary numbers that directly controlled the hardware. This process was tedious, error-prone, and required intimate knowledge of the computer's architecture.",
        "Grace Hopper pioneered the development of compilers, programs that could translate human-readable code into machine instructions. Her work on the A-0 compiler in 1952 opened new possibilities for software development.",
        "FORTRAN, developed by John Backus and his team at IBM between 1954 and 1957, became the first widely used high-level programming language. It was designed primarily for scientific and engineering calculations.",
        "COBOL, created in 1959, was designed for business data processing. Its English-like syntax made it accessible to a broader audience and it remained dominant in business computing for decades.",
        "The 1960s saw an explosion of programming language innovation, including BASIC (1964), designed for teaching, and Simula (1967), which introduced object-oriented programming concepts.",
    ]),
    ("Chapter 3: The Microprocessor Revolution", [
        "The invention of the integrated circuit by Jack Kilby and Robert Noyce in the late 1950s set the stage for miniaturization of computing components. Entire circuits could now be fabricated on a single silicon chip.",
        "Intel's 4004, released in 1971, was the first commercially available microprocessor. Though it had only 2,300 transistors and could process 4 bits at a time, it represented a paradigm shift in computing.",
        "The Intel 8080, introduced in 1974, became the processor at the heart of the Altair 8800, widely considered the first personal computer kit. This device inspired a generation of hobbyists and entrepreneurs.",
        "The Apple II, released in 1977 by Steve Wozniak and Steve Jobs, was one of the first mass-produced personal computers. Its open architecture and color graphics capabilities made it enormously popular.",
        "The IBM PC, launched in August 1981, established the standard for personal computing that persists in modified form to this day. Its open architecture allowed third-party manufacturers to create compatible hardware.",
    ]),
    ("Chapter 4: The Internet Age", [
        "ARPANET, the precursor to the modern Internet, began as a U.S. Department of Defense project in 1969. Its packet-switching technology allowed multiple computers to communicate over shared networks.",
        "Tim Berners-Lee invented the World Wide Web at CERN in 1989, creating HTML, HTTP, and the first web browser. This innovation transformed the Internet from a tool for researchers into a global information platform.",
        "The release of the Mosaic web browser in 1993 brought the Web to mainstream users. Its graphical interface and ease of use sparked explosive growth in Internet adoption.",
        "E-commerce pioneers like Amazon (founded 1994) and eBay (founded 1995) demonstrated that the Internet could fundamentally transform retail and commerce. Online shopping grew from a novelty to an essential part of the economy.",
        "The dot-com boom of the late 1990s saw massive investment in Internet companies. While many failed in the subsequent bust of 2000-2001, the surviving companies laid the groundwork for the modern digital economy.",
    ]),
    ("Chapter 5: Artificial Intelligence and Machine Learning", [
        "The term 'artificial intelligence' was coined at the Dartmouth Conference in 1956. Early AI researchers were optimistic that human-level intelligence could be achieved within a generation.",
        "Expert systems, popular in the 1980s, used hand-crafted rules to solve problems in specific domains. Systems like MYCIN for medical diagnosis showed both the promise and limitations of rule-based AI.",
        "The development of neural networks gained momentum in the 1980s with the backpropagation algorithm. However, limited computing power and data availability constrained progress for years.",
        "Deep learning emerged in the 2010s as a transformative approach, enabled by GPUs and massive datasets. Convolutional neural networks achieved breakthrough results in image recognition, surpassing human performance on many benchmarks.",
        "Large language models, trained on vast corpora of text, demonstrated remarkable capabilities in natural language understanding and generation. These models opened new possibilities for human-computer interaction and automated reasoning.",
    ]),
    ("Chapter 6: Cloud Computing and Modern Infrastructure", [
        "Cloud computing emerged in the mid-2000s as companies like Amazon, Google, and Microsoft began offering computing resources as a service. This model eliminated the need for organizations to maintain their own data centers.",
        "Amazon Web Services, launched in 2006, pioneered the infrastructure-as-a-service model. Its elastic computing capabilities allowed businesses to scale their technology resources on demand.",
        "Containerization, popularized by Docker in 2013, revolutionized software deployment. Containers package applications with their dependencies, ensuring consistent behavior across different computing environments.",
        "Kubernetes, open-sourced by Google in 2014, became the standard for container orchestration. It automated the deployment, scaling, and management of containerized applications across clusters of machines.",
        "Serverless computing, exemplified by AWS Lambda (2014), abstracted infrastructure management even further. Developers could focus entirely on code without worrying about server provisioning or maintenance.",
    ]),
]

def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions: Letter size
    PAGE_W, PAGE_H = 612, 792
    BORDER = 50  # scanner border width

    # Content area (inside the border)
    CONTENT_X0 = BORDER + 10
    CONTENT_Y0 = BORDER + 10
    CONTENT_X1 = PAGE_W - BORDER - 10
    CONTENT_Y1 = PAGE_H - BORDER - 10

    page_num = 0

    for ch_idx, (chapter_title, paragraphs) in enumerate(CHAPTERS):
        # We need 120 pages total, so each chapter gets 20 pages
        pages_per_chapter = 20

        for pg_in_chapter in range(pages_per_chapter):
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            shape = page.new_shape()

            # Draw dark border (scanner artifact) on all four sides
            border_color = (0.12, 0.12, 0.12)  # very dark gray

            # Top border
            shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, BORDER))
            shape.finish(color=border_color, fill=border_color)
            # Bottom border
            shape.draw_rect(pymupdf.Rect(0, PAGE_H - BORDER, PAGE_W, PAGE_H))
            shape.finish(color=border_color, fill=border_color)
            # Left border
            shape.draw_rect(pymupdf.Rect(0, BORDER, BORDER, PAGE_H - BORDER))
            shape.finish(color=border_color, fill=border_color)
            # Right border
            shape.draw_rect(pymupdf.Rect(PAGE_W - BORDER, BORDER, PAGE_W, PAGE_H - BORDER))
            shape.finish(color=border_color, fill=border_color)

            shape.commit()

            # Add text content inside the borders
            y_pos = CONTENT_Y0 + 5

            if pg_in_chapter == 0:
                # Chapter title page
                page.insert_text(
                    pymupdf.Point(CONTENT_X0, y_pos + 30),
                    chapter_title,
                    fontsize=16,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
                y_pos += 60

                # First paragraph
                if paragraphs:
                    text_rect = pymupdf.Rect(CONTENT_X0, y_pos, CONTENT_X1, CONTENT_Y1 - 30)
                    page.insert_textbox(
                        text_rect,
                        paragraphs[0],
                        fontsize=11,
                        fontname="tiro",
                        color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
            else:
                # Regular content pages
                para_idx = pg_in_chapter % len(paragraphs)
                para_text = paragraphs[para_idx]

                # Add a section heading occasionally
                if pg_in_chapter % 4 == 1:
                    section_num = ch_idx + 1
                    subsection = (pg_in_chapter // 4) + 1
                    heading = f"{section_num}.{subsection} Detailed Analysis"
                    page.insert_text(
                        pymupdf.Point(CONTENT_X0, y_pos + 14),
                        heading,
                        fontsize=13,
                        fontname="hebo",
                        color=(0, 0, 0),
                    )
                    y_pos += 30

                # Main body text - repeat and vary the paragraph content
                body_text = para_text
                # Add page-specific variation
                body_text += f" This analysis continues on page {page_num + 1} of the document, expanding on the themes introduced earlier in the chapter."
                body_text += " The implications of these developments continue to shape the field today, influencing research directions, industry practices, and educational curricula around the world."

                text_rect = pymupdf.Rect(CONTENT_X0, y_pos, CONTENT_X1, CONTENT_Y1 - 30)
                page.insert_textbox(
                    text_rect,
                    body_text,
                    fontsize=11,
                    fontname="tiro",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )

            # Page number at bottom center (inside content area)
            page.insert_text(
                pymupdf.Point(PAGE_W / 2 - 10, CONTENT_Y1),
                str(page_num + 1),
                fontsize=10,
                fontname="tiro",
                color=(0.3, 0.3, 0.3),
            )

            page_num += 1

    # Set metadata
    doc.set_metadata({
        "title": "A History of Computing: From Babbage to the Cloud",
        "author": "Dr. Elizabeth Warren-Mitchell",
        "subject": "Computer Science History",
        "keywords": "computing, history, technology, programming, internet",
        "creator": "Scanner Pro 3000",
        "producer": "Scanner Pro 3000 v4.2",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_num}')


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


create_initial()

# Open the PDF in Evince for the GUI agent
launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
print('GUI_READY: launched Evince with DISPLAY=:0')
