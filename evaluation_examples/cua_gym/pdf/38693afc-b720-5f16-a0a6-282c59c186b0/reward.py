"""
Reward Script: Side-by-side PDF comparison document
Task ID: pdf_res_031
Domain: pdf
Scoring:
  Component 1: Output file exists and is a valid PDF (0.15 pts) — gate + basic validity
  Component 2: Page count is exactly 5 (0.25 pts)
  Component 3: Pages are wider than source pages (double-width layout) (0.25 pts)
  Component 4: Each page contains content from both original and revised PDFs (0.35 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_031'

OUTPUT_PATH = f'{WORKDIR}/papers/side_by_side.pdf'
ORIGINAL_PATH = f'{WORKDIR}/papers/original.pdf'
REVISED_PATH = f'{WORKDIR}/papers/revised.pdf'

EXPECTED_PAGE_COUNT = 5
# Source pages are A4: 595 x 842. Side-by-side should be significantly wider.
MIN_EXPECTED_WIDTH = 1000  # generous threshold — actual golden is 1210


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source files must exist (gate, no points)
    if not os.path.exists(ORIGINAL_PATH) or not os.path.exists(REVISED_PATH):
        print(f"CRITICAL: Source PDF files not found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and is a valid PDF (0.15 pts)
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 — side_by_side.pdf does not exist at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(OUTPUT_PATH)
        if doc.page_count < 1:
            print(f"FAIL: Component 1 — PDF has no pages")
            doc.close()
            print("REWARD: 0.0")
            return 0.0

        if doc.page_count >= 1:
            print(f"PASS: Component 1 — side_by_side.pdf exists and is valid ({doc.page_count} pages) (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open side_by_side.pdf: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Page count is exactly 5 (0.25 pts)
    try:
        if doc.page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {doc.page_count} (expected {EXPECTED_PAGE_COUNT}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Page count is {doc.page_count}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages are wider than source pages (double-width layout) (0.25 pts)
    try:
        # Get source page width for reference
        orig_doc = pymupdf.open(ORIGINAL_PATH)
        source_width = orig_doc[0].rect.width
        orig_doc.close()

        wide_pages = 0
        pages_to_check = min(doc.page_count, EXPECTED_PAGE_COUNT)
        for i in range(pages_to_check):
            page = doc[i]
            page_width = page.rect.width
            if page_width >= MIN_EXPECTED_WIDTH:
                wide_pages += 1
            else:
                print(f"  Page {i}: width={page_width:.1f}, below minimum {MIN_EXPECTED_WIDTH}")

        if wide_pages == pages_to_check and pages_to_check > 0:
            print(f"PASS: Component 3 — All {pages_to_check} pages are wide ({doc[0].rect.width:.1f} pts, source was {source_width:.1f} pts) (0.25 pts)")
            total_score += 0.25
        elif wide_pages > 0:
            partial = 0.25 * (wide_pages / pages_to_check)
            print(f"PARTIAL: Component 3 — {wide_pages}/{pages_to_check} pages are wide enough ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages are wider than {MIN_EXPECTED_WIDTH} pts")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Each page contains content from both original and revised PDFs (0.35 pts)
    try:
        orig_doc = pymupdf.open(ORIGINAL_PATH)
        rev_doc = pymupdf.open(REVISED_PATH)

        pages_with_both = 0
        pages_to_check = min(doc.page_count, EXPECTED_PAGE_COUNT)

        for i in range(pages_to_check):
            sbs_text = doc[i].get_text("text")

            # Get distinctive text from each source page
            orig_text_snippet = orig_doc[i].get_text("text")[:200].strip()
            rev_text_snippet = rev_doc[i].get_text("text")[:200].strip()

            # Check for presence of identifiers from both sources
            # The source files are labeled "ORIGINAL" and "REVISED"
            has_original = "ORIGINAL" in sbs_text
            has_revised = "REVISED" in sbs_text

            # Also check for actual text overlap with source pages
            # Extract a few distinctive words from each source
            orig_words = set(w for w in orig_text_snippet.split() if len(w) > 5)
            rev_words = set(w for w in rev_text_snippet.split() if len(w) > 5)

            orig_match = sum(1 for w in list(orig_words)[:10] if w in sbs_text)
            rev_match = sum(1 for w in list(rev_words)[:10] if w in sbs_text)

            has_orig_content = has_original or orig_match >= 3
            has_rev_content = has_revised or rev_match >= 3

            if has_orig_content and has_rev_content:
                pages_with_both += 1
            else:
                print(f"  Page {i}: orig_content={has_orig_content}, rev_content={has_rev_content}")

        orig_doc.close()
        rev_doc.close()

        if pages_with_both == pages_to_check and pages_to_check > 0:
            print(f"PASS: Component 4 — All {pages_to_check} pages contain content from both original and revised PDFs (0.35 pts)")
            total_score += 0.35
        elif pages_with_both > 0:
            partial = 0.35 * (pages_with_both / pages_to_check)
            print(f"PARTIAL: Component 4 — {pages_with_both}/{pages_to_check} pages have content from both sources ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages contain content from both source PDFs")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
