"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 175 is still tied to a master page called “Default”. I need that master page renamed to exactly “Corporate Blue” so everyone knows it’s the branded layout. How do I do this in LibreOffice Impress?
Generated: 2025-09-10 18:32:09
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pptx import Presentation

def verify_master_renamed(file_path: str) -> float:
    """Verify that slide 175 is tied to a layout whose name has been
    changed from the default to exactly 'Corporate Blue'. Progressive
    scoring is used so partial completion receives partial credit.
    Returns a float between 0.0 and 1.0.
    """

    print(f"Verifying master rename in: {file_path}")
    total_score = 0.0
    MAX_SCORE = 1.0

    # --- Preliminary checks (no points awarded) ---------------------
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        return 0.0  # hard-failure

    try:
        prs = Presentation(file_path)  # prerequisite load (no points)
    except Exception as e:
        print(f"✗ Unable to load PPTX: {e}")
        return 0.0

    slide_count = len(prs.slides)
    print(f"Slide count in presentation: {slide_count}")

    # --- Requirement 1: Presentation must contain at least 175 slides
    if slide_count < 175:
        print("✗ Presentation contains fewer than 175 slides – cannot assess slide 175")
        return 0.0  # cannot continue meaningful checks

    # ----------------------------------------------------------------
    # Locate the slideLayout used by slide 175 via the relationships file
    target_slide_index = 174  # zero-based index for slide 175
    rels_path = f"ppt/slides/_rels/slide{target_slide_index + 1}.xml.rels"

    try:
        with zipfile.ZipFile(file_path, "r") as z:
            if rels_path not in z.namelist():
                print("✗ Relationship file for slide 175 is missing")
                return 0.0

            rels_xml = z.read(rels_path)
            rels_root = ET.fromstring(rels_xml)
            ns = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
            layout_target = None
            for rel in rels_root.findall(ns):
                if rel.get("Type") == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout":
                    layout_target = rel.get("Target")
                    break

            if not layout_target:
                print("✗ Slide 175 does not reference a slideLayout – invalid state")
                return 0.0

            # Resolve the target path to an absolute path inside the zip
            if layout_target.startswith("../"):
                layout_path = "ppt/" + layout_target.replace("../", "")
            else:
                layout_path = os.path.join(os.path.dirname(rels_path), layout_target)

            if layout_path not in z.namelist():
                print("✗ Referenced slideLayout file not found in archive")
                return 0.0

            layout_xml = z.read(layout_path)
            layout_root = ET.fromstring(layout_xml)
            layout_name = layout_root.get("name")  # attribute holds the human name

            print(f"Slide 175 uses layout: '{layout_name}' (file: {layout_path})")

            # --- Scoring ----------------------------------------------------
            # 1) Layout renamed exactly to 'Corporate Blue' (0.5)
            if layout_name and layout_name.strip() == "Corporate Blue":
                total_score += 0.5
                print("✓ Layout name exactly 'Corporate Blue' (+0.5)")
            else:
                print("✗ Layout name is not exactly 'Corporate Blue' (0 points)")

            # 2) Layout name no longer contains the word 'Default' (0.3)
            if layout_name and "Default" not in layout_name:
                total_score += 0.3
                print("✓ Layout name does not contain 'Default' (+0.3)")
            else:
                print("✗ Layout name still contains 'Default' (0 points)")

            # 3) At least one layout anywhere in the presentation is named
            #    exactly 'Corporate Blue' – ensures global rename (0.2)
            has_corporate_blue_layout = False
            layout_files = [f for f in z.namelist() if f.startswith("ppt/slideLayouts/") and f.endswith(".xml")]
            for lf in layout_files:
                xml_bytes = z.read(lf)
                root = ET.fromstring(xml_bytes)
                if root.get("name") and root.get("name").strip() == "Corporate Blue":
                    has_corporate_blue_layout = True
                    break

            if has_corporate_blue_layout:
                total_score += 0.2
                print("✓ Presentation contains a layout named 'Corporate Blue' (+0.2)")
            else:
                print("✗ No layout named 'Corporate Blue' found in the presentation (0 points)")

    except Exception as e:
        print(f"✗ Unexpected error during verification: {e}")
        return 0.0

    final_score = min(total_score, MAX_SCORE)
    print(f"Total score awarded: {final_score}/{MAX_SCORE}")
    return final_score


# ------------------------ RUN VERIFICATION ---------------------------
if __name__ == "__main__":
    presentation_path = "/home/user/slide_175_is_still_tied_to_a_master_page_called_default_i_need_that_master_page_renamed_to_exactly_c_golden.pptx"
    reward_value = verify_master_renamed(presentation_path)
    print(f"REWARD: {reward_value}")
