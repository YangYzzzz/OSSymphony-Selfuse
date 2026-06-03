"""
FINAL REWARD SCRIPT - SUCCESS
Task: I left the default name on the active layer—please rename it to “New Layer.”
Generated: 2025-09-01 12:28:07
Status: success
Model: o3
Total Steps: 2
"""

"""
Reward Script for GIMP Task Verification
Task: The default-named active layer must be renamed exactly to "New Layer" in the file
       /tmp/rename_layer_task.xcf

Scoring Rules (progressive, 0.0-1.0):
1. 0.7 points  – a layer named exactly "New Layer" exists (primary requirement)
2. +0.3 points – bonus to reach 1.0 *only* if the file now contains exactly one layer and
                 that layer is the correctly renamed one (reflects typical starting file)
3. 0.3 points  – fallback partial credit if no exact match but a layer name contains the word
                 "new" (case-insensitive), recognising an incomplete attempt.

The script never awards points for:
• File existence / loading (prerequisite)
• Natural conditions (having layers, valid dimensions, etc.)

It complies with all anti-hacking rules – no hard-coded success, no filesystem search, real
inspection with gimpformats.
"""

from gimpformats.gimpXcfDocument import GimpDocument

# 🚨 MANDATORY: Use the EXACT path provided in the task context – DO NOT SEARCH!
XCF_FILE_PATH: str = "/tmp/rename_layer_task.xcf"


def verify_layer_renamed(file_path: str) -> float:
    """Verify that the active (and only) layer has been renamed to exactly 'New Layer'.

    Returns a float between 0.0 and 1.0 according to the progressive scoring rules.
    """
    print(f"🎯 Verifying GIMP task using provided file: {file_path}")

    # ---------- Prerequisite: load the XCF file ----------
    try:
        doc = GimpDocument(file_path)
        print("✓ XCF file loaded successfully (prerequisite – no points)")
    except Exception as e:
        print(f"✗ Failed to load XCF file: {e}")
        print("REWARD: 0.0")
        return 0.0  # Cannot proceed if file is unreadable

    # ---------- Gather layer information ----------
    layer_names = [layer.name for layer in doc._layers]
    print(f"Found layers ({len(layer_names)}): {layer_names}")

    total_score = 0.0  # Progressive score accumulator
    max_score = 1.0

    # ---------- Primary Requirement: exact name match ----------
    if "New Layer" in layer_names:
        print("✓ Layer named exactly 'New Layer' found (primary requirement – 0.7 pts)")
        total_score += 0.7
    else:
        print("✗ No layer exactly named 'New Layer' found")

    # ---------- Bonus for full completion ----------
    if len(layer_names) == 1 and layer_names[0] == "New Layer":
        print("✓ Only one layer and it is correctly named – awarding full score")
        total_score = max_score  # Overrides any previous partial score to full
    else:
        # ---------- Partial attempt detection ----------
        if total_score == 0.0 and any("new" in name.lower() for name in layer_names):
            print("• Detected layer partially renamed containing the word 'new' – partial credit 0.3 pts")
            total_score += 0.3

    # ---------- Finalise score ----------
    final_score = min(total_score, max_score)
    print(f"Calculated score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -------------------- Execute Verification --------------------
if __name__ == "__main__":
    verify_layer_renamed(XCF_FILE_PATH)

