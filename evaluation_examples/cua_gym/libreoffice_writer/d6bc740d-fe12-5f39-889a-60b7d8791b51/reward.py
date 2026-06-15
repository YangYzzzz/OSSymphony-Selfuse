"""
Reward Script: Apply photo fixes from photo_fix_list.docx to old_photo.jpg and save as old_photo_restored.jpg
Task ID: osworld_multi_apps_writer_gimp_067
Domain: libreoffice_writer + gimp (multi-app)
Scoring:
  - Component 1: Image is greyscale (black-and-white conversion done)     0.40 pts
  - Component 2: Midtones are brightened vs original old_photo.jpg        0.30 pts
  - Component 3: Scratch at y=319-322 is removed (row std dev normalized) 0.30 pts
  Total: 1.0

Task: Check photo_fix_list.docx for corrections to old_photo.jpg.
Apply (1) scratch removal at y=320, (2) exposure correction (raise midpoints by 15),
(3) convert to greyscale. Save as old_photo_restored.jpg on Desktop.
"""

import os

# PIL is available on the VM via Pillow
from PIL import Image
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_writer_gimp_067'

ORIGINAL_PATH = f'{WORKDIR}/Desktop/old_photo.jpg'
RESTORED_PATH = f'{WORKDIR}/Desktop/old_photo_restored.jpg'

# Known baseline from initial_env analysis:
# original mean brightness (greyscale) ≈ 95.85
# scratch rows y=319-322 have std dev ≈ 54-60 (anomalous vs surrounding ~17-18)
ORIGINAL_MEAN_BRIGHTNESS = 95.85
SCRATCH_ROWS = [319, 320, 321, 322]
NORMAL_STD_THRESHOLD = 35.0  # std dev must be below this for scratch to be considered removed


def check_greyscale(img: Image.Image) -> tuple:
    """
    Returns (is_greyscale: bool, details: str).
    Checks if image is truly greyscale (mode L) or has identical RGB channels.
    """
    mode = img.mode
    if mode == 'L':
        return (mode == 'L'), f"mode={mode}"
    # For RGB/RGBA or other modes, check if all channels are equal
    arr = np.array(img.convert('RGB'))
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    channel_diff = float(
        np.abs(r.astype(int) - g.astype(int)).mean() +
        np.abs(r.astype(int) - b.astype(int)).mean()
    )
    return channel_diff < 2.0, f"mode={mode}, channel_diff={channel_diff:.2f}"


def verify_task(restored_path: str, original_path: str) -> float:
    """
    Verify that old_photo_restored.jpg correctly implements all three fixes.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Gate: restored file must exist (not scored on its own)
    if not os.path.isfile(restored_path):
        print(f"GATE FAIL: Restored file not found at {restored_path}")
        print("REWARD: 0.0")
        return 0.0

    # Try loading the restored image
    try:
        img_restored = Image.open(restored_path)
    except Exception as e:
        print(f"GATE FAIL: Cannot open restored image: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load original image for brightness comparison
    try:
        img_original = Image.open(original_path).convert('L')
        arr_original = np.array(img_original)
        original_brightness = float(arr_original.mean())
    except Exception as e:
        print(f"WARN: Cannot open original image: {e}. Using baseline {ORIGINAL_MEAN_BRIGHTNESS}")
        original_brightness = ORIGINAL_MEAN_BRIGHTNESS

    # Component 1: Image is greyscale (black-and-white conversion completed) — 0.40 points
    # Task requires: "Convert to greyscale"
    try:
        greyscale_result, greyscale_details = check_greyscale(img_restored)
        if greyscale_result:
            print(f"PASS: Component 1 — Image is greyscale ({greyscale_details}) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — Image is NOT greyscale ({greyscale_details}); expected greyscale")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Midtones brightened — exposure correction applied — 0.30 points
    # Task requires: "Increase exposure (Curves: raise midpoints by 15)"
    # Original mean brightness ≈ 95.85; after raising midpoints by 15, expect ~107-115
    # Threshold: restored must be at least 5 points brighter than original
    try:
        arr_restored = np.array(img_restored.convert('L'))
        restored_brightness = float(arr_restored.mean())
        brightness_delta = restored_brightness - original_brightness
        if brightness_delta >= 5.0:
            print(f"PASS: Component 2 — Midtones brightened (delta=+{brightness_delta:.2f}, "
                  f"original={original_brightness:.2f}, restored={restored_brightness:.2f}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected brightness gain >=5, got delta={brightness_delta:.2f} "
                  f"(original={original_brightness:.2f}, restored={restored_brightness:.2f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Scratch at y=319-322 removed — 0.30 points
    # Task requires: "Use Heal tool to remove the scratch at y=320"
    # In the initial image, rows y=319-322 have anomalously high std dev (54-60)
    # vs surrounding rows (~17-18). After healing, those rows should have normal std dev.
    try:
        arr_restored_gray = np.array(img_restored.convert('L'))
        scratch_stds = [float(arr_restored_gray[y, :].std()) for y in SCRATCH_ROWS]
        max_scratch_std = max(scratch_stds)
        stds_str = ', '.join(f'y={y}:{s:.1f}' for y, s in zip(SCRATCH_ROWS, scratch_stds))
        if max_scratch_std < NORMAL_STD_THRESHOLD:
            print(f"PASS: Component 3 — Scratch removed (max_std={max_scratch_std:.2f} < {NORMAL_STD_THRESHOLD})"
                  f" [{stds_str}] (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Scratch NOT fully removed "
                  f"(max_std={max_scratch_std:.2f} >= {NORMAL_STD_THRESHOLD}) [{stds_str}]")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isfile(RESTORED_PATH):
    print(f"File not found: {RESTORED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(RESTORED_PATH, ORIGINAL_PATH)
