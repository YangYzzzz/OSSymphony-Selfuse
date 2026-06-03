"""
Reward Script: Read checklist in photo_tasks.docx, edit scenery.jpg in GIMP and export as scenery_done.jpg
Task ID: osworld_multi_apps_writer_gimp_059
Domain: libreoffice_writer / gimp (multi-app)
Scoring:
  Component 1: scenery_done.jpg exists on Desktop (0.2 pts)
  Component 2: Saturation increased by ~30% compared to original scenery.jpg (0.3 pts)
  Component 3: Vignette effect present — corners significantly darker than center (0.3 pts)
  Component 4: Rotation applied (-2 degrees) — structural match with -2 deg rotated original (0.2 pts)
Total: 1.0
"""

import os

# Domain-specific imports
from PIL import Image, ImageEnhance
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_writer_gimp_059'
DESKTOP = '/home/user/Desktop'

DONE_PATH = f'{DESKTOP}/scenery_done.jpg'
ORIG_PATH = f'{DESKTOP}/scenery.jpg'


def get_saturation_mean(img: Image.Image) -> float:
    """Compute mean saturation channel value (HSV S channel)."""
    hsv = img.convert('HSV')
    sat_channel = np.array(hsv.split()[1])
    return float(np.mean(sat_channel))


def compute_vignette_ratio(img: Image.Image) -> float:
    """
    Compute the ratio of corner brightness to center brightness.
    A vignette darkens corners: ratio << 1.0 indicates vignette present.
    """
    arr = np.array(img.convert('RGB'), dtype=float)
    h, w = arr.shape[:2]
    # Center region (middle 50% area)
    center = arr[h // 4:3 * h // 4, w // 4:3 * w // 4]
    # Four corner regions
    corner_sz_h = h // 8
    corner_sz_w = w // 8
    c_tl = arr[:corner_sz_h, :corner_sz_w]
    c_tr = arr[:corner_sz_h, w - corner_sz_w:]
    c_bl = arr[h - corner_sz_h:, :corner_sz_w]
    c_br = arr[h - corner_sz_h:, w - corner_sz_w:]
    center_brightness = np.mean(center)
    corner_brightness = (np.mean(c_tl) + np.mean(c_tr) + np.mean(c_bl) + np.mean(c_br)) / 4
    if center_brightness == 0:
        # Degenerate case: black image, treat as no vignette
        return 0.0
    return corner_brightness / center_brightness


def compute_rotation_mse(done: Image.Image, orig: Image.Image, angle: float) -> float:
    """
    Rotate orig by angle, then compare center region against done.
    Returns MSE (lower = better match).
    """
    rotated = orig.rotate(angle, resample=Image.BICUBIC, expand=False)
    arr_rot = np.array(rotated.convert('RGB'), dtype=float)
    arr_done = np.array(done.convert('RGB'), dtype=float)

    h, w = arr_done.shape[:2]
    cy_start, cy_end = h // 5, 4 * h // 5
    cx_start, cx_end = w // 5, 4 * w // 5

    center_rot = arr_rot[cy_start:cy_end, cx_start:cx_end]
    center_done = arr_done[cy_start:cy_end, cx_start:cx_end]

    # Normalize brightness to isolate structural differences
    rot_mean = np.mean(center_rot)
    done_mean = np.mean(center_done)
    if done_mean == 0:
        # Degenerate case: black done image, treat as worst match
        return 9999.0
    factor = rot_mean / done_mean
    center_done_norm = center_done * factor

    mse = float(np.mean((center_rot / 255.0 - center_done_norm / 255.0) ** 2))
    return mse


def verify_task(done_path: str, orig_path: str) -> float:
    """
    Verify all four GIMP editing steps were applied and exported to scenery_done.jpg.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load the output image
    try:
        done_img = Image.open(done_path).convert('RGB')
    except Exception as e:
        print(f"CRITICAL: Cannot load {done_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load original for comparison
    try:
        orig_img = Image.open(orig_path).convert('RGB')
    except Exception as e:
        print(f"CRITICAL: Cannot load {orig_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: scenery_done.jpg exists on Desktop (0.2 pts)
    # This only passes if the file was created (absent from initial_env)
    try:
        if os.path.isfile(done_path):
            print(f"PASS: Component 1 — scenery_done.jpg exists at {done_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — scenery_done.jpg not found at {done_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Saturation boosted by ~30% (0.3 pts)
    # Task: "Boost saturation by 30%"
    # Expected: done image saturation / original image saturation in range [1.10, 1.50]
    # (GIMP workflow may produce slightly different boost factor than PIL due to color model)
    try:
        orig_sat = get_saturation_mean(orig_img)
        done_sat = get_saturation_mean(done_img)
        if orig_sat > 0:
            sat_ratio = done_sat / orig_sat
        else:
            sat_ratio = 0.0
        print(f"  Saturation: orig={orig_sat:.2f}, done={done_sat:.2f}, ratio={sat_ratio:.3f}")
        if 1.10 <= sat_ratio <= 1.50:
            print(f"PASS: Component 2 — Saturation increased by ~30% (ratio={sat_ratio:.3f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Saturation ratio={sat_ratio:.3f}, expected in [1.10, 1.50]")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Vignette effect present (0.3 pts)
    # Task: "Add a vignette effect"
    # A vignette darkens the corners relative to center.
    # Expected: vignette ratio (corner_brightness / center_brightness) < 0.75
    # The original image has an inverted pattern (bright corners): ratio ~1.22
    try:
        done_vignette = compute_vignette_ratio(done_img)
        orig_vignette = compute_vignette_ratio(orig_img)
        print(f"  Vignette ratio: orig={orig_vignette:.3f}, done={done_vignette:.3f}")
        # done corners must be darker than center (< 0.75)
        # AND done corners must be significantly darker than in the original (done_vignette < orig_vignette * 0.7)
        if done_vignette < 0.75 and done_vignette < orig_vignette * 0.7:
            print(f"PASS: Component 3 — Vignette effect present (ratio={done_vignette:.3f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Vignette not detected (ratio={done_vignette:.3f}, expected < 0.75)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Rotation applied (-2 degrees) (0.2 pts)
    # Task: "Correct perspective distortion (rotate -2 degrees)"
    # Verify by comparing: MSE(done, rot(-2, orig)) should be much lower than MSE(done, orig)
    try:
        mse_rot_neg2 = compute_rotation_mse(done_img, orig_img, -2.0)
        mse_zero = compute_rotation_mse(done_img, orig_img, 0.0)
        print(f"  Rotation MSE: no-rot={mse_zero:.6f}, rot-2={mse_rot_neg2:.6f}")
        # The -2 degree rotated version should match done better than 0 degrees
        # AND the absolute MSE should be reasonably low (< 0.005)
        if mse_rot_neg2 < mse_zero * 0.8 and mse_rot_neg2 < 0.005:
            print(f"PASS: Component 4 — Rotation -2 deg applied (mse_rot-2={mse_rot_neg2:.6f}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Rotation not detected (mse_rot-2={mse_rot_neg2:.6f}, mse_no_rot={mse_zero:.6f})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: check that output file exists before proceeding
if not os.path.isfile(DONE_PATH):
    print(f"File not found: {DONE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DONE_PATH, ORIG_PATH)
