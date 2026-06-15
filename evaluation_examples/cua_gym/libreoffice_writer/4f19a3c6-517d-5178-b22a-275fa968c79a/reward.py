"""
Reward Script: Create custom 'Blockquote' paragraph style in Writer document
Task ID: writer_bs_077
Domain: libreoffice_writer
Scoring:
  Component 1: Blockquote style exists as paragraph style (0.15)
  Component 2: Font = Georgia, 10pt, Italic (0.25)
  Component 3: Left indent 1.0cm, Right indent 1.0cm (0.20)
  Component 4: Spacing above 0.3cm, below 0.3cm (0.15)
  Component 5: Left border 2pt solid #CCCCCC, no other borders (0.25)
"""

import os
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_077'

# Tolerance helpers
def approx_cm(emu_val, expected_cm, tol=0.1):
    """Check if EMU value is approximately expected_cm within tolerance."""
    if emu_val is None:
        return False
    actual_cm = emu_val / 360000.0
    return abs(actual_cm - expected_cm) <= tol

def approx_twips(twip_val, expected_cm, tol=0.1):
    """Check twip value (from XML) against expected cm. 1cm = 567 twips approx."""
    if twip_val is None:
        return False
    actual_cm = int(twip_val) / 567.0
    return abs(actual_cm - expected_cm) <= tol


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

    # Find Blockquote style
    bq_style = None
    for s in doc.styles:
        if s.name == 'Blockquote':
            bq_style = s
            break

    # Component 1: Blockquote style exists as paragraph style (0.15 points)
    try:
        if bq_style is not None and str(bq_style.type) == 'PARAGRAPH (1)':
            print(f"PASS: Component 1 -- Blockquote paragraph style exists (0.15 pts)")
            total_score += 0.15
        else:
            if bq_style is None:
                print(f"FAIL: Component 1 -- No style named 'Blockquote' found")
            else:
                print(f"FAIL: Component 1 -- Blockquote exists but type is {bq_style.type}, not PARAGRAPH")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if bq_style is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Font = Georgia, 10pt, Italic (0.25 points)
    try:
        font = bq_style.font
        sub_score = 0.0

        # Check font name
        font_name = font.name
        if font_name and font_name.lower() == 'georgia':
            sub_score += 0.10
            print(f"  PASS: Font name is Georgia")
        else:
            print(f"  FAIL: Font name expected Georgia, found {font_name}")

        # Check font size = 10pt
        if font.size is not None and abs(font.size.pt - 10.0) < 0.5:
            sub_score += 0.08
            print(f"  PASS: Font size is {font.size.pt}pt")
        else:
            sz = font.size.pt if font.size else None
            print(f"  FAIL: Font size expected 10pt, found {sz}")

        # Check italic
        if font.italic is True:
            sub_score += 0.07
            print(f"  PASS: Font is italic")
        else:
            print(f"  FAIL: Font italic expected True, found {font.italic}")

        if sub_score > 0:
            print(f"PASS: Component 2 -- Font properties ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 -- All font checks failed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Left indent 1.0cm, Right indent 1.0cm (0.20 points)
    try:
        pf = bq_style.paragraph_format
        sub_score = 0.0

        if pf.left_indent is not None and approx_cm(pf.left_indent, 1.0, tol=0.15):
            sub_score += 0.10
            actual_left = pf.left_indent / 360000.0
            print(f"  PASS: Left indent ~{actual_left:.3f}cm (expected 1.0cm)")
        else:
            actual_left = pf.left_indent / 360000.0 if pf.left_indent else None
            print(f"  FAIL: Left indent expected ~1.0cm, found {actual_left}")

        if pf.right_indent is not None and approx_cm(pf.right_indent, 1.0, tol=0.15):
            sub_score += 0.10
            actual_right = pf.right_indent / 360000.0
            print(f"  PASS: Right indent ~{actual_right:.3f}cm (expected 1.0cm)")
        else:
            actual_right = pf.right_indent / 360000.0 if pf.right_indent else None
            print(f"  FAIL: Right indent expected ~1.0cm, found {actual_right}")

        if sub_score > 0:
            print(f"PASS: Component 3 -- Indents ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 3 -- All indent checks failed")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Spacing above 0.3cm, below 0.3cm (0.15 points)
    try:
        pf = bq_style.paragraph_format
        sub_score = 0.0

        if pf.space_before is not None and approx_cm(pf.space_before, 0.3, tol=0.1):
            sub_score += 0.075
            actual_before = pf.space_before / 360000.0
            print(f"  PASS: Space before ~{actual_before:.3f}cm (expected 0.3cm)")
        else:
            actual_before = pf.space_before / 360000.0 if pf.space_before else None
            print(f"  FAIL: Space before expected ~0.3cm, found {actual_before}")

        if pf.space_after is not None and approx_cm(pf.space_after, 0.3, tol=0.1):
            sub_score += 0.075
            actual_after = pf.space_after / 360000.0
            print(f"  PASS: Space after ~{actual_after:.3f}cm (expected 0.3cm)")
        else:
            actual_after = pf.space_after / 360000.0 if pf.space_after else None
            print(f"  FAIL: Space after expected ~0.3cm, found {actual_after}")

        if sub_score > 0:
            print(f"PASS: Component 4 -- Spacing ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 -- All spacing checks failed")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Left border 2pt solid #CCCCCC, no other borders (0.25 points)
    try:
        # Parse borders from style XML
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        pPr = bq_style.element.find('.//w:pPr', ns)
        sub_score = 0.0

        if pPr is not None:
            pBdr = pPr.find('w:pBdr', ns)
            if pBdr is not None:
                left_bdr = pBdr.find('w:left', ns)
                if left_bdr is not None:
                    bdr_val = left_bdr.get(qn('w:val'))
                    bdr_sz = left_bdr.get(qn('w:sz'))
                    bdr_color = left_bdr.get(qn('w:color'))

                    # Check border type is single/solid
                    if bdr_val in ('single', 'solid'):
                        sub_score += 0.05
                        print(f"  PASS: Left border style is '{bdr_val}'")
                    else:
                        print(f"  FAIL: Left border style expected single, found '{bdr_val}'")

                    # Check border size = 2pt (16 eighth-points)
                    if bdr_sz is not None:
                        sz_val = int(bdr_sz)
                        # 2pt = 16 eighth-points; allow some tolerance
                        if 14 <= sz_val <= 18:
                            sub_score += 0.08
                            print(f"  PASS: Left border size={sz_val} (~2pt)")
                        else:
                            print(f"  FAIL: Left border size expected ~16 (2pt), found {sz_val}")
                    else:
                        print(f"  FAIL: Left border size not set")

                    # Check border color = CCCCCC
                    if bdr_color is not None and bdr_color.upper() == 'CCCCCC':
                        sub_score += 0.07
                        print(f"  PASS: Left border color is #{bdr_color}")
                    else:
                        print(f"  FAIL: Left border color expected CCCCCC, found {bdr_color}")
                else:
                    print(f"  FAIL: No left border element found")

                # Check no other borders (top, bottom, right)
                other_borders = []
                for side in ['top', 'bottom', 'right']:
                    side_bdr = pBdr.find(f'w:{side}', ns)
                    if side_bdr is not None:
                        side_val = side_bdr.get(qn('w:val'))
                        if side_val and side_val not in ('none', 'nil'):
                            other_borders.append(side)

                if len(other_borders) == 0:
                    sub_score += 0.05
                    print(f"  PASS: No borders on top/bottom/right sides")
                else:
                    print(f"  FAIL: Unexpected borders found on: {other_borders}")
            else:
                print(f"  FAIL: No paragraph borders element found in style")
        else:
            print(f"  FAIL: No paragraph properties found in style")

        if sub_score > 0:
            print(f"PASS: Component 5 -- Border properties ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 -- All border checks failed")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
