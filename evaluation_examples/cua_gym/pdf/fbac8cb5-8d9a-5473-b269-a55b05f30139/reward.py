"""
FINAL REWARD SCRIPT - SUCCESS
Task: Rotate all pages in 'landscape_slides.pdf' on Desktop counterclockwise by 90 degrees to make them portrait. Save as 'portrait_slides.pdf'.
Generated: 2025-11-29 09:45:05
Status: success
Model: o3
Total Steps: 11
"""

from pathlib import Path
from PyPDF2 import PdfReader


def _normalize_rotation(val):
    """Return an int in the range 0-359 representing /Rotate value."""
    if val is None:
        return 0
    try:
        return int(val) % 360
    except Exception:
        # Handle the rare case where val is an indirect object
        try:
            return int(val.get_object()) % 360  # type: ignore[attr-defined]
        except Exception:
            return 0


def verify_rotation_task() -> float:
    """Reward script for the task:
    "Rotate all pages in 'landscape_slides.pdf' counter-clockwise by 90° and
    save as 'portrait_slides.pdf' on the Desktop."

    Verification logic
    ------------------
    1. Both PDFs exist on the Desktop (no points for mere existence).
    2. Page count of the new PDF equals the original (0.3 pts).
    3. Every page in the new PDF is rotated exactly –90° (i.e. 270°) relative
       to its counterpart in the original. The remaining 0.7 points are
       distributed evenly across pages.
    4. If *all* checks pass, score is forced to 1.0 to avoid floating-point
       precision issues.
    """

    orig_path = Path.home() / "Desktop" / "landscape_slides.pdf"
    new_path = Path.home() / "Desktop" / "portrait_slides.pdf"

    max_score = 1.0
    score = 0.0

    # Fail fast if either file is missing (prints are mandatory for auditability)
    if not orig_path.exists():
        print(f"✗ Original PDF missing: {orig_path}")
        print("REWARD: 0.0")
        return 0.0
    if not new_path.exists():
        print(f"✗ New PDF missing: {new_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDFs
    try:
        reader_orig = PdfReader(str(orig_path))
        reader_new  = PdfReader(str(new_path))
    except Exception as e:
        print(f"✗ Failed to load PDFs: {e}")
        print("REWARD: 0.0")
        return 0.0

    orig_pages = reader_orig.pages
    new_pages  = reader_new.pages

    # Requirement 1 – page-count consistency
    if len(orig_pages) == len(new_pages) and len(new_pages) > 0:
        score += 0.3
        print(f"✓ Page count matches ({len(new_pages)} pages) (+0.3)")
    else:
        print(f"✗ Page count mismatch: original={len(orig_pages)} new={len(new_pages)}")

    # Requirement 2 – per-page rotation
    if len(orig_pages):
        per_page_val = 0.7 / len(orig_pages)
    else:
        per_page_val = 0.0  # Should never happen because of check above

    correct_pages = 0
    for idx, (page_orig, page_new) in enumerate(zip(orig_pages, new_pages), start=1):
        rot_orig = _normalize_rotation(page_orig.get("/Rotate", 0))
        rot_new  = _normalize_rotation(page_new.get("/Rotate", 0))
        expected = (rot_orig - 90) % 360
        if rot_new == expected:
            correct_pages += 1
            score += per_page_val
            print(f"✓ Page {idx}: rotation correct (found {rot_new}, expected {expected}) (+{per_page_val:.3f})")
        else:
            print(f"✗ Page {idx}: rotation incorrect (found {rot_new}, expected {expected})")

    # Perfect completion → force 1.0 to dodge FP rounding artefacts
    if correct_pages == len(orig_pages) and len(orig_pages) == len(new_pages):
        final_score = 1.0
    else:
        final_score = round(min(score, max_score), 4)

    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_rotation_task()
