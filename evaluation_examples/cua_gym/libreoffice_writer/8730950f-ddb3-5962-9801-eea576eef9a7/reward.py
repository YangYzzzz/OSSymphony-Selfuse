"""
Reward Script: Create 'Variable Name' character style and apply to variable names
Task ID: writer_bs_055
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): 'Variable Name' character style exists
  Component 2 (0.15): Style font is Consolas 10pt
  Component 3 (0.15): Style is bold with color #006400
  Component 4 (0.20): 'maxCount' occurrences have the style applied
  Component 5 (0.20): 'inputArray' occurrences have the style applied
  Component 6 (0.15): 'resultMap' occurrences have the style applied
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_055'


def persist_app_state():
    """Best-effort save via Ctrl+S in case LibreOffice has unsaved changes."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
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

    # ---- Locate the 'Variable Name' character style ----
    var_style = None
    for style in doc.styles:
        if style.name == 'Variable Name' and str(style.type) == 'CHARACTER (2)':
            var_style = style
            break

    # Component 1: 'Variable Name' character style exists (0.15 points)
    try:
        if var_style is not None:
            print(f"PASS: Component 1 — 'Variable Name' character style exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 'Variable Name' character style not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Style font is Consolas 10pt (0.15 points)
    try:
        if var_style is not None:
            font_name = var_style.font.name
            font_size_pt = var_style.font.size.pt if var_style.font.size else None
            font_ok = (font_name == 'Consolas' and font_size_pt == 10.0)
            if font_ok:
                print(f"PASS: Component 2 — Style font=Consolas, size=10pt (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Expected font=Consolas/10pt, found font={font_name}/{font_size_pt}pt")
        else:
            print(f"FAIL: Component 2 — Style does not exist, cannot check font")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Style is bold with color #006400 (0.15 points)
    try:
        if var_style is not None:
            is_bold = var_style.font.bold is True
            color_rgb = var_style.font.color.rgb if var_style.font.color else None
            color_ok = (color_rgb is not None and str(color_rgb) == '006400')
            if is_bold and color_ok:
                print(f"PASS: Component 3 — Style bold=True, color=#006400 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Expected bold=True/color=#006400, found bold={var_style.font.bold}, color={color_rgb}")
        else:
            print(f"FAIL: Component 3 — Style does not exist, cannot check bold/color")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Check style application to variable name runs ----
    # For each variable name, count runs with text matching the name that have the style applied.
    # A run has the style if run.style.name == 'Variable Name'.
    # We require at least 1 occurrence for each variable to be styled.

    variable_names = ['maxCount', 'inputArray', 'resultMap']
    styled_counts = {v: 0 for v in variable_names}
    total_text_counts = {v: 0 for v in variable_names}

    for para in doc.paragraphs:
        for run in para.runs:
            txt = run.text.strip()
            if txt in variable_names:
                total_text_counts[txt] += 1
                # Check if the run has the 'Variable Name' character style applied
                if run.style and run.style.name == 'Variable Name':
                    styled_counts[txt] += 1

    # Component 4: 'maxCount' occurrences have the style applied (0.20 points)
    try:
        mc_styled = styled_counts['maxCount']
        mc_total = total_text_counts['maxCount']
        if mc_total > 0 and mc_styled == mc_total:
            print(f"PASS: Component 4 — All {mc_styled}/{mc_total} 'maxCount' runs have 'Variable Name' style (0.20 pts)")
            total_score += 0.20
        elif mc_styled > 0:
            # Partial credit: some but not all styled
            partial = 0.20 * (mc_styled / mc_total) if mc_total > 0 else 0.0
            print(f"PARTIAL: Component 4 — {mc_styled}/{mc_total} 'maxCount' runs styled ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — 0/{mc_total} 'maxCount' runs have 'Variable Name' style")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 'inputArray' occurrences have the style applied (0.20 points)
    try:
        ia_styled = styled_counts['inputArray']
        ia_total = total_text_counts['inputArray']
        if ia_total > 0 and ia_styled == ia_total:
            print(f"PASS: Component 5 — All {ia_styled}/{ia_total} 'inputArray' runs have 'Variable Name' style (0.20 pts)")
            total_score += 0.20
        elif ia_styled > 0:
            partial = 0.20 * (ia_styled / ia_total) if ia_total > 0 else 0.0
            print(f"PARTIAL: Component 5 — {ia_styled}/{ia_total} 'inputArray' runs styled ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — 0/{ia_total} 'inputArray' runs have 'Variable Name' style")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 'resultMap' occurrences have the style applied (0.15 points)
    try:
        rm_styled = styled_counts['resultMap']
        rm_total = total_text_counts['resultMap']
        if rm_total > 0 and rm_styled == rm_total:
            print(f"PASS: Component 6 — All {rm_styled}/{rm_total} 'resultMap' runs have 'Variable Name' style (0.15 pts)")
            total_score += 0.15
        elif rm_styled > 0:
            partial = 0.15 * (rm_styled / rm_total) if rm_total > 0 else 0.0
            print(f"PARTIAL: Component 6 — {rm_styled}/{rm_total} 'resultMap' runs styled ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — 0/{rm_total} 'resultMap' runs have 'Variable Name' style")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
