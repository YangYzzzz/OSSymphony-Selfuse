"""
Reward Script: Format newsletter into two-column layout
Task ID: writer_hr_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Document has multiple sections (>=3) for column layout changes
  Component 2 (0.30): A section with exactly 2 columns exists for article content
  Component 3 (0.20): The 2-column section has ~0.5cm (180000 EMU) column spacing
  Component 4 (0.25): Proper structure: header single-col, then 2-col articles, then footer single-col
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_034'


def persist_app_state(domain):
    """Try to save any unsaved changes via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_section_info(doc):
    """
    Extract section info from the document.
    Sections are defined by:
    1. <w:sectPr> inside <w:pPr> of paragraphs (inline section breaks)
    2. The final <w:sectPr> child of <w:body> (last section)

    Returns list of dicts with 'num_cols', 'col_space', 'type' for each section.
    """
    sections_info = []

    for section in doc.sections:
        sectPr = section._sectPr
        cols_elem = sectPr.find(qn('w:cols'))

        num_cols = 1
        col_space = None

        if cols_elem is not None:
            num_str = cols_elem.get(qn('w:num'))
            if num_str is not None:
                num_cols = int(num_str)
            space_str = cols_elem.get(qn('w:space'))
            if space_str is not None:
                col_space = int(space_str)

        type_elem = sectPr.find(qn('w:type'))
        sec_type = None
        if type_elem is not None:
            sec_type = type_elem.get(qn('w:val'))

        sections_info.append({
            'num_cols': num_cols,
            'col_space': col_space,
            'type': sec_type,
        })

    return sections_info


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

    sections = get_section_info(doc)
    num_sections = len(sections)
    print(f"INFO: Document has {num_sections} section(s)")
    for i, s in enumerate(sections):
        print(f"  Section {i}: cols={s['num_cols']}, space={s['col_space']}, type={s['type']}")

    # Component 1: Document has multiple sections (>=3) for column layout (0.25 pts)
    # Initial has 1 section, golden has 3 sections (header, articles, footer)
    try:
        if num_sections >= 3:
            print(f"PASS: Component 1 -- Document has {num_sections} sections (>=3) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Document has {num_sections} sections, expected >=3")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: A section with exactly 2 columns exists (0.30 pts)
    # Initial has no 2-column section; golden has one for articles
    try:
        two_col_sections = [s for s in sections if s['num_cols'] == 2]
        if len(two_col_sections) > 0:
            print(f"PASS: Component 2 -- Found {len(two_col_sections)} section(s) with 2 columns (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- No section with 2 columns found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The 2-column section has approximately 0.5cm spacing (0.20 pts)
    # 0.5 cm = 180000 EMU (1 cm = 360000 EMU). Allow tolerance of +-10%
    try:
        target_space = 180000  # 0.5 cm in EMU
        tolerance = 18000  # 10% tolerance
        spacing_ok = False
        for s in sections:
            if s['num_cols'] == 2 and s['col_space'] is not None:
                diff = abs(s['col_space'] - target_space)
                if diff <= tolerance:
                    spacing_ok = True
                    print(f"  Found 2-col section with space={s['col_space']} EMU (target={target_space}, diff={diff})")
                    break
                else:
                    print(f"  2-col section space={s['col_space']} EMU, target={target_space}, diff={diff} exceeds tolerance")

        if spacing_ok:
            print(f"PASS: Component 3 -- Column spacing is ~0.5cm ({target_space} EMU) (0.20 pts)")
            total_score += 0.20
        else:
            if len(two_col_sections) > 0:
                spaces = [s['col_space'] for s in sections if s['num_cols'] == 2]
                print(f"FAIL: Component 3 -- Column spacing {spaces} not within tolerance of {target_space} EMU")
            else:
                print(f"FAIL: Component 3 -- No 2-column section to check spacing")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Proper structural layout (0.25 pts)
    # Must have: first section single-col, then 2-col, then single-col
    # This verifies the header stays single, articles are 2-col, footer returns to single
    try:
        if num_sections >= 3:
            # Find the pattern: 1-col -> 2-col -> 1-col
            found_pattern = False
            for i in range(len(sections) - 2):
                if (sections[i]['num_cols'] == 1 and
                    sections[i + 1]['num_cols'] == 2 and
                    sections[i + 2]['num_cols'] == 1):
                    found_pattern = True
                    break

            if found_pattern:
                print(f"PASS: Component 4 -- Found 1-col -> 2-col -> 1-col section pattern (0.25 pts)")
                total_score += 0.25
            else:
                col_seq = [s['num_cols'] for s in sections]
                print(f"FAIL: Component 4 -- Section column pattern {col_seq} does not match 1->2->1")
        else:
            print(f"FAIL: Component 4 -- Need >=3 sections for layout pattern check, found {num_sections}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
