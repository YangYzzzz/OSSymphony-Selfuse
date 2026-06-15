"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm laying out a 1200×628 px web banner (72 DPI) and need the headline text (Montserrat Bold 64 pt) to stand out. Could you show me how to give that text a #000000 drop shadow offset 6 px right and 6 px down, with a 10 px blur and 60 % opacity in GIMP?
Generated: 2025-09-01 13:34:38
Status: success
Model: o3
Total Steps: 17
"""

from gimpformats.gimpXcfDocument import GimpDocument
import subprocess
import tempfile
import os
from PIL import Image
import numpy as np

# 🚨 MANDATORY: use the exact path provided in the task context
XCF_PATH = "/tmp/web_banner_shadow.xcf"

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def export_layer_to_png(xcf_path: str, layer_name: str):
    """Export a single layer to a temporary PNG using xcf2png."""
    tmp_png = tempfile.mktemp(suffix=".png")
    try:
        result = subprocess.run(
            ["xcf2png", "-o", tmp_png, xcf_path, layer_name],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"✗ xcf2png failed for '{layer_name}': {result.stderr.strip()}")
            return None
        return tmp_png
    except FileNotFoundError:
        print("✗ xcftools (xcf2png) not installed in VM")
        return None


def bbox_from_png(png_path: str):
    """Return bounding-box (minX, minY, maxX, maxY) of non-transparent pixels."""
    img = Image.open(png_path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    coords = np.argwhere(alpha > 0)
    if coords.size == 0:
        return None
    ys, xs = coords[:, 0], coords[:, 1]
    return xs.min(), ys.min(), xs.max(), ys.max()


def mean_rgb_non_transparent(png_path: str):
    img = Image.open(png_path).convert("RGBA")
    arr = np.array(img)
    mask = arr[:, :, 3] > 0
    if not np.any(mask):
        return None
    rgb = arr[:, :, :3][mask]
    return rgb.mean(axis=0)

# ------------------------------------------------------------
# Main verification routine
# ------------------------------------------------------------

def verify_task():
    total_score = 0.0
    max_score = 1.0

    # ---------- Prerequisite: file exists & loads ----------
    if not os.path.exists(XCF_PATH):
        print("✗ XCF file not found at provided path")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = GimpDocument(XCF_PATH)
        print("✓ XCF loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load XCF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- Locate headline & shadow layers ----------
    headline_layer = None
    shadow_layer = None
    for layer in doc._layers:
        lname = layer.name.lower()
        if "headline" in lname:
            headline_layer = layer
        if "shadow" in lname:
            shadow_layer = layer

    if headline_layer:
        print(f"✓ Headline layer found: '{headline_layer.name}'")
    else:
        print("✗ Headline layer not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    if shadow_layer:
        print(f"✓ Drop shadow layer found: '{shadow_layer.name}'")
        # 0.2 points for having a separate drop-shadow layer
        total_score += 0.2
    else:
        print("✗ Drop shadow layer missing")

    # ---------- Check opacity of shadow layer ----------
    if shadow_layer:
        opacity = shadow_layer.opacity  # 0–1 range in gimpformats
        print(f"Shadow opacity: {opacity:.3f}")
        if 0.55 <= opacity <= 0.65:
            print("✓ Opacity within 60 % ± 5 %")
            total_score += 0.2
        else:
            print("✗ Opacity outside expected range (60 %)")

    # ---------- Pixel-level checks (offset & colour) ----------
    head_png = export_layer_to_png(XCF_PATH, headline_layer.name)
    shadow_png = export_layer_to_png(XCF_PATH, shadow_layer.name) if shadow_layer else None

    if head_png and shadow_png:
        bbox_head = bbox_from_png(head_png)
        bbox_shadow = bbox_from_png(shadow_png)
        if bbox_head and bbox_shadow:
            hx0, hy0, hx1, hy1 = bbox_head
            sx0, sy0, sx1, sy1 = bbox_shadow
            dx, dy = sx0 - hx0, sy0 - hy0
            print(f"Offset between shadow & text: dx={dx}px, dy={dy}px")

            # Offset accuracy (expected 6 px right & 6 px down)
            if 5 <= dx <= 7 and 5 <= dy <= 7:
                print("✓ Offset within 6 ± 1 px")
                total_score += 0.3
            else:
                print("✗ Offset incorrect – expected 6 px right/down")

            # Shadow colour – should be black (#000000)
            mean_rgb = mean_rgb_non_transparent(shadow_png)
            if mean_rgb is not None:
                print(f"Mean RGB of shadow: {mean_rgb}")
                if mean_rgb.max() < 50:  # very dark – close to black
                    print("✓ Shadow colour close to #000000")
                    total_score += 0.3
                else:
                    print("✗ Shadow colour not dark enough – not black")
        else:
            print("✗ Could not determine bounding boxes for layers")
    else:
        print("✗ Failed to export layers for pixel analysis")

    # Clean-up temporary files
    for tmp in [head_png, shadow_png]:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)

    if total_score > max_score:
        total_score = max_score

    print(f"Total score: {total_score}/{max_score}")
    print(f"REWARD: {total_score}")
    return total_score

# ------------------------------------------------------------------
# Execute verification when run as a script
# ------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()

