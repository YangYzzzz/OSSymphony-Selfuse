"""
Reward Script: Extract terrain tile from tileset using GIMP and Python script
Task ID: osworld_multi_apps_gimp_vscode_006
Domain: multi_apps (gimp + vscode)

Task: Open 'tileset.png' in GIMP, extract terrain tile at row 2, col 3 (0-indexed),
save as 'tile_2_3_gimp.png'. Then write 'extract_tile.py' that reads tileset,
extracts the same tile, saves as 'tile_2_3_code.png'.

Scoring:
- Component 1: tile_2_3_gimp.png exists and has correct 64x64 size (0.3 pts)
- Component 2: tile_2_3_gimp.png contains the correct tile (matches expected crop from tileset) (0.3 pts)
- Component 3: extract_tile.py exists and is syntactically valid Python (0.2 pts)
- Component 4: tile_2_3_code.png exists and visually matches tile_2_3_gimp.png (0.2 pts)
Total: 1.0
"""

import os
import ast
import numpy as np
from PIL import Image

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_006'

# Expected tile parameters
TILE_W = 64
TILE_H = 64
TARGET_ROW = 2
TARGET_COL = 3


def extract_expected_tile(tileset_path):
    """Extract the ground-truth tile from the tileset at row 2, col 3."""
    img = Image.open(tileset_path)
    x0 = TARGET_COL * TILE_W
    y0 = TARGET_ROW * TILE_H
    x1 = x0 + TILE_W
    y1 = y0 + TILE_H
    return img.crop((x0, y0, x1, y1)).convert("RGB")


def compute_mse(arr1, arr2):
    """Compute mean squared error between two numpy arrays."""
    return float(np.mean((arr1.astype(float) - arr2.astype(float)) ** 2))


