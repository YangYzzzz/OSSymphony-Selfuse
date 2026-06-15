"""
Reward Script: Open logo_v2.png in GIMP, add drop shadow, save as logo_shadow_gimp.png.
              Also write logo_shadow.py that produces logo_shadow_code.png with SSIM >= 0.80.
Task ID: osworld_multi_apps_gimp_vscode_013
Domain: gimp + vscode (multi-app)
Scoring:
  Component 1: logo_shadow_gimp.png exists with drop shadow effect (0.4 pts)
               - file must be larger than original 400x200 (shadow adds margin)
               - must have more non-white pixels than original (shadow darkens)
  Component 2: logo_shadow.py exists and is a valid Python script (0.2 pts)
               - file must exist and be parseable as Python
  Component 3: logo_shadow_code.png exists and matches logo_shadow_gimp.png SSIM >= 0.80 (0.4 pts)
               - both images must exist
               - SSIM between them must be >= 0.80
"""

import os
import ast

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_013'

ORIG_PATH = os.path.join(WORKDIR, 'logo_v2.png')
GIMP_OUT  = os.path.join(WORKDIR, 'logo_shadow_gimp.png')
CODE_OUT  = os.path.join(WORKDIR, 'logo_shadow_code.png')
SCRIPT    = os.path.join(WORKDIR, 'logo_shadow.py')

# Original image dimensions per task context
ORIG_WIDTH  = 400
ORIG_HEIGHT = 200


def check_gimp_shadow():
    """
    Returns (passed: bool, detail: str)
    Checks that logo_shadow_gimp.png:
    - exists and can be opened
    - has canvas larger than original 400x200 (drop shadow expands canvas)
    - has a higher fraction of non-white pixels than original (shadow darkens area)
    """
    from PIL import Image
    import numpy as np

    if not os.path.isfile(GIMP_OUT):
        return False, f"logo_shadow_gimp.png not found at {GIMP_OUT}"

    img_gimp = Image.open(GIMP_OUT).convert('RGB')
    w, h = img_gimp.size

    if not (w > ORIG_WIDTH and h > ORIG_HEIGHT):
        return False, (f"size {w}x{h} not larger than original {ORIG_WIDTH}x{ORIG_HEIGHT}; "
                       "expected canvas expansion from drop shadow margin")

    gimp_arr = np.array(img_gimp)
    non_white_gimp = float(np.sum(np.any(gimp_arr < 230, axis=2))) / (w * h)

    orig_non_white = 0.0
    if os.path.isfile(ORIG_PATH):
        img_orig = Image.open(ORIG_PATH).convert('RGB')
        orig_arr = np.array(img_orig)
        orig_non_white = float(
            np.sum(np.any(orig_arr < 230, axis=2))
        ) / (img_orig.width * img_orig.height)

    if not (non_white_gimp > orig_non_white):
        return False, (f"no additional shadow pixels detected: "
                       f"non-white fraction {non_white_gimp:.4f} not > original {orig_non_white:.4f}")

    return True, (f"size={w}x{h}, non-white={non_white_gimp:.4f} > orig={orig_non_white:.4f}")


def check_script_valid():
    """
    Returns (passed: bool, detail: str)
    Checks that logo_shadow.py exists and is syntactically valid Python.
    """
    if not os.path.isfile(SCRIPT):
        return False, f"logo_shadow.py not found at {SCRIPT}"

    with open(SCRIPT, 'r') as fh:
        source = fh.read()

    line_count = len(source.splitlines())
    try:
        ast.parse(source)
    except SyntaxError as se:
        return False, f"syntax error in logo_shadow.py: {se}"

    return True, f"{line_count} lines, valid Python syntax"


def check_ssim_match():
    """
    Returns (passed: bool, detail: str, ssim_score: float)
    Checks that logo_shadow_code.png matches logo_shadow_gimp.png with SSIM >= 0.80.
    """
    from PIL import Image
    import numpy as np

    if not os.path.isfile(CODE_OUT):
        return False, f"logo_shadow_code.png not found at {CODE_OUT}", 0.0
    if not os.path.isfile(GIMP_OUT):
        return False, "logo_shadow_gimp.png missing for comparison", 0.0

    img_gimp = Image.open(GIMP_OUT).convert('RGB')
    img_code = Image.open(CODE_OUT).convert('RGB')

    if img_code.size != img_gimp.size:
        from PIL.Image import Resampling
        img_code = img_code.resize(img_gimp.size, Resampling.LANCZOS)

    arr_gimp = np.array(img_gimp)
    arr_code = np.array(img_code)

    score_ssim = 0.0
    try:
        from skimage.metrics import structural_similarity as ssim_func
        min_dim = min(arr_gimp.shape[0], arr_gimp.shape[1])
        win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
        try:
            score_ssim = ssim_func(arr_gimp, arr_code, win_size=win_size, channel_axis=2)
        except TypeError:
            score_ssim = ssim_func(arr_gimp, arr_code, win_size=win_size, multichannel=True)
    except ImportError:
        # Fallback: normalized MSE if scikit-image unavailable
        diff = (arr_gimp.astype(float) - arr_code.astype(float)) / 255.0
        mse = float(np.mean(diff ** 2))
        score_ssim = max(0.0, 1.0 - mse * 10)

    if score_ssim >= 0.80:
        return True, f"SSIM={score_ssim:.4f} >= 0.80", score_ssim
    return False, f"SSIM={score_ssim:.4f} < 0.80", score_ssim


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------
    # Component 1: logo_shadow_gimp.png exists and shows drop shadow (0.4 pts)
    # -------------------------------------------------------------------
    try:
        passed, detail = check_gimp_shadow()
        if passed:
            print(f"PASS: Component 1 — drop shadow verified: {detail} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: logo_shadow.py exists and is valid Python (0.2 pts)
    # -------------------------------------------------------------------
    try:
        passed, detail = check_script_valid()
        if passed:
            print(f"PASS: Component 2 — script valid: {detail} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: logo_shadow_code.png matches logo_shadow_gimp.png SSIM >= 0.80 (0.4 pts)
    # -------------------------------------------------------------------
    try:
        passed, detail, _ = check_ssim_match()
        if passed:
            print(f"PASS: Component 3 — code image matches gimp image: {detail} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
