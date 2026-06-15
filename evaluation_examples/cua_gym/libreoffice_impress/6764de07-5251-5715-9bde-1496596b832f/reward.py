"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 78 has a solid background that’s messing with the look of my graphics. In LibreOffice Impress, how can I set that slide’s background fill to “No Fill” while leaving every object already on the slide exactly as it is?
Generated: 2025-09-10 15:42:29
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from pptx import Presentation
from lxml import etree

def verify_slide_78_no_fill(file_path: str) -> float:
    """Verify that slide 78 in the given PPTX has its background
    fill set to *No Fill* (a:noFill) and award a progressive score.

    Scoring rubric (max 1.0):
        0.2 – Presentation contains at least 78 slides (basic structural check)
        0.8 – Slide 78 <p:bgPr> contains <a:noFill> **and** does NOT contain
              <a:solidFill> (i.e., truly *No Fill*)
    """

    print(f"Verifying presentation: {file_path}\n")
    total_score = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # Requirement 1: File must be a valid PPTX with ≥ 78 slides
    # ------------------------------------------------------------------
    try:
        prs = Presentation(file_path)
        slide_count = len(prs.slides)
        print(f"Slide count detected: {slide_count}")

        if slide_count >= 78:
            print("✓ Presentation contains at least 78 slides (0.2 points)")
            total_score += 0.2
        else:
            print("✗ Presentation has fewer than 78 slides (0 points)")
    except Exception as e:
        print(f"✗ Error loading presentation: {e}")
        return 0.0  # Can't proceed if file is unreadable

    # ------------------------------------------------------------------
    # Requirement 2: Slide 78 background must be set to *No Fill*
    # ------------------------------------------------------------------
    try:
        slide_xml_path = "ppt/slides/slide78.xml"  # 1-based index
        with zipfile.ZipFile(file_path, "r") as z:
            if slide_xml_path not in z.namelist():
                print(f"✗ Slide XML not found: {slide_xml_path}")
                return total_score  # give partial if earlier check passed

            slide_xml = z.read(slide_xml_path)

        root = etree.fromstring(slide_xml)
        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        }

        bgPr = root.find(".//p:bg/p:bgPr", namespaces=ns)
        if bgPr is None:
            print("✗ <p:bgPr> element not found on slide 78 (0 points)")
        else:
            has_no_fill = bgPr.find("a:noFill", namespaces=ns) is not None
            has_solid_fill = bgPr.find("a:solidFill", namespaces=ns) is not None
            print(
                f"Background properties → noFill={has_no_fill}, solidFill={has_solid_fill}"
            )

            if has_no_fill and not has_solid_fill:
                print("✓ Slide 78 background set to 'No Fill' (0.8 points)")
                total_score += 0.8
            else:
                print("✗ Slide 78 background is not correctly set to 'No Fill' (0 points)")

    except Exception as e:
        print(f"✗ Error verifying slide background: {e}")

    # ------------------------------------------------------------------
    final_score = min(total_score, max_score)  # safety cap
    print(f"\nTotal score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------
# Execute verification
# ------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/slide_78_has_a_solid_background_thats_messing_with_the_look_of_my_graphics_in_libreoffice_impress_ho_golden.pptx"
    verify_slide_78_no_fill(FILE_PATH)

