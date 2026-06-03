"""
Reward Script: Create InlineCode character style and apply to code references
Task ID: writer_tech_025
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): InlineCode character style exists
  Component 2 (0.3): InlineCode style has correct properties (Liberation Mono 10pt, #333333, #F0F0F0 shading)
  Component 3 (0.4): All three code references have InlineCode style applied
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_025'

# The three inline code references that must have the style applied
CODE_REFS = ['config.yaml', 'init()', 'ENV_PATH']


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


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

    # ---- Component 1: InlineCode character style exists (0.3 pts) ----
    inline_code_style = None
    try:
        for style in doc.styles:
            if style.name == 'InlineCode' and style.type is not None and style.type.name == 'CHARACTER':
                inline_code_style = style
                break

        if inline_code_style is not None:
            print(f"PASS: Component 1 -- InlineCode character style exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- InlineCode character style not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ---- Component 2: InlineCode style properties correct (0.3 pts) ----
    # Sub-checks: font name (0.075), font size 10pt (0.075), color #333333 (0.075), shading #F0F0F0 (0.075)
    try:
        if inline_code_style is not None:
            sub_score = 0.0

            # 2a: Font name is Liberation Mono
            font_name = inline_code_style.font.name
            if font_name == 'Liberation Mono':
                print(f"PASS: Component 2a -- Font name is 'Liberation Mono' (0.075 pts)")
                sub_score += 0.075
            else:
                print(f"FAIL: Component 2a -- Expected font 'Liberation Mono', found '{font_name}'")

            # 2b: Font size is 10pt
            font_size = inline_code_style.font.size
            if font_size is not None and abs(font_size.pt - 10.0) < 0.5:
                print(f"PASS: Component 2b -- Font size is {font_size.pt}pt (0.075 pts)")
                sub_score += 0.075
            else:
                size_str = f"{font_size.pt}pt" if font_size else "None"
                print(f"FAIL: Component 2b -- Expected 10pt, found {size_str}")

            # 2c: Font color is #333333
            color_rgb = inline_code_style.font.color.rgb
            if color_rgb is not None and str(color_rgb).upper() == '333333':
                print(f"PASS: Component 2c -- Color is #{color_rgb} (0.075 pts)")
                sub_score += 0.075
            else:
                print(f"FAIL: Component 2c -- Expected #333333, found #{color_rgb}")

            # 2d: Shading/highlight background is #F0F0F0
            # python-docx highlight_color uses WD_COLOR_INDEX (limited palette).
            # The task uses #F0F0F0 which is a custom shading via w:shd element.
            rpr = inline_code_style.element.find(qn('w:rPr'))
            shd_elem = rpr.find(qn('w:shd')) if rpr is not None else None
            if shd_elem is not None:
                fill_color = shd_elem.get(qn('w:fill'), '').upper()
                if fill_color == 'F0F0F0':
                    print(f"PASS: Component 2d -- Shading fill is #F0F0F0 (0.075 pts)")
                    sub_score += 0.075
                else:
                    print(f"FAIL: Component 2d -- Expected shading #F0F0F0, found #{fill_color}")
            else:
                # Also check highlight_color as fallback
                hl = inline_code_style.font.highlight_color
                print(f"FAIL: Component 2d -- No shading element found (highlight_color={hl})")

            total_score += sub_score
        else:
            print(f"FAIL: Component 2 -- Cannot check properties, InlineCode style does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---- Component 3: All three code references have InlineCode style applied (0.4 pts) ----
    # Each reference found with correct style = 0.4/3 pts
    try:
        pts_per_ref = 0.4 / 3.0
        refs_found = {ref: False for ref in CODE_REFS}

        # Only check paragraphs in the first section (before the second Heading 1)
        first_section_paras = []
        heading_count = 0
        for para in doc.paragraphs:
            if para.style.name == 'Heading 1':
                heading_count += 1
                if heading_count > 1:
                    break
            first_section_paras.append(para)

        for para in first_section_paras:
            for run in para.runs:
                text = run.text.strip()
                if text in CODE_REFS and not refs_found[text]:
                    # Check if run has InlineCode style applied
                    run_style_name = None
                    # Check via run.style
                    if run.style and run.style.name == 'InlineCode':
                        run_style_name = 'InlineCode'
                    else:
                        # Fallback: check XML for rStyle
                        rpr = run.element.find(qn('w:rPr'))
                        if rpr is not None:
                            rstyle = rpr.find(qn('w:rStyle'))
                            if rstyle is not None:
                                run_style_name = rstyle.get(qn('w:val'))

                    if run_style_name == 'InlineCode':
                        print(f"PASS: Component 3 -- '{text}' has InlineCode style ({pts_per_ref:.4f} pts)")
                        total_score += pts_per_ref
                        refs_found[text] = True
                    else:
                        print(f"FAIL: Component 3 -- '{text}' has style '{run_style_name}', expected 'InlineCode'")
                        refs_found[text] = True  # mark as found but wrong style

        for ref, found in refs_found.items():
            if not found:
                print(f"FAIL: Component 3 -- '{ref}' not found in first section runs")

    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state('libreoffice_writer')

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
