"""
Reward Script: Set column spacing to 1.0cm and add separator line between columns
Task ID: writer_page_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Column spacing changed to ~1.0cm (567 twips in w:space attribute)
  Component 2 (0.3): Separator line enabled (w:sep="1" on cols element)
  Component 3 (0.2): Column count still 2 and page layout intact (precondition satisfied)
Total: 1.0

Context ground truth:
  - column spacing changed from 0.50cm to 1.0cm  →  w:space ~567 twips
  - separator line enabled  →  w:sep="1"
  - column count remains 2
  - other page settings unchanged (A4, portrait, margins)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_032'
FILE_PATH = f'{WORKDIR}/parish_newsletter.docx'

# 1 cm in twips = 1440 / 2.54 ≈ 566.93  →  we accept 557-577 (~±1%)
CM_TO_TWIPS = 1440.0 / 2.54          # ≈ 566.93
TARGET_SPACING_CM = 1.0
TARGET_SPACING_TWIPS = CM_TO_TWIPS * TARGET_SPACING_CM  # ≈ 566.93
SPACING_TOLERANCE = 20               # twips tolerance (~0.035 cm)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Precondition gate: file must be loadable ──────────────────────────────
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Grab the section's sectPr element (first section covers the whole document)
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        cols_elem = sectPr.find(qn('w:cols'))
    except Exception as e:
        print(f"CRITICAL: Cannot access section/cols element: {e}")
        print("REWARD: 0.0")
        return 0.0

    if cols_elem is None:
        print("CRITICAL: No <w:cols> element found — column layout missing")
        print("REWARD: 0.0")
        return 0.0

    # ── Component 1: Column spacing changed to ~1.0 cm (0.5 points) ──────────
    # The w:space attribute on <w:cols> holds the gap between columns in twips.
    # Initial: 283 twips (~0.5cm).  Golden: 567 twips (~1.0cm).
    try:
        space_attr = cols_elem.get(qn('w:space'))
        if space_attr is not None:
            space_twips = int(space_attr)
            diff = abs(space_twips - TARGET_SPACING_TWIPS)
            if diff <= SPACING_TOLERANCE:
                print(f"PASS: Component 1 — column spacing is {space_twips} twips "
                      f"(~{space_twips / CM_TO_TWIPS:.3f} cm, expected ~1.0 cm) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — column spacing is {space_twips} twips "
                      f"(~{space_twips / CM_TO_TWIPS:.3f} cm), expected ~{TARGET_SPACING_TWIPS:.0f} twips (~1.0 cm)")
        else:
            print("FAIL: Component 1 — w:space attribute missing on <w:cols>")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: Separator line enabled between columns (0.3 points) ─────
    # The w:sep attribute on <w:cols> controls the thin vertical separator line.
    # Initial: absent.  Golden: w:sep="1".
    try:
        sep_attr = cols_elem.get(qn('w:sep'))
        if sep_attr is not None and sep_attr in ('1', 'true', 'on'):
            print(f"PASS: Component 2 — separator line enabled (w:sep={sep_attr!r}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — separator line not enabled "
                  f"(w:sep={sep_attr!r}, expected '1')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: Spacing AND column width correctly adjusted (0.2 points) ──
    # When spacing is widened from ~0.5cm to ~1.0cm the individual column widths
    # decrease accordingly to keep the total text area constant.  In the golden
    # file each col element carries w:space=567 and w:w≈4819.  This compound
    # check verifies that the spacing change propagated to the per-column
    # w:space value AND that the col widths were recalculated — something that
    # ONLY happens after the task is completed.  In the initial file the per-col
    # w:space is 283 and w:w is 4961, so this check will FAIL on initial_env.
    try:
        col_elems = cols_elem.findall(qn('w:col'))
        if len(col_elems) >= 1:
            first_col_space = col_elems[0].get(qn('w:space'))
            first_col_w = col_elems[0].get(qn('w:w'))
            first_col_space_val = int(first_col_space) if first_col_space is not None else None
            first_col_w_val = int(first_col_w) if first_col_w is not None else None

            # Per-column spacing should match the global spacing (~567 twips)
            space_ok = (first_col_space_val is not None and
                        abs(first_col_space_val - TARGET_SPACING_TWIPS) <= SPACING_TOLERANCE)
            # Column width should be reduced from 4961 (initial) to ~4819 (golden)
            # Accept any value strictly less than 4900 to avoid false positive on initial
            width_reduced = (first_col_w_val is not None and first_col_w_val < 4900)

            if space_ok and width_reduced:
                print(f"PASS: Component 3 — per-column spacing={first_col_space_val} twips "
                      f"and width={first_col_w_val} twips (correctly adjusted) (0.2 pts)")
                total_score += 0.2
            else:
                reasons = []
                if not space_ok:
                    reasons.append(f"per-col w:space={first_col_space_val} (expected ~567)")
                if not width_reduced:
                    reasons.append(f"col w:w={first_col_w_val} (expected <4900, got initial-like value)")
                print(f"FAIL: Component 3 — {'; '.join(reasons)}")
        else:
            print("FAIL: Component 3 — no <w:col> child elements found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
