"""
Reward Script: Create 'Landscape Wide' page style with landscape A4, 1.5cm margins, 0.5pt gray border
Task ID: writer_bs_059
Domain: libreoffice_writer
Scoring:
  Component 1: New section with landscape orientation (0.25 pts)
  Component 2: A4 page size in landscape (0.20 pts)
  Component 3: All margins = 1.5cm (0.25 pts)
  Component 4: 0.5pt gray (#808080) border on all four sides (0.30 pts)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_059'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


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

    sections = list(doc.sections)

    # The task requires creating a NEW page style (section) with landscape orientation.
    # The initial document has only 1 section (portrait). The golden has 2 sections,
    # where the second section has landscape orientation + specific properties.
    # We look for ANY section (beyond the first) that has the landscape properties,
    # or even the first section if the document was restructured.

    # Find a landscape section with the task-required properties
    landscape_section = None
    for section in sections:
        sectPr = section._sectPr
        pgSz = sectPr.find(f'{{{W_NS}}}pgSz')
        if pgSz is not None:
            orient = pgSz.get(f'{{{W_NS}}}orient')
            if orient == 'landscape':
                landscape_section = section
                break

    # Also check: if document has >1 section, the new section might be landscape
    if landscape_section is None and len(sections) > 1:
        # Check sections beyond the first
        for section in sections[1:]:
            sectPr = section._sectPr
            pgSz = sectPr.find(f'{{{W_NS}}}pgSz')
            if pgSz is not None:
                orient = pgSz.get(f'{{{W_NS}}}orient')
                if orient == 'landscape':
                    landscape_section = section
                    break

    # Component 1: A section with landscape orientation exists (0.25 points)
    # This FAILS on initial (only portrait) and PASSES on golden (has landscape section)
    try:
        if landscape_section is not None:
            print(f"PASS: Component 1 — Landscape section found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No landscape section found in {len(sections)} section(s)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if landscape_section is None:
        # No landscape section means no further checks can pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    sectPr = landscape_section._sectPr

    # Component 2: Page size is A4 in landscape (w=16838, h=11906 twips) (0.20 points)
    # A4 portrait is 11906 x 16838; landscape swaps to 16838 x 11906
    # Allow small tolerance of +/-10 twips for rounding
    try:
        pgSz = sectPr.find(f'{{{W_NS}}}pgSz')
        if pgSz is not None:
            w_val = int(pgSz.get(f'{{{W_NS}}}w', '0'))
            h_val = int(pgSz.get(f'{{{W_NS}}}h', '0'))
            # A4 landscape: width ~16838 twips, height ~11906 twips
            w_ok = abs(w_val - 16838) <= 20
            h_ok = abs(h_val - 11906) <= 20
            if w_ok and h_ok:
                print(f"PASS: Component 2 — A4 landscape size (w={w_val}, h={h_val}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Expected A4 landscape (16838x11906), found ({w_val}x{h_val})")
        else:
            print(f"FAIL: Component 2 — No pgSz element found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All margins = 1.5cm = ~850 twips (0.25 points)
    # 1.5cm = 850.39 twips, allow tolerance of +/-15 twips
    try:
        pgMar = sectPr.find(f'{{{W_NS}}}pgMar')
        if pgMar is not None:
            margins = {}
            for side in ['top', 'right', 'bottom', 'left']:
                margins[side] = int(pgMar.get(f'{{{W_NS}}}{side}', '0'))

            EXPECTED_MARGIN = 850
            TOLERANCE = 20
            bad_margins = [s for s, v in margins.items() if abs(v - EXPECTED_MARGIN) > TOLERANCE]
            for side in bad_margins:
                print(f"  DETAIL: Margin {side}={margins[side]} twips (expected ~{EXPECTED_MARGIN})")

            if len(bad_margins) == 0:
                print(f"PASS: Component 3 — All margins ~1.5cm ({margins}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Margins not all 1.5cm: {margins}")
        else:
            print(f"FAIL: Component 3 — No pgMar element found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 0.5pt gray (#808080) border on all four sides (0.30 points)
    # In OOXML, 0.5pt = sz="4" (eighths of a point), color="808080", val="single"
    try:
        pgBorders = sectPr.find(f'{{{W_NS}}}pgBorders')
        if pgBorders is not None:
            border_sides = ['top', 'left', 'bottom', 'right']
            borders_ok = 0
            for side in border_sides:
                border_el = pgBorders.find(f'{{{W_NS}}}{side}')
                if border_el is not None:
                    val = border_el.get(f'{{{W_NS}}}val', '')
                    sz = border_el.get(f'{{{W_NS}}}sz', '0')
                    color = border_el.get(f'{{{W_NS}}}color', '').lower()

                    # val should be "single", sz should be "4" (0.5pt), color should be "808080"
                    val_ok = val == 'single'
                    sz_ok = sz == '4'
                    color_ok = color == '808080'

                    if val_ok and sz_ok and color_ok:
                        borders_ok += 1
                    else:
                        print(f"  DETAIL: Border {side}: val={val} sz={sz} color={color}")
                else:
                    print(f"  DETAIL: Border {side} element missing")

            if borders_ok == 4:
                print(f"PASS: Component 4 — All 4 borders: single, 0.5pt, #808080 (0.30 pts)")
                total_score += 0.30
            elif borders_ok > 0:
                partial = round(0.30 * borders_ok / 4, 2)
                print(f"PARTIAL: Component 4 — {borders_ok}/4 borders correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No correct borders found")
        else:
            print(f"FAIL: Component 4 — No pgBorders element in landscape section")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
