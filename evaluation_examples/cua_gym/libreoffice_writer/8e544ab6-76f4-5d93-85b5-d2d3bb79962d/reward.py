"""
Reward Script: Apply light blue background (#D6EAF8) and 0.3 cm padding to code example paragraphs
Task ID: writer_para_036
Domain: libreoffice_writer
Scoring:
  Component 1: Para 3 (first code example) has background fill == D6EAF8         (0.40 pts)
  Component 2: Para 3 has 0.3 cm padding via indent (left=170, right=170 twips)   (0.30 pts)
  Component 3: Para 6 (second code example) has background fill == D6EAF8
               AND 0.3 cm padding (left=170, right=170 twips indent)               (0.30 pts)

0.3 cm = 170.08 ≈ 170 twips (Word XML unit for indents/spacing)
Padding is implemented as left/right indent of 170 twips and spacing before/after of 170 twips.
"""

import os

from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_para_036'
FILE_PATH = f'{WORKDIR}/python_tutorial.docx'

# Target paragraph indices (0-based) — code example paragraphs
CODE_PARA_1_IDX = 3   # 'student = {"name": "Alice", ...}'
CODE_PARA_2_IDX = 6   # 'for key, value in student.items(): ...'

# Expected values
TARGET_BG_COLOR = 'D6EAF8'   # light blue hex (without #)
TARGET_INDENT_TWIPS = 170     # 0.3 cm in twips
INDENT_TOLERANCE = 5          # twips tolerance for floating-point conversions


def get_para_shd_fill(para):
    """Extract paragraph shading fill color from XML. Returns hex string or None."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None
    shd = pPr.find(qn('w:shd'))
    if shd is None:
        return None
    fill = shd.get(qn('w:fill'))
    return fill  # e.g. 'D6EAF8' or 'auto' or None


def get_para_indent(para):
    """Extract paragraph indent (left, right) in twips from XML. Returns (left, right) or (None, None)."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None, None
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        return None, None
    left = ind.get(qn('w:left'))
    right = ind.get(qn('w:right'))
    try:
        left = int(left) if left is not None else None
    except (ValueError, TypeError):
        left = None
    try:
        right = int(right) if right is not None else None
    except (ValueError, TypeError):
        right = None
    return left, right


def get_para_spacing(para):
    """Extract paragraph spacing (before, after) in twips from XML. Returns (before, after) or (None, None)."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None, None
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        return None, None
    before = spacing.get(qn('w:before'))
    after = spacing.get(qn('w:after'))
    try:
        before = int(before) if before is not None else None
    except (ValueError, TypeError):
        before = None
    try:
        after = int(after) if after is not None else None
    except (ValueError, TypeError):
        after = None
    return before, after


def check_bg_color(fill, target=TARGET_BG_COLOR):
    """Return True if fill matches target color (case-insensitive)."""
    if fill is None:
        return False
    return fill.upper() == target.upper()


def check_padding(left, right, target=TARGET_INDENT_TWIPS, tol=INDENT_TOLERANCE):
    """Return True if both left and right indent are within tolerance of target."""
    if left is None or right is None:
        return False
    return (abs(left - target) <= tol) and (abs(right - target) <= tol)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — critical gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    n = len(paragraphs)
    print(f"INFO: Document has {n} paragraphs.")

    if n < 7:
        print(f"CRITICAL: Expected at least 7 paragraphs, found {n}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Para 3 (first code example) has background fill D6EAF8
    #              (0.40 points)
    # -----------------------------------------------------------------------
    try:
        para3 = paragraphs[CODE_PARA_1_IDX]
        fill3 = get_para_shd_fill(para3)
        if check_bg_color(fill3):
            print(f"PASS: Component 1 — Para {CODE_PARA_1_IDX} has background #D6EAF8 (found: {fill3}) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — Para {CODE_PARA_1_IDX} background expected D6EAF8, found: {fill3}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Para 3 has 0.3 cm padding as left/right indent ~170 twips
    #              (0.30 points)
    # -----------------------------------------------------------------------
    try:
        para3 = paragraphs[CODE_PARA_1_IDX]
        left3, right3 = get_para_indent(para3)
        if check_padding(left3, right3):
            print(f"PASS: Component 2 — Para {CODE_PARA_1_IDX} has 0.3 cm indent (left={left3}, right={right3} twips) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Para {CODE_PARA_1_IDX} indent expected ~{TARGET_INDENT_TWIPS} twips on each side, found left={left3}, right={right3}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Para 6 (second code example) has background fill D6EAF8
    #              AND 0.3 cm padding as left/right indent ~170 twips
    #              (0.30 points)
    # -----------------------------------------------------------------------
    try:
        para6 = paragraphs[CODE_PARA_2_IDX]
        fill6 = get_para_shd_fill(para6)
        left6, right6 = get_para_indent(para6)
        bg_ok = check_bg_color(fill6)
        pad_ok = check_padding(left6, right6)
        if bg_ok and pad_ok:
            print(f"PASS: Component 3 — Para {CODE_PARA_2_IDX} has background {fill6} and indent left={left6}/right={right6} twips (0.30 pts)")
            total_score += 0.30
        else:
            reasons = []
            if not bg_ok:
                reasons.append(f"background expected D6EAF8 found {fill6}")
            if not pad_ok:
                reasons.append(f"indent expected ~{TARGET_INDENT_TWIPS} found left={left6}/right={right6}")
            print(f"FAIL: Component 3 — Para {CODE_PARA_2_IDX}: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
