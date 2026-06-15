"""
Reward Script: Fill multi-page grant application PDF form
Task ID: pdf_fm_024
Domain: pdf
Scoring:
  - Component 1: Page 1 text fields (pi_name, institution, grant_title) — 0.3 pts
  - Component 2: Page 2 text fields (budget_total, duration, start_date) — 0.3 pts
  - Component 3: Page 3 checkboxes (irb_approved, conflict_none, terms_accepted) — 0.3 pts
  - Component 4: Non-mentioned fields remain empty/unchecked — 0.1 pts
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_024'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'grant_application_filled.pdf')

# Expected field values (from task instruction)
EXPECTED_TEXT_FIELDS_PAGE1 = {
    'pi_name': 'Dr. Elena Vasquez',
    'institution': 'MIT',
    'grant_title': 'Neural Interface Design',
}

EXPECTED_TEXT_FIELDS_PAGE2 = {
    'budget_total': '$450,000',
    'duration': '3 years',
    'start_date': 'January 2026',
}

EXPECTED_CHECKBOXES_PAGE3 = ['irb_approved', 'conflict_none', 'terms_accepted']

# Fields that should remain empty (pages 4 and 5)
SHOULD_BE_EMPTY_FIELDS = [
    'abstract', 'keywords',
    'reference_1_name', 'reference_1_email',
    'reference_2_name', 'reference_2_email',
    'reference_3_name', 'reference_3_email',
]


def get_all_fields(doc):
    """Extract all form fields from all pages into a dict keyed by field_name."""
    fields = {}
    for page in doc:
        for w in page.widgets():
            fields[w.field_name] = {
                'value': w.field_value,
                'type': w.field_type_string,
            }
    return fields


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    fields = get_all_fields(doc)
    doc.close()

    # Component 1: Page 1 text fields (0.3 points)
    # pi_name, institution, grant_title must match exact values
    try:
        page1_passed = 0
        for field_name, expected_value in EXPECTED_TEXT_FIELDS_PAGE1.items():
            if field_name in fields:
                actual = fields[field_name]['value']
                if actual is not None and str(actual).strip() == expected_value:
                    print(f"PASS: {field_name} = '{actual}'")
                    page1_passed += 1
                else:
                    print(f"FAIL: {field_name} — expected '{expected_value}', found '{actual}'")
            else:
                print(f"FAIL: {field_name} — field not found in PDF")

        if page1_passed == 3:
            print(f"PASS: Component 1 — All Page 1 fields correct (0.3 pts)")
            total_score += 0.3
        elif page1_passed > 0:
            partial = round(0.1 * page1_passed, 2)
            print(f"PARTIAL: Component 1 — {page1_passed}/3 Page 1 fields correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No Page 1 fields correct")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 2 text fields (0.3 points)
    # budget_total, duration, start_date must match exact values
    try:
        page2_passed = 0
        for field_name, expected_value in EXPECTED_TEXT_FIELDS_PAGE2.items():
            if field_name in fields:
                actual = fields[field_name]['value']
                if actual is not None and str(actual).strip() == expected_value:
                    print(f"PASS: {field_name} = '{actual}'")
                    page2_passed += 1
                else:
                    print(f"FAIL: {field_name} — expected '{expected_value}', found '{actual}'")
            else:
                print(f"FAIL: {field_name} — field not found in PDF")

        if page2_passed == 3:
            print(f"PASS: Component 2 — All Page 2 fields correct (0.3 pts)")
            total_score += 0.3
        elif page2_passed > 0:
            partial = round(0.1 * page2_passed, 2)
            print(f"PARTIAL: Component 2 — {page2_passed}/3 Page 2 fields correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Page 2 fields correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 3 checkboxes (0.3 points)
    # irb_approved, conflict_none, terms_accepted must be checked
    try:
        checkboxes_passed = 0
        for field_name in EXPECTED_CHECKBOXES_PAGE3:
            if field_name in fields:
                actual = fields[field_name]['value']
                # Checked checkboxes have value "Yes", unchecked have "Off"
                if actual is not None and str(actual).strip() not in ('', 'Off'):
                    print(f"PASS: {field_name} is checked (value='{actual}')")
                    checkboxes_passed += 1
                else:
                    print(f"FAIL: {field_name} — checkbox not checked (value='{actual}')")
            else:
                print(f"FAIL: {field_name} — field not found in PDF")

        if checkboxes_passed == 3:
            print(f"PASS: Component 3 — All checkboxes checked (0.3 pts)")
            total_score += 0.3
        elif checkboxes_passed > 0:
            partial = round(0.1 * checkboxes_passed, 2)
            print(f"PARTIAL: Component 3 — {checkboxes_passed}/3 checkboxes checked ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No checkboxes checked")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Non-mentioned fields remain empty/unchecked (0.1 points)
    # Fields on pages 4 and 5 should not be filled
    try:
        empty_count = 0
        for field_name in SHOULD_BE_EMPTY_FIELDS:
            if field_name in fields:
                actual = fields[field_name]['value']
                if actual is None or str(actual).strip() in ('', 'Off'):
                    empty_count += 1
                else:
                    print(f"WARN: {field_name} should be empty but has value '{actual}'")

        if empty_count == len(SHOULD_BE_EMPTY_FIELDS):
            print(f"PASS: Component 4 — All non-mentioned fields remain empty (0.1 pts)")
            total_score += 0.1
        else:
            filled = len(SHOULD_BE_EMPTY_FIELDS) - empty_count
            print(f"FAIL: Component 4 — {filled} non-mentioned fields were unexpectedly filled")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
