"""
Reward Script: Create 'Pleading Paper' page style with specific margins and line numbering
Task ID: writer_legal_075
Domain: libreoffice_writer
Scoring:
  Component 1 — Left margin set to 1.5 inches (0.30 pts)
  Component 2 — Right margin set to 0.5 inches (0.30 pts)
  Component 3 — Line numbering enabled (0.40 pts)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_075'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
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

    Task: Create a custom page style 'Pleading Paper' with:
    - Left margin 1.5 inches (2160 twips / 1371600 EMU / 3.81 cm)
    - Right margin 0.5 inches (720 twips / 457200 EMU / 1.27 cm)
    - Top margin 1 inch (precondition — already set)
    - Bottom margin 1 inch (precondition — already set)
    - Line numbering enabled

    Verification strategy: Check section-level properties in the .docx XML,
    since page styles in LibreOffice map to section properties in OOXML.
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Tolerance for margin comparison: 5% of target value
    # 1.5 inches = 1371600 EMU, tolerance ~68580 EMU
    # 0.5 inches = 457200 EMU, tolerance ~22860 EMU

    # Component 1: Left margin is ~1.5 inches (0.30 points)
    # Initial: 914400 EMU (1.0 in), Golden: 1371600 EMU (1.5 in)
    try:
        left_margin = section.left_margin
        target_left = 1371600  # 1.5 inches in EMU
        tolerance_left = 68580  # ~5% tolerance
        if left_margin is not None and abs(left_margin - target_left) <= tolerance_left:
            print(f"PASS: Component 1 — Left margin is {left_margin / 914400:.2f} inches "
                  f"(target: 1.50 in) (0.30 pts)")
            total_score += 0.30
        else:
            actual_in = left_margin / 914400 if left_margin else 'None'
            print(f"FAIL: Component 1 — Left margin is {actual_in} inches, expected ~1.50 inches")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Right margin is ~0.5 inches (0.30 points)
    # Initial: 914400 EMU (1.0 in), Golden: 457200 EMU (0.5 in)
    try:
        right_margin = section.right_margin
        target_right = 457200  # 0.5 inches in EMU
        tolerance_right = 22860  # ~5% tolerance
        if right_margin is not None and abs(right_margin - target_right) <= tolerance_right:
            print(f"PASS: Component 2 — Right margin is {right_margin / 914400:.2f} inches "
                  f"(target: 0.50 in) (0.30 pts)")
            total_score += 0.30
        else:
            actual_in = right_margin / 914400 if right_margin else 'None'
            print(f"FAIL: Component 2 — Right margin is {actual_in} inches, expected ~0.50 inches")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line numbering is enabled (0.40 points)
    # Initial: no lnNumType element. Golden: lnNumType with countBy="1", restart="newPage"
    try:
        nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        sect_pr = section._sectPr
        ln_num_elements = sect_pr.findall('.//w:lnNumType', nsmap)

        if len(ln_num_elements) > 0:
            ln_elem = ln_num_elements[0]
            count_by = ln_elem.get(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}countBy')
            print(f"PASS: Component 3 — Line numbering enabled "
                  f"(countBy={count_by}) (0.40 pts)")
            total_score += 0.40
        else:
            print("FAIL: Component 3 — Line numbering not enabled (no lnNumType element found)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
