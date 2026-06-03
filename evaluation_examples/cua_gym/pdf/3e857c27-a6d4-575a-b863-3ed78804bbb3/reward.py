"""
Reward Script: Fill permit_application.pdf form fields in Evince
Task ID: pdf_basic_096
Domain: pdf
Scoring:
  Component 1: Project Type dropdown == 'Residential'           (0.30 pts)
  Component 2: Property Address == '456 Oak Lane, Austin, TX 78701' (0.30 pts)
  Component 3: Estimated Cost == '$45,000'                      (0.20 pts)
  Component 4: Start Date == '04/01/2025'                       (0.20 pts)
  Total: 1.0
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Desktop'
TASK_FILE = 'permit_application.pdf'
PDF_PATH = os.path.join(WORKDIR, TASK_FILE)


def verify_task(pdf_path: str) -> float:
    """
    Verify that all four required form fields have been filled with the
    task-specified values. Returns a progressive float 0.0 – 1.0.
    Only the four fields explicitly listed in the task instruction are scored;
    other pre-existing fields that remain empty are NOT scored (they are
    preconditions / unrelated to the task).
    """
    total_score = 0.0

    # Load form fields from the PDF
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all widget values into a dict for easy lookup
    fields = {}
    try:
        for page in doc:
            for widget in page.widgets():
                fields[widget.field_name] = widget.field_value
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot read form fields: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    print(f"DEBUG: Extracted fields: {fields}")

    # Component 1: 'Project Type' dropdown should be 'Residential' (0.30 points)
    try:
        actual_type = str(fields.get('Project Type', '') or '').strip()
        expected_type = 'Residential'
        if actual_type == expected_type:
            print(f"PASS: Component 1 — Project Type == '{expected_type}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Project Type: expected '{expected_type}', found '{actual_type}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Property Address' text field (0.30 points)
    try:
        actual_addr = str(fields.get('Property Address', '') or '').strip()
        expected_addr = '456 Oak Lane, Austin, TX 78701'
        if actual_addr == expected_addr:
            print(f"PASS: Component 2 — Property Address == '{expected_addr}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Property Address: expected '{expected_addr}', found '{actual_addr}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Estimated Cost' text field (0.20 points)
    try:
        actual_cost = str(fields.get('Estimated Cost', '') or '').strip()
        expected_cost = '$45,000'
        if actual_cost == expected_cost:
            print(f"PASS: Component 3 — Estimated Cost == '{expected_cost}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Estimated Cost: expected '{expected_cost}', found '{actual_cost}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'Start Date' text field (0.20 points)
    try:
        actual_date = str(fields.get('Start Date', '') or '').strip()
        expected_date = '04/01/2025'
        if actual_date == expected_date:
            print(f"PASS: Component 4 — Start Date == '{expected_date}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Start Date: expected '{expected_date}', found '{actual_date}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
