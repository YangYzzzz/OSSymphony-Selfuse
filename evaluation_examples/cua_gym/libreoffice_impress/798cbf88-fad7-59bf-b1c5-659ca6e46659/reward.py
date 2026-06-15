"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set the image wrap to Optimal and spacing 0.2 cm on all sides.
Generated: 2025-10-17 13:14:14
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import zipfile
from lxml import etree


def verify_image_wrap_optimal_spacing(file_path: str) -> float:
    """Verify that every (or at least one) picture in the presentation has
    LibreOffice specific wrap information set to:
        • type = "optimal"
        • lIns / tIns / rIns / bIns = 72000 (which equals 0.2 cm)
    Progressive scoring is awarded for:
        0.3 – wrap element present
        0.3 – wrap type == optimal
        0.1 × 4 – correct spacing on the four sides
    The score is capped at 1.0 and drops to 0 if the file contains no pictures.
    """
    print(f"Verifying image wrap settings for file: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            # Collect all slide XML parts
            slide_files = [f for f in z.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml")]
            if not slide_files:
                print("✗ No slide XML files found – invalid/empty presentation")
                return 0.0

            print(f"Found {len(slide_files)} slide xml files")

            ns = {
                "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
                "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
                "loExt": "http://libreoffice.org/loExt",
            }

            found_picture = False      # at least one <p:pic> encountered
            wrap_present = False       # at least one <loExt:wrap>
            optimal_type = False       # wrap@type == "optimal"
            spacing_ok = {side: False for side in ("lIns", "tIns", "rIns", "bIns")}
            target_emu = 72000         # 0.2 cm expressed in EMUs

            for slide_file in slide_files:
                root = etree.fromstring(z.read(slide_file))
                pictures = root.xpath(".//p:pic", namespaces=ns)
                if pictures:
                    print(f"Slide {slide_file} contains {len(pictures)} picture element(s)")
                for pic in pictures:
                    found_picture = True

                    # LibreOffice stores wrap info under   p:extLst/p:ext/loExt:wrap
                    wrap_nodes = pic.xpath(".//p:extLst/p:ext/loExt:wrap", namespaces=ns)
                    if not wrap_nodes:
                        continue

                    wrap_present = True
                    wrap = wrap_nodes[0]

                    # Check wrap type
                    wrap_type = wrap.get("type")
                    if wrap_type and wrap_type.lower() == "optimal":
                        optimal_type = True
                    else:
                        print(f"  Wrap type is not optimal (found: {wrap_type})")

                    # Check spacing on each side
                    for side in spacing_ok.keys():
                        val = wrap.get(side)
                        if val is None:
                            print(f"  Missing attribute {side} on wrap element")
                            continue
                        try:
                            if abs(int(val) - target_emu) <= 10:  # tiny tolerance
                                spacing_ok[side] = True
                            else:
                                print(f"  Attribute {side} has value {val}, expected {target_emu}")
                        except ValueError:
                            print(f"  Attribute {side} value '{val}' is not an integer")

                # Early stop if everything already perfect
                if optimal_type and all(spacing_ok.values()):
                    break

            # Compute progressive score
            score = 0.0
            if wrap_present:
                score += 0.3
            if optimal_type:
                score += 0.3
            score += 0.1 * sum(spacing_ok.values())  # 0-0.4 depending on sides

            if not found_picture:
                print("✗ No pictures found in presentation – task not applicable")
                score = 0.0

            score = min(score, 1.0)

            print("Verification summary:")
            print(f"  Wrap element present: {wrap_present}")
            print(f"  Wrap type optimal:   {optimal_type}")
            print(f"  Spacing correct:     {spacing_ok}")
            print(f"  Calculated score:    {score}")
            return score

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        return 0.0


if __name__ == "__main__":
    # Path provided by the task description
    FILE_PATH = "/home/user/set_the_image_wrap_to_optimal_and_spacing_02_cm_on_all_sides.pptx"
    reward = verify_image_wrap_optimal_spacing(FILE_PATH)
    print(f"REWARD: {reward}")

