"""
FINAL REWARD SCRIPT - SUCCESS
Task: The page numbers on my deck are blending into a dark background. How can I format every slide number so they display in bright red (#FF0000) on every slide in LibreOffice Impress?
Generated: 2025-09-10 13:22:36
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import re
import zipfile
from lxml import etree

# -------------------------------------------------------------
# Reward Script : verify_red_slide_numbers
# -------------------------------------------------------------
# Task description
# "Format every slide number so they display in bright red (#FF0000) on every slide in LibreOffice Impress"
# -------------------------------------------------------------
# Verification strategy
# 1. Open the PPTX file as a zip-archive (the .pptx format is a zip container)
# 2. Iterate over every slide XML (ppt/slides/slide*.xml)
# 3. For each slide, look through **every run (a:r)** for a solid-fill
#    colour value of FF0000 **and** text that represents a slide number
#    (digit or common placeholder symbol).  
# 4. Count how many slides have at least one such run.  
# 5. Score = (slides_with_red_numbers / total_slides) so the score is
#    progressive and reaches exactly 1.0 only when **all** slides pass.  
# -------------------------------------------------------------

HEX_RED = "FF0000"
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def is_slide_number_text(text: str) -> bool:
    """Return True if *text* plausibly represents a slide-number placeholder."""
    if not text:
        return False
    text = text.strip()
    # Regular digit (e.g., "1", "2", …)
    if text.isdigit():
        return True
    # LibreOffice placeholder glyphs such as "‹#›" (U+2039, U+203A wrappers)
    placeholder_variants = {"‹#›", "<#>", "#"}
    return text in placeholder_variants


def verify_red_slide_numbers(file_path: str) -> float:
    """Return a reward score [0.0-1.0] based on bright-red slide numbers."""

    print(f"Verifying bright-red slide numbers in: {file_path}")

    # PRECONDITION: File must exist – 0 points if not found
    if not os.path.exists(file_path):
        print("✗ File not found – task failed")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, "r") as z:
            slide_files = [
                name for name in z.namelist()
                if name.startswith("ppt/slides/slide") and name.endswith(".xml")
            ]
            slide_files.sort(key=lambda n: int(re.findall(r"slide(\d+)", n)[0]))

            if not slide_files:
                print("✗ No slide XML files present – invalid presentation")
                return 0.0

            total_slides = len(slide_files)
            slides_with_red = 0

            for idx, slide_xml_name in enumerate(slide_files, start=1):
                xml_bytes = z.read(slide_xml_name)
                root = etree.fromstring(xml_bytes)

                red_found = False
                # Iterate over every run element <a:r>
                for run in root.xpath(".//a:r", namespaces=NS):
                    # Find colour setting on the run
                    color_elems = run.xpath(
                        "./a:rPr/a:solidFill/a:srgbClr", namespaces=NS
                    )
                    if not color_elems:
                        continue

                    colour_val = color_elems[0].get("val", "").upper()
                    if colour_val != HEX_RED:
                        continue  # Colour is not bright red

                    # Grab the run's text to be sure it's the slide number
                    text_elem = run.find("./a:t", namespaces=NS)
                    text = text_elem.text if text_elem is not None else ""

                    if is_slide_number_text(text):
                        red_found = True
                        break  # No need to keep searching this slide

                print(
                    f"Slide {idx}: {'✓ bright-red number' if red_found else '✗ not red or missing'}"
                )
                if red_found:
                    slides_with_red += 1

            # Progressive scoring – proportion of slides that comply
            score = slides_with_red / total_slides
            print(
                f"Bright-red slide numbers found on {slides_with_red}/{total_slides} slides"
            )
            print(f"REWARD: {score}")
            return score

    except Exception as exc:
        print(f"✗ Error while verifying presentation: {exc}")
        return 0.0


# -------------------------------------------------------------
# MAIN EXECUTION (path is provided in the task context)
# -------------------------------------------------------------
if __name__ == "__main__":
    PRESENTATION_PATH = (
        "/home/user/"
        "the_page_numbers_on_my_deck_are_blending_into_a_dark_background_"
        "how_can_i_format_every_slide_number__golden.pptx"
    )
    verify_red_slide_numbers(PRESENTATION_PATH)

