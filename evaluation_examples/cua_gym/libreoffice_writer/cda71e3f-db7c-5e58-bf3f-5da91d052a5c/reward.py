"""
Reward Script: Configure page numbering with lowercase Roman numerals for front matter
Task ID: writer_fs_045
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Document has >= 2 sections (section break added)
  Component 2 (0.30): First section uses lowerRoman page number format
  Component 3 (0.20): Second section uses decimal format with page number restarted at 1
  Component 4 (0.20): Second section footer has a PAGE field (page numbers displayed)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_045'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
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
    Verify page numbering configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_sections = len(doc.sections)
    print(f"INFO: Document has {num_sections} section(s)")

    # Component 1: Document has at least 2 sections (0.30 points)
    # The task requires a section break between front matter (pages 1-3)
    # and main content (pages 4+). Initial doc has only 1 section.
    try:
        if num_sections >= 2:
            print(f"PASS: Component 1 — Document has {num_sections} sections (>= 2) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected >= 2 sections, found {num_sections}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: First section uses lowerRoman page number format (0.30 points)
    # The task requires pages 1-3 (front matter) to use lowercase Roman numerals (i, ii, iii).
    # Initial doc uses 'decimal' for all pages.
    try:
        sec0 = doc.sections[0]
        sect_pr = sec0._sectPr
        pg_num_type = sect_pr.find(qn('w:pgNumType'))
        fmt0 = pg_num_type.get(qn('w:fmt')) if pg_num_type is not None else None
        print(f"INFO: Section 0 pgNumFmt = {fmt0}")

        if fmt0 == 'lowerRoman':
            print(f"PASS: Component 2 — First section uses lowerRoman format (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected lowerRoman format, found {fmt0}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Second section uses decimal format with start=1 (0.20 points)
    # The task requires pages 4+ to restart Arabic numbering from 1.
    # Initial doc has no second section at all.
    try:
        if num_sections >= 2:
            sec1 = doc.sections[1]
            sect_pr1 = sec1._sectPr
            pg_num_type1 = sect_pr1.find(qn('w:pgNumType'))
            fmt1 = pg_num_type1.get(qn('w:fmt')) if pg_num_type1 is not None else None
            start1 = pg_num_type1.get(qn('w:start')) if pg_num_type1 is not None else None
            print(f"INFO: Section 1 pgNumFmt = {fmt1}, pgNumStart = {start1}")

            if fmt1 == 'decimal' and start1 == '1':
                print(f"PASS: Component 3 — Second section uses decimal format starting at 1 (0.20 pts)")
                total_score += 0.20
            elif fmt1 == 'decimal':
                # Decimal but without explicit start=1 — partial credit
                print(f"PARTIAL: Component 3 — Decimal format but start={start1} (expected 1) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Expected decimal format with start=1, found fmt={fmt1} start={start1}")
        else:
            print(f"FAIL: Component 3 — No second section exists")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Second section has its own footer with PAGE field (0.20 points)
    # Both sections should display page numbers. The second section footer
    # must not be linked to previous (so it shows its own numbering scheme).
    # Initial doc has only 1 section so this cannot pass.
    try:
        if num_sections >= 2:
            sec1 = doc.sections[1]
            ftr1 = sec1.footer
            linked = ftr1.is_linked_to_previous
            # Check for PAGE field in footer using count of matching instrText elements
            page_field_count = sum(
                1 for fp in ftr1.paragraphs
                for fi in fp._element.findall('.//' + qn('w:instrText'))
                if fi.text and 'PAGE' in fi.text.upper()
            )
            has_page_field = page_field_count > 0

            print(f"INFO: Section 1 footer linked_to_previous={linked}, has_page_field={has_page_field}")

            if has_page_field and not linked:
                print(f"PASS: Component 4 — Second section has independent footer with PAGE field (0.20 pts)")
                total_score += 0.20
            elif has_page_field and linked:
                # Has page field but linked — still shows pages, partial credit
                print(f"PARTIAL: Component 4 — Footer has PAGE field but is linked to previous (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Second section footer missing PAGE field or linked")
        else:
            print(f"FAIL: Component 4 — No second section exists")
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
