"""
Reward Script: Configure slide show settings (start slide, pen pointer, end black slide)
Task ID: impress_gf3_050
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Slide show starts from slide 3 (sldRg st="3" in showPr)
  Component 2 (0.3): Pen color configured in show properties (penClr in showPr)
  Component 3 (0.3): End with black slide enabled (EndWithBlackSlide in LO config)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_050'
LO_CONFIG = os.path.join(WORKDIR, '.config/libreoffice/4/user/registrymodifications.xcu')

# Namespaces used in PPTX XML
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice state via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_impress")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify slide show configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Verify PPTX file showPr settings ----
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/presentation.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse PPTX file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find showPr element
    show_pr = root.find(f'.//{{{NS_P}}}showPr')

    # Component 1: Slide show starts from slide 3 (0.4 points)
    try:
        if show_pr is not None:
            sld_rg = show_pr.find(f'{{{NS_P}}}sldRg')
            if sld_rg is not None:
                st_val = sld_rg.get('st')
                if st_val == '3':
                    print(f"PASS: Component 1 — Slide range starts at slide 3 (st={st_val}) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — Expected slide range st=3, found st={st_val}")
            else:
                print("FAIL: Component 1 — No <p:sldRg> element found in showPr")
        else:
            print("FAIL: Component 1 — No <p:showPr> element found in presentation.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Pen color configured in show properties (0.3 points)
    # The presence of <p:penClr> within <p:showPr> indicates the pen/pointer is configured
    try:
        if show_pr is not None:
            pen_clr = show_pr.find(f'{{{NS_P}}}penClr')
            if pen_clr is not None:
                # Verify it has a color child (srgbClr or similar)
                color_el = pen_clr.find(f'{{{NS_A}}}srgbClr')
                if color_el is not None:
                    color_val = color_el.get('val')
                    print(f"PASS: Component 2 — Pen color configured in showPr (color={color_val}) (0.3 pts)")
                    total_score += 0.3
                else:
                    # Accept any color specification (theme, etc.)
                    children = list(pen_clr)
                    if len(children) > 0:
                        print(f"PASS: Component 2 — Pen color configured in showPr (non-srgb color) (0.3 pts)")
                        total_score += 0.3
                    else:
                        print("FAIL: Component 2 — penClr element found but has no color child")
            else:
                print("FAIL: Component 2 — No <p:penClr> element found in showPr")
        else:
            print("FAIL: Component 2 — No <p:showPr> element found in presentation.xml")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: End with black slide enabled (0.3 points)
    # This is stored in LibreOffice's registrymodifications.xcu, NOT in the PPTX file
    try:
        if os.path.exists(LO_CONFIG):
            with open(LO_CONFIG, 'r') as f:
                config_content = f.read()
            # Look for EndWithBlackSlide setting
            pattern = r'<prop\s+oor:name="EndWithBlackSlide"[^>]*>\s*<value>(.*?)</value>'
            match = re.search(pattern, config_content)
            if match:
                value = match.group(1).strip().lower()
                if value == 'true':
                    print(f"PASS: Component 3 — EndWithBlackSlide=true in LO config (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — EndWithBlackSlide={value}, expected true")
            else:
                print("FAIL: Component 3 — EndWithBlackSlide setting not found in LO config")
        else:
            print(f"FAIL: Component 3 — LibreOffice config not found at {LO_CONFIG}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
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
