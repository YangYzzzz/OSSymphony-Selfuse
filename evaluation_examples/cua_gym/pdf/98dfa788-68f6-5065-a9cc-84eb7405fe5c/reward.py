"""
Reward Script: Merge four quarterly report PDFs into a single annual report
with separator pages labeled Q1, Q2, Q3, Q4 between each section.
Task ID: pdf_gf2_001
Domain: pdf
Scoring:
  - Precondition: merged file exists and is valid PDF (gate)
  - Component 1 (0.25): Correct total page count (38 pages)
  - Component 2 (0.35): Four separator pages at correct positions with correct labels
  - Component 3 (0.25): Content from all four quarterly reports preserved
  - Component 4 (0.15): Original quarterly PDFs still intact
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_001'
MERGED_PATH = os.path.join(WORKDIR, 'finance', 'annual_report_2025.pdf')
FINANCE_DIR = os.path.join(WORKDIR, 'finance')

# Expected structure:
# Page 0: Q1 separator
# Pages 1-8: Q1 content (8 pages)
# Page 9: Q2 separator
# Pages 10-18: Q2 content (9 pages)
# Page 19: Q3 separator
# Pages 20-26: Q3 content (7 pages)
# Page 27: Q4 separator
# Pages 28-37: Q4 content (10 pages)
# Total: 4 separators + 34 content = 38 pages

EXPECTED_PAGE_COUNT = 38
SEPARATOR_PAGES = {
    0: 'Q1',
    9: 'Q2',
    19: 'Q3',
    27: 'Q4',
}
QUARTERLY_FILES = ['q1_report.pdf', 'q2_report.pdf', 'q3_report.pdf', 'q4_report.pdf']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File exists and is a valid PDF
    if not os.path.exists(MERGED_PATH):
        print(f"CRITICAL: Merged file not found at {MERGED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(MERGED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open merged PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct total page count (0.25 points)
    try:
        actual_count = doc.page_count
        if actual_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Page count is {actual_count} (expected {EXPECTED_PAGE_COUNT}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Page count is {actual_count}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Separator pages at correct positions with correct labels (0.35 points)
    # Each separator is worth 0.35/4 = 0.0875 points
    try:
        sep_score = 0.0
        points_per_sep = 0.35 / 4.0
        for page_idx, expected_label in SEPARATOR_PAGES.items():
            if page_idx >= doc.page_count:
                print(f"FAIL: Component 2 — Page {page_idx} does not exist (need '{expected_label}' separator)")
                continue
            page = doc[page_idx]
            text = page.get_text().strip()
            if text == expected_label:
                print(f"PASS: Component 2 — Page {page_idx} is '{expected_label}' separator ({points_per_sep:.4f} pts)")
                sep_score += points_per_sep
            else:
                # Allow some flexibility: check if the label is present even if other text exists
                if expected_label in text and len(text) < 20:
                    print(f"PASS: Component 2 — Page {page_idx} contains '{expected_label}' (text: '{text}') ({points_per_sep:.4f} pts)")
                    sep_score += points_per_sep
                else:
                    print(f"FAIL: Component 2 — Page {page_idx} text is '{text[:50]}', expected '{expected_label}'")
        total_score += sep_score
        print(f"  Component 2 subtotal: {sep_score:.4f}/0.35")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content from quarterly reports preserved (0.25 points)
    # Check distinctive text from each quarter's content pages
    try:
        content_score = 0.0
        points_per_quarter = 0.25 / 4.0

        # Q1: check page 1 (first content page after Q1 separator)
        # Expected: "Meridian Technologies Inc." and "Q1 (January - March)"
        checks = [
            (1, "Q1 (January - March)", "Q1 title page"),
            (10, "Q2 (April - June)", "Q2 title page"),
            (20, "Q3 (July - September)", "Q3 title page"),
            (28, "Q4 (October - December)", "Q4 title page"),
        ]
        for page_idx, search_text, desc in checks:
            if page_idx >= doc.page_count:
                print(f"FAIL: Component 3 — Page {page_idx} missing for {desc}")
                continue
            page_text = doc[page_idx].get_text()
            if search_text in page_text:
                print(f"PASS: Component 3 — {desc} found on page {page_idx} ({points_per_quarter:.4f} pts)")
                content_score += points_per_quarter
            else:
                print(f"FAIL: Component 3 — {desc} not found on page {page_idx}")
        total_score += content_score
        print(f"  Component 3 subtotal: {content_score:.4f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    # Component 4: Original quarterly PDFs still intact (0.15 points)
    try:
        orig_score = 0.0
        points_per_file = 0.15 / 4.0
        expected_pages = {'q1_report.pdf': 8, 'q2_report.pdf': 9, 'q3_report.pdf': 7, 'q4_report.pdf': 10}
        for fname, exp_pages in expected_pages.items():
            fpath = os.path.join(FINANCE_DIR, fname)
            if os.path.exists(fpath):
                try:
                    qdoc = pymupdf.open(fpath)
                    if qdoc.page_count == exp_pages:
                        print(f"PASS: Component 4 — {fname} exists with {exp_pages} pages ({points_per_file:.4f} pts)")
                        orig_score += points_per_file
                    else:
                        print(f"FAIL: Component 4 — {fname} has {qdoc.page_count} pages, expected {exp_pages}")
                    qdoc.close()
                except Exception as e:
                    print(f"FAIL: Component 4 — Cannot open {fname}: {e}")
            else:
                print(f"FAIL: Component 4 — {fname} missing")
        total_score += orig_score
        print(f"  Component 4 subtotal: {orig_score:.4f}/0.15")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
