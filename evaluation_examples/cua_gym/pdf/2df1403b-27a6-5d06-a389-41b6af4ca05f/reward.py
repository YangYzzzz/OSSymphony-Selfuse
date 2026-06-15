"""
Reward Script: Verify fillable PDF claim form has been correctly filled.
Task ID: pdf_basic_128
Domain: pdf

Scoring rubric (total = 1.0):
  Component 1 (0.25): 'Claim Number' field == 'CLM-2025-78432'
  Component 2 (0.25): 'Date of Incident' field == '02/14/2025'
  Component 3 (0.30): 'Description' field == 'Water damage to ground floor office area'
  Component 4 (0.20): 'Claim Type' field == 'Property Damage'

All checks fail on initial_env (all fields are empty/default).
All checks pass on golden_env (all fields have the required values).
"""

import os
import sys

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
FILE_PATH = f'{DESKTOP}/claim_form.pdf'

# Optional: persist any unsaved GUI edits before scoring
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.2)
        print("PERSIST: ctrl+s sent for Evince PDF form")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify the claim form has been filled with the required values.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all form fields into a dict for easy lookup
    fields = {}
    try:
        for page in doc:
            for widget in page.widgets():
                fields[widget.field_name] = widget.field_value
    except Exception as e:
        print(f"ERROR: Could not read form fields: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    doc.close()
    print(f"Form fields found: {list(fields.keys())}")

    # -----------------------------------------------------------------------
    # Component 1: Claim Number == 'CLM-2025-78432'  (0.25 points)
    # -----------------------------------------------------------------------
    try:
        actual = fields.get("Claim Number", "")
        expected = "CLM-2025-78432"
        if str(actual).strip() == expected:
            print(f"PASS: Component 1 — Claim Number == '{expected}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Claim Number: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Date of Incident == '02/14/2025'  (0.25 points)
    # -----------------------------------------------------------------------
    try:
        actual = fields.get("Date of Incident", "")
        expected = "02/14/2025"
        if str(actual).strip() == expected:
            print(f"PASS: Component 2 — Date of Incident == '{expected}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Date of Incident: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Description == 'Water damage to ground floor office area'  (0.30 points)
    # -----------------------------------------------------------------------
    try:
        actual = fields.get("Description", "")
        expected = "Water damage to ground floor office area"
        if str(actual).strip() == expected:
            print(f"PASS: Component 3 — Description matches (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Description: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Claim Type == 'Property Damage'  (0.20 points)
    # -----------------------------------------------------------------------
    try:
        actual = fields.get("Claim Type", "")
        expected = "Property Damage"
        if str(actual).strip() == expected:
            print(f"PASS: Component 4 — Claim Type == '{expected}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Claim Type: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI edits first
persist_app_state()

# Evaluate
verify_task(FILE_PATH)
