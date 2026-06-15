"""
FINAL REWARD SCRIPT - SUCCESS
Task: Paragraph 7 has a few standalone capital “A”s (e.g., “… A sample …”). LibreOffice keeps orphaning that letter at the line end, which looks awful. How can I replace the regular space that comes right after each single-letter “A” in that paragraph with a non-breaking space (Ctrl+Shift+Space) so the “A” always stays glued to the next word?
Generated: 2025-09-10 17:39:57
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os
import re
import textwrap

def verify_non_breaking_space_after_A(file_path: str) -> float:
    """
    Verification script for the LibreOffice Writer task:
    "Paragraph 7 has a few standalone capital “A”s … Replace the regular space that comes right after each
    single-letter “A” in that paragraph with a non-breaking space so the “A” always stays glued to the next word."

    Scoring logic (progressive):
        • 0.6  points – at least one standalone “A” followed by a non-breaking space (NBSP) is present
        • +0 → +0.4 points – proportional to the fraction of *all* standalone “A ” occurrences that were fixed
          (full 0.4 when every occurrence is fixed, smaller when partial)
        • 1.0      – perfect score when ALL regular spaces after standalone “A” are replaced by NBSP

    The script ONLY awards points for the actual presence of NBSP after the standalone capital letter “A”.
    It gives NO credit for natural conditions such as file existence or successful loading.
    """

    print(f"Verifying file: {file_path}\n")

    # --- Preliminary checks (NO points awarded here) ---
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load DOCX: {e}")
        return 0.0

    # --- Locate paragraph 7 (1-based index) ---
    paragraphs = doc.paragraphs
    if not paragraphs:
        print("✗ Document contains no paragraphs")
        return 0.0

    target_index = 6 if len(paragraphs) > 6 else len(paragraphs) - 1  # zero-based
    target_para = paragraphs[target_index].text

    print(f"Total paragraphs in document: {len(paragraphs)}")
    print(f"Target paragraph index inspected: {target_index} (Paragraph 7 in specification)\n")
    print("Target paragraph snippet:\n" + textwrap.shorten(target_para, width=120, placeholder="..."))

    # --- Define regex patterns ---
    pattern_regular = r"\bA "      # capital A followed by normal space
    pattern_nbsp    = r"\bA\u00A0"  # capital A followed by NBSP (Unicode 00A0)

    # Count occurrences in paragraph 7
    regular_count = len(re.findall(pattern_regular, target_para))
    nbsp_count    = len(re.findall(pattern_nbsp, target_para))

    print(f"Occurrences with regular space after 'A': {regular_count}")
    print(f"Occurrences with non-breaking space after 'A': {nbsp_count}\n")

    # --- Progressive scoring ---
    score = 0.0
    if nbsp_count > 0:
        # Primary achievement: at least one NBSP present
        score += 0.6

        # Additional points based on how many fixes were completed
        total_occurrences = regular_count + nbsp_count
        if total_occurrences > 0:
            correction_fraction = nbsp_count / total_occurrences  # 0-1 range
            # Up to +0.4 depending on fraction corrected
            score += 0.4 * correction_fraction
    else:
        print("✗ No non-breaking spaces found after standalone 'A'.")

    # Cap score at 1.0
    score = min(score, 1.0)
    print(f"Total score (progressive): {score}")
    return score

# -----------------------------------------------------------------------------
# ACTUAL EXECUTION – The path is provided by the grading environment.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    file_path = (
        "/home/user/paragraph_7_has_a_few_standalone_capital_as_eg_a_sample_"  # noqa: E501
        "libreoffice_keeps_orphaning_that_letter_at_t.docx"
    )
    reward = verify_non_breaking_space_after_A(file_path)
    print(f"REWARD: {reward}")

