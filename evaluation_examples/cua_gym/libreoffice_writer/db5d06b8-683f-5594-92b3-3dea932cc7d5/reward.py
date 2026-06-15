"""
Reward Script: Apply 0.5cm first-line indent and justified alignment to body paragraphs
Task ID: writer_para_043
Domain: libreoffice_writer

Scoring Rubric:
  Component 1: All 4 body paragraphs have first_line_indent ~= 0.5cm  (0.5 pts)
  Component 2: All 4 body paragraphs have JUSTIFY alignment            (0.4 pts)
  Component 3: Heading paragraphs retain non-JUSTIFY formatting        (0.1 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_para_043'
FILE_PATH = f'{WORKDIR}/journal_article.docx'

# Expected body paragraph indices (0-based) from task context:
#   Para 0: Heading 1 — 'Climate Change Adaptation Strategies...'
#   Para 1: Heading 2 — 'Abstract'
#   Para 2: Normal    — body text (must be modified)
#   Para 3: Heading 2 — '1. Introduction'
#   Para 4: Normal    — body text (must be modified)
#   Para 5: Normal    — body text (must be modified)
#   Para 6: Heading 2 — '2. Study Areas'
#   Para 7: Normal    — body text (must be modified)

# Tolerance for EMU comparison: ~0.003 cm (1000 EMU)
EMU_TOLERANCE = 1000
TARGET_INDENT_EMU = int(Cm(0.5))  # 180000 EMU


def is_heading_style(style_name):
    """Check if a paragraph style is a heading."""
    return 'Heading' in style_name or style_name.startswith('Title')


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

    # Identify body paragraphs (Normal style) and heading paragraphs
    body_paras = []
    heading_paras = []
    for i, para in enumerate(doc.paragraphs):
        style_name = para.style.name
        if is_heading_style(style_name):
            heading_paras.append((i, para))
        elif para.text.strip():  # non-empty normal paragraphs
            body_paras.append((i, para))

    print(f"Found {len(body_paras)} body paragraph(s) and {len(heading_paras)} heading paragraph(s)")

    if len(body_paras) == 0:
        print("CRITICAL: No body paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All body paragraphs have first_line_indent ~= 0.5cm (0.5 points)
    # This should FAIL on initial_env (fli=None) and PASS on golden_env (fli≈0.5cm)
    try:
        indent_pass_count = 0
        indent_total = len(body_paras)
        for idx, para in body_paras:
            pf = para.paragraph_format
            fli = pf.first_line_indent
            if fli is not None and abs(fli - TARGET_INDENT_EMU) <= EMU_TOLERANCE:
                indent_pass_count += 1
                print(f"PASS: Para {idx} first_line_indent={fli} EMU (~{fli/360000:.4f}cm) within tolerance")
            else:
                fli_cm = f"{fli/360000:.4f}cm" if fli is not None else "None"
                print(f"FAIL: Para {idx} first_line_indent={fli_cm}, expected ~0.5cm")

        if indent_pass_count == indent_total:
            print(f"PASS: Component 1 — all {indent_total} body paragraphs have first_line_indent ~0.5cm (0.5 pts)")
            total_score += 0.5
        elif indent_pass_count > 0:
            partial = round(0.5 * indent_pass_count / indent_total, 4)
            print(f"PARTIAL: Component 1 — {indent_pass_count}/{indent_total} body paragraphs have correct indent ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — no body paragraphs have first_line_indent ~0.5cm (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All body paragraphs have JUSTIFY alignment (0.4 points)
    # This should FAIL on initial_env (align=LEFT) and PASS on golden_env (align=JUSTIFY)
    try:
        justify_pass_count = 0
        justify_total = len(body_paras)
        for idx, para in body_paras:
            pf = para.paragraph_format
            align = pf.alignment
            if align == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
                justify_pass_count += 1
                print(f"PASS: Para {idx} alignment=JUSTIFY")
            else:
                print(f"FAIL: Para {idx} alignment={align}, expected JUSTIFY")

        if justify_pass_count == justify_total:
            print(f"PASS: Component 2 — all {justify_total} body paragraphs have JUSTIFY alignment (0.4 pts)")
            total_score += 0.4
        elif justify_pass_count > 0:
            partial = round(0.4 * justify_pass_count / justify_total, 4)
            print(f"PARTIAL: Component 2 — {justify_pass_count}/{justify_total} body paragraphs have JUSTIFY alignment ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no body paragraphs have JUSTIFY alignment (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Compound check — body paragraphs changed to JUSTIFY AND headings NOT changed (0.1 points)
    # This is a compound check: both conditions must hold simultaneously.
    # On initial_env: body paras have LEFT alignment (not JUSTIFY) → compound check fails → 0.0 pts
    # On golden_env: body paras have JUSTIFY AND headings still have non-JUSTIFY → 0.1 pts
    try:
        # Sub-condition A: at least one body paragraph has JUSTIFY (task was applied)
        any_body_justified = any(
            para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            for _, para in body_paras
        )

        # Sub-condition B: all heading paragraphs do NOT have JUSTIFY alignment
        # If no headings, vacuously ok (all([]) == True in Python)
        headings_ok = all(
            para.paragraph_format.alignment != WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            for _, para in heading_paras
        )

        if any_body_justified and headings_ok:
            print(f"PASS: Component 3 — body paragraphs have JUSTIFY and heading paragraphs retain non-JUSTIFY formatting (0.1 pts)")
            total_score += 0.1
        elif not any_body_justified:
            print(f"FAIL: Component 3 — body paragraphs have not been changed to JUSTIFY (0.0 pts)")
        else:
            print(f"FAIL: Component 3 — heading paragraphs were incorrectly changed to JUSTIFY (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
