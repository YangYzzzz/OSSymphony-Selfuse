"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert landscape video to portrait orientation and save to /home/user/Desktop/portrait.mov.
Generated: 2025-09-13 10:32:34
Status: success
Model: azure-o3
Total Steps: 14
"""

import os
import subprocess
import json
import sys

"""
Reward Script: Verify conversion of landscape video to portrait orientation

Scoring Breakdown (max 1.0):
  1. Valid output video exists and contains a video stream ............ 0.4
  2. Video is in portrait orientation (height>width or rotate=90/270) .. 0.6

Output is printed step-by-step with the final score as:
    REWARD: X.X
"""

TARGET_PATH = '/home/user/Desktop/portrait.mov'

# ---------------- Helper Functions -----------------

def run_ffprobe(path):
    """Return ffprobe JSON for the first video stream or None on error."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,side_data_list:stream_tags=rotate',
        '-of', 'json',
        path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def extract_metadata(path):
    """Return (width, height, rotation) for the first video stream."""
    data = run_ffprobe(path)
    if not data or 'streams' not in data or not data['streams']:
        return None, None, None

    stream = data['streams'][0]
    width = stream.get('width')
    height = stream.get('height')

    # Rotation metadata can live in tags or side_data_list
    rotate = None
    tags = stream.get('tags') or {}
    if 'rotate' in tags and tags['rotate'] != '':
        try:
            rotate = int(float(tags['rotate']))
        except ValueError:
            pass

    for side in stream.get('side_data_list') or []:
        if 'rotation' in side:
            try:
                rotate = int(float(side['rotation']))
            except ValueError:
                pass

    return width, height, rotate

# ---------------- Verification Logic ---------------

def verify_task():
    max_score = 1.0
    score = 0.0

    print('--- Landscape → Portrait Conversion Verification ---')
    print(f'Expected output file: {TARGET_PATH}')

    # Check 1: File existence and valid video
    if not os.path.isfile(TARGET_PATH):
        print('✗ portrait.mov not found.')
        print('REWARD: 0.0')
        return 0.0

    width, height, rotate = extract_metadata(TARGET_PATH)
    if width is None or height is None:
        print('✗ File exists but no video stream detected.')
        print('REWARD: 0.0')
        return 0.0

    print(f'✓ Valid video stream detected — resolution {width}x{height}, rotation metadata: {rotate}')
    score += 0.4  # Earn points for producing a valid video output

    # Check 2: Portrait orientation verification
    is_portrait_dimension = height > width if (width and height) else False
    is_portrait_rotation = rotate is not None and (abs(rotate) % 180 == 90)

    if is_portrait_dimension or is_portrait_rotation:
        print('✓ Portrait orientation confirmed.')
        score += 0.6
    else:
        print('✗ Video is not portrait oriented (height ≤ width and no 90/270° rotation metadata).')

    final_score = min(score, max_score)
    print(f'REWARD: {final_score}')
    return final_score

if __name__ == '__main__':
    verify_task()
