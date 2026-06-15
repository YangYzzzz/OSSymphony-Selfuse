"""
FINAL REWARD SCRIPT - SUCCESS
Task: Switch the color of italic text to a deep navy (#003366) so it stands out from the black body text.
Generated: 2025-10-14 08:42:49
Status: success
Model: azure-o3
Total Steps: 3
"""

from docx import Document
import os


def rgb_to_hex(rgb_color):
    """Convert a python-docx RGBColor object to a lowercase hex string (e.g., '003366').
    Returns None if rgb_color is None."""
    if rgb_color is None:
        return None
    # str(RGBColor) already yields a 6-digit hex string without the leading '#'
    return str(rgb_color).lower()


def verify_italic_color(file_path: str, target_hex: str = "003366") -> float:
    """Verify that every italic run in the DOCX has the specified navy colour
    and that non-italic runs do *not* use that colour.

    Scoring (progressive):
    – 70 % of the score depends on the share of italic runs correctly coloured
    – 30 % depends on the share of non-italic runs that *avoid* the navy colour
    The final score is rounded to two decimals and capped at 1.0.
    """
    print(f"Verifying italic colour in document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not load DOCX: {e}")
        return 0.0

    target_hex = target_hex.lower().lstrip("#")

    # Counters
    total_italic = 0
    italic_correct = 0
    total_non_italic = 0
    non_italic_wrong_colour = 0

    for para in doc.paragraphs:
        for run in para.runs:
            # Determine italic status (explicit True or inherited via style)
            is_italic = False
            if run.italic is True:
                is_italic = True
            elif run.italic is None and run.style and run.style.font and run.style.font.italic:
                is_italic = True

            # Determine explicit colour on the run
            colour_hex = None
            if run.font.color and run.font.color.rgb is not None:
                colour_hex = rgb_to_hex(run.font.color.rgb)

            if is_italic:
                total_italic += 1
                if colour_hex == target_hex:
                    italic_correct += 1
            else:
                total_non_italic += 1
                if colour_hex == target_hex:
                    non_italic_wrong_colour += 1

    print(f"Total italic runs: {total_italic}")
    print(f"Italic runs with correct navy colour: {italic_correct}")
    print(f"Total non-italic runs: {total_non_italic}")
    print(f"Non-italic runs incorrectly using navy: {non_italic_wrong_colour}")

    if total_italic == 0:
        print("✗ No italic text found; cannot assess task completion")
        return 0.0

    # 70 % weighting for italic correctness
    italic_accuracy = italic_correct / total_italic
    italic_score = 0.7 * italic_accuracy
    print(f"Italic colour accuracy contribution: {italic_score:.2f}")

    # 30 % weighting for keeping non-italic text free from the navy colour
    if total_non_italic == 0:
        non_italic_accuracy = 1.0
    else:
        non_italic_accuracy = 1 - (non_italic_wrong_colour / total_non_italic)
    non_italic_score = 0.3 * non_italic_accuracy
    print(f"Non-italic colour correctness contribution: {non_italic_score:.2f}")

    final_score = round(min(italic_score + non_italic_score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    FILE_PATH = "/home/user/switch_the_color_of_italic_text_to_a_deep_navy_003366_so_it_stands_out_from_the_black_body_text.docx"
    verify_italic_color(FILE_PATH)

