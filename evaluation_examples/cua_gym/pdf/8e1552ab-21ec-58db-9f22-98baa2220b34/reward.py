"""
Reward Script: Check agree_to_terms checkbox and select express_shipping in purchase_order.pdf
Task ID: pdf_fm_013
Domain: pdf
Scoring:
  Component 1 (0.4): agree_to_terms checkbox is checked (Yes)
  Component 2 (0.4): express_shipping checkbox is checked (Yes)
  Component 3 (0.2): Other controls remain unchecked (standard_shipping, overnight_shipping, subscribe_newsletter = Off)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_013'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'purchase_order.pdf')


def get_form_fields(pdf_path):
    """Extract all form fields from the PDF."""
    doc = pymupdf.open(pdf_path)
    fields = {}
    for page in doc:
        for widget in page.widgets():
            fields[widget.field_name] = {
                "type": widget.field_type_string,
                "value": widget.field_value,
            }
    doc.close()
    return fields


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        fields = get_form_fields(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF or extract fields: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(fields)} form fields: {list(fields.keys())}")

    # Component 1: agree_to_terms checkbox is checked (0.4 points)
    try:
        if 'agree_to_terms' in fields:
            val = fields['agree_to_terms']['value']
            if val not in ('Off', '', None):
                print(f"PASS: Component 1 — agree_to_terms is checked (value: {val!r}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — agree_to_terms is unchecked (value: {val!r})")
        else:
            print("FAIL: Component 1 — agree_to_terms field not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: express_shipping is checked (0.4 points)
    try:
        if 'express_shipping' in fields:
            val = fields['express_shipping']['value']
            if val not in ('Off', '', None):
                print(f"PASS: Component 2 — express_shipping is checked (value: {val!r}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — express_shipping is unchecked (value: {val!r})")
        else:
            print("FAIL: Component 2 — express_shipping field not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Task changes applied AND other controls remain unchecked (0.2 points)
    # This is a compound check: both target fields must be checked, AND
    # standard_shipping, overnight_shipping, subscribe_newsletter must remain Off.
    # Anchored to task change: requires agree_to_terms AND express_shipping to be checked.
    try:
        agree_checked = ('agree_to_terms' in fields and
                         fields['agree_to_terms']['value'] not in ('Off', '', None))
        express_checked = ('express_shipping' in fields and
                           fields['express_shipping']['value'] not in ('Off', '', None))

        others_correct = 0
        other_fields = ['standard_shipping', 'overnight_shipping', 'subscribe_newsletter']
        for fname in other_fields:
            if fname in fields:
                val = fields[fname]['value']
                if val in ('Off', '', None):
                    others_correct += 1
                    print(f"  OK: {fname} is unchecked (value: {val!r})")
                else:
                    print(f"  ISSUE: {fname} should be unchecked but has value: {val!r}")
            else:
                print(f"  WARN: {fname} field not found")

        if agree_checked and express_checked and others_correct == len(other_fields):
            print(f"PASS: Component 3 — Both targets checked and other controls remain unchecked (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Requires both targets checked ({agree_checked}, {express_checked}) "
                  f"and {others_correct}/{len(other_fields)} others unchecked")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
