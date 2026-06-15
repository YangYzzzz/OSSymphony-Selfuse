"""
Reward Script: Apply strikethrough formatting to the third sentence in the second paragraph
Task ID: osworld_writer_strikethrough_last_para_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Third sentence run (run index 2) in the second paragraph has strikethrough applied
  Component 2 (0.4): Compound check — third sentence run has strikethrough AND it contains the correct
                     sentence text AND no other runs in that paragraph have unwanted strikethrough
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_strikethrough_last_para_003'

# Expected third sentence text fragment
THIRD_SENTENCE_FRAGMENT = 'It was proposed that the budget allocation for the Beta testing environment be reduced by 15%'


def verify_task(file_path):
    """
    Verify task completion: strikethrough applied to the third sentence of the second paragraph.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have at least 3 content paragraphs
    # Paragraph layout: [0]=title, [1]=first paragraph, [2]=second paragraph, [3]=third paragraph
    try:
        paras = doc.paragraphs
        if len(paras) < 3:
            print(f"CRITICAL: Expected at least 3 paragraphs, found {len(paras)}")
            print("REWARD: 0.0")
            return 0.0

        # Second paragraph is at index 2 (title=0, first_para=1, second_para=2)
        second_para = paras[2]
        runs = second_para.runs

        if len(runs) < 3:
            print(f"CRITICAL: Second paragraph expected at least 3 runs (sentences), found {len(runs)}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Structure check failed: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Third sentence run (index 2) has strikethrough applied (0.6 points)
    # This is the core task change: run index 2 goes from strike=None/False to strike=True
    try:
        run_3 = second_para.runs[2]
        if run_3.font.strike is True:
            print(f"PASS: Component 1 — Run 2 (third sentence) has strikethrough=True (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Expected strikethrough=True on third sentence run, got: {run_3.font.strike}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Compound check — third sentence run has strikethrough AND contains the correct
    # sentence text AND no other runs in the paragraph have unwanted strikethrough (0.4 points)
    # This verifies: (a) correct sentence was targeted, (b) only that sentence was formatted
    # All three sub-conditions must be true for this component to pass
    try:
        run_3 = second_para.runs[2]
        run_3_has_strike = run_3.font.strike is True
        run_3_text_correct = THIRD_SENTENCE_FRAGMENT in run_3.text

        # Count surrounding runs that have unwanted strikethrough
        unexpected_strike_count = sum(
            1 for idx in range(len(second_para.runs))
            if idx != 2 and second_para.runs[idx].font.strike is True
        )
        surrounding_clean = (unexpected_strike_count == 0)

        if run_3_has_strike and run_3_text_correct and surrounding_clean:
            print(f"PASS: Component 2 — Third sentence has strikethrough, correct text, and no unwanted strikes (0.4 pts)")
            total_score += 0.4
        else:
            reasons = []
            if not run_3_has_strike:
                reasons.append("third sentence run does not have strikethrough")
            if not run_3_text_correct:
                reasons.append(f"third sentence run text does not match expected (got: '{run_3.text[:50]}')")
            if not surrounding_clean:
                reasons.append(f"{unexpected_strike_count} other run(s) have unexpected strikethrough")
            print(f"FAIL: Component 2 — {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
