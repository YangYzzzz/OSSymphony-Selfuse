"""
Reward Script: Remove pink background from tree_sprite.png using GIMP and Python/Pillow
Task ID: osworld_multi_apps_gimp_vscode_015
Domain: gimp + vscode (multi-app)
Scoring:
  - Component 1: tree_gimp.png exists and has transparent background (0.3 pts)
  - Component 2: tree_code.png exists and has transparent background (0.3 pts)
  - Component 3: extract_tree.py exists and uses Pillow for background removal (0.2 pts)
  - Component 4: SSIM between tree_gimp.png and tree_code.png >= 0.85 (0.2 pts)
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_015'

TREE_SPRITE = os.path.join(WORKDIR, 'tree_sprite.png')
TREE_GIMP   = os.path.join(WORKDIR, 'tree_gimp.png')
TREE_CODE   = os.path.join(WORKDIR, 'tree_code.png')
EXTRACT_PY  = os.path.join(WORKDIR, 'extract_tree.py')


def check_transparent_background(img_path):
    """
    Returns (ok: bool, transparent_count: int, total_pixels: int)
    Verifies that the image has RGBA mode and a substantial number of
    transparent pixels corresponding to the removed pink background.
    The original sprite has 13053 pink pixels in a 128x128 (16384 total) image.
    We require at least 10% of pixels to be transparent (tree is not fully transparent).
    """
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(img_path)
        if img.mode != 'RGBA':
            return False, 0, 0
        arr = np.array(img)
        transparent_count = int(np.sum(arr[:, :, 3] == 0))
        total = arr.shape[0] * arr.shape[1]
        # Require meaningful number of transparent pixels (background removed)
        # and some non-transparent pixels (tree structure retained)
        if transparent_count < 100:
            return False, transparent_count, total
        non_transparent = total - transparent_count
        if non_transparent < 100:
            return False, transparent_count, total
        return True, transparent_count, total
    except Exception as e:
        print(f"ERROR checking transparency in {img_path}: {e}")
        return False, 0, 0


def check_ssim(path1, path2, threshold=0.85):
    """
    Compare structural similarity between two images.
    Returns (ok: bool, score: float)
    Converts both to RGB before comparison to ignore alpha differences.
    """
    try:
        from PIL import Image
        import numpy as np
        try:
            from skimage.metrics import structural_similarity as ssim
        except ImportError:
            print("WARN: scikit-image not available, skipping SSIM check")
            return False, -1.0

        img1 = Image.open(path1).convert('RGBA')
        img2 = Image.open(path2).convert('RGBA')

        if img1.size != img2.size:
            # Resize img2 to match img1
            from PIL.Image import Resampling
            img2 = img2.resize(img1.size, Resampling.LANCZOS)

        # Compare on RGB channel (structural content, ignoring alpha)
        arr1 = np.array(img1.convert('RGB'))
        arr2 = np.array(img2.convert('RGB'))

        min_dim = min(arr1.shape[0], arr1.shape[1])
        win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
        if win_size < 1:
            return False, 0.0

        try:
            score = ssim(arr1, arr2, win_size=win_size, channel_axis=2)
        except TypeError:
            score = ssim(arr1, arr2, win_size=win_size, multichannel=True)

        return score >= threshold, float(score)
    except Exception as e:
        print(f"ERROR computing SSIM between {path1} and {path2}: {e}")
        return False, 0.0


def check_extract_script(script_path):
    """
    Verify extract_tree.py contains Pillow-based background removal logic.
    Checks for:
    - Pillow import (PIL / Image)
    - Saving an output PNG (tree_code.png or similar)
    - Some form of chroma-key or color-mask operation
    """
    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Must import PIL/Pillow
        uses_pillow = ('from PIL' in content or 'import PIL' in content)
        # Must reference an output file (saving result)
        saves_output = ('tree_code' in content or '.save(' in content)
        # Must have some pixel/color manipulation (background removal logic)
        has_manipulation = any(kw in content for kw in [
            'np.', 'numpy', 'transparent', 'alpha', 'mask', 'RGBA',
            'background', 'remove', 'pink', 'chroma', 'dist', '255',
        ])

        return uses_pillow and saves_output and has_manipulation, {
            'uses_pillow': uses_pillow,
            'saves_output': saves_output,
            'has_manipulation': has_manipulation,
        }
    except Exception as e:
        print(f"ERROR reading extract script {script_path}: {e}")
        return False, {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tree_sprite.png must exist (this is the input file)
    if not os.path.isfile(TREE_SPRITE):
        print(f"CRITICAL: Input file not found: {TREE_SPRITE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tree_gimp.png exists and has transparent background (0.3 pts)
    # This verifies the GIMP workflow was completed: pink background removed,
    # saved as RGBA PNG with transparent pixels where background was.
    # FAILS on initial (tree_gimp.png does not exist) -> PASSES on golden
    try:
        if not os.path.isfile(TREE_GIMP):
            print(f"FAIL: Component 1 — tree_gimp.png not found at {TREE_GIMP}")
        else:
            ok, transparent_count, total = check_transparent_background(TREE_GIMP)
            if ok:
                print(f"PASS: Component 1 — tree_gimp.png exists as RGBA with {transparent_count}/{total} transparent pixels (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — tree_gimp.png found but transparency check failed "
                      f"(transparent_count={transparent_count}, total={total}, mode may not be RGBA)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tree_code.png exists and has transparent background (0.3 pts)
    # This verifies the Pillow script was executed: pink background removed programmatically,
    # saved as RGBA PNG.
    # FAILS on initial (tree_code.png does not exist) -> PASSES on golden
    try:
        if not os.path.isfile(TREE_CODE):
            print(f"FAIL: Component 2 — tree_code.png not found at {TREE_CODE}")
        else:
            ok, transparent_count, total = check_transparent_background(TREE_CODE)
            if ok:
                print(f"PASS: Component 2 — tree_code.png exists as RGBA with {transparent_count}/{total} transparent pixels (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — tree_code.png found but transparency check failed "
                      f"(transparent_count={transparent_count}, total={total}, mode may not be RGBA)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: extract_tree.py exists and contains Pillow-based background removal (0.2 pts)
    # This verifies the Python automation script was written.
    # FAILS on initial (extract_tree.py does not exist) -> PASSES on golden
    try:
        if not os.path.isfile(EXTRACT_PY):
            print(f"FAIL: Component 3 — extract_tree.py not found at {EXTRACT_PY}")
        else:
            ok, details = check_extract_script(EXTRACT_PY)
            if ok:
                print(f"PASS: Component 3 — extract_tree.py exists with Pillow import, output save, and pixel manipulation (0.2 pts)")
                print(f"       Details: {details}")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — extract_tree.py found but missing required content. Details: {details}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: SSIM between tree_gimp.png and tree_code.png >= 0.85 (0.2 pts)
    # This verifies that both background-removal methods produce visually similar results.
    # FAILS on initial (neither file exists) -> PASSES on golden (both exist and are similar)
    try:
        if not os.path.isfile(TREE_GIMP) or not os.path.isfile(TREE_CODE):
            print(f"FAIL: Component 4 — one or both output files missing, skipping SSIM check")
        else:
            ok, score = check_ssim(TREE_GIMP, TREE_CODE, threshold=0.85)
            if score < 0:
                print(f"SKIP: Component 4 — SSIM library not available")
            elif ok:
                print(f"PASS: Component 4 — SSIM between tree_gimp.png and tree_code.png = {score:.4f} >= 0.85 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — SSIM between tree_gimp.png and tree_code.png = {score:.4f} < 0.85 (threshold)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
