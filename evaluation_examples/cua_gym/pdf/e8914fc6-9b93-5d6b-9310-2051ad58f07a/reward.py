"""
Reward Script: Add 'DRAFT - DO NOT DISTRIBUTE' watermark to every page of a PDF
Task ID: pdf_res_026
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists and is a valid PDF with 14 pages
  Component 2 (0.5): All 14 pages contain the exact watermark text 'DRAFT - DO NOT DISTRIBUTE'
  Component 3 (0.3): Watermark text is present on every page (completeness ratio)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_026'

OUTPUT_PATH = f'{WORKDIR}/papers/working_paper_draft.pdf'
ORIGINAL_PATH = f'{WORKDIR}/papers/working_paper.pdf'
WATERMARK_TEXT = 'DRAFT - DO NOT DISTRIBUTE'
EXPECTED_PAGES = 14


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid PDF
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Output file is a valid PDF with correct page count (0.2 points)
    # Initial env does NOT have working_paper_draft.pdf, so this only passes on golden
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Output PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages contain the exact watermark text (0.5 points)
    # This is the core task requirement - watermark on EVERY page
    try:
        pages_with_watermark = 0
        pages_missing = []
        for i in range(page_count):
            page = doc[i]
            text = page.get_text()
            if WATERMARK_TEXT in text:
                pages_with_watermark += 1
            else:
                pages_missing.append(i)

        if pages_with_watermark == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 — All {page_count} pages have watermark text (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — {pages_with_watermark}/{page_count} pages have watermark")
            if pages_missing:
                print(f"  Missing on pages: {pages_missing[:10]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Watermark coverage ratio (0.3 points, progressive)
    # Awards partial credit based on fraction of pages with watermark
    try:
        if page_count > 0 and pages_with_watermark > 0:
            ratio = pages_with_watermark / EXPECTED_PAGES
            component_score = round(0.3 * ratio, 2)
            if ratio >= 1.0:
                print(f"PASS: Component 3 — Watermark coverage {pages_with_watermark}/{EXPECTED_PAGES} = 100% (0.3 pts)")
                total_score += 0.3
            else:
                print(f"PARTIAL: Component 3 — Watermark coverage {pages_with_watermark}/{EXPECTED_PAGES} = {ratio*100:.0f}% ({component_score} pts)")
                total_score += component_score
        else:
            print(f"FAIL: Component 3 — No pages with watermark found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
