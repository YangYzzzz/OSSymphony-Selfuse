"""
Reward Script: Two-column layout with full-width heading
Task ID: writer_fs_050
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Document has multiple sections with continuous section break
  Component 2 (0.25): Title 'Annual Report 2024' is in the first single-column section
  Component 3 (0.30): Second section has 2-column layout
  Component 4 (0.20): Body text paragraphs present in the two-column section
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_050'


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    body = doc.element.body
    num_sections = len(doc.sections)

    # Component 1: Document has multiple sections with a continuous section break (0.25 pts)
    # In the initial file there is only 1 section. The golden file has 2+ sections
    # with a continuous break separating title from body.
    try:
        has_continuous_break = False

        if num_sections >= 2:
            # Check that at least one section (after the first) uses continuous break
            for i in range(1, num_sections):
                sec = doc.sections[i]
                type_el = sec._sectPr.find(qn('w:type'))
                if type_el is not None and type_el.get(qn('w:val')) == 'continuous':
                    has_continuous_break = True
                    break

        if num_sections >= 2 and has_continuous_break:
            print(f"PASS: Component 1 — {num_sections} sections with continuous break (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — sections={num_sections}, continuous_break={has_continuous_break}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title 'Annual Report 2024' is in a SEPARATE single-column section
    # before a multi-column section (0.25 pts)
    # This component ONLY passes when there is a section break separating the title
    # from the body. In the initial file (single section), this MUST fail.
    try:
        # Find paragraphs in the first section (before the first inline sectPr)
        first_section_paras = []
        found_inline_sectPr = False
        for child in body:
            if child.tag == qn('w:p'):
                pPr = child.find(qn('w:pPr'))
                has_sect = pPr is not None and pPr.find(qn('w:sectPr')) is not None
                first_section_paras.append(child)
                if has_sect:
                    found_inline_sectPr = True
                    break

        # Must have an inline section break to separate title from body
        if not found_inline_sectPr:
            print(f"FAIL: Component 2 — No inline section break found; title not in separate section")
        else:
            # Extract text from first section paragraphs
            first_section_texts = []
            for p_el in first_section_paras:
                texts = []
                for r in p_el.findall('.//' + qn('w:t')):
                    if r.text:
                        texts.append(r.text)
                first_section_texts.append(''.join(texts))

            title_in_first_section = any('Annual Report 2024' in t for t in first_section_texts)

            # Check that the first section (defined by the inline sectPr) is single-column
            first_sect_cols_num = 1
            last_p = first_section_paras[-1]
            pPr = last_p.find(qn('w:pPr'))
            if pPr is not None:
                sectPr = pPr.find(qn('w:sectPr'))
                if sectPr is not None:
                    cols_el = sectPr.find(qn('w:cols'))
                    if cols_el is not None:
                        num_val = cols_el.get(qn('w:num'))
                        if num_val is not None:
                            first_sect_cols_num = int(num_val)

            first_section_single_col = (first_sect_cols_num <= 1)

            if title_in_first_section and first_section_single_col:
                print(f"PASS: Component 2 — Title 'Annual Report 2024' in separate single-column section (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — title_in_first={title_in_first_section}, single_col={first_section_single_col}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A section (after the title) has 2-column layout (0.30 pts)
    # This is the core task requirement — the body should be in 2 columns.
    try:
        found_two_col_section = False
        two_col_section_idx = -1
        for i in range(num_sections):
            sec = doc.sections[i]
            cols_el = sec._sectPr.find(qn('w:cols'))
            if cols_el is not None:
                num_val = cols_el.get(qn('w:num'))
                if num_val is not None and int(num_val) == 2:
                    found_two_col_section = True
                    two_col_section_idx = i
                    break

        if found_two_col_section:
            print(f"PASS: Component 3 — Section {two_col_section_idx} has 2-column layout (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — No section with 2 columns found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Body text paragraphs are present in the two-column section (0.20 pts)
    # After the section break, there should be actual body text paragraphs.
    try:
        # Collect paragraphs AFTER the first inline sectPr
        found_break = False
        post_break_texts = []
        for child in body:
            if child.tag == qn('w:p'):
                if found_break:
                    texts = []
                    for r in child.findall('.//' + qn('w:t')):
                        if r.text:
                            texts.append(r.text)
                    full_text = ''.join(texts).strip()
                    if full_text:
                        post_break_texts.append(full_text)
                else:
                    pPr = child.find(qn('w:pPr'))
                    if pPr is not None and pPr.find(qn('w:sectPr')) is not None:
                        found_break = True

        # Should have at least 3 body paragraphs in the two-column section
        if len(post_break_texts) >= 3:
            print(f"PASS: Component 4 — {len(post_break_texts)} body paragraphs in two-column section (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Only {len(post_break_texts)} body paragraphs after section break (need >= 3)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
