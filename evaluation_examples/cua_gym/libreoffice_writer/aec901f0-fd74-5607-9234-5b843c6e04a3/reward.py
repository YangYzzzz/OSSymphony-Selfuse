"""
Reward Script: Create a custom page style 'Landscape Table' with landscape orientation
                and apply it to the page containing the wide financial comparison table,
                then return to portrait for the rest of the document.
Task ID: writer_biz_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35) — Document has multiple sections (>1), indicating section breaks were added
  Component 2 (0.35) — A landscape-oriented section exists in the document
  Component 3 (0.30) — Sections before and after the landscape section are portrait
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_040'


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

    sections = doc.sections
    num_sections = len(sections)

    # Component 1: Document has multiple sections (0.35 points)
    # Initial doc has only 1 section. The task requires adding section breaks
    # to isolate the table page, so we need at least 3 sections.
    try:
        if num_sections >= 3:
            print(f"PASS: Component 1 — Document has {num_sections} sections (>= 3) (0.35 pts)")
            total_score += 0.35
        elif num_sections == 2:
            print(f"PARTIAL: Component 1 — Document has 2 sections (need >= 3 for before/landscape/after) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Document has only {num_sections} section(s), expected >= 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: A landscape-oriented section exists (0.35 points)
    # The initial doc has no landscape sections. The task requires creating one.
    try:
        landscape_found = False
        landscape_section_indices = []
        for i, sec in enumerate(sections):
            is_landscape = sec.orientation == WD_ORIENT.LANDSCAPE
            # Also check via page dimensions: width > height means landscape
            if not is_landscape:
                # python-docx may not always report orientation enum correctly;
                # check actual page dimensions as fallback
                if sec.page_width is not None and sec.page_height is not None:
                    if sec.page_width > sec.page_height:
                        is_landscape = True
            if is_landscape:
                landscape_found = True
                landscape_section_indices.append(i)

        if landscape_found:
            print(f"PASS: Component 2 — Landscape section found at index(es) {landscape_section_indices} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — No landscape-oriented section found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sections before and after the landscape section are portrait (0.30 points)
    # The task requires returning to portrait for the rest of the document.
    # This verifies that the landscape section is sandwiched between portrait sections.
    try:
        if not landscape_found or num_sections < 3:
            print(f"FAIL: Component 3 — Cannot verify portrait sandwich (no landscape or < 3 sections)")
        else:
            # Check that the first section is portrait
            first_portrait = (sections[0].orientation != WD_ORIENT.LANDSCAPE)
            if not first_portrait and sections[0].page_width is not None and sections[0].page_height is not None:
                first_portrait = sections[0].page_width <= sections[0].page_height

            # Check that the last section is portrait
            last_sec = sections[-1]
            last_portrait = (last_sec.orientation != WD_ORIENT.LANDSCAPE)
            if not last_portrait and last_sec.page_width is not None and last_sec.page_height is not None:
                last_portrait = last_sec.page_width <= last_sec.page_height

            # The landscape section should NOT be first or last
            landscape_not_at_edges = (0 not in landscape_section_indices) and ((num_sections - 1) not in landscape_section_indices)

            if first_portrait and last_portrait and landscape_not_at_edges:
                print(f"PASS: Component 3 — First section portrait={first_portrait}, last section portrait={last_portrait}, landscape not at edges (0.30 pts)")
                total_score += 0.30
            elif first_portrait and last_portrait:
                print(f"PARTIAL: Component 3 — Portrait at edges but landscape at edge too (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — First portrait={first_portrait}, last portrait={last_portrait}, landscape indices={landscape_section_indices}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
