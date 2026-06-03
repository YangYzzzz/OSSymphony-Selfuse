"""
FINAL REWARD SCRIPT - SUCCESS
Task: Apply strikethrough to the closing paragraph's repeated content so it's clear what to cut.
Generated: 2025-10-14 06:16:44
Status: success
Model: azure-o3
Total Steps: 3
"""

from docx import Document
import os
import re

def verify_strikethrough_repeats(file_path: str) -> float:
    """Verify that the closing paragraph contains duplicated text and that the
    repeated portion has been formatted with strikethrough so it's clear
    what to cut.

    Scoring (progressive):
        0.5  – At least one run in the last non-empty paragraph is formatted
                with strikethrough.
        0.5  – The text inside a strikethrough run duplicates text that
                appears earlier in the same paragraph (i.e., it's truly the
                repeated content being marked for deletion).
        1.0  – Both conditions satisfied.
    """

    print(f"Verifying file: {file_path}")
    score = 0.0

    # ---------- 1. Basic file checks (no points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading DOCX: {e}")
        return 0.0

    # ---------- 2. Locate the closing (last non-empty) paragraph ----------
    last_para = next((p for p in reversed(doc.paragraphs) if p.text.strip()), None)
    if not last_para:
        print("✗ Document has no non-empty paragraph")
        return 0.0
    print(f"Last paragraph text: {repr(last_para.text)}")

    # ---------- 3. Look for strikethrough formatting ----------
    strike_runs = [(idx, run.text) for idx, run in enumerate(last_para.runs)
                   if getattr(run.font, "strike", False)]
    if strike_runs:
        print(f"✓ Found {len(strike_runs)} strikethrough run(s)")
        score += 0.5  # award 0.5 for using strikethrough formatting
    else:
        print("✗ No strikethrough runs found")

    # ---------- 4. Confirm the stricken text is repeated content ----------
    duplication_confirmed = False
    if strike_runs:
        cumulative_text = ""
        for run in last_para.runs:
            if getattr(run.font, "strike", False):
                strike_text = re.sub(r"\s+", " ", run.text.strip())
                earlier_text = re.sub(r"\s+", " ", cumulative_text.strip())
                if strike_text and strike_text in earlier_text:
                    duplication_confirmed = True
                    print(f"✓ Strikethrough text duplicates earlier text: '{strike_text}'")
                    break
            cumulative_text += run.text  # build up text seen so far

    if duplication_confirmed:
        score += 0.5  # award remaining 0.5 for correctly marking duplicates
    elif strike_runs:
        print("✗ Strikethrough text does not match earlier content")

    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/apply_strikethrough_to_the_closing_paragraphs_repeated_content_so_its_clear_what_to_cut.docx"
    verify_strikethrough_repeats(DOC_PATH)
