"""
Reward Script: Overlay letterhead onto financial memo
Task ID: pdf_fin_056
Domain: pdf
Scoring:
  Component 1 (0.3): memo_final.pdf has exactly 4 pages
  Component 2 (0.4): Every page contains letterhead text (background overlay applied)
  Component 3 (0.3): Every page retains original memo content (foreground preserved)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_056'

# Expected paths
FINAL_PATH = os.path.join(WORKDIR, 'finance', 'memo_final.pdf')
DRAFT_PATH = os.path.join(WORKDIR, 'finance', 'memo_draft.pdf')
LETTERHEAD_PATH = os.path.join(WORKDIR, 'finance', 'templates', 'letterhead.pdf')

# Letterhead marker text (present on letterhead template)
LETTERHEAD_MARKER = 'MERIDIAN CAPITAL PARTNERS'

# Per-page memo content markers from the original draft
MEMO_PAGE_MARKERS = [
    'CONFIDENTIAL FINANCIAL MEMO',
    'PORTFOLIO PERFORMANCE SUMMARY',
    'RISK MANAGEMENT UPDATE',
    'Q2 2025 OUTLOOK',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: memo_final.pdf must exist (precondition, no points)
    if not os.path.exists(FINAL_PATH):
        print(f"CRITICAL: Output file not found: {FINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(FINAL_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open {FINAL_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: memo_final.pdf has exactly 4 pages (0.3 points)
    # The draft has 4 pages; the merged output should preserve all 4.
    try:
        if page_count == 4:
            print(f"PASS: Component 1 — Page count is 4 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every page contains letterhead text (0.4 points)
    # The letterhead should be overlaid as background on every page.
    # Award partial credit per page: 0.1 per page.
    try:
        letterhead_pages_pass = 0
        for i in range(min(page_count, 4)):
            text = doc[i].get_text()
            if LETTERHEAD_MARKER in text:
                letterhead_pages_pass += 1
                print(f"  Page {i}: letterhead text found")
            else:
                print(f"  Page {i}: letterhead text NOT found")

        if letterhead_pages_pass == 4:
            print(f"PASS: Component 2 — Letterhead on all 4 pages (0.4 pts)")
            total_score += 0.4
        elif letterhead_pages_pass > 0:
            partial = round(0.1 * letterhead_pages_pass, 2)
            print(f"PARTIAL: Component 2 — Letterhead on {letterhead_pages_pass}/4 pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Letterhead text not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Every page retains original memo content (0.3 points)
    # Each page should still contain the corresponding memo section.
    # Award partial credit per page: 0.075 per page.
    try:
        memo_pages_pass = 0
        for i in range(min(page_count, 4)):
            text = doc[i].get_text()
            if MEMO_PAGE_MARKERS[i] in text:
                memo_pages_pass += 1
                print(f"  Page {i}: memo content '{MEMO_PAGE_MARKERS[i]}' found")
            else:
                print(f"  Page {i}: memo content '{MEMO_PAGE_MARKERS[i]}' NOT found")

        if memo_pages_pass == 4:
            print(f"PASS: Component 3 — Memo content preserved on all 4 pages (0.3 pts)")
            total_score += 0.3
        elif memo_pages_pass > 0:
            partial = round(0.075 * memo_pages_pass, 3)
            print(f"PARTIAL: Component 3 — Memo content on {memo_pages_pass}/4 pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Original memo content not found on any page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FINAL_PATH):
    print(f"File not found: {FINAL_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
