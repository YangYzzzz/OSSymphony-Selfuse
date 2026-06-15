"""
Reward Script: Create fillable PDF form with interactive fields
Task ID: pdf_pw_018
Domain: pdf
Scoring:
  Component 1 (0.30) - All 6 form fields exist with correct names
  Component 2 (0.25) - Correct field types (text, combobox, checkbox)
  Component 3 (0.20) - Priority dropdown has 4 correct options
  Component 4 (0.15) - Description field is multi-line (~400x100 pts)
  Component 5 (0.10) - Approved field is a checkbox
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_018'
FILE_PATH = os.path.join(WORKDIR, 'forms', 'project_request.pdf')

# Expected field definitions
EXPECTED_FIELDS = {
    'project_name': 'Text',
    'requester': 'Text',
    'budget_estimate': 'Text',
    'priority': 'ComboBox',
    'description': 'Text',
    'approved': 'CheckBox',
}

EXPECTED_PRIORITY_OPTIONS = ['Low', 'Medium', 'High', 'Critical']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) == 0:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]

    # Collect all widgets
    widgets = {}
    try:
        for w in page.widgets():
            widgets[w.field_name] = {
                'type': w.field_type_string,
                'rect': tuple(w.rect),
                'flags': w.field_flags,
                'choices': w.choice_values,
                'value': w.field_value,
            }
    except Exception as e:
        print(f"ERROR: Failed to read widgets: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(widgets)} widget(s): {list(widgets.keys())}")

    # Component 1: All 6 form fields exist with correct names (0.30 points)
    # This checks that the task-introduced interactive fields are present.
    # Initial PDF has 0 widgets, so this will fail on initial_env.
    try:
        found_names = set(widgets.keys())
        expected_names = set(EXPECTED_FIELDS.keys())
        matching = found_names & expected_names
        missing = expected_names - found_names

        if len(matching) == 6:
            print(f"PASS: Component 1 - All 6 form fields present: {sorted(matching)} (0.30 pts)")
            total_score += 0.30
        elif len(matching) >= 4:
            partial = round(0.30 * len(matching) / 6, 2)
            print(f"PARTIAL: Component 1 - {len(matching)}/6 fields present, missing: {sorted(missing)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Only {len(matching)}/6 fields present. Missing: {sorted(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Correct field types (0.25 points)
    # Verifies each field has the right type (text, combobox, checkbox)
    try:
        type_matches = 0
        type_total = 0
        for name, expected_type in EXPECTED_FIELDS.items():
            if name in widgets:
                type_total += 1
                actual_type = widgets[name]['type']
                if actual_type == expected_type:
                    type_matches += 1
                else:
                    print(f"  MISMATCH: {name} type={actual_type}, expected={expected_type}")

        if type_total > 0 and type_matches == type_total:
            print(f"PASS: Component 2 - All {type_matches} field types correct (0.25 pts)")
            total_score += 0.25
        elif type_matches > 0:
            partial = round(0.25 * type_matches / max(type_total, 1), 2)
            print(f"PARTIAL: Component 2 - {type_matches}/{type_total} field types correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No field types matched (checked {type_total} fields)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Priority dropdown has correct 4 options (0.20 points)
    try:
        if 'priority' in widgets:
            choices = widgets['priority'].get('choices') or []
            if choices == EXPECTED_PRIORITY_OPTIONS:
                print(f"PASS: Component 3 - Priority dropdown has correct options: {choices} (0.20 pts)")
                total_score += 0.20
            elif set(choices) == set(EXPECTED_PRIORITY_OPTIONS):
                # Correct options but different order
                print(f"PARTIAL: Component 3 - Priority options correct but wrong order: {choices} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 - Priority options: {choices}, expected: {EXPECTED_PRIORITY_OPTIONS}")
        else:
            print("FAIL: Component 3 - 'priority' field not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Description field is multi-line with appropriate dimensions (0.15 points)
    try:
        if 'description' in widgets:
            desc = widgets['description']
            flags = desc['flags']
            # PDF_TX_FIELD_IS_MULTILINE = 4096 (bit 12)
            is_multiline = bool(flags & 4096)
            rect = desc['rect']
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            multiline_ok = is_multiline
            # Allow some tolerance on dimensions (within 20% of 400x100)
            dim_ok = (320 <= width <= 480) and (80 <= height <= 120)

            if multiline_ok and dim_ok:
                print(f"PASS: Component 4 - Description is multi-line, size={width:.0f}x{height:.0f} pts (0.15 pts)")
                total_score += 0.15
            elif multiline_ok:
                print(f"PARTIAL: Component 4 - Description is multi-line but size={width:.0f}x{height:.0f} (expected ~400x100) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 - Description multiline={is_multiline}, size={width:.0f}x{height:.0f}")
        else:
            print("FAIL: Component 4 - 'description' field not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Approved field is a checkbox (0.10 points)
    try:
        if 'approved' in widgets:
            if widgets['approved']['type'] == 'CheckBox':
                print(f"PASS: Component 5 - 'approved' is a CheckBox (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - 'approved' type={widgets['approved']['type']}, expected CheckBox")
        else:
            print("FAIL: Component 5 - 'approved' field not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
