"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 233, there’s a shape labeled “Rectangle 1.” I want to give that rectangle a modest 3-D pop by applying an extrusion depth of exactly 2 pt. What steps do I follow in LibreOffice Impress to make that happen?
Generated: 2025-09-10 19:52:12
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
from lxml import etree


def verify_extrusion_depth(file_path: str,
                            target_slide_num: int = 233,
                            shape_name: str = "Rectangle 1",
                            expected_depth_pt: float = 2.0) -> float:
    """Verify that the given PPTX file has, on slide `target_slide_num`,
    a shape named `shape_name` whose 3-D extrusion depth is exactly
    `expected_depth_pt` points.

    Scoring (progressive):
        0.0  – File missing / unreadable or target slide not present
        +0.4 – Target shape present on the specified slide
        +0.6 – Shape has a:sp3d element with extrusionH equal to
                expected depth (in EMUs)
        ==> 1.0 maximum
    """

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    max_score = 1.0
    score = 0.0

    # ---------- Basic safety checks (no points awarded) ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        pptx_zip = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"✗ Unable to open PPTX file: {e}")
        return 0.0

    slide_path = f"ppt/slides/slide{target_slide_num}.xml"
    if slide_path not in pptx_zip.namelist():
        print(f"✗ Target slide ({target_slide_num}) not found in PPTX")
        return 0.0

    try:
        slide_xml = pptx_zip.read(slide_path)
        root = etree.fromstring(slide_xml)
    except Exception as e:
        print(f"✗ Failed to parse slide XML: {e}")
        return 0.0

    # ---------- Locate the shape ----------
    shape_found = False
    correct_extrusion = False

    # Convert expected depth from points to EMUs (1 pt == 12700 EMU)
    expected_depth_emu = int(round(expected_depth_pt * 12700))

    for sp in root.findall(".//p:sp", ns):
        cNvPr = sp.find("./p:nvSpPr/p:cNvPr", ns)
        if cNvPr is None:
            continue
        name = cNvPr.get("name", "")
        if name == shape_name:
            shape_found = True
            # Look for 3-D properties (a:sp3d)
            sp3d = sp.find(".//a:sp3d", ns)
            if sp3d is not None:
                extrusionH = sp3d.get("extrusionH")
                if extrusionH is not None:
                    try:
                        extrusion_val = int(extrusionH)
                        print(
                            f"Found extrusion depth (EMU): {extrusion_val} – Expected: {expected_depth_emu}"
                        )
                        if extrusion_val == expected_depth_emu:
                            correct_extrusion = True
                    except ValueError:
                        print("✗ extrusionH attribute is not an integer value")
                else:
                    print("✗ 3-D properties present but extrusionH attribute missing")
            else:
                print("✗ Shape found, but no 3-D properties (a:sp3d) applied")
            break  # No need to inspect more shapes once target is handled

    # ---------- Scoring ----------
    if not shape_found:
        print("✗ Target shape not found on the slide")
    else:
        print("✓ Target shape found")
        score += 0.4  # Shape presence earns 0.4
        if correct_extrusion:
            print("✓ Correct extrusion depth applied")
            score += 0.6  # Correct depth earns remaining 0.6
        else:
            print("✗ Incorrect or missing extrusion depth")

    final_score = min(score, max_score)
    print(f"Total Score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    # Path to the presentation the grading system will evaluate
    FILE_PATH = (
        "/home/user/on_slide_233_theres_a_shape_labeled_rectangle_1_i_want_to_give_"
        "that_rectangle_a_modest_3_d_pop_by_ap_golden.pptx"
    )

    reward = verify_extrusion_depth(FILE_PATH)
    print(f"REWARD: {reward}")
