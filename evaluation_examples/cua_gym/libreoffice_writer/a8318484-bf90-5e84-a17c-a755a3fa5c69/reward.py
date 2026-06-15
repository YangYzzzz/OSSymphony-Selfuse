"""
Reward Script: Set up page border with box arrangement using solid red (#FF0000) line at 2pt width,
               padding 1cm from page edge on all sides.
Task ID: writer_page_063
Domain: libreoffice_writer
Scoring:
  Component 1: All four page borders present (box arrangement) — 0.3 pts
  Component 2: Border color is red (#FF0000) on all sides — 0.3 pts
  Component 3: Border width is 2pt (sz=16 in 1/8pt units) on all sides — 0.2 pts
  Component 4: Border padding is ~1cm from page edge (space≈28pt) on all sides — 0.2 pts
  Total: 1.0
"""

import os
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_063'
FILE_PATH = f'{WORKDIR}/safety_notice.docx'

# Namespaces for OOXML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = f'{{{W_NS}}}'

SIDES = ['top', 'left', 'bottom', 'right']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Verification approach:
    - Load the .docx file using python-docx to access the sectPr XML
    - Check for the presence of <w:pgBorders> with all four sides
    - Verify border color is FF0000 (red) on all sides
    - Verify border width is sz=16 (2pt in 1/8pt units) on all sides
    - Verify padding (space attribute) is approximately 28pt (~1cm) on all sides
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get section properties XML
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
    except Exception as e:
        print(f"CRITICAL: Cannot access section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All four page borders present (box arrangement) — 0.3 pts
    # Initial: no pgBorders element. Golden: pgBorders with top, left, bottom, right.
    try:
        pgBorders = sectPr.find(f'{W}pgBorders')
        if pgBorders is None:
            print("FAIL: Component 1 — No <w:pgBorders> element found (no page border set)")
        else:
            sides_present = [pgBorders.find(f'{W}{side}') is not None for side in SIDES]
            if all(sides_present):
                print(f"PASS: Component 1 — All four page border sides present (box arrangement) (0.3 pts)")
                total_score += 0.3
            else:
                missing = [s for s, p in zip(SIDES, sides_present) if not p]
                print(f"FAIL: Component 1 — Missing border sides: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Border color is red (#FF0000) on all sides — 0.3 pts
    # Initial: no borders. Golden: color="FF0000" on all four sides.
    try:
        pgBorders = sectPr.find(f'{W}pgBorders')
        if pgBorders is None:
            print("FAIL: Component 2 — No <w:pgBorders> element found")
        else:
            color_results = {}
            for side in SIDES:
                elem = pgBorders.find(f'{W}{side}')
                if elem is not None:
                    color = elem.get(f'{W}color', '').upper()
                    color_results[side] = color
                else:
                    color_results[side] = None

            all_red = all(
                color_results.get(s) == 'FF0000'
                for s in SIDES
            )
            if all_red:
                print(f"PASS: Component 2 — All four sides have red color (#FF0000) (0.3 pts)")
                total_score += 0.3
            else:
                bad = {s: v for s, v in color_results.items() if v != 'FF0000'}
                print(f"FAIL: Component 2 — Expected FF0000, found mismatches: {bad}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Border width is 2pt (sz=16 in 1/8pt units) on all sides — 0.2 pts
    # Initial: no borders. Golden: sz="16" on all four sides (2pt = 16 eighths-of-a-point).
    try:
        pgBorders = sectPr.find(f'{W}pgBorders')
        if pgBorders is None:
            print("FAIL: Component 3 — No <w:pgBorders> element found")
        else:
            sz_results = {}
            for side in SIDES:
                elem = pgBorders.find(f'{W}{side}')
                if elem is not None:
                    sz_val = elem.get(f'{W}sz')
                    sz_results[side] = int(sz_val) if sz_val is not None else None
                else:
                    sz_results[side] = None

            # sz=16 means 2pt (16 * 1/8pt = 2pt)
            # Allow slight tolerance: sz in [14, 18] ~ 1.75pt to 2.25pt
            all_2pt = all(
                sz_results.get(s) is not None and 14 <= sz_results[s] <= 18
                for s in SIDES
            )
            if all_2pt:
                actual_pt = sz_results['top'] / 8.0
                print(f"PASS: Component 3 — All sides have width ~2pt (sz={sz_results['top']}, = {actual_pt}pt) (0.2 pts)")
                total_score += 0.2
            else:
                bad = {s: v for s, v in sz_results.items() if v is None or not (14 <= v <= 18)}
                print(f"FAIL: Component 3 — Expected sz=16 (2pt), found mismatches: {bad}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Padding from page edge is ~1cm (space≈28pt) on all sides — 0.2 pts
    # Initial: no borders. Golden: space="28" on all four sides, offsetFrom="page".
    # 1cm = 28.346pt ≈ 28pt. Allow tolerance: space in [24, 32].
    try:
        pgBorders = sectPr.find(f'{W}pgBorders')
        if pgBorders is None:
            print("FAIL: Component 4 — No <w:pgBorders> element found")
        else:
            # Check offsetFrom="page"
            offset_from = pgBorders.get(f'{W}offsetFrom', '')
            space_results = {}
            for side in SIDES:
                elem = pgBorders.find(f'{W}{side}')
                if elem is not None:
                    space_val = elem.get(f'{W}space')
                    space_results[side] = int(space_val) if space_val is not None else None
                else:
                    space_results[side] = None

            # space is in points; 1cm = 28.346pt → accept range [24, 32]
            all_1cm = all(
                space_results.get(s) is not None and 24 <= space_results[s] <= 32
                for s in SIDES
            )
            offset_ok = (offset_from == 'page')

            if all_1cm and offset_ok:
                actual_cm = space_results['top'] / 28.346
                print(f"PASS: Component 4 — All sides have ~1cm padding from page edge "
                      f"(space={space_results['top']}pt ≈ {actual_cm:.2f}cm, offsetFrom=page) (0.2 pts)")
                total_score += 0.2
            elif all_1cm and not offset_ok:
                actual_cm = space_results['top'] / 28.346
                print(f"FAIL: Component 4 — Space values OK (~{actual_cm:.2f}cm) "
                      f"but offsetFrom='{offset_from}' (expected 'page')")
            else:
                bad = {s: v for s, v in space_results.items() if v is None or not (24 <= v <= 32)}
                print(f"FAIL: Component 4 — Expected space≈28pt (~1cm from page), "
                      f"found mismatches: {bad} (offsetFrom='{offset_from}')")
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
