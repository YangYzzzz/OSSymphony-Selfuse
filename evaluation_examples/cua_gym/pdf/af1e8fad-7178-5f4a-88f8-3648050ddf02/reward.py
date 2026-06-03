"""
Reward Script: Insurance claim form filling verification
Task ID: pdf_fm_031
Domain: pdf
Scoring:
  - policy_number correct (0.15)
  - claimant_name correct (0.15)
  - date_of_loss correct (0.10)
  - loss_type dropdown correct (0.15)
  - estimated_amount correct (0.10)
  - description correct (0.15)
  - police_report_filed checked (0.10)
  - photos_attached unchecked (0.10)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_031'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'claim_form_filled.pdf')


def get_form_fields(pdf_path):
    """Extract all form fields from all pages of the PDF."""
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

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: file must be a valid PDF with form fields
    try:
        fields = get_form_fields(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF or extract fields: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not fields:
        print("CRITICAL: No form fields found in PDF")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(fields)} form fields: {list(fields.keys())}")

    # Component 1: policy_number == 'INS-2025-78432' (0.15 points)
    try:
        val = fields.get("policy_number", {}).get("value", "")
        if str(val).strip() == "INS-2025-78432":
            print(f"PASS: Component 1 - policy_number = '{val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - policy_number expected 'INS-2025-78432', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: claimant_name == 'Marcus Williams' (0.15 points)
    try:
        val = fields.get("claimant_name", {}).get("value", "")
        if str(val).strip() == "Marcus Williams":
            print(f"PASS: Component 2 - claimant_name = '{val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - claimant_name expected 'Marcus Williams', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: date_of_loss == '07/15/2025' (0.10 points)
    try:
        val = fields.get("date_of_loss", {}).get("value", "")
        if str(val).strip() == "07/15/2025":
            print(f"PASS: Component 3 - date_of_loss = '{val}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - date_of_loss expected '07/15/2025', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: loss_type == 'Property Damage' (0.15 points)
    try:
        val = fields.get("loss_type", {}).get("value", "")
        if str(val).strip() == "Property Damage":
            print(f"PASS: Component 4 - loss_type = '{val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - loss_type expected 'Property Damage', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: estimated_amount == '$12,500.00' (0.10 points)
    try:
        val = fields.get("estimated_amount", {}).get("value", "")
        if str(val).strip() == "$12,500.00":
            print(f"PASS: Component 5 - estimated_amount = '{val}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - estimated_amount expected '$12,500.00', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: description == 'Water damage from burst pipe in basement' (0.15 points)
    try:
        val = fields.get("description", {}).get("value", "")
        if str(val).strip() == "Water damage from burst pipe in basement":
            print(f"PASS: Component 6 - description = '{val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - description expected 'Water damage from burst pipe in basement', found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: police_report_filed checkbox is checked (0.10 points)
    # Checked = value not in ("Off", "", None); typically "Yes"
    try:
        val = fields.get("police_report_filed", {}).get("value", "")
        is_checked = val not in ("Off", "", None, False)
        if is_checked:
            print(f"PASS: Component 7 - police_report_filed is checked (value='{val}') (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 - police_report_filed expected checked, found '{val}'")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    # Component 8: photos_attached checkbox is unchecked (0.10 points)
    # This verifies the agent did NOT check photos_attached (task only asks to check police_report_filed)
    # Initial state: unchecked. Golden state: still unchecked. This component only contributes
    # when combined with at least one other task-change passing (to avoid scoring on initial).
    try:
        val = fields.get("photos_attached", {}).get("value", "")
        is_unchecked = val in ("Off", "", None, False)
        # Only award points if police_report_filed is checked (a task-introduced change),
        # ensuring this component doesn't score on the initial state where both are unchecked.
        police_val = fields.get("police_report_filed", {}).get("value", "")
        police_checked = police_val not in ("Off", "", None, False)
        if is_unchecked and police_checked:
            print(f"PASS: Component 8 - photos_attached remains unchecked AND police_report_filed is checked (0.10 pts)")
            total_score += 0.10
        elif not is_unchecked:
            print(f"FAIL: Component 8 - photos_attached should be unchecked, found '{val}'")
        else:
            print(f"FAIL: Component 8 - photos_attached unchecked but police_report_filed not checked (precondition not met)")
    except Exception as e:
        print(f"ERROR: Component 8 - {e}")

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
