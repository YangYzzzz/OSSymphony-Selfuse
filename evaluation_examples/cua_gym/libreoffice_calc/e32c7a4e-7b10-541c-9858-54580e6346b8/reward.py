"""
Reward Script: GIMP background removal + Pillow extract_coin.py
Task ID: osworld_multi_apps_gimp_vscode_005
Domain: gimp / vscode (multi-app)
Scoring:
  Component 1 (0.35): coin_gimp.png exists with RGBA mode and transparent (black-removed) background
  Component 2 (0.30): extract_coin.py exists, uses Pillow, and produces coin_code.png
  Component 3 (0.20): coin_code.png exists with RGBA mode and transparent (black-removed) background
  Component 4 (0.15): SSIM between coin_gimp.png and coin_code.png >= 0.85
"""

import os
import sys

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_005'

COIN_SPRITE = os.path.join(WORKDIR, 'coin_sprite.png')
COIN_GIMP = os.path.join(WORKDIR, 'coin_gimp.png')
COIN_CODE = os.path.join(WORKDIR, 'coin_code.png')
EXTRACT_SCRIPT = os.path.join(WORKDIR, 'extract_coin.py')

# Try to import required libraries
try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("CRITICAL: PIL or numpy not available")
    print("REWARD: 0.0")
    sys.exit(0)


def has_transparent_background(img_path, black_threshold=50):
    """
    Check that an image has RGBA mode and that pixels which were black
    in the original coin_sprite.png are now transparent (alpha == 0).
    Returns (bool, details_str)
    """
    try:
        img = Image.open(img_path)
        if img.mode != 'RGBA':
            return False, f"mode is {img.mode}, expected RGBA"
        arr = np.array(img)
        alpha = arr[:, :, 3]
        # Count transparent pixels
        transparent_count = int(np.sum(alpha == 0))
        opaque_count = int(np.sum(alpha > 0))
        total = arr.shape[0] * arr.shape[1]
        # The original coin_sprite.png is 128x128 with a black background
        # We expect a significant number of transparent pixels (background was black)
        # Original dark pixels (all channels < black_threshold) in coin_sprite
        if os.path.exists(COIN_SPRITE):
            orig = Image.open(COIN_SPRITE).convert('RGB')
            orig_arr = np.array(orig)
            dark_mask = (
                (orig_arr[:, :, 0].astype(int) < black_threshold) &
                (orig_arr[:, :, 1].astype(int) < black_threshold) &
                (orig_arr[:, :, 2].astype(int) < black_threshold)
            )
            dark_in_orig = int(np.sum(dark_mask))
            # Check that transparent pixels in output correspond to dark pixels in original
            # At least 50% of the dark pixels in the original should now be transparent
            if dark_in_orig > 0 and transparent_count >= dark_in_orig * 0.5:
                return True, (f"RGBA, transparent={transparent_count}, "
                              f"orig_dark={dark_in_orig}, opaque={opaque_count}")
            else:
                return False, (f"Not enough background removal: "
                               f"transparent={transparent_count} vs dark_in_orig={dark_in_orig}")
        else:
            # Fallback: just check there are some transparent pixels (at least 30% of image)
            if transparent_count >= total * 0.3:
                return True, f"RGBA, transparent={transparent_count}/{total}"
            else:
                return False, f"Too few transparent pixels: {transparent_count}/{total}"
    except Exception as e:
        return False, str(e)


