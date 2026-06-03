"""
Initial Setup: PDF email extraction task
Task ID: pdf_cross_092
Domain: pdf
Description: Creates a 5-page contact_list.pdf with ~40 email addresses
             (some duplicates) from company.com, gmail.com, outlook.com.
             Also ensures ~/scripts/ directory exists without extract_emails.py.
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
TASK_ID = 'pdf_cross_092'
PDF_OUTPUT = f'{WORKDIR}/Documents/contact_list.pdf'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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
    # Ensure directories exist
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Remove any pre-existing output files (idempotent)
    if os.path.exists(f'{WORKDIR}/Documents/emails.json'):
        os.remove(f'{WORKDIR}/Documents/emails.json')
    if os.path.exists(f'{SCRIPTS_DIR}/extract_emails.py'):
        os.remove(f'{SCRIPTS_DIR}/extract_emails.py')

    # Define email pool: ~40 emails spread across 5 pages, with duplicates
    # Unique emails: 32 across three domains
    unique_emails = [
        # company.com emails (12)
        'alice.wang@company.com',
        'bob.harris@company.com',
        'carol.smith@company.com',
        'david.lee@company.com',
        'emma.johnson@company.com',
        'frank.miller@company.com',
        'grace.chen@company.com',
        'henry.taylor@company.com',
        'isabella.davis@company.com',
        'james.wilson@company.com',
        'katherine.moore@company.com',
        'liam.anderson@company.com',
        # gmail.com emails (10)
        'michael.brown92@gmail.com',
        'natalie.white@gmail.com',
        'oliver.jones@gmail.com',
        'patricia.garcia@gmail.com',
        'quincy.martinez@gmail.com',
        'rachel.thompson@gmail.com',
        'samuel.jackson@gmail.com',
        'tina.robinson@gmail.com',
        'umar.hassan@gmail.com',
        'victoria.lewis@gmail.com',
        # outlook.com emails (10)
        'william.clark@outlook.com',
        'xena.rodriguez@outlook.com',
        'yasmine.walker@outlook.com',
        'zachary.hall@outlook.com',
        'amelia.young@outlook.com',
        'benjamin.king@outlook.com',
        'charlotte.wright@outlook.com',
        'daniel.scott@outlook.com',
        'eleanor.green@outlook.com',
        'finn.baker@outlook.com',
    ]

    # Build ~40 emails for distribution across pages (8 duplicates)
    all_emails_in_doc = unique_emails + [
        'alice.wang@company.com',     # dup
        'michael.brown92@gmail.com',  # dup
        'rachel.thompson@gmail.com',  # dup
        'bob.harris@company.com',     # dup
        'william.clark@outlook.com',  # dup
        'grace.chen@company.com',     # dup
        'patricia.garcia@gmail.com',  # dup
        'eleanor.green@outlook.com',  # dup
    ]
    # Total: 30 unique + 8 duplicates = 38 email mentions in doc

    # Page content: realistic contact list pages
    page_data = [
        {
            "title": "Acme Corporation — Contact Directory",
            "subtitle": "Engineering & Product Teams",
            "sections": [
                {
                    "heading": "Software Engineering Department",
                    "contacts": [
                        ("Alice Wang", "Senior Engineer", all_emails_in_doc[0], "+1-408-555-0101"),
                        ("Bob Harris", "Lead Developer", all_emails_in_doc[1], "+1-408-555-0102"),
                        ("Carol Smith", "DevOps Engineer", all_emails_in_doc[2], "+1-415-555-0103"),
                        ("David Lee", "Backend Engineer", all_emails_in_doc[3], "+1-415-555-0104"),
                        ("Emma Johnson", "Frontend Developer", all_emails_in_doc[4], "+1-510-555-0105"),
                    ]
                },
                {
                    "heading": "Product Management",
                    "contacts": [
                        ("Frank Miller", "Product Manager", all_emails_in_doc[5], "+1-650-555-0201"),
                        ("Grace Chen", "UX Designer", all_emails_in_doc[6], "+1-650-555-0202"),
                    ]
                }
            ]
        },
        {
            "title": "Acme Corporation — Contact Directory",
            "subtitle": "Sales & Marketing Teams",
            "sections": [
                {
                    "heading": "Sales Department",
                    "contacts": [
                        ("Henry Taylor", "Sales Director", all_emails_in_doc[7], "+1-212-555-0301"),
                        ("Isabella Davis", "Account Executive", all_emails_in_doc[8], "+1-212-555-0302"),
                        ("James Wilson", "Sales Engineer", all_emails_in_doc[9], "+1-212-555-0303"),
                        ("Katherine Moore", "Regional Manager", all_emails_in_doc[10], "+1-646-555-0304"),
                        ("Liam Anderson", "Business Dev.", all_emails_in_doc[11], "+1-646-555-0305"),
                    ]
                },
                {
                    "heading": "Marketing Team",
                    "contacts": [
                        ("Michael Brown", "Marketing Lead", all_emails_in_doc[12], "+1-415-555-0401"),
                        ("Natalie White", "Content Strategist", all_emails_in_doc[13], "+1-415-555-0402"),
                        ("Oliver Jones", "SEO Specialist", all_emails_in_doc[14], "+1-415-555-0403"),
                    ]
                }
            ]
        },
        {
            "title": "Acme Corporation — Contact Directory",
            "subtitle": "Finance & HR Teams",
            "sections": [
                {
                    "heading": "Finance Department",
                    "contacts": [
                        ("Patricia Garcia", "CFO", all_emails_in_doc[15], "+1-212-555-0501"),
                        ("Quincy Martinez", "Finance Analyst", all_emails_in_doc[16], "+1-212-555-0502"),
                        ("Rachel Thompson", "Controller", all_emails_in_doc[17], "+1-212-555-0503"),
                        ("Samuel Jackson", "Tax Specialist", all_emails_in_doc[18], "+1-646-555-0504"),
                    ]
                },
                {
                    "heading": "Human Resources",
                    "contacts": [
                        ("Tina Robinson", "HR Director", all_emails_in_doc[19], "+1-415-555-0601"),
                        ("Umar Hassan", "Recruiter", all_emails_in_doc[20], "+1-415-555-0602"),
                        ("Victoria Lewis", "Benefits Manager", all_emails_in_doc[21], "+1-415-555-0603"),
                    ]
                }
            ]
        },
        {
            "title": "Acme Corporation — Contact Directory",
            "subtitle": "Operations & IT Teams",
            "sections": [
                {
                    "heading": "IT Department",
                    "contacts": [
                        ("William Clark", "IT Director", all_emails_in_doc[22], "+1-408-555-0701"),
                        ("Xena Rodriguez", "Systems Admin", all_emails_in_doc[23], "+1-408-555-0702"),
                        ("Yasmine Walker", "Network Engineer", all_emails_in_doc[24], "+1-408-555-0703"),
                        ("Zachary Hall", "Security Analyst", all_emails_in_doc[25], "+1-408-555-0704"),
                    ]
                },
                {
                    "heading": "Operations",
                    "contacts": [
                        ("Amelia Young", "COO", all_emails_in_doc[26], "+1-650-555-0801"),
                        ("Benjamin King", "Operations Mgr.", all_emails_in_doc[27], "+1-650-555-0802"),
                        ("Charlotte Wright", "Supply Chain", all_emails_in_doc[28], "+1-650-555-0803"),
                    ]
                }
            ]
        },
        {
            "title": "Acme Corporation — Contact Directory",
            "subtitle": "Legal & Executive Teams + Updated Contacts",
            "sections": [
                {
                    "heading": "Legal Department",
                    "contacts": [
                        ("Daniel Scott", "General Counsel", all_emails_in_doc[29], "+1-212-555-0901"),
                        ("Eleanor Green", "Associate Counsel", all_emails_in_doc[30], "+1-212-555-0902"),
                        ("Finn Baker", "Paralegal", all_emails_in_doc[31], "+1-212-555-0903"),
                    ]
                },
                {
                    "heading": "Updated / Duplicate Entries (Please discard old records)",
                    "contacts": [
                        ("Alice Wang", "Senior Engineer (updated)", all_emails_in_doc[32], "+1-408-555-0101"),
                        ("Michael Brown", "Marketing Lead (new ext.)", all_emails_in_doc[33], "+1-415-555-9401"),
                        ("Rachel Thompson", "Controller (promoted)", all_emails_in_doc[34], "+1-212-555-9503"),
                        ("Bob Harris", "Lead Developer (updated)", all_emails_in_doc[35], "+1-408-555-9102"),
                        ("William Clark", "IT Director (updated)", all_emails_in_doc[36], "+1-408-555-9701"),
                        ("Grace Chen", "UX Designer (new ext.)", all_emails_in_doc[37], "+1-650-555-9202"),
                        ("Patricia Garcia", "CFO (updated)", all_emails_in_doc[38], "+1-212-555-9501"),
                        ("Eleanor Green", "Sr. Associate Counsel", all_emails_in_doc[39], "+1-212-555-9902"),
                    ]
                }
            ]
        },
    ]

    doc = pymupdf.open()

    for page_idx, page_info in enumerate(page_data):
        page = doc.new_page(width=612, height=792)  # Letter size

        y = 50

        # Page title
        page.insert_text(
            pymupdf.Point(50, y),
            page_info["title"],
            fontsize=16,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )
        y += 22

        # Subtitle
        page.insert_text(
            pymupdf.Point(50, y),
            page_info["subtitle"],
            fontsize=12,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )
        y += 10

        # Divider line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(50, y + 5), pymupdf.Point(562, y + 5))
        shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
        shape.commit()
        y += 18

        # Page number
        page.insert_text(
            pymupdf.Point(530, 780),
            f"Page {page_idx + 1} of 5",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Sections
        for section in page_info["sections"]:
            # Section heading
            page.insert_text(
                pymupdf.Point(50, y),
                section["heading"],
                fontsize=11,
                fontname="hebo",
                color=(0.2, 0.2, 0.2),
            )
            y += 6

            # Underline for heading
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(50, y), pymupdf.Point(400, y))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()
            y += 12

            # Column headers
            page.insert_text(pymupdf.Point(50, y), "Name", fontsize=9, fontname="hebo", color=(0.4, 0.4, 0.4))
            page.insert_text(pymupdf.Point(175, y), "Title", fontsize=9, fontname="hebo", color=(0.4, 0.4, 0.4))
            page.insert_text(pymupdf.Point(295, y), "Email", fontsize=9, fontname="hebo", color=(0.4, 0.4, 0.4))
            page.insert_text(pymupdf.Point(460, y), "Phone", fontsize=9, fontname="hebo", color=(0.4, 0.4, 0.4))
            y += 4

            # Thin column header underline
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(50, y), pymupdf.Point(562, y))
            shape.finish(color=(0.85, 0.85, 0.85), width=0.3)
            shape.commit()
            y += 10

            # Contacts
            for i, (name, title, email, phone) in enumerate(section["contacts"]):
                row_color = (0.96, 0.96, 0.98) if i % 2 == 0 else (1.0, 1.0, 1.0)

                # Row background
                shape = page.new_shape()
                shape.draw_rect(pymupdf.Rect(48, y - 9, 564, y + 4))
                shape.finish(fill=row_color, color=None, width=0)
                shape.commit()

                # Name
                page.insert_text(pymupdf.Point(50, y), name, fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1))
                # Title
                page.insert_text(pymupdf.Point(175, y), title, fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
                # Email (blue, monospace feel)
                page.insert_text(pymupdf.Point(295, y), email, fontsize=8.5, fontname="cour", color=(0.0, 0.2, 0.7))
                # Phone
                page.insert_text(pymupdf.Point(460, y), phone, fontsize=8.5, fontname="helv", color=(0.3, 0.3, 0.3))

                y += 15

            y += 12  # Gap between sections

    # Save the PDF
    doc.save(PDF_OUTPUT)
    doc.close()
    print(f'Initial PDF created: {PDF_OUTPUT}')

    # Confirm scripts dir exists without extract_emails.py
    assert os.path.isdir(SCRIPTS_DIR), f"Scripts dir not created: {SCRIPTS_DIR}"
    assert not os.path.exists(f'{SCRIPTS_DIR}/extract_emails.py'), "extract_emails.py should not exist yet"
    assert not os.path.exists(f'{WORKDIR}/Documents/emails.json'), "emails.json should not exist yet"
    print(f'Scripts dir ready (no extract_emails.py): {SCRIPTS_DIR}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
