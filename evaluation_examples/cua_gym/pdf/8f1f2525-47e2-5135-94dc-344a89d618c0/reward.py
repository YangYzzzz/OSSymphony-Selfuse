"""
Reward Script: Rotate pages 5 and 6 of landscape_figures.pdf by 90 degrees clockwise
Task ID: pdf_res_030
Domain: pdf
Scoring:
  - Component 1: Output file exists (0.1 pts) — task-introduced, file does not exist in initial_env
  - Component 2: Pages 5 and 6 (1-indexed) have rotation=90 (0.5 pts)
  - Component 3: All other pages retain rotation=0 (0.3 pts)
  - Component 4: Page count remains 10 (0.1 pts) — combined with file loadability
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_030'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'landscape_figures_fixed.pdf')

# Pages that should be rotated (1-indexed pages 5 and 6 = 0-indexed 4 and 5)
ROTATED_PAGES = {4, 5}
EXPECTED_ROTATION = 90
TOTAL_PAGES = 10


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.1 points)
    # This is task-introduced: the file does NOT exist in initial_env
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"PASS: Component 1 — Output file exists at {file_path} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Output file not found or empty at {file_path}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 4 (gate + scoring): Page count remains 10 (0.1 points)
    try:
        page_count = len(doc)
        if page_count == TOTAL_PAGES:
            print(f"PASS: Component 4 — Page count is {page_count} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Expected {TOTAL_PAGES} pages, found {page_count}")
            # Don't return early; partial credit possible but page checks may be off
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 2: Pages 5 and 6 (0-indexed 4, 5) have rotation=90 (0.5 points)
    # 0.25 points per correctly rotated page
    try:
        rotated_score = 0.0
        for page_idx in sorted(ROTATED_PAGES):
            if page_idx < len(doc):
                page = doc[page_idx]
                rotation = page.rotation
                if rotation == EXPECTED_ROTATION:
                    print(f"PASS: Component 2 — Page {page_idx + 1} rotation is {rotation} degrees (0.25 pts)")
                    rotated_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Page {page_idx + 1} rotation is {rotation}, expected {EXPECTED_ROTATION}")
            else:
                print(f"FAIL: Component 2 — Page {page_idx + 1} does not exist (only {len(doc)} pages)")
        if rotated_score > 0:
            total_score += rotated_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All other pages retain rotation=0 (0.3 points)
    # Distribute evenly across the 8 non-rotated pages (0.0375 each)
    try:
        other_correct = 0
        other_total = 0
        for page_idx in range(min(len(doc), TOTAL_PAGES)):
            if page_idx not in ROTATED_PAGES:
                other_total += 1
                page = doc[page_idx]
                rotation = page.rotation
                if rotation == 0:
                    other_correct += 1
                else:
                    print(f"FAIL: Component 3 — Page {page_idx + 1} rotation is {rotation}, expected 0")

        if other_total > 0:
            comp3_score = 0.3 * (other_correct / other_total)
            if other_correct == other_total:
                print(f"PASS: Component 3 — All {other_total} non-rotated pages have rotation=0 (0.3 pts)")
            else:
                print(f"PARTIAL: Component 3 — {other_correct}/{other_total} non-rotated pages correct ({comp3_score:.3f} pts)")
            if comp3_score > 0:
                total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No non-rotated pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
