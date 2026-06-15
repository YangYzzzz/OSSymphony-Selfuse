"""
Reward Script: Merge three thesis chapter PDFs into one
Task ID: pdf_res_006
Domain: pdf
Scoring:
  Component 1 (0.2): chapter3_complete.pdf exists
  Component 2 (0.3): Merged PDF has exactly 15 pages (4+6+5)
  Component 3 (0.25): Intro pages appear first (pages 0-3 match chapter3_intro.pdf)
  Component 4 (0.25): Methods then Results pages follow in order (pages 4-14)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_006'

MERGED_PATH = f'{WORKDIR}/thesis/chapter3_complete.pdf'
INTRO_PATH = f'{WORKDIR}/thesis/chapter3_intro.pdf'
METHODS_PATH = f'{WORKDIR}/thesis/chapter3_methods.pdf'
RESULTS_PATH = f'{WORKDIR}/thesis/chapter3_results.pdf'


def get_page_text_signature(doc, page_idx):
    """Get first 120 chars of text from a page as a signature for comparison."""
    try:
        page = doc[page_idx]
        text = page.get_text().strip()[:120]
        return text
    except Exception:
        return ""


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Merged PDF file exists (0.2 points)
    # This FAILS on initial_env (file not created yet), PASSES on golden_env
    try:
        if os.path.exists(MERGED_PATH):
            print(f"PASS: Component 1 -- chapter3_complete.pdf exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- chapter3_complete.pdf not found at {MERGED_PATH}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load merged document
    try:
        merged_doc = fitz.open(MERGED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open {MERGED_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page count is exactly 15 (4 intro + 6 methods + 5 results) (0.3 points)
    try:
        page_count = len(merged_doc)
        if page_count == 15:
            print(f"PASS: Component 2 -- Merged PDF has exactly 15 pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Expected 15 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Load source documents for content comparison
    try:
        intro_doc = fitz.open(INTRO_PATH)
        methods_doc = fitz.open(METHODS_PATH)
        results_doc = fitz.open(RESULTS_PATH)
    except Exception as e:
        print(f"ERROR: Cannot load source PDFs for comparison: {e}")
        merged_doc.close()
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Intro pages appear first (pages 0-3 match chapter3_intro.pdf) (0.25 points)
    # This verifies correct ordering -- intro must be first
    try:
        intro_matches = 0
        intro_total = len(intro_doc)  # expected 4
        for i in range(min(intro_total, len(merged_doc))):
            merged_sig = get_page_text_signature(merged_doc, i)
            intro_sig = get_page_text_signature(intro_doc, i)
            if merged_sig and intro_sig and merged_sig == intro_sig:
                intro_matches += 1

        if intro_matches == intro_total and intro_total > 0:
            print(f"PASS: Component 3 -- All {intro_total} intro pages match in correct position (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Intro page matches: {intro_matches}/{intro_total}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Methods then Results pages follow intro in correct order (0.25 points)
    # Pages 4-9 should match methods, pages 10-14 should match results
    try:
        methods_matches = 0
        methods_total = len(methods_doc)  # expected 6
        methods_offset = len(intro_doc)  # expected 4
        for i in range(min(methods_total, len(merged_doc) - methods_offset)):
            merged_sig = get_page_text_signature(merged_doc, methods_offset + i)
            methods_sig = get_page_text_signature(methods_doc, i)
            if merged_sig and methods_sig and merged_sig == methods_sig:
                methods_matches += 1

        results_matches = 0
        results_total = len(results_doc)  # expected 5
        results_offset = len(intro_doc) + len(methods_doc)  # expected 10
        for i in range(min(results_total, len(merged_doc) - results_offset)):
            merged_sig = get_page_text_signature(merged_doc, results_offset + i)
            results_sig = get_page_text_signature(results_doc, i)
            if merged_sig and results_sig and merged_sig == results_sig:
                results_matches += 1

        all_methods_ok = (methods_matches == methods_total and methods_total > 0)
        all_results_ok = (results_matches == results_total and results_total > 0)

        if all_methods_ok and all_results_ok:
            print(f"PASS: Component 4 -- Methods ({methods_matches}/{methods_total}) and Results ({results_matches}/{results_total}) pages in correct order (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- Methods matches: {methods_matches}/{methods_total}, Results matches: {results_matches}/{results_total}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Cleanup
    merged_doc.close()
    intro_doc.close()
    methods_doc.close()
    results_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(MERGED_PATH):
    print(f"File not found: {MERGED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
