"""
FINAL REWARD SCRIPT - SUCCESS
Task: Keep italics at 12 but change their color to a dark gray (#444444) for clearer contrast.
Generated: 2025-10-14 06:56:57
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
from docx import Document
from docx.shared import RGBColor

"""
Reward Script: Verify that all italic text in the target DOCX that is 12-point size
has been recolored to dark gray (#444444).

Scoring:
  • 0.0  – No qualifying italic 12-pt runs found, or none correctly recolored
  • 0<x<1 – Proportion of italic 12-pt runs that have the correct color
  • 1.0  – Every italic 12-pt run is correctly colored #444444

Rationale: The task only concerns italics that remain at 12 pt while changing their
font color. Any other italics sizes (e.g., 14 pt) are ignored. Progressive scoring is
based solely on the fraction of qualifying runs that meet the color requirement.
"""

# ---- Constants -------------------------------------------------------------
SIZE_PT_TARGET = 12
EMU_PER_POINT = 12700                  # python-docx stores font size in EMU
SIZE_12PT_EMU = SIZE_PT_TARGET * EMU_PER_POINT  # 12 pt expressed in EMU
SIZE_TOLERANCE = 100                   # ±100 EMU ≈ 0.008 pt
TARGET_COLOR = RGBColor(0x44, 0x44, 0x44)  # Dark gray #444444

# ---- Helper functions ------------------------------------------------------

def effective_font_size(run):
    """Return the run's effective font size in EMU, considering style fallback."""
    if run.font.size is not None:
        return run.font.size
    if run.style and run.style.font and run.style.font.size is not None:
        return run.style.font.size
    return None


def effective_color(run):
    """Return the run's effective RGBColor, considering style fallback."""
    if run.font.color is not None and run.font.color.rgb is not None:
        return run.font.color.rgb
    if run.style and run.style.font and run.style.font.color and run.style.font.color.rgb is not None:
        return run.style.font.color.rgb
    return None

# ---- File location helper --------------------------------------------------

def locate_docx():
    """Locate the learner's edited .docx.
    Preference order:
      1. A file in /home/user/ that matches the task prefix and is NOT the golden file
      2. Any file that matches the prefix (possibly the golden one)
    """
    user_dir = "/home/user"
    prefix = "keep_italics_at_12_but_change_their_color_to_a_dark_gray_444444_for_clearer_contrast"
    candidates = [f for f in os.listdir(user_dir) if f.lower().startswith(prefix) and f.lower().endswith('.docx')]
    # Prefer a non-golden candidate
    for fname in candidates:
        if 'golden' not in fname.lower():
            return os.path.join(user_dir, fname)
    if candidates:
        return os.path.join(user_dir, candidates[0])
    return None

# ---- Core verification -----------------------------------------------------

def verify_task(doc_path):
    print(f"Verifying document: {doc_path}")
    try:
        doc = Document(doc_path)
    except Exception as e:
        print(f"✗ Could not open DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    total_target_runs = 0   # italic runs that are exactly 12 pt
    correct_color_runs = 0  # of those, how many are dark gray

    for para in doc.paragraphs:
        for run in para.runs:
            if not run.italic:
                continue  # Only assess italic text
            size = effective_font_size(run)
            if size is None:
                continue  # size unspecified; cannot grade
            if abs(size - SIZE_12PT_EMU) <= SIZE_TOLERANCE:
                total_target_runs += 1
                color = effective_color(run)
                if color == TARGET_COLOR:
                    correct_color_runs += 1
                else:
                    print(f"   ✗ Run '{run.text[:30]}' has size 12 pt but wrong color: {color}")

    print(f"Total italic 12 pt runs: {total_target_runs}")
    print(f"Correctly colored runs (#444444): {correct_color_runs}")

    if total_target_runs == 0:
        print("✗ No italic 12 pt runs found – nothing to grade")
        print("REWARD: 0.0")
        return 0.0

    # Progressive scoring
    score = round(correct_color_runs / total_target_runs, 2)
    print(f"Calculated score: {score}")
    print(f"REWARD: {score}")
    return score

# ---- Main entry point ------------------------------------------------------
if __name__ == "__main__":
    docx_path = locate_docx()
    if not docx_path or not os.path.exists(docx_path):
        print("✗ Could not locate the expected .docx file to verify.")
        print("REWARD: 0.0")
    else:
        verify_task(docx_path)

