"""
Reward Script: Change TOC Heading 1 entries to dark blue (#003366) font color
Task ID: writer_mt_089
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): 'toc 1' style font color is #003366
  Component 2 (0.3): All toc 1 paragraph runs display #003366
  Component 3 (0.3): All toc 2/toc 3 paragraph runs remain #000000 (black)
"""

import os

from docx import Document
from docx.shared import RGBColor
from math import sqrt

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_089'


def color_distance(c1, c2):
    """Euclidean distance between two RGBColor objects."""
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


TARGET_BLUE = RGBColor(0x00, 0x33, 0x66)   # #003366
TARGET_BLACK = RGBColor(0x00, 0x00, 0x00)   # #000000
COLOR_THRESHOLD = 15  # max acceptable Euclidean RGB distance


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

    # Collect TOC paragraphs by style
    toc1_paras = []
    toc2_paras = []
    toc3_paras = []
    for para in doc.paragraphs:
        sn = para.style.name if para.style else ''
        if sn == 'toc 1':
            toc1_paras.append(para)
        elif sn == 'toc 2':
            toc2_paras.append(para)
        elif sn == 'toc 3':
            toc3_paras.append(para)

    # Precondition: TOC entries must exist
    if not toc1_paras:
        print("FAIL: No toc 1 paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'toc 1' style font color is #003366 (0.4 points)
    try:
        toc1_style = doc.styles['toc 1']
        style_color = toc1_style.font.color.rgb if toc1_style.font.color and toc1_style.font.color.rgb else None
        if style_color is not None and color_distance(style_color, TARGET_BLUE) < COLOR_THRESHOLD:
            print(f"PASS: Component 1 - 'toc 1' style font color is {style_color} (close to #003366) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - 'toc 1' style font color is {style_color}, expected close to #003366")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All toc 1 paragraph runs display #003366 (0.3 points)
    try:
        toc1_blue_count = 0
        toc1_total_runs = 0
        for para in toc1_paras:
            for run in para.runs:
                if not run.text.strip():
                    continue
                toc1_total_runs += 1
                run_color = run.font.color.rgb if run.font.color and run.font.color.rgb else None
                if run_color is not None and color_distance(run_color, TARGET_BLUE) < COLOR_THRESHOLD:
                    toc1_blue_count += 1

        if toc1_total_runs > 0 and toc1_blue_count == toc1_total_runs:
            print(f"PASS: Component 2 - All {toc1_total_runs} toc 1 runs are dark blue (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - {toc1_blue_count}/{toc1_total_runs} toc 1 runs are dark blue")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: toc 1 is blue AND toc 2/toc 3 runs remain black (0.3 points)
    # This compound check anchors to the task change: only awards points when toc 1 IS blue
    # (so it fails on initial_env where toc 1 is still black)
    try:
        # First gate: toc 1 style must already be blue (anchored to task change)
        toc1_style_color = None
        try:
            toc1_style_check = doc.styles['toc 1']
            toc1_style_color = toc1_style_check.font.color.rgb if toc1_style_check.font.color and toc1_style_check.font.color.rgb else None
        except Exception:
            pass

        if toc1_style_color is None or color_distance(toc1_style_color, TARGET_BLUE) >= COLOR_THRESHOLD:
            print(f"FAIL: Component 3 - toc 1 style is not blue, so compound check fails")
        else:
            non_toc1_paras = toc2_paras + toc3_paras
            black_count = 0
            total_runs = 0
            for para in non_toc1_paras:
                for run in para.runs:
                    if not run.text.strip():
                        continue
                    total_runs += 1
                    run_color = run.font.color.rgb if run.font.color and run.font.color.rgb else None
                    if run_color is None or color_distance(run_color, TARGET_BLACK) < COLOR_THRESHOLD:
                        black_count += 1

            if total_runs > 0 and black_count == total_runs:
                print(f"PASS: Component 3 - toc 1 is blue AND all {total_runs} toc 2/toc 3 runs remain black (0.3 pts)")
                total_score += 0.3
            elif total_runs == 0:
                print(f"FAIL: Component 3 - No toc 2/toc 3 runs found")
            else:
                print(f"FAIL: Component 3 - {black_count}/{total_runs} toc 2/toc 3 runs are black")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
