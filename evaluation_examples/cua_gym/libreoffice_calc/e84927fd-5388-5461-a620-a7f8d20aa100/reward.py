"""
Reward Script: Remove green-screen background from avatar.png using GIMP and write a Python script
Task ID: osworld_multi_apps_gimp_vscode_004
Domain: multi_apps (GIMP + VSCode)

Scoring rubric (sums to 1.0):
  Component 1 — avatar_cutout.png exists and is RGBA                    (0.2 pts)
  Component 2 — avatar_cutout.png has substantial transparent area       (0.3 pts)
  Component 3 — extract_avatar.py contains functional background removal (0.2 pts)
  Component 4 — avatar_code.png exists and matches avatar_cutout.png     (0.3 pts)
"""

import os
from PIL import Image, ImageChops
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_004'

# Expected pixel counts from golden exploration
TOTAL_PIXELS = 256 * 256  # 65536
MIN_TRANSPARENT_RATIO = 0.30  # at least 30% of pixels transparent (green bg removed)

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    cutout_path = os.path.join(WORKDIR, 'avatar_cutout.png')
    code_path   = os.path.join(WORKDIR, 'avatar_code.png')
    script_path = os.path.join(WORKDIR, 'extract_avatar.py')

    # ===========================================================
    # Component 1: avatar_cutout.png exists and has RGBA mode (0.2 pts)
    # This FAILS on initial (file doesn't exist) → PASSES on golden
    # ===========================================================
    try:
        if not os.path.isfile(cutout_path):
            print(f"FAIL: Component 1 — avatar_cutout.png not found at {cutout_path}")
        else:
            img_cutout = Image.open(cutout_path)
            if img_cutout.mode == 'RGBA':
                print(f"PASS: Component 1 — avatar_cutout.png exists with RGBA mode (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — avatar_cutout.png mode is '{img_cutout.mode}', expected 'RGBA' (no alpha channel = no transparency)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ===========================================================
    # Component 2: avatar_cutout.png has substantial transparent area (0.3 pts)
    # Green background (~43091 / 65536 ≈ 66% pixels) should be transparent.
    # We use MIN_TRANSPARENT_RATIO=0.30 as a lenient threshold.
    # This FAILS on initial (file absent) → PASSES on golden
    # ===========================================================
    try:
        if not os.path.isfile(cutout_path):
            print(f"FAIL: Component 2 — avatar_cutout.png not found, skipping transparency check")
        else:
            img_cutout = Image.open(cutout_path).convert('RGBA')
            arr = np.array(img_cutout)
            alpha = arr[:, :, 3]
            transparent_pixels = int(np.sum(alpha == 0))
            transparent_ratio  = transparent_pixels / TOTAL_PIXELS
            if transparent_ratio >= MIN_TRANSPARENT_RATIO:
                print(f"PASS: Component 2 — {transparent_pixels}/{TOTAL_PIXELS} pixels transparent"
                      f" ({transparent_ratio:.1%} >= {MIN_TRANSPARENT_RATIO:.0%} threshold) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — only {transparent_pixels}/{TOTAL_PIXELS} pixels transparent"
                      f" ({transparent_ratio:.1%} < {MIN_TRANSPARENT_RATIO:.0%} threshold)"
                      " — green background may not have been removed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ===========================================================
    # Component 3: extract_avatar.py is non-trivial functional script (0.2 pts)
    # Must contain: real code (>200 chars), PIL import, numpy import,
    # and reference to output avatar_code.png.
    # This FAILS on initial (file is a 1-line comment stub) → PASSES on golden
    # ===========================================================
    try:
        if not os.path.isfile(script_path):
            print(f"FAIL: Component 3 — extract_avatar.py not found at {script_path}")
        else:
            content = open(script_path, 'r').read()
            has_substance = len(content) > 200
            has_pil       = ('from PIL' in content or 'import PIL' in content)
            has_numpy     = ('import numpy' in content or 'import np' in content)
            has_output    = 'avatar_code.png' in content

            checks = {
                'substantial code (>200 chars)': has_substance,
                'PIL/Pillow import': has_pil,
                'numpy import': has_numpy,
                'avatar_code.png output': has_output,
            }
            passed = [k for k, v in checks.items() if v]
            failed = [k for k, v in checks.items() if not v]

            if len(failed) == 0:
                print(f"PASS: Component 3 — extract_avatar.py has all required elements: {passed} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — extract_avatar.py missing: {failed}; present: {passed}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ===========================================================
    # Component 4: avatar_code.png exists and pixel-matches avatar_cutout.png (0.3 pts)
    # The script output must match the manually-created cutout.
    # This FAILS on initial (avatar_code.png absent) → PASSES on golden
    # ===========================================================
    try:
        if not os.path.isfile(code_path):
            print(f"FAIL: Component 4 — avatar_code.png not found at {code_path}")
        elif not os.path.isfile(cutout_path):
            print(f"FAIL: Component 4 — avatar_cutout.png not found, cannot compare")
        else:
            img_code   = Image.open(code_path).convert('RGBA')
            img_cutout = Image.open(cutout_path).convert('RGBA')

            # Verify sizes match
            if img_code.size != img_cutout.size:
                print(f"FAIL: Component 4 — size mismatch: avatar_code.png {img_code.size} vs avatar_cutout.png {img_cutout.size}")
            else:
                arr_code   = np.array(img_code)
                arr_cutout = np.array(img_cutout)

                # Use alpha-channel agreement as the primary metric:
                # Both should have the same transparent/opaque layout
                alpha_code   = arr_code[:, :, 3]
                alpha_cutout = arr_cutout[:, :, 3]
                alpha_agree  = np.sum((alpha_code == 0) == (alpha_cutout == 0))
                alpha_ratio  = alpha_agree / TOTAL_PIXELS

                # Also compute a pixel-level agreement on non-transparent pixels
                opaque_mask = (alpha_cutout > 0) & (alpha_code > 0)
                if opaque_mask.sum() > 0:
                    rgb_diff = np.abs(arr_code[:, :, :3].astype(np.float32) -
                                      arr_cutout[:, :, :3].astype(np.float32))
                    mse = float(np.mean(rgb_diff[opaque_mask]))
                else:
                    mse = 999.0

                if alpha_ratio >= 0.85 and mse < 30.0:
                    print(f"PASS: Component 4 — avatar_code.png matches avatar_cutout.png "
                          f"(alpha agreement: {alpha_ratio:.2%}, opaque-pixel MSE: {mse:.2f}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 4 — avatar_code.png does not match avatar_cutout.png "
                          f"(alpha agreement: {alpha_ratio:.2%}, opaque-pixel MSE: {mse:.2f})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
