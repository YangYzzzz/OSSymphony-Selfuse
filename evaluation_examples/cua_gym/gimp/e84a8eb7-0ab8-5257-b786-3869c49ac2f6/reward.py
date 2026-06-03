"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve already selected the area I want—can you tell me the fastest way to flood-fill that selection with our brand orange (#FF6A00) in GIMP?
Generated: 2025-09-01 14:25:21
Status: success
Model: o3
Total Steps: 6
"""

import os
import subprocess
from collections import deque
from PIL import Image

"""
Reward Verification Script for:
"I’ve already selected the area I want—can you tell me the fastest way to flood-fill that selection with our brand orange (#FF6A00) in GIMP?"

WHAT WE VERIFY
--------------
1. We flatten the supplied XCF file (exact path mandated by the task context) to a PNG using `xcf2png` (part of *xcftools*).
2. We analyse the flattened raster and look for the *largest contiguous* region that is exactly our brand-orange RGB value (255,106,0).
3. The score is proportional to how much of the whole canvas that largest orange region occupies.
   • ≥ 20 %  → 1.0 (task fully completed – big flood-filled area)
   • ≥ 10 %  → 0.8
   • ≥  5 %  → 0.6
   • ≥  1 %  → 0.4
   •  > 0    → 0.2 (some orange pixels but no significant flood fill)
   •  == 0   → 0.0 (no orange at all)

ANTI-HACKING / RULE COMPLIANCE
------------------------------
• Uses the *exact* file path: /tmp/flood_fill_orange_task.xcf (no searching, globbing, or walking the FS).
• No hard-coded success values – score derives from real pixel analysis.
• No points for natural conditions (file exists, loads, etc.).
• Progressive scoring with clear, falsifiable checks.
"""

# CONSTANTS
XCF_PATH = "/tmp/flood_fill_orange_task.xcf"  # exact path from task context
TARGET_RGB = (255, 106, 0)  # brand orange #FF6A00
TMP_PNG   = "/tmp/_reward_flat.png"          # temp file for flattened image


# ---------------------------------------------------------------------------
# Helper: convert XCF → PNG (flattened) using xcf2png
# ---------------------------------------------------------------------------

def flatten_xcf_to_png(xcf_path: str, png_path: str):
    """Return PIL.Image or None if conversion failed."""
    # Clean any previous artefact
    if os.path.exists(png_path):
        os.remove(png_path)

    try:
        result = subprocess.run(
            ["xcf2png", xcf_path, "-o", png_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"✗ xcf2png failed: {result.stderr.strip()}")
            return None
        if not os.path.isfile(png_path):
            print("✗ xcf2png did not create output file")
            return None
        print("✓ xcf2png conversion successful")
        return Image.open(png_path).convert("RGB")
    except FileNotFoundError:
        print("✗ xcftools (xcf2png) is not installed in the VM")
        return None
    except Exception as e:
        print(f"✗ Exception during xcf2png: {e}")
        return None


# ---------------------------------------------------------------------------
# Helper: calculate ratio of largest connected TARGET_RGB region
# ---------------------------------------------------------------------------

def largest_orange_region_ratio(img: Image.Image) -> float:
    w, h = img.size
    pixels = img.load()

    # Flood-fill style BFS to find connected components of exact orange pixels
    visited = [[False] * w for _ in range(h)]
    dirs    = [(1,0), (-1,0), (0,1), (0,-1)]
    largest = 0

    for y in range(h):
        for x in range(w):
            if pixels[x, y] == TARGET_RGB and not visited[y][x]:
                size = 0
                dq   = deque([(x, y)])
                visited[y][x] = True
                while dq:
                    cx, cy = dq.pop()
                    size += 1
                    for dx, dy in dirs:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx] and pixels[nx, ny] == TARGET_RGB:
                            visited[ny][nx] = True
                            dq.append((nx, ny))
                largest = max(largest, size)

    ratio = largest / (w * h)
    print(f"Largest orange component: {largest} pixels ⇒ ratio {ratio:.3f}")
    return ratio


# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def verify_task() -> float:
    if not os.path.isfile(XCF_PATH):
        print("✗ Task file missing – cannot verify")
        print("REWARD: 0.0")
        return 0.0

    print(f"🎯 Verifying file: {XCF_PATH}")
    img = flatten_xcf_to_png(XCF_PATH, TMP_PNG)
    if img is None:
        print("REWARD: 0.0")
        return 0.0

    ratio = largest_orange_region_ratio(img)

    # Progressive scoring
    if   ratio >= 0.20:
        score = 1.0
    elif ratio >= 0.10:
        score = 0.8
    elif ratio >= 0.05:
        score = 0.6
    elif ratio >= 0.01:
        score = 0.4
    elif ratio >  0.0:
        score = 0.2
    else:
        score = 0.0

    print(f"Final score: {score}")
    print(f"REWARD: {score}")
    return score


# ---------------------------------------------------------------------------
# Execute when run as script
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()

