"""
Reward Script: Extract code cells from Jupyter notebook and save as fastai_intro_code.py
Task ID: osworld_multi_apps_code_to_writer_file_007
Domain: libreoffice_writer / os
Scoring:
  Component 1 (0.4): fastai_intro_code.py exists on Desktop with a comment at the top
  Component 2 (0.3): File contains actual fastai code cells (fastai-specific code identifiers present)
  Component 3 (0.3): File has substantial content indicating multiple code cells were concatenated (>20 non-blank lines)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_007'
TARGET_FILE = '/home/user/Desktop/fastai_intro_code.py'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"FAIL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print(f"FAIL: File is empty at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File starts with a comment at the top noting syntax observations (0.4 points)
    # The task requires opening in Writer and noting any syntax issues (or noting there are none)
    # The golden file starts with "# No obvious syntax issues found" or similar comment
    try:
        non_empty_lines = [l for l in lines if l.strip()]
        if non_empty_lines:
            first_non_empty = non_empty_lines[0].strip()
            # Check that the first non-empty line is a Python comment
            if first_non_empty.startswith('#'):
                # Check it's a meaningful syntax observation (not just a blank comment)
                # Acceptable: "# No obvious syntax issues found" or notes about specific issues
                comment_text = first_non_empty[1:].strip().lower()
                if len(comment_text) > 3:  # Must have some content beyond just '#'
                    print(f"PASS: Component 1 — File starts with comment: '{first_non_empty}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — First comment is too short/empty: '{first_non_empty}'")
            else:
                print(f"FAIL: Component 1 — File does not start with a comment. First line: '{first_non_empty}'")
        else:
            print("FAIL: Component 1 — File has no non-empty lines")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains actual fastai code cells from the notebook (0.3 points)
    # The task asks to extract code cells from the fastai/fastbook Chapter 1 notebook.
    # Presence of fastai-specific identifiers confirms real code cells were extracted.
    try:
        fastai_indicators = [
            'fastai',
            'ImageDataLoaders',
            'vision_learner',
            'TextDataLoaders',
            'TabularDataLoaders',
            'CollabDataLoaders',
            'untar_data',
            'learn.fine_tune',
            'fastbook',
        ]
        found_indicators = [ind for ind in fastai_indicators if ind in content]
        if len(found_indicators) >= 3:
            print(f"PASS: Component 2 — fastai code identifiers found: {found_indicators[:5]} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Insufficient fastai code identifiers. Found: {found_indicators}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File has substantial content (multiple code cells concatenated) (0.3 points)
    # The task requires concatenating ALL code cells from a large notebook.
    # The golden file has 119 lines; we require at least 20 non-blank, non-comment-only lines.
    try:
        non_blank_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        code_line_count = len(non_blank_lines)
        if code_line_count >= 20:
            print(f"PASS: Component 3 — File has {code_line_count} code lines (>=20 expected) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — File has only {code_line_count} code lines, expected >=20")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against canonical artifact path
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
