"""
Reward Script: Extract audio from MP4 and save as OGG Vorbis at 192 kbps
Task ID: vlcconv_005
Domain: vlc

Scoring:
  Component 1: OGG container format          (0.20)
  Component 2: Vorbis audio codec             (0.25)
  Component 3: Audio-only, no video streams   (0.20)
  Component 4: Bitrate ~192 kbps              (0.20)
  Component 5: Duration matches source        (0.15)
  Total:                                       1.00

Verification approach: Pure Python OGG/Vorbis header parsing using struct.
No subprocess or external tools. OGG page headers and Vorbis identification
header are parsed from raw bytes per the OGG and Vorbis specs.
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_005'

OUTPUT_PATH = os.path.join(WORKDIR, 'Desktop', 'Concert_Live_Audio.ogg')
SOURCE_PATH = os.path.join(WORKDIR, 'Videos', 'Concert_Live_2025.mp4')


def parse_ogg_vorbis_info(file_path):
    """
    Parse an OGG file to extract Vorbis identification header info.
    Returns dict with: is_ogg, is_vorbis, channels, sample_rate, bitrate_nominal,
    num_logical_streams, file_size, duration_samples (from last granule position).
    """
    info = {
        'is_ogg': False,
        'is_vorbis': False,
        'channels': 0,
        'sample_rate': 0,
        'bitrate_nominal': 0,
        'num_logical_streams': set(),
        'file_size': 0,
        'last_granule': 0,
        'has_video_stream': False,
    }

    try:
        info['file_size'] = os.path.getsize(file_path)
    except Exception:
        return info

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception:
        return info

    # Parse OGG pages
    # OGG page header: "OggS" (4 bytes), version (1), header_type (1),
    # granule_position (8, little-endian int64), serial (4), page_seq (4),
    # checksum (4), num_segments (1), segment_table (num_segments bytes)
    pos = 0
    first_page_payloads = {}  # serial -> first page payload

    while pos < len(data) - 27:
        # Look for OggS sync
        if data[pos:pos+4] != b'OggS':
            pos += 1
            continue

        info['is_ogg'] = True

        # Parse page header
        version = data[pos+4]
        header_type = data[pos+5]
        granule_pos = struct.unpack_from('<q', data, pos+6)[0]
        serial = struct.unpack_from('<I', data, pos+14)[0]
        page_seq = struct.unpack_from('<I', data, pos+18)[0]
        num_segments = data[pos+26]

        info['num_logical_streams'].add(serial)

        # Track last granule position for duration estimation
        if granule_pos > 0 and granule_pos != -1:
            if granule_pos > info['last_granule']:
                info['last_granule'] = granule_pos

        # Read segment table
        seg_table_start = pos + 27
        if seg_table_start + num_segments > len(data):
            break
        segment_sizes = list(data[seg_table_start:seg_table_start + num_segments])

        # Compute payload size and start
        payload_start = seg_table_start + num_segments
        payload_size = sum(segment_sizes)

        if payload_start + payload_size > len(data):
            break

        payload = data[payload_start:payload_start + payload_size]

        # Store first page payload for each stream (BOS pages)
        if header_type & 0x02:  # BOS (beginning of stream)
            first_page_payloads[serial] = payload

        # Move to next page
        pos = payload_start + payload_size

    # Analyze first page payloads to identify codecs
    for serial, payload in first_page_payloads.items():
        # Check for Vorbis identification header
        # Starts with: packet_type (1 byte, 0x01), "vorbis" (6 bytes)
        if len(payload) >= 30 and payload[0:7] == b'\x01vorbis':
            info['is_vorbis'] = True
            # Vorbis identification header fields (after the 7-byte header):
            # vorbis_version (4), channels (1), sample_rate (4),
            # bitrate_maximum (4), bitrate_nominal (4), bitrate_minimum (4)
            vorbis_version = struct.unpack_from('<I', payload, 7)[0]
            channels = payload[11]
            sample_rate = struct.unpack_from('<I', payload, 12)[0]
            bitrate_max = struct.unpack_from('<i', payload, 16)[0]
            bitrate_nominal = struct.unpack_from('<i', payload, 20)[0]
            bitrate_min = struct.unpack_from('<i', payload, 24)[0]

            info['channels'] = channels
            info['sample_rate'] = sample_rate
            info['bitrate_nominal'] = bitrate_nominal

        # Check for Theora video header (starts with 0x80 "theora")
        if len(payload) >= 7 and payload[0:7] == b'\x80theora':
            info['has_video_stream'] = True

        # Check for other video codecs (e.g., dirac starts with "BBCD")
        if len(payload) >= 4 and payload[0:4] == b'BBCD':
            info['has_video_stream'] = True

    # Convert set to count
    info['num_logical_streams'] = len(info['num_logical_streams'])

    return info


def get_mp4_duration_approx(file_path):
    """
    Estimate MP4 duration by parsing the moov/mvhd atom.
    Returns duration in seconds or None.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception:
        return None

    # Search for 'mvhd' atom
    idx = data.find(b'mvhd')
    if idx < 0:
        return None

    try:
        # mvhd layout after 'mvhd' tag (4 bytes):
        # version (1 byte) + flags (3 bytes) = 4 bytes
        # Then for version 0: creation_time(4), modification_time(4), timescale(4), duration(4)
        # Then for version 1: creation_time(8), modification_time(8), timescale(4), duration(8)
        version = data[idx + 4]
        base = idx + 8  # skip 'mvhd' (already at idx) + version(1) + flags(3)
        if version == 0:
            timescale = struct.unpack_from('>I', data, base + 8)[0]
            duration_units = struct.unpack_from('>I', data, base + 12)[0]
        else:
            timescale = struct.unpack_from('>I', data, base + 16)[0]
            duration_units = struct.unpack_from('>Q', data, base + 20)[0]

        if timescale > 0:
            return duration_units / timescale
    except Exception:
        pass

    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: output file must be non-empty
    file_size = os.path.getsize(OUTPUT_PATH)
    if file_size == 0:
        print(f"CRITICAL: Output file is empty: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the OGG file
    ogg_info = parse_ogg_vorbis_info(OUTPUT_PATH)
    print(f"INFO: Parsed OGG info: is_ogg={ogg_info['is_ogg']}, is_vorbis={ogg_info['is_vorbis']}, "
          f"channels={ogg_info['channels']}, sample_rate={ogg_info['sample_rate']}, "
          f"bitrate_nominal={ogg_info['bitrate_nominal']}, streams={ogg_info['num_logical_streams']}, "
          f"has_video={ogg_info['has_video_stream']}, file_size={ogg_info['file_size']}")

    # Component 1: OGG container format (0.20 points)
    try:
        if ogg_info['is_ogg']:
            print(f"PASS: Component 1 - OGG container format detected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - File is not in OGG format")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Vorbis audio codec (0.25 points)
    try:
        if ogg_info['is_vorbis']:
            print(f"PASS: Component 2 - Vorbis audio codec detected (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - No Vorbis identification header found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Audio-only, no video streams (0.20 points)
    try:
        if not ogg_info['has_video_stream'] and ogg_info['is_vorbis']:
            print(f"PASS: Component 3 - Audio-only file, {ogg_info['num_logical_streams']} logical stream(s), no video (0.20 pts)")
            total_score += 0.20
        else:
            if ogg_info['has_video_stream']:
                print(f"FAIL: Component 3 - File contains video stream(s)")
            else:
                print(f"FAIL: Component 3 - No valid audio stream found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Bitrate approximately 192 kbps (0.20 points)
    # Check the nominal bitrate from Vorbis header (150k-240k range)
    try:
        bitrate = ogg_info['bitrate_nominal']
        bitrate_kbps = bitrate / 1000.0
        if 150.0 <= bitrate_kbps <= 240.0:
            print(f"PASS: Component 4 - Nominal bitrate {bitrate_kbps:.0f} kbps within 150-240 range (0.20 pts)")
            total_score += 0.20
        else:
            # Fallback: estimate from file size and duration
            if ogg_info['sample_rate'] > 0 and ogg_info['last_granule'] > 0:
                duration = ogg_info['last_granule'] / ogg_info['sample_rate']
                if duration > 0:
                    estimated_kbps = (ogg_info['file_size'] * 8) / (duration * 1000)
                    if 100.0 <= estimated_kbps <= 300.0:
                        print(f"FAIL: Component 4 - Nominal bitrate {bitrate_kbps:.0f} kbps out of range, "
                              f"but estimated bitrate {estimated_kbps:.0f} kbps (using file size/duration). "
                              f"Nominal header may not reflect -b:a flag accurately.")
                    else:
                        print(f"FAIL: Component 4 - Nominal bitrate {bitrate_kbps:.0f} kbps and estimated {estimated_kbps:.0f} kbps both out of 150-240 range")
                else:
                    print(f"FAIL: Component 4 - Nominal bitrate {bitrate_kbps:.0f} kbps out of 150-240 range")
            else:
                print(f"FAIL: Component 4 - Nominal bitrate {bitrate_kbps:.0f} kbps out of 150-240 range")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Duration matches source (0.15 points)
    # Compare OGG duration (from granule position) to MP4 source duration
    try:
        if ogg_info['sample_rate'] > 0 and ogg_info['last_granule'] > 0:
            ogg_duration = ogg_info['last_granule'] / ogg_info['sample_rate']

            source_duration = get_mp4_duration_approx(SOURCE_PATH)
            if source_duration is not None and source_duration > 0:
                duration_diff = abs(ogg_duration - source_duration)
                if duration_diff < 2.0:
                    print(f"PASS: Component 5 - OGG duration {ogg_duration:.1f}s matches source {source_duration:.1f}s (diff: {duration_diff:.2f}s) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 - OGG duration {ogg_duration:.1f}s differs from source {source_duration:.1f}s by {duration_diff:.1f}s")
            else:
                print(f"FAIL: Component 5 - Could not parse source MP4 duration for comparison")
        else:
            print(f"FAIL: Component 5 - Could not determine OGG duration (sample_rate={ogg_info['sample_rate']}, last_granule={ogg_info['last_granule']})")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
