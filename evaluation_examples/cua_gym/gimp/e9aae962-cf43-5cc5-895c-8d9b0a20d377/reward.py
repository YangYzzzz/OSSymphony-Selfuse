"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m working on a 2400×3000 px poster at 300 DPI. Before I start flattening, please duplicate the active layer named “Color Grading” and rename the copy to “Color Grading backup.”
Generated: 2025-09-01 13:20:31
Status: success
Model: o3
Total Steps: 11
"""

# Reward verification script for GIMP task
# Task: Duplicate the active layer named “Color Grading” and rename the copy to “Color Grading backup”.
# File path is provided and must be used exactly as-is.

from gimpformats.gimpXcfDocument import GimpDocument
from hashlib import md5

# 🚨 CRITICAL: use the EXACT path from the task context – NO SEARCHING!
XCF_PATH = "/tmp/color_grading_poster.xcf"

def verify_task(xcf_path: str) -> float:
    """Verify that the Color Grading layer was duplicated and renamed correctly.

    Scoring (progressive up to 1.0):
      0.4  – duplicated layer named "Color Grading backup" exists
      0.1  – original layer "Color Grading" still present
      0.3  – pixel data of backup matches original (true duplicate)
      0.1  – layer dimensions equal original & full image size
      0.1  – image resolution is exactly 300 DPI (horizontal & vertical)
    """

    print(f"🎯 Verifying file at: {xcf_path}")
    total_score = 0.0
    max_score = 1.0

    # ---------- Load XCF (prerequisite, no points) ----------
    try:
        doc = GimpDocument(xcf_path)
        print("✓ Loaded XCF file")
    except Exception as e:
        print(f"✗ Failed to load XCF: {e}")
        return 0.0  # cannot continue verification

    # ---------- Basic info (no points, just context) ----------
    print(f"Image dimensions: {doc.width}x{doc.height}")
    print(f"Resolution: H={doc.horizontalResolution} dpi  V={doc.verticalResolution} dpi")

    # Build a quick lookup of layers by name
    layer_dict = {layer.name: layer for layer in doc._layers}
    layer_names = list(layer_dict.keys())
    print("Layers found:", layer_names)

    # ---------- Requirement 1: backup layer exists ----------
    backup_layer = layer_dict.get("Color Grading backup")
    if backup_layer:
        print("✓ Found duplicated layer \"Color Grading backup\" (0.4)")
        total_score += 0.4
    else:
        print("✗ Missing duplicated layer \"Color Grading backup\"")

    # ---------- Requirement 2: original layer retained ----------
    orig_layer = layer_dict.get("Color Grading")
    if orig_layer:
        print("✓ Original layer \"Color Grading\" present (0.1)")
        total_score += 0.1
    else:
        print("✗ Original layer \"Color Grading\" missing")

    # ---------- Requirement 3: backup matches original pixel data ----------
    if orig_layer and backup_layer:
        try:
            md_orig = md5(orig_layer._data).hexdigest()
            md_dup  = md5(backup_layer._data).hexdigest()
            if md_orig == md_dup:
                print("✓ Backup layer pixel data matches original (0.3)")
                total_score += 0.3
            else:
                print("✗ Backup layer pixel data differs from original")
        except Exception as e:
            print(f"✗ Error comparing layer data: {e}")

    # ---------- Requirement 4a: dimensions match ----------
    if orig_layer and backup_layer:
        if (
            orig_layer.width  == backup_layer.width  == doc.width and
            orig_layer.height == backup_layer.height == doc.height
        ):
            print("✓ Layer dimensions correct (0.1)")
            total_score += 0.1
        else:
            print("✗ Layer dimensions mismatch")

    # ---------- Requirement 4b: resolution 300 DPI ----------
    if (
        abs(doc.horizontalResolution - 300) < 0.01 and
        abs(doc.verticalResolution   - 300) < 0.01
    ):
        print("✓ Image resolution is 300 DPI (0.1)")
        total_score += 0.1
    else:
        print("✗ Image resolution not 300 DPI")

    # Cap at 1.0
    total_score = min(total_score, max_score)
    print(f"Total score: {total_score}/{max_score}")
    return total_score


# -------------------- Run Verification --------------------
reward = verify_task(XCF_PATH)
print(f"REWARD: {reward}")

