"""
Reward Script: Add a page border only on the bottom edge with dashed line style in gray color.
Task ID: writer_page_060
Domain: libreoffice_writer
Scoring:
  - Component 1: pgBorders element exists in sectPr (0.2 pts)
  - Component 2: Bottom border has dashed style (0.3 pts)
  - Component 3: Bottom border has gray color (#808080) (0.3 pts)
  - Component 4: Only bottom border set (no top/left/right borders) (0.2 pts)
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_FILE = 'email_template.docx'
FILE_PATH = os.path.join(WORKDIR, TASK_FILE)

# XML namespaces for OOXML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def get_sect_pr(file_path):
    """Extract the sectPr element from the document XML."""
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
    root = tree.getroot()
    body = root.find(f'{{{W_NS}}}body')
    if body is None:
        return None
    sect_pr = body.find(f'{{{W_NS}}}sectPr')
    return sect_pr


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sect_pr = get_sect_pr(file_path)
        if sect_pr is None:
            print("CRITICAL: Could not find <w:sectPr> in document.xml")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: <w:pgBorders> element exists in sectPr (0.2 points)
    # This should NOT exist in initial_env and SHOULD exist in golden_env
    try:
        pg_borders = sect_pr.find(f'{{{W_NS}}}pgBorders')
        if pg_borders is not None:
            print("PASS: Component 1 — <w:pgBorders> element found in sectPr (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — <w:pgBorders> element not found in sectPr")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        pg_borders = None

    # Component 2: Bottom border has dashed style (0.3 points)
    # Task requires style=dashed line; in OOXML this maps to w:val="dashed"
    try:
        if pg_borders is not None:
            bottom_border = pg_borders.find(f'{{{W_NS}}}bottom')
            if bottom_border is not None:
                val = bottom_border.get(f'{{{W_NS}}}val')
                if val == 'dashed':
                    print(f"PASS: Component 2 — Bottom border has dashed style (w:val='{val}') (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Bottom border style expected 'dashed', found '{val}'")
            else:
                print("FAIL: Component 2 — No <w:bottom> border element found in pgBorders")
        else:
            print("FAIL: Component 2 — Cannot check border style: pgBorders missing")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bottom border has gray color (#808080) (0.3 points)
    # Task specifies gray color (#808080); OOXML stores it as w:color="808080" (no #)
    try:
        if pg_borders is not None:
            bottom_border = pg_borders.find(f'{{{W_NS}}}bottom')
            if bottom_border is not None:
                color = bottom_border.get(f'{{{W_NS}}}color')
                if color is None:
                    color = bottom_border.get('color')
                expected_color = '808080'
                if color is not None and color.upper() == expected_color.upper():
                    print(f"PASS: Component 3 — Bottom border color is gray (#{color}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Expected bottom border color '#808080', found '{color}'")
            else:
                print("FAIL: Component 3 — No <w:bottom> border element found")
        else:
            print("FAIL: Component 3 — Cannot check border color: pgBorders missing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Only bottom border set — no top, left, or right borders (0.2 points)
    # Task says "border only on the bottom edge"
    try:
        if pg_borders is not None:
            top_border = pg_borders.find(f'{{{W_NS}}}top')
            left_border = pg_borders.find(f'{{{W_NS}}}left')
            right_border = pg_borders.find(f'{{{W_NS}}}right')
            bottom_border = pg_borders.find(f'{{{W_NS}}}bottom')

            has_bottom = bottom_border is not None
            no_top = top_border is None
            no_left = left_border is None
            no_right = right_border is None

            if has_bottom and no_top and no_left and no_right:
                print("PASS: Component 4 — Only bottom border set (no top/left/right borders) (0.2 pts)")
                total_score += 0.2
            else:
                extras = []
                if not no_top:
                    extras.append('top')
                if not no_left:
                    extras.append('left')
                if not no_right:
                    extras.append('right')
                if not has_bottom:
                    extras.append('(missing bottom)')
                print(f"FAIL: Component 4 — Expected only bottom border, found extra borders: {extras}")
        else:
            print("FAIL: Component 4 — Cannot check border sides: pgBorders missing")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
