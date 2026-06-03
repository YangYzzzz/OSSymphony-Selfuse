"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 90 stubbornly shows up in Portrait, but the rest of my deck is meant to be widescreen. In LibreOffice Impress, what steps do I follow to switch that slide—and every other slide in this file—to Landscape orientation all at once?
Generated: 2025-09-10 15:46:10
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
from pptx import Presentation

def verify_landscape_widescreen(file_path: str) -> float:
    """Verify that the entire presentation is set to Landscape orientation
    with a widescreen (~16:9) aspect ratio.  
    Progressive scoring:  
      • 0.7 points – file is truly Landscape (width > height)  
      • +0.3 points – aspect‐ratio is within a typical widescreen range
        (1.6–1.9)
    The function prints detailed diagnostics and always returns a score
    between 0.0 and 1.0 (float).
    """
    MAX_SCORE = 1.0
    LANDSCAPE_POINTS = 0.7
    WIDESCREEN_POINTS = 0.3
    total_score = 0.0

    # 1) Basic existence check (no points awarded!)
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Attempt to load the PPTX
    try:
        prs = Presentation(file_path)
        slide_count = len(prs.slides)
        print(f"✓ Loaded presentation successfully with {slide_count} slides\n")
    except Exception as e:
        print(f"✗ Failed to load presentation: {e}")
        print("REWARD: 0.0")
        return 0.0  # Loading failure means task not completed

    # 3) Determine global slide size (applies to all slides)
    width = prs.slide_width  # EMU units
    height = prs.slide_height
    print(f"Slide page size (EMU): width = {width}, height = {height}")

    # 3a) Orientation check – MUST be landscape for any credit
    if width > height:
        print("✓ Presentation is in landscape orientation")
        total_score += LANDSCAPE_POINTS
    else:
        print("✗ Presentation is not in landscape orientation (portrait detected)")
        print(f"REWARD: {total_score}")
        return total_score  # Early return – cannot be widescreen if portrait

    # 3b) Aspect-ratio check for widescreen (approx. 16:9 ≈ 1.77)
    try:
        aspect_ratio = width / height
        print(f"Calculated aspect ratio: {aspect_ratio:.3f}")
        # Accept a small tolerance around 16:9 (1.6–1.9)
        if 1.6 <= aspect_ratio <= 1.9:
            print("✓ Aspect ratio is within widescreen range (≈16:9)")
            total_score += WIDESCREEN_POINTS
        else:
            print("✗ Aspect ratio is not in widescreen range – no extra points")
    except ZeroDivisionError:
        print("✗ Error: height is zero – cannot compute aspect ratio")

    # 4) Clamp final score to [0.0, 1.0]
    final_score = min(total_score, MAX_SCORE)

    # 5) Report & return
    print(f"\nFinal Score: {final_score}/{MAX_SCORE}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------------
# Execute verification when script is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Path provided in task context
    FILE_PATH = "/home/user/slide_90_stubbornly_shows_up_in_portrait_but_the_rest_of_my_deck_is_meant_to_be_widescreen_in_libreo_golden.pptx"
    verify_landscape_widescreen(FILE_PATH)

