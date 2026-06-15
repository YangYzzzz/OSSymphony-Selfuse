"""
FINAL REWARD SCRIPT - SUCCESS
Task: Fill in the application form 'job_application.pdf' on Desktop with Name: 'John Smith', Email: 'john@email.com', Phone: '555-1234', and save as 'application_filled.pdf'.
Generated: 2025-11-29 09:58:40
Status: success
Model: o3
Total Steps: 7
"""

"""
Reward Script: verify_application_form.py
---------------------------------------
This script verifies that the user correctly filled in the PDF form
`application_filled.pdf` on the Desktop with the required field values.
It awards points progressively and returns a float in the range [0.0, 1.0].
It prints detailed diagnostics for each verification step and finally prints
`REWARD: X.X`, where `X.X` is the calculated score (exactly 1.0 for full
completion).
"""

from pathlib import Path
from PyPDF2 import PdfReader


def verify_application_form() -> float:
    """Return a reward score between 0.0 and 1.0 based on form completion."""

    expected_fields = {
        "name": "John Smith",
        "email": "john@email.com",
        "phone": "555-1234",
    }

    pdf_path = Path("/home/user/Desktop/application_filled.pdf")
    total_score = 0.0  # progressive scoring accumulator

    # 1. Check for PDF existence and loadability (0.2 points)
    if pdf_path.exists():
        print(f"✓ PDF found at {pdf_path} (0.2 points)")
        total_score += 0.2
        try:
            reader = PdfReader(str(pdf_path))  # load PDF
            fields = reader.get_fields() or {}
        except Exception as e:
            print(f"✗ Failed to load PDF or retrieve fields: {e}")
            fields = {}
    else:
        print(f"✗ PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0  # cannot proceed further if file missing

    # 2. Verify each expected AcroForm field
    #    Presence  = 0.1 pts each (3 * 0.1 = 0.3)
    #    Correct value = 0.2 pts each (3 * 0.2 = 0.6)
    for field_name, expected_value in expected_fields.items():
        if field_name in fields:
            print(f"✓ Field '{field_name}' present (0.1 points)")
            total_score += 0.1
            actual_value = fields[field_name].get("/V", "")
            if str(actual_value).strip() == expected_value:
                print(f"  ✓ Value correct: {actual_value} (0.2 points)")
                total_score += 0.2
            else:
                print(
                    f"  ✗ Value incorrect. Expected '{expected_value}', got '{actual_value}'"
                )
        else:
            print(f"✗ Field '{field_name}' missing from PDF")

    # 3. Cap at 1.0 and print final reward
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total computed score: {total_score} -> Capped final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_application_form()

