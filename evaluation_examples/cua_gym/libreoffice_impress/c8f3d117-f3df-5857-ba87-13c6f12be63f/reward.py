"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m polishing a huge slide deck in LibreOffice Impress—slide number 190 is looking a bit static. How can I add the “Checkerboard” transition to that specific slide and keep the speed at the Medium setting?
Generated: 2025-09-10 18:11:04
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree


def verify_checkerboard_transition(file_path: str, slide_number: int = 190) -> float:
    """Reward-script verifier for the LibreOffice Impress task.

    It checks that slide `slide_number` in the given PPTX has:
      1. A transition element present            – 0.4 pts
      2. The transition type set to Checkerboard – 0.3 pts
      3. The transition speed set to Medium      – 0.3 pts

    Returns a progressive score between 0.0 and 1.0 and prints
    detailed diagnostics plus the final line:  "REWARD: X.X".
    """

    print(f"Starting verification for file: {file_path}")

    max_score = 1.0
    total_score = 0.0  # progressive score accumulator

    # ---------------------------------------------------------------------
    # Prerequisite checks (NO POINTS – just failure blocking)
    # ---------------------------------------------------------------------
    if not (os.path.exists(file_path) and file_path.endswith(".pptx")):
        print("✗ File missing or not a .pptx – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    try:
        pptx_zip = zipfile.ZipFile(file_path, "r")
    except Exception as e:
        print(f"✗ Failed to open PPTX: {e}")
        print("REWARD: 0.0")
        return 0.0

    slide_filename = f"ppt/slides/slide{slide_number}.xml"
    if slide_filename not in pptx_zip.namelist():
        print(f"✗ Slide {slide_number} not found in presentation")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------------
    # Parse the selected slide XML
    # ---------------------------------------------------------------------
    try:
        slide_xml = pptx_zip.read(slide_filename)
        root = etree.fromstring(slide_xml)
    except Exception as e:
        print(f"✗ Error parsing slide XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    transition_elem = root.find(".//p:transition", namespaces=ns)

    # ---------------------------------------------------------------------
    # Requirement 1: Transition exists (0.4 pts)
    # ---------------------------------------------------------------------
    if transition_elem is not None:
        print(f"✓ Transition element found on slide {slide_number} (0.4 points)")
        total_score += 0.4
    else:
        print(f"✗ No transition element on slide {slide_number}")
        print(f"REWARD: {total_score}")
        return total_score  # Cannot check further without a transition

    # ---------------------------------------------------------------------
    # Requirement 2: Transition type is Checkerboard (0.3 pts)
    # ---------------------------------------------------------------------
    checker_found = any(
        etree.QName(child.tag).localname.lower() == "checker" for child in transition_elem
    )
    if checker_found:
        print("✓ Checkerboard transition type confirmed (0.3 points)")
        total_score += 0.3
    else:
        print("✗ Transition type is not Checkerboard (0 points)")

    # ---------------------------------------------------------------------
    # Requirement 3: Speed is Medium (0.3 pts)
    # ---------------------------------------------------------------------
    speed_attr = transition_elem.get("spd")  # expected values: slow | med | fast
    print(f"Detected transition speed attribute: {speed_attr}")
    if speed_attr == "med":
        print("✓ Transition speed is set to Medium (0.3 points)")
        total_score += 0.3
    else:
        print("✗ Transition speed is not Medium (0 points)")

    # ---------------------------------------------------------------------
    # Final score output
    # ---------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score breakdown: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -------------------------------------------------------------------------
# Execute verification when this script is run directly
# -------------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = (
        "/home/user/im_polishing_a_huge_slide_deck_in_libreoffice_impressslide_"
        "number_190_is_looking_a_bit_static_how_ca_golden.pptx"
    )
    verify_checkerboard_transition(FILE_PATH)

