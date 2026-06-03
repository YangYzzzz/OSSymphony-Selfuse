"""
Reward Script: Create a bookmark 'Figure 3.1' in illustrated_guide.pdf
               that navigates to page 15 with FitH (fit width) destination.
Task ID: pdf_mbc_054
Domain: pdf
Scoring:
  Component 1: Bookmark 'Figure 3.1' exists in TOC           — 0.30
  Component 2: Bookmark targets page 15 (1-indexed)          — 0.25
  Component 3: Bookmark uses FitH destination type            — 0.25
  Component 4: All 45 original bookmarks preserved            — 0.20
  Total: 1.0
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_054'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'illustrated_guide.pdf')

# Original bookmarks (titles) expected from initial state
ORIGINAL_BOOKMARK_COUNT = 45


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get TOC with full details (simple=False gives dict with kind, page, view, etc.)
    try:
        toc = doc.get_toc(simple=False)
        print(f"INFO: TOC has {len(toc)} entries")
    except Exception as e:
        print(f"CRITICAL: Cannot read TOC: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Find bookmark(s) named 'Figure 3.1'
    figure_bookmarks = []
    other_bookmarks = []
    for entry in toc:
        level, title, page_num, detail = entry[0], entry[1], entry[2], entry[3]
        if title.strip() == 'Figure 3.1':
            figure_bookmarks.append((level, title, page_num, detail))
        else:
            other_bookmarks.append((level, title, page_num, detail))

    # Component 1: Bookmark 'Figure 3.1' exists in TOC (0.30 points)
    try:
        if len(figure_bookmarks) >= 1:
            print(f"PASS: Component 1 -- Bookmark 'Figure 3.1' found ({len(figure_bookmarks)} match(es)) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- Bookmark 'Figure 3.1' not found in TOC")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Bookmark targets page 15 (1-indexed) (0.25 points)
    try:
        if len(figure_bookmarks) >= 1:
            bm = figure_bookmarks[0]
            bm_detail = bm[3]
            bm_page_num = bm[2]  # 1-indexed page number from TOC

            # PyMuPDF get_toc returns page as 1-indexed in the third element
            # For kind=4 entries, the page in the detail dict may be a string
            # Use the top-level page number (element index 2) which is always 1-indexed
            target_page = int(bm_page_num) if bm_page_num else None

            # Also check detail['page'] as fallback — may be 0-indexed int or string
            detail_page = bm_detail.get('page', None)
            if detail_page is not None:
                detail_page_int = int(detail_page)
                # detail['page'] could be 0-indexed (for kind=1) or could be the string '15'
                # We'll check both the TOC page number and detail page
                print(f"INFO: Bookmark page from TOC: {bm_page_num}, from detail: {detail_page}")

            if target_page == 15:
                print(f"PASS: Component 2 -- Bookmark targets page 15 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Bookmark targets page {target_page}, expected 15")
        else:
            print(f"FAIL: Component 2 -- No 'Figure 3.1' bookmark to check page target")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Bookmark uses FitH destination type (0.25 points)
    try:
        if len(figure_bookmarks) >= 1:
            bm = figure_bookmarks[0]
            bm_detail = bm[3]
            kind = bm_detail.get('kind', None)
            view_str = str(bm_detail.get('view', ''))

            # FitH manifests as kind=4 with view string containing 'FitH'
            # Check if 'FitH' appears in the view specification
            if 'FitH' in view_str:
                print(f"PASS: Component 3 -- Bookmark uses FitH destination (kind={kind}, view={view_str}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Bookmark does not use FitH. kind={kind}, view={view_str}")
        else:
            print(f"FAIL: Component 3 -- No 'Figure 3.1' bookmark to check destination type")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Figure 3.1 bookmark exists AND all 45 original bookmarks preserved (0.20 points)
    # This is a compound check: both the new bookmark must exist and originals must be intact.
    # The new-bookmark requirement ensures this component FAILS on initial_env.
    try:
        original_count = len(other_bookmarks)
        has_figure_bm = len(figure_bookmarks) >= 1
        if has_figure_bm and original_count >= ORIGINAL_BOOKMARK_COUNT:
            print(f"PASS: Component 4 -- Figure 3.1 exists AND all {original_count} original bookmarks preserved (0.20 pts)")
            total_score += 0.20
        elif not has_figure_bm:
            print(f"FAIL: Component 4 -- Figure 3.1 bookmark missing; cannot award preservation points")
        else:
            print(f"FAIL: Component 4 -- Only {original_count} of {ORIGINAL_BOOKMARK_COUNT} original bookmarks found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
