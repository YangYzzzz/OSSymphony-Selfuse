"""
Reward Script: Insert date field and author field in document header
Task ID: writer_struct_056
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Header contains required static text 'Date: ' and ' | Author: '
  Component 2 (0.35): A DATE field (w:instrText containing DATE) is present in the header
  Component 3 (0.30): An AUTHOR field (w:instrText containing AUTHOR) is present in the header
Total: 1.0
"""

import os
import lxml.etree as etree

from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_056'
FILE_PATH = '/home/user/Desktop/lab_notebook.docx'

# XML namespaces for field code inspection
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def get_header_instr_texts(header):
    """Extract all instrText values from the header element."""
    instr_texts = []
    for elem in header._element.iter(qn('w:instrText')):
        if elem.text:
            instr_texts.append(elem.text.strip())
    return instr_texts


def get_header_plain_text(header):
    """Get the plain text content of all header paragraphs."""
    texts = []
    for para in header.paragraphs:
        texts.append(para.text)
    return ' '.join(texts)


def verify_task(file_path):
    """
    Verify that a DATE field and an AUTHOR field were inserted in the document header,
    formatted as 'Date: [date] | Author: [author]'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have at least one section with a header
    try:
        section = doc.sections[0]
        header = section.header
    except Exception as e:
        print(f"CRITICAL: Cannot access document header: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Header contains required static text 'Date: ' and ' | Author: ' (0.35 points)
    # The task specifies the format: 'Date: [date] | Author: [author]'
    # Static labels 'Date: ' and '| Author: ' must be present as literal text in header.
    try:
        header_text = get_header_plain_text(header)
        has_date_label = 'Date:' in header_text
        has_author_label = 'Author:' in header_text
        has_separator = '|' in header_text

        if has_date_label and has_author_label and has_separator:
            print(f"PASS: Component 1 — Header contains 'Date:', '|', and 'Author:' labels (header text: {repr(header_text[:80])}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Missing required text labels in header. "
                  f"has_date_label={has_date_label}, has_author_label={has_author_label}, "
                  f"has_separator={has_separator}. Header text: {repr(header_text[:80])}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check header text: {e}")

    # Component 2: A DATE field is present in the header (0.35 points)
    # The task says 'insert a date field using Insert > Field'.
    # This translates to a <w:instrText> element containing 'DATE' in the header XML.
    try:
        instr_texts = get_header_instr_texts(header)
        date_field_found = any('DATE' in instr.upper() for instr in instr_texts)

        if date_field_found:
            matching = [t for t in instr_texts if 'DATE' in t.upper()]
            print(f"PASS: Component 2 — DATE field found in header instrText: {matching} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — No DATE field found in header. instrText values found: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check DATE field: {e}")

    # Component 3: An AUTHOR field is present in the header (0.30 points)
    # The task says 'insert an author field using Insert > Field'.
    # This translates to a <w:instrText> element containing 'AUTHOR' in the header XML.
    try:
        # Re-use instr_texts from component 2 if available, else re-fetch
        if 'instr_texts' not in dir():
            instr_texts = get_header_instr_texts(header)
        author_field_found = any('AUTHOR' in instr.upper() for instr in instr_texts)

        if author_field_found:
            matching = [t for t in instr_texts if 'AUTHOR' in t.upper()]
            print(f"PASS: Component 3 — AUTHOR field found in header instrText: {matching} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — No AUTHOR field found in header. instrText values found: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check AUTHOR field: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
