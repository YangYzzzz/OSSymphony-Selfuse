"""
Reward Script: Add line numbers to every page of a legal declaration PDF
Task ID: pdf_legal_047
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists with correct page count (5 pages)
  Component 2 (0.4): Each page has 28 line numbers in left margin (x near 36)
  Component 3 (0.2): Line numbers are sequential 1-28 on each page
  Component 4 (0.2): Font size is approximately 10pt
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_047'
OUTPUT_PATH = f'{WORKDIR}/legal/declaration_lined.pdf'
EXPECTED_PAGES = 5
EXPECTED_LINES_PER_PAGE = 28
EXPECTED_X = 36.0
X_TOLERANCE = 10.0  # allow some tolerance on x position
EXPECTED_FONTSIZE = 10.0
FONTSIZE_TOLERANCE = 2.0


def get_left_margin_line_numbers(page, x_threshold=50):
    """Extract text spans from the left margin that look like line numbers."""
    blocks = page.get_text('dict')['blocks']
    line_nums = []
    for b in blocks:
        if 'lines' not in b:
            continue
        for line in b['lines']:
            for span in line['spans']:
                bbox = span['bbox']
                text = span['text'].strip()
                # Must be in left margin area
                if bbox[0] < x_threshold and text.isdigit():
                    line_nums.append({
                        'x': bbox[0],
                        'y': bbox[1],
                        'text': text,
                        'number': int(text),
                        'size': span['size'],
                    })
    # Sort by y position
    line_nums.sort(key=lambda ln: ln['y'])
    return line_nums


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
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

    # Component 1: Output file has correct page count (0.2 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — PDF has {page_count} pages as expected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each page has 28 line numbers in left margin (0.4 points)
    # Award partial credit per page: 0.4 / 5 = 0.08 per page
    try:
        pages_with_correct_count = 0
        all_page_line_nums = []
        for i in range(min(doc.page_count, EXPECTED_PAGES)):
            page = doc[i]
            line_nums = get_left_margin_line_numbers(page)
            all_page_line_nums.append(line_nums)
            if len(line_nums) == EXPECTED_LINES_PER_PAGE:
                pages_with_correct_count += 1
                print(f"  Page {i}: Found {len(line_nums)} line numbers — correct")
            else:
                print(f"  Page {i}: Found {len(line_nums)} line numbers — expected {EXPECTED_LINES_PER_PAGE}")

        if pages_with_correct_count == EXPECTED_PAGES:
            comp2_score = 0.4
            print(f"PASS: Component 2 — All {EXPECTED_PAGES} pages have {EXPECTED_LINES_PER_PAGE} line numbers ({comp2_score} pts)")
            total_score += comp2_score
        elif pages_with_correct_count > 0:
            comp2_score = (pages_with_correct_count / EXPECTED_PAGES) * 0.4
            print(f"PARTIAL: Component 2 — {pages_with_correct_count}/{EXPECTED_PAGES} pages correct ({comp2_score:.2f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No pages have correct line number count")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        all_page_line_nums = []

    # Component 3: Line numbers are sequential 1-28 on each page (0.2 points)
    # Award partial credit per page: 0.2 / 5 = 0.04 per page
    try:
        pages_with_correct_sequence = 0
        for i, line_nums in enumerate(all_page_line_nums):
            if len(line_nums) == EXPECTED_LINES_PER_PAGE:
                numbers = [ln['number'] for ln in line_nums]
                expected_seq = list(range(1, EXPECTED_LINES_PER_PAGE + 1))
                if numbers == expected_seq:
                    pages_with_correct_sequence += 1
                else:
                    print(f"  Page {i}: Sequence mismatch — got {numbers[:5]}...{numbers[-3:]}")
            else:
                print(f"  Page {i}: Skipped sequence check (wrong count)")

        if pages_with_correct_sequence == EXPECTED_PAGES:
            comp3_score = 0.2
            print(f"PASS: Component 3 — All pages have sequential 1-28 numbering ({comp3_score} pts)")
            total_score += comp3_score
        elif pages_with_correct_sequence > 0:
            comp3_score = (pages_with_correct_sequence / EXPECTED_PAGES) * 0.2
            print(f"PARTIAL: Component 3 — {pages_with_correct_sequence}/{EXPECTED_PAGES} pages with correct sequence ({comp3_score:.2f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No pages have correct 1-28 sequence")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Font size is approximately 10pt (0.2 points)
    # Check average font size across all line numbers
    try:
        all_sizes = []
        for line_nums in all_page_line_nums:
            for ln in line_nums:
                all_sizes.append(ln['size'])

        if len(all_sizes) > 0:
            avg_size = sum(all_sizes) / len(all_sizes)
            if abs(avg_size - EXPECTED_FONTSIZE) <= FONTSIZE_TOLERANCE:
                print(f"PASS: Component 4 — Average font size {avg_size:.1f}pt is within tolerance of {EXPECTED_FONTSIZE}pt (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Average font size {avg_size:.1f}pt, expected ~{EXPECTED_FONTSIZE}pt")
        else:
            print(f"FAIL: Component 4 — No line numbers found to check font size")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
