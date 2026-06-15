"""
FINAL REWARD SCRIPT - SUCCESS
Task: Is there a quick way to give only slide 127 a 'Checkerboard' transition set to Medium speed without affecting any other slides in my LibreOffice Impress deck?
Generated: 2025-09-10 23:07:58
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
import re
from lxml import etree

"""
Reward Verification Script
--------------------------
Checks that ONLY slide 127 of the provided PPTX file has:
  • A transition element
  • Transition type = Checkerboard
  • Transition speed = Medium
and that NO other slide in the deck contains a transition element.
Progressive scoring (weights sum to 1.0):
  • Transition element present on slide 127        → 0.4
  • Transition type is Checkerboard                → 0.2
  • Transition speed is Medium                     → 0.2
  • No other slide contains a transition element   → 0.2
Slide existence is a prerequisite and earns no points.
Returns a float between 0.0 and 1.0, printed as "REWARD: X.X".
"""

FILE_PATH = "/home/user/is_there_a_quick_way_to_give_only_slide_127_a_checkerboard_transition_set_to_medium_speed_without_af_golden.pptx"

# XML namespaces used inside PPTX slide files
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def load_slides(zip_obj):
    """Return a dict {slide_number: slide_xml_root}."""
    slide_files = [
        f for f in zip_obj.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml")
    ]
    num_re = re.compile(r"slide(\d+)\.xml")
    slides = {}
    for fname in slide_files:
        m = num_re.search(fname)
        if not m:
            continue
        num = int(m.group(1))
        slides[num] = etree.fromstring(zip_obj.read(fname))
    return slides


def verify_slide_127_transition(slides):
    """Return progressive score based on transition checks."""
    score = 0.0
    max_score = 1.0

    WEIGHTS = {
        "transition_exists": 0.4,
        "checker_type": 0.2,
        "medium_speed": 0.2,
        "other_slides_clean": 0.2,
    }

    # Ensure slide 127 exists (prerequisite, 0 pts)
    if 127 not in slides:
        print("✗ Slide 127 does not exist in the presentation")
        return 0.0
    print("✓ Slide 127 found")

    slide_127_root = slides[127]

    # --- Check transition on slide 127 ---
    transition_el = slide_127_root.find(".//p:transition", namespaces=NS)
    if transition_el is None:
        print("✗ No transition element found on slide 127")
    else:
        print("✓ Transition element found on slide 127")
        score += WEIGHTS["transition_exists"]

        # Transition type ➔ Checkerboard?
        child = transition_el.find("./*", namespaces=NS)
        if child is not None and etree.QName(child.tag).localname.lower() == "checker":
            print("✓ Transition type is Checkerboard")
            score += WEIGHTS["checker_type"]
        else:
            print("✗ Transition type is not Checkerboard")

        # Transition speed ➔ Medium?
        speed = transition_el.get("spd")
        if speed and speed.lower() == "med":
            print("✓ Transition speed is Medium")
            score += WEIGHTS["medium_speed"]
        else:
            print(f"✗ Transition speed is not Medium (found: {speed})")

    # --- Ensure no other slide has transitions ---
    other_with_trans = [
        num
        for num, root in slides.items()
        if num != 127 and root.find(".//p:transition", namespaces=NS) is not None
    ]
    if other_with_trans:
        print(f"✗ Transitions found on other slides: {other_with_trans}")
    else:
        print("✓ No transitions found on other slides")
        score += WEIGHTS["other_slides_clean"]

    final_score = min(score, max_score)
    print(f"Total score breakdown: {final_score}/{max_score}")
    return final_score


def verify_task(file_path):
    if not os.path.exists(file_path):
        print(f"✗ File does not exist: {file_path}")
        return 0.0
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            slides = load_slides(z)
            print(f"Loaded {len(slides)} slides from presentation")
            return verify_slide_127_transition(slides)
    except Exception as e:
        print(f"✗ Error processing presentation: {e}")
        return 0.0


if __name__ == "__main__":
    reward = verify_task(FILE_PATH)
    print(f"REWARD: {reward}")
