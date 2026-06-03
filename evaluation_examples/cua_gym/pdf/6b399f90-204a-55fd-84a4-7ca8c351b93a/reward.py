"""
Reward Script: Remove DRAFT watermark from every page of a 16-page legal contract.
Task ID: pdf_legal_073
Domain: pdf
Scoring:
  - Component 1 (0.20): Clean PDF exists with correct page count (16 pages)
  - Component 2 (0.50): DRAFT watermark text removed from all pages
  - Component 3 (0.30): Original contract content preserved
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_073'

CLEAN_PATH = os.path.join(WORKDIR, 'legal', 'final_contract_clean.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'legal', 'final_contract.pdf')
EXPECTED_PAGES = 16


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: clean file must exist
    if not os.path.exists(CLEAN_PATH):
        print(f"CRITICAL: Clean file not found at {CLEAN_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Neither fitz nor pymupdf available")
            print("REWARD: 0.0")
            return 0.0

    try:
        clean_doc = fitz.open(CLEAN_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open clean PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Clean PDF has correct page count (0.20 points)
    # This verifies the output file is structurally valid with the expected 16 pages.
    # Fails on initial_env because the clean file does not exist there (gate above).
    try:
        page_count = len(clean_doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Clean PDF has {page_count} pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: DRAFT watermark removed from ALL pages (0.50 points)
    # Award partial credit proportional to pages cleaned.
    # On initial_env this fails because clean file doesn't exist (gate above).
    try:
        pages_clean = 0
        pages_with_draft = []
        for i in range(len(clean_doc)):
            page = clean_doc[i]
            text = page.get_text()
            # Check both via text extraction and search
            search_results = page.search_for('DRAFT')
            text_has_draft = 'DRAFT' in text
            if len(search_results) == 0 and not text_has_draft:
                pages_clean += 1
            else:
                pages_with_draft.append(i)

        if pages_clean == EXPECTED_PAGES:
            print(f"PASS: Component 2 -- DRAFT removed from all {EXPECTED_PAGES} pages (0.50 pts)")
            total_score += 0.50
        elif pages_clean > 0:
            # Partial credit: proportional to pages cleaned
            partial = 0.50 * (pages_clean / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 -- DRAFT removed from {pages_clean}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            print(f"  Pages still with DRAFT: {pages_with_draft}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- DRAFT still present on all pages")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Original contract content preserved (0.30 points)
    # Verify that the non-watermark content from the original is still present in the clean file.
    # On initial_env this fails because clean file doesn't exist (gate above).
    try:
        if not os.path.exists(ORIGINAL_PATH):
            print(f"WARN: Component 3 -- Original file not found at {ORIGINAL_PATH}, skipping content check")
        else:
            orig_doc = fitz.open(ORIGINAL_PATH)
            # Sample pages to compare content (check pages 0, 4, 8, 12, 15)
            sample_pages = [0, 4, 8, 12, min(15, len(orig_doc) - 1)]
            pages_preserved = 0
            total_checked = 0

            for page_idx in sample_pages:
                if page_idx >= len(orig_doc) or page_idx >= len(clean_doc):
                    continue
                total_checked += 1

                orig_text = orig_doc[page_idx].get_text()
                clean_text = clean_doc[page_idx].get_text()

                # Remove DRAFT from original text for comparison
                orig_text_no_draft = orig_text.replace('DRAFT', '').strip()
                clean_text_stripped = clean_text.strip()

                # Get meaningful words (skip very short tokens)
                orig_words = [w for w in orig_text_no_draft.split() if len(w) > 2]
                clean_words_set = set(clean_text_stripped.split())

                if len(orig_words) == 0:
                    # Empty page, trivially preserved
                    pages_preserved += 1
                    continue

                # Check that at least 80% of original words appear in clean
                matched = sum(1 for w in orig_words if w in clean_words_set)
                ratio = matched / len(orig_words)
                if ratio >= 0.80:
                    pages_preserved += 1
                else:
                    print(f"  Page {page_idx}: content match ratio = {ratio:.2%} (below 80%)")

            orig_doc.close()

            if total_checked > 0 and pages_preserved == total_checked:
                print(f"PASS: Component 3 -- Content preserved across {total_checked} sampled pages (0.30 pts)")
                total_score += 0.30
            elif total_checked > 0 and pages_preserved > 0:
                partial = 0.30 * (pages_preserved / total_checked)
                print(f"PARTIAL: Component 3 -- Content preserved on {pages_preserved}/{total_checked} sampled pages ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Content not preserved (0/{total_checked} sampled pages)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    clean_doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
