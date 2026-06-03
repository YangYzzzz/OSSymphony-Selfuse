"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m polishing up a quick-start guide and have to keep it screen-reader friendly. For the flowchart image I just dropped on page 2, where do I plug in the alt-text so it reads exactly "Workflow overview" in LibreOffice Writer?
Generated: 2025-09-10 19:35:36
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

"""
Reward Script: Verify that the flowchart image in the provided DOCX file
has alternative text set exactly to "Workflow overview".
Progressive scoring:
  • 0.4 points – At least one image/drawing object contains ANY alt-text (accessibility step)
  • 0.6 points – An image/drawing object’s alt-text (descr or title) matches exactly
                 "Workflow overview" (case sensitive, per instructions)
Total score = 1.0 only when both conditions are satisfied.
"""

EXPECTED_ALT = "Workflow overview"
FILE_PATH = "/home/user/im_polishing_up_a_quick_start_guide_and_have_to_keep_it_screen_reader_friendly_for_the_flowchart_ima.docx"


def extract_docpr_alt_attributes(docx_path):
    """Return a list of (descr, title) tuples for every wp:docPr element inside the DOCX file."""
    with zipfile.ZipFile(docx_path) as zf:
        document_xml = zf.read("word/document.xml")

    # Parse XML and extract wp:docPr elements – they store alt-text in 'descr' or 'title'
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    }
    root = etree.fromstring(document_xml)

    alt_pairs = []
    for docpr in root.xpath("//wp:docPr", namespaces=ns):
        descr = docpr.get("descr") or ""
        title = docpr.get("title") or ""
        alt_pairs.append((descr, title))
    return alt_pairs


def verify_alt_text(file_path: str, expected_alt: str) -> float:
    print(f"Starting verification for file: {file_path}")
    total_score = 0.0

    # Preliminary: file must exist (no points for existence, but fail gracefully if missing)
    if not os.path.isfile(file_path):
        print("✗ File not found. Task incomplete.")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to extract alt-text information
    try:
        alt_pairs = extract_docpr_alt_attributes(file_path)
        print(f"Found {len(alt_pairs)} image/drawing element(s) in document.")
    except Exception as e:
        print(f"✗ Error while parsing DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Requirement 1: At least one image has SOME alt-text (descr or title not empty)
    images_with_any_alt = [(d, t) for d, t in alt_pairs if d or t]
    if images_with_any_alt:
        total_score += 0.4
        print("✓ Detected image(s) with alternative text (0.4 points)")
    else:
        print("✗ No alternative text detected on any image (0 points)")

    # Requirement 2: An image’s alt-text matches expected string exactly
    correct_alt_present = any(d == expected_alt or t == expected_alt for d, t in alt_pairs)
    if correct_alt_present:
        total_score += 0.6  # brings total to 1.0 when both requirements met
        print(f"✓ Image found with alt-text exactly '{expected_alt}' (0.6 points)")
    else:
        print(f"✗ No image found with alt-text exactly '{expected_alt}' (0 points)")

    # Cap score at 1.0 and round for cleanliness
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when script runs
if __name__ == "__main__":
    verify_alt_text(FILE_PATH, EXPECTED_ALT)

