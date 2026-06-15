"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Impress, could you show me how to make only slides 1, 3, and 5 use the “Wipe from Bottom” transition, timed at exactly 0.7 seconds? I don’t want the other slides touched—just those three.
Generated: 2025-09-10 14:14:45
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
import zipfile
from lxml import etree

# -------------------------------------------------------------
# Reward Script for LibreOffice Impress Transition Verification
# -------------------------------------------------------------
# Task:  
# “Make ONLY slides 1, 3, and 5 use the ‘Wipe from Bottom’ transition,
#  timed at exactly 0.7 seconds. No other slides should be touched.”
# -------------------------------------------------------------
# Scoring Logic (progressive – max 1.0):
#   • 0.60 pts → Correct transition (type, direction, duration) on slides 1,3,5
#                 – each target slide worth 0.20 (0.05 existence, 0.05 type,
#                   0.05 direction, 0.05 duration).
#   • 0.40 pts → ZERO transition on every non-target slide
#                 (awarded proportionally).
# -------------------------------------------------------------

TARGET_SLIDES = {1, 3, 5}  # 1-based slide indices
TRANS_TYPE_EXPECTED = "wipe"          # wipe transition
TRANS_DIR_EXPECTED = "b"              # bottom direction in PPTX spec
TRANS_DURATION_MS   = 700             # 0.7 seconds  → 700 ms


def _slide_files(pptx_zip):
    """Return list of slide XML paths ordered by slide number."""
    files = [f for f in pptx_zip.namelist()
             if f.startswith("ppt/slides/slide") and f.endswith(".xml")]
    files.sort(key=lambda x: int(re.findall(r"slide(\d+).xml", x)[0]))
    return files


def _parse_transition(xml_bytes):
    """Extract transition info from a slide XML. Return dict or None."""
    root = etree.fromstring(xml_bytes)
    trans_el = root.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}transition")
    if trans_el is None:
        return None

    # First child element indicates the transition type (e.g., <p:wipe …/>)
    child = next(iter(trans_el), None)
    trans_type = etree.QName(child).localname if child is not None else None
    direction  = child.get("dir") if child is not None else None
    duration   = int(trans_el.get("dur")) if trans_el.get("dur") and trans_el.get("dur").isdigit() else None
    return {"type": trans_type, "dir": direction, "duration": duration}


def verify_impress_transition_task(file_path: str) -> float:
    """Main verification routine – returns score between 0.0 and 1.0."""
    print(f"Verifying presentation transitions in: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found – task failed")
        return 0.0

    total_score = 0.0  # progressive accumulation
    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slides = _slide_files(pptx_zip)
            slide_count = len(slides)
            print(f"Total slides detected: {slide_count}")

            # ---------------------------------------------------------
            # PART 1 – Check target slides (max 0.60)
            # ---------------------------------------------------------
            per_slide_total = 0.20  # max for each target slide
            for idx, slide_path in enumerate(slides, start=1):
                xml_bytes   = pptx_zip.read(slide_path)
                trans_info  = _parse_transition(xml_bytes)

                if idx in TARGET_SLIDES:
                    print(f"Checking TARGET slide {idx} …")
                    if trans_info is None:
                        print("  ✗ No transition found – 0 pts for this slide")
                        continue  # no points can be earned for this slide

                    # 0.05 for mere presence (already ensured) – add later
                    slide_score = 0.05

                    # 0.05 type check
                    if trans_info["type"] == TRANS_TYPE_EXPECTED:
                        slide_score += 0.05
                        print("  ✓ Transition type = wipe (+0.05)")
                    else:
                        print(f"  ✗ Wrong transition type: {trans_info['type']}")

                    # 0.05 direction check
                    if trans_info["dir"] == TRANS_DIR_EXPECTED:
                        slide_score += 0.05
                        print("  ✓ Direction = bottom (+0.05)")
                    else:
                        print(f"  ✗ Wrong direction: {trans_info['dir']}")

                    # 0.05 duration check (700 ms)
                    if trans_info["duration"] == TRANS_DURATION_MS:
                        slide_score += 0.05
                        print("  ✓ Duration = 700 ms (+0.05)")
                    else:
                        print(f"  ✗ Wrong duration: {trans_info['duration']} ms")

                    print(f"  → Slide {idx} score: {slide_score:.2f}/{per_slide_total}")
                    total_score += slide_score

            # ---------------------------------------------------------
            # PART 2 – Ensure non-target slides have NO transition (max 0.40)
            # ---------------------------------------------------------
            non_target_indices = [i for i in range(1, slide_count + 1) if i not in TARGET_SLIDES]
            no_transition_count = 0
            for i in non_target_indices:
                xml_bytes  = pptx_zip.read(slides[i - 1])
                if _parse_transition(xml_bytes) is None:
                    no_transition_count += 1

            if non_target_indices:
                proportion_clean = no_transition_count / len(non_target_indices)
                non_target_score = proportion_clean * 0.40
                print(f"Non-target slides without transitions: {no_transition_count}/"
                      f"{len(non_target_indices)} → +{non_target_score:.2f} pts")
                total_score += non_target_score
            else:
                # Edge case: presentation only contains target slides
                total_score += 0.40

    except Exception as exc:
        print(f"✗ Error while verifying: {exc}")
        return 0.0

    # Cap and round score
    final_score = round(min(total_score, 1.0), 2)
    print(f"FINAL SCORE: {final_score}")
    return final_score


if __name__ == "__main__":
    FILE_PATH = "/home/user/in_libreoffice_impress_could_you_show_me_how_to_make_only_slides_1_3_and_5_use_the_wipe_from_bottom__golden.pptx"
    reward = verify_impress_transition_task(FILE_PATH)
    print(f"REWARD: {reward}")

