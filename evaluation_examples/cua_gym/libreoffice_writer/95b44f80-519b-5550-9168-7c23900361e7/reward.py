"""
Reward Script: Apply outline text effect to the chapter title 'Chapter 1: The Beginning'
Task ID: writer_txtfmt_026
Domain: libreoffice_writer
Scoring:
  Component 1 (0.7): Outline text effect is enabled on 'Chapter 1: The Beginning'
  Component 2 (0.3): Outline is enabled AND font properties preserved (Georgia, 18pt, Bold)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_026'
FILE_NAME = 'novel_draft.docx'

# Namespace for direct XML checks
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_outline_enabled(run):
    """
    Check if outline effect is truly enabled for a run.
    In OOXML, <w:outline/> with no val attribute means enabled (True).
    <w:outline w:val='0'/> means explicitly disabled (False).
    python-docx's run.font.outline correctly returns True/False/None.
    We use it directly but also verify via XML to be explicit.
    """
    rPr = run._element.find(f'{{{W_NS}}}rPr')
    if rPr is None:
        return False
    outline_elem = rPr.find(f'{{{W_NS}}}outline')
    if outline_elem is None:
        return False
    val = outline_elem.get(f'{{{W_NS}}}val')
    # val=None means the element is present without a val attribute => outline is ON
    # val='0' or val='false' means explicitly turned OFF
    return val not in ('0', 'false')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Apply outline text effect to 'Chapter 1: The Beginning'.
    Ground truth: outline_effect=True, font/size/bold unchanged.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the chapter title paragraph
    chapter_para = None
    for para in doc.paragraphs:
        if para.text.strip() == 'Chapter 1: The Beginning':
            chapter_para = para
            break

    if chapter_para is None:
        print("FAIL: Paragraph 'Chapter 1: The Beginning' not found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Get the first (and only) run of the chapter title
    chapter_runs = [r for r in chapter_para.runs if r.text.strip()]
    if not chapter_runs:
        print("FAIL: No runs found in 'Chapter 1: The Beginning' paragraph")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # We check properties on all runs containing the chapter title text
    # (typically just one run)

    # Component 1: Outline text effect is enabled on 'Chapter 1: The Beginning' (0.7 points)
    # This FAILS on initial (outline has w:val='0') and PASSES on golden (outline element has no val)
    try:
        outline_enabled_all = all(get_outline_enabled(run) for run in chapter_runs)
        if outline_enabled_all:
            print("PASS: Component 1 — Outline text effect is enabled on 'Chapter 1: The Beginning' (0.7 pts)")
            total_score += 0.7
        else:
            # Provide detailed diagnostic
            for i, run in enumerate(chapter_runs):
                enabled = get_outline_enabled(run)
                docx_val = run.font.outline
                print(f"FAIL: Component 1 — Run {i} '{run.text[:30]}': outline_enabled={enabled}, "
                      f"font.outline={docx_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Outline is enabled AND font properties preserved (Georgia, 18pt, Bold) (0.3 points)
    # This is a compound check — it FAILS on initial because outline is not enabled.
    # It only PASSES on golden when outline is True AND the original font properties are preserved.
    try:
        # Collect per-run results; pass only if ALL runs satisfy the compound condition
        failing_runs = []
        for i, run in enumerate(chapter_runs):
            # Check outline (must be enabled — already checked in Component 1, but recheck here)
            outline_ok = get_outline_enabled(run)
            # Check font name
            font_name_ok = run.font.name == 'Georgia'
            # Check font size (18pt = Pt(18))
            font_size_ok = run.font.size is not None and abs(run.font.size.pt - 18.0) < 0.5
            # Check bold
            bold_ok = run.font.bold is True

            if not (outline_ok and font_name_ok and font_size_ok and bold_ok):
                failing_runs.append(
                    f"Run {i}: outline={outline_ok}, "
                    f"font_name={run.font.name}(expected Georgia), "
                    f"size={run.font.size.pt if run.font.size else None}pt(expected 18.0), "
                    f"bold={run.font.bold}(expected True)"
                )

        if not failing_runs:
            print("PASS: Component 2 — Outline enabled AND font preserved (Georgia, 18pt, Bold) (0.3 pts)")
            total_score += 0.3
        else:
            for msg in failing_runs:
                print(f"FAIL: Component 2 — {msg}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
