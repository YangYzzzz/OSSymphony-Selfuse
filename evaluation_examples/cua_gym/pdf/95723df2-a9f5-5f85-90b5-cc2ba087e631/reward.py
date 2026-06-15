"""
Reward Script: Verify PDF form field completion in feedback_survey.pdf
Task ID: pdf_fm_043
Domain: pdf
Scoring:
  Component 1: satisfaction dropdown = 'Very Satisfied' (0.35 pts)
  Component 2: recommend checkbox is checked (0.30 pts)
  Component 3: comments text = 'Great product quality and customer service' (0.35 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_043'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'feedback_survey.pdf')


def get_form_fields(pdf_path):
    """Extract all form fields from the PDF."""
    doc = pymupdf.open(pdf_path)
    fields = {}
    for page in doc:
        for widget in page.widgets():
            fields[widget.field_name] = {
                "type": widget.field_type_string,
                "value": widget.field_value,
                "choices": widget.choice_values,
            }
    doc.close()
    return fields


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF with form fields
    try:
        fields = get_form_fields(file_path)
        if not fields:
            print("CRITICAL: No form fields found in PDF")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load or parse PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found fields: {list(fields.keys())}")

    # Component 1: satisfaction dropdown set to 'Very Satisfied' (0.35 points)
    try:
        if 'satisfaction' in fields:
            actual = fields['satisfaction']['value']
            if actual == 'Very Satisfied':
                print(f"PASS: Component 1 -- satisfaction = 'Very Satisfied' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 -- expected satisfaction='Very Satisfied', found '{actual}'")
        else:
            print("FAIL: Component 1 -- 'satisfaction' field not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: recommend checkbox is checked (0.30 points)
    try:
        if 'recommend' in fields:
            actual = fields['recommend']['value']
            # Checkbox: checked values are anything other than 'Off', '', None
            is_checked = actual not in ('Off', '', None, False)
            if is_checked:
                print(f"PASS: Component 2 -- recommend checkbox is checked (value='{actual}') (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 -- recommend checkbox is unchecked (value='{actual}')")
        else:
            print("FAIL: Component 2 -- 'recommend' field not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: comments text field = 'Great product quality and customer service' (0.35 points)
    try:
        if 'comments' in fields:
            actual = fields['comments']['value']
            expected = 'Great product quality and customer service'
            if actual and actual.strip() == expected:
                print(f"PASS: Component 3 -- comments matches expected text exactly (0.35 pts)")
                total_score += 0.35
            elif actual and expected.lower() in actual.strip().lower():
                # Partial credit: text contains the expected string (case-insensitive)
                print(f"PARTIAL: Component 3 -- comments contains expected text (0.20 pts). Actual: '{actual}'")
                total_score += 0.20
            elif actual and len(actual.strip()) > 0:
                # Minimal credit: something was typed but doesn't match
                print(f"FAIL: Component 3 -- comments has text but doesn't match. Expected: '{expected}', Found: '{actual}'")
            else:
                print(f"FAIL: Component 3 -- comments field is empty")
        else:
            print("FAIL: Component 3 -- 'comments' field not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
