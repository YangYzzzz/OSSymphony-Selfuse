"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m finished tweaking the layers and need an editable copy for later. How do I save this project as “website_mockup.xcf” in GIMP?
Generated: 2025-09-01 12:19:30
Status: success
Model: o3
Total Steps: 5
"""

# Reward script for verifying that the GIMP project was saved
# as an editable XCF named "website_mockup.xcf" at the exact
# path provided in the task context.
#
# This script performs REAL verification using the gimpformats
# library – it loads the file, inspects its layer structure, and
# awards progressive score based on concrete evidence that the
# user produced an EDITABLE multi-layer XCF.
#
# STRICTLY follows anti-search rules: we reference the file via
# the given absolute path ONLY – no directory walking, globbing,
# or guessing.

import os
from gimpformats.gimpXcfDocument import GimpDocument

# 🔒 EXACT path from the task context (DO NOT SEARCH!)
XCF_PATH = "/tmp/website_mockup.xcf"

# Scoring weights – sum to 1.0 when all requirements are met
WEIGHTS = {
    "valid_format": 0.5,       # Loads successfully as a real XCF
    "multiple_layers": 0.3,    # ≥2 layers (retains editability)
    "non_bg_layer": 0.2        # At least one layer not named purely "Background"
}

def is_valid_xcf(path: str) -> bool:
    """Return True if file loads as a genuine XCF via gimpformats."""
    try:
        _ = GimpDocument(path)
        return True
    except Exception as e:
        print(f"✗ Not a valid XCF or failed to load: {e}")
        return False

def get_layers(doc):
    """Return the list of layers from a GimpDocument (handles internal attr)."""
    if hasattr(doc, "_layers"):
        return doc._layers
    if hasattr(doc, "layers"):
        return doc.layers  # pragma: no cover  # compat fallback
    return []

def verify_saved_project(path: str) -> float:
    print(f"🎯 Verifying saved GIMP project at: {path}")
    score = 0.0

    # -- Prerequisite: file existence (no points) ---------------------------
    if not os.path.exists(path):
        print("✗ File does not exist – task not completed")
        print("REWARD: 0.0")
        return 0.0
    print("✓ File exists (prerequisite – no points)")

    # -- Requirement 1: Valid XCF format ------------------------------------
    if is_valid_xcf(path):
        print("✓ File is a valid XCF and loads successfully")
        score += WEIGHTS["valid_format"]
        doc = GimpDocument(path)  # reuse for later checks
    else:
        print("✗ File is not a valid XCF – cannot be an editable copy")
        print(f"REWARD: {score}")
        return score  # cannot proceed further

    # -- Requirement 2: Multiple layers (editability) -----------------------
    layers = get_layers(doc)
    num_layers = len(layers)
    print(f"Layer count: {num_layers}")
    if num_layers >= 2:
        print("✓ Image contains multiple layers (editing info preserved)")
        score += WEIGHTS["multiple_layers"]
    else:
        print("✗ Only one layer – likely flattened (no points for multiple_layers)")

    # -- Requirement 3: At least one non-background layer -------------------
    non_bg_exists = any(layer.name.lower() != "background" for layer in layers)
    if non_bg_exists:
        print("✓ Found a non-background layer – project remains editable")
        score += WEIGHTS["non_bg_layer"]
    else:
        print("✗ No non-background layer found – may be flattened")

    # -- Final score ---------------------------------------------------------
    final_score = min(score, 1.0)  # safety cap
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification when script is run standalone
if __name__ == "__main__":
    verify_saved_project(XCF_PATH)
