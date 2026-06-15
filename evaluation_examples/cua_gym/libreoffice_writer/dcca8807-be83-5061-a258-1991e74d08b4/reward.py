"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps centering my page numbers and kicks them off with a “0.” I need them to read “1, 2, 3…” in the header’s top-right corner instead. What exact steps should I follow so the numbering starts at 1 and stays right-aligned in the header on every page?
Generated: 2025-09-10 13:27:29
Status: success
Model: azure-o3
Total Steps: 14
"""

# Reward Script for LibreOffice Page Numbering Task
# 
# Verifies that the user has:
#   1) Inserted a PAGE field into every header part of the DOCX
#   2) Set numbering to start at 1 (not 0)
#   3) Added at least one right-aligned paragraph in every header (to
#      encourage – and in the golden file confirm – right-hand placement)
#
# Progressive scoring (adds up to max 1.0):
#   • 0.5  – PAGE field present in ALL header parts
#   • 0.3  – Page-numbering sequence starts at 1
#   • 0.2  – Every header contains at least one right-aligned paragraph
#
# NO points are awarded for natural conditions such as file existence or
# successful loading – those are prerequisites, not achievements.

import os
import zipfile
from lxml import etree

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def _list_header_parts(zipf):
    """Return a list of header XML part names inside the DOCX archive."""
    return [p for p in zipf.namelist() if p.startswith('word/header') and p.endswith('.xml')]

def _paragraph_is_right_aligned(p):
    """Check <w:p> element for right (or RTL *end*) alignment."""
    jc = p.find('./w:pPr/w:jc', NS)
    if jc is not None:
        val = jc.get(f'{{{W_NS}}}val') or jc.get('val')
        if val in ('right', 'end'):
            return True
    return False

def _paragraph_has_page_field(p):
    """Detect PAGE field in <w:p> (handles simple & complex fields)."""
    # Simple field representation
    for fld in p.findall('.//w:fldSimple', NS):
        instr = (
            fld.get(f'{{{W_NS}}}instr')
            or fld.get('instr')
            or fld.get('w:instr')
        )
        if instr and 'PAGE' in instr.upper():
            return True
    # Complex field: look for <w:instrText> fragments
    for instr in p.findall('.//w:instrText', NS):
        if instr.text and 'PAGE' in instr.text.upper():
            return True
    return False

def _all_headers_have_page_field(zipf, header_parts):
    """True if EVERY header part contains at least one PAGE field."""
    for part in header_parts:
        root = etree.fromstring(zipf.read(part))
        if not any(_paragraph_has_page_field(p) for p in root.findall('.//w:p', NS)):
            print(f"✗ Header '{part}' is missing a PAGE field")
            return False
    return True

def _headers_have_right_alignment(zipf, header_parts):
    """True if every header part has at least ONE right-aligned paragraph."""
    for part in header_parts:
        root = etree.fromstring(zipf.read(part))
        if not any(_paragraph_is_right_aligned(p) for p in root.findall('.//w:p', NS)):
            print(f"✗ Header '{part}' has no right-aligned paragraph")
            return False
    return True

def _numbering_starts_at_one(zipf):
    """Check that page numbering (pgNumType/@w:start) equals 1 everywhere."""
    root = etree.fromstring(zipf.read('word/document.xml'))
    for pg in root.xpath('//w:sectPr/w:pgNumType', namespaces=NS):
        start_val = pg.get(f'{{{W_NS}}}start')
        if start_val and start_val != '1':
            print(f"✗ Found pgNumType start='{start_val}' (expected 1)")
            return False
    # If attribute absent, default is 1 – acceptable
    return True

# ----------------------------------------------------------------------
# Main verification function
# ----------------------------------------------------------------------

def verify_page_numbering_task(file_path: str) -> float:
    """Return a progressive reward score [0.0 – 1.0] for the task."""
    max_score = 1.0
    score = 0.0

    print(f"Verifying document: {file_path}")

    # Prerequisite checks (NO points awarded here!)
    if not os.path.exists(file_path):
        print("✗ File not found – task failed")
        print("REWARD: 0.0")
        return 0.0
    try:
        zipf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"✗ Unable to open DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    header_parts = _list_header_parts(zipf)
    if not header_parts:
        print("✗ No header parts found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Requirement 1 – PAGE field present in ALL headers (0.5)
    # ------------------------------------------------------------------
    if _all_headers_have_page_field(zipf, header_parts):
        score += 0.5
        print("✓ PAGE field present in every header (0.5)")
    else:
        print("✗ Missing PAGE field – 0 points for this requirement")

    # ------------------------------------------------------------------
    # Requirement 2 – Numbering starts at 1 (0.3)
    # ------------------------------------------------------------------
    try:
        if _numbering_starts_at_one(zipf):
            score += 0.3
            print("✓ Page numbering starts at 1 (0.3)")
        else:
            print("✗ Page numbering start incorrect – 0 points for this requirement")
    except KeyError:
        print("✗ word/document.xml missing – cannot verify numbering start")

    # ------------------------------------------------------------------
    # Requirement 3 – Right-aligned header content (0.2)
    # ------------------------------------------------------------------
    if _headers_have_right_alignment(zipf, header_parts):
        score += 0.2
        print("✓ Right-aligned paragraph found in every header (0.2)")
    else:
        print("✗ Headers lack right-aligned paragraph – 0 points for this requirement")

    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ----------------------------------------------------------------------
# Execute verification when run as a script
# ----------------------------------------------------------------------
if __name__ == "__main__":
    DOC_PATH = (
        "/home/user/"
        "libreoffice_keeps_centering_my_page_numbers_and_kicks_them_off_with_a_0_i_need_them_to_read_1_2_3_in.docx"
    )
    verify_page_numbering_task(DOC_PATH)

