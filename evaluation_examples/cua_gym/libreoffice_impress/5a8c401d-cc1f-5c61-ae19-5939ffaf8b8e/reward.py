"""
Reward Script: Verify custom slide shows in Annual_Review_2025.pptx
Task ID: impress_ps_041
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.15): custShowLst element exists with exactly 3 custom shows
  - Component 2 (0.30): 'Executive Summary' show with correct slides (1,3,6,12)
  - Component 3 (0.30): 'Financial Deep Dive' show with correct slides (1,4,5,6,7)
  - Component 4 (0.25): 'Team Review' show with correct slides (1,8,9,10,11)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ps_041'

# Persistence hook: save any unsaved LibreOffice changes
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_slide_number_map(root, ns):
    """Build a mapping from rId to 1-based slide number from sldIdLst."""
    sld_id_lst = root.find('.//p:sldIdLst', ns)
    if sld_id_lst is None:
        return {}
    rid_to_num = {}
    for idx, sld_id in enumerate(sld_id_lst.findall('p:sldId', ns), start=1):
        rid = sld_id.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        if rid:
            rid_to_num[rid] = idx
    return rid_to_num


def get_custom_shows(pptx_path):
    """Parse custom slide shows from presentation.xml.
    Returns dict: {show_name: [slide_numbers_in_order]} or None if no custShowLst.
    """
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/presentation.xml') as f:
            root = ET.parse(f).getroot()

    rid_to_num = get_slide_number_map(root, ns)
    if not rid_to_num:
        print("FAIL: Could not parse sldIdLst from presentation.xml")
        return None

    cust_list = root.find('.//p:custShowLst', ns)
    if cust_list is None:
        return None

    shows = {}
    r_ns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    for show in cust_list.findall('p:custShow', ns):
        name = show.get('name', '')
        sld_lst = show.find('p:sldLst', ns)
        slide_nums = []
        if sld_lst is not None:
            for sld in sld_lst.findall('p:sld', ns):
                rid = sld.get(f'{r_ns}id')
                if rid and rid in rid_to_num:
                    slide_nums.append(rid_to_num[rid])
        shows[name] = slide_nums

    return shows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        shows = get_custom_shows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: custShowLst exists with exactly 3 custom shows (0.15 points)
    try:
        if shows is None:
            print("FAIL: Component 1 -- No custom slide shows found (custShowLst missing)")
        elif len(shows) != 3:
            print(f"FAIL: Component 1 -- Expected 3 custom shows, found {len(shows)}: {list(shows.keys())}")
        else:
            print(f"PASS: Component 1 -- Found 3 custom shows: {list(shows.keys())} (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if shows is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Expected custom shows
    expected = {
        'Executive Summary': [1, 3, 6, 12],
        'Financial Deep Dive': [1, 4, 5, 6, 7],
        'Team Review': [1, 8, 9, 10, 11],
    }

    # Component 2: 'Executive Summary' with slides 1,3,6,12 (0.30 points)
    try:
        show_name = 'Executive Summary'
        if show_name not in shows:
            print(f"FAIL: Component 2 -- '{show_name}' custom show not found. Shows: {list(shows.keys())}")
        elif shows[show_name] == expected[show_name]:
            print(f"PASS: Component 2 -- '{show_name}' has correct slides {shows[show_name]} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- '{show_name}' slides {shows[show_name]}, expected {expected[show_name]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'Financial Deep Dive' with slides 1,4,5,6,7 (0.30 points)
    try:
        show_name = 'Financial Deep Dive'
        if show_name not in shows:
            print(f"FAIL: Component 3 -- '{show_name}' custom show not found. Shows: {list(shows.keys())}")
        elif shows[show_name] == expected[show_name]:
            print(f"PASS: Component 3 -- '{show_name}' has correct slides {shows[show_name]} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- '{show_name}' slides {shows[show_name]}, expected {expected[show_name]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'Team Review' with slides 1,8,9,10,11 (0.25 points)
    try:
        show_name = 'Team Review'
        if show_name not in shows:
            print(f"FAIL: Component 4 -- '{show_name}' custom show not found. Shows: {list(shows.keys())}")
        elif shows[show_name] == expected[show_name]:
            print(f"PASS: Component 4 -- '{show_name}' has correct slides {shows[show_name]} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- '{show_name}' slides {shows[show_name]}, expected {expected[show_name]}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
