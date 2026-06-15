"""
FINAL REWARD SCRIPT - SUCCESS
Task: For slide 298, I’d like to swap in the “Dissolve” transition, set the duration to exactly 1.2 seconds, and keep it on manual advance so it only moves when I click. How do I do that in LibreOffice Impress?
Generated: 2025-09-10 20:02:27
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree as ET


def verify_pptx_transition(file_path: str, slide_number: int = 298) -> float:
    """Verify that a specific slide has a Dissolve transition, 1.2 s duration,
    and advances only on mouse click.

    Scoring (progressive):
        0.1  – slide file exists inside pptx
        0.2  – <p:transition> element present
        0.3  – transition type is dissolve
        0.2  – duration attribute equals 1200 ms (1.2 s)
        0.2  – manual advance (advClick="1" and no/zero advTm)
    Returns a float between 0 and 1.
    """

    print(f"Verifying transition settings for slide {slide_number} in: {file_path}")
    score = 0.0
    max_score = 1.0

    # 1. Basic file existence check (no points – prerequisite)
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            # -----------------------------------------------------------------
            # 2. Locate the slide XML inside the PPTX
            # -----------------------------------------------------------------
            slide_path = f"ppt/slides/slide{slide_number}.xml"
            if slide_path not in z.namelist():
                print(f"✗ Slide file {slide_path} not found in PPTX")
                return 0.0
            print("✓ Slide file exists (0.1 points)")
            score += 0.1

            # -----------------------------------------------------------------
            # 3. Parse the slide XML and locate the <p:transition> element
            # -----------------------------------------------------------------
            xml_bytes = z.read(slide_path)
            root = ET.fromstring(xml_bytes)
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
            transition_el = root.find(".//p:transition", ns)

            if transition_el is None:
                print("✗ No <p:transition> element found on the slide")
                return score  # early exit with current partial score
            print("✓ Transition element found (0.2 points)")
            score += 0.2

            # -----------------------------------------------------------------
            # 4. Verify transition type is Dissolve
            # -----------------------------------------------------------------
            dissolve_child = None
            for child in transition_el:
                if ET.QName(child).localname.lower() == "dissolve":
                    dissolve_child = child
                    break
            if dissolve_child is None:
                print("✗ Transition is not 'Dissolve'")
            else:
                print("✓ Transition type is 'Dissolve' (0.3 points)")
                score += 0.3

            # -----------------------------------------------------------------
            # 5. Verify duration is exactly 1200 ms (1.2 s)
            # -----------------------------------------------------------------
            duration_attr = transition_el.get("dur")  # duration in milliseconds
            if duration_attr == "1200":
                print("✓ Duration is exactly 1200 ms (0.2 points)")
                score += 0.2
            else:
                print(f"✗ Duration is not 1200 ms (found: {duration_attr})")

            # -----------------------------------------------------------------
            # 6. Verify manual advance (on-click only)
            # -----------------------------------------------------------------
            adv_click = transition_el.get("advClick")
            adv_time = transition_el.get("advTm")

            if adv_click == "1" and (adv_time in (None, "0")):
                print("✓ Slide is set to advance on click only (0.2 points)")
                score += 0.2
            else:
                print(
                    f"✗ Manual advance condition failed (advClick={adv_click}, advTm={adv_time})"
                )
    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0

    final_score = min(score, max_score)
    print(f"Total Score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    test_path = "/home/user/for_slide_298_id_like_to_swap_in_the_dissolve_transition_set_the_duration_to_exactly_12_seconds_and__golden.pptx"
    reward_val = verify_pptx_transition(test_path)
    print(f"REWARD: {reward_val}")
