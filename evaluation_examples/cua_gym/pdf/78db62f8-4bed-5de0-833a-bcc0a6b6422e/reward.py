"""
Reward Script: Add page number stamps to appellate record PDF
Task ID: pdf_legal_062
Domain: pdf
Scoring:
  Component 1 (0.3): Output file exists with correct page count and AR-format stamps present
  Component 2 (0.4): Correct sequential AR-XXXX stamps on sampled pages (10 pages)
  Component 3 (0.3): Font size ~9pt and top-center positioning
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_062'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'appellate', 'record_numbered.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Correct page count + AR stamps present on first page (0.3 points)
    # This checks that the output PDF has 350 pages and that AR-0001 stamp is on page 1
    try:
        if page_count == 350:
            print(f"PASS: Page count is 350")
            # Check first page for AR-0001
            page0 = doc[0]
            text0 = page0.get_text()
            if 'AR-0001' in text0:
                print(f"PASS: Component 1 -- 350 pages and AR-0001 found on page 1 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- 350 pages but AR-0001 not found on page 1")
        else:
            print(f"FAIL: Component 1 -- Expected 350 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct sequential AR-XXXX stamps on sampled pages (0.4 points)
    # Sample 10 pages spread across the document and verify correct stamp text
    try:
        sample_indices = [0, 1, 9, 24, 49, 99, 149, 199, 274, 349]
        # Filter to valid pages
        sample_indices = [i for i in sample_indices if i < page_count]
        correct_count = 0

        for pg_idx in sample_indices:
            expected_stamp = f"AR-{pg_idx + 1:04d}"
            page = doc[pg_idx]
            text = page.get_text()
            if expected_stamp in text:
                correct_count += 1
                print(f"  Page {pg_idx}: {expected_stamp} found")
            else:
                print(f"  Page {pg_idx}: {expected_stamp} NOT found (text excerpt: {text[:100]}...)")

        if len(sample_indices) > 0:
            ratio = correct_count / len(sample_indices)
            comp2_score = round(0.4 * ratio, 2)
            if comp2_score > 0:
                print(f"PASS: Component 2 -- {correct_count}/{len(sample_indices)} sampled pages have correct stamps ({comp2_score} pts)")
                total_score += comp2_score
            else:
                print(f"FAIL: Component 2 -- 0/{len(sample_indices)} sampled pages have correct stamps")
        else:
            print(f"FAIL: Component 2 -- No valid sample pages")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Font size ~9pt and top-center positioning (0.3 points)
    # Verify the stamp is placed at top-center with approximately 9pt font
    try:
        # Check a few pages for font size and position
        check_pages = [0, 49, 349]
        check_pages = [i for i in check_pages if i < page_count]
        font_ok_count = 0
        pos_ok_count = 0

        for pg_idx in check_pages:
            page = doc[pg_idx]
            expected_stamp = f"AR-{pg_idx + 1:04d}"
            blocks = page.get_text('dict')
            page_width = page.rect.width

            for block in blocks['blocks']:
                if block['type'] != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        if expected_stamp in span['text']:
                            # Check font size (should be ~9pt, allow 7-11 tolerance)
                            font_size = span['size']
                            if 7.0 <= font_size <= 11.0:
                                font_ok_count += 1
                                print(f"  Page {pg_idx}: Font size {font_size} OK")
                            else:
                                print(f"  Page {pg_idx}: Font size {font_size} outside range 7-11")

                            # Check top-center positioning
                            # BBox: (x0, y0, x1, y1) -- y0 should be near top (< 60pt)
                            # x center should be near page center
                            bbox = span['bbox']
                            text_center_x = (bbox[0] + bbox[2]) / 2
                            page_center_x = page_width / 2
                            y_top = bbox[1]

                            if y_top < 60 and abs(text_center_x - page_center_x) < 50:
                                pos_ok_count += 1
                                print(f"  Page {pg_idx}: Position OK (y={y_top:.1f}, center_x={text_center_x:.1f}, page_center={page_center_x:.1f})")
                            else:
                                print(f"  Page {pg_idx}: Position BAD (y={y_top:.1f}, center_x={text_center_x:.1f}, page_center={page_center_x:.1f})")

        total_checks = len(check_pages)
        if total_checks > 0:
            font_ratio = font_ok_count / total_checks
            pos_ratio = pos_ok_count / total_checks
            # Split: 0.15 for font, 0.15 for position
            comp3_font = round(0.15 * font_ratio, 2)
            comp3_pos = round(0.15 * pos_ratio, 2)
            comp3_total = comp3_font + comp3_pos

            if comp3_total > 0:
                print(f"PASS: Component 3 -- font={font_ok_count}/{total_checks}, position={pos_ok_count}/{total_checks} ({comp3_total} pts)")
                total_score += comp3_total
            else:
                print(f"FAIL: Component 3 -- font={font_ok_count}/{total_checks}, position={pos_ok_count}/{total_checks}")
        else:
            print(f"FAIL: Component 3 -- no pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
    verify_task(OUTPUT_PATH)
