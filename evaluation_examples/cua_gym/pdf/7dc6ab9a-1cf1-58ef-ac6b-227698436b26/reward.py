"""
Reward Script: Create an index page listing all unique bold words with page numbers
Task ID: pdf_res_064
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists at correct path
  - Component 2 (0.25): Page count is 26 (25 original + 1 index)
  - Component 3 (0.20): Original 25 pages content preserved
  - Component 4 (0.15): Last page contains "Index of Bold Terms" title
  - Component 5 (0.25): Last page has alphabetically sorted bold terms with page numbers
"""

import os
import sys

# PyMuPDF for PDF verification
try:
    import fitz
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_064'
OUTPUT_PATH = f'{WORKDIR}/papers/textbook_chapter_indexed.pdf'
ORIGINAL_PATH = f'{WORKDIR}/papers/textbook_chapter.pdf'


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

    # Precondition: original file must exist (for comparison)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        indexed_doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open indexed PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        orig_doc = fitz.open(ORIGINAL_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open original PDF: {e}")
        indexed_doc.close()
        print("REWARD: 0.0")
        return 0.0

    orig_page_count = orig_doc.page_count

    # Component 1: Output file is a valid PDF with more pages than original (0.15 points)
    # This fails on initial_env because textbook_chapter_indexed.pdf does not exist there
    try:
        if indexed_doc.page_count > orig_page_count:
            print(f"PASS: Component 1 — Output PDF has {indexed_doc.page_count} pages, "
                  f"more than original {orig_page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Output PDF has {indexed_doc.page_count} pages, "
                  f"expected more than original {orig_page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page count is exactly 26 (25 original + 1 index) (0.25 points)
    try:
        expected_pages = orig_page_count + 1  # original pages + 1 index page
        if indexed_doc.page_count == expected_pages:
            print(f"PASS: Component 2 — Page count is {indexed_doc.page_count} "
                  f"(original {orig_page_count} + 1 index) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Page count is {indexed_doc.page_count}, "
                  f"expected {expected_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original pages content is preserved (0.20 points)
    # Verify that the first N pages of the indexed PDF match the original
    try:
        pages_match = 0
        pages_to_check = min(orig_page_count, 5)  # sample 5 pages for efficiency
        check_indices = [0, orig_page_count // 4, orig_page_count // 2,
                         3 * orig_page_count // 4, orig_page_count - 1]
        check_indices = list(set(check_indices))[:pages_to_check]

        for idx in check_indices:
            if idx < indexed_doc.page_count and idx < orig_page_count:
                orig_text = orig_doc[idx].get_text()[:500]
                indexed_text = indexed_doc[idx].get_text()[:500]
                if orig_text == indexed_text:
                    pages_match += 1

        if pages_match == len(check_indices) and len(check_indices) > 0:
            print(f"PASS: Component 3 — All {pages_match} sampled pages match original (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {pages_match}/{len(check_indices)} sampled pages match original")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Last page contains index title (0.15 points)
    try:
        last_page = indexed_doc[-1]
        last_text = last_page.get_text()
        last_text_lower = last_text.lower()

        # Check for index-related title
        has_index_title = ("index" in last_text_lower and "bold" in last_text_lower) or \
                          "index of bold terms" in last_text_lower or \
                          "bold terms index" in last_text_lower

        if has_index_title:
            print(f"PASS: Component 4 — Last page has index title (0.15 pts)")
            total_score += 0.15
        else:
            # Also check for just "index" as title
            lines = [l.strip() for l in last_text.split('\n') if l.strip()]
            first_lines = ' '.join(lines[:3]).lower() if lines else ''
            if 'index' in first_lines:
                print(f"PASS: Component 4 — Last page has index-related title (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Last page does not contain index title. "
                      f"First 200 chars: {last_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Last page has alphabetically sorted terms with page numbers (0.25 points)
    try:
        last_page = indexed_doc[-1]
        last_text = last_page.get_text()
        lines = [l.strip() for l in last_text.split('\n') if l.strip()]

        # Parse terms and page numbers from the index
        # Expected format: term on one line, page numbers on the next
        terms = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Skip title and section headers (single letter)
            if line.lower().startswith('index') or (len(line) == 1 and line.isalpha()):
                i += 1
                continue
            # Skip pure page number lines
            if all(c.isdigit() or c in ', ' for c in line):
                i += 1
                continue
            # This looks like a term - check if next line is page numbers
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if all(c.isdigit() or c in ', ' for c in next_line) and next_line:
                    terms.append(line)
                    i += 2
                    continue
            # Term might have page numbers on same line (e.g., "term ... 1, 2, 3")
            terms.append(line)
            i += 1

        has_terms = len(terms) >= 10  # Should have many bold terms
        is_sorted = all(terms[j].lower() <= terms[j + 1].lower()
                        for j in range(len(terms) - 1)) if len(terms) > 1 else False

        sub_score = 0.0
        if has_terms:
            sub_score += 0.10
            print(f"  Sub-check: Found {len(terms)} terms in index")
        else:
            print(f"  Sub-check FAIL: Only found {len(terms)} terms, expected >= 10")

        if is_sorted:
            sub_score += 0.15
            print(f"  Sub-check: Terms are alphabetically sorted")
        else:
            print(f"  Sub-check FAIL: Terms are not alphabetically sorted")
            if len(terms) > 1:
                for j in range(len(terms) - 1):
                    if terms[j].lower() > terms[j + 1].lower():
                        print(f"    First unsorted pair: '{terms[j]}' > '{terms[j+1]}'")
                        break

        if sub_score > 0:
            print(f"PASS: Component 5 — Index terms verified ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 — Index verification failed")

    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    orig_doc.close()
    indexed_doc.close()

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
