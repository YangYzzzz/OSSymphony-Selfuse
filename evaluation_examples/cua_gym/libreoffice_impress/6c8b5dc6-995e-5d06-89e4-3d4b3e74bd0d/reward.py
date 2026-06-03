"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert a bookmark named 'sec-methods' at Heading 2 'Methods'.
Generated: 2025-10-17 11:27:11
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import zipfile
from typing import List
import lxml.etree as ET


def verify_bookmark(file_path: str) -> float:
    """
    Verify that a bookmark (shape name) called 'sec-methods' exists on the
    same slide that contains the Heading 2 text 'Methods'. Progressive
    scoring is applied based on:
      1. Bookmark presence                    – 0.4 pts
      2. Heading-2 text 'Methods' found       – 0.3 pts
      3. Bookmark and heading on same slide  – 0.3 pts
    Returns a float in the range 0-1.
    """
    print(f"Verifying bookmark in: {file_path}")

    # Namespace map for PPTX XML
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }

    if not os.path.exists(file_path):
        print("✗ File does not exist.")
        return 0.0

    score = 0.0
    max_score = 1.0

    try:
        with zipfile.ZipFile(file_path) as z:
            # Collect slide XML paths
            slide_files: List[str] = sorted(
                f for f in z.namelist()
                if f.startswith("ppt/slides/slide") and f.endswith(".xml")
            )
            if not slide_files:
                print("✗ No slide XML files found in PPTX – corrupt or empty presentation")
                return 0.0

            bookmark_slides: List[int] = []  # slides containing the bookmark
            methods_slides: List[int] = []   # slides containing the heading text

            for slide_path in slide_files:
                slide_num_match = re.search(r"slide(\d+).xml", slide_path)
                if not slide_num_match:
                    continue  # Skip unexpected naming
                slide_idx = int(slide_num_match.group(1))

                xml_data = z.read(slide_path)
                root = ET.fromstring(xml_data)

                # --- Check for heading text 'Methods' (case-insensitive) ---
                text_elements = root.xpath(".//a:t", namespaces=ns)
                texts = [t.text for t in text_elements if t.text]
                if any(re.search(r"\bmethods\b", t, re.IGNORECASE) for t in texts):
                    methods_slides.append(slide_idx)

                # --- Check for bookmark shape named 'sec-methods' ---
                bookmark_shapes = root.xpath(
                    './/p:sp/p:nvSpPr/p:cNvPr[@name="sec-methods"]', namespaces=ns
                )
                if bookmark_shapes:
                    bookmark_slides.append(slide_idx)

            # ---------- Scoring ----------
            if bookmark_slides:
                print(f"✓ Found bookmark 'sec-methods' on slide(s): {sorted(bookmark_slides)}")
                score += 0.4
            else:
                print("✗ Bookmark 'sec-methods' not found in any slide")

            if methods_slides:
                print(f"✓ Found heading 'Methods' on slide(s): {sorted(methods_slides)}")
                score += 0.3
            else:
                print("✗ Heading text 'Methods' not found in presentation")

            overlap = set(bookmark_slides) & set(methods_slides)
            if overlap:
                print(f"✓ Bookmark resides on same slide(s) as heading: {sorted(overlap)}")
                score += 0.3
            elif bookmark_slides and methods_slides:
                print("✗ Bookmark and heading are on different slides")

            final_score = min(score, max_score)
            print(f"Total Score: {final_score}/{max_score}")
            return final_score

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0


if __name__ == "__main__":
    # Path provided by the task description
    FILE_PATH = "/home/user/insert_a_bookmark_named_sec_methods_at_heading_2_methods.pptx"

    reward = verify_bookmark(FILE_PATH)
    print(f"REWARD: {reward}")

