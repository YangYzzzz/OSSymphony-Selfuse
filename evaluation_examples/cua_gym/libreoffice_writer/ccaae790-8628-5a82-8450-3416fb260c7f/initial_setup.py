"""
Initial Setup: Create org_structure.odt with raw JSON content
Task ID: osworld_multi_apps_json_reformat_writer_009
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user/Documents'
TASK_ID = 'org_structure'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    # Build the org chart JSON data
    org_data = {
        "company": "TechCorp Inc.",
        "departments": {
            "Engineering": {
                "manager": {
                    "name": "Diana Foster",
                    "title": "VP of Engineering"
                },
                "employees": [
                    {"name": "Alex Rivera", "title": "Senior Software Engineer"},
                    {"name": "Priya Nair", "title": "Software Engineer"},
                    {"name": "James O'Brien", "title": "Backend Developer"},
                    {"name": "Leila Hassan", "title": "Frontend Developer"},
                    {"name": "Tyler Brooks", "title": "DevOps Engineer"}
                ]
            },
            "Marketing": {
                "manager": {
                    "name": "Samuel Okonkwo",
                    "title": "Head of Marketing"
                },
                "employees": [
                    {"name": "Chloe Bennett", "title": "Marketing Specialist"},
                    {"name": "Ryan Park", "title": "Content Strategist"},
                    {"name": "Nina Vasquez", "title": "Brand Designer"}
                ]
            },
            "Sales": {
                "manager": {
                    "name": "Rachel Kim",
                    "title": "Director of Sales"
                },
                "employees": [
                    {"name": "Marco Delgado", "title": "Account Executive"},
                    {"name": "Sophie Turner", "title": "Sales Representative"},
                    {"name": "David Osei", "title": "Sales Representative"},
                    {"name": "Amara Singh", "title": "Business Development Rep"}
                ]
            },
            "HR": {
                "manager": {
                    "name": "Karen Walsh",
                    "title": "HR Manager"
                },
                "employees": [
                    {"name": "Ben Nakamura", "title": "HR Coordinator"},
                    {"name": "Fatima Al-Rashid", "title": "Recruiter"},
                    {"name": "Luke Petrov", "title": "Benefits Specialist"},
                    {"name": "Anita Flores", "title": "HR Assistant"},
                    {"name": "Jacob Mensah", "title": "Training Specialist"},
                    {"name": "Elena Kovac", "title": "Employee Relations Specialist"}
                ]
            }
        }
    }

    json_text = json.dumps(org_data, indent=2)

    # Use odfpy to create the ODT file with raw JSON content
    from odf.opendocument import OpenDocumentText
    from odf.text import P
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Add a monospace style for the JSON
    mono_style = Style(name="JSONContent", family="paragraph")
    mono_style.addElement(TextProperties(fontname="Courier New", fontsize="10pt"))
    doc.automaticstyles.addElement(mono_style)

    # Add the JSON content as paragraphs (one per line for readability)
    for line in json_text.split('\n'):
        p = P(stylename="JSONContent", text=line)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the ODT in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
