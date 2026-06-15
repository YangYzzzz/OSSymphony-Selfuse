"""
Reward Script: Add sequential Bates numbering to every page of a PDF
Task ID: pdf_pw_022
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and has 45 pages
  Component 2 (0.35): First, middle, and last pages have correct Bates numbers
  Component 3 (0.30): All 45 pages have correctly sequenced Bates numbers
  Component 4 (0.20): Bates numbers are positioned at bottom-right and use ~9pt monospace font
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_022'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'evidence_bundle_bates.pdf')
EXPECTED_PAGES = 45
BATES_PREFIX = 'CASE-2026-'


def verify_task():
    """
    Verify Bates numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Page count is {page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Key pages have correct Bates numbers (0.35 points)
    # Check page 1 (000001), a middle page (000023), and last page (000045)
    try:
        key_pages = [
            (0, 'CASE-2026-000001'),
            (22, 'CASE-2026-000023'),
            (44, 'CASE-2026-000045'),
        ]
        key_pass = 0
        for page_idx, expected_bates in key_pages:
            if page_idx >= doc.page_count:
                print(f"FAIL: Component 2 — Page {page_idx} does not exist")
                continue
            page = doc[page_idx]
            results = page.search_for(expected_bates)
            if len(results) > 0:
                key_pass += 1
                print(f"PASS: Component 2 — Page {page_idx}: found '{expected_bates}'")
            else:
                # Also check via text extraction
                text = page.get_text('text')
                if expected_bates in text:
                    key_pass += 1
                    print(f"PASS: Component 2 — Page {page_idx}: found '{expected_bates}' in text")
                else:
                    print(f"FAIL: Component 2 — Page {page_idx}: '{expected_bates}' not found")

        if key_pass == 3:
            total_score += 0.35
            print(f"PASS: Component 2 — All 3 key pages verified (0.35 pts)")
        elif key_pass > 0:
            partial = round(0.35 * key_pass / 3, 2)
            total_score += partial
            print(f"PARTIAL: Component 2 — {key_pass}/3 key pages verified ({partial} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 45 pages have correct sequential Bates numbers (0.30 points)
    try:
        correct_count = 0
        for i in range(min(EXPECTED_PAGES, doc.page_count)):
            expected_bates = f'CASE-2026-{i+1:06d}'
            page = doc[i]
            text = page.get_text('text')
            if expected_bates in text:
                correct_count += 1
            else:
                # Try search_for as fallback
                results = page.search_for(expected_bates)
                if len(results) > 0:
                    correct_count += 1
                else:
                    print(f"FAIL: Component 3 — Page {i}: '{expected_bates}' not found")

        if correct_count == EXPECTED_PAGES:
            total_score += 0.30
            print(f"PASS: Component 3 — All {EXPECTED_PAGES} pages have correct Bates numbers (0.30 pts)")
        elif correct_count > 0:
            ratio = correct_count / EXPECTED_PAGES
            partial = round(0.30 * ratio, 2)
            total_score += partial
            print(f"PARTIAL: Component 3 — {correct_count}/{EXPECTED_PAGES} pages correct ({partial} pts)")
        else:
            print(f"FAIL: Component 3 — No pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bates numbers positioned at bottom-right in monospace font ~9pt (0.20 points)
    try:
        # Check font and position on page 0
        page = doc[0]
        data = page.get_text('dict')
        bates_span = None
        for block in data.get('blocks', []):
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    if BATES_PREFIX in span.get('text', ''):
                        bates_span = span
                        break
                if bates_span:
                    break
            if bates_span:
                break

        if bates_span is None:
            print(f"FAIL: Component 4 — Could not find Bates span on page 0 for font/position check")
        else:
            sub_score = 0.0
            font_name = bates_span.get('font', '').lower()
            font_size = bates_span.get('size', 0)
            color = bates_span.get('color', -1)
            bbox = bates_span.get('bbox', (0, 0, 0, 0))
            page_rect = page.rect

            # Sub-check 4a: Monospace font (Courier family)
            is_monospace = 'courier' in font_name or 'mono' in font_name or 'cour' in font_name
            if is_monospace:
                sub_score += 0.05
                print(f"PASS: Component 4a — Font is monospace: '{bates_span.get('font')}'")
            else:
                print(f"FAIL: Component 4a — Expected monospace font, found: '{bates_span.get('font')}'")

            # Sub-check 4b: Font size approximately 9pt (allow 7-11)
            if 7 <= font_size <= 11:
                sub_score += 0.05
                print(f"PASS: Component 4b — Font size is {font_size}pt")
            else:
                print(f"FAIL: Component 4b — Expected ~9pt font, found: {font_size}pt")

            # Sub-check 4c: Black color (color == 0 means black in PyMuPDF int format)
            if color == 0:
                sub_score += 0.05
                print(f"PASS: Component 4c — Color is black (0)")
            else:
                print(f"FAIL: Component 4c — Expected black (0), found: {color}")

            # Sub-check 4d: Positioned at bottom-right
            # bbox[1] (top of text) should be in bottom 10% of page
            # bbox[2] (right of text) should be in right 40% of page
            bottom_threshold = page_rect.height * 0.90
            right_threshold = page_rect.width * 0.60
            is_bottom = bbox[1] >= bottom_threshold
            is_right = bbox[2] >= right_threshold

            if is_bottom and is_right:
                sub_score += 0.05
                print(f"PASS: Component 4d — Position is bottom-right (bbox: {bbox}, page: {page_rect.width}x{page_rect.height})")
            else:
                print(f"FAIL: Component 4d — Not at bottom-right. bbox: {bbox}, thresholds: bottom>{bottom_threshold}, right>{right_threshold}")

            total_score += sub_score
            print(f"Component 4 total: {sub_score}/0.20 pts")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
