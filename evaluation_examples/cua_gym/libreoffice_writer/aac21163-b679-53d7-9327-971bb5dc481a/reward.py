"""
Reward Script: Apply strikethrough to the penultimate (second-to-last) paragraph
Task ID: osworld_writer_strikethrough_last_para_005
Domain: libreoffice_writer
Scoring:
  Component 1 (0.7): All runs in paragraph index -2 (penultimate) have strikethrough=True
  Component 2 (0.3): The penultimate paragraph text content is preserved intact
                     (strikethrough applied without altering the text itself)
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_strikethrough_last_para_005'

# Ground truth: the known text of the penultimate paragraph from the task context
# (verified via VM exploration — paragraph 3 in a 5-paragraph document)
EXPECTED_PENULTIMATE_TEXT_START = 'Prior to the v2.8 release'


def verify_task(file_path):
    """
    Verify that the penultimate paragraph (second-to-last) has strikethrough
    applied to all its text runs, without modifying the text content.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify the document has at least 2 paragraphs
    paras = doc.paragraphs
    num_paras = len(paras)
    if num_paras < 2:
        print(f"CRITICAL: Document has {num_paras} paragraphs, expected at least 2")
        print("REWARD: 0.0")
        return 0.0

    # The penultimate paragraph is at index len-2
    penultimate_idx = num_paras - 2
    penultimate_para = paras[penultimate_idx]

    # Component 1: All runs in the penultimate paragraph have strikethrough=True (0.7 points)
    # This changes between initial_env (strike=None) and golden_env (strike=True).
    try:
        runs_with_text = [run for run in penultimate_para.runs if run.text.strip()]

        if len(runs_with_text) == 0:
            print(f"FAIL: Component 1 — Penultimate paragraph (index {penultimate_idx}) has no text runs")
        else:
            all_strike = all(run.font.strike is True for run in runs_with_text)
            if all_strike:
                print(f"PASS: Component 1 — All {len(runs_with_text)} run(s) in penultimate paragraph "
                      f"(index {penultimate_idx}) have strikethrough=True (0.7 pts)")
                total_score += 0.7
            else:
                non_strike_runs = [
                    run.text[:40] for run in runs_with_text if run.font.strike is not True
                ]
                print(f"FAIL: Component 1 — Not all runs in penultimate paragraph have strikethrough. "
                      f"Runs missing strikethrough: {non_strike_runs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The penultimate paragraph text content is preserved intact (0.3 points)
    # The strikethrough is a formatting change; the text itself must remain unchanged.
    # This is a sub-condition of the task: strikethrough was applied in-place.
    # In the initial env, Component 1 fails (no strikethrough), so this component
    # is only reachable together with Component 1 passing — making it a compound check
    # that together represents the correct golden state.
    # NOTE: We gate Component 2 on Component 1 passing to ensure initial_env scores 0.0.
    try:
        if total_score > 0.0:
            # Only award Component 2 points if Component 1 also passed
            full_text = penultimate_para.text
            if full_text.startswith(EXPECTED_PENULTIMATE_TEXT_START):
                print(f"PASS: Component 2 — Penultimate paragraph text preserved intact "
                      f"(starts with expected prefix, 0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Penultimate paragraph text does not start with expected prefix. "
                      f"Found: {full_text[:60]!r}")
        else:
            print(f"SKIP: Component 2 — Skipped because Component 1 did not pass")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
