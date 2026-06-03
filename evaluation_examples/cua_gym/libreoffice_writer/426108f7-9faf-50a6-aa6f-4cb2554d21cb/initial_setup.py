"""
Initial Setup: Open product_catalog.odt from Documents, which contains a deeply nested JSON product catalog.
Task ID: osworld_multi_apps_json_reformat_writer_010
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_010'
# The task says "Open 'product_catalog.odt' from Documents"
OUTPUT = f'{WORKDIR}/Documents/product_catalog.odt'


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
    import odf.opendocument as opendoc
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf import style as odfsty

    # Ensure Documents directory exists
    docs_dir = f'{WORKDIR}/Documents'
    os.makedirs(docs_dir, exist_ok=True)

    # Build the nested JSON data
    catalog = {
        "catalog": {
            "Electronics": {
                "Smartphones": [
                    {"id": "E-SM-001", "name": "ProMax X15", "price": 1299.99, "stock": 85, "tags": ["flagship", "5G", "OLED"]},
                    {"id": "E-SM-002", "name": "Galaxy Ultra S24", "price": 1149.50, "stock": 102, "tags": ["Android", "5G", "camera"]},
                    {"id": "E-SM-003", "name": "Pixel 8 Pro", "price": 999.00, "stock": 73, "tags": ["Google", "AI", "photography"]},
                    {"id": "E-SM-004", "name": "OnePlus 12R", "price": 699.99, "stock": 134, "tags": ["fast-charge", "5G", "performance"]}
                ],
                "Laptops": [
                    {"id": "E-LP-001", "name": "ThinkPad X1 Carbon", "price": 1849.00, "stock": 41, "tags": ["business", "lightweight", "14-inch"]},
                    {"id": "E-LP-002", "name": "MacBook Pro 14", "price": 1999.99, "stock": 55, "tags": ["Apple", "M3", "professional"]},
                    {"id": "E-LP-003", "name": "Dell XPS 15", "price": 1699.00, "stock": 38, "tags": ["OLED", "Intel", "creator"]},
                    {"id": "E-LP-004", "name": "ASUS ZenBook Pro", "price": 1549.00, "stock": 62, "tags": ["OLED", "AMD", "portable"]},
                    {"id": "E-LP-005", "name": "HP Spectre x360", "price": 1399.00, "stock": 47, "tags": ["convertible", "2-in-1", "touchscreen"]}
                ]
            },
            "Clothing": {
                "Men's Wear": [
                    {"id": "C-MW-001", "name": "Classic Oxford Shirt", "price": 79.95, "stock": 215, "tags": ["formal", "cotton", "slim-fit"]},
                    {"id": "C-MW-002", "name": "Merino Wool Sweater", "price": 124.50, "stock": 188, "tags": ["wool", "casual", "warm"]},
                    {"id": "C-MW-003", "name": "Slim Chino Trousers", "price": 89.99, "stock": 302, "tags": ["casual", "stretch", "versatile"]},
                    {"id": "C-MW-004", "name": "Leather Derby Shoes", "price": 199.00, "stock": 97, "tags": ["leather", "formal", "handcrafted"]}
                ],
                "Women's Wear": [
                    {"id": "C-WW-001", "name": "Silk Blouse Elegance", "price": 149.99, "stock": 173, "tags": ["silk", "formal", "office"]},
                    {"id": "C-WW-002", "name": "High-Waist Linen Trousers", "price": 109.00, "stock": 241, "tags": ["linen", "summer", "comfortable"]},
                    {"id": "C-WW-003", "name": "Cashmere Wrap Cardigan", "price": 229.50, "stock": 88, "tags": ["cashmere", "luxury", "winter"]},
                    {"id": "C-WW-004", "name": "Printed Wrap Dress", "price": 119.95, "stock": 156, "tags": ["floral", "casual", "spring"]}
                ]
            },
            "Books": {
                "Technology": [
                    {"id": "B-TC-001", "name": "Clean Code", "price": 34.99, "stock": 420, "tags": ["programming", "best-practices", "Robert-Martin"]},
                    {"id": "B-TC-002", "name": "Designing Data-Intensive Applications", "price": 49.95, "stock": 318, "tags": ["distributed-systems", "databases", "architecture"]},
                    {"id": "B-TC-003", "name": "The Pragmatic Programmer", "price": 44.99, "stock": 375, "tags": ["software-engineering", "career", "practices"]},
                    {"id": "B-TC-004", "name": "Deep Learning with Python", "price": 39.99, "stock": 289, "tags": ["ML", "Keras", "Francois-Chollet"]},
                    {"id": "B-TC-005", "name": "System Design Interview", "price": 29.99, "stock": 512, "tags": ["interviews", "architecture", "scalability"]}
                ],
                "Fiction": [
                    {"id": "B-FI-001", "name": "The Midnight Library", "price": 16.99, "stock": 634, "tags": ["contemporary", "philosophical", "Matt-Haig"]},
                    {"id": "B-FI-002", "name": "Project Hail Mary", "price": 18.99, "stock": 571, "tags": ["sci-fi", "space", "Andy-Weir"]},
                    {"id": "B-FI-003", "name": "Klara and the Sun", "price": 17.50, "stock": 448, "tags": ["literary", "AI", "Kazuo-Ishiguro"]},
                    {"id": "B-FI-004", "name": "The Thursday Murder Club", "price": 15.99, "stock": 389, "tags": ["mystery", "cozy", "Richard-Osman"]}
                ]
            }
        }
    }

    json_text = json.dumps(catalog, indent=2)

    # Create an ODT document containing the raw JSON text
    doc = opendoc.OpenDocumentText()

    # Add a title paragraph
    title_style = Style(name="Heading1Style", family="paragraph")
    title_style.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    doc.styles.addElement(title_style)

    # Title
    h = H(outlinelevel=1, text="Product Catalog Data")
    doc.text.addElement(h)

    # Add introductory paragraph
    intro = P(text="The following JSON data represents the product catalog. Please reformat this data into a hierarchical report structure.")
    doc.text.addElement(intro)

    # Add empty paragraph separator
    doc.text.addElement(P())

    # Add the JSON as a single text block — split into lines so it's readable
    for line in json_text.split('\n'):
        p = P(text=line)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the ODT file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