def compute_ssim_simple(img1_path, img2_path):
    """
    Compute SSIM between two images using scikit-image if available,
    or fall back to a simplified structural comparison using numpy.
    """
    try:
        from skimage.metrics import structural_similarity as ssim
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')
        if img1.size != img2.size:
            img1 = img1.resize(img2.size, Image.LANCZOS)
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        min_dim = min(arr1.shape[0], arr1.shape[1])
        win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
        try:
            score = ssim(arr1, arr2, win_size=win_size, channel_axis=2)
        except TypeError:
            score = ssim(arr1, arr2, win_size=win_size, multichannel=True)
        return float(score), 'skimage'
    except ImportError:
        # Fallback: use normalized cross-correlation as a proxy for structural similarity
        try:
            img1 = Image.open(img1_path).convert('L')
            img2 = Image.open(img2_path).convert('L')
            if img1.size != img2.size:
                img1 = img1.resize(img2.size, Image.LANCZOS)
            a1 = np.array(img1, dtype=np.float64)
            a2 = np.array(img2, dtype=np.float64)
            # Normalize
            a1 = (a1 - a1.mean()) / (a1.std() + 1e-8)
            a2 = (a2 - a2.mean()) / (a2.std() + 1e-8)
            ncc = float(np.mean(a1 * a2))
            # NCC in [-1, 1], convert to [0, 1]
            score = (ncc + 1.0) / 2.0
            return score, 'ncc_fallback'
        except Exception as e:
            return 0.0, f'error: {e}'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: coin_sprite.png must exist (it was on the Desktop initially)
    if not os.path.exists(COIN_SPRITE):
        print(f"PRECONDITION FAIL: coin_sprite.png not found at {COIN_SPRITE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: coin_gimp.png exists with RGBA mode and transparent black-background removed (0.35 points)
    try:
        if not os.path.exists(COIN_GIMP):
            print(f"FAIL: Component 1 — coin_gimp.png not found at {COIN_GIMP}")
        else:
            ok, details = has_transparent_background(COIN_GIMP)
            if ok:
                print(f"PASS: Component 1 — coin_gimp.png has transparent background ({details}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — coin_gimp.png background not properly removed: {details}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: extract_coin.py exists and contains Pillow-based background removal code (0.30 points)
    try:
        if not os.path.exists(EXTRACT_SCRIPT):
            print(f"FAIL: Component 2 — extract_coin.py not found at {EXTRACT_SCRIPT}")
        else:
            with open(EXTRACT_SCRIPT, 'r') as f:
                script_content = f.read()
            # Check for required elements: Pillow (PIL), image open/save, coin_code.png reference
            has_pil = 'PIL' in script_content or 'pillow' in script_content.lower()
            has_image = 'Image' in script_content
            has_output = 'coin_code.png' in script_content
            has_save = '.save(' in script_content or 'save(' in script_content
            # Check for background-removal logic: should be manipulating pixels/arrays
            has_alpha = ('RGBA' in script_content or 'alpha' in script_content.lower() or
                         'transparent' in script_content.lower() or 'mask' in script_content.lower() or
                         'numpy' in script_content or 'np.' in script_content)
            if has_pil and has_image and has_output and has_save and has_alpha:
                print(f"PASS: Component 2 — extract_coin.py uses Pillow, references coin_code.png, "
                      f"contains background removal logic (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not has_pil:
                    missing.append('PIL/Pillow import')
                if not has_image:
                    missing.append('Image usage')
                if not has_output:
                    missing.append('coin_code.png reference')
                if not has_save:
                    missing.append('save() call')
                if not has_alpha:
                    missing.append('alpha/transparency manipulation')
                print(f"FAIL: Component 2 — extract_coin.py missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: coin_code.png exists with RGBA mode and transparent black-background removed (0.20 points)
    try:
        if not os.path.exists(COIN_CODE):
            print(f"FAIL: Component 3 — coin_code.png not found at {COIN_CODE}")
        else:
            ok, details = has_transparent_background(COIN_CODE)
            if ok:
                print(f"PASS: Component 3 — coin_code.png has transparent background ({details}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — coin_code.png background not properly removed: {details}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: SSIM between coin_gimp.png and coin_code.png >= 0.85 (0.15 points)
    # Only meaningful if both files exist and passed transparency checks
    try:
        if not os.path.exists(COIN_GIMP) or not os.path.exists(COIN_CODE):
            print("FAIL: Component 4 — one or both output images missing, cannot compute SSIM")
        else:
            score_val, method = compute_ssim_simple(COIN_GIMP, COIN_CODE)
            threshold = 0.85
            if score_val >= threshold:
                print(f"PASS: Component 4 — SSIM(coin_gimp, coin_code)={score_val:.4f} >= {threshold} "
                      f"(method: {method}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — SSIM(coin_gimp, coin_code)={score_val:.4f} < {threshold} "
                      f"(method: {method})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
