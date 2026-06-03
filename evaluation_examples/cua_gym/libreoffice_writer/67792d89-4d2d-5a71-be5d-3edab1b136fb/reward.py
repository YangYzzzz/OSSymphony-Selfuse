"""
Reward Script: Accept all tracked changes in thesis chapter document
Task ID: writer_rm_005
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): No tracked insertions remain
  Component 2 (0.35): No tracked deletions remain
  Component 3 (0.30): No tracked formatting changes remain
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_005'


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
    Verify that all tracked changes have been accepted.
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

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }
    body = doc.element.body

    # Component 1: No tracked insertions remain (0.35 points)
    try:
        insertions = body.findall('.//w:ins', ns)
        ins_count = len(insertions)
        if ins_count == 0:
            print(f"PASS: Component 1 — No tracked insertions found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Found {ins_count} tracked insertions still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No tracked deletions remain (0.35 points)
    try:
        deletions = body.findall('.//w:del', ns)
        del_count = len(deletions)
        if del_count == 0:
            print(f"PASS: Component 2 — No tracked deletions found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Found {del_count} tracked deletions still present")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No tracked formatting changes remain (0.30 points)
    try:
        rpr_changes = body.findall('.//w:rPrChange', ns)
        ppr_changes = body.findall('.//w:pPrChange', ns)
        sect_changes = body.findall('.//w:sectPrChange', ns)
        fmt_count = len(rpr_changes) + len(ppr_changes) + len(sect_changes)
        if fmt_count == 0:
            print(f"PASS: Component 3 — No tracked formatting changes found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Found {fmt_count} tracked formatting changes (rPr={len(rpr_changes)}, pPr={len(ppr_changes)}, sect={len(sect_changes)})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verifying
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
