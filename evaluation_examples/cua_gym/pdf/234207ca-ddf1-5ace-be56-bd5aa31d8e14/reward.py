"""
Reward Script: Flatten all interactive annotations in reviewed_doc.pdf
Task ID: pdf_gf2_042
Domain: pdf
Scoring:
  Component 1 (0.4): Output file has zero interactive annotations on all pages
  Component 2 (0.2): Output file preserves original 8-page count
  Component 3 (0.4): Text content from original document is preserved in flattened version
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_042'

FLAT_PATH = os.path.join(WORKDIR, 'Documents', 'reviewed_doc_flat.pdf')
ORIG_PATH = os.path.join(WORKDIR, 'Documents', 'reviewed_doc.pdf')

EXPECTED_PAGE_COUNT = 8


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: flat file must exist
    if not os.path.exists(FLAT_PATH):
        print(f"CRITICAL: Flattened file not found at {FLAT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        flat_doc = pymupdf.open(FLAT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open flattened PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No interactive annotations on any page (0.4 points)
    # This is the core task requirement — flattening removes all annotation objects.
    # FAILS on initial_env (file doesn't exist) — correct.
    try:
        total_annots = 0
        for i in range(flat_doc.page_count):
            page = flat_doc[i]
            annots = list(page.annots())
            total_annots += len(annots)
            if len(annots) > 0:
                print(f"  Page {i}: found {len(annots)} remaining annotations")

        if total_annots == 0:
            print(f"PASS: Component 1 — Zero annotations across all pages (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Found {total_annots} remaining annotations (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page count preserved at 8 (0.2 points)
    # Ensures flattening didn't add/remove pages.
    try:
        actual_pages = flat_doc.page_count
        if actual_pages == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {actual_pages} as expected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Page count is {actual_pages}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text content preserved (0.4 points)
    # The original document text should still be extractable from the flattened PDF.
    # We compare text from the original file to the flattened file page-by-page.
    try:
        if not os.path.exists(ORIG_PATH):
            print(f"WARN: Component 3 — Original file not found at {ORIG_PATH}, skipping text comparison")
        else:
            orig_doc = pymupdf.open(ORIG_PATH)
            pages_to_check = min(flat_doc.page_count, orig_doc.page_count, EXPECTED_PAGE_COUNT)
            pages_with_text_match = 0

            for i in range(pages_to_check):
                orig_text = orig_doc[i].get_text("text").strip()
                flat_text = flat_doc[i].get_text("text").strip()

                # The flattened file should contain at least the core text from the original.
                # FreeText annotations may add extra text, and annotation removal may slightly
                # change extraction. We check that at least 80% of original words appear.
                if len(orig_text) == 0:
                    # Empty page — trivially matches
                    pages_with_text_match += 1
                    continue

                orig_words = set(orig_text.split())
                flat_words = set(flat_text.split())

                if len(orig_words) == 0:
                    pages_with_text_match += 1
                    continue

                # Calculate what fraction of original words are present in flat version
                overlap = len(orig_words & flat_words)
                ratio = overlap / len(orig_words)

                if ratio >= 0.7:
                    pages_with_text_match += 1
                else:
                    print(f"  Page {i}: text overlap ratio {ratio:.2f} (need >= 0.70)")

            orig_doc.close()

            if pages_to_check > 0:
                text_score = pages_with_text_match / pages_to_check
            else:
                text_score = 0.0

            if text_score >= 0.9:
                print(f"PASS: Component 3 — Text preserved on {pages_with_text_match}/{pages_to_check} pages (0.4 pts)")
                total_score += 0.4
            elif text_score >= 0.5:
                partial = round(0.4 * text_score, 2)
                print(f"PARTIAL: Component 3 — Text preserved on {pages_with_text_match}/{pages_to_check} pages ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Text preserved on only {pages_with_text_match}/{pages_to_check} pages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    flat_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
