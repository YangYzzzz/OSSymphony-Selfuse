"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tweaking slide 66 and I’d love the title to use the “Float In” entrance effect, but with a 0.2-second delay before it starts. How do I set that up in LibreOffice Impress?
Generated: 2025-09-11 00:53:13
Status: success
Model: azure-o3
Total Steps: 6
"""

import os, zipfile
from lxml import etree as ET

def verify_float_in_title(file_path: str) -> float:
    """Verify that slide 66 has a title with the 'Float In' entrance animation
    and that the animation is configured with a 0.2-second (200 ms) delay.

    Scoring (progressive):
        0.2 – Slide 66 exists in the file
        0.4 – A 200 ms delay ( <p:cond delay="200"/> ) is present in timing XML
        0.4 – The animation preset corresponds to the 'Float In' entrance effect
                (presetClass="entr" and presetID="35")
    Returns a float between 0.0 and 1.0 (inclusive).
    """

    # Namespaces used in PPTX presentation XML
    NS = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    max_score = 1.0
    score = 0.0

    # ---------- Basic file checks (NO points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        return 0.0

    try:
        pptx_zip = zipfile.ZipFile(file_path)
    except Exception as e:
        print("✗ Unable to open PPTX file:", e)
        return 0.0

    # ---------- Requirement 1: Slide 66 must exist (0.2 pts) ----------
    slide_path = "ppt/slides/slide66.xml"  # slides are 1-based in PPTX internals
    if slide_path in pptx_zip.namelist():
        score += 0.2
        print("✓ Slide 66 exists (+0.2)")
    else:
        print("✗ slide66.xml not found – cannot verify further")
        return score  # Early exit; nothing else can be checked

    # Parse the slide XML
    try:
        slide_xml = pptx_zip.read(slide_path)
        slide_root = ET.fromstring(slide_xml)
    except Exception as e:
        print("✗ Error parsing slide 66 XML:", e)
        return score

    # Locate the <p:timing> element that stores all animation information
    timing = slide_root.find(".//p:timing", NS)
    if timing is None:
        print("✗ No <p:timing> element – slide has no animations")
        return score

    print("✓ <p:timing> element found")

    # ---------- Requirement 2: 0.2-second delay present (0.4 pts) ----------
    delay_found = False
    for cond in timing.findall(".//p:cond", NS):
        delay_val = cond.get("delay")
        if delay_val is not None:
            try:
                if abs(int(delay_val) - 200) <= 1:  # accept exact 200 ms
                    delay_found = True
                    break
            except ValueError:
                pass  # Non-integer delays ignored

    if delay_found:
        score += 0.4
        print("✓ 0.2-second (200 ms) delay found (+0.4)")
    else:
        print("✗ Required 200 ms delay not found")

    # ---------- Requirement 3: 'Float In' entrance effect present (0.4 pts) ----------
    # In PPTX, the 'Float In' effect is presetClass="entr" & presetID="35"
    float_in_found = False
    for anim in timing.findall(".//p:animEffect", NS):
        if anim.get("presetClass") == "entr" and anim.get("presetID") == "35":
            float_in_found = True
            break

    if float_in_found:
        score += 0.4
        print("✓ 'Float In' entrance effect detected (+0.4)")
    else:
        print("✗ 'Float In' entrance effect not found on slide 66")

    final_score = min(score, max_score)
    print("Total score:", final_score)
    return final_score


if __name__ == "__main__":
    # Path to the PPTX provided in the task context
    FILE_PATH = "/home/user/im_tweaking_slide_66_and_id_love_the_title_to_use_the_float_in_entrance_effect_but_with_a_02_second__golden.pptx"

    reward = verify_float_in_title(FILE_PATH)
    print(f"REWARD: {reward}")
