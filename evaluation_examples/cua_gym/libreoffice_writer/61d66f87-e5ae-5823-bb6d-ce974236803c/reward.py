"""
Reward Script: Clear all character formatting from the second paragraph
Task ID: writer_txtfmt_041
Domain: libreoffice_writer
Scoring:
  Component 1: No bold formatting in paragraph 2 runs (0.4 pts)
  Component 2: No italic or underline formatting in paragraph 2 runs (0.3 pts)
  Component 3: No color formatting (no RGB color) in paragraph 2 runs (0.3 pts)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_txtfmt_041'

def verify_task(file_path):
    """
    Verify that all character formatting has been cleared from paragraph 2.
    Initial state: paragraph 2 has bold, italic, underline, red and blue colors.
    Golden state: paragraph 2 has all formatting cleared (bold=False, italic=False,
                  underline=False, no color).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify paragraph 2 (index 2, 0-based). It should contain the Spring Festival text.
    paragraphs = doc.paragraphs
    if len(paragraphs) < 3:
        print(f"FAIL: Expected at least 3 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    para2 = paragraphs[2]
    para2_text = para2.text
    print(f"INFO: Paragraph 2 text: {repr(para2_text[:80])}")
    print(f"INFO: Number of runs in paragraph 2: {len(para2.runs)}")

    # Verify this is the correct paragraph (contains Spring Festival content)
    if 'Spring Festival' not in para2_text and 'April 12th' not in para2_text:
        print(f"WARN: Paragraph 2 may not be the expected Spring Festival paragraph.")

    # Component 1: No bold formatting in any run of paragraph 2 (0.4 pts)
    # In initial_env, runs 1, 5, 9, 13 have bold=True.
    # In golden_env, the single run has bold=False.
    try:
        bold_runs = []
        for j, run in enumerate(para2.runs):
            # bold=True means explicitly bold; bold=None means inherited (not explicitly set bold)
            if run.font.bold is True:
                bold_runs.append((j, run.text[:30]))

        if len(bold_runs) == 0:
            print(f"PASS: Component 1 — No bold runs found in paragraph 2 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Found {len(bold_runs)} bold run(s) in paragraph 2: {bold_runs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No italic or underline formatting in any run of paragraph 2 (0.3 pts)
    # In initial_env, runs 3, 5, 11 have italic=True; runs 3, 7, 13 have underline=True.
    # In golden_env, the single run has italic=False and underline=False.
    try:
        italic_runs = []
        underline_runs = []
        for j, run in enumerate(para2.runs):
            if run.font.italic is True:
                italic_runs.append((j, run.text[:30]))
            if run.font.underline is True:
                underline_runs.append((j, run.text[:30]))

        if len(italic_runs) == 0 and len(underline_runs) == 0:
            print(f"PASS: Component 2 — No italic or underline runs found in paragraph 2 (0.3 pts)")
            total_score += 0.3
        else:
            if italic_runs:
                print(f"FAIL: Component 2 — Found {len(italic_runs)} italic run(s): {italic_runs}")
            if underline_runs:
                print(f"FAIL: Component 2 — Found {len(underline_runs)} underline run(s): {underline_runs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No explicit color formatting in any run of paragraph 2 (0.3 pts)
    # In initial_env, runs 1, 11 have red color (FF0000); runs 5, 13 have blue color (0000FF).
    # In golden_env, the single run has color=None (no explicit color = default/automatic).
    try:
        colored_runs = []
        for j, run in enumerate(para2.runs):
            try:
                rgb = run.font.color.rgb if run.font.color and run.font.color.type else None
                if rgb is not None:
                    colored_runs.append((j, run.text[:30], str(rgb)))
            except Exception:
                pass  # color.rgb may raise if type is not RGB

        if len(colored_runs) == 0:
            print(f"PASS: Component 3 — No explicit color found in paragraph 2 runs (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Found {len(colored_runs)} colored run(s): {colored_runs}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in a given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
