"""
Reward Script: Create 'AppendixPage' custom page style with landscape, 1.5cm margins, bold centered APPENDIX header
Task ID: writer_tech_063
Domain: libreoffice_writer
Scoring:
  Component 1: Multiple sections exist (Appendix gets its own section) — 0.15
  Component 2: Appendix section has landscape orientation — 0.25
  Component 3: Appendix section has ~1.5 cm margins (all four) — 0.20
  Component 4: Appendix section header contains bold centered 'APPENDIX' — 0.25
  Component 5: Appendix section header is unlinked from previous — 0.15
"""

import os
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_063'

# Tolerance for margin comparison (~0.1 cm)
MARGIN_TOLERANCE = 36000  # EMU; 0.1 cm = 36000 EMU
TARGET_MARGIN = Cm(1.5)   # 540000 EMU


def find_appendix_section(doc):
    """Find the section that contains the Appendix heading.
    In a multi-section doc, the Appendix section should be a later section
    (not section 0) that has distinct page setup."""
    if len(doc.sections) < 2:
        return None
    # The task says "apply it starting from the Appendix section",
    # so we expect a section break before the Appendix content.
    # Return the last section (most likely the Appendix section).
    # Verify by checking if the section actually differs from section 0.
    return doc.sections[-1]


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

    # Component 1: Document has multiple sections (0.15 points)
    # The task requires a section break to apply a different page style to the Appendix.
    # Initial state has only 1 section; golden must have >= 2.
    try:
        num_sections = len(doc.sections)
        if num_sections >= 2:
            print(f"PASS: Component 1 — Document has {num_sections} sections (>= 2) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Document has only {num_sections} section(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the Appendix section for remaining checks
    appendix_section = find_appendix_section(doc)
    if appendix_section is None:
        print("FAIL: No Appendix section found (only 1 section). Remaining checks skipped.")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Appendix section has landscape orientation (0.25 points)
    try:
        is_landscape = appendix_section.orientation == WD_ORIENT.LANDSCAPE
        # Also verify width > height (landscape means wider than tall)
        width_gt_height = appendix_section.page_width > appendix_section.page_height
        if is_landscape and width_gt_height:
            print(f"PASS: Component 2 — Appendix section is landscape (w={appendix_section.page_width}, h={appendix_section.page_height}) (0.25 pts)")
            total_score += 0.25
        elif is_landscape or width_gt_height:
            # Partial: orientation flag set but dimensions not swapped, or vice versa
            print(f"PARTIAL: Component 2 — Landscape partially applied (orient={appendix_section.orientation}, w={appendix_section.page_width}, h={appendix_section.page_height}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Appendix section is not landscape (orient={appendix_section.orientation})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Appendix section has ~1.5 cm margins on all four sides (0.20 points)
    try:
        margins = {
            'left': appendix_section.left_margin,
            'right': appendix_section.right_margin,
            'top': appendix_section.top_margin,
            'bottom': appendix_section.bottom_margin,
        }
        margins_ok = 0
        for name, val in margins.items():
            if val is not None and abs(val - TARGET_MARGIN) <= MARGIN_TOLERANCE:
                margins_ok += 1
                print(f"  Margin {name}: {val} EMU ({val/360000:.2f} cm) — OK")
            else:
                print(f"  Margin {name}: {val} EMU ({val/360000:.2f} cm if set) — expected ~1.5 cm")

        if margins_ok == 4:
            print(f"PASS: Component 3 — All 4 margins are ~1.5 cm (0.20 pts)")
            total_score += 0.20
        elif margins_ok >= 2:
            partial = round(0.20 * margins_ok / 4, 2)
            print(f"PARTIAL: Component 3 — {margins_ok}/4 margins correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {margins_ok}/4 margins match ~1.5 cm")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Appendix section header has centered bold 'APPENDIX' text (0.25 points)
    try:
        header = appendix_section.header
        header_paras = header.paragraphs
        sub_score = 0.0
        header_text = ""

        # Sub-check 4a: Header contains 'APPENDIX' text (0.10 pts)
        appendix_para = None
        if header_paras:
            for p in header_paras:
                if 'APPENDIX' in p.text.strip().upper():
                    appendix_para = p
                    header_text = p.text.strip()
                    break

        if appendix_para is not None:
            sub_score += 0.10
            print(f"  Header text found: '{header_text}'")

            # Sub-check 4b: APPENDIX run is bold (0.075 pts)
            bold_found = any(
                r.bold for r in appendix_para.runs if 'APPENDIX' in r.text.upper()
            )
            if bold_found:
                sub_score += 0.075
                print(f"  Header APPENDIX text is bold")
            else:
                print(f"  FAIL: Header APPENDIX text is not bold")

            # Sub-check 4c: Header paragraph is centered (0.075 pts)
            if appendix_para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                sub_score += 0.075
                print(f"  Header is centered")
            else:
                print(f"  FAIL: Header is not centered")
        else:
            print(f"  FAIL: Header does not contain 'APPENDIX'")

        if sub_score > 0:
            print(f"{'PASS' if sub_score >= 0.25 else 'PARTIAL'}: Component 4 — Header check ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 — No matching header content found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Appendix section header is unlinked from previous (0.15 points)
    # This ensures the header is distinct/not inherited from the first section.
    try:
        header = appendix_section.header
        is_unlinked = not header.is_linked_to_previous
        if is_unlinked:
            print(f"PASS: Component 5 — Header is unlinked from previous section (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Header is still linked to previous section")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
