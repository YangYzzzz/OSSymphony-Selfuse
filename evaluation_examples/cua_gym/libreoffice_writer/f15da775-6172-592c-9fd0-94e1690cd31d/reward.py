"""
Reward Script: Insert Date and File Name fields in footer
Task ID: writer_fs_079
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Footer contains a DATE field with dd/MM/yyyy format
  Component 2 (0.25): Footer contains a FILENAME field
  Component 3 (0.20): Right-aligned tab stop in footer paragraph
  Component 4 (0.20): Footer text has date-like pattern on left and filename on right separated by tab
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_079'


def find_date_field(instr_texts):
    """Search instrText elements for a DATE field. Returns (found, format_ok)."""
    for instr in instr_texts:
        text = instr.text or ''
        if 'DATE' in text.upper():
            fmt_ok = bool(
                re.search(r'dd[/\\-]MM[/\\-]yyyy', text, re.IGNORECASE)
                or re.search(r'dd[/\\-]MM[/\\-]YYYY', text)
            )
            return (True, fmt_ok)
    return (False, False)


def find_filename_field(instr_texts):
    """Search instrText elements for a FILENAME field."""
    for instr in instr_texts:
        text = instr.text or ''
        if 'FILENAME' in text.upper():
            return True
    return False


def find_right_tab_stop(footer_element, ns):
    """Check if any footer paragraph has a right-aligned tab stop definition."""
    for para_elem in footer_element.findall('.//w:p', ns):
        pPr = para_elem.find('w:pPr', ns)
        if pPr is not None:
            for tab_def in pPr.findall('.//w:tab', ns):
                val = tab_def.get(f'{{{ns["w"]}}}val', '')
                if val == 'right':
                    return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the footer from the first section
    try:
        section = doc.sections[0]
        footer = section.footer
    except Exception as e:
        print(f"CRITICAL: Cannot access footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    instr_texts = footer._element.findall('.//w:instrText', ns)

    # Component 1: DATE field with dd/MM/yyyy format (0.35 points)
    try:
        date_found, date_fmt_ok = find_date_field(instr_texts)
        if date_found and date_fmt_ok:
            print(f"PASS: Component 1 -- DATE field with dd/MM/yyyy format found (0.35 pts)")
            total_score += 0.35
        elif date_found:
            print(f"PARTIAL: Component 1 -- DATE field found but format may not be dd/MM/yyyy (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- No DATE field found in footer")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: FILENAME field present (0.25 points)
    try:
        if find_filename_field(instr_texts):
            print(f"PASS: Component 2 -- FILENAME field found in footer (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No FILENAME field found in footer")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Right-aligned tab stop in footer paragraph (0.20 points)
    try:
        if find_right_tab_stop(footer._element, ns):
            print(f"PASS: Component 3 -- Right-aligned tab stop found in footer (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- No right-aligned tab stop found in footer paragraph")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Footer text contains date pattern + tab + filename pattern (0.20 points)
    try:
        footer_text = ''
        for para in footer.paragraphs:
            footer_text += para.text

        # Check for a date-like pattern (dd/mm/yyyy) and filename
        has_date_pattern = bool(re.search(r'\d{2}/\d{2}/\d{4}', footer_text))
        has_filename = TASK_ID in footer_text
        has_tab_separator = '\t' in footer_text

        if has_date_pattern and has_filename and has_tab_separator:
            print(f"PASS: Component 4 -- Footer text has date, tab, and filename (0.20 pts)")
            total_score += 0.20
        elif has_date_pattern and has_filename:
            print(f"PARTIAL: Component 4 -- Date and filename present but no tab separator (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not has_date_pattern:
                missing.append('date pattern')
            if not has_filename:
                missing.append('filename')
            if not has_tab_separator:
                missing.append('tab separator')
            print(f"FAIL: Component 4 -- Missing in footer: {', '.join(missing)}. Footer text: [{footer_text}]")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
