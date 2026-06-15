"""
Reward Script: Set all table borders on slide 3 to solid 2pt dark blue (#003366)
Task ID: impress_tct_003
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): Border color — all borders are #003366
  Component 2 (0.4): Border width — all borders are 2pt (25400 EMU)
  Component 3 (0.2): Border style — all borders are solid single lines
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_003'

# Expected values
EXPECTED_COLOR = '003366'
EXPECTED_WIDTH = '25400'  # 2pt = 25400 EMU (1pt = 12700 EMU)
EXPECTED_DASH = 'solid'
EXPECTED_COMPOUND = 'sng'

# Table is 4 rows x 5 columns = 20 cells, each with 4 borders = 80 total borders
EXPECTED_TOTAL_BORDERS = 80

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
BORDER_TAGS = ['lnL', 'lnR', 'lnT', 'lnB']


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def extract_table_borders(pptx_path, slide_number=3):
    """
    Extract all border properties from the table on the specified slide.
    Returns a list of dicts with keys: row, col, side, width, color, dash, compound
    """
    borders = []
    slide_xml = f'ppt/slides/slide{slide_number}.xml'

    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            with z.open(slide_xml) as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide XML: {e}")
        return borders

    tbl = root.find('.//a:tbl', NS)
    if tbl is None:
        print("CRITICAL: No table found on slide 3")
        return borders

    rows = tbl.findall('a:tr', NS)
    for ri, row in enumerate(rows):
        cells = row.findall('a:tc', NS)
        for ci, tc in enumerate(cells):
            tcPr = tc.find('a:tcPr', NS)
            if tcPr is None:
                # No border properties at all — record as missing
                for side in BORDER_TAGS:
                    borders.append({
                        'row': ri, 'col': ci, 'side': side,
                        'width': None, 'color': None,
                        'dash': None, 'compound': None
                    })
                continue

            for side in BORDER_TAGS:
                ln = tcPr.find(f'a:{side}', NS)
                if ln is None:
                    borders.append({
                        'row': ri, 'col': ci, 'side': side,
                        'width': None, 'color': None,
                        'dash': None, 'compound': None
                    })
                    continue

                width = ln.get('w', None)
                compound = ln.get('cmpd', None)

                fill = ln.find('a:solidFill', NS)
                color = None
                if fill is not None:
                    clr = fill.find('a:srgbClr', NS)
                    if clr is not None:
                        color = clr.get('val', None)

                dash_el = ln.find('a:prstDash', NS)
                dash = dash_el.get('val', None) if dash_el is not None else None

                borders.append({
                    'row': ri, 'col': ci, 'side': side,
                    'width': width, 'color': color,
                    'dash': dash, 'compound': compound
                })

    return borders


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

    # Precondition: must have a table on slide 3
    borders = extract_table_borders(file_path, slide_number=3)
    if len(borders) == 0:
        print("CRITICAL: No borders extracted — table missing or unreadable")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Extracted {len(borders)} border entries from table on slide 3")

    # Component 1: Border color — all borders are #003366 (0.4 points)
    try:
        color_match = 0
        color_total = 0
        color_failures = []
        for b in borders:
            color_total += 1
            if b['color'] is not None and b['color'].upper() == EXPECTED_COLOR.upper():
                color_match += 1
            else:
                if len(color_failures) < 5:
                    color_failures.append(
                        f"Cell({b['row']},{b['col']}) {b['side']}: color={b['color']}"
                    )

        if color_total > 0 and color_match == color_total:
            print(f"PASS: Component 1 — All {color_match}/{color_total} borders have color #{EXPECTED_COLOR} (0.4 pts)")
            total_score += 0.4
        elif color_total > 0:
            ratio = color_match / color_total
            partial = round(0.4 * ratio, 2)
            print(f"FAIL: Component 1 — {color_match}/{color_total} borders have correct color (partial: {partial} pts)")
            if color_failures:
                for cf in color_failures:
                    print(f"  Detail: {cf}")
            total_score += partial
        else:
            print("FAIL: Component 1 — No borders found to check")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Border width — all borders are 2pt / 25400 EMU (0.4 points)
    try:
        width_match = 0
        width_total = 0
        width_failures = []
        for b in borders:
            width_total += 1
            if b['width'] is not None and b['width'] == EXPECTED_WIDTH:
                width_match += 1
            else:
                if len(width_failures) < 5:
                    width_failures.append(
                        f"Cell({b['row']},{b['col']}) {b['side']}: width={b['width']}"
                    )

        if width_total > 0 and width_match == width_total:
            print(f"PASS: Component 2 — All {width_match}/{width_total} borders have width 2pt (0.4 pts)")
            total_score += 0.4
        elif width_total > 0:
            ratio = width_match / width_total
            partial = round(0.4 * ratio, 2)
            print(f"FAIL: Component 2 — {width_match}/{width_total} borders have correct width (partial: {partial} pts)")
            if width_failures:
                for wf in width_failures:
                    print(f"  Detail: {wf}")
            total_score += partial
        else:
            print("FAIL: Component 2 — No borders found to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Border style — all borders are solid single lines (0.2 points)
    try:
        style_match = 0
        style_total = 0
        style_failures = []
        for b in borders:
            style_total += 1
            dash_ok = b['dash'] is not None and b['dash'] == EXPECTED_DASH
            compound_ok = b['compound'] is not None and b['compound'] == EXPECTED_COMPOUND
            if dash_ok and compound_ok:
                style_match += 1
            else:
                if len(style_failures) < 5:
                    style_failures.append(
                        f"Cell({b['row']},{b['col']}) {b['side']}: dash={b['dash']}, compound={b['compound']}"
                    )

        if style_total > 0 and style_match == style_total:
            print(f"PASS: Component 3 — All {style_match}/{style_total} borders are solid single lines (0.2 pts)")
            total_score += 0.2
        elif style_total > 0:
            ratio = style_match / style_total
            partial = round(0.2 * ratio, 2)
            print(f"FAIL: Component 3 — {style_match}/{style_total} borders have correct style (partial: {partial} pts)")
            if style_failures:
                for sf in style_failures:
                    print(f"  Detail: {sf}")
            total_score += partial
        else:
            print("FAIL: Component 3 — No borders found to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
