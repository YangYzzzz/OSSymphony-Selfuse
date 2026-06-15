"""
Initial Setup: Create mailing labels using Avery 5160 format
Task ID: writer_mt_010
Domain: libreoffice_writer

Creates:
  - /home/user/Desktop/mailing_list.csv with 30 realistic contacts
  - /home/user/writer_mt_010.docx blank document
  - Opens LibreOffice Writer with the blank document
"""

import csv
import os
import shlex
import subprocess
import time

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_010'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'
CSV_PATH = f'{WORKDIR}/Desktop/mailing_list.csv'


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


def create_csv():
    """Create a realistic mailing list CSV with 30 records."""
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    contacts = [
        ("Sarah Chen", "1420 Oak Valley Drive", "Austin", "TX", "78701"),
        ("Marcus Johnson", "8835 Riverside Boulevard", "Portland", "OR", "97201"),
        ("Elena Rodriguez", "2541 Maple Street", "San Diego", "CA", "92101"),
        ("David Kim", "670 Birchwood Lane", "Seattle", "WA", "98101"),
        ("Rachel Foster", "3312 Sunset Avenue", "Denver", "CO", "80201"),
        ("James O'Brien", "4480 Elmwood Court", "Chicago", "IL", "60601"),
        ("Priya Patel", "1127 Cedar Ridge Road", "Phoenix", "AZ", "85001"),
        ("Michael Torres", "5593 Willow Creek Way", "Miami", "FL", "33101"),
        ("Amanda Blackwell", "7021 Pinehurst Drive", "Nashville", "TN", "37201"),
        ("Christopher Lee", "928 Magnolia Terrace", "Atlanta", "GA", "30301"),
        ("Jessica Huang", "3856 Lakeview Boulevard", "Minneapolis", "MN", "55401"),
        ("Robert Nakamura", "6134 Brookside Lane", "San Francisco", "CA", "94101"),
        ("Olivia Martinez", "2297 Chestnut Hill Road", "Boston", "MA", "02101"),
        ("Thomas Anderson", "4718 Sycamore Street", "Dallas", "TX", "75201"),
        ("Natalie Wright", "1845 Foxglove Court", "Raleigh", "NC", "27601"),
        ("Andrew Sullivan", "3062 Hawthorn Avenue", "Columbus", "OH", "43201"),
        ("Maria Gonzalez", "5479 Aspen Ridge Drive", "Las Vegas", "NV", "89101"),
        ("Daniel Cooper", "7803 Ivy Lane", "Salt Lake City", "UT", "84101"),
        ("Samantha Reed", "1256 Cherry Blossom Way", "Charlotte", "NC", "28201"),
        ("William Chang", "4391 Cottonwood Circle", "Kansas City", "MO", "64101"),
        ("Catherine Brooks", "6627 Dogwood Trail", "Indianapolis", "IN", "46201"),
        ("Joseph Garcia", "2984 Juniper Street", "San Antonio", "TX", "78201"),
        ("Emily Watson", "8150 Hemlock Drive", "Philadelphia", "PA", "19101"),
        ("Benjamin Clark", "3573 Spruce Hollow Road", "Jacksonville", "FL", "32201"),
        ("Hannah Mitchell", "5816 Redwood Avenue", "Sacramento", "CA", "95801"),
        ("Kevin Murphy", "1439 Cypress Point Lane", "Milwaukee", "WI", "53201"),
        ("Lisa Yamamoto", "7264 Birch Glen Court", "Honolulu", "HI", "96801"),
        ("Patrick O'Connor", "4097 Oakridge Drive", "Oklahoma City", "OK", "73101"),
        ("Stephanie Lewis", "6582 Walnut Creek Road", "Louisville", "KY", "40201"),
        ("George Harrison", "2315 Palm Valley Way", "Tucson", "AZ", "85701"),
    ]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Street", "City", "State", "Zip"])
        for contact in contacts:
            writer.writerow(contact)

    print(f'CSV created: {CSV_PATH} ({len(contacts)} records)')


def create_blank_document():
    """Create a blank Writer document as the initial state."""
    doc = Document()
    # Add a single empty paragraph (default blank document)
    doc.save(OUTPUT)
    print(f'Blank document created: {OUTPUT}')


def main():
    create_csv()
    create_blank_document()

    # Launch LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
