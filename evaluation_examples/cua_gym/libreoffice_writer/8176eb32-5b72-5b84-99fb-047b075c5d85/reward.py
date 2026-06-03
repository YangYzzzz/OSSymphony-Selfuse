"""
FINAL REWARD SCRIPT - SUCCESS
Task: Remove any remaining text highlight so no words are still marked.
Generated: 2025-10-14 08:11:24
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

def verify_no_text_highlight(file_path: str) -> float:
    """
    Verify that a DOCX document contains no active text highlight.
    Scoring logic:
        - If there are no <w:highlight> tags at all → score 1.0 (perfect)
        - If highlight tags exist, score is the proportion of highlight tags
          that have been disabled (val="none") or have no active colour.
        - Any highlight tag whose val attribute is *missing* or set to a colour
          other than "none" counts as an active highlight and lowers the score.
    Returns a float between 0.0 and 1.0.
    """

    print(f"Verifying document for remaining text highlight: {file_path}")

    # Preliminary check – file must exist
    if not os.path.exists(file_path):
        print("✗ File not found – returning 0.0")
        return 0.0  # No credit if the file is missing

    try:
        # Open DOCX (a DOCX is a ZIP archive)
        with zipfile.ZipFile(file_path, 'r') as docx_zip:
            if 'word/document.xml' not in docx_zip.namelist():
                print("✗ document.xml not found inside DOCX – returning 0.0")
                return 0.0

            # Parse the main document XML
            xml_bytes = docx_zip.read('word/document.xml')
            root = etree.fromstring(xml_bytes)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Locate every <w:highlight> element in the document
            highlight_elements = root.xpath('.//w:rPr/w:highlight', namespaces=ns)
            total_highlight_tags = len(highlight_elements)

            # Determine which highlight tags are still *active*
            active_highlights = []
            for elem in highlight_elements:
                val = elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
                # “none” (or explicit empty) means highlight removed
                if val and val.lower() != 'none':
                    active_highlights.append(val)
                elif val == '' and len(elem.attrib) == 0:
                    # A <w:highlight/> with no attributes defaults to active yellow highlight
                    active_highlights.append('default')

            print(f"Total <w:highlight> tags: {total_highlight_tags}")
            print(f"Active highlights still present: {len(active_highlights)} – {active_highlights}")

            # Scoring
            if total_highlight_tags == 0:
                # Perfect – no highlight tags at all
                score = 1.0
            else:
                # Proportion of highlight tags that are disabled
                score = (total_highlight_tags - len(active_highlights)) / total_highlight_tags
                # Clamp to 0-1 range just in case
                score = max(0.0, min(1.0, score))

            print(f"Computed score: {score}")
            return score

    except Exception as e:
        print(f"✗ Error while inspecting DOCX: {e}")
        return 0.0  # Any error → no credit


if __name__ == "__main__":
    # Path provided by the task description
    DOCX_PATH = "/home/user/remove_any_remaining_text_highlight_so_no_words_are_still_marked.docx"

    reward = verify_no_text_highlight(DOCX_PATH)
    print(f"REWARD: {reward}")
