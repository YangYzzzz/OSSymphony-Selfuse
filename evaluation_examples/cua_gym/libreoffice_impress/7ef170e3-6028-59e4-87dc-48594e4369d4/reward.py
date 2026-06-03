"""
Reward Script: Set up a custom slide show named 'Quick Demo' with slides 1, 3, 5, 7, and 10
Task ID: impress_sales_039
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Custom show named 'Quick Demo' exists
  Component 2 (0.3): Custom show contains exactly 5 slides
  Component 3 (0.3): The 5 slides are exactly slides 1, 3, 5, 7, and 10 (correct rIds)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_sales_039'

def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
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
    Verify that a custom slide show named 'Quick Demo' exists
    and contains exactly slides 1, 3, 5, 7, and 10.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    ns = {'p': ns_p, 'r': ns_r}

    try:
        zf = zipfile.ZipFile(file_path, 'r')
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build slide index: map rId -> 1-based slide number
    sld_id_lst = root.find(f'.//{{{ns_p}}}sldIdLst')
    if sld_id_lst is None:
        print("FAIL: No sldIdLst found in presentation.xml")
        print("REWARD: 0.0")
        return 0.0

    slide_rids = []
    for sld_id in sld_id_lst.findall(f'{{{ns_p}}}sldId'):
        rid = sld_id.get(f'{{{ns_r}}}id')
        slide_rids.append(rid)

    rid_to_slide_num = {rid: idx + 1 for idx, rid in enumerate(slide_rids)}
    print(f"INFO: Found {len(slide_rids)} slides. rId mapping: {rid_to_slide_num}")

    # Find custShowLst
    cust_show_lst = root.find(f'.//{{{ns_p}}}custShowLst')
    if cust_show_lst is None:
        print("FAIL: No custShowLst found — no custom slide shows defined")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Custom show named 'Quick Demo' exists (0.4 points)
    try:
        quick_demo = None
        for show in cust_show_lst.findall(f'{{{ns_p}}}custShow'):
            name = show.get('name', '')
            print(f"INFO: Found custom show: '{name}'")
            if name == 'Quick Demo':
                quick_demo = show
                break

        if quick_demo is not None:
            print(f"PASS: Component 1 — Custom show 'Quick Demo' exists (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No custom show named 'Quick Demo' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if quick_demo is None:
        # Can't check further components without the show
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Get slide rIds in the custom show
    sld_lst = quick_demo.find(f'{{{ns_p}}}sldLst')
    show_rids = []
    if sld_lst is not None:
        for sld in sld_lst.findall(f'{{{ns_p}}}sld'):
            rid = sld.get(f'{{{ns_r}}}id')
            if rid:
                show_rids.append(rid)

    show_slide_nums = [rid_to_slide_num.get(rid, -1) for rid in show_rids]
    print(f"INFO: Custom show slide rIds: {show_rids}")
    print(f"INFO: Custom show slide numbers: {show_slide_nums}")

    expected_slides = [1, 3, 5, 7, 10]

    # Component 2: Custom show contains exactly 5 slides (0.3 points)
    try:
        if len(show_rids) == 5:
            print(f"PASS: Component 2 — Custom show has exactly 5 slides (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 5 slides, found {len(show_rids)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The slides are exactly 1, 3, 5, 7, 10 in order (0.3 points)
    try:
        if show_slide_nums == expected_slides:
            print(f"PASS: Component 3 — Slides are exactly {expected_slides} in order (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected slides {expected_slides}, found {show_slide_nums}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
