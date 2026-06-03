"""
reward.py — pdf_basic_045

Verifies that ~/Desktop/consent_form.pdf has been filled in correctly:
  1. File exists at ~/Desktop/consent_form.pdf                        (0.10)
  2. agree_terms checkbox is checked                                   (0.20)
  3. consent_data checkbox is checked                                  (0.20)
  4. date_field == "03/15/2025"                                        (0.25)
  5. full_name_field == "Emily Rodriguez"                              (0.25)

Returns a float score in [0.0, 1.0] and prints "REWARD: <score>".

Initial state (all fields empty/unchecked) → 0.0
Golden state (all fields correctly filled) → 1.0
"""

import sys
import os

PDF_PATH = "/home/user/Desktop/consent_form.pdf"

def compute_reward(pdf_path: str) -> float:
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("ERROR: pymupdf / fitz not available", file=sys.stderr)
            return 0.0

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}", file=sys.stderr)
        return 0.0

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"Cannot open PDF: {e}", file=sys.stderr)
        return 0.0

    # Collect widgets from all pages
    fields = {}
    for page in doc:
        for widget in page.widgets():
            fields[widget.field_name] = widget

    doc.close()

    score = 0.0

    # --- Check 1: file exists and is a valid PDF with form fields (0.10) ---
    if len(fields) >= 4:
        score += 0.10

    # --- Check 2: agree_terms checkbox is checked (0.20) ---
    w = fields.get("agree_terms")
    if w is not None:
        val = w.field_value
        if val not in ("Off", "", None, False):
            score += 0.20

    # --- Check 3: consent_data checkbox is checked (0.20) ---
    w = fields.get("consent_data")
    if w is not None:
        val = w.field_value
        if val not in ("Off", "", None, False):
            score += 0.20

    # --- Check 4: date_field == "03/15/2025" (0.25) ---
    w = fields.get("date_field")
    if w is not None:
        val = str(w.field_value).strip()
        if val == "03/15/2025":
            score += 0.25

    # --- Check 5: full_name_field == "Emily Rodriguez" (0.25) ---
    w = fields.get("full_name_field")
    if w is not None:
        val = str(w.field_value).strip()
        if val == "Emily Rodriguez":
            score += 0.25

    return round(min(score, 1.0), 2)


if __name__ == "__main__":
    reward = compute_reward(PDF_PATH)
    print(f"REWARD: {reward}")
