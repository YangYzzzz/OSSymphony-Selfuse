"""
Reward Script: Save terminal screenshot of 'netstat -tuln' output as 'open_ports.png' on the Desktop.
Task ID: osworld_multi_apps_terminal_screenshot_013
Domain: os (multi_apps / terminal screenshot)
Scoring:
  - Component 1: open_ports.png exists on Desktop and is a valid PNG image (0.4 pts)
  - Component 2: Image has terminal-like dark background (dark pixel ratio > 85%) (0.3 pts)
  - Component 3: Image contains multiple text line groups (at least 10 groups of bright pixels
                  consistent with netstat output rows) (0.3 pts)
Total: 1.0
"""

import os
import struct
import zlib

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_screenshot_013'
DESKTOP_PATH = f'{WORKDIR}/Desktop'
TARGET_FILE = f'{DESKTOP_PATH}/open_ports.png'


def read_png_metadata(file_path):
    """
    Read PNG metadata without external libraries.
    Returns (width, height, bit_depth, color_type) or raises on invalid PNG.
    """
    with open(file_path, 'rb') as f:
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            raise ValueError(f"Not a valid PNG file: invalid signature {signature[:4]}")
        # Read IHDR chunk
        length_bytes = f.read(4)
        chunk_length = struct.unpack('>I', length_bytes)[0]
        chunk_type = f.read(4)
        if chunk_type != b'IHDR':
            raise ValueError(f"Expected IHDR chunk, got {chunk_type}")
        ihdr_data = f.read(chunk_length)
        width = struct.unpack('>I', ihdr_data[0:4])[0]
        height = struct.unpack('>I', ihdr_data[4:8])[0]
        bit_depth = ihdr_data[8]
        color_type = ihdr_data[9]
        return width, height, bit_depth, color_type


def analyze_png_image(file_path):
    """
    Analyze PNG image properties using PIL (Pillow) if available,
    or fall back to basic struct-based analysis.
    Returns dict with analysis results.
    """
    result = {
        'width': 0,
        'height': 0,
        'dark_pixel_ratio': 0.0,
        'text_line_groups': 0,
        'mean_brightness': 0.0,
    }
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(file_path)
        img_rgb = img.convert('RGB')
        arr = np.array(img_rgb)
        result['width'] = arr.shape[1]
        result['height'] = arr.shape[0]
        # Dark pixel ratio: pixels where all channels < 60
        dark_mask = arr.mean(axis=2) < 60
        result['dark_pixel_ratio'] = float(dark_mask.mean())
        result['mean_brightness'] = float(arr.mean())
        # Count groups of text rows: rows with >20 pixels above brightness 120
        text_line_groups = 0
        in_text_group = False
        for row_idx in range(arr.shape[0]):
            bright_in_row = int((arr[row_idx, :, 0] > 120).sum())
            if bright_in_row > 20 and not in_text_group:
                text_line_groups += 1
                in_text_group = True
            elif bright_in_row <= 20:
                in_text_group = False
        result['text_line_groups'] = text_line_groups
        return result
    except ImportError:
        # PIL not available: fall back to basic struct-based PNG read for dimensions only
        try:
            w, h, _, _ = read_png_metadata(file_path)
            result['width'] = w
            result['height'] = h
        except Exception:
            pass
        return result
    except Exception as e:
        print(f"  WARN: PIL analysis failed: {e}")
        return result


def verify_task():
    """
    Verify task completion: screenshot of netstat -tuln output saved as open_ports.png on Desktop.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: open_ports.png exists on Desktop AND is a valid PNG (0.4 pts)
    # This is the primary task deliverable — the file must not have existed
    # in the initial state (no file was on Desktop before the task).
    # -------------------------------------------------------------------------
    try:
        file_exists = os.path.isfile(TARGET_FILE)
        if not file_exists:
            print(f"FAIL: Component 1 — open_ports.png not found at {TARGET_FILE}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Verify it is a valid PNG by checking the PNG magic bytes
        with open(TARGET_FILE, 'rb') as f:
            magic = f.read(8)
        is_valid_png = (magic == b'\x89PNG\r\n\x1a\n')

        file_size = os.path.getsize(TARGET_FILE)

        if is_valid_png and file_size > 1000:
            print(f"PASS: Component 1 — open_ports.png exists at Desktop, valid PNG, size={file_size} bytes (0.4 pts)")
            total_score += 0.4
        elif not is_valid_png:
            print(f"FAIL: Component 1 — file exists but is not a valid PNG (magic bytes: {magic[:4]})")
        else:
            print(f"FAIL: Component 1 — file exists but too small ({file_size} bytes), likely empty or corrupt")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Image has terminal-like dark background (dark pixel ratio > 85%) (0.3 pts)
    # Terminal screenshots have predominantly dark backgrounds.
    # A screenshot of netstat output in a terminal would be mostly dark.
    # This check FAILS on initial_env (no file) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        analysis = analyze_png_image(TARGET_FILE)
        dark_ratio = analysis.get('dark_pixel_ratio', 0.0)
        mean_brightness = analysis.get('mean_brightness', 255.0)

        if dark_ratio > 0.85:
            print(f"PASS: Component 2 — terminal dark background confirmed: dark_pixel_ratio={dark_ratio:.2%}, mean_brightness={mean_brightness:.1f} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected dark terminal background (>85% dark pixels), got dark_pixel_ratio={dark_ratio:.2%}, mean_brightness={mean_brightness:.1f}")
            print(f"  NOTE: A terminal screenshot should be mostly dark. This image appears too bright.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Image contains multiple text line groups (>=10 groups) (0.3 pts)
    # netstat -tuln output has multiple rows (header + several lines per protocol).
    # Terminal screenshots show structured text rows separated by dark gaps.
    # Requires at least 10 distinct text line groups to confirm meaningful output.
    # This check FAILS on initial_env (no file) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        analysis = analyze_png_image(TARGET_FILE)
        text_groups = analysis.get('text_line_groups', 0)

        if text_groups >= 10:
            print(f"PASS: Component 3 — found {text_groups} text line groups (>=10 required for netstat output) (0.3 pts)")
            total_score += 0.3
        elif text_groups >= 5:
            # Partial credit: some text is present but not enough for full netstat output
            print(f"PARTIAL: Component 3 — found {text_groups} text line groups (5-9, partial credit). netstat -tuln typically produces 10+ output rows.")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — found only {text_groups} text line groups, expected >=10 for netstat output")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
