"""
Reward Script: Insert a section named 'Appendix A' around the last three paragraphs
Task ID: writer_struct_011
Domain: libreoffice_writer
Scoring:
  Component 1: A section named 'Appendix A' exists (implemented as w:sdt with alias 'Appendix A') — 0.5 pts
  Component 2: The section contains exactly 3 paragraphs — 0.3 pts
  Component 3: The section's first paragraph starts with 'Table A-1' — 0.2 pts
  Total: 1.0
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'annual_report'
FILE_PATH = f'{WORKDIR}/{TASK_ID}.docx'

# Namespace constants
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def find_section_sdt(body):
    """
    Find a w:sdt element in the document body that has:
      - w:sdtPr/w:tag with w:val='ooow:section'  (LibreOffice section marker)
      - w:sdtPr/w:alias with a name
    Returns the sdt element and its alias value, or (None, None).
    """
    for child in body:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local == 'sdt':
            sdt_pr = child.find(f'{{{W_NS}}}sdtPr')
            if sdt_pr is not None:
                tag_el = sdt_pr.find(f'{{{W_NS}}}tag')
                alias_el = sdt_pr.find(f'{{{W_NS}}}alias')
                tag_val = tag_el.get(f'{{{W_NS}}}val', '') if tag_el is not None else ''
                alias_val = alias_el.get(f'{{{W_NS}}}val', '') if alias_el is not None else ''
                if tag_val == 'ooow:section':
                    return child, alias_val
    return None, None


def get_sdt_paragraphs(sdt_el):
    """Return list of text strings from paragraphs inside the w:sdtContent of a w:sdt."""
    sdt_content = sdt_el.find(f'{{{W_NS}}}sdtContent')
    if sdt_content is None:
        return []
    paragraphs = []
    for child in sdt_content:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local == 'p':
            # Gather all text runs
            texts = []
            for r in child.iter(f'{{{W_NS}}}t'):
                texts.append(r.text or '')
            paragraphs.append(''.join(texts))
    return paragraphs


def verify_task(file_path):
    """
    Verify that 'annual_report.docx' has a section named 'Appendix A'
    enclosing the last three paragraphs of the document.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Component 1: A section named 'Appendix A' exists as a w:sdt element (0.5 points)
    # LibreOffice Writer stores named sections as w:sdt with w:tag val='ooow:section'
    # and w:alias val=<section_name>
    try:
        sdt_el, alias_val = find_section_sdt(body)
        if sdt_el is not None and alias_val.strip().lower() == 'appendix a':
            print(f"PASS: Component 1 — Section named 'Appendix A' found (alias='{alias_val}') (0.5 pts)")
            total_score += 0.5
        else:
            if sdt_el is None:
                print("FAIL: Component 1 — No w:sdt section element found in document body")
            else:
                print(f"FAIL: Component 1 — Section found but alias is '{alias_val}', expected 'Appendix A'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The section contains exactly 3 paragraphs (0.3 points)
    # The task specifies the last three paragraphs should be enclosed
    try:
        if sdt_el is not None:
            paras = get_sdt_paragraphs(sdt_el)
            if len(paras) == 3:
                print(f"PASS: Component 2 — Section contains exactly 3 paragraphs (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Section contains {len(paras)} paragraphs, expected 3")
        else:
            print("FAIL: Component 2 — Cannot check paragraph count: no section found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The section's first paragraph starts with 'Table A-1' (0.2 points)
    # The task specifies the last three paragraphs start from 'Table A-1 shows the raw revenue data...'
    try:
        if sdt_el is not None:
            paras = get_sdt_paragraphs(sdt_el)
            if paras and paras[0].strip().startswith('Table A-1'):
                print(f"PASS: Component 3 — Section's first paragraph starts with 'Table A-1' (0.2 pts)")
                total_score += 0.2
            else:
                first_text = paras[0][:60] if paras else '(empty)'
                print(f"FAIL: Component 3 — Section's first paragraph starts with: '{first_text}', expected 'Table A-1'")
        else:
            print("FAIL: Component 3 — Cannot check first paragraph: no section found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
