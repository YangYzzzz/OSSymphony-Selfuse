"""
Reward Script: Create PDF with table of contents (bookmarks)
Task ID: pdf_cr_019
Domain: pdf
Scoring:
  Component 1 (0.20): PDF exists with exactly 4 pages
  Component 2 (0.50): TOC structure matches expected 5 entries (levels, titles, page numbers)
  Component 3 (0.15): Page 1 text contains 'Introduction'
  Component 4 (0.15): Page 3 text contains 'Methodology'
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_019'

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

    # Component 1: PDF has exactly 4 pages (0.20 points)
    try:
        page_count = len(doc)
        if page_count == 4:
            print(f"PASS: Component 1 — PDF has 4 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC structure matches expected entries (0.50 points)
    # Expected TOC: 5 entries with specific levels, titles, and page numbers
    try:
        toc = doc.get_toc()
        expected_toc = [
            [1, 'Introduction', 1],
            [1, 'Literature Review', 2],
            [2, 'Previous Work', 2],
            [1, 'Methodology', 3],
            [1, 'Conclusion', 4],
        ]

        if len(toc) < 5:
            print(f"FAIL: Component 2 — Expected at least 5 TOC entries, found {len(toc)}")
        else:
            # Check each expected entry against actual TOC
            matched_entries = 0
            for i, expected_entry in enumerate(expected_toc):
                if i < len(toc):
                    actual = toc[i]
                    level_ok = actual[0] == expected_entry[0]
                    title_ok = actual[1].strip() == expected_entry[1].strip()
                    page_ok = actual[2] == expected_entry[2]
                    if level_ok and title_ok and page_ok:
                        matched_entries += 1
                    else:
                        print(f"  TOC entry {i}: expected {expected_entry}, got {actual}")

            if matched_entries == 5:
                print(f"PASS: Component 2 — All 5 TOC entries match expected structure (0.50 pts)")
                total_score += 0.50
            elif matched_entries >= 3:
                partial = round(0.50 * (matched_entries / 5), 2)
                print(f"PARTIAL: Component 2 — {matched_entries}/5 TOC entries match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {matched_entries}/5 TOC entries match")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 1 text contains 'Introduction' (0.15 points)
    try:
        page1_text = doc[0].get_text("text")
        if 'Introduction' in page1_text:
            print(f"PASS: Component 3 — Page 1 contains 'Introduction' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Page 1 does not contain 'Introduction'. Text start: {page1_text[:100]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 3 text contains 'Methodology' (0.15 points)
    try:
        page3_text = doc[2].get_text("text")
        if 'Methodology' in page3_text:
            print(f"PASS: Component 4 — Page 3 contains 'Methodology' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Page 3 does not contain 'Methodology'. Text start: {page3_text[:100]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/toc_document.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
