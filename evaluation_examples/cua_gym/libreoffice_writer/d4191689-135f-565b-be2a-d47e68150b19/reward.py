"""
Reward Script: Create 'Chapter Start' page style with decorative top border, 5.0cm top margin,
               applied to Chapter 3 via section break.
Task ID: writer_rd_019
Domain: libreoffice_writer
Scoring:
  Component 1: Multiple sections exist (section breaks around Chapter 3) — 0.25 pts
  Component 2: Chapter 3 section has top margin ~5.0 cm — 0.30 pts
  Component 3: Chapter 3 section has decorative double top border — 0.25 pts
  Component 4: Section break is placed correctly before Chapter 3 heading — 0.20 pts
"""

import os
from docx import Document
from docx.shared import Pt, Emu
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_019'


def persist_app_state(domain):
    """Best-effort save for unsaved GUI edits."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_chapter3_section_index(doc):
    """
    Find which section contains the Chapter 3 heading.
    In OOXML, section breaks in paragraph pPr define the END of a section.
    The last section is defined by the body-level sectPr.
    We need to map paragraphs to sections.
    """
    body = doc.element.body
    all_paras = body.findall(qn('w:p'))

    # Find section break positions (paragraph indices that END a section)
    section_break_indices = []
    for idx, p_elem in enumerate(all_paras):
        pPr = p_elem.find(qn('w:pPr'))
        if pPr is not None:
            sectPr = pPr.find(qn('w:sectPr'))
            if sectPr is not None:
                section_break_indices.append(idx)

    # Find Chapter 3 heading paragraph index
    ch3_idx = None
    for idx, p_elem in enumerate(all_paras):
        text = ''
        for t in p_elem.iter(qn('w:t')):
            text += t.text if t.text else ''
        if 'Chapter 3' in text:
            ch3_idx = idx
            break

    return section_break_indices, ch3_idx


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

    sections = list(doc.sections)
    num_sections = len(sections)
    section_break_indices, ch3_idx = find_chapter3_section_index(doc)

    print(f"INFO: Document has {num_sections} sections, {len(section_break_indices)} section breaks in paragraphs")
    print(f"INFO: Section break para indices: {section_break_indices}")
    print(f"INFO: Chapter 3 heading at para index: {ch3_idx}")

    # Component 1: Multiple sections exist — section breaks around Chapter 3 (0.25 points)
    # Initial has 1 section; golden has 3. We need at least 2 section breaks.
    try:
        if num_sections >= 3 and len(section_break_indices) >= 2:
            print(f"PASS: Component 1 — Document has {num_sections} sections with {len(section_break_indices)} breaks (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected >= 3 sections with >= 2 breaks, found {num_sections} sections, {len(section_break_indices)} breaks")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chapter 3 section has top margin ~5.0 cm (0.30 points)
    # In golden, the section containing Chapter 3 has top_margin = 2835 twips = 5.00cm
    # 5.0 cm = 1800000 EMU (360000 EMU per cm)
    try:
        # The Chapter 3 section is the one AFTER the first section break
        # In OOXML: sectPr in para N's pPr defines the section for paras 0..N
        # So the section for Chapter 3 is defined by the SECOND sectPr (or body sectPr)
        ch3_section_found = False
        if ch3_idx is not None and len(section_break_indices) >= 2:
            # Chapter 3 is between section_break_indices[0] and section_break_indices[1]
            # The section properties for Chapter 3's section are in section_break_indices[1]'s sectPr
            body = doc.element.body
            all_paras = body.findall(qn('w:p'))
            sb_para = all_paras[section_break_indices[1]]
            pPr = sb_para.find(qn('w:pPr'))
            sectPr = pPr.find(qn('w:sectPr'))
            pgMar = sectPr.find(qn('w:pgMar'))
            if pgMar is not None:
                top_twips = int(pgMar.get(qn('w:top'), '0'))
                top_cm = top_twips / 567.0
                print(f"INFO: Chapter 3 section top margin = {top_cm:.2f} cm ({top_twips} twips)")
                if abs(top_cm - 5.0) < 0.2:
                    print(f"PASS: Component 2 — Chapter 3 section top margin is {top_cm:.2f} cm (~5.0 cm) (0.30 pts)")
                    total_score += 0.30
                    ch3_section_found = True
                else:
                    print(f"FAIL: Component 2 — Expected ~5.0 cm top margin, found {top_cm:.2f} cm")

        if not ch3_section_found and ch3_idx is not None:
            # Fallback: check all sections for one with ~5.0cm top margin
            for i, s in enumerate(sections):
                if s.top_margin:
                    tm_cm = s.top_margin / 360000
                    if abs(tm_cm - 5.0) < 0.2:
                        print(f"PASS: Component 2 — Section {i} has top margin {tm_cm:.2f} cm (~5.0 cm) (0.30 pts)")
                        total_score += 0.30
                        ch3_section_found = True
                        break
            if not ch3_section_found:
                margins = [s.top_margin / 360000 if s.top_margin else 0 for s in sections]
                print(f"FAIL: Component 2 — No section with ~5.0 cm top margin found. Margins: {margins}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chapter 3 section has decorative double top border (0.25 points)
    # Golden has pgBorders > top with val='double', sz='12'
    try:
        border_found = False
        # Check sectPr elements in paragraph pPr for pgBorders
        body = doc.element.body
        all_paras = body.findall(qn('w:p'))
        for idx, p_elem in enumerate(all_paras):
            pPr = p_elem.find(qn('w:pPr'))
            if pPr is not None:
                sectPr = pPr.find(qn('w:sectPr'))
                if sectPr is not None:
                    pgBorders = sectPr.find(qn('w:pgBorders'))
                    if pgBorders is not None:
                        top_border = pgBorders.find(qn('w:top'))
                        if top_border is not None:
                            val = top_border.get(qn('w:val'))
                            sz = top_border.get(qn('w:sz'))
                            print(f"INFO: Found top border in sectPr at para {idx}: val={val}, sz={sz}")
                            if val == 'double':
                                print(f"PASS: Component 3 — Double top border found (val={val}, sz={sz}) (0.25 pts)")
                                total_score += 0.25
                                border_found = True
                                break

        # Also check body-level sectPr (last section)
        if not border_found:
            for s in sections:
                pgBorders = s._sectPr.find(qn('w:pgBorders'))
                if pgBorders is not None:
                    top_border = pgBorders.find(qn('w:top'))
                    if top_border is not None:
                        val = top_border.get(qn('w:val'))
                        sz = top_border.get(qn('w:sz'))
                        if val == 'double':
                            print(f"PASS: Component 3 — Double top border in section (val={val}, sz={sz}) (0.25 pts)")
                            total_score += 0.25
                            border_found = True
                            break

        if not border_found:
            print("FAIL: Component 3 — No double top border found in any section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Section break is correctly placed before Chapter 3 heading (0.20 points)
    # In golden, the section break (in para pPr) is in the paragraph BEFORE Chapter 3,
    # and the next paragraph is Chapter 3. This means Chapter 3 starts on a new page
    # with the special section formatting.
    try:
        if ch3_idx is not None and len(section_break_indices) >= 1:
            # The first section break should be right before Chapter 3
            first_break = section_break_indices[0]
            # Chapter 3 should be at first_break + 1
            if first_break == ch3_idx - 1:
                print(f"PASS: Component 4 — Section break at para {first_break}, Chapter 3 at para {ch3_idx} (0.20 pts)")
                total_score += 0.20
            else:
                # Accept if any section break is immediately before Chapter 3
                found_break_before_ch3 = any(sb == ch3_idx - 1 for sb in section_break_indices)
                if found_break_before_ch3:
                    print(f"PASS: Component 4 — Section break found immediately before Chapter 3 (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — No section break immediately before Chapter 3 (ch3={ch3_idx}, breaks={section_break_indices})")
        else:
            print(f"FAIL: Component 4 — Chapter 3 not found or no section breaks")
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
