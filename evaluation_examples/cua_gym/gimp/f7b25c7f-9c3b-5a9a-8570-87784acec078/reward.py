"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a folder of roughly 200 product photos (mixed JPEG and PNG). I need a 150 × 150 px thumbnail for each image, saved as JPEG at quality 85, with “_thumb” added right before the file extension. What’s the quickest way to batch-run this in GIMP?
Generated: 2025-09-01 15:00:46
Status: success
Model: o3
Total Steps: 5
"""

import os
from gimpformats.gimpXcfDocument import GimpDocument

# -------------------------------------------------------------
# Reward Script: 150×150 px Product Thumbnail Verification
# -------------------------------------------------------------
# Task to verify
#   • Canvas is 150 × 150 px (thumbnails size requirement)
#   • Every layer (representing individual thumbnails) is also 150 × 150 px
#   • Progressive scoring: 0.4 pts for correct canvas size, the remaining
#     0.6 pts distributed proportionally across all layers that meet the
#     required dimensions.
# -------------------------------------------------------------
# CRITICAL: use EXACT path provided in task context – NO searching!
# -------------------------------------------------------------
XCF_PATH = "/tmp/product_thumbnail_task.xcf"  # ← mandatory path from context


def verify_thumbnails(xcf_path: str) -> float:
    """Verify that the provided XCF contains 150×150 px thumbnails.

    Scoring:
      • 0.4 – Canvas is exactly 150×150 px
      • 0.6 – Pro-rata for layers that are each 150×150 px
    Returns a float from 0.0 to 1.0 (max).
    """

    max_score = 1.0
    score = 0.0

    # -----------------------
    # 1. Prerequisite checks
    # -----------------------
    if not os.path.exists(xcf_path):
        print("✗ XCF file missing at provided path – task failed")
        print("REWARD: 0.0")
        return 0.0

    try:
        print(f"🎯 Loading XCF from provided path: {xcf_path}")
        doc = GimpDocument(xcf_path)
    except Exception as e:
        print(f"✗ Unable to load XCF file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------
    # 2. Canvas size check
    # -----------------------
    width, height = doc.width, doc.height
    print(f"Image canvas size: {width}×{height}")
    if width == 150 and height == 150:
        print("✓ Canvas size is 150×150 (adds 0.4 points)")
        score += 0.4
    else:
        print("✗ Canvas size incorrect (no points for canvas)")

    # -----------------------
    # 3. Layer dimension check
    # -----------------------
    layers = doc._layers  # gimpformats uses _layers internally
    num_layers = len(layers)
    print(f"Found {num_layers} layer(s) in file")

    if num_layers == 0:
        print("✗ No layers present – cannot verify thumbnails")
        final = score  # might already have partial score for canvas
        print(f"REWARD: {final}")
        return final

    correct_layers = 0
    for layer in layers:
        if layer.width == 150 and layer.height == 150:
            correct_layers += 1
        else:
            print(f"   ✗ Layer '{layer.name}' is {layer.width}×{layer.height} (expected 150×150)")

    ratio = correct_layers / num_layers
    layer_score = 0.6 * ratio  # distribute remaining 0.6 proportionally
    score += layer_score

    print(f"✓ {correct_layers}/{num_layers} layers match 150×150 (adds {layer_score:.2f} points)")

    # -----------------------
    # 4. Final score
    # -----------------------
    final_score = min(score, max_score)
    print(f"Total score: {final_score:.2f}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_thumbnails(XCF_PATH)

