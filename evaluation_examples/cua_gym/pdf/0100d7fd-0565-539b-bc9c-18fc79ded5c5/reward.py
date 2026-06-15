"""
Reward Script: Fill PDF form fields from JSON data
Task ID: pdf_cross_109
Domain: pdf
Scoring:
  - Precondition gate: application_filled.pdf exists (else 0.0)
  - Component 1: 'name' field == 'Sarah Mitchell'           (0.17 pts)
  - Component 2: 'address' field == '789 Pine Street...'    (0.17 pts)
  - Component 3: 'phone' field == '(303) 555-0198'          (0.17 pts)
  - Component 4: 'email' field == 'sarah.m@email.com'       (0.17 pts)
  - Component 5: 'dob' field == '1990-07-22'                (0.16 pts)
  - Component 6: 'signature' field == 'Sarah Mitchell'      (0.16 pts)
  Total: 1.0
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_109'

FILLED_PDF = os.path.join(WORKDIR, 'Documents', 'application_filled.pdf')

# Ground truth values from task context / form_data.json
EXPECTED_FIELDS = {
    'name':      'Sarah Mitchell',
    'address':   '789 Pine Street, Denver, CO 80202',
    'phone':     '(303) 555-0198',
    'email':     'sarah.m@email.com',
    'dob':       '1990-07-22',
    'signature': 'Sarah Mitchell',
}

# Weights for each field (6 fields, sum to 1.0)
FIELD_WEIGHTS = {
    'name':      0.17,
    'address':   0.17,
    'phone':     0.17,
    'email':     0.17,
    'dob':       0.16,
    'signature': 0.16,
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that all form fields in application_filled.pdf have the
    expected values from form_data.json.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all widgets (form fields) across all pages
    actual_fields = {}
    try:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            for widget in page.widgets():
                name = widget.field_name
                value = widget.field_value
                # Normalize: strip whitespace
                actual_fields[name] = (value or '').strip()
    except Exception as e:
        print(f"ERROR: Could not enumerate form fields: {e}")
    finally:
        doc.close()

    print(f"INFO: Found form fields: {list(actual_fields.keys())}")

    # Component 1: 'name' field value (0.17 points)
    try:
        expected = EXPECTED_FIELDS['name']
        actual = actual_fields.get('name', '')
        if actual == expected:
            print(f"PASS: Component 1 — name field == '{expected}' (0.17 pts)")
            total_score += FIELD_WEIGHTS['name']
        else:
            print(f"FAIL: Component 1 — name field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'address' field value (0.17 points)
    try:
        expected = EXPECTED_FIELDS['address']
        actual = actual_fields.get('address', '')
        if actual == expected:
            print(f"PASS: Component 2 — address field == '{expected}' (0.17 pts)")
            total_score += FIELD_WEIGHTS['address']
        else:
            print(f"FAIL: Component 2 — address field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'phone' field value (0.17 points)
    try:
        expected = EXPECTED_FIELDS['phone']
        actual = actual_fields.get('phone', '')
        if actual == expected:
            print(f"PASS: Component 3 — phone field == '{expected}' (0.17 pts)")
            total_score += FIELD_WEIGHTS['phone']
        else:
            print(f"FAIL: Component 3 — phone field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'email' field value (0.17 points)
    try:
        expected = EXPECTED_FIELDS['email']
        actual = actual_fields.get('email', '')
        if actual == expected:
            print(f"PASS: Component 4 — email field == '{expected}' (0.17 pts)")
            total_score += FIELD_WEIGHTS['email']
        else:
            print(f"FAIL: Component 4 — email field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 'dob' field value (0.16 points)
    try:
        expected = EXPECTED_FIELDS['dob']
        actual = actual_fields.get('dob', '')
        if actual == expected:
            print(f"PASS: Component 5 — dob field == '{expected}' (0.16 pts)")
            total_score += FIELD_WEIGHTS['dob']
        else:
            print(f"FAIL: Component 5 — dob field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 'signature' field value (0.16 points)
    try:
        expected = EXPECTED_FIELDS['signature']
        actual = actual_fields.get('signature', '')
        if actual == expected:
            print(f"PASS: Component 6 — signature field == '{expected}' (0.16 pts)")
            total_score += FIELD_WEIGHTS['signature']
        else:
            print(f"FAIL: Component 6 — signature field: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical path
if not os.path.exists(FILLED_PDF):
    print(f"File not found: {FILLED_PDF}")
    print("REWARD: 0.0")
else:
    verify_task(FILLED_PDF)
