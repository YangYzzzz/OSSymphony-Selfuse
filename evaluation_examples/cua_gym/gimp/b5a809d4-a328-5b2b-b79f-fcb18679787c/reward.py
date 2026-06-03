"""
FINAL REWARD SCRIPT - SUCCESS
Task: Need to batch-convert 120 PNG product shots to WebP at 1024 × 1024 px, WebP quality 80, and strip all metadata.
Generated: 2025-09-01 14:03:55
Status: success
Model: o3
Total Steps: 18
"""

# Reward Script: PNG → WebP Batch-Conversion Verification
# --------------------------------------------------------
# Verifies that the GIMP XCF at the *exact* path provided in the
# task context represents a COMPLETED state for the assignment:
# "Batch-convert 120 PNG product shots to WebP at 1024×1024 px,
#  WebP quality 80, strip all metadata."
#
# Scoring (progressive):
#   0.4 – Image dimensions are exactly 1024×1024 px
#   0.3 – File contains exactly ONE layer named "ProductShot_Final"
#   0.3 – No disallowed metadata parasites (EXIF/ICC/XMP, etc.)
# Returns float in [0.0, 1.0] and prints "REWARD: X.X".
# --------------------------------------------------------

from gimpformats.gimpXcfDocument import GimpDocument
import os, traceback

# 🔥  MANDATORY: USE THE EXACT PATH FROM CONTEXT – DO NOT SEARCH!
XCF_PATH = "/tmp/product_batch_conversion.xcf"

# Scoring weights
DIM_SCORE   = 0.4  # correct size
LAYER_SCORE = 0.3  # single final layer
META_SCORE  = 0.3  # metadata stripped
MAX_SCORE   = DIM_SCORE + LAYER_SCORE + META_SCORE  # 1.0


def verify_dimensions(doc):
    """Returns True if image is exactly 1024×1024 px."""
    # gimpformats exposes width/height; fall back to private attrs if needed
    width  = getattr(doc, 'width',  getattr(doc, '_width',  None))
    height = getattr(doc, 'height', getattr(doc, '_height', None))
    print(f"Image dimensions found: {width}×{height}")
    return width == 1024 and height == 1024


def verify_single_final_layer(doc):
    """Returns earned points (0, half, or full) for layer requirement."""
    layers = getattr(doc, '_layers', [])
    layer_count = len(layers)
    print(f"Layer count: {layer_count}")

    if layer_count != 1:
        print("✗ Expected exactly 1 layer")
        return 0.0

    layer_name = layers[0].name.strip() if hasattr(layers[0], 'name') else ''
    print(f"Top layer name: '{layer_name}'")

    if layer_name == 'ProductShot_Final':
        return LAYER_SCORE       # full credit
    else:
        print("⚠️  Layer name deviates from expected 'ProductShot_Final'")
        return LAYER_SCORE * 0.5  # partial credit


def verify_metadata_stripped(doc):
    """Returns META_SCORE if no disallowed parasites remain."""
    disallowed_prefixes = (
        'exif', 'icc', 'xmp', 'iptc', 'profile-icc',
        'gimp-metadata', 'xml'
    )
    parasites = getattr(doc, 'parasites', [])
    parasite_names = [p.name.lower() for p in parasites]
    print(f"Parasites present: {parasite_names}")

    offending = [n for n in parasite_names if n.startswith(disallowed_prefixes)]
    if offending:
        print(f"✗ Metadata parasites still present: {offending}")
        return 0.0
    return META_SCORE


def verify_task():
    print("🎯 Starting verification for PNG→WebP batch conversion task…")
    total = 0.0

    # File existence (no points – prerequisite)
    if not os.path.isfile(XCF_PATH):
        print(f"✗ XCF file not found at expected path: {XCF_PATH}")
        print(f"REWARD: {total}")
        return total

    # Load XCF
    try:
        doc = GimpDocument(XCF_PATH)
        print("✓ XCF file loaded successfully")
    except Exception as e:
        print("✗ Failed to load XCF file:")
        traceback.print_exc()
        print(f"REWARD: {total}")
        return total

    # 1) Dimension check
    if verify_dimensions(doc):
        total += DIM_SCORE
        print(f"✓ Dimension requirement met (+{DIM_SCORE})")
    else:
        print("✗ Dimension requirement NOT met (+0.0)")

    # 2) Layer check (progressive)
    layer_points = verify_single_final_layer(doc)
    total += layer_points
    print(f"Layer check awarded +{layer_points}")

    # 3) Metadata check
    meta_points = verify_metadata_stripped(doc)
    total += meta_points
    print(f"Metadata check awarded +{meta_points}")

    # Clamp score & output
    final_score = max(0.0, min(total, MAX_SCORE))
    print(f"Total score: {final_score}/{MAX_SCORE}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
