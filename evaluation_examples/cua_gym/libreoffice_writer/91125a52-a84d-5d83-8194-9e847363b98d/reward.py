"""
Reward Script: Insert a formatted index of tables in a Writer document
Task ID: writer_rd_088
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) — TOC field code with category "Table" exists after 'List of Tables' heading
  Component 2 (0.40) — All 8 table captions listed in index entries with correct names
  Component 3 (0.15) — Each index entry has a page number
  Component 4 (0.15) — Index entries appear between 'List of Tables' heading and '1. Executive Summary'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_088'

# The 8 expected table captions from the document
EXPECTED_TABLES = [
    "Table 1: Sales by Region",
    "Table 2: Product Performance",
    "Table 3: Customer Acquisition by Channel",
    "Table 4: Customer Retention Metrics",
    "Table 5: Quarterly Financial Summary",
    "Table 6: Expense Breakdown",
    "Table 7: Platform Uptime and Performance",
    "Table 8: Support Ticket Summary",
]


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
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
    Verify that a formatted index of tables has been inserted below the
    'List of Tables' heading.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Missing python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # ---------------------------------------------------------------
    # Component 1: TOC field code with category "Table" (0.30 points)
    # The golden file contains a field code like: TOC \h \z \c "Table"
    # This field code is what LibreOffice generates when inserting a
    # "Table of Figures" index with category set to "Table".
    # ---------------------------------------------------------------
    try:
        has_toc_table_field = False
        for p_elem in doc.element.body.findall(qn('w:p')):
            for instr in p_elem.findall('.//w:instrText', ns):
                if instr.text and 'TOC' in instr.text.upper():
                    # Check for the "Table" category marker
                    # Format: TOC \c "Table" or variations
                    if re.search(r'\\c\s+"Table"', instr.text, re.IGNORECASE):
                        has_toc_table_field = True
                        print(f"PASS: Component 1 — TOC field with Table category found: {instr.text!r} (0.30 pts)")
                        total_score += 0.30
                        break
            if has_toc_table_field:
                break

        if not has_toc_table_field:
            print("FAIL: Component 1 — No TOC field code with category 'Table' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: All 8 table captions listed in index (0.40 points)
    # Index entries should appear between 'List of Tables' and
    # '1. Executive Summary' headings. Each entry text should match
    # one of the 8 expected table captions.
    # ---------------------------------------------------------------
    try:
        # Find the region between 'List of Tables' and '1. Executive Summary'
        paras = doc.paragraphs
        lot_idx = None
        exec_idx = None
        for i, p in enumerate(paras):
            if p.style and p.style.name.startswith('Heading') and 'List of Tables' in p.text:
                lot_idx = i
            if p.style and p.style.name.startswith('Heading') and 'Executive Summary' in p.text:
                exec_idx = i
                break

        if lot_idx is None or exec_idx is None:
            print("FAIL: Component 2 — Could not find 'List of Tables' or 'Executive Summary' headings")
        else:
            # Collect index entry texts from the region
            index_texts = []
            for i in range(lot_idx + 1, exec_idx):
                text = paras[i].text.strip()
                if text:
                    index_texts.append(text)

            # Check how many of the 8 expected tables are present
            found_count = 0
            for expected in EXPECTED_TABLES:
                # Each index entry may have a page number appended (e.g., "Table 1: Sales by Region\t2")
                matched = False
                for entry_text in index_texts:
                    # Strip trailing page numbers and tabs
                    clean_entry = re.sub(r'[\t ]+\d+\s*$', '', entry_text).strip()
                    # Also handle entries where page number is stuck to text
                    clean_entry2 = re.sub(r'\d+\s*$', '', entry_text).strip()
                    if expected in entry_text or expected == clean_entry or expected == clean_entry2:
                        matched = True
                        break
                if matched:
                    found_count += 1

            if found_count == 8:
                print(f"PASS: Component 2 — All 8 table captions found in index entries (0.40 pts)")
                total_score += 0.40
            elif found_count > 0:
                partial = round(0.40 * (found_count / 8), 2)
                print(f"PARTIAL: Component 2 — {found_count}/8 table captions found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No table captions found in index area. Index entries: {index_texts[:3]}...")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Each index entry has a page number (0.15 points)
    # Entries should contain a tab + numeric page reference.
    # ---------------------------------------------------------------
    try:
        if lot_idx is not None and exec_idx is not None:
            entries_with_page = 0
            total_entries = 0
            for i in range(lot_idx + 1, exec_idx):
                text = paras[i].text.strip()
                if text and any(expected.split(':')[0] in text for expected in EXPECTED_TABLES):
                    total_entries += 1
                    # Check for page number (digit after tab or at end)
                    if re.search(r'\t\s*\d+', text) or re.search(r'\d+\s*$', text):
                        entries_with_page += 1

            if total_entries > 0 and entries_with_page == total_entries:
                print(f"PASS: Component 3 — All {total_entries} index entries have page numbers (0.15 pts)")
                total_score += 0.15
            elif entries_with_page > 0:
                partial = round(0.15 * (entries_with_page / max(total_entries, 1)), 2)
                print(f"PARTIAL: Component 3 — {entries_with_page}/{total_entries} entries have page numbers ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No page numbers found in index entries")
        else:
            print(f"FAIL: Component 3 — Could not locate index area (headings not found)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Index entries are correctly positioned (0.15 points)
    # The index content must be between 'List of Tables' heading
    # and '1. Executive Summary' heading, and there must be multiple
    # non-empty paragraphs in that region (at least 8 for 8 tables).
    # ---------------------------------------------------------------
    try:
        if lot_idx is not None and exec_idx is not None:
            non_empty_between = 0
            for i in range(lot_idx + 1, exec_idx):
                if paras[i].text.strip():
                    non_empty_between += 1

            if non_empty_between >= 8:
                print(f"PASS: Component 4 — {non_empty_between} non-empty paragraphs between headings (>= 8 expected) (0.15 pts)")
                total_score += 0.15
            elif non_empty_between > 0:
                partial = round(0.15 * min(non_empty_between / 8, 1.0), 2)
                print(f"PARTIAL: Component 4 — Only {non_empty_between} non-empty paragraphs between headings ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No content between 'List of Tables' and 'Executive Summary'")
        else:
            print(f"FAIL: Component 4 — Could not locate index area")
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
