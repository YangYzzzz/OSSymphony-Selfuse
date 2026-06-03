"""
FINAL REWARD SCRIPT - SUCCESS
Task: For Heading 1, set spacing below to 12 pt and enable 'Keep with next'.
Generated: 2025-10-17 11:37:48
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
import xml.etree.ElementTree as ET


def verify_heading1_spacing_keep(file_path: str) -> float:
    """Verify that every paragraph whose text equals 'Heading 1' (case-insensitive)
    satisfies BOTH of the following formatting requirements:
        1.   Space After (spacing below) is exactly 12 pt  -> stored as 1200 in pptx XML
        2.   The paragraph has the keepNext="1" attribute  -> LibreOffice ‘Keep with next’

    Scoring (progressive):
        • 0.5 points for correct spacing setting on each Heading 1 paragraph
        • 0.5 points for having keepNext="1" on each Heading 1 paragraph
      The final score is the average across all Heading 1 paragraphs, capped at 1.0.
    """

    # XML namespaces used in PPTX drawingml / presentationml
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    heading_count = 0        # total Heading 1 paragraphs discovered
    correct_spacing = 0      # how many have 12-pt spacing below
    correct_keep = 0         # how many have keepNext="1"

    try:
        with zipfile.ZipFile(file_path) as z:
            # Collect all slide XML files
            slide_files = [name for name in z.namelist()
                           if name.startswith('ppt/slides/slide') and name.endswith('.xml')]

            for slide_name in slide_files:
                slide_xml = z.read(slide_name)
                root = ET.fromstring(slide_xml)

                # Iterate over every paragraph element
                for p in root.findall('.//a:p', ns):
                    # Concatenate all text runs inside this paragraph
                    para_text = ''.join(t.text or '' for t in p.findall('.//a:t', ns)).strip()

                    if para_text.lower() == 'heading 1':
                        heading_count += 1
                        pPr = p.find('a:pPr', ns)
                        if pPr is not None:
                            # 1) Verify Keep-with-next
                            if pPr.get('keepNext') == '1':
                                correct_keep += 1

                            # 2) Verify 12-pt space below (1200 = 12 * 100  in EMUs)
                            spcAft = pPr.find('a:spcAft', ns)
                            if spcAft is not None:
                                spcPts = spcAft.find('a:spcPts', ns)
                                if spcPts is not None:
                                    val_attr = spcPts.get('val')
                                    if val_attr is not None:
                                        try:
                                            if int(val_attr) == 1200:
                                                correct_spacing += 1
                                        except ValueError:
                                            pass  # If value isn't an int, treat as incorrect

        # If no Heading 1 paragraphs were found, task not completed
        if heading_count == 0:
            print('✗ No "Heading 1" paragraphs found in the presentation.')
            return 0.0

        # Progressive scoring: each condition worth 0.5 per paragraph
        spacing_score = (correct_spacing / heading_count) * 0.5
        keep_score = (correct_keep / heading_count) * 0.5
        total_score = spacing_score + keep_score

        # Debugging output
        print(f"Heading 1 paragraphs found: {heading_count}")
        print(f"✓ Correct spacing (12 pt)       : {correct_spacing}/{heading_count}")
        print(f"✓ Keep with next enabled       : {correct_keep}/{heading_count}")
        print(f"Computed score                : {total_score}")

        return min(total_score, 1.0)

    except Exception as e:
        print(f"✗ Error while verifying presentation: {e}")
        return 0.0


if __name__ == '__main__':
    # Path where the grader expects the participant's file to be located
    FILE_PATH = '/home/user/for_heading_1_set_spacing_below_to_12_pt_and_enable_keep_with_next.pptx'

    reward = verify_heading1_spacing_keep(FILE_PATH)
    print(f"REWARD: {reward}")
