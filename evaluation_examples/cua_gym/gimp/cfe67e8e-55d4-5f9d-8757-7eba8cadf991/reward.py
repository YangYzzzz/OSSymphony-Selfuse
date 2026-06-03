"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m ready to export this as a 2048×2048 px JPEG (quality 85). What’s the quickest way to merge all the layers I can see into one before I save?
Generated: 2025-09-01 13:50:44
Status: success
Model: o3
Total Steps: 4
"""

# Reward Script for verifying that all visible layers were merged into one in the given XCF file
# Task context:
#   The user needed to quickly merge all visible layers into a single layer before exporting
#   (target export 2048×2048 JPEG).  Verification focuses ONLY on the merge-visible step.
#
# MANDATORY RULES FOLLOWED:
#   • Uses EXACT provided path: /tmp/merge_visible_layers_task.xcf
#   • No filesystem searching (glob / os.walk etc.)
#   • Real verification with gimpformats (inspects layer structure)
#   • Progressive scoring (1.0 only if 100 % correct)
#   • No natural-condition points (file existence, basic load etc.)
#
# Scoring rubric:
#   0.7  – Exactly one VISIBLE layer present (means visible layers were merged)
#   0.3  – Only ONE total layer in file (all layers flattened, incl. hidden)
#   1.0  – Both conditions satisfied
#   (other combinations give 0.0–0.7 accordingly)

from gimpformats.gimpXcfDocument import GimpDocument
import sys

# 🚨 CRITICAL: Use the exact path supplied in context – DO NOT SEARCH! 🚨
XCF_PATH = "/tmp/merge_visible_layers_task.xcf"


def verify_merge_visible_layers(xcf_path: str) -> float:
    """Verify that all visible layers were merged into a single layer.

    Returns a progressive score between 0.0 and 1.0.
    """
    print(f"🎯 Loading XCF from context: {xcf_path}")

    try:
        doc = GimpDocument(xcf_path)  # prerequisite: must succeed
        print("✓ XCF file loaded successfully (prerequisite – no points awarded)")
    except Exception as e:
        print(f"✗ Unable to load XCF file: {e}")
        return 0.0  # cannot continue without loading

    # Basic image info (prerequisite, no points)
    print(f"Image dimensions: {doc.width}x{doc.height}")

    layers = doc._layers  # list of GimpLayer objects
    total_layers = len(layers)
    visible_layers = [ly for ly in layers if getattr(ly, "visible", True)]
    hidden_layers = [ly for ly in layers if not getattr(ly, "visible", True)]

    print(f"Total layers in file: {total_layers}")
    print(f"Visible layers: {len(visible_layers)} | Hidden layers: {len(hidden_layers)}")

    # Progressive scoring
    score = 0.0

    # Requirement 1 – Only ONE visible layer left → 0.7 pts
    if len(visible_layers) == 1:
        print("✓ Exactly one visible layer present → +0.7")
        score += 0.7
    else:
        print("✗ Multiple visible layers remain → +0.0")

    # Requirement 2 – Only ONE total layer in file (all flattened) → additional 0.3 pts
    if total_layers == 1:
        print("✓ File contains only one layer (flattened) → +0.3")
        score += 0.3
    else:
        print("⚠ Hidden/extra layers still exist → +0.0")

    final_score = min(score, 1.0)  # safety cap
    print(f"Reward score computed: {final_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_merge_visible_layers(XCF_PATH)
    print(f"REWARD: {reward}")
