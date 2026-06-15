"""
FINAL REWARD SCRIPT - SUCCESS
Task: I dropped a block of terminal results into my Writer file and it’s ruining the layout. How can I take the single paragraph that begins with "Sample Output" and switch it to the built-in "Preformatted Text" paragraph style so the alignment and fixed-width look are preserved?
Generated: 2025-09-10 20:32:37
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
from docx import Document

def verify_preformatted_paragraph_style(file_path: str,
                                         paragraph_start_text: str = "Sample Output",
                                         target_style: str = "Preformatted Text") -> float:
    """Verify that the paragraph beginning with `paragraph_start_text` is styled with
    `target_style` (case-insensitive).

    Returns a progressive score between 0.0 and 1.0.
    """
    print(f"Verifying document: {file_path}")

    score = 0.0            # progressive score
    max_score = 1.0        # never exceed this

    # 1) Prerequisite: file must exist and be loadable (no points for that!)
    if not os.path.exists(file_path):
        print("✗ File does not exist.")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Failed to load DOCX: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Locate the target paragraph (0.3 points)
    target_para = None
    for para in doc.paragraphs:
        if para.text.strip().startswith(paragraph_start_text):
            target_para = para
            break

    if target_para is None:
        print(f"✗ No paragraph starts with '{paragraph_start_text}'.")
    else:
        print(f"✓ Found target paragraph starting with '{paragraph_start_text}'. (0.3 points)")
        score += 0.3

        # 3) Verify the paragraph style (0.7 points)
        style_name = target_para.style.name if target_para.style is not None else "(No style)"
        print(f"   Detected style name: '{style_name}'")
        if style_name.lower() == target_style.lower():
            print(f"✓ Paragraph is correctly styled as '{target_style}'. (0.7 points)")
            score += 0.7
        else:
            print(f"✗ Paragraph is not styled as '{target_style}'.")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# -----------------------------------------------------------------------------
# Execute verification when run as a script
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/i_dropped_a_block_of_terminal_results_into_my_writer_file_and_its_ruining_the_layout_how_can_i_take_.docx"
    verify_preformatted_paragraph_style(FILE_PATH)

