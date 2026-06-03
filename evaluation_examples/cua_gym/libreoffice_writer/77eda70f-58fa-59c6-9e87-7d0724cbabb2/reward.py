"""
Reward Script: Configure mixed page numbering (Roman for preface, Arabic for main content)
Task ID: writer_af_019
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Section 0 page number format is lowerRoman
  Component 2 (0.35): Section 1 page number start is 1 (restart Arabic numbering)
  Component 3 (0.25): Section 0 pgNumType start is 1 AND section 1 fmt is decimal (compound integrity)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_af_019'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    - Pages 1-4 (section 0): Roman numeral page numbering (lowerRoman)
    - Page 5 onward (section 1): Arabic numbering restarted from 1

    Initial state has both sections using decimal format, with section 1 starting at 5.
    Golden state changes section 0 to lowerRoman and section 1 start to 1.
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least 2 sections
    if len(doc.sections) < 2:
        print(f"PRECONDITION FAIL: Expected at least 2 sections, found {len(doc.sections)}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Helper to get pgNumType attributes for a section
    def get_pgnum_attrs(section_index):
        sec = doc.sections[section_index]
        sectPr = sec._sectPr
        pgNumType = sectPr.find('.//w:pgNumType', ns)
        if pgNumType is None:
            return {}
        attrs = {}
        for key, val in pgNumType.attrib.items():
            # Strip namespace from attribute name
            local_name = key.split('}')[-1] if '}' in key else key
            attrs[local_name] = val
        return attrs

    sec0_attrs = get_pgnum_attrs(0)
    sec1_attrs = get_pgnum_attrs(1)

    print(f"Section 0 pgNumType: {sec0_attrs}")
    print(f"Section 1 pgNumType: {sec1_attrs}")

    # Component 1: Section 0 page number format is lowerRoman (0.40 points)
    # Initial has 'decimal', golden should have 'lowerRoman'
    try:
        sec0_fmt = sec0_attrs.get('fmt', '')
        if sec0_fmt == 'lowerRoman':
            print(f"PASS: Component 1 - Section 0 fmt is 'lowerRoman' (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 - Expected section 0 fmt='lowerRoman', found '{sec0_fmt}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Section 1 page number start is 1 (0.35 points)
    # Initial has start='5', golden should have start='1' (restart from 1)
    try:
        sec1_start = sec1_attrs.get('start', '')
        if sec1_start == '1':
            print(f"PASS: Component 2 - Section 1 start is '1' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - Expected section 1 start='1', found '{sec1_start}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Compound integrity check (0.25 points)
    # Section 0 starts at page 1 AND section 1 uses decimal format
    # This verifies the overall numbering scheme is correct:
    #   - preface starts at Roman i (start=1)
    #   - main content uses Arabic (fmt=decimal)
    # In initial_env: sec0 start=1 AND sec1 fmt=decimal => both true,
    # BUT we anchor this to the lowerRoman change: score only if sec0 is lowerRoman
    try:
        sec0_start = sec0_attrs.get('start', '')
        sec1_fmt = sec1_attrs.get('fmt', '')
        # Only award if section 0 is Roman AND section 1 is decimal AND section 0 starts at 1
        if sec0_fmt == 'lowerRoman' and sec1_fmt == 'decimal' and sec0_start == '1':
            print(f"PASS: Component 3 - Full numbering scheme correct: Roman(start=1) + Decimal (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Incomplete numbering scheme: sec0 fmt={sec0_fmt}, start={sec0_start}; sec1 fmt={sec1_fmt}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
