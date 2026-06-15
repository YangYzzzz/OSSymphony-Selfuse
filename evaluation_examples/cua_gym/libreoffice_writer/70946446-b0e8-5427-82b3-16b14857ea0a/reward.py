"""
Reward Script: Create two sections 'Part A' (1-column) and 'Part B' (2-column) in newsletter_draft.docx
Task ID: writer_struct_055
Domain: libreoffice_writer
Scoring:
  Component 1: 'Part A' section (sdt) exists with correct alias        — 0.30 pts
  Component 2: 'Part A' section has 1-column layout (sectPr cols.num=1) — 0.20 pts
  Component 3: 'Part B' section (sdt) exists with correct alias        — 0.30 pts
  Component 4: 'Part B' section has 2-column layout (sectPr cols.num=2) — 0.20 pts
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_055'
NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def find_sdt_sections(body):
    """
    Find all sdt (structured document tag) elements in the body that represent
    named sections. Returns a dict of {alias_name: sdt_element}.
    """
    sections = {}
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'sdt':
            sdtPr = child.find('{%s}sdtPr' % NS)
            if sdtPr is not None:
                alias_el = sdtPr.find('{%s}alias' % NS)
                if alias_el is not None:
                    alias_val = alias_el.get('{%s}val' % NS)
                    if alias_val:
                        sections[alias_val] = child
    return sections


def get_sdt_cols_num(sdt_elem):
    """
    Get the number of columns specified in a sectPr inside an sdt element.
    Returns None if no sectPr or no cols element found.
    """
    # The sectPr is in the last paragraph of sdtContent
    sectPr_list = sdt_elem.findall('.//{%s}sectPr' % NS)
    if not sectPr_list:
        return None
    # Use the last one (the section-ending paragraph)
    for sectPr in sectPr_list:
        cols = sectPr.find('{%s}cols' % NS)
        if cols is not None:
            num_val = cols.get('{%s}num' % NS)
            if num_val is not None:
                try:
                    return int(num_val)
                except ValueError:
                    return None
    return None


def get_sdt_content_texts(sdt_elem):
    """
    Extract all non-empty paragraph texts from an sdt element's content.
    """
    texts = []
    sdtContent = sdt_elem.find('{%s}sdtContent' % NS)
    if sdtContent is None:
        return texts
    for cc in sdtContent:
        cc_tag = cc.tag.split('}')[-1]
        if cc_tag == 'p':
            text = ''.join(t.text or '' for t in cc.findall('.//{%s}t' % NS))
            if text.strip():
                texts.append(text.strip())
    return texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Create 'Part A' (1-column) and 'Part B' (2-column) sections in newsletter_draft.docx.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Precondition: document body must be accessible
    if body is None:
        print("CRITICAL: Document body is None — cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    # Find all named sdt sections in the document
    sdt_sections = find_sdt_sections(body)
    print("Named sdt sections found: %s" % list(sdt_sections.keys()))

    # Component 1: 'Part A' section exists as an sdt with alias 'Part A' (0.30 points)
    # This FAILS on initial_env (no sdt elements) and PASSES on golden_env
    try:
        part_a_sdt = sdt_sections.get('Part A')
        if part_a_sdt is not None:
            # Also verify it contains lead story paragraphs (not empty)
            part_a_texts = get_sdt_content_texts(part_a_sdt)
            if len(part_a_texts) >= 5:
                print("PASS: Component 1 — 'Part A' section exists with %d content paragraphs (0.30 pts)"
                      % len(part_a_texts))
                total_score += 0.30
            else:
                print("FAIL: Component 1 — 'Part A' section found but has only %d content paragraphs "
                      "(expected >= 5)" % len(part_a_texts))
        else:
            print("FAIL: Component 1 — No sdt section with alias 'Part A' found. "
                  "Sections found: %s" % list(sdt_sections.keys()))
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: 'Part A' section uses 1-column layout (0.20 points)
    # This FAILS on initial_env (no sectPr in Part A) and PASSES on golden_env (cols.num=1)
    try:
        part_a_sdt = sdt_sections.get('Part A')
        if part_a_sdt is not None:
            cols_num = get_sdt_cols_num(part_a_sdt)
            if cols_num == 1:
                print("PASS: Component 2 — 'Part A' has 1-column layout (cols.num=1) (0.20 pts)")
                total_score += 0.20
            else:
                print("FAIL: Component 2 — 'Part A' expected cols.num=1, found: %s" % cols_num)
        else:
            print("FAIL: Component 2 — Cannot check columns: 'Part A' section not found")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: 'Part B' section exists as an sdt with alias 'Part B' (0.30 points)
    # This FAILS on initial_env (no sdt elements) and PASSES on golden_env
    try:
        part_b_sdt = sdt_sections.get('Part B')
        if part_b_sdt is not None:
            # Also verify it contains brief item paragraphs (not empty)
            part_b_texts = get_sdt_content_texts(part_b_sdt)
            if len(part_b_texts) >= 5:
                print("PASS: Component 3 — 'Part B' section exists with %d content paragraphs (0.30 pts)"
                      % len(part_b_texts))
                total_score += 0.30
            else:
                print("FAIL: Component 3 — 'Part B' section found but has only %d content paragraphs "
                      "(expected >= 5)" % len(part_b_texts))
        else:
            print("FAIL: Component 3 — No sdt section with alias 'Part B' found. "
                  "Sections found: %s" % list(sdt_sections.keys()))
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # Component 4: 'Part B' section uses 2-column layout (0.20 points)
    # This FAILS on initial_env (no sectPr in Part B) and PASSES on golden_env (cols.num=2)
    try:
        part_b_sdt = sdt_sections.get('Part B')
        if part_b_sdt is not None:
            cols_num = get_sdt_cols_num(part_b_sdt)
            if cols_num == 2:
                print("PASS: Component 4 — 'Part B' has 2-column layout (cols.num=2) (0.20 pts)")
                total_score += 0.20
            else:
                print("FAIL: Component 4 — 'Part B' expected cols.num=2, found: %s" % cols_num)
        else:
            print("FAIL: Component 4 — Cannot check columns: 'Part B' section not found")
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Default: test against canonical artifact path
file_path = '%s/Desktop/newsletter_draft.docx' % WORKDIR
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
