"""
FINAL REWARD SCRIPT - SUCCESS
Task: My manuscript is littered with the quick-typed triple hyphen '---', but the publisher insists on the proper em dash '—'. In LibreOffice Writer, how can I replace every single occurrence of exactly those three consecutive hyphens with the em dash throughout the entire file at once?
Generated: 2025-09-10 19:49:57
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import re
from docx import Document


def count_triple_hyphen(text: str) -> int:
    """Count exact occurrences of three consecutive hyphens (---) **not** surrounded by additional hyphens.
    This avoids counting longer strings like "----" twice.
    """
    # Negative look-behind & look-ahead ensure exactly three hyphens
    pattern = r"(?<!-)(---)(?!-)"
    return len(re.findall(pattern, text))


def verify_emdash_replacement(file_path: str) -> float:
    """
    Verify that every instance of exactly three consecutive hyphens (---)
    has been replaced by an em dash (—) in the given DOCX file.

    Scoring (progressive):
      • 0.4 points – at least one em dash is present in the document
      • up to 0.6 points – proportion of triple-hyphen sequences successfully
        eliminated (all replaced ⇒ full 0.6)
    Returns a float between 0.0 and 1.0 inclusive.
    """

    max_score = 1.0
    score = 0.0

    # ---------- 1. Load document ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0  # Cannot continue if file is missing

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- 2. Concatenate all paragraph text ----------
    all_text = "\n".join(p.text for p in doc.paragraphs)

    # ---------- 3. Count patterns ----------
    triple_count = count_triple_hyphen(all_text)
    emdash_count = all_text.count("—")

    print(f"Triple hyphen occurrences remaining: {triple_count}")
    print(f"Em dash occurrences found: {emdash_count}")

    # ---------- 4. Scoring ----------
    # 4a. Presence of at least one em dash (0.4 pts)
    if emdash_count > 0:
        score += 0.4
        print("✓ Detected at least one em dash (0.4 points)")
    else:
        print("✗ No em dash detected (0 points)")

    # 4b. Elimination of triple hyphens (up to 0.6 pts)
    if triple_count == 0:
        score += 0.6
        print("✓ No triple hyphens remain (0.6 points)")
    else:
        # Partial credit proportional to replacement ratio
        original_sequences = triple_count + emdash_count  # rough estimate
        if original_sequences > 0:
            replaced_fraction = emdash_count / original_sequences
            partial_points = 0.6 * replaced_fraction
            score += partial_points
            print(
                f"Partial replacement: {replaced_fraction*100:.1f}% → {partial_points:.2f} points"
            )
        else:
            print("No triple-hyphen or em dash sequences found – 0 points for replacement")

    final_score = min(score, max_score)

    # ---------- 5. Output result ----------
    print(f"Total Score: {final_score}")
    print(f"REWARD: {final_score}")

    return final_score


# ------------------ MAIN EXECUTION ------------------
if __name__ == "__main__":
    DOC_PATH = (
        "/home/user/"
        "my_manuscript_is_littered_with_the_quick_typed_triple_hyphen_but_the_publisher_insists_on_the_proper.docx"
    )
    verify_emdash_replacement(DOC_PATH)

