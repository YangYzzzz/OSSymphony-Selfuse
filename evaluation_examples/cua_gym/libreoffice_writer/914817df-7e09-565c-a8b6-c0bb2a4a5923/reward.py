"""
FINAL REWARD SCRIPT - SUCCESS
Task: In paragraph 6 I’ve got a bunch of math expressions where I accidentally typed a plain hyphen (-) instead of the real minus sign (−). How can I tell LibreOffice Writer to fix just that paragraph—basically, select paragraph 6, open Find & Replace, enable regular expressions, search for the pattern (?<=\d)-( ?)(?=\d), and swap every match with the proper Unicode minus (−) in one go?
Generated: 2025-09-10 16:12:53
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
from docx import Document


def verify_minus_replacement(file_path: str) -> float:
    """Verify that only paragraph 6 of the document had hyphen-minus characters
    (U+002D) between digits replaced by the real minus sign (U+2212), while the
    other paragraphs remain unchanged.

    Scoring (progressive):
      • 0.3 – Paragraph 6 contains at least one U+2212 between digits
      • 0.3 – Paragraph 6 no longer contains hyphen-minus between digits
      • 0.4 – A control paragraph (paragraph 4) still keeps its original
               hyphen-minus between digits and has **no** U+2212, proving that
               the search-and-replace was scoped to paragraph 6 only.
      ⇒ 1.0 when all three conditions are met.
    """

    unicode_minus = "\u2212"
    score = 0.0

    # ---------- 0.  Load the document (prerequisite – no points) ---------- #
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("✗ Unable to load DOCX:", e)
        return 0.0

    paragraphs = doc.paragraphs
    print(f"✓ Loaded document with {len(paragraphs)} paragraphs")

    if len(paragraphs) < 6:
        print("✗ Document should have at least 6 paragraphs – cannot verify")
        return 0.0

    # ---------- 1.  Analyse paragraph 6 (index 5) ------------------------- #
    p6_text = paragraphs[5].text
    print("Paragraph 6 text:", p6_text)

    regex_unicode_minus = re.compile(r"(?<=\d)" + unicode_minus + r"(?=\d)")
    regex_hyphen_minus = re.compile(r"(?<=\d)-( ?:)?(?=\d)")  # hyphen between digits (optional space)"

    # 1A. At least one proper minus sign present
    unicode_matches = regex_unicode_minus.findall(p6_text)
    if unicode_matches:
        print(f"✓ Found {len(unicode_matches)} Unicode minus occurrence(s) between digits in paragraph 6")
        score += 0.3
    else:
        print("✗ No Unicode minus between digits found in paragraph 6")

    # 1B. No residual hyphen-minus between digits
    hyphen_matches = regex_hyphen_minus.findall(p6_text)
    if not hyphen_matches:
        print("✓ No hyphen-minus between digits left in paragraph 6")
        score += 0.3
    else:
        print(f"✗ Found {len(hyphen_matches)} residual hyphen-minus occurrence(s) between digits in paragraph 6")

    # ---------- 2.  Control paragraph (paragraph 4, index 3) -------------- #
    # It should still contain the original hyphen-minus 8-9 and *not* contain U+2212
    if len(paragraphs) >= 4:
        p4_text = paragraphs[3].text
    else:
        p4_text = ""

    print("Paragraph 4 text:", p4_text)
    control_hyphen = re.findall(r"(?<=\d)-( ?:)?(?=\d)", p4_text)
    control_unicode = re.findall(regex_unicode_minus, p4_text)

    if control_hyphen and not control_unicode:
        print("✓ Paragraph 4 still contains hyphen-minus between digits and has no Unicode minus (unchanged)")
        score += 0.4
    else:
        if not control_hyphen:
            print("✗ Hyphen-minus between digits missing from paragraph 4 – may have been incorrectly replaced")
        if control_unicode:
            print("✗ Unicode minus found in paragraph 4 – replacements should have been limited to paragraph 6")

    # ---------- 3.  Final score ------------------------------------------ #
    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


# -------------------- RUN VERIFICATION IMMEDIATELY ----------------------- #
if __name__ == "__main__":
    test_path = "/home/user/in_paragraph_6_ive_got_a_bunch_of_math_expressions_where_i_accidentally_typed_a_plain_hyphen_instead.docx"
    verify_minus_replacement(test_path)
