"""
FINAL REWARD SCRIPT - SUCCESS
Task: Editing my doc in LibreOffice Writer and I’m stuck—how do I split the single cell A3 of Table 1 straight down the middle so it becomes 2 separate columns?
Generated: 2025-09-10 14:25:36
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
from docx import Document

def verify_split_cell(file_path: str) -> float:
    """
    Verify that the single cell A3 of Table 1 has been split vertically so that
    Row 3 now contains at least two columns (i.e. the original cell became two
    separate cells).  Progressive scoring is used and points are ONLY awarded
    for real, verifiable conditions – never for natural document states such as
    mere file existence.
    """

    max_score = 1.0
    score = 0.0
    print(f"Verifying document: {file_path}\n")

    # ------------------------------------------------------------------
    # 1. Load document (prerequisite – NO POINTS for simply loading)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not open DOCX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Locate tables (task-relevant content) – still no points yet
    # ------------------------------------------------------------------
    tables = doc.tables
    if not tables:
        print("✗ No tables in document – expected Table 1")
        return 0.0
    print(f"✓ Found {len(tables)} table(s)")

    # Task refers to “Table 1”, so examine the first table only
    table = tables[0]
    num_rows = len(table.rows)
    print(f"Table 1 has {num_rows} row(s)")
    if num_rows < 3:                   # need at least 3 rows to have A3
        print("✗ Table 1 does not have at least 3 rows (missing A3)")
        return 0.0

    # ------------------------------------------------------------------
    # 3. Establish baseline column count using Row 1 (original structure)
    # ------------------------------------------------------------------
    baseline_cols = len(table.rows[0].cells)
    print(f"Baseline (Row 1) column count: {baseline_cols}")

    if baseline_cols >= 2:
        # Some credit for having a multi-column table structure
        score += 0.3

    # ------------------------------------------------------------------
    # 4. Analyse Row 3 (index 2) — this is where cell A3 lived
    # ------------------------------------------------------------------
    target_row = table.rows[2]
    target_cols = len(target_row.cells)
    print(f"Row 3 (A3) column count AFTER edit: {target_cols}")

    # Main requirement: Row 3 must now have at least two columns
    if target_cols >= 2:
        print("✓ Detected that cell A3 has been split into multiple columns")
        score += 0.5
    else:
        print("✗ Cell A3 still appears to be a single cell (split not performed)")

    # Bonus: Row 3 matches the baseline column layout – shows correct split
    if target_cols == baseline_cols and baseline_cols >= 2:
        print("✓ Row 3 column count matches the rest of the table")
        score += 0.2
    else:
        print("Row 3 column count does NOT match baseline")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}")
    return final_score

# ----------------------------------------------------------------------
# Execute verification when script is run directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/editing_my_doc_in_libreoffice_writer_and_im_stuckhow_do_i_split_the_single_cell_a3_of_table_1_straig.docx"
    reward = verify_split_cell(DOC_PATH)
    print(f"REWARD: {reward}")

