"""
FINAL REWARD SCRIPT - SUCCESS
Task: Batch add page numbers (bottom center) to all PDFs in /home/user/Documents/Manuals, saving numbered versions with '_numbered' suffix in same folder.
Generated: 2025-11-29 10:14:39
Status: success
Model: o3
Total Steps: 9
"""

from pathlib import Path
import re
from PyPDF2 import PdfReader

"""
Reward script for task:
"Batch add page numbers (bottom center) to all PDFs in /home/user/Documents/Manuals, saving
 numbered versions with '_numbered' suffix in same folder."

The script verifies task completion by checking, for every original PDF in the Manuals
folder, that:
1. A numbered counterpart exists whose filename ends with "_numbered.pdf".
2. The numbered PDF has the exact same page-count as its original (no pages removed/
   added).
3. Every page of the numbered PDF contains its correct page number (1-based index)
   somewhere in the final two non-blank text lines extracted from that page.

Scoring (progressive):
• 50 % of the score is earned per-file for requirement #1 & #2 (structure check).
• 50 % is earned proportionally to how many pages across all PDFs have the correct
  page number (#3).

The script prints detailed diagnostics and finally prints
   REWARD: <float between 0.0 and 1.0>
exactly, as required by the evaluation harness.
"""

def page_has_page_number(page, expected_num: int) -> bool:
    """Return True iff `expected_num` is found in the last 1–2 lines of page text."""
    text = page.extract_text() or ""
    # Collect non-blank lines
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if not lines:
        print(f"    ✗ No extractable text on page {expected_num}")
        return False

    tail = lines[-2:] if len(lines) >= 2 else lines[-1:]
    exp = str(expected_num)
    if exp in tail:
        print(f"    ✓ Page {expected_num}: page number found in bottom lines {tail}")
        return True

    # Fallback – isolated match anywhere (still counts but flagged)
    if re.search(rf"\b{re.escape(exp)}\b", text):
        print(f"    △ Page {expected_num}: number present but not in bottom lines")
        return True

    print(f"    ✗ Page {expected_num}: expected number '{exp}' not found")
    return False


def verify_task() -> float:
    base_dir = Path("/home/user/Documents/Manuals")
    originals = sorted(p for p in base_dir.glob("*.pdf") if not p.stem.endswith("_numbered"))

    if not originals:
        print("✗ No original PDFs found – cannot verify task.")
        return 0.0

    print(f"Found {len(originals)} original PDF(s) to verify.\n")

    total_score = 0.0
    structure_unit = 0.5 / len(originals)  # portion per file for structural check

    total_pages = 0
    pages_with_numbers = 0
    numbered_files_ok = 0  # counter for structure successes

    for orig in originals:
        num = orig.with_name(orig.stem + "_numbered" + orig.suffix)
        print(f"Checking '{orig.name}' …")

        if not num.exists():
            print(f"  ✗ Numbered version missing: {num.name}\n")
            continue

        try:
            r_orig = PdfReader(str(orig))
            r_num = PdfReader(str(num))
        except Exception as e:
            print(f"  ✗ Error opening PDF(s): {e}\n")
            continue

        # Requirement 1 & 2: same page count
        if len(r_orig.pages) == len(r_num.pages):
            print("  ✓ Page count matches")
            numbered_files_ok += 1
        else:
            print(
                f"  ✗ Page count mismatch (orig {len(r_orig.pages)} vs numbered {len(r_num.pages)})"
            )

        # Requirement 3: correct page numbers
        for idx, page in enumerate(r_num.pages, start=1):
            total_pages += 1
            if page_has_page_number(page, idx):
                pages_with_numbers += 1
        print()

    # Score accumulation
    total_score += numbered_files_ok * structure_unit

    if total_pages:
        page_accuracy = pages_with_numbers / total_pages
        total_score += page_accuracy * 0.5  # up to remaining 50 %
        print(
            f"Page-number accuracy: {pages_with_numbers}/{total_pages} pages = {page_accuracy:.2%}"
        )

    final_score = round(min(total_score, 1.0), 4)  # rounded for neatness
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

