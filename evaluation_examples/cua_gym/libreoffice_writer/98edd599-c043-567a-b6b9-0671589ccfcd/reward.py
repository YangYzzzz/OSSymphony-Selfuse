"""
Reward Script: Insert company logo into document header with resize and alignment
Task ID: writer_obj_025
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Header contains an inline image (logo inserted into header)
  Component 2 (0.3): Image dimensions are 3cm x 2cm (within 5% tolerance)
  Component 3 (0.3): Header paragraph alignment is LEFT
"""

import os
import re

# python-docx
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_obj_025'

# Target dimensions: 3cm wide, 2cm tall
TARGET_CX_EMU = int(Cm(3))   # 1080000
TARGET_CY_EMU = int(Cm(2))   # 720000
TOLERANCE = 0.05              # 5% tolerance on dimensions


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that the document header contains the logo image at the correct
    size (3cm x 2cm) and aligned to the left.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — if it fails, return 0.0 immediately
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least one section with a header
    try:
        section = doc.sections[0]
        header = section.header
    except Exception as e:
        print(f"CRITICAL: Cannot access document section/header: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve raw header XML for image checks
    header_xml = header._element.xml

    # Component 1: Header contains an inline image (0.4 points)
    # This FAILS on initial_env (empty header) and PASSES on golden_env (logo inserted)
    try:
        has_image = 'graphicData' in header_xml
        if has_image:
            print("PASS: Component 1 — header contains an inline image (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — no image found in header (expected logo.png)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Image dimensions are 3cm x 2cm (0.3 points)
    # Target: cx=1080000 EMU (3cm), cy=720000 EMU (2cm), with 5% tolerance
    # This FAILS on initial_env (no image) and PASSES on golden_env
    try:
        extent_match = re.search(r'wp:extent cx="(\d+)" cy="(\d+)"', header_xml)
        if extent_match:
            cx = int(extent_match.group(1))
            cy = int(extent_match.group(2))
            cx_ok = abs(cx - TARGET_CX_EMU) / TARGET_CX_EMU <= TOLERANCE
            cy_ok = abs(cy - TARGET_CY_EMU) / TARGET_CY_EMU <= TOLERANCE
            if cx_ok and cy_ok:
                print(f"PASS: Component 2 — image dimensions {cx/360000:.3f}cm x {cy/360000:.3f}cm (target: 3.0cm x 2.0cm) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — image dimensions {cx/360000:.3f}cm x {cy/360000:.3f}cm, expected 3.0cm x 2.0cm (cx_ok={cx_ok}, cy_ok={cy_ok})")
        else:
            print("FAIL: Component 2 — no wp:extent element found in header (no image dimensions)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Header paragraph is aligned LEFT (0.3 points)
    # python-docx returns WD_PARAGRAPH_ALIGNMENT.LEFT (0) or None for default left
    # The golden file sets explicit <w:jc w:val="left"/> in the header paragraph.
    # This FAILS on initial_env (alignment is None/unset, no image paragraph) and
    # PASSES on golden_env (alignment explicitly set to LEFT with image).
    # We gate this check on image presence to ensure it only passes for the task-change state.
    try:
        if 'graphicData' in header_xml:
            para = header.paragraphs[0]
            alignment = para.paragraph_format.alignment
            # Accept explicit LEFT (0) or also check XML directly for <w:jc w:val="left">
            xml_has_jc_left = '<w:jc w:val="left"/>' in header_xml
            if alignment == WD_PARAGRAPH_ALIGNMENT.LEFT or xml_has_jc_left:
                print(f"PASS: Component 3 — header paragraph aligned LEFT (alignment={alignment}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — header paragraph alignment is {alignment}, expected LEFT (WD_PARAGRAPH_ALIGNMENT.LEFT)")
        else:
            print("FAIL: Component 3 — no image in header, alignment check skipped (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entry point: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/official_letter.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
