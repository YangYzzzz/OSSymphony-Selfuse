"""
FINAL REWARD SCRIPT - SUCCESS
Task: The title on my first slide isn't fitting well into the frame. Is there an option to automatically adjust the font size so it fits perfectly within the text box?
Generated: 2025-08-07 12:15:41
Status: success
Model: o4-mini
Total Steps: 3
"""

import os, zipfile
from pptx import Presentation
from lxml import etree

def verify_autofit_option(file_path):
    """
    Verifies if the 'auto-fit' option is enabled for the title text box on the first slide of a PPTX file.
    Returns a progressive score up to 1.0.
    Scoring:
      - 0.2: File exists
      - 0.1: Presentation loads successfully
      - 0.7: Auto-fit element (normAutofit, autoFit, or spAutoFit) found under the first slide's title bodyPr
    """
    total_score = 0.0
    max_score = 1.0

    # Requirement 1: File existence (0.2)
    print(f"Verifying file existence: {file_path}")
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0
    print("✓ File exists (0.2)")
    total_score += 0.2

    # Requirement 2: Load presentation (0.1)
    try:
        prs = Presentation(file_path)
        print(f"✓ Presentation loaded with {len(prs.slides)} slides (0.1)")
        total_score += 0.1
    except Exception as e:
        print(f"✗ Error loading presentation: {e}")
        return min(total_score, max_score)

    # Requirement 3: Check for auto-fit option in first slide (0.7)
    try:
        with zipfile.ZipFile(file_path, 'r') as pptx_zip:
            xml_data = pptx_zip.read('ppt/slides/slide1.xml')
            root = etree.fromstring(xml_data)
            ns = {
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
            }
            # Look for auto-fit related elements under bodyPr
            xpath_expr = (
                "//p:sp//p:txBody/a:bodyPr/*[local-name() = 'autoFit' "
                "or local-name() = 'normAutofit' or local-name() = 'spAutoFit']"
            )
            autofit_elems = root.xpath(xpath_expr, namespaces=ns)
            if autofit_elems:
                for elem in autofit_elems:
                    print(f"✓ Found element for auto-fit: {elem.tag}")
                print("✓ Auto-fit option enabled (0.7)")
                total_score += 0.7
            else:
                print("✗ No auto-fit option element found (0.0)")
    except Exception as e:
        print(f"✗ Error reading slide XML: {e}")

    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}")
    return final_score

if __name__ == '__main__':
    # Path to the target presentation
    file_path = '/home/user/the_title_on_my_first_slide_isnt_fitting_well_into_the_frame_is_there_an_option_to_automatically_adj.pptx'
    score = verify_autofit_option(file_path)
    print(f"REWARD: {score}")
