"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add an owner password 'admin2024' to 'financial_data.pdf' in /home/user/Documents to restrict editing while keeping it readable. Save as 'financial_secured.pdf'.
Generated: 2025-11-29 09:47:48
Status: success
Model: o3
Total Steps: 10
"""

"""
Reward Script: Verify owner-password protection of financial_secured.pdf
Task:  Add an owner password 'admin2024' to 'financial_data.pdf' (kept readable) and
       save result as 'financial_secured.pdf' in /home/user/Documents.

Verification Strategy (progressive score):
  1) PDF must exist and report as encrypted                        – 0.4
  2) Empty password must decrypt with USER privileges (readable)   – 0.3
  3) Owner password 'admin2024' must decrypt with OWNER privileges – 0.3

Total possible score = 1.0.  Any failure in the above steps loses the
associated points.  No points are awarded for mere file existence alone;
all points require successful, falsifiable checks using PyPDF2.
"""

from pathlib import Path
from PyPDF2 import PdfReader, PasswordType

# ---------------------------------------------------------------------------
# CONFIGURATION --------------------------------------------------------------
# ---------------------------------------------------------------------------
SECURED_PATH = Path("/home/user/Documents/financial_secured.pdf")
OWNER_PWD    = "admin2024"
# ---------------------------------------------------------------------------


def verify_pdf_security(pdf_path: Path, owner_pwd: str) -> float:
    """Return a progressive score ∈ [0.0, 1.0] for the verification task."""

    max_score = 1.0
    score     = 0.0

    # ----- Step 0: File existence ------------------------------------------------
    if not pdf_path.exists():
        print("✗ Secured PDF is missing – task failed early")
        print("REWARD: 0.0")
        return 0.0

    # ----- Step 1: Load PDF -------------------------------------------------------
    try:
        reader = PdfReader(pdf_path)
    except Exception as exc:
        print(f"✗ Unable to load PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # ----- Step 2: Must be encrypted ---------------------------------------------
    if reader.is_encrypted:
        print("✓ PDF reports as encrypted (0.4 points)")
        score += 0.4
    else:
        print("✗ PDF is not encrypted – no owner password applied")
        print(f"REWARD: {score}")
        return score  # cannot continue meaningfully

    # ----- Step 3: Empty password should decrypt (USER) --------------------------
    try:
        res_user = reader.decrypt("")
        if res_user in (PasswordType.USER_PASSWORD, 1):  # 1 is fallback for PyPDF2<3.0
            # Confirm we can access at least one page to prove readability
            _ = reader.pages[0]
            print("✓ Empty password opens PDF with USER privileges (0.3 points)")
            score += 0.3
        else:
            print("✗ Empty password failed to provide USER access")
    except Exception as exc:
        print(f"✗ Error decrypting with empty password: {exc}")

    # ----- Step 4: Owner password must decrypt (OWNER) ---------------------------
    try:
        owner_reader = PdfReader(pdf_path)
        res_owner = owner_reader.decrypt(owner_pwd)
        if res_owner in (PasswordType.OWNER_PASSWORD, 2):  # 2 is fallback code
            _ = owner_reader.pages[0]
            print("✓ Owner password 'admin2024' unlocks OWNER privileges (0.3 points)")
            score += 0.3
        else:
            print("✗ Owner password did not grant OWNER privileges")
    except Exception as exc:
        print(f"✗ Error decrypting with owner password: {exc}")

    # ----- Final reporting -------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total Score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_pdf_security(SECURED_PATH, OWNER_PWD)

