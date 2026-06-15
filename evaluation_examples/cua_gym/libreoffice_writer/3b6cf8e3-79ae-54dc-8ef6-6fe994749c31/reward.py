"""
Reward Script: Set page border padding to 2cm from the page edge on all four sides
Task ID: writer_page_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.7 pts): Border padding (w:space) changed to ~2cm (55-58 pts) on all four sides
  Component 2 (0.3 pts): Border style (val, color, sz) preserved AND padding is ~2cm — compound check
                          (fails on initial because padding is still 0.5cm)
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_048'
FILE_NAME = 'framed_announcement.docx'

# Tolerance: 2.0cm = 56.693 points; accept 55-58 (within ~1.5% tolerance)
TARGET_SPACE_MIN = 55
TARGET_SPACE_MAX = 58

SIDE_NAMES = ['top', 'left', 'bottom', 'right']
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_pg_borders(doc):
    """Return the pgBorders element from the first section, or None."""
    from docx.oxml.ns import qn
    section = doc.sections[0]
    sect_pr = section._sectPr
    return sect_pr.find(qn('w:pgBorders'))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Checks:
      1. Page border padding on all four sides changed to ~2.0cm (w:space in [55,58])
      2. Border style preserved (val=single, color=0000FF, sz=8) AND padding ~2cm — compound check
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate pgBorders element (precondition gate — no score awarded for existence)
    try:
        pg_borders = get_pg_borders(doc)
        if pg_borders is None:
            print("FAIL: No pgBorders element found — document has no page border")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"CRITICAL: Cannot read pgBorders: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect border attributes for all four sides
    side_data = {}
    for side in SIDE_NAMES:
        el = pg_borders.find(f'{{{W_NS}}}{side}')
        if el is None:
            side_data[side] = {}
        else:
            space_str = el.get(f'{{{W_NS}}}space')
            side_data[side] = {
                'val':   el.get(f'{{{W_NS}}}val'),
                'sz':    el.get(f'{{{W_NS}}}sz'),
                'color': el.get(f'{{{W_NS}}}color'),
                'space': int(space_str) if space_str is not None else None,
            }

    # Component 1: Border padding changed to ~2cm on all four sides (0.7 points)
    # This FAILS on initial_env (space=14) and PASSES on golden_env (space=57)
    try:
        space_values = {s: side_data[s].get('space') for s in SIDE_NAMES}
        all_padding_correct = all(
            v is not None and TARGET_SPACE_MIN <= v <= TARGET_SPACE_MAX
            for v in space_values.values()
        )
        if all_padding_correct:
            print(f"PASS: Component 1 — Border padding set to ~2cm on all sides: {space_values} (0.7 pts)")
            total_score += 0.7
        else:
            print(f"FAIL: Component 1 — Expected w:space in [{TARGET_SPACE_MIN},{TARGET_SPACE_MAX}] on all sides; found: {space_values}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Border style preserved (single, 0000FF, 1pt=sz8) AND padding ~2cm (compound) (0.3 points)
    # Compound: requires BOTH padding ~2cm AND correct style on every side.
    # Because the padding requirement is embedded, this FAILS on initial_env.
    try:
        compound_checks = {}
        for side in SIDE_NAMES:
            d = side_data[side]
            space_ok = d.get('space') is not None and TARGET_SPACE_MIN <= d['space'] <= TARGET_SPACE_MAX
            val_ok   = d.get('val') == 'single'
            color_ok = d.get('color') is not None and d['color'].upper() == '0000FF'
            sz_ok    = d.get('sz') == '8'
            compound_checks[side] = space_ok and val_ok and color_ok and sz_ok
            if not compound_checks[side]:
                details = (f"space={d.get('space')}, val={d.get('val')}, "
                           f"color={d.get('color')}, sz={d.get('sz')}")
                print(f"FAIL: Component 2 side '{side}' — {details}")

        if all(compound_checks.values()):
            print("PASS: Component 2 — All sides have 2cm padding and preserved style (single/0000FF/sz=8) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Compound padding+style check failed: {compound_checks}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
