"""
Reward Script: Convert article.pdf to linearized (web-optimized) PDF
Task ID: pdf_gf1_034
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.15 points)
  Component 2: Page count matches original 8 pages (0.20 points)
  Component 3: PDF is linearized (/Linearized marker in header) (0.35 points)
  Component 4: Text content preserved across all pages (0.30 points)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_034'

ORIGINAL_PATH = f'{WORKDIR}/Documents/article.pdf'
LINEARIZED_PATH = f'{WORKDIR}/Documents/article_linearized.pdf'
EXPECTED_PAGE_COUNT = 8


def check_linearized(file_path):
    """Check if a PDF file has the /Linearized marker in its header.
    Linearized PDFs place a /Linearized dictionary in the first ~1024 bytes."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4096).decode('latin-1')
        return '/Linearized' in header
    except Exception:
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist (gate, not scored)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists at correct path (0.15 points)
    # This is a task-introduced change: the file does NOT exist in initial_env
    try:
        if os.path.exists(LINEARIZED_PATH):
            # Additional check: file must be a valid PDF (not empty/corrupt)
            doc = pymupdf.open(LINEARIZED_PATH)
            valid = doc.page_count > 0
            doc.close()
            if valid:
                print(f"PASS: Component 1 — article_linearized.pdf exists and is a valid PDF (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — article_linearized.pdf exists but is not a valid PDF")
        else:
            print(f"FAIL: Component 1 — article_linearized.pdf not found at {LINEARIZED_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If output file doesn't exist, remaining checks cannot proceed
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page count matches original (0.20 points)
    # The linearized PDF must preserve all 8 pages
    try:
        doc = pymupdf.open(LINEARIZED_PATH)
        actual_pages = doc.page_count
        doc.close()
        if actual_pages == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {actual_pages} (matches expected {EXPECTED_PAGE_COUNT}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Page count is {actual_pages}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF is linearized (0.35 points)
    # The core requirement: the output must be a linearized/web-optimized PDF
    try:
        is_linearized = check_linearized(LINEARIZED_PATH)
        if is_linearized:
            print(f"PASS: Component 3 — PDF has /Linearized marker in header (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — PDF does NOT have /Linearized marker — not linearized")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text content preserved across all pages (0.30 points)
    # Linearization should not alter content — verify text matches original
    try:
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        doc_lin = pymupdf.open(LINEARIZED_PATH)

        if doc_lin.page_count != doc_orig.page_count:
            print(f"FAIL: Component 4 — Cannot compare: page counts differ ({doc_lin.page_count} vs {doc_orig.page_count})")
        else:
            matching_pages = 0
            total_pages = doc_orig.page_count
            for i in range(total_pages):
                text_orig = doc_orig[i].get_text('text')
                text_lin = doc_lin[i].get_text('text')
                if text_orig == text_lin:
                    matching_pages += 1
                else:
                    print(f"  Page {i}: text mismatch (orig len={len(text_orig)}, lin len={len(text_lin)})")

            if matching_pages == total_pages:
                print(f"PASS: Component 4 — All {total_pages} pages have identical text content (0.30 pts)")
                total_score += 0.30
            elif matching_pages > 0:
                # Partial credit: proportional to pages that match
                partial = 0.30 * (matching_pages / total_pages)
                print(f"PARTIAL: Component 4 — {matching_pages}/{total_pages} pages match ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No pages have matching text content")

        doc_orig.close()
        doc_lin.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LINEARIZED_PATH):
    # Check if the file might be at an alternate location
    print(f"File not found: {LINEARIZED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
