"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please clear all filled data from 'reusable_form.pdf' in /home/user/Documents and save as 'form_blank.pdf' to create a clean template.
Generated: 2025-11-29 10:02:26
Status: success
Model: o3
Total Steps: 7
"""

import hashlib
from pathlib import Path
from PyPDF2 import PdfReader

"""
Reward script for:
"Please clear all filled data from 'reusable_form.pdf' in /home/user/Documents and save as 'form_blank.pdf' to create a clean template."

Scoring rubric (progressive 0.0–1.0):
1. Page-count of new PDF matches original (0.3)
2. All AcroForm fields exist AND are blank (0.7)
   • original must have contained at least one non-blank value to prove clearing
3. (Optional bonus) MD5 hash equals provided golden reference (maxes score at 1.0)

Returns exactly 1.0 when every requirement is satisfied.
"""

def _md5(path: Path) -> str:
    """Return MD5 hash of a file (binary-safe, chunked)."""
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def _is_blank(val) -> bool:
    """True if a PDF form value is considered blank/off/empty."""
    if val is None:
        return True
    if isinstance(val, str):
        stripped = val.strip()
        return stripped == "" or stripped in {"/Off", "Off"}
    # PyPDF2 NameObject equality works on str compare
    try:
        from PyPDF2.generic import NameObject
        if isinstance(val, NameObject) and val == "/Off":
            return True
    except Exception:
        pass
    return False

def verify_task() -> float:
    original_pdf = Path("/home/user/Documents/reusable_form.pdf")
    blank_pdf    = Path("/home/user/Documents/form_blank.pdf")
    golden_pdf   = Path("/home/user/please_clear_all_filled_data_from_reusable_formpdf_in_homeuserdocuments_and_save_as_form_blankpdf_to_golden.pdf")

    max_score   = 1.0
    total_score = 0.0

    # ---------- prerequisite: output must exist ----------
    if not blank_pdf.exists():
        print(f"✗ Expected output file not found: {blank_pdf}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- load PDFs ----------
    try:
        original_reader = PdfReader(str(original_pdf))
        blank_reader    = PdfReader(str(blank_pdf))
    except Exception as e:
        print(f"✗ Error loading PDFs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- requirement 1: page-count unchanged ----------
    if len(original_reader.pages) == len(blank_reader.pages):
        print("✓ Page count matches original (0.3)")
        total_score += 0.3
    else:
        print(f"✗ Page count differs → original:{len(original_reader.pages)} blank:{len(blank_reader.pages)}")

    # ---------- requirement 2: all form fields present & blank ----------
    orig_fields  = original_reader.get_fields() or {}
    blank_fields = blank_reader.get_fields()    or {}

    if not blank_fields:
        print("✗ No AcroForm fields detected in form_blank.pdf – form structure lost")
    else:
        # (a) every field truly blank in new PDF
        all_blank = True
        for fname, fdata in blank_fields.items():
            val = fdata.get("/V")
            if not _is_blank(val):
                all_blank = False
                print(f"✗ Field '{fname}' is NOT blank (value={val})")
        # (b) prove that at least one field WAS filled in the original
        previously_filled = any(not _is_blank(fdata.get("/V")) for fdata in orig_fields.values())

        if all_blank and previously_filled:
            print("✓ All fields are blank and original had filled values (0.7)")
            total_score += 0.7
        elif all_blank:
            # No evidence of clearing; grant partial credit
            print("! Fields blank but original contained no filled values (0.35)")
            total_score += 0.35
        else:
            print("✗ Some fields still contain data – no credit for this section")

    # ---------- optional integrity: exact match to golden ----------
    if golden_pdf.exists() and total_score < max_score:
        if _md5(blank_pdf) == _md5(golden_pdf):
            bonus = min(max_score - total_score, 0.1)
            print(f"✓ Output exactly matches golden reference (+{bonus:.2f})")
            total_score += bonus
        else:
            print("ℹ Output differs from golden reference (no bonus)")
    else:
        if not golden_pdf.exists():
            print("ℹ Golden reference not found – hash comparison skipped")

    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ------------- run verification -------------
if __name__ == "__main__":
    verify_task()
