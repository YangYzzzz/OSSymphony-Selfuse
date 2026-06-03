"""
Reward Script: Insert date, page number, and page count fields in footer
Task ID: writer_struct_069
Domain: libreoffice_writer
Scoring:
  Component 1: Footer contains a DATE field (fldChar begin/instrText ' DATE '/end) — 0.35 pts
  Component 2: Footer contains a PAGE field (fldChar begin/instrText ' PAGE '/end) — 0.35 pts
  Component 3: Footer contains a NUMPAGES field (fldChar begin/instrText ' NUMPAGES '/end) — 0.30 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_069'
FILE_PATH = f'{WORKDIR}/Desktop/audit_report.docx'

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_footer_instr_texts(doc):
    """
    Extract all instrText values found inside fldChar field blocks in the first section's footer.
    Returns a list of stripped, uppercased field instruction strings.
    """
    section = doc.sections[0]
    footer = section.footer
    instr_texts = []
    for para in footer.paragraphs:
        for elem in para._element.iter(f'{{{NS}}}instrText'):
            instr_texts.append(elem.text.strip().upper())
    return instr_texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document; critical failure returns 0.0 immediately
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify footer exists and is accessible
    try:
        section = doc.sections[0]
        footer = section.footer
        if footer is None:
            print("CRITICAL: Footer not found in document.")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot access footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all field instruction texts in the footer
    instr_texts = get_footer_instr_texts(doc)
    print(f"DEBUG: Footer field instrText values found: {instr_texts}")

    # Component 1: Footer contains a DATE field (0.35 points)
    # Task requires 'Date: [date_field]' — verified by presence of DATE instrText in footer
    # This FAILS on initial_env (empty footer) and PASSES on golden_env
    try:
        if 'DATE' in instr_texts:
            print("PASS: Component 1 — DATE field found in footer (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — DATE field NOT found in footer. Expected instrText 'DATE'.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer contains a PAGE number field (0.35 points)
    # Task requires 'Page [page_number_field]' — verified by presence of PAGE instrText in footer
    # This FAILS on initial_env (empty footer) and PASSES on golden_env
    try:
        if 'PAGE' in instr_texts:
            print("PASS: Component 2 — PAGE field found in footer (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — PAGE field NOT found in footer. Expected instrText 'PAGE'.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer contains a NUMPAGES (page count / total pages) field (0.30 points)
    # Task requires 'of [total_pages_field]' — verified by presence of NUMPAGES instrText in footer
    # This FAILS on initial_env (empty footer) and PASSES on golden_env
    try:
        if 'NUMPAGES' in instr_texts:
            print("PASS: Component 3 — NUMPAGES field found in footer (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 3 — NUMPAGES field NOT found in footer. Expected instrText 'NUMPAGES'.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
