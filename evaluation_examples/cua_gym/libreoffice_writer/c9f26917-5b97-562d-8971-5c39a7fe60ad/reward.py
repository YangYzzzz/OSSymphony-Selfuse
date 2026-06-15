"""
Reward Script: Continuous page numbering across chapter sections
Task ID: writer_rm_062
Domain: libreoffice_writer
Scoring: Verify that sections 2-5 (Ch2-Ch5) have continuous page numbering
         (no w:start attribute on pgNumType) while section 0 (Preface) keeps
         lowerRoman and section 1 (Ch1) keeps decimal start=1.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_062'


def persist_app_state(domain):
    """Try to save any unsaved state in LibreOffice."""
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

    The task requires continuous page numbering across chapter sections (2-5).
    In the initial state, every chapter section restarts numbering (start="1").
    In the golden state, sections 2-5 have no start attribute (continuous numbering).

    Scoring:
      - Precondition: File loads, has 6 sections, section 0 is lowerRoman, section 1 is decimal with start=1
      - Component 1: Section 2 (Ch2) has no start attribute (0.25 pts)
      - Component 2: Section 3 (Ch3) has no start attribute (0.25 pts)
      - Component 3: Section 4 (Ch4) has no start attribute (0.25 pts)
      - Component 4: Section 5 (Ch5) has no start attribute (0.25 pts)
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Missing dependency: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Document has 6 sections
    sections = doc.sections
    if len(sections) < 6:
        print(f"PRECONDITION FAIL: Expected 6 sections, found {len(sections)}")
        print("REWARD: 0.0")
        return 0.0
    print(f"PRECONDITION PASS: Document has {len(sections)} sections")

    # Precondition: Section 0 (Preface) uses lowerRoman format
    try:
        sec0_sectPr = sections[0]._sectPr
        pgNumType0 = sec0_sectPr.find(qn('w:pgNumType'))
        if pgNumType0 is not None:
            fmt0 = pgNumType0.get(qn('w:fmt'))
            if fmt0 == 'lowerRoman':
                print(f"PRECONDITION PASS: Section 0 (Preface) uses lowerRoman format")
            else:
                print(f"PRECONDITION WARN: Section 0 fmt={fmt0}, expected lowerRoman")
        else:
            print(f"PRECONDITION WARN: Section 0 has no pgNumType element")
    except Exception as e:
        print(f"PRECONDITION ERROR: Section 0 check failed: {e}")

    # Precondition: Section 1 (Ch1) uses decimal with start=1
    try:
        sec1_sectPr = sections[1]._sectPr
        pgNumType1 = sec1_sectPr.find(qn('w:pgNumType'))
        if pgNumType1 is not None:
            fmt1 = pgNumType1.get(qn('w:fmt'))
            start1 = pgNumType1.get(qn('w:start'))
            if fmt1 == 'decimal' and start1 == '1':
                print(f"PRECONDITION PASS: Section 1 (Ch1) uses decimal with start=1")
            else:
                print(f"PRECONDITION WARN: Section 1 fmt={fmt1}, start={start1}")
        else:
            print(f"PRECONDITION WARN: Section 1 has no pgNumType element")
    except Exception as e:
        print(f"PRECONDITION ERROR: Section 1 check failed: {e}")

    # Helper: check if a section has continuous numbering (no start attribute)
    def section_has_continuous_numbering(sec_index):
        """Returns True if the section's pgNumType has no 'start' attribute (continuous)."""
        sectPr = sections[sec_index]._sectPr
        pgNumType = sectPr.find(qn('w:pgNumType'))
        if pgNumType is None:
            # No pgNumType element at all means default (continuous)
            return True
        start_val = pgNumType.get(qn('w:start'))
        # start=None means no restart, i.e., continuous numbering
        return start_val is None

    # Component 1: Section 2 (Ch2) has continuous numbering (0.25 points)
    try:
        if section_has_continuous_numbering(2):
            print(f"PASS: Component 1 -- Section 2 (Ch2) has continuous numbering (0.25 pts)")
            total_score += 0.25
        else:
            sectPr = sections[2]._sectPr
            pgNumType = sectPr.find(qn('w:pgNumType'))
            start_val = pgNumType.get(qn('w:start')) if pgNumType is not None else 'N/A'
            print(f"FAIL: Component 1 -- Section 2 (Ch2) restarts numbering (start={start_val})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section 3 (Ch3) has continuous numbering (0.25 points)
    try:
        if section_has_continuous_numbering(3):
            print(f"PASS: Component 2 -- Section 3 (Ch3) has continuous numbering (0.25 pts)")
            total_score += 0.25
        else:
            sectPr = sections[3]._sectPr
            pgNumType = sectPr.find(qn('w:pgNumType'))
            start_val = pgNumType.get(qn('w:start')) if pgNumType is not None else 'N/A'
            print(f"FAIL: Component 2 -- Section 3 (Ch3) restarts numbering (start={start_val})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Section 4 (Ch4) has continuous numbering (0.25 points)
    try:
        if section_has_continuous_numbering(4):
            print(f"PASS: Component 3 -- Section 4 (Ch4) has continuous numbering (0.25 pts)")
            total_score += 0.25
        else:
            sectPr = sections[4]._sectPr
            pgNumType = sectPr.find(qn('w:pgNumType'))
            start_val = pgNumType.get(qn('w:start')) if pgNumType is not None else 'N/A'
            print(f"FAIL: Component 3 -- Section 4 (Ch4) restarts numbering (start={start_val})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Section 5 (Ch5) has continuous numbering (0.25 points)
    try:
        if section_has_continuous_numbering(5):
            print(f"PASS: Component 4 -- Section 5 (Ch5) has continuous numbering (0.25 pts)")
            total_score += 0.25
        else:
            sectPr = sections[5]._sectPr
            pgNumType = sectPr.find(qn('w:pgNumType'))
            start_val = pgNumType.get(qn('w:start')) if pgNumType is not None else 'N/A'
            print(f"FAIL: Component 4 -- Section 5 (Ch5) restarts numbering (start={start_val})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
