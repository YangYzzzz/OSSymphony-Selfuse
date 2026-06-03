"""
FINAL REWARD SCRIPT - SUCCESS
Task: In my 120-slide training deck, I want slide 80 to spin in with the “Wheel” transition (make sure it’s the 8-spoke variant) and keep it snappy—0.8 seconds flat. How do I set that up in LibreOffice Impress?
Generated: 2025-09-11 00:05:51
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import re
import zipfile
from lxml import etree


def verify_slide_80_wheel_transition(file_path: str) -> float:
    """Verify that slide 80 in the PPTX has an 8-spoke Wheel transition
    with a duration of ~0.8 s (800 ms).  Progressive scoring is applied.
    Returns a score between 0.0 and 1.0 and prints detailed feedback.
    """

    # Scoring rubric (must sum to 1.0)
    points = {
        "slide_count": 0.20,        # presentation has at least 80 slides
        "transition_exists": 0.20, # <p:transition> present on slide 80
        "wheel_type": 0.20,        # transition type is Wheel
        "spokes": 0.20,            # Wheel has spokes="8"
        "duration": 0.20           # duration attribute ≈ 800 ms
    }

    total_score = 0.0
    max_score = 1.0

    print(f"Verifying presentation: {file_path}")

    # 1. File existence (no points—prerequisite)
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task.")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as pptx_zip:
            # 2. Enumerate slide XML files
            slide_entries = [
                name for name in pptx_zip.namelist()
                if re.match(r"ppt/slides/slide\d+\.xml$", name)
            ]
            slide_nums = [
                (int(re.search(r"slide(\d+)\.xml$", name).group(1)), name)
                for name in slide_entries
            ]
            slide_nums.sort(key=lambda x: x[0])

            slide_count = len(slide_nums)
            print(f"Found {slide_count} slide XML files in deck")

            # Slide count requirement
            if slide_count >= 80:
                total_score += points["slide_count"]
                print(f"✓ Slide count requirement met (+{points['slide_count']})")
            else:
                print("✗ Presentation contains fewer than 80 slides")

            # Locate slide 80
            slide80_path = dict(slide_nums).get(80)
            if not slide80_path:
                print("✗ Slide 80 not found in file – cannot continue verification")
                return total_score

            # Parse slide 80 XML
            slide_xml = etree.fromstring(pptx_zip.read(slide80_path))
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

            # 3. Transition element existence
            transition = slide_xml.find(".//p:transition", ns)
            if transition is not None:
                total_score += points["transition_exists"]
                print(f"✓ <p:transition> element found (+{points['transition_exists']})")
            else:
                print("✗ No transition element on slide 80")
                return total_score  # other checks depend on it

            # 4. Transition type = Wheel
            wheel_elem = transition.find("p:wheel", ns)
            if wheel_elem is not None:
                total_score += points["wheel_type"]
                print(f"✓ Wheel transition detected (+{points['wheel_type']})")
            else:
                print("✗ Transition on slide 80 is not a Wheel type")
                wheel_elem = None  # ensure no spokes points awarded

            # 5. Wheel spokes = 8
            if wheel_elem is not None:
                spokes_val = wheel_elem.get("spokes")
                if spokes_val == "8":
                    total_score += points["spokes"]
                    print(f"✓ Wheel spokes = 8 (+{points['spokes']})")
                else:
                    print(f"✗ Wheel spokes expected '8', found '{spokes_val}'")

            # 6. Duration ≈ 800 ms  (allow ±50 ms tolerance)
            dur_attr = transition.get("dur")  # duration is in milliseconds
            if dur_attr is not None:
                try:
                    dur_ms = int(dur_attr)
                    if 750 <= dur_ms <= 850:
                        total_score += points["duration"]
                        print(
                            f"✓ Duration {dur_ms} ms within expected range (+{points['duration']})"
                        )
                    else:
                        print(f"✗ Duration {dur_ms} ms outside expected 0.8 s range")
                except ValueError:
                    print("✗ Duration attribute is not an integer value – invalid format")
            else:
                print("✗ Duration attribute missing on transition element")

    except Exception as exc:
        print(f"✗ Error processing PPTX file: {exc}")
        return 0.0

    # Cap score at 1.0 and return
    final_score = min(total_score, max_score)
    print(f"Final score: {final_score}")
    return final_score


# --------------------
# Script entry-point
# --------------------
if __name__ == "__main__":
    test_path = (
        "/home/user/"
        "in_my_120_slide_training_deck_i_want_slide_80_to_spin_in_with_the_wheel_"
        "transition_make_sure_its_the_golden.pptx"
    )
    reward = verify_slide_80_wheel_transition(test_path)
    print(f"REWARD: {reward}")

