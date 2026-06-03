"""
Reward Script: Merge PDFs in alphabetical order with bookmarks
Task ID: pdf_legal_056
Domain: pdf
Scoring:
  Component 1 — Output file exists at correct path (0.1 pts)
  Component 2 — Total page count is 40 (0.2 pts)
  Component 3 — Exactly 8 bookmarks present (0.2 pts)
  Component 4 — Bookmark titles match filenames (no ext), alphabetical order (0.3 pts)
  Component 5 — Bookmark page offsets are correct (0.2 pts)
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_056'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'closing_binder_complete.pdf')
SOURCE_DIR = os.path.join(WORKDIR, 'legal', 'closing_docs')

# Expected files in alphabetical order with their page counts
EXPECTED_FILES = [
    ('assignment', 3),
    ('bill_of_sale', 2),
    ('closing_statement', 4),
    ('deed', 2),
    ('escrow_instructions', 6),
    ('mortgage', 12),
    ('promissory_note', 3),
    ('title_policy', 8),
]

EXPECTED_TOTAL_PAGES = 40


def compute_expected_offsets():
    """Compute expected 1-indexed page offsets for bookmarks."""
    offsets = []
    current_page = 1
    for name, page_count in EXPECTED_FILES:
        offsets.append((name, current_page))
        current_page += page_count
    return offsets


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.1 points)
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            print(f"PASS: Component 1 -- Output file exists at {OUTPUT_PATH} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- Output file not found or empty at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the merged PDF
    try:
        doc = pymupdf.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open {OUTPUT_PATH}: {e}")
        print("REWARD: 0.1")
        return 0.1

    # Component 2: Total page count is 40 (0.2 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_TOTAL_PAGES:
            print(f"PASS: Component 2 -- Page count is {page_count} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- Expected {EXPECTED_TOTAL_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Get TOC (bookmarks)
    try:
        toc = doc.get_toc()
    except Exception as e:
        print(f"CRITICAL: Cannot read TOC: {e}")
        doc.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Exactly 8 bookmarks present (0.2 points)
    try:
        num_bookmarks = len(toc)
        if num_bookmarks == 8:
            print(f"PASS: Component 3 -- Found {num_bookmarks} bookmarks (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected 8 bookmarks, found {num_bookmarks}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Bookmark titles match filenames (no ext) in alphabetical order (0.3 points)
    try:
        expected_names = [name for name, _ in EXPECTED_FILES]
        actual_names = [entry[1].strip() for entry in toc]
        if actual_names == expected_names:
            print(f"PASS: Component 4 -- Bookmark titles correct and in alphabetical order (0.3 pts)")
            total_score += 0.3
        else:
            # Partial credit: count how many titles match in order
            matches = 0
            for i in range(min(len(actual_names), len(expected_names))):
                if actual_names[i] == expected_names[i]:
                    matches += 1
            if len(expected_names) > 0:
                ratio = matches / len(expected_names)
                partial = round(0.3 * ratio, 2)
                total_score += partial
                print(f"PARTIAL: Component 4 -- {matches}/{len(expected_names)} titles match ({partial} pts)")
            print(f"  Expected: {expected_names}")
            print(f"  Actual:   {actual_names}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Bookmark page offsets are correct (0.2 points)
    try:
        expected_offsets = compute_expected_offsets()
        if len(toc) == len(expected_offsets):
            correct_offsets = 0
            for i, (exp_name, exp_page) in enumerate(expected_offsets):
                actual_page = toc[i][2]
                if actual_page == exp_page:
                    correct_offsets += 1
                else:
                    print(f"  Offset mismatch for '{exp_name}': expected page {exp_page}, got {actual_page}")
            if correct_offsets == len(expected_offsets):
                print(f"PASS: Component 5 -- All 8 bookmark offsets correct (0.2 pts)")
                total_score += 0.2
            else:
                ratio = correct_offsets / len(expected_offsets)
                partial = round(0.2 * ratio, 2)
                total_score += partial
                print(f"PARTIAL: Component 5 -- {correct_offsets}/{len(expected_offsets)} offsets correct ({partial} pts)")
        else:
            print(f"FAIL: Component 5 -- Cannot check offsets, bookmark count mismatch")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
