"""
Reward Script: Edit landscape.jpg following editing_checklist.docx steps, save as landscape_edited.jpg
Task ID: osworld_multi_apps_writer_to_gimp_007
Domain: multi_apps (libreoffice_writer + gimp)

Scoring Rubric:
  Component 1: landscape_edited.jpg exists on Desktop                    — 0.2 pts
  Component 2: Image has correct 16:9 crop (1920x1080)                   — 0.3 pts
  Component 3: Saturation increased by ~20% compared to original         — 0.3 pts
  Component 4: Vignette effect applied (edges darker than center)        — 0.2 pts
  Total: 1.0
"""

import os

# Only standard + imaging libs used
from PIL import Image, ImageEnhance
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_to_gimp_007'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Read editing_checklist.docx (crop to 16:9, saturate by 1.2, add vignette)
    2. Apply these operations to landscape.jpg (1920x1200)
    3. Save result as landscape_edited.jpg on Desktop

    Golden state:
    - landscape_edited.jpg exists at /home/user/Desktop/landscape_edited.jpg
    - Size: 1920x1080 (16:9 from centered crop of 1920x1200)
    - Saturation: ~1.2x of cropped original (mean HSV-S around 158 vs 136)
    - Vignette: corners are ~15-20% darker than they would be without vignette
    """
    total_score = 0.0

    edited_path = os.path.join(WORKDIR, 'landscape_edited.jpg')
    orig_path = os.path.join(WORKDIR, 'landscape.jpg')

    # Precondition: original file must exist
    if not os.path.exists(orig_path):
        print(f"CRITICAL: Original landscape.jpg not found at {orig_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: landscape_edited.jpg exists on Desktop (0.2 points)
    # This is ONLY true in golden_env (not initial_env), so it measures task completion.
    try:
        if os.path.exists(edited_path):
            print(f"PASS: Component 1 — landscape_edited.jpg exists at {edited_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — landscape_edited.jpg not found at {edited_path}")
            # No output file at all — cannot proceed with further checks
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the edited image for subsequent checks
    try:
        img_edit = Image.open(edited_path).convert("RGB")
        img_orig = Image.open(orig_path).convert("RGB")
    except Exception as e:
        print(f"CRITICAL: Cannot open image(s): {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Image cropped to 16:9 aspect ratio (0.3 points)
    # Original is 1920x1200 (non-16:9). Checklist step 1: crop to 16:9 centered.
    # Expected result: 1920x1080 (since 1920/16*9 = 1080)
    # This FAILS on initial_env (no edited file) and PASSES on golden_env.
    try:
        edit_w, edit_h = img_edit.size
        aspect_ratio = edit_w / edit_h
        expected_ratio = 16 / 9  # 1.7778

        # Check if dimensions are 1920x1080 (exact expected crop) with small tolerance
        # Also accept any 16:9 crop with tolerance of ±0.01 in ratio
        is_correct_ratio = abs(aspect_ratio - expected_ratio) < 0.01

        # Specifically check for the expected 1920x1080 dimensions (centered crop of 1920x1200)
        is_correct_size = (edit_w == 1920 and edit_h == 1080)

        # Either exact dimensions or correct ratio is acceptable
        if is_correct_size:
            print(f"PASS: Component 2 — Image is 1920x1080 (exact 16:9 centered crop) (0.3 pts)")
            total_score += 0.3
        elif is_correct_ratio:
            print(f"PASS: Component 2 — Image has 16:9 ratio ({edit_w}x{edit_h}, ratio={aspect_ratio:.4f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 16:9 ratio ({expected_ratio:.4f}), got {edit_w}x{edit_h} (ratio={aspect_ratio:.4f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Saturation increased by ~20% (0.3 points)
    # Checklist step 2: increase saturation by 20% (factor 1.2).
    # We compare the edited image's HSV saturation against the original (cropped) image.
    # The saturation mean should be at least 5% higher (lenient tolerance for JPEG compression).
    # This FAILS on initial_env (no edited file) and PASSES on golden_env.
    try:
        # Get original image saturation (using same crop as step 1 for fair comparison)
        orig_w, orig_h = img_orig.size
        # Simulate the centered 16:9 crop from original
        if orig_w == 1920 and orig_h == 1200:
            # Centered crop: top/bottom trim to get 1080 height
            crop_top = (orig_h - 1080) // 2
            img_orig_cropped = img_orig.crop((0, crop_top, orig_w, orig_h - crop_top))
        else:
            # Fallback: use the full original
            img_orig_cropped = img_orig

        orig_hsv = img_orig_cropped.convert("HSV")
        edit_hsv = img_edit.convert("HSV")
        orig_sat_mean = float(np.mean(np.array(orig_hsv.split()[1])))
        edit_sat_mean = float(np.mean(np.array(edit_hsv.split()[1])))

        sat_increase_ratio = edit_sat_mean / orig_sat_mean if orig_sat_mean > 0 else 0.0

        # The task asks for 1.2x saturation increase.
        # JPEG compression can shift this slightly, so we accept >= 1.05x (5% increase minimum).
        # A properly enhanced image should be around 1.15-1.20x.
        if sat_increase_ratio >= 1.05:
            print(f"PASS: Component 3 — Saturation increased by {sat_increase_ratio:.4f}x "
                  f"(orig={orig_sat_mean:.2f}, edited={edit_sat_mean:.2f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Saturation not sufficiently increased: "
                  f"ratio={sat_increase_ratio:.4f} (orig={orig_sat_mean:.2f}, edited={edit_sat_mean:.2f}), "
                  f"need >= 1.05x")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Vignette effect applied (0.2 points)
    # Checklist step 3: darken edges with a gradual circular fade to black.
    # We verify this by comparing corners vs center in the edited image RELATIVE to
    # what they would look like in the sat-enhanced-only version.
    # Vignette means: edited_corner_brightness < sat_enhanced_corner_brightness
    # while center brightness remains approximately unchanged.
    # This FAILS on initial_env (no edited file) and PASSES on golden_env.
    try:
        # Simulate sat-enhanced without vignette (for comparison)
        if orig_w == 1920 and orig_h == 1200:
            crop_top = (orig_h - 1080) // 2
            img_cropped_for_sat = img_orig.crop((0, crop_top, orig_w, orig_h - crop_top))
        else:
            img_cropped_for_sat = img_orig

        enhancer = ImageEnhance.Color(img_cropped_for_sat)
        sat_enhanced_only = enhancer.enhance(1.2)

        edit_arr = np.array(img_edit, dtype=float)
        sat_arr = np.array(sat_enhanced_only, dtype=float)
        h_e, w_e = edit_arr.shape[:2]

        # Must be same size for comparison
        if edit_arr.shape != sat_arr.shape:
            print(f"WARN: Component 4 — Shape mismatch: edited={edit_arr.shape} vs sat_only={sat_arr.shape}, skipping vignette check")
        else:
            # Corner regions (10% of dimensions)
            corner_h = max(1, h_e // 10)
            corner_w = max(1, w_e // 10)
            center_h_slice = slice(h_e // 3, 2 * h_e // 3)
            center_w_slice = slice(w_e // 3, 2 * w_e // 3)

            # Ratio = edited / sat_enhanced for corners and center
            # Vignette: corners should be dimmer (ratio < 1) compared to sat_enhanced_only
            # Center: approximately unchanged (ratio ~1.0)
            corners_edit = np.mean([
                np.mean(edit_arr[:corner_h, :corner_w]),
                np.mean(edit_arr[:corner_h, -corner_w:]),
                np.mean(edit_arr[-corner_h:, :corner_w]),
                np.mean(edit_arr[-corner_h:, -corner_w:])
            ])
            corners_sat = np.mean([
                np.mean(sat_arr[:corner_h, :corner_w]),
                np.mean(sat_arr[:corner_h, -corner_w:]),
                np.mean(sat_arr[-corner_h:, :corner_w]),
                np.mean(sat_arr[-corner_h:, -corner_w:])
            ])
            center_edit = np.mean(edit_arr[center_h_slice, center_w_slice])
            center_sat = np.mean(sat_arr[center_h_slice, center_w_slice])

            corner_ratio = corners_edit / corners_sat if corners_sat > 0 else 1.0
            center_ratio = center_edit / center_sat if center_sat > 0 else 1.0

            # Vignette criteria:
            # 1. Corner ratio < 0.95 (corners are at least 5% darker than sat-only)
            # 2. Center ratio > 0.95 (center is mostly unchanged, within 5%)
            vignette_at_corners = corner_ratio < 0.95
            center_preserved = center_ratio > 0.95

            if vignette_at_corners and center_preserved:
                print(f"PASS: Component 4 — Vignette detected: corner_ratio={corner_ratio:.4f} "
                      f"(< 0.95), center_ratio={center_ratio:.4f} (> 0.95) (0.2 pts)")
                total_score += 0.2
            elif vignette_at_corners and not center_preserved:
                print(f"FAIL: Component 4 — Corners darkened (corner_ratio={corner_ratio:.4f}) "
                      f"but center also affected (center_ratio={center_ratio:.4f}), vignette not pure")
            else:
                print(f"FAIL: Component 4 — Vignette not detected: corner_ratio={corner_ratio:.4f} "
                      f"(need < 0.95), center_ratio={center_ratio:.4f}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
