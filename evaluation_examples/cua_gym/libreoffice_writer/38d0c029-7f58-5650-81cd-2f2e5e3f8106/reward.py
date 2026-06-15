"""
Reward Script: Apply 3-column layout to Features section only
Task ID: writer_rd_084
Domain: libreoffice_writer
Scoring:
  C1 (0.25) - Document has 3 sections (continuous section breaks)
  C2 (0.30) - Middle section has 3 columns
  C3 (0.20) - Middle section has separator lines and ~0.4cm spacing
  C4 (0.15) - First section remains single-column
  C5 (0.10) - Last section remains single-column
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_084'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice edits."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for %s" % domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: %s" % e)


def verify_task(file_path):
    """
    Verify that the Features section has 3-column layout while
    Introduction and Conclusion remain single-column.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError as e:
        print("CRITICAL: Missing library: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    num_sections = len(doc.sections)

    # Component 1: Document has 3 sections (0.25 points)
    # Initial has 1 section; golden has 3 (intro, features 3-col, conclusion)
    try:
        if num_sections >= 3:
            print("PASS: Component 1 — Document has %d sections (>= 3) (0.25 pts)" % num_sections)
            total_score += 0.25
        else:
            print("FAIL: Component 1 — Expected >= 3 sections, found %d" % num_sections)
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Early exit if fewer than 3 sections — remaining checks require it
    if num_sections < 3:
        final_score = min(total_score, 1.0)
        print("\nScore: %.2f/1.0" % total_score)
        print("REWARD: %.1f" % final_score)
        return final_score

    # Helper to get column count from a section
    def get_section_cols(sec):
        """Return (num_cols, space_twips, has_sep) from a section's w:cols element."""
        sectPr = sec._sectPr
        cols_elem = sectPr.find(qn('w:cols'))
        if cols_elem is None:
            return (1, 0, False)
        num_attr = cols_elem.get(qn('w:num'))
        num = int(num_attr) if num_attr else 1
        space_attr = cols_elem.get(qn('w:space'))
        space = int(space_attr) if space_attr else 0
        sep_attr = cols_elem.get(qn('w:sep'))
        has_sep = sep_attr == '1' or sep_attr == 'true'
        return (num, space, has_sep)

    # Component 2: Middle section has 3 columns (0.30 points)
    try:
        mid_cols, mid_space, mid_sep = get_section_cols(doc.sections[1])
        if mid_cols == 3:
            print("PASS: Component 2 — Middle section has 3 columns (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 2 — Expected 3 columns in middle section, found %d" % mid_cols)
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Middle section has separator lines and ~0.4cm spacing (0.20 points)
    # 0.4 cm = ~227 twips (1 cm = 567 twips). Accept range 200-260 twips.
    try:
        mid_cols, mid_space, mid_sep = get_section_cols(doc.sections[1])
        sub_score = 0.0
        # Check separator lines (0.10 of the 0.20)
        if mid_sep:
            print("  PASS: Separator lines enabled in middle section")
            sub_score += 0.10
        else:
            print("  FAIL: No separator lines in middle section")
        # Check spacing (0.10 of the 0.20)
        if 180 <= mid_space <= 300:
            print("  PASS: Column spacing = %d twips (within acceptable range for ~0.4cm)" % mid_space)
            sub_score += 0.10
        else:
            print("  FAIL: Column spacing = %d twips (expected ~226 twips / 0.4cm)" % mid_space)
        if sub_score > 0:
            print("PASS: Component 3 — Separator/spacing checks (%.2f pts)" % sub_score)
            total_score += sub_score
        else:
            print("FAIL: Component 3 — Neither separator nor spacing matched")
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # Component 4: First section remains single-column (0.15 points)
    try:
        first_cols, _, _ = get_section_cols(doc.sections[0])
        if first_cols == 1:
            print("PASS: Component 4 — First section is single-column (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 4 — First section has %d columns, expected 1" % first_cols)
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    # Component 5: Last section remains single-column (0.10 points)
    try:
        last_cols, _, _ = get_section_cols(doc.sections[-1])
        if last_cols == 1:
            print("PASS: Component 5 — Last section is single-column (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 5 — Last section has %d columns, expected 1" % last_cols)
    except Exception as e:
        print("ERROR: Component 5 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
