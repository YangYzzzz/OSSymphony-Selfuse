"""
Initial Setup: Library borrowing log with duplicate ISBNs
Task ID: osworld_writer_dedup_009
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import random
from docx import Document

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_writer_dedup_009'
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


def create_initial():
    doc = Document()

    # Define a set of unique ISBNs representing distinct books
    # Format: ISBN-978-X-XXX-XXXXX-X (realistic ISBN-13 format)
    unique_isbns = [
        'ISBN-978-0-061-96436-9',
        'ISBN-978-0-743-27356-5',
        'ISBN-978-0-385-33348-1',
        'ISBN-978-0-316-76948-0',
        'ISBN-978-0-307-47441-4',
        'ISBN-978-0-525-55360-5',
        'ISBN-978-0-735-22447-1',
        'ISBN-978-0-062-31609-7',
        'ISBN-978-1-982-10793-4',
        'ISBN-978-0-593-31012-3',
        'ISBN-978-0-385-54734-4',
        'ISBN-978-1-250-30185-3',
        'ISBN-978-0-316-31609-6',
        'ISBN-978-0-525-55946-1',
        'ISBN-978-1-501-15643-9',
        'ISBN-978-0-062-89418-4',
        'ISBN-978-0-385-49031-1',
        'ISBN-978-1-250-17788-8',
        'ISBN-978-0-593-08924-7',
        'ISBN-978-0-525-51916-8',
        'ISBN-978-1-982-13526-5',
        'ISBN-978-0-385-54585-2',
        'ISBN-978-0-316-45691-3',
        'ISBN-978-1-250-79097-2',
        'ISBN-978-0-062-98659-2',
        'ISBN-978-0-735-21500-4',
        'ISBN-978-0-385-53764-2',
        'ISBN-978-1-982-11238-9',
        'ISBN-978-0-062-69021-5',
        'ISBN-978-1-250-62233-4',
        'ISBN-978-0-593-18896-3',
        'ISBN-978-0-385-54754-2',
        'ISBN-978-0-316-17922-7',
        'ISBN-978-1-982-10891-7',
        'ISBN-978-0-062-96173-5',
    ]

    # Build a chronological borrow log with duplicates
    # Popular books (first 10) appear 10-15 times, rest appear 3-7 times
    random.seed(42)

    borrow_log = []

    # Add popular books multiple times (10-15 occurrences each)
    popular_books = unique_isbns[:10]
    for isbn in popular_books:
        count = random.randint(10, 15)
        borrow_log.extend([isbn] * count)

    # Add remaining books 3-7 times each
    less_popular = unique_isbns[10:]
    for isbn in less_popular:
        count = random.randint(3, 7)
        borrow_log.extend([isbn] * count)

    # Shuffle to simulate chronological borrow order (not sorted by book)
    random.shuffle(borrow_log)

    # Write each ISBN as a separate paragraph (line) in the document
    for isbn in borrow_log:
        doc.add_paragraph(isbn)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines (with duplicates): {len(borrow_log)}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
