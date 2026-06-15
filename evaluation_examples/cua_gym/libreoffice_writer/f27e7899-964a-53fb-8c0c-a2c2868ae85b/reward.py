"""
Reward Script: Set up gutter margin of 1.5 cm on left side for binding
Task ID: writer_rd_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.50): Effective left margin is ~4.04 cm (2.54 + 1.5 gutter)
  Component 2 (0.30): Left margin changed AND right margin still ~2.54 cm (not accidentally changed)
  Component 3 (0.20): Left margin changed AND top+bottom margins still ~2.54 cm (not accidentally changed)

All components are gated on the left margin having changed from its initial 2.54 cm,
ensuring initial_env scores 0.0.
"""

import os
from docx import Document
from docx.shared import Emu
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_054'

# Namespace for Word XML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# Tolerance: 0.15 cm in EMU
TOLERANCE_CM = 0.15
TOLERANCE_EMU = int(TOLERANCE_CM * 360000)

# Expected values in EMU
CM_254 = 914400   # 2.54 cm = 1 inch = 914400 EMU
CM_150 = 540000   # 1.5 cm = 540000 EMU
CM_404 = CM_254 + CM_150  # 4.04 cm = 1454400 EMU


def emu_to_cm(emu):
    """Convert EMU to centimeters."""
    return emu / 360000.0


def twips_to_emu(twips):
    """Convert twips to EMU (1 twip = 635 EMU)."""
    return int(twips) * 635


def close_enough(actual, expected, tolerance=TOLERANCE_EMU):
    """Check if actual is within tolerance of expected."""
    return abs(actual - expected) <= tolerance


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

    section = doc.sections[0]

    # Parse XML to get gutter value
    gutter_emu = 0
    try:
        pgMar_list = section._sectPr.findall(f'{{{W_NS}}}pgMar')
        if pgMar_list:
            pgMar = pgMar_list[0]
            gutter_twips = pgMar.get(f'{{{W_NS}}}gutter', '0')
            gutter_emu = twips_to_emu(gutter_twips)
            print(f"INFO: XML gutter = {gutter_twips} twips = {emu_to_cm(gutter_emu):.4f} cm")
    except Exception as e:
        print(f"WARN: Could not parse gutter from XML: {e}")

    left_margin_emu = section.left_margin
    right_margin_emu = section.right_margin
    top_margin_emu = section.top_margin
    bottom_margin_emu = section.bottom_margin

    # Effective left space = left_margin + gutter (handles both implementation approaches)
    effective_left_emu = left_margin_emu + gutter_emu

    print(f"INFO: left_margin  = {emu_to_cm(left_margin_emu):.4f} cm ({left_margin_emu} EMU)")
    print(f"INFO: right_margin = {emu_to_cm(right_margin_emu):.4f} cm ({right_margin_emu} EMU)")
    print(f"INFO: top_margin   = {emu_to_cm(top_margin_emu):.4f} cm ({top_margin_emu} EMU)")
    print(f"INFO: bottom_margin= {emu_to_cm(bottom_margin_emu):.4f} cm ({bottom_margin_emu} EMU)")
    print(f"INFO: gutter       = {emu_to_cm(gutter_emu):.4f} cm ({gutter_emu} EMU)")
    print(f"INFO: effective_left = {emu_to_cm(effective_left_emu):.4f} cm ({effective_left_emu} EMU)")

    # Gate: check if effective left margin has been changed from the initial 2.54 cm
    left_changed = not close_enough(effective_left_emu, CM_254)

    # Component 1: Effective left margin ~4.04 cm (0.50 points)
    # This is the core task: adding 1.5 cm gutter to the 2.54 cm left margin.
    try:
        if close_enough(effective_left_emu, CM_404):
            print(f"PASS: Component 1 — Effective left margin is {emu_to_cm(effective_left_emu):.2f} cm (expected ~4.04 cm) (0.50 pts)")
            total_score += 0.50
        else:
            print(f"FAIL: Component 1 — Effective left margin is {emu_to_cm(effective_left_emu):.2f} cm, expected ~4.04 cm")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Left margin changed AND right margin still ~2.54 cm (0.30 points)
    # Verifies the agent only modified the left side, not the right.
    try:
        if left_changed and close_enough(right_margin_emu, CM_254):
            print(f"PASS: Component 2 — Left changed + right margin preserved at {emu_to_cm(right_margin_emu):.2f} cm (0.30 pts)")
            total_score += 0.30
        elif not left_changed:
            print(f"FAIL: Component 2 — Left margin not changed from initial (effective: {emu_to_cm(effective_left_emu):.2f} cm)")
        else:
            print(f"FAIL: Component 2 — Right margin changed to {emu_to_cm(right_margin_emu):.2f} cm (expected ~2.54 cm)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left margin changed AND top+bottom margins still ~2.54 cm (0.20 points)
    # Verifies the agent didn't accidentally modify top/bottom margins.
    try:
        top_ok = close_enough(top_margin_emu, CM_254)
        bottom_ok = close_enough(bottom_margin_emu, CM_254)
        if left_changed and top_ok and bottom_ok:
            print(f"PASS: Component 3 — Left changed + top ({emu_to_cm(top_margin_emu):.2f} cm) and bottom ({emu_to_cm(bottom_margin_emu):.2f} cm) preserved (0.20 pts)")
            total_score += 0.20
        elif not left_changed:
            print(f"FAIL: Component 3 — Left margin not changed from initial")
        else:
            print(f"FAIL: Component 3 — Top={emu_to_cm(top_margin_emu):.2f} cm, Bottom={emu_to_cm(bottom_margin_emu):.2f} cm (expected ~2.54 cm each)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
