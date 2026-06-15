"""
Reward Script: Apply 'Note' admonition box formatting to the NOTE: paragraph
Task ID: writer_tech_036
Domain: libreoffice_writer
Scoring:
  Component 1: Blue left border on NOTE paragraph (0.3 pts)
  Component 2: Light blue (#E3F2FD) background shading (0.3 pts)
  Component 3: 'NOTE:' prefix is bold and blue (0.4 pts)
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from math import sqrt

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_036'


def color_distance_hex(hex1, hex2):
    """Euclidean RGB distance between two hex color strings (e.g. '1565C0')."""
    r1, g1, b1 = int(hex1[0:2], 16), int(hex1[2:4], 16), int(hex1[4:6], 16)
    r2, g2, b2 = int(hex2[0:2], 16), int(hex2[2:4], 16), int(hex2[4:6], 16)
    return sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def find_note_paragraph(doc):
    """Find the paragraph starting with 'NOTE:'."""
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip().startswith('NOTE:'):
            return i, para
    return None, None


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

    # Find the NOTE: paragraph
    para_idx, note_para = find_note_paragraph(doc)
    if note_para is None:
        print("CRITICAL: No paragraph starting with 'NOTE:' found")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found NOTE paragraph at index {para_idx}: {note_para.text[:80]}...")

    # Component 1: Blue left border on NOTE paragraph (0.3 points)
    # In initial_env: no border. In golden_env: w:left with blue color.
    try:
        pPr = note_para._element.find(qn('w:pPr'))
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                left_bdr = pBdr.find(qn('w:left'))
                if left_bdr is not None:
                    border_color = left_bdr.get(qn('w:color'), '')
                    border_val = left_bdr.get(qn('w:val'), '')
                    # Check it's a visible border (not "none") with a blue-ish color
                    if border_val and border_val != 'none' and border_color:
                        # Blue tolerance: check distance from pure blue range
                        # 1565C0 is the expected color, but accept any blue shade
                        dist = color_distance_hex(border_color.upper(), '1565C0')
                        if dist < 100:  # generous tolerance for blue shades
                            print(f"PASS: Component 1 — Blue left border found (color={border_color}, val={border_val}) (0.3 pts)")
                            total_score += 0.3
                        else:
                            print(f"FAIL: Component 1 — Left border color {border_color} is not blue enough (distance={dist:.1f})")
                    else:
                        print(f"FAIL: Component 1 — Left border exists but val={border_val}, color={border_color}")
                else:
                    print("FAIL: Component 1 — No left border element found in pBdr")
            else:
                print("FAIL: Component 1 — No paragraph borders (pBdr) found")
        else:
            print("FAIL: Component 1 — No paragraph properties (pPr) found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Light blue (#E3F2FD) background shading (0.3 points)
    # In initial_env: no shading. In golden_env: w:shd fill="E3F2FD".
    try:
        pPr = note_para._element.find(qn('w:pPr'))
        if pPr is not None:
            shd = pPr.find(qn('w:shd'))
            if shd is not None:
                fill_color = shd.get(qn('w:fill'), '')
                if fill_color:
                    dist = color_distance_hex(fill_color.upper(), 'E3F2FD')
                    if dist < 50:  # tight tolerance for the specific light blue
                        print(f"PASS: Component 2 — Light blue background shading (fill={fill_color}) (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 2 — Background fill color {fill_color} doesn't match E3F2FD (distance={dist:.1f})")
                else:
                    print("FAIL: Component 2 — Shading element has no fill color")
            else:
                print("FAIL: Component 2 — No shading element found")
        else:
            print("FAIL: Component 2 — No paragraph properties (pPr) found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'NOTE:' prefix is bold and blue (0.4 points)
    # In initial_env: single run, no bold, no color. In golden_env: first run is 'NOTE:' with bold and blue.
    # Split into sub-components: bold (0.2) + blue color (0.2)
    try:
        runs = note_para.runs
        if len(runs) == 0:
            print("FAIL: Component 3 — No runs found in NOTE paragraph")
        else:
            # Find the run containing "NOTE:"
            note_run = None
            for run in runs:
                if 'NOTE:' in run.text:
                    note_run = run
                    break

            if note_run is None:
                print("FAIL: Component 3 — No run containing 'NOTE:' text found")
            else:
                # Sub-check 3a: NOTE: is bold (0.2 pts)
                if note_run.font.bold is True:
                    print(f"PASS: Component 3a — 'NOTE:' run is bold (0.2 pts)")
                    total_score += 0.2
                else:
                    # Also check XML directly for <w:b/> element
                    rPr = note_run._element.find(qn('w:rPr'))
                    if rPr is not None and rPr.find(qn('w:b')) is not None:
                        print(f"PASS: Component 3a — 'NOTE:' run has <w:b/> element (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 3a — 'NOTE:' run bold={note_run.font.bold}")

                # Sub-check 3b: NOTE: is blue (0.2 pts)
                try:
                    run_color = note_run.font.color.rgb
                    if run_color is not None:
                        color_hex = str(run_color)
                        dist = color_distance_hex(color_hex.upper(), '1565C0')
                        if dist < 100:  # blue tolerance
                            print(f"PASS: Component 3b — 'NOTE:' run color is blue ({color_hex}) (0.2 pts)")
                            total_score += 0.2
                        else:
                            print(f"FAIL: Component 3b — 'NOTE:' run color {color_hex} not blue enough (dist={dist:.1f})")
                    else:
                        # Check XML directly
                        rPr = note_run._element.find(qn('w:rPr'))
                        if rPr is not None:
                            color_el = rPr.find(qn('w:color'))
                            if color_el is not None:
                                val = color_el.get(qn('w:val'), '')
                                dist = color_distance_hex(val.upper(), '1565C0')
                                if dist < 100:
                                    print(f"PASS: Component 3b — 'NOTE:' run XML color is blue ({val}) (0.2 pts)")
                                    total_score += 0.2
                                else:
                                    print(f"FAIL: Component 3b — 'NOTE:' run XML color {val} not blue")
                            else:
                                print("FAIL: Component 3b — No color element in run properties")
                        else:
                            print("FAIL: Component 3b — No run properties found")
                except Exception as e:
                    print(f"ERROR: Component 3b — {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
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
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
