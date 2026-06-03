"""
Reward Script: Configure custom page size 20cm wide x 25cm tall
Task ID: writer_page_005
Domain: libreoffice_writer
Scoring:
  Component 1: Page width == 20.0cm (±0.15cm)                               — 0.5 pts
  Component 2: Page height == 25.0cm (±0.15cm)                              — 0.3 pts
  Component 3: Full page setup correct (width+height both set, portrait,
               and all 4 margins unchanged at 2.54cm)                       — 0.2 pts
Total: 1.0

Note: Component 3 is a compound "completeness bonus" — it only fires when
      both width AND height are already correct, ensuring it never passes on
      the initial_env (which has wrong width and wrong height).
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user/Desktop'
FILE_NAME = 'custom_brochure.docx'

# Target values
WIDTH_TARGET_CM = 20.0
HEIGHT_TARGET_CM = 25.0
MARGIN_TARGET_CM = 2.54
TOLERANCE_CM = 0.15   # ±0.15 cm covers rounding in docx unit storage
MARGIN_TOL_CM = 0.05  # ±0.05 cm for unchanged margins


def verify_task(file_path):
    """
    Verify that the document page size has been changed to 20cm x 25cm
    while keeping the portrait orientation and 2.54cm margins unchanged.

    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have at least one section
    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document.")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Read all values once
    try:
        width_cm = section.page_width.cm
        height_cm = section.page_height.cm
        orientation = section.orientation
        top_cm = section.top_margin.cm
        bottom_cm = section.bottom_margin.cm
        left_cm = section.left_margin.cm
        right_cm = section.right_margin.cm
    except Exception as e:
        print(f"CRITICAL: Cannot read section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------ #
    # Component 1: Page width changed to 20.0cm  (0.5 points)
    # Initial: ~21.0cm (A4). Golden: ~20.0cm. FAILS on initial.
    # ------------------------------------------------------------------ #
    try:
        diff_w = abs(width_cm - WIDTH_TARGET_CM)
        if diff_w <= TOLERANCE_CM:
            print(f"PASS: Component 1 — page width = {width_cm:.4f} cm "
                  f"(target {WIDTH_TARGET_CM} cm, diff {diff_w:.4f} cm) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected page width ~{WIDTH_TARGET_CM} cm, "
                  f"found {width_cm:.4f} cm (diff {diff_w:.4f} cm)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------ #
    # Component 2: Page height changed to 25.0cm  (0.3 points)
    # Initial: ~29.7cm (A4). Golden: ~25.0cm. FAILS on initial.
    # ------------------------------------------------------------------ #
    try:
        diff_h = abs(height_cm - HEIGHT_TARGET_CM)
        if diff_h <= TOLERANCE_CM:
            print(f"PASS: Component 2 — page height = {height_cm:.4f} cm "
                  f"(target {HEIGHT_TARGET_CM} cm, diff {diff_h:.4f} cm) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected page height ~{HEIGHT_TARGET_CM} cm, "
                  f"found {height_cm:.4f} cm (diff {diff_h:.4f} cm)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------ #
    # Component 3: Full completeness check  (0.2 points)
    # Width AND height both correct, PLUS orientation portrait AND
    # all four margins preserved at 2.54cm.
    # This is a compound bonus — because it requires width correct (Component 1)
    # it can never fire on the initial_env where width is wrong (~21cm).
    # ------------------------------------------------------------------ #
    try:
        width_ok = abs(width_cm - WIDTH_TARGET_CM) <= TOLERANCE_CM
        height_ok = abs(height_cm - HEIGHT_TARGET_CM) <= TOLERANCE_CM
        is_portrait = (orientation == WD_ORIENT.PORTRAIT)
        margins_ok = (
            abs(top_cm - MARGIN_TARGET_CM) <= MARGIN_TOL_CM
            and abs(bottom_cm - MARGIN_TARGET_CM) <= MARGIN_TOL_CM
            and abs(left_cm - MARGIN_TARGET_CM) <= MARGIN_TOL_CM
            and abs(right_cm - MARGIN_TARGET_CM) <= MARGIN_TOL_CM
        )

        comp3_pass = width_ok and height_ok and is_portrait and margins_ok
        if comp3_pass:
            print(f"PASS: Component 3 — full page setup correct: width={width_cm:.4f} cm, height={height_cm:.4f} cm, orientation=PORTRAIT, all margins ~{MARGIN_TARGET_CM} cm (0.2 pts)")
            total_score += 0.2
        else:
            failures = []
            if not width_ok:
                failures.append(f"width={width_cm:.4f} cm (expected ~{WIDTH_TARGET_CM})")
            if not height_ok:
                failures.append(f"height={height_cm:.4f} cm (expected ~{HEIGHT_TARGET_CM})")
            if not is_portrait:
                failures.append(f"orientation={orientation} (expected PORTRAIT)")
            if not margins_ok:
                failures.append(
                    f"margins top={top_cm:.4f} bottom={bottom_cm:.4f} "
                    f"left={left_cm:.4f} right={right_cm:.4f} "
                    f"(expected all ~{MARGIN_TARGET_CM})"
                )
            print(f"FAIL: Component 3 — {'; '.join(failures)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# ------------------------------------------------------------------ #
# Entrypoint — runs on the VM where the file lives at WORKDIR
# ------------------------------------------------------------------ #
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
