"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract text from the conference proceedings 'proceedings_2023.pdf' in /home/user/Research, separating each paper with a delimiter, and save to 'papers_combined.txt'.
Generated: 2025-11-29 09:15:17
Status: success
Model: o3
Total Steps: 7
"""

"""
Reward script for task:
Extract text from the conference proceedings 'proceedings_2023.pdf' in /home/user/Research,
separating each paper with a delimiter, and save to 'papers_combined.txt'.

The script verifies two concrete aspects:
1. Text from EVERY page of the PDF appears in the combined TXT file (major requirement).
   - It takes the first ~120 characters of text from each PDF page, normalises whitespace & case,
     and checks the substring exists in the TXT file (also normalised).
   - 0.6 points are awarded proportionally to the percentage of pages whose snippet is found.

2. Papers are separated by a visible delimiter line in the TXT file (secondary requirement).
   - A delimiter is defined as any line composed of a single repeating character (e.g. "-----" or
     "=====") of length ≥3.
   - The TXT file must contain at least (page_count - 1) delimiter lines, otherwise points are
     granted proportionally.
   - 0.4 points are awarded for correct delimiter usage.

The score is capped at 1.0 and printed as required ("REWARD: X.X").
The script gives 0 points for natural conditions such as mere file existence.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

PDF_PATH = "/home/user/Research/proceedings_2023.pdf"
TXT_PATH = "/home/user/Research/papers_combined.txt"

# ----------------------- Helper functions ---------------------------------- #

def _normalise(text: str) -> str:
    """Lower-cases and collapses all whitespace so substring matching is robust."""
    return re.sub(r"\s+", " ", text).strip().lower()


def _page_snippets(reader: PdfReader, chars: int = 120) -> List[str]:
    """Return a list with the first *chars* characters of normalised text per page."""
    snippets: List[str] = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        normalised = _normalise(page_text)
        snippets.append(normalised[:chars])
        print(f"Page {idx+1}: snippet length {len(snippets[-1])} chars")
    return snippets


def _find_delimiter_lines(text: str) -> List[str]:
    """Return lines that consist of the same character repeated ≥3 times."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and len(stripped) >= 3 and len(set(stripped)) == 1:
            lines.append(stripped)
    return lines

# ----------------------- Verification logic --------------------------------- #

def verify_task(pdf_path: str, txt_path: str) -> float:
    total_score = 0.0
    MAX_SCORE = 1.0

    # ---------- Requirement 1: Combined TXT contains each page's text ---------
    try:
        txt_file = Path(txt_path)
        if not txt_file.exists():
            print(f"✗ Combined TXT file missing at {txt_path}")
            return 0.0  # cannot award points without output file

        combined_text = txt_file.read_text(encoding="utf-8", errors="ignore")
        combined_norm = _normalise(combined_text)

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        print(f"PDF has {num_pages} pages")

        snippets = _page_snippets(reader)
        missing = 0
        for i, snippet in enumerate(snippets, start=1):
            # Protect against empty pages: skip scoring for empty snippet
            if not snippet:
                print(f"Page {i} is empty – excluded from scoring")
                continue
            if snippet in combined_norm:
                print(f"✓ Snippet from page {i} found in combined text")
            else:
                print(f"✗ Snippet from page {i} NOT found in combined text")
                missing += 1

        pages_considered = len([s for s in snippets if s])
        if pages_considered:
            found_ratio = (pages_considered - missing) / pages_considered
            text_score = 0.6 * found_ratio
            total_score += text_score
            print(f"Text coverage score: {text_score:.2f} (ratio {found_ratio:.2%})")
        else:
            print("No non-empty pages to verify – 0 points for text coverage")
    except Exception as e:
        print(f"✗ Error during text coverage verification: {e}")

    # ---------- Requirement 2: Delimiter lines between papers ----------------
    try:
        delimiter_lines = _find_delimiter_lines(combined_text)
        unique_delims = set(delimiter_lines)
        print(f"Found delimiter lines: {delimiter_lines}")
        expected_count = max(0, num_pages - 1)  # one delimiter between consecutive papers
        actual_count = len(delimiter_lines)

        if expected_count == 0:  # single-page PDF edge-case
            delim_score = 0.4  # full points – no delimiter needed
        else:
            ratio = min(actual_count, expected_count) / expected_count
            delim_score = 0.4 * ratio
        total_score += delim_score
        print(
            f"Delimiter score: {delim_score:.2f} (found {actual_count}, expected {expected_count})"
        )
    except Exception as e:
        print(f"✗ Error during delimiter verification: {e}")

    final_score = min(total_score, MAX_SCORE)
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------ Run check ----------------------------------- #

if __name__ == "__main__":
    verify_task(PDF_PATH, TXT_PATH)

