"""
Reward Script: Insert a Table of Figures at the end of the document
Task ID: writer_rd_046
Domain: libreoffice_writer
Scoring:
  Component 1: "List of Figures" heading exists with Heading 1 style (0.20)
  Component 2: Table of Figures is placed before Appendix (0.15)
  Component 3: All 6 figure captions are listed (0.30)
  Component 4: Each entry has a page number after a tab (0.15)
  Component 5: Entries use RIGHT-aligned tab stops with dotted leaders (0.20)
"""

import os
import re

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_046'

# Expected figure captions (from task context: 6 figures)
EXPECTED_FIGURES = [
    'Figure 1',
    'Figure 2',
    'Figure 3',
    'Figure 4',
    'Figure 5',
    'Figure 6',
]


def persist_app_state(domain):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a Table of Figures has been inserted at the end of the document
    with all 6 figure captions, page numbers, and dotted tab leaders.
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

    # --- Locate the "List of Figures" heading ---
    lof_index = None
    for i, p in enumerate(paragraphs):
        text_lower = p.text.strip().lower()
        if text_lower in ('list of figures', 'table of figures'):
            lof_index = i
            break

    if lof_index is None:
        print("FAIL: No 'List of Figures' or 'Table of Figures' heading found in document")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: Heading exists with appropriate style (0.20 pts) ---
    try:
        lof_para = paragraphs[lof_index]
        style_name = lof_para.style.name if lof_para.style else ''
        # Accept Heading 1, Heading 2, or any heading style as reasonable
        is_heading = style_name.startswith('Heading')
        if is_heading:
            print(f"PASS: Component 1 — 'List of Figures' heading found at paragraph {lof_index} "
                  f"with style '{style_name}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — 'List of Figures' found but style is '{style_name}', "
                  f"expected a Heading style")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Placed before Appendix (correct position) (0.15 pts) ---
    try:
        appendix_index = None
        for i, p in enumerate(paragraphs):
            if p.text.strip().lower().startswith('appendix'):
                style_name = p.style.name if p.style else ''
                if style_name.startswith('Heading'):
                    appendix_index = i
                    break

        if appendix_index is not None:
            if lof_index < appendix_index:
                print(f"PASS: Component 2 — Table of Figures (para {lof_index}) is before "
                      f"Appendix (para {appendix_index}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Table of Figures (para {lof_index}) is NOT before "
                      f"Appendix (para {appendix_index})")
        else:
            # No appendix found; the task says "before the appendix if any", so if no appendix
            # exists and the TOF is near the end, that's acceptable
            # Check it's in the latter half of the document
            if lof_index > len(paragraphs) // 2:
                print(f"PASS: Component 2 — No Appendix found; Table of Figures is near end "
                      f"of document (para {lof_index}/{len(paragraphs)}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Table of Figures at para {lof_index} is not near "
                      f"the end of the document ({len(paragraphs)} paragraphs)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Collect entries following the List of Figures heading ---
    # Entries are paragraphs after the heading until the next heading or end
    entries = []
    for i in range(lof_index + 1, len(paragraphs)):
        p = paragraphs[i]
        style_name = p.style.name if p.style else ''
        text = p.text.strip()
        # Stop at next heading
        if style_name.startswith('Heading') and text:
            break
        # Skip empty paragraphs
        if not text:
            continue
        entries.append(p)

    # --- Component 3: All 6 figure captions are listed (0.30 pts) ---
    try:
        found_figures = []
        for fig_prefix in EXPECTED_FIGURES:
            for entry in entries:
                if fig_prefix.lower() in entry.text.lower():
                    found_figures.append(fig_prefix)
                    break

        num_found = len(found_figures)
        if num_found == 6:
            print(f"PASS: Component 3 — All 6 figures found in Table of Figures (0.30 pts)")
            total_score += 0.30
        elif num_found >= 4:
            partial = round(0.30 * (num_found / 6), 2)
            print(f"PARTIAL: Component 3 — {num_found}/6 figures found ({partial} pts)")
            total_score += partial
        elif num_found >= 1:
            partial = round(0.30 * (num_found / 6), 2)
            print(f"PARTIAL: Component 3 — {num_found}/6 figures found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No figure entries found after 'List of Figures' heading")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Each entry has a page number after a tab (0.15 pts) ---
    try:
        entries_with_page_num = 0
        for entry in entries:
            text = entry.text
            # Pattern: caption text followed by tab and a number
            if '\t' in text:
                parts = text.split('\t')
                last_part = parts[-1].strip()
                if last_part.isdigit():
                    entries_with_page_num += 1

        if len(entries) > 0 and entries_with_page_num == len(entries) and entries_with_page_num >= 6:
            print(f"PASS: Component 4 — All {entries_with_page_num} entries have page numbers "
                  f"after tabs (0.15 pts)")
            total_score += 0.15
        elif entries_with_page_num >= 4:
            partial = round(0.15 * (entries_with_page_num / max(len(entries), 6)), 2)
            print(f"PARTIAL: Component 4 — {entries_with_page_num}/{len(entries)} entries have "
                  f"page numbers ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {entries_with_page_num}/{len(entries)} entries "
                  f"have tab+page number format")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # --- Component 5: Tab stops use RIGHT alignment with DOTS leader (0.20 pts) ---
    try:
        entries_with_dots = 0
        for entry in entries:
            for ts in entry.paragraph_format.tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                if ts.alignment == WD_TAB_ALIGNMENT.RIGHT and ts.leader == WD_TAB_LEADER.DOTS:
                    entries_with_dots += 1
                    break

        if len(entries) > 0 and entries_with_dots == len(entries) and entries_with_dots >= 6:
            print(f"PASS: Component 5 — All {entries_with_dots} entries have RIGHT-aligned "
                  f"dotted tab leaders (0.20 pts)")
            total_score += 0.20
        elif entries_with_dots >= 4:
            partial = round(0.20 * (entries_with_dots / max(len(entries), 6)), 2)
            print(f"PARTIAL: Component 5 — {entries_with_dots}/{len(entries)} entries have "
                  f"dotted leaders ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Only {entries_with_dots}/{len(entries)} entries have "
                  f"RIGHT-aligned dotted tab leaders")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
