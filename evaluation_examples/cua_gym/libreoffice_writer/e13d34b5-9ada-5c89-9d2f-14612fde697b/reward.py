"""
Reward Script: Reorder paragraphs — move paragraph 4 (Overview) to position 2
Task ID: wrpara_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Paragraph at index 1 starts with "Overview"
  Component 2 (0.3): Paragraph at index 2 starts with "Ingredients"
  Component 3 (0.3): Paragraph at index 3 starts with "Equipment Needed"
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'wrpara_023'


def persist_app_state(domain: str):
    """Save any unsaved changes in the GUI application."""
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
    The task requires reordering paragraphs so that:
      - Original order: Title, Ingredients, Equipment, Overview, Instructions, Serving
      - Expected order: Title, Overview, Ingredients, Equipment, Instructions, Serving
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

    paragraphs = doc.paragraphs
    num_paras = len(paragraphs)
    print(f"INFO: Document has {num_paras} paragraphs")

    if num_paras < 6:
        print(f"FAIL: Expected at least 6 paragraphs, found {num_paras}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: get the first line of a paragraph (the section heading)
    def first_line(para):
        lines = para.text.split('\n')
        return lines[0].strip() if lines else ''

    # Print current paragraph order for debugging
    for i, p in enumerate(paragraphs):
        fl = first_line(p)
        print(f"  Para {i}: {fl[:60]!r}")

    # Component 1: Paragraph at index 1 starts with "Overview" (0.4 points)
    # In initial_env, index 1 is "Ingredients" — this check FAILS on initial
    try:
        fl1 = first_line(paragraphs[1])
        if fl1.lower().startswith("overview"):
            print(f"PASS: Component 1 — Para 1 starts with 'Overview': {fl1!r} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected para 1 to start with 'Overview', found: {fl1!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph at index 2 starts with "Ingredients" (0.3 points)
    # In initial_env, index 2 is "Equipment Needed" — this check FAILS on initial
    try:
        fl2 = first_line(paragraphs[2])
        if fl2.lower().startswith("ingredients"):
            print(f"PASS: Component 2 — Para 2 starts with 'Ingredients': {fl2!r} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected para 2 to start with 'Ingredients', found: {fl2!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph at index 3 starts with "Equipment Needed" (0.3 points)
    # In initial_env, index 3 is "Overview" — this check FAILS on initial
    try:
        fl3 = first_line(paragraphs[3])
        if fl3.lower().startswith("equipment"):
            print(f"PASS: Component 3 — Para 3 starts with 'Equipment': {fl3!r} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected para 3 to start with 'Equipment', found: {fl3!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
