"""
Reward Script: Format warning box with red left border, light yellow background, bold red WARNING prefix
Task ID: writer_tech_029
Domain: libreoffice_writer
Scoring:
  Component 1: Red left border on WARNING paragraph (0.3 pts)
  Component 2: Light yellow (#FFFDE7) background shading (0.3 pts)
  Component 3: 'WARNING:' prefix is bold and red (0.4 pts)
"""

import os
import time


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


WORKDIR = '/home/user'
TASK_ID = 'writer_tech_029'


def find_warning_paragraph(doc):
    """Find the paragraph containing the WARNING text."""
    for i, para in enumerate(doc.paragraphs):
        if 'WARNING' in para.text and 'Do not modify' in para.text:
            return i, para
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: find the WARNING paragraph
    idx, warning_para = find_warning_paragraph(doc)
    if warning_para is None:
        print("CRITICAL: WARNING paragraph not found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found WARNING paragraph at index {idx}: {repr(warning_para.text[:60])}")

    # Component 1: Red left border on WARNING paragraph (0.3 points)
    try:
        pPr = warning_para._element.find(qn('w:pPr'))
        has_red_left_border = False
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                left_bdr = pBdr.find(qn('w:left'))
                if left_bdr is not None:
                    border_color = left_bdr.get(qn('w:color'), '')
                    border_val = left_bdr.get(qn('w:val'), '')
                    # Accept any non-none border with red-ish color
                    if border_val and border_val != 'none':
                        # Check color is red (FF0000 or close variants)
                        if border_color.upper() in ('FF0000', 'RED'):
                            has_red_left_border = True
                            print(f"PASS: Component 1 -- Red left border found (val={border_val}, color={border_color}) (0.3 pts)")
                        else:
                            print(f"FAIL: Component 1 -- Left border exists but color is {border_color}, expected FF0000/red")
                    else:
                        print(f"FAIL: Component 1 -- Left border val is '{border_val}', expected non-none border")
                else:
                    print("FAIL: Component 1 -- No left border element in pBdr")
            else:
                print("FAIL: Component 1 -- No paragraph borders (pBdr) element")
        else:
            print("FAIL: Component 1 -- No paragraph properties (pPr) element")

        if has_red_left_border:
            total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Light yellow (#FFFDE7) background shading (0.3 points)
    try:
        pPr = warning_para._element.find(qn('w:pPr'))
        has_yellow_bg = False
        if pPr is not None:
            shd = pPr.find(qn('w:shd'))
            if shd is not None:
                fill_color = shd.get(qn('w:fill'), '')
                # Accept FFFDE7 exactly or close light yellow variants
                if fill_color.upper() == 'FFFDE7':
                    has_yellow_bg = True
                    print(f"PASS: Component 2 -- Light yellow background found (fill={fill_color}) (0.3 pts)")
                else:
                    # Allow some tolerance for near-yellow fills
                    print(f"FAIL: Component 2 -- Shading fill is {fill_color}, expected FFFDE7")
            else:
                print("FAIL: Component 2 -- No shading element in pPr")
        else:
            print("FAIL: Component 2 -- No paragraph properties (pPr) element")

        if has_yellow_bg:
            total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'WARNING:' prefix is bold and red (0.4 points)
    try:
        runs = warning_para.runs
        warning_bold_red = False

        if len(runs) >= 1:
            # Look for a run that contains 'WARNING:' and is bold + red
            for run in runs:
                if 'WARNING:' in run.text or run.text.strip() == 'WARNING:':
                    is_bold = run.font.bold is True
                    color_rgb = run.font.color.rgb
                    is_red = False
                    if color_rgb is not None:
                        color_hex = str(color_rgb).upper()
                        if color_hex == 'FF0000':
                            is_red = True

                    if is_bold and is_red:
                        warning_bold_red = True
                        print(f"PASS: Component 3 -- 'WARNING:' run is bold={run.font.bold}, color={run.font.color.rgb} (0.4 pts)")
                    elif is_bold and not is_red:
                        # Partial: bold but not red
                        print(f"PARTIAL: Component 3 -- 'WARNING:' is bold but color is {color_rgb}, expected FF0000")
                        total_score += 0.2
                    elif not is_bold and is_red:
                        # Partial: red but not bold
                        print(f"PARTIAL: Component 3 -- 'WARNING:' is red but not bold (bold={run.font.bold})")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 3 -- 'WARNING:' run is bold={run.font.bold}, color={color_rgb}, expected bold=True+color=FF0000")
                    break
            else:
                # No run containing 'WARNING:' found separately
                # Check if all text is in a single run (initial state)
                if len(runs) == 1 and 'WARNING:' in runs[0].text:
                    is_bold = runs[0].font.bold is True
                    color_rgb = runs[0].font.color.rgb
                    is_red = color_rgb is not None and str(color_rgb).upper() == 'FF0000'
                    if is_bold and is_red:
                        # Entire paragraph is bold+red including WARNING:
                        warning_bold_red = True
                        print(f"PASS: Component 3 -- Single run with 'WARNING:' is bold+red (0.4 pts)")
                    else:
                        print(f"FAIL: Component 3 -- Single run, bold={is_bold}, red={is_red}")
                else:
                    print(f"FAIL: Component 3 -- No run containing 'WARNING:' found")

        if warning_bold_red:
            total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
