"""
Reward Script: Page numbering with Roman numerals for front matter, Arabic restarting at 1 for main body
Task ID: writer_fs_064
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.30): Document has 2+ sections (section break between front matter and main body)
  - Component 2 (0.30): Section 0 (front matter) uses lowerRoman page number format
  - Component 3 (0.25): Section 1 (main body) uses decimal format with start=1
  - Component 4 (0.15): Section 1 has its own footer with PAGE field code
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_064'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
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
    Verify page numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sections = doc.sections

    # Component 1: Document has 2+ sections (0.30 points)
    # Initial has only 1 section; golden should have 2 (front matter + main body)
    try:
        num_sections = len(sections)
        if num_sections >= 2:
            print(f"PASS: Component 1 - Document has {num_sections} sections (>= 2) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Document has {num_sections} section(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Section 0 (front matter) uses lowerRoman page number format (0.30 points)
    # Initial has no pgNumType at all; golden section 0 should have fmt=lowerRoman
    try:
        if len(sections) >= 1:
            sec0 = sections[0]._sectPr
            pgNumType0 = sec0.find(qn('w:pgNumType'))
            if pgNumType0 is not None:
                fmt0 = pgNumType0.get(qn('w:fmt'))
                if fmt0 == 'lowerRoman':
                    print(f"PASS: Component 2 - Section 0 pgNumType fmt=lowerRoman (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 - Section 0 fmt={fmt0}, expected lowerRoman")
            else:
                print(f"FAIL: Component 2 - Section 0 has no pgNumType element")
        else:
            print(f"FAIL: Component 2 - No sections found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Section 1 (main body) uses decimal format with start=1 (0.25 points)
    # Initial has no second section; golden section 1 should have fmt=decimal, start=1
    try:
        if len(sections) >= 2:
            sec1 = sections[1]._sectPr
            pgNumType1 = sec1.find(qn('w:pgNumType'))
            if pgNumType1 is not None:
                fmt1 = pgNumType1.get(qn('w:fmt'))
                start1 = pgNumType1.get(qn('w:start'))
                # fmt can be decimal or None (default is decimal)
                fmt_ok = fmt1 in ('decimal', None)
                start_ok = start1 == '1'
                if fmt_ok and start_ok:
                    print(f"PASS: Component 3 - Section 1 fmt={fmt1}, start={start1} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 - Section 1 fmt={fmt1} (need decimal), start={start1} (need 1)")
            else:
                print(f"FAIL: Component 3 - Section 1 has no pgNumType element")
        else:
            print(f"FAIL: Component 3 - Less than 2 sections, cannot check section 1")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Section 1 has its own footer with PAGE field code (0.15 points)
    # This ensures page numbers actually display in the main body section
    try:
        if len(sections) >= 2:
            footer1 = sections[1].footer
            footer_xml = footer1._element.xml
            has_page_field = 'PAGE' in footer_xml and 'instrText' in footer_xml
            if has_page_field:
                print(f"PASS: Component 4 - Section 1 footer has PAGE field code (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Section 1 footer missing PAGE field code")
        else:
            print(f"FAIL: Component 4 - Less than 2 sections, cannot check section 1 footer")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
