"""
Reward Script: Add header to every page of court transcript PDF
Task ID: pdf_legal_080
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid PDF with 200 pages
  Component 2 (0.45): Header text present on all 200 pages
  Component 3 (0.20): Header positioned near top of each page (y < 40pt)
  Component 4 (0.20): Header font size approximately 8pt
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_080'
EXPECTED_HEADER = 'Case No. 2024-CR-4567 | People v. Anderson | Official Transcript'
EXPECTED_PAGE_COUNT = 200
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'transcript_headed.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file is valid PDF with 200 pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 -- PDF has {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Header text present on all pages (0.45 points)
    # Check every page; award partial credit proportionally
    try:
        pages_with_header = 0
        pages_checked = doc.page_count
        for pg_idx in range(pages_checked):
            page = doc[pg_idx]
            text = page.get_text("text")
            if EXPECTED_HEADER in text:
                pages_with_header += 1

        if pages_checked > 0:
            header_ratio = pages_with_header / pages_checked
        else:
            header_ratio = 0.0

        if header_ratio >= 1.0:
            print(f"PASS: Component 2 -- Header found on all {pages_with_header}/{pages_checked} pages (0.45 pts)")
            total_score += 0.45
        elif header_ratio > 0:
            partial = round(0.45 * header_ratio, 3)
            print(f"PARTIAL: Component 2 -- Header found on {pages_with_header}/{pages_checked} pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Header not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Header positioned at top of page (y < 40pt) on all pages (0.20 points)
    # Sample 10 evenly spaced pages for efficiency
    try:
        sample_pages = [0, 20, 40, 60, 80, 100, 120, 140, 160, 199]
        sample_pages = [p for p in sample_pages if p < doc.page_count]
        pages_with_top_header = 0
        for pg_idx in sample_pages:
            page = doc[pg_idx]
            blocks = page.get_text("blocks")
            found_at_top = False
            for b in blocks:
                # b = (x0, y0, x1, y1, text, block_no, block_type)
                if b[6] == 0 and EXPECTED_HEADER in b[4] and b[1] < 40:
                    found_at_top = True
                    break
            if found_at_top:
                pages_with_top_header += 1

        if len(sample_pages) > 0:
            top_ratio = pages_with_top_header / len(sample_pages)
        else:
            top_ratio = 0.0

        if top_ratio >= 1.0:
            print(f"PASS: Component 3 -- Header at top on all {pages_with_top_header}/{len(sample_pages)} sampled pages (0.20 pts)")
            total_score += 0.20
        elif top_ratio > 0:
            partial = round(0.20 * top_ratio, 3)
            print(f"PARTIAL: Component 3 -- Header at top on {pages_with_top_header}/{len(sample_pages)} sampled pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Header not found at top of any sampled page")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Header font size approximately 8pt (0.20 points)
    # Check font size on sampled pages
    try:
        sample_pages_font = [0, 50, 100, 199]
        sample_pages_font = [p for p in sample_pages_font if p < doc.page_count]
        pages_with_correct_font = 0
        for pg_idx in sample_pages_font:
            page = doc[pg_idx]
            data = page.get_text("dict")
            found_correct_size = False
            for block in data.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        span_text = span.get("text", "")
                        span_y = span.get("bbox", [0, 999, 0, 0])[1]
                        span_size = span.get("size", 0)
                        if "Case No." in span_text and span_y < 40:
                            # Check font size is close to 8pt (allow tolerance)
                            if abs(span_size - 8.0) < 1.5:
                                found_correct_size = True
                                break
                    if found_correct_size:
                        break
                if found_correct_size:
                    break
            if found_correct_size:
                pages_with_correct_font += 1

        if len(sample_pages_font) > 0:
            font_ratio = pages_with_correct_font / len(sample_pages_font)
        else:
            font_ratio = 0.0

        if font_ratio >= 1.0:
            print(f"PASS: Component 4 -- Header font ~8pt on all {pages_with_correct_font}/{len(sample_pages_font)} sampled pages (0.20 pts)")
            total_score += 0.20
        elif font_ratio > 0:
            partial = round(0.20 * font_ratio, 3)
            print(f"PARTIAL: Component 4 -- Header font ~8pt on {pages_with_correct_font}/{len(sample_pages_font)} sampled pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Header font size not ~8pt on any sampled page")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
