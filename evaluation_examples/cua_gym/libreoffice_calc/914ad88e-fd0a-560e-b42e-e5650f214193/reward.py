"""
Reward Script: Split mosaic.png into 3x3 grid and rearrange tiles in cool-to-warm hue order
Task ID: osworld_multi_apps_gimp_os_021
Domain: gimp / os
Scoring:
  - Component 1: rearranged_mosaic.png has correct dimensions (900x900) (0.2 pts)
  - Component 2: All 9 original tiles are present in the rearranged image (0.3 pts)
  - Component 3: Tiles are sorted in hue order (cool-to-warm = descending hue) (0.5 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_021'

ORIGINAL_PATH = f'{WORKDIR}/mosaic.png'
RESULT_PATH = f'{WORKDIR}/rearranged_mosaic.png'


def get_tile_avg_hue(tile_arr):
    """
    Compute average hue of a tile image array (float32, 0-1 range, HxWx3 RGB).
    Only considers pixels with saturation > 0.1 to avoid grey/white pixels.
    Returns float hue in [0, 1].
    """
    import colorsys
    hues = []
    for row in tile_arr:
        for px in row:
            r, g, b = float(px[0]), float(px[1]), float(px[2])
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            if s > 0.1:
                hues.append(h)
    if not hues:
        return 0.0
    import numpy as np
    return float(np.mean(hues))


def verify_task():
    """
    Verify that rearranged_mosaic.png exists on the Desktop and:
    1. Has the correct 900x900 dimensions
    2. Contains all 9 tiles from the original mosaic
    3. Tiles are arranged in cool-to-warm hue order (descending hue, reading order)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: result file must exist
    if not os.path.isfile(RESULT_PATH):
        print(f"FAIL: rearranged_mosaic.png not found at {RESULT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: original mosaic must exist for tile extraction
    if not os.path.isfile(ORIGINAL_PATH):
        print(f"FAIL: mosaic.png not found at {ORIGINAL_PATH} — cannot verify")
        print("REWARD: 0.0")
        return 0.0

    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Cannot import required libraries: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load both images
    try:
        orig_img = Image.open(ORIGINAL_PATH).convert('RGB')
        result_img = Image.open(RESULT_PATH).convert('RGB')
    except Exception as e:
        print(f"CRITICAL: Cannot open image files: {e}")
        print("REWARD: 0.0")
        return 0.0

    orig_w, orig_h = orig_img.size
    result_w, result_h = result_img.size

    # Component 1: rearranged_mosaic.png has correct 900x900 dimensions (0.2 pts)
    try:
        expected_w, expected_h = orig_w, orig_h  # same dimensions as original
        if result_w == expected_w and result_h == expected_h:
            print(f"PASS: Component 1 — rearranged_mosaic.png is {result_w}x{result_h} (correct) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected {expected_w}x{expected_h}, found {result_w}x{result_h}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract tiles from original and result
    tile_w = orig_w // 3
    tile_h = orig_h // 3

    try:
        orig_arr = np.array(orig_img, dtype=np.float32) / 255.0
        result_arr = np.array(result_img, dtype=np.float32) / 255.0
    except Exception as e:
        print(f"CRITICAL: Cannot convert images to numpy arrays: {e}")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Extract all 9 tiles from original and compute their hues
    orig_tiles = []
    try:
        for row in range(3):
            for col in range(3):
                y0 = row * tile_h
                x0 = col * tile_w
                tile = orig_arr[y0:y0+tile_h, x0:x0+tile_w, :]
                avg_hue = get_tile_avg_hue(tile)
                orig_tiles.append((row, col, tile, avg_hue))
    except Exception as e:
        print(f"ERROR: Could not extract original tiles: {e}")

    # Extract all 9 tiles from result and compute their hues
    result_tiles = []
    try:
        for row in range(3):
            for col in range(3):
                y0 = row * tile_h
                x0 = col * tile_w
                tile = result_arr[y0:y0+tile_h, x0:x0+tile_w, :]
                avg_hue = get_tile_avg_hue(tile)
                result_tiles.append((row, col, tile, avg_hue))
    except Exception as e:
        print(f"ERROR: Could not extract result tiles: {e}")

    # Component 2: All 9 original tiles are present in the rearranged image (0.3 pts)
    # For each original tile, check that there is a matching tile in the result
    # (matching = same pixel content, pixel-wise MSE < threshold)
    try:
        mse_threshold = 0.001  # very tight: tiles should be pixel-identical
        matched_count = 0
        for orig_row, orig_col, orig_tile, orig_hue in orig_tiles:
            best_mse = float('inf')
            for res_row, res_col, res_tile, res_hue in result_tiles:
                if orig_tile.shape == res_tile.shape:
                    mse = float(np.mean((orig_tile - res_tile) ** 2))
                    if mse < best_mse:
                        best_mse = mse
            if best_mse <= mse_threshold:
                matched_count += 1

        if matched_count == 9:
            print(f"PASS: Component 2 — all 9 original tiles found in rearranged image (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — only {matched_count}/9 original tiles found in rearranged image")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Tiles are sorted in cool-to-warm hue order (descending hue, reading order) (0.5 pts)
    # Cool colors (blues/purples) have high hue values (~0.5-0.8)
    # Warm colors (reds/oranges) have low hue values (~0.0-0.15)
    # So cool-to-warm = descending hue order
    try:
        result_hues = [t[3] for t in result_tiles]  # reading order hues

        # Check that hues are monotonically non-increasing (descending)
        is_sorted_desc = all(result_hues[i] >= result_hues[i+1] for i in range(len(result_hues)-1))

        if is_sorted_desc:
            print(f"PASS: Component 3 — tiles are in cool-to-warm hue order (descending) {[round(h, 3) for h in result_hues]} (0.5 pts)")
            total_score += 0.5
        else:
            # Partial credit: check how many consecutive pairs are in correct order
            correct_pairs = sum(1 for i in range(len(result_hues)-1) if result_hues[i] >= result_hues[i+1])
            print(f"FAIL: Component 3 — tiles NOT in correct hue order. Got {[round(h, 3) for h in result_hues]}. {correct_pairs}/8 consecutive pairs correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
