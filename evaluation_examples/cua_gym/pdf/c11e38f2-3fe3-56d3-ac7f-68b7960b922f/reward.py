"""
Reward Script: Add internal GoTo link and external URI link to linked_doc.pdf
Task ID: pdf_adv_190
Domain: pdf

Scoring:
- Component 1: File ~/Documents/linked_doc.pdf exists and is openable (gate)
- Component 2: File has exactly 15 pages (0.10 pts)
- Component 3: Page 1 has exactly 2 link annotations total (0.20 pts)
- Component 4: URI link exists at rect (72, 730, 300, 745) pointing to
               'https://www.example.com/resources' (0.35 pts)
               - Partial (0.20): URI link exists anywhere on page 1 with correct URL
               - Full (0.35): URI link at correct rect AND correct URL
- Component 5: GoTo link exists at rect (72, 750, 200, 765) pointing to page 10 (0.35 pts)
               - Partial (0.20): GoTo link exists anywhere on page 1 pointing to page 10
               - Full (0.35): GoTo link at correct rect AND target page 10
Total: 1.0
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_190'
TARGET_FILE = f'{WORKDIR}/Documents/linked_doc.pdf'

# Expected link specifications
EXPECTED_NUM_PAGES = 15
EXPECTED_LINK_COUNT_PAGE1 = 2

GOTO_RECT_EXPECTED = pymupdf.Rect(72, 750, 200, 765)
GOTO_TARGET_PAGE = 9   # 0-indexed (page 10 in 1-indexed)

URI_RECT_EXPECTED = pymupdf.Rect(72, 730, 300, 745)
URI_TARGET = 'https://www.example.com/resources'

RECT_TOLERANCE = 3.0  # points tolerance for rect comparison


def rects_close(r1, r2, tol=RECT_TOLERANCE):
    """Return True if two Rect objects are within tolerance of each other."""
    return (abs(r1.x0 - r2.x0) <= tol and
            abs(r1.y0 - r2.y0) <= tol and
            abs(r1.x1 - r2.x1) <= tol and
            abs(r1.y1 - r2.y1) <= tol)


def verify_task(file_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be openable
    if not os.path.exists(file_path):
        print(f"FAIL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count
    print(f"INFO: Opened {file_path} — {page_count} pages")

    # Component 1: Page count == 15 (0.10 points)
    try:
        if page_count == EXPECTED_NUM_PAGES:
            print(f"PASS: Page count == {EXPECTED_NUM_PAGES} (+0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Expected {EXPECTED_NUM_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 (page count) — {e}")

    # Get all links on page 1
    try:
        page1 = doc[0]
        links = page1.get_links()
        print(f"INFO: Page 1 has {len(links)} link(s)")
        for lnk in links:
            print(f"  kind={lnk.get('kind')}, from={lnk.get('from')}, "
                  f"uri='{lnk.get('uri', '')}', page={lnk.get('page', 'N/A')}")
    except Exception as e:
        print(f"ERROR: Cannot read links from page 1 — {e}")
        doc.close()
        print(f"REWARD: {total_score:.2f}")
        return round(total_score, 2)

    # Component 2: Exactly 2 link annotations on page 1 (0.20 points)
    try:
        if len(links) == EXPECTED_LINK_COUNT_PAGE1:
            print(f"PASS: Page 1 has exactly {EXPECTED_LINK_COUNT_PAGE1} links (+0.20 pts)")
            total_score += 0.20
        elif len(links) >= 2:
            # Has at least 2 links (might have extra)
            print(f"PARTIAL: Page 1 has {len(links)} links (expected {EXPECTED_LINK_COUNT_PAGE1}), "
                  f"partial credit (+0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Page 1 has {len(links)} links, expected {EXPECTED_LINK_COUNT_PAGE1}")
    except Exception as e:
        print(f"ERROR: Component 2 (link count) — {e}")

    # Separate URI links and GoTo links
    uri_links = [l for l in links if l.get('kind') == pymupdf.LINK_URI]
    goto_links = [l for l in links if l.get('kind') == pymupdf.LINK_GOTO]

    # Component 3: URI link at correct rect pointing to correct URL (0.35 points)
    try:
        # Check if any URI link points to the correct URL
        correct_url_links = [l for l in uri_links if l.get('uri', '') == URI_TARGET]

        if correct_url_links:
            # Check if one is at the correct rect
            lnk_from_rects = [pymupdf.Rect(l['from']) if isinstance(l['from'], (tuple, list))
                              else l['from'] for l in correct_url_links]
            at_correct_rect = any(rects_close(r, URI_RECT_EXPECTED) for r in lnk_from_rects)

            if at_correct_rect:
                print(f"PASS: URI link at correct rect {URI_RECT_EXPECTED} pointing to "
                      f"'{URI_TARGET}' (+0.35 pts)")
                total_score += 0.35
            else:
                print(f"PARTIAL: URI link to '{URI_TARGET}' exists but at wrong rect "
                      f"(expected {URI_RECT_EXPECTED}) (+0.20 pts)")
                total_score += 0.20
        elif uri_links:
            # Has URI links but wrong URL
            print(f"FAIL: URI links exist but none point to '{URI_TARGET}'. "
                  f"Found URIs: {[l.get('uri') for l in uri_links]}")
        else:
            print(f"FAIL: No URI link found on page 1 (expected URI: '{URI_TARGET}')")
    except Exception as e:
        print(f"ERROR: Component 3 (URI link) — {e}")

    # Component 4: GoTo link at correct rect pointing to page 10 (0.35 points)
    try:
        # Check if any GoTo link points to correct page (0-indexed: 9 = page 10)
        correct_page_goto_links = [
            l for l in goto_links
            if l.get('page') == GOTO_TARGET_PAGE
        ]

        if correct_page_goto_links:
            # Check if one is at the correct rect
            lnk_from_rects = [pymupdf.Rect(l['from']) if isinstance(l['from'], (tuple, list))
                              else l['from'] for l in correct_page_goto_links]
            at_correct_rect = any(rects_close(r, GOTO_RECT_EXPECTED) for r in lnk_from_rects)

            if at_correct_rect:
                print(f"PASS: GoTo link at correct rect {GOTO_RECT_EXPECTED} pointing to "
                      f"page {GOTO_TARGET_PAGE + 1} (0-indexed: {GOTO_TARGET_PAGE}) (+0.35 pts)")
                total_score += 0.35
            else:
                print(f"PARTIAL: GoTo link to page {GOTO_TARGET_PAGE + 1} exists but at wrong rect "
                      f"(expected {GOTO_RECT_EXPECTED}) (+0.20 pts)")
                total_score += 0.20
        elif goto_links:
            # Has GoTo links but wrong page
            target_pages = [l.get('page') for l in goto_links]
            print(f"FAIL: GoTo links exist but none target page 10 (0-indexed: 9). "
                  f"Found targets (0-indexed): {target_pages}")
        else:
            print(f"FAIL: No GoTo link found on page 1 (expected target: page 10)")
    except Exception as e:
        print(f"ERROR: Component 4 (GoTo link) — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore breakdown: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
