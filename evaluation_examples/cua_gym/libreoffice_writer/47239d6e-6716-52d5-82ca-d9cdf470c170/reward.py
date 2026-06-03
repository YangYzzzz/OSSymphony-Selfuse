"""
Reward Script: Prepare artwork.jpg to print specifications documented in print_requirements.docx
Task ID: osworld_multi_apps_writer_to_gimp_014
Domain: gimp (multi-app: libreoffice_writer + gimp)

Scoring Rubric (total = 1.0):
  Component 1: Output file artwork_print_ready.jpg exists (precondition gate)
  Component 2: 300 DPI resolution metadata in output file (0.4 points)
  Component 3: Correct canvas size after bleed addition (670x520 px) (0.4 points)
  Component 4: RGB color mode in output file (0.2 points)

Requirements from print_requirements.docx:
  - RGB color mode
  - 300 DPI resolution
  - 3 mm bleed on all sides (~35 px at 300 DPI → +70 width, +70 height)
  - Output file: artwork_print_ready.jpg on Desktop

Initial artwork.jpg: 600x450, 72 DPI, RGB
Expected output: 670x520, 300 DPI, RGB
"""

import os
from PIL import Image

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_014'

# Expected specifications from print_requirements.docx
EXPECTED_DPI = 300
# Initial artwork is 600x450; bleed adds 35 px per side → +70 per dimension
INITIAL_WIDTH = 600
INITIAL_HEIGHT = 450
BLEED_PX = 35  # 3 mm at 300 DPI ≈ 35 px
EXPECTED_WIDTH = INITIAL_WIDTH + 2 * BLEED_PX   # 670
EXPECTED_HEIGHT = INITIAL_HEIGHT + 2 * BLEED_PX  # 520
EXPECTED_MODE = 'RGB'
# Allow small tolerance in bleed (±2 px per side) due to rounding differences
BLEED_TOLERANCE = 2


def verify_task(output_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.isfile(output_path):
        print(f"FAIL: Output file not found: {output_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the output image
    try:
        img = Image.open(output_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open output file {output_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    actual_mode = img.mode
    actual_size = img.size  # (width, height)
    actual_dpi = img.info.get('dpi', None)

    print(f"INFO: Output image — mode={actual_mode}, size={actual_size}, dpi={actual_dpi}")

    # Component 1: RGB color mode (0.2 points)
    # The requirements specify RGB mode. FAILS on initial_env (file absent).
    try:
        if actual_mode == EXPECTED_MODE:
            print(f"PASS: Component 1 — RGB color mode confirmed (mode={actual_mode}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected mode={EXPECTED_MODE}, found mode={actual_mode}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 300 DPI resolution metadata (0.4 points)
    # The requirements specify exactly 300 DPI. Initial artwork.jpg has 72 DPI.
    # FAILS on initial_env (file absent). PASSES on golden_env (300 DPI saved).
    try:
        dpi_matches = (actual_dpi is not None
                       and abs(actual_dpi[0] - EXPECTED_DPI) <= 1
                       and abs(actual_dpi[1] - EXPECTED_DPI) <= 1)
        if dpi_matches:
            print(f"PASS: Component 2 — 300 DPI metadata confirmed (dpi={actual_dpi}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected DPI={EXPECTED_DPI}x{EXPECTED_DPI}, found dpi={actual_dpi}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct canvas size including 3mm bleed (0.4 points)
    # Requirements: add 35 px bleed on each of 4 sides.
    # Initial (600x450) → Expected (670x520).
    # FAILS on initial_env (file absent). PASSES on golden_env (670x520).
    try:
        actual_width, actual_height = actual_size
        width_ok = abs(actual_width - EXPECTED_WIDTH) <= BLEED_TOLERANCE
        height_ok = abs(actual_height - EXPECTED_HEIGHT) <= BLEED_TOLERANCE
        if width_ok and height_ok:
            print(f"PASS: Component 3 — Correct canvas size {actual_size} matches expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} (bleed=35px/side) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — Expected size {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} (bleed=35px/side), found {actual_size}")
            # Partial: check if either width OR height matches (partial bleed applied)
            if width_ok or height_ok:
                print(f"  Note: partial bleed detected (one axis matches)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical output path
output_file = os.path.join(WORKDIR, 'artwork_print_ready.jpg')
verify_task(output_file)
