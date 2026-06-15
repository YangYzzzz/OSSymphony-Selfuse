"""
Reward Script: Fill out patient intake form with specified values
Task ID: pdf_fm_046
Domain: pdf
Scoring:
  Component 1: patient_name = 'Lisa Park'                    (0.20)
  Component 2: dob = '05/14/1985'                            (0.15)
  Component 3: allergies = 'Penicillin, Sulfa drugs'         (0.15)
  Component 4: current_medications = 'Lisinopril 10mg, Metformin 500mg' (0.20)
  Component 5: 'female' checkbox checked                     (0.15)
  Component 6: 'insurance_yes' checkbox checked              (0.15)
  Total: 1.0
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_046'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'forms', 'patient_intake.pdf')


def get_field_map(pdf_path: str) -> dict:
    """Read all form fields across all pages into a dict keyed by field_name."""
    doc = pymupdf.open(pdf_path)
    fields = {}
    for page in doc:
        for w in page.widgets():
            fields[w.field_name] = {
                "type": w.field_type_string,
                "value": w.field_value,
            }
    doc.close()
    return fields


def verify_task(file_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF with form fields
    try:
        fields = get_field_map(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load or parse PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not fields:
        print("CRITICAL: No form fields found in PDF")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: patient_name = 'Lisa Park' (0.20 points)
    try:
        val = fields.get("patient_name", {}).get("value", "")
        if val and val.strip() == "Lisa Park":
            print(f"PASS: Component 1 — patient_name is 'Lisa Park' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected patient_name='Lisa Park', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: dob = '05/14/1985' (0.15 points)
    try:
        val = fields.get("dob", {}).get("value", "")
        if val and val.strip() == "05/14/1985":
            print(f"PASS: Component 2 — dob is '05/14/1985' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected dob='05/14/1985', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: allergies = 'Penicillin, Sulfa drugs' (0.15 points)
    try:
        val = fields.get("allergies", {}).get("value", "")
        if val and val.strip() == "Penicillin, Sulfa drugs":
            print(f"PASS: Component 3 — allergies is 'Penicillin, Sulfa drugs' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — expected allergies='Penicillin, Sulfa drugs', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: current_medications = 'Lisinopril 10mg, Metformin 500mg' (0.20 points)
    try:
        val = fields.get("current_medications", {}).get("value", "")
        if val and val.strip() == "Lisinopril 10mg, Metformin 500mg":
            print(f"PASS: Component 4 — current_medications is 'Lisinopril 10mg, Metformin 500mg' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — expected current_medications='Lisinopril 10mg, Metformin 500mg', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 'female' checkbox is checked (0.15 points)
    try:
        val = fields.get("female", {}).get("value", "")
        if val and val.strip() != "Off":
            print(f"PASS: Component 5 — 'female' checkbox is checked (value={val!r}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — expected 'female' checkbox checked, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 'insurance_yes' checkbox is checked (0.15 points)
    try:
        val = fields.get("insurance_yes", {}).get("value", "")
        if val and val.strip() != "Off":
            print(f"PASS: Component 6 — 'insurance_yes' checkbox is checked (value={val!r}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — expected 'insurance_yes' checkbox checked, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

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
