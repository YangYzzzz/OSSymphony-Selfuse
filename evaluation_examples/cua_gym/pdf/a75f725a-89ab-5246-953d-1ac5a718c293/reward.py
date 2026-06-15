"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a PDF 'double_sided.pdf' with pages scanning as [front1, back1, front2, back2, ...]. Reorder them to [front1, front2, front3, ...] in 'single_sided_ordered.pdf'.
Generated: 2025-11-29 09:40:24
Status: success
Model: o3
Total Steps: 6
"""

from pathlib import Path
from PyPDF2 import PdfReader


def verify_reordering(original_path: str = "/home/user/double_sided.pdf",
                      result_path: str = "/home/user/single_sided_ordered.pdf") -> float:
    """Verify that the double-sided scan has been reordered into a single-sided PDF.

    Scoring (progressive):
      • 0.4 – result PDF has the exact number of front pages
      • 0.6 – every page appears in the correct order (front1, front2, …)
      • 1.0 – both conditions satisfied
    """

    max_score = 1.0
    score = 0.0

    original = Path(original_path)
    result = Path(result_path)

    # ---------- Basic existence checks (no points awarded) ----------
    if not original.exists():
        print(f"✗ Original PDF missing: {original_path}")
        return 0.0
    if not result.exists():
        print(f"✗ Result PDF missing: {result_path}")
        return 0.0

    # ---------- Load PDFs ----------
    try:
        orig_reader = PdfReader(original.open("rb"))
    except Exception as e:
        print(f"✗ Failed to read original PDF: {e}")
        return 0.0

    try:
        res_reader = PdfReader(result.open("rb"))
    except Exception as e:
        print(f"✗ Failed to read result PDF: {e}")
        return 0.0

    orig_pages = len(orig_reader.pages)
    res_pages = len(res_reader.pages)

    # ---------- Requirement 1: Correct page count ----------
    expected_front_pages = (orig_pages + 1) // 2  # half, rounding up
    print(f"Original pages          : {orig_pages}")
    print(f"Expected front pages    : {expected_front_pages}")
    print(f"Result PDF page count   : {res_pages}")

    if res_pages == expected_front_pages:
        score += 0.4
        print("✓ Result PDF has correct number of pages (0.4)")
    else:
        print("✗ Incorrect number of pages in result PDF (0 pts)")

    # ---------- Requirement 2: Correct ordering of front pages ----------
    expected_texts = []
    for i in range(0, orig_pages, 2):  # 0,2,4,… → front pages only
        txt = orig_reader.pages[i].extract_text() or ""
        expected_texts.append(txt.strip())

    ordering_ok = True
    if res_pages != len(expected_texts):
        ordering_ok = False
    else:
        for idx in range(res_pages):
            expected_text = expected_texts[idx]
            actual_text = (res_reader.pages[idx].extract_text() or "").strip()
            if actual_text != expected_text:
                print(f"✗ Page {idx+1} mismatch: expected '{expected_text}' | got '{actual_text}'")
                ordering_ok = False
            else:
                print(f"✓ Page {idx+1} text matches expected '{expected_text}'")

    if ordering_ok:
        score += 0.6
        print("✓ All page texts in correct order (0.6)")
    else:
        print("✗ Page ordering incorrect (0 pts)")

    # ---------- Final score ----------
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_reordering()

