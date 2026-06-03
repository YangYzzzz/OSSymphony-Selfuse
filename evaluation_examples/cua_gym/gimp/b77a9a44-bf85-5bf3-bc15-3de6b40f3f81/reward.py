"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to isolate a precise area: please create a 200 × 300 px rectangular selection so I can drop a logo in that spot.
Generated: 2025-09-01 14:22:38
Status: success
Model: o3
Total Steps: 19
"""

"""
Reward Script for GIMP Selection Verification
Task: Verify that the user created a 200×300 px rectangular selection in the
provided XCF file.

Scoring (progressive ‑ totals to 1.0):
  • 0.3 – A non-empty selection mask exists
  • 0.3 – Bounding-box size is exactly 200 × 300 px (width × height)
  • 0.4 – Selection is a perfect filled rectangle (all pixels inside bbox
          selected, none outside)

The script uses the gimpformats library (pure-Python) to read the XCF file, so
no external binaries are required.  It does NOT search the filesystem – it
uses the exact path mandated in the task context (/tmp/rect_selection_task.xcf).
All checks involve real pixel data; no points are awarded for natural
conditions such as file existence or successful load.
"""
import os
import traceback
from typing import Optional

import numpy as np
from gimpformats.gimpXcfDocument import GimpDocument

# 🚨 MANDATORY: use the exact path given in the task context – no searching!
XCF_PATH = "/tmp/rect_selection_task.xcf"

# Progressive score weights
WEIGHTS = {
    "selection_exists": 0.3,
    "size_correct": 0.3,
    "rectangular": 0.4,
}

def find_selection_channel(doc: GimpDocument) -> Optional[object]:
    """Return the first channel whose name starts with 'Selection', else None."""
    for ch in doc._channels:
        if ch.name.lower().startswith("selection"):
            return ch
    return None

def verify_selection(file_path: str) -> float:
    print(f"🎯 Verifying selection in XCF file: {file_path}")
    total_score = 0.0

    # ---------- Prerequisite checks (no points) ----------
    if not os.path.isfile(file_path):
        print("✗ XCF file not found – task failed")
        return 0.0

    try:
        doc = GimpDocument(file_path)
        print("✓ XCF loaded successfully (prerequisite)")
    except Exception as e:
        print(f"✗ Failed to load XCF: {e}")
        return 0.0

    # ---------- 1) Selection mask presence & non-emptiness ----------
    selection_channel = find_selection_channel(doc)
    if selection_channel is None:
        print("✗ No selection mask channel found")
        # early exit – nothing else to check
        return 0.0

    # Convert selection to NumPy boolean mask (selected = True)
    try:
        sel_img = selection_channel.image.convert("L")  # ensure greyscale
        mask = np.array(sel_img) > 0                    # bool array
    except Exception:
        print("✗ Unable to extract pixel data from selection channel")
        return 0.0

    sel_pixels = int(mask.sum())
    print(f"Selected pixel count: {sel_pixels}")

    if sel_pixels == 0:
        print("✗ Selection channel is empty – no selected pixels")
    else:
        total_score += WEIGHTS["selection_exists"]
        print(f"✓ Selection channel present and non-empty (+{WEIGHTS['selection_exists']})")

        # ---------- 2) Bounding-box dimension check ----------
        ys, xs = np.where(mask)
        y_min, y_max = ys.min(), ys.max()
        x_min, x_max = xs.min(), xs.max()
        bbox_w = x_max - x_min + 1
        bbox_h = y_max - y_min + 1
        print(f"Bounding box – x:{x_min}-{x_max} (w={bbox_w}), y:{y_min}-{y_max} (h={bbox_h})")

        if bbox_w == 200 and bbox_h == 300:
            total_score += WEIGHTS["size_correct"]
            print(f"✓ Bounding-box dimensions match 200×300 px (+{WEIGHTS['size_correct']})")
        else:
            print("✗ Bounding-box dimensions are incorrect – expected 200×300 px")

        # ---------- 3) Rectangular solidity check ----------
        inside_mask = mask[y_min : y_max + 1, x_min : x_max + 1]
        if inside_mask.all() and (sel_pixels == inside_mask.size):
            total_score += WEIGHTS["rectangular"]
            print(f"✓ Selection forms a perfect rectangle (+{WEIGHTS['rectangular']})")
        else:
            print("✗ Selection is not a solid filled rectangle or contains stray pixels")

    # ---------- Final score ----------
    final_score = round(min(total_score, 1.0), 4)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    try:
        reward = verify_selection(XCF_PATH)
    except Exception:
        print("✗ Unexpected exception during verification:")
        traceback.print_exc()
        reward = 0.0

    print(f"REWARD: {reward}")

