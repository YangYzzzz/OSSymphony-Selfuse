"""
FINAL REWARD SCRIPT - SUCCESS
Task: For the opening slide in LibreOffice Impress, I want a smooth Fade transition that lasts 1.5 seconds, and I need the slide to flip to the next one automatically after 5.0 seconds. How do I set that up?
Generated: 2025-09-10 14:47:42
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
from lxml import etree as ET


def verify_impress_fade(file_path: str) -> float:
    """Reward script to verify the task:
    Opening slide must have a Fade transition lasting ~1.5 s and
    must advance automatically after ~5 s.

    Progressive scoring (adds up to 1.0):
      • Transition element present ................ 0.4
      • Fade transition type ...................... 0.3
      • Duration ≈ 1.5 s (1400-1600 ms) ........... 0.2
      • Auto-advance ≈ 5 s (4900-5100 ms) ......... 0.1
    """

    print(f"Verifying presentation transitions in: {file_path}")
    score = 0.0

    # ---------- Preliminary checks (no points awarded) ----------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0
    if not file_path.lower().endswith(".pptx"):
        print("✗ Unsupported format (expected .pptx)")
        return 0.0

    # ---------- Read first-slide XML ----------
    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slide1_path = "ppt/slides/slide1.xml"
            if slide1_path not in pptx_zip.namelist():
                print("✗ slide1.xml not found in pptx")
                return 0.0

            root = ET.fromstring(pptx_zip.read(slide1_path))
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
            transition = root.find(".//p:transition", ns)

            # ---------- 1) Transition element present ----------
            if transition is None:
                print("✗ No transition element on first slide")
                return 0.0
            print("✓ Transition element present (0.4)")
            score += 0.4

            # ---------- 2) Fade transition type ----------
            if transition.find("p:fade", ns) is not None:
                print("✓ Fade transition detected (0.3)")
                score += 0.3
            else:
                print("✗ Transition is not fade")

            # ---------- 3) Duration ≈ 1.5 s ----------
            dur_attr = transition.attrib.get("dur")  # value in milliseconds
            if dur_attr:
                try:
                    dur_ms = int(dur_attr)
                    print(f"  Duration: {dur_ms} ms")
                    if 1400 <= dur_ms <= 1600:
                        print("✓ Duration ~1.5 s (0.2)")
                        score += 0.2
                    else:
                        print("✗ Duration not in 1.5 s range")
                except ValueError:
                    print("✗ Invalid duration value")
            else:
                print("✗ Duration attribute missing")

            # ---------- 4) Auto-advance ≈ 5 s ----------
            adv_attr = transition.attrib.get("advTm")  # value in milliseconds
            if adv_attr:
                try:
                    adv_ms = int(adv_attr)
                    print(f"  Advance time: {adv_ms} ms")
                    if 4900 <= adv_ms <= 5100:
                        print("✓ Advance time ~5 s (0.1)")
                        score += 0.1
                    else:
                        print("✗ Advance time not in 5 s range")
                except ValueError:
                    print("✗ Invalid advTm value")
            else:
                print("✗ advTm attribute missing")

    except Exception as e:
        print("✗ Error reading PPTX:", e)
        return 0.0

    # Avoid floating-point epsilon issues
    final_score = score if score < 0.999 else 1.0
    print(f"Final score: {final_score}")
    return final_score


if __name__ == "__main__":
    test_path = "/home/user/for_the_opening_slide_in_libreoffice_impress_i_want_a_smooth_fade_transition_that_lasts_15_seconds_a_golden.pptx"
    reward_val = verify_impress_fade(test_path)
    print(f"REWARD: {reward_val}")
