"""
Reward Script: Split sprite sheet with GIMP and write Python split script
Task ID: osworld_multi_apps_gimp_vscode_009
Domain: gimp + vscode (multi-app)
Scoring:
  Component 1 (0.40): Four enemy_0X.png files (64x64) exist and match correct crop from enemies_sheet.png (SSIM >= 0.85 each)
  Component 2 (0.20): split_sprites.py exists, is valid Python, and contains expected logic
  Component 3 (0.40): Four enemy_code_0X.png files exist and match corresponding enemy_0X.png (SSIM >= 0.85 each)
"""

import os
import ast

from PIL import Image
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_009'

SHEET_PATH = os.path.join(WORKDIR, 'enemies_sheet.png')
SSIM_THRESHOLD = 0.85


def compute_ssim(arr1, arr2):
    """Compute SSIM between two HxWx3 uint8 arrays using skimage."""
    try:
        from skimage.metrics import structural_similarity as ssim
        min_dim = min(arr1.shape[0], arr1.shape[1])
        win_size = min(7, min_dim if min_dim % 2 == 1 else min_dim - 1)
        try:
            return ssim(arr1, arr2, win_size=win_size, channel_axis=2)
        except TypeError:
            return ssim(arr1, arr2, win_size=win_size, multichannel=True)
    except ImportError:
        # Fallback: normalized cross-correlation approximation
        a1 = arr1.astype(np.float32) / 255.0
        a2 = arr2.astype(np.float32) / 255.0
        mu1, mu2 = a1.mean(), a2.mean()
        sigma1 = a1.std()
        sigma2 = a2.std()
        sigma12 = ((a1 - mu1) * (a2 - mu2)).mean()
        c1, c2 = 0.01 ** 2, 0.03 ** 2
        return float((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2) /
                     ((mu1 ** 2 + mu2 ** 2 + c1) * (sigma1 ** 2 + sigma2 ** 2 + c2)))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: the source sheet must exist
    if not os.path.exists(SHEET_PATH):
        print(f"CRITICAL: Source sheet not found: {SHEET_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sheet = Image.open(SHEET_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open enemies_sheet.png: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected crops: 2x2 grid of 64x64 sprites from a 128x128 sheet
    # Layout: enemy_01=top-left, enemy_02=top-right,
    #         enemy_03=bottom-left, enemy_04=bottom-right
    expected_crops = {
        'enemy_01.png': (0,  0,  64, 64),
        'enemy_02.png': (64, 0,  128, 64),
        'enemy_03.png': (0,  64, 64,  128),
        'enemy_04.png': (64, 64, 128, 128),
    }

    # -------------------------------------------------------------------------
    # Component 1: Four enemy_0X.png files exist and match sheet crops (0.40 pts)
    # Each sprite that passes the SSIM check contributes 0.10 pts (4 x 0.10 = 0.40)
    # -------------------------------------------------------------------------
    component1_score = 0.0
    try:
        for fname, box in expected_crops.items():
            sprite_path = os.path.join(WORKDIR, fname)
            if not os.path.exists(sprite_path):
                print(f"FAIL: Component 1 — {fname} does not exist")
                continue

            try:
                sprite = Image.open(sprite_path)
            except Exception as e:
                print(f"FAIL: Component 1 — cannot open {fname}: {e}")
                continue

            # Size check: must be 64x64
            if sprite.size != (64, 64):
                print(f"FAIL: Component 1 — {fname} size is {sprite.size}, expected (64, 64)")
                continue

            # SSIM against expected crop from sheet
            expected_crop = sheet.crop(box).convert('RGB')
            actual_rgb = sprite.convert('RGB')
            arr_exp = np.array(expected_crop)
            arr_act = np.array(actual_rgb)

            score_val = compute_ssim(arr_exp, arr_act)
            if score_val >= SSIM_THRESHOLD:
                print(f"PASS: Component 1 — {fname} SSIM={score_val:.4f} >= {SSIM_THRESHOLD} (0.10 pts)")
                component1_score += 0.10
            else:
                print(f"FAIL: Component 1 — {fname} SSIM={score_val:.4f} < {SSIM_THRESHOLD}")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    total_score += component1_score
    print(f"Component 1 subtotal: {component1_score:.2f}/0.40")

    # -------------------------------------------------------------------------
    # Component 2: split_sprites.py exists and is valid Python with correct logic (0.20 pts)
    # -------------------------------------------------------------------------
    component2_score = 0.0
    script_path = os.path.join(WORKDIR, 'split_sprites.py')
    try:
        if not os.path.exists(script_path):
            print("FAIL: Component 2 — split_sprites.py does not exist")
        else:
            with open(script_path, 'r') as f:
                content = f.read()

            # Check valid Python syntax (0.08 pts)
            syntax_ok = False
            try:
                ast.parse(content)
                syntax_ok = True
                print("PASS: Component 2 — split_sprites.py is valid Python syntax (0.08 pts)")
                component2_score += 0.08
            except SyntaxError as e:
                print(f"FAIL: Component 2 — split_sprites.py has syntax error: {e}")

            if syntax_ok:
                # Check reads enemies_sheet.png (0.04 pts)
                if 'enemies_sheet' in content:
                    print("PASS: Component 2 — script references enemies_sheet (0.04 pts)")
                    component2_score += 0.04
                else:
                    print("FAIL: Component 2 — script does not reference enemies_sheet")

                # Check saves enemy_code files (0.04 pts)
                if 'enemy_code' in content and '.save(' in content:
                    print("PASS: Component 2 — script saves enemy_code files (0.04 pts)")
                    component2_score += 0.04
                else:
                    print("FAIL: Component 2 — script does not save enemy_code files correctly")

                # Check uses crop or image splitting logic (0.04 pts)
                if 'crop' in content or 'split' in content.lower():
                    print("PASS: Component 2 — script uses crop/split logic (0.04 pts)")
                    component2_score += 0.04
                else:
                    print("FAIL: Component 2 — script lacks crop/split logic")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    total_score += component2_score
    print(f"Component 2 subtotal: {component2_score:.2f}/0.20")

    # -------------------------------------------------------------------------
    # Component 3: Four enemy_code_0X.png files match corresponding enemy_0X.png (0.40 pts)
    # Each pair that achieves SSIM >= 0.85 contributes 0.10 pts (4 x 0.10 = 0.40)
    # We compare against the expected sheet crop (source of truth), not enemy_0X.png,
    # so this independently verifies the code-generated output.
    # -------------------------------------------------------------------------
    component3_score = 0.0
    code_files = {
        'enemy_code_01.png': (0,  0,  64, 64),
        'enemy_code_02.png': (64, 0,  128, 64),
        'enemy_code_03.png': (0,  64, 64,  128),
        'enemy_code_04.png': (64, 64, 128, 128),
    }
    try:
        for fname, box in code_files.items():
            code_path = os.path.join(WORKDIR, fname)
            if not os.path.exists(code_path):
                print(f"FAIL: Component 3 — {fname} does not exist")
                continue

            try:
                code_img = Image.open(code_path)
            except Exception as e:
                print(f"FAIL: Component 3 — cannot open {fname}: {e}")
                continue

            # Size check: must be 64x64
            if code_img.size != (64, 64):
                print(f"FAIL: Component 3 — {fname} size is {code_img.size}, expected (64, 64)")
                continue

            # SSIM against expected crop from sheet
            expected_crop = sheet.crop(box).convert('RGB')
            actual_rgb = code_img.convert('RGB')
            arr_exp = np.array(expected_crop)
            arr_act = np.array(actual_rgb)

            score_val = compute_ssim(arr_exp, arr_act)
            if score_val >= SSIM_THRESHOLD:
                print(f"PASS: Component 3 — {fname} SSIM={score_val:.4f} >= {SSIM_THRESHOLD} (0.10 pts)")
                component3_score += 0.10
            else:
                print(f"FAIL: Component 3 — {fname} SSIM={score_val:.4f} < {SSIM_THRESHOLD}")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    total_score += component3_score
    print(f"Component 3 subtotal: {component3_score:.2f}/0.40")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
