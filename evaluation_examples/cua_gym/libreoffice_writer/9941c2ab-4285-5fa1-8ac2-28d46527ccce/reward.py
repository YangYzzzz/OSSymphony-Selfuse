"""
Reward Script: Format trademark references with bold small caps
Task ID: writer_txtfmt_064
Domain: libreoffice_writer
Scoring:
  Component 1: Bold formatting applied to all 6 brand name occurrences (0.5 pts)
  Component 2: SmallCaps formatting applied to all 6 brand name occurrences (0.5 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_064'
FILE_PATH = f'{WORKDIR}/brand_guidelines.docx'

# Brand terms to check (each appears exactly twice per task spec)
BRAND_TERMS = ['Pinnacle Solutions', 'SmartFlow', 'DataBridge']


def has_small_caps(run):
    """
    Check if a run has SmallCaps formatting via XML inspection.
    The w:smallCaps element is present in w:rPr when SmallCaps is applied.
    When the element exists with no val attribute (or val='true'/'1'), it is enabled.
    When val='false' or '0', it is explicitly disabled.
    """
    rpr = run._element.find(qn('w:rPr'))
    if rpr is None:
        return False
    sc_elem = rpr.find(qn('w:smallCaps'))
    if sc_elem is None:
        return False
    val = sc_elem.get(qn('w:val'))
    # No val attribute means enabled (True by default)
    # val='false' or '0' means disabled
    if val is None:
        return True
    return val.lower() not in ('false', '0')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that all 6 brand name occurrences have bold=True AND SmallCaps applied.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all runs matching brand terms
    brand_runs = []
    for i, para in enumerate(doc.paragraphs):
        for j, run in enumerate(para.runs):
            if run.text in BRAND_TERMS:
                brand_runs.append((i, j, run))

    print(f"Found {len(brand_runs)} brand name runs (expected 6)")

    if len(brand_runs) == 0:
        print("FAIL: No brand name runs found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Bold formatting applied to all 6 brand name occurrences (0.5 points)
    # In the initial state, brand names have bold=None (not bold).
    # After task completion, they must have bold=True.
    try:
        bold_count = 0
        bold_details = []
        for (para_idx, run_idx, run) in brand_runs:
            is_bold = (run.bold is True) or (run.font.bold is True)
            if is_bold:
                bold_count += 1
                bold_details.append(f"Para {para_idx} '{run.text}': bold=True")
            else:
                bold_details.append(f"Para {para_idx} '{run.text}': bold={run.bold} (FAIL)")

        for detail in bold_details:
            print(detail)

        if bold_count == 6:
            print(f"PASS: Component 1 — All 6 brand name occurrences are bold (0.5 pts)")
            total_score += 0.5
        elif bold_count > 0:
            # Partial credit: award proportional points for partial bold application
            partial = round((bold_count / 6) * 0.5, 4)
            print(f"PARTIAL: Component 1 — {bold_count}/6 brand name occurrences are bold ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No brand name occurrences are bold (expected 6)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: SmallCaps formatting applied to all 6 brand name occurrences (0.5 points)
    # In the initial state, brand names have no SmallCaps element.
    # After task completion, they must have the w:smallCaps element present and enabled.
    try:
        sc_count = 0
        sc_details = []
        for (para_idx, run_idx, run) in brand_runs:
            is_sc = has_small_caps(run)
            if is_sc:
                sc_count += 1
                sc_details.append(f"Para {para_idx} '{run.text}': smallCaps=True")
            else:
                sc_details.append(f"Para {para_idx} '{run.text}': smallCaps=False (FAIL)")

        for detail in sc_details:
            print(detail)

        if sc_count == 6:
            print(f"PASS: Component 2 — All 6 brand name occurrences have SmallCaps (0.5 pts)")
            total_score += 0.5
        elif sc_count > 0:
            partial = round((sc_count / 6) * 0.5, 4)
            print(f"PARTIAL: Component 2 — {sc_count}/6 brand name occurrences have SmallCaps ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 2 — No brand name occurrences have SmallCaps (expected 6)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
