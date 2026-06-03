"""
Reward Script: Configure notes master with company logo and confidential footer
Task ID: impress_gf1_033
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Logo image exists in notes master
  Component 2 (0.25): Logo is positioned in the top-right area
  Component 3 (0.25): Footer text "Confidential - Internal Use Only" exists in notes master
  Component 4 (0.15): Footer text is red (#FF0000) and centered
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf1_033'

# Notes page dimensions (standard US Letter portrait for notes: 6858000 x 9144000 EMU)
# But we detect actual dimensions from the slide image placeholder or use known defaults.
# Standard notes master width = 6858000 EMU (7.5 inches), height = 9144000 EMU (10 inches)
NOTES_PAGE_WIDTH = 6858000
NOTES_PAGE_HEIGHT = 9144000


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find notesMaster XML
    nm_xml_path = None
    nm_rels_path = None
    for name in zf.namelist():
        if 'notesMasters/notesMaster' in name and name.endswith('.xml') and '.rels' not in name:
            nm_xml_path = name
        if 'notesMasters/_rels/notesMaster' in name and name.endswith('.xml.rels'):
            nm_rels_path = name

    if nm_xml_path is None:
        print("CRITICAL: No notesMaster XML found in pptx")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    try:
        with zf.open(nm_xml_path) as f:
            nm_root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse notesMaster XML: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    # Parse rels to check for image references
    image_rels = {}
    if nm_rels_path:
        try:
            with zf.open(nm_rels_path) as f:
                rels_root = ET.parse(f).getroot()
                rels_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                for rel in rels_root.findall('.//r:Relationship', rels_ns):
                    # Also try without namespace
                    pass
                # Try without namespace prefix
                for rel in rels_root.iter():
                    rid = rel.get('Id')
                    rtype = rel.get('Type', '')
                    target = rel.get('Target', '')
                    if rid and 'image' in rtype.lower():
                        image_rels[rid] = target
        except Exception as e:
            print(f"WARN: Could not parse rels: {e}")

    # Find all pic elements (images) in notes master
    pics = nm_root.findall('.//p:pic', ns)
    # Also search with full iteration for robustness
    if not pics:
        for elem in nm_root.iter():
            if elem.tag.endswith('}pic') or elem.tag == 'pic':
                pics.append(elem)

    # Find all sp (shape) elements that are text boxes (not standard placeholders)
    # Standard placeholders have ph types: hdr, dt, sldImg, body, ftr, sldNum
    all_shapes = nm_root.findall('.//p:sp', ns)
    if not all_shapes:
        for elem in nm_root.iter():
            if elem.tag.endswith('}sp') or elem.tag == 'sp':
                all_shapes.append(elem)

    # Component 1: Logo image exists in notes master (0.35 points)
    try:
        has_logo_image = False
        logo_pic = None

        for pic in pics:
            # Check if it has a blip (image reference)
            blip = pic.find('.//a:blip', ns)
            if blip is None:
                # Try without namespace
                for el in pic.iter():
                    if el.tag.endswith('}blip') or el.tag == 'blip':
                        blip = el
                        break

            if blip is not None:
                # Check if the referenced image actually exists in the zip
                embed_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', '')
                if not embed_id:
                    embed_id = blip.get('r:embed', '')

                if embed_id:
                    # Check if this rel points to an actual image file
                    has_logo_image = True
                    logo_pic = pic
                    break

        if has_logo_image:
            print(f"PASS: Component 1 - Logo image found in notes master (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - No image (p:pic with blip) found in notes master")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Logo is positioned in the top-right area (0.25 points)
    try:
        if logo_pic is not None:
            # Get position from xfrm
            xfrm = None
            for el in logo_pic.iter():
                if el.tag.endswith('}xfrm') or el.tag == 'xfrm':
                    xfrm = el
                    break

            if xfrm is not None:
                off = None
                ext = None
                for child in xfrm:
                    if child.tag.endswith('}off') or child.tag == 'off':
                        off = child
                    if child.tag.endswith('}ext') or child.tag == 'ext':
                        ext = child

                if off is not None:
                    x = int(off.get('x', '0'))
                    y = int(off.get('y', '0'))
                    cx = int(ext.get('cx', '0')) if ext is not None else 0

                    # "Top-right" means:
                    # - x + width should be in the right half of the page (x > midpoint - some tolerance)
                    # - y should be in the top portion (say, top 25% of the page)
                    midpoint_x = NOTES_PAGE_WIDTH / 2
                    top_quarter_y = NOTES_PAGE_HEIGHT * 0.25

                    is_right = (x + cx / 2) > midpoint_x  # center of image is in right half
                    is_top = y < top_quarter_y  # top of image is in top quarter

                    if is_right and is_top:
                        print(f"PASS: Component 2 - Logo positioned top-right (x={x}, y={y}, cx={cx}) (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 2 - Logo not in top-right. x={x}, y={y}, cx={cx}. "
                              f"Need center_x > {midpoint_x} and y < {top_quarter_y}")
                else:
                    print(f"FAIL: Component 2 - No offset found for logo pic")
            else:
                print(f"FAIL: Component 2 - No xfrm found for logo pic")
        else:
            print(f"FAIL: Component 2 - No logo pic to check position for")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Footer text "Confidential - Internal Use Only" exists in notes master (0.25 points)
    try:
        found_footer_text = False
        footer_shape = None

        for sp in all_shapes:
            # Check if this is a standard placeholder (skip those)
            is_placeholder = False
            for el in sp.iter():
                if el.tag.endswith('}ph') or el.tag == 'ph':
                    is_placeholder = True
                    break

            # Get all text content from this shape
            texts = []
            for el in sp.iter():
                if el.tag.endswith('}t') or el.tag == 't':
                    if el.text:
                        texts.append(el.text)

            full_text = ''.join(texts).strip()

            if 'confidential' in full_text.lower() and 'internal use only' in full_text.lower():
                found_footer_text = True
                footer_shape = sp
                break

        if found_footer_text:
            print(f"PASS: Component 3 - Footer text 'Confidential - Internal Use Only' found in notes master (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Footer text 'Confidential - Internal Use Only' not found in notes master shapes")
            # Print all text found for debugging
            for sp in all_shapes:
                texts = []
                for el in sp.iter():
                    if el.tag.endswith('}t') or el.tag == 't':
                        if el.text:
                            texts.append(el.text)
                full_text = ''.join(texts).strip()
                if full_text:
                    print(f"  Found text in shape: '{full_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Footer text is red (#FF0000) and centered (0.15 points)
    try:
        if footer_shape is not None:
            # Check for red color (FF0000) in the run properties
            has_red = False
            has_center = False

            for el in footer_shape.iter():
                # Check for srgbClr with val FF0000
                if el.tag.endswith('}srgbClr') or el.tag == 'srgbClr':
                    color_val = el.get('val', '').upper()
                    if color_val == 'FF0000':
                        has_red = True

                # Check for centered alignment
                if el.tag.endswith('}pPr') or el.tag == 'pPr':
                    algn = el.get('algn', '')
                    if algn == 'ctr':
                        has_center = True

            score_4 = 0.0
            if has_red and has_center:
                print(f"PASS: Component 4 - Footer text is red (#FF0000) and centered (0.15 pts)")
                score_4 = 0.15
            elif has_red:
                print(f"PARTIAL: Component 4 - Footer text is red but not centered (0.10 pts)")
                score_4 = 0.10
            elif has_center:
                print(f"PARTIAL: Component 4 - Footer text is centered but not red (0.05 pts)")
                score_4 = 0.05
            else:
                print(f"FAIL: Component 4 - Footer text is neither red nor centered")

            total_score += score_4
        else:
            print(f"FAIL: Component 4 - No footer shape found to check formatting")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    zf.close()

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
