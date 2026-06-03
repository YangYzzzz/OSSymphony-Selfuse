"""
Reward Script: Read client_feedback.docx and apply changes to mockup.png → mockup_revised.png
Task ID: osworld_multi_apps_writer_to_gimp_008
Domain: multi_apps (libreoffice_writer + gimp)

Task: Read client_feedback.docx on Desktop. It specifies 3 modifications to mockup.png:
  1. Change background color to white (#FFFFFF) — original background is dark/colored
  2. Scale image to 50% of original dimensions (800x600 → 400x300)
  3. Apply a Gaussian blur with radius 2 pixels
Save the result as 'mockup_revised.png' on the Desktop.

Scoring (total 1.0):
  Component 1: mockup_revised.png exists on Desktop           — 0.2 pts
  Component 2: Image size is 50% of original (400×300)       — 0.3 pts
  Component 3: Background is replaced with white              — 0.3 pts
  Component 4: Gaussian blur applied (image is significantly blurrier than naive resize)  — 0.2 pts
"""

import os
from PIL import Image, ImageFilter
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_008'

# Original mockup.png properties (from setup)
ORIGINAL_PATH = f'{WORKDIR}/mockup.png'
REVISED_PATH = f'{WORKDIR}/mockup_revised.png'

# Expected dimensions after 50% scale
EXPECTED_WIDTH = 400
EXPECTED_HEIGHT = 300

# Original background color (dark navy: [30, 45, 90])
ORIG_BG_COLOR = np.array([30, 45, 90])
ORIG_BG_TOLERANCE = 25  # pixels within this distance of original bg are considered "background"

# Sharpness threshold: revised image should be much less sharp than naive resize
# Golden image has sharpness ratio ~0.068 (vs naive resize). Use 0.4 as generous upper bound.
SHARPNESS_RATIO_THRESHOLD = 0.4


def compute_sharpness(arr: np.ndarray) -> float:
    """Compute image sharpness using horizontal+vertical gradient variance."""
    gray = arr.mean(axis=2)
    diff_h = np.diff(gray, axis=1)
    diff_v = np.diff(gray, axis=0)
    return float(np.var(diff_h) + np.var(diff_v))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: mockup_revised.png exists (0.2 points)
    # This FAILS on initial_env (file not present), PASSES on golden_env
    try:
        if os.path.isfile(REVISED_PATH):
            print(f"PASS: Component 1 — mockup_revised.png exists at {REVISED_PATH} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — mockup_revised.png not found at {REVISED_PATH}")
            # File doesn't exist; remaining checks would all fail too
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the revised image — gate for remaining components
    try:
        img_rev = Image.open(REVISED_PATH).convert('RGB')
        arr_rev = np.array(img_rev)
    except Exception as e:
        print(f"CRITICAL: Cannot load mockup_revised.png: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load original image for comparison (reference)
    try:
        img_orig = Image.open(ORIGINAL_PATH).convert('RGB')
        arr_orig = np.array(img_orig)
        orig_w, orig_h = img_orig.size
    except Exception as e:
        print(f"WARN: Cannot load original mockup.png for comparison: {e}")
        orig_w, orig_h = 800, 600  # fallback to known values
        arr_orig = None
        img_orig = None

    # Component 2: Image scaled to 50% of original dimensions (0.3 points)
    # Expected: 400×300 (50% of 800×600)
    # This FAILS on initial_env (file doesn't exist), PASSES on golden_env (size=400×300)
    try:
        rev_w, rev_h = img_rev.size
        expected_w = orig_w // 2
        expected_h = orig_h // 2
        if rev_w == expected_w and rev_h == expected_h:
            print(f"PASS: Component 2 — Image size is {rev_w}×{rev_h} = 50% of {orig_w}×{orig_h} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected size {expected_w}×{expected_h}, found {rev_w}×{rev_h}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Background replaced with white (0.3 points)
    # Original background is dark navy [30, 45, 90]. In revised, corners should be white
    # and no pixels matching original background color should remain.
    # This FAILS on initial_env (file doesn't exist), PASSES on golden_env (corners white, no dark bg)
    try:
        # Check corner pixels — should all be white (255, 255, 255)
        corners = [
            arr_rev[0, 0],       # top-left
            arr_rev[0, -1],      # top-right
            arr_rev[-1, 0],      # bottom-left
            arr_rev[-1, -1],     # bottom-right
        ]
        all_corners_white = all(
            int(c[0]) > 240 and int(c[1]) > 240 and int(c[2]) > 240
            for c in corners
        )
        # Check that no dark background-colored pixels remain
        dark_bg_mask = np.all(
            np.abs(arr_rev.astype(int) - ORIG_BG_COLOR) < ORIG_BG_TOLERANCE,
            axis=2
        )
        no_dark_bg_pixels = dark_bg_mask.sum() == 0

        if all_corners_white and no_dark_bg_pixels:
            print(f"PASS: Component 3 — Background is white (corners all white, 0 dark bg pixels) (0.3 pts)")
            total_score += 0.3
        elif all_corners_white and not no_dark_bg_pixels:
            print(f"FAIL: Component 3 — Corners are white but {dark_bg_mask.sum()} dark bg pixels remain")
        elif not all_corners_white and no_dark_bg_pixels:
            print(f"FAIL: Component 3 — No dark bg pixels but corners not white: {[c.tolist() for c in corners]}")
        else:
            print(f"FAIL: Component 3 — Corners not white ({[c.tolist() for c in corners]}) "
                  f"and {dark_bg_mask.sum()} dark bg pixels remain")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Gaussian blur applied (0.2 points)
    # The revised image should be significantly less sharp than a naive resize without blur.
    # We compute sharpness (gradient variance) of revised vs. naive 50% resize.
    # Sharpness ratio of golden_env ≈ 0.068 (much less sharp than naive resize).
    # Use generous threshold of 0.4 to account for any blur approach.
    # This FAILS on initial_env (file doesn't exist), PASSES on golden_env (ratio ≈ 0.068)
    try:
        if img_orig is not None:
            # Create a naive 50% resize (no blur) for comparison
            naive_resize = img_orig.resize((EXPECTED_WIDTH, EXPECTED_HEIGHT), Image.LANCZOS)
            naive_arr = np.array(naive_resize)
            sharpness_naive = compute_sharpness(naive_arr)
        else:
            # Use original size estimate
            sharpness_naive = 530.0  # fallback from known measurement

        sharpness_revised = compute_sharpness(arr_rev)

        if sharpness_naive > 0:
            ratio = sharpness_revised / sharpness_naive
        else:
            ratio = 1.0

        if ratio < SHARPNESS_RATIO_THRESHOLD:
            print(f"PASS: Component 4 — Blur applied. Sharpness ratio={ratio:.4f} "
                  f"(revised={sharpness_revised:.2f} vs naive={sharpness_naive:.2f}) < {SHARPNESS_RATIO_THRESHOLD} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — No significant blur detected. "
                  f"Sharpness ratio={ratio:.4f} >= {SHARPNESS_RATIO_THRESHOLD} "
                  f"(revised={sharpness_revised:.2f} vs naive={sharpness_naive:.2f})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
