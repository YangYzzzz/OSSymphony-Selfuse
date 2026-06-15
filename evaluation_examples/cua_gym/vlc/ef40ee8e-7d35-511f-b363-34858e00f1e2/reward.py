"""
Reward Script: Take three snapshots from concert video at 1:00, 2:00, 3:00
Task ID: vlcplay_016
Domain: vlc
Scoring:
  Component 1: frame_1m.png exists and matches video frame at 1:00 (0.34 pts)
  Component 2: frame_2m.png exists and matches video frame at 2:00 (0.33 pts)
  Component 3: frame_3m.png exists and matches video frame at 3:00 (0.33 pts)
"""

import os
import numpy as np
from PIL import Image

WORKDIR = '/home/user'
TASK_ID = 'vlcplay_016'
SNAP_DIR = os.path.join(WORKDIR, 'Pictures', 'Snapshots')
VIDEO_PATH = os.path.join(WORKDIR, 'Videos', 'concert.mp4')

# Timestamps (HH:MM:SS) and filenames for the three snapshots
SNAPSHOTS = [
    ('00:01:00', 'frame_1m.png', 0.34),
    ('00:02:00', 'frame_2m.png', 0.33),
    ('00:03:00', 'frame_3m.png', 0.33),
]


def extract_reference_frame(video_path, timestamp_str, output_path):
    """Extract a single frame from the video at the given timestamp using ffmpeg via os.system."""
    # Remove any pre-existing file to detect failure
    if os.path.exists(output_path):
        os.remove(output_path)
    cmd = 'ffmpeg -y -i "{}" -ss {} -frames:v 1 "{}" >/dev/null 2>&1'.format(
        video_path, timestamp_str, output_path
    )
    os.system(cmd)
    return os.path.exists(output_path)


def compute_ssim(img1_path, img2_path):
    """Compute SSIM between two images. Returns float 0.0-1.0."""
    i1 = np.array(Image.open(img1_path).convert('L'), dtype=float)
    i2 = np.array(Image.open(img2_path).convert('L'), dtype=float)
    # Resize to match if dimensions differ
    if i1.shape != i2.shape:
        h = min(i1.shape[0], i2.shape[0])
        w = min(i1.shape[1], i2.shape[1])
        i1_r = np.array(Image.open(img1_path).convert('L').resize((w, h), Image.LANCZOS), dtype=float)
        i2_r = np.array(Image.open(img2_path).convert('L').resize((w, h), Image.LANCZOS), dtype=float)
        i1, i2 = i1_r, i2_r
    mu1, mu2 = i1.mean(), i2.mean()
    s1, s2 = i1.var(), i2.var()
    s12 = ((i1 - mu1) * (i2 - mu2)).mean()
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    return ((2 * mu1 * mu2 + c1) * (2 * s12 + c2)) / ((mu1 ** 2 + mu2 ** 2 + c1) * (s1 + s2 + c2))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: video file must exist to extract reference frames
    if not os.path.exists(VIDEO_PATH):
        print(f"CRITICAL: Video file not found at {VIDEO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Check each snapshot independently
    for idx, (timestamp, filename, weight) in enumerate(SNAPSHOTS, 1):
        snap_path = os.path.join(SNAP_DIR, filename)

        # Component N: <filename> exists and matches video at <timestamp>
        try:
            if not os.path.exists(snap_path):
                print(f"FAIL: Component {idx} -- {filename} does not exist in {SNAP_DIR}")
                continue

            # Verify it is a valid image with reasonable dimensions
            img = Image.open(snap_path)
            w_img, h_img = img.size
            if w_img < 100 or h_img < 100:
                print(f"FAIL: Component {idx} -- {filename} has invalid dimensions: {img.size}")
                continue

            # Extract reference frame from video at the target timestamp
            ref_path = '/tmp/reward_ref_{}.png'.format(idx)
            if not extract_reference_frame(VIDEO_PATH, timestamp, ref_path):
                print(f"ERROR: Component {idx} -- Could not extract reference frame at {timestamp}")
                continue

            # Compare snapshot to reference frame using SSIM
            ssim_score = compute_ssim(snap_path, ref_path)
            # Threshold: SSIM >= 0.85 means it is a match from the correct timestamp
            if ssim_score >= 0.85:
                print(f"PASS: Component {idx} -- {filename} matches video at {timestamp} (SSIM={ssim_score:.4f}) ({weight} pts)")
                total_score += weight
            else:
                print(f"FAIL: Component {idx} -- {filename} SSIM={ssim_score:.4f} (threshold 0.85), may be wrong timestamp")

        except Exception as e:
            print(f"ERROR: Component {idx} -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
