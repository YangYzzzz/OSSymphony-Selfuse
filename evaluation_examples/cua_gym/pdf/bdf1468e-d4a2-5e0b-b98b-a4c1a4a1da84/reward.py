"""
Reward Script: Combine trial exhibits with Bates numbering
Task ID: pdf_legal_018
Domain: pdf
Scoring:
  Component 1 (0.25): Combined file exists with 25 pages
  Component 2 (0.35): Correct Bates numbers PL-EX-0001 through PL-EX-0025
  Component 3 (0.15): Bates numbers positioned at bottom-right of each page
  Component 4 (0.25): 3 bookmarks with correct titles and page targets
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_018'
COMBINED_PATH = os.path.join(WORKDIR, 'legal', 'trial', 'plaintiff_exhibits_combined.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Combined file has exactly 25 pages (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 25:
            print(f"PASS: Component 1 — Page count is 25 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 25 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct Bates numbers PL-EX-0001 through PL-EX-0025 (0.35 points)
    try:
        bates_correct = 0
        bates_total = 25
        for i in range(min(doc.page_count, 25)):
            page = doc[i]
            text = page.get_text()
            expected_bates = f"PL-EX-{i+1:04d}"
            if expected_bates in text:
                bates_correct += 1
            else:
                # Check with regex for any PL-EX number on this page
                found = re.findall(r'PL-EX-\d+', text)
                print(f"  Page {i+1}: Expected {expected_bates}, found {found}")

        if bates_correct == bates_total:
            print(f"PASS: Component 2 — All 25 Bates numbers correct (0.35 pts)")
            total_score += 0.35
        elif bates_correct > 0:
            partial = 0.35 * (bates_correct / bates_total)
            print(f"PARTIAL: Component 2 — {bates_correct}/{bates_total} Bates numbers correct ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No correct Bates numbers found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bates numbers positioned at bottom-right (0.15 points)
    # Bottom-right means: x > 60% of page width AND y > 85% of page height
    try:
        position_correct = 0
        pages_checked = min(doc.page_count, 25)
        for i in range(pages_checked):
            page = doc[i]
            page_w = page.rect.width
            page_h = page.rect.height
            blocks = page.get_text('dict')['blocks']
            for block in blocks:
                if 'lines' not in block:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        if re.match(r'PL-EX-\d{4}', span['text']):
                            bbox = span['bbox']
                            # bbox[0] is x-left, bbox[1] is y-top
                            x_left = bbox[0]
                            y_top = bbox[1]
                            if x_left > page_w * 0.6 and y_top > page_h * 0.85:
                                position_correct += 1

        if position_correct == pages_checked:
            print(f"PASS: Component 3 — All Bates numbers at bottom-right (0.15 pts)")
            total_score += 0.15
        elif position_correct > 0:
            partial = 0.15 * (position_correct / pages_checked)
            print(f"PARTIAL: Component 3 — {position_correct}/{pages_checked} positioned correctly ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Bates numbers not at bottom-right")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bookmarks (TOC) with correct titles and page targets (0.25 points)
    try:
        toc = doc.get_toc()
        expected_toc = [
            [1, 'Plaintiff Exhibit 1', 1],
            [1, 'Plaintiff Exhibit 2', 9],
            [1, 'Plaintiff Exhibit 3', 21],
        ]

        if len(toc) >= 3:
            bookmark_score = 0.0
            matched = 0
            for expected in expected_toc:
                for entry in toc:
                    if (expected[1].lower().strip() in entry[1].lower().strip()
                            and entry[2] == expected[2]):
                        matched += 1
                        break

            if matched == 3:
                print(f"PASS: Component 4 — All 3 bookmarks correct (0.25 pts)")
                total_score += 0.25
            elif matched > 0:
                partial = 0.25 * (matched / 3)
                print(f"PARTIAL: Component 4 — {matched}/3 bookmarks correct ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No matching bookmarks. Found: {toc}")
        else:
            print(f"FAIL: Component 4 — Expected 3 bookmarks, found {len(toc)}: {toc}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMBINED_PATH):
    print(f"File not found: {COMBINED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(COMBINED_PATH)
