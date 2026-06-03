"""
Reward Script: Add reviewer annotation to every page of a PDF
Task ID: pdf_res_073
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.1 pts)
  Component 2: PDF has correct page count of 12 (0.15 pts)
  Component 3: All 12 pages contain the reviewer label text (0.45 pts, progressive)
  Component 4: Label text positioned in top margin (y < 50) on all pages (0.15 pts)
  Component 5: Label text is small font and gray color on all pages (0.15 pts)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_073'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'draft_feedback_labeled.pdf')
EXPECTED_LABEL = 'Reviewer: Dr. Smith | Round 2 | Confidential'
EXPECTED_PAGES = 12


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.1 pts)
    # This checks for the NEW file created by the task, not the source file.
    try:
        if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
            print("PASS: Component 1 -- Output file exists: %s (0.1 pts)" % OUTPUT_FILE)
            total_score += 0.1
        else:
            print("FAIL: Component 1 -- Output file not found or empty: %s" % OUTPUT_FILE)
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print("CRITICAL: Cannot load PDF %s: %s" % (OUTPUT_FILE, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Correct page count (0.15 pts)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print("PASS: Component 2 -- Page count is %d (0.15 pts)" % page_count)
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- Expected %d pages, found %d" % (EXPECTED_PAGES, page_count))
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: All pages contain the reviewer label text (0.45 pts, progressive)
    # Each page contributes 0.45/12 = 0.0375 points
    try:
        pages_with_label = 0
        per_page_score = 0.45 / EXPECTED_PAGES
        for i in range(min(len(doc), EXPECTED_PAGES)):
            page = doc[i]
            text = page.get_text()
            if 'Reviewer: Dr. Smith' in text and 'Round 2' in text and 'Confidential' in text:
                pages_with_label += 1
                total_score += per_page_score
            else:
                print("FAIL: Component 3 -- Page %d missing label text" % i)

        if pages_with_label == EXPECTED_PAGES:
            print("PASS: Component 3 -- All %d pages contain reviewer label (0.45 pts)" % pages_with_label)
        elif pages_with_label > 0:
            earned = round(pages_with_label * per_page_score, 4)
            print("PARTIAL: Component 3 -- %d/%d pages have label (%.4f pts)" % (pages_with_label, EXPECTED_PAGES, earned))
        else:
            print("FAIL: Component 3 -- No pages contain the reviewer label")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    # Component 4: Label text in top margin (y < 50) on all pages (0.15 pts)
    try:
        pages_top_margin = 0
        for i in range(min(len(doc), EXPECTED_PAGES)):
            page = doc[i]
            blocks = page.get_text('dict')['blocks']
            found_in_top = False
            for block in blocks:
                if block.get('type') == 0:  # text block
                    for line in block.get('lines', []):
                        for span in line.get('spans', []):
                            span_text = span.get('text', '')
                            if 'Reviewer' in span_text and 'Dr. Smith' in span_text:
                                bbox = span['bbox']
                                if bbox[1] < 50:  # y-coordinate in top margin
                                    found_in_top = True
            if found_in_top:
                pages_top_margin += 1

        if pages_top_margin == EXPECTED_PAGES:
            print("PASS: Component 4 -- Label in top margin on all %d pages (0.15 pts)" % pages_top_margin)
            total_score += 0.15
        elif pages_top_margin > 0:
            earned = round(0.15 * pages_top_margin / EXPECTED_PAGES, 4)
            total_score += earned
            print("PARTIAL: Component 4 -- Label in top margin on %d/%d pages (%.4f pts)" % (pages_top_margin, EXPECTED_PAGES, earned))
        else:
            print("FAIL: Component 4 -- Label not in top margin on any page")
    except Exception as e:
        print("ERROR: Component 4 -- %s" % e)

    # Component 5: Label text has small font (<=10pt) and gray color on all pages (0.15 pts)
    try:
        pages_correct_style = 0
        for i in range(min(len(doc), EXPECTED_PAGES)):
            page = doc[i]
            blocks = page.get_text('dict')['blocks']
            style_ok = False
            for block in blocks:
                if block.get('type') == 0:
                    for line in block.get('lines', []):
                        for span in line.get('spans', []):
                            span_text = span.get('text', '')
                            if 'Reviewer' in span_text and 'Dr. Smith' in span_text:
                                font_size = span.get('size', 0)
                                color_int = span.get('color', 0)
                                # Extract RGB components
                                r = (color_int >> 16) & 0xFF
                                g = (color_int >> 8) & 0xFF
                                b = color_int & 0xFF
                                # Small font: size <= 10
                                # Gray: r==g==b and value between 80 and 200 (not black, not white)
                                is_small = font_size <= 10
                                is_gray = (r == g == b) and (80 <= r <= 200)
                                if is_small and is_gray:
                                    style_ok = True
            if style_ok:
                pages_correct_style += 1

        if pages_correct_style == EXPECTED_PAGES:
            print("PASS: Component 5 -- Small gray text on all %d pages (0.15 pts)" % pages_correct_style)
            total_score += 0.15
        elif pages_correct_style > 0:
            earned = round(0.15 * pages_correct_style / EXPECTED_PAGES, 4)
            total_score += earned
            print("PARTIAL: Component 5 -- Small gray text on %d/%d pages (%.4f pts)" % (pages_correct_style, EXPECTED_PAGES, earned))
        else:
            print("FAIL: Component 5 -- Label text not small gray on any page")
    except Exception as e:
        print("ERROR: Component 5 -- %s" % e)

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Execute verification
verify_task()
