"""
Reward Script: Apply alternating line spacing to 4 paragraphs
Task ID: osworld_writer_line_spacing_per_paragraph_006
Domain: libreoffice_writer
Scoring:
  Component 1: Alternating pair (para 1 = 1.0, para 2 = 1.5) — 0.5 pts
  Component 2: Alternating pair (para 3 = 1.0, para 4 = 1.5) — 0.5 pts
Total: 1.0

Note: Each component checks an odd-even pair together, so it FAILS on initial_env
(all paragraphs start at 1.0) and PASSES on golden_env (p2 and p4 changed to 1.5).
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_line_spacing_per_paragraph_006'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Task: Apply alternating line spacing to 4 paragraphs in an employee handbook.
    - Paragraph 1 (odd): single spacing (1.0)
    - Paragraph 2 (even): 1.5x spacing (1.5)
    - Paragraph 3 (odd): single spacing (1.0)
    - Paragraph 4 (even): 1.5x spacing (1.5)

    Initial state: all paragraphs use 1.0 spacing.
    Golden state: paragraphs 2 and 4 changed to 1.5 spacing.

    Each scoring component checks an odd+even pair together,
    ensuring initial_env scores 0.0 (even paragraphs unchanged at 1.0).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have exactly 4 paragraphs
    paragraphs = doc.paragraphs
    if len(paragraphs) != 4:
        print(f"PRECONDITION FAIL: Expected 4 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: First odd-even pair — paragraph 1 at 1.0 AND paragraph 2 at 1.5 (0.5 points)
    # This FAILS on initial_env (p2 is still 1.0) → PASSES on golden_env (p2 changed to 1.5)
    try:
        p1_ls = paragraphs[0].paragraph_format.line_spacing
        p2_ls = paragraphs[1].paragraph_format.line_spacing

        # p1 should be single (1.0 or None, which inherits default single spacing)
        p1_single = (p1_ls == 1.0 or p1_ls is None)
        # p2 should be 1.5x (explicitly set)
        p2_one_five = (p2_ls == 1.5)

        if p1_single and p2_one_five:
            print(f"PASS: Component 1 — Paragraph 1 has single spacing ({p1_ls}) "
                  f"and paragraph 2 has 1.5x spacing ({p2_ls}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected p1=1.0 and p2=1.5, "
                  f"found p1={p1_ls}, p2={p2_ls}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Second odd-even pair — paragraph 3 at 1.0 AND paragraph 4 at 1.5 (0.5 points)
    # This FAILS on initial_env (p4 is still 1.0) → PASSES on golden_env (p4 changed to 1.5)
    try:
        p3_ls = paragraphs[2].paragraph_format.line_spacing
        p4_ls = paragraphs[3].paragraph_format.line_spacing

        # p3 should be single (1.0 or None)
        p3_single = (p3_ls == 1.0 or p3_ls is None)
        # p4 should be 1.5x (explicitly set)
        p4_one_five = (p4_ls == 1.5)

        if p3_single and p4_one_five:
            print(f"PASS: Component 2 — Paragraph 3 has single spacing ({p3_ls}) "
                  f"and paragraph 4 has 1.5x spacing ({p4_ls}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected p3=1.0 and p4=1.5, "
                  f"found p3={p3_ls}, p4={p4_ls}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
