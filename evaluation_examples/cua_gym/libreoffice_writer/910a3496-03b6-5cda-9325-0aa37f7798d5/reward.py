"""
Reward Script: Apply 'Strong Emphasis' character style to all 'MeridianPro' instances
Task ID: writer_biz_076
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Proportional credit for MeridianPro runs with 'Strong' char style
  Component 2 (0.3): All 12 instances have 'Strong' char style (perfect consistency)
  Component 3 (0.2): No MeridianPro run has stale direct italic formatting
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_076'
EXPECTED_COUNT = 12


def get_meridianpro_runs(doc):
    """Find all runs containing 'MeridianPro' and extract their style info."""
    results = []
    for i, para in enumerate(doc.paragraphs):
        for j, run in enumerate(para.runs):
            if 'MeridianPro' in run.text:
                # Extract character style from XML
                rPr = run._element.find(qn('w:rPr'))
                rStyle = rPr.find(qn('w:rStyle')) if rPr is not None else None
                style_val = rStyle.get(qn('w:val')) if rStyle is not None else None
                results.append({
                    'para': i,
                    'run': j,
                    'text': run.text,
                    'char_style': style_val,
                    'style_name': run.style.name,
                    'bold': run.bold,
                    'italic': run.italic,
                })
    return results


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

    runs_info = get_meridianpro_runs(doc)
    total_found = len(runs_info)
    print(f"INFO: Found {total_found} runs containing 'MeridianPro'")

    if total_found == 0:
        print("FAIL: No MeridianPro runs found in document")
        print("REWARD: 0.0")
        return 0.0

    # Count how many have 'Strong' character style applied
    strong_count = 0
    for r in runs_info:
        if r['char_style'] == 'Strong':
            strong_count += 1

    # Count how many have stale direct italic (should be removed when style applied)
    italic_count = 0
    for r in runs_info:
        if r['italic'] is True:
            italic_count += 1

    print(f"INFO: {strong_count}/{total_found} have 'Strong' char style")
    print(f"INFO: {italic_count}/{total_found} have direct italic formatting")

    # Component 1: Proportional credit for Strong-styled runs (0.5 points)
    # Score proportionally based on how many MeridianPro runs have the Strong style
    try:
        proportion = strong_count / max(total_found, EXPECTED_COUNT)
        comp1_score = round(0.5 * proportion, 2)
        if comp1_score > 0:
            print(f"PASS: Component 1 — {strong_count}/{total_found} runs with Strong style ({comp1_score} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 — No runs have 'Strong' character style")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All instances have Strong style (0.3 points)
    # Only awards if every single MeridianPro run has the Strong character style
    try:
        if strong_count == total_found and total_found >= EXPECTED_COUNT:
            print(f"PASS: Component 2 — All {total_found} instances have 'Strong' style ({0.3} pts)")
            total_score += 0.3
        else:
            missing = total_found - strong_count
            print(f"FAIL: Component 2 — {missing} instance(s) missing 'Strong' style "
                  f"(need all {EXPECTED_COUNT}, got {strong_count}/{total_found})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No stale direct italic formatting on MeridianPro runs (0.2 points)
    # In the initial file, some MeridianPro runs had direct italic. After applying
    # the Strong character style, those direct italic overrides should be cleared.
    try:
        meridian_italic = [r for r in runs_info if r['italic'] is True]
        if len(meridian_italic) == 0 and strong_count >= EXPECTED_COUNT:
            print(f"PASS: Component 3 — No stale italic on MeridianPro runs ({0.2} pts)")
            total_score += 0.2
        else:
            if strong_count < EXPECTED_COUNT:
                print(f"FAIL: Component 3 — Strong style not fully applied yet "
                      f"({strong_count}/{EXPECTED_COUNT})")
            else:
                print(f"FAIL: Component 3 — {len(meridian_italic)} runs still have direct italic")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
