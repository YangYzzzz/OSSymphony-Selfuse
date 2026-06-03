"""
Reward Script: Remove all annotations from reviewed_draft.pdf and save clean version
Task ID: pdf_gf1_026
Domain: pdf
Scoring:
  Component 1 (0.15): Clean PDF file exists
  Component 2 (0.15): Clean PDF has correct page count (6 pages)
  Component 3 (0.40): All annotations removed (0 annotations across all pages)
  Component 4 (0.30): Text content preserved (matches original on every page)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_026'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    clean_path = f'{WORKDIR}/Documents/reviewed_draft_clean.pdf'
    orig_path = f'{WORKDIR}/Documents/reviewed_draft.pdf'

    # Component 1: Clean PDF file exists (0.15 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env
    try:
        if os.path.exists(clean_path):
            import fitz
            doc = fitz.open(clean_path)
            if len(doc) > 0:
                print(f"PASS: Component 1 — Clean PDF exists at {clean_path} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Clean PDF exists but has 0 pages")
            doc.close()
        else:
            print(f"FAIL: Component 1 — Clean PDF not found at {clean_path}")
            # Early exit: no point checking further if file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Clean PDF has correct page count — 6 pages (0.15 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        import fitz
        doc = fitz.open(clean_path)
        page_count = len(doc)
        doc.close()
        if page_count == 6:
            print(f"PASS: Component 2 — Clean PDF has 6 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 6 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All annotations removed — 0 annotations total (0.40 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        import fitz
        doc = fitz.open(clean_path)
        total_annots = 0
        page_annot_details = []
        for i, page in enumerate(doc):
            annots = list(page.annots())
            count = len(annots)
            total_annots += count
            if count > 0:
                page_annot_details.append(f"page {i}: {count}")
        doc.close()

        if total_annots == 0:
            print(f"PASS: Component 3 — Zero annotations across all 6 pages (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 3 — Found {total_annots} annotations remaining: {', '.join(page_annot_details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text content preserved across all pages (0.30 points)
    # Compares text from the clean file to the original to ensure no content loss
    # This FAILS on initial_env (clean file doesn't exist) and PASSES on golden_env
    try:
        import fitz
        doc_clean = fitz.open(clean_path)
        doc_orig = fitz.open(orig_path)

        if len(doc_orig) == 0:
            print(f"FAIL: Component 4 — Original PDF has 0 pages, cannot compare")
        else:
            pages_to_check = min(len(doc_clean), len(doc_orig))
            pages_matching = 0
            for i in range(pages_to_check):
                orig_text = doc_orig[i].get_text().strip()
                clean_text = doc_clean[i].get_text().strip()
                if orig_text == clean_text:
                    pages_matching += 1
                else:
                    print(f"  Page {i}: text mismatch — orig len {len(orig_text)}, clean len {len(clean_text)}")

            doc_clean.close()
            doc_orig.close()

            if pages_matching == pages_to_check and pages_to_check == 6:
                print(f"PASS: Component 4 — Text content matches on all {pages_matching} pages (0.30 pts)")
                total_score += 0.30
            elif pages_matching == pages_to_check and pages_to_check > 0:
                # Partial: correct text but wrong page count
                partial = 0.30 * (pages_matching / 6.0)
                print(f"PARTIAL: Component 4 — Text matches on {pages_matching}/{pages_to_check} pages ({partial:.2f} pts)")
                total_score += partial
            else:
                partial = 0.30 * (pages_matching / 6.0)
                print(f"PARTIAL: Component 4 — Text matches on {pages_matching}/{pages_to_check} pages ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
