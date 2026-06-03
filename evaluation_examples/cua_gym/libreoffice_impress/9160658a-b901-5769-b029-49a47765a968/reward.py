"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a throwaway placeholder sitting on slide 2, but I still want to keep it in the file for reference. What’s the quickest way in LibreOffice Impress to hide that exact slide—slide 2—so it never appears during the slideshow?
Generated: 2025-09-10 19:27:33
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
import lxml.etree as ET
from pptx import Presentation


def is_slide_hidden(pptx_path: str, slide_index: int = 2) -> bool:
    """Return True if the given (1-based) slide index is hidden in the PPTX file."""
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            # 1. Check the slide XML itself for a <p:sld show="0"> attribute
            slide_xml_path = f"ppt/slides/slide{slide_index}.xml"
            if slide_xml_path not in z.namelist():
                print(f"✗ {slide_xml_path} not found in archive")
                return False
            xml_bytes = z.read(slide_xml_path)
            root = ET.fromstring(xml_bytes)
            # In Office XML, the attribute can literally be show="0"
            show_attr = root.attrib.get('show')
            print(f"  Slide XML 'show' attribute: {show_attr}")
            if show_attr is not None and show_attr in ("0", "false", "False"):
                print("✓ Slide XML indicates it is hidden")
                return True

            # 2. Check the sldId entry inside ppt/presentation.xml for hide/show flags
            pres_xml = ET.fromstring(z.read('ppt/presentation.xml'))
            ns = {
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
                'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'
            }
            sld_ids = pres_xml.findall('.//p:sldIdLst/p:sldId', ns)
            if len(sld_ids) >= slide_index:
                sld_id = sld_ids[slide_index - 1]
                show_attr2 = sld_id.attrib.get('{http://schemas.microsoft.com/office/powerpoint/2010/main}show')
                hide_attr = sld_id.attrib.get('{http://schemas.microsoft.com/office/powerpoint/2010/main}hide')
                print(f"  sldId attributes -> p14:show={show_attr2}, p14:hide={hide_attr}")
                # Either p14:show="0" OR p14:hide="1" means hidden
                if (show_attr2 is not None and show_attr2 in ("0", "false", "False")) or (
                    hide_attr is not None and hide_attr in ("1", "true", "True")):
                    print("✓ sldId entry indicates slide is hidden")
                    return True

            print("✗ No hidden indicators found for this slide")
            return False
    except Exception as e:
        print(f"✗ Error while checking hidden status: {e}")
        return False


def verify_task(pptx_path: str) -> float:
    """Verify that slide 2 exists and is hidden; return a progressive score between 0-1."""
    print("Verifying hidden-slide task…")
    score = 0.0

    # Preliminary: file must exist and be a PPTX we can open
    if not os.path.exists(pptx_path):
        print(f"✗ File not found: {pptx_path}")
        return 0.0

    try:
        prs = Presentation(pptx_path)
        slide_count = len(prs.slides)
        print(f"✓ Presentation loaded successfully ‑ {slide_count} slides present")
    except Exception as e:
        print(f"✗ Unable to load PPTX: {e}")
        return 0.0

    # Requirement 1 – Slide 2 still exists (0.3 pts)
    if slide_count >= 2:
        score += 0.3
        print("✓ Slide 2 exists (0.3 points)")
    else:
        print("✗ Slide 2 is missing (no points)")

    # Requirement 2 – Slide 2 is hidden (0.7 pts)
    if is_slide_hidden(pptx_path, slide_index=2):
        score += 0.7
        print("✓ Slide 2 is hidden (0.7 points)")
    else:
        print("✗ Slide 2 is NOT hidden (0 points)")

    final_score = min(score, 1.0)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path provided by the task context
    FILE_PATH = "/home/user/ive_got_a_throwaway_placeholder_sitting_on_slide_2_but_i_still_want_to_keep_it_in_the_file_for_refer_golden.pptx"
    reward_value = verify_task(FILE_PATH)
    print(f"REWARD: {reward_value}")

