"""
Reward Script: Add sequential section numbers to thesis headings
Task ID: pdf_res_092
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists at correct path
  Component 2 (0.50): All 6 numbered headings present ("1. Introduction" through "6. Conclusion")
  Component 3 (0.20): No unnumbered standalone headings remain on their section pages
  Component 4 (0.15): Page count preserved (30 pages)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_092'
OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'numbered_thesis.pdf')

# The 6 headings and their expected numbered forms
HEADINGS = [
    ('Introduction', '1. Introduction'),
    ('Background', '2. Background'),
    ('Methodology', '3. Methodology'),
    ('Results', '4. Results'),
    ('Discussion', '5. Discussion'),
    ('Conclusion', '6. Conclusion'),
]

# Known heading pages (0-indexed) in the thesis
# Each heading appears as a bold title at the top of its section start page
HEADING_PAGES = {
    '1. Introduction': 2,
    '2. Background': 6,
    '3. Methodology': 10,
    '4. Results': 14,
    '5. Discussion': 18,
    '6. Conclusion': 22,
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.15 points)
    # This is a task-introduced change: numbered_thesis.pdf does NOT exist in initial_env
    try:
        if os.path.exists(OUTPUT_PATH):
            # Additional check: must be a valid PDF (not empty/corrupted)
            doc = pymupdf.open(OUTPUT_PATH)
            page_count = len(doc)
            doc.close()
            if page_count > 0:
                print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} with {page_count} pages (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — File exists but has 0 pages")
        else:
            print(f"FAIL: Component 1 — Output file not found at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document for remaining checks
    try:
        doc = pymupdf.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All 6 numbered headings present (0.50 points)
    # Each heading is worth ~0.0833 points (0.50 / 6)
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text") + "\n"

        found_count = 0
        per_heading_score = 0.50 / 6.0
        for orig, numbered in HEADINGS:
            if numbered in all_text:
                found_count += 1
                total_score += per_heading_score
                print(f"PASS: Component 2 — Found '{numbered}' in document ({per_heading_score:.4f} pts)")
            else:
                print(f"FAIL: Component 2 — '{numbered}' not found in document text")

        print(f"INFO: Component 2 summary — {found_count}/6 numbered headings found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No standalone unnumbered headings remain on section pages (0.20 points)
    # On each heading page, the heading text should now start with the number prefix
    # The unnumbered version should NOT appear as a standalone heading at the top
    try:
        unnumbered_removed = 0
        per_check = 0.20 / 6.0
        for orig, numbered in HEADINGS:
            expected_page = HEADING_PAGES.get(numbered)
            if expected_page is None or expected_page >= len(doc):
                continue

            page = doc[expected_page]
            page_text = page.get_text("text")

            # Get text lines to check if the unnumbered heading appears as a standalone line
            lines = [l.strip() for l in page_text.split('\n') if l.strip()]

            # Check that the unnumbered heading does NOT appear as a standalone line
            # (it's OK if it appears as part of a numbered heading like "1. Introduction")
            has_standalone_unnumbered = False
            for line in lines:
                # A standalone unnumbered heading would be just the word (e.g., "Introduction")
                # without a number prefix
                if line == orig:
                    has_standalone_unnumbered = True
                    break

            if not has_standalone_unnumbered:
                unnumbered_removed += 1
                total_score += per_check
                print(f"PASS: Component 3 — No standalone '{orig}' on page {expected_page} ({per_check:.4f} pts)")
            else:
                print(f"FAIL: Component 3 — Standalone '{orig}' still present on page {expected_page}")

        print(f"INFO: Component 3 summary — {unnumbered_removed}/6 unnumbered headings removed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page count preserved at 30 pages (0.15 points)
    # The numbered thesis should maintain the same page count as the original
    try:
        if len(doc) == 30:
            print(f"PASS: Component 4 — Page count is 30 as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected 30 pages, found {len(doc)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
