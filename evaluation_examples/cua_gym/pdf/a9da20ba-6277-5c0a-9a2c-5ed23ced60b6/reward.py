"""
Reward Script: Fill court filing form with case information
Task ID: pdf_legal_013
Domain: pdf
Scoring:
  - 6 form field checks (each ~0.167 points) = 1.0 total
  - File existence is a precondition gate (0 points if missing)
  - Each field must contain the exact expected value
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_013'
FILE_PATH = f'{WORKDIR}/legal/forms/civil_cover_sheet_filled.pdf'

# Expected form field values from task instruction
EXPECTED_FIELDS = {
    'CaseTitle': 'Smith v. Johnson',
    'CaseNumber': '2024-CV-5678',
    'Court': 'Superior Court of California',
    'FilingDate': '03/15/2024',
    'AttorneyName': 'Sarah Chen, Esq.',
    'BarNumber': '123456',
}

# Points per field (6 fields, equal weight)
POINTS_PER_FIELD = 1.0 / 6.0  # ~0.1667 each


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all form field values
    field_values = {}
    try:
        for page in doc:
            for widget in page.widgets():
                if widget.field_name:
                    field_values[widget.field_name] = widget.field_value or ''
        print(f"INFO: Found {len(field_values)} form fields: {list(field_values.keys())}")
    except Exception as e:
        print(f"CRITICAL: Cannot read form fields: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    doc.close()

    # Verify each expected field value
    for i, (field_name, expected_value) in enumerate(EXPECTED_FIELDS.items(), 1):
        try:
            actual_value = field_values.get(field_name, '')
            if str(actual_value).strip() == str(expected_value).strip():
                print(f"PASS: Component {i} — {field_name} = '{actual_value}' ({POINTS_PER_FIELD:.4f} pts)")
                total_score += POINTS_PER_FIELD
            else:
                print(f"FAIL: Component {i} — {field_name}: expected '{expected_value}', found '{actual_value}'")
        except Exception as e:
            print(f"ERROR: Component {i} — {field_name}: {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
