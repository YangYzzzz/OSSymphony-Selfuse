"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please change the 2 in "CO2" to a subscript in the summary line.
Generated: 2025-10-14 08:21:47
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
from docx import Document

"""
Reward Script for: "Please change the 2 in \"CO2\" to a subscript in the summary line."

This script verifies that, in the provided DOCX file, every occurrence of the
chemical formula “CO2” has the digit “2” formatted as a subscript **while** the
letters “C” and “O” remain **not** subscript.  
It awards:
 • 0.7 points once it detects at least one valid instance where the digit 2 is
   a subscript (or is the Unicode subscript character ‘₂’).  
 • An additional 0.3 points (for a total of 1.0) if, for that instance, *only*
   the “2” is subscript and the letters “C” and “O” are not.

Progressive scoring ensures partial credit if the subscript formatting is
partially correct.

The result is printed as “REWARD: X.X” where X.X ∈ [0.0, 1.0].
"""

FILE_PATH = (
    "/home/user/please_change_the_2_in_co2_to_a_subscript_in_the_summary_line.docx"
)


def analyze_document(file_path: str) -> float:
    """Analyze the DOCX file and compute the reward score."""

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load document: {e}")
        return 0.0  # No points if the document cannot be opened

    found_subscript2 = False          # At least one ‘2’ is subscript
    found_correct_only2_subscript = False  # Only ‘2’ is subscript, ‘CO’ are normal
    co2_instances_evaluated = 0      # Number of CO2 patterns inspected (debug info)

    # Iterate through every paragraph and its runs to capture character-level
    # subscript information.
    for para in doc.paragraphs:
        char_list = []  # List of tuples: (character, is_subscript?)
        for run in para.runs:
            is_sub = run.font.subscript is True
            for ch in run.text:
                char_list.append((ch, is_sub))

        # Scan a sliding window of three characters to locate the pattern "CO2".
        for i in range(len(char_list) - 2):
            ch_c, sub_c = char_list[i]
            ch_o, sub_o = char_list[i + 1]
            ch_2, sub_2 = char_list[i + 2]

            if (
                ch_c.upper() == "C"
                and ch_o.upper() == "O"
                and ch_2 in {"2", "₂", "\u2082"}
            ):
                co2_instances_evaluated += 1

                # CASE 1 – ‘₂’ literal character (already subscript by glyph)
                if ch_2 in {"₂", "\u2082"}:
                    found_subscript2 = True
                    if not sub_c and not sub_o:
                        found_correct_only2_subscript = True

                # CASE 2 – regular “2” but formatted with subscript property
                else:
                    if sub_2:  # The ‘2’ run has subscript formatting
                        found_subscript2 = True
                        if not sub_c and not sub_o:
                            found_correct_only2_subscript = True

    # Scoring logic -----------------------------------------------------------
    score = 0.0

    if found_subscript2:
        score += 0.7
        print("✓ Found at least one CO₂ instance where ‘2’ is subscript (0.7)")

        if found_correct_only2_subscript:
            score += 0.3
            print("✓ ‘C’ and ‘O’ are normal, only ‘2’ is subscript (additional 0.3)")
        else:
            print(
                "⚠️ ‘C’ and/or ‘O’ also formatted as subscript; partial credit only"
            )
    else:
        print("✗ No correctly subscripted ‘2’ found in any CO2 instance")

    score = min(score, 1.0)  # Safety cap
    print(f"Total score calculated: {score}")
    return score


def main() -> None:
    if not os.path.exists(FILE_PATH):
        print(f"✗ File does not exist: {FILE_PATH}")
        print("REWARD: 0.0")
        return

    reward = analyze_document(FILE_PATH)
    print(f"REWARD: {reward}")


if __name__ == "__main__":
    main()

