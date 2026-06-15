"""
Reward Script: Recipe steps spacing task
Task ID: osworld_writer_spacing_010
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): 8 cooking steps split into individual paragraphs (not one block)
  Component 2 (0.3): At least 6 empty paragraphs separating consecutive cooking steps
  Component 3 (0.3): Serving suggestions paragraph is present and unchanged at end
"""

import os
import re

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spacing_010'

# The 8 expected cooking step sentences (ground truth from task context)
EXPECTED_STEPS = [
    'Preheat the oven to 375 degrees Fahrenheit.',
    'Grease a 9x13 baking pan thoroughly.',
    'Mix the dry ingredients in a large bowl.',
    'Brown the ground beef with onion and garlic in a skillet.',
    'Simmer the meat sauce for 20 minutes over medium heat.',
    'Layer noodles, ricotta mixture, meat sauce, and mozzarella cheese.',
    'Repeat layers until all ingredients are used, finishing with cheese.',
    'Bake covered with foil for 45 minutes, then uncovered for 15 minutes.',
]

# The serving suggestions paragraph starts with this prefix
SERVING_PREFIX = 'Serving suggestions:'


def persist_app_state():
    """Attempt to save LibreOffice Writer state before verification."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. The first paragraph (block of 8 cooking steps) be split into 8 individual paragraphs
    2. An empty paragraph inserted after each step to visually separate them
    3. The serving suggestions paragraph must remain unchanged at the end
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    para_texts = [p.text for p in paragraphs]
    print(f"INFO: Document has {len(paragraphs)} paragraphs total")
    print(f"INFO: Paragraph texts: {para_texts}")

    # --------------------------------------------------------------------------
    # Component 1: Each of the 8 cooking steps exists as a separate paragraph (0.4 points)
    # In the initial state all 8 steps are crammed into one paragraph.
    # This component passes ONLY when the steps have been split out.
    # --------------------------------------------------------------------------
    try:
        found_steps = 0
        for step in EXPECTED_STEPS:
            # Check if any paragraph's text equals this step (stripped)
            for p in paragraphs:
                if p.text.strip() == step.strip():
                    found_steps += 1
                    break

        if found_steps == len(EXPECTED_STEPS):
            print(f"PASS: Component 1 — All {len(EXPECTED_STEPS)} cooking steps found as individual paragraphs (0.4 pts)")
            total_score += 0.4
        elif found_steps > 0:
            # Partial: some steps split but not all
            partial = round((found_steps / len(EXPECTED_STEPS)) * 0.4, 3)
            print(f"PARTIAL: Component 1 — {found_steps}/{len(EXPECTED_STEPS)} steps found as individual paragraphs "
                  f"(awarding {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No cooking steps found as individual paragraphs (0 pts). "
                  f"Steps are still in one block or do not match expected text.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --------------------------------------------------------------------------
    # Component 2: Empty paragraphs inserted between consecutive cooking steps (0.3 points)
    # We expect at least 6 empty paragraphs that fall between consecutive step paragraphs.
    # In initial state there are no empty paragraphs separating the steps.
    # --------------------------------------------------------------------------
    try:
        # Build an index mapping each step text to its paragraph index
        step_positions = {}
        for i, p in enumerate(paragraphs):
            text = p.text.strip()
            for j, step in enumerate(EXPECTED_STEPS):
                if text == step.strip():
                    step_positions[j] = i

        # Count how many consecutive step pairs have at least one empty paragraph between them
        pairs_with_empty = 0
        total_consecutive_pairs = len(EXPECTED_STEPS) - 1  # 7 pairs for 8 steps

        for j in range(total_consecutive_pairs):
            if j in step_positions and (j + 1) in step_positions:
                pos_a = step_positions[j]
                pos_b = step_positions[j + 1]
                # Check if there's at least one empty paragraph between step j and step j+1
                has_empty_between = False
                for k in range(pos_a + 1, pos_b):
                    if paragraphs[k].text.strip() == '':
                        has_empty_between = True
                        break
                if has_empty_between:
                    pairs_with_empty += 1

        if pairs_with_empty >= total_consecutive_pairs:
            print(f"PASS: Component 2 — All {total_consecutive_pairs} consecutive step pairs have empty paragraphs "
                  f"between them (0.3 pts)")
            total_score += 0.3
        elif pairs_with_empty >= 6:
            # Nearly all pairs separated — award partial
            partial = round((pairs_with_empty / total_consecutive_pairs) * 0.3, 3)
            print(f"PARTIAL: Component 2 — {pairs_with_empty}/{total_consecutive_pairs} consecutive pairs have empty "
                  f"paragraphs between them (awarding {partial} pts)")
            total_score += partial
        elif pairs_with_empty > 0:
            partial = round((pairs_with_empty / total_consecutive_pairs) * 0.3, 3)
            print(f"PARTIAL: Component 2 — Only {pairs_with_empty}/{total_consecutive_pairs} pairs separated by empty "
                  f"paragraphs (awarding {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No empty paragraphs found between consecutive cooking steps (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --------------------------------------------------------------------------
    # Component 3: Original single-block paragraph is broken up — no paragraph
    # should contain more than one cooking step sentence (0.3 points).
    # In the initial state, one paragraph contains all 8 steps as a continuous block.
    # This passes ONLY when that block has been split into individual step paragraphs.
    # Serving suggestions existence is a precondition — not scored here.
    # --------------------------------------------------------------------------
    try:
        # Check that no paragraph contains 2 or more of the expected cooking steps
        block_paragraph_found = False
        for p in paragraphs:
            text = p.text.strip()
            steps_found_in_para = sum(1 for step in EXPECTED_STEPS if step.strip() in text)
            if steps_found_in_para >= 2:
                block_paragraph_found = True
                print(f"FAIL: Component 3 — Found paragraph containing {steps_found_in_para} steps still merged: "
                      f"{repr(text[:80])}")
                break

        if not block_paragraph_found:
            # Verify that the total document structure has been expanded as expected:
            # heading (1) + step paragraphs (8) + empty paragraphs (7) + serving (1) = 17 min
            # (in initial state there are only 3 paragraphs: heading + block + serving)
            total_para_count = len(paragraphs)
            if total_para_count >= 16:
                print(f"PASS: Component 3 — No merged block paragraph found; document expanded to "
                      f"{total_para_count} paragraphs (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — No merged block but document has only {total_para_count} paragraphs "
                      f"(expected >= 16 after splitting 8 steps with empty lines)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {round(final_score, 4)}")
    return final_score


# Default: test against canonical artifact path in the VM env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
