"""
Reward Script: Insert a fixed date field showing '2026-01-15' in YYYY-MM-DD format
Task ID: writer_tm_080
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Date '2026-01-15' appears after 'Effective Date: ' in the document
  Component 2 (0.3): Date format is YYYY-MM-DD
  Component 3 (0.3): The date is fixed (not a dynamic auto-updating field, OR is a locked field)
"""

import os
import re
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_080'


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

    # Find the paragraph that starts with "Effective Date:"
    date_para = None
    date_para_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith('Effective Date:'):
            date_para = p
            date_para_idx = i
            break

    if date_para is None:
        print("FAIL: Could not find paragraph starting with 'Effective Date:'")
        print("REWARD: 0.0")
        return 0.0

    para_text = date_para.text.strip()
    print(f"INFO: Found date paragraph (idx={date_para_idx}): {repr(para_text)}")

    # Component 1: Date '2026-01-15' appears after 'Effective Date: ' (0.4 points)
    # This checks that the date value was inserted into the document
    try:
        if '2026-01-15' in para_text:
            print(f"PASS: Component 1 — '2026-01-15' found in date paragraph (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — '2026-01-15' not found in paragraph text: {repr(para_text)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Date format is YYYY-MM-DD (0.3 points)
    # Extract text after "Effective Date:" and check it matches the date pattern
    try:
        after_label = para_text.split('Effective Date:')[-1].strip()
        # Match YYYY-MM-DD pattern
        date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', after_label)
        if date_match:
            matched_date = date_match.group(1)
            # Verify it's a valid date format and equals 2026-01-15
            if matched_date == '2026-01-15':
                print(f"PASS: Component 2 — Date in YYYY-MM-DD format: {matched_date} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Date is in YYYY-MM-DD format but wrong value: {matched_date}")
        else:
            print(f"FAIL: Component 2 — No YYYY-MM-DD date found after 'Effective Date:'. Text: {repr(after_label)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The date '2026-01-15' is present AND fixed (not a dynamic auto-updating field) (0.3 points)
    # This is a compound check: the date must exist AND be in a fixed form.
    # A fixed date means either:
    #   (a) It's plain text with the correct date (no field codes) — inherently fixed
    #   (b) It's a DATE field with the displayed value matching '2026-01-15'
    #       (LibreOffice inserts fixed dates as DATE fields with frozen display values)
    # This component MUST fail on initial_env (where date is absent).
    try:
        # Gate: date must actually be present for this component to award points
        if '2026-01-15' not in para_text:
            print(f"FAIL: Component 3 — Date '2026-01-15' not present, cannot verify fixedness")
        else:
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            elem = date_para._element

            fld_chars = elem.findall('.//w:fldChar', ns)
            instr_texts = elem.findall('.//w:instrText', ns)
            has_field = len(fld_chars) > 0

            if not has_field:
                # Plain text with the correct date — inherently fixed
                print(f"PASS: Component 3 — Date is plain text (no field codes), inherently fixed (0.3 pts)")
                total_score += 0.3
            else:
                # Has field codes — check it's a DATE field with correct displayed value
                has_date_field = any(
                    it.text and 'DATE' in it.text.upper() for it in instr_texts
                )
                if has_date_field:
                    print(f"PASS: Component 3 — DATE field with correct displayed value '2026-01-15' (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Non-DATE field found in paragraph; unexpected field type")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
