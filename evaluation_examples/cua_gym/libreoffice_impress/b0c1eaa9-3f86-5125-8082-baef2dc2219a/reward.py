"""
Reward Script: Create two custom slide shows in a presentation
Task ID: impress_fix_036
Domain: libreoffice_impress
Scoring:
  - Component 1: 'Technical Deep Dive' show exists (0.15)
  - Component 2: 'Technical Deep Dive' has correct slides (0.35)
  - Component 3: 'Business Overview' show exists (0.15)
  - Component 4: 'Business Overview' has correct slides (0.35)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_036'

# Expected custom slide shows
EXPECTED_SHOWS = {
    'Technical Deep Dive': [1, 4, 5, 6, 8, 10, 14, 15, 18, 20],
    'Business Overview': [1, 2, 3, 7, 11, 16, 19, 20],
}


def parse_custom_shows(pptx_path):
    """
    Parse custom slide shows from a .pptx file by reading the XML directly.
    Returns a dict: {show_name: [slide_numbers]} or None if no custom shows.
    """
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    ns_pkg = 'http://schemas.openxmlformats.org/package/2006/relationships'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Build rId -> slide number mapping from rels
        with zf.open('ppt/_rels/presentation.xml.rels') as f:
            rels_root = ET.parse(f).getroot()
        rid_to_num = {}
        for rel in rels_root.findall(f'{{{ns_pkg}}}Relationship'):
            rid = rel.get('Id')
            target = rel.get('Target')
            if target and 'slide' in target.lower() and 'slideLayout' not in target and 'slideMaster' not in target:
                m = re.search(r'slide(\d+)\.xml', target)
                if m:
                    rid_to_num[rid] = int(m.group(1))

        # Parse presentation.xml for custom shows
        with zf.open('ppt/presentation.xml') as f:
            pres_root = ET.parse(f).getroot()

        cust_show_lst = pres_root.find(f'.//{{{ns_p}}}custShowLst')
        if cust_show_lst is None:
            return None

        shows = {}
        for show in cust_show_lst.findall(f'{{{ns_p}}}custShow'):
            name = show.get('name')
            sld_lst = show.find(f'{{{ns_p}}}sldLst')
            slide_nums = []
            if sld_lst is not None:
                for sld in sld_lst.findall(f'{{{ns_p}}}sld'):
                    rid = sld.get(f'{{{ns_r}}}id')
                    num = rid_to_num.get(rid)
                    if num is not None:
                        slide_nums.append(num)
            shows[name] = slide_nums

        return shows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        shows = parse_custom_shows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse pptx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if shows is None:
        print("FAIL: No custom slide shows found in presentation")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(shows)} custom show(s): {list(shows.keys())}")

    # Component 1: 'Technical Deep Dive' show exists (0.15 points)
    try:
        if 'Technical Deep Dive' in shows:
            print(f"PASS: Component 1 -- 'Technical Deep Dive' show exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- 'Technical Deep Dive' show not found. Shows: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'Technical Deep Dive' has correct slides (0.35 points)
    try:
        expected = EXPECTED_SHOWS['Technical Deep Dive']
        if 'Technical Deep Dive' in shows:
            actual = shows['Technical Deep Dive']
            if actual == expected:
                print(f"PASS: Component 2 -- 'Technical Deep Dive' slides correct: {actual} (0.35 pts)")
                total_score += 0.35
            else:
                # Partial credit: fraction of correct slides in correct positions
                matching = sum(1 for a, e in zip(actual, expected) if a == e)
                max_len = max(len(actual), len(expected))
                if max_len > 0 and matching > 0:
                    partial = 0.35 * (matching / max_len)
                    # Only give partial if at least half match
                    if matching >= max_len / 2:
                        total_score += round(partial, 4)
                        print(f"PARTIAL: Component 2 -- 'Technical Deep Dive' slides partially correct. Expected: {expected}, Got: {actual}. Matched {matching}/{max_len} (+{round(partial, 4)} pts)")
                    else:
                        print(f"FAIL: Component 2 -- 'Technical Deep Dive' slides wrong. Expected: {expected}, Got: {actual}")
                else:
                    print(f"FAIL: Component 2 -- 'Technical Deep Dive' slides wrong. Expected: {expected}, Got: {actual}")
        else:
            print(f"FAIL: Component 2 -- 'Technical Deep Dive' show does not exist, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'Business Overview' show exists (0.15 points)
    try:
        if 'Business Overview' in shows:
            print(f"PASS: Component 3 -- 'Business Overview' show exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- 'Business Overview' show not found. Shows: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'Business Overview' has correct slides (0.35 points)
    try:
        expected = EXPECTED_SHOWS['Business Overview']
        if 'Business Overview' in shows:
            actual = shows['Business Overview']
            if actual == expected:
                print(f"PASS: Component 4 -- 'Business Overview' slides correct: {actual} (0.35 pts)")
                total_score += 0.35
            else:
                matching = sum(1 for a, e in zip(actual, expected) if a == e)
                max_len = max(len(actual), len(expected))
                if max_len > 0 and matching > 0:
                    partial = 0.35 * (matching / max_len)
                    if matching >= max_len / 2:
                        total_score += round(partial, 4)
                        print(f"PARTIAL: Component 4 -- 'Business Overview' slides partially correct. Expected: {expected}, Got: {actual}. Matched {matching}/{max_len} (+{round(partial, 4)} pts)")
                    else:
                        print(f"FAIL: Component 4 -- 'Business Overview' slides wrong. Expected: {expected}, Got: {actual}")
                else:
                    print(f"FAIL: Component 4 -- 'Business Overview' slides wrong. Expected: {expected}, Got: {actual}")
        else:
            print(f"FAIL: Component 4 -- 'Business Overview' show does not exist, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
