"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m blending two texture layers and need the top one set to exactly 50 % opacity so it shows the base layer underneath—what’s the quickest way to do that in GIMP?
Generated: 2025-09-01 12:36:24
Status: success
Model: o3
Total Steps: 2
"""

# Reward script for verifying GIMP opacity task
# -------------------------------------------------
# Task: Ensure the top texture layer is set to exactly 50% opacity in the
#       provided XCF file.
# Verification approach:
#   1. Load the XCF with gimpformats (no filesystem searching; exact path).
#   2. Confirm there are at least two layers (base + top) – small partial credit.
#   3. Check the opacity of the topmost layer. Award the majority of points
#      if the opacity is exactly 0.5 (±0.01 tolerance).  Provide smoothly
#      decreasing partial credit if the value is close but not exact.
#   4. Print detailed diagnostics and the final reward as "REWARD: X.X".
# -------------------------------------------------

from gimpformats.gimpXcfDocument import GimpDocument
import os
import math

# 🔥 MANDATORY: Use the exact path provided in the task context
XCF_FILE_PATH = "/tmp/blend_opacity_task.xcf"

# Numeric tolerance for an "exact" 50% opacity (allows tiny rounding error)
TOLERANCE = 0.01  # ±1 %


def verify_opacity_task(file_path: str) -> float:
    """Verify that the top layer has 50% opacity.  Returns a score 0.0–1.0."""
    print(f"🎯 Verifying task using XCF file: {file_path}")
    total_score = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # Prerequisite: File must exist and load – NO points for this step
    # ------------------------------------------------------------------
    if not os.path.isfile(file_path):
        print("✗ XCF file is missing at the provided path – task failed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = GimpDocument(file_path)
        print("✓ XCF file loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load XCF file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Requirement 1: Presence of at least two layers (base + top)
    # ------------------------------------------------------------------
    layer_count = len(doc._layers)
    print(f"Layer count: {layer_count}")
    if layer_count >= 2:
        print("✓ Image contains at least two layers (required for blending)")
        total_score += 0.2  # 20 % of score
    else:
        print("✗ Less than two layers found – cannot verify blending")
        print(f"REWARD: {total_score}")
        return total_score  # Cannot proceed further

    # ------------------------------------------------------------------
    # Requirement 2: Top layer opacity is 50 %
    # ------------------------------------------------------------------
    top_layer = doc._layers[0]  # gimpformats lists top-most first
    opacity_value = top_layer.opacity  # Already 0–1 range
    print(f'Top layer "{top_layer.name}" opacity: {opacity_value}')

    diff = abs(opacity_value - 0.5)

    if diff <= TOLERANCE:
        print("✓ Top layer opacity is exactly 50% (within tolerance)")
        total_score += 0.8  # full remaining credit
    else:
        # Award partial credit if reasonably close (linear drop-off up to ±0.1)
        if diff <= 0.1:
            partial = 0.8 * (1 - diff / 0.1)
            print(f"⚠︎ Top layer opacity close to 50% – partial credit {partial:.3f}")
            total_score += partial
        else:
            print("✗ Top layer opacity far from 50% – no credit for opacity")

    # ------------------------------------------------------------------
    # Final score (clamped and rounded for neatness)
    # ------------------------------------------------------------------
    final_score = round(min(total_score, max_score), 4)
    print(f"Total score breakdown: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_opacity_task(XCF_FILE_PATH)

