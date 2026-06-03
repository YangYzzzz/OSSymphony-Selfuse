"""
Reward Script: Add a clickable table-of-contents page at the beginning of ebook.pdf
Task ID: pdf_gf1_037
Domain: pdf
Scoring:
  Component 1: Output file exists and is valid PDF (0.1 pts)
  Component 2: Page count is 51 (original 50 + 1 TOC page) (0.2 pts)
  Component 3: TOC page contains 'Table of Contents' heading (0.15 pts)
  Component 4: TOC page contains all 5 chapter titles (0.2 pts)
  Component 5: TOC page has 5 internal GOTO links (0.15 pts)
  Component 6: Links point to correct target pages (shifted by +1) (0.2 pts)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_037'

# Expected chapter titles and their ORIGINAL page numbers (1-indexed, before TOC insertion)
EXPECTED_CHAPTERS = [
    ("Prologue", 1),
    ("Chapter 1", 8),
    ("Chapter 2", 20),
    ("Chapter 3", 33),
    ("Epilogue", 45),
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF (0.1 pts)
    # This check differentiates initial (file doesn't exist) from golden (file exists)
    try:
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count > 0:
            print(f"PASS: Component 1 - File is a valid PDF with {page_count} pages (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 - PDF has 0 pages")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot load file {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Page count is 51 (original 50 + 1 TOC page) (0.2 pts)
    try:
        if page_count == 51:
            print(f"PASS: Component 2 - Page count is 51 as expected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - Expected 51 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: TOC page (page 0) contains 'Table of Contents' heading (0.15 pts)
    try:
        toc_page = doc[0]
        toc_text = toc_page.get_text("text")
        if "Table of Contents" in toc_text:
            print(f"PASS: Component 3 - TOC page contains 'Table of Contents' heading (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - 'Table of Contents' not found on page 0. Text starts with: {toc_text[:100]!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: TOC page contains all 5 chapter titles (0.2 pts)
    # Award partial credit: 0.04 per title found
    try:
        toc_text = doc[0].get_text("text")
        titles_found = 0
        for title, _ in EXPECTED_CHAPTERS:
            if title in toc_text:
                titles_found += 1
                print(f"  Found title: '{title}'")
            else:
                print(f"  Missing title: '{title}'")

        if titles_found == 5:
            print(f"PASS: Component 4 - All 5 chapter titles found on TOC page (0.2 pts)")
            total_score += 0.2
        elif titles_found > 0:
            partial = round(0.04 * titles_found, 2)
            print(f"PARTIAL: Component 4 - {titles_found}/5 titles found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - No chapter titles found on TOC page")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: TOC page has 5 internal GOTO links (0.15 pts)
    try:
        links = doc[0].get_links()
        # Filter for internal GOTO links (kind == 1 is LINK_GOTO)
        goto_links = [l for l in links if l.get("kind") == 1]
        if len(goto_links) == 5:
            print(f"PASS: Component 5 - TOC page has 5 internal GOTO links (0.15 pts)")
            total_score += 0.15
        elif len(goto_links) > 0:
            # Partial credit if some links exist
            partial = round(0.15 * min(len(goto_links), 5) / 5, 2)
            print(f"PARTIAL: Component 5 - Found {len(goto_links)} GOTO links, expected 5 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No internal GOTO links found on TOC page (found {len(links)} total links)")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Links point to correct target pages (0.2 pts)
    # After inserting TOC page at beginning, original pages shift by +1
    # So original page N (1-indexed) becomes page N+1 (1-indexed) = page N (0-indexed)
    # Expected target pages (0-indexed): Prologue->1, Ch1->8, Ch2->20, Ch3->33, Epilogue->45
    try:
        links = doc[0].get_links()
        goto_links = [l for l in links if l.get("kind") == 1]

        # Extract target pages from links (0-indexed)
        link_targets = sorted([l.get("page", -1) for l in goto_links])
        # Expected targets: original pages were 1,8,20,33,45 (1-indexed).
        # After prepending TOC page, they become pages 2,9,21,34,46 (1-indexed) = 1,8,20,33,45 (0-indexed)
        expected_targets = sorted([1, 8, 20, 33, 45])

        correct_count = 0
        for expected in expected_targets:
            if expected in link_targets:
                correct_count += 1
                print(f"  Link target page {expected} (0-indexed) found")
            else:
                print(f"  Link target page {expected} (0-indexed) NOT found")

        if correct_count == 5:
            print(f"PASS: Component 6 - All 5 links point to correct pages (0.2 pts)")
            total_score += 0.2
        elif correct_count > 0:
            partial = round(0.04 * correct_count, 2)
            print(f"PARTIAL: Component 6 - {correct_count}/5 links point to correct pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 - No links point to expected pages. Found targets: {link_targets}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/ebook_with_toc.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
