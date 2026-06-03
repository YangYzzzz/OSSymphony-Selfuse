"""
FINAL REWARD SCRIPT - SUCCESS
Task: I just need to save the current logo layer (it’s exactly 512×512 px) as a transparent PNG called “logo.png”. How do I export only that active layer?
Generated: 2025-09-01 14:45:26
Status: success
Model: o3
Total Steps: 18
"""

import os
from PIL import Image
from gimpformats.gimpXcfDocument import GimpDocument

"""
Reward script for verifying the task:
"Save the current logo layer (exactly 512×512 px) as a transparent PNG called “logo.png”."

Verification logic (progressive scoring – max 1.0):
  • 0.5 – exported PNG matches size of 512×512 (or a 512×512 layer found in XCF)
  • 0.25 – exported PNG actually contains transparency (alpha channel with some <255 values)
  • 0.25 – exported PNG is not fully transparent (has at least one opaque pixel)

Forbidden patterns (hard-coding success, file searching, etc.) are strictly avoided.
The script uses ONLY the provided XCF path.
"""

# -------------------------------------------------
# CONSTANTS (MUST use exact path from task context)
# -------------------------------------------------
XCF_PATH = "/tmp/logo_export_task.xcf"  #  🚨 PROVIDED – do NOT search
PNG_PATH = "/tmp/logo.png"               #  expected export result

# -------------------------------------------------
# VERIFICATION FUNCTION
# -------------------------------------------------

def verify_logo_export(xcf_path: str, png_path: str) -> float:
    print("Checking task completion…")
    total_score = 0.0
    max_score   = 1.0

    # ----- 1) Load the XCF file (prerequisite, no points) -----
    try:
        doc = GimpDocument(xcf_path)
        print(f"✓ Loaded XCF file: {xcf_path}")
    except Exception as e:
        print(f"✗ Unable to load XCF file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate a 512×512 layer in the XCF (should be the logo layer)
    logo_layer = next((ly for ly in doc._layers if ly.width == 512 and ly.height == 512), None)
    if logo_layer:
        print(f"✓ Found 512×512 layer in XCF (layer name: '{logo_layer.name}')")
    else:
        print("✗ No 512×512 layer found – dimension check will default to 512×512 expectation")

    # ----- 2) Validate exported PNG file presence & integrity -----
    if not os.path.exists(png_path):
        print(f"✗ Expected PNG '{png_path}' not found")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found PNG: {png_path}")

    try:
        # `verify()` checks basic integrity, need reopen for pixel access afterwards
        Image.open(png_path).verify()
        img = Image.open(png_path)
        img.load()
        if img.format != 'PNG':
            raise ValueError(f"File format is {img.format}, expected PNG")
        print("✓ PNG is a valid, readable PNG file")
    except Exception as e:
        print(f"✗ PNG unreadable or invalid: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----- 3) Requirement #1 – correct dimensions (0.5) -----
    png_w, png_h = img.size
    expected_dims = (logo_layer.width, logo_layer.height) if logo_layer else (512, 512)
    if (png_w, png_h) == expected_dims:
        total_score += 0.5
        print("✓ PNG dimensions match expected logo layer (0.5 points)")
    else:
        print(f"✗ PNG dimensions {png_w}×{png_h} != expected {expected_dims} (0 points)")

    # Prepare RGBA for transparency/opacity checks
    rgba  = img.convert('RGBA')
    alpha = rgba.getchannel('A')
    min_a, max_a = alpha.getextrema()

    # ----- 4) Requirement #2 – transparency present (0.25) -----
    if 'A' in img.getbands() and min_a < 255:
        total_score += 0.25
        print("✓ PNG contains transparent pixels (0.25 points)")
    else:
        print("✗ PNG lacks transparency (0 points)")

    # ----- 5) Requirement #3 – visible content (not fully transparent) (0.25) -----
    if max_a > 0:
        total_score += 0.25
        print("✓ PNG has visible (non-transparent) pixels (0.25 points)")
    else:
        print("✗ PNG fully transparent (0 points)")

    # ----- Final score -----
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# -------------------------------------------------
# MAIN (executes when run as script)
# -------------------------------------------------
if __name__ == "__main__":
    verify_logo_export(XCF_PATH, PNG_PATH)
