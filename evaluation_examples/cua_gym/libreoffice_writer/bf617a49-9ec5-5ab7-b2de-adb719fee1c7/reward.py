"""
FINAL REWARD SCRIPT - SUCCESS
Task: Create a table with 7 columns and 5 rows exactly at the caret.
Generated: 2025-10-14 05:52:05
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
from pathlib import Path
from docx import Document

def verify_table_creation(file_path: str,
                           expected_rows: int = 5,
                           expected_cols: int = 7) -> float:
    """Reward script for the task: "Create a table with 7 columns and 5 rows".

    Scoring breakdown (progressive, max 1.0):
      • 0.4  – Document contains at least one table
      • 0.3  – At least one table has exactly the expected number of rows
      • 0.3  – At least one table has exactly the expected number of columns
        OR
      • 0.6  – A single table satisfies BOTH expected rows *and* columns

    Returns a float in the range [0.0, 1.0] and prints detailed diagnostics
    including a final line:  "REWARD: X.X".
    """

    max_score = 1.0
    score = 0.0

    # ---------- Prerequisite: file must exist and open ----------
    if not Path(file_path).exists():
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load DOCX file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- Step 1: Table presence ----------
    tables = doc.tables
    if not tables:
        print("✗ No tables detected in the document")
        print("REWARD: 0.0")
        return 0.0  # Cannot earn further points without a table

    print(f"✓ Found {len(tables)} table(s) in the document (0.4 points)")
    score += 0.4

    # ---------- Step 2: Dimensional accuracy ----------
    has_correct_rows = False
    has_correct_cols = False
    has_perfect_table = False

    for idx, tbl in enumerate(tables, start=1):
        rows = len(tbl.rows)
        cols = len(tbl.columns) if tbl.rows else 0
        print(f"  • Table {idx}: {rows} rows × {cols} columns")

        if rows == expected_rows:
            has_correct_rows = True
        if cols == expected_cols:
            has_correct_cols = True
        if rows == expected_rows and cols == expected_cols:
            has_perfect_table = True

    if has_perfect_table:
        print(f"✓ Located a table with exactly {expected_rows} rows and {expected_cols} columns (0.6 points)")
        score += 0.6  # replaces individual row/col points
    else:
        if has_correct_rows:
            print(f"✓ At least one table has {expected_rows} rows (0.3 points)")
            score += 0.3
        else:
            print(f"✗ No table with exactly {expected_rows} rows")

        if has_correct_cols:
            print(f"✓ At least one table has {expected_cols} columns (0.3 points)")
            score += 0.3
        else:
            print(f"✗ No table with exactly {expected_cols} columns")

    # ---------- Finalise score ----------
    final_score = min(score, max_score)
    print(f"Final score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# -------------------- Script entry point --------------------
if __name__ == "__main__":
    # Path to the document to verify (modify if needed)
    DOC_PATH = "/home/user/create_a_table_with_7_columns_and_5_rows_exactly_at_the_caret.docx"
    verify_table_creation(DOC_PATH)

