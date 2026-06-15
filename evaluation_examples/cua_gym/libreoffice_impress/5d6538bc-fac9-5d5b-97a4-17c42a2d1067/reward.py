"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 7 still has a plain 1-2-3 numbered list, but the team wants it formatted as a checklist. In LibreOffice Impress, how do I replace those numbers with the built-in “Checkmark” bullet style (the green ✔ symbol) just for that single slide?
Generated: 2025-09-10 14:31:45
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import glob
import zipfile
from lxml import etree as ET


def verify_checklist_bullet(file_path: str, slide_number: int = 7) -> float:
    """Verify that slide `slide_number` in `file_path` uses a green check-mark
    bullet style (Wingdings ✔) instead of a numbered list.

    Scoring (progressive, up to 1.0):
      • 0.4 – No <a:buAutoNum> elements (numbers removed)
      • 0.4 – Presence of <a:buChar> elements (bullets defined)
      • 0.2 – Bullet char/font corresponds to a check-mark style
    """
    print(f"Verifying checklist bullet on slide {slide_number} -> {file_path}\n")

    score = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # 1. Basic file existence check (no points awarded)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Extract target slide XML from PPTX
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            slide_path = f"ppt/slides/slide{slide_number}.xml"
            if slide_path not in z.namelist():
                print(f"✗ Slide XML not found: {slide_path}")
                return 0.0
            slide_xml = z.read(slide_path)
    except Exception as e:
        print(f"✗ Error reading PPTX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 3. Parse XML & prepare namespaces
    # ------------------------------------------------------------------
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }
    try:
        root = ET.fromstring(slide_xml)
    except ET.XMLSyntaxError as e:
        print(f"✗ XML parse error: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 4. Verification steps with progressive scoring
    # ------------------------------------------------------------------
    # 4a – Ensure numbered list removed (no <a:buAutoNum>)
    auto_num_elems = root.xpath(".//a:buAutoNum", namespaces=ns)
    if not auto_num_elems:
        print("✓ No <a:buAutoNum> elements found (numbers removed) (+0.4)")
        score += 0.4
    else:
        print(f"✗ Found {len(auto_num_elems)} numbered bullet elements – numbers remain")

    # 4b – Check that bullet characters (<a:buChar>) are present
    bu_char_elems = root.xpath(".//a:buChar", namespaces=ns)
    if bu_char_elems:
        print(f"✓ Found {len(bu_char_elems)} <a:buChar> bullet character elements (+0.4)")
        score += 0.4
    else:
        print("✗ No <a:buChar> elements found – bullets not defined")

    # 4c – Verify bullet represents a check-mark (character or Wingdings font)
    accepted_chars = {
        "\u2713",  # ✓ (check mark)
        "\u2714",  # ✔ (heavy check mark)
        "\uF0FC",  #  (private-use tick)
        "\u00FC",  # ü (Wingdings tick when Wingdings font is used)
    }
    tick_found = False
    tick_font_found = False
    for elem in bu_char_elems:
        char = elem.get("char")
        if char in accepted_chars:
            tick_found = True
        parent = elem.getparent()
        bu_font_elems = parent.xpath("./a:buFont", namespaces=ns)
        for bf in bu_font_elems:
            tf = bf.get("typeface")
            if tf and tf.lower() == "wingdings":
                tick_font_found = True
    if tick_found or tick_font_found:
        print("✓ Bullet character corresponds to check-mark style (+0.2)")
        score += 0.2
    else:
        print("✗ Bullet character does not match expected check-mark style")

    # ------------------------------------------------------------------
    # 5. Final score
    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"\nTotal Score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    # Auto-detect the provided PPTX inside /home/user (unique name fragment)
    candidates = glob.glob(
        "/home/user/*slide_7_still_has_a_plain*_formatted_as_a_checklist_in_libr*.pptx"
    )
    pptx_file = (
        candidates[0]
        if candidates
        else "/home/user/slide_7_still_has_a_plain_1_2_3_numbered_list_but_the_team_wants_it_formatted_as_a_checklist_in_libr_golden.pptx"
    )

    reward_value = verify_checklist_bullet(pptx_file)
    print(f"REWARD: {reward_value}")

