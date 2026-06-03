"""
Reward Script: Fillable PDF form with 5 interactive fields
Task ID: pdf_pw_003
Domain: pdf
Scoring:
  Component 1 (0.15): Total form field count == 5
  Component 2 (0.25): Three text fields exist with correct names
  Component 3 (0.20): Text field rectangles at specified coordinates
  Component 4 (0.25): Dropdown 'department' as ComboBox with correct options
  Component 5 (0.15): Checkbox 'nda_signed' exists at correct position
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_003'
FILE_PATH = os.path.join(WORKDIR, 'forms', 'employee_onboarding.pdf')

# Expected field specifications from task_config
EXPECTED_TEXT_FIELDS = {
    'full_name':    pymupdf.Rect(72, 120, 350, 140),
    'employee_id':  pymupdf.Rect(72, 170, 200, 190),
    'start_date':   pymupdf.Rect(72, 220, 200, 240),
}

EXPECTED_DROPDOWN_NAME = 'department'
EXPECTED_DROPDOWN_RECT = pymupdf.Rect(72, 270, 250, 290)
EXPECTED_DROPDOWN_OPTIONS = ['Engineering', 'Marketing', 'Finance', 'HR', 'Operations']

EXPECTED_CHECKBOX_NAME = 'nda_signed'
EXPECTED_CHECKBOX_RECT = pymupdf.Rect(72, 320, 90, 338)

# Tolerance for coordinate comparison (points)
COORD_TOLERANCE = 2.0


def rects_close(r1, r2, tol=COORD_TOLERANCE):
    """Check if two rectangles are approximately equal within tolerance."""
    return (abs(r1.x0 - r2.x0) <= tol and
            abs(r1.y0 - r2.y0) <= tol and
            abs(r1.x1 - r2.x1) <= tol and
            abs(r1.y1 - r2.y1) <= tol)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = pymupdf.open(file_path)
        page = doc[0]
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all widgets into a dict by name
    widgets = {}
    for w in page.widgets():
        widgets[w.field_name] = {
            'type': w.field_type_string,
            'rect': w.rect,
            'choices': w.choice_values,
        }

    widget_count = len(widgets)
    print(f"INFO: Found {widget_count} form field(s): {list(widgets.keys())}")

    # Component 1: Total form field count == 5 (0.15 points)
    try:
        if widget_count == 5:
            print(f"PASS: Component 1 — form field count is 5 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected 5 form fields, found {widget_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Three text fields exist with correct names (0.25 points)
    # Each text field earns ~0.083 points
    try:
        text_field_score = 0.0
        for fname in EXPECTED_TEXT_FIELDS:
            if fname in widgets and widgets[fname]['type'] == 'Text':
                text_field_score += 1
                print(f"  PASS: Text field '{fname}' found")
            else:
                print(f"  FAIL: Text field '{fname}' not found or wrong type "
                      f"(found: {widgets.get(fname, {}).get('type', 'MISSING')})")
        if text_field_score == 3:
            print(f"PASS: Component 2 — all 3 text fields present (0.25 pts)")
            total_score += 0.25
        elif text_field_score > 0:
            partial = round(0.25 * (text_field_score / 3), 2)
            print(f"PARTIAL: Component 2 — {int(text_field_score)}/3 text fields ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no text fields found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text field rectangles at specified coordinates (0.20 points)
    try:
        rect_matches = 0
        for fname, expected_rect in EXPECTED_TEXT_FIELDS.items():
            if fname in widgets:
                actual_rect = widgets[fname]['rect']
                if rects_close(actual_rect, expected_rect):
                    rect_matches += 1
                    print(f"  PASS: '{fname}' rect matches ({tuple(actual_rect)})")
                else:
                    print(f"  FAIL: '{fname}' rect mismatch — expected {tuple(expected_rect)}, "
                          f"got {tuple(actual_rect)}")
            else:
                print(f"  FAIL: '{fname}' not found — cannot check rect")
        if rect_matches == 3:
            print(f"PASS: Component 3 — all text field rects correct (0.20 pts)")
            total_score += 0.20
        elif rect_matches > 0:
            partial = round(0.20 * (rect_matches / 3), 2)
            print(f"PARTIAL: Component 3 — {rect_matches}/3 rects correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no text field rects correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Dropdown 'department' as ComboBox with correct options (0.25 points)
    try:
        if EXPECTED_DROPDOWN_NAME in widgets:
            w = widgets[EXPECTED_DROPDOWN_NAME]
            sub_score = 0.0

            # 4a: Field type is ComboBox (0.08)
            if w['type'] == 'ComboBox':
                sub_score += 0.08
                print(f"  PASS: 'department' is ComboBox type")
            else:
                print(f"  FAIL: 'department' type is {w['type']}, expected ComboBox")

            # 4b: Has the correct 5 options (0.10)
            actual_choices = w.get('choices') or []
            if actual_choices == EXPECTED_DROPDOWN_OPTIONS:
                sub_score += 0.10
                print(f"  PASS: 'department' options match exactly")
            else:
                print(f"  FAIL: 'department' options mismatch — expected {EXPECTED_DROPDOWN_OPTIONS}, "
                      f"got {actual_choices}")

            # 4c: Rect is at specified position (0.07)
            if rects_close(w['rect'], EXPECTED_DROPDOWN_RECT):
                sub_score += 0.07
                print(f"  PASS: 'department' rect matches ({tuple(w['rect'])})")
            else:
                print(f"  FAIL: 'department' rect mismatch — expected {tuple(EXPECTED_DROPDOWN_RECT)}, "
                      f"got {tuple(w['rect'])}")

            if sub_score > 0:
                total_score += sub_score
                print(f"{'PASS' if sub_score >= 0.25 else 'PARTIAL'}: Component 4 — "
                      f"department dropdown ({sub_score} pts)")
        else:
            print(f"FAIL: Component 4 — 'department' field not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Checkbox 'nda_signed' at correct position (0.15 points)
    try:
        if EXPECTED_CHECKBOX_NAME in widgets:
            w = widgets[EXPECTED_CHECKBOX_NAME]
            sub_score = 0.0

            # 5a: Field type is CheckBox (0.08)
            if w['type'] == 'CheckBox':
                sub_score += 0.08
                print(f"  PASS: 'nda_signed' is CheckBox type")
            else:
                print(f"  FAIL: 'nda_signed' type is {w['type']}, expected CheckBox")

            # 5b: Rect is at specified position (0.07)
            if rects_close(w['rect'], EXPECTED_CHECKBOX_RECT):
                sub_score += 0.07
                print(f"  PASS: 'nda_signed' rect matches ({tuple(w['rect'])})")
            else:
                print(f"  FAIL: 'nda_signed' rect mismatch — expected {tuple(EXPECTED_CHECKBOX_RECT)}, "
                      f"got {tuple(w['rect'])}")

            if sub_score > 0:
                total_score += sub_score
                print(f"{'PASS' if sub_score >= 0.15 else 'PARTIAL'}: Component 5 — "
                      f"nda_signed checkbox ({sub_score} pts)")
        else:
            print(f"FAIL: Component 5 — 'nda_signed' field not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

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
