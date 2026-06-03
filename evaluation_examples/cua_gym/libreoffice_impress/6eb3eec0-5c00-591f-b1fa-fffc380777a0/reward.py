"""
FINAL REWARD SCRIPT - SUCCESS
Task: Justify paragraphs 2–4 and set hyphenation on for them.
Generated: 2025-10-17 17:33:33
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET


def verify_task(file_path: str) -> float:
    """Verify that paragraphs 2–4 in the presentation are
    (1) justified and (2) have hyphenation enabled.

    Returns a progressive score between 0.0 and 1.0.
    """

    print(f"Starting verification for: {file_path}")

    # Basic existence / type checks (no points awarded here)
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0
    if not file_path.lower().endswith('.pptx'):
        print("✗ File is not a PPTX")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as pptx_zip:
            # Collect slide XML files (e.g. ppt/slides/slide1.xml …)
            slide_files = [
                f for f in pptx_zip.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", f)
            ]
            if not slide_files:
                print("✗ No slide XML files found – invalid PPTX structure")
                return 0.0

            # Sort slides by numeric order to preserve reading order
            slide_files.sort(key=lambda f: int(re.search(r'slide(\d+)', f).group(1)))

            # Gather every <a:p> (paragraph) element across all slides
            ns = {
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
            }
            paragraphs = []
            for slide in slide_files:
                xml_bytes = pptx_zip.read(slide)
                root = ET.fromstring(xml_bytes)
                paragraphs.extend(root.findall('.//a:p', ns))

            total_paragraphs = len(paragraphs)
            print(f"Total paragraphs detected: {total_paragraphs}")
            if total_paragraphs < 4:
                print("✗ Presentation contains fewer than 4 paragraphs – cannot verify paragraphs 2–4")
                return 0.0

            # Helper functions ------------------------------------------------
            def para_props(p_elem):
                return p_elem.find('./a:pPr', ns)

            def is_justified(ppr):
                if ppr is None:
                    return False
                for attr, val in ppr.attrib.items():
                    if attr.endswith('algn') and val.startswith('just'):
                        return True
                return False

            def has_hyphenation(ppr):
                if ppr is None:
                    return False
                for attr, val in ppr.attrib.items():
                    if attr.endswith('hyphenation') and val.lower() in {'true', '1', 'yes'}:
                        return True
                return False
            # ------------------------------------------------------------------

            target_indices = [1, 2, 3]  # zero-based indices for paragraphs 2–4
            points_each = 1.0 / len(target_indices)
            score = 0.0

            for idx in target_indices:
                p_elem = paragraphs[idx]
                ppr = para_props(p_elem)
                justified = is_justified(ppr)
                hyphenated = has_hyphenation(ppr)
                print(f"Paragraph {idx + 1}: justified={justified}, hyphenation={hyphenated}")
                if justified and hyphenated:
                    score += points_each

            final_score = round(min(score, 1.0), 2)
            print(f"Computed score: {final_score}")
            return final_score

    except Exception as e:
        print("✗ Exception during verification:")
        import traceback
        traceback.print_exc()
        return 0.0


if __name__ == '__main__':
    # Path to the file to be checked in the evaluation environment
    FILE_PATH = '/home/user/justify_paragraphs_24_and_set_hyphenation_on_for_them.pptx'
    reward = verify_task(FILE_PATH)
    print(f"REWARD: {reward}")

