"""
Reward Script: Place page numbers in bottom-right footer instead of center
Task ID: writer_page_030
Domain: libreoffice_writer
Scoring:
  Component 1: Footer paragraph alignment is RIGHT (not CENTER) — 0.6 pts
  Component 2: Footer is RIGHT-aligned AND PAGE field code is intact — 0.4 pts
Total: 1.0
"""

import os

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_030'
FILE_PATH = f'{WORKDIR}/user_guide.docx'


def has_page_field(para):
    """
    Check if a paragraph contains a PAGE field code instruction (w:instrText with ' PAGE ').
    Page number fields are stored as fldChar/instrText elements, not as visible text.
    """
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    for elem in para._element.iter(f'{{{ns}}}instrText'):
        if 'PAGE' in (elem.text or ''):
            return True
    return False


def verify_task(file_path):
    """
    Verify that the footer page number has been moved from center to right alignment.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate footer paragraphs across all sections
    footer_paras = []
    try:
        for section in doc.sections:
            footer = section.footer
            if footer:
                for para in footer.paragraphs:
                    footer_paras.append(para)
    except Exception as e:
        print(f"CRITICAL: Cannot read footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not footer_paras:
        print("FAIL: No footer paragraphs found in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Identify the footer paragraph that contains page number field code
    page_num_para = None
    for para in footer_paras:
        if has_page_field(para):
            page_num_para = para
            break

    # Fallback: if no explicit PAGE field found, use first footer paragraph
    if page_num_para is None:
        page_num_para = footer_paras[0]
        print("INFO: No explicit PAGE field found; using first footer paragraph for alignment check")

    actual_alignment = page_num_para.paragraph_format.alignment

    # Component 1: Footer paragraph alignment is RIGHT (0.6 points)
    # Task requires: move page number from center to bottom-right corner
    # FAILS on initial_env (CENTER) — PASSES on golden_env (RIGHT)
    try:
        if actual_alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT:
            print(f"PASS: Component 1 — Footer alignment is RIGHT (0.6 pts)")
            total_score += 0.6
        else:
            alignment_name = str(actual_alignment) if actual_alignment is not None else "None/inherited"
            print(f"FAIL: Component 1 — Expected RIGHT alignment, found: {alignment_name}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer is RIGHT-aligned AND PAGE field code is intact (0.4 points)
    # Compound check: ensures the page number is still present after the alignment change.
    # Only awards points if alignment is RIGHT (task change) AND field code is preserved.
    # FAILS on initial_env (CENTER) — PASSES on golden_env (RIGHT + PAGE field)
    try:
        page_field_present = has_page_field(page_num_para)
        if actual_alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT and page_field_present:
            print(f"PASS: Component 2 — Footer is RIGHT-aligned AND PAGE field code is intact (0.4 pts)")
            total_score += 0.4
        elif actual_alignment != WD_PARAGRAPH_ALIGNMENT.RIGHT:
            print(f"FAIL: Component 2 — Footer alignment is not RIGHT; page field present={page_field_present}")
        else:
            print(f"FAIL: Component 2 — Footer is RIGHT-aligned but PAGE field code not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
