"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm preparing an Instagram post and need some extra breathing room around the graphic. Could you walk me through bumping the canvas up to exactly 1200×1200 px and filling any newly-added area with pure white (#FFFFFF)?
Generated: 2025-09-01 15:17:59
Status: success
Model: o3
Total Steps: 9
"""

import os
import re
import subprocess
import tempfile
from typing import Tuple

import numpy as np
from PIL import Image
from gimpformats.gimpXcfDocument import GimpDocument

# ------------------------------------------------------------------
# 📁 MAIN XCF PATH (DO NOT CHANGE / DO NOT SEARCH!)
# ------------------------------------------------------------------
XCF_FILE_PATH: str = "/tmp/instagram_canvas_task.xcf"  # ← Provided in task context

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _dimensions_with_gimpformats(path: str) -> Tuple[int, int]:
    """Return image (width, height) using gimpformats. Falls back to (None, None) on error."""
    try:
        doc = GimpDocument(path)
        return doc.width, doc.height
    except Exception as e:
        print(f"⚠️  gimpformats could not read dimensions: {e}")
        return None, None


def _dimensions_with_xcfinfo(path: str) -> Tuple[int, int]:
    """Return image (width, height) via `xcfinfo` CLI. Returns (None, None) on error."""
    try:
        result = subprocess.run(["xcfinfo", path], capture_output=True, text=True, check=True)
        # Example line: "Version 11, 1200x1200 RGB color, 1 layers, compressed RLE"
        match = re.search(r"(\d+)x(\d+)", result.stdout)
        if match:
            return int(match.group(1)), int(match.group(2))
    except Exception as e:
        print(f"⚠️  xcfinfo failed: {e}")
    return None, None


def _get_dimensions(path: str) -> Tuple[int, int]:
    """Get dimensions using gimpformats first, then xcfinfo as fallback."""
    w, h = _dimensions_with_gimpformats(path)
    if w is None or h is None:
        w, h = _dimensions_with_xcfinfo(path)
    return w, h


def _export_xcf_to_png(xcf_path: str, png_path: str) -> bool:
    """Flatten/export XCF → PNG via xcf2png. Returns True on success."""
    try:
        subprocess.run(["xcf2png", xcf_path, "-o", png_path], check=True, capture_output=True)
        return os.path.exists(png_path)
    except subprocess.CalledProcessError as e:
        print(f"✗ xcf2png error: {e.stderr.decode(errors='ignore')}")
    except FileNotFoundError:
        print("✗ xcf2png tool not found (install xcftools).")
    return False


def _border_whiteness(png_path: str, thickness_ratio: float = 0.03) -> float:
    """Compute fraction of white (#FFFFFF) pixels along border of PNG."""
    img = Image.open(png_path).convert("RGB")
    arr = np.array(img)
    h, w, _ = arr.shape
    thickness = max(1, int(min(w, h) * thickness_ratio))

    # Boolean mask for border region
    mask = np.zeros((h, w), dtype=bool)
    mask[:thickness, :] = True
    mask[-thickness:, :] = True
    mask[:, :thickness] = True
    mask[:, -thickness:] = True

    border_pixels = arr[mask]
    white_mask = (
        (border_pixels[:, 0] >= 250)
        & (border_pixels[:, 1] >= 250)
        & (border_pixels[:, 2] >= 250)
    )
    return float(white_mask.mean()) if border_pixels.size else 0.0

# ------------------------------------------------------------------
# Main verification function
# ------------------------------------------------------------------

def verify_instagram_canvas_task(xcf_path: str) -> float:
    """Verify task completion and return reward score between 0.0–1.0."""
    print("🎯 Verifying Instagram canvas resize & white border task …")

    if not os.path.exists(xcf_path):
        print(f"✗ XCF file not found at expected path: {xcf_path}")
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0

    # ------------------------------------------------------------------
    # Requirement 1: Canvas exactly 1200 × 1200 px
    # ------------------------------------------------------------------
    width, height = _get_dimensions(xcf_path)
    if width == 1200 and height == 1200:
        print(f"✓ Canvas size is correct: {width}×{height} px (0.4 points)")
        total_score += 0.4
    else:
        print(f"✗ Canvas size is {width}×{height} px – expected 1200×1200 px")

    # ------------------------------------------------------------------
    # Requirement 2: Newly added area filled with pure white (#FFFFFF)
    # ------------------------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp_dir:
        png_path = os.path.join(tmp_dir, "export.png")
        if _export_xcf_to_png(xcf_path, png_path):
            whiteness = _border_whiteness(png_path)
            print(f"Border whiteness ratio: {whiteness:.3f}")

            if whiteness >= 0.95:
                print("✓ Border region is pure white (0.6 points)")
                total_score += 0.6
            elif whiteness >= 0.70:
                print("△ Border mostly white – minor issues (0.3 points)")
                total_score += 0.3
            else:
                print("✗ Border not sufficiently white (0 points)")
        else:
            print("✗ Could not export XCF to PNG – border check skipped (0 points)")

    # ------------------------------------------------------------------
    # Final scoring
    # ------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ------------------------------------------------------------------
# Execute verification when run as script
# ------------------------------------------------------------------
if __name__ == "__main__":
    verify_instagram_canvas_task(XCF_FILE_PATH)

