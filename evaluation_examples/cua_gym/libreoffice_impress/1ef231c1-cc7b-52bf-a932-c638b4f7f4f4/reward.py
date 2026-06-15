"""
Reward Script: Verify custom slide shows in product_launch.pptx
Task ID: impress_gf5_013
Domain: libreoffice_impress
Scoring:
  Gate: Original slide order preserved (15 slides, 1-15) — precondition, not scored
  Component 1 (0.20): "Executive Version" custom show exists
  Component 2 (0.30): "Executive Version" has correct slides [1,2,5,8,12] in order
  Component 3 (0.20): "Technical Deep Dive" custom show exists
  Component 4 (0.30): "Technical Deep Dive" has correct slides [1,3,4,6,7,9,10] in order
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf5_013'

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'


def build_rid_to_slide_map(zf):
    """Map relationship IDs to slide numbers from presentation.xml.rels."""
    rid_map = {}
    with zf.open('ppt/_rels/presentation.xml.rels') as rf:
        rels_root = ET.fromstring(rf.read())
        for rel in rels_root.findall(f'{{{NS_PKG}}}Relationship'):
            target = rel.get('Target', '')
            rid = rel.get('Id', '')
            if target.startswith('slides/slide'):
                slide_num = int(target.replace('slides/slide', '').replace('.xml', ''))
                rid_map[rid] = slide_num
    return rid_map


def parse_custom_shows(zf, rid_map):
    """Parse custom shows from presentation.xml, returning {name: [slide_nums]}."""
    with zf.open('ppt/presentation.xml') as f:
        root = ET.fromstring(f.read())

    shows = {}
    cust_show_lst = root.find(f'.//{{{NS_P}}}custShowLst')
    if cust_show_lst is None:
        return shows

    for cs in cust_show_lst.findall(f'{{{NS_P}}}custShow'):
        name = cs.get('name', '')
        slide_nums = []
        sld_lst = cs.find(f'{{{NS_P}}}sldLst')
        if sld_lst is not None:
            for sld in sld_lst.findall(f'{{{NS_P}}}sld'):
                rid = sld.get(f'{{{NS_R}}}id', '')
                slide_nums.append(rid_map.get(rid, -1))
        shows[name] = slide_nums
    return shows


def get_slide_order(zf, rid_map):
    """Return ordered list of slide numbers from the main presentation."""
    with zf.open('ppt/presentation.xml') as f:
        root = ET.fromstring(f.read())
    sld_id_lst = root.find(f'.//{{{NS_P}}}sldIdLst')
    if sld_id_lst is None:
        return []
    order = []
    for sld_id in sld_id_lst.findall(f'{{{NS_P}}}sldId'):
        rid = sld_id.get(f'{{{NS_R}}}id', '')
        order.append(rid_map.get(rid, -1))
    return order


def verify_task(file_path):
    """
    Verify custom slide show creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        rid_map = build_rid_to_slide_map(zf)
    except Exception as e:
        print(f"CRITICAL: Cannot parse relationships: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    try:
        shows = parse_custom_shows(zf, rid_map)
    except Exception as e:
        print(f"CRITICAL: Cannot parse custom shows: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Gate: Original slide order preserved (precondition, not scored)
    expected_order = list(range(1, 16))
    try:
        slide_order = get_slide_order(zf, rid_map)
        if slide_order != expected_order:
            print(f"GATE FAIL: Slide order changed — {slide_order}, expected {expected_order}")
            print(f"REWARD: 0.0")
            zf.close()
            return 0.0
        else:
            print(f"GATE PASS: Slide order preserved: {slide_order}")
    except Exception as e:
        print(f"GATE ERROR: Could not check slide order: {e}")

    print(f"Found {len(shows)} custom show(s): {list(shows.keys())}")

    # Component 1: "Executive Version" custom show exists (0.20 points)
    exec_exists = False
    try:
        if 'Executive Version' in shows:
            print(f"PASS: Component 1 — 'Executive Version' custom show exists (0.20 pts)")
            total_score += 0.20
            exec_exists = True
        else:
            print(f"FAIL: Component 1 — 'Executive Version' not found among: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: "Executive Version" has slides [1,2,5,8,12] in order (0.30 points)
    expected_exec = [1, 2, 5, 8, 12]
    try:
        if exec_exists:
            actual = shows['Executive Version']
            if actual == expected_exec:
                print(f"PASS: Component 2 — 'Executive Version' slides {actual} match expected {expected_exec} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — 'Executive Version' slides {actual}, expected {expected_exec}")
        else:
            print(f"FAIL: Component 2 — 'Executive Version' does not exist, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Technical Deep Dive" custom show exists (0.20 points)
    tech_exists = False
    try:
        if 'Technical Deep Dive' in shows:
            print(f"PASS: Component 3 — 'Technical Deep Dive' custom show exists (0.20 pts)")
            total_score += 0.20
            tech_exists = True
        else:
            print(f"FAIL: Component 3 — 'Technical Deep Dive' not found among: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "Technical Deep Dive" has slides [1,3,4,6,7,9,10] in order (0.30 points)
    expected_tech = [1, 3, 4, 6, 7, 9, 10]
    try:
        if tech_exists:
            actual = shows['Technical Deep Dive']
            if actual == expected_tech:
                print(f"PASS: Component 4 — 'Technical Deep Dive' slides {actual} match expected {expected_tech} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 4 — 'Technical Deep Dive' slides {actual}, expected {expected_tech}")
        else:
            print(f"FAIL: Component 4 — 'Technical Deep Dive' does not exist, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

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
