"""
FINAL REWARD SCRIPT - SUCCESS
Task: I just dumped a bunch of names into “Table 1” and they’re all jumbled up. What’s the quickest way in LibreOffice Writer to sort Column 1 alphabetically (treat the values as text and put them in A→Z order)?
Generated: 2025-09-10 16:16:26
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
from docx import Document

def verify_column_sorted(file_path: str, table_index: int = 0, column_index: int = 0) -> float:
    """Reward script for LibreOffice Writer sorting task.

    The function verifies that Column 1 of *Table 1* in the provided
    document is sorted alphabetically (A→Z, case-insensitive).  
    Scoring is progressive: the reward equals the fraction of adjacent
    pairs that are in correct order, yielding 1.0 only for a perfectly
    sorted column.
    """

    print(f"Verifying alphabetical sort in: {file_path}")

    # ------------------------------------------------------------------
    # 0. Preliminary checks (NO points awarded for these)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0  # Cannot evaluate further

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load document: {e}")
        return 0.0  # Loading failure → no progress

    # ------------------------------------------------------------------
    # 1. Locate the requested table (Table 1)
    # ------------------------------------------------------------------
    tables = doc.tables
    if len(tables) <= table_index:
        print(f"✗ Table {table_index + 1} not found (only {len(tables)} table(s) present)")
        return 0.0  # Cannot assess sorting without the table

    table = tables[table_index]

    # ------------------------------------------------------------------
    # 2. Extract values from the requested column (Column 1)
    # ------------------------------------------------------------------
    column_values = []
    for row in table.rows:
        if len(row.cells) > column_index:
            column_values.append(row.cells[column_index].text.strip())
        else:
            column_values.append("")  # Treat missing cell as empty string

    if len(column_values) < 2:
        print("✗ Not enough rows to assess sorting")
        return 0.0

    print(f"✓ Retrieved {len(column_values)} values from Column {column_index + 1} of Table {table_index + 1}")
    print("  Values:", column_values)

    # ------------------------------------------------------------------
    # 3. Evaluate alphabetical ordering (progressive scoring)
    # ------------------------------------------------------------------
    total_pairs = len(column_values) - 1
    correct_pairs = 0
    for current_val, next_val in zip(column_values, column_values[1:]):
        if current_val.lower() <= next_val.lower():
            correct_pairs += 1

    ratio_sorted = correct_pairs / total_pairs  # Range 0.0‒1.0
    print(f"  Adjacent pairs in correct order: {correct_pairs}/{total_pairs} → ratio={ratio_sorted:.2f}")

    # The ratio itself is the reward (rounded for stability)
    final_score = round(ratio_sorted, 2)
    print(f"Final score based on sorting correctness: {final_score}")
    return final_score


if __name__ == "__main__":
    # Default path provided by the task description
    file_path = "/home/user/i_just_dumped_a_bunch_of_names_into_table_1_and_theyre_all_jumbled_up_whats_the_quickest_way_in_libr.docx"
    reward = verify_column_sorted(file_path)
    print(f"REWARD: {reward}")
