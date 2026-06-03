"""
Reward Script: Definition-style glossary list with bold hanging indent terms and indented definitions
Task ID: writer_lec_031
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.35): Term paragraphs are bold
  - Component 2 (0.35): Term paragraphs have hanging indent (negative first_line_indent + positive left_indent)
  - Component 3 (0.30): Definition paragraphs are indented (~2.0 cm left_indent)
"""

import os
from docx import Document
from docx.shared import Pt, Inches, Emu

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_031'

# 8 term-definition pairs starting after the heading (paragraph index 0)
# Terms at indices 1,3,5,...,15; definitions at indices 2,4,6,...,16
TERM_INDICES = [1, 3, 5, 7, 9, 11, 13, 15]
DEF_INDICES = [2, 4, 6, 8, 10, 12, 14, 16]

# Tolerance for indent checks: 2.0 cm = 720000 EMU, allow +/- 100000 EMU (~0.28 cm)
INDENT_TARGET_EMU = 720000
INDENT_TOLERANCE_EMU = 100000


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

    paras = doc.paragraphs
    if len(paras) < 17:
        print(f"FAIL: Expected at least 17 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Term paragraphs have bold formatting (0.35 points)
    # In initial_env, terms are not bold. In golden_env, they should be bold.
    try:
        bold_count = 0
        for idx in TERM_INDICES:
            para = paras[idx]
            runs_with_text = [r for r in para.runs if r.text.strip()]
            if runs_with_text and all(r.font.bold is True for r in runs_with_text):
                bold_count += 1

        if bold_count == len(TERM_INDICES):
            print(f"PASS: Component 1 — All {bold_count}/{len(TERM_INDICES)} term paragraphs are bold (0.35 pts)")
            total_score += 0.35
        elif bold_count > 0:
            partial = round(0.35 * bold_count / len(TERM_INDICES), 2)
            print(f"PARTIAL: Component 1 — {bold_count}/{len(TERM_INDICES)} term paragraphs are bold ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No term paragraphs are bold (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Term paragraphs have hanging indent (0.35 points)
    # Hanging indent = positive left_indent + negative first_line_indent
    # In initial_env, no indentation. In golden_env, hanging indent should be present.
    try:
        hanging_count = 0
        for idx in TERM_INDICES:
            para = paras[idx]
            pf = para.paragraph_format
            left_ind = pf.left_indent
            first_line = pf.first_line_indent

            if (left_ind is not None and
                abs(left_ind - INDENT_TARGET_EMU) < INDENT_TOLERANCE_EMU and
                first_line is not None and
                first_line < 0):
                hanging_count += 1

        if hanging_count == len(TERM_INDICES):
            print(f"PASS: Component 2 — All {hanging_count}/{len(TERM_INDICES)} term paragraphs have hanging indent (0.35 pts)")
            total_score += 0.35
        elif hanging_count > 0:
            partial = round(0.35 * hanging_count / len(TERM_INDICES), 2)
            print(f"PARTIAL: Component 2 — {hanging_count}/{len(TERM_INDICES)} term paragraphs have hanging indent ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No term paragraphs have hanging indent (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Definition paragraphs are indented ~2.0 cm (0.30 points)
    # In initial_env, no indentation. In golden_env, definitions should have left_indent ~2.0 cm.
    try:
        indent_count = 0
        for idx in DEF_INDICES:
            para = paras[idx]
            pf = para.paragraph_format
            left_ind = pf.left_indent

            if (left_ind is not None and
                abs(left_ind - INDENT_TARGET_EMU) < INDENT_TOLERANCE_EMU):
                indent_count += 1

        if indent_count == len(DEF_INDICES):
            print(f"PASS: Component 3 — All {indent_count}/{len(DEF_INDICES)} definition paragraphs are indented (0.30 pts)")
            total_score += 0.30
        elif indent_count > 0:
            partial = round(0.30 * indent_count / len(DEF_INDICES), 2)
            print(f"PARTIAL: Component 3 — {indent_count}/{len(DEF_INDICES)} definition paragraphs are indented ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No definition paragraphs are indented (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
