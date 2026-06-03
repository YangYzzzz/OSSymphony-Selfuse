"""
Reward Script: Bold, underline, and blue-color all 8 occurrences of 'API endpoint'
Task ID: osworld_writer_text_formatting_basic_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 8 target 'API endpoint' runs are bold AND underlined
  Component 2 (0.5): All 8 target 'API endpoint' runs have blue font color (0000FF)

  Target runs: exactly 8 runs whose text does NOT start with 'API endpoint:'
  (excludes the pre-existing glossary label "API endpoint: " which was already bold)
"""

import os

from docx import Document
from docx.shared import RGBColor

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_text_formatting_basic_004'

# Blue target: 0x0000FF
BLUE_TUPLE = (0, 0, 255)


def color_distance(rgb1, rgb2):
    """Euclidean distance between two RGB tuples."""
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — gate check
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all 'API endpoint' runs that are TARGET runs.
    # Target: runs whose text contains 'API endpoint' but does NOT start with 'API endpoint:'
    # (the glossary label "API endpoint: " is pre-existing bold and should be excluded)
    target_runs = []  # expected: 8

    try:
        for i, para in enumerate(doc.paragraphs):
            for run in para.runs:
                if 'API endpoint' in run.text:
                    # Exclude glossary label "API endpoint: " (has trailing colon)
                    if not run.text.strip().startswith('API endpoint:'):
                        target_runs.append((i, run))
    except Exception as e:
        print(f"ERROR: Could not iterate paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(target_runs)} target 'API endpoint' runs (expected 8)")

    # -------------------------------------------------------------------
    # Component 1: All 8 target runs are bold AND underlined (0.5 points)
    # This should FAIL on initial (none are bold+underlined)
    # and PASS on golden (all 8 are bold+underlined).
    # -------------------------------------------------------------------
    try:
        if len(target_runs) == 0:
            print("FAIL: Component 1 — no target 'API endpoint' runs found")
        else:
            bold_underline_count = 0
            fail_details = []
            for (para_idx, run) in target_runs:
                is_bold = run.bold is True
                is_underline = run.underline is True
                if is_bold and is_underline:
                    bold_underline_count += 1
                else:
                    fail_details.append(
                        f"  Para {para_idx}: bold={run.bold}, underline={run.underline}"
                    )

            if bold_underline_count == 8 and len(target_runs) == 8:
                print(f"PASS: Component 1 — all 8 target runs are bold and underlined (0.5 pts)")
                total_score += 0.5
            elif bold_underline_count > 0:
                # Proportional partial credit for partial formatting
                partial = round(0.5 * (bold_underline_count / 8), 4)
                for d in fail_details:
                    print(d)
                print(f"PARTIAL: Component 1 — {bold_underline_count}/8 runs bold+underlined")
                if partial > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 1 — 0/8 runs are bold and underlined")
                for d in fail_details:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: All 8 target runs have blue font color (0x0000FF) (0.5 points)
    # This should FAIL on initial (all are black 000000)
    # and PASS on golden (all 8 are blue 0000FF).
    # -------------------------------------------------------------------
    try:
        if len(target_runs) == 0:
            print("FAIL: Component 2 — no target 'API endpoint' runs found")
        else:
            blue_count = 0
            fail_details = []
            for (para_idx, run) in target_runs:
                rgb = run.font.color.rgb
                if rgb is not None:
                    # RGBColor is a tuple-like: access by index
                    dist = color_distance((rgb[0], rgb[1], rgb[2]), BLUE_TUPLE)
                    if dist < 30:
                        blue_count += 1
                    else:
                        fail_details.append(
                            f"  Para {para_idx}: color={rgb} (dist_from_blue={dist:.1f})"
                        )
                else:
                    fail_details.append(
                        f"  Para {para_idx}: color=None (not set)"
                    )

            if blue_count == 8 and len(target_runs) == 8:
                print(f"PASS: Component 2 — all 8 target runs have blue color (0.5 pts)")
                total_score += 0.5
            elif blue_count > 0:
                partial = round(0.5 * (blue_count / 8), 4)
                for d in fail_details:
                    print(d)
                print(f"PARTIAL: Component 2 — {blue_count}/8 runs have blue color")
                if partial > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 2 — 0/8 runs have blue color")
                for d in fail_details:
                    print(d)
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
