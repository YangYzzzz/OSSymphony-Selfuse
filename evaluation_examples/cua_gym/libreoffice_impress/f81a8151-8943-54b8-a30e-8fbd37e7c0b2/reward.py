"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set Default Page Style margins: Top 2.0 cm, Bottom 2.0 cm, Left 3.0 cm, Right 3.0 cm.
Generated: 2025-10-17 07:05:43
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import re
import zipfile


def find_target_file():
    """Search the user home directory for the presentation created by the agent.
    We look for filenames that contain the task keywords and end with .pptx or .odp
    (prioritising .pptx if both exist)."""
    home = "/home/user"
    keyword = r"set_default_page_style_margins"
    candidates = []
    for fname in os.listdir(home):
        if re.search(keyword, fname, re.IGNORECASE) and (fname.endswith(".pptx") or fname.endswith(".odp")):
            candidates.append(os.path.join(home, fname))

    # Prioritise .pptx files because margin extraction logic is implemented for them.
    for cand in candidates:
        if cand.endswith(".pptx"):
            return cand
    return candidates[0] if candidates else None


# -----------------------------------------------------------------------------
# PPTX-specific helpers
# -----------------------------------------------------------------------------

def extract_margins_pptx(file_path):
    """Read ppt/presentation.xml inside the PPTX and extract the print-margin
    attributes (marginT, marginB, marginL, marginR).  Returns a dict mapping
    T/B/L/R → integer EMU values or an empty dict if not found."""
    margins = {}
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            xml_data = z.read("ppt/presentation.xml").decode("utf-8")
        for side in ("T", "B", "L", "R"):
            m = re.search(rf"margin{side}=\"(\d+)\"", xml_data)
            if m:
                margins[side] = int(m.group(1))
    except Exception as exc:
        print(f"✗ Error reading PPTX margins: {exc}")
    return margins


# -----------------------------------------------------------------------------
# Verification core
# -----------------------------------------------------------------------------

def verify_task():
    """Main verification routine.  Progressive scoring:
    0.25 points per correctly-set margin (Top, Bottom, Left, Right).
    Full 1.0 reward only if all four margins exactly match the specification."""
    max_score = 1.0
    total_score = 0.0

    file_path = find_target_file()
    if not file_path:
        print("✗ No presentation file matching task name found in /home/user")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found presentation: {file_path}")

    # ------------------------------------------------------------------
    # Extract margins depending on file type
    # ------------------------------------------------------------------
    if file_path.endswith(".pptx"):
        margins = extract_margins_pptx(file_path)
    else:
        # Only PPTX expected for this task; ODP support can be added if needed.
        margins = {}

    if not margins:
        print("✗ Unable to extract margin information from presentation")
        print("REWARD: 0.0")
        return 0.0

    print("Extracted margins (EMU units):", margins)

    # ------------------------------------------------------------------
    # Compute expected EMU values
    #   EMU per inch  = 914400
    #   1 inch        = 2.54 cm
    # Therefore EMU per cm = 914400 / 2.54
    # Task: Top 2 cm, Bottom 2 cm, Left 3 cm, Right 3 cm
    # ------------------------------------------------------------------
    emu_per_cm = 914400 / 2.54  # ≈ 360000 EMU per cm
    expected = {
        "T": int(round(2.0 * emu_per_cm)),   # 2 cm → 720000 EMU
        "B": int(round(2.0 * emu_per_cm)),   # 2 cm → 720000 EMU
        "L": int(round(3.0 * emu_per_cm)),   # 3 cm → 1080000 EMU
        "R": int(round(3.0 * emu_per_cm)),   # 3 cm → 1080000 EMU
    }
    print("Expected margins (EMU units):", expected)

    # ------------------------------------------------------------------
    # Scoring: 0.25 each margin
    # ------------------------------------------------------------------
    for side, exp_val in expected.items():
        found_val = margins.get(side)
        if found_val == exp_val:
            total_score += 0.25
            print(f"✓ Margin {side} correct ({found_val}) (+0.25)")
        else:
            print(f"✗ Margin {side} incorrect (found {found_val}, expected {exp_val}) (+0.0)")

    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -----------------------------------------------------------------------------
# Execute verification when script is run directly
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    verify_task()

