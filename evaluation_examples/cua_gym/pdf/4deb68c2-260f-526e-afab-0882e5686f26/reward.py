"""
Reward Script: Add clickable hyperlinks to a financial report PDF
Task ID: pdf_fin_075
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count and has exactly 3 links on page 1
  Component 2 (0.10): All 3 links are internal (LINK_GOTO, kind=1)
  Component 3 (0.25): Link 1 at rect (100,200,300,215) targets page 10 (0-indexed: 9)
  Component 4 (0.25): Link 2 at rect (100,220,300,235) targets page 15 (0-indexed: 14)
  Component 5 (0.25): Link 3 at rect (100,240,300,255) targets page 20 (0-indexed: 19)
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_075'
OUTPUT_FILE = f'{WORKDIR}/finance/report_with_links.pdf'

# Tolerance for rect coordinate comparison
RECT_TOL = 2.0


def rect_close(actual_rect, expected_rect, tol=RECT_TOL):
    """Check if two rects are approximately equal within tolerance."""
    for a, e in zip(actual_rect, expected_rect):
        if abs(a - e) > tol:
            return False
    return True


def find_link_by_rect(links, expected_rect, tol=RECT_TOL):
    """Find a link matching the expected rect (approximately)."""
    for link in links:
        link_rect = link.get("from")
        if link_rect is not None and rect_close(tuple(link_rect), expected_rect, tol):
            return link
    return None


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

    try:
        page_count = doc.page_count
        links = doc[0].get_links()
    except Exception as e:
        print(f"CRITICAL: Cannot read page 0 links: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 25 pages and exactly 3 links on page 1 (0.15 pts)
    try:
        if page_count == 25 and len(links) == 3:
            print(f"PASS: Component 1 -- 25 pages and 3 links on page 0 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 25 pages & 3 links, found {page_count} pages & {len(links)} links")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 3 links are internal LINK_GOTO (kind=1) (0.10 pts)
    try:
        goto_count = sum(1 for link in links if link.get("kind") == 1)
        if goto_count == 3:
            print(f"PASS: Component 2 -- All 3 links are LINK_GOTO (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Expected 3 LINK_GOTO links, found {goto_count}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Link at rect (100,200,300,215) targets page 9 (0-indexed = page 10) (0.25 pts)
    try:
        expected_rect_1 = (100.0, 200.0, 300.0, 215.0)
        link1 = find_link_by_rect(links, expected_rect_1)
        if link1 is not None and link1.get("page") == 9:
            print(f"PASS: Component 3 -- Link 1 at ~{expected_rect_1} targets page 9 (0.25 pts)")
            total_score += 0.25
        elif link1 is not None:
            print(f"FAIL: Component 3 -- Link 1 found at correct rect but targets page {link1.get('page')}, expected 9")
        else:
            print(f"FAIL: Component 3 -- No link found at rect ~{expected_rect_1}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Link at rect (100,220,300,235) targets page 14 (0-indexed = page 15) (0.25 pts)
    try:
        expected_rect_2 = (100.0, 220.0, 300.0, 235.0)
        link2 = find_link_by_rect(links, expected_rect_2)
        if link2 is not None and link2.get("page") == 14:
            print(f"PASS: Component 4 -- Link 2 at ~{expected_rect_2} targets page 14 (0.25 pts)")
            total_score += 0.25
        elif link2 is not None:
            print(f"FAIL: Component 4 -- Link 2 found at correct rect but targets page {link2.get('page')}, expected 14")
        else:
            print(f"FAIL: Component 4 -- No link found at rect ~{expected_rect_2}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Link at rect (100,240,300,255) targets page 19 (0-indexed = page 20) (0.25 pts)
    try:
        expected_rect_3 = (100.0, 240.0, 300.0, 255.0)
        link3 = find_link_by_rect(links, expected_rect_3)
        if link3 is not None and link3.get("page") == 19:
            print(f"PASS: Component 5 -- Link 3 at ~{expected_rect_3} targets page 19 (0.25 pts)")
            total_score += 0.25
        elif link3 is not None:
            print(f"FAIL: Component 5 -- Link 3 found at correct rect but targets page {link3.get('page')}, expected 19")
        else:
            print(f"FAIL: Component 5 -- No link found at rect ~{expected_rect_3}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
