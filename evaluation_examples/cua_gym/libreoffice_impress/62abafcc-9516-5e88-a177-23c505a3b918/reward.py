"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 9, the title is blending into the background. In LibreOffice Impress, how can I enable a drop shadow for that title and set both the horizontal and vertical offset to exactly 0.2 cm?
Generated: 2025-09-10 13:52:21
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------
# Reward script: Verify that on slide 9 the TITLE has a drop shadow with
#                both horizontal and vertical offsets set to 0.2 cm.
# ---------------------------------------------------------------------
# Conversion note:  1 cm  = 360000 EMUs  ➜ 0.2 cm = 72000 EMUs
EXPECTED_OFFSET_EMU = 72000            # 0.2 cm in EMUs
TOLERANCE           = 1000             # ±1000 EMUs tolerance (~0.003 cm)

# Namespaces used inside PPTX XML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

# ------------------------------------------------------------------
# Helper-functions
# ------------------------------------------------------------------

def get_slide_path(zipf: zipfile.ZipFile, index_1based: int):
    """Return the internal path of the slide in *presentation order*.
       index_1based = 1 ➜ first slide, 9 ➜ ninth slide …
    """
    try:
        pres_root = ET.fromstring(zipf.read('ppt/presentation.xml'))
        rel_root  = ET.fromstring(zipf.read('ppt/_rels/presentation.xml.rels'))

        # Relationships map  rId ➜ target path (e.g. "slides/slide9.xml")
        rel_ns  = {'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
        rel_map = {rel.get('Id'): rel.get('Target')
                   for rel in rel_root.findall('pr:Relationship', rel_ns)}

        slide_ids = pres_root.findall('.//p:sldIdLst/p:sldId', NS)
        if index_1based - 1 >= len(slide_ids):
            return None
        rId = slide_ids[index_1based - 1].get('{%s}id' % NS['r'])
        target = rel_map.get(rId)
        if not target:
            return None
        return 'ppt/' + target.lstrip('/')
    except Exception:
        return None


def find_title_shape(slide_root):
    """Locate the shape that is the title placeholder (title or ctrTitle)."""
    for sp in slide_root.findall('.//p:sp', NS):
        ph = sp.find('.//p:nvPr/p:ph', NS)
        if ph is not None:
            ph_type = ph.get('type')  # None → default title
            if ph_type in (None, 'title', 'ctrTitle'):
                return sp
    return None


def shadow_info(shape):
    """Return (has_shadow: bool, off_x: str|None, off_y: str|None)."""
    spPr  = shape.find('p:spPr', NS)
    if spPr is None:
        return False, None, None
    outer = spPr.find('.//a:outerShdw', NS)
    if outer is None:
        return False, None, None

    # Offsets can be expressed via <a:off x= y=> *or* attributes dx/dy
    off = outer.find('a:off', NS)
    if off is not None:
        return True, off.get('x'), off.get('y')
    return True, outer.get('dx'), outer.get('dy')


def to_int(val):
    try:
        return int(val) if val is not None else None
    except ValueError:
        return None

# ------------------------------------------------------------------
# Main verification routine
# ------------------------------------------------------------------

def verify_task(file_path: str) -> float:
    print(f"Checking presentation file: {file_path}")
    score = 0.0

    # ---------- prerequisite checks ----------
    if not (os.path.isfile(file_path) and file_path.lower().endswith('.pptx')):
        print("✗ File missing or not a .pptx – cannot verify.")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as zf:
            # 1) Slide 9 must exist -------------------------------------------------
            slide_path = get_slide_path(zf, 9)
            if slide_path and slide_path in zf.namelist():
                print(f"✓ Slide 9 found  → {slide_path}  (+0.25)")
                score += 0.25
            else:
                print("✗ Slide 9 not found – stopping verification.")
                return score

            slide_root = ET.fromstring(zf.read(slide_path))

            # 2) Title shape present ----------------------------------------------
            title_shape = find_title_shape(slide_root)
            if title_shape is not None:
                print("✓ Title placeholder detected on slide 9  (+0.25)")
                score += 0.25
            else:
                print("✗ Title placeholder missing – stopping verification.")
                return score

            # 3) Drop shadow enabled ---------------------------------------------
            has_shadow, x_val, y_val = shadow_info(title_shape)
            if has_shadow:
                print("✓ Drop-shadow effect present  (+0.25)")
                score += 0.25
            else:
                print("✗ No drop-shadow found – stopping verification.")
                return score

            # 4) Offsets exactly 0.2 cm in both directions ------------------------
            x_int = to_int(x_val)
            y_int = to_int(y_val)
            if x_int is None or y_int is None:
                print(f"✗ Offset values unreadable (x={x_val}, y={y_val}).")
                return score

            if (abs(x_int - EXPECTED_OFFSET_EMU) <= TOLERANCE and
                abs(y_int - EXPECTED_OFFSET_EMU) <= TOLERANCE):
                print(f"✓ Offsets match 0.2 cm (x={x_int}, y={y_int})  (+0.25)")
                score += 0.25
            else:
                print(f"✗ Offsets incorrect: x={x_int}, y={y_int} – expected {EXPECTED_OFFSET_EMU} EMUs.")

    except zipfile.BadZipFile:
        print("✗ File is not a valid PPTX archive.")
        return 0.0
    except Exception as e:
        print(f"✗ Unexpected error during verification: {e}")
        return 0.0

    final_score = min(score, 1.0)
    print(f"Reward score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------------------------------------------
# Execute verification (automatically when script runs) -------------
# ------------------------------------------------------------------
if __name__ == "__main__":
    FILE = "/home/user/on_slide_9_the_title_is_blending_into_the_background_in_libreoffice_impress_how_can_i_enable_a_drop__golden.pptx"
    verify_task(FILE)
