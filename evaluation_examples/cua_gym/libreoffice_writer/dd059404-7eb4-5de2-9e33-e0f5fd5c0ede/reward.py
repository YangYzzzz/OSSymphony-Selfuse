"""
Reward Script: Accept formatting-only tracked changes, leave text content changes
Task ID: writer_rm_017
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All formatting tracked changes (rPrChange) are accepted (count == 0)
  Component 2 (0.3): Formatting accepted AND text insertions preserved (compound check)
  Component 3 (0.3): Formatting accepted AND text deletions preserved (compound check)

All components are gated on the formatting changes being accepted (rPrChange == 0),
so they all FAIL on initial_env (which has 6 rPrChange) and PASS on golden_env.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_017'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
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
    Verify that formatting-only tracked changes were accepted
    while text content changes remain as tracked changes.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Count tracked change types
    rpr_changes = body.findall('.//w:rPrChange', ns)
    ppr_changes = body.findall('.//w:pPrChange', ns)
    ins_elements = body.findall('.//w:ins', ns)
    del_elements = body.findall('.//w:del', ns)

    rpr_count = len(rpr_changes)
    ppr_count = len(ppr_changes)
    ins_count = len(ins_elements)
    del_count = len(del_elements)
    fmt_count = rpr_count + ppr_count  # all formatting tracked changes

    print(f"Found: rPrChange={rpr_count}, pPrChange={ppr_count}, ins={ins_count}, del={del_count}")
    print(f"Total formatting tracked changes: {fmt_count}")
    print(f"Total text content tracked changes: {ins_count + del_count}")

    # Component 1: All formatting tracked changes accepted (0.4 points)
    # Initial has 6 rPrChange; golden has 0.
    # This component ONLY checks that formatting changes are gone.
    try:
        if fmt_count == 0:
            print(f"PASS: Component 1 — All formatting changes accepted (rPrChange=0, pPrChange=0) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 0 formatting tracked changes, found {fmt_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formatting accepted AND text insertions still tracked (0.3 points)
    # Compound check: both conditions must be true. Fails on initial because fmt_count > 0.
    try:
        if fmt_count == 0 and ins_count >= 5:
            # Accept 5-6 insertions (allow slight tolerance)
            print(f"PASS: Component 2 — Formatting accepted AND {ins_count} text insertions preserved (0.3 pts)")
            total_score += 0.3
        elif fmt_count > 0:
            print(f"FAIL: Component 2 — Formatting changes not yet accepted ({fmt_count} remain)")
        else:
            print(f"FAIL: Component 2 — Expected >=5 tracked insertions, found {ins_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Formatting accepted AND text deletions still tracked (0.3 points)
    # Compound check: both conditions must be true. Fails on initial because fmt_count > 0.
    try:
        if fmt_count == 0 and del_count >= 2:
            # Accept 2-3 deletions (allow slight tolerance)
            print(f"PASS: Component 3 — Formatting accepted AND {del_count} text deletions preserved (0.3 pts)")
            total_score += 0.3
        elif fmt_count > 0:
            print(f"FAIL: Component 3 — Formatting changes not yet accepted ({fmt_count} remain)")
        else:
            print(f"FAIL: Component 3 — Expected >=2 tracked deletions, found {del_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before checking
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
