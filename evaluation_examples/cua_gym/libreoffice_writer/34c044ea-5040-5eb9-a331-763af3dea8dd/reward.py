"""
Reward Script: Photo album caption-date layout with tabstops
Task ID: osworld_writer_tabstop_004
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5 pts): All 9 paragraphs have a right-aligned tab stop at ~8cm
  - Component 2 (0.5 pts): All 9 paragraphs have a tab character inserted after the first word
Total: 1.0
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_004'

# 8cm in EMU = 2,880,000; allow ~1% tolerance (~28,800 EMU ~ 0.08cm)
TARGET_POS_EMU = int(Cm(8))       # 2,880,000
TOLERANCE_EMU = 36000             # ±0.1cm tolerance

def has_right_tab_at_8cm(para):
    """Check if the paragraph has a right-aligned tab stop at ~8cm."""
    for ts in para.paragraph_format.tab_stops:
        if ts.alignment == WD_TAB_ALIGNMENT.RIGHT:
            if abs(ts.position - TARGET_POS_EMU) <= TOLERANCE_EMU:
                return True
    return False


def has_tab_after_first_word(para):
    """Check if paragraph text has a tab character after the first word."""
    text = para.text
    if not text.strip():
        return False
    # A tab character should appear after the first word
    # First word is separated by a tab
    parts = text.split('\t', 1)
    if len(parts) < 2:
        return False
    first_part = parts[0].strip()
    # First part should be a single word (no spaces)
    if ' ' in first_part or not first_part:
        return False
    return True


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

    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    num_paras = len(paragraphs)

    if num_paras == 0:
        print("FAIL: No non-empty paragraphs found in document")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All paragraphs have a right-aligned tab stop at ~8cm (0.5 points)
    # This FAILS on initial (no tab stops) → PASSES on golden (RIGHT tab at ~8cm)
    try:
        paras_with_right_tab = 0
        failed_paras = []
        for i, para in enumerate(paragraphs):
            if has_right_tab_at_8cm(para):
                paras_with_right_tab += 1
            else:
                failed_paras.append(i)

        if paras_with_right_tab == num_paras:
            print(f"PASS: Component 1 — All {num_paras} paragraphs have right-aligned tab stop at ~8cm (0.5 pts)")
            total_score += 0.5
        elif paras_with_right_tab > 0:
            partial = 0.5 * (paras_with_right_tab / num_paras)
            print(f"PARTIAL: Component 1 — {paras_with_right_tab}/{num_paras} paragraphs have right-aligned tab stop at ~8cm ({partial:.2f} pts)")
            print(f"  Failed paragraph indices: {failed_paras}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have right-aligned tab stop at ~8cm (expected {TARGET_POS_EMU} EMU ±{TOLERANCE_EMU})")
            # Debug: show actual tab stops for first paragraph
            if paragraphs:
                ts_info = [(str(ts.alignment), ts.position) for ts in paragraphs[0].paragraph_format.tab_stops]
                print(f"  First para tab stops: {ts_info}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All paragraphs have a tab character inserted after the first word (0.5 points)
    # This FAILS on initial (plain text, no tabs) → PASSES on golden (tab after first word)
    try:
        paras_with_tab = 0
        failed_tab_paras = []
        for i, para in enumerate(paragraphs):
            if has_tab_after_first_word(para):
                paras_with_tab += 1
            else:
                failed_tab_paras.append((i, repr(para.text[:60])))

        if paras_with_tab == num_paras:
            print(f"PASS: Component 2 — All {num_paras} paragraphs have tab inserted after first word (0.5 pts)")
            total_score += 0.5
        elif paras_with_tab > 0:
            partial = 0.5 * (paras_with_tab / num_paras)
            print(f"PARTIAL: Component 2 — {paras_with_tab}/{num_paras} paragraphs have tab after first word ({partial:.2f} pts)")
            print(f"  Failed: {failed_tab_paras}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs have tab character after first word")
            if paragraphs:
                print(f"  First para text: {repr(paragraphs[0].text[:80])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
