"""
Reward Script: Export slide 1 as a JPEG image to the Desktop
Task ID: impstruct_040
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35) - cover.jpg exists and is a valid JPEG file
  Component 2 (0.35) - Image has correct landscape aspect ratio matching slide dimensions
  Component 3 (0.30) - Image has reasonable resolution and is not degenerate/corrupt
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impstruct_040'
DESKTOP_PATH = os.path.join(WORKDIR, 'Desktop')
EXPECTED_FILE = os.path.join(DESKTOP_PATH, 'cover.jpg')

# Slide dimensions from the pptx (in EMU): 9144000 x 6858000 => aspect ratio 4:3
SLIDE_ASPECT_RATIO = 9144000 / 6858000  # ~1.3333


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist at expected path
    if not os.path.exists(EXPECTED_FILE):
        print(f"CRITICAL: Expected file not found at {EXPECTED_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: cover.jpg is a valid JPEG image (0.35 points)
    # This FAILS on initial_env (file doesn't exist, caught above) and PASSES on golden_env
    try:
        from PIL import Image
        img = Image.open(EXPECTED_FILE)
        img.load()  # Force full load to detect corruption
        if img.format == 'JPEG':
            print(f"PASS: Component 1 - File is a valid JPEG image (format={img.format}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - File is not JPEG format, found: {img.format}")
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot open as image: {e}")

    # Component 2: Image has correct landscape aspect ratio matching the presentation slide (0.35 points)
    # The slide is 4:3 landscape (9144000 x 6858000 EMU). The exported image should have matching ratio.
    try:
        from PIL import Image
        img = Image.open(EXPECTED_FILE)
        width, height = img.size
        if width > 0 and height > 0:
            img_aspect = width / height
            # Allow 5% tolerance on aspect ratio
            ratio_diff = abs(img_aspect - SLIDE_ASPECT_RATIO) / SLIDE_ASPECT_RATIO
            if ratio_diff <= 0.05 and width > height:
                print(f"PASS: Component 2 - Landscape aspect ratio matches slide "
                      f"(img={img_aspect:.4f}, slide={SLIDE_ASPECT_RATIO:.4f}, diff={ratio_diff:.4f}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - Aspect ratio mismatch or not landscape "
                      f"(img={img_aspect:.4f}, slide={SLIDE_ASPECT_RATIO:.4f}, "
                      f"width={width}, height={height})")
        else:
            print(f"FAIL: Component 2 - Degenerate image dimensions: {width}x{height}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Image has reasonable resolution and is not degenerate (0.30 points)
    # A proper slide export should produce an image of at least 400x300 pixels and be RGB mode.
    try:
        from PIL import Image
        img = Image.open(EXPECTED_FILE)
        width, height = img.size
        file_size = os.path.getsize(EXPECTED_FILE)
        if width >= 400 and height >= 300 and img.mode in ('RGB', 'RGBA') and file_size > 1000:
            print(f"PASS: Component 3 - Resolution={width}x{height}, mode={img.mode}, "
                  f"size={file_size} bytes (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - Image may be degenerate: "
                  f"resolution={width}x{height}, mode={img.mode}, size={file_size} bytes")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
