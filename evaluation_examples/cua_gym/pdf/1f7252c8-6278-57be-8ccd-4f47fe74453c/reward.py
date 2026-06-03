"""
Reward Script: Optimize large_report.pdf to reduce file size
Task ID: pdf_gf1_019
Domain: pdf
Scoring:
  Component 1 (0.25): Optimized file is a valid PDF with 20 pages
  Component 2 (0.30): Optimized file size is strictly less than original
  Component 3 (0.25): Text content preserved across sampled pages
  Component 4 (0.20): Non-essential metadata removed/reduced
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_019'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'large_report.pdf')
OPTIMIZED_PATH = os.path.join(WORKDIR, 'Documents', 'large_report_optimized.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: optimized file must exist (gate, not scored alone)
    if not os.path.exists(OPTIMIZED_PATH):
        print(f"CRITICAL: Optimized file not found: {OPTIMIZED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    import pymupdf

    # Component 1: Optimized file is a valid PDF with 20 pages (0.25 points)
    try:
        doc_opt = pymupdf.open(OPTIMIZED_PATH)
        opt_page_count = doc_opt.page_count
        doc_opt.close()

        if opt_page_count == 20:
            print(f"PASS: Component 1 — Valid PDF with {opt_page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 20 pages, found {opt_page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open optimized PDF: {e}")

    # Component 2: File size strictly less than original (0.30 points)
    try:
        orig_size = os.path.getsize(ORIGINAL_PATH)
        opt_size = os.path.getsize(OPTIMIZED_PATH)
        if opt_size < orig_size:
            reduction_pct = (1 - opt_size / orig_size) * 100
            print(f"PASS: Component 2 — Optimized size {opt_size} < original {orig_size} "
                  f"({reduction_pct:.1f}% reduction) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Optimized size {opt_size} >= original {orig_size}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text content preserved across sampled pages (0.25 points)
    try:
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        doc_opt = pymupdf.open(OPTIMIZED_PATH)

        # Sample pages 0, 4, 9, 14, 19 (first, ~quarter, middle, ~3/4, last)
        sample_pages = [0, 4, 9, 14, 19]
        pages_match = 0
        pages_checked = 0

        for p in sample_pages:
            if p < doc_orig.page_count and p < doc_opt.page_count:
                orig_text = doc_orig[p].get_text("text").strip()
                opt_text = doc_opt[p].get_text("text").strip()
                pages_checked += 1
                if orig_text == opt_text:
                    pages_match += 1
                else:
                    # Try normalized comparison (whitespace differences acceptable)
                    import re
                    orig_norm = re.sub(r'\s+', ' ', orig_text)
                    opt_norm = re.sub(r'\s+', ' ', opt_text)
                    if orig_norm == opt_norm:
                        pages_match += 1
                    else:
                        print(f"  Page {p}: text mismatch (orig len={len(orig_text)}, opt len={len(opt_text)})")

        doc_orig.close()
        doc_opt.close()

        if pages_checked > 0 and pages_match == pages_checked:
            print(f"PASS: Component 3 — All {pages_checked} sampled pages have matching text (0.25 pts)")
            total_score += 0.25
        elif pages_checked > 0 and pages_match >= pages_checked * 0.8:
            partial = 0.15
            print(f"PARTIAL: Component 3 — {pages_match}/{pages_checked} pages match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {pages_match}/{pages_checked} pages match")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Non-essential metadata removed/reduced (0.20 points)
    try:
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        doc_opt = pymupdf.open(OPTIMIZED_PATH)

        orig_meta = doc_orig.metadata
        opt_meta = doc_opt.metadata

        doc_orig.close()
        doc_opt.close()

        # Check that non-essential metadata fields are reduced/removed
        # Non-essential: subject, keywords, creator, producer
        non_essential_keys = ['subject', 'keywords', 'creator', 'producer']
        removed_count = 0
        total_non_essential = 0

        for key in non_essential_keys:
            orig_val = (orig_meta.get(key, '') or '').strip()
            opt_val = (opt_meta.get(key, '') or '').strip()
            if orig_val:  # Only count if original had content
                total_non_essential += 1
                if not opt_val or len(opt_val) < len(orig_val):
                    removed_count += 1

        if total_non_essential > 0 and removed_count >= total_non_essential * 0.5:
            print(f"PASS: Component 4 — {removed_count}/{total_non_essential} non-essential "
                  f"metadata fields removed/reduced (0.20 pts)")
            total_score += 0.20
        elif total_non_essential == 0:
            # Original had no non-essential metadata to remove; skip this check
            # but don't penalize — give partial credit if file is otherwise optimized
            print(f"INFO: Component 4 — Original had no non-essential metadata; awarding 0.10 pts")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Only {removed_count}/{total_non_essential} "
                  f"non-essential metadata fields removed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OPTIMIZED_PATH):
    print(f"File not found: {OPTIMIZED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
