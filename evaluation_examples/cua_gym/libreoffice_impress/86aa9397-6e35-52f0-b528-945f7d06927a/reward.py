"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 29 I’d like the content to slide in with the “Push from Right” transition, set to 0.8 seconds, and then have that slide move on automatically after 7 seconds. How do I set that up in LibreOffice Impress?
Generated: 2025-09-10 15:10:07
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import re
import zipfile
from lxml import etree

def verify_slide29_transition(file_path: str) -> float:
    """Verify that slide 29 of a PPTX has:
    1. A transition element
    2. Transition type = Push from Right
    3. Duration ≈ 0.8 s (800 ms)
    4. Automatic advance after ≈ 7 s (7000 ms)

    Returns a progressive score between 0.0 and 1.0.
    """

    REQUIRED_SLIDE_INDEX = 29  # 1-indexed as per user request
    MAX_SCORE = 1.0
    score = 0.0

    print(f"Verifying transitions in file: {file_path}")

    # --- Preliminary checks (no points for these — natural conditions) ---
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0
    if not file_path.lower().endswith(".pptx"):
        print("✗ File is not a .pptx PowerPoint")
        return 0.0

    try:
        # Open pptx container
        with zipfile.ZipFile(file_path, "r") as archive:
            # Collect slide XML paths
            slide_files = [n for n in archive.namelist() if re.match(r"ppt/slides/slide[0-9]+\.xml", n)]
            if not slide_files:
                print("✗ No slide XML files found in presentation")
                return 0.0
            # Sort numerically (slide1.xml, slide2.xml, …)
            slide_files.sort(key=lambda x: int(re.findall(r"(\d+)", x)[-1]))
            total_slides = len(slide_files)
            print(f"Found {total_slides} slide XML files")

            if total_slides < REQUIRED_SLIDE_INDEX:
                print(f"✗ Slide {REQUIRED_SLIDE_INDEX} does not exist (only {total_slides} slides)")
                return 0.0

            target_slide_name = slide_files[REQUIRED_SLIDE_INDEX - 1]
            print(f"Slide {REQUIRED_SLIDE_INDEX} maps to file: {target_slide_name}")

            # Parse XML of target slide
            slide_xml = archive.read(target_slide_name)
            root = etree.fromstring(slide_xml)
            ns = {
                "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            }

            # 1) Transition element presence (0.4)
            transition_el = root.find(".//p:transition", ns)
            if transition_el is not None:
                print("✓ <p:transition> element found")
                score += 0.4
            else:
                print("✗ No transition element on slide")
                print(f"Total score: {score}/{MAX_SCORE}")
                return score

            # 2) Push-from-right type (0.3)
            push_el = transition_el.find("p:push", ns)
            if push_el is not None and push_el.get("dir") == "r":
                print("✓ Transition type is Push from Right")
                score += 0.3
            else:
                print("✗ Transition is not Push from Right")

            # 3) Duration ≈ 800 ms (0.2)
            dur_attr = transition_el.get("dur")
            if dur_attr is not None:
                try:
                    dur_val = int(dur_attr)
                    if abs(dur_val - 800) <= 50:  # ±50 ms tolerance
                        print(f"✓ Duration {dur_val} ms is within tolerance of 800 ms")
                        score += 0.2
                    else:
                        print(f"✗ Duration {dur_val} ms is not close to 800 ms")
                except ValueError:
                    print("✗ Duration attribute is not an integer")
            else:
                print("✗ No duration (dur) attribute found")

            # 4) Auto-advance ≈ 7000 ms (0.1)
            adv_attr = transition_el.get("advTm")
            if adv_attr is not None:
                try:
                    adv_val = int(adv_attr)
                    if abs(adv_val - 7000) <= 200:  # ±200 ms tolerance
                        print(f"✓ Advance time {adv_val} ms is within tolerance of 7000 ms")
                        score += 0.1
                    else:
                        print(f"✗ Advance time {adv_val} ms is not close to 7000 ms")
                except ValueError:
                    print("✗ advTm attribute is not an integer")
            else:
                print("✗ No advTm (auto-advance) attribute found")

            # Clamp and round score
            if score > 0.99:
                score = 1.0
            score = min(score, MAX_SCORE)
            final_score = round(score, 3)
            print(f"Total score: {final_score}/{MAX_SCORE}")
            return final_score

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        return 0.0


# -------------------- Stand-alone execution ---------------------------
if __name__ == "__main__":
    default_pptx = (
        "/home/user/on_slide_29_id_like_the_content_to_slide_in_with_the_push_from_right_"
        "transition_set_to_08_seconds_an_golden.pptx"
    )
    reward = verify_slide29_transition(default_pptx)
    print(f"REWARD: {reward}")
