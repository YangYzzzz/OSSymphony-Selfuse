"""
Reward Script: Drop Cap effect on first paragraph
Task ID: writer_rd_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): framePr with dropCap attribute exists on first body paragraph
  Component 2 (0.3): dropCap type is "drop" and lines == "3"
  Component 3 (0.3): hSpace (distance from text) is set to a reasonable value
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_003'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_drop_cap_paragraph(doc):
    """
    Find the paragraph with drop cap formatting.
    LibreOffice may implement drop caps in two ways:
    1. framePr on the existing paragraph (python-docx / programmatic)
    2. Split first letter into a separate paragraph with framePr (GUI)
    Returns (framePr_element, paragraph_index) or (None, None).
    """
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # The first body paragraph is index 1 (index 0 is heading).
    # But LibreOffice GUI may split, creating a new para at index 1 for the letter.
    # So check paragraphs 1 and 2 for framePr with dropCap.
    for i, para in enumerate(doc.paragraphs):
        pPr = para._element.find('w:pPr', ns)
        if pPr is not None:
            framePr = pPr.find('w:framePr', ns)
            if framePr is not None:
                drop_cap_attr = framePr.get(f'{{{ns["w"]}}}dropCap')
                if drop_cap_attr is not None:
                    return framePr, i
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Find any paragraph with drop cap
    framePr, para_idx = find_drop_cap_paragraph(doc)

    # Component 1: A framePr with dropCap attribute exists (0.4 points)
    # This checks that the drop cap effect was applied at all.
    try:
        if framePr is not None:
            print(f"PASS: Component 1 — framePr with dropCap found on paragraph {para_idx} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No paragraph has framePr with dropCap attribute")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: dropCap type is "drop" and lines is "3" (0.3 points)
    # The task requires drop cap spanning 3 lines.
    try:
        if framePr is not None:
            drop_cap_val = framePr.get(f'{{{ns["w"]}}}dropCap')
            lines_val = framePr.get(f'{{{ns["w"]}}}lines')
            print(f"  DEBUG: dropCap={drop_cap_val}, lines={lines_val}")

            # Accept "drop" or "margin" as valid drop cap types
            valid_type = drop_cap_val in ("drop", "margin")
            valid_lines = lines_val == "3"

            if valid_type and valid_lines:
                print(f"PASS: Component 2 — dropCap={drop_cap_val}, lines={lines_val} (0.3 pts)")
                total_score += 0.3
            elif valid_type and not valid_lines:
                # Partial: correct type but wrong line count
                print(f"FAIL: Component 2 — dropCap={drop_cap_val} correct, but lines={lines_val} (expected 3)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — dropCap={drop_cap_val}, lines={lines_val} (expected drop/margin, 3)")
        else:
            print("FAIL: Component 2 — No framePr found, cannot check dropCap/lines")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: hSpace (distance from text) is set (0.3 points)
    # The task specifies 0.3 cm distance. 0.3cm = ~170 twips.
    # Accept any hSpace > 0 as partial, exact ~170 for full.
    try:
        if framePr is not None:
            hSpace_val = framePr.get(f'{{{ns["w"]}}}hSpace')
            print(f"  DEBUG: hSpace={hSpace_val}")

            if hSpace_val is not None:
                hSpace_int = int(hSpace_val)
                if hSpace_int > 0:
                    # 170 twips = 0.3cm. Accept range 100-250 for full credit.
                    if 100 <= hSpace_int <= 250:
                        print(f"PASS: Component 3 — hSpace={hSpace_int} twips (~{hSpace_int * 0.01764:.2f}cm), within expected range (0.3 pts)")
                        total_score += 0.3
                    else:
                        # Some distance is set, give partial
                        print(f"PARTIAL: Component 3 — hSpace={hSpace_int} twips, outside ideal range 100-250 (0.15 pts)")
                        total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — hSpace={hSpace_int} (expected > 0)")
            else:
                # No hSpace but drop cap exists - partial credit (some implementations omit hSpace)
                print("FAIL: Component 3 — hSpace not set on framePr")
        else:
            print("FAIL: Component 3 — No framePr found, cannot check hSpace")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state("libreoffice_writer")

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
