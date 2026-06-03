"""
Reward Script: Extract 5 frames from documentary.mp4 using VLC, process each in GIMP
               (grayscale + 5-pixel black border), and combine into animated GIF.
Task ID: osworld_multi_apps_media_image_008
Domain: multi_apps (VLC + GIMP)
Scoring:
  Component 1: 5 frame PNGs exist and have correct size (640x480, RGB)   — 0.30 pts
  Component 2: 5 bw PNGs are grayscale (L mode), 650x490, 5-pixel border — 0.30 pts
  Component 3: Animated GIF has 5 frames at 1000ms each, correct size    — 0.40 pts
"""

import os
from PIL import Image
import numpy as np

WORKDIR = '/home/user/frames'


def verify_task(frames_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: frames directory must exist
    if not os.path.isdir(frames_dir):
        print(f"CRITICAL: Frames directory not found: {frames_dir}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: 5 frame PNGs extracted from video (0.30 points)
    # Expected: frame_1.png through frame_5.png, each 640x480 RGB
    # This FAILS on initial_env (frames dir is empty) and
    # PASSES on golden_env (frames present with correct size).
    # ------------------------------------------------------------------
    try:
        frames_found = 0
        frames_correct_size = 0
        for i in range(1, 6):
            frame_path = os.path.join(frames_dir, f'frame_{i}.png')
            if os.path.isfile(frame_path):
                frames_found += 1
                img = Image.open(frame_path)
                # Frames must be RGB and 640x480
                if img.mode == 'RGB' and img.size == (640, 480):
                    frames_correct_size += 1
                else:
                    print(f"FAIL: Component 1 — frame_{i}.png has mode={img.mode}, size={img.size}, expected RGB 640x480")
            else:
                print(f"FAIL: Component 1 — frame_{i}.png not found at {frame_path}")

        if frames_correct_size == 5:
            print(f"PASS: Component 1 — All 5 frame PNGs found (640x480 RGB) (0.30 pts)")
            total_score += 0.30
        elif frames_found > 0:
            partial = round(0.30 * frames_correct_size / 5, 4)
            print(f"PARTIAL: Component 1 — {frames_correct_size}/5 correct frame PNGs found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No frame PNGs found in {frames_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: 5 bw PNGs are grayscale with 5-pixel black border (0.30 points)
    # Expected: bw_1.png through bw_5.png
    #   - mode = L (grayscale, not RGB)
    #   - size = 650x490 (640+5*2 x 480+5*2 — 5-pixel border added each side)
    #   - all border pixels (top/bottom 5 rows, left/right 5 columns) are black (0)
    # This FAILS on initial_env and PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        bw_correct = 0
        for i in range(1, 6):
            bw_path = os.path.join(frames_dir, f'bw_{i}.png')
            if not os.path.isfile(bw_path):
                print(f"FAIL: Component 2 — bw_{i}.png not found at {bw_path}")
                continue

            img = Image.open(bw_path)
            arr = np.array(img.convert('L'))

            # Check mode: must be grayscale (L)
            if img.mode not in ('L', 'LA'):
                print(f"FAIL: Component 2 — bw_{i}.png mode={img.mode}, expected L (grayscale)")
                continue

            # Check size: must be 650x490 (5-pixel border added on all sides)
            if img.size != (650, 490):
                print(f"FAIL: Component 2 — bw_{i}.png size={img.size}, expected (650, 490)")
                continue

            # Check border: top/bottom 5 rows and left/right 5 columns must be black (0)
            top_border_black = np.all(arr[:5, :] == 0)
            bottom_border_black = np.all(arr[-5:, :] == 0)
            left_border_black = np.all(arr[:, :5] == 0)
            right_border_black = np.all(arr[:, -5:] == 0)

            if top_border_black and bottom_border_black and left_border_black and right_border_black:
                # Also check that inner content is not entirely black
                inner_max = arr[5:485, 5:645].max()
                if inner_max > 0:
                    bw_correct += 1
                else:
                    print(f"FAIL: Component 2 — bw_{i}.png inner content is entirely black (bad conversion)")
            else:
                print(f"FAIL: Component 2 — bw_{i}.png border check: top={top_border_black}, "
                      f"bottom={bottom_border_black}, left={left_border_black}, right={right_border_black}")

        if bw_correct == 5:
            print(f"PASS: Component 2 — All 5 bw PNGs are grayscale (L mode, 650x490) with 5px black border (0.30 pts)")
            total_score += 0.30
        elif bw_correct > 0:
            partial = round(0.30 * bw_correct / 5, 4)
            print(f"PARTIAL: Component 2 — {bw_correct}/5 bw PNGs correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No valid bw PNGs found in {frames_dir}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Animated GIF with 5 frames at 1000ms delay each (0.40 points)
    # Expected: documentary_storyboard.gif
    #   - size = 650x490 (matches bw images)
    #   - 5 frames
    #   - each frame has 1000ms duration
    # This FAILS on initial_env and PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        gif_path = os.path.join(frames_dir, 'documentary_storyboard.gif')

        if not os.path.isfile(gif_path):
            print(f"FAIL: Component 3 — documentary_storyboard.gif not found at {gif_path}")
        else:
            gif = Image.open(gif_path)

            # Check size matches bw images (650x490)
            gif_size_ok = gif.size == (650, 490)
            if not gif_size_ok:
                print(f"FAIL: Component 3 — GIF size={gif.size}, expected (650, 490)")

            # Count frames and check duration
            frame_count = 0
            durations = []
            try:
                while True:
                    gif.seek(frame_count)
                    duration = gif.info.get('duration', 0)
                    durations.append(duration)
                    frame_count += 1
            except EOFError:
                pass

            frame_count_ok = frame_count == 5
            if not frame_count_ok:
                print(f"FAIL: Component 3 — GIF has {frame_count} frames, expected 5")

            # All frames must have 1000ms duration (1 second per frame as per task)
            duration_ok = all(d == 1000 for d in durations)
            if not duration_ok:
                print(f"FAIL: Component 3 — GIF durations={durations}, expected all 1000ms")

            if gif_size_ok and frame_count_ok and duration_ok:
                print(f"PASS: Component 3 — Animated GIF: {frame_count} frames, size={gif.size}, "
                      f"durations={durations} (0.40 pts)")
                total_score += 0.40
            else:
                # Partial: give some credit if GIF exists with correct number of frames
                if frame_count_ok and gif_size_ok:
                    print(f"PARTIAL: Component 3 — GIF has correct size/frames but wrong durations (0.20 pts)")
                    total_score += 0.20
                elif frame_count_ok:
                    print(f"PARTIAL: Component 3 — GIF has correct frame count but wrong size (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 — GIF does not meet requirements")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical frames directory path
if not os.path.isdir(WORKDIR):
    print(f"Frames directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task(WORKDIR)
