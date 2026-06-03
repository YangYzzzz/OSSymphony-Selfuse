"""
Reward Script: GIMP background removal + Python replication with robot_sprite.png
Task ID: osworld_multi_apps_gimp_vscode_012
Domain: gimp + vscode (multi-app)
Scoring:
  Component 1 (0.30): robot_gimp.png exists, is RGBA, has transparent background (>= 20% transparent pixels)
  Component 2 (0.30): robot_extract.py exists and uses numpy AND PIL/Pillow with save output
  Component 3 (0.20): robot_code.png exists, is RGBA, has transparent background (>= 20% transparent pixels)
  Component 4 (0.20): robot_gimp.png and robot_code.png are similar (>= 85% alpha channel pixel agreement)
"""

import os
import numpy as np
from PIL import Image

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_012'

ROBOT_GIMP_PATH = os.path.join(DESKTOP, 'robot_gimp.png')
ROBOT_CODE_PATH = os.path.join(DESKTOP, 'robot_code.png')
ROBOT_EXTRACT_PATH = os.path.join(DESKTOP, 'robot_extract.py')

# Minimum fraction of transparent pixels to consider background successfully removed
# The task states the robot is on a sky-blue background. In the golden output, ~70% of pixels are transparent.
# We use a lenient threshold of 20% to allow minor variations.
MIN_TRANSPARENT_FRACTION = 0.20


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: robot_gimp.png exists, is RGBA, has transparent background (0.30 points)
    # This verifies the GIMP-produced cutout. The background should be removed (transparent pixels present).
    # FAILS on initial_env (file does not exist). PASSES on golden_env.
    try:
        if not os.path.isfile(ROBOT_GIMP_PATH):
            print(f"FAIL: Component 1 — robot_gimp.png not found at {ROBOT_GIMP_PATH}")
        else:
            img_gimp = Image.open(ROBOT_GIMP_PATH)
            if img_gimp.mode != 'RGBA':
                print(f"FAIL: Component 1 — robot_gimp.png mode is {img_gimp.mode}, expected RGBA (no transparency)")
            else:
                arr = np.array(img_gimp)
                total_pixels = arr.shape[0] * arr.shape[1]
                transparent_pixels = int((arr[:, :, 3] == 0).sum())
                transparent_fraction = transparent_pixels / total_pixels
                if transparent_fraction >= MIN_TRANSPARENT_FRACTION:
                    print(f"PASS: Component 1 — robot_gimp.png is RGBA with {transparent_pixels}/{total_pixels} "
                          f"transparent pixels ({transparent_fraction:.1%}) (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 — robot_gimp.png has only {transparent_fraction:.1%} transparent pixels "
                          f"(need >= {MIN_TRANSPARENT_FRACTION:.0%}); background not sufficiently removed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: robot_extract.py exists, uses numpy AND PIL/Pillow, and saves output (0.30 points)
    # This verifies the Python script was written correctly per the task requirements.
    # FAILS on initial_env (file does not exist). PASSES on golden_env.
    try:
        if not os.path.isfile(ROBOT_EXTRACT_PATH):
            print(f"FAIL: Component 2 — robot_extract.py not found at {ROBOT_EXTRACT_PATH}")
        else:
            with open(ROBOT_EXTRACT_PATH, 'r') as f:
                script_content = f.read()
            uses_numpy = 'numpy' in script_content or 'import numpy' in script_content
            uses_pil = 'PIL' in script_content or 'from PIL' in script_content or 'import PIL' in script_content
            saves_output = '.save(' in script_content
            if uses_numpy and uses_pil and saves_output:
                print(f"PASS: Component 2 — robot_extract.py uses numpy, PIL/Pillow, and saves output (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not uses_numpy:
                    missing.append('numpy import')
                if not uses_pil:
                    missing.append('PIL/Pillow import')
                if not saves_output:
                    missing.append('.save() call')
                print(f"FAIL: Component 2 — robot_extract.py missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: robot_code.png exists, is RGBA, has transparent background (0.20 points)
    # This verifies the Python script was actually run and produced output.
    # FAILS on initial_env (file does not exist). PASSES on golden_env.
    try:
        if not os.path.isfile(ROBOT_CODE_PATH):
            print(f"FAIL: Component 3 — robot_code.png not found at {ROBOT_CODE_PATH}")
        else:
            img_code = Image.open(ROBOT_CODE_PATH)
            if img_code.mode != 'RGBA':
                print(f"FAIL: Component 3 — robot_code.png mode is {img_code.mode}, expected RGBA (no transparency)")
            else:
                arr = np.array(img_code)
                total_pixels = arr.shape[0] * arr.shape[1]
                transparent_pixels = int((arr[:, :, 3] == 0).sum())
                transparent_fraction = transparent_pixels / total_pixels
                if transparent_fraction >= MIN_TRANSPARENT_FRACTION:
                    print(f"PASS: Component 3 — robot_code.png is RGBA with {transparent_pixels}/{total_pixels} "
                          f"transparent pixels ({transparent_fraction:.1%}) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 — robot_code.png has only {transparent_fraction:.1%} transparent pixels "
                          f"(need >= {MIN_TRANSPARENT_FRACTION:.0%}); background not sufficiently removed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: robot_gimp.png and robot_code.png are visually similar (SSIM >= 0.85) (0.20 points)
    # This verifies that both extractions match each other as required by the task.
    # Uses alpha-channel pixel agreement and RGB MSE as proxy (scikit-image may not be available).
    # FAILS on initial_env (files do not exist). PASSES on golden_env.
    try:
        if not os.path.isfile(ROBOT_GIMP_PATH) or not os.path.isfile(ROBOT_CODE_PATH):
            print(f"FAIL: Component 4 — one or both output images missing; cannot compare")
        else:
            img_gimp = Image.open(ROBOT_GIMP_PATH).convert('RGBA')
            img_code = Image.open(ROBOT_CODE_PATH).convert('RGBA')

            # Resize to same size if needed (both should be 96x96 but be safe)
            if img_gimp.size != img_code.size:
                img_code = img_code.resize(img_gimp.size, Image.LANCZOS)

            arr_gimp = np.array(img_gimp, dtype=np.float32)
            arr_code = np.array(img_code, dtype=np.float32)

            # Try SSIM first
            try:
                from skimage.metrics import structural_similarity as ssim
                arr_g_rgb = arr_gimp[:, :, :3].astype(np.uint8)
                arr_c_rgb = arr_code[:, :, :3].astype(np.uint8)
                min_dim = min(arr_g_rgb.shape[0], arr_g_rgb.shape[1])
                win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
                try:
                    score_val = ssim(arr_g_rgb, arr_c_rgb, win_size=win_size, channel_axis=2)
                except TypeError:
                    score_val = ssim(arr_g_rgb, arr_c_rgb, win_size=win_size, multichannel=True)
                similarity_method = 'SSIM'
                similarity_value = float(score_val)
                threshold = 0.85
            except ImportError:
                # Fallback: use pixel-level agreement on alpha channel + RGB MSE for non-transparent pixels
                alpha_gimp = arr_gimp[:, :, 3]
                alpha_code = arr_code[:, :, 3]
                transparent_gimp = (alpha_gimp == 0)
                transparent_code = (alpha_code == 0)
                # Agreement rate: fraction of pixels where both agree on transparency
                alpha_agreement = float(np.mean(transparent_gimp == transparent_code))

                # For non-transparent pixels in both, compute normalized RGB MSE
                non_transparent = (~transparent_gimp) & (~transparent_code)
                if non_transparent.sum() > 0:
                    rgb_gimp = arr_gimp[:, :, :3][non_transparent] / 255.0
                    rgb_code = arr_code[:, :, :3][non_transparent] / 255.0
                    rgb_mse = float(np.mean((rgb_gimp - rgb_code) ** 2))
                    rgb_similarity = max(0.0, 1.0 - rgb_mse * 10)  # scale MSE to 0-1 range
                else:
                    rgb_similarity = 1.0

                # Combined score: average of alpha agreement and RGB similarity
                similarity_value = (alpha_agreement + rgb_similarity) / 2.0
                similarity_method = 'alpha+RGB agreement'
                threshold = 0.85

            if similarity_value >= threshold:
                print(f"PASS: Component 4 — robot_gimp.png and robot_code.png are similar "
                      f"({similarity_method}={similarity_value:.3f} >= {threshold}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — robot_gimp.png and robot_code.png differ too much "
                      f"({similarity_method}={similarity_value:.3f} < {threshold})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
