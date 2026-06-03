"""
Reward Script: Automatic figure numbering with chapter-based numbering
Task ID: writer_tech_064
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 6 caption paragraphs contain SEQ Figure field codes
  Component 2 (0.3): All 6 caption paragraphs contain STYLEREF field codes for chapter refs
  Component 3 (0.2): Caption descriptions preserved AND have auto-numbering fields (compound check)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_064'

# Expected caption descriptions (the part after "Figure X-Y: ")
EXPECTED_CAPTIONS = [
    "Core switch topology for Austin headquarters",
    "Server rack layout with hot aisle containment",
    "VLAN segmentation diagram with subnet allocations",
    "Network monitoring dashboard overview",
    "Firewall rule matrix between security zones",
    "Intrusion detection sensor placement diagram",
]

# Paragraph indices where captions live (known from document structure)
CAPTION_INDICES = [9, 14, 22, 27, 35, 40]


def find_caption_paragraphs(doc):
    """Find paragraphs that contain figure captions by matching description text."""
    caption_paras = []
    for expected_desc in EXPECTED_CAPTIONS:
        found = False
        for para in doc.paragraphs:
            if expected_desc in para.text:
                caption_paras.append(para)
                found = True
                break
        if not found:
            caption_paras.append(None)
    return caption_paras


def has_seq_figure_field(para):
    """Check if a paragraph contains a SEQ Figure field code for automatic numbering."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    instrs = para._element.findall('.//w:instrText', ns)
    for instr in instrs:
        if instr.text and 'SEQ' in instr.text and 'Figure' in instr.text:
            return True
    return False


def has_styleref_field(para):
    """Check if a paragraph contains a STYLEREF field code for chapter-based numbering."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    instrs = para._element.findall('.//w:instrText', ns)
    for instr in instrs:
        if instr.text and 'STYLEREF' in instr.text:
            return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find caption paragraphs by matching description text
    caption_paras = find_caption_paragraphs(doc)
    found_count = sum(1 for p in caption_paras if p is not None)
    print(f"INFO: Found {found_count}/6 caption paragraphs by description match")

    if found_count == 0:
        print("CRITICAL: No caption paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: SEQ Figure field codes for automatic numbering (0.5 points)
    # Each caption with SEQ field earns 0.5/6 points
    try:
        seq_count = 0
        for i, para in enumerate(caption_paras):
            if para is not None and has_seq_figure_field(para):
                seq_count += 1
                print(f"  PASS: Caption {i+1} has SEQ Figure field")
            elif para is not None:
                print(f"  FAIL: Caption {i+1} missing SEQ Figure field")
            else:
                print(f"  FAIL: Caption {i+1} paragraph not found")

        if seq_count > 0:
            comp1_score = 0.5 * (seq_count / 6)
            print(f"PASS: Component 1 -- SEQ Figure fields: {seq_count}/6 ({comp1_score:.3f} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 -- No SEQ Figure fields found in any caption")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: STYLEREF field codes for chapter-based numbering (0.3 points)
    # Each caption with STYLEREF earns 0.3/6 points
    try:
        styleref_count = 0
        for i, para in enumerate(caption_paras):
            if para is not None and has_styleref_field(para):
                styleref_count += 1
                print(f"  PASS: Caption {i+1} has STYLEREF field")
            elif para is not None:
                print(f"  FAIL: Caption {i+1} missing STYLEREF field")
            else:
                print(f"  FAIL: Caption {i+1} paragraph not found")

        if styleref_count > 0:
            comp2_score = 0.3 * (styleref_count / 6)
            print(f"PASS: Component 2 -- STYLEREF fields: {styleref_count}/6 ({comp2_score:.3f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 -- No STYLEREF fields found in any caption")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Caption text preserved WITH auto-numbering (0.2 points)
    # Compound check: description text is preserved AND SEQ field is present
    # This ensures the conversion to auto-numbering didn't lose the caption descriptions
    try:
        compound_count = 0
        for i, (para, expected_desc) in enumerate(zip(caption_paras, EXPECTED_CAPTIONS)):
            if para is not None and expected_desc in para.text and has_seq_figure_field(para):
                compound_count += 1
            elif para is not None:
                if expected_desc not in para.text:
                    print(f"  FAIL: Caption {i+1} text mismatch: {para.text!r}")
                else:
                    print(f"  FAIL: Caption {i+1} has text but missing SEQ field")
            else:
                print(f"  FAIL: Caption {i+1} not found")

        if compound_count > 0:
            comp3_score = 0.2 * (compound_count / 6)
            print(f"PASS: Component 3 -- Captions with text+fields: {compound_count}/6 ({comp3_score:.3f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- No captions have both preserved text and auto-numbering fields")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
