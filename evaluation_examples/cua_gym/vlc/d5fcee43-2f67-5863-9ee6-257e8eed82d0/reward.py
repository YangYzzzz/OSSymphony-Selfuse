"""
Reward Script: Convert Travel_Vlog_Paris.mp4 to AVI with MPEG-4 video, MP3 audio, 720p
Task ID: vlcconv_007
Domain: vlc
Scoring:
  Component 1: Output file exists and is AVI/RIFF container (0.2)
  Component 2: Video codec is MPEG-4 (0.25)
  Component 3: Audio codec is MP3 (0.25)
  Component 4: Video resolution is 720p (0.3)

Verification approach: Pure Python parsing of AVI RIFF headers (no subprocess).
AVI files use RIFF container format with 'AVI ' form type.
Video codec is in the 'strh'/'strf' chunks under 'strl' lists.
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_007'
OUTPUT_PATH = os.path.join(WORKDIR, 'Desktop', 'Travel_Vlog_Paris.avi')


def parse_avi_info(file_path):
    """
    Parse AVI file RIFF headers to extract container, codec, and resolution info.
    Returns dict with keys: is_avi, video_codec, audio_codec, width, height
    """
    result = {
        'is_avi': False,
        'video_codec': None,
        'audio_codec': None,
        'audio_format_tag': None,
        'width': 0,
        'height': 0,
    }

    with open(file_path, 'rb') as f:
        # Read RIFF header
        riff_id = f.read(4)
        if riff_id != b'RIFF':
            return result
        riff_size = struct.unpack('<I', f.read(4))[0]
        form_type = f.read(4)
        if form_type != b'AVI ':
            return result
        result['is_avi'] = True

        # Parse chunks within the RIFF AVI container
        # We need to find 'hdrl' list -> 'strl' lists -> 'strh' and 'strf' chunks
        end_pos = min(12 + riff_size, os.path.getsize(file_path))
        stream_index = 0

        def parse_chunks(start, end, depth=0):
            """Recursively parse RIFF chunks."""
            nonlocal stream_index
            pos = start
            current_stream_type = None

            while pos + 8 <= end:
                f.seek(pos)
                chunk_id = f.read(4)
                if len(chunk_id) < 4:
                    break
                chunk_size = struct.unpack('<I', f.read(4))[0]

                if chunk_id == b'LIST':
                    list_type = f.read(4)
                    if list_type in (b'hdrl', b'strl', b'movi', b'odml'):
                        if list_type == b'strl':
                            current_stream_type = None
                        parse_chunks(pos + 12, pos + 8 + chunk_size, depth + 1)
                        if list_type == b'strl':
                            stream_index += 1

                elif chunk_id == b'strh':
                    # Stream header: fccType (4 bytes) + fccHandler (4 bytes)
                    stream_type = f.read(4)  # 'vids' or 'auds'
                    handler = f.read(4)      # codec FourCC for video
                    current_stream_type = stream_type

                    if stream_type == b'vids':
                        # handler is the video codec FourCC
                        codec_str = handler.decode('ascii', errors='replace').strip('\x00').upper()
                        result['video_codec'] = codec_str

                elif chunk_id == b'strf':
                    # Stream format - depends on stream type from preceding strh
                    # For video (BITMAPINFOHEADER): biSize(4), biWidth(4), biHeight(4), biPlanes(2), biBitCount(2), biCompression(4)
                    # For audio (WAVEFORMATEX): wFormatTag(2), nChannels(2), nSamplesPerSec(4), ...
                    strf_data = f.read(min(chunk_size, 64))

                    # Determine stream type by checking what we saw in the preceding strh
                    # We check both video and audio patterns
                    if len(strf_data) >= 16:
                        # Try as BITMAPINFOHEADER (video)
                        bi_size = struct.unpack('<I', strf_data[0:4])[0]
                        if bi_size >= 40 and len(strf_data) >= 20:
                            width = struct.unpack('<i', strf_data[4:8])[0]
                            height = struct.unpack('<i', strf_data[8:12])[0]
                            # biCompression FourCC
                            compression = strf_data[16:20]

                            # If width/height look reasonable for video, treat as video
                            if 100 < abs(width) < 10000 and 100 < abs(height) < 10000:
                                if result['width'] == 0:
                                    result['width'] = abs(width)
                                    result['height'] = abs(height)
                                    # Also extract compression codec
                                    comp_str = compression.decode('ascii', errors='replace').strip('\x00').upper()
                                    if comp_str and result['video_codec'] is None:
                                        result['video_codec'] = comp_str

                    if len(strf_data) >= 2:
                        # Try as WAVEFORMATEX (audio)
                        format_tag = struct.unpack('<H', strf_data[0:2])[0]
                        # MP3 format tags: 0x0055 (MPEG Layer 3), 0x0050 (MPEG Layer 1/2)
                        if format_tag in (0x0055, 0x0050):
                            result['audio_format_tag'] = format_tag
                            if format_tag == 0x0055:
                                result['audio_codec'] = 'mp3'
                            elif format_tag == 0x0050:
                                result['audio_codec'] = 'mpeg_audio'

                # Move to next chunk (chunks are word-aligned)
                pos += 8 + chunk_size
                if chunk_size % 2 == 1:
                    pos += 1

        parse_chunks(12, end_pos)

    return result


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be non-trivially sized (at least 10KB)
    file_size = os.path.getsize(OUTPUT_PATH)
    if file_size < 10240:
        print(f"CRITICAL: Output file too small ({file_size} bytes), likely corrupt")
        print("REWARD: 0.0")
        return 0.0

    # Parse AVI headers
    try:
        info = parse_avi_info(OUTPUT_PATH)
        print(f"DEBUG: Parsed AVI info: {info}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse AVI headers: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: AVI container format (0.2 points)
    try:
        if info['is_avi']:
            print(f"PASS: Component 1 - AVI/RIFF container detected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - File is not a valid AVI/RIFF container")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Video codec is MPEG-4 (0.25 points)
    # MPEG-4 Part 2 FourCC values: FMP4, DIVX, XVID, MP4V, DX50, mp4v, fmp4
    try:
        video_codec = (info.get('video_codec') or '').upper()
        mpeg4_fourccs = {'FMP4', 'DIVX', 'XVID', 'MP4V', 'DX50', 'MP4S', 'MPEG4'}
        if video_codec in mpeg4_fourccs:
            print(f"PASS: Component 2 - MPEG-4 video codec detected (FourCC: {video_codec}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Expected MPEG-4 video codec, found FourCC: '{video_codec}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Audio codec is MP3 (0.25 points)
    # MP3 in AVI uses format tag 0x0055
    try:
        audio_codec = info.get('audio_codec', '')
        audio_tag = info.get('audio_format_tag')
        if audio_codec == 'mp3' or audio_tag == 0x0055:
            print(f"PASS: Component 3 - MP3 audio codec detected (tag: {hex(audio_tag) if audio_tag else 'N/A'}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Expected MP3 audio (tag 0x0055), found codec='{audio_codec}', tag={hex(audio_tag) if audio_tag else 'None'}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Resolution is 720p (0.3 points)
    try:
        height = info.get('height', 0)
        width = info.get('width', 0)
        if height == 720:
            print(f"PASS: Component 4 - 720p resolution detected ({width}x{height}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 - Expected height=720, found {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
