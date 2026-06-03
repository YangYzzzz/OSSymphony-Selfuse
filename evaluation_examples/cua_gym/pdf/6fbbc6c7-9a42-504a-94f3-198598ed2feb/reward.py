"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please check the boxes for 'Option A', 'Option C', and 'Option E' in the checklist form 'preferences.pdf' on Desktop and save as 'preferences_selected.pdf'.
Generated: 2025-11-29 09:59:14
Status: success
Model: o3
Total Steps: 6
"""

"""
Reward script for verifying the task:
"Please check the boxes for 'Option A', 'Option C', and 'Option E' in the checklist 
form 'preferences.pdf' on Desktop and save as 'preferences_selected.pdf'."

The script checks the completed PDF (preferences_selected.pdf) and awards a
progressive score based on whether:
  • Option A, C, E are checked ("/Yes")              – 0.30 pts each
  • Option B, D remain unchecked ("/Off" or blank)    – 0.05 pts each
Total possible = 1.0

No points are given for natural conditions such as the mere existence of the
file or the ability to open it.
"""
from pathlib import Path
from typing import Dict

from PyPDF2 import PdfReader

OUTPUT_PDF = Path("/home/user/Desktop/preferences_selected.pdf")

# Per-field weights (must sum to 1.0)
WEIGHTS: Dict[str, float] = {
    "optionA": 0.30,
    "optionC": 0.30,
    "optionE": 0.30,
    "optionB_off": 0.05,
    "optionD_off": 0.05,
}


def verify_preferences_selected(pdf_path: Path = OUTPUT_PDF) -> float:
    """Verify that the correct check-boxes are selected in the output PDF.

    Returns a float between 0.0 and 1.0.
    """
    max_score = 1.0
    score = 0.0

    # 1) Check that the file exists -------------------------------------------------
    if not pdf_path.exists():
        print(f"✗ Output file not found: {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Load PDF safely -----------------------------------------------------------
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"✗ Unable to open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 3) Extract form fields -------------------------------------------------------
    fields = reader.get_fields() or {}
    print(f"Found form fields: {list(fields.keys())}")

    # Expected state definitions ---------------------------------------------------
    expected_yes = {"optionA", "optionC", "optionE"}
    expected_off = {"optionB", "optionD"}

    # 4) Verify that A/C/E are checked (Yes) --------------------------------------
    for field_name in expected_yes:
        field = fields.get(field_name)
        if field is None:
            print(f"✗ Missing field '{field_name}' in PDF")
            continue  # No points awarded
        current_val = field.get("/V")
        if str(current_val) == "/Yes":
            print(f"✓ {field_name} correctly checked (/Yes)")
            score += WEIGHTS[field_name]
        else:
            print(f"✗ {field_name} expected '/Yes' but got '{current_val}'")

    # 5) Verify that B/D are NOT checked (Off) ------------------------------------
    for field_name in expected_off:
        field = fields.get(field_name)
        weight_key = f"{field_name}_off"
        if field is None:
            print(f"✗ Missing field '{field_name}' in PDF")
            continue  # No points awarded
        current_val = field.get("/V", "")
        if str(current_val) in {"/Off", ""}:  # unselected states
            print(f"✓ {field_name} correctly unchecked (/Off)")
            score += WEIGHTS[weight_key]
        else:
            print(f"✗ {field_name} expected '/Off' but got '{current_val}'")

    # 6) Clamp and output ----------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Partial score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_preferences_selected()

