"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 24 feels jam-packed right now. In LibreOffice Impress, could you bump the line spacing of Content Text Box 1 to exactly 18 pt so the bullets don’t sit on top of each other?
Generated: 2025-09-10 13:44:39
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
import math
import zipfile
from lxml import etree

def verify_task(file_path: str) -> float:
    """Verify that the line-spacing of *Content Text Box 1* on slide 24
    is exactly 18 pt and return a progressive score (0.0 – 1.0).
    The score equals the proportion of paragraphs that meet the 18 pt
    requirement. A perfect file therefore yields 1.0.
    """
    print(f"Verifying presentation for 18 pt line spacing on slide 24 …")

    # ------------------------------------------------------------------
    # 0. Preliminary checks
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found.")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 1. Locate slide 24 inside the pptx ZIP
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slide_paths = [p for p in pptx_zip.namelist()
                           if p.startswith("ppt/slides/slide") and p.endswith(".xml")]
            if len(slide_paths) < 24:
                print("✗ Presentation contains fewer than 24 slides.")
                print("REWARD: 0.0")
                return 0.0

            # Sort by numeric slide index to get the correct order
            slide_paths.sort(key=lambda p: int(re.search(r"slide(\d+).xml", p).group(1)))
            slide24_path = slide_paths[23]          # zero-indexed → slide 24
            print(f"✓ Located slide 24 XML: {slide24_path}")

            slide_xml_bytes = pptx_zip.read(slide24_path)
    except Exception as e:
        print(f"✗ Error while reading pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Parse slide XML and find *Content Text Box 1*
    # ------------------------------------------------------------------
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }
    try:
        root = etree.fromstring(slide_xml_bytes)

        target_shape = None
        # Iterate through all simple shapes (<p:sp>)
        for sp in root.findall(".//p:sp", namespaces=ns):
            cNvPr = sp.find("./p:nvSpPr/p:cNvPr", namespaces=ns)
            if cNvPr is not None and cNvPr.get("name") == "Content Text Box 1":
                target_shape = sp
                break

        if target_shape is None:
            print("✗ Could not find shape named 'Content Text Box 1' on slide 24.")
            print("REWARD: 0.0")
            return 0.0
        print("✓ Found 'Content Text Box 1'")

        # ------------------------------------------------------------------
        # 3. Check every paragraph's line spacing value
        # ------------------------------------------------------------------
        paragraphs = target_shape.findall(".//a:p", namespaces=ns)
        if not paragraphs:
            print("✗ No paragraphs found inside the target text box.")
            print("REWARD: 0.0")
            return 0.0

        correct_count = 0
        for p in paragraphs:
            lnspc = p.find("./a:pPr/a:lnSpc", namespaces=ns)
            pts_val = None
            if lnspc is not None:
                spcPts = lnspc.find("./a:spcPts", namespaces=ns)
                if spcPts is not None and "val" in spcPts.attrib:
                    # Value is stored in hundredths of a point → convert to pt
                    pts_val = int(spcPts.attrib["val"]) / 100.0

            if pts_val is not None and math.isclose(pts_val, 18.0, abs_tol=0.1):
                correct_count += 1
            else:
                print(f"  ✗ Paragraph line spacing is {pts_val} pt, expected 18 pt.")

        total_paragraphs = len(paragraphs)
        print(f"Paragraphs with correct spacing: {correct_count}/{total_paragraphs}")

        # ------------------------------------------------------------------
        # 4. Scoring — proportion of correctly spaced paragraphs
        # ------------------------------------------------------------------
        score = round(correct_count / total_paragraphs, 2)
        print(f"REWARD: {score}")
        return score

    except Exception as e:
        print(f"✗ Error during XML parsing: {e}")
        print("REWARD: 0.0")
        return 0.0

# ----------------------------------------------------------------------
# Execute verification when the script is run directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/slide_24_feels_jam_packed_right_now_in_libreoffice_impress_could_you_bump_the_line_spacing_of_conten_golden.pptx"
    verify_task(FILE_PATH)

