"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert the document title field centered in the header.
Generated: 2025-10-17 13:23:22
Status: success
Model: azure-o3
Total Steps: 14
"""

import os
import zipfile
from pptx import Presentation
from lxml import etree as ET


def verify_title_header_centered(file_path: str) -> float:
    """
    Verify that the PPTX contains the *document title* (core property) in a
    header shape and that the text is CENTER-aligned (algn="ctr").

    Scoring (progressive):
        0.5 – A header/master/layout shape contains the core title text
        0.5 – That text paragraph has algn="ctr" (i.e., centred)
        1.0 – Both conditions satisfied
    """

    print(f"Verifying document title field centered in header for: {file_path}")

    max_score = 1.0
    score = 0.0

    # --- Basic file check ---------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        return 0.0

    # --- Read core document properties -------------------------------------
    try:
        prs = Presentation(file_path)
        doc_title = (prs.core_properties.title or '').strip()
        if not doc_title:
            print("✗ Core document title property is empty – cannot match title field")
            return 0.0
        print(f"✓ Core document title found: '{doc_title}'")
    except Exception as e:
        print(f"✗ Unable to load presentation with python-pptx: {e}")
        return 0.0

    # --- Search masters/layouts for a shape containing that title ----------
    try:
        with zipfile.ZipFile(file_path) as z:
            xml_files = [n for n in z.namelist()
                         if n.startswith(('ppt/slideMasters/', 'ppt/slideLayouts/')) and n.endswith('.xml')]

            found_shape = False
            centered = False

            ns = {
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
            }

            for xml_name in xml_files:
                xml_bytes = z.read(xml_name)
                # quick text filter before parsing
                if doc_title.encode() not in xml_bytes:
                    continue

                root = ET.fromstring(xml_bytes)
                for sp in root.xpath('.//p:sp', namespaces=ns):
                    texts = [t.text for t in sp.xpath('.//a:t', namespaces=ns) if t.text]
                    if not texts:
                        continue
                    full_text = ' '.join(texts).strip()
                    if doc_title not in full_text:
                        continue  # not our title

                    # --- Requirement 1 satisfied ---------------------------------
                    found_shape = True
                    print(f"✓ Found shape with title text in '{xml_name}'")

                    # Check paragraph alignment for centred text
                    pPr = sp.find('.//a:p/a:pPr', namespaces=ns)
                    if pPr is not None and pPr.get('algn') == 'ctr':
                        centered = True
                        print("✓ Text alignment attribute algn='ctr' found (centred)")
                    else:
                        print("✗ Title text not centred (algn!='ctr')")
                    break  # stop after first matching shape
                if found_shape:
                    break

            # --- Scoring ------------------------------------------------------
            if found_shape:
                score += 0.5
                print("✓ Requirement: Header shape containing document title present (0.5 points)")
                if centered:
                    score += 0.5
                    print("✓ Requirement: Title text centred (0.5 points)")
                else:
                    print("✗ Alignment requirement failed (0 points)")
            else:
                print("✗ No header shape containing the document title was found (0 points)")

    except Exception as e:
        print(f"✗ Error while parsing PPTX XML structure: {e}")
        return 0.0

    final_score = min(score, max_score)
    print(f"Total Score: {final_score}")
    return final_score


# ---------------------------------------------------------------------------
# Execute verification when script is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/insert_the_document_title_field_centered_in_the_header.pptx"
    reward_value = verify_title_header_centered(FILE_PATH)
    print(f"REWARD: {reward_value}")
