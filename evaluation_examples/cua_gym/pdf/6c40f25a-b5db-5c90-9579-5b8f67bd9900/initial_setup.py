"""
Initial Setup: Build a PDF form validation engine
Task ID: pdf_gf3_042
Domain: pdf

Creates:
  /home/user/forms/filled_application.pdf  - PDF form with 12 filled fields
  /home/user/rules/form_rules.json         - Validation rules for each field
  /home/user/scripts/                      - Empty directory (agent must create form_validator.py)
"""

import json
import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_042'
FORMS_DIR = f'{WORKDIR}/forms'
RULES_DIR = f'{WORKDIR}/rules'
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


def create_filled_form():
    """Create a PDF form with 12 fields, pre-filled with realistic data."""
    os.makedirs(FORMS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    # Title
    page.insert_text(
        pymupdf.Point(72, 50),
        "Employment Application Form",
        fontsize=20,
        fontname="hebo",
        color=(0, 0, 0.5),
    )
    page.insert_text(
        pymupdf.Point(72, 75),
        "Please fill in all required fields below.",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Define 12 form fields with labels and filled values
    fields = [
        # (field_name, label, y_pos, field_type, value, rect_width, extra_kwargs)
        ("first_name", "First Name *", 110, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "Elena", 200, {}),
        ("last_name", "Last Name *", 150, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "Kowalski", 200, {}),
        ("email", "Email Address *", 190, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "elena.kowalski@techcorp.com", 250, {}),
        ("phone", "Phone Number", 230, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "555-0142", 200, {}),
        ("date_of_birth", "Date of Birth *", 270, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "1992-07-15", 150, {}),
        ("application_date", "Application Date *", 310, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "2025-03-20", 150, {}),
        ("years_experience", "Years of Experience *", 350, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "8", 80, {}),
        ("desired_salary", "Desired Salary ($) *", 390, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "95000", 120, {}),
        ("department", "Department *", 430, pymupdf.PDF_WIDGET_TYPE_COMBOBOX,
         "Engineering", 200,
         {"choices": ["Engineering", "Marketing", "Finance", "HR", "Operations"]}),
        ("education_level", "Education Level", 470, pymupdf.PDF_WIDGET_TYPE_COMBOBOX,
         "Masters", 200,
         {"choices": ["High School", "Bachelors", "Masters", "PhD"]}),
        ("agree_terms", "I agree to terms *", 510, pymupdf.PDF_WIDGET_TYPE_CHECKBOX,
         "Yes", 20, {}),
        ("cover_letter", "Cover Letter Summary", 550, pymupdf.PDF_WIDGET_TYPE_TEXT,
         "I am excited to apply for this position. With over 8 years of software engineering experience at leading companies, I bring expertise in distributed systems and cloud infrastructure.",
         450, {"multiline": True, "height": 70}),
    ]

    for fname, label, y, ftype, value, rw, extra in fields:
        # Label
        page.insert_text(
            pymupdf.Point(72, y + 15),
            label + ":",
            fontsize=10,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Widget
        widget = pymupdf.Widget()
        widget.field_type = ftype
        widget.field_name = fname

        if ftype == pymupdf.PDF_WIDGET_TYPE_CHECKBOX:
            widget.rect = pymupdf.Rect(250, y, 250 + rw, y + 20)
            widget.field_value = value
            widget.border_color = (0, 0, 0)
        elif ftype == pymupdf.PDF_WIDGET_TYPE_COMBOBOX:
            widget.rect = pymupdf.Rect(250, y, 250 + rw, y + 22)
            widget.choice_values = extra.get("choices", [])
            widget.field_value = value
            widget.text_fontsize = 10
            widget.fill_color = (1, 1, 1)
            widget.border_color = (0.5, 0.5, 0.5)
        else:
            h = extra.get("height", 20)
            widget.rect = pymupdf.Rect(250, y, 250 + rw, y + h)
            widget.field_value = value
            widget.text_fontsize = 10
            widget.fill_color = (0.97, 0.97, 0.97)
            widget.border_color = (0.5, 0.5, 0.5)
            if extra.get("multiline"):
                widget.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE

        page.add_widget(widget)

    output_path = f'{FORMS_DIR}/filled_application.pdf'
    doc.save(output_path)
    doc.close()
    print(f'Created filled PDF form: {output_path}')
    return output_path


def create_rules():
    """Create validation rules JSON file."""
    os.makedirs(RULES_DIR, exist_ok=True)

    rules = [
        {
            "field_name": "first_name",
            "type": "text",
            "required": True,
            "min_length": 2,
            "max_length": 50,
            "regex_pattern": None
        },
        {
            "field_name": "last_name",
            "type": "text",
            "required": True,
            "min_length": 2,
            "max_length": 50,
            "regex_pattern": None
        },
        {
            "field_name": "email",
            "type": "email",
            "required": True,
            "min_length": 5,
            "max_length": 100,
            "regex_pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        {
            "field_name": "phone",
            "type": "text",
            "required": False,
            "min_length": 7,
            "max_length": 20,
            "regex_pattern": "^[0-9\\-\\+\\(\\)\\s]+$"
        },
        {
            "field_name": "date_of_birth",
            "type": "date",
            "required": True,
            "min_length": 10,
            "max_length": 10,
            "regex_pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        {
            "field_name": "application_date",
            "type": "date",
            "required": True,
            "min_length": 10,
            "max_length": 10,
            "regex_pattern": "^\\d{4}-\\d{2}-\\d{2}$"
        },
        {
            "field_name": "years_experience",
            "type": "number",
            "required": True,
            "min_length": 1,
            "max_length": 3,
            "regex_pattern": "^\\d+$"
        },
        {
            "field_name": "desired_salary",
            "type": "number",
            "required": True,
            "min_length": 1,
            "max_length": 10,
            "regex_pattern": "^\\d+$"
        },
        {
            "field_name": "department",
            "type": "text",
            "required": True,
            "min_length": 2,
            "max_length": 50,
            "regex_pattern": None
        },
        {
            "field_name": "education_level",
            "type": "text",
            "required": False,
            "min_length": 2,
            "max_length": 30,
            "regex_pattern": None
        },
        {
            "field_name": "agree_terms",
            "type": "text",
            "required": True,
            "min_length": 1,
            "max_length": 10,
            "regex_pattern": None
        },
        {
            "field_name": "cover_letter",
            "type": "text",
            "required": False,
            "min_length": 10,
            "max_length": 2000,
            "regex_pattern": None
        }
    ]

    rules_path = f'{RULES_DIR}/form_rules.json'
    with open(rules_path, 'w') as f:
        json.dump(rules, f, indent=2)
    print(f'Created rules file: {rules_path}')


def create_scripts_dir():
    """Create empty scripts directory (agent must create form_validator.py)."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    print(f'Created scripts directory: {SCRIPTS_DIR}')


def main():
    pdf_path = create_filled_form()
    create_rules()
    create_scripts_dir()

    # GUI-ready startup: open the PDF form and a file manager
    launch_gui(f'evince "{pdf_path}"', delay_sec=2.0)
    launch_gui(f'nautilus "{WORKDIR}"', delay_sec=1.0)
    print('GUI_READY: launched evince and nautilus with DISPLAY=:0')


main()
