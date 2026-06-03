"""
Reward Script: Add page numbers '[N/20]' at bottom center starting from page 3
Task ID: pdf_adv_193
Domain: pdf
Scoring:
  - Component 1: PDF has exactly 20 pages            (0.10 pts)
  - Component 2: Pages 1-2 have no page numbers      (0.20 pts)
  - Component 3: Pages 3-20 each have correct [N/20] (0.50 pts, per-page partial)
  - Component 4: Page numbers are at bottom center   (0.20 pts)
  Total: 1.0
"""

import os
import re

# Try both import names (pymupdf >= 1.24 canonical; fitz is legacy alias)
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_193'
CANONICAL_PATH = '/home/user/Documents/spec_doc_numbered.pdf'
FALLBACK_PATH  = '/home/user/pdf_adv_193_numbered.pdf'

TOTAL_PAGES = 20
# Pages 3-20 must have page numbers; pages 1-2 must not.
NUMBERED_PAGES = list(range(3, 21))   # 1-indexed: 3..20


def verify_task(file_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: open the PDF ---
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: Page count (0.10 pts)
    # Pages 1-2 must have no page numbers; the PDF must remain 20 pages.
    # ------------------------------------------------------------------
    try:
        pc = doc.page_count
        if pc == TOTAL_PAGES:
            print(f"PASS: Component 1 — page count is {pc} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — expected {TOTAL_PAGES} pages, found {pc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Pages 1-2 have NO page number annotations (0.20 pts)
    # Passes only if NEITHER page 1 nor page 2 contains [N/20] pattern.
    # ------------------------------------------------------------------
    try:
        pages_without_numbers = 0
        for page_idx in range(2):           # 0-indexed → pages 1 and 2
            page = doc[page_idx]
            text = page.get_text("text")
            # Look for any [N/20] pattern
            matches = re.findall(r'\[\d+/20\]', text)
            if not matches:
                pages_without_numbers += 1
            else:
                print(f"FAIL: Component 2 — page {page_idx + 1} unexpectedly "
                      f"contains page number(s): {matches}")
        if pages_without_numbers == 2:
            print("PASS: Component 2 — pages 1-2 have no page numbers (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — only {pages_without_numbers}/2 unnumbered pages correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Pages 3-20 each have the correct [N/20] label (0.50 pts)
    # Partial credit: each correct page earns 0.50 / 18.
    # ------------------------------------------------------------------
    try:
        per_page_score = 0.50 / 18
        correct_pages = 0
        for page_num in NUMBERED_PAGES:   # 1-indexed 3..20
            page_idx = page_num - 1       # 0-indexed
            page = doc[page_idx]
            text = page.get_text("text")
            expected_label = f"[{page_num}/20]"
            if expected_label in text:
                correct_pages += 1
            else:
                print(f"FAIL: Component 3 — page {page_num} does not contain '{expected_label}'")
        component3_score = round(correct_pages * per_page_score, 6)
        if correct_pages > 0:
            total_score += component3_score
        print(f"{'PASS' if correct_pages == 18 else 'PARTIAL'}: "
              f"Component 3 — {correct_pages}/18 pages have correct labels "
              f"({component3_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Page numbers are at bottom center (0.20 pts)
    # Check that each [N/20] label on pages 3-20 is:
    #   (a) in the bottom 15% of the page (y_center > page_height * 0.85)
    #   (b) horizontally centered within 60 pts of the page midpoint
    # Partial credit: same per-page fraction as Component 3.
    # ------------------------------------------------------------------
    try:
        per_page_score_pos = 0.20 / 18
        correct_position = 0
        for page_num in NUMBERED_PAGES:
            page_idx = page_num - 1
            page = doc[page_idx]
            pw = page.rect.width
            ph = page.rect.height
            label = f"[{page_num}/20]"
            instances = page.search_for(label)
            if not instances:
                print(f"FAIL: Component 4 — page {page_num}: '{label}' not found for position check")
                continue
            rect = instances[0]
            cx = (rect.x0 + rect.x1) / 2
            cy = (rect.y0 + rect.y1) / 2
            is_bottom = cy > ph * 0.85
            is_hcentered = abs(cx - pw / 2) < 60   # 60 pt ≈ ~2 cm tolerance
            if is_bottom and is_hcentered:
                correct_position += 1
            else:
                print(f"FAIL: Component 4 — page {page_num}: "
                      f"center=({cx:.1f},{cy:.1f}), "
                      f"page=({pw:.0f}x{ph:.0f}), "
                      f"bottom={is_bottom}, hcenter={is_hcentered}")
        component4_score = round(correct_position * per_page_score_pos, 6)
        if correct_position > 0:
            total_score += component4_score
        print(f"{'PASS' if correct_position == 18 else 'PARTIAL'}: "
              f"Component 4 — {correct_position}/18 page numbers at bottom center "
              f"({component4_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# -----------------------------------------------------------------------
# Entrypoint: test against canonical artifact path; fall back if needed.
# -----------------------------------------------------------------------
file_path = CANONICAL_PATH
if not os.path.exists(file_path):
    # Try fallback path (setup-gen may also place a copy here)
    if os.path.exists(FALLBACK_PATH):
        print(f"INFO: Canonical path not found; using fallback: {FALLBACK_PATH}")
        file_path = FALLBACK_PATH
    else:
        print(f"File not found: {file_path}")
        print(f"Also tried: {FALLBACK_PATH}")
        print("REWARD: 0.0")
        import sys
        sys.exit(0)

verify_task(file_path)
