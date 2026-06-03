"""
Reward Script: Apply posterize effect and color reduction to illustration.png, save as illustration_poster.png
Task ID: osworld_multi_apps_writer_gimp_066
Domain: libreoffice_writer + gimp (multi-app)
Scoring:
  - Component 1: illustration_poster.png file exists on Desktop (0.2 pts, precondition for further checks)
  - Component 2: Color count significantly reduced (<= 32 unique colors, consistent with indexed 32-color palette) (0.4 pts)
  - Component 3: Posterize effect applied — all channel values are multiples of 64 (levels=4 posterization) (0.4 pts)
Total: 1.0
"""

import os
from PIL import Image
import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_writer_gimp_066'

POSTER_PATH = os.path.join(WORKDIR, 'illustration_poster.png')
ORIGINAL_PATH = os.path.join(WORKDIR, 'illustration.png')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Task: Read instructions from notes.docx, apply posterize (levels=4) and
    indexed color reduction (32 colors) to illustration.png, save as illustration_poster.png.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: illustration_poster.png must exist
    if not os.path.exists(POSTER_PATH):
        print(f"FAIL: illustration_poster.png not found at {POSTER_PATH}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: illustration_poster.png file exists and is a valid image (0.2 points)
    # This is the minimum signal that the agent completed the save step.
    img = None
    try:
        img = Image.open(POSTER_PATH).convert('RGB')
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open illustration_poster.png: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    if img is not None:
        print(f"PASS: Component 1 — illustration_poster.png exists and is readable (0.2 pts)")
        total_score += 0.2

    # Component 2: Color count significantly reduced (<= 32 unique colors) (0.4 points)
    # The task requires converting to indexed mode with 32 colors. The golden image
    # has 19 unique colors (well within 32-color limit). Initial has 179 unique colors.
    try:
        arr = np.array(img)
        unique_colors = set(map(tuple, arr.reshape(-1, 3)))
        num_colors = len(unique_colors)
        if num_colors <= 32:
            print(f"PASS: Component 2 — Color count is {num_colors} (<= 32 as required by indexed 32-color palette) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected <= 32 unique colors, found {num_colors}. Indexed color reduction not applied.")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not count unique colors: {e}")

    # Component 3: Posterize effect applied — all RGB channel values are multiples of 64 (0.4 points)
    # GIMP Posterize with levels=4 maps all channel values to {0, 64, 128, 192}.
    # This is a strong signal that posterization at 4 levels was correctly applied.
    # The original illustration.png has a wide range of channel values that are NOT
    # all multiples of 64, so this check will correctly fail on the initial env.
    try:
        arr = np.array(img)
        unique_vals = np.unique(arr)
        non_multiples = [int(v) for v in unique_vals if int(v) % 64 != 0]
        if len(non_multiples) == 0:
            posterize_vals = sorted(set(int(v) for v in unique_vals))
            total_score += 0.4
            print(f"PASS: Component 3 — All channel values are multiples of 64 {posterize_vals}, "
                  f"confirming posterize levels=4 was applied (0.4 pts)")
        else:
            print(f"FAIL: Component 3 — Found channel values not multiples of 64: {non_multiples[:10]}... "
                  f"Posterize levels=4 not correctly applied.")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify posterize effect: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
