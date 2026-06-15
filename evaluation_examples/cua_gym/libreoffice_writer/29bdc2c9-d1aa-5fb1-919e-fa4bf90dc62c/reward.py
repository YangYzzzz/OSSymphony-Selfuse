"""
Reward Script: Format glossary with left and center tabstops at 0cm and 8cm,
and insert tab after each term (first word) in each line.
Task ID: osworld_writer_tabstop_008
Domain: libreoffice_writer
Scoring:
  Component 1: All paragraphs have a tab character inserted after the first word (0.4 pts)
  Component 2: All paragraphs have a CENTER tab stop at 8cm (0.4 pts)
  Component 3: All paragraphs have a LEFT tab stop at 0cm (0.2 pts)
Total: 1.0
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_008'

# 8cm in EMU (English Metric Units): 1 inch = 914400 EMU, 1 cm = 360000 EMU
CM_8_EMU = 8 * 360000  # 2880000 EMU
# Allow a small tolerance of ~10000 EMU (~0.03 cm) for rounding differences
TOLERANCE_EMU = 15000


def persist_app_state():
    """Best-effort save for LibreOffice Writer before verification."""
    try:
        import time
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.2)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Format a glossary where each term (first word) is left-aligned and
    the definition starts at a center tab stop at 8cm.

    Changes between initial_env and golden_env:
    - Initial: no tab stops, no tab characters, plain text "TERM Definition..."
    - Golden: LEFT tab stop at 0cm + CENTER tab stop at 8cm per paragraph,
              tab character inserted after each term word: "TERM\tDefinition..."
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    total_paras = len(paragraphs)
    if total_paras == 0:
        print("CRITICAL: No non-empty paragraphs found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {total_paras} non-empty paragraphs")

    # Component 1: Tab character inserted after first word in each paragraph (0.4 points)
    # Initial state: no tab characters — all text is continuous "TERM Definition..."
    # Golden state: tab character after term — "TERM\tDefinition..."
    try:
        paras_with_tab = 0
        paras_without_tab = []
        for para in paragraphs:
            if '\t' in para.text:
                # Also verify the tab is after the first word (not just anywhere)
                parts = para.text.split('\t', 1)
                first_word = parts[0].strip()
                if first_word and ' ' not in first_word:
                    # First segment is a single word (the term), rest is the definition
                    paras_with_tab += 1
                else:
                    paras_without_tab.append(f"'{para.text[:40]}' (tab not after single term word)")
            else:
                paras_without_tab.append(f"'{para.text[:40]}' (no tab)")

        tab_ratio = paras_with_tab / total_paras
        if tab_ratio == 1.0:
            print(f"PASS: Component 1 — All {total_paras} paragraphs have tab after term word (0.4 pts)")
            total_score += 0.4
        elif tab_ratio >= 0.8:
            partial = round(0.4 * tab_ratio, 2)
            print(f"PARTIAL: Component 1 — {paras_with_tab}/{total_paras} paragraphs have tab ({partial} pts)")
            print(f"  Failing: {paras_without_tab[:3]}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {paras_with_tab}/{total_paras} paragraphs have tab after term")
            print(f"  Failing examples: {paras_without_tab[:3]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CENTER tab stop at 8cm in each paragraph (0.4 points)
    # Initial state: no tab stops defined
    # Golden state: CENTER tab stop at 8cm (2880000 EMU) per paragraph
    try:
        paras_with_center_8cm = 0
        paras_without_center = []
        for para in paragraphs:
            tab_stops = list(para.paragraph_format.tab_stops)
            found_center_8cm = False
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.CENTER:
                    if abs(ts.position - CM_8_EMU) <= TOLERANCE_EMU:
                        found_center_8cm = True
                        break
            if found_center_8cm:
                paras_with_center_8cm += 1
            else:
                paras_without_center.append(f"'{para.text[:20]}' tabs={[(ts.alignment, ts.position) for ts in tab_stops]}")

        center_ratio = paras_with_center_8cm / total_paras
        if center_ratio == 1.0:
            print(f"PASS: Component 2 — All {total_paras} paragraphs have CENTER tab stop at 8cm (0.4 pts)")
            total_score += 0.4
        elif center_ratio >= 0.8:
            partial = round(0.4 * center_ratio, 2)
            print(f"PARTIAL: Component 2 — {paras_with_center_8cm}/{total_paras} have CENTER@8cm ({partial} pts)")
            print(f"  Failing: {paras_without_center[:2]}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {paras_with_center_8cm}/{total_paras} have CENTER tab stop at 8cm")
            print(f"  Failing examples: {paras_without_center[:2]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: LEFT tab stop at 0cm in each paragraph (0.2 points)
    # Initial state: no tab stops defined
    # Golden state: LEFT tab stop at 0cm (position=0) per paragraph
    try:
        paras_with_left_0cm = 0
        paras_without_left = []
        for para in paragraphs:
            tab_stops = list(para.paragraph_format.tab_stops)
            found_left_0cm = False
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                    found_left_0cm = True
                    break
            if found_left_0cm:
                paras_with_left_0cm += 1
            else:
                paras_without_left.append(f"'{para.text[:20]}'")

        left_ratio = paras_with_left_0cm / total_paras
        if left_ratio == 1.0:
            print(f"PASS: Component 3 — All {total_paras} paragraphs have LEFT tab stop at 0cm (0.2 pts)")
            total_score += 0.2
        elif left_ratio >= 0.8:
            partial = round(0.2 * left_ratio, 2)
            print(f"PARTIAL: Component 3 — {paras_with_left_0cm}/{total_paras} have LEFT@0cm ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {paras_with_left_0cm}/{total_paras} have LEFT tab stop at 0cm")
            print(f"  Failing examples: {paras_without_left[:3]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state (in case the document is still open and unsaved)
persist_app_state()

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
