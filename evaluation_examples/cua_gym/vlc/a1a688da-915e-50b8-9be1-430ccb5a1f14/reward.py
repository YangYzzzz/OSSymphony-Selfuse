"""
Reward Script: Extract audio from MP4 and save as FLAC
Task ID: vlcconv_006
Domain: vlc
Scoring:
  Component 1 (0.2): Output file exists at ~/Music/Meditation_Audio.flac
  Component 2 (0.3): File is valid FLAC format (magic bytes + codec name)
  Component 3 (0.2): Audio-only output (1 audio stream, 0 video streams)
  Component 4 (0.3): Audio properties match source (~30s duration, stereo, ~44100Hz)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_006'
OUTPUT_PATH = os.path.join(WORKDIR, 'Music', 'Meditation_Audio.flac')
SOURCE_PATH = os.path.join(WORKDIR, 'Videos', 'Meditation_Guide.mp4')


def get_ffprobe_info(file_path):
    """Use ffprobe via os.popen to get media file info as JSON dict."""
    cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams "{file_path}" 2>/dev/null'
    raw = os.popen(cmd).read()
    if not raw.strip():
        return None
    return json.loads(raw)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.2 points)
    # This is a task-introduced change: initial_env has no file here.
    try:
        if os.path.isfile(OUTPUT_PATH):
            file_size = os.path.getsize(OUTPUT_PATH)
            if file_size > 1000:  # Must be non-trivially sized (> 1KB)
                print(f"PASS: Component 1 - Output file exists at {OUTPUT_PATH}, size={file_size} bytes (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 - File exists but too small ({file_size} bytes), likely corrupt")
        else:
            print(f"FAIL: Component 1 - Output file not found at {OUTPUT_PATH}")
            # No file means nothing else can pass; return early
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Valid FLAC format (0.3 points)
    # Check magic bytes and ffprobe codec identification
    try:
        # Check FLAC magic bytes (first 4 bytes should be 'fLaC')
        with open(OUTPUT_PATH, 'rb') as f:
            magic = f.read(4)

        is_flac_magic = (magic == b'fLaC')

        # Also verify via ffprobe
        info = get_ffprobe_info(OUTPUT_PATH)
        format_name = ''
        if info and 'format' in info:
            format_name = info['format'].get('format_name', '')

        is_flac_format = ('flac' in format_name.lower())

        if is_flac_magic and is_flac_format:
            print(f"PASS: Component 2 - Valid FLAC (magic={magic}, format={format_name}) (0.3 pts)")
            total_score += 0.3
        elif is_flac_magic:
            print(f"PARTIAL: Component 2 - FLAC magic OK but format_name={format_name} (0.15 pts)")
            total_score += 0.15
        elif is_flac_format:
            print(f"PARTIAL: Component 2 - format_name OK but magic={magic} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Not FLAC (magic={magic}, format={format_name})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Audio-only (no video streams) (0.2 points)
    # The task extracts audio, so the output should have only audio streams
    try:
        if info and 'streams' in info:
            audio_streams = [s for s in info['streams'] if s.get('codec_type') == 'audio']
            video_streams = [s for s in info['streams'] if s.get('codec_type') == 'video']

            if len(audio_streams) >= 1 and len(video_streams) == 0:
                codec_name = audio_streams[0].get('codec_name', 'unknown')
                if codec_name == 'flac':
                    print(f"PASS: Component 3 - Audio-only, {len(audio_streams)} audio stream(s), codec={codec_name} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 - Audio codec is {codec_name}, expected flac")
            else:
                print(f"FAIL: Component 3 - Expected audio-only, found {len(audio_streams)} audio + {len(video_streams)} video streams")
        else:
            print(f"FAIL: Component 3 - Could not parse streams from ffprobe output")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Audio properties match source (0.3 points)
    # Duration ~30s, stereo (2 channels), sample rate ~44100Hz
    try:
        if info and 'streams' in info:
            audio_streams = [s for s in info['streams'] if s.get('codec_type') == 'audio']
            if audio_streams:
                stream = audio_streams[0]
                sub_score = 0.0

                # Duration check (~30s, allow tolerance of 2s)
                duration = float(info.get('format', {}).get('duration', 0))
                if 28.0 <= duration <= 32.0:
                    sub_score += 0.1
                    print(f"  Duration OK: {duration:.2f}s (expected ~30s)")
                else:
                    print(f"  Duration MISMATCH: {duration:.2f}s (expected ~30s)")

                # Channel count check (stereo = 2)
                channels = stream.get('channels', 0)
                if channels == 2:
                    sub_score += 0.1
                    print(f"  Channels OK: {channels} (stereo)")
                else:
                    print(f"  Channels MISMATCH: {channels} (expected 2/stereo)")

                # Sample rate check (44100Hz)
                sample_rate = int(stream.get('sample_rate', 0))
                if 44000 <= sample_rate <= 48100:
                    sub_score += 0.1
                    print(f"  Sample rate OK: {sample_rate}Hz")
                else:
                    print(f"  Sample rate MISMATCH: {sample_rate}Hz (expected ~44100)")

                if sub_score > 0:
                    print(f"PASS: Component 4 - Audio properties ({sub_score} pts)")
                    total_score += sub_score
                else:
                    print(f"FAIL: Component 4 - No audio properties matched")
            else:
                print(f"FAIL: Component 4 - No audio streams found")
        else:
            print(f"FAIL: Component 4 - No ffprobe info available")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
