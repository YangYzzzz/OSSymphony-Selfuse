"""
FINAL REWARD SCRIPT - SUCCESS
Task: Apply drop caps to the first paragraph: 1 character over 2 lines.
Generated: 2025-10-17 07:11:18
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree as ET


def verify_drop_cap_task(pptx_path: str) -> float:
    """Verify that the first paragraph in a PPTX file has a drop-cap style
    (1 character over 2 lines).  Because the PPTX format stores a drop cap as
    a separate run that contains a single (first) character with a
    significantly larger font size, we check for:
        1. A paragraph whose first run is exactly ONE character long.
        2. A second run that contains the remainder of the paragraph text.
        3. The font size of the first run is at least 1.5× the size of the
           following run (indicating the enlarged drop cap).
    Progressive scoring:
        • 0.6 points – A paragraph with the single-character first run followed
          by additional text is found.
        • +0.4 points – The first-run character’s font size is ≥ 1.5× the font
          size of the following run (evidence of visual enlargement).
    The final score is capped at 1.0.
    """

    if not os.path.exists(pptx_path):
        print(f"✗ File not found: {pptx_path}")
        return 0.0

    try:
        with zipfile.ZipFile(pptx_path, "r") as zf:
            # Collect all slide XML files
            slide_files = [f for f in zf.namelist()
                           if f.startswith("ppt/slides/slide") and f.endswith(".xml")]
            slide_files.sort()  # Ensure deterministic order (first slide first)

            # XML namespaces needed for xpath queries
            ns = {
                "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            }

            found_paragraph = False
            big_enough        = False  # whether size ratio criterion met

            # Iterate through slides (stop at first qualifying paragraph)
            for slide in slide_files:
                slide_xml = zf.read(slide)
                root = ET.fromstring(slide_xml)

                # All paragraphs in the slide
                paragraphs = root.xpath(".//a:p", namespaces=ns)
                for p in paragraphs:
                    # Runs directly under this paragraph (not nested hyperlinks, etc.)
                    runs = p.xpath("./a:r", namespaces=ns)
                    if len(runs) < 2:
                        continue  # Need at least two runs: drop-cap + rest

                    # --- Examine first & second run --------------------------------------------------
                    first_run_text = "".join(runs[0].xpath(".//a:t/text()", namespaces=ns)).strip()
                    second_run_text = "".join(runs[1].xpath(".//a:t/text()", namespaces=ns)).strip()

                    if len(first_run_text) != 1 or len(second_run_text) == 0:
                        continue  # Not a drop-cap pattern

                    # Font sizes are stored in EMUs * 100 (1/100 pt).  We need integer compare.
                    def run_font_size(run):
                        rPr = run.find("./a:rPr", namespaces=ns)
                        if rPr is not None and "sz" in rPr.attrib:
                            try:
                                return int(rPr.attrib["sz"])
                            except ValueError:
                                pass
                        return None

                    size_first = run_font_size(runs[0])
                    size_second = run_font_size(runs[1])

                    # Determine whether the first character is significantly larger
                    if size_first and size_second and size_first >= 1.5 * size_second:
                        big_enough = True

                    found_paragraph = True
                    # Stop after first qualifying paragraph (it should be the first)
                    break
                if found_paragraph:
                    break

            # ------------------------- Scoring -----------------------------------
            total_score = 0.0
            if found_paragraph:
                print("✓ Found paragraph with single-character first run (potential drop cap) (0.6 pts)")
                total_score += 0.6
            else:
                print("✗ No paragraph with a single-character first run found – no drop cap detected")
                return 0.0

            if big_enough:
                print("✓ First character font size ≥ 1.5× following text (visual enlargement) (0.4 pts)")
                total_score += 0.4
            else:
                print("✗ First character is not sufficiently larger than subsequent text – looks like drop cap not applied fully")

            final_score = min(total_score, 1.0)
            print(f"Total score: {final_score}")
            return final_score

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        return 0.0


# -----------------------------------------------------------------------------
# Execute verification when run as a script
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    PPTX_PATH = "/home/user/apply_drop_caps_to_the_first_paragraph_1_character_over_2_lines.pptx"
    reward = verify_drop_cap_task(PPTX_PATH)
    print(f"REWARD: {reward}")
