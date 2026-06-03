"""
Initial Setup: Create json_catalog.odt with embedded JSON product catalog
Task ID: osworld_multi_apps_media_doc_edit_007
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_doc_edit_007'
DOCUMENTS_DIR = f'{WORKDIR}/documents'
OUTPUT = f'{DOCUMENTS_DIR}/json_catalog.odt'


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
    # Ensure documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Build the ODT file using odfpy
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import P, Span, H
    from odf.namespaces import TEXTNS

    doc = OpenDocumentText()

    # Define styles
    # Normal body style
    normal_style = Style(name="Normal", family="paragraph")
    normal_tp = TextProperties(
        fontname="Liberation Serif",
        fontsize="11pt",
    )
    normal_style.addElement(normal_tp)
    doc.styles.addElement(normal_style)

    # Code block style - monospace, slightly indented
    code_style = Style(name="CodeBlock", family="paragraph")
    code_pp = ParagraphProperties(
        marginleft="0.5in",
        marginright="0.5in",
    )
    code_tp2 = TextProperties(
        fontname="Liberation Mono",
        fontsize="10pt",
    )
    code_style.addElement(code_pp)
    code_style.addElement(code_tp2)
    doc.styles.addElement(code_style)

    # Title style
    title_style = Style(name="DocumentTitle", family="paragraph")
    title_pp = ParagraphProperties(textalign="center")
    title_tp = TextProperties(
        fontname="Liberation Serif",
        fontsize="16pt",
        fontweight="bold",
    )
    title_style.addElement(title_pp)
    title_style.addElement(title_tp)
    doc.styles.addElement(title_style)

    # Heading style
    heading_style = Style(name="SectionHeading", family="paragraph")
    heading_tp = TextProperties(
        fontname="Liberation Serif",
        fontsize="13pt",
        fontweight="bold",
    )
    heading_style.addElement(heading_tp)
    doc.styles.addElement(heading_style)

    # Intro paragraph
    intro_p = P(stylename="Normal")
    intro_p.addText("This document contains a product catalog in JSON format. The JSON data below describes 8 products across 3 categories: Electronics, Books, and Home & Garden.")
    doc.text.addElement(intro_p)

    # Empty line
    doc.text.addElement(P(stylename="Normal"))

    # Section heading for JSON data
    json_heading = P(stylename="SectionHeading")
    json_heading.addText("Product Catalog Data (JSON)")
    doc.text.addElement(json_heading)

    # Empty line before JSON block
    doc.text.addElement(P(stylename="Normal"))

    # The JSON content - 8 products across 3 categories
    json_lines = [
        '[',
        '  {',
        '    "id": 1,',
        '    "name": "Wireless Noise-Cancelling Headphones",',
        '    "price": 149.99,',
        '    "category": "Electronics",',
        '    "description": "Over-ear headphones with 30-hour battery life and active noise cancellation for immersive listening experience."',
        '  },',
        '  {',
        '    "id": 2,',
        '    "name": "Smart LED Desk Lamp",',
        '    "price": 45.00,',
        '    "category": "Electronics",',
        '    "description": "Adjustable color temperature and brightness with USB charging port, ideal for home office use."',
        '  },',
        '  {',
        '    "id": 3,',
        '    "name": "Portable Bluetooth Speaker",',
        '    "price": 79.95,',
        '    "category": "Electronics",',
        '    "description": "Waterproof IPX7 rated speaker with 360-degree surround sound and 12-hour playtime."',
        '  },',
        '  {',
        '    "id": 4,',
        '    "name": "The Art of Clean Code",',
        '    "price": 34.99,',
        '    "category": "Books",',
        '    "description": "A practical guide to writing elegant, maintainable software by a seasoned software engineer."',
        '  },',
        '  {',
        '    "id": 5,',
        '    "name": "Deep Work: Rules for Focused Success",',
        '    "price": 18.50,',
        '    "category": "Books",',
        '    "description": "Strategies for cultivating deep work habits and eliminating shallow distractions in professional life."',
        '  },',
        '  {',
        '    "id": 6,',
        '    "name": "The Pragmatic Programmer",',
        '    "price": 42.00,',
        '    "category": "Books",',
        '    "description": "Classic software development guide covering topics from personal responsibility to career development and technical excellence."',
        '  },',
        '  {',
        '    "id": 7,',
        '    "name": "Ergonomic Garden Kneeler",',
        '    "price": 27.99,',
        '    "category": "Home & Garden",',
        '    "description": "Foam padded kneeler that converts to a garden seat, with tool pockets on each side panel."',
        '  },',
        '  {',
        '    "id": 8,',
        '    "name": "Stainless Steel Compost Bin",',
        '    "price": 36.50,',
        '    "category": "Home & Garden",',
        '    "description": "1.3-gallon countertop compost bin with charcoal filter to eliminate odors, fits neatly under kitchen sink."',
        '  }',
        ']',
    ]

    for line in json_lines:
        p = P(stylename="CodeBlock")
        p.addText(line)
        doc.text.addElement(p)

    # Footer note
    doc.text.addElement(P(stylename="Normal"))
    note_p = P(stylename="Normal")
    note_p.addText("Note: Parse the JSON above and reformat the content into a structured document with category sections and consistent styling.")
    doc.text.addElement(note_p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open json_catalog.odt in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
