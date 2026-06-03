"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 130, I want the title to just blink out when the slide finishes—no fancy spins or fades, just the standard “Disappear” exit effect. Can you set that up with a 0.3-second duration in LibreOffice Impress?
Generated: 2025-09-10 16:55:37
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
import math
from lxml import etree

"""
Reward Script for LibreOffice Impress Task
Task: Ensure that on slide 130 the title has a standard "Disappear" exit animation
      with a duration of 0.3 seconds.
Verification Approach:
1. Confirm the presentation file exists.
2. Ensure slide130.xml is present (verifies the slide really exists).
3. Parse slide130.xml and gather the shape IDs that correspond to the title placeholder.
4. Search for <p:animEffect> elements whose filter="disappear" and transition="out".
5. For every matching animation, verify:
   • the duration (dur) is 300 ms (±10 % tolerance) → 0.3 s
   • the animation targets one of the title-placeholder shape IDs.
6. Score progressively and print detailed diagnostics.
Scoring Weights (sum to 1.0):
   0.1 – Slide 130 exists
   0.4 – Disappear exit effect found
   0.3 – Duration equals 0.3 s
   0.2 – Target is the title placeholder
The script prints a final line formatted exactly as "REWARD: X.X".
"""

FILE_PATH = "/home/user/on_slide_130_i_want_the_title_to_just_blink_out_when_the_slide_finishesno_fancy_spins_or_fades_just__golden.pptx"


def verify_slide_130_disappear_effect(file_path: str) -> float:
    print(f"Verifying disappear animation on slide 130 in: {file_path}")

    # Progressive score initialisation
    score = 0.0
    MAX_SCORE = 1.0

    # Scoring weights
    W_SLIDE_EXISTS = 0.10
    W_DISAPPEAR_FOUND = 0.40
    W_DURATION_CORRECT = 0.30
    W_TARGET_TITLE = 0.20

    # 1. Basic file existence check (no points – prerequisite only)
    if not os.path.exists(file_path):
        print("✗ Presentation file not found.")
        return 0.0

    try:
        # 2. Open pptx as zip and check slide 130 exists
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slide_path = "ppt/slides/slide130.xml"
            if slide_path not in pptx_zip.namelist():
                print("✗ slide130.xml not present – slide 130 missing.")
                return 0.0
            score += W_SLIDE_EXISTS
            print(f"✓ slide130.xml found (+{W_SLIDE_EXISTS})")

            slide_xml = pptx_zip.read(slide_path)
            ns = {
                "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            }
            root = etree.fromstring(slide_xml)

            # 3. Identify title placeholder shape IDs
            title_spids = set()
            for sp in root.findall(".//p:sp", ns):
                ph = sp.find(".//p:ph", ns)
                if ph is not None and ph.get("type") in {"title", "ctrTitle"}:
                    c_nv_pr = sp.find(".//p:cNvPr", ns)
                    if c_nv_pr is not None and c_nv_pr.get("id"):
                        title_spids.add(c_nv_pr.get("id"))
            print(f"Title placeholder shape IDs detected: {title_spids if title_spids else 'None'}")

            # 4-5. Search for the disappear animation, duration, and target
            disappear_found = False
            duration_ok = False
            target_is_title = False

            for anim in root.findall(".//p:animEffect", ns):
                if (anim.get("filter", "").lower() == "disappear" and
                        (anim.get("transition") is None or anim.get("transition", "").lower() == "out")):
                    disappear_found = True

                    # Duration check
                    ctn = anim.find(".//p:cBhvr/p:cTn", ns)
                    if ctn is not None and ctn.get("dur"):
                        dur_raw = ctn.get("dur")
                        try:
                            dur_ms = float(dur_raw)
                        except ValueError:
                            # Sometimes duration is stored in seconds – convert to ms
                            try:
                                dur_ms = float(dur_raw) * 1000
                            except Exception:
                                dur_ms = None
                        if dur_ms is not None and math.isclose(dur_ms, 300, rel_tol=0.10):
                            duration_ok = True

                    # Target shape check
                    sp_tgt = anim.find(".//p:spTgt", ns)
                    if sp_tgt is not None and sp_tgt.get("spid") in title_spids:
                        target_is_title = True

            # Scoring based on findings
            if disappear_found:
                score += W_DISAPPEAR_FOUND
                print(f"✓ Disappear exit effect detected (+{W_DISAPPEAR_FOUND})")
            else:
                print("✗ No disappear exit effect detected on slide 130.")

            if duration_ok:
                score += W_DURATION_CORRECT
                print(f"✓ Animation duration is 0.3 s (+{W_DURATION_CORRECT})")
            elif disappear_found:
                print("✗ Animation duration is not 0.3 s (expected 300 ms).")

            if target_is_title:
                score += W_TARGET_TITLE
                print(f"✓ Animation targets the title placeholder (+{W_TARGET_TITLE})")
            elif disappear_found:
                print("✗ Animation does not target the title placeholder.")

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        return 0.0

    # 6. Final result (capped at MAX_SCORE)
    final_score = min(score, MAX_SCORE)
    print(f"Total Score: {final_score}/{MAX_SCORE}")
    return final_score


if __name__ == "__main__":
    reward_value = verify_slide_130_disappear_effect(FILE_PATH)
    print(f"REWARD: {reward_value}")
