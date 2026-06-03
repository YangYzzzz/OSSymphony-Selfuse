"""
Reward Script: Merge PDFs - Insert appendix after page 5 of main document
Task ID: pdf_gf1_023
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid PDF with readable pages
  Component 2 (0.15): Total page count is exactly 14
  Component 3 (0.30): Pages 1-5 of output match pages 1-5 of main_document.pdf
  Component 4 (0.25): Pages 6-9 of output match pages 1-4 of appendix.pdf
  Component 5 (0.15): Pages 10-14 of output match pages 6-10 of main_document.pdf
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_023'

OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'document_with_appendix.pdf')
MAIN_PATH = os.path.join(WORKDIR, 'Documents', 'main_document.pdf')
APPENDIX_PATH = os.path.join(WORKDIR, 'Documents', 'appendix.pdf')


def get_page_text(doc, page_idx):
    """Extract text from a page for comparison."""
    try:
        return doc[page_idx].get_text().strip()
    except Exception:
        return None


def pages_match(doc_a, idx_a, doc_b, idx_b):
    """Compare two pages by text content. Returns True if they match."""
    text_a = get_page_text(doc_a, idx_a)
    text_b = get_page_text(doc_b, idx_b)
    if text_a is None or text_b is None:
        return False
    return text_a == text_b


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source files must exist (not scored — they are pre-existing)
    if not os.path.exists(MAIN_PATH):
        print(f"CRITICAL: Source file not found: {MAIN_PATH}")
        print("REWARD: 0.0")
        return 0.0
    if not os.path.exists(APPENDIX_PATH):
        print(f"CRITICAL: Source file not found: {APPENDIX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and is a valid PDF (0.15 points)
    # This is a task-introduced change: the file does not exist in initial_env
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 — Output file does not exist: {OUTPUT_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        import fitz
        merged = fitz.open(OUTPUT_PATH)
        page_count = len(merged)
        if page_count > 0 and merged[0].get_text() is not None:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
            merged.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open output PDF: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load source documents for comparison
    try:
        main_doc = fitz.open(MAIN_PATH)
        appendix_doc = fitz.open(APPENDIX_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open source PDFs: {e}")
        merged.close()
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Total page count is exactly 14 (0.15 points)
    try:
        if page_count == 14:
            print(f"PASS: Component 2 — Page count is 14 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 14 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages 1-5 of output match pages 1-5 of main_document (0.30 points)
    # These pages should be the first 5 pages of the original main document
    try:
        matching = 0
        for i in range(5):
            if i < page_count and i < len(main_doc):
                if pages_match(merged, i, main_doc, i):
                    matching += 1
                else:
                    print(f"  MISMATCH: Output page {i+1} does not match main_document page {i+1}")
            else:
                print(f"  MISSING: Cannot compare page {i+1} (out of range)")

        if matching == 5:
            print(f"PASS: Component 3 — All 5 pages (1-5) match main_document pages 1-5 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Only {matching}/5 pages match main_document pages 1-5")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages 6-9 of output match pages 1-4 of appendix (0.25 points)
    # These are the appendix pages inserted after page 5
    try:
        matching = 0
        for i in range(4):
            merged_idx = 5 + i  # pages 6-9 (0-indexed: 5-8)
            appendix_idx = i    # pages 1-4 of appendix (0-indexed: 0-3)
            if merged_idx < page_count and appendix_idx < len(appendix_doc):
                if pages_match(merged, merged_idx, appendix_doc, appendix_idx):
                    matching += 1
                else:
                    print(f"  MISMATCH: Output page {merged_idx+1} does not match appendix page {appendix_idx+1}")
            else:
                print(f"  MISSING: Cannot compare output page {merged_idx+1} with appendix page {appendix_idx+1}")

        if matching == 4:
            print(f"PASS: Component 4 — All 4 pages (6-9) match appendix pages 1-4 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Only {matching}/4 pages match appendix pages 1-4")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Pages 10-14 of output match pages 6-10 of main_document (0.15 points)
    # These are the remaining pages of the main document after the insertion point
    try:
        matching = 0
        for i in range(5):
            merged_idx = 9 + i  # pages 10-14 (0-indexed: 9-13)
            main_idx = 5 + i    # pages 6-10 of main (0-indexed: 5-9)
            if merged_idx < page_count and main_idx < len(main_doc):
                if pages_match(merged, merged_idx, main_doc, main_idx):
                    matching += 1
                else:
                    print(f"  MISMATCH: Output page {merged_idx+1} does not match main_document page {main_idx+1}")
            else:
                print(f"  MISSING: Cannot compare output page {merged_idx+1} with main_document page {main_idx+1}")

        if matching == 5:
            print(f"PASS: Component 5 — All 5 pages (10-14) match main_document pages 6-10 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Only {matching}/5 pages match main_document pages 6-10")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Clean up
    merged.close()
    main_doc.close()
    appendix_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
