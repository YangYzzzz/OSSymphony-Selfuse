"""
Reward Script: Create Fontwork 'SALE' with 3D metallic style, gold color, centered ~12cm wide
Task ID: impress_ndo_059
Domain: libreoffice_impress
Scoring:
  Component 1: Fontwork/WordArt shape with text 'SALE' on slide 1 (0.30)
  Component 2: Gold color #FFD700 applied to text (0.20)
  Component 3: Width approximately 12cm (4320000 EMU +/- 15%) (0.20)
  Component 4: Horizontally centered on slide (0.15)
  Component 5: 3D metallic material properties present (0.15)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_059'


def find_sale_wordart_shape(pptx_path):
    """
    Search slide 1 XML for a shape containing text 'SALE' that appears to be
    a WordArt/Fontwork element (not a regular textbox from initial state).
    Returns the shape XML element or None.
    """
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slides/slide1.xml') as f:
                content = f.read().decode()
    except Exception as e:
        print(f"ERROR: Cannot read slide1.xml: {e}")
        return None, None

    root = ET.fromstring(content)

    # Define namespace map
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    # Iterate all sp elements looking for one containing text 'SALE'
    for sp in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}sp'):
        # Check text content
        texts = []
        for t_elem in sp.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
            if t_elem.text:
                texts.append(t_elem.text)
        full_text = ''.join(texts).strip()

        if 'SALE' not in full_text.upper():
            continue

        # Check if this is a WordArt/Fontwork shape (not a plain textbox)
        # Indicators: name contains 'WordArt', or has prstTxWarp, or has 3D props, or is AUTO_SHAPE type
        nvSpPr = sp.find('{http://schemas.openxmlformats.org/presentationml/2006/main}nvSpPr')
        cNvPr = None
        if nvSpPr is not None:
            cNvPr = nvSpPr.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr')
        shape_name = cNvPr.get('name', '') if cNvPr is not None else ''

        # Accept if name has WordArt, or has prstTxWarp, or has scene3d/sp3d, or is not one of the initial textboxes
        is_wordart = False
        if 'wordart' in shape_name.lower() or 'fontwork' in shape_name.lower():
            is_wordart = True

        # Check for text warp preset
        for warp in sp.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}prstTxWarp'):
            is_wordart = True
            break

        # Check for 3D scene/material
        for scene3d in sp.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}scene3d'):
            is_wordart = True
            break
        for sp3d in sp.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}sp3d'):
            is_wordart = True
            break

        # Also accept if shape is an AUTO_SHAPE (not TEXT_BOX) with SALE text
        spPr = sp.find('{http://schemas.openxmlformats.org/presentationml/2006/main}spPr')
        if spPr is None:
            spPr = sp.find('{http://schemas.openxmlformats.org/drawingml/2006/main}spPr')

        # If shape has 'SALE' text and is not one of the known initial textboxes, accept it
        if full_text == 'SALE':
            is_wordart = True

        if is_wordart:
            return sp, ns

    return None, ns


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    a_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    p_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    sp, ns = find_sale_wordart_shape(file_path)

    # Component 1: Fontwork/WordArt shape with text 'SALE' on slide 1 (0.30 points)
    try:
        if sp is not None:
            # Verify text is exactly 'SALE'
            texts = []
            for t_elem in sp.iter(f'{{{a_ns}}}t'):
                if t_elem.text:
                    texts.append(t_elem.text)
            full_text = ''.join(texts).strip()
            if full_text.upper() == 'SALE':
                print(f"PASS: Component 1 - WordArt/Fontwork shape with text 'SALE' found on slide 1 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - Shape found but text is '{full_text}', expected 'SALE'")
        else:
            print("FAIL: Component 1 - No WordArt/Fontwork shape with text 'SALE' found on slide 1")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if sp is None:
        # No shape found, cannot check further components
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Gold color #FFD700 applied to text (0.20 points)
    try:
        color_found = False
        # Check solidFill in run properties for FFD700
        for rPr in sp.iter(f'{{{a_ns}}}rPr'):
            solidFill = rPr.find(f'{{{a_ns}}}solidFill')
            if solidFill is not None:
                srgbClr = solidFill.find(f'{{{a_ns}}}srgbClr')
                if srgbClr is not None:
                    color_val = srgbClr.get('val', '').upper()
                    if color_val == 'FFD700':
                        color_found = True
                        break
        if color_found:
            print(f"PASS: Component 2 - Gold color #FFD700 applied to text (0.20 pts)")
            total_score += 0.20
        else:
            # Also check if color is close to gold (within a small range)
            print(f"FAIL: Component 2 - Gold color #FFD700 not found on text run")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Width approximately 12cm (4320000 EMU, +/- 15%) (0.20 points)
    try:
        spPr = sp.find(f'{{{p_ns}}}spPr')
        if spPr is None:
            spPr = sp.find(f'{{{a_ns}}}spPr')
        xfrm = spPr.find(f'{{{a_ns}}}xfrm') if spPr is not None else None
        ext = xfrm.find(f'{{{a_ns}}}ext') if xfrm is not None else None

        if ext is not None:
            width_emu = int(ext.get('cx', '0'))
            # 12cm = 4320000 EMU (1 cm = 360000 EMU)
            target_width = 4320000
            tolerance = 0.15  # 15%
            lower = target_width * (1 - tolerance)
            upper = target_width * (1 + tolerance)
            width_cm = width_emu / 360000.0

            if lower <= width_emu <= upper:
                print(f"PASS: Component 3 - Width {width_cm:.1f}cm (~{width_emu} EMU) is within 15% of 12cm (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - Width {width_cm:.1f}cm ({width_emu} EMU) is outside 15% tolerance of 12cm ({lower}-{upper} EMU)")
        else:
            print("FAIL: Component 3 - Could not find shape dimensions")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Horizontally centered on slide (0.15 points)
    try:
        # Slide width is standard 9144000 EMU (25.4cm)
        from pptx import Presentation
        prs = Presentation(file_path)
        slide_width = prs.slide_width  # EMU

        spPr = sp.find(f'{{{p_ns}}}spPr')
        if spPr is None:
            spPr = sp.find(f'{{{a_ns}}}spPr')
        xfrm = spPr.find(f'{{{a_ns}}}xfrm') if spPr is not None else None
        off = xfrm.find(f'{{{a_ns}}}off') if xfrm is not None else None
        ext = xfrm.find(f'{{{a_ns}}}ext') if xfrm is not None else None

        if off is not None and ext is not None:
            shape_left = int(off.get('x', '0'))
            shape_width = int(ext.get('cx', '0'))
            # Center position: shape_left + shape_width/2 should be approximately slide_width/2
            shape_center = shape_left + shape_width / 2
            slide_center = slide_width / 2
            # Allow 10% of slide width tolerance
            tolerance_emu = slide_width * 0.10

            if abs(shape_center - slide_center) <= tolerance_emu:
                print(f"PASS: Component 4 - Shape center ({shape_center:.0f}) is within 10% of slide center ({slide_center:.0f}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Shape center ({shape_center:.0f}) is NOT within 10% of slide center ({slide_center:.0f})")
        else:
            print("FAIL: Component 4 - Could not determine shape position")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: 3D metallic material properties present (0.15 points)
    try:
        has_3d_metallic = False
        # Check for sp3d element with prstMaterial="metal" anywhere in the shape
        for sp3d in sp.iter(f'{{{a_ns}}}sp3d'):
            material = sp3d.get('prstMaterial', '')
            if material == 'metal':
                has_3d_metallic = True
                break

        if has_3d_metallic:
            print(f"PASS: Component 5 - 3D metallic material found (0.15 pts)")
            total_score += 0.15
        else:
            # Check if any 3D properties exist at all (partial)
            has_any_3d = False
            for scene3d in sp.iter(f'{{{a_ns}}}scene3d'):
                has_any_3d = True
                break
            for sp3d in sp.iter(f'{{{a_ns}}}sp3d'):
                has_any_3d = True
                break
            if has_any_3d:
                print(f"FAIL: Component 5 - 3D properties found but material is not 'metal'")
            else:
                print(f"FAIL: Component 5 - No 3D properties found on shape")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
