"""
Reward Script: Add bibliography entry for a book chapter
Task ID: writer_bs_033
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): A new (4th) bibliography entry exists after the existing 3
  Component 2 (0.25): Entry has correct author (Lipton) and title (Recurrent Neural Networks)
  Component 3 (0.25): Entry has book section details (Deep Learning Textbook, Goodfellow, MIT Press)
  Component 4 (0.25): Entry has year (2016), pages (367-415), chapter (10)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_033'


def persist_app_state(domain: str):
    """Try to save any unsaved changes in LibreOffice."""
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
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all bibliography entries: paragraphs starting with [N] after the "Bibliography" heading
    bib_entries = []
    in_bibliography = False
    for para in doc.paragraphs:
        txt = para.text.strip()
        if txt.lower() == 'bibliography':
            in_bibliography = (txt.lower() == 'bibliography')  # set flag when heading found
            continue
        if in_bibliography and txt:
            # Check if it looks like a bibliography entry [N]
            if re.match(r'^\[\d+\]', txt):
                bib_entries.append(txt)

    print(f"INFO: Found {len(bib_entries)} bibliography entries")
    for i, entry in enumerate(bib_entries):
        print(f"  Entry {i}: {entry[:120]}...")

    # Component 1: More than 3 bibliography entries (a new one was added) (0.25 points)
    # Initial has exactly 3 entries. Golden should have >= 4.
    try:
        if len(bib_entries) >= 4:
            print(f"PASS: Component 1 — Found {len(bib_entries)} bib entries (>= 4) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Only {len(bib_entries)} bib entries, expected >= 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For Components 2-4, find the new entry containing Lipton / Recurrent Neural Networks
    new_entry = None
    for entry in bib_entries:
        if 'lipton' in entry.lower() or 'recurrent neural network' in entry.lower():
            new_entry = entry
            break

    if new_entry is None:
        print("FAIL: No bibliography entry found mentioning 'Lipton' or 'Recurrent Neural Networks'")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: New entry text: {new_entry}")

    # Component 2: Author contains "Lipton" AND title contains "Recurrent Neural Networks" (0.25 points)
    try:
        has_author = 'lipton' in new_entry.lower()
        has_title = 'recurrent neural network' in new_entry.lower()
        if has_author and has_title:
            print(f"PASS: Component 2 — Author 'Lipton' and title 'Recurrent Neural Networks' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — author_found={has_author}, title_found={has_title}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Book section details — booktitle, editor, publisher (0.25 points)
    try:
        has_booktitle = 'deep learning textbook' in new_entry.lower()
        has_editor = 'goodfellow' in new_entry.lower()
        has_publisher = 'mit press' in new_entry.lower()
        sub_score = 0.0
        if has_booktitle:
            sub_score += 0.10
        if has_editor:
            sub_score += 0.075
        if has_publisher:
            sub_score += 0.075
        if sub_score > 0:
            print(f"PASS: Component 3 — booktitle={has_booktitle}, editor={has_editor}, publisher={has_publisher} ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 3 — booktitle={has_booktitle}, editor={has_editor}, publisher={has_publisher}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Year (2016), pages (367-415), chapter (10) (0.25 points)
    try:
        has_year = '2016' in new_entry
        has_pages = '367' in new_entry and '415' in new_entry
        has_chapter = bool(re.search(r'chapter\s*10', new_entry, re.IGNORECASE)) or \
                      bool(re.search(r'ch\.\s*10', new_entry, re.IGNORECASE)) or \
                      bool(re.search(r'chap\w*\s*10', new_entry, re.IGNORECASE))
        sub_score = 0.0
        if has_year:
            sub_score += 0.10
        if has_pages:
            sub_score += 0.075
        if has_chapter:
            sub_score += 0.075
        if sub_score > 0:
            print(f"PASS: Component 4 — year={has_year}, pages={has_pages}, chapter={has_chapter} ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 — year={has_year}, pages={has_pages}, chapter={has_chapter}")
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
