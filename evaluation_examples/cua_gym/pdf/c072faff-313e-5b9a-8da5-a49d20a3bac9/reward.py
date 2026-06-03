"""
Reward Script: Rotate landscape pages to portrait in a mixed-orientation PDF
Task ID: pdf_gf1_039
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid PDF
  Component 2 (0.15): PDF has exactly 8 pages
  Component 3 (0.40): Pages 3 and 6 (originally landscape) are now effectively portrait
  Component 4 (0.30): Portrait pages (1,2,4,5,7,8) remain portrait with no rotation change
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_039'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF (0.15 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        if doc.is_pdf:
            print(f"PASS: Component 1 — Output file exists and is a valid PDF (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — File is not a valid PDF")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"FAIL: Component 1 — Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: PDF has exactly 8 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 8:
            print(f"PASS: Component 2 — PDF has exactly 8 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages 3 and 6 are now effectively portrait (0.40 points)
    # These were landscape (792x612) in the original. After rotation they should be portrait.
    # We check that the effective rect has height > width.
    try:
        landscape_pages = [2, 5]  # 0-indexed: pages 3 and 6
        rotated_count = 0
        for idx in landscape_pages:
            if idx < len(doc):
                page = doc[idx]
                r = page.rect  # effective rect (accounts for rotation)
                if r.height > r.width:
                    rotated_count += 1
                    print(f"  Page {idx+1}: effectively portrait ({r.width:.0f}x{r.height:.0f}, rot={page.rotation}) — OK")
                else:
                    print(f"  Page {idx+1}: still landscape ({r.width:.0f}x{r.height:.0f}, rot={page.rotation}) — FAIL")
            else:
                print(f"  Page {idx+1}: does not exist")

        if rotated_count == 2:
            print(f"PASS: Component 3 — Both landscape pages are now portrait (0.40 pts)")
            total_score += 0.40
        elif rotated_count == 1:
            print(f"PARTIAL: Component 3 — Only 1 of 2 landscape pages corrected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Neither landscape page was corrected")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Portrait pages (1,2,4,5,7,8) remain portrait with no rotation added (0.30 points)
    # These should still be portrait (height > width) and ideally have rotation=0.
    try:
        portrait_pages = [0, 1, 3, 4, 6, 7]  # 0-indexed: pages 1,2,4,5,7,8
        unchanged_count = 0
        for idx in portrait_pages:
            if idx < len(doc):
                page = doc[idx]
                r = page.rect
                if r.height > r.width:
                    unchanged_count += 1
                else:
                    print(f"  Page {idx+1}: not portrait ({r.width:.0f}x{r.height:.0f}, rot={page.rotation}) — FAIL")

        if unchanged_count == 6:
            print(f"PASS: Component 4 — All 6 portrait pages remain portrait (0.30 pts)")
            total_score += 0.30
        elif unchanged_count >= 4:
            partial = round(0.30 * (unchanged_count / 6), 2)
            print(f"PARTIAL: Component 4 — {unchanged_count}/6 portrait pages remain portrait ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {unchanged_count}/6 portrait pages are correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/mixed_orientation_fixed.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
