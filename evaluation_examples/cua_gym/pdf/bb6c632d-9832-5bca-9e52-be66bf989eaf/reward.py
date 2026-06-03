"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to OCR the mathematical equations in 'math_textbook_scan.pdf' in /home/user/Study and save to 'equations.txt', preserving mathematical notation as much as possible.
Generated: 2025-11-29 10:07:03
Status: success
Model: o3
Total Steps: 6
"""

from pathlib import Path
import os
import re
from typing import List
from PyPDF2 import PdfReader

# -----------------------------------------------------------------------------
# Reward Script : OCR Verification for mathematical equations
# -----------------------------------------------------------------------------
# Task Recap
# The user had to OCR the mathematical equations in the scanned PDF
#   /home/user/Study/math_textbook_scan.pdf
# and save the recognised equations to
#   /home/user/Study/equations.txt
# while preserving the mathematical notation as closely as possible.
#
# This script verifies the task by:
# 1. Heuristically extracting *equation-like* lines from the source PDF.
# 2. Reading the lines produced by the user in equations.txt.
# 3. Comparing both lists for coverage (all expected equations present)
#    and cleanliness (no unexpected extra equation-like lines).
# 4. Returning a progressive score where:
#       • up to 0.8 points come from how many expected equations are present
#       • 0.2 bonus points if no spurious equation lines are present
#    thus awarding exactly 1.0 only for perfect completion.
# -----------------------------------------------------------------------------

def extract_equations(pdf_path: str) -> List[str]:
    """Extract equation-like lines from a PDF using simple heuristics.
    A line is considered an equation if it contains typical math symbols
    such as '=', '\\', '^', '*', integral (∫), summation (∑), plus/minus (±).
    Headings such as 'Mathematical …' are ignored.
    Returns the list of trimmed strings in original order.
    """
    reader = PdfReader(pdf_path)
    equations = []
    for page in reader.pages:
        text = page.extract_text() or ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            # Ignore obvious non-equation headings
            if re.match(r"^(mathematical|chapter|section)", line, re.I):
                continue
            # Heuristic for math content
            if re.search(r"(=|\\\\|\^|\*|∫|∑|±)", line):
                equations.append(line)
    return equations


def verify_ocr_task() -> float:
    pdf_path = "/home/user/Study/math_textbook_scan.pdf"
    txt_path = "/home/user/Study/equations.txt"
    max_score = 1.0
    score = 0.0

    # ------------------------------------------------------------------
    # Preliminary existence checks (no points awarded for mere existence)
    # ------------------------------------------------------------------
    if not os.path.exists(pdf_path):
        print(f"✗ Source PDF missing: {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(txt_path):
        print(f"✗ Output text file missing: {txt_path}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Extract expected and user-provided equation lines
    # ---------------------------------------------------------------
    expected_equations = extract_equations(pdf_path)
    expected_set = [eq.strip() for eq in expected_equations]

    print(f"Expected equations ({len(expected_set)}):")
    for eq in expected_set:
        print(f"  - {eq}")

    txt_content = Path(txt_path).read_text(encoding="utf-8", errors="ignore")
    user_lines = [ln.strip() for ln in txt_content.splitlines() if ln.strip()]

    print(f"User equations ({len(user_lines)}):")
    for ln in user_lines:
        print(f"  * {ln}")

    # ---------------------------------------------------------------
    # Content coverage scoring: up to 0.8 points
    # ---------------------------------------------------------------
    match_flags = [eq in user_lines for eq in expected_set]
    matches = sum(match_flags)
    print(f"Matched {matches} / {len(expected_set)} expected equations.")

    if expected_set:
        per_eq_score = 0.8 / len(expected_set)
        score += per_eq_score * matches

    # ---------------------------------------------------------------
    # Bonus cleanliness check: +0.2 if no unexpected equations
    # ---------------------------------------------------------------
    def looks_like_equation(line: str) -> bool:
        return bool(re.search(r"(=|\\\\|\^|\*|∫|∑|±)", line))

    unexpected = [l for l in user_lines if looks_like_equation(l) and l not in expected_set]

    if unexpected:
        print("✗ Unexpected equation-like lines found:")
        for l in unexpected:
            print(f"    -> {l}")
    else:
        print("✓ No unexpected extra equation lines found")
        score += 0.2

    final_score = round(min(score, max_score), 2)

    print(f"Resulting score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -----------------------------------------------------------------------------
# Execute verification when the script runs as main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    verify_ocr_task()

