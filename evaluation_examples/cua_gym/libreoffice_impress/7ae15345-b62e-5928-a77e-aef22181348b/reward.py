"""
FINAL REWARD SCRIPT - SUCCESS
Task: Make the first three words of paragraph 1 left-aligned and the rest right-aligned using tab stops.
Generated: 2025-10-17 11:54:24
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
import re
from lxml import etree

"""
Reward verification script for the task:
"Make the first three words of paragraph 1 left-aligned and the rest right-aligned using tab stops."  
The script checks a provided PPTX file for:
 1. Presence of a tab character in the first paragraph (indicates use of a tab stop)
 2. A right-aligned tab stop defined in the paragraph properties
 3. Exactly three words before the tab and at least one word after it
Progressive scoring (adds up to 1.0):
 • 0.3 – Tab character found in paragraph text
 • 0.3 – Right-aligned tab stop (<a:tab algn="r">) present
 • 0.4 – Exactly three words before the tab, and ≥1 after
The script prints detailed diagnostics and the final score as
"REWARD: X.X".
"""

FILE_PATH = "/home/user/make_the_first_three_words_of_paragraph_1_left_aligned_and_the_rest_right_aligned_using_tab_stops.pptx"

# XML namespaces used inside PPTX slide files
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

def verify_task(file_path: str = FILE_PATH) -> float:
    """Return a progressive score between 0.0 and 1.0 verifying task completion."""
    total_score = 0.0
    max_score = 1.0

    # ---------- 0. File existence (no points, prerequisite) ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- 1. Read slide1.xml ----------
    try:
        with zipfile.ZipFile(file_path) as z:
            slide_path = "ppt/slides/slide1.xml"  # Paragraph 1 expected on first slide
            if slide_path not in z.namelist():
                print("✗ slide1.xml not present in PPTX")
                print("REWARD: 0.0")
                return 0.0
            slide_xml = z.read(slide_path)
    except Exception as e:
        print(f"✗ Error opening PPTX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- 2. Parse XML ----------
    root = etree.fromstring(slide_xml)

    # Locate first <a:p> (paragraph) with any text/tab content
    p_elems = root.xpath(".//a:p", namespaces=NS)
    if not p_elems:
        print("✗ No paragraph elements found on slide 1")
        print("REWARD: 0.0")
        return 0.0
    first_para = p_elems[0]

    # Gather combined text (tabs preserved) from <a:t> elements
    para_text = "".join(t.text for t in first_para.xpath(".//a:t", namespaces=NS) if t.text)

    # ---------- 3. Check for tab character ----------
    has_tab_char = "\t" in para_text
    if has_tab_char:
        total_score += 0.3
        print("✓ Found tab character in paragraph text (0.3 points)")
    else:
        print("✗ No tab character found in paragraph text (0 points)")

    # ---------- 4. Verify right-aligned tab stop definition ----------
    right_tab_present = False
    pPr = first_para.find(".//a:pPr", namespaces=NS)
    if pPr is not None:
        for tab in pPr.xpath(".//a:tab", namespaces=NS):
            if tab.get("algn") == "r":
                right_tab_present = True
                break
    if right_tab_present:
        total_score += 0.3
        print("✓ Right-aligned tab stop (<a:tab algn='r'>) present (0.3 points)")
    else:
        print("✗ Right-aligned tab stop not found (0 points)")

    # ---------- 5. Check word distribution (3 before, ≥1 after) ----------
    if has_tab_char:
        before_text, after_text = para_text.split("\t", 1)
        words_before = re.findall(r"[\w'-]+", before_text)
        words_after = re.findall(r"[\w'-]+", after_text)
        if len(words_before) == 3 and len(words_after) >= 1:
            total_score += 0.4
            print(f"✓ Word distribution correct: 3 before, {len(words_after)} after (0.4 points)")
        else:
            print(f"✗ Incorrect word distribution (before={len(words_before)}, after={len(words_after)}) (0 points)")

    # ---------- 6. Final score ----------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when run as script
if __name__ == "__main__":
    verify_task()

