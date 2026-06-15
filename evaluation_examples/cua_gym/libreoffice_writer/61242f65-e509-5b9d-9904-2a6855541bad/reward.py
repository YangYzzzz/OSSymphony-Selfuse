"""
Reward Script: Apply image edits from my_notes.docx to screenshot.png using GIMP
Task ID: osworld_multi_apps_writer_to_gimp_011
Domain: multi_apps (libreoffice_writer + gimp)

Task: Read my_notes.docx on Desktop (which specifies: crop top 100 pixels, add 50% opacity blue overlay),
then apply those edits to screenshot.png using GIMP, saving result as screenshot_edited.png.

Scoring Rubric:
  Component 1: screenshot_edited.png exists with correct dimensions (1280x700) — 0.4 pts
               Verifies that the crop (top 100px removed) was applied correctly
  Component 2: Blue overlay correctly applied — pixel values match expected formula — 0.4 pts
               Expected: edited = original_cropped * 0.5 + [0, 0, 255] * 0.5 (within tolerance of 10)
  Component 3: Strong blue channel dominance — mean blue >> mean red and mean green — 0.2 pts
               Final sanity check that the blue tint is clearly dominant
  Total: 1.0
"""

import os
import sys

# Image processing libraries available in VM
from PIL import Image
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_011'

EDITED_PATH = f'{WORKDIR}/screenshot_edited.png'
ORIGINAL_PATH = f'{WORKDIR}/screenshot.png'

# Expected values based on task requirements from my_notes.docx:
#   Step 1: Crop top 100 pixels -> expected size (1280, 700)
#   Step 2: Add 50% opacity blue (0, 0, 255) overlay
EXPECTED_WIDTH = 1280
EXPECTED_HEIGHT = 700  # 800 - 100 = 700
CROP_TOP = 100
BLUE_OVERLAY_OPACITY = 0.5
PIXEL_TOLERANCE = 10  # allow rounding differences from GIMP PNG export


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: screenshot_edited.png must exist to score anything
    if not os.path.exists(EDITED_PATH):
        print(f"FAIL: screenshot_edited.png not found at {EDITED_PATH}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load edited image
    try:
        img_edited = Image.open(EDITED_PATH).convert('RGB')
    except Exception as e:
        print(f"CRITICAL: Cannot load edited image {EDITED_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Correct image dimensions (1280x700 — crop top 100px from 1280x800) (0.4 pts)
    try:
        actual_width, actual_height = img_edited.size
        if actual_width == EXPECTED_WIDTH and actual_height == EXPECTED_HEIGHT:
            print(f"PASS: Component 1 — Correct dimensions {actual_width}x{actual_height} "
                  f"(expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, top {CROP_TOP}px cropped) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected dimensions {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, "
                  f"found {actual_width}x{actual_height}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Blue overlay correctly applied (0.4 pts)
    # Expected formula: edited[x,y] = original[100+x, y] * 0.5 + [0, 0, 255] * 0.5
    # i.e., each channel: R_out = R_orig * 0.5, G_out = G_orig * 0.5, B_out = B_orig * 0.5 + 127.5
    try:
        if not os.path.exists(ORIGINAL_PATH):
            print(f"FAIL: Component 2 — Original screenshot.png not found at {ORIGINAL_PATH}")
        else:
            img_orig = Image.open(ORIGINAL_PATH).convert('RGB')
            arr_orig = np.array(img_orig, dtype=np.float32)
            arr_edited = np.array(img_edited, dtype=np.float32)

            # Compute expected result: crop top 100px then blend with blue at 50% opacity
            arr_cropped = arr_orig[CROP_TOP:, :, :]  # shape (700, 1280, 3)

            if arr_cropped.shape != arr_edited.shape:
                print(f"FAIL: Component 2 — Shape mismatch: cropped={arr_cropped.shape}, "
                      f"edited={arr_edited.shape}")
            else:
                blue_overlay = np.array([0, 0, 255], dtype=np.float32)
                expected = arr_cropped * (1 - BLUE_OVERLAY_OPACITY) + blue_overlay * BLUE_OVERLAY_OPACITY
                expected = np.clip(expected, 0, 255)

                diff = np.abs(arr_edited - expected)
                max_diff = float(diff.max())
                mean_diff = float(diff.mean())
                pct_within_tol = float((diff <= PIXEL_TOLERANCE).all(axis=2).mean()) * 100

                if pct_within_tol >= 99.0:
                    print(f"PASS: Component 2 — Blue overlay correctly applied "
                          f"(mean diff={mean_diff:.3f}, max diff={max_diff:.1f}, "
                          f"{pct_within_tol:.1f}% pixels within {PIXEL_TOLERANCE} tolerance) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Blue overlay not correctly applied "
                          f"(mean diff={mean_diff:.3f}, max diff={max_diff:.1f}, "
                          f"only {pct_within_tol:.1f}% pixels within {PIXEL_TOLERANCE} tolerance)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Blue channel significantly dominates (0.2 pts)
    # After 50% blue overlay, mean B should be >> mean R and mean G
    try:
        arr_edited = np.array(img_edited, dtype=np.float32)
        mean_r = float(arr_edited[:, :, 0].mean())
        mean_g = float(arr_edited[:, :, 1].mean())
        mean_b = float(arr_edited[:, :, 2].mean())

        # Blue channel should be significantly higher (at least 100 units above R and G)
        # In golden: B≈234, R≈105, G≈105 — difference is ~129
        blue_dominance_r = mean_b - mean_r
        blue_dominance_g = mean_b - mean_g
        threshold = 80  # generous threshold to account for different source images

        if mean_b > mean_r and mean_b > mean_g and blue_dominance_r > threshold and blue_dominance_g > threshold:
            print(f"PASS: Component 3 — Blue channel dominant "
                  f"(mean R={mean_r:.1f}, G={mean_g:.1f}, B={mean_b:.1f}, "
                  f"B-R diff={blue_dominance_r:.1f}, B-G diff={blue_dominance_g:.1f}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Blue channel not sufficiently dominant "
                  f"(mean R={mean_r:.1f}, G={mean_g:.1f}, B={mean_b:.1f}, "
                  f"B-R diff={blue_dominance_r:.1f}, B-G diff={blue_dominance_g:.1f})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
