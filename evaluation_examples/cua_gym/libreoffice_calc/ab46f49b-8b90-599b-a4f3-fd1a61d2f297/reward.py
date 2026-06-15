"""
Reward Script: Remove light-grey background from map_sprite.png using GIMP and Python script.
Task ID: osworld_multi_apps_gimp_vscode_007
Domain: gimp + vscode (multi-app)
Scoring:
  Component 1: map_sprite_gimp.png exists with transparent background (RGBA, >20% transparent pixels) — 0.35 pts
  Component 2: clean_markers.py exists as a valid Python script — 0.30 pts
  Component 3: map_sprite_code.png exists with transparent background and SSIM >= 0.85 vs map_sprite_gimp.png — 0.35 pts
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_007'

GIMP_OUTPUT = os.path.join(WORKDIR, 'map_sprite_gimp.png')
CODE_OUTPUT = os.path.join(WORKDIR, 'map_sprite_code.png')
SCRIPT_PATH = os.path.join(WORKDIR, 'clean_markers.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: map_sprite_gimp.png has transparent background (RGBA with > 20% transparent pixels)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        from PIL import Image
        import numpy as np

        if not os.path.isfile(GIMP_OUTPUT):
            print(f"FAIL: Component 1 — map_sprite_gimp.png not found at {GIMP_OUTPUT}")
        else:
            gimp_img = Image.open(GIMP_OUTPUT)
            if gimp_img.mode != 'RGBA':
                print(f"FAIL: Component 1 — map_sprite_gimp.png mode is {gimp_img.mode}, expected RGBA (no transparency)")
            else:
                data = np.array(gimp_img)
                alpha = data[:, :, 3]
                total_pixels = data.shape[0] * data.shape[1]
                transparent_pixels = int(np.sum(alpha == 0))
                transparency_ratio = transparent_pixels / total_pixels

                if transparency_ratio >= 0.20:
                    print(f"PASS: Component 1 — map_sprite_gimp.png has RGBA mode with {transparent_pixels}/{total_pixels} "
                          f"transparent pixels ({transparency_ratio:.1%}) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 1 — map_sprite_gimp.png has RGBA mode but only "
                          f"{transparent_pixels}/{total_pixels} transparent pixels ({transparency_ratio:.1%}), "
                          f"expected >= 20% for background removal")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: clean_markers.py exists and is a valid Python script
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print(f"FAIL: Component 2 — clean_markers.py not found at {SCRIPT_PATH}")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()

            # Validate it is a non-trivial Python script (>10 lines, contains image processing)
            lines = [l for l in script_content.splitlines() if l.strip() and not l.strip().startswith('#')]
            has_image_processing = any(
                keyword in script_content
                for keyword in ['PIL', 'Image', 'numpy', 'np.', 'png', 'PNG', 'RGBA', 'transparent', 'background']
            )
            # Compile to check for syntax errors
            syntax_error_msg = None
            try:
                compile(script_content, 'clean_markers.py', 'exec')
            except SyntaxError as se:
                syntax_error_msg = str(se)
                print(f"FAIL: Component 2 — clean_markers.py has syntax error: {se}")

            if syntax_error_msg is None and len(lines) >= 5 and has_image_processing:
                print(f"PASS: Component 2 — clean_markers.py is a valid Python image-processing script "
                      f"({len(lines)} non-comment lines) (0.30 pts)")
                total_score += 0.30
            elif syntax_error_msg is None and len(lines) >= 5:
                print(f"FAIL: Component 2 — clean_markers.py has {len(lines)} lines but does not appear "
                      f"to perform image processing (missing PIL/Image/numpy/RGBA keywords)")
            elif syntax_error_msg is not None:
                pass  # already reported
            else:
                print(f"FAIL: Component 2 — clean_markers.py too short ({len(lines)} non-comment lines)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: map_sprite_code.png exists with transparent background and SSIM >= 0.85 vs map_sprite_gimp.png
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        from PIL import Image
        import numpy as np

        if not os.path.isfile(CODE_OUTPUT):
            print(f"FAIL: Component 3 — map_sprite_code.png not found at {CODE_OUTPUT}")
        elif not os.path.isfile(GIMP_OUTPUT):
            print(f"FAIL: Component 3 — map_sprite_gimp.png not found, cannot compute SSIM")
        else:
            code_img = Image.open(CODE_OUTPUT)
            gimp_img = Image.open(GIMP_OUTPUT)

            # Check transparency in code output
            if code_img.mode != 'RGBA':
                print(f"FAIL: Component 3 — map_sprite_code.png mode is {code_img.mode}, expected RGBA")
            else:
                data = np.array(code_img)
                alpha = data[:, :, 3]
                total_pixels = data.shape[0] * data.shape[1]
                transparent_pixels = int(np.sum(alpha == 0))
                transparency_ratio = transparent_pixels / total_pixels

                if transparency_ratio < 0.20:
                    print(f"FAIL: Component 3 — map_sprite_code.png only has {transparency_ratio:.1%} "
                          f"transparent pixels, expected >= 20%")
                else:
                    # Compute SSIM between map_sprite_code and map_sprite_gimp
                    try:
                        from skimage.metrics import structural_similarity as ssim_func

                        code_rgb = code_img.convert('RGB')
                        gimp_rgb = gimp_img.convert('RGB')

                        if code_rgb.size != gimp_rgb.size:
                            from PIL.Image import Resampling
                            code_rgb = code_rgb.resize(gimp_rgb.size, Resampling.LANCZOS)

                        arr1 = np.array(code_rgb)
                        arr2 = np.array(gimp_rgb)
                        min_dim = min(arr1.shape[0], arr1.shape[1])
                        win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)

                        try:
                            score = ssim_func(arr1, arr2, win_size=win_size, channel_axis=2)
                        except TypeError:
                            score = ssim_func(arr1, arr2, win_size=win_size, multichannel=True)

                        if score >= 0.85:
                            print(f"PASS: Component 3 — map_sprite_code.png has RGBA mode, "
                                  f"{transparent_pixels}/{total_pixels} transparent pixels ({transparency_ratio:.1%}), "
                                  f"SSIM vs gimp output = {score:.4f} >= 0.85 (0.35 pts)")
                            total_score += 0.35
                        else:
                            print(f"FAIL: Component 3 — map_sprite_code.png SSIM vs map_sprite_gimp.png = "
                                  f"{score:.4f}, expected >= 0.85 (task requires SSIM >= 0.85)")

                    except ImportError:
                        # scikit-image not available — fall back to checking transparency only
                        print(f"WARN: scikit-image not available, scoring Component 3 based on transparency alone")
                        if transparency_ratio >= 0.20:
                            print(f"PASS: Component 3 (partial — no SSIM) — map_sprite_code.png has "
                                  f"{transparent_pixels}/{total_pixels} transparent pixels ({transparency_ratio:.1%}) (0.20 pts)")
                            total_score += 0.20
                        else:
                            print(f"FAIL: Component 3 — insufficient transparency")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
