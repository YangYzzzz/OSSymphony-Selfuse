"""
FINAL REWARD SCRIPT - SUCCESS
Task: Paragraph 2 is still shouting at me in ALL CAPS. In LibreOffice Writer, is there a quick way to flip every uppercase word in that specific paragraph to lowercase all at once, instead of re-typing everything?
Generated: 2025-09-10 14:05:03
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
from docx import Document


def _calculate_score(upper_ratio: float) -> float:
    """Return progressive score based on the fraction of words still in ALL-CAPS.
    1.0  – no all-caps words remain (perfect)
    0.7  – ≤10 % caps
    0.5  – ≤30 % caps
    0.3  – ≤50 % caps
    0.1  – >50 % caps (barely changed)"""
    if upper_ratio == 0:
        return 1.0
    elif upper_ratio <= 0.10:
        return 0.7
    elif upper_ratio <= 0.30:
        return 0.5
    elif upper_ratio <= 0.50:
        return 0.3
    else:
        return 0.1


def verify_task(file_path: str) -> float:
    """Verify that paragraph 2 no longer shouts (i.e., no ALL-CAPS words).

    The function inspects the 2nd non-empty paragraph of the document and
    counts fully-uppercase words (length>1 to ignore pronoun ‘I’, article ‘A’).
    A progressive score is returned based on how many such words are left.
    """
    print(f"Starting verification for: {file_path}")

    # ---------- prerequisite checks (no points awarded) ----------
    if not os.path.exists(file_path):
        print("✗ File not found – task not completed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not open DOCX file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect non-empty paragraph texts
    paragraph_texts = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]

    if len(paragraph_texts) < 2:
        print("✗ Document has fewer than 2 non-empty paragraphs – cannot evaluate paragraph 2")
        print("REWARD: 0.0")
        return 0.0

    para2 = paragraph_texts[1]
    print("Paragraph 2 content (first 120 chars):")
    print(para2[:120] + ("..." if len(para2) > 120 else ""))

    # ---------- real verification begins (points awarded) ----------
    words = re.findall(r"[A-Za-z]+", para2)  # alphabetic word tokens
    if not words:
        print("✗ No alphabetic words found in paragraph 2 – unusual, giving 0 score")
        print("REWARD: 0.0")
        return 0.0

    # Count fully-uppercase words (length>1)
    upper_words = [w for w in words if len(w) > 1 and w.isupper()]
    upper_ratio = len(upper_words) / len(words)

    print(f"Total alphabetic words: {len(words)}")
    print(f"Fully uppercase words (length>1): {len(upper_words)}")
    print(f"Uppercase ratio: {upper_ratio:.2%}")

    score = _calculate_score(upper_ratio)

    # Human-readable status
    if score == 1.0:
        print("✓ All-caps words successfully converted – perfect completion (1.0)")
    elif score >= 0.7:
        print("✓ Paragraph mostly converted, minor caps remain (0.7)")
    elif score >= 0.5:
        print("✓ Partial progress – noticeable caps remain (0.5)")
    elif score >= 0.3:
        print("✗ Significant caps remain – limited progress (0.3)")
    else:
        print("✗ Paragraph largely unchanged – very low progress (0.1)")

    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    TARGET_FILE = "/home/user/paragraph_2_is_still_shouting_at_me_in_all_caps_in_libreoffice_writer_is_there_a_quick_way_to_flip_e.docx"
    verify_task(TARGET_FILE)
