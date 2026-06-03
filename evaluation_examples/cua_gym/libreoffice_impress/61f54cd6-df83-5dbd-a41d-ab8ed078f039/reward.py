"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 18 I want Text Box 1 to just pop onto the screen as soon as the slide shows—no extra click. In LibreOffice Impress, how do I give it the “Appear” animation and set it to start “With previous”?
Generated: 2025-09-10 13:34:18
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree as ET


def verify_animation(file_path: str) -> float:
    """Verify that on slide 18, shape "Text Box 1" has an Appear animation
    set to start *With Previous* (i.e., no extra click). Returns a progressive
    score between 0.0 and 1.0. Exact 1.0 only if both conditions are met.
    """

    print(f"Verifying presentation: {file_path}")
    total_score = 0.0  # progressive score
    max_score = 1.0

    # 1) Basic sanity checks -------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0
    if not file_path.lower().endswith(".pptx"):
        print("✗ Not a .pptx file – verification aborted")
        return 0.0

    try:
        # ------------------------------------------------------------------
        # 2) Locate slide 18 inside the pptx package
        # ------------------------------------------------------------------
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            # Read presentation.xml to map slide order → relationship Id
            pres_root = ET.fromstring(pptx_zip.read("ppt/presentation.xml"))
            ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
            slide_ids = pres_root.xpath(".//p:sldIdLst/p:sldId", namespaces=ns)

            if len(slide_ids) < 18:
                print("✗ Presentation has fewer than 18 slides; slide 18 absent")
                return 0.0

            r_id_slide18 = slide_ids[17].get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            # Resolve r:id → actual slide path via presentation.xml.rels
            rels_root = ET.fromstring(pptx_zip.read("ppt/_rels/presentation.xml.rels"))
            target_slide_path = None
            for rel in rels_root:
                if rel.get("Id") == r_id_slide18:
                    target_slide_path = "ppt/" + rel.get("Target").lstrip("/")
                    break
            if not target_slide_path:
                print("✗ Could not resolve slide 18 path in package")
                return 0.0

            # ------------------------------------------------------------------
            # 3) Parse slide 18 XML and map shape names → shape ids
            # ------------------------------------------------------------------
            slide_root = ET.fromstring(pptx_zip.read(target_slide_path))
            ns.update({"a": "http://schemas.openxmlformats.org/drawingml/2006/main"})

            shape_name_to_id = {}
            for sp in slide_root.findall(".//p:sp", ns):
                cNvPr = sp.find("./p:nvSpPr/p:cNvPr", ns)
                if cNvPr is not None:
                    name = cNvPr.get("name", "")
                    spid = cNvPr.get("id")  # shape id inside slide timeline
                    shape_name_to_id[name] = spid

            print("Shape names on slide 18:", list(shape_name_to_id.keys()))

            # Accept either "Text Box 1" or "TextBox 1" (LibreOffice/PowerPoint variant)
            target_shape_name = None
            for nm in shape_name_to_id:
                if nm.replace(" ", "").lower() == "textbox1":
                    target_shape_name = nm
                    break

            if not target_shape_name:
                print("✗ Shape 'Text Box 1' not found on slide 18")
                return 0.0  # nothing further to verify

            target_shape_id = shape_name_to_id[target_shape_name]
            print(f"✓ Found target shape '{target_shape_name}' with id {target_shape_id}")

            # ------------------------------------------------------------------
            # 4) Inspect timing (animation) XML for the target shape
            # ------------------------------------------------------------------
            timing = slide_root.find(".//p:timing", ns)
            if timing is None:
                print("✗ No animation/timing information present on slide 18")
                return 0.0

            appear_found = False  # Appear effect attached to the shape
            with_previous = False  # Starts automatically (no onClick condition)

            for anim_effect in timing.findall(".//p:animEffect", ns):
                parent = anim_effect.getparent()

                # Ascend until we reach the parent cTn container
                ctn = parent
                while ctn is not None and ET.QName(ctn).localname != "cTn":
                    ctn = ctn.getparent()

                # Identify the target element for this animation
                sp_tgt = ctn.find(".//p:spTgt", ns) if ctn is not None else None
                if sp_tgt is None or sp_tgt.get("spid") != target_shape_id:
                    continue  # Not our shape – skip

                # Check animation type → Appear
                if (anim_effect.get("filter", "").lower() == "appear") or (
                    anim_effect.get("transition", "").lower() == "in"
                ):
                    appear_found = True

                    # Determine start condition → *With Previous* means there is
                    # NO explicit onClick start condition. If stCondLst/prevCondLst
                    # exist search for evt="onClick"; their absence also implies
                    # With Previous (auto-start).
                    has_click_condition = False
                    for cond_list_tag in ("stCondLst", "prevCondLst"):
                        cond_parent = ctn.find(f"./p:{cond_list_tag}", ns)
                        if cond_parent is not None:
                            for cond in cond_parent.findall(".//p:cond", ns):
                                if cond.get("evt") == "onClick":
                                    has_click_condition = True
                                    break
                        if has_click_condition:
                            break

                    with_previous = not has_click_condition  # true when auto-start
                    break  # First matching animation is enough

            # ------------------------------------------------------------------
            # 5) Progressive scoring based on findings
            # ------------------------------------------------------------------
            if appear_found:
                print("✓ Appear animation correctly assigned to the shape (0.5)")
                total_score += 0.5
            else:
                print("✗ Appear animation NOT found for the target shape")

            if with_previous:
                print("✓ Animation is configured to start 'With Previous' (0.5)")
                total_score += 0.5
            else:
                print("✗ Animation does NOT start 'With Previous'")

    except Exception as err:
        print(f"✗ Verification failed due to error: {err}")
        return 0.0

    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}")
    return final_score


# ---------------------------------------------------------------------------
# Execute verification when the script runs as __main__
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = (
        "/home/user/"
        "on_slide_18_i_want_text_box_1_to_just_pop_onto_the_screen_as_soon_as_the_slide_showsno_extra_click_i_golden.pptx"
    )
    reward = verify_animation(FILE_PATH)
    print(f"REWARD: {reward}")
