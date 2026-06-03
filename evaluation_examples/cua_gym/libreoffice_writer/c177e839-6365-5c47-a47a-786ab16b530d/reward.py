"""
Reward Script: Add bookmarks to key sections of an employee handbook
Task ID: writer_hr_055
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Correct total bookmark count (8)
  Component 2 (0.4): All 8 expected bookmark names present (0.05 each)
  Component 3 (0.3): Bookmarks placed at correct heading paragraphs (0.0375 each)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_055'

# Expected bookmarks: name -> heading text they should be anchored to
EXPECTED_BOOKMARKS = {
    'Section_Introduction': 'Introduction',
    'Section_Employment_Policies': 'Employment Policies',
    'Section_Compensation': 'Compensation',
    'Section_Benefits': 'Benefits',
    'Section_Leave_Policies': 'Leave Policies',
    'Section_Code_of_Conduct': 'Code of Conduct',
    'Section_Safety': 'Safety',
    'Section_Acknowledgment': 'Acknowledgment',
}

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body
    bookmark_starts = body.findall('.//w:bookmarkStart', NS)

    # Build a dict of bookmark_name -> parent paragraph text
    bm_map = {}
    for bm in bookmark_starts:
        name = bm.get(f'{{{WNS}}}name', '')
        # Skip internal bookmarks like _GoBack
        if name.startswith('_'):
            continue
        parent = bm.getparent()
        if parent is not None:
            texts = parent.findall('.//w:t', NS)
            para_text = ''.join((t.text or '') for t in texts).strip()
        else:
            para_text = ''
        bm_map[name] = para_text

    num_bookmarks = len(bm_map)
    print(f"INFO: Found {num_bookmarks} bookmarks (excluding internal): {list(bm_map.keys())}")

    # Component 1: Correct total bookmark count (0.3 points)
    try:
        if num_bookmarks == 8:
            print(f"PASS: Component 1 - Correct bookmark count: {num_bookmarks} (0.3 pts)")
            total_score += 0.3
        elif num_bookmarks > 0:
            # Partial: proportional but capped
            partial = min(0.2, 0.025 * num_bookmarks)
            print(f"PARTIAL: Component 1 - Found {num_bookmarks}/8 bookmarks ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No bookmarks found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All 8 expected bookmark names present (0.4 points, 0.05 each)
    try:
        name_score = 0.0
        for bm_name in EXPECTED_BOOKMARKS:
            if bm_name in bm_map:
                name_score += 0.05
                print(f"PASS: Component 2 - Bookmark '{bm_name}' found (0.05 pts)")
            else:
                print(f"FAIL: Component 2 - Bookmark '{bm_name}' NOT found")
        if name_score > 0:
            total_score += name_score
            print(f"SUBTOTAL: Component 2 - {name_score:.2f}/0.40 pts")
        else:
            print(f"FAIL: Component 2 - No expected bookmark names found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Bookmarks placed at correct heading paragraphs (0.3 points, 0.0375 each)
    try:
        placement_score = 0.0
        for bm_name, expected_heading in EXPECTED_BOOKMARKS.items():
            if bm_name in bm_map:
                actual_text = bm_map[bm_name]
                if expected_heading.lower() in actual_text.lower():
                    placement_score += 0.0375
                    print(f"PASS: Component 3 - '{bm_name}' correctly at '{actual_text}' (0.0375 pts)")
                else:
                    print(f"FAIL: Component 3 - '{bm_name}' at wrong paragraph: '{actual_text}' (expected '{expected_heading}')")
            else:
                print(f"FAIL: Component 3 - '{bm_name}' missing, cannot check placement")
        if placement_score > 0:
            total_score += placement_score
            print(f"SUBTOTAL: Component 3 - {placement_score:.4f}/0.30 pts")
        else:
            print(f"FAIL: Component 3 - No bookmarks correctly placed")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
