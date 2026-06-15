"""
Reward Script: Convert AVI files to MP4 (H.264 + AAC) using ffmpeg
Task ID: vlcconv_014
Domain: vlc
Scoring:
  Precondition gate: Source AVI files must exist in ~/Videos/Old_Recordings/ (0 pts, early exit if missing)
  Component 1: Output directory ~/Videos/Converted/ exists (0.1 pts)
  Component 2: All 5 MP4 files exist in ~/Videos/Converted/ with size > 0 (0.3 pts)
  Component 3: Each MP4 uses H.264 video codec (0.3 pts)
  Component 4: Each MP4 uses AAC audio codec (0.3 pts)
"""

import os
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_014'

SOURCE_DIR = os.path.join(WORKDIR, 'Videos', 'Old_Recordings')
OUTPUT_DIR = os.path.join(WORKDIR, 'Videos', 'Converted')

FILE_BASES = ['clip_01', 'clip_02', 'clip_03', 'clip_04', 'clip_05']


def get_codec(filepath, stream_type):
    """Use ffprobe to get codec_name for a given stream type (v:0 or a:0)."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-select_streams', stream_type,
             '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', filepath],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split('\n')[0].strip() if result.stdout.strip() else None
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: Source AVI files must still exist
    # This is true in both initial and golden envs, so it's a gate, not a scoring component.
    try:
        for base in FILE_BASES:
            avi_path = os.path.join(SOURCE_DIR, f'{base}.avi')
            if not os.path.isfile(avi_path):
                print(f"PRECONDITION FAIL: Source file missing: {avi_path}")
                print("REWARD: 0.0")
                return 0.0
        print("PRECONDITION: All 5 source AVI files present in Old_Recordings/")
    except Exception as e:
        print(f"PRECONDITION ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output directory ~/Videos/Converted/ exists (0.1 pts)
    # This directory does NOT exist in initial_env, only created by the task.
    try:
        if os.path.isdir(OUTPUT_DIR):
            print(f"PASS: Component 1 — Output directory {OUTPUT_DIR} exists (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Output directory {OUTPUT_DIR} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 MP4 files exist with size > 0 in ~/Videos/Converted/ (0.3 pts)
    # Partial credit: 0.06 per file found with size > 0
    try:
        mp4_valid = 0
        for base in FILE_BASES:
            mp4_path = os.path.join(OUTPUT_DIR, f'{base}.mp4')
            if os.path.isfile(mp4_path) and os.path.getsize(mp4_path) > 0:
                mp4_valid += 1
            else:
                print(f"FAIL: Component 2 — Missing or empty: {base}.mp4")
        if mp4_valid == 5:
            print(f"PASS: Component 2 — All 5 MP4 files found with size > 0 (0.3 pts)")
            total_score += 0.3
        elif mp4_valid > 0:
            partial = round(mp4_valid * 0.06, 2)
            print(f"PARTIAL: Component 2 — {mp4_valid}/5 valid MP4 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No valid MP4 files in {OUTPUT_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each MP4 uses H.264 video codec (0.3 pts)
    # Partial credit: 0.06 per file with correct video codec
    try:
        h264_count = 0
        for base in FILE_BASES:
            mp4_path = os.path.join(OUTPUT_DIR, f'{base}.mp4')
            if not os.path.isfile(mp4_path):
                continue
            vcodec = get_codec(mp4_path, 'v:0')
            if vcodec == 'h264':
                h264_count += 1
            else:
                print(f"FAIL: Component 3 — {base}.mp4 video codec is '{vcodec}', expected 'h264'")
        if h264_count == 5:
            print(f"PASS: Component 3 — All 5 MP4 files use H.264 video codec (0.3 pts)")
            total_score += 0.3
        elif h264_count > 0:
            partial = round(h264_count * 0.06, 2)
            print(f"PARTIAL: Component 3 — {h264_count}/5 files with H.264 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No files with H.264 video codec")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Each MP4 uses AAC audio codec (0.3 pts)
    # Partial credit: 0.06 per file with correct audio codec
    try:
        aac_count = 0
        for base in FILE_BASES:
            mp4_path = os.path.join(OUTPUT_DIR, f'{base}.mp4')
            if not os.path.isfile(mp4_path):
                continue
            acodec = get_codec(mp4_path, 'a:0')
            if acodec == 'aac':
                aac_count += 1
            else:
                print(f"FAIL: Component 4 — {base}.mp4 audio codec is '{acodec}', expected 'aac'")
        if aac_count == 5:
            print(f"PASS: Component 4 — All 5 MP4 files use AAC audio codec (0.3 pts)")
            total_score += 0.3
        elif aac_count > 0:
            partial = round(aac_count * 0.06, 2)
            print(f"PARTIAL: Component 4 — {aac_count}/5 files with AAC ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No files with AAC audio codec")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
