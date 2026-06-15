"""
Reward Script: Rotate pages of a scanned PDF
Task ID: pdf_gf2_018
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists, valid PDF, 10 pages
  - Component 2 (0.35): Pages 1-4 rotated 90 degrees CW
  - Component 3 (0.25): Pages 5-6 rotated 180 degrees
  - Component 4 (0.25): Pages 7-10 have rotation 0 (unchanged)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_018'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists, is a valid PDF, and has exactly 10 pages (0.15 points)
    try:
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count == 10:
            print(f"PASS: Component 1 — valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected 10 pages, found {page_count}")
            doc.close()
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Pages 1-4 (indices 0-3) have rotation == 90 (0.35 points)
    # Each page contributes 0.35/4 = 0.0875 points
    try:
        correct_count = 0
        for i in range(4):
            rotation = doc[i].rotation
            if rotation == 90:
                correct_count += 1
                print(f"  Page {i+1}: rotation={rotation} — CORRECT")
            else:
                print(f"  Page {i+1}: rotation={rotation} — expected 90")

        if correct_count == 4:
            print(f"PASS: Component 2 — all 4 pages (1-4) rotated 90° CW (0.35 pts)")
            total_score += 0.35
        elif correct_count > 0:
            partial = round(0.35 * correct_count / 4, 4)
            print(f"PARTIAL: Component 2 — {correct_count}/4 pages correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no pages 1-4 have rotation 90")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages 5-6 (indices 4-5) have rotation == 180 (0.25 points)
    # Each page contributes 0.25/2 = 0.125 points
    try:
        correct_count = 0
        for i in range(4, 6):
            rotation = doc[i].rotation
            if rotation == 180:
                correct_count += 1
                print(f"  Page {i+1}: rotation={rotation} — CORRECT")
            else:
                print(f"  Page {i+1}: rotation={rotation} — expected 180")

        if correct_count == 2:
            print(f"PASS: Component 3 — both pages (5-6) rotated 180° (0.25 pts)")
            total_score += 0.25
        elif correct_count > 0:
            partial = round(0.25 * correct_count / 2, 4)
            print(f"PARTIAL: Component 3 — {correct_count}/2 pages correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no pages 5-6 have rotation 180")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages 7-10 (indices 6-9) have rotation == 0 (0.25 points)
    # Each page contributes 0.25/4 = 0.0625 points
    try:
        correct_count = 0
        for i in range(6, 10):
            rotation = doc[i].rotation
            if rotation == 0:
                correct_count += 1
                print(f"  Page {i+1}: rotation={rotation} — CORRECT")
            else:
                print(f"  Page {i+1}: rotation={rotation} — expected 0")

        if correct_count == 4:
            print(f"PASS: Component 4 — all 4 pages (7-10) have rotation 0 (0.25 pts)")
            total_score += 0.25
        elif correct_count > 0:
            partial = round(0.25 * correct_count / 4, 4)
            print(f"PARTIAL: Component 4 — {correct_count}/4 pages correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no pages 7-10 have rotation 0")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/scans/mixed_scan_corrected.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
