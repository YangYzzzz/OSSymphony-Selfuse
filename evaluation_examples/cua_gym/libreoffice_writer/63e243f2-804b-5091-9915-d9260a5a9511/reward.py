"""
FINAL REWARD SCRIPT - SUCCESS
Task: I pasted a long block of text into LibreOffice Writer, and the client wants only the fifth paragraph screaming in FULL CAPS. How can I quickly turn just paragraph 5 into uppercase without messing with the rest of the document?
Generated: 2025-09-10 12:05:13
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os

# -------------------------------------------------------------------
# Reward Script: Verify that ONLY the 5th paragraph is in FULL CAPS
# -------------------------------------------------------------------
# Scoring Logic (progressive – max 1.0):
#   0.7 pts  -> 5th non-empty paragraph text is entirely uppercase
#   0.3 pts  -> Previous paragraphs (1-4) are *not* entirely uppercase
#               (ensures no other text was unintentionally converted)
# -------------------------------------------------------------------

def is_all_upper(text: str) -> bool:
    """Return True if every alphabetical character in *text* is uppercase."""
    letters = [c for c in text if c.isalpha()]
    if not letters:                       # no alphabetic characters → treat as not-upper
        return False
    return all(c.isupper() for c in letters)

def verify_fifth_paragraph_uppercase(file_path: str) -> float:
    """Verify Writer task completion and return a score between 0.0-1.0."""
    print(f"Verifying document at: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to load the DOCX (LibreOffice saves .docx fine for this check)
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to open document: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather non-empty paragraphs to mirror Writer behaviour of visible paras
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    print(f"Total non-empty paragraphs found: {len(paragraphs)}")

    # Must have at least 5 paragraphs for task to make sense
    if len(paragraphs) < 5:
        print("✗ Document contains fewer than 5 paragraphs – task impossible")
        print("REWARD: 0.0")
        return 0.0

    fifth_para = paragraphs[4]
    print(f"Paragraph 5 text: '{fifth_para[:60]}{'...' if len(fifth_para)>60 else ''}'")

    total_score = 0.0  # progressive scoring

    # Requirement 1 – 5th paragraph must be FULL CAPS
    if is_all_upper(fifth_para):
        print("✓ Fifth paragraph is in FULL CAPS (0.7 pts)")
        total_score += 0.7
    else:
        print("✗ Fifth paragraph is not entirely uppercase (0 pts)")

    # Requirement 2 – Paragraphs 1-4 should remain mixed/lower case
    others_ok = any(not is_all_upper(paragraphs[i]) for i in range(min(4, len(paragraphs))))
    if others_ok:
        print("✓ Other paragraphs remain unaffected (0.3 pts)")
        total_score += 0.3
    else:
        print("✗ Paragraphs 1-4 are all uppercase – likely incorrect (0 pts)")

    # Final capped score
    final_score = min(total_score, 1.0)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------------------------------
# Execute verification when script is run directly
# ------------------------------------------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/i_pasted_a_long_block_of_text_into_libreoffice_writer_and_the_client_wants_only_the_fifth_paragraph_.docx"
    verify_fifth_paragraph_uppercase(DOC_PATH)

