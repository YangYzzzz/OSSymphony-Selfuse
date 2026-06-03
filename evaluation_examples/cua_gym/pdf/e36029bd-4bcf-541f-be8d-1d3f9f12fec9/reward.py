"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to rotate pages 3, 5, and 7 in 'scanned_document.pdf' clockwise by 90 degrees. Save the corrected version as 'document_rotated.pdf' in /home/user/Documents.
Generated: 2025-11-29 09:41:39
Status: success
Model: o3
Total Steps: 8
"""

from PyPDF2 import PdfReader
from pathlib import Path


def verify_pdf_rotation() -> float:
    """Reward script for:
    Rotate pages 3, 5, and 7 in 'scanned_document.pdf' clockwise by 90°
    and save as 'document_rotated.pdf' in /home/user/Documents.

    Returns a progressive score (0.0–1.0) and prints detailed feedback.
    """

    original_path = Path("/home/user/Documents/scanned_document.pdf")
    rotated_path = Path("/home/user/Documents/document_rotated.pdf")
    target_pages = [3, 5, 7]  # 1-indexed page numbers to be rotated

    max_score = 1.0
    score = 0.0

    print("--- PDF Rotation Verification ---")
    print(f"Original PDF: {original_path}")
    print(f"Rotated  PDF: {rotated_path}\n")

    # 1. Verify files exist and are readable
    if not rotated_path.exists():
        print(f"✗ Rotated PDF not found at {rotated_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        orig_reader = PdfReader(str(original_path))
        rot_reader = PdfReader(str(rotated_path))
        print("✓ Both PDFs successfully loaded")
    except Exception as e:
        print(f"✗ Error opening PDFs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 2. Page-count consistency (0.2 pts)
    orig_pages = len(orig_reader.pages)
    rot_pages = len(rot_reader.pages)
    if orig_pages == rot_pages and orig_pages > 0:
        score += 0.2
        print(f"✓ Page count matches ({orig_pages}) (+0.2)")
    else:
        print(f"✗ Page count mismatch (orig={orig_pages}, rot={rot_pages})")

    # 3. Rotation checks (0.2 pts each for p3, p5, p7)
    target_zero_idx = {p - 1 for p in target_pages}  # convert to 0-indexed
    non_target_clean = True

    for idx in range(rot_pages):
        orig_rot = (orig_reader.pages[idx].get("/Rotate") or 0) % 360
        new_rot  = (rot_reader.pages[idx].get("/Rotate") or 0) % 360
        diff     = (new_rot - orig_rot) % 360
        page_num = idx + 1

        if idx in target_zero_idx:
            if diff == 90:
                score += 0.2
                print(f"✓ Page {page_num} correctly rotated +90° (+0.2)")
            else:
                print(f"✗ Page {page_num} rotation off by {diff}° (expected 90°)")
        else:
            if diff != 0:
                non_target_clean = False
                print(f"✗ Page {page_num} unexpectedly rotated by {diff}°")

    # 4. Bonus if all non-target pages are untouched (0.2 pts)
    if non_target_clean and rot_pages > len(target_zero_idx):
        score += 0.2
        print("✓ All non-target pages unchanged (+0.2)")
    elif not non_target_clean:
        print("✗ One or more non-target pages were altered")
    else:
        # Edge case: every page was a target
        print("ℹ No non-target pages to verify")

    final_score = min(score, max_score)
    print(f"\nTotal score: {final_score:.2f}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_pdf_rotation()

