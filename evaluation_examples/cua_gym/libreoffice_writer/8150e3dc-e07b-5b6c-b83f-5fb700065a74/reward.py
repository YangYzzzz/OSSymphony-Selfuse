"""
Reward Script: Apply color correction steps from docx to food photo and save as food_corrected.jpg
Task ID: osworld_multi_apps_writer_gimp_072
Domain: libreoffice_writer + gimp (multi-app)
Scoring:
  - Component 1: food_corrected.jpg exists on Desktop (0.4 pts)
  - Component 2: Overall warmth applied — red channel increased, blue decreased (0.3 pts)
  - Component 3: Color grading applied in shadow regions — red/warmth increase relative to blue in dark areas (0.3 pts)
"""

import os
from PIL import Image
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_writer_gimp_072'

ORIG_PATH = '/home/user/Desktop/food_photo.jpg'
CORR_PATH = '/home/user/Desktop/food_corrected.jpg'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: food_corrected.jpg exists on Desktop (0.4 points)
    # This FAILS on initial_env (file absent) and PASSES on golden_env (file present)
    # Note: file existence here is a TASK-introduced change (it did not exist before the agent acted)
    try:
        file_exists = os.path.isfile(CORR_PATH)
        if file_exists:
            print(f"PASS: Component 1 — food_corrected.jpg found at {CORR_PATH} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — food_corrected.jpg not found at {CORR_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Precondition gate: load both images for further analysis
    try:
        img_corr = Image.open(CORR_PATH).convert('RGB')
        arr_corr = np.array(img_corr).astype(float)
    except Exception as e:
        print(f"CRITICAL: Cannot load corrected image {CORR_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    try:
        img_orig = Image.open(ORIG_PATH).convert('RGB')
        arr_orig = np.array(img_orig).astype(float)
    except Exception as e:
        print(f"CRITICAL: Cannot load original image {ORIG_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Verify images have same dimensions (content preserved)
    if img_orig.size != img_corr.size:
        print(f"FAIL: Image size changed — original {img_orig.size}, corrected {img_corr.size}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Compute per-pixel difference
    diff = arr_corr - arr_orig

    # Component 2: Overall warmth applied — red channel increased AND blue decreased (0.3 points)
    # Task specifies: Hue/Saturation Warmth +8 (via hue rotation) — should increase red tones overall
    # and reduce blue. This FAILS on initial_env (file absent blocks scoring) and PASSES on golden_env.
    try:
        overall_r_diff = diff[:, :, 0].mean()
        overall_b_diff = diff[:, :, 2].mean()
        r_increased = overall_r_diff > 0.5   # red channel mean should increase
        b_decreased = overall_b_diff < -0.5  # blue channel mean should decrease (warmth)

        print(f"  INFO: Overall mean diff R={overall_r_diff:.3f}, G={diff[:,:,1].mean():.3f}, B={overall_b_diff:.3f}")

        if r_increased and b_decreased:
            print(f"PASS: Component 2 — Warmth applied: red +{overall_r_diff:.2f}, blue {overall_b_diff:.2f} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected red > 0 and blue < 0, got R={overall_r_diff:.3f}, B={overall_b_diff:.3f}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Color grading in shadow areas — reduce cyan in shadows means red boosted
    # relative to blue in dark/shadow regions. Task specifies: Color Balance Shadows -8 Cyan.
    # Cyan = complement of Red, so -8 Cyan in shadows means red is relatively increased.
    # This FAILS on initial_env (file absent blocks scoring) and PASSES on golden_env.
    try:
        # Shadow region: pixels where luminance in original is low (< 100)
        lum_orig = arr_orig.mean(axis=2)
        mask_shadows = lum_orig < 100
        shadow_count = mask_shadows.sum()

        if shadow_count > 100:
            sh_diff = diff[mask_shadows]
            sh_r_diff = sh_diff[:, 0].mean()
            sh_b_diff = sh_diff[:, 2].mean()

            print(f"  INFO: Shadow pixel count={shadow_count}, shadow diff R={sh_r_diff:.3f}, B={sh_b_diff:.3f}")

            # Reducing cyan in shadows: red should increase more than blue (or blue should decrease)
            # The criterion: in shadows, red increased AND blue decreased relative to red
            r_gt_b_in_shadows = sh_r_diff > sh_b_diff  # red changed more positively than blue

            if r_gt_b_in_shadows and shadow_count > 0:
                print(f"PASS: Component 3 — Cyan reduced in shadows: R diff={sh_r_diff:.2f} > B diff={sh_b_diff:.2f} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected R diff > B diff in shadows, got R={sh_r_diff:.3f}, B={sh_b_diff:.3f}")
        else:
            # If there are very few dark pixels, use a more lenient check on midtones
            print(f"  WARN: Few shadow pixels ({shadow_count}), checking midtone color shift instead")
            lum_mid = (lum_orig >= 60) & (lum_orig < 150)
            if lum_mid.any():
                mid_diff = diff[lum_mid]
                mid_r_diff = mid_diff[:, 0].mean()
                mid_b_diff = mid_diff[:, 2].mean()
                if mid_r_diff > mid_b_diff:
                    print(f"PASS: Component 3 — Midtone color shift confirms cyan reduction: R={mid_r_diff:.3f}, B={mid_b_diff:.3f} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Midtone check failed: R={mid_r_diff:.3f}, B={mid_b_diff:.3f}")
            else:
                print(f"FAIL: Component 3 — Cannot determine shadow/midtone color shift")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
