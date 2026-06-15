"""
Reward Script: Extract audio from MP4 to MP3 at 128 kbps using VLC CLI
Task ID: vlcconv_015
Domain: vlc
Scoring:
  Component 1 (0.20): Output directory exists and contains the output file
  Component 2 (0.25): Output file is a valid MP3 (starts with ID3 tag or MPEG sync word, and contains MP3 frames)
  Component 3 (0.30): Bitrate is approximately 128 kbps (within +-32 kbps tolerance)
  Component 4 (0.25): Audio duration is close to source duration (~30 seconds, within +-5s)
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_015'
OUTPUT_DIR = os.path.join(WORKDIR, 'Documents', 'Lecture_Audio')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'Lecture_History_Ep7_audio.mp3')
SOURCE_FILE = os.path.join(WORKDIR, 'Videos', 'Lecture_History_Ep7.mp4')

# MP3 bitrate table for MPEG1 Layer3
BITRATE_TABLE_V1_L3 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
# MP3 sample rate table for MPEG1
SAMPLERATE_TABLE_V1 = [44100, 48000, 32000, 0]
# Samples per frame for MPEG1 Layer3
SAMPLES_PER_FRAME_V1_L3 = 1152


def skip_id3v2(f):
    """Skip ID3v2 tag if present. Returns offset after ID3 tag."""
    header = f.read(3)
    if header == b'ID3':
        f.read(3)  # version + flags
        size_bytes = f.read(4)
        # ID3v2 size is syncsafe integer
        size = (size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]
        f.seek(10 + size)
        return 10 + size
    else:
        f.seek(0)
        return 0


def find_first_mp3_frame(f, max_search=8192):
    """Find the first valid MP3 frame header. Returns (bitrate_kbps, sample_rate, frame_size) or None."""
    start_pos = f.tell()
    data = f.read(max_search)
    for i in range(len(data) - 4):
        if data[i] == 0xFF and (data[i + 1] & 0xE0) == 0xE0:
            # Potential sync word found
            b1 = data[i + 1]
            b2 = data[i + 2]

            # MPEG version: bits 4-3 of byte 1
            version_bits = (b1 >> 3) & 0x03
            # Layer: bits 2-1 of byte 1
            layer_bits = (b1 >> 1) & 0x03

            # We want MPEG1 (version_bits == 3) Layer3 (layer_bits == 1)
            # But also accept MPEG2 (version_bits == 2) and MPEG2.5 (version_bits == 0)
            if layer_bits == 0:  # reserved
                continue

            # Bitrate index: bits 7-4 of byte 2
            bitrate_idx = (b2 >> 4) & 0x0F
            # Sample rate index: bits 3-2 of byte 2
            srate_idx = (b2 >> 2) & 0x03

            if bitrate_idx == 0 or bitrate_idx == 15:  # free/bad
                continue
            if srate_idx == 3:  # reserved
                continue

            if version_bits == 3 and layer_bits == 1:
                # MPEG1 Layer3
                bitrate = BITRATE_TABLE_V1_L3[bitrate_idx]
                srate = SAMPLERATE_TABLE_V1[srate_idx]
            else:
                # For other versions, approximate
                # MPEG2/2.5 Layer3 bitrate table
                mpeg2_l3_bitrates = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]
                if layer_bits == 1:  # Layer 3
                    bitrate = mpeg2_l3_bitrates[bitrate_idx]
                else:
                    continue  # skip non-layer3 for simplicity

                if version_bits == 2:  # MPEG2
                    srate_table = [22050, 24000, 16000, 0]
                elif version_bits == 0:  # MPEG2.5
                    srate_table = [11025, 12000, 8000, 0]
                else:
                    continue
                srate = srate_table[srate_idx]

            if bitrate > 0 and srate > 0:
                # Padding bit
                padding = (b2 >> 1) & 0x01
                if version_bits == 3:  # MPEG1
                    frame_size = (144 * bitrate * 1000 // srate) + padding
                else:  # MPEG2/2.5
                    frame_size = (72 * bitrate * 1000 // srate) + padding

                f.seek(start_pos + i)
                return bitrate, srate, frame_size

    return None


def estimate_duration_from_filesize(file_size, audio_start_offset, bitrate_kbps):
    """Estimate MP3 duration from file size and bitrate."""
    audio_bytes = file_size - audio_start_offset
    if bitrate_kbps <= 0:
        return 0.0
    duration = audio_bytes * 8.0 / (bitrate_kbps * 1000.0)
    return duration


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output directory and file exist (0.20 points)
    # This checks that the agent created the directory AND the output file
    try:
        dir_exists = os.path.isdir(OUTPUT_DIR)
        file_exists = os.path.isfile(OUTPUT_FILE)
        file_size = os.path.getsize(OUTPUT_FILE) if file_exists else 0

        if dir_exists and file_exists and file_size > 1000:
            print(f"PASS: Component 1 -- Output dir and file exist, size={file_size} bytes (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- dir_exists={dir_exists}, file_exists={file_exists}, size={file_size}")
            # If file doesn't exist, no point checking further
            if not file_exists:
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: File is a valid MP3 with proper frame headers (0.25 points)
    try:
        with open(OUTPUT_FILE, 'rb') as f:
            id3_offset = skip_id3v2(f)
            frame_info = find_first_mp3_frame(f)

        if frame_info is not None:
            bitrate, srate, frame_size = frame_info
            print(f"PASS: Component 2 -- Valid MP3: bitrate={bitrate}kbps, srate={srate}Hz, frame_size={frame_size} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No valid MP3 frame header found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")
        frame_info = None

    # Component 3: Bitrate is approximately 128 kbps (0.30 points)
    # Tolerance: 96-160 kbps (128 +/- 32)
    try:
        if frame_info is not None:
            bitrate = frame_info[0]
            if 96 <= bitrate <= 160:
                print(f"PASS: Component 3 -- Bitrate {bitrate} kbps is within 128 +/- 32 kbps range (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- Bitrate {bitrate} kbps is outside acceptable range (96-160)")
        else:
            print(f"FAIL: Component 3 -- Cannot check bitrate, no valid frame found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Audio duration approximately matches source (~30 seconds, +-5s) (0.25 points)
    try:
        if frame_info is not None:
            bitrate = frame_info[0]
            file_size = os.path.getsize(OUTPUT_FILE)
            # Find audio data start offset
            with open(OUTPUT_FILE, 'rb') as f:
                audio_offset = skip_id3v2(f)

            duration = estimate_duration_from_filesize(file_size, audio_offset, bitrate)
            # Source is ~30 seconds; accept 25-35 seconds
            if 25.0 <= duration <= 35.0:
                print(f"PASS: Component 4 -- Duration ~{duration:.1f}s is within expected range 25-35s (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Duration ~{duration:.1f}s is outside expected range (25-35s)")
        else:
            print(f"FAIL: Component 4 -- Cannot estimate duration, no valid frame found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isfile(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()
