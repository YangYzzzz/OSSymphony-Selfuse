"""
Reward Script: Insert page breaks with landscape page style for appendix
Task ID: writer_fs_027
Domain: libreoffice_writer

Scoring Rubric:
  Component 1 (0.30): Document has exactly 3 sections (initial has 1)
  Component 2 (0.30): The section containing 'Appendix A: Data Tables' is landscape
  Component 3 (0.20): First section (before appendix) and last section (after appendix) are portrait
  Component 4 (0.20): Section breaks are correctly placed — one before 'Appendix A' and one before 'References'
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_027'


def find_paragraph_section_index(doc):
    """
    Map key paragraphs to their section index.
    Section breaks in docx are stored as sectPr elements inside paragraph properties.
    Paragraphs before the first sectPr belong to section 0, etc.
    """
    section_idx = 0
    para_section_map = {}
    appendix_para_idx = None
    references_para_idx = None

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text.startswith('Appendix A'):
            appendix_para_idx = i
            para_section_map['appendix'] = section_idx
        if text == 'References':
            references_para_idx = i
            para_section_map['references'] = section_idx

        # Check if this paragraph has a section break after it
        pPr = p._element.find(qn('w:pPr'))
        if pPr is not None:
            sectPr = pPr.find(qn('w:sectPr'))
            if sectPr is not None:
                section_idx += 1

    para_section_map['total_sections'] = section_idx + 1  # +1 for the final body section
    para_section_map['appendix_idx'] = appendix_para_idx
    para_section_map['references_idx'] = references_para_idx
    return para_section_map


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

    num_sections = len(doc.sections)
    para_map = find_paragraph_section_index(doc)

    # Component 1: Document has exactly 3 sections (0.30 points)
    # Initial doc has 1 section; golden has 3 (portrait, landscape, portrait)
    try:
        if num_sections == 3:
            print(f"PASS: Component 1 — Document has 3 sections (0.30 pts)")
            total_score += 0.30
        elif num_sections >= 2:
            # Partial: at least some section breaks were added
            print(f"PARTIAL: Component 1 — Document has {num_sections} sections, expected 3 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Document has {num_sections} section(s), expected 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The section containing 'Appendix A: Data Tables' is landscape (0.30 points)
    # This is the core task requirement: appendix pages should be landscape
    try:
        appendix_section_idx = para_map.get('appendix')
        if appendix_section_idx is not None and appendix_section_idx < num_sections:
            appendix_section = doc.sections[appendix_section_idx]
            is_landscape = appendix_section.orientation == WD_ORIENT.LANDSCAPE
            # Also check width > height as a secondary confirmation
            width_gt_height = appendix_section.page_width > appendix_section.page_height
            if is_landscape and width_gt_height:
                print(f"PASS: Component 2 — Appendix section (idx {appendix_section_idx}) is landscape "
                      f"({appendix_section.page_width}x{appendix_section.page_height}) (0.30 pts)")
                total_score += 0.30
            elif is_landscape or width_gt_height:
                print(f"PARTIAL: Component 2 — Appendix section orientation={appendix_section.orientation}, "
                      f"dims={appendix_section.page_width}x{appendix_section.page_height} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Appendix section is not landscape. "
                      f"orient={appendix_section.orientation}, "
                      f"dims={appendix_section.page_width}x{appendix_section.page_height}")
        else:
            print(f"FAIL: Component 2 — Could not find Appendix section. "
                  f"appendix_section_idx={appendix_section_idx}, num_sections={num_sections}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: First and last sections are portrait (0.20 points)
    # The task says to return to portrait 'Default Page Style' after the appendix
    try:
        if num_sections >= 3:
            first_section = doc.sections[0]
            last_section = doc.sections[-1]
            first_portrait = (first_section.orientation == WD_ORIENT.PORTRAIT or
                              first_section.orientation is None)
            first_dims_ok = first_section.page_height > first_section.page_width
            last_portrait = (last_section.orientation == WD_ORIENT.PORTRAIT or
                             last_section.orientation is None)
            last_dims_ok = last_section.page_height > last_section.page_width

            score_3 = 0.0
            if first_portrait and first_dims_ok:
                score_3 += 0.10
                print(f"PASS: Component 3a — First section is portrait")
            else:
                print(f"FAIL: Component 3a — First section not portrait: "
                      f"orient={first_section.orientation}, "
                      f"dims={first_section.page_width}x{first_section.page_height}")

            if last_portrait and last_dims_ok:
                score_3 += 0.10
                print(f"PASS: Component 3b — Last section is portrait")
            else:
                print(f"FAIL: Component 3b — Last section not portrait: "
                      f"orient={last_section.orientation}, "
                      f"dims={last_section.page_width}x{last_section.page_height}")

            if score_3 > 0:
                print(f"Component 3 total: {score_3} pts")
                total_score += score_3
        else:
            print(f"FAIL: Component 3 — Need at least 3 sections to check first/last portrait, "
                  f"found {num_sections}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Section breaks correctly placed (0.20 points)
    # Break before 'Appendix A' heading (so appendix starts a new landscape section)
    # Break before 'References' heading (so references starts a new portrait section)
    try:
        if num_sections >= 3:
            # 'Appendix A' should be in a different section than the content before it
            # 'References' should be in a different section than the appendix
            appendix_sec = para_map.get('appendix')
            references_sec = para_map.get('references')

            score_4 = 0.0
            if appendix_sec is not None and appendix_sec >= 1:
                # Appendix is in section 1 or later (not section 0)
                print(f"PASS: Component 4a — Appendix starts in section {appendix_sec} (not section 0)")
                score_4 += 0.10
            else:
                print(f"FAIL: Component 4a — Appendix is in section {appendix_sec}, expected >= 1")

            if references_sec is not None and appendix_sec is not None and references_sec > appendix_sec:
                # References is in a later section than appendix
                print(f"PASS: Component 4b — References in section {references_sec}, "
                      f"after appendix section {appendix_sec}")
                score_4 += 0.10
            else:
                print(f"FAIL: Component 4b — References section={references_sec}, "
                      f"appendix section={appendix_sec}")

            if score_4 > 0:
                print(f"Component 4 total: {score_4} pts")
                total_score += score_4
        else:
            print(f"FAIL: Component 4 — Need at least 3 sections, found {num_sections}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
