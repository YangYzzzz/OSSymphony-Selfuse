"""
Reward Script: Memorial letter formatting for easy readout
Task ID: writer_creative_068
Domain: libreoffice_writer
Scoring:
  Component 1: Title "For Grandpa Henry" — 22pt, bold, center, Liberation Serif (0.25)
  Component 2: Body paragraphs — 14pt font size, line_spacing=1.8 (0.25)
  Component 3: Pause markers — [PAUSE] replaced with decorative symbol on centered line (0.20)
  Component 4: Margins — 1.25 inches on all sides (0.15)
  Component 5: Page border — single thin border on all 4 sides (0.15)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_creative_068'
FILE_PATH = f'{WORKDIR}/memorial_letter.docx'

# Known decorative pause symbols (or similar)
PAUSE_SYMBOLS = ['— ✦ —', '* * *', '—✦—', '✦', '* * *', '---', '~ ~ ~', '— — —']

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

    paragraphs = doc.paragraphs

    # -----------------------------------------------------------------------
    # Component 1: Title "For Grandpa Henry" formatting (0.25 points)
    # Expected: font_size=22pt, bold=True, alignment=center, font=Liberation Serif
    # -----------------------------------------------------------------------
    try:
        title_para = None
        for para in paragraphs:
            if 'For Grandpa Henry' in para.text:
                title_para = para
                break

        if title_para is None:
            print("FAIL: Component 1 — Title 'For Grandpa Henry' paragraph not found")
        else:
            pf = title_para.paragraph_format
            runs = [r for r in title_para.runs if r.text.strip()]
            if not runs:
                print("FAIL: Component 1 — Title has no runs with text")
            else:
                run = runs[0]
                size_ok = run.font.size is not None and abs(run.font.size.pt - 22.0) < 0.5
                bold_ok = run.font.bold is True
                align_ok = pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
                font_ok = run.font.name is not None and 'Liberation Serif' in run.font.name

                details = (
                    f"size={run.font.size.pt if run.font.size else None}pt "
                    f"bold={run.font.bold} "
                    f"align={pf.alignment} "
                    f"font={run.font.name}"
                )
                if size_ok and bold_ok and align_ok and font_ok:
                    print(f"PASS: Component 1 — Title formatting correct ({details}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 1 — Title formatting incomplete. "
                          f"size_ok={size_ok}, bold_ok={bold_ok}, align_ok={align_ok}, font_ok={font_ok}. {details}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Body paragraphs — 14pt, line_spacing=1.8 (0.25 points)
    # Body paragraphs are the 6 tribute paragraphs (not title/byline/date/pause markers)
    # Expected: font_size=14pt, line_spacing=1.8
    # -----------------------------------------------------------------------
    try:
        # Identify body paragraphs: skip empty, title, byline, date, and pause marker paragraphs
        skip_texts = {'For Grandpa Henry', 'Read by his grandson, Daniel Walker', 'March 8, 2026'}
        body_paras = []
        for para in paragraphs:
            text = para.text.strip()
            if not text:
                continue
            if text in skip_texts:
                continue
            # Skip pause marker paragraphs (they contain decorative symbols, short)
            if len(text) <= 20 and any(sym in text for sym in PAUSE_SYMBOLS):
                continue
            # Skip likely pause markers that are short and centered
            if len(text) <= 15 and para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                continue
            body_paras.append(para)

        if not body_paras:
            print("FAIL: Component 2 — No body paragraphs found")
        else:
            body_size_ok_count = 0
            body_spacing_ok_count = 0
            for para in body_paras:
                runs = [r for r in para.runs if r.text.strip()]
                if runs:
                    size_pt = runs[0].font.size.pt if runs[0].font.size else None
                    if size_pt is not None and abs(size_pt - 14.0) < 0.5:
                        body_size_ok_count += 1
                pf = para.paragraph_format
                # line_spacing=1.8 (as float, not as Pt)
                ls = pf.line_spacing
                if ls is not None:
                    # Could be stored as float (1.8) or as EMU
                    if isinstance(ls, float) and abs(ls - 1.8) < 0.1:
                        body_spacing_ok_count += 1
                    elif hasattr(ls, 'pt'):
                        # If it's stored as length in EMU (unlikely for 1.8), skip
                        pass
                    elif abs(float(ls) - 1.8) < 0.1:
                        body_spacing_ok_count += 1

            total_body = len(body_paras)
            size_ratio = body_size_ok_count / total_body if total_body > 0 else 0
            spacing_ratio = body_spacing_ok_count / total_body if total_body > 0 else 0

            # Award points if majority (>=50%) of body paragraphs pass
            if size_ratio >= 0.5 and spacing_ratio >= 0.5:
                print(f"PASS: Component 2 — Body paragraph formatting correct "
                      f"(size {body_size_ok_count}/{total_body}, spacing {body_spacing_ok_count}/{total_body}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Body paragraph formatting incomplete. "
                      f"14pt: {body_size_ok_count}/{total_body}, spacing=1.8: {body_spacing_ok_count}/{total_body}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Pause markers — decorative symbol on centered line (0.20 points)
    # [PAUSE] at end of paragraphs 2, 4, 6 should be replaced by a decorative symbol
    # centered on its own line, 12pt
    # -----------------------------------------------------------------------
    try:
        # Find centered paragraphs with short decorative text (not title/byline/date)
        skip_texts_header = {'For Grandpa Henry', 'Read by his grandson, Daniel Walker', 'March 8, 2026'}
        pause_marker_paras = []
        for para in paragraphs:
            text = para.text.strip()
            if not text or text in skip_texts_header:
                continue
            pf = para.paragraph_format
            # Pause markers should be: centered, short, and contain decorative chars
            # They should NOT contain [PAUSE] (which was the old format)
            if '[PAUSE]' not in text and pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER and len(text) <= 20:
                # Likely a pause marker if it's non-body-text (very short, centered)
                # Accept any decorative symbol pattern
                pause_marker_paras.append(para)

        # Check that there are no [PAUSE] markers remaining
        pause_remaining = []
        for para in paragraphs:
            if '[PAUSE]' in para.text:
                pause_remaining.append(para.text[:60])

        if pause_remaining:
            print(f"FAIL: Component 3 — [PAUSE] markers still present: {pause_remaining}")
        elif len(pause_marker_paras) >= 3:
            # Check font size of pause markers should be 12pt
            sizes_ok = 0
            for pm in pause_marker_paras[:3]:
                runs = [r for r in pm.runs if r.text.strip()]
                if runs:
                    sz = runs[0].font.size.pt if runs[0].font.size else None
                    if sz is not None and abs(sz - 12.0) < 0.5:
                        sizes_ok += 1
                    else:
                        # size might be inherited — still count it as present
                        sizes_ok += 1
                else:
                    sizes_ok += 1  # runs not found but para exists

            print(f"PASS: Component 3 — {len(pause_marker_paras)} pause markers found, centered, no [PAUSE] text (0.20 pts)")
            total_score += 0.20
        elif len(pause_marker_paras) >= 1:
            partial = 0.10
            print(f"PARTIAL: Component 3 — Only {len(pause_marker_paras)} pause marker(s) found (expected 3), "
                  f"awarding {partial} pts")
            total_score += partial
        else:
            print("FAIL: Component 3 — No decorative pause marker paragraphs found (expected 3 centered symbols)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Margins — 1.25 inches all around (0.15 points)
    # Initial: 1.0in all around; Expected: 1.25in all around
    # -----------------------------------------------------------------------
    try:
        s = doc.sections[0]
        margin_tolerance = 0.05  # 0.05 inch tolerance

        left_ok = abs(s.left_margin.inches - 1.25) < margin_tolerance
        right_ok = abs(s.right_margin.inches - 1.25) < margin_tolerance
        top_ok = abs(s.top_margin.inches - 1.25) < margin_tolerance
        bottom_ok = abs(s.bottom_margin.inches - 1.25) < margin_tolerance

        margins_str = (
            f"left={s.left_margin.inches:.3f}in "
            f"right={s.right_margin.inches:.3f}in "
            f"top={s.top_margin.inches:.3f}in "
            f"bottom={s.bottom_margin.inches:.3f}in"
        )

        if left_ok and right_ok and top_ok and bottom_ok:
            print(f"PASS: Component 4 — Margins 1.25in all sides ({margins_str}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Margins not 1.25in. "
                  f"left_ok={left_ok}, right_ok={right_ok}, top_ok={top_ok}, bottom_ok={bottom_ok}. {margins_str}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Page border — single border on all 4 sides (0.15 points)
    # Initial: no border; Expected: single thin line border on top/left/bottom/right
    # -----------------------------------------------------------------------
    try:
        s = doc.sections[0]
        sectPr = s._sectPr
        pgBorders = sectPr.find(qn('w:pgBorders'))

        if pgBorders is None:
            print("FAIL: Component 5 — No page borders element found in document")
        else:
            # Check all 4 sides are present with val="single" or similar border type
            border_sides = ['top', 'left', 'bottom', 'right']
            sides_found = []
            for side in border_sides:
                elem = pgBorders.find(qn(f'w:{side}'))
                if elem is not None:
                    val = elem.get(qn('w:val'))
                    if val is not None and val != 'none' and val != 'nil':
                        sides_found.append(side)

            if len(sides_found) == 4:
                print(f"PASS: Component 5 — Page border on all 4 sides: {sides_found} (0.15 pts)")
                total_score += 0.15
            elif len(sides_found) >= 2:
                partial = 0.08
                print(f"PARTIAL: Component 5 — Page border on {len(sides_found)}/4 sides: {sides_found}, "
                      f"awarding {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Page border on only {len(sides_found)}/4 sides: {sides_found}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
