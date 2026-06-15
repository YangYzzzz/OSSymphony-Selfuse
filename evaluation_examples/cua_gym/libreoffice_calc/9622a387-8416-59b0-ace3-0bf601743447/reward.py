"""
Reward Script: Divide timeline.png into three equal vertical slices and sort by blue channel average (descending)
Task ID: osworld_multi_apps_gimp_os_027
Domain: gimp / os (image manipulation via terminal + Pillow)
Scoring:
  - Component 1 (0.25): timeline_sorted.png exists on Desktop with correct 900x300 dimensions
  - Component 2 (0.35): Slices are sorted in strictly descending order by average blue channel value
  - Component 3 (0.40): Each output slice's blue average matches one of the three original source
                        slice blue averages (preserving pixel data from original, no duplication)
Total: 1.0

Note: The original timeline.png has slices with blue averages approximately:
  Slice 0: 43.12  (least blue)
  Slice 1: 92.77  (medium blue)
  Slice 2: 210.94 (most blue)
  => Expected sorted order: [210.94, 92.77, 43.12]
"""

import os

# All execution happens on the VM; paths are VM-side.
WORKDIR = '/home/user/Desktop'

OUTPUT_FILE = os.path.join(WORKDIR, 'timeline_sorted.png')

# Known blue channel averages of the three original slices from timeline.png
# (established during reward design via exploration of initial_env)
# These are used to verify that the sorted image uses the ORIGINAL pixel data.
ORIGINAL_SLICE_BLUE_AVGS = [43.1163, 92.7657, 210.9371]  # sorted ascending
EXPECTED_SORTED_BLUE_AVGS = [210.9371, 92.7657, 43.1163]  # expected: descending

# Tolerance for floating-point comparison of blue channel averages
BLUE_AVG_TOLERANCE = 2.0  # allow small PNG compression rounding


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task asks to:
      1. Load 'timeline.png' (900x300) from the Desktop
      2. Split it into 3 equal vertical slices (each 300x300)
      3. Sort the slices by average blue channel value, highest first
      4. Save as 'timeline_sorted.png' on the Desktop
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Precondition gate: import libraries
    # -------------------------------------------------------------------------
    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"CRITICAL: Missing required library: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Output file exists with correct dimensions (0.25 points)
    # FAILS on initial_env (file absent), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        if not os.path.isfile(OUTPUT_FILE):
            print(f"FAIL: Component 1 — 'timeline_sorted.png' not found at {OUTPUT_FILE}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        img_out = Image.open(OUTPUT_FILE).convert('RGB')
        out_w, out_h = img_out.size  # (width, height)

        if out_w == 900 and out_h == 300:
            print(f"PASS: Component 1 — timeline_sorted.png exists with correct size {img_out.size} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — timeline_sorted.png has wrong size {img_out.size}, expected (900, 300)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: The three slices are ordered in descending blue channel avg
    #              (most blue on the left, least blue on the right) (0.35 points)
    # FAILS on initial_env (file absent), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        from PIL import Image
        import numpy as np
        img_out = Image.open(OUTPUT_FILE).convert('RGB')
        arr_out = np.array(img_out)

        out_w = arr_out.shape[1]
        slice_w = out_w // 3

        blue_avgs = []
        for i in range(3):
            s = arr_out[:, i * slice_w:(i + 1) * slice_w, :]
            blue_avgs.append(float(s[:, :, 2].mean()))

        print(f"INFO: Blue channel averages per slice [left, mid, right]: "
              f"{[round(b, 4) for b in blue_avgs]}")

        # Check strict descending order: slice0 > slice1 > slice2
        # (use >= to handle edge case of equal-blue slices)
        is_descending = (blue_avgs[0] >= blue_avgs[1]) and (blue_avgs[1] >= blue_avgs[2])

        if is_descending:
            print(f"PASS: Component 2 — Slices sorted descending by blue avg "
                  f"({blue_avgs[0]:.4f} >= {blue_avgs[1]:.4f} >= {blue_avgs[2]:.4f}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Slices NOT in descending blue order: {blue_avgs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Each output slice's blue channel average matches one of the
    #              known original slice blue averages (within tolerance).
    #              This verifies pixel content is from timeline.png (not fabricated),
    #              and that all three distinct slices are present (no duplication).
    #              (0.40 points)
    # FAILS on initial_env (file absent), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        from PIL import Image
        import numpy as np
        img_out = Image.open(OUTPUT_FILE).convert('RGB')
        arr_out = np.array(img_out)

        out_w = arr_out.shape[1]
        slice_w = out_w // 3

        output_blue_avgs = []
        for i in range(3):
            s = arr_out[:, i * slice_w:(i + 1) * slice_w, :]
            output_blue_avgs.append(float(s[:, :, 2].mean()))

        # Check that each output slice matches exactly one of the original slice blue avgs
        orig_avgs_remaining = list(ORIGINAL_SLICE_BLUE_AVGS)
        mismatch_count = 0
        matched_count = 0

        for oi, ob in enumerate(output_blue_avgs):
            # Find the closest original slice by blue average
            best_diff = float('inf')
            best_idx = -1
            for idx, orig_b in enumerate(orig_avgs_remaining):
                diff = abs(ob - orig_b)
                if diff < best_diff:
                    best_diff = diff
                    best_idx = idx

            if best_diff <= BLUE_AVG_TOLERANCE:
                matched_val = orig_avgs_remaining.pop(best_idx)
                matched_count += 1
                print(f"INFO: Output slice {oi} blue_avg={ob:.4f} matches original "
                      f"slice blue_avg={matched_val:.4f} (diff={best_diff:.4f})")
            else:
                mismatch_count += 1
                print(f"FAIL: Output slice {oi} blue_avg={ob:.4f} does not match any "
                      f"original slice (closest diff={best_diff:.4f}, tolerance={BLUE_AVG_TOLERANCE})")

        if mismatch_count == 0 and matched_count == 3 and len(orig_avgs_remaining) == 0:
            print(f"PASS: Component 3 — All 3 output slices match unique original slices "
                  f"(no duplication, correct pixel data from timeline.png) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 3 — matched_count={matched_count}/3, mismatch_count={mismatch_count}, "
                  f"unmatched_orig_avgs={orig_avgs_remaining}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Final score
    # -------------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
