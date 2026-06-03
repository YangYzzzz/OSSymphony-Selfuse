"""
Reward Script: Extract 5-second clip from animation.mp4 and export as animation_clip.gif with 64 colors
Task ID: osworld_multi_apps_vlc_gimp_035
Domain: multi_apps (VLC + GIMP)
Scoring:
  Component 1: animation_clip.gif exists and is a valid animated GIF (precondition gate)
  Component 2: GIF has ~5-second total duration (50 frames at 10fps = 5000ms) (0.4 pts)
  Component 3: GIF color palette has at most 64 colors (0.4 pts)
  Component 4: GIF frame dimensions match source video 320x240 (0.2 pts)
"""

import os
from PIL import Image

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vlc_gimp_035'
GIF_PATH = f'{WORKDIR}/animation_clip.gif'


def verify_task(gif_path):
    """
    Verify task completion with progressive scoring.
    Task: Use VLC to extract a 5-second clip (00:05-00:10) from animation.mp4,
    import frames into GIMP, reduce color palette to 64 colors, export as animation_clip.gif.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: GIF file must exist and be a valid animated GIF
    if not os.path.isfile(gif_path):
        print(f"FAIL: animation_clip.gif not found at {gif_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        img = Image.open(gif_path)
        if img.format != 'GIF':
            print(f"FAIL: File is not a GIF, format={img.format}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open {gif_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: GIF found at {gif_path}")
    print(f"INFO: Format={img.format}, Mode={img.mode}, Size={img.size}")

    # Component 1: GIF is animated AND has approximately 5-second total duration (0.4 points)
    # The task requires a 5-second clip; animated means it has multiple frames;
    # total duration should be ~5000ms (5 seconds, allowing +/- 25% tolerance for encoding variation)
    try:
        n_frames = getattr(img, 'n_frames', 1)
        print(f"INFO: n_frames = {n_frames}")

        if n_frames <= 1:
            print(f"FAIL: Component 1 — GIF is not animated (n_frames={n_frames}), expected >1 frames for a 5-second clip")
        else:
            # Sum up frame durations
            total_duration_ms = 0
            for frame_no in range(n_frames):
                img.seek(frame_no)
                frame_duration = img.info.get('duration', 0)
                total_duration_ms += frame_duration

            print(f"INFO: Total duration = {total_duration_ms} ms ({total_duration_ms / 1000.0:.2f} s), n_frames={n_frames}")

            # Allow tolerance: 3750ms to 6250ms (5000ms +/- 25%)
            min_duration_ms = 3750
            max_duration_ms = 6250
            if min_duration_ms <= total_duration_ms <= max_duration_ms:
                print(f"PASS: Component 1 — Animated GIF with {total_duration_ms}ms duration (~5 seconds) ({n_frames} frames) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — Expected ~5000ms duration (3750-6250ms), found {total_duration_ms}ms")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: GIF color palette has at most 64 colors (0.4 points)
    # The task requires reducing color palette to 64 colors to minimize file size.
    # In GIF palette mode ('P'), the palette length / 3 gives the number of color entries.
    try:
        img.seek(0)
        if img.mode == 'P':
            palette_data = img.getpalette()
            if palette_data:
                # palette_data is a list of R,G,B values; divide by 3 to get entry count
                palette_entry_count = len(palette_data) // 3
                print(f"INFO: Palette data length = {len(palette_data)}, entries = {palette_entry_count}")
                if palette_entry_count <= 64:
                    print(f"PASS: Component 2 — Color palette has {palette_entry_count} entries (<= 64) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Expected palette <= 64 colors, found {palette_entry_count}")
            else:
                print("FAIL: Component 2 — Could not read palette data")
        else:
            # For non-palette modes, count actual unique colors
            unique_colors = set()
            n_frames = getattr(img, 'n_frames', 1)
            for frame_no in range(n_frames):
                img.seek(frame_no)
                frame_rgb = img.convert('RGB')
                unique_colors.update(frame_rgb.getdata())
            print(f"INFO: Non-palette mode={img.mode}, unique colors = {len(unique_colors)}")
            if len(unique_colors) <= 64:
                print(f"PASS: Component 2 — Total unique colors {len(unique_colors)} <= 64 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Expected at most 64 colors, found {len(unique_colors)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: GIF frame dimensions match source video (320x240) (0.2 points)
    # The source animation.mp4 is 320x240; the exported GIF should preserve these dimensions.
    try:
        img.seek(0)
        width, height = img.size
        print(f"INFO: GIF dimensions = {width}x{height}")
        # Source video is 320x240; allow some tolerance for resize (within 10 pixels)
        if abs(width - 320) <= 10 and abs(height - 240) <= 10:
            print(f"PASS: Component 3 — GIF dimensions {width}x{height} match source video 320x240 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected dimensions ~320x240, found {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isfile(GIF_PATH):
    print(f"File not found: {GIF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(GIF_PATH)
