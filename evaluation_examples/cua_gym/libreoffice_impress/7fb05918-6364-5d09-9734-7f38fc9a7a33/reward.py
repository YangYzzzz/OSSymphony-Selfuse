"""
Reward Script: Create custom slide show 'Executive Summary' with slides 1, 3, 7, 12, 15
Task ID: impress_fix_035
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.3): Custom show named 'Executive Summary' exists
  - Component 2 (0.4): Custom show contains exactly slides 1, 3, 7, 12, 15 in order
  - Component 3 (0.2): Only one custom show exists (no extras)
  - Component 4 (0.1): All 20 original slides preserved
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_035'

# Namespaces used in OOXML presentation.xml
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

EXPECTED_SHOW_NAME = 'Executive Summary'
EXPECTED_SLIDES = [1, 3, 7, 12, 15]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load or parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'p': P_NS}

    # Build rId -> slide number mapping from sldIdLst
    try:
        sldIdLst = root.find('.//p:sldIdLst', ns)
        sld_ids = sldIdLst.findall('p:sldId', ns) if sldIdLst is not None else []
        rid_to_num = {}
        for i, sld in enumerate(sld_ids):
            rid = sld.get('{' + R_NS + '}id')
            rid_to_num[rid] = i + 1
        total_slides = len(sld_ids)
        print(f"INFO: Found {total_slides} slides, rId mapping built with {len(rid_to_num)} entries")
    except Exception as e:
        print(f"ERROR: Could not build slide mapping: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all custom shows
    cust_show_lst = root.find('.//p:custShowLst', ns)
    cust_shows = cust_show_lst.findall('p:custShow', ns) if cust_show_lst is not None else []
    show_names = [s.get('name') for s in cust_shows]
    print(f"INFO: Custom shows found: {show_names}")

    # Component 1: Custom show named 'Executive Summary' exists (0.3 points)
    try:
        target_show = None
        for show in cust_shows:
            if show.get('name') == EXPECTED_SHOW_NAME:
                target_show = show
                break

        if target_show is not None:
            print(f"PASS: Component 1 — Custom show '{EXPECTED_SHOW_NAME}' exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Custom show '{EXPECTED_SHOW_NAME}' not found. Found: {show_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Custom show contains exactly slides 1, 3, 7, 12, 15 in order (0.4 points)
    try:
        if target_show is not None:
            sld_lst = target_show.find('p:sldLst', ns)
            show_slds = sld_lst.findall('p:sld', ns) if sld_lst is not None else []
            actual_slides = []
            for sld in show_slds:
                rid = sld.get('{' + R_NS + '}id')
                slide_num = rid_to_num.get(rid, -1)
                actual_slides.append(slide_num)

            if actual_slides == EXPECTED_SLIDES:
                print(f"PASS: Component 2 — Custom show slides are {actual_slides} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected slides {EXPECTED_SLIDES}, found {actual_slides}")
        else:
            print(f"FAIL: Component 2 — No target show to check slides")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly one custom show exists, correctly named, AND all 20 slides preserved (0.3 points)
    # Compound check: the custom show must exist (task change) AND slides must be intact (integrity)
    try:
        if len(cust_shows) == 1 and cust_shows[0].get('name') == EXPECTED_SHOW_NAME and total_slides == 20:
            print(f"PASS: Component 3 — Exactly 1 custom show, correctly named, all 20 slides preserved (0.3 pts)")
            total_score += 0.3
        elif len(cust_shows) == 0:
            print(f"FAIL: Component 3 — No custom shows exist")
        elif total_slides != 20:
            print(f"FAIL: Component 3 — Expected 20 slides, found {total_slides}")
        else:
            extra = [s.get('name') for s in cust_shows if s.get('name') != EXPECTED_SHOW_NAME]
            print(f"FAIL: Component 3 — Found {len(cust_shows)} custom shows, extras: {extra}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice changes
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
