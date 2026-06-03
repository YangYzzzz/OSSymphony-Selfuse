"""
Initial Setup: Create mail merge envelopes for vendors
Task ID: writer_mt_013
Domain: libreoffice_writer

Creates:
  - /home/user/Desktop/company_logo.png (200x80px company logo)
  - /home/user/vendors.csv (25 vendor records)
  - Opens LibreOffice Writer with a blank document
"""

import csv
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_013'
DESKTOP = f'{WORKDIR}/Desktop'
LOGO_PATH = f'{DESKTOP}/company_logo.png'
CSV_PATH = f'{WORKDIR}/vendors.csv'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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


def create_logo():
    """Create a simple company logo PNG (200x80px)."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGBA', (200, 80), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Blue rectangle background
    draw.rounded_rectangle([5, 5, 195, 75], radius=8, fill=(0, 71, 171, 255))

    # Company name text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except (IOError, OSError):
        font = ImageFont.load_default()

    draw.text((20, 15), "NEXUS", fill=(255, 255, 255), font=font)

    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except (IOError, OSError):
        font_small = ImageFont.load_default()

    draw.text((20, 45), "Global Supply Co.", fill=(200, 220, 255), font=font_small)

    os.makedirs(DESKTOP, exist_ok=True)
    img.save(LOGO_PATH)
    print(f'Logo created: {LOGO_PATH}')


def create_vendor_database():
    """Create a CSV with 25 vendor records."""
    vendors = [
        ("Müller Industrietechnik GmbH", "Hans Müller", "Industriestraße 45", "Munich", "Germany", "80331"),
        ("Precision Parts Ltd", "James Whitfield", "12 Kingsway Road", "London", "United Kingdom", "WC2B 6NH"),
        ("Sakura Electronics Co.", "Yuki Tanaka", "3-14-8 Shinjuku", "Tokyo", "Japan", "160-0022"),
        ("Nordic Supply AB", "Erik Johansson", "Vasagatan 28", "Stockholm", "Sweden", "111 20"),
        ("Atlas Machinery S.p.A.", "Marco Bianchi", "Via Roma 156", "Milan", "Italy", "20121"),
        ("Maple Leaf Components Inc.", "Sarah Henderson", "450 Bay Street", "Toronto", "Canada", "M5H 2Y4"),
        ("Pacific Trade Solutions Pty", "David Chen", "88 Collins Street", "Melbourne", "Australia", "3000"),
        ("Rhine Valley Chemicals AG", "Klara Hoffmann", "Rheinstraße 12", "Düsseldorf", "Germany", "40213"),
        ("Iberian Metal Works S.L.", "Carlos Fernández", "Calle Mayor 78", "Madrid", "Spain", "28013"),
        ("Summit Engineering LLC", "Robert Parker", "2100 Market Street", "Philadelphia", "United States", "19103"),
        ("Han Wei Industrial Co.", "Wei Zhang", "88 Nanjing Road", "Shanghai", "China", "200001"),
        ("Fjord Logistics AS", "Ingrid Larsen", "Storgata 15", "Oslo", "Norway", "0155"),
        ("Coral Bay Trading Pte Ltd", "Priya Nair", "1 Raffles Place", "Singapore", "Singapore", "048616"),
        ("Andean Minerals S.A.", "Luis Morales", "Av. Providencia 1234", "Santiago", "Chile", "7500000"),
        ("Celtic Precision Eng. Ltd", "Fiona O'Brien", "23 Grafton Street", "Dublin", "Ireland", "D02 HK78"),
        ("Brasília Auto Parts Ltda", "Pedro Santos", "Rua Augusta 500", "São Paulo", "Brazil", "01304-000"),
        ("Silk Road Textiles FZE", "Amir Hassan", "Jebel Ali Free Zone", "Dubai", "UAE", "17000"),
        ("Aurora Optics Oy", "Mikko Virtanen", "Mannerheimintie 20", "Helsinki", "Finland", "00100"),
        ("Kalahari Resources Ltd", "Thabo Molefe", "44 Sandton Drive", "Johannesburg", "South Africa", "2196"),
        ("Vienna Instruments GmbH", "Anna Schneider", "Mariahilfer Str. 90", "Vienna", "Austria", "1070"),
        ("Bengal Spice Exports Pvt", "Arjun Chatterjee", "Park Street 15", "Kolkata", "India", "700016"),
        ("Aegean Maritime S.A.", "Nikos Papadopoulos", "Akti Miaouli 51", "Piraeus", "Greece", "18536"),
        ("Zurich Timing AG", "Lukas Brunner", "Bahnhofstrasse 42", "Zurich", "Switzerland", "8001"),
        ("New Seoul Tech Co.", "Min-ji Park", "Gangnam-daero 396", "Seoul", "South Korea", "06253"),
        ("Sahara Solar Solutions SARL", "Fatima Benali", "Boulevard Mohammed V", "Casablanca", "Morocco", "20250"),
    ]

    headers = ['VendorName', 'ContactPerson', 'Address', 'City', 'Country', 'PostalCode']
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(vendors)
    print(f'Vendor database created: {CSV_PATH} ({len(vendors)} records)')


def create_initial_document():
    """Create a blank Writer document as the starting point."""
    from docx import Document

    doc = Document()
    # Just a blank document - the agent needs to create the envelope layout
    doc.save(OUTPUT)
    print(f'Initial document created: {OUTPUT}')


def main():
    create_logo()
    create_vendor_database()
    create_initial_document()

    # Open LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
