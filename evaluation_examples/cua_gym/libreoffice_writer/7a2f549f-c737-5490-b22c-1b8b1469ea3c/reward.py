"""
Reward Script: Add 3pt solid gray left border and 1.5cm left indent to paragraphs 4 and 8
Task ID: writer_para_050
Domain: libreoffice_writer
Scoring:
  Component 1a: Para 4 (0-indexed: 3) has correct left-only border (single/solid, #999999, 3pt) — 0.3 pts
  Component 1b: Para 8 (0-indexed: 7) has correct left-only border (single/solid, #999999, 3pt) — 0.3 pts
  Component 2a: Para 4 (0-indexed: 3) has left_indent ≈ 1.5cm — 0.2 pts
  Component 2b: Para 8 (0-indexed: 7) has left_indent ≈ 1.5cm — 0.2 pts
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Cm
from docx.oxml.ns import qn

WORKDIR = '/home/user'
FILE_PATH = f'{WORKDIR}/interview_transcript.docx'

# Tolerance for indent comparison (0.5mm = 18000 EMU)
INDENT_TOLERANCE_EMU = 18000
# Expected indent: 1.5cm = 540000 EMU
EXPECTED_INDENT_EMU = 540000

# Target paragraph indices (0-indexed): paragraphs 4 and 8 in 1-indexed notation
TARGET_PARA_INDICES = [3, 7]

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def check_left_border(para):
    """
    Check if a paragraph has a left-only border with:
      - val='single' (solid style)
      - color='999999'
      - sz=24 (3pt, since sz is in 1/8-point units, 24/8 = 3.0pt)
    Returns (bool, str) — (passed, detail_message)
    """
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        return False, "no pPr element"
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        return False, "no pBdr element"

    left = pBdr.find(qn('w:left'))
    if left is None:
        return False, "no w:left border element"

    val = left.get(f'{{{W_NS}}}val', '')
    color = left.get(f'{{{W_NS}}}color', '').lower().lstrip('#')
    sz_str = left.get(f'{{{W_NS}}}sz', '0')
    try:
        sz = int(sz_str)
    except ValueError:
        sz = 0

    issues = []
    # Style: 'single' corresponds to SOLID
    if val not in ('single', 'thick'):
        issues.append(f"val='{val}' (expected 'single')")
    # Color: must be 999999
    if color != '999999':
        issues.append(f"color='{color}' (expected '999999')")
    # Width: sz=24 means 3pt (24 eighths-of-a-point)
    if sz != 24:
        issues.append(f"sz={sz} (expected 24 = 3pt)")

    # Check that there are no other sides (top, right, bottom) with active borders
    for side in ('top', 'right', 'bottom'):
        elem = pBdr.find(qn(f'w:{side}'))
        if elem is not None:
            side_val = elem.get(f'{{{W_NS}}}val', '')
            if side_val not in ('none', 'nil', ''):
                issues.append(f"unexpected {side} border: val='{side_val}'")

    if issues:
        return False, '; '.join(issues)
    return True, f"val={val!r}, color={color!r}, sz={sz}"


def check_left_indent(para):
    """
    Check if a paragraph has left_indent close to 1.5cm (540000 EMU).
    Returns (bool, str) — (passed, detail_message)
    """
    pf = para.paragraph_format
    indent = pf.left_indent
    if indent is None:
        return False, f"left_indent=None (expected ~{EXPECTED_INDENT_EMU} EMU = 1.5cm)"
    diff = abs(int(indent) - EXPECTED_INDENT_EMU)
    if diff <= INDENT_TOLERANCE_EMU:
        return True, f"left_indent={int(indent)} EMU (~{int(indent)/360000:.2f}cm)"
    return False, f"left_indent={int(indent)} EMU (~{int(indent)/360000:.2f}cm), expected ~{EXPECTED_INDENT_EMU} EMU (1.5cm)"


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — if fails, bail out immediately
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    if len(paras) < 8:
        print(f"CRITICAL: Document has {len(paras)} paragraphs, expected at least 8")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1a: Para 4 (0-indexed: 3) has correct left-only border (0.3 pts)
    # -----------------------------------------------------------------------
    try:
        passed_1a, detail_1a = check_left_border(paras[3])
        if passed_1a:
            print(f"PASS: Component 1a — para 4 has correct left border ({detail_1a}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1a — para 4 left border check failed: {detail_1a}")
    except Exception as e:
        print(f"ERROR: Component 1a — {e}")

    # -----------------------------------------------------------------------
    # Component 1b: Para 8 (0-indexed: 7) has correct left-only border (0.3 pts)
    # -----------------------------------------------------------------------
    try:
        passed_1b, detail_1b = check_left_border(paras[7])
        if passed_1b:
            print(f"PASS: Component 1b — para 8 has correct left border ({detail_1b}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1b — para 8 left border check failed: {detail_1b}")
    except Exception as e:
        print(f"ERROR: Component 1b — {e}")

    # -----------------------------------------------------------------------
    # Component 2a: Para 4 (0-indexed: 3) has left_indent ≈ 1.5cm (0.2 pts)
    # -----------------------------------------------------------------------
    try:
        passed_2a, detail_2a = check_left_indent(paras[3])
        if passed_2a:
            print(f"PASS: Component 2a — para 4 left_indent correct ({detail_2a}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2a — para 4 left_indent incorrect: {detail_2a}")
    except Exception as e:
        print(f"ERROR: Component 2a — {e}")

    # -----------------------------------------------------------------------
    # Component 2b: Para 8 (0-indexed: 7) has left_indent ≈ 1.5cm (0.2 pts)
    # -----------------------------------------------------------------------
    try:
        passed_2b, detail_2b = check_left_indent(paras[7])
        if passed_2b:
            print(f"PASS: Component 2b — para 8 left_indent correct ({detail_2b}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2b — para 8 left_indent incorrect: {detail_2b}")
    except Exception as e:
        print(f"ERROR: Component 2b — {e}")

    # -----------------------------------------------------------------------
    # Sanity check: other paragraphs should NOT have borders (informational only, no scoring)
    # -----------------------------------------------------------------------
    try:
        non_target = [i for i in range(len(paras)) if i not in TARGET_PARA_INDICES]
        for idx in non_target:
            para = paras[idx]
            pPr = para._p.find(qn('w:pPr'))
            if pPr is not None:
                pBdr = pPr.find(qn('w:pBdr'))
                if pBdr is not None:
                    left_elem = pBdr.find(qn('w:left'))
                    if left_elem is not None:
                        val = left_elem.get(f'{{{W_NS}}}val', 'none')
                        if val not in ('none', 'nil', ''):
                            print(f"INFO: para {idx+1} unexpectedly has left border (val={val!r})")
    except Exception as e:
        print(f"INFO: Could not check non-target paragraphs: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
