"""
Reward Script: Merge PDFs, add nested bookmarks, add signature fields
Task ID: pdf_pw_011
Domain: pdf
Scoring:
  Component 1: Merged file exists with 13 pages (0.25 pts)
  Component 2: Two top-level bookmarks with correct names (0.20 pts)
  Component 3: Nested children: 8 body sub-bookmarks + 5 exhibit sub-bookmarks (0.25 pts)
  Component 4: Signature_Party_A form field on last page with ~200x30 size (0.15 pts)
  Component 5: Signature_Party_B form field on last page with ~200x30 size (0.15 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_011'
MERGED_PATH = os.path.join(WORKDIR, 'legal', 'complete_contract.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Merged file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Merged file has 13 pages (0.25 pts)
    # Initial env has no merged file, so this only passes on golden.
    try:
        page_count = doc.page_count
        if page_count == 13:
            print(f"PASS: Component 1 — Merged file has 13 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 13 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Two top-level bookmarks with correct names (0.20 pts)
    # TOC format: [[level, title, page_num], ...]
    try:
        toc = doc.get_toc()
        top_level = [entry for entry in toc if entry[0] == 1]
        top_names = [entry[1] for entry in top_level]

        has_contract_body = any('Contract Body' in name for name in top_names)
        has_exhibits = any('Exhibit' in name for name in top_names)

        if len(top_level) >= 2 and has_contract_body and has_exhibits:
            print(f"PASS: Component 2 — Two top-level bookmarks found: {top_names} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 2 top-level bookmarks (Contract Body, Exhibits), found: {top_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Nested sub-bookmarks (0.25 pts)
    # Contract Body should have sub-bookmarks for each of the 8 original pages.
    # Exhibits should have sub-bookmarks for each of the 5 exhibit pages.
    try:
        toc = doc.get_toc()
        # Find children: entries with level > 1
        children = [entry for entry in toc if entry[0] > 1]
        num_children = len(children)

        # We expect 8 sub-bookmarks under Contract Body + 5 under Exhibits = 13 total children
        # Award partial credit: at least 10 children = full, some = partial
        if num_children >= 13:
            print(f"PASS: Component 3 — {num_children} nested sub-bookmarks found (0.25 pts)")
            total_score += 0.25
        elif num_children >= 8:
            partial = 0.15
            print(f"PARTIAL: Component 3 — {num_children}/13 nested sub-bookmarks ({partial} pts)")
            total_score += partial
        elif num_children >= 2:
            partial = 0.05
            print(f"PARTIAL: Component 3 — {num_children}/13 nested sub-bookmarks ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Expected 13 nested sub-bookmarks, found {num_children}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Signature_Party_A form field on last page (~200x30 pts) (0.15 pts)
    try:
        last_page = doc[-1]
        found_a = False
        for widget in last_page.widgets():
            if widget.field_name == 'Signature_Party_A':
                r = widget.rect
                w = r[2] - r[0]
                h = r[3] - r[1]
                # Check dimensions with tolerance (allow +/- 20 points)
                if abs(w - 200) <= 20 and abs(h - 30) <= 20:
                    found_a = True
                    print(f"PASS: Component 4 — Signature_Party_A found on last page, size {w:.0f}x{h:.0f} (0.15 pts)")
                else:
                    print(f"FAIL: Component 4 — Signature_Party_A found but wrong size: {w:.0f}x{h:.0f} (expected ~200x30)")
                break
        if not found_a and 'Signature_Party_A' not in [w.field_name for w in last_page.widgets()]:
            print(f"FAIL: Component 4 — Signature_Party_A not found on last page")
        if found_a:
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Signature_Party_B form field on last page (~200x30 pts) (0.15 pts)
    try:
        last_page = doc[-1]
        found_b = False
        for widget in last_page.widgets():
            if widget.field_name == 'Signature_Party_B':
                r = widget.rect
                w = r[2] - r[0]
                h = r[3] - r[1]
                if abs(w - 200) <= 20 and abs(h - 30) <= 20:
                    found_b = True
                    print(f"PASS: Component 5 — Signature_Party_B found on last page, size {w:.0f}x{h:.0f} (0.15 pts)")
                else:
                    print(f"FAIL: Component 5 — Signature_Party_B found but wrong size: {w:.0f}x{h:.0f} (expected ~200x30)")
                break
        if not found_b and 'Signature_Party_B' not in [w.field_name for w in last_page.widgets()]:
            print(f"FAIL: Component 5 — Signature_Party_B not found on last page")
        if found_b:
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(MERGED_PATH):
    print(f"File not found: {MERGED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(MERGED_PATH)
