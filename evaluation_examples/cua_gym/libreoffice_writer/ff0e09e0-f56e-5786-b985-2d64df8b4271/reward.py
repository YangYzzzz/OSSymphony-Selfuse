"""
Reward Script: Remove blank paragraphs and add 18pt spacing after each remaining paragraph
Task ID: wrpara_047
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All blank paragraphs removed — exactly 12 content paragraphs, none blank
  Component 2 (0.3): All 12 paragraphs have space_after == 18pt
  Component 3 (0.3): Text content of content paragraphs is preserved
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_047'

# Expected first words of each content paragraph (for content preservation check)
EXPECTED_STARTS = [
    "Distinguished delegates",
    "We gather at a pivotal",
    "Let me begin with what",
    "But knowledge without action",
    "That is why I am announcing",
    "The initiative rests on three",
    "Critics will say this",
    "I also want to address",
    "Furthermore, we must ensure",
    "To the young people listening",
    "In closing, let me share",
    "The path forward will not",
]


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

    paragraphs = doc.paragraphs
    num_paras = len(paragraphs)
    blank_count = sum(1 for p in paragraphs if not p.text.strip())

    # Component 1: All blank paragraphs removed (0.4 points)
    # Initial has 23 paragraphs (12 content + 11 blank). Golden should have exactly 12, all non-blank.
    try:
        if num_paras == 12 and blank_count == 0:
            print(f"PASS: Component 1 — 12 non-blank paragraphs found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 12 non-blank paragraphs, found {num_paras} total with {blank_count} blank")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All remaining paragraphs have space_after == 18pt (0.3 points)
    # Initial has space_after=None for all paragraphs. Golden should have 18.0pt.
    try:
        content_paras = [p for p in paragraphs if p.text.strip()]
        if len(content_paras) == 0:
            print(f"FAIL: Component 2 — no content paragraphs found")
        else:
            correct_spacing = 0
            for p in content_paras:
                sa = p.paragraph_format.space_after
                if sa is not None and abs(sa.pt - 18.0) < 0.5:
                    correct_spacing += 1
            if correct_spacing == len(content_paras) and len(content_paras) >= 12:
                print(f"PASS: Component 2 — all {correct_spacing} paragraphs have 18pt spacing after (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — {correct_spacing}/{len(content_paras)} paragraphs have 18pt spacing after")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text content preserved AND blanks removed (0.3 points)
    # Compound check: only awards points when blanks are removed (task change)
    # AND the remaining paragraphs have the correct text content (data integrity).
    # This FAILS on initial_env because blank_count > 0, and PASSES on golden_env.
    try:
        if blank_count > 0:
            print(f"FAIL: Component 3 — {blank_count} blank paragraphs still present, content check skipped")
        elif num_paras != 12:
            print(f"FAIL: Component 3 — expected exactly 12 paragraphs, found {num_paras}")
        else:
            matches = 0
            for i, expected_start in enumerate(EXPECTED_STARTS):
                if i < len(paragraphs) and paragraphs[i].text.strip().startswith(expected_start):
                    matches += 1
            if matches == 12:
                print(f"PASS: Component 3 — blanks removed and all 12 content paragraphs preserved (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — {matches}/12 paragraphs match expected text starts")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
