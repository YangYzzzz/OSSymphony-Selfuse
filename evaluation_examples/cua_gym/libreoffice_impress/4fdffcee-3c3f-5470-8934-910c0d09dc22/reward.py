"""
Reward Script: Change rectangle fill to diagonal hatching pattern
Task ID: impress_ndo_049
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Fill type is pattern (pattFill), not solid
  Component 2 (0.3): Pattern preset is diagonal
  Component 3 (0.2): Foreground color is #1A1A1A
  Component 4 (0.2): Background color is #F0F0F0
"""

import os
import time
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_049'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_rectangle_spPr(pptx_path):
    """
    Find the rectangle shape (Shape 2, named 'Rectangle 3') on slide 2
    and return its spPr XML element.
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Slide 2
        with zf.open('ppt/slides/slide2.xml') as f:
            root = ET.fromstring(f.read())

        shapes = root.findall('.//p:sp', ns)
        for sp in shapes:
            # Find the rectangle by checking prstGeom == 'rect' and position/size
            spPr = sp.find('.//p:spPr', ns)
            if spPr is None:
                continue

            prstGeom = spPr.find('a:prstGeom', ns)
            if prstGeom is None:
                continue

            if prstGeom.get('prst') != 'rect':
                continue

            # Check it's the main rectangle (10cm x 6cm = 3600000 x 2160000 EMU)
            xfrm = spPr.find('a:xfrm', ns)
            if xfrm is None:
                continue

            ext = xfrm.find('a:ext', ns)
            if ext is None:
                continue

            cx = int(ext.get('cx', 0))
            cy = int(ext.get('cy', 0))

            # Match the rectangle (~3600000 x 2160000)
            if abs(cx - 3600000) < 100000 and abs(cy - 2160000) < 100000:
                return spPr

    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    # Precondition: file exists and is a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        spPr = get_rectangle_spPr(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse pptx {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if spPr is None:
        print("CRITICAL: Rectangle shape not found on slide 2")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Fill type is pattern (pattFill present, solidFill absent) — 0.3 points
    try:
        pattFill = spPr.find('a:pattFill', ns)
        solidFill = spPr.find('a:solidFill', ns)

        has_pattern = pattFill is not None
        has_solid = solidFill is not None

        if has_pattern and not has_solid:
            print(f"PASS: Component 1 -- Fill is pattern (pattFill present, solidFill absent) (0.3 pts)")
            total_score += 0.3
        elif has_pattern and has_solid:
            print(f"PARTIAL: Component 1 -- pattFill present but solidFill also present")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected pattFill, found solidFill={has_solid}, pattFill={has_pattern}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Pattern preset is diagonal — 0.3 points
    try:
        pattFill = spPr.find('a:pattFill', ns)
        if pattFill is not None:
            prst = pattFill.get('prst', '')
            # Accept diagonal variants: dnDiag, upDiag, ltDnDiag, ltUpDiag, dkDnDiag, dkUpDiag, wdDnDiag, wdUpDiag, narDiag
            is_diagonal = 'diag' in prst.lower() or 'Diag' in prst
            if is_diagonal:
                print(f"PASS: Component 2 -- Pattern preset is diagonal: '{prst}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected diagonal pattern, found preset: '{prst}'")
        else:
            print(f"FAIL: Component 2 -- No pattFill element found (cannot check pattern preset)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Foreground color is #1A1A1A — 0.2 points
    try:
        pattFill = spPr.find('a:pattFill', ns)
        if pattFill is not None:
            fgClr = pattFill.find('a:fgClr', ns)
            if fgClr is not None:
                srgbClr = fgClr.find('a:srgbClr', ns)
                if srgbClr is not None:
                    fg_val = srgbClr.get('val', '').upper()
                    if fg_val == '1A1A1A':
                        print(f"PASS: Component 3 -- Foreground color is #1A1A1A (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 3 -- Expected fg color #1A1A1A, found #{fg_val}")
                else:
                    print(f"FAIL: Component 3 -- fgClr has no srgbClr element")
            else:
                print(f"FAIL: Component 3 -- No fgClr element in pattFill")
        else:
            print(f"FAIL: Component 3 -- No pattFill element found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Background color is #F0F0F0 — 0.2 points
    try:
        pattFill = spPr.find('a:pattFill', ns)
        if pattFill is not None:
            bgClr = pattFill.find('a:bgClr', ns)
            if bgClr is not None:
                srgbClr = bgClr.find('a:srgbClr', ns)
                if srgbClr is not None:
                    bg_val = srgbClr.get('val', '').upper()
                    if bg_val == 'F0F0F0':
                        print(f"PASS: Component 4 -- Background color is #F0F0F0 (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 4 -- Expected bg color #F0F0F0, found #{bg_val}")
                else:
                    print(f"FAIL: Component 4 -- bgClr has no srgbClr element")
            else:
                print(f"FAIL: Component 4 -- No bgClr element in pattFill")
        else:
            print(f"FAIL: Component 4 -- No pattFill element found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
