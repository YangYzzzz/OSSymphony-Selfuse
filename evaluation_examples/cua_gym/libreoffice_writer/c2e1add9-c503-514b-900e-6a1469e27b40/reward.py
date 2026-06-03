"""
FINAL REWARD SCRIPT - SUCCESS
Task: Paragraphs 2 and 3 in my LibreOffice Writer file are way too tight. How can I set just those two paragraphs to an ‘Exactly 18 pt’ line spacing so they look less cramped?
Generated: 2025-09-10 13:32:06
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
import xml.etree.ElementTree as ET


def verify_exact_line_spacing(file_path: str) -> float:
    """Verify that ONLY paragraphs 2 and 3 have an ‘Exactly 18 pt’ (360 twips) line spacing.

    Scoring (progressive, max 1.0):
        • 0.3 – Paragraph 2 has Exactly 18 pt spacing
        • 0.3 – Paragraph 3 has Exactly 18 pt spacing
        • 0.4 – No OTHER paragraph has Exactly 18 pt spacing
    """

    print(f"Verifying document: {file_path}\n")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0  # task failed – prerequisite missing

    try:
        # --------------------------------------------------------------
        # Extract paragraph spacing information directly from document.xml
        # --------------------------------------------------------------
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        with zipfile.ZipFile(file_path) as z:
            doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)

        spacing_info = []  # [(rule, line_value_twips) per paragraph]
        for p in root.findall(".//w:body/w:p", ns):
            spacing = p.find("./w:pPr/w:spacing", ns)
            if spacing is not None:
                rule = spacing.get(f"{{{ns['w']}}}lineRule")  # e.g., "exact"
                line_val = spacing.get(f"{{{ns['w']}}}line")  # value in twips
                line_val = int(line_val) if line_val is not None else None
            else:
                rule, line_val = None, None
            spacing_info.append((rule, line_val))

        print(f"✓ Found {len(spacing_info)} paragraphs in document")

        # --------------------------------------------------------------
        # Progressive scoring based on real checks (no bias!)
        # --------------------------------------------------------------
        score = 0.0
        max_score = 1.0

        # Requirement 1 – Paragraph 2 spacing
        if len(spacing_info) >= 2:
            p2_rule, p2_val = spacing_info[1]
            if p2_rule == "exact" and p2_val == 360:
                print("✓ Paragraph 2 has Exactly 18 pt line spacing (0.3)")
                score += 0.3
            else:
                print("✗ Paragraph 2 spacing incorrect (0 pts)")
        else:
            print("✗ Document too short – no Paragraph 2 (0 pts)")

        # Requirement 2 – Paragraph 3 spacing
        if len(spacing_info) >= 3:
            p3_rule, p3_val = spacing_info[2]
            if p3_rule == "exact" and p3_val == 360:
                print("✓ Paragraph 3 has Exactly 18 pt line spacing (0.3)")
                score += 0.3
            else:
                print("✗ Paragraph 3 spacing incorrect (0 pts)")
        else:
            print("✗ Document too short – no Paragraph 3 (0 pts)")

        # Requirement 3 – No other paragraphs use that spacing
        others_ok = True
        for idx, (rule, val) in enumerate(spacing_info):
            if idx in (1, 2):
                continue  # skip paragraphs 2 & 3
            if rule == "exact" and val == 360:
                print(f"✗ Paragraph {idx+1} also has Exactly 18 pt spacing (should not) – 0.4 pts lost")
                others_ok = False
                break
        if others_ok:
            print("✓ Only Paragraphs 2 & 3 have Exactly 18 pt spacing (0.4)")
            score += 0.4

        final_score = min(score, max_score)
        print(f"\nTotal score: {final_score} / {max_score}")
        return final_score

    except Exception as e:
        print(f"✗ Error verifying document: {e}")
        return 0.0


if __name__ == "__main__":
    # Path to the user's Writer (DOCX) file
    DOC_PATH = "/home/user/paragraphs_2_and_3_in_my_libreoffice_writer_file_are_way_too_tight_how_can_i_set_just_those_two_para.docx"

    reward = verify_exact_line_spacing(DOC_PATH)
    print(f"REWARD: {reward}")

