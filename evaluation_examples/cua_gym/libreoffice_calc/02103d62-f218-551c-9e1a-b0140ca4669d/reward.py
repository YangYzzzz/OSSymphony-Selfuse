"""
Reward Script: Redact dollar amounts on pages 1-3 of invoice_bundle.pdf
Task ID: pdf_adv_014
Domain: pdf
Scoring:
  Component 1 (0.15): Redacted file exists at /home/user/finance/invoice_bundle_redacted.pdf
  Component 2 (0.15): Redacted file has 10 pages (same page count as original)
  Component 3 (0.30): No dollar amounts remain on pages 1-3
  Component 4 (0.25): Pages 1-3 contain [AMOUNT REDACTED] replacement text
  Component 5 (0.15): Pages 4-10 text is unchanged compared to original
"""

import os
import re
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_014'

ORIGINAL_PATH = os.path.join(WORKDIR, 'finance', 'invoice_bundle.pdf')
REDACTED_PATH = os.path.join(WORKDIR, 'finance', 'invoice_bundle_redacted.pdf')

DOLLAR_PATTERN = r'\$[\d,]+\.\d{2}'


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

    # Component 1: Redacted file exists (0.15 points)
    # This is a task-introduced change: the file does not exist before the task.
    try:
        if os.path.exists(REDACTED_PATH):
            print(f"PASS: Component 1 — Redacted file exists at {REDACTED_PATH} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Redacted file not found at {REDACTED_PATH}")
            # If no redacted file, nothing more to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load both documents
    try:
        orig_doc = pymupdf.open(ORIGINAL_PATH)
        redc_doc = pymupdf.open(REDACTED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF files: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page count matches original (0.15 points)
    try:
        orig_pages = orig_doc.page_count
        redc_pages = redc_doc.page_count
        if redc_pages == orig_pages and redc_pages == 10:
            print(f"PASS: Component 2 — Redacted file has {redc_pages} pages matching original (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected {orig_pages} pages, redacted has {redc_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No dollar amounts on pages 1-3 (0.30 points)
    # Progressive: 0.10 per page with no remaining dollar amounts
    try:
        pages_clean = 0
        for page_idx in range(3):
            if page_idx >= redc_doc.page_count:
                print(f"FAIL: Component 3 — Page {page_idx + 1} does not exist in redacted file")
                continue
            text = redc_doc[page_idx].get_text("text")
            amounts_found = re.findall(DOLLAR_PATTERN, text)
            if len(amounts_found) == 0:
                pages_clean += 1
                print(f"PASS: Component 3.{page_idx + 1} — Page {page_idx + 1} has no dollar amounts")
            else:
                print(f"FAIL: Component 3.{page_idx + 1} — Page {page_idx + 1} still has {len(amounts_found)} dollar amounts: {amounts_found[:3]}")

        comp3_score = (pages_clean / 3.0) * 0.30
        if comp3_score > 0:
            print(f"PASS: Component 3 — {pages_clean}/3 pages clean ({comp3_score:.2f} pts)")
        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages 1-3 contain [AMOUNT REDACTED] markers (0.25 points)
    # Each page must have at least one marker. Progressive scoring.
    try:
        pages_with_markers = 0
        total_markers = 0
        for page_idx in range(3):
            if page_idx >= redc_doc.page_count:
                continue
            text = redc_doc[page_idx].get_text("text")
            marker_count = text.count("[AMOUNT REDACTED]")
            total_markers += marker_count
            if marker_count > 0:
                pages_with_markers += 1
                print(f"PASS: Component 4.{page_idx + 1} — Page {page_idx + 1} has {marker_count} redaction markers")
            else:
                print(f"FAIL: Component 4.{page_idx + 1} — Page {page_idx + 1} has no [AMOUNT REDACTED] markers")

        comp4_score = (pages_with_markers / 3.0) * 0.25
        if comp4_score > 0:
            print(f"PASS: Component 4 — {pages_with_markers}/3 pages have markers, total {total_markers} ({comp4_score:.2f} pts)")
        total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Pages 4-10 unchanged (0.15 points)
    # Compare text content of pages 4-10 between original and redacted
    try:
        pages_unchanged = 0
        pages_to_check = min(orig_doc.page_count, redc_doc.page_count) - 3
        if pages_to_check <= 0:
            print(f"FAIL: Component 5 — Not enough pages to compare (4-10)")
        else:
            for page_idx in range(3, min(orig_doc.page_count, redc_doc.page_count)):
                orig_text = orig_doc[page_idx].get_text("text")
                redc_text = redc_doc[page_idx].get_text("text")
                if orig_text == redc_text:
                    pages_unchanged += 1
                else:
                    print(f"FAIL: Component 5 — Page {page_idx + 1} text differs from original")

            if pages_unchanged == pages_to_check:
                print(f"PASS: Component 5 — All {pages_unchanged} pages (4-10) unchanged (0.15 pts)")
                total_score += 0.15
            elif pages_unchanged > 0:
                partial = (pages_unchanged / pages_to_check) * 0.15
                print(f"PARTIAL: Component 5 — {pages_unchanged}/{pages_to_check} pages unchanged ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    orig_doc.close()
    redc_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
