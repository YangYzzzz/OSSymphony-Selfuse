"""
Reward Script: Apply a drop cap of 2 lines to the opening paragraph of each chapter section
Task ID: writer_para_051
Domain: libreoffice_writer
Scoring:
  Component 1: Paragraph 3 (first paragraph of Part One) has drop cap dropCap='drop', lines='2' (0.4 pts)
  Component 2: Paragraph 6 (first paragraph of Part Two) has drop cap dropCap='drop', lines='2' (0.4 pts)
  Component 3: All other paragraphs have no drop caps (0.2 pts)
Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_para_051'

# These are the expected text prefixes of the two section-opening paragraphs
PARA2_PREFIX = 'Behind the bustling streets'   # first paragraph of Part One
PARA5_PREFIX = 'In 2018, a group'              # first paragraph of Part Two


def get_drop_cap_info(para):
    """
    Return (dropCap, lines) from a paragraph's framePr element, or (None, None) if absent.
    """
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None, None
    framePr = pPr.find(qn('w:framePr'))
    if framePr is None:
        return None, None
    drop_cap = framePr.get(qn('w:dropCap'))
    lines = framePr.get(qn('w:lines'))
    return drop_cap, lines


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Sanity check: expect exactly 7 paragraphs
    if len(paragraphs) != 7:
        print(f"WARN: Expected 7 paragraphs, found {len(paragraphs)} — proceeding anyway")

    # Component 1: Paragraph index 2 ("Behind the bustling streets...") has drop cap
    # with dropCap='drop' and lines='2'. Fails on initial (no drop caps), passes on golden.
    # (0.4 points)
    try:
        para2 = paragraphs[2]
        if not para2.text.startswith(PARA2_PREFIX):
            print(f"FAIL: Component 1 — Para[2] text prefix mismatch: {para2.text[:40]!r}")
        else:
            drop_cap, lines = get_drop_cap_info(para2)
            if drop_cap == 'drop' and lines == '2':
                print(f"PASS: Component 1 — Para[2] ('{PARA2_PREFIX}') has dropCap='drop', lines='2' (0.4 pts)")
                total_score += 0.4
            else:
                print(
                    f"FAIL: Component 1 — Para[2] drop cap expected dropCap='drop', lines='2', "
                    f"found dropCap={drop_cap!r}, lines={lines!r}"
                )
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph index 5 ("In 2018, a group...") has drop cap
    # with dropCap='drop' and lines='2'. Fails on initial (no drop caps), passes on golden.
    # (0.4 points)
    try:
        para5 = paragraphs[5]
        if not para5.text.startswith(PARA5_PREFIX):
            print(f"FAIL: Component 2 — Para[5] text prefix mismatch: {para5.text[:40]!r}")
        else:
            drop_cap, lines = get_drop_cap_info(para5)
            if drop_cap == 'drop' and lines == '2':
                print(f"PASS: Component 2 — Para[5] ('{PARA5_PREFIX}') has dropCap='drop', lines='2' (0.4 pts)")
                total_score += 0.4
            else:
                print(
                    f"FAIL: Component 2 — Para[5] drop cap expected dropCap='drop', lines='2', "
                    f"found dropCap={drop_cap!r}, lines={lines!r}"
                )
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Compound integrity check — BOTH target paragraphs have drop caps AND
    # all other paragraphs (indices 0, 1, 3, 4, 6) have NO drop cap.
    # This check is anchored to the task change: it only passes when the task is complete
    # (drop caps added to targets) AND no collateral changes were made to non-targets.
    # Fails on initial (no drop caps anywhere), passes only on golden.
    # (0.2 points)
    try:
        # Sub-check A: both target paragraphs have drop caps (prerequisite for this component)
        para2_ok = get_drop_cap_info(paragraphs[2]) == ('drop', '2')
        para5_ok = get_drop_cap_info(paragraphs[5]) == ('drop', '2')

        # Sub-check B: non-target paragraphs are clean
        non_target_indices = [0, 1, 3, 4, 6]
        stray_drop_caps = []
        for idx in non_target_indices:
            if idx < len(paragraphs):
                drop_cap, _ = get_drop_cap_info(paragraphs[idx])
                if drop_cap is not None:
                    stray_drop_caps.append((idx, paragraphs[idx].text[:30]))

        if para2_ok and para5_ok and not stray_drop_caps:
            print("PASS: Component 3 — Both targets have drop caps and no stray drop caps on non-targets (0.2 pts)")
            total_score += 0.2
        elif not para2_ok or not para5_ok:
            print(
                f"FAIL: Component 3 — Target paragraphs incomplete: para2_ok={para2_ok}, para5_ok={para5_ok}"
            )
        else:
            print(
                f"FAIL: Component 3 — Unexpected drop caps on non-target paragraphs: {stray_drop_caps}"
            )
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the task artifact
file_path = f'{WORKDIR}/magazine_article.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
