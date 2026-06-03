"""
FINAL REWARD SCRIPT - SUCCESS
Task: Whenever I try to add a caption to my first table in LibreOffice Writer, it insists on placing the label underneath. For this particular table I need the caption line to read exactly "Table 1: Participants" and it has to sit above the table, not below it. Using the Insert ▸ Caption… dialog, which Category should I pick (I assume "Table") and how do I force the Position to "Above" so the caption shows up in the right spot?
Generated: 2025-09-10 15:56:12
Status: success
Model: azure-o3
Total Steps: 3
"""

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from pathlib import Path
from typing import Union

# -----------------------------------------------------------------------------
# Reward Script
# -----------------------------------------------------------------------------
# This script verifies that, in the given document, the FIRST table has the
# caption line exactly "Table 1: Participants" positioned *above* the table and
# nowhere else.  A progressive score is awarded:
#   +0.3 : First table successfully detected
#   +0.6 : Caption text matches *and* is immediately ABOVE the first table
#   +0.1 : Caption appears only once in the whole document and NOT below table
# The script returns a float between 0.0 and 1.0 and prints detailed diagnostics
# followed by "REWARD: X.X".
# -----------------------------------------------------------------------------

FILE_PATH = Path(
    "/home/user/whenever_i_try_to_add_a_caption_to_my_first_table_in_libreoffice_writer_it_insists_on_placing_the_la.docx"
)


def iter_block_items(doc):
    """Yield each top-level paragraph and table in document order."""
    from docx.oxml.ns import qn

    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, doc)
        elif child.tag == qn("w:tbl"):
            yield Table(child, doc)


def verify_caption_above_first_table(file_path: Union[str, Path]) -> float:
    """Verify caption placement and text for the first table with progressive scoring."""

    caption_text_expected = "Table 1: Participants"
    max_score = 1.0
    score = 0.0

    path = Path(file_path)
    if not path.exists():
        print("✗ File does not exist")
        return 0.0  # hard failure – nothing to score

    # ------------------------------------------------------------------
    # Load document (prerequisite – gives NO points by itself)
    # ------------------------------------------------------------------
    try:
        doc = Document(str(path))
    except Exception as e:
        print(f"✗ Failed to open DOCX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # Locate first table and surrounding blocks
    # ------------------------------------------------------------------
    blocks = list(iter_block_items(doc))
    print(f"Document contains {len(blocks)} top-level blocks (paragraphs + tables)")

    first_table_idx = None
    for idx, blk in enumerate(blocks):
        if isinstance(blk, Table):
            first_table_idx = idx
            break

    if first_table_idx is None:
        print("✗ No tables found – cannot verify caption placement")
        return 0.0

    print(f"✓ Found the first table at block index {first_table_idx}")
    score += 0.3  # credit for detecting a table we can work with

    # ------------------------------------------------------------------
    # Verify caption immediately ABOVE the first table
    # ------------------------------------------------------------------
    caption_above_ok = False
    if first_table_idx > 0:
        preceding_block = blocks[first_table_idx - 1]
        if isinstance(preceding_block, Paragraph):
            text_above = preceding_block.text.strip()
            print(f"Text above table: '{text_above}'")
            if text_above == caption_text_expected:
                caption_above_ok = True
                print("✓ Caption text matches expected and is ABOVE the table")
            else:
                print("✗ Paragraph above table does not match required caption text")
        else:
            print("✗ Block above the table is not a paragraph – caption missing or misplaced")
    else:
        print("✗ Table is the first block – cannot have caption above it")

    if caption_above_ok:
        score += 0.6

    # ------------------------------------------------------------------
    # Ensure caption appears ONLY ONCE and NOT below the table
    # ------------------------------------------------------------------
    caption_occurrences = sum(
        1 for p in doc.paragraphs if p.text.strip() == caption_text_expected
    )
    print(f"Caption occurrences in entire document: {caption_occurrences}")

    duplicate_below = False
    if first_table_idx + 1 < len(blocks):
        following_block = blocks[first_table_idx + 1]
        if isinstance(following_block, Paragraph):
            if following_block.text.strip() == caption_text_expected:
                duplicate_below = True
                print("✗ Duplicate caption found immediately BELOW the table")
            else:
                print("✓ No caption found immediately below the table – good")
        else:
            print("✓ Block below table is not a caption paragraph – good")

    if caption_above_ok and caption_occurrences == 1 and not duplicate_below:
        score += 0.1  # bonus for uniqueness and correct placement only
        print("✓ Caption appears exactly once and only above the table – bonus awarded")
    else:
        if caption_occurrences != 1:
            print("✗ Caption does not appear exactly once in the document")

    # ------------------------------------------------------------------
    # Final score (capped to 1.0) & output
    # ------------------------------------------------------------------
    final_score = min(round(score, 2), max_score)
    print(f"Final verification score: {final_score}")
    return final_score


if __name__ == "__main__":
    reward_value = verify_caption_above_first_table(FILE_PATH)
    print(f"REWARD: {reward_value}")

