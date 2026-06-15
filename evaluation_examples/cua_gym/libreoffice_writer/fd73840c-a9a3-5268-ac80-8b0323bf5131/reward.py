"""
Reward Script: Add tab stops to table-of-contents entries so page numbers are right-aligned at 15cm
Task ID: osworld_writer_tabstop_002
Domain: libreoffice_writer
Scoring:
  Component 1: All content paragraphs use a tab character to separate section name from page number (0.4 pts)
  Component 2: All content paragraphs have a RIGHT-aligned tab stop at 15cm (0.4 pts)
  Component 3: All content paragraphs have a LEFT-aligned tab stop at 0cm (0.2 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_002'

# Tolerance for tab stop position comparison (EMU). 15cm = 5400000 EMU.
# Allow +/- 720 EMU (~0.02cm) tolerance for rounding.
RIGHT_TAB_TARGET_CM = 15.0
RIGHT_TAB_TARGET_EMU = RIGHT_TAB_TARGET_CM / 2.54 * 914400  # ~5400000
EMU_TOLERANCE = 36000  # ~0.1cm tolerance

# Content paragraph indices in the document (0=title, 1=blank, 2..13=content lines)
CONTENT_PARA_START = 2
EXPECTED_CONTENT_COUNT = 12


def cm_from_emu(emu):
    return emu / 914400 * 2.54


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect content paragraphs (skip title and blank intro para)
    all_paras = doc.paragraphs
    if len(all_paras) < CONTENT_PARA_START + 1:
        print(f"FAIL: Document has too few paragraphs ({len(all_paras)}), expected at least {CONTENT_PARA_START + 1}")
        print("REWARD: 0.0")
        return 0.0

    content_paras = all_paras[CONTENT_PARA_START:]

    # Filter to non-empty paragraphs that represent TOC entries
    toc_paras = [p for p in content_paras if p.text.strip()]
    print(f"INFO: Found {len(toc_paras)} non-empty content paragraphs")

    # -----------------------------------------------------------------------
    # Component 1: Tab character present in each TOC entry (0.4 points)
    # The section name and page number must be separated by a tab (\t),
    # not a plain space. This verifies the structural reformatting of content.
    # -----------------------------------------------------------------------
    try:
        paras_with_tab = [p for p in toc_paras if '\t' in p.text]
        paras_without_tab = [p for p in toc_paras if '\t' not in p.text]
        ratio_tab = len(paras_with_tab) / len(toc_paras) if toc_paras else 0.0

        if ratio_tab == 1.0:
            print(f"PASS: Component 1 — All {len(toc_paras)} content paragraphs contain a tab character (0.4 pts)")
            total_score += 0.4
        elif ratio_tab >= 0.5:
            partial = round(0.4 * ratio_tab, 3)
            print(f"PARTIAL: Component 1 — {len(paras_with_tab)}/{len(toc_paras)} paragraphs have tab character ({partial} pts)")
            print(f"  Missing tab in: {[p.text for p in paras_without_tab]}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {len(paras_with_tab)}/{len(toc_paras)} paragraphs have tab character (expected all)")
            print(f"  Example missing: {[p.text for p in paras_without_tab[:3]]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: RIGHT-aligned tab stop at 15cm on each TOC entry (0.4 points)
    # The page number should be right-aligned at exactly 15cm from the left margin.
    # Target EMU: ~5400000 (15cm / 2.54 * 914400)
    # -----------------------------------------------------------------------
    try:
        paras_with_right_tab = []
        paras_missing_right_tab = []

        for p in toc_paras:
            tab_stops = list(p.paragraph_format.tab_stops)
            has_right_tab = False
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                if ts.alignment == WD_TAB_ALIGNMENT.RIGHT:
                    pos_cm = cm_from_emu(ts.position)
                    if abs(ts.position - RIGHT_TAB_TARGET_EMU) <= EMU_TOLERANCE:
                        has_right_tab = True
                        break
            if has_right_tab:
                paras_with_right_tab.append(p)
            else:
                paras_missing_right_tab.append(p)

        ratio_right = len(paras_with_right_tab) / len(toc_paras) if toc_paras else 0.0

        if ratio_right == 1.0:
            print(f"PASS: Component 2 — All {len(toc_paras)} content paragraphs have RIGHT tab stop at ~15cm (0.4 pts)")
            total_score += 0.4
        elif ratio_right >= 0.5:
            partial = round(0.4 * ratio_right, 3)
            print(f"PARTIAL: Component 2 — {len(paras_with_right_tab)}/{len(toc_paras)} paragraphs have RIGHT tab at 15cm ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {len(paras_with_right_tab)}/{len(toc_paras)} paragraphs have RIGHT tab stop at ~15cm")
            if paras_missing_right_tab:
                # Show what tab stops the first missing para has
                ts_info = [(ts.alignment, cm_from_emu(ts.position)) for ts in paras_missing_right_tab[0].paragraph_format.tab_stops]
                print(f"  First failing para: {repr(paras_missing_right_tab[0].text)}, tab stops: {ts_info}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: LEFT-aligned tab stop at 0cm on each TOC entry (0.2 points)
    # A left tab stop at 0cm anchors the section name at the left margin.
    # -----------------------------------------------------------------------
    try:
        paras_with_left_tab = []
        paras_missing_left_tab = []

        for p in toc_paras:
            tab_stops = list(p.paragraph_format.tab_stops)
            has_left_tab = False
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position <= EMU_TOLERANCE:
                    has_left_tab = True
                    break
            if has_left_tab:
                paras_with_left_tab.append(p)
            else:
                paras_missing_left_tab.append(p)

        ratio_left = len(paras_with_left_tab) / len(toc_paras) if toc_paras else 0.0

        if ratio_left == 1.0:
            print(f"PASS: Component 3 — All {len(toc_paras)} content paragraphs have LEFT tab stop at 0cm (0.2 pts)")
            total_score += 0.2
        elif ratio_left >= 0.5:
            partial = round(0.2 * ratio_left, 3)
            print(f"PARTIAL: Component 3 — {len(paras_with_left_tab)}/{len(toc_paras)} paragraphs have LEFT tab at 0cm ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(paras_with_left_tab)}/{len(toc_paras)} paragraphs have LEFT tab stop at 0cm")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in this env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
