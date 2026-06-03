"""
FINAL REWARD SCRIPT - SUCCESS
Task: Make Heading 1 'Keep with next' and 'Do not split' enabled.
Generated: 2025-10-17 17:46:02
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import zipfile
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
# Reward Script : verify_heading_keep_with_next_and_do_not_split_enabled()
# -----------------------------------------------------------------------------
# Task to verify
# "Make Heading 1 'Keep with next' and 'Do not split' enabled."
# -----------------------------------------------------------------------------
# Scoring rubric (progressive):
#   0.2  – The presentation contains a paragraph whose text is "Heading 1"
#   0.4  – At least one paragraph in the file (ideally the Heading 1 para) has
#           the keepNext (<a:keepNext/>) property set  ➜  ‘Keep with next’
#   0.4  – At least one paragraph in the file has the keepLines
#           (<a:keepLines/>) property set  ➜  ‘Do not split’
# -----------------------------------------------------------------------------
# Maximum score 1.0.  All points only awarded when the corresponding XML elements
# are actually present – no natural-state points are given.
# -----------------------------------------------------------------------------

a_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'

A_P          = f'{{{a_ns}}}p'
A_PPR        = f'{{{a_ns}}}pPr'
A_T          = f'{{{a_ns}}}t'
A_KEEPNEXT   = f'{{{a_ns}}}keepNext'   # “Keep with next”
A_KEEPLINES  = f'{{{a_ns}}}keepLines'  # “Do not split” (keep lines together)

def verify_heading_keep_with_next_and_do_not_split_enabled(file_path: str) -> float:
    """Verify that the PPTX satisfies the Heading 1 keep-options requirements.

    Returns a float between 0.0 and 1.0.
    """

    print(f"Verifying presentation: {file_path}\n")

    max_score = 1.0
    score = 0.0

    # 1. Existence check (no points – prerequisite)
    if not os.path.exists(file_path):
        print("✗ File not found – verification failed")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as pptx_zip:
            # Collect slide XML files
            slide_files = [f for f in pptx_zip.namelist()
                           if f.startswith('ppt/slides/slide') and f.endswith('.xml')]

            if not slide_files:
                print("✗ No slide files located inside PPTX – cannot verify")
                return 0.0

            heading_found   = False  # "Heading 1" paragraph present?
            keepNext_found  = False  # any <a:keepNext/>
            keepLines_found = False  # any <a:keepLines/>

            for slide_file in slide_files:
                slide_xml = pptx_zip.read(slide_file)
                root = ET.fromstring(slide_xml)

                # Iterate over all paragraphs (<a:p>) in the slide
                for p in root.iter(A_P):
                    # Full paragraph text (concatenate all <a:t>)
                    texts = [t.text for t in p.findall('.//' + A_T) if t.text]
                    paragraph_text = ' '.join(texts).strip()

                    # Locate paragraph properties element
                    pPr = p.find(A_PPR)
                    if pPr is None:
                        continue

                    has_keepNext  = pPr.find(A_KEEPNEXT)  is not None
                    has_keepLines = pPr.find(A_KEEPLINES) is not None

                    # Aggregate findings
                    if has_keepNext:
                        keepNext_found = True
                    if has_keepLines:
                        keepLines_found = True
                    if paragraph_text.lower() == 'heading 1':
                        heading_found = True

            # Progressive scoring ------------------------------------------------
            if heading_found:
                score += 0.2
                print("✓ Found paragraph with text 'Heading 1' (0.2 points)")
            else:
                print("✗ No paragraph with text 'Heading 1' found (0 points)")

            if keepNext_found:
                score += 0.4
                print("✓ <a:keepNext/> present – 'Keep with next' enabled (0.4 points)")
            else:
                print("✗ Missing <a:keepNext/> – 'Keep with next' NOT enabled (0 points)")

            if keepLines_found:
                score += 0.4
                print("✓ <a:keepLines/> present – 'Do not split' enabled (0.4 points)")
            else:
                print("✗ Missing <a:keepLines/> – 'Do not split' NOT enabled (0 points)")

    except Exception as exc:
        print(f"✗ Error analysing PPTX: {exc}")
        return 0.0

    final = min(score, max_score)
    print(f"\nTotal Score: {final}/{max_score}")
    return final

# -----------------------------------------------------------------------------
# Execute verification when run as a script
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    TEST_FILE = "/home/user/make_heading_1_keep_with_next_and_do_not_split_enabled.pptx"
    reward = verify_heading_keep_with_next_and_do_not_split_enabled(TEST_FILE)
    print(f"REWARD: {reward}")

