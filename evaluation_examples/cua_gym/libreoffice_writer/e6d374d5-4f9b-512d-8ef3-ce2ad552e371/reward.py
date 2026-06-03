"""
Reward Script: Insert figure and table captions, create List of Figures and List of Tables
Task ID: writer_pd_023
Domain: libreoffice_writer
Scoring:
  Component 1: 6 figure captions in document body (0.25)
  Component 2: 4 table captions in document body (0.25)
  Component 3: List of Figures heading with 6 entries on page 2 area (0.25)
  Component 4: List of Tables heading with 4 entries on page 2 area (0.25)
"""

import os
import re
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_023'

# Expected figure captions (in body, not in list section)
EXPECTED_FIGURES = [
    "Figure 1",
    "Figure 2",
    "Figure 3",
    "Figure 4",
    "Figure 5",
    "Figure 6",
]

# Expected table captions (in body, not in list section)
EXPECTED_TABLES = [
    "Table 1",
    "Table 2",
    "Table 3",
    "Table 4",
]


def find_heading_index(paragraphs, heading_text):
    """Find the paragraph index of a heading containing the given text."""
    for i, para in enumerate(paragraphs):
        style = para.style.name if para.style else ''
        if 'Heading' in style and heading_text.lower() in para.text.strip().lower():
            return i
    return -1


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

    # Identify the list section boundaries (page 2 area)
    # The List of Figures and List of Tables should appear before Chapter 1
    lof_idx = find_heading_index(paragraphs, "List of Figures")
    lot_idx = find_heading_index(paragraphs, "List of Tables")
    ch1_idx = find_heading_index(paragraphs, "Chapter 1")

    # If no Chapter 1 found, use a high number
    if ch1_idx < 0:
        ch1_idx = len(paragraphs)

    # Determine body paragraphs (after the list section / after Chapter 1 heading)
    body_start = ch1_idx

    # ------------------------------------------------------------------
    # Component 1: 6 figure captions in document body (0.25 points)
    # These are "Figure N: <description>" paragraphs in the body (after Chapter 1)
    # ------------------------------------------------------------------
    try:
        fig_caption_count = 0
        found_figs = []
        for i in range(body_start, len(paragraphs)):
            txt = paragraphs[i].text.strip()
            if re.match(r'^Figure\s+\d+\s*[:\.]', txt):
                fig_caption_count += 1
                found_figs.append(txt[:60])

        if fig_caption_count >= 6:
            print(f"PASS: Component 1 - Found {fig_caption_count} figure captions in body (0.25 pts)")
            total_score += 0.25
        elif fig_caption_count >= 3:
            partial = round(0.25 * fig_caption_count / 6, 3)
            print(f"PARTIAL: Component 1 - Found {fig_caption_count}/6 figure captions ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Found {fig_caption_count}/6 figure captions in body")
        for f in found_figs:
            print(f"  Found: {f}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # ------------------------------------------------------------------
    # Component 2: 4 table captions in document body (0.25 points)
    # These are "Table N: <description>" paragraphs in the body (after Chapter 1)
    # ------------------------------------------------------------------
    try:
        tbl_caption_count = 0
        found_tbls = []
        for i in range(body_start, len(paragraphs)):
            txt = paragraphs[i].text.strip()
            if re.match(r'^Table\s+\d+\s*[:\.]', txt):
                tbl_caption_count += 1
                found_tbls.append(txt[:60])

        if tbl_caption_count >= 4:
            print(f"PASS: Component 2 - Found {tbl_caption_count} table captions in body (0.25 pts)")
            total_score += 0.25
        elif tbl_caption_count >= 2:
            partial = round(0.25 * tbl_caption_count / 4, 3)
            print(f"PARTIAL: Component 2 - Found {tbl_caption_count}/4 table captions ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Found {tbl_caption_count}/4 table captions in body")
        for t in found_tbls:
            print(f"  Found: {t}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # ------------------------------------------------------------------
    # Component 3: List of Figures heading with 6 figure entries (0.25 points)
    # Should be before Chapter 1, with entries like "Figure N: ... <page>"
    # ------------------------------------------------------------------
    try:
        if lof_idx >= 0:
            # Count entries between List of Figures heading and next heading or List of Tables
            end_idx = lot_idx if lot_idx > lof_idx else ch1_idx
            lof_entries = 0
            for i in range(lof_idx + 1, end_idx):
                txt = paragraphs[i].text.strip()
                if re.match(r'^Figure\s+\d+', txt):
                    lof_entries += 1
            if lof_entries >= 6:
                print(f"PASS: Component 3 - List of Figures with {lof_entries} entries (0.25 pts)")
                total_score += 0.25
            elif lof_entries >= 3:
                partial = round(0.25 * lof_entries / 6, 3)
                print(f"PARTIAL: Component 3 - List of Figures with {lof_entries}/6 entries ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 - List of Figures found but only {lof_entries}/6 entries")
        else:
            print("FAIL: Component 3 - 'List of Figures' heading not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # ------------------------------------------------------------------
    # Component 4: List of Tables heading with 4 table entries (0.25 points)
    # Should be before Chapter 1, with entries like "Table N: ... <page>"
    # ------------------------------------------------------------------
    try:
        if lot_idx >= 0:
            # Count entries between List of Tables heading and Chapter 1
            end_idx = ch1_idx
            lot_entries = 0
            for i in range(lot_idx + 1, end_idx):
                txt = paragraphs[i].text.strip()
                if re.match(r'^Table\s+\d+', txt):
                    lot_entries += 1
            if lot_entries >= 4:
                print(f"PASS: Component 4 - List of Tables with {lot_entries} entries (0.25 pts)")
                total_score += 0.25
            elif lot_entries >= 2:
                partial = round(0.25 * lot_entries / 4, 3)
                print(f"PARTIAL: Component 4 - List of Tables with {lot_entries}/4 entries ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 - List of Tables found but only {lot_entries}/4 entries")
        else:
            print("FAIL: Component 4 - 'List of Tables' heading not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
