"""
Reward Script: Apply page break before 'Appendix A' and set landscape orientation
Task ID: writer_page_073
Domain: libreoffice_writer
Scoring:
  Component 1: Document has 2 sections (section break inserted before Appendix A) — 0.30 pts
  Component 2: The second section (Appendix A section) uses landscape orientation — 0.40 pts
  Component 3: Landscape section has correct A4 dimensions and preserved 2.54cm margins — 0.30 pts
Total: 1.0

Key facts from exploration:
  - File: /home/user/Desktop/technical_report.docx
  - Initial: 1 section (portrait), 60 paragraphs
  - Golden: 2 sections — Section 0: portrait A4 (21x29.7cm), Section 1: landscape A4 (29.7x21cm)
  - Section break encoded as sectPr in para 54 (empty paragraph before Appendix A at para 55)
  - All margins: 2.54cm (914400 EMU) top/bottom/left/right in both sections
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_073'
FILE_NAME = 'technical_report.docx'
FILE_PATH = os.path.join(WORKDIR, FILE_NAME)

# Tolerance for dimension comparison (EMU): ±30000 (~0.08cm, accounting for rounding)
EMU_TOLERANCE = 30000

# Expected dimensions for A4 in EMU (1 inch = 914400 EMU, 1 cm = 914400/2.54 EMU)
# A4 portrait: 21cm x 29.7cm
# A4 landscape: 29.7cm x 21.0cm
A4_PORTRAIT_W = 7560310   # ~21.00 cm
A4_PORTRAIT_H = 10692130  # ~29.70 cm
A4_LANDSCAPE_W = 10692130  # ~29.70 cm
A4_LANDSCAPE_H = 7560310   # ~21.00 cm
MARGIN_2_54CM = 914400      # 2.54 cm in EMU


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file ' + str(file_path) + ': ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    sections = doc.sections

    # Component 1: Document has exactly 2 sections (section break inserted before Appendix A) (0.30 pts)
    # In the initial file there is only 1 section. Adding a section break creates 2 sections.
    try:
        num_sections = len(sections)
        if num_sections >= 2:
            print('PASS: Component 1 — Document has ' + str(num_sections) + ' sections (expected >= 2). Section break inserted. (0.30 pts)')
            total_score += 0.30
        else:
            print('FAIL: Component 1 — Expected >= 2 sections, found: ' + str(num_sections) + '. No section break detected before Appendix A.')
    except Exception as e:
        print('ERROR: Component 1 — ' + str(e))

    # Component 2: The second section (index 1) uses landscape orientation (0.40 pts)
    # The section containing Appendix A should be landscape. In initial, there is only 1 section (portrait).
    try:
        if len(sections) >= 2:
            landscape_section = sections[1]
            orientation = landscape_section.orientation
            if orientation == WD_ORIENT.LANDSCAPE:
                print('PASS: Component 2 — Section 1 orientation is LANDSCAPE. Appendix A section correctly set to landscape. (0.40 pts)')
                total_score += 0.40
            else:
                print('FAIL: Component 2 — Section 1 orientation is ' + str(orientation) + ', expected LANDSCAPE.')
        else:
            print('FAIL: Component 2 — No Section 1 exists (only ' + str(len(sections)) + ' section(s) found). Cannot check orientation.')
    except Exception as e:
        print('ERROR: Component 2 — ' + str(e))

    # Component 3: Landscape section has correct A4 landscape dimensions and preserved margins (0.30 pts)
    # A4 landscape: width ~29.7cm (10692130 EMU), height ~21.0cm (7560310 EMU)
    # Margins should be 2.54cm (914400 EMU) on all sides
    try:
        if len(sections) >= 2:
            ls = sections[1]
            w = ls.page_width
            h = ls.page_height
            tm = ls.top_margin
            bm = ls.bottom_margin
            lm = ls.left_margin
            rm = ls.right_margin

            # Check A4 landscape dimensions
            w_ok = abs(w - A4_LANDSCAPE_W) <= EMU_TOLERANCE
            h_ok = abs(h - A4_LANDSCAPE_H) <= EMU_TOLERANCE

            # Check margins preserved (2.54cm = 914400 EMU, allow ±10000 EMU tolerance)
            margin_tol = 30000
            tm_ok = abs(tm - MARGIN_2_54CM) <= margin_tol
            bm_ok = abs(bm - MARGIN_2_54CM) <= margin_tol
            lm_ok = abs(lm - MARGIN_2_54CM) <= margin_tol
            rm_ok = abs(rm - MARGIN_2_54CM) <= margin_tol
            margins_ok = tm_ok and bm_ok and lm_ok and rm_ok

            w_cm = round(w / 914400 * 2.54, 2) if w else None
            h_cm = round(h / 914400 * 2.54, 2) if h else None
            tm_cm = round(tm / 914400 * 2.54, 2) if tm else None

            if w_ok and h_ok and margins_ok:
                print('PASS: Component 3 — Landscape section has correct A4 dimensions (' + str(w_cm) + 'cm x ' + str(h_cm) + 'cm) and preserved margins (top=' + str(tm_cm) + 'cm). (0.30 pts)')
                total_score += 0.30
            elif w_ok and h_ok:
                print('PARTIAL: Component 3 — A4 dimensions correct (' + str(w_cm) + 'cm x ' + str(h_cm) + 'cm) but margins not preserved (top=' + str(tm_cm) + 'cm, expected 2.54cm). (0.15 pts)')
                total_score += 0.15
            else:
                print('FAIL: Component 3 — Landscape section dimensions: ' + str(w_cm) + 'cm x ' + str(h_cm) + 'cm (expected ~29.70cm x 21.00cm). Margins top=' + str(tm_cm) + 'cm.')
        else:
            print('FAIL: Component 3 — No Section 1 exists. Cannot check dimensions.')
    except Exception as e:
        print('ERROR: Component 3 — ' + str(e))

    final_score = min(total_score, 1.0)
    print('')
    print('Score: ' + str(total_score) + '/1.0')
    print('REWARD: ' + str(final_score))
    return final_score


if not os.path.exists(FILE_PATH):
    print('File not found: ' + FILE_PATH)
    print('REWARD: 0.0')
else:
    verify_task(FILE_PATH)
