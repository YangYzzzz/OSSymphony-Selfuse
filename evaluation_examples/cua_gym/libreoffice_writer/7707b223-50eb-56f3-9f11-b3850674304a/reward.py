"""
Reward Script: Format body section into 2 columns with 0.8 cm gap and vertical line separator.
Task ID: osworld_writer_section_columns_003
Domain: libreoffice_writer

Scoring rubric (total 1.0):
  Component 1: Body section (section 1) has 2 columns (w:num=2)            — 0.4 pts
  Component 2: Column spacing is approximately 0.8 cm (w:space ~453 twips) — 0.3 pts
  Component 3: Vertical line separator between columns (w:sep=1)            — 0.3 pts

Context:
  The document is a magazine-style article. Section 0 is the header/intro area (stays single column).
  Section 1 is the body section that must be formatted as 2 columns.
  In OOXML, w:space in w:cols is in twentieths of a point (twips).
  0.8 cm = 453.5 twips ≈ 453 twips (as set by LibreOffice Writer).
  We accept values in the range 440–470 twips (~0.78–0.83 cm) for tolerance.
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_section_columns_003'

# Twips per cm: 1440 twips per inch, 2.54 cm per inch
TWIPS_PER_CM = 1440 / 2.54  # ~566.93 twips/cm

# Target: 0.8 cm spacing in twips
TARGET_SPACE_CM = 0.8
TARGET_SPACE_TWIPS = TARGET_SPACE_CM * TWIPS_PER_CM  # ~453.5
SPACE_TOLERANCE_TWIPS = 30  # ±30 twips ≈ ±0.053 cm tolerance


def verify_task(file_path):
    """
    Verify that the body section (section index 1) of the document is formatted
    as 2 columns with ~0.8 cm spacing and a vertical line separator.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: verify file can be loaded and has expected multi-section structure
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least 2 sections (header + body)
    num_sections = len(doc.sections)
    if num_sections < 2:
        print(f"FAIL: Expected at least 2 sections, found {num_sections}. Document structure may be wrong.")
        print("REWARD: 0.0")
        return 0.0

    # The body section is section index 1 (the last section in a 2-section doc)
    body_section = doc.sections[1]
    sectPr = body_section._sectPr
    cols_elem = sectPr.find(qn('w:cols'))

    if cols_elem is None:
        print("FAIL: Body section (section 1) has no w:cols element — single column layout.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the col attributes
    num_cols_str = cols_elem.get(qn('w:num'))
    space_str = cols_elem.get(qn('w:space'))
    sep_str = cols_elem.get(qn('w:sep'))

    print(f"INFO: w:cols attributes — num={num_cols_str!r}, space={space_str!r}, sep={sep_str!r}")

    # Component 1: Body section has 2 columns (w:num=2) — 0.4 points
    try:
        num_cols = int(num_cols_str) if num_cols_str is not None else 1
        if num_cols == 2:
            print(f"PASS: Component 1 — Body section has 2 columns (w:num={num_cols}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 2 columns, found w:num={num_cols_str!r} (effective {num_cols})")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not read column count: {e}")

    # Component 2: Column spacing is approximately 0.8 cm (~453 twips) — 0.3 points
    try:
        if space_str is not None:
            space_twips = int(space_str)
            space_cm = space_twips / TWIPS_PER_CM
            lower = TARGET_SPACE_TWIPS - SPACE_TOLERANCE_TWIPS
            upper = TARGET_SPACE_TWIPS + SPACE_TOLERANCE_TWIPS
            if lower <= space_twips <= upper:
                print(f"PASS: Component 2 — Column spacing is {space_cm:.3f} cm ({space_twips} twips), expected ~{TARGET_SPACE_CM} cm (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Column spacing {space_cm:.3f} cm ({space_twips} twips) not within tolerance of {TARGET_SPACE_CM} cm")
                print(f"       Acceptable range: {lower:.0f}–{upper:.0f} twips ({lower/TWIPS_PER_CM:.3f}–{upper/TWIPS_PER_CM:.3f} cm)")
        else:
            print("FAIL: Component 2 — No w:space attribute found on w:cols element")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not read column spacing: {e}")

    # Component 3: Vertical line separator between columns (w:sep=1) — 0.3 points
    try:
        if sep_str is not None and sep_str == '1':
            print(f"PASS: Component 3 — Vertical line separator is present (w:sep={sep_str}) (0.3 pts)")
            total_score += 0.3
        else:
            actual_sep = sep_str if sep_str is not None else '(not set)'
            print(f"FAIL: Component 3 — Vertical separator not set. w:sep={actual_sep!r}, expected '1'")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check vertical separator: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path on VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
