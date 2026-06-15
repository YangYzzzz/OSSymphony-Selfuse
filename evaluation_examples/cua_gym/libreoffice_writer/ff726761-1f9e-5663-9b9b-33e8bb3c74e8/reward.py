"""
Reward Script: Change Heading 1 style font color to dark blue (#003366)
Task ID: osworld_writer_heading_styles_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Heading 1 style font color is dark blue #003366
  Component 2 (0.4): Compound — Heading 1 style is dark blue AND all 4 headings display it (no conflicting run overrides)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import RGBColor

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_heading_styles_003'

# Target color: dark blue #003366
TARGET_RGB = RGBColor(0x00, 0x33, 0x66)
TARGET_HEX = '003366'


def color_distance(rgb1, rgb2):
    """Euclidean distance in RGB color space. RGBColor is indexable: [0]=R, [1]=G, [2]=B."""
    return ((rgb1[0] - rgb2[0]) ** 2 +
            (rgb1[1] - rgb2[1]) ** 2 +
            (rgb1[2] - rgb2[2]) ** 2) ** 0.5


def verify_task(file_path):
    """
    Verify that the Heading 1 style font color has been changed to dark blue (#003366).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — gate check
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: Heading 1 style defines font color as #003366 (0.6 points) ---
    # This checks the style definition itself; must change from None to #003366
    try:
        h1_style = doc.styles['Heading 1']
        style_color = h1_style.font.color.rgb

        if style_color is not None:
            dist = color_distance(style_color, TARGET_RGB)
            if dist < 10:  # tolerance: allow minor encoding variation
                print(f"PASS: Component 1 — Heading 1 style color is #{str(style_color)} (target #{TARGET_HEX}), distance={dist:.1f} ({0.6} pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — Heading 1 style color is #{str(style_color)}, expected #{TARGET_HEX}, distance={dist:.1f}")
        else:
            print(f"FAIL: Component 1 — Heading 1 style color is None (not set), expected #{TARGET_HEX}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Heading 1 style color is dark blue AND all 4 headings effectively display it (0.4 points) ---
    # Compound check: requires that the style has the correct dark blue color (change introduced) AND
    # all 4 Heading 1 paragraphs do not have conflicting run-level color overrides that would override
    # the style color. Both sub-conditions must be true — this fails on initial_env because the style
    # color has not been changed.
    try:
        h1_style_check = doc.styles['Heading 1']
        style_color_check = h1_style_check.font.color.rgb

        # Sub-condition A: style color must be dark blue (this fails on initial env)
        style_ok = (style_color_check is not None and
                    color_distance(style_color_check, TARGET_RGB) < 10)

        # Sub-condition B: all 4 headings present with no conflicting run overrides
        h1_paras = [p for p in doc.paragraphs if p.style.name == 'Heading 1']
        count = len(h1_paras)
        conflicting_runs = []
        for para in h1_paras:
            for run in para.runs:
                run_color = run.font.color.rgb
                if run_color is not None:
                    dist = color_distance(run_color, TARGET_RGB)
                    if dist >= 10:
                        conflicting_runs.append(
                            f"'{para.text[:30]}' run color=#{str(run_color)}"
                        )

        headings_ok = (count == 4 and len(conflicting_runs) == 0)

        if style_ok and headings_ok:
            print(f"PASS: Component 2 — Heading 1 style is dark blue AND all {count} headings inherit it without run overrides ({0.4} pts)")
            total_score += 0.4
        elif not style_ok:
            print(f"FAIL: Component 2 — Heading 1 style color not set to dark blue (required for headings to display correctly)")
        elif not headings_ok:
            print(f"FAIL: Component 2 — {count} heading(s) found, or conflicting run overrides: {conflicting_runs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in this env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
