"""
Reward Script: Create 'Appendix' page style with page numbering restart at 1 using A-1, A-2, A-3 format
Task ID: writer_fs_081
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Document has 2+ sections (section break before appendix)
  Component 2 (0.25): Second section has page numbering restarting at 1
  Component 3 (0.25): Second section footer contains 'A-' prefix with PAGE field
  Component 4 (0.20): Second section footer is not linked to previous (independent footer)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_081'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sections = doc.sections

    # Component 1: Document has at least 2 sections (0.30 points)
    # The initial doc has only 1 section. The task requires a section break before the appendix.
    try:
        num_sections = len(sections)
        if num_sections >= 2:
            print(f"PASS: Component 1 - Document has {num_sections} sections (>= 2) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Document has {num_sections} section(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Second (or last non-first) section has page numbering restart at 1 (0.25 points)
    # Check for pgNumType with start="1" in the appendix section's sectPr
    try:
        if len(sections) >= 2:
            # The appendix section is the last section
            appendix_sec = sections[-1]
            # Access the section's XML element via the _sectPr property
            sect_el = None
            # Try to get the section element from the body
            body = doc.element.body
            all_sectPr = body.findall('.//w:sectPr', NS)
            if len(all_sectPr) >= 2:
                sect_el = all_sectPr[-1]  # Last sectPr = final section

            found_restart = False
            if sect_el is not None:
                pgnum_els = sect_el.findall('w:pgNumType', NS)
                for pg in pgnum_els:
                    start_val = pg.get(f'{{{WNS}}}start')
                    if start_val == '1':
                        found_restart = True
                        break

            if found_restart:
                print(f"PASS: Component 2 - Appendix section has pgNumType start=1 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Appendix section does not have page numbering restart at 1")
        else:
            print(f"FAIL: Component 2 - Cannot check page numbering without 2+ sections")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Appendix section footer contains 'A-' prefix and PAGE field code (0.25 points)
    # The footer should have a run with 'A-' text followed by a PAGE field
    try:
        if len(sections) >= 2:
            appendix_sec = sections[-1]
            footer = appendix_sec.footer

            has_a_prefix = False
            has_page_field = False

            for para in footer.paragraphs:
                # Check for 'A-' text in any run
                for run in para.runs:
                    if 'A-' in run.text:
                        has_a_prefix = True

                # Check for PAGE field code in the paragraph XML
                instr_texts = para._element.findall('.//w:instrText', NS)
                for instr in instr_texts:
                    if instr.text and 'PAGE' in instr.text.upper():
                        has_page_field = True

            if has_a_prefix and has_page_field:
                print(f"PASS: Component 3 - Footer has 'A-' prefix and PAGE field (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 - Footer: A-prefix={has_a_prefix}, PAGE field={has_page_field}")
        else:
            print(f"FAIL: Component 3 - Cannot check footer without 2+ sections")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Appendix section footer is NOT linked to previous (0.20 points)
    # This ensures the appendix has its own independent footer with the A- numbering
    try:
        if len(sections) >= 2:
            appendix_sec = sections[-1]
            footer = appendix_sec.footer
            is_linked = footer.is_linked_to_previous

            if not is_linked:
                print(f"PASS: Component 4 - Appendix footer is not linked to previous (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - Appendix footer is linked to previous (should be independent)")
        else:
            print(f"FAIL: Component 4 - Cannot check footer linkage without 2+ sections")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
