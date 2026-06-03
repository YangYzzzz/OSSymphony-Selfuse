"""
Reward Script: Add a 2pt solid dark gray (#424242) border with 3pt shadow to the image on page 1.
Task ID: writer_obj_033
Domain: libreoffice_writer
Scoring:
  Component 1: Image has a border (a:ln element present in pic:spPr)          — 0.3 pts
  Component 2: Border color is solid dark gray (#424242)                       — 0.3 pts
  Component 3: Border line width is approximately 2pt (25400 EMU ±12700)       — 0.2 pts
  Component 4: Image has an outer shadow effect (a:outerShdw in a:effectLst)   — 0.2 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'photo_album'
FILE_PATH = f'{WORKDIR}/Desktop/{TASK_ID}.docx'

# Namespace constants
NS_W    = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_A    = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_PIC  = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
NS_WP   = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'


def get_first_page_image_spPr(doc):
    """
    Find the pic:spPr element of the first image on page 1 (before any page break).
    Returns the spPr lxml element or None.
    """
    body = doc.element.body
    # Iterate paragraphs in body until we hit a page break
    for para in body.findall(f'{{{NS_W}}}p'):
        # Check if this paragraph contains a page break
        for run in para.findall(f'.//{{{NS_W}}}r'):
            for br in run.findall(f'{{{NS_W}}}br'):
                br_type = br.get(f'{{{NS_W}}}type')
                if br_type == 'page':
                    # We've reached the end of page 1 without finding an image
                    return None
        # Check for drawing elements in this paragraph
        drawings = para.findall(f'.//{{{NS_W}}}drawing')
        for drawing in drawings:
            # Look for pic:spPr inside the drawing
            spPr_list = drawing.findall(f'.//{{{NS_PIC}}}spPr')
            if spPr_list:
                return spPr_list[0]
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that the first image on page 1 has:
      1. A border (a:ln element)
      2. Border color #424242
      3. Border width ~2pt (25400 EMU ±12700, i.e. 1pt to 3pt)
      4. An outer shadow effect
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the first image's spPr on page 1
    try:
        spPr = get_first_page_image_spPr(doc)
        if spPr is None:
            print("CRITICAL: Could not find any image on page 1")
            print("REWARD: 0.0")
            return 0.0
        print(f"INFO: Found image spPr element on page 1")
    except Exception as e:
        print(f"CRITICAL: Error locating image on page 1: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Border element (a:ln) exists in spPr (0.3 points)
    try:
        ln_elements = spPr.findall(f'{{{NS_A}}}ln')
        if ln_elements:
            print(f"PASS: Component 1 — Border element <a:ln> found in pic:spPr (0.3 pts)")
            total_score += 0.3
            ln_el = ln_elements[0]
        else:
            print(f"FAIL: Component 1 — No <a:ln> border element found in pic:spPr")
            ln_el = None
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        ln_el = None

    # Component 2: Border color is solid #424242 (0.3 points)
    try:
        if ln_el is not None:
            # Check for a:solidFill > a:srgbClr with val="424242"
            solid_fills = ln_el.findall(f'.//{{{NS_A}}}solidFill')
            color_found = False
            actual_color = None
            for sf in solid_fills:
                srgb_list = sf.findall(f'{{{NS_A}}}srgbClr')
                for srgb in srgb_list:
                    color_val = srgb.get('val', '').lower()
                    actual_color = color_val
                    if color_val == '424242':
                        color_found = True
                        break
                if color_found:
                    break
            if color_found:
                print(f"PASS: Component 2 — Border color is #424242 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Expected border color #424242, found: {actual_color}")
        else:
            print(f"FAIL: Component 2 — Skipped (no border element found)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Border line width is approximately 2pt (25400 EMU ±12700, i.e. 1-3pt) (0.2 points)
    try:
        if ln_el is not None:
            w_attr = ln_el.get('w')
            if w_attr is not None:
                width_emu = int(w_attr)
                # 1pt = 12700 EMU; 2pt = 25400 EMU; allow ±12700 (1pt tolerance)
                # Accept range: 12700 (1pt) to 38100 (3pt)
                width_pt = width_emu / 12700.0
                if 12700 <= width_emu <= 38100:
                    print(f"PASS: Component 3 — Border width is {width_pt:.2f}pt ({width_emu} EMU), approximately 2pt (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Border width {width_pt:.2f}pt ({width_emu} EMU) is outside 1-3pt range")
            else:
                # No 'w' attribute means default width (1pt / 12700 EMU) — close enough for tolerance
                print(f"FAIL: Component 3 — Border element has no width attribute (w), expected ~25400 EMU")
        else:
            print(f"FAIL: Component 3 — Skipped (no border element found)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Outer shadow effect exists (a:effectLst with a:outerShdw) (0.2 points)
    try:
        effect_lists = spPr.findall(f'{{{NS_A}}}effectLst')
        shadow_found = False
        for el in effect_lists:
            outer_shdw = el.findall(f'{{{NS_A}}}outerShdw')
            if outer_shdw:
                # Optionally verify shadow distance is approximately 3pt (38100 EMU)
                shdw_el = outer_shdw[0]
                dist_attr = shdw_el.get('dist')
                if dist_attr is not None:
                    dist_emu = int(dist_attr)
                    dist_pt = dist_emu / 12700.0
                    # Accept shadow offset in range 1pt-6pt (12700-76200 EMU)
                    if 12700 <= dist_emu <= 76200:
                        print(f"PASS: Component 4 — Outer shadow effect found with dist={dist_pt:.2f}pt (~3pt expected) (0.2 pts)")
                        shadow_found = True
                    else:
                        print(f"FAIL: Component 4 — Shadow found but dist={dist_pt:.2f}pt is outside 1-6pt range")
                else:
                    # outerShdw exists but no dist attribute — still counts as shadow present
                    print(f"PASS: Component 4 — Outer shadow effect found (no dist attr) (0.2 pts)")
                    shadow_found = True
                break

        if shadow_found:
            total_score += 0.2
        elif not effect_lists:
            print(f"FAIL: Component 4 — No <a:effectLst> element found in pic:spPr")
        else:
            print(f"FAIL: Component 4 — <a:effectLst> exists but no <a:outerShdw> inside")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
