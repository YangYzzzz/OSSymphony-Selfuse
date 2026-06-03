"""
Reward Script: Format JoinDate merge field to display as full date (e.g., 'March 15, 2025')
Task ID: writer_mt_019
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): JoinDate merge field has a date format switch (\\@)
  Component 2 (0.3): Format switch contains long-date pattern (full month name)
  Component 3 (0.3): Cached/displayed value is in long date format, not ISO
"""

import os
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_019'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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


def find_merge_field_info(doc_element, field_name):
    """
    Walk the XML to find a MERGEFIELD with the given name.
    Returns a dict with:
      - 'found': bool
      - 'instr_text': the full instrText content for this field
      - 'cached_value': the text between separate and end fldChars
    """
    result = {'found': False, 'instr_text': '', 'cached_value': ''}

    # Collect all runs in document order from the body
    body = doc_element.body
    all_runs = list(body.iter(f'{{{W_NS}}}r'))

    # Walk through runs tracking field state
    in_field = False
    field_instr = ''
    after_separate = False
    cached_parts = []
    target_field = False

    for run in all_runs:
        fld_chars = run.findall(f'{{{W_NS}}}fldChar', NS)
        instr_texts = run.findall(f'{{{W_NS}}}instrText', NS)
        t_elems = run.findall(f'{{{W_NS}}}t', NS)

        for fc in fld_chars:
            ftype = fc.get(f'{{{W_NS}}}fldCharType')
            if ftype == 'begin':
                in_field = True
                field_instr = ''
                after_separate = False
                cached_parts = []
                target_field = False
            elif ftype == 'separate':
                # Check if this is the target field
                if field_name.upper() in field_instr.upper():
                    target_field = True
                after_separate = True
            elif ftype == 'end':
                if target_field:
                    result['found'] = True
                    result['instr_text'] = field_instr.strip()
                    result['cached_value'] = ''.join(cached_parts).strip()
                    return result
                in_field = False
                after_separate = False

        for it in instr_texts:
            if in_field and not after_separate:
                field_instr += (it.text or '')

        if after_separate and target_field:
            for t in t_elems:
                cached_parts.append(t.text or '')

    return result


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

    # Find the JoinDate merge field
    field_info = find_merge_field_info(doc.element, 'JoinDate')

    if not field_info['found']:
        print("CRITICAL: JoinDate merge field not found in document")
        print("REWARD: 0.0")
        return 0.0

    instr = field_info['instr_text']
    cached = field_info['cached_value']
    print(f"INFO: JoinDate instrText = {repr(instr)}")
    print(f"INFO: JoinDate cached value = {repr(cached)}")

    # Component 1: JoinDate merge field has a date format switch (\@) (0.4 points)
    try:
        # The \@ switch in Word field codes specifies date/time formatting
        if r'\@' in instr or '\\@' in instr:
            print(f"PASS: Component 1 -- JoinDate field has date format switch (\\@) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- JoinDate field missing date format switch (\\@). instrText: {repr(instr)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Format switch contains long-date pattern with full month name (0.3 points)
    try:
        # Long date patterns use MMMM (full month name) in the format string
        # Accept variations: MMMM d, yyyy / MMMM D, YYYY / etc.
        instr_upper = instr.upper()
        if 'MMMM' in instr_upper:
            print(f"PASS: Component 2 -- Format switch contains MMMM (full month name) pattern (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Format switch does not contain MMMM pattern. instrText: {repr(instr)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Cached/displayed value is in long date format (0.3 points)
    try:
        # The cached value should look like "March 15, 2025" (full month name + day + year)
        # and NOT be in ISO format "2025-03-15"
        # Match pattern: <FullMonthName> <day>, <year>
        long_date_pattern = re.compile(
            r'(January|February|March|April|May|June|July|August|September|October|November|December)'
            r'\s+\d{1,2},?\s+\d{4}',
            re.IGNORECASE
        )
        iso_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

        if long_date_pattern.search(cached):
            print(f"PASS: Component 3 -- Cached value '{cached}' is in long date format (0.3 pts)")
            total_score += 0.3
        elif iso_pattern.search(cached):
            print(f"FAIL: Component 3 -- Cached value '{cached}' is still in ISO format")
        else:
            print(f"FAIL: Component 3 -- Cached value '{cached}' does not match expected long date format")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