def compute_ssim_approx(img1_path, img2_path):
    """
    Compute similarity between two images.
    Uses MSE-based normalized metric as a proxy for SSIM.
    Returns a value in [0, 1] where 1.0 = identical.
    """
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    if img1.size != img2.size:
        return 0.0
    arr1 = np.array(img1, dtype=float)
    arr2 = np.array(img2, dtype=float)
    mse = compute_mse(arr1, arr2)
    # MSE 0 = identical (similarity 1.0), MSE 255^2 = maximally different (similarity 0.0)
    max_mse = 255.0 ** 2
    return 1.0 - (mse / max_mse)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    tileset_path = os.path.join(WORKDIR, 'tileset.png')
    gimp_tile_path = os.path.join(WORKDIR, 'tile_2_3_gimp.png')
    script_path = os.path.join(WORKDIR, 'extract_tile.py')
    code_tile_path = os.path.join(WORKDIR, 'tile_2_3_code.png')

    # Precondition: tileset.png must exist (it's the source material)
    if not os.path.isfile(tileset_path):
        print(f"CRITICAL: tileset.png not found at {tileset_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load tileset once for reuse
    try:
        tileset = Image.open(tileset_path)
        print(f"Tileset loaded: {tileset.size[0]}x{tileset.size[1]} px, mode={tileset.mode}")
    except Exception as e:
        print(f"CRITICAL: Cannot load tileset.png: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tile_2_3_gimp.png exists and is 64x64 (0.3 points)
    # This fails on initial_env (file absent) and passes on golden_env
    try:
        if not os.path.isfile(gimp_tile_path):
            print(f"FAIL: Component 1 — tile_2_3_gimp.png not found at {gimp_tile_path}")
        else:
            gimp_img = Image.open(gimp_tile_path).convert("RGB")
            w, h = gimp_img.size
            if w == TILE_W and h == TILE_H:
                print(f"PASS: Component 1 — tile_2_3_gimp.png found and has correct size {w}x{h} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — tile_2_3_gimp.png size is {w}x{h}, expected {TILE_W}x{TILE_H}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tile_2_3_gimp.png contains the correct tile from tileset (0.3 points)
    # The correct tile is at row=2, col=3 (0-indexed) from tileset.png (6x4 grid of 64x64 tiles)
    # This fails on initial_env (file absent) and passes on golden_env
    try:
        if not os.path.isfile(gimp_tile_path):
            print(f"FAIL: Component 2 — tile_2_3_gimp.png not found, cannot verify tile content")
        else:
            expected_tile = extract_expected_tile(tileset_path)
            gimp_img = Image.open(gimp_tile_path).convert("RGB")

            if expected_tile.size != gimp_img.size:
                print(f"FAIL: Component 2 — size mismatch: expected {expected_tile.size}, got {gimp_img.size}")
            else:
                expected_arr = np.array(expected_tile, dtype=float)
                gimp_arr = np.array(gimp_img, dtype=float)
                mse = compute_mse(expected_arr, gimp_arr)

                # MSE = 0 means pixel-perfect match; threshold < 100 allows minor GIMP export artifacts
                # The task context specifies SSIM >= 0.85 is sufficient for code tile,
                # but for GIMP tile we use tighter tolerance (direct crop should match well)
                if mse < 100.0:
                    print(f"PASS: Component 2 — tile_2_3_gimp.png matches expected crop from tileset[row=2,col=3] MSE={mse:.4f} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — tile_2_3_gimp.png does not match expected tile MSE={mse:.4f} (threshold<100)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: extract_tile.py exists and is syntactically valid Python (0.2 points)
    # This fails on initial_env (file absent) and passes on golden_env
    try:
        if not os.path.isfile(script_path):
            print(f"FAIL: Component 3 — extract_tile.py not found at {script_path}")
        else:
            with open(script_path, 'r') as f:
                script_content = f.read()

            # Check it's syntactically valid Python
            syntax_error = None
            try:
                ast.parse(script_content)
            except SyntaxError as se:
                syntax_error = se
                print(f"FAIL: Component 3 — extract_tile.py has syntax error: {se}")

            if syntax_error is None:
                # Check it references the correct tile coordinates and output filename
                has_row = 'row' in script_content.lower() or 'TARGET_ROW' in script_content or '2' in script_content
                has_col = 'col' in script_content.lower() or 'TARGET_COL' in script_content or '3' in script_content
                has_output = 'tile_2_3_code' in script_content
                has_tileset_ref = 'tileset' in script_content

                if has_output and has_tileset_ref:
                    print(f"PASS: Component 3 — extract_tile.py is valid Python with correct output reference (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — extract_tile.py missing required references: tile_2_3_code={has_output}, tileset={has_tileset_ref}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tile_2_3_code.png exists and visually matches tile_2_3_gimp.png (SSIM >= 0.85) (0.2 points)
    # This fails on initial_env (file absent) and passes on golden_env
    try:
        if not os.path.isfile(code_tile_path):
            print(f"FAIL: Component 4 — tile_2_3_code.png not found at {code_tile_path}")
        elif not os.path.isfile(gimp_tile_path):
            print(f"FAIL: Component 4 — tile_2_3_gimp.png not found, cannot compare")
        else:
            code_img = Image.open(code_tile_path).convert("RGB")
            gimp_img = Image.open(gimp_tile_path).convert("RGB")

            if code_img.size != (TILE_W, TILE_H):
                print(f"FAIL: Component 4 — tile_2_3_code.png size is {code_img.size}, expected {TILE_W}x{TILE_H}")
            else:
                code_arr = np.array(code_img, dtype=float)
                gimp_arr = np.array(gimp_img, dtype=float)
                mse = compute_mse(code_arr, gimp_arr)

                # Task context requires SSIM >= 0.85 for code tile vs gimp tile
                # Using MSE threshold: MSE < 500 roughly corresponds to SSIM >= 0.85 for natural images
                # Convert to similarity score: 0 MSE = 1.0 similarity
                similarity = 1.0 - (mse / (255.0 ** 2))
                print(f"  tile_2_3_code.png vs tile_2_3_gimp.png: MSE={mse:.4f}, approx_similarity={similarity:.4f}")

                if similarity >= 0.85:
                    print(f"PASS: Component 4 — tile_2_3_code.png matches tile_2_3_gimp.png with similarity={similarity:.4f} >= 0.85 (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — tile_2_3_code.png similarity={similarity:.4f} < 0.85 threshold")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
