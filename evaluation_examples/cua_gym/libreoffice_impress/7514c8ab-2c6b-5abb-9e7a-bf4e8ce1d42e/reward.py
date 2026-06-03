"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert the document title field in the header, center-aligned.
Generated: 2025-10-17 16:58:46
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pptx import Presentation

# --------------------------- CONFIGURATION --------------------------- #
FILE_PATH = "/home/user/insert_the_document_title_field_in_the_header_center_aligned.pptx"

# XML namespaces used inside PPTX files
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
# -------------------------------------------------------------------- #


def _get_core_title(zipf):
    """Return the core-property document title (dc:title) or None if absent."""
    try:
        core_xml = zipf.read("docProps/core.xml")
        root = ET.fromstring(core_xml)
        ns = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
        }
        title_node = root.find("dc:title", ns)
        if title_node is not None and title_node.text:
            return title_node.text.strip()
    except Exception as e:
        print(f"✗ Unable to read core title: {e}")
    return None


def _inspect_slide(slide_root, doc_title, slide_height):
    """Inspect a slide XML tree and return booleans (found, centered, at_top)."""
    found = False
    centered = False
    at_top = False

    for sp in slide_root.findall(".//p:sp", NS):
        # Gather all text inside this shape
        text = "".join(t.text or "" for t in sp.findall(".//a:t", NS)).strip()
        if text != doc_title:
            continue

        # Found the document title text on this shape
        found = True

        # Alignment check
        pPr = sp.find(".//a:pPr", NS)
        if pPr is not None and pPr.get("algn") == "ctr":
            centered = True

        # Position (top-region) check
        off = sp.find("p:spPr/a:xfrm/a:off", NS)
        if off is not None and off.get("y"):
            try:
                y_val = int(off.get("y"))
                if y_val <= 0.2 * slide_height:  # within top 20 % of slide
                    at_top = True
            except ValueError:
                pass

        # Do NOT break – if multiple shapes contain the title we want to
        # allow any of them to satisfy each criterion.
    return found, centered, at_top


def verify_header_title_centered(file_path: str) -> float:
    """Verify that the document title appears in the header, centre-aligned.

    Scoring (progressive):
      • 0.40 × (slides containing the title ÷ total slides)
      • 0.30 × (slides where that text is centred ÷ total slides)
      • 0.30 × (slides where that text is in the top region ÷ total slides)
    A perfect result yields 1.0.
    """
    max_score = 1.0
    score = 0.0

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # Open presentation via python-pptx (for dimensions) and as Zip (for raw XML)
    try:
        prs = Presentation(file_path)
    except Exception as e:
        print(f"✗ Cannot open presentation: {e}")
        return 0.0

    try:
        zipf = zipfile.ZipFile(file_path, "r")
    except Exception as e:
        print(f"✗ Cannot open PPTX as zip: {e}")
        return 0.0

    # Core-property title (what the Title field should display)
    doc_title = _get_core_title(zipf)
    if not doc_title:
        print("✗ Document core title missing – cannot verify header field")
        return 0.0
    print(f"Document title detected: '{doc_title}'")

    slide_files = sorted(
        f for f in zipf.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml")
    )
    if not slide_files:
        print("✗ No slide XML files found in presentation")
        return 0.0

    total_slides = len(slide_files)
    slide_height = prs.slide_height  # EMU units

    slides_with_title = 0
    slides_centered = 0
    slides_at_top = 0

    # --- Inspect each slide --- #
    for sf in slide_files:
        root = ET.fromstring(zipf.read(sf))
        found, centered, at_top = _inspect_slide(root, doc_title, slide_height)
        if found:
            slides_with_title += 1
        if centered:
            slides_centered += 1
        if at_top:
            slides_at_top += 1

    # --- Progressive Scoring --- #
    if slides_with_title:
        presence_ratio = slides_with_title / total_slides
        score += 0.40 * presence_ratio
        print(
            f"✓ Title present on {slides_with_title}/{total_slides} slides (score {0.40 * presence_ratio:.2f})"
        )
    else:
        print("✗ Title not present on any slide – header missing")

    if slides_centered:
        center_ratio = slides_centered / total_slides
        score += 0.30 * center_ratio
        print(
            f"✓ Centre alignment verified on {slides_centered}/{total_slides} slides (score {0.30 * center_ratio:.2f})"
        )
    else:
        print("✗ Header text not centre-aligned on any slide")

    if slides_at_top:
        top_ratio = slides_at_top / total_slides
        score += 0.30 * top_ratio
        print(
            f"✓ Header located in top region on {slides_at_top}/{total_slides} slides (score {0.30 * top_ratio:.2f})"
        )
    else:
        print("✗ Header text not found in top region on any slide")

    final_score = round(min(score, max_score), 2)
    print(f"Total verification score: {final_score}/{max_score}")
    return final_score


# --------------------------- RUN VERIFICATION ------------------------ #
if __name__ == "__main__":
    reward = verify_header_title_centered(FILE_PATH)
    print(f"REWARD: {reward}")

