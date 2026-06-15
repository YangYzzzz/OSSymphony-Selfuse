"""
Reward Script: Extract 5-second clip from interview.mp4 at 02:00, crop to 16:9, save as interview_clip.gif
Task ID: osworld_multi_apps_vlc_gimp_037
Domain: multi_apps (VLC + GIMP)
Scoring:
  Component 1: interview_clip.gif exists on Desktop (0.3 pts)
  Component 2: GIF has 16:9 aspect ratio dimensions (0.3 pts)
  Component 3: GIF is animated with approx 5-second duration (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vlc_gimp_037'
GIF_PATH = '/home/user/Desktop/interview_clip.gif'


def verify_task():
    """
    Verify that the animated GIF was correctly created from interview.mp4:
    - File must exist at /home/user/Desktop/interview_clip.gif
    - Must be a valid GIF with 16:9 aspect ratio (e.g., 1280x720)
    - Must be animated with approximately 5 seconds of content
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: interview_clip.gif exists on the Desktop (0.3 points)
    # This FAILS on initial_env (file does not exist yet)
    try:
        from PIL import Image
        if not os.path.isfile(GIF_PATH):
            print(f"FAIL: Component 1 — File not found: {GIF_PATH}")
            # Cannot proceed if file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Verify it is a valid GIF format
        img = Image.open(GIF_PATH)
        img.verify()  # raises if not valid
        print(f"PASS: Component 1 — interview_clip.gif exists and is a valid image (0.3 pts)")
        total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Reopen the GIF for further analysis (verify() invalidates the file pointer)
    try:
        img = Image.open(GIF_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot reopen GIF after verify: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: GIF dimensions are 16:9 aspect ratio (0.3 points)
    # Task requires cropping frames to a 16:9 centered region.
    # The original video is 1280x720 which is already 16:9.
    # A valid 16:9 crop yields width/height == 16/9 (within tolerance).
    try:
        w, h = img.size
        if h == 0:
            raise ValueError("Height is zero")
        aspect_ratio = w / h
        expected_ratio = 16 / 9  # ~1.7778
        # Accept ratio within 2% tolerance to allow for various crop sizes
        ratio_ok = abs(aspect_ratio - expected_ratio) / expected_ratio < 0.02
        if ratio_ok:
            print(f"PASS: Component 2 — GIF dimensions {w}x{h} have 16:9 aspect ratio "
                  f"(ratio={aspect_ratio:.4f}, expected={expected_ratio:.4f}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — GIF dimensions {w}x{h} do NOT have 16:9 ratio "
                  f"(ratio={aspect_ratio:.4f}, expected={expected_ratio:.4f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: GIF is animated with approximately 5 seconds of content (0.4 points)
    # Task requires extracting exactly 5 seconds at 02:00 from the video.
    # Verification: total GIF duration should be 4.0-6.5 seconds (allowing encoding flexibility)
    # and must have multiple frames (animated, not a static GIF).
    try:
        # Reload image
        img = Image.open(GIF_PATH)
        durations = []
        frame_count = 0
        try:
            while True:
                d = img.info.get('duration', 100)  # default 100ms if not specified
                durations.append(d)
                frame_count += 1
                img.seek(img.tell() + 1)
        except EOFError:
            pass

        total_duration_ms = sum(durations)
        total_duration_s = total_duration_ms / 1000.0

        duration_ok = (4.0 <= total_duration_s <= 6.5)
        frames_ok = frame_count >= 2
        if frames_ok and duration_ok:
            print(f"PASS: Component 3 — GIF is animated with {frame_count} frames, "
                  f"total duration {total_duration_s:.2f}s (expected ~5s) (0.4 pts)")
            total_score += 0.4
        elif frame_count < 2:
            print(f"FAIL: Component 3 — GIF has only {frame_count} frame(s); expected animated GIF with multiple frames")
        else:
            print(f"FAIL: Component 3 — GIF total duration is {total_duration_s:.2f}s "
                  f"({frame_count} frames); expected 4.0-6.5 seconds for a 5-second clip")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists('/home/user/Desktop'):
    print("CRITICAL: Desktop directory not found at /home/user/Desktop")
    print("REWARD: 0.0")
else:
    verify_task()
