"""
Reward Script: Pleading paper formatting with line numbers and double border
Task ID: writer_legal_047
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) — Line numbering enabled with countBy=1 and restart=newPage
  Component 2 (0.30) — Left page border is double-line style
  Component 3 (0.20) — Border color is black (000000) and positioned from page
  Component 4 (0.15) — Line number distance is set (non-zero)
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_047'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify pleading paper formatting: line numbering + double vertical border.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # We need at least one section to check
    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    sectPr = section._sectPr

    # Component 1: Line numbering enabled with countBy=1 and restart=newPage (0.35 points)
    try:
        lnNumType = sectPr.find('w:lnNumType', NS)
        if lnNumType is not None:
            countBy = lnNumType.get(f'{{{WNS}}}countBy')
            restart = lnNumType.get(f'{{{WNS}}}restart')

            countBy_ok = (countBy == '1')
            restart_ok = (restart == 'newPage')

            if countBy_ok and restart_ok:
                print(f"PASS: Component 1 — Line numbering: countBy={countBy}, restart={restart} (0.35 pts)")
                total_score += 0.35
            elif countBy_ok:
                # Partial: countBy correct but restart wrong
                print(f"PARTIAL: Component 1 — countBy={countBy} correct, but restart={restart} (expected newPage) (0.15 pts)")
                total_score += 0.15
            elif restart_ok:
                # Partial: restart correct but countBy wrong
                print(f"PARTIAL: Component 1 — restart={restart} correct, but countBy={countBy} (expected 1) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — countBy={countBy} (expected 1), restart={restart} (expected newPage)")
        else:
            print("FAIL: Component 1 — No <w:lnNumType> element found; line numbering not enabled")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Left page border is double-line style (0.30 points)
    try:
        pgBorders = sectPr.find('w:pgBorders', NS)
        if pgBorders is not None:
            left_border = pgBorders.find('w:left', NS)
            if left_border is not None:
                val = left_border.get(f'{{{WNS}}}val')
                if val == 'double':
                    print(f"PASS: Component 2 — Left border val='{val}' is double (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — Left border val='{val}', expected 'double'")
            else:
                print("FAIL: Component 2 — No <w:left> element inside <w:pgBorders>")
        else:
            print("FAIL: Component 2 — No <w:pgBorders> element found; no page borders defined")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Border color is black and offsetFrom is page (0.20 points)
    try:
        pgBorders = sectPr.find('w:pgBorders', NS)
        if pgBorders is not None:
            left_border = pgBorders.find('w:left', NS)
            offsetFrom = pgBorders.get(f'{{{WNS}}}offsetFrom')

            color = left_border.get(f'{{{WNS}}}color') if left_border is not None else None
            # Accept black variants: 000000, auto
            is_color_ok = (color in ('000000', 'auto'))
            is_offset_ok = (offsetFrom == 'page')

            if is_color_ok and is_offset_ok:
                print(f"PASS: Component 3 — Border color={color}, offsetFrom={offsetFrom} (0.20 pts)")
                total_score += 0.20
            elif is_color_ok:
                print(f"PARTIAL: Component 3 — Color correct but offsetFrom={offsetFrom} (expected page) (0.10 pts)")
                total_score += 0.10
            elif is_offset_ok:
                print(f"PARTIAL: Component 3 — offsetFrom correct but color={color} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Border color={color} or offsetFrom={offsetFrom} not correct")
        else:
            print("FAIL: Component 3 — No <w:pgBorders> element found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Line number distance is set (non-zero) (0.15 points)
    try:
        lnNumType = sectPr.find('w:lnNumType', NS)
        if lnNumType is not None:
            distance = lnNumType.get(f'{{{WNS}}}distance')
            if distance is not None and int(distance) > 0:
                print(f"PASS: Component 4 — Line number distance={distance} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Line number distance={distance} (expected > 0)")
        else:
            print("FAIL: Component 4 — No <w:lnNumType> element; cannot check distance")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
