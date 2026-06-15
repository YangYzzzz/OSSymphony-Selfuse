"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert a blank page immediately after the current page.
Generated: 2025-10-14 08:09:25
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import zipfile
from lxml import etree

################################################################################################
# Reward Script: Verify that a blank page was inserted immediately after the current page
# Task Definition (from user instructions):
#   "Insert a blank page immediately after the current page."
# Verification strategy:
#   1. Open the DOCX file as a zip archive and parse `word/document.xml`.
#   2. Locate the FIRST manual page break element (<w:br w:type="page"/>).
#   3. Inspect all subsequent elements up to the next page-break (or end of document).
#      • If no non-empty text runs (<w:t> with non-whitespace text) are found in this range,
#        we infer that the page after the break is blank.
#   4. Scoring (progressive):
#      • 0.5 points for detecting at least one page break (evidence a page was inserted).
#      • Additional 0.5 points if the page immediately following the first break contains
#        no textual content (confirming it is blank).
#      • Total score is capped at 1.0.
#   5. Print detailed diagnostics and final reward as "REWARD: X.X".
################################################################################################

def verify_blank_page_after_current(file_path: str) -> float:
    print(f"Verifying document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0  # No progress if file missing

    try:
        # ----- Load document.xml from DOCX -----
        with zipfile.ZipFile(file_path, "r") as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml not found inside DOCX")
                return 0.0
            doc_xml = z.read("word/document.xml")

        # Parse XML
        root = etree.fromstring(doc_xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        # Flatten elements in document order to inspect sequence easily
        all_elems = list(root.iter())

        # Identify manual page breaks: <w:br w:type="page"/>
        page_break_indices = [idx for idx, el in enumerate(all_elems)
                              if el.tag == f"{{{ns['w']}}}br" and el.get(f"{{{ns['w']}}}type") == "page"]
        print(f"Found {len(page_break_indices)} page break(s)")

        if not page_break_indices:
            print("✗ No manual page break found – blank page likely not inserted")
            return 0.0  # Task not completed

        # --- Partial credit for having at least one page break ---
        score = 0.5

        # Analyse the region between first and second page break (or end of doc)
        first_break_idx = page_break_indices[0]
        next_break_idx = page_break_indices[1] if len(page_break_indices) > 1 else len(all_elems)

        # Flag to detect any non-empty text within that range
        non_empty_text_found = False
        for el in all_elems[first_break_idx + 1: next_break_idx]:
            if el.tag == f"{{{ns['w']}}}t":  # text run
                text_content = (el.text or "").strip()
                if text_content:
                    non_empty_text_found = True
                    print(f"Non-empty text found after first page break: '{text_content[:40]}…'")
                    break

        if non_empty_text_found:
            print("✗ Text detected after first page break – page is not blank")
        else:
            print("✓ No text found between page breaks – blank page confirmed")
            score += 0.5  # Full credit for a truly blank page

        final_score = min(score, 1.0)
        print(f"Final Score: {final_score}")
        return final_score

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0  # Robust failure handling


if __name__ == "__main__":
    FILE_PATH = "/home/user/insert_a_blank_page_immediately_after_the_current_page.docx"
    reward = verify_blank_page_after_current(FILE_PATH)
    print(f"REWARD: {reward}")

