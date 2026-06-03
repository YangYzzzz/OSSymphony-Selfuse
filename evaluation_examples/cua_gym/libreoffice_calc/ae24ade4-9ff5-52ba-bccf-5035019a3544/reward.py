"""
Reward Script: Split sunset.png into three equal vertical columns with progressive warm filter
Task ID: osworld_multi_apps_gimp_os_029
Domain: gimp / os (image processing via command line with Pillow)

Scoring Rubric:
  Component 1: sunset_enhanced.png exists on Desktop with correct dimensions (0.2 pts)
  Component 2: Each column has warm color profile (R > B, warm-looking) (0.2 pts)
  Component 3: Red channel increases progressively left to right (0.3 pts)
  Component 4: Blue channel decreases progressively left to right (0.3 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_029'
ENHANCED_FILE = os.path.join(WORKDIR, 'sunset_enhanced.png')
ORIGINAL_FILE = os.path.join(WORKDIR, 'sunset.png')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: output file must exist
    if not os.path.isfile(ENHANCED_FILE):
        print(f"CRITICAL: Output file not found: {ENHANCED_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Load the enhanced image
    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Required library not available: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        enhanced = Image.open(ENHANCED_FILE).convert("RGB")
        enh_width, enh_height = enhanced.size
    except Exception as e:
        print(f"CRITICAL: Cannot open enhanced image {ENHANCED_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the original for comparison
    try:
        original = Image.open(ORIGINAL_FILE).convert("RGB")
        orig_width, orig_height = original.size
    except Exception as e:
        print(f"CRITICAL: Cannot open original image {ORIGINAL_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct output file dimensions (same as original 1200x800) (0.2 pts)
    try:
        expected_width = 1200
        expected_height = 800
        if enh_width == expected_width and enh_height == expected_height:
            print(f"PASS: Component 1 — Output image has correct dimensions {enh_width}x{enh_height} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {expected_width}x{expected_height}, got {enh_width}x{enh_height}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Compute column boundaries (3 equal vertical columns)
    col_width = enh_width // 3  # should be 400 for 1200-wide image

    # Compute per-column channel means for the enhanced image
    try:
        enh_arr = np.array(enhanced)
        orig_arr = np.array(original)
        # Column boundaries: col0=[0:col_width], col1=[col_width:2*col_width], col2=[2*col_width:]
        enh_col_r = []
        enh_col_b = []
        orig_col_r = []
        orig_col_b = []
        for i in range(3):
            left = i * col_width
            right = (i + 1) * col_width if i < 2 else enh_width
            enh_col_r.append(enh_arr[:, left:right, 0].mean())
            enh_col_b.append(enh_arr[:, left:right, 2].mean())
            orig_col_r.append(orig_arr[:, left:right, 0].mean())
            orig_col_b.append(orig_arr[:, left:right, 2].mean())
    except Exception as e:
        print(f"ERROR: Column analysis failed — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    print(f"INFO: Enhanced R per column: {[round(x, 2) for x in enh_col_r]}")
    print(f"INFO: Enhanced B per column: {[round(x, 2) for x in enh_col_b]}")
    print(f"INFO: Original R per column: {[round(x, 2) for x in orig_col_r]}")
    print(f"INFO: Original B per column: {[round(x, 2) for x in orig_col_b]}")

    # Component 2: Warm color profile — all three columns have more red than blue
    # AND all columns have higher R and lower B than the original corresponding column (0.2 pts)
    try:
        warm_check = all(
            enh_col_r[i] > enh_col_b[i] and
            enh_col_r[i] > orig_col_r[i] and
            enh_col_b[i] < orig_col_b[i]
            for i in range(3)
        )
        if warm_check:
            print("PASS: Component 2 — All columns show warm filter (R > B, R boosted, B reduced) (0.2 pts)")
            total_score += 0.2
        else:
            # Report which columns failed
            for i in range(3):
                r_gt_b = enh_col_r[i] > enh_col_b[i]
                r_boosted = enh_col_r[i] > orig_col_r[i]
                b_reduced = enh_col_b[i] < orig_col_b[i]
                print(f"FAIL: Component 2 — Column {i+1}: R>B={r_gt_b}, R_boosted={r_boosted}, B_reduced={b_reduced}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Red channel increases progressively left to right (0.3 pts)
    # Each subsequent column must have strictly more red than the previous
    try:
        r_progressive = (enh_col_r[0] < enh_col_r[1]) and (enh_col_r[1] < enh_col_r[2])
        if r_progressive:
            print(f"PASS: Component 3 — Red increases progressively: {[round(x, 2) for x in enh_col_r]} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Red does NOT increase progressively: {[round(x, 2) for x in enh_col_r]}")
            print(f"      Expected: col1 < col2 < col3 (left=mild, center=moderate, right=strong)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Blue channel decreases progressively left to right (0.3 pts)
    # Each subsequent column must have strictly less blue than the previous
    try:
        b_progressive = (enh_col_b[0] > enh_col_b[1]) and (enh_col_b[1] > enh_col_b[2])
        if b_progressive:
            print(f"PASS: Component 4 — Blue decreases progressively: {[round(x, 2) for x in enh_col_b]} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — Blue does NOT decrease progressively: {[round(x, 2) for x in enh_col_b]}")
            print(f"      Expected: col1 > col2 > col3 (left=mild, center=moderate, right=strong)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
