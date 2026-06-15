"""
Reward Script: Insert Appendix_A section with 2-column layout and separator line
Task ID: writer_fs_066
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20) — Appendix heading exists after References
  Component 2 (0.20) — A section break creates a separate section for the appendix
  Component 3 (0.30) — The appendix section has 2 columns
  Component 4 (0.15) — The appendix section has separator line enabled
  Component 5 (0.15) — The main body (pre-appendix) remains single column
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_066'


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

    # =========================================================
    # Component 1: Appendix heading exists after References (0.20 pts)
    # =========================================================
    try:
        paragraphs = doc.paragraphs
        references_idx = None
        appendix_idx = None
        appendix_text = None

        for i, p in enumerate(paragraphs):
            if p.text.strip().lower().startswith('references'):
                references_idx = i
            if 'appendix' in p.text.strip().lower():
                appendix_idx = i
                appendix_text = p.text.strip()

        if appendix_idx is not None and references_idx is not None and appendix_idx > references_idx:
            print(f"PASS: Component 1 — Appendix heading found at P{appendix_idx} after References at P{references_idx}: '{appendix_text}' (0.20 pts)")
            total_score += 0.20
        elif appendix_idx is not None:
            print(f"FAIL: Component 1 — Appendix found at P{appendix_idx} but not after References (ref_idx={references_idx})")
        else:
            print(f"FAIL: Component 1 — No paragraph containing 'appendix' found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================
    # Component 2: Document has >1 section (section break exists) (0.20 pts)
    # =========================================================
    try:
        num_sections = len(doc.sections)
        if num_sections >= 2:
            print(f"PASS: Component 2 — Document has {num_sections} sections (section break present) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Document has only {num_sections} section(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================
    # Component 3: The appendix section has 2 columns (0.30 pts)
    # =========================================================
    try:
        # Find a section with 2 columns (the appendix section)
        two_col_section_idx = next(
            (i for i, section in enumerate(doc.sections)
             if section._sectPr.find(qn('w:cols')) is not None
             and section._sectPr.find(qn('w:cols')).get(qn('w:num'), '1') == '2'),
            -1
        )

        if two_col_section_idx >= 0:
            print(f"PASS: Component 3 — Section {two_col_section_idx} has 2 columns (0.30 pts)")
            total_score += 0.30
        else:
            for i, section in enumerate(doc.sections):
                cols_el = section._sectPr.find(qn('w:cols'))
                if cols_el is not None:
                    num_cols = cols_el.get(qn('w:num'), '1')
                    print(f"  Section {i}: cols num={num_cols}")
                else:
                    print(f"  Section {i}: no cols element")
            print(f"FAIL: Component 3 — No section with 2 columns found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: The appendix (2-col) section has separator line (0.15 pts)
    # =========================================================
    try:
        # Find a section with 2 columns AND separator line
        sep_section_idx = next(
            (i for i, section in enumerate(doc.sections)
             if section._sectPr.find(qn('w:cols')) is not None
             and section._sectPr.find(qn('w:cols')).get(qn('w:num'), '1') == '2'
             and section._sectPr.find(qn('w:cols')).get(qn('w:sep'), '0') == '1'),
            -1
        )

        if sep_section_idx >= 0:
            print(f"PASS: Component 4 — Section {sep_section_idx} has 2 columns with separator line (sep=1) (0.15 pts)")
            total_score += 0.15
        else:
            # Check if there's a 2-col section without separator
            for i, section in enumerate(doc.sections):
                cols_el = section._sectPr.find(qn('w:cols'))
                if cols_el is not None:
                    num_cols = cols_el.get(qn('w:num'), '1')
                    sep = cols_el.get(qn('w:sep'), '0')
                    if str(num_cols) == '2':
                        print(f"FAIL: Component 4 — Section {i} has 2 columns but sep={sep}, expected 1")
            if not any(
                section._sectPr.find(qn('w:cols')) is not None and
                section._sectPr.find(qn('w:cols')).get(qn('w:num'), '1') == '2'
                for section in doc.sections
            ):
                print(f"FAIL: Component 4 — No 2-column section found to check separator")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: Main body stays single column WHILE appendix has 2 cols (0.15 pts)
    # This is a compound check: requires both a 2-col appendix section AND
    # the pre-appendix section(s) remaining single column.
    # It FAILS on initial_env because there is no 2-col section at all.
    # =========================================================
    try:
        has_2col_section = any(
            section._sectPr.find(qn('w:cols')) is not None and
            section._sectPr.find(qn('w:cols')).get(qn('w:num'), '1') == '2'
            for section in doc.sections
        )

        if not has_2col_section:
            print(f"FAIL: Component 5 — No 2-column appendix section exists, so compound check fails")
        else:
            # Check the first section and any inline section breaks are single column
            first_section = doc.sections[0]
            cols_el = first_section._sectPr.find(qn('w:cols'))
            first_num = '1'
            if cols_el is not None:
                first_num = cols_el.get(qn('w:num'), '1')

            body = doc.element.body
            # Collect any inline section breaks with non-single-column settings
            multi_col_inline = [
                elem for elem in body
                if (elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag) == 'p'
                and elem.find(qn('w:pPr')) is not None
                and elem.find(qn('w:pPr')).find(qn('w:sectPr')) is not None
                and elem.find(qn('w:pPr')).find(qn('w:sectPr')).find(qn('w:cols')) is not None
                and elem.find(qn('w:pPr')).find(qn('w:sectPr')).find(qn('w:cols')).get(qn('w:num'), '1') != '1'
            ]

            if str(first_num) == '1' and len(multi_col_inline) == 0:
                print(f"PASS: Component 5 — Main body remains single column while appendix has 2 cols (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — First section cols num={first_num}, multi-col inline breaks={len(multi_col_inline)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
