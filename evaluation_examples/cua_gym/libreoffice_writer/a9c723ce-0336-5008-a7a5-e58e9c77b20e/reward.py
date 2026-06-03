"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add a 7-by-5 empty table at my current typing position in the document.
Generated: 2025-10-14 09:25:21
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os

def verify_table_task(file_path: str) -> float:
    """
    Verify that the document contains **one (or more) 7-by-5 tables** where **every cell is empty**.
    Progressive scoring:
        • 0.0 – document missing / cannot open / no tables
        • 0.5 – a 7×5 table exists (structure correct)
        • +0.5 – that 7×5 table has **only empty cells** (fully meets task)
      Returns a score in [0.0, 1.0].
    """

    max_score = 1.0
    score = 0.0

    print(f"Verifying document: {file_path}")

    # ---------- Prerequisite: file must exist & load ----------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0  # no progress possible
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not open document: {e}")
        return 0.0

    # ---------- Table verification ----------
    tables = doc.tables
    print(f"Document contains {len(tables)} table(s)")

    if not tables:  # nothing to verify further
        print("✗ No tables found in document")
        return 0.0

    # Flags for progressive scoring
    correct_table_found = False
    correct_table_empty = False

    for idx, tbl in enumerate(tables):
        rows = len(tbl.rows)
        cols = len(tbl.columns) if rows else 0
        print(f"  Table {idx+1}: {rows} rows × {cols} cols")

        # Dimension check
        if rows == 7 and cols == 5:
            correct_table_found = True

            # Check every cell is empty (only whitespace allowed)
            all_empty = True
            for r in tbl.rows:
                for c in r.cells:
                    if c.text.strip():  # any visible text
                        all_empty = False
                        break
                if not all_empty:
                    break
            if all_empty:
                correct_table_empty = True
                break  # perfect table located; stop scanning further

    # ---------- Scoring ----------
    if correct_table_found:
        print("✓ Found table with 7×5 dimensions (0.5 points)")
        score += 0.5
        if correct_table_empty:
            print("✓ All cells in the 7×5 table are empty (additional 0.5 points)")
            score += 0.5
        else:
            print("✗ 7×5 table contains non-empty cells (no extra points)")
    else:
        print("✗ No 7×5 table found")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path provided in task context
    default_path = "/home/user/add_a_7_by_5_empty_table_at_my_current_typing_position_in_the_document.docx"
    verify_table_task(default_path)

