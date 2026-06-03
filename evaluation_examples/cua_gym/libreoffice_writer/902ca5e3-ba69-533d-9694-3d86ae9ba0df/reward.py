"""
Reward Script: Professional memo template with bold header labels and tab stops
Task ID: writer_biz_025
Domain: libreoffice_writer

Scoring rubric (4 components, total 1.0):
  Component 1 (0.30) - Four memo paragraphs present with correct labels
  Component 2 (0.25) - Labels are bold
  Component 3 (0.25) - Each label is followed by a tab character
  Component 4 (0.20) - Left tab stop at 1.5 inches (1371600 EMU) on each paragraph
"""

import os

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_025'
EXPECTED_LABELS = ['TO:', 'FROM:', 'DATE:', 'SUBJECT:']
TAB_POSITION_EMU = 1371600  # 1.5 inches = 3.81 cm
TAB_TOLERANCE_EMU = 50000   # ~0.05 inch tolerance


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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

    paragraphs = doc.paragraphs
    num_paras = len(paragraphs)

    # Component 1: Four memo paragraphs with correct labels (0.30 points)
    # Each paragraph text should start with the expected label.
    try:
        labels_found = 0
        if num_paras >= 4:
            for i, expected_label in enumerate(EXPECTED_LABELS):
                para_text = paragraphs[i].text.strip()
                if para_text.startswith(expected_label):
                    labels_found += 1
                else:
                    print(f"FAIL: Component 1 — paragraph {i} starts with {repr(para_text[:20])}, expected {repr(expected_label)}")

        if labels_found == 4:
            print(f"PASS: Component 1 — all 4 memo labels found in correct order (0.30 pts)")
            total_score += 0.30
        elif labels_found > 0:
            partial = round(0.30 * labels_found / 4, 2)
            print(f"PARTIAL: Component 1 — {labels_found}/4 labels found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — no memo labels found (found {num_paras} paragraphs)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Labels are bold (0.25 points)
    # The first run of each of the first 4 paragraphs must have bold=True
    try:
        bold_count = 0
        if num_paras >= 4:
            for i in range(4):
                runs = paragraphs[i].runs
                if len(runs) >= 1 and runs[0].font.bold:
                    bold_count += 1
                else:
                    bold_val = runs[0].font.bold if len(runs) >= 1 else 'no runs'
                    print(f"FAIL: Component 2 — paragraph {i} label run bold={bold_val}")

        if bold_count == 4:
            print(f"PASS: Component 2 — all 4 labels are bold (0.25 pts)")
            total_score += 0.25
        elif bold_count > 0:
            partial = round(0.25 * bold_count / 4, 2)
            print(f"PARTIAL: Component 2 — {bold_count}/4 labels bold ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no labels are bold")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each label is followed by a tab character (0.25 points)
    # The paragraph text should contain a tab after the label
    try:
        tab_char_count = 0
        if num_paras >= 4:
            for i in range(4):
                para_text = paragraphs[i].text
                if '\t' in para_text:
                    tab_char_count += 1
                else:
                    print(f"FAIL: Component 3 — paragraph {i} has no tab character, text={repr(para_text)}")

        if tab_char_count == 4:
            print(f"PASS: Component 3 — all 4 paragraphs have tab characters (0.25 pts)")
            total_score += 0.25
        elif tab_char_count > 0:
            partial = round(0.25 * tab_char_count / 4, 2)
            print(f"PARTIAL: Component 3 — {tab_char_count}/4 have tabs ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no tab characters found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Left tab stop at 1.5 inches on each paragraph (0.20 points)
    # Check that each of the first 4 paragraphs has a LEFT tab stop near 1371600 EMU
    try:
        tab_stop_count = 0
        if num_paras >= 4:
            for i in range(4):
                pf = paragraphs[i].paragraph_format
                found_tab_stop = False
                for ts in pf.tab_stops:
                    if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                        continue
                    if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                        continue
                    if abs(ts.position - TAB_POSITION_EMU) <= TAB_TOLERANCE_EMU:
                        found_tab_stop = True
                        break
                if found_tab_stop:
                    tab_stop_count += 1
                else:
                    print(f"FAIL: Component 4 — paragraph {i} missing tab stop at 1.5 inches")

        if tab_stop_count == 4:
            print(f"PASS: Component 4 — all 4 paragraphs have tab stop at 1.5 inches (0.20 pts)")
            total_score += 0.20
        elif tab_stop_count > 0:
            partial = round(0.20 * tab_stop_count / 4, 2)
            print(f"PARTIAL: Component 4 — {tab_stop_count}/4 have correct tab stops ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no paragraphs have tab stop at 1.5 inches")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
