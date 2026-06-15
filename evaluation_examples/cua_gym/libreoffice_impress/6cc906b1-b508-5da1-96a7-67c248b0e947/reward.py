"""
FINAL REWARD SCRIPT - SUCCESS
Task: For my self-running trade-show deck, I need slide 230 to fade in quickly and then move on by itself. Where in LibreOffice Impress do I set the transition to “Fade” with a 0.5-second duration and tell the slide to auto-advance exactly 8 seconds later?
Generated: 2025-09-10 20:51:38
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree as ET


def verify_transition_slide(file_path: str, slide_number: int = 230) -> float:
    """Verify that the specified slide has:
       1. A transition element
       2. Transition subtype = fade
       3. Duration = 0.5 s  (500 ms)
       4. Auto-advance after 8 s (advClick = 0, advTm = 8000)
       Progressive scoring (0.25 each).
       Returns a float between 0.0 and 1.0.
    """
    print(f"Verifying slide {slide_number} transition settings in: {file_path}")
    score = 0.0

    # Basic existence check (no points awarded)
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slide_path = f"ppt/slides/slide{slide_number}.xml"
            if slide_path not in pptx_zip.namelist():
                print(f"✗ Slide file not present in PPTX: {slide_path}")
                return 0.0

            slide_xml = pptx_zip.read(slide_path)
            root = ET.fromstring(slide_xml)
            NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

            transition = root.find(".//p:transition", namespaces=NS)
            if transition is None:
                print("✗ No <p:transition> element found on the slide")
            else:
                print("✓ Transition element present (0.25 points)")
                score += 0.25

                # Check subtype (first child element of transition)
                subtype = None
                for child in transition:
                    subtype = ET.QName(child).localname.lower()
                    break
                if subtype == "fade":
                    print("✓ Transition subtype is 'fade' (0.25 points)")
                    score += 0.25
                else:
                    print(f"✗ Transition subtype is not 'fade' (found: {subtype})")

                # Check duration attribute
                dur = transition.get("dur")
                if dur == "500":
                    print("✓ Duration is 500 ms (0.25 points)")
                    score += 0.25
                else:
                    print(f"✗ Duration is not 500 ms (found: {dur})")

                # Check automatic advance attributes
                adv_click = transition.get("advClick")
                adv_tm = transition.get("advTm")
                if adv_click == "0" and adv_tm == "8000":
                    print("✓ Auto-advance after 8 s and no click required (0.25 points)")
                    score += 0.25
                else:
                    print(
                        f"✗ Auto-advance not set correctly (advClick={adv_click}, advTm={adv_tm})"
                    )
    except Exception as e:
        print(f"✗ Error processing PPTX: {e}")
        return 0.0

    final_score = min(score, 1.0)
    print(f"Final score: {final_score}")
    return final_score


if __name__ == "__main__":
    FILE_PATH = "/home/user/for_my_self_running_trade_show_deck_i_need_slide_230_to_fade_in_quickly_and_then_move_on_by_itself_w_golden.pptx"
    reward = verify_transition_slide(FILE_PATH)
    print(f"REWARD: {reward}")
