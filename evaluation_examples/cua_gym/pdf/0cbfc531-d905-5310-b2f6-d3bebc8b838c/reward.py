"""
Reward Script: Bates numbering on two exhibit sets and merge with bookmarks
Task ID: pdf_legal_078
Domain: pdf
Scoring:
  Component 1 (0.15): Combined file exists with 35 pages
  Component 2 (0.30): Bates PLEX-A-0001..0020 on pages 1-20 of combined
  Component 3 (0.25): Bates PLEX-B-0001..0015 on pages 21-35 of combined
  Component 4 (0.15): Bookmarks 'Exhibit Set A' (pg 1) and 'Exhibit Set B' (pg 21)
  Component 5 (0.15): Individual set_a.pdf and set_b.pdf have Bates stamps
"""

import os
import re

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
COMBINED_PATH = os.path.join(WORKDIR, 'legal', 'exhibits', 'combined_exhibits_bates.pdf')
SET_A_PATH = os.path.join(WORKDIR, 'legal', 'exhibits', 'set_a.pdf')
SET_B_PATH = os.path.join(WORKDIR, 'legal', 'exhibits', 'set_b.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Combined file exists with 35 pages (0.15 points)
    try:
        if not os.path.exists(COMBINED_PATH):
            print(f"FAIL: Component 1 — combined file not found at {COMBINED_PATH}")
            print("REWARD: 0.0")
            return 0.0
        doc = pymupdf.open(COMBINED_PATH)
        page_count = doc.page_count
        if page_count == 35:
            print(f"PASS: Component 1 — combined file has 35 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected 35 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Bates PLEX-A-0001..0020 on pages 1-20 of combined (0.30 points)
    try:
        matches_a = 0
        for i in range(min(20, doc.page_count)):
            page = doc[i]
            text = page.get_text("text")
            expected_bates = f"PLEX-A-{i+1:04d}"
            if expected_bates in text:
                matches_a += 1
            else:
                print(f"  DETAIL: Page {i+1} missing {expected_bates}")
        if matches_a == 20:
            print(f"PASS: Component 2 — all 20 Set A Bates numbers present (0.30 pts)")
            total_score += 0.30
        elif matches_a > 0:
            partial = round(0.30 * matches_a / 20, 4)
            print(f"PARTIAL: Component 2 — {matches_a}/20 Set A Bates found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no Set A Bates numbers found on pages 1-20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bates PLEX-B-0001..0015 on pages 21-35 of combined (0.25 points)
    try:
        matches_b = 0
        for i in range(20, min(35, doc.page_count)):
            page = doc[i]
            text = page.get_text("text")
            b_num = i - 20 + 1
            expected_bates = f"PLEX-B-{b_num:04d}"
            if expected_bates in text:
                matches_b += 1
            else:
                print(f"  DETAIL: Page {i+1} missing {expected_bates}")
        if matches_b == 15:
            print(f"PASS: Component 3 — all 15 Set B Bates numbers present (0.25 pts)")
            total_score += 0.25
        elif matches_b > 0:
            partial = round(0.25 * matches_b / 15, 4)
            print(f"PARTIAL: Component 3 — {matches_b}/15 Set B Bates found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no Set B Bates numbers found on pages 21-35")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bookmarks (0.15 points)
    try:
        toc = doc.get_toc()
        bookmark_a_ok = any('Exhibit Set A' in e[1] and e[2] == 1 for e in toc)
        bookmark_b_ok = any('Exhibit Set B' in e[1] and e[2] == 21 for e in toc)

        if bookmark_a_ok and bookmark_b_ok:
            print(f"PASS: Component 4 — both bookmarks correct (0.15 pts)")
            total_score += 0.15
        elif bookmark_a_ok or bookmark_b_ok:
            print(f"PARTIAL: Component 4 — only one bookmark correct (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 4 — bookmarks missing or incorrect. TOC: {toc}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    # Component 5: Individual stamped files have Bates (0.15 points)
    try:
        sub_score = 0.0
        # Check set_a.pdf
        if os.path.exists(SET_A_PATH):
            doc_a = pymupdf.open(SET_A_PATH)
            a_first = 'PLEX-A-0001' in doc_a[0].get_text("text")
            a_last = f'PLEX-A-{doc_a.page_count:04d}' in doc_a[doc_a.page_count - 1].get_text("text")
            doc_a.close()
            if a_first and a_last:
                sub_score += 0.075
                print(f"  set_a.pdf: Bates stamps verified on first and last pages")
            else:
                print(f"  set_a.pdf: Bates stamps missing (first={a_first}, last={a_last})")
        else:
            print(f"  set_a.pdf not found")

        # Check set_b.pdf
        if os.path.exists(SET_B_PATH):
            doc_b = pymupdf.open(SET_B_PATH)
            b_first = 'PLEX-B-0001' in doc_b[0].get_text("text")
            b_last = f'PLEX-B-{doc_b.page_count:04d}' in doc_b[doc_b.page_count - 1].get_text("text")
            doc_b.close()
            if b_first and b_last:
                sub_score += 0.075
                print(f"  set_b.pdf: Bates stamps verified on first and last pages")
            else:
                print(f"  set_b.pdf: Bates stamps missing (first={b_first}, last={b_last})")
        else:
            print(f"  set_b.pdf not found")

        if sub_score > 0:
            print(f"PASS: Component 5 — individual files stamped ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 — individual files not stamped")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
