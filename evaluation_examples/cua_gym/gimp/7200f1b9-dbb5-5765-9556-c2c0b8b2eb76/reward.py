"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a folder of about 60 JPEGs, each roughly 4000 × 3000 px, and I need every image scaled down to exactly 50 % of its current width and height for faster web loading. What’s the quickest way to batch-resize all of them in GIMP?
Generated: 2025-09-01 15:10:21
Status: success
Model: o3
Total Steps: 12
"""

import os
import re
import subprocess

# =============================================================
# Reward Verification Script for GIMP Batch-Resize Task
# =============================================================
# The task: scale every 4000×3000 image down to exactly 50 % (→ 2000×1500).
# Verification focuses on the supplied XCF file that should now be 2000×1500.
# -------------------------------------------------------------
# MANDATORY: use the EXACT path provided in the context – NO SEARCHING!
XCF_PATH = "/tmp/batch_resize_task.xcf"  # ← Do NOT modify

# -------------------------------------------------------------
# Helper 1: Try to read dimensions with gimpformats (preferred)
# -------------------------------------------------------------

def _dims_with_gimpformats(path: str):
    try:
        from gimpformats.gimpXcfDocument import GimpDocument  # lightweight Python reader
        doc = GimpDocument(path)
        return int(doc.width), int(doc.height)
    except Exception as e:
        print(f"  • gimpformats failed: {e}")
        return None

# -------------------------------------------------------------
# Helper 2: Fallback – read dimensions via xcftools (xcfinfo)
# -------------------------------------------------------------

def _dims_with_xcftools(path: str):
    try:
        proc = subprocess.run(["xcfinfo", path], capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"  • xcfinfo failed: {proc.stderr.strip()}")
            return None
        m = re.search(r"Width:\s*(\d+)\s*Height:\s*(\d+)", proc.stdout)
        if m:
            return int(m.group(1)), int(m.group(2))
        print("  • Could not parse dimensions from xcfinfo output")
    except FileNotFoundError:
        print("  • xcftools not installed (xcfinfo missing)")
    except Exception as e:
        print(f"  • Unexpected xcftools error: {e}")
    return None

# -------------------------------------------------------------
# Unified dimension loader – tries gimpformats, then xcftools
# -------------------------------------------------------------

def load_dimensions(path: str):
    print(f"Loading XCF from provided path: {path}")
    dims = _dims_with_gimpformats(path)
    if dims:
        print("  ✓ Dimensions retrieved via gimpformats")
        return dims
    print("  • Falling back to xcftools …")
    dims = _dims_with_xcftools(path)
    if dims:
        print("  ✓ Dimensions retrieved via xcftools")
    return dims

# -------------------------------------------------------------
# Main verification & progressive scoring
# -------------------------------------------------------------

def verify_batch_resize() -> float:
    total_score = 0.0

    # 1) Prerequisite: file must exist
    if not os.path.exists(XCF_PATH):
        print("✗ XCF file not found – task likely not attempted")
        return 0.0

    # 2) Read image dimensions
    dims = load_dimensions(XCF_PATH)
    if not dims:
        print("✗ Unable to load XCF or obtain dimensions – verification failed")
        return 0.0

    width, height = dims
    print(f"  → Detected dimensions: {width}×{height}")

    # 3) Scoring logic
    TARGET_W, TARGET_H = 2000, 1500  # 50 % of 4000×3000

    if width == TARGET_W and height == TARGET_H:
        total_score = 1.0
        print("✓ Perfect resize detected (2000×1500) – full credit")
    else:
        # Near-perfect (≤5 % deviation)
        w_ratio = width / TARGET_W
        h_ratio = height / TARGET_H
        if 0.95 <= w_ratio <= 1.05 and 0.95 <= h_ratio <= 1.05:
            total_score = 0.8
            print("✓ Resize close to target (within 5 %) – partial credit 0.8")
        # Any down-scaling (both dimensions < original)
        elif width < 4000 and height < 3000:
            # Map average reduction ratio to 0.4–0.6 range
            avg_ratio = (width / 4000 + height / 3000) / 2  # 1.0 = no change
            reduction_score = 0.6 - avg_ratio * 0.2  # linear mapping
            total_score = max(0.4, min(0.6, reduction_score))
            print(f"✓ Image reduced but not to target – partial credit {total_score:.2f}")
        else:
            print("✗ No down-scaling detected – no credit")
            total_score = 0.0

    return round(total_score, 2)

# -------------------------------------------------------------
# Execute verification and print reward (required format)
# -------------------------------------------------------------
if __name__ == "__main__":
    reward_value = verify_batch_resize()
    print(f"REWARD: {reward_value}")

