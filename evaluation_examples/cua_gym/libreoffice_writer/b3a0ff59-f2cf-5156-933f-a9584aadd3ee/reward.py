"""
Reward Script: Convert numbered list to bulleted list
Task ID: writer_lec_019
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Level 1 items use 'List Bullet' style
  Component 2 (0.3): Level 2 items use 'List Bullet 2' style
  Component 3 (0.3): All text content preserved exactly
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_019'

# Expected text content for each list paragraph (paragraphs index 2-9)
EXPECTED_TEXTS = [
    "Conduct comprehensive market research across all target demographics",
    "Develop brand positioning strategy for the Asia-Pacific region",
    "Identify key competitors and analyze their market share",
    "Define unique value propositions for each sub-market",
    "Design integrated digital advertising campaigns for Q3 and Q4",
    "Allocate budget across social media, search, and display channels",
    "Establish partnerships with regional influencers and content creators",
    "Set up quarterly performance review meetings with all stakeholders",
]

# Expected levels: which paragraphs (by list index 0-7) should be level 1 vs level 2
# Level 1 (List Bullet): indices 0, 1, 4, 6, 7
# Level 2 (List Bullet 2): indices 2, 3, 5
LEVEL1_INDICES = {0, 1, 4, 6, 7}
LEVEL2_INDICES = {2, 3, 5}


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Extract list paragraphs (skip heading and blank paragraph)
    list_paras = []
    for p in doc.paragraphs:
        style_name = p.style.name if p.style else ''
        if style_name.startswith('List Bullet') or style_name.startswith('List Number'):
            list_paras.append(p)

    if len(list_paras) != 8:
        print(f"FAIL: Expected 8 list paragraphs, found {len(list_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Level 1 items use 'List Bullet' style (0.4 points)
    try:
        level1_correct = 0
        level1_total = len(LEVEL1_INDICES)
        for idx in LEVEL1_INDICES:
            style_name = list_paras[idx].style.name if list_paras[idx].style else ''
            if style_name == 'List Bullet':
                level1_correct += 1
            else:
                print(f"FAIL: List item {idx} style is '{style_name}', expected 'List Bullet'")

        if level1_correct == level1_total:
            print(f"PASS: Component 1 -- All {level1_total} level-1 items use 'List Bullet' (0.4 pts)")
            total_score += 0.4
        elif level1_correct > 0:
            partial = 0.4 * (level1_correct / level1_total)
            print(f"PARTIAL: Component 1 -- {level1_correct}/{level1_total} level-1 items correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No level-1 items use 'List Bullet'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Level 2 items use 'List Bullet 2' style (0.3 points)
    try:
        level2_correct = 0
        level2_total = len(LEVEL2_INDICES)
        for idx in LEVEL2_INDICES:
            style_name = list_paras[idx].style.name if list_paras[idx].style else ''
            if style_name == 'List Bullet 2':
                level2_correct += 1
            else:
                print(f"FAIL: List item {idx} style is '{style_name}', expected 'List Bullet 2'")

        if level2_correct == level2_total:
            print(f"PASS: Component 2 -- All {level2_total} level-2 items use 'List Bullet 2' (0.3 pts)")
            total_score += 0.3
        elif level2_correct > 0:
            partial = 0.3 * (level2_correct / level2_total)
            print(f"PARTIAL: Component 2 -- {level2_correct}/{level2_total} level-2 items correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No level-2 items use 'List Bullet 2'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All text content preserved AND all items are bullet-styled (0.3 points)
    # This is a compound check: text must match AND styles must be bullet (not numbered).
    # On initial_env, styles are List Number/List Number 2, so this FAILS.
    try:
        text_correct = 0
        text_total = len(EXPECTED_TEXTS)
        non_bullet_count = 0
        for idx, expected in enumerate(EXPECTED_TEXTS):
            actual = list_paras[idx].text.strip()
            style_name = list_paras[idx].style.name if list_paras[idx].style else ''
            if actual == expected:
                text_correct += 1
            else:
                print(f"FAIL: Text mismatch at item {idx}: expected '{expected[:40]}...', got '{actual[:40]}...'")
            if not style_name.startswith('List Bullet'):
                non_bullet_count += 1

        if text_correct == text_total and non_bullet_count == 0:
            print(f"PASS: Component 3 -- All {text_total} texts preserved and all styles are bullet (0.3 pts)")
            total_score += 0.3
        elif text_correct == text_total and non_bullet_count > 0:
            print(f"FAIL: Component 3 -- Texts preserved but {non_bullet_count} styles not bullet yet")
        else:
            print(f"FAIL: Component 3 -- {text_correct}/{text_total} texts match, non_bullet={non_bullet_count}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved edits, then verify
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
