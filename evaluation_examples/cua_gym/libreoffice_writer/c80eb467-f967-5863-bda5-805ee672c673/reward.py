"""
Reward Script: Page numbering with Roman numerals for TOC and Arabic restart for main content
Task ID: writer_fs_093
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Section 1 (TOC) page number format is lowerRoman
  Component 2 (0.30): Section 1 (TOC) page numbering starts at 2
  Component 3 (0.30): Section 2 (main content) page numbering restarts at 1
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_093'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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

    Task: Set page numbering so TOC pages (pages 2-4) show lowercase Roman
    numerals (ii, iii, iv) and main content restarts at Arabic numeral 1 on page 5.

    Expected section structure (3 sections):
      Section 0: Title page (no page number)
      Section 1: TOC pages -> lowerRoman format, starting at 2
      Section 2: Main content -> decimal format, starting at 1
    """
    total_score = 0.0

    # Precondition: load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least 3 sections
    num_sections = len(doc.sections)
    if num_sections < 3:
        print(f"PRECONDITION FAIL: Expected >= 3 sections, found {num_sections}")
        print("REWARD: 0.0")
        return 0.0

    print(f"PRECONDITION: Document has {num_sections} sections (>= 3 required)")

    # Helper: extract pgNumType attributes from a section
    def get_pgnum_info(section):
        """Returns (fmt, start) from w:pgNumType element, or (None, None) if absent."""
        sect_pr = section._sectPr
        pgnum_el = sect_pr.find(qn('w:pgNumType'))
        if pgnum_el is None:
            return (None, None)
        fmt = pgnum_el.get(qn('w:fmt'))
        start_str = pgnum_el.get(qn('w:start'))
        start = int(start_str) if start_str is not None else None
        return (fmt, start)

    sec1 = doc.sections[1]  # TOC section
    sec2 = doc.sections[2]  # Main content section

    sec1_fmt, sec1_start = get_pgnum_info(sec1)
    sec2_fmt, sec2_start = get_pgnum_info(sec2)

    print(f"Section 1 (TOC):     fmt={sec1_fmt}, start={sec1_start}")
    print(f"Section 2 (Main):    fmt={sec2_fmt}, start={sec2_start}")

    # Component 1: Section 1 (TOC) page number format is lowerRoman (0.40 points)
    # Initial has decimal; golden should have lowerRoman
    try:
        if sec1_fmt == 'lowerRoman':
            print(f"PASS: Component 1 -- TOC section uses lowerRoman format (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 -- Expected lowerRoman format for TOC, found: {sec1_fmt}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section 1 (TOC) page numbering starts at 2 (0.30 points)
    # Initial has no start value; golden should start at 2 (for ii)
    try:
        if sec1_start == 2:
            print(f"PASS: Component 2 -- TOC section starts at page number 2 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- Expected TOC start=2, found: {sec1_start}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Section 2 (main content) page numbering restarts at 1 (0.30 points)
    # Initial has no start value; golden should restart at 1
    try:
        if sec2_start == 1:
            print(f"PASS: Component 3 -- Main content section restarts at page number 1 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- Expected main content start=1, found: {sec2_start}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
