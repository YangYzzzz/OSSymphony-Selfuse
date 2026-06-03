"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 183 of my LibreOffice Impress presentation, Picture 1 still shows an outline. How do I set its Line style to "None" so the image has absolutely no border?
Generated: 2025-09-10 17:51:18
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import zipfile
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
# Reward Script : Verify that on slide 183 the shape named "Picture 1" has its
#                 line style set to "None" (i.e., absolutely no border).
# -----------------------------------------------------------------------------
# Scoring rules
# 1.0 – Picture found AND border explicitly removed (a:noFill or no <a:ln>)
# 0.6 – Picture found, border width "0" (invisible but not explicitly none)
# 0.0 – Picture missing OR still has a visible border
# -----------------------------------------------------------------------------

def _check_picture_border_style(pic_elem, ns):
    """Classify border style for a <p:pic> element.

    Returns one of: 'none', 'width_zero', 'present'"""
    ln = pic_elem.find('.//p:spPr/a:ln', ns)
    if ln is None:
        # No line element at all ⇒ no border
        return 'none'

    # Explicit no-fill child ⇒ no border
    if ln.find('a:noFill', ns) is not None:
        return 'none'

    # Width attribute equal to 0 ⇒ border is effectively invisible
    w_attr = ln.get('w')
    if w_attr is not None:
        try:
            if int(w_attr) == 0:
                return 'width_zero'
        except ValueError:
            pass  # Non-integer width – treat as present

    # Anything else ⇒ border present
    return 'present'


def verify_impress_picture_border(file_path,
                                  slide_number=183,
                                  picture_name='Picture 1'):
    """Main verification function – returns a progressive reward (float)."""

    # Namespace map for PPTX drawing/presentation XML
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    # ------------------------------------------------------------------
    # 1. Preliminary checks – file & slide must be present (no points)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print(f"✗ Presentation file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    slide_xml_path = f"ppt/slides/slide{slide_number}.xml"

    try:
        with zipfile.ZipFile(file_path) as z:
            if slide_xml_path not in z.namelist():
                print(f"✗ Slide XML not found: {slide_xml_path}")
                print("REWARD: 0.0")
                return 0.0
            slide_xml = z.read(slide_xml_path)
    except Exception as e:
        print(f"✗ Error reading PPTX file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Parse slide XML & locate the requested picture
    # ------------------------------------------------------------------
    try:
        root = ET.fromstring(slide_xml)
    except Exception as e:
        print(f"✗ Error parsing slide XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    pic_elems = root.findall('.//p:pic', ns)
    target_pic = None
    for pic in pic_elems:
        cNvPr = pic.find('.//p:cNvPr', ns)
        if cNvPr is not None and cNvPr.get('name') == picture_name:
            target_pic = pic
            break

    if target_pic is None:
        print(f"✗ Picture '{picture_name}' not found on slide {slide_number}")
        print("REWARD: 0.0")
        return 0.0

    print(f"✓ Picture '{picture_name}' found on slide {slide_number}")

    # ------------------------------------------------------------------
    # 3. Evaluate border style and assign score
    # ------------------------------------------------------------------
    border_status = _check_picture_border_style(target_pic, ns)
    if border_status == 'none':
        print("✓ Border style is set to 'None' (no outline)")
        score = 1.0
    elif border_status == 'width_zero':
        print("⚠ Border width is 0 (invisible) – not explicitly set to 'None'")
        score = 0.6  # Partial credit
    else:
        print("✗ Picture still has a visible border (outline present)")
        score = 0.0

    # ------------------------------------------------------------------
    # 4. Finalise score
    # ------------------------------------------------------------------
    print(f"REWARD: {score}")
    return score


# -------------------
# Execute verification
# -------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/on_slide_183_of_my_libreoffice_impress_presentation_picture_1_still_shows_an_outline_how_do_i_set_it_golden.pptx"
    verify_impress_picture_border(FILE_PATH)

