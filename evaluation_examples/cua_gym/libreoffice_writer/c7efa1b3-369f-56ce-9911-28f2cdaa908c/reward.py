"""
Reward Script: Journal entry formatting task — apply heading styles and borders
Task ID: writer_creative_042
Domain: libreoffice_writer
Scoring:
  Component 1: Document title 'My Journal — 2026' has Heading 1 style (0.2 pts)
  Component 2: All 5 date lines have Heading 2 style (0.5 pts — 0.1 per heading)
  Component 3: All 5 Heading 2 paragraphs have a bottom border (0.3 pts — 0.06 per heading)
Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_creative_042'

# Expected date headings (exact text)
EXPECTED_DATE_HEADINGS = [
    'January 15, 2026',
    'February 3, 2026',
    'February 18, 2026',
    'March 1, 2026',
    'March 4, 2026',
]

EXPECTED_TITLE = 'My Journal \u2014 2026'


def has_bottom_border(para):
    """Check if a paragraph has a bottom border set in its paragraph properties."""
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        return False
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        return False
    bottom = pBdr.find(qn('w:bottom'))
    if bottom is None:
        return False
    # Check the border val is not 'none' or 'nil'
    val = bottom.attrib.get(qn('w:val'), '')
    return val not in ('none', 'nil', '')


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

    # Build a lookup of paragraph index -> paragraph for quick access
    paragraphs = doc.paragraphs

    # Component 1: Document title has Heading 1 style (0.2 points)
    # The title 'My Journal — 2026' must be formatted as Heading 1
    try:
        title_para = None
        for para in paragraphs:
            if EXPECTED_TITLE in para.text:
                title_para = para
                break

        if title_para is None:
            print(f"FAIL: Component 1 — Could not find title paragraph '{EXPECTED_TITLE}'")
        elif title_para.style.name == 'Heading 1':
            print(f"PASS: Component 1 — Title '{EXPECTED_TITLE}' has Heading 1 style (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Title style is '{title_para.style.name}', expected 'Heading 1'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 date lines have Heading 2 style (0.1 each = 0.5 total)
    # Each date heading must be individually formatted as Heading 2
    try:
        para_by_text = {}
        for para in paragraphs:
            for date_str in EXPECTED_DATE_HEADINGS:
                if date_str in para.text:
                    para_by_text[date_str] = para

        for date_str in EXPECTED_DATE_HEADINGS:
            if date_str not in para_by_text:
                print(f"FAIL: Component 2 — Could not find date paragraph '{date_str}'")
                continue
            para = para_by_text[date_str]
            if para.style.name == 'Heading 2':
                print(f"PASS: Component 2 — '{date_str}' has Heading 2 style (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — '{date_str}' style is '{para.style.name}', expected 'Heading 2'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 Heading 2 paragraphs have a bottom border (0.06 each = 0.3 total)
    # The bottom border should be a thin single line below each date heading
    try:
        for date_str in EXPECTED_DATE_HEADINGS:
            if date_str not in para_by_text:
                print(f"FAIL: Component 3 — Could not find paragraph for '{date_str}'")
                continue
            para = para_by_text[date_str]
            if has_bottom_border(para):
                print(f"PASS: Component 3 — '{date_str}' has bottom border (0.06 pts)")
                total_score += 0.06
            else:
                print(f"FAIL: Component 3 — '{date_str}' missing bottom border in paragraph properties")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/journal_2026.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
