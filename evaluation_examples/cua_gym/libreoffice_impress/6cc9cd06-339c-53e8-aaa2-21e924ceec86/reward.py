"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Impress, slide 45’s title needs a bit of punch: can you show me how to set its character background highlight to solid yellow (#FFFF00) only for that slide?
Generated: 2025-09-10 22:23:43
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
import zipfile
from lxml import etree


def _sorted_slide_paths(zip_obj):
    """Return slide XML paths sorted by slide number (1-based)."""
    slide_paths = [p for p in zip_obj.namelist()
                  if p.startswith("ppt/slides/slide") and p.endswith(".xml")]
    slide_paths.sort(key=lambda p: int(re.search(r"slide(\d+)\.xml$", p).group(1)))
    return slide_paths


def _highlight_info(root, target_rgb):
    """Detect highlight runs and whether they reside in the title placeholder."""
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    highlight_found = False
    highlight_in_title = False

    for hl in root.xpath(".//a:highlight", namespaces=ns):
        clr = hl.find(".//a:srgbClr", namespaces=ns)
        if clr is not None and clr.get("val", "").lower() == target_rgb.lower():
            highlight_found = True
            # climb ancestors to see if inside a title placeholder <p:ph type="title"/ctrTitle>
            for anc in hl.iterancestors("{http://schemas.openxmlformats.org/presentationml/2006/main}sp"):
                ph = anc.find(".//p:nvSpPr/p:nvPr/p:ph", namespaces=ns)
                if ph is not None and ph.get("type") in ("title", "ctrTitle"):
                    highlight_in_title = True
                    break
    return highlight_found, highlight_in_title


def verify_task(file_path: str) -> float:
    """Reward script for verifying yellow highlight on slide 45 title only."""
    print(f"Verifying task for file: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0

    score = 0.0  # progressive score
    target_rgb = "ffff00"  # solid yellow

    try:
        with zipfile.ZipFile(file_path) as z:
            slide_paths = _sorted_slide_paths(z)
            slide_count = len(slide_paths)
            print(f"Total slides detected: {slide_count}")

            if slide_count < 45:
                print("✗ Presentation has fewer than 45 slides – requirement not met")
                print("REWARD: 0.0")
                return 0.0

            # --- Check slide 45 ---
            slide45_path = slide_paths[44]  # zero-based index
            root45 = etree.fromstring(z.read(slide45_path))
            found, in_title = _highlight_info(root45, target_rgb)

            if found:
                print("✓ Yellow highlight (FFFF00) present on slide 45 (0.5)")
                score += 0.5
                if in_title:
                    print("✓ Highlight applied to title placeholder (0.3)")
                    score += 0.3
                else:
                    print("✗ Highlight not applied to the title placeholder (0.0)")
            else:
                print("✗ Yellow highlight not found on slide 45 (0.0)")

            # --- Ensure yellow highlight NOT on other slides ---
            highlight_elsewhere = False
            if found:  # only meaningful to check if highlight exists at all
                ns = {
                    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
                }
                for idx, path in enumerate(slide_paths):
                    if idx == 44:
                        continue  # skip slide 45
                    data = z.read(path)
                    if b"<a:highlight" not in data:
                        continue  # quick filter
                    root = etree.fromstring(data)
                    for hl in root.xpath(".//a:highlight", namespaces=ns):
                        clr = hl.find(".//a:srgbClr", namespaces=ns)
                        if clr is not None and clr.get("val", "").lower() == target_rgb:
                            highlight_elsewhere = True
                            print(f"✗ Yellow highlight also found on slide {idx+1} – should be unique")
                            break
                    if highlight_elsewhere:
                        break

                if not highlight_elsewhere:
                    print("✓ No yellow highlight found on other slides (0.2)")
                    score += 0.2

    except Exception as e:
        print("✗ Error during verification:", e)
        print("REWARD: 0.0")
        return 0.0

    final_score = min(score, 1.0)
    print(f"Reward score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when run as a script
if __name__ == "__main__":
    verify_task("/home/user/in_libreoffice_impress_slide_45s_title_needs_a_bit_of_punch_can_you_show_me_how_to_set_its_character_golden.pptx")
