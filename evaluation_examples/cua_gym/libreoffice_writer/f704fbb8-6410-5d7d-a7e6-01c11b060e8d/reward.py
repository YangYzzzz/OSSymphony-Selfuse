"""
Reward Script: Make signature block left-aligned with 10cm left indent
Task ID: writer_para_034
Domain: libreoffice_writer
Scoring:
  Component 1: All 3 signature paragraphs (7,8,9) have left_indent ~10cm  (0.6 pts)
  Component 2: Signature paragraphs have ~10cm indent AND LEFT alignment
               AND other paragraphs retain zero indent                     (0.4 pts)
  Total: 1.0

Note: Components 2 gates on Component 1 passing to form a compound check
that verifies the full task requirement simultaneously, ensuring initial_env
scores 0.0.
"""

import os
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_para_034'

# EMU constants
CM_10_EMU = int(Cm(10))       # 3600000 EMU
TOLERANCE_EMU = 36000         # 0.1cm tolerance (~1%)

# Paragraph indices (0-based) that form the signature block
SIGNATURE_INDICES = [7, 8, 9]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    LITMUS TEST: Every scoring component must FAIL on initial_env (no indent set)
    and PASS on golden_env (10cm indent applied to signature block).
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs

    # Precondition gate: confirm document has expected 10-paragraph structure
    if len(paras) < 10:
        print(f"CRITICAL: Expected at least 10 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Signature paragraphs (7,8,9) have left_indent ~10cm (0.6 points)
    # This FAILS on initial (indent=0), PASSES on golden (indent=~3600000 EMU)
    try:
        sig_indent_count = 0
        for idx in SIGNATURE_INDICES:
            para = paras[idx]
            pf = para.paragraph_format
            indent = pf.left_indent

            if indent is not None and abs(indent - CM_10_EMU) <= TOLERANCE_EMU:
                print(f"INFO: Para {idx} ('{para.text[:30]}') indent={indent} EMU — OK (~10cm)")
                sig_indent_count += 1
            else:
                print(f"FAIL: Component 1 — Para {idx} ('{para.text[:30]}') indent={indent} EMU, "
                      f"expected {CM_10_EMU} EMU (±{TOLERANCE_EMU})")

        if sig_indent_count == len(SIGNATURE_INDICES):
            print(f"PASS: Component 1 — All 3 signature paragraphs have ~10cm left indent (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Only {sig_indent_count}/3 signature paragraphs have ~10cm indent")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Compound check — signature paragraphs have 10cm indent AND LEFT alignment
    # AND all non-signature paragraphs retain zero/no left indent (0.4 points)
    # This FAILS on initial (signature paragraphs have no indent at all),
    # PASSES on golden (signature paragraphs have 10cm + LEFT, others have 0)
    try:
        comp2_failures = 0

        # Sub-check 2a: Signature paragraphs have ~10cm indent AND LEFT alignment
        for idx in SIGNATURE_INDICES:
            para = paras[idx]
            pf = para.paragraph_format
            indent = pf.left_indent
            align = pf.alignment

            # Must have the 10cm indent (task-introduced change)
            has_indent = (indent is not None and abs(indent - CM_10_EMU) <= TOLERANCE_EMU)
            # Must have LEFT alignment (or inherited-LEFT which shows as None)
            has_left_align = (align is None or align == WD_PARAGRAPH_ALIGNMENT.LEFT)

            if not has_indent:
                print(f"FAIL: Component 2 — Para {idx} missing ~10cm indent (indent={indent})")
                comp2_failures += 1
            elif not has_left_align:
                print(f"FAIL: Component 2 — Para {idx} has ~10cm indent but alignment={align} (expected LEFT)")
                comp2_failures += 1
            else:
                print(f"INFO: Para {idx} — indent={indent} EMU (~10cm) AND alignment=LEFT: OK")

        # Sub-check 2b: Non-signature paragraphs have NOT gained unexpected indents
        for idx in range(len(paras)):
            if idx in SIGNATURE_INDICES:
                continue
            para = paras[idx]
            pf = para.paragraph_format
            indent = pf.left_indent
            if indent is not None and abs(indent) > TOLERANCE_EMU:
                print(f"FAIL: Component 2 — Para {idx} ('{para.text[:30]}') unexpectedly has indent={indent} EMU")
                comp2_failures += 1

        if comp2_failures == 0:
            print(f"PASS: Component 2 — Signature block fully formatted (10cm+LEFT) and others unchanged (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Compound check failed ({comp2_failures} sub-check(s) failed)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/office_memo.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
