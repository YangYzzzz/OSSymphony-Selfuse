"""
Reward Script: Multi-level list numbering for legal document
Task ID: writer_pd_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Automatic numbering applied to all 15 clause paragraphs
  Component 2 (0.25): Correct multi-level structure (ilvl 0/1/2 matches expected)
  Component 3 (0.20): Manual numbers removed from paragraph text
  Component 4 (0.20): Consistent indentation per level
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_003'

# Expected ilvl for paragraphs P2-P16 (the 15 clause paragraphs)
# Level 1 (ilvl=0): P2, P7, P12
# Level 2 (ilvl=1): P3, P4, P8, P9, P13, P16
# Level 3 (ilvl=2): P5, P6, P10, P11, P14, P15
EXPECTED_ILVL = [0, 1, 1, 2, 2, 0, 1, 1, 2, 2, 0, 1, 2, 2, 1]

# Indentation targets in EMU (1 cm = 360000 EMU)
# Level 1: ~0 cm, Level 2: ~1.27 cm (457200 EMU), Level 3: ~2.54 cm (914400 EMU)
INDENT_TARGETS = {
    0: 0,        # Level 1: 0 cm
    1: 457200,   # Level 2: 1.27 cm
    2: 914400,   # Level 3: 2.54 cm
}
INDENT_TOLERANCE = 90000  # ~0.25 cm tolerance


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
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
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Identify the 15 clause paragraphs (P2 through P16, indices 2-16)
    clause_paras = doc.paragraphs[2:17]
    if len(clause_paras) != 15:
        print(f"WARN: Expected 15 clause paragraphs, found {len(clause_paras)}")

    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Component 1: Automatic numbering applied (0.35 points)
    # All 15 clause paragraphs must have numPr with a valid numId
    try:
        numbered_count = 0
        for para in clause_paras:
            numPr = para._element.find(f'.//{{{ns}}}numPr')
            if numPr is not None:
                numId_el = numPr.find(f'{{{ns}}}numId')
                if numId_el is not None:
                    val = numId_el.get(f'{{{ns}}}val')
                    if val is not None and int(val) > 0:
                        numbered_count += 1
        if numbered_count == 15:
            print(f"PASS: Component 1 — All 15 clause paragraphs have automatic numbering (0.35 pts)")
            total_score += 0.35
        elif numbered_count > 0:
            partial = round(0.35 * (numbered_count / 15), 2)
            print(f"PARTIAL: Component 1 — {numbered_count}/15 paragraphs have numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have automatic numbering (0/15)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct multi-level structure (0.25 points)
    # Each paragraph's ilvl must match the expected level
    try:
        correct_levels = 0
        for idx, para in enumerate(clause_paras):
            numPr = para._element.find(f'.//{{{ns}}}numPr')
            if numPr is not None:
                ilvl_el = numPr.find(f'{{{ns}}}ilvl')
                if ilvl_el is not None:
                    actual_ilvl = int(ilvl_el.get(f'{{{ns}}}val'))
                    if actual_ilvl == EXPECTED_ILVL[idx]:
                        correct_levels += 1
                    else:
                        print(f"  P{idx+2}: expected ilvl={EXPECTED_ILVL[idx]}, got {actual_ilvl}")
        if correct_levels == 15:
            print(f"PASS: Component 2 — All 15 paragraphs have correct ilvl (0.25 pts)")
            total_score += 0.25
        elif correct_levels > 0:
            partial = round(0.25 * (correct_levels / 15), 2)
            print(f"PARTIAL: Component 2 — {correct_levels}/15 correct levels ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs have correct ilvl")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Manual numbers removed from text (0.20 points)
    # No clause paragraph should start with a manual number pattern like "1.", "1.1", "1.2.1"
    try:
        manual_pattern = re.compile(r'^\d+(\.\d+)*\.?\s')
        clean_count = 0
        for idx, para in enumerate(clause_paras):
            if not manual_pattern.match(para.text):
                clean_count += 1
            else:
                print(f"  P{idx+2}: still has manual number: {para.text[:30]!r}")
        if clean_count == 15:
            print(f"PASS: Component 3 — All 15 paragraphs have manual numbers removed (0.20 pts)")
            total_score += 0.20
        elif clean_count > 0:
            partial = round(0.20 * (clean_count / 15), 2)
            print(f"PARTIAL: Component 3 — {clean_count}/15 paragraphs clean ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — All paragraphs still have manual numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Consistent indentation per level (0.20 points)
    # Level 1 (ilvl=0): ~0 cm, Level 2 (ilvl=1): ~1.27 cm, Level 3 (ilvl=2): ~2.54 cm
    # GATE: Only score if paragraph has automatic numbering (avoids scoring pre-existing indents)
    try:
        indent_correct = 0
        numbered_with_indent = 0
        for idx, para in enumerate(clause_paras):
            # Only check indent for paragraphs that have numPr (automatic numbering)
            numPr = para._element.find(f'.//{{{ns}}}numPr')
            if numPr is None:
                continue
            numbered_with_indent += 1
            expected_level = EXPECTED_ILVL[idx]
            target_indent = INDENT_TARGETS[expected_level]
            actual_indent = para.paragraph_format.left_indent
            actual_val = actual_indent if actual_indent else 0
            if abs(actual_val - target_indent) <= INDENT_TOLERANCE:
                indent_correct += 1
            else:
                actual_cm = round(actual_val / 360000, 2) if actual_val else 0
                target_cm = round(target_indent / 360000, 2)
                print(f"  P{idx+2}: indent={actual_cm}cm, expected ~{target_cm}cm")
        if numbered_with_indent == 0:
            print(f"FAIL: Component 4 — No numbered paragraphs to check indentation")
        elif indent_correct == numbered_with_indent and numbered_with_indent == 15:
            print(f"PASS: Component 4 — All 15 paragraphs have correct indentation (0.20 pts)")
            total_score += 0.20
        elif indent_correct > 0:
            partial = round(0.20 * (indent_correct / 15), 2)
            print(f"PARTIAL: Component 4 — {indent_correct}/{numbered_with_indent} correct indentation ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No paragraphs have correct indentation")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
