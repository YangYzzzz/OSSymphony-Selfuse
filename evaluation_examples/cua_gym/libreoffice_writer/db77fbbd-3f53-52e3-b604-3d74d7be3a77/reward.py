"""
Reward Script: Change all 'Heading 2' paragraphs to 'Heading 3' style
Task ID: writer_frd_012
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): No 'Heading 2' paragraphs remain
  Component 2 (0.4): Exactly 8 paragraphs now have 'Heading 3' style (progressive)
  Component 3 (0.2): Text content of heading paragraphs is preserved
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_012'

# Expected heading texts from the initial document (the 8 Heading 2 paragraphs)
EXPECTED_HEADING_TEXTS = [
    'Executive Summary',
    'Financial Performance',
    'Product Innovation and Development',
    'Market Expansion and Customer Growth',
    'Sustainability and Corporate Responsibility',
    'Talent and Organizational Development',
    'Risk Management and Governance',
    'Strategic Outlook for 2026',
]


def persist_app_state(domain: str):
    """Attempt to save any unsaved LibreOffice edits."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect style info for all paragraphs
    heading2_paras = []
    heading3_paras = []
    for para in doc.paragraphs:
        if para.style.name == 'Heading 2':
            heading2_paras.append(para.text)
        elif para.style.name == 'Heading 3':
            heading3_paras.append(para.text)

    # Component 1: No 'Heading 2' paragraphs remain (0.4 points)
    # In initial_env, there are 8 Heading 2 paras, so this FAILS on initial.
    # In golden_env, all are changed to Heading 3, so this PASSES on golden.
    try:
        num_heading2 = len(heading2_paras)
        if num_heading2 == 0:
            print(f"PASS: Component 1 -- No 'Heading 2' paragraphs remain (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- {num_heading2} 'Heading 2' paragraphs still present: {heading2_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 8 paragraphs with 'Heading 3' style (0.4 points, progressive)
    # In initial_env, there are 0 Heading 3 paras -> 0 points.
    # In golden_env, there should be 8 -> full 0.4 points.
    try:
        num_heading3 = len(heading3_paras)
        if num_heading3 >= 8:
            print(f"PASS: Component 2 -- Found {num_heading3} 'Heading 3' paragraphs (0.4 pts)")
            total_score += 0.4
        elif num_heading3 > 0:
            # Partial credit: proportional to how many were converted
            partial = 0.4 * (num_heading3 / 8.0)
            print(f"PARTIAL: Component 2 -- Found {num_heading3}/8 'Heading 3' paragraphs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No 'Heading 3' paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Text content of the 8 heading paragraphs is preserved (0.2 points)
    # This checks that Heading 3 paragraphs have the exact expected texts.
    # In initial_env, heading3_paras is empty -> 0 matches -> FAILS.
    # In golden_env, heading3_paras should contain all 8 expected texts -> PASSES.
    try:
        matched = 0
        for expected_text in EXPECTED_HEADING_TEXTS:
            if expected_text in heading3_paras:
                matched += 1

        if matched == 8:
            print(f"PASS: Component 3 -- All 8 heading texts preserved in 'Heading 3' paragraphs (0.2 pts)")
            total_score += 0.2
        elif matched > 0:
            partial = 0.2 * (matched / 8.0)
            print(f"PARTIAL: Component 3 -- {matched}/8 heading texts match in 'Heading 3' paragraphs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No expected heading texts found in 'Heading 3' paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state('libreoffice_writer')

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
