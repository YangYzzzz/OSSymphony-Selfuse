"""
Reward Script: Remove page border from top and bottom, keeping only left and right borders.
Task ID: writer_page_038
Domain: libreoffice_writer
Scoring:
  Component 1: Top border removed from pgBorders (0.4 pts)
  Component 2: Bottom border removed AND only left+right remain (0.6 pts)
  Total: 1.0

Design note: Component 3 (left/right preserved) must be coupled with a task-change
check to avoid scoring a pre-existing property that is true in both initial and golden states.
The combined check in Component 2 — bottom removed AND left+right are the ONLY borders —
ensures it fails on initial (where top+bottom also exist) and passes on golden.
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'memo_template'

# Canonical file path on the VM
FILE_PATH = f'{WORKDIR}/Desktop/{TASK_ID}.docx'


def verify_task(file_path):
    """
    Verify task completion: page border removed from top and bottom,
    left and right borders kept (solid black, sz=8).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the pgBorders element in the section properties
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        pgBorders = sectPr.find(qn('w:pgBorders'))
        if pgBorders is None:
            print("FAIL: No w:pgBorders element found in document — cannot verify any border.")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"CRITICAL: Cannot access section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Top border removed (0.4 points)
    # Task requires: top border must be absent from pgBorders
    # FAILS on initial (top present), PASSES on golden (top absent)
    try:
        top_elem = pgBorders.find(qn('w:top'))
        if top_elem is None:
            print("PASS: Component 1 — Top border element is absent (correctly removed) (0.4 pts)")
            total_score += 0.4
        else:
            top_val = top_elem.get(qn('w:val'), '')
            print(f"FAIL: Component 1 — Top border still present (w:val='{top_val}'). Expected: absent.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bottom border removed AND left+right are the ONLY remaining borders (0.6 points)
    # Verifies BOTH that bottom is removed AND that the total set of borders is exactly {left, right}.
    # This compound check FAILS on initial (bottom+top still present, total = 4 borders)
    # and PASSES on golden (bottom absent, top absent, total = 2 borders: left+right).
    try:
        bottom_elem = pgBorders.find(qn('w:bottom'))

        # All border child elements with valid (non-nil) style
        border_tags = {'w:top', 'w:left', 'w:bottom', 'w:right', 'w:insideH', 'w:insideV'}
        present_borders = set()
        for child in pgBorders:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            full_tag = f'w:{local}'
            if full_tag in border_tags:
                val = child.get(qn('w:val'), '')
                if val and val != 'none' and val != 'nil':
                    present_borders.add(local)

        bottom_absent = (bottom_elem is None)
        only_left_right = (present_borders == {'left', 'right'})

        if bottom_absent and only_left_right:
            print(f"PASS: Component 2 — Bottom border absent AND exactly left+right borders remain "
                  f"(present={sorted(present_borders)}) (0.6 pts)")
            total_score += 0.6
        else:
            if not bottom_absent:
                bottom_val = bottom_elem.get(qn('w:val'), '')
                print(f"FAIL: Component 2 — Bottom border still present (w:val='{bottom_val}'). "
                      f"Present borders: {sorted(present_borders)}")
            else:
                print(f"FAIL: Component 2 — Border set is not exactly left+right. "
                      f"Present borders: {sorted(present_borders)}. Expected: ['left', 'right']")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
