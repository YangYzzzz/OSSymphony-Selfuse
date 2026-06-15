"""
Reward Script: Remove blank separator pages and add sequential footer numbering
Task ID: pdf_pw_039
Domain: pdf
Scoring:
  Component 1 (0.25): Output file exists with exactly 12 pages
  Component 2 (0.25): No blank pages remain in the output
  Component 3 (0.25): Content pages preserved in correct chapter order
  Component 4 (0.25): Each page has centered footer 'Page X of 12'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_039'

# Expected chapter titles in order after removing blank separator pages
EXPECTED_CHAPTERS = [
    "Chapter 1",
    "Chapter 2",
    "Chapter 3",
    "Chapter 4",
    "Chapter 5",
    "Chapter 6",
    "Chapter 7",
    "Chapter 8",
    "Chapter 9",
    "Chapter 10",
    "Chapter 11",
    "Chapter 12",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: Output file has exactly 12 pages (0.25 points)
    try:
        if page_count == 12:
            print(f"PASS: Component 1 — Output has exactly 12 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 12 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No blank pages in the output (0.25 points)
    try:
        blank_pages = []
        for i in range(page_count):
            page = doc[i]
            text = page.get_text().strip()
            if len(text) == 0:
                blank_pages.append(i)
        if len(blank_pages) == 0:
            print(f"PASS: Component 2 — No blank pages found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Found {len(blank_pages)} blank page(s) at indices: {blank_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content pages in correct chapter order (0.25 points)
    try:
        chapters_found = 0
        chapters_mismatched = 0
        for i in range(min(page_count, 12)):
            page = doc[i]
            text = page.get_text().strip()
            first_line = text.split('\n')[0] if text else ""
            expected = EXPECTED_CHAPTERS[i] if i < len(EXPECTED_CHAPTERS) else None
            if expected and expected in first_line:
                chapters_found += 1
            elif expected:
                chapters_mismatched += 1
                print(f"  Page {i}: expected '{expected}' in first line, got '{first_line[:60]}'")

        if chapters_mismatched == 0 and chapters_found == 12:
            print(f"PASS: Component 3 — All 12 chapters in correct order (0.25 pts)")
            total_score += 0.25
        elif chapters_found >= 10:
            if chapters_found > 0:
                partial = 0.25 * (chapters_found / 12)
                print(f"PARTIAL: Component 3 — {chapters_found}/12 chapters in order ({partial:.3f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {chapters_found}/12 chapters found in order")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Footer page numbering 'Page X of 12' on each page (0.25 points)
    try:
        pages_with_correct_footer = 0
        for i in range(page_count):
            page = doc[i]
            text = page.get_text().strip()
            expected_footer = f"Page {i + 1} of 12"
            if expected_footer in text:
                pages_with_correct_footer += 1
            else:
                # Check with regex for slight variations
                pattern = rf"Page\s+{i + 1}\s+of\s+12"
                if re.search(pattern, text):
                    pages_with_correct_footer += 1
                else:
                    print(f"  Page {i}: missing footer '{expected_footer}'")

        if pages_with_correct_footer == page_count and page_count == 12:
            print(f"PASS: Component 4 — All 12 pages have correct footer numbering (0.25 pts)")
            total_score += 0.25
        elif pages_with_correct_footer > 0:
            partial = 0.25 * (pages_with_correct_footer / max(page_count, 12))
            print(f"PARTIAL: Component 4 — {pages_with_correct_footer}/{page_count} pages have correct footer ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have correct footer numbering")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/draft_manual_clean.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
