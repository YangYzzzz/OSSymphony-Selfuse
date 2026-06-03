"""
Reward Script: Build an automated image processing pipeline
Task ID: osworld_multi_apps_media_image_010
Domain: multi_apps (os + vlc + python/pillow)
Scoring:
  - Component 1: Python script exists at /home/user/scripts/process_images.py (0.20)
  - Component 2: 10 processed JPEG images exist in /home/user/pictures/processed/
                 with correct resize (max dim <= 1920px, aspect ratio preserved) (0.30)
  - Component 3: Watermark 'Copyright 2024' visible in bottom-right corner of
                 processed images (white text on dark background) (0.20)
  - Component 4: M3U playlist at /home/user/pictures/slideshow.m3u with 10 entries,
                 each set to display for 3 seconds, pointing to processed/ dir (0.30)
Total: 1.00
"""

import os
from PIL import Image

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_010'

RAW_DIR = '/home/user/pictures/raw'
PROCESSED_DIR = '/home/user/pictures/processed'
SCRIPT_PATH = '/home/user/scripts/process_images.py'
PLAYLIST_PATH = '/home/user/pictures/slideshow.m3u'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: raw directory must exist with JPEG files
    try:
        raw_files = sorted([f for f in os.listdir(RAW_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
        if len(raw_files) == 0:
            print("CRITICAL: No JPEG files in raw directory — cannot verify task")
            print("REWARD: 0.0")
            return 0.0
        print(f"PRECONDITION: Found {len(raw_files)} raw JPEG files")
    except Exception as e:
        print(f"CRITICAL: Cannot access raw directory {RAW_DIR}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------
    # Component 1: Python script exists at /home/user/scripts/process_images.py (0.20 points)
    # -------------------------------------------------------------------
    try:
        if os.path.isfile(SCRIPT_PATH):
            # Also verify it's a non-empty Python file
            size = os.path.getsize(SCRIPT_PATH)
            if size > 50:
                print(f"PASS: Component 1 — process_images.py exists at {SCRIPT_PATH} ({size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Script file too small ({size} bytes), likely empty")
        else:
            print(f"FAIL: Component 1 — Script not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: 10 processed JPEG images with correct resize (0.30 points)
    # All 10 images must exist AND have max dimension <= 1920px
    # -------------------------------------------------------------------
    try:
        if not os.path.isdir(PROCESSED_DIR):
            print(f"FAIL: Component 2 — Processed directory not found: {PROCESSED_DIR}")
        else:
            processed_files = sorted([f for f in os.listdir(PROCESSED_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            expected_count = len(raw_files)

            if len(processed_files) < expected_count:
                print(f"FAIL: Component 2 — Expected {expected_count} processed files, found {len(processed_files)}")
            else:
                # Verify dimensions: max dimension must be <= 1920px
                resize_pass = 0
                resize_fail = 0
                valid_jpeg = 0
                for fname in processed_files:
                    proc_path = os.path.join(PROCESSED_DIR, fname)
                    try:
                        img = Image.open(proc_path)
                        # Verify it's a valid JPEG
                        if img.format == 'JPEG' or img.format is None:
                            valid_jpeg += 1
                        w, h = img.size
                        max_dim = max(w, h)
                        if max_dim <= 1920:
                            resize_pass += 1
                        else:
                            resize_fail += 1
                            print(f"  FAIL: {fname} has max dim {max_dim} > 1920px (size={w}x{h})")
                    except Exception as img_e:
                        print(f"  ERROR: Cannot open {fname}: {img_e}")

                if resize_pass == expected_count and len(processed_files) == expected_count:
                    print(f"PASS: Component 2 — All {expected_count} processed images exist with max dim <= 1920px (0.30 pts)")
                    total_score += 0.30
                elif resize_pass > 0:
                    comp2_partial = round(0.30 * (resize_pass / expected_count), 2)
                    print(f"PARTIAL: Component 2 — {resize_pass}/{expected_count} images correctly resized ({comp2_partial} pts)")
                    if comp2_partial > 0:
                        total_score += comp2_partial
                else:
                    print(f"FAIL: Component 2 — No correctly resized images found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: Watermark 'Copyright 2024' visible in bottom-right corner (0.20 points)
    # Watermark = white text on dark (black) background in bottom-right
    # Detection: look for black rectangle pixels in bottom-right 200x60 area
    # -------------------------------------------------------------------
    try:
        if not os.path.isdir(PROCESSED_DIR):
            print(f"FAIL: Component 3 — Processed directory not found")
        else:
            processed_files = sorted([f for f in os.listdir(PROCESSED_DIR) if f.lower().endswith(('.jpg', '.jpeg'))])
            if len(processed_files) == 0:
                print(f"FAIL: Component 3 — No processed files to check for watermark")
            else:
                watermark_pass = 0
                watermark_fail = 0
                for fname in processed_files:
                    proc_path = os.path.join(PROCESSED_DIR, fname)
                    try:
                        img = Image.open(proc_path).convert('RGB')
                        w, h = img.size
                        # Check bottom-right 250x80 area for black background pixels
                        # (the watermark has a black rectangle behind white text)
                        check_w = min(250, w)
                        check_h = min(80, h)
                        corner = img.crop((w - check_w, h - check_h, w, h))
                        pixels = list(corner.getdata())
                        # Count dark pixels (black background of watermark box)
                        dark_pixels = sum(1 for r, g, b in pixels if r < 60 and g < 60 and b < 60)
                        # Count bright pixels (white text of watermark)
                        bright_pixels = sum(1 for r, g, b in pixels if r > 200 and g > 200 and b > 200)
                        total_pixels = len(pixels)
                        # Watermark has both dark background and white text
                        if dark_pixels > 50 and bright_pixels > 50:
                            watermark_pass += 1
                        else:
                            watermark_fail += 1
                            print(f"  FAIL: {fname} — dark_px={dark_pixels}, bright_px={bright_pixels} in corner")
                    except Exception as img_e:
                        print(f"  ERROR: Cannot check watermark in {fname}: {img_e}")

                if watermark_pass == len(processed_files):
                    print(f"PASS: Component 3 — Watermark detected in all {watermark_pass} processed images (0.20 pts)")
                    total_score += 0.20
                elif watermark_pass > len(processed_files) // 2:
                    comp3_partial = round(0.20 * (watermark_pass / len(processed_files)), 2)
                    print(f"PARTIAL: Component 3 — Watermark detected in {watermark_pass}/{len(processed_files)} images ({comp3_partial} pts)")
                    if comp3_partial > 0:
                        total_score += comp3_partial
                else:
                    print(f"FAIL: Component 3 — Watermark not detected in {watermark_fail} of {len(processed_files)} images")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: M3U playlist exists with 10 entries at 3 seconds each,
    #              pointing to /home/user/pictures/processed/ (0.30 points)
    # -------------------------------------------------------------------
    try:
        if not os.path.isfile(PLAYLIST_PATH):
            print(f"FAIL: Component 4 — Playlist not found at {PLAYLIST_PATH}")
        else:
            with open(PLAYLIST_PATH, 'r') as f:
                content = f.read()

            lines = content.strip().split('\n')

            # Check for EXTM3U header
            has_header = lines[0].strip() == '#EXTM3U'
            if not has_header:
                print(f"WARN: Component 4 — Missing #EXTM3U header (first line: '{lines[0]}')")

            # Extract EXTINF lines and file path lines
            extinf_lines = [l.strip() for l in lines if l.strip().startswith('#EXTINF:')]
            file_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]

            entry_count = len(file_lines)
            extinf_count = len(extinf_lines)

            # Verify 10 entries
            expected_entries = len(raw_files)
            count_ok = (entry_count == expected_entries)

            # Verify each EXTINF has duration == 3
            duration_ok_count = 0
            duration_fail_count = 0
            for extinf in extinf_lines:
                try:
                    # Format: #EXTINF:<duration>,<title>
                    duration_str = extinf.split(':')[1].split(',')[0].strip()
                    duration_val = float(duration_str)
                    if duration_val == 3.0:
                        duration_ok_count += 1
                    else:
                        duration_fail_count += 1
                        print(f"  FAIL: EXTINF duration={duration_val}, expected 3")
                except Exception as parse_e:
                    duration_fail_count += 1
                    print(f"  ERROR: Parsing EXTINF '{extinf}': {parse_e}")

            # Verify all file paths point to processed/ dir
            paths_ok = sum(1 for fl in file_lines if '/home/user/pictures/processed/' in fl)

            print(f"  Playlist entries: {entry_count} (expected {expected_entries})")
            print(f"  Duration=3s entries: {duration_ok_count}/{extinf_count}")
            print(f"  Paths in processed/: {paths_ok}/{entry_count}")

            if count_ok and duration_ok_count == expected_entries and paths_ok == expected_entries:
                print(f"PASS: Component 4 — M3U playlist has {entry_count} entries with 3s duration each, all pointing to processed/ (0.30 pts)")
                total_score += 0.30
            elif count_ok and duration_ok_count > 0:
                # Partial: count is right but some durations wrong
                comp4_partial = round(0.30 * 0.7 + 0.30 * 0.3 * (duration_ok_count / expected_entries), 2)
                print(f"PARTIAL: Component 4 — Playlist has correct count but {duration_fail_count} incorrect durations ({comp4_partial} pts)")
                if comp4_partial > 0:
                    total_score += comp4_partial
            elif entry_count > 0 and entry_count < expected_entries:
                comp4_partial = round(0.30 * (entry_count / expected_entries), 2)
                print(f"PARTIAL: Component 4 — Playlist has {entry_count}/{expected_entries} entries ({comp4_partial} pts)")
                if comp4_partial > 0:
                    total_score += comp4_partial
            else:
                print(f"FAIL: Component 4 — Playlist verification failed: count={entry_count}, duration_ok={duration_ok_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------
    # Final score
    # -------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
