"""
Reward Script: Add page numbers to PDF
Task ID: pdf_ro_012
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists with correct page count (45 pages)
  Component 2 (0.4): All pages have correct 'Page X of 45' text
  Component 3 (0.2): Font is Helvetica 10pt black
  Component 4 (0.2): Page numbers centered horizontally near y=770
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_012'
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'manual_numbered.pdf')
EXPECTED_PAGES = 45
PAGE_WIDTH = 612.0  # Letter size


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 45 pages (0.2 points)
    # This component checks that the output file preserves the original page count.
    # The initial_env does NOT have manual_numbered.pdf, so this fails on initial.
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Page count is {page_count} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All pages have correct 'Page X of 45' text (0.4 points)
    # Award partial credit: 0.4 * (pages_correct / 45)
    try:
        correct_pages = 0
        for i in range(min(doc.page_count, EXPECTED_PAGES)):
            page_text = doc[i].get_text("text")
            expected_label = f"Page {i + 1} of {EXPECTED_PAGES}"
            if expected_label in page_text:
                correct_pages += 1
            else:
                if correct_pages < 3 or i >= EXPECTED_PAGES - 2:
                    print(f"  Page {i}: missing '{expected_label}'")

        ratio = correct_pages / EXPECTED_PAGES
        comp2_score = round(0.4 * ratio, 4)
        if correct_pages == EXPECTED_PAGES:
            print(f"PASS: Component 2 -- All {EXPECTED_PAGES} pages have correct page number text ({comp2_score} pts)")
        else:
            print(f"PARTIAL: Component 2 -- {correct_pages}/{EXPECTED_PAGES} pages correct ({comp2_score} pts)")
        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Font is Helvetica 10pt black (0.2 points)
    # Check on a sample of pages (first, middle, last)
    try:
        sample_pages = [0, EXPECTED_PAGES // 2, EXPECTED_PAGES - 1]
        font_correct = 0
        for idx in sample_pages:
            if idx >= doc.page_count:
                continue
            page = doc[idx]
            d = page.get_text("dict")
            expected_label = f"Page {idx + 1} of {EXPECTED_PAGES}"
            for block in d.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if expected_label in span.get("text", ""):
                            font_name = span.get("font", "")
                            font_size = span.get("size", 0)
                            font_color = span.get("color", -1)
                            # Check: Helvetica (or helv variant), 10pt, black (color=0)
                            is_helv = "Helvetica" in font_name or "helv" in font_name.lower()
                            is_10pt = abs(font_size - 10.0) < 0.5
                            is_black = font_color == 0
                            if is_helv and is_10pt and is_black:
                                font_correct += 1
                            else:
                                print(f"  Page {idx}: font={font_name}, size={font_size}, color={font_color}")

        if font_correct == len(sample_pages):
            print(f"PASS: Component 3 -- Helvetica 10pt black on all sampled pages (0.2 pts)")
            total_score += 0.2
        elif font_correct > 0:
            partial = round(0.2 * font_correct / len(sample_pages), 4)
            print(f"PARTIAL: Component 3 -- {font_correct}/{len(sample_pages)} sampled pages correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Font check failed on all sampled pages")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Page numbers centered horizontally near y=770 (0.2 points)
    # Check that the text origin x is roughly centered on the page and y is near 770
    try:
        position_correct = 0
        for idx in sample_pages:
            if idx >= doc.page_count:
                continue
            page = doc[idx]
            d = page.get_text("dict")
            expected_label = f"Page {idx + 1} of {EXPECTED_PAGES}"
            page_w = page.rect.width
            center_x = page_w / 2.0
            for block in d.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if expected_label in span.get("text", ""):
                            origin = span.get("origin", (0, 0))
                            bbox = span.get("bbox", (0, 0, 0, 0))
                            # Text should be roughly centered: midpoint of bbox close to page center
                            text_mid_x = (bbox[0] + bbox[2]) / 2.0
                            # y origin should be near 770 (tolerance of 5pts)
                            y_ok = abs(origin[1] - 770.0) < 5.0
                            # x centered: midpoint within 30pts of page center
                            x_ok = abs(text_mid_x - center_x) < 30.0
                            if x_ok and y_ok:
                                position_correct += 1
                            else:
                                print(f"  Page {idx}: origin={origin}, bbox_mid_x={text_mid_x:.1f}, center={center_x:.1f}")

        if position_correct == len(sample_pages):
            print(f"PASS: Component 4 -- Page numbers centered at y~770 on all sampled pages (0.2 pts)")
            total_score += 0.2
        elif position_correct > 0:
            partial = round(0.2 * position_correct / len(sample_pages), 4)
            print(f"PARTIAL: Component 4 -- {position_correct}/{len(sample_pages)} sampled pages positioned correctly ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Position check failed on all sampled pages")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
