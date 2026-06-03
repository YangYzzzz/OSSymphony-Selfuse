"""
FINAL REWARD SCRIPT - SUCCESS
Task: I flagged a bunch of sentences in #FFFF00 highlight while editing a 30-page report in LibreOffice Writer. Now that the review is done, I want to wipe out every trace of that yellow in one sweep instead of removing it line by line. What’s the quickest way to clear all #FFFF00 highlighting across the entire document?
Generated: 2025-09-10 12:40:58
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree

def verify_clear_yellow_highlight(file_path: str) -> float:
    """Verify that every trace of #FFFF00 (yellow) highlighting has been removed from
    the entire document.

    Scoring rules (progressive):
        • 1.0 – No yellow highlight/shading elements remain
        • 0.5 – Fewer than 5 yellow occurrences remain (almost complete)
        • 0.2 – 5 or more yellow occurrences remain (minimal progress)
        • 0.0 – Verification error / file missing
    """
    print(f"Verifying yellow highlight removal in: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0  # No progress if the file itself is missing

    try:
        # -------------------------------------------------------------
        # 1. Extract document.xml from the DOCX package for inspection
        # -------------------------------------------------------------
        with zipfile.ZipFile(file_path) as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml not found inside DOCX – invalid file structure")
                print("REWARD: 0.0")
                return 0.0
            document_xml = z.read("word/document.xml")

        # -------------------------------------------------------------
        # 2. Parse XML and locate all highlight & shading nodes
        # -------------------------------------------------------------
        root = etree.fromstring(document_xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        highlight_nodes = root.xpath("//w:highlight", namespaces=ns)
        shading_nodes   = root.xpath("//w:shd",        namespaces=ns)

        print(f"Total <w:highlight> tags found: {len(highlight_nodes)}")
        print(f"Total <w:shd>        tags found: {len(shading_nodes)}")

        # -------------------------------------------------------------
        # 3. Count the occurrences that represent *yellow* specifically
        # -------------------------------------------------------------
        yellow_occurrences = 0
        yellow_keywords = {"yellow", "ffff00", "#ffff00"}

        # w:highlight nodes use the attribute w:val
        for h in highlight_nodes:
            val = h.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
            if val and val.lower() in yellow_keywords:
                yellow_occurrences += 1

        # w:shd (shading) nodes use the attribute w:fill
        for shd in shading_nodes:
            fill = shd.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill")
            if fill and fill.lower() in yellow_keywords:
                yellow_occurrences += 1

        print(f"Yellow highlight/shading occurrences detected: {yellow_occurrences}")

        # -------------------------------------------------------------
        # 4. Progressive scoring based on remaining yellow highlights
        # -------------------------------------------------------------
        if yellow_occurrences == 0:
            score = 1.0
            print("✓ No yellow highlights remain – task fully completed (1.0)")
        elif yellow_occurrences < 5:
            score = 0.5
            print("• Only a few yellow highlights remain – partial completion (0.5)")
        else:
            score = 0.2
            print("✗ Many yellow highlights remain – minimal completion (0.2)")

    except Exception as e:
        # Any parsing/extraction error yields 0.0 (task verification failed)
        print(f"✗ Error during verification: {e}")
        score = 0.0

    # Ensure the score is within [0.0, 1.0]
    score = max(0.0, min(score, 1.0))
    print(f"REWARD: {score}")
    return score

# ------------------------------------------------------------------
# When executed as a script, run verification on the expected file
# ------------------------------------------------------------------
if __name__ == "__main__":
    target_file = "/home/user/i_flagged_a_bunch_of_sentences_in_ffff00_highlight_while_editing_a_30_page_report_in_libreoffice_wri.docx"
    verify_clear_yellow_highlight(target_file)
