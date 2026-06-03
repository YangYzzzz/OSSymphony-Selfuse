"""
Reward Script: Fill tax_form_w2.pdf with specified form field values
Task ID: pdf_basic_072
Domain: pdf
Scoring:
  Component 1: 'Employer Name' field == 'TechStart Inc.' (0.25 pts)
  Component 2: 'Wages' field == '78500.00' (0.25 pts)
  Component 3: 'Federal Tax Withheld' field == '15700.00' (0.25 pts)
  Component 4: 'State' field == 'NY' (0.25 pts)
  Total: 1.0
"""

import os

# Try pymupdf first (v1.24+), fall back to fitz
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_basic_072'
FILE_PATH = '/home/user/Desktop/tax_form_w2.pdf'


def get_form_fields(pdf_path):
    """Read all form field names and values from the PDF."""
    doc = pymupdf.open(pdf_path)
    fields = {}
    for page in doc:
        for widget in page.widgets():
            fields[widget.field_name] = widget.field_value
    doc.close()
    return fields


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Each of the 4 form fields is worth 0.25 points.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be openable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        fields = get_form_fields(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read form fields from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found fields: {fields}")

    # Component 1: 'Employer Name' field == 'TechStart Inc.' (0.25 points)
    try:
        actual = fields.get('Employer Name', None)
        expected = 'TechStart Inc.'
        if actual is not None and str(actual).strip() == expected:
            print(f"PASS: Component 1 — 'Employer Name' = {repr(actual)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'Employer Name': expected {repr(expected)}, found {repr(actual)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Wages' field == '78500.00' (0.25 points)
    try:
        actual = fields.get('Wages', None)
        expected = '78500.00'
        if actual is not None and str(actual).strip() == expected:
            print(f"PASS: Component 2 — 'Wages' = {repr(actual)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — 'Wages': expected {repr(expected)}, found {repr(actual)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Federal Tax Withheld' field == '15700.00' (0.25 points)
    try:
        actual = fields.get('Federal Tax Withheld', None)
        expected = '15700.00'
        if actual is not None and str(actual).strip() == expected:
            print(f"PASS: Component 3 — 'Federal Tax Withheld' = {repr(actual)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — 'Federal Tax Withheld': expected {repr(expected)}, found {repr(actual)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'State' field == 'NY' (0.25 points)
    try:
        actual = fields.get('State', None)
        expected = 'NY'
        if actual is not None and str(actual).strip() == expected:
            print(f"PASS: Component 4 — 'State' = {repr(actual)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — 'State': expected {repr(expected)}, found {repr(actual)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(FILE_PATH)
