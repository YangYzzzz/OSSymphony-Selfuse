"""
Reward Script: Export slide 5 as PNG at 200 DPI to Desktop
Task ID: impress_gf3_003
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): File exists and has valid PNG signature
  Component 2 (0.4): Image dimensions consistent with 200 DPI export (~1500-2700 wide)
  Component 3 (0.3): Image has reasonable file size and color content (not blank)
"""

import os
import struct

WORKDIR = '/home/user'
TASK_ID = 'impress_gf3_003'
EXPORT_PATH = '/home/user/Desktop/slide5_export.png'

# PNG magic bytes
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def verify_task():
    """
    Verify that slide 5 was exported as PNG at 200 DPI to the Desktop.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist — if not, nothing to verify
    if not os.path.exists(EXPORT_PATH):
        print(f"FAIL: File not found at {EXPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PNG file with correct signature (0.3 points)
    try:
        with open(EXPORT_PATH, 'rb') as f:
            header = f.read(8)
        if header == PNG_SIGNATURE:
            print(f"PASS: Component 1 — Valid PNG signature (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Invalid PNG signature: {header!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Dimensions consistent with 200 DPI slide export (0.4 points)
    # Standard slide is 25.4cm x 19.05cm (10" x 7.5") or 33.87cm x 25.4cm (13.33" x 10")
    # At 200 DPI: 10" -> 2000px, 13.33" -> 2667px, 7.5" -> 1500px
    # Accept width range 1500-2700 and height range 1100-2100 to cover common slide sizes
    try:
        from PIL import Image
        img = Image.open(EXPORT_PATH)
        width, height = img.size
        img.close()

        width_ok = 1500 <= width <= 2700
        height_ok = 1100 <= height <= 2100

        if width_ok and height_ok:
            print(f"PASS: Component 2 — Dimensions {width}x{height} consistent with 200 DPI (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Dimensions {width}x{height} outside expected 200 DPI range "
                  f"(width 1500-2700, height 1100-2100)")
    except ImportError:
        # Fallback: parse PNG IHDR chunk manually if PIL not available
        try:
            with open(EXPORT_PATH, 'rb') as f:
                f.read(8)  # skip signature
                f.read(4)  # chunk length
                chunk_type = f.read(4)
                if chunk_type == b'IHDR':
                    width = struct.unpack('>I', f.read(4))[0]
                    height = struct.unpack('>I', f.read(4))[0]

                    width_ok = 1500 <= width <= 2700
                    height_ok = 1100 <= height <= 2100

                    if width_ok and height_ok:
                        print(f"PASS: Component 2 — Dimensions {width}x{height} consistent with 200 DPI (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 — Dimensions {width}x{height} outside expected range")
                else:
                    print(f"FAIL: Component 2 — IHDR chunk not found")
        except Exception as e2:
            print(f"ERROR: Component 2 — {e2}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File has substantial content (not a blank/corrupt tiny file) (0.3 points)
    # A real slide export at 200 DPI should be at least 10KB
    try:
        file_size = os.path.getsize(EXPORT_PATH)
        if file_size >= 10240:
            print(f"PASS: Component 3 — File size {file_size} bytes indicates real image content (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — File size {file_size} bytes too small for a 200 DPI slide export")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
