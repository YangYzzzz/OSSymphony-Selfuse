"""
Reward Script: Add page numbers to PDF in 'Page X of Y' format
Task ID: pdf_gf3_007
Domain: pdf
Scoring:
  Component 1: File exists with correct page count (0.15)
  Component 2: Page number text present on all pages (0.35)
  Component 3: Page numbers are sequentially correct (0.20)
  Component 4: Font size ~10pt (0.15)
  Component 5: Text color is gray #808080 (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_007'


def find_page_number_spans(doc, page_idx):
    """Find spans matching 'Page X of Y' pattern on a given page."""
    page = doc[page_idx]
    data = page.get_text('dict')
    matches = []
    for block in data.get('blocks', []):
        if block.get('type', 0) != 0:
            continue
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                txt = span.get('text', '').strip()
                if re.match(r'^Page\s+\d+\s+of\s+\d+$', txt):
                    matches.append(span)
    return matches


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: File has 30 pages (0.15 points)
    try:
        if page_count == 30:
            print(f"PASS: Component 1 — PDF has {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 30 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Page X of Y' text present on ALL 30 pages (0.35 points)
    try:
        pages_with_number = 0
        pages_missing_number = []
        for i in range(page_count):
            spans = find_page_number_spans(doc, i)
            if len(spans) > 0:
                pages_with_number += 1
            else:
                pages_missing_number.append(i + 1)

        if page_count > 0 and pages_with_number == page_count:
            print(f"PASS: Component 2 — All {page_count} pages have 'Page X of Y' text (0.35 pts)")
            total_score += 0.35
        elif pages_with_number > 0:
            # Partial credit: proportional to pages that have numbers
            partial = 0.35 * (pages_with_number / page_count)
            print(f"PARTIAL: Component 2 — {pages_with_number}/{page_count} pages have page numbers ({partial:.3f} pts)")
            print(f"  Missing on pages: {pages_missing_number[:10]}{'...' if len(pages_missing_number) > 10 else ''}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have 'Page X of Y' text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page numbers are sequentially correct (Page 1 of 30 ... Page 30 of 30) (0.20 points)
    try:
        correct_count = 0
        incorrect_pages = []
        for i in range(page_count):
            spans = find_page_number_spans(doc, i)
            expected = f"Page {i + 1} of {page_count}"
            found_correct = False
            for span in spans:
                txt = span.get('text', '').strip()
                # Normalize whitespace for comparison
                normalized = re.sub(r'\s+', ' ', txt)
                if normalized == expected:
                    found_correct = True
                    break
            if found_correct:
                correct_count += 1
            else:
                actual_texts = [s.get('text', '').strip() for s in spans]
                incorrect_pages.append((i + 1, expected, actual_texts))

        if page_count > 0 and correct_count == page_count:
            print(f"PASS: Component 3 — All page numbers are sequentially correct (0.20 pts)")
            total_score += 0.20
        elif correct_count > 0:
            partial = 0.20 * (correct_count / page_count)
            print(f"PARTIAL: Component 3 — {correct_count}/{page_count} correct ({partial:.3f} pts)")
            for pg, exp, act in incorrect_pages[:5]:
                print(f"  Page {pg}: expected '{exp}', found {act}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No correct page numbers found")
            if incorrect_pages:
                for pg, exp, act in incorrect_pages[:3]:
                    print(f"  Page {pg}: expected '{exp}', found {act}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Font size is approximately 10pt (0.15 points)
    try:
        pages_correct_size = 0
        sample_sizes = []
        for i in range(page_count):
            spans = find_page_number_spans(doc, i)
            for span in spans:
                size = span.get('size', 0)
                sample_sizes.append(size)
                if abs(size - 10.0) <= 1.5:  # tolerance of 1.5pt
                    pages_correct_size += 1
                    break

        if page_count > 0 and pages_correct_size == page_count:
            print(f"PASS: Component 4 — Font size ~10pt on all pages (0.15 pts)")
            total_score += 0.15
        elif pages_correct_size > 0:
            partial = 0.15 * (pages_correct_size / page_count)
            print(f"PARTIAL: Component 4 — {pages_correct_size}/{page_count} pages have ~10pt size ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Font size not ~10pt. Found sizes: {sample_sizes[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Text color is gray #808080 = rgb(128,128,128) (0.15 points)
    try:
        pages_correct_color = 0
        sample_colors = []
        target_rgb = (128, 128, 128)
        tolerance = 20  # allow some tolerance in color matching

        for i in range(page_count):
            spans = find_page_number_spans(doc, i)
            for span in spans:
                c = span.get('color', 0)
                rgb = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
                sample_colors.append(rgb)
                if all(abs(a - e) <= tolerance for a, e in zip(rgb, target_rgb)):
                    pages_correct_color += 1
                    break

        if page_count > 0 and pages_correct_color == page_count:
            print(f"PASS: Component 5 — Text color is gray #808080 on all pages (0.15 pts)")
            total_score += 0.15
        elif pages_correct_color > 0:
            partial = 0.15 * (pages_correct_color / page_count)
            print(f"PARTIAL: Component 5 — {pages_correct_color}/{page_count} pages have correct gray color ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Color not gray #808080. Found: {sample_colors[:5]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/documents/manual_numbered.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
