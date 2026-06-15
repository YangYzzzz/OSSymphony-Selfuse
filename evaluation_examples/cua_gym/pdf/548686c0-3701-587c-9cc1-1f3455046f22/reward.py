"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to fill in the date field with '2024-12-15', signature field with 'John Doe', and check the 'I agree' checkbox in 'consent_form.pdf' in /home/user/Documents/Legal. Save as 'consent_signed.pdf'.
Generated: 2025-11-29 10:01:11
Status: success
Model: o3
Total Steps: 7
"""

from pathlib import Path
from PyPDF2 import PdfReader

def verify_pdf_task():
    """
    Reward script for task:
    Fill in the date field with '2024-12-15', signature field with 'John Doe', and
    check the 'I agree' checkbox in `consent_form.pdf` located at
    /home/user/Documents/Legal.  The completed file must be saved as
    `consent_signed.pdf` in the same directory.

    The script loads the resulting PDF and verifies, field-by-field, that the
    required values are present.  Progressive scoring is used:
        • Date field correct      -> 0.30 pts
        • Signature field correct -> 0.30 pts
        • Checkbox ticked         -> 0.40 pts
    A perfect file therefore earns 1.0.
    """

    target_pdf = Path("/home/user/Documents/Legal/consent_signed.pdf")

    # --- early existence check (no points just prerequisite) -----------------
    if not target_pdf.exists():
        print(f"✗ Required PDF not found: {target_pdf}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found target PDF: {target_pdf}")

    # --- try loading & extracting AcroForm fields ---------------------------
    try:
        reader = PdfReader(str(target_pdf))
        fields = reader.get_fields() or {}
        print(f"Detected form fields: {list(fields.keys())}")
    except Exception as exc:
        print(f"✗ Failed to read PDF or extract fields: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # --- verification weights ----------------------------------------------
    weights = {
        "date": 0.3,
        "signature": 0.3,
        "agree": 0.4,
    }
    score = 0.0

    # 1) Date field -----------------------------------------------------------
    expected_date = "2024-12-15"
    actual_date = str(fields.get("date", {}).get("/V", "")).strip()
    if actual_date == expected_date:
        print(f"✓ Date field correct: {actual_date} (+{weights['date']})")
        score += weights["date"]
    else:
        print(f"✗ Date field incorrect – expected '{expected_date}', got '{actual_date}'")

    # 2) Signature field ------------------------------------------------------
    expected_sig = "John Doe"
    actual_sig = str(fields.get("signature", {}).get("/V", "")).strip()
    if actual_sig == expected_sig:
        print(f"✓ Signature field correct: {actual_sig} (+{weights['signature']})")
        score += weights["signature"]
    else:
        print(f"✗ Signature field incorrect – expected '{expected_sig}', got '{actual_sig}'")

    # 3) Checkbox field -------------------------------------------------------
    # Checkbox values are usually '/Yes', '/On', etc.  Normalise for safety.
    expected_truthy = {"yes", "on", "true", "1"}
    raw_checkbox_val = str(fields.get("agree", {}).get("/V", "")).strip()
    normalised_val = raw_checkbox_val.replace("/", "").lower()
    if normalised_val in expected_truthy:
        print(f"✓ 'I agree' checkbox checked (value='{raw_checkbox_val}') (+{weights['agree']})")
        score += weights["agree"]
    else:
        print(f"✗ 'I agree' checkbox not checked – value='{raw_checkbox_val}'")

    # --- final score capping -------------------------------------------------
    score = min(score, 1.0)
    print(f"Total score: {score}/1.0")
    print(f"REWARD: {score}")
    return score

if __name__ == "__main__":
    verify_pdf_task()

