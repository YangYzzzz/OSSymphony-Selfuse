"""
Reward Script: Restructure bullet list hierarchy on slide 3 and remove all bullet symbols
Task ID: osworld_impress_bullet_indent_remove_008
Domain: libreoffice_impress
Scoring:
  Component 1 (0.6): Correct two-level hierarchy on slide 3
    - Items 1 and 4 at level 0 (top-level)
    - Items 2 and 3 are sub-bullets (level 1) under item 1
    - Items 5 and 6 are sub-bullets (level 1) under item 4
  Component 2 (0.4): All bullet symbols removed from all 6 items
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_bullet_indent_remove_008'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Namespace for DrawingML
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    # Parse slide 3 XML directly from the pptx zip archive
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide3.xml') as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot open/parse pptx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraphs with their text, level, and bullet info
    try:
        paragraphs_info = []
        for para in root.findall('.//a:p', ns):
            pPr = para.find('a:pPr', ns)
            lvl_str = pPr.get('lvl') if pPr is not None else None
            lvl = int(lvl_str) if lvl_str is not None else 0
            buNone = pPr.find('a:buNone', ns) if pPr is not None else None
            buChar = pPr.find('a:buChar', ns) if pPr is not None else None
            text = ''.join(t.text or '' for t in para.findall('.//a:t', ns)).strip()
            if text:
                paragraphs_info.append({
                    'text': text,
                    'level': lvl,
                    'buNone': buNone is not None,
                    'buChar': buChar
                })
    except Exception as e:
        print(f"CRITICAL: Cannot parse paragraphs from slide3: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Filter out the title (first paragraph is slide title "Process Steps")
    # Bullet items are the 6 items in the content placeholder
    bullet_items = [p for p in paragraphs_info if p['text'] != 'Process Steps']

    print(f"Found {len(bullet_items)} bullet items on slide 3:")
    for i, item in enumerate(bullet_items):
        print(f"  Item {i+1}: level={item['level']}, buNone={item['buNone']}, text='{item['text']}'")

    if len(bullet_items) < 6:
        print(f"FAIL: Expected 6 bullet items, found {len(bullet_items)}. Cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct two-level hierarchy (0.6 points)
    # Expected: items 1,4 at level 0; items 2,3,5,6 at level 1
    try:
        item1 = bullet_items[0]  # "Define Scope and Objectives" — should be level 0
        item2 = bullet_items[1]  # "Conduct Stakeholder Analysis" — should be level 1
        item3 = bullet_items[2]  # "Map Current State Processes" — should be level 1
        item4 = bullet_items[3]  # "Identify Improvement Opportunities" — should be level 0
        item5 = bullet_items[4]  # "Develop Action Plans" — should be level 1
        item6 = bullet_items[5]  # "Implement and Monitor Results" — should be level 1

        top_level_correct = (item1['level'] == 0 and item4['level'] == 0)
        sub_level_correct = (
            item2['level'] == 1 and
            item3['level'] == 1 and
            item5['level'] == 1 and
            item6['level'] == 1
        )
        hierarchy_correct = top_level_correct and sub_level_correct

        if hierarchy_correct:
            print(f"PASS: Component 1 — Hierarchy correct: items 1,4 at level 0; items 2,3,5,6 at level 1 (0.6 pts)")
            total_score += 0.6
        else:
            details = []
            if not top_level_correct:
                details.append(f"top-level: item1={item1['level']}, item4={item4['level']} (expected both 0)")
            if not sub_level_correct:
                details.append(
                    f"sub-level: item2={item2['level']}, item3={item3['level']}, "
                    f"item5={item5['level']}, item6={item6['level']} (expected all 1)"
                )
            print(f"FAIL: Component 1 — Hierarchy incorrect: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All bullet symbols removed from all 6 items (0.4 points)
    # In the golden state, each paragraph has <a:buNone/> element set
    try:
        all_bullets_removed = all(item['buNone'] for item in bullet_items)

        if all_bullets_removed:
            print(f"PASS: Component 2 — All 6 bullet symbols removed (buNone present on all items) (0.4 pts)")
            total_score += 0.4
        else:
            items_with_bullets = [i + 1 for i, item in enumerate(bullet_items) if not item['buNone']]
            print(f"FAIL: Component 2 — Bullet symbols NOT removed from items: {items_with_bullets}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the given env
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
