"""
Reward Script: Create a 'Pull Quote' paragraph style
Task ID: writer_bs_090
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): Style 'Pull Quote' exists as a paragraph style
  Component 2 (0.25): Font — Palatino Linotype, 16pt, italic, color #37474F
  Component 3 (0.30): Paragraph — centered, 2.0cm L/R indent, 0.8cm space before/after
  Component 4 (0.30): Borders — 3pt top/bottom #78909C, no left/right borders
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_090'
FILE_NAME = f'{TASK_ID}.docx'

# Tolerance for dimension checks (EMU-based)
# 0.05cm tolerance
CM_TOLERANCE = Cm(0.05)
# Border size tolerance: 24 eighth-points = 3pt; allow +/- 2 eighth-points
BORDER_SZ_TARGET = 24
BORDER_SZ_TOLERANCE = 2


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

    # Locate 'Pull Quote' style
    pull_quote_style = None
    for s in doc.styles:
        if s.name == 'Pull Quote':
            pull_quote_style = s
            break

    # Component 1: Style 'Pull Quote' exists as a paragraph style (0.15 points)
    try:
        if pull_quote_style is not None and pull_quote_style.type == WD_STYLE_TYPE.PARAGRAPH:
            print(f"PASS: Component 1 — 'Pull Quote' paragraph style exists (0.15 pts)")
            total_score += 0.15
        elif pull_quote_style is not None:
            print(f"FAIL: Component 1 — 'Pull Quote' exists but type is {pull_quote_style.type}, expected PARAGRAPH")
        else:
            print(f"FAIL: Component 1 — 'Pull Quote' style not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If the style doesn't exist, remaining checks are impossible
    if pull_quote_style is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Font — Palatino Linotype, 16pt, italic, color #37474F (0.25 points)
    try:
        font = pull_quote_style.font
        sub_score = 0.0
        sub_total = 4  # 4 sub-checks

        # 2a: Font name
        if font.name and font.name.lower() == 'palatino linotype':
            sub_score += 1
            print(f"  PASS: 2a — Font name = '{font.name}'")
        else:
            print(f"  FAIL: 2a — Font name = '{font.name}', expected 'Palatino Linotype'")

        # 2b: Font size = 16pt
        if font.size and abs(font.size.pt - 16.0) < 0.5:
            sub_score += 1
            print(f"  PASS: 2b — Font size = {font.size.pt}pt")
        else:
            print(f"  FAIL: 2b — Font size = {font.size.pt if font.size else None}pt, expected 16.0pt")

        # 2c: Italic
        if font.italic is True:
            sub_score += 1
            print(f"  PASS: 2c — Italic = True")
        else:
            print(f"  FAIL: 2c — Italic = {font.italic}, expected True")

        # 2d: Color = #37474F
        if font.color and font.color.rgb == RGBColor(0x37, 0x47, 0x4F):
            sub_score += 1
            print(f"  PASS: 2d — Color = #{font.color.rgb}")
        else:
            actual_color = font.color.rgb if font.color and font.color.rgb else None
            print(f"  FAIL: 2d — Color = {actual_color}, expected #37474F")

        comp2_pts = 0.25 * (sub_score / sub_total)
        if comp2_pts > 0:
            print(f"PASS: Component 2 — Font checks {sub_score}/{sub_total} ({comp2_pts:.4f} pts)")
            total_score += comp2_pts
        else:
            print(f"FAIL: Component 2 — All font sub-checks failed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph — centered, 2.0cm L/R indent, 0.8cm space before/after (0.30 points)
    try:
        pf = pull_quote_style.paragraph_format
        sub_score = 0.0
        sub_total = 5  # 5 sub-checks

        # 3a: Alignment = CENTER
        if pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            sub_score += 1
            print(f"  PASS: 3a — Alignment = CENTER")
        else:
            print(f"  FAIL: 3a — Alignment = {pf.alignment}, expected CENTER")

        # 3b: Left indent ~2.0cm
        if pf.left_indent and abs(pf.left_indent - Cm(2.0)) <= CM_TOLERANCE:
            sub_score += 1
            print(f"  PASS: 3b — Left indent = {pf.left_indent / Cm(1):.3f}cm")
        else:
            val = pf.left_indent / Cm(1) if pf.left_indent else None
            print(f"  FAIL: 3b — Left indent = {val}cm, expected 2.0cm")

        # 3c: Right indent ~2.0cm
        if pf.right_indent and abs(pf.right_indent - Cm(2.0)) <= CM_TOLERANCE:
            sub_score += 1
            print(f"  PASS: 3c — Right indent = {pf.right_indent / Cm(1):.3f}cm")
        else:
            val = pf.right_indent / Cm(1) if pf.right_indent else None
            print(f"  FAIL: 3c — Right indent = {val}cm, expected 2.0cm")

        # 3d: Space before ~0.8cm
        if pf.space_before and abs(pf.space_before - Cm(0.8)) <= CM_TOLERANCE:
            sub_score += 1
            print(f"  PASS: 3d — Space before = {pf.space_before / Cm(1):.3f}cm")
        else:
            val = pf.space_before / Cm(1) if pf.space_before else None
            print(f"  FAIL: 3d — Space before = {val}cm, expected 0.8cm")

        # 3e: Space after ~0.8cm
        if pf.space_after and abs(pf.space_after - Cm(0.8)) <= CM_TOLERANCE:
            sub_score += 1
            print(f"  PASS: 3e — Space after = {pf.space_after / Cm(1):.3f}cm")
        else:
            val = pf.space_after / Cm(1) if pf.space_after else None
            print(f"  FAIL: 3e — Space after = {val}cm, expected 0.8cm")

        comp3_pts = 0.30 * (sub_score / sub_total)
        if comp3_pts > 0:
            print(f"PASS: Component 3 — Paragraph checks {sub_score}/{sub_total} ({comp3_pts:.4f} pts)")
            total_score += comp3_pts
        else:
            print(f"FAIL: Component 3 — All paragraph sub-checks failed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Borders — 3pt top/bottom in #78909C, no left/right (0.30 points)
    try:
        pPr = pull_quote_style.element.find(qn('w:pPr'))
        pBdr = pPr.find(qn('w:pBdr')) if pPr is not None else None

        sub_score = 0.0
        sub_total = 4  # top border, bottom border, no left, no right

        if pBdr is None:
            print(f"  FAIL: 4 — No paragraph border element found")
        else:
            w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

            # 4a: Top border — 3pt (sz=24), single, color #78909C
            top_el = pBdr.find(qn('w:top'))
            if top_el is not None:
                sz = int(top_el.get(qn('w:sz'), '0'))
                val = top_el.get(qn('w:val'), '')
                color = top_el.get(qn('w:color'), '').upper()
                if val == 'single' and abs(sz - BORDER_SZ_TARGET) <= BORDER_SZ_TOLERANCE and color == '78909C':
                    sub_score += 1
                    print(f"  PASS: 4a — Top border: single, sz={sz}, color={color}")
                else:
                    print(f"  FAIL: 4a — Top border: val={val}, sz={sz}, color={color} (expected single/24/78909C)")
            else:
                print(f"  FAIL: 4a — No top border element")

            # 4b: Bottom border — 3pt (sz=24), single, color #78909C
            bottom_el = pBdr.find(qn('w:bottom'))
            if bottom_el is not None:
                sz = int(bottom_el.get(qn('w:sz'), '0'))
                val = bottom_el.get(qn('w:val'), '')
                color = bottom_el.get(qn('w:color'), '').upper()
                if val == 'single' and abs(sz - BORDER_SZ_TARGET) <= BORDER_SZ_TOLERANCE and color == '78909C':
                    sub_score += 1
                    print(f"  PASS: 4b — Bottom border: single, sz={sz}, color={color}")
                else:
                    print(f"  FAIL: 4b — Bottom border: val={val}, sz={sz}, color={color} (expected single/24/78909C)")
            else:
                print(f"  FAIL: 4b — No bottom border element")

            # 4c: No left border
            left_el = pBdr.find(qn('w:left'))
            if left_el is None or left_el.get(qn('w:val'), 'none') == 'none':
                sub_score += 1
                print(f"  PASS: 4c — No left border")
            else:
                print(f"  FAIL: 4c — Left border found: {dict(left_el.attrib)}")

            # 4d: No right border
            right_el = pBdr.find(qn('w:right'))
            if right_el is None or right_el.get(qn('w:val'), 'none') == 'none':
                sub_score += 1
                print(f"  PASS: 4d — No right border")
            else:
                print(f"  FAIL: 4d — Right border found: {dict(right_el.attrib)}")

        comp4_pts = 0.30 * (sub_score / sub_total)
        if comp4_pts > 0:
            print(f"PASS: Component 4 — Border checks {sub_score}/{sub_total} ({comp4_pts:.4f} pts)")
            total_score += comp4_pts
        else:
            print(f"FAIL: Component 4 — All border sub-checks failed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook — save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{FILE_NAME}'
persist_app_state()
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
