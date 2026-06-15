"""
Initial Setup: academic_records.odt with nested JSON student data
Task ID: osworld_multi_apps_json_reformat_writer_012
Domain: libreoffice_writer

Creates /home/user/Documents/academic_records.odt containing raw JSON
for 5 students with nested personal info, address, and course arrays.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_012'
FILENAME = 'academic_records.odt'
OUTPUT = f'{WORKDIR}/{FILENAME}'


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

    # Define 5 students with realistic nested JSON data
    # Letter grades: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0
    students = [
        {
            "student_id": "STU-2024-001",
            "name": "Emily Hartman",
            "major": "Computer Science",
            "address": {
                "street": "742 Evergreen Terrace",
                "city": "Boston",
                "country": "USA"
            },
            "courses": [
                {"code": "CS301", "name": "Data Structures", "grade": "A", "credits": 4},
                {"code": "CS302", "name": "Algorithms", "grade": "A", "credits": 4},
                {"code": "MATH201", "name": "Linear Algebra", "grade": "B", "credits": 3},
                {"code": "CS310", "name": "Operating Systems", "grade": "B", "credits": 3},
                {"code": "PHYS101", "name": "Physics I", "grade": "C", "credits": 3}
            ]
        },
        {
            "student_id": "STU-2024-002",
            "name": "Marcus Okonkwo",
            "major": "Electrical Engineering",
            "address": {
                "street": "15 Maple Grove Avenue",
                "city": "Toronto",
                "country": "Canada"
            },
            "courses": [
                {"code": "EE201", "name": "Circuit Analysis", "grade": "A", "credits": 4},
                {"code": "EE202", "name": "Electronics I", "grade": "B", "credits": 3},
                {"code": "MATH301", "name": "Differential Equations", "grade": "A", "credits": 3},
                {"code": "EE310", "name": "Signals and Systems", "grade": "B", "credits": 4},
                {"code": "EE320", "name": "Electromagnetic Fields", "grade": "C", "credits": 3},
                {"code": "PHYS201", "name": "Physics II", "grade": "B", "credits": 3}
            ]
        },
        {
            "student_id": "STU-2024-003",
            "name": "Sofia Reyes",
            "major": "Biochemistry",
            "address": {
                "street": "88 Paseo de la Reforma",
                "city": "Mexico City",
                "country": "Mexico"
            },
            "courses": [
                {"code": "CHEM301", "name": "Organic Chemistry I", "grade": "A", "credits": 4},
                {"code": "CHEM302", "name": "Organic Chemistry II", "grade": "A", "credits": 4},
                {"code": "BIO201", "name": "Molecular Biology", "grade": "B", "credits": 3},
                {"code": "CHEM310", "name": "Biochemistry", "grade": "A", "credits": 4},
                {"code": "BIO210", "name": "Cell Biology", "grade": "B", "credits": 3}
            ]
        },
        {
            "student_id": "STU-2024-004",
            "name": "James Thornton",
            "major": "Economics",
            "address": {
                "street": "23 Russell Square",
                "city": "London",
                "country": "UK"
            },
            "courses": [
                {"code": "ECON201", "name": "Microeconomics", "grade": "B", "credits": 3},
                {"code": "ECON202", "name": "Macroeconomics", "grade": "B", "credits": 3},
                {"code": "ECON310", "name": "Econometrics", "grade": "C", "credits": 4},
                {"code": "MATH210", "name": "Statistics", "grade": "B", "credits": 3},
                {"code": "ECON320", "name": "International Trade", "grade": "A", "credits": 3},
                {"code": "ECON330", "name": "Development Economics", "grade": "C", "credits": 3}
            ]
        },
        {
            "student_id": "STU-2024-005",
            "name": "Aisha Nakamura",
            "major": "Psychology",
            "address": {
                "street": "5-12 Shibuya",
                "city": "Tokyo",
                "country": "Japan"
            },
            "courses": [
                {"code": "PSYC201", "name": "Research Methods", "grade": "A", "credits": 3},
                {"code": "PSYC202", "name": "Cognitive Psychology", "grade": "A", "credits": 3},
                {"code": "PSYC310", "name": "Abnormal Psychology", "grade": "B", "credits": 3},
                {"code": "PSYC320", "name": "Social Psychology", "grade": "B", "credits": 3},
                {"code": "STAT201", "name": "Applied Statistics", "grade": "A", "credits": 3}
            ]
        }
    ]

    json_text = json.dumps(students, indent=2)

    # Create ODT file using odfpy
    from odf.opendocument import OpenDocumentText
    from odf.text import P, Span
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Add a heading paragraph
    heading_style = Style(name="Heading", family="paragraph")
    heading_style.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    doc.automaticstyles.addElement(heading_style)

    heading_p = P(stylename="Heading1")
    heading_p.addText("Academic Records - Raw Data")
    doc.text.addElement(heading_p)

    # Add a note paragraph
    note_p = P()
    note_p.addText("The following JSON contains student academic records for the current semester.")
    doc.text.addElement(note_p)

    # Add JSON content split by lines (each line as a paragraph for readability)
    for line in json_text.split('\n'):
        p = P()
        p.addText(line)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
