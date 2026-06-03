"""
Reward Script: Set line spacing of body text to double spacing in court filing
Task ID: writer_legal_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): >=80% of Normal paragraphs have double line spacing
  Component 2 (0.3): 100% of Normal paragraphs have double line spacing
  Component 3 (0.2): Heading paragraphs remain unchanged (not set to double)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_003'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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
    Verify that all body text paragraphs have double line spacing (2.0)
    while headings remain unchanged.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Classify paragraphs
    normal_paras = []
    heading_paras = []
    for p in doc.paragraphs:
        style_name = p.style.name if p.style else 'Normal'
        if style_name.startswith('Heading'):
            heading_paras.append(p)
        else:
            normal_paras.append(p)

    print(f"INFO: Found {len(normal_paras)} Normal paragraphs, {len(heading_paras)} Heading paragraphs")

    if len(normal_paras) == 0:
        print("FAIL: No Normal paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: >=80% of Normal paragraphs have double line spacing (0.5 points)
    # This checks that the task was substantially completed.
    try:
        double_count = 0
        for p in normal_paras:
            ls = p.paragraph_format.line_spacing
            if ls is not None and abs(float(ls) - 2.0) < 0.01:
                double_count += 1
        ratio = double_count / len(normal_paras)
        print(f"INFO: {double_count}/{len(normal_paras)} Normal paragraphs have double spacing ({ratio:.1%})")
        if ratio >= 0.80:
            print(f"PASS: Component 1 — >=80% Normal paragraphs have double spacing ({ratio:.1%}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Only {ratio:.1%} of Normal paragraphs have double spacing (need >=80%)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 100% of Normal paragraphs have double line spacing (0.3 points)
    # Full compliance - every single body paragraph must be double-spaced.
    try:
        if double_count == len(normal_paras):
            print(f"PASS: Component 2 — All {len(normal_paras)} Normal paragraphs have double spacing (0.3 pts)")
            total_score += 0.3
        else:
            missing = len(normal_paras) - double_count
            print(f"FAIL: Component 2 — {missing} Normal paragraphs still not double-spaced")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Body text is double-spaced AND headings remain unchanged (0.2 points)
    # This compound check anchors to the task change: it only passes when body text
    # HAS been changed to double AND headings were NOT changed. This ensures it fails
    # on initial_env (where body text is single-spaced).
    try:
        body_all_double = (double_count == len(normal_paras))
        if len(heading_paras) == 0:
            headings_ok = body_all_double  # no headings to check, gate on body change
        else:
            headings_unchanged = 0
            for p in heading_paras:
                ls = p.paragraph_format.line_spacing
                if ls is None or abs(float(ls) - 2.0) >= 0.01:
                    headings_unchanged += 1
            headings_ok = (headings_unchanged == len(heading_paras))

        if body_all_double and headings_ok:
            print(f"PASS: Component 3 — All body text double-spaced AND all {len(heading_paras)} headings unchanged (0.2 pts)")
            total_score += 0.2
        elif not body_all_double:
            print(f"FAIL: Component 3 — Body text not fully double-spaced; compound check fails")
        else:
            changed = len(heading_paras) - headings_unchanged
            print(f"FAIL: Component 3 — {changed}/{len(heading_paras)} headings were changed to double spacing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
