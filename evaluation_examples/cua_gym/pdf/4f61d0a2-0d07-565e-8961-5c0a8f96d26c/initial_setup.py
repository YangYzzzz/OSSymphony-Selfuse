"""
Initial Setup: Create a scanned book PDF with 30-point white borders
Task ID: pdf_gf1_014
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
TASK_ID = 'pdf_gf1_014'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/scanned_book.pdf'

MARGIN = 30  # 30-point white border on all sides
PAGE_W, PAGE_H = 612, 792  # US Letter


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


# Book content for 8 pages -- realistic scanned book text
chapters = [
    {
        "title": "Chapter 1: The Origins of Modern Computing",
        "body": (
            "The story of modern computing begins in the early twentieth century, "
            "when mathematicians and engineers first envisioned machines capable of "
            "performing complex calculations automatically. Charles Babbage designed "
            "the Analytical Engine in 1837, widely regarded as the first concept of "
            "a general-purpose computer. Ada Lovelace, working alongside Babbage, "
            "wrote what many consider the first computer program.\n\n"
            "By the 1930s, Alan Turing formalized the concept of computation with "
            "his theoretical Turing machine, establishing the mathematical foundations "
            "that would guide decades of development. His work at Bletchley Park "
            "during World War II demonstrated the practical power of automated "
            "computation in breaking the Enigma cipher."
        ),
    },
    {
        "title": "Chapter 2: The Transistor Revolution",
        "body": (
            "The invention of the transistor at Bell Labs in 1947 by John Bardeen, "
            "Walter Brattain, and William Shockley marked a turning point in electronics. "
            "Vacuum tubes, which had powered early computers like ENIAC, were bulky, "
            "unreliable, and consumed enormous amounts of electricity. The transistor "
            "offered a smaller, more efficient alternative.\n\n"
            "By the late 1950s, transistorized computers began replacing their vacuum-tube "
            "predecessors. The IBM 7090, introduced in 1959, became one of the most "
            "successful transistorized mainframes. Universities and research laboratories "
            "adopted these machines for scientific calculations, weather prediction, "
            "and early experiments in artificial intelligence."
        ),
    },
    {
        "title": "Chapter 3: Integrated Circuits and Miniaturization",
        "body": (
            "Jack Kilby of Texas Instruments and Robert Noyce of Fairchild Semiconductor "
            "independently developed the integrated circuit in 1958 and 1959. This "
            "innovation allowed multiple transistors to be fabricated on a single chip "
            "of semiconductor material, dramatically reducing size and cost.\n\n"
            "Gordon Moore observed in 1965 that the number of transistors on a chip "
            "doubled approximately every two years, a prediction now known as Moore's Law. "
            "This exponential growth in computing power drove the development of smaller, "
            "faster, and cheaper computers throughout the following decades."
        ),
    },
    {
        "title": "Chapter 4: The Rise of Personal Computing",
        "body": (
            "The 1970s witnessed the birth of personal computing. The Altair 8800, "
            "introduced in 1975, inspired hobbyists and entrepreneurs alike. Steve Wozniak "
            "and Steve Jobs founded Apple Computer in 1976, releasing the Apple II the "
            "following year. It became one of the first mass-produced personal computers.\n\n"
            "IBM entered the personal computer market in 1981 with the IBM PC, which "
            "quickly became the industry standard. Microsoft provided the operating system, "
            "MS-DOS, establishing a partnership that would shape the industry for decades. "
            "The spreadsheet application VisiCalc and later Lotus 1-2-3 demonstrated that "
            "personal computers could be powerful business tools."
        ),
    },
    {
        "title": "Chapter 5: Networking and the Internet",
        "body": (
            "ARPANET, funded by the U.S. Department of Defense, connected its first four "
            "nodes in 1969. This experimental network laid the groundwork for the Internet. "
            "Vint Cerf and Bob Kahn developed the TCP/IP protocol suite in the 1970s, "
            "providing a universal language for networked computers.\n\n"
            "Tim Berners-Lee invented the World Wide Web at CERN in 1989, creating HTML, "
            "HTTP, and the first web browser. The release of the Mosaic browser in 1993 "
            "brought the Web to a mainstream audience. Within a few years, the Internet "
            "transformed communication, commerce, and entertainment on a global scale."
        ),
    },
    {
        "title": "Chapter 6: The Mobile Revolution",
        "body": (
            "The introduction of the iPhone in 2007 fundamentally changed how people "
            "interact with technology. Smartphones combined communication, computing, "
            "and connectivity into a device that fit in a pocket. The App Store, launched "
            "in 2008, created an entirely new software ecosystem.\n\n"
            "Android, developed by Google, brought smartphone capabilities to a wider "
            "range of devices and price points. By 2015, more people accessed the Internet "
            "through mobile devices than desktop computers. Mobile computing also drove "
            "advances in battery technology, display manufacturing, and wireless networking."
        ),
    },
    {
        "title": "Chapter 7: Cloud Computing and Big Data",
        "body": (
            "Amazon Web Services launched in 2006, pioneering the concept of renting "
            "computing resources on demand. Cloud computing eliminated the need for "
            "organizations to maintain expensive on-premises hardware. Microsoft Azure "
            "and Google Cloud Platform soon followed, creating a competitive market.\n\n"
            "The explosion of digital data created new challenges and opportunities. "
            "Technologies like Hadoop and Spark enabled the processing of massive datasets "
            "across distributed clusters. Companies leveraged big data analytics to optimize "
            "operations, personalize customer experiences, and develop predictive models "
            "that transformed industries from healthcare to finance."
        ),
    },
    {
        "title": "Chapter 8: Artificial Intelligence and the Future",
        "body": (
            "Deep learning, powered by neural networks with many layers, achieved "
            "breakthroughs in image recognition, natural language processing, and game "
            "playing. AlexNet's victory in the 2012 ImageNet competition demonstrated "
            "that deep learning could outperform traditional computer vision methods.\n\n"
            "Large language models like GPT and transformer architectures brought AI "
            "capabilities to millions of users. These systems can generate text, write "
            "code, analyze documents, and assist with complex reasoning tasks. As AI "
            "continues to advance, society faces important questions about ethics, "
            "employment, privacy, and the responsible development of increasingly "
            "powerful systems."
        ),
    },
]


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, chapter in enumerate(chapters):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # Content area is inside the 30pt margin
        content_left = MARGIN + 10
        content_top = MARGIN + 10
        content_right = PAGE_W - MARGIN - 10
        content_bottom = PAGE_H - MARGIN - 10

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - MARGIN - 15),
            str(i + 1),
            fontsize=10,
            fontname="tiro",
            color=(0.3, 0.3, 0.3),
        )

        # Chapter title
        page.insert_text(
            pymupdf.Point(content_left, content_top + 30),
            chapter["title"],
            fontsize=18,
            fontname="tibo",
            color=(0, 0, 0),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(
            pymupdf.Point(content_left, content_top + 40),
            pymupdf.Point(content_right, content_top + 40),
        )
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()

        # Body text in a text box
        text_rect = pymupdf.Rect(
            content_left, content_top + 55, content_right, content_bottom
        )
        page.insert_textbox(
            text_rect,
            chapter["body"],
            fontsize=11,
            fontname="tiro",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
