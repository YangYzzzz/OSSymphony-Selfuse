"""
Reward Script: Framed tip callout with green border, light green background, bold green 'TIP:'
Task ID: writer_tech_039
Domain: libreoffice_writer
Scoring:
  Component 1: Light green (#E8F5E9) paragraph background shading — 0.3 pts
  Component 2: Green left border on the tip paragraph — 0.3 pts
  Component 3: 'TIP:' run is bold — 0.2 pts
  Component 4: 'TIP:' run is green colored — 0.2 pts
"""

import os
from math import sqrt
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_039'
TIP_TEXT = 'TIP: Use environment variables to manage different deployment configurations.'


def color_distance_hex(hex1, hex2):
    """Compute Euclidean RGB distance between two hex color strings (no '#')."""
    r1, g1, b1 = int(hex1[0:2], 16), int(hex1[2:4], 16), int(hex1[4:6], 16)
    r2, g2, b2 = int(hex2[0:2], 16), int(hex2[2:4], 16), int(hex2[4:6], 16)
    return sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def find_tip_paragraph(doc):
    """Find the paragraph containing the TIP text."""
    for para in doc.paragraphs:
        if 'TIP:' in para.text and 'environment variables' in para.text:
            return para
    return None


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

    # Find the TIP paragraph
    tip_para = find_tip_paragraph(doc)
    if tip_para is None:
        print("CRITICAL: Could not find TIP paragraph in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found TIP paragraph: {repr(tip_para.text[:60])}...")

    # Component 1: Light green (#E8F5E9) paragraph background shading (0.3 points)
    try:
        pPr = tip_para._element.find(qn('w:pPr'))
        if pPr is not None:
            shd = pPr.find(qn('w:shd'))
            if shd is not None:
                fill_color = shd.get(qn('w:fill'))
                if fill_color:
                    fill_color = fill_color.upper().lstrip('#')
                    dist = color_distance_hex(fill_color, 'E8F5E9')
                    if dist < 50:
                        print(f"PASS: Component 1 — Background shading fill={fill_color}, distance={dist:.1f} from E8F5E9 (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 1 — Background fill={fill_color}, distance={dist:.1f} from E8F5E9 (too far)")
                else:
                    print("FAIL: Component 1 — shd element has no fill attribute")
            else:
                print("FAIL: Component 1 — No shading element found on TIP paragraph")
        else:
            print("FAIL: Component 1 — No paragraph properties found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Green left border on the tip paragraph (0.3 points)
    try:
        pPr = tip_para._element.find(qn('w:pPr'))
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                left_bdr = pBdr.find(qn('w:left'))
                if left_bdr is not None:
                    bdr_color = left_bdr.get(qn('w:color'))
                    bdr_val = left_bdr.get(qn('w:val'))
                    if bdr_color and bdr_val and bdr_val != 'none':
                        bdr_color_upper = bdr_color.upper().lstrip('#')
                        # Check it's a green-ish color (distance from pure green family)
                        dist = color_distance_hex(bdr_color_upper, '2E7D32')
                        if dist < 80:
                            print(f"PASS: Component 2 — Left border color={bdr_color_upper}, style={bdr_val}, distance={dist:.1f} from 2E7D32 (0.3 pts)")
                            total_score += 0.3
                        else:
                            # Also accept other green shades
                            r = int(bdr_color_upper[0:2], 16)
                            g = int(bdr_color_upper[2:4], 16)
                            b = int(bdr_color_upper[4:6], 16)
                            if g > r and g > b and g > 80:
                                print(f"PASS: Component 2 — Left border color={bdr_color_upper} is green-ish (0.3 pts)")
                                total_score += 0.3
                            else:
                                print(f"FAIL: Component 2 — Left border color={bdr_color_upper} is not green")
                    else:
                        print(f"FAIL: Component 2 — Left border has no color or style=none")
                else:
                    print("FAIL: Component 2 — No left border element found")
            else:
                print("FAIL: Component 2 — No paragraph border element found")
        else:
            print("FAIL: Component 2 — No paragraph properties found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'TIP:' run is bold (0.2 points)
    try:
        tip_run = None
        for run in tip_para.runs:
            if 'TIP:' in run.text:
                tip_run = run
                break

        if tip_run is not None:
            if tip_run.font.bold is True:
                print(f"PASS: Component 3 — 'TIP:' run is bold (0.2 pts)")
                total_score += 0.2
            else:
                # Also check XML directly for w:b element
                rPr = tip_run._element.find(qn('w:rPr'))
                if rPr is not None and rPr.find(qn('w:b')) is not None:
                    print(f"PASS: Component 3 — 'TIP:' run has <w:b/> element (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — 'TIP:' run bold={tip_run.font.bold}")
        else:
            # Check if the whole paragraph is one run with TIP: at start and it's bold
            if len(tip_para.runs) == 1 and tip_para.runs[0].text.startswith('TIP:'):
                if tip_para.runs[0].font.bold is True:
                    # Whole run is bold but not separated — partial credit questionable
                    # The task asks for TIP: in bold, if whole text is bold it's not quite right
                    print(f"FAIL: Component 3 — Entire text is one bold run, 'TIP:' not separately formatted")
                else:
                    print(f"FAIL: Component 3 — Single run, not bold")
            else:
                print("FAIL: Component 3 — Could not find a run containing 'TIP:'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'TIP:' run is green colored (0.2 points)
    try:
        tip_run = None
        for run in tip_para.runs:
            if 'TIP:' in run.text:
                tip_run = run
                break

        if tip_run is not None:
            rgb = tip_run.font.color.rgb if tip_run.font.color else None
            if rgb is not None:
                rgb_hex = str(rgb).upper()
                # Check it's green (close to 2E7D32 or generally green)
                dist = color_distance_hex(rgb_hex, '2E7D32')
                if dist < 80:
                    print(f"PASS: Component 4 — 'TIP:' run color={rgb_hex}, distance={dist:.1f} from 2E7D32 (0.2 pts)")
                    total_score += 0.2
                else:
                    r = int(rgb_hex[0:2], 16)
                    g = int(rgb_hex[2:4], 16)
                    b = int(rgb_hex[4:6], 16)
                    if g > r and g > b and g > 80:
                        print(f"PASS: Component 4 — 'TIP:' run color={rgb_hex} is green-ish (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 4 — 'TIP:' run color={rgb_hex} is not green")
            else:
                # Check XML directly
                rPr = tip_run._element.find(qn('w:rPr'))
                if rPr is not None:
                    color_el = rPr.find(qn('w:color'))
                    if color_el is not None:
                        val = color_el.get(qn('w:val'))
                        if val:
                            val_upper = val.upper().lstrip('#')
                            dist = color_distance_hex(val_upper, '2E7D32')
                            if dist < 80:
                                print(f"PASS: Component 4 — 'TIP:' run XML color={val_upper} (0.2 pts)")
                                total_score += 0.2
                            else:
                                print(f"FAIL: Component 4 — 'TIP:' XML color={val_upper} not green")
                        else:
                            print("FAIL: Component 4 — color element has no val")
                    else:
                        print("FAIL: Component 4 — No color element in run properties")
                else:
                    print("FAIL: Component 4 — No run properties, no color set")
        else:
            print("FAIL: Component 4 — Could not find a run containing 'TIP:'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
