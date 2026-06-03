"""
Reward Script: Format the document title with multiple effects
Task ID: writer_txtfmt_056
Domain: libreoffice_writer
Scoring:
  Component 1: Shadow effect enabled on title run              (0.25 pts)
  Component 2: Bold enabled on title run                       (0.25 pts)
  Component 3: Font family Arial AND size 22pt on title run    (0.25 pts)
  Component 4: Font color #00008B (dark blue) on title run     (0.25 pts)
  Total: 1.0

Ground truth (from task_config.json context):
  - shadow_effect=True
  - bold=True
  - font_size=22pt
  - font_family='Arial'
  - font_color=#00008B
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_056'
TITLE_TEXT = 'CORPORATE GOVERNANCE REPORT'

def verify_task(file_path):
    """
    Verify task completion: title paragraph 'CORPORATE GOVERNANCE REPORT'
    must have shadow=True, bold=True, Arial 22pt, and dark blue #00008B color.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load document — if it fails, the task is incomplete
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the title paragraph (first paragraph with the expected text)
    title_para = None
    for para in doc.paragraphs:
        if para.text.strip() == TITLE_TEXT:
            title_para = para
            break

    if title_para is None:
        print(f"FAIL: Title paragraph '{TITLE_TEXT}' not found in document.")
        print("REWARD: 0.0")
        return 0.0

    # Collect all runs in the title paragraph that have non-empty text
    title_runs = [run for run in title_para.runs if run.text.strip()]
    if not title_runs:
        print("FAIL: Title paragraph has no non-empty runs.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Shadow effect enabled (0.25 points)
    # Initial: run.font.shadow is None (no shadow)
    # Golden:  run.font.shadow is True (shadow applied)
    try:
        shadow_ok = all(run.font.shadow is True for run in title_runs)
        if shadow_ok:
            print(f"PASS: Component 1 — Shadow effect is enabled on title (0.25 pts)")
            total_score += 0.25
        else:
            shadow_vals = [run.font.shadow for run in title_runs]
            print(f"FAIL: Component 1 — Shadow not enabled on title; shadow values: {shadow_vals}")
    except Exception as e:
        print(f"ERROR: Component 1 — Shadow check failed: {e}")

    # Component 2: Bold enabled (0.25 points)
    # Initial: run.font.bold is False
    # Golden:  run.font.bold is True
    try:
        bold_ok = all(run.font.bold is True for run in title_runs)
        if bold_ok:
            print(f"PASS: Component 2 — Bold is enabled on title (0.25 pts)")
            total_score += 0.25
        else:
            bold_vals = [run.font.bold for run in title_runs]
            print(f"FAIL: Component 2 — Bold not enabled on title; bold values: {bold_vals}")
    except Exception as e:
        print(f"ERROR: Component 2 — Bold check failed: {e}")

    # Component 3: Font family is Arial AND size is 22pt (0.25 points)
    # Initial: font.name='Times New Roman', size=14pt
    # Golden:  font.name='Arial', size=22pt
    try:
        font_name_ok = all(run.font.name == 'Arial' for run in title_runs)
        font_size_ok = all(
            run.font.size is not None and abs(run.font.size.pt - 22.0) < 0.5
            for run in title_runs
        )
        if font_name_ok and font_size_ok:
            print(f"PASS: Component 3 — Font is Arial 22pt on title (0.25 pts)")
            total_score += 0.25
        else:
            names = [run.font.name for run in title_runs]
            sizes = [run.font.size.pt if run.font.size else None for run in title_runs]
            if not font_name_ok:
                print(f"FAIL: Component 3 — Font name not Arial; found: {names}")
            if not font_size_ok:
                print(f"FAIL: Component 3 — Font size not 22pt; found: {sizes}")
    except Exception as e:
        print(f"ERROR: Component 3 — Font name/size check failed: {e}")

    # Component 4: Font color is #00008B (dark blue) (0.25 points)
    # Initial: color.rgb=000000 (black)
    # Golden:  color.rgb=00008B (dark blue)
    try:
        target_r, target_g, target_b = 0x00, 0x00, 0x8B
        failed_colors = []
        for run in title_runs:
            rgb = run.font.color.rgb
            if rgb is None:
                failed_colors.append(f"'{run.text[:20]}' -> None")
            else:
                r, g, b = rgb[0], rgb[1], rgb[2]
                # Use a small tolerance (<=5 per channel) for color matching
                if abs(r - target_r) > 5 or abs(g - target_g) > 5 or abs(b - target_b) > 5:
                    failed_colors.append(f"'{run.text[:20]}' -> #{r:02X}{g:02X}{b:02X}")
        if not failed_colors:
            print(f"PASS: Component 4 — Font color is #00008B (dark blue) on title (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected #00008B; mismatches: {failed_colors}")
    except Exception as e:
        print(f"ERROR: Component 4 — Color check failed: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Canonical artifact path on the VM
file_path = f'{WORKDIR}/governance_report.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
