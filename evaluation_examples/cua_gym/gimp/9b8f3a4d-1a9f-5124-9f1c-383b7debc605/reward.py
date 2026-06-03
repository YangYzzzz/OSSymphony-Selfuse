"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a folder with 120 product shots, each 2400×2400 px at 72 DPI. I need to stamp our logo (a 300×100 px PNG) onto every image—bottom-right corner, exactly 30 px from both edges, at 60 % opacity—then re-export them as JPEG (quality 85) while keeping the original filenames. What’s the fastest way to do this in GIMP?
Generated: 2025-09-01 14:05:35
Status: success
Model: o3
Total Steps: 19
"""

import os
import math
from gimpformats.gimpXcfDocument import GimpDocument

"""
Reward script for verifying the GIMP batch-logo task.

Scoring rubric (adds up to 1.0):
    0.2 – Image dimensions are exactly 2400×2400 px
    0.3 – A layer whose name contains the word "logo" exists
    0.3 – That logo layer has ~60 % opacity (±5 %)
    0.2 – Logo layer is placed on top of the layer stack

The script MUST only use the exact XCF path supplied in the task context
and must not search the file-system.
"""

# ------------------------------------------------------------------
# 🚨 CRITICAL: USE THE EXACT PATH PROVIDED IN CONTEXT – NO SEARCHING
# ------------------------------------------------------------------
XCF_PATH = "/tmp/product_logo_task.xcf"  # ← do not change or search

# ----------------------- Helper Functions -------------------------

def _find_logo_layer(layers):
    """Return the first layer whose name includes 'logo' (case-insensitive)."""
    for layer in layers:
        if "logo" in layer.name.lower():
            return layer
    return None

# ----------------------- Main Verification ------------------------

def verify_gimp_logo_task(path: str) -> float:
    """Verify completion of the logo-stamping task and return a score [0,1]."""
    max_score = 1.0
    score = 0.0

    print(f"🎯 Loading XCF from provided path: {path}")
    if not os.path.isfile(path):
        print("✗ File not found – task failed")
        return 0.0

    try:
        doc = GimpDocument(path)
        print("✓ XCF file loaded")
    except Exception as e:
        print(f"✗ Failed to load XCF: {e}")
        return 0.0

    layers = doc._layers  # list of GimpLayer objects
    layer_names = [layer.name for layer in layers]
    print(f"Found {len(layers)} layers: {layer_names}")

    # ---------- Requirement 1: Dimensions (0.2) ------------------
    if doc.width == 2400 and doc.height == 2400:
        print("✓ Image dimensions are 2400×2400 px (0.2)")
        score += 0.2
    else:
        print(f"✗ Image dimensions mismatch – got {doc.width}×{doc.height}")

    # ---------- Requirement 2: Logo layer exists (0.3) -----------
    logo_layer = _find_logo_layer(layers)
    if logo_layer is not None:
        print(f"✓ Logo layer '{logo_layer.name}' found (0.3)")
        score += 0.3
    else:
        print("✗ No logo layer found")

    # ---------- Requirement 3: Logo opacity ≈60 % (0.3) ---------
    if logo_layer is not None:
        opacity_val = logo_layer.opacity  # observed as 0-1 float
        # If library stores 0-100, normalise
        if opacity_val > 1.0:
            opacity_val /= 100.0
        if math.isclose(opacity_val, 0.60, abs_tol=0.05):
            print(f"✓ Logo opacity ≈60 % (actual {opacity_val:.2f}) (0.3)")
            score += 0.3
        else:
            print(f"✗ Logo opacity {opacity_val:.2f} not within 60 % ±5 %")

    # ---------- Requirement 4: Logo is top layer (0.2) -----------
    if logo_layer is not None and layers.index(logo_layer) == 0:
        print("✓ Logo layer is on top of the stack (0.2)")
        score += 0.2
    elif logo_layer is not None:
        print("✗ Logo layer is not on top of the stack")

    # ------------------------ Final Score -------------------------
    final_score = min(score, max_score)
    print(f"FINAL SCORE BREAKDOWN: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------- Entry Point ---------------------------
if __name__ == "__main__":
    verify_gimp_logo_task(XCF_PATH)

