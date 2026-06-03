"""
Reward Script: Set up a 'Landscape Table' page style with landscape orientation for page 5
Task ID: writer_af_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Document has multiple sections (>= 3) indicating section breaks were added
  Component 2 (0.3): A landscape-oriented section exists in the document
  Component 3 (0.2): The section following the landscape section is portrait (return to portrait)
  Component 4 (0.2): The wide 12-column table is inside the landscape section
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_af_032'


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
    print(f"INFO: Document has {num_sections} section(s)")

    # Component 1: Document has >= 3 sections (0.3 points)
    # Initial doc has only 1 section. The task requires adding section breaks
    # to create a landscape section for the wide table, so we need at least 3:
    # portrait -> landscape (table) -> portrait
    try:
        if num_sections >= 3:
            print(f"PASS: Component 1 — Document has {num_sections} sections (>= 3 required) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Document has {num_sections} sections, expected >= 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: At least one section has landscape orientation (0.3 points)
    # Initial doc has no landscape sections. The task requires creating a
    # landscape section for the wide table.
    try:
        landscape_sections = []
        for i, section in enumerate(doc.sections):
            orient = section.orientation
            pg_w = section.page_width
            pg_h = section.page_height
            is_landscape = (orient == WD_ORIENT.LANDSCAPE) or (pg_w is not None and pg_h is not None and pg_w > pg_h)
            print(f"  Section {i}: orientation={orient}, width={pg_w}, height={pg_h}, is_landscape={is_landscape}")
            if is_landscape:
                landscape_sections.append(i)

        if len(landscape_sections) > 0:
            print(f"PASS: Component 2 — Found landscape section(s): {landscape_sections} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No landscape sections found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The section AFTER the landscape section returns to portrait (0.2 points)
    # This verifies the task requirement that page 6 onwards returns to portrait.
    try:
        found_return_to_portrait = False
        for ls_idx in landscape_sections:
            next_idx = ls_idx + 1
            if next_idx < num_sections:
                next_section = doc.sections[next_idx]
                next_orient = next_section.orientation
                next_w = next_section.page_width
                next_h = next_section.page_height
                is_portrait = (next_orient == WD_ORIENT.PORTRAIT or next_orient is None) and (next_w is not None and next_h is not None and next_h > next_w)
                if is_portrait:
                    found_return_to_portrait = True
                    break

        if found_return_to_portrait:
            print(f"PASS: Component 3 — Section after landscape returns to portrait (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — No portrait section found after landscape section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The wide 12-column table is inside the landscape section (0.2 points)
    # The initial doc has a 12-col table (Infrastructure Capacity Planning) that is
    # cut off in portrait. In the golden state, this table should be in the landscape section.
    try:
        body = doc.element.body
        current_section_idx = 0
        wide_table_in_landscape = False

        for elem in body:
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

            if tag == 'p':
                # Check if this paragraph ends a section (has sectPr in pPr)
                pPr = elem.find(qn('w:pPr'))
                if pPr is not None:
                    sect = pPr.find(qn('w:sectPr'))
                    if sect is not None:
                        current_section_idx += 1

            elif tag == 'tbl':
                # Count columns in first row
                first_row = elem.find(qn('w:tr'))
                col_count = 0
                if first_row is not None:
                    col_count = len(first_row.findall(qn('w:tc')))

                # Check if this is our wide table (12 columns)
                if col_count >= 10:
                    # Check if current section is landscape
                    if current_section_idx < num_sections:
                        sect = doc.sections[current_section_idx]
                        orient = sect.orientation
                        pg_w = sect.page_width
                        pg_h = sect.page_height
                        is_landscape = (orient == WD_ORIENT.LANDSCAPE) or (pg_w is not None and pg_h is not None and pg_w > pg_h)
                        print(f"  Wide table ({col_count} cols) found in section {current_section_idx}, landscape={is_landscape}")
                        if is_landscape:
                            wide_table_in_landscape = True

        if wide_table_in_landscape:
            print(f"PASS: Component 4 — Wide table (>=10 cols) is in landscape section (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Wide table not found in a landscape section")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
