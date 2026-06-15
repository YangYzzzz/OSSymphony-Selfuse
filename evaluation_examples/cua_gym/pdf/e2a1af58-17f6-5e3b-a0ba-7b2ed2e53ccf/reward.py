"""
Reward Script: Fill form fields in tax_form.pdf and save as tax_form_filled.pdf
Task ID: pdf_ro_006
Domain: pdf
Scoring:
  - Component 1: Output file exists at correct path (0.10)
  - Component 2: taxpayer_name == 'Eleanor Vance' (0.18)
  - Component 3: ssn == '***-**-7890' (0.18)
  - Component 4: filing_status == 'Single' (0.18)
  - Component 5: gross_income == '$85,420.00' (0.18)
  - Component 6: tax_owed == '$12,813.00' (0.18)
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_006'
FILLED_PATH = os.path.join(WORKDIR, 'forms', 'tax_form_filled.pdf')

# Expected field values (ground truth from task instruction)
EXPECTED_FIELDS = {
    'taxpayer_name': 'Eleanor Vance',
    'ssn': '***-**-7890',
    'filing_status': 'Single',
    'gross_income': '$85,420.00',
    'tax_owed': '$12,813.00',
}

# Points per field (5 fields x 0.18 = 0.90, plus 0.10 for file existence = 1.0)
FIELD_POINTS = 0.18
FILE_EXISTS_POINTS = 0.10


def get_form_field_values(pdf_path):
    """Read all form field values from all pages of the PDF."""
    field_values = {}
    doc = pymupdf.open(pdf_path)
    for page in doc:
        for widget in page.widgets():
            if widget.field_name:
                field_values[widget.field_name] = widget.field_value or ''
    doc.close()
    return field_values


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at /home/user/forms/tax_form_filled.pdf (0.10 points)
    # This file does NOT exist in initial_env, so it is a task-introduced change
    try:
        if os.path.isfile(FILLED_PATH):
            print(f"PASS: Component 1 — Output file exists at {FILLED_PATH} ({FILE_EXISTS_POINTS} pts)")
            total_score += FILE_EXISTS_POINTS
        else:
            print(f"FAIL: Component 1 — Output file not found at {FILLED_PATH}")
            # No file means no further checks possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load form fields from the filled PDF
    try:
        field_values = get_form_field_values(FILLED_PATH)
        print(f"INFO: Found form fields: {list(field_values.keys())}")
    except Exception as e:
        print(f"CRITICAL: Cannot read form fields from {FILLED_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Components 2-6: Verify each form field value
    component_num = 2
    for field_name, expected_value in EXPECTED_FIELDS.items():
        try:
            actual_value = field_values.get(field_name, None)
            if actual_value is not None and str(actual_value).strip() == expected_value:
                print(f"PASS: Component {component_num} — {field_name} = '{actual_value}' ({FIELD_POINTS} pts)")
                total_score += FIELD_POINTS
            else:
                print(f"FAIL: Component {component_num} — {field_name}: expected '{expected_value}', found '{actual_value}'")
        except Exception as e:
            print(f"ERROR: Component {component_num} — {field_name}: {e}")
        component_num += 1

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
