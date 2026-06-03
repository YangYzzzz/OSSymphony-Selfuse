"""
Reward Script: Create custom slideshow 'Technical Deep Dive' with slides 1,4,5,6,7,10
Task ID: impress_tm_068
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.3): Custom show named 'Technical Deep Dive' exists
  - Component 2 (0.2): Custom show contains exactly 6 slides
  - Component 3 (0.3): Slides are 1,4,5,6,7,10 in correct order
  - Component 4 (0.2): showPr set to use this custom show as default
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_068'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

EXPECTED_SHOW_NAME = 'Technical Deep Dive'
EXPECTED_SLIDE_NUMBERS = [1, 4, 5, 6, 7, 10]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse presentation.xml from the pptx ZIP
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            pres_xml = zf.read('ppt/presentation.xml').decode()
        root = ET.fromstring(pres_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build rId-to-slide-number mapping from sldIdLst
    slide_rid_map = {}
    try:
        sld_id_lst = root.find(f'{{{NS_P}}}sldIdLst')
        if sld_id_lst is not None:
            for i, sld_id in enumerate(sld_id_lst):
                rid = sld_id.get(f'{{{NS_R}}}id')
                if rid:
                    slide_rid_map[rid] = i + 1  # 1-based slide number
        print(f"INFO: Found {len(slide_rid_map)} slides in sldIdLst")
    except Exception as e:
        print(f"ERROR: Could not build slide rId mapping: {e}")

    # Find custom show list
    cust_show_lst = root.find(f'{{{NS_P}}}custShowLst')
    target_show = None
    target_show_id = None

    if cust_show_lst is not None:
        for show in cust_show_lst:
            if show.get('name') == EXPECTED_SHOW_NAME:
                target_show = show
                target_show_id = show.get('id')
                break

    # Component 1: Custom show named 'Technical Deep Dive' exists (0.3 points)
    try:
        if target_show is not None:
            print(f"PASS: Component 1 — Custom show '{EXPECTED_SHOW_NAME}' exists with id={target_show_id} (0.3 pts)")
            total_score += 0.3
        else:
            if cust_show_lst is not None:
                names = [s.get('name') for s in cust_show_lst]
                print(f"FAIL: Component 1 — No custom show named '{EXPECTED_SHOW_NAME}'. Found: {names}")
            else:
                print(f"FAIL: Component 1 — No custShowLst element found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Custom show contains exactly 6 slides (0.2 points)
    slide_rids = []
    try:
        if target_show is not None:
            sld_lst = target_show.find(f'{{{NS_P}}}sldLst')
            if sld_lst is not None:
                slide_rids = [sld.get(f'{{{NS_R}}}id') for sld in sld_lst]
            count = len(slide_rids)
            if count == len(EXPECTED_SLIDE_NUMBERS):
                print(f"PASS: Component 2 — Custom show has {count} slides (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected {len(EXPECTED_SLIDE_NUMBERS)} slides, found {count}")
        else:
            print(f"FAIL: Component 2 — No custom show to check slide count")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slides are 1,4,5,6,7,10 in correct order (0.3 points)
    try:
        if slide_rids and slide_rid_map:
            actual_slide_nums = [slide_rid_map.get(rid, -1) for rid in slide_rids]
            if actual_slide_nums == EXPECTED_SLIDE_NUMBERS:
                print(f"PASS: Component 3 — Slide order matches {EXPECTED_SLIDE_NUMBERS} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected slide order {EXPECTED_SLIDE_NUMBERS}, found {actual_slide_nums}")
        else:
            print(f"FAIL: Component 3 — Cannot verify slide order (no custom show or no rId mapping)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: showPr set to use this custom show as default (0.2 points)
    try:
        show_pr = root.find(f'{{{NS_P}}}showPr')
        if show_pr is not None:
            cust_show_ref = show_pr.find(f'{{{NS_P}}}custShow')
            if cust_show_ref is not None:
                ref_id = cust_show_ref.get('id')
                if ref_id == target_show_id:
                    print(f"PASS: Component 4 — showPr references custShow id={ref_id} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — showPr custShow id={ref_id}, expected {target_show_id}")
            else:
                print(f"FAIL: Component 4 — showPr exists but no custShow child element")
        else:
            print(f"FAIL: Component 4 — No showPr element found in presentation.xml")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
