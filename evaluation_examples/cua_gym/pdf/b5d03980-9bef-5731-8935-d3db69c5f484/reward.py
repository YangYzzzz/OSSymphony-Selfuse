"""
Reward Script: PDF stamp overlay template creation and application
Task ID: pdf_aw_040
Domain: pdf

Scoring rubric:
  Component 1: Stamp template exists with correct page size ~5x3 cm       (0.15)
  Component 2: Stamp template has 'APPROVED' text, bold, ~36pt, green     (0.15)
  Component 3: Stamp template has a green rounded-rectangle border drawing (0.10)
  Component 4: Proposal PDF still has all 12 pages                        (0.10)
  Component 5: Pages 1,5,10 (idx 0,4,9) contain 'APPROVED' text overlay  (0.25)
  Component 6: Non-stamped pages do NOT contain 'APPROVED' text           (0.15)
  Component 7: Stamp is positioned in the top-right corner area           (0.10)
  Total: 1.0
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_040'

STAMP_PATH = os.path.join(WORKDIR, 'templates', 'approved_stamp.pdf')
PROPOSAL_PATH = os.path.join(WORKDIR, 'docs', 'proposal.pdf')

# Pages that should have the stamp (1-indexed: 1, 5, 10 -> 0-indexed: 0, 4, 9)
STAMPED_PAGES = {0, 4, 9}
EXPECTED_PAGE_COUNT = 12


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # === PRECONDITION: Both files must exist ===
    if not os.path.exists(STAMP_PATH):
        print(f"CRITICAL: Stamp template not found at {STAMP_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(PROPOSAL_PATH):
        print(f"CRITICAL: Proposal PDF not found at {PROPOSAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # ============================================================
    # Component 1: Stamp template page size ~5x3 cm (0.15 points)
    # 5 cm = ~141.73 pts, 3 cm = ~85.04 pts (72 pts/inch, 2.54 cm/inch)
    # ============================================================
    try:
        stamp_doc = fitz.open(STAMP_PATH)
        if stamp_doc.page_count >= 1:
            sp = stamp_doc[0]
            w_cm = sp.rect.width / 72 * 2.54
            h_cm = sp.rect.height / 72 * 2.54
            # Allow 10% tolerance on dimensions
            w_ok = 4.5 <= w_cm <= 5.5
            h_ok = 2.7 <= h_cm <= 3.3
            if w_ok and h_ok:
                print(f"PASS: Component 1 - Stamp template size {w_cm:.2f}x{h_cm:.2f} cm (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 - Stamp size {w_cm:.2f}x{h_cm:.2f} cm, expected ~5x3 cm")
        else:
            print("FAIL: Component 1 - Stamp template has no pages")
        stamp_doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # ============================================================
    # Component 2: Stamp has 'APPROVED' text, bold, ~36pt, green (0.15 pts)
    # ============================================================
    try:
        stamp_doc = fitz.open(STAMP_PATH)
        sp = stamp_doc[0]
        text = sp.get_text()
        has_approved_text = 'APPROVED' in text

        # Check text properties via dict blocks
        approved_bold_green = False
        blocks = sp.get_text('dict')['blocks']
        for b in blocks:
            if b.get('type') != 0:
                continue
            for line in b.get('lines', []):
                for span in line.get('spans', []):
                    if 'APPROVED' in span.get('text', ''):
                        sz = span.get('size', 0)
                        font = span.get('font', '')
                        color_int = int(span.get('color', 0))
                        # Green color: check that green channel is dominant
                        r = (color_int >> 16) & 0xFF
                        g = (color_int >> 8) & 0xFF
                        b_val = color_int & 0xFF
                        is_green = g > 100 and g > r and g > b_val
                        is_bold = 'Bold' in font or 'bold' in font or 'Bo' in font
                        is_right_size = 30 <= sz <= 42
                        if is_green and is_bold and is_right_size:
                            approved_bold_green = 1  # verified via API

        if has_approved_text and approved_bold_green:
            print(f"PASS: Component 2 - Stamp has bold green 'APPROVED' text (0.15 pts)")
            total_score += 0.15
        elif has_approved_text:
            print(f"FAIL: Component 2 - 'APPROVED' text found but style mismatch (bold/green/size)")
        else:
            print(f"FAIL: Component 2 - No 'APPROVED' text in stamp template")
        stamp_doc.close()
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ============================================================
    # Component 3: Stamp has green rounded-rectangle border drawing (0.10 pts)
    # ============================================================
    try:
        stamp_doc = fitz.open(STAMP_PATH)
        sp = stamp_doc[0]
        drawings = sp.get_drawings()
        has_green_border = False
        for d in drawings:
            color = d.get('color')
            if color is not None:
                # Green color: color is (R, G, B) floats 0-1
                if isinstance(color, (tuple, list)) and len(color) >= 3:
                    r, g, b_val = color[0], color[1], color[2]
                    if g > 0.3 and g > r and g > b_val:
                        has_green_border = 1  # verified via API
                        break

        if has_green_border:
            print(f"PASS: Component 3 - Green border drawing found in stamp (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - No green border drawing found in stamp (found {len(drawings)} drawings)")
        stamp_doc.close()
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ============================================================
    # Component 4: Proposal still has 12 pages (0.10 pts)
    # ============================================================
    try:
        doc = fitz.open(PROPOSAL_PATH)
        pc = doc.page_count
        if pc == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 4 - Proposal has {pc} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - Proposal has {pc} pages, expected {EXPECTED_PAGE_COUNT}")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # ============================================================
    # Component 5: Pages 1,5,10 have 'APPROVED' text overlay (0.25 pts)
    # Each stamped page contributes equally: ~0.0833 pts
    # ============================================================
    try:
        doc = fitz.open(PROPOSAL_PATH)
        stamped_count = 0
        for pg_idx in sorted(STAMPED_PAGES):
            page = doc[pg_idx]
            text = page.get_text()
            if 'APPROVED' in text:
                stamped_count += 1
                print(f"  Page {pg_idx+1}: APPROVED text found")
            else:
                print(f"  Page {pg_idx+1}: APPROVED text NOT found")

        if stamped_count == len(STAMPED_PAGES):
            print(f"PASS: Component 5 - All {stamped_count}/{len(STAMPED_PAGES)} stamped pages have APPROVED (0.25 pts)")
            total_score += 0.25
        elif stamped_count > 0:
            partial = round(0.25 * stamped_count / len(STAMPED_PAGES), 4)
            print(f"PARTIAL: Component 5 - {stamped_count}/{len(STAMPED_PAGES)} stamped pages have APPROVED ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No stamped pages have APPROVED text")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # ============================================================
    # Component 6: Non-stamped pages do NOT have 'APPROVED' text (0.15 pts)
    # ============================================================
    try:
        doc = fitz.open(PROPOSAL_PATH)
        clean_pages = 0
        non_stamped = set(range(EXPECTED_PAGE_COUNT)) - STAMPED_PAGES
        for pg_idx in sorted(non_stamped):
            page = doc[pg_idx]
            text = page.get_text()
            if 'APPROVED' not in text:
                clean_pages += 1
            else:
                print(f"  Page {pg_idx+1}: Unexpected APPROVED text found")

        expected_clean = len(non_stamped)
        if clean_pages == expected_clean:
            print(f"PASS: Component 6 - All {clean_pages} non-stamped pages are clean (0.15 pts)")
            total_score += 0.15
        elif clean_pages > 0:
            partial = round(0.15 * clean_pages / expected_clean, 4)
            print(f"PARTIAL: Component 6 - {clean_pages}/{expected_clean} non-stamped pages are clean ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 - APPROVED text found on non-stamped pages")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # ============================================================
    # Component 7: Stamp positioned in top-right corner on stamped pages (0.10 pts)
    # Page is 612x792 pts. Top-right means the APPROVED text bbox should be
    # in the right half (x > 300) and upper portion (y < 200) of the page.
    # ============================================================
    try:
        doc = fitz.open(PROPOSAL_PATH)
        positioned_ok = 0
        for pg_idx in sorted(STAMPED_PAGES):
            page = doc[pg_idx]
            blocks = page.get_text('dict')['blocks']
            found_tr = False
            for bl in blocks:
                if bl.get('type') != 0:
                    continue
                for line in bl.get('lines', []):
                    for span in line.get('spans', []):
                        if 'APPROVED' in span.get('text', ''):
                            bbox = span.get('bbox', (0, 0, 0, 0))
                            # bbox = (x0, y0, x1, y1)
                            x0, y0, x1, y1 = bbox
                            # Right half: x0 > 300 (page width 612)
                            # Upper area: at least part of bbox in top third (y0 < 300)
                            if x0 > 300 and y0 < 300:
                                found_tr = 1  # verified via API
            if found_tr:
                positioned_ok += 1
                print(f"  Page {pg_idx+1}: Stamp positioned in top-right")
            else:
                print(f"  Page {pg_idx+1}: Stamp NOT in top-right position")

        if positioned_ok == len(STAMPED_PAGES):
            print(f"PASS: Component 7 - All stamps in top-right corner (0.10 pts)")
            total_score += 0.10
        elif positioned_ok > 0:
            partial = round(0.10 * positioned_ok / len(STAMPED_PAGES), 4)
            print(f"PARTIAL: Component 7 - {positioned_ok}/{len(STAMPED_PAGES)} stamps in top-right ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 - No stamps found in top-right position")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
