"""
Reward Script: Make bullet characters red (RGB 255,0,0) and 14pt while keeping text at 11pt
Task ID: writer_list_021
Domain: libreoffice_writer
Scoring:
  Component 1: All 5 bullet paragraph marks have red color (FF0000) in pPr/rPr  (0.5 pts)
  Component 2: All 5 bullet paragraph marks have 14pt font size (sz=28) in pPr/rPr  (0.5 pts)
  Total: 1.0

The key insight: In DOCX, bullet character formatting is stored in the paragraph mark run
properties (w:pPr/w:rPr). The task requires:
  - w:color w:val="FF0000" (or close red) in pPr/rPr for bullet color
  - w:sz w:val="28" (14pt = 28 half-points) in pPr/rPr for bullet size
  - Text runs must remain 11pt (w:sz w:val="22") black (verifying text is NOT changed)
"""

import os
import re

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_list_021'
FILE_PATH = f'{WORKDIR}/Desktop/highlights.docx'

# Expected bullet text content (the 5 items)
EXPECTED_TEXTS = [
    "Record-breaking Q3 revenue of $12.5M",
    "Customer satisfaction score increased to 94%",
    "Successfully launched mobile application",
    "Opened three new regional offices",
    "Employee retention rate above 92%",
]

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def get_ppr_rpr_color(para):
    """Extract the color value from pPr/rPr (paragraph mark formatting)."""
    pPr = para._element.find('.//w:pPr', NS)
    if pPr is None:
        return None
    rPr = pPr.find('w:rPr', NS)
    if rPr is None:
        return None
    color_el = rPr.find('w:color', NS)
    if color_el is None:
        return None
    return color_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')


def get_ppr_rpr_sz(para):
    """Extract the sz (font size in half-points) from pPr/rPr (paragraph mark formatting)."""
    pPr = para._element.find('.//w:pPr', NS)
    if pPr is None:
        return None
    rPr = pPr.find('w:rPr', NS)
    if rPr is None:
        return None
    sz_el = rPr.find('w:sz', NS)
    if sz_el is None:
        return None
    val = sz_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
    return int(val) if val is not None else None


def is_red_color(hex_val):
    """Check if the hex color value is red (FF0000 or close variants like FF0000)."""
    if hex_val is None:
        return False
    hex_val = hex_val.upper().strip('#')
    if len(hex_val) != 6:
        return False
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)
    # Accept red: r >= 200, g < 60, b < 60
    return r >= 200 and g < 60 and b < 60


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have 5 paragraphs (all bullet items)
    # Style name is 'List Bullet' (with space) in python-docx
    bullet_paras = [p for p in doc.paragraphs if p.style and 'List Bullet' in p.style.name]
    if len(bullet_paras) < 5:
        print(f"FAIL: Expected 5 bullet paragraphs, found {len(bullet_paras)}. File may be corrupted.")
        print("REWARD: 0.0")
        return 0.0

    # Verify the text content is correct (data integrity gate)
    para_texts = [p.text.strip() for p in bullet_paras[:5]]
    texts_match = all(t in ' '.join(para_texts) or any(t in pt for pt in para_texts) for t in EXPECTED_TEXTS)
    if not texts_match:
        print(f"WARN: Bullet text does not match expected. Found: {para_texts}")
        # Not a hard gate - still attempt scoring

    # Component 1: All 5 bullet paragraph marks have red color (FF0000) in pPr/rPr (0.5 pts)
    # This verifies that bullet CHARACTERS (not text) are colored red.
    # In DOCX: the paragraph mark rPr inside pPr controls bullet character formatting.
    try:
        red_count = 0
        red_details = []
        for i, para in enumerate(bullet_paras[:5]):
            color_val = get_ppr_rpr_color(para)
            if is_red_color(color_val):
                red_count += 1
                red_details.append(f"Para {i}: color={color_val} (red)")
            else:
                red_details.append(f"Para {i}: color={color_val} (NOT red)")

        comp1_pass = (red_count == 5)
        if comp1_pass:
            total_score += 0.5
            print(f"PASS: Component 1 — All 5 bullet paragraph marks have red color")
            for d in red_details:
                print(f"  {d}")
        else:
            print(f"FAIL: Component 1 — Only {red_count}/5 bullet paragraph marks have red color")
            for d in red_details:
                print(f"  {d}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 bullet paragraph marks have 14pt font size (sz=28) in pPr/rPr (0.5 pts)
    # This verifies that bullet CHARACTERS are sized at 14pt (28 half-points).
    # sz=28 because OOXML uses half-points: 14pt * 2 = 28.
    try:
        size_count = 0
        size_details = []
        for i, para in enumerate(bullet_paras[:5]):
            sz_val = get_ppr_rpr_sz(para)
            # Accept sz=28 (14pt). Allow tolerance: 27 or 29 as well.
            if sz_val is not None and abs(sz_val - 28) <= 1:
                size_count += 1
                size_details.append(f"Para {i}: sz={sz_val} ({sz_val/2}pt — correct 14pt)")
            else:
                size_details.append(f"Para {i}: sz={sz_val} ({sz_val/2 if sz_val else None}pt — NOT 14pt)")

        comp2_pass = (size_count == 5)
        if comp2_pass:
            total_score += 0.5
            print(f"PASS: Component 2 — All 5 bullet paragraph marks have 14pt font size")
            for d in size_details:
                print(f"  {d}")
        else:
            print(f"FAIL: Component 2 — Only {size_count}/5 bullet paragraph marks have 14pt size")
            for d in size_details:
                print(f"  {d}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Informational: verify text runs are still 11pt black (not part of score, just diagnostic)
    try:
        text_ok_count = 0
        for para in bullet_paras[:5]:
            for run in para.runs:
                if run.text.strip():
                    run_sz = run._element.find('.//w:rPr/w:sz', NS)
                    sz_val = int(run_sz.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')) if run_sz is not None else None
                    if sz_val is None or sz_val == 22:  # 22 half-pts = 11pt
                        text_ok_count += 1
        print(f"INFO: Text runs at 11pt: {text_ok_count}/5 (diagnostic only, not scored)")
    except Exception as e:
        print(f"INFO: Could not check text run sizes: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
