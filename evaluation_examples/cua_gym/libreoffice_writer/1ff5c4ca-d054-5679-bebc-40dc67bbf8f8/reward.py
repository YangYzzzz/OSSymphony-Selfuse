"""
Reward Script: Set hanging indent for bibliography references
Task ID: writer_fs_046
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Majority of reference paragraphs have left_indent ~1.27cm
  Component 2 (0.4): Majority of reference paragraphs have first_line_indent ~-1.27cm
  Component 3 (0.2): ALL reference paragraphs have both correct indents (completeness)
"""

import os
from docx import Document
from docx.shared import Emu

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_046'

# Tolerance: 1.27cm = 0.5in. Allow +/- 0.15cm tolerance
TARGET_LEFT_CM = 1.27
TARGET_FIRST_CM = -1.27
TOLERANCE_CM = 0.15


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

    # Identify reference paragraphs (skip the heading, only Normal-style paragraphs with text)
    ref_paras = []
    for para in doc.paragraphs:
        if para.style and para.style.name == 'Normal' and para.text.strip():
            ref_paras.append(para)

    if len(ref_paras) == 0:
        print("FAIL: No reference paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(ref_paras)} reference paragraphs")

    # Analyze indents for each reference paragraph
    left_correct_count = 0
    first_correct_count = 0
    both_correct_count = 0

    for i, para in enumerate(ref_paras):
        pf = para.paragraph_format
        left = pf.left_indent
        first = pf.first_line_indent

        left_cm = round(Emu(left).cm, 4) if left else 0.0
        first_cm = round(Emu(first).cm, 4) if first else 0.0

        left_ok = abs(left_cm - TARGET_LEFT_CM) <= TOLERANCE_CM
        first_ok = abs(first_cm - TARGET_FIRST_CM) <= TOLERANCE_CM

        if left_ok:
            left_correct_count += 1
        if first_ok:
            first_correct_count += 1
        if left_ok and first_ok:
            both_correct_count += 1

        if not (left_ok and first_ok):
            print(f"  P{i}: left={left_cm}cm (expect ~{TARGET_LEFT_CM}), first={first_cm}cm (expect ~{TARGET_FIRST_CM})")

    total_refs = len(ref_paras)
    threshold = int(total_refs * 0.75)

    # Component 1: Majority of reference paragraphs have left_indent ~1.27cm (0.4 points)
    try:
        if left_correct_count >= threshold:
            print(f"PASS: Component 1 — {left_correct_count}/{total_refs} paragraphs have correct left_indent (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — only {left_correct_count}/{total_refs} paragraphs have correct left_indent (need {threshold})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Majority of reference paragraphs have first_line_indent ~-1.27cm (0.4 points)
    try:
        if first_correct_count >= threshold:
            print(f"PASS: Component 2 — {first_correct_count}/{total_refs} paragraphs have correct first_line_indent (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — only {first_correct_count}/{total_refs} paragraphs have correct first_line_indent (need {threshold})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ALL reference paragraphs have both correct indents (0.2 points)
    try:
        if both_correct_count == total_refs:
            print(f"PASS: Component 3 — all {total_refs} paragraphs have both correct indents (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {both_correct_count}/{total_refs} paragraphs have both correct indents (need all)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
