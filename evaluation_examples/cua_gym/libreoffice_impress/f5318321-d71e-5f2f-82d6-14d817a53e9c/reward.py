"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set page size to A5 Landscape with 2.5 cm margins on all sides.
Generated: 2025-10-17 11:37:43
Status: success
Model: azure-o3
Total Steps: 16
"""

import os
import zipfile
import re
from pptx import Presentation


def cm_to_emu(cm: float) -> int:
    """Convert centimetres to English Metric Units (EMU)."""
    # 1 inch  = 914400 EMU
    # 1 inch  = 2.54 cm  ⇒ 1 cm ≈ 360000 EMU
    return int(round(cm * 360000))


def verify_presentation_page_setup(file_path: str) -> float:
    """Verify that the presentation has:
    1. Page size set to A5 Landscape (21.0 cm × 14.8 cm)
    2. Margins (print settings) set to 2.5 cm on all sides

    Returns a progressive score between 0.0 and 1.0.
    """
    max_score = 1.0
    score = 0.0

    print(f"Verifying presentation file: {file_path}")

    # ------------------------------------------------------------------
    # 0. Preliminary – file existence & loading (no points for this!)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        return 0.0

    try:
        prs = Presentation(file_path)
    except Exception as e:
        print(f"✗ Failed to load PPTX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 1. Slide size must be A5 landscape
    # ------------------------------------------------------------------
    expected_width_cm = 21.0   # A5 long edge
    expected_height_cm = 14.8  # A5 short edge

    expected_width_emu = cm_to_emu(expected_width_cm)
    expected_height_emu = cm_to_emu(expected_height_cm)

    actual_width_emu = prs.slide_width
    actual_height_emu = prs.slide_height

    tolerance = 10000  # EMU tolerance (~0.03 cm) to allow minor rounding

    width_matches = abs(actual_width_emu - expected_width_emu) <= tolerance
    height_matches = abs(actual_height_emu - expected_height_emu) <= tolerance
    orientation_ok = actual_width_emu > actual_height_emu  # landscape

    if width_matches and height_matches and orientation_ok:
        print(f"✓ Slide size matches A5 landscape ({actual_width_emu} × {actual_height_emu} EMU)")
        score += 0.6
    else:
        print("✗ Slide size does not match A5 landscape")
        print(f"  Expected ≈ {expected_width_emu} × {expected_height_emu} EMU, "
              f"got {actual_width_emu} × {actual_height_emu} EMU")

    # ------------------------------------------------------------------
    # 2. Margins (print settings) must be 2.5 cm on all sides
    # ------------------------------------------------------------------
    expected_margin_emu = cm_to_emu(2.5)
    margin_verified = False

    try:
        with zipfile.ZipFile(file_path) as z:
            if "ppt/presentation.xml" in z.namelist():
                xml_data = z.read("ppt/presentation.xml").decode("utf-8", errors="ignore")

                # Look for <p:prnPr ... lm=".." tm=".." rm=".." bm=".." /> elements
                for match in re.finditer(r"<p:prnPr[^>]+>", xml_data):
                    tag = match.group(0)
                    attrs = dict(re.findall(r"\b([ltrb]m)=\"(\d+)\"", tag))  # lm, tm, rm, bm

                    if all(side in attrs for side in ("lm", "tm", "rm", "bm")):
                        values = [int(attrs[side]) for side in ("lm", "tm", "rm", "bm")]
                        if all(abs(v - expected_margin_emu) <= tolerance for v in values):
                            margin_verified = True
                            print(f"✓ Found prnPr with correct 2.5 cm margins: {values}")
                            break
    except Exception as e:
        print(f"✗ Error while reading presentation XML for margin verification: {e}")

    if margin_verified:
        score += 0.4
    else:
        print("✗ Margins are not set to 2.5 cm on all sides")

    # ------------------------------------------------------------------
    # Final scoring
    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# ----------------------------
# Execute verification routine
# ----------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/set_page_size_to_a5_landscape_with_25_cm_margins_on_all_sides.pptx"
    verify_presentation_page_setup(FILE_PATH)

