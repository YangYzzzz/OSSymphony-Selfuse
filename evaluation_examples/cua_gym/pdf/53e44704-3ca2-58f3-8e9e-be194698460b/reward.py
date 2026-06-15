"""
Reward Script: Add page numbers to PDF
Task ID: pdf_gf1_021
Domain: pdf
Scoring:
  Component 1 (0.20): Page count is 9
  Component 2 (0.30): Every page has correct "Page N of 9" text
  Component 3 (0.20): Page numbers positioned near bottom of page (within 50pt of bottom edge)
  Component 4 (0.15): Page numbers use Helvetica font at ~12pt size
  Component 5 (0.15): Page numbers are horizontally centered
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_021'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: Page count is 9 (0.20 points)
    # The task says initial PDF has 9 pages; the numbered output must also have 9 pages.
    try:
        if page_count == 9:
            print(f"PASS: Component 1 — Page count is 9 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 9 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page has correct "Page N of M" text (0.30 points)
    # Check all pages for the correct page number string.
    try:
        correct_count = 0
        total_pages = page_count
        for i in range(total_pages):
            page = doc[i]
            text = page.get_text("text")
            expected_str = f"Page {i+1} of {total_pages}"
            if expected_str in text:
                correct_count += 1
            else:
                print(f"  DETAIL: Page {i}: expected '{expected_str}', not found in extracted text")

        if correct_count == total_pages and total_pages > 0:
            print(f"PASS: Component 2 — All {total_pages} pages have correct 'Page N of {total_pages}' text (0.30 pts)")
            total_score += 0.30
        elif correct_count > 0:
            partial = 0.30 * (correct_count / total_pages)
            print(f"PARTIAL: Component 2 — {correct_count}/{total_pages} pages have correct page numbers ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have correct 'Page N of M' text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page numbers positioned near bottom (within 50pt of bottom edge) (0.20 points)
    # Page height is 792pt; we expect the page number text block y0 >= 742 (792 - 50).
    try:
        bottom_ok_count = 0
        for i in range(page_count):
            page = doc[i]
            page_height = page.rect.height
            threshold_y = page_height - 50  # within 50pt of bottom
            blocks = page.get_text("blocks")
            expected_str = f"Page {i+1} of"
            for b in blocks:
                # b = (x0, y0, x1, y1, text, block_no, block_type)
                block_text = b[4].strip() if isinstance(b[4], str) else ""
                if expected_str in block_text and b[1] >= threshold_y:
                    bottom_ok_count += 1
                    break

        if bottom_ok_count == page_count and page_count > 0:
            print(f"PASS: Component 3 — All page numbers positioned in bottom 50pt area (0.20 pts)")
            total_score += 0.20
        elif bottom_ok_count > 0:
            partial = 0.20 * (bottom_ok_count / page_count)
            print(f"PARTIAL: Component 3 — {bottom_ok_count}/{page_count} page numbers in correct position ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No page numbers found in the bottom 50pt area")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page numbers use Helvetica font at ~12pt (0.15 points)
    # Check font info on a sample of pages (first, middle, last).
    try:
        sample_pages = [0, page_count // 2, page_count - 1] if page_count >= 3 else list(range(page_count))
        font_ok_count = 0
        for i in sample_pages:
            page = doc[i]
            data = page.get_text("dict")
            expected_str = f"Page {i+1} of"
            for block in data["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if expected_str in span["text"]:
                            font_name = span["font"].lower()
                            font_size = span["size"]
                            if "helvetica" in font_name and abs(font_size - 12.0) < 1.0:
                                font_ok_count += 1

        if font_ok_count == len(sample_pages):
            print(f"PASS: Component 4 — Page numbers use Helvetica ~12pt font (0.15 pts)")
            total_score += 0.15
        elif font_ok_count > 0:
            partial = 0.15 * (font_ok_count / len(sample_pages))
            print(f"PARTIAL: Component 4 — {font_ok_count}/{len(sample_pages)} sampled pages have correct font ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Page numbers do not use Helvetica ~12pt font")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page numbers are horizontally centered (0.15 points)
    # For a 612pt wide page, the center is 306. We check that the page number text block
    # is roughly centered (midpoint of text within 50pt of page center).
    try:
        center_ok_count = 0
        for i in range(page_count):
            page = doc[i]
            page_width = page.rect.width
            page_center_x = page_width / 2.0
            expected_str = f"Page {i+1} of"
            blocks = page.get_text("blocks")
            for b in blocks:
                block_text = b[4].strip() if isinstance(b[4], str) else ""
                if expected_str in block_text:
                    block_mid_x = (b[0] + b[2]) / 2.0
                    if abs(block_mid_x - page_center_x) < 50:
                        center_ok_count += 1
                    else:
                        print(f"  DETAIL: Page {i} number mid_x={block_mid_x:.1f}, page_center={page_center_x:.1f}")
                    break

        if center_ok_count == page_count and page_count > 0:
            print(f"PASS: Component 5 — All page numbers are horizontally centered (0.15 pts)")
            total_score += 0.15
        elif center_ok_count > 0:
            partial = 0.15 * (center_ok_count / page_count)
            print(f"PARTIAL: Component 5 — {center_ok_count}/{page_count} page numbers centered ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Page numbers are not horizontally centered")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/report_draft_numbered.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
