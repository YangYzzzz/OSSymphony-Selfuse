"""
Reward Script: GIMP background removal + Python OpenCV script
Task ID: osworld_multi_apps_gimp_vscode_011
Domain: multi_apps (GIMP + VSCode/Python)
Scoring:
  Component 1 (0.35): product_cutout_gimp.png — RGBA image with substantial transparency
  Component 2 (0.30): product_cutout.py — Python script with OpenCV usage present
  Component 3 (0.35): product_cutout_code.png — RGBA image with SSIM >= 0.80 vs gimp cutout
"""

import os
import ast

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_011'

GIMP_OUTPUT = os.path.join(WORKDIR, 'product_cutout_gimp.png')
CODE_SCRIPT = os.path.join(WORKDIR, 'product_cutout.py')
CODE_OUTPUT = os.path.join(WORKDIR, 'product_cutout_code.png')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: product_cutout_gimp.png — RGBA image with substantial
    # transparency (>= 60% transparent pixels, indicating background removed).
    # Fails on initial_env (file doesn't exist); passes on golden_env.
    # (0.35 points)
    # -----------------------------------------------------------------------
    try:
        from PIL import Image
        import numpy as np

        if not os.path.isfile(GIMP_OUTPUT):
            print(f"FAIL: Component 1 — product_cutout_gimp.png not found at {GIMP_OUTPUT}")
        else:
            img_gimp = Image.open(GIMP_OUTPUT)
            if img_gimp.mode != 'RGBA':
                print(f"FAIL: Component 1 — product_cutout_gimp.png mode is {img_gimp.mode}, expected RGBA")
            else:
                alpha = img_gimp.split()[3]
                alpha_arr = np.array(alpha)
                total_pixels = alpha_arr.size
                transparent_pixels = int(np.sum(alpha_arr == 0))
                transparency_ratio = transparent_pixels / total_pixels
                # Also confirm there is a meaningful non-transparent region
                # (product content still present, not fully transparent)
                opaque_pixels = int(np.sum(alpha_arr > 128))
                opaque_ratio = opaque_pixels / total_pixels

                if transparency_ratio >= 0.60 and opaque_ratio >= 0.02:
                    print(f"PASS: Component 1 — product_cutout_gimp.png is RGBA with "
                          f"{transparency_ratio*100:.1f}% transparent and "
                          f"{opaque_ratio*100:.1f}% opaque pixels (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 1 — transparency={transparency_ratio*100:.1f}%, "
                          f"opaque={opaque_ratio*100:.1f}% — need >=60% transparent and >=2% opaque")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: product_cutout.py — Python script that uses cv2/OpenCV
    # to process the image. Must exist, be valid Python, and import cv2 or
    # reference OpenCV operations.
    # Fails on initial_env (file doesn't exist); passes on golden_env.
    # (0.30 points)
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(CODE_SCRIPT):
            print(f"FAIL: Component 2 — product_cutout.py not found at {CODE_SCRIPT}")
        else:
            with open(CODE_SCRIPT, 'r', encoding='utf-8', errors='replace') as f:
                script_content = f.read()

            # Verify it's valid Python syntax
            try:
                ast.parse(script_content)
                syntax_ok = True
            except SyntaxError as se:
                syntax_ok = False
                print(f"FAIL: Component 2 — product_cutout.py has syntax error: {se}")

            if syntax_ok:
                # Check it imports cv2 (OpenCV) and processes images
                uses_cv2 = 'import cv2' in script_content or 'cv2.' in script_content
                uses_numpy = 'import numpy' in script_content or 'np.' in script_content
                saves_output = 'product_cutout_code.png' in script_content or 'cv2.imwrite' in script_content

                if uses_cv2 and saves_output:
                    print(f"PASS: Component 2 — product_cutout.py is valid Python, uses OpenCV, "
                          f"references output file (0.30 pts)")
                    total_score += 0.30
                else:
                    missing = []
                    if not uses_cv2:
                        missing.append("cv2 import/usage")
                    if not saves_output:
                        missing.append("output file reference or cv2.imwrite")
                    print(f"FAIL: Component 2 — product_cutout.py missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: product_cutout_code.png — RGBA image with transparent
    # background, similar (SSIM >= 0.80) to product_cutout_gimp.png.
    # Measures that the code output matches the GIMP output structurally.
    # Fails on initial_env (file doesn't exist); passes on golden_env.
    # (0.35 points)
    # -----------------------------------------------------------------------
    try:
        from PIL import Image
        import numpy as np

        if not os.path.isfile(CODE_OUTPUT):
            print(f"FAIL: Component 3 — product_cutout_code.png not found at {CODE_OUTPUT}")
        elif not os.path.isfile(GIMP_OUTPUT):
            print(f"FAIL: Component 3 — product_cutout_gimp.png not found (needed for SSIM comparison)")
        else:
            img_code = Image.open(CODE_OUTPUT)
            img_gimp_ref = Image.open(GIMP_OUTPUT)

            if img_code.mode not in ('RGBA', 'LA', 'RGB'):
                print(f"FAIL: Component 3 — product_cutout_code.png has unexpected mode: {img_code.mode}")
            else:
                # Check code output has transparency (background removed)
                if img_code.mode in ('RGBA', 'LA'):
                    alpha_code = img_code.split()[-1]
                    alpha_code_arr = np.array(alpha_code)
                    code_transparency = int(np.sum(alpha_code_arr == 0)) / alpha_code_arr.size
                    has_transparency = code_transparency >= 0.50
                else:
                    has_transparency = False
                    code_transparency = 0.0

                # SSIM comparison between code output and GIMP output (both as RGB)
                try:
                    from skimage.metrics import structural_similarity as ssim

                    img_code_rgb = img_code.convert('RGB')
                    img_gimp_rgb = img_gimp_ref.convert('RGB')

                    # Ensure same size for SSIM
                    if img_code_rgb.size != img_gimp_rgb.size:
                        img_code_rgb = img_code_rgb.resize(img_gimp_rgb.size)

                    arr_code = np.array(img_code_rgb)
                    arr_gimp = np.array(img_gimp_rgb)

                    min_dim = min(arr_code.shape[0], arr_code.shape[1])
                    win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)

                    try:
                        ssim_score = ssim(arr_code, arr_gimp, win_size=win_size, channel_axis=2)
                    except TypeError:
                        ssim_score = ssim(arr_code, arr_gimp, win_size=win_size, multichannel=True)

                    print(f"INFO: Component 3 — SSIM(code vs gimp) = {ssim_score:.4f}, "
                          f"code transparency = {code_transparency*100:.1f}%")

                    if ssim_score >= 0.80:
                        print(f"PASS: Component 3 — product_cutout_code.png SSIM={ssim_score:.4f} >= 0.80 "
                              f"(0.35 pts)")
                        total_score += 0.35
                    else:
                        print(f"FAIL: Component 3 — SSIM={ssim_score:.4f} < 0.80 threshold")

                except ImportError:
                    # Fallback: if skimage not available, check only that code output
                    # has transparency and roughly same size as GIMP output
                    if has_transparency and img_code.size == img_gimp_ref.size:
                        print(f"PASS: Component 3 — product_cutout_code.png has RGBA with "
                              f"{code_transparency*100:.1f}% transparency and same size as GIMP output "
                              f"(SSIM skipped — skimage unavailable) (0.35 pts)")
                        total_score += 0.35
                    else:
                        print(f"FAIL: Component 3 — skimage unavailable for SSIM; "
                              f"fallback check failed (transparency={code_transparency*100:.1f}%, "
                              f"size_match={img_code.size == img_gimp_ref.size})")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
