"""
Reward Script: Create paragraph style hierarchy in Writer document
Task ID: writer_bs_067
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): 'Report Body' style — Georgia 11pt, justified, line spacing 1.15
  Component 2 (0.35): 'Report Quote' style — inherits Report Body, italic, 1.5cm indents
  Component 3 (0.30): 'Report Note' style — inherits Report Body, 9pt, color #666666
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_067'


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

    # Build a lookup of style names for quick access
    style_names = {s.name for s in doc.styles}

    # Component 1: 'Report Body' style with correct properties (0.35 points)
    try:
        if 'Report Body' not in style_names:
            print("FAIL: Component 1 — 'Report Body' style does not exist")
        else:
            style = doc.styles['Report Body']
            font = style.font
            pf = style.paragraph_format
            sub_score = 0.0
            sub_total = 4  # font name, size, alignment, line spacing

            # Check font name = Georgia
            if font.name and font.name.lower() == 'georgia':
                sub_score += 1
                print(f"  PASS: Report Body font.name = {font.name!r}")
            else:
                print(f"  FAIL: Report Body font.name = {font.name!r}, expected 'Georgia'")

            # Check font size = 11pt
            if font.size and abs(font.size.pt - 11.0) < 0.5:
                sub_score += 1
                print(f"  PASS: Report Body font.size = {font.size.pt}pt")
            else:
                pt_val = font.size.pt if font.size else None
                print(f"  FAIL: Report Body font.size = {pt_val}pt, expected 11pt")

            # Check alignment = JUSTIFY (value 3)
            if pf.alignment is not None and pf.alignment == 3:
                sub_score += 1
                print(f"  PASS: Report Body alignment = JUSTIFY")
            else:
                print(f"  FAIL: Report Body alignment = {pf.alignment}, expected JUSTIFY (3)")

            # Check line spacing = 1.15
            if pf.line_spacing is not None and abs(float(pf.line_spacing) - 1.15) < 0.05:
                sub_score += 1
                print(f"  PASS: Report Body line_spacing = {pf.line_spacing}")
            else:
                print(f"  FAIL: Report Body line_spacing = {pf.line_spacing}, expected 1.15")

            comp1_score = 0.35 * (sub_score / sub_total)
            total_score += comp1_score
            print(f"PASS: Component 1 — 'Report Body' style ({sub_score}/{sub_total} checks, {comp1_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Report Quote' style inheriting from Report Body, italic, 1.5cm indents (0.35 points)
    try:
        if 'Report Quote' not in style_names:
            print("FAIL: Component 2 — 'Report Quote' style does not exist")
        else:
            style = doc.styles['Report Quote']
            font = style.font
            pf = style.paragraph_format
            sub_score = 0.0
            sub_total = 3  # base style, italic, indents

            # Check base style = Report Body
            if style.base_style and style.base_style.name == 'Report Body':
                sub_score += 1
                print(f"  PASS: Report Quote base_style = 'Report Body'")
            else:
                base_name = style.base_style.name if style.base_style else None
                print(f"  FAIL: Report Quote base_style = {base_name!r}, expected 'Report Body'")

            # Check italic = True
            if font.italic is True:
                sub_score += 1
                print(f"  PASS: Report Quote font.italic = True")
            else:
                print(f"  FAIL: Report Quote font.italic = {font.italic}, expected True")

            # Check left/right indent ~1.5cm (tolerance 0.1cm)
            # 1.5cm in EMU = 540000 (approx); golden shows 539750
            left_ok = False
            right_ok = False
            if pf.left_indent is not None:
                left_cm = pf.left_indent / Cm(1)
                if abs(left_cm - 1.5) < 0.1:
                    left_ok = True
                    print(f"  PASS: Report Quote left_indent = {left_cm:.3f}cm")
                else:
                    print(f"  FAIL: Report Quote left_indent = {left_cm:.3f}cm, expected ~1.5cm")
            else:
                print(f"  FAIL: Report Quote left_indent = None, expected ~1.5cm")

            if pf.right_indent is not None:
                right_cm = pf.right_indent / Cm(1)
                if abs(right_cm - 1.5) < 0.1:
                    right_ok = True
                    print(f"  PASS: Report Quote right_indent = {right_cm:.3f}cm")
                else:
                    print(f"  FAIL: Report Quote right_indent = {right_cm:.3f}cm, expected ~1.5cm")
            else:
                print(f"  FAIL: Report Quote right_indent = None, expected ~1.5cm")

            if left_ok and right_ok:
                sub_score += 1

            comp2_score = 0.35 * (sub_score / sub_total)
            total_score += comp2_score
            print(f"PASS: Component 2 — 'Report Quote' style ({sub_score}/{sub_total} checks, {comp2_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Report Note' style inheriting from Report Body, 9pt, color #666666 (0.30 points)
    try:
        if 'Report Note' not in style_names:
            print("FAIL: Component 3 — 'Report Note' style does not exist")
        else:
            style = doc.styles['Report Note']
            font = style.font
            sub_score = 0.0
            sub_total = 3  # base style, size, color

            # Check base style = Report Body
            if style.base_style and style.base_style.name == 'Report Body':
                sub_score += 1
                print(f"  PASS: Report Note base_style = 'Report Body'")
            else:
                base_name = style.base_style.name if style.base_style else None
                print(f"  FAIL: Report Note base_style = {base_name!r}, expected 'Report Body'")

            # Check font size = 9pt
            if font.size and abs(font.size.pt - 9.0) < 0.5:
                sub_score += 1
                print(f"  PASS: Report Note font.size = {font.size.pt}pt")
            else:
                pt_val = font.size.pt if font.size else None
                print(f"  FAIL: Report Note font.size = {pt_val}pt, expected 9pt")

            # Check font color = #666666
            if font.color and font.color.rgb:
                actual_rgb = str(font.color.rgb).upper()
                if actual_rgb == '666666':
                    sub_score += 1
                    print(f"  PASS: Report Note font.color.rgb = {actual_rgb}")
                else:
                    print(f"  FAIL: Report Note font.color.rgb = {actual_rgb}, expected '666666'")
            else:
                print(f"  FAIL: Report Note font.color.rgb = None, expected '666666'")

            comp3_score = 0.30 * (sub_score / sub_total)
            total_score += comp3_score
            print(f"PASS: Component 3 — 'Report Note' style ({sub_score}/{sub_total} checks, {comp3_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
