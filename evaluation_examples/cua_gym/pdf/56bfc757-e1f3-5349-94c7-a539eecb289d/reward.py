"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to select radio button 'Option 2' for question 1 and 'Option 3' for question 5 in 'exam_answer_sheet.pdf' on Desktop. Save as 'exam_answers.pdf'.
Generated: 2025-11-29 10:02:24
Status: success
Model: o3
Total Steps: 12
"""

from pathlib import Path
from typing import Dict
from PyPDF2 import PdfReader


def _normalize_pdf_value(val) -> str:
    """Return a clean string representation for a PDF form value."""
    if val is None:
        return ""
    s = str(val)
    # NameObjects often start with '/' (e.g. '/Option 2') – strip it off
    if s.startswith('/'):
        s = s[1:]
    return s.strip()


def verify_exam_answers(pdf_path: str = "/home/user/Desktop/exam_answers.pdf") -> float:
    """Verify that the required radio-button answers are selected.

    Returns
    -------
    float
        Progressive score between 0.0 and 1.0. Exactly 1.0 means both
        required answers are present and correct.
    """

    # Expected radio-button selections (field name ➜ expected value)
    expected: Dict[str, str] = {
        "q1": "Option 2",   # Question 1 must have Option 2 selected
        "q5": "Option 3",   # Question 5 must have Option 3 selected
    }

    max_score = 1.0
    score_per_field = max_score / len(expected)
    total_score = 0.0

    pdf_file = Path(pdf_path)

    # ---------- 1) File existence ( NO POINTS for mere existence ) ----------
    if not pdf_file.exists():
        print(f"✗ Expected PDF not found: {pdf_file}")
        print("REWARD: 0.0")
        return 0.0  # Cannot verify anything further

    # ---------- 2) Load PDF safely -----------------------------------------
    try:
        reader = PdfReader(str(pdf_file))
        form_fields = reader.get_fields() or {}
        print(
            f"Loaded '{pdf_file.name}' – pages: {len(reader.pages)}, form fields: {len(form_fields)}"
        )
    except Exception as e:
        print(f"✗ Failed to load PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- 3) Verify each expected field ------------------------------
    for field_name, expected_val in expected.items():
        field_info = form_fields.get(field_name)
        if field_info is None:
            print(f"✗ Missing form field '{field_name}' – no points awarded")
            continue  # Do not crash; allow partial credit for other fields

        actual_val = _normalize_pdf_value(field_info.get("/V"))
        if actual_val == expected_val:
            total_score += score_per_field
            print(
                f"✓ {field_name} correctly set to '{expected_val}' (+{score_per_field:.2f})"
            )
        else:
            print(
                f"✗ {field_name} value incorrect – expected '{expected_val}', found '{actual_val}'"
            )

    # ---------- 4) Final score --------------------------------------------
    final_score = round(min(total_score, max_score), 2)
    print(f"REWARD: {final_score}")
    return final_score


# ---------------------------------------------------------------------------
# Execute verification when the script is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_exam_answers()

