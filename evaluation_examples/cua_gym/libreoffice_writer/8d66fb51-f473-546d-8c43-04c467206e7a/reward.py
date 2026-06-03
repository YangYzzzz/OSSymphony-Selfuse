"""
FINAL REWARD SCRIPT - SUCCESS
Task: I accidentally typed “colour” in British spelling throughout my draft, but for consistency I only need the American spelling in paragraphs 18 through 24. In LibreOffice Writer, what’s the quickest way to swap every single “colour” for “color” just within those seven paragraphs without touching the rest of the document?
Generated: 2025-09-10 19:01:26
Status: success
Model: azure-o3
Total Steps: 3
"""

"""
Reward script for verifying LibreOffice Writer task:
Task: Replace every instance of the British spelling "colour" with the American spelling
"color" ONLY in paragraphs 18 through 24, leaving all other paragraphs unchanged.

Scoring (progressive, 0.0–1.0):
  • Up to 0.5 pts – Each of paragraphs 18-24 contains at least one whole-word
    "color" and **no** occurrence of "colour" (pro-rated by how many satisfy this).
  • Up to 0.5 pts – Every paragraph outside 18-24 still contains at least one
    whole-word "colour" (i.e. was *not* altered).  Score is pro-rated likewise.

Only these two verifiable outcomes earn points.  File existence and loading give
no points – they are prerequisites.  The script relies on python-docx to read the
DOCX file and uses regex to ensure whole-word matching.
"""
import os
import re
from typing import List
from docx import Document

# Path to the document provided by the grader environment
FILE_PATH = "/home/user/i_accidentally_typed_colour_in_british_spelling_throughout_my_draft_but_for_consistency_i_only_need_.docx"

# Paragraph range that should be modified (1-based, inclusive)
INSIDE_START = 18
INSIDE_END = 24


def contains_word(word: str, text: str) -> bool:
    """Case-insensitive check for a whole word *word* inside *text*."""
    pattern = rf"\b{re.escape(word)}\b"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def verify_task(file_path: str) -> float:
    """Return a reward score between 0.0 and 1.0 based on task completion."""

    # ---------- Prerequisite: load the document ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs: List[str] = [p.text for p in doc.paragraphs]
    total_paras = len(paragraphs)
    print(f"Loaded document: {total_paras} paragraphs found")

    inside_indices = range(INSIDE_START, INSIDE_END + 1)  # 1-based inclusive

    # Counters for progressive scoring
    inside_total = 0
    inside_correct = 0
    outside_total = 0
    outside_correct = 0

    # ---------- Core verification ----------
    for idx, para_text in enumerate(paragraphs, start=1):
        txt_lower = para_text.lower()
        has_colour = contains_word("colour", txt_lower)
        has_color = contains_word("color", txt_lower)

        if idx in inside_indices:
            inside_total += 1
            if has_color and not has_colour:
                inside_correct += 1
                print(f"✓ Paragraph {idx}: correct ('color' present, 'colour' absent)")
            else:
                issues = []
                if not has_color:
                    issues.append("missing 'color'")
                if has_colour:
                    issues.append("contains 'colour'")
                print(f"✗ Paragraph {idx}: {' & '.join(issues)} -> '{para_text[:70]}…'")
        else:
            outside_total += 1
            # Outside range must still have at least one 'colour'
            if has_colour:
                outside_correct += 1
            else:
                reason = ("'colour' replaced outside allowed range" if has_color
                          else "original text altered – 'colour' missing")
                print(f"✗ Paragraph {idx}: {reason} -> '{para_text[:70]}…'")

    # ---------- Scoring ----------
    inside_score = (inside_correct / inside_total) * 0.5 if inside_total else 0.0
    outside_score = (outside_correct / outside_total) * 0.5 if outside_total else 0.0
    final_score = round(inside_score + outside_score, 4)

    print(f"Inside paragraphs correct: {inside_correct}/{inside_total} -> {inside_score:.2f}")
    print(f"Outside paragraphs unchanged: {outside_correct}/{outside_total} -> {outside_score:.2f}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task(FILE_PATH)

