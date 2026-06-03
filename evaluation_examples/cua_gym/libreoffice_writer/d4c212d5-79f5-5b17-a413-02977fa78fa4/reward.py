"""
Reward Script: Apply 'Keep with next' to all Heading 1 paragraphs
Task ID: writer_legal_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Progressive — proportion of Heading 1 paragraphs with keep_with_next enabled
  Component 2 (0.4): Full completion — ALL Heading 1 paragraphs have keep_with_next enabled
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_040'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice Writer."""
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
    Verify that all Heading 1 styled paragraphs have 'Keep with next' enabled.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all Heading 1 paragraphs
    heading1_paras = []
    try:
        for i, para in enumerate(doc.paragraphs):
            if para.style.name == 'Heading 1':
                heading1_paras.append((i, para))
    except Exception as e:
        print(f"ERROR: Could not iterate paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(heading1_paras) == 0:
        print("FAIL: No Heading 1 paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(heading1_paras)} Heading 1 paragraphs")

    # Count how many have keep_with_next enabled
    kwn_enabled_count = 0
    for idx, para in heading1_paras:
        try:
            kwn = para.paragraph_format.keep_with_next
            if kwn is True:
                kwn_enabled_count += 1
            else:
                print(f"  FAIL: Para {idx} ('{para.text[:50]}') keep_with_next={kwn}")
        except Exception as e:
            print(f"  ERROR: Para {idx}: {e}")

    total_headings = len(heading1_paras)
    fraction_enabled = kwn_enabled_count / total_headings

    print(f"INFO: {kwn_enabled_count}/{total_headings} Heading 1 paragraphs have keep_with_next enabled")

    # Component 1: Progressive — proportion of Heading 1 paragraphs with keep_with_next (0.6 points)
    # This awards partial credit proportional to how many headings were fixed.
    try:
        comp1_score = 0.6 * fraction_enabled
        if comp1_score > 0:
            print(f"PASS: Component 1 — {kwn_enabled_count}/{total_headings} headings enabled ({comp1_score:.2f} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 — no headings have keep_with_next enabled")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Full completion — ALL Heading 1 paragraphs have keep_with_next (0.4 points)
    # Only awarded when every single Heading 1 paragraph is correctly formatted.
    try:
        if kwn_enabled_count == total_headings:
            print(f"PASS: Component 2 — all {total_headings} headings have keep_with_next (0.4 pts)")
            total_score += 0.4
        else:
            missing = total_headings - kwn_enabled_count
            print(f"FAIL: Component 2 — {missing} heading(s) still missing keep_with_next")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verifying
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
