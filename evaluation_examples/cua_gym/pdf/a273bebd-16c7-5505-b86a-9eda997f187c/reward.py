"""
Reward Script: Add running chapter headers to user_guide.pdf
Task ID: pdf_pw_038
Domain: pdf
Scoring:
  - Component 1 (0.10): Output file exists with 25 pages
  - Component 2 (0.25): Pages 1-5 have 'Chapter 1: Getting Started' header
  - Component 3 (0.25): Pages 6-12 have 'Chapter 2: Configuration' header
  - Component 4 (0.20): Pages 13-20 have 'Chapter 3: Advanced Usage' header
  - Component 5 (0.20): Pages 21-25 have 'Chapter 4: Troubleshooting' header
  Each chapter component checks: correct text, ~9pt size, italic font, gray color.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_038'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'user_guide_headers.pdf')

# Chapter mapping: (start_page_1indexed, end_page_1indexed, expected_text)
CHAPTERS = [
    (1, 5, 'Chapter 1: Getting Started'),
    (6, 12, 'Chapter 2: Configuration'),
    (13, 20, 'Chapter 3: Advanced Usage'),
    (21, 25, 'Chapter 4: Troubleshooting'),
]

# Gray color 0x666666 = 6710886 in decimal (PyMuPDF integer color representation)
EXPECTED_COLOR = 6710886
COLOR_TOLERANCE = 200000  # allow some tolerance for color matching
EXPECTED_FONT_SIZE = 9.0
FONT_SIZE_TOLERANCE = 1.5


def find_header_span(page, y_threshold=35):
    """
    Search for a header-like text span in the top area of a page (y < y_threshold).
    Returns the span dict if found, or None.
    We look for spans with size around 9pt in the top margin area.
    """
    blocks = page.get_text('dict')['blocks']
    for block in blocks:
        if 'lines' not in block:
            continue
        for line in block['lines']:
            bbox = line['bbox']
            # bbox = (x0, y0, x1, y1) — check if top of line is in header area
            if bbox[1] < y_threshold:
                for span in line['spans']:
                    # Filter for header-sized text (around 9pt, not large chapter titles)
                    if abs(span['size'] - EXPECTED_FONT_SIZE) < FONT_SIZE_TOLERANCE:
                        return span
    return None


def check_chapter_headers(doc, start_page, end_page, expected_text):
    """
    Check that all pages in [start_page, end_page] (1-indexed) have the correct header.
    Returns (score_fraction, details_str) where score_fraction is 0.0 to 1.0
    representing how many pages in this chapter range have correct headers.
    """
    total_pages = end_page - start_page + 1
    correct_pages = 0
    issues = []

    for page_num_1 in range(start_page, end_page + 1):
        page_idx = page_num_1 - 1
        page = doc[page_idx]
        span = find_header_span(page)

        if span is None:
            issues.append(f'Page {page_num_1}: no header found in top margin')
            continue

        # Check text content
        text_ok = span['text'].strip() == expected_text

        # Check font size (~9pt)
        size_ok = abs(span['size'] - EXPECTED_FONT_SIZE) < FONT_SIZE_TOLERANCE

        # Check italic font (font name should contain 'Italic' or 'it' or 'oblique')
        font_name = span.get('font', '')
        italic_ok = any(kw in font_name.lower() for kw in ['italic', 'oblique', 'it'])

        # Check gray color (should be close to 0x666666 = 6710886)
        color_val = span.get('color', 0)
        color_ok = abs(color_val - EXPECTED_COLOR) < COLOR_TOLERANCE

        if text_ok and size_ok and italic_ok and color_ok:
            correct_pages += 1
        else:
            detail_parts = []
            if not text_ok:
                detail_parts.append(f'text={repr(span["text"])}')
            if not size_ok:
                detail_parts.append(f'size={span["size"]}')
            if not italic_ok:
                detail_parts.append(f'font={font_name}')
            if not color_ok:
                detail_parts.append(f'color={color_val}')
            issues.append(f'Page {page_num_1}: ' + ', '.join(detail_parts))

    fraction = correct_pages / total_pages
    return fraction, correct_pages, total_pages, issues


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct page count (0.1 points)
    # This changes between initial and golden because the output file only exists in golden.
    try:
        page_count = len(doc)
        if page_count == 25:
            print(f"PASS: Component 1 — Page count is 25 (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Expected 25 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Components 2-5: Chapter headers
    chapter_weights = [0.25, 0.25, 0.20, 0.20]
    for idx, (start, end, text) in enumerate(CHAPTERS):
        comp_num = idx + 2
        weight = chapter_weights[idx]
        try:
            fraction, correct, total, issues = check_chapter_headers(doc, start, end, text)
            earned = round(weight * fraction, 4)
            if fraction == 1.0:
                print(f"PASS: Component {comp_num} — '{text}' headers correct on all {total} pages ({weight} pts)")
                total_score += weight
            elif fraction > 0:
                print(f"PARTIAL: Component {comp_num} — '{text}' headers correct on {correct}/{total} pages ({earned}/{weight} pts)")
                for issue in issues:
                    print(f"  - {issue}")
                total_score += earned
            else:
                print(f"FAIL: Component {comp_num} — '{text}' headers missing or incorrect on all {total} pages")
                for issue in issues[:3]:
                    print(f"  - {issue}")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
