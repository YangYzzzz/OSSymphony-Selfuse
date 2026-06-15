"""
FINAL REWARD SCRIPT - SUCCESS
Task: The project codes in the second column of “Table 1” are jumbled (e.g., A12, A2, B4), and Writer keeps treating them like numbers. How can I sort the entire table so Column 2 is ordered alphabetically A-Z, forcing LibreOffice to handle the entries strictly as text?
Generated: 2025-09-10 13:32:45
Status: success
Model: azure-o3
Total Steps: 14
"""

import os
import re
import glob
from docx import Document

def locate_document():
    """Return the most likely .docx that the user worked on.
    Primary path is the one given in the task description.
    Fallback: first .docx in the home directory if the primary path is absent."""
    primary = (
        "/home/user/"
        "the_project_codes_in_the_second_column_of_table_1_are_jumbled_eg_a12_a2_b4_"
        "and_writer_keeps_treating.docx"
    )
    if os.path.exists(primary):
        return primary

    # Fallback search (only if primary not found)
    candidates = sorted(glob.glob("/home/user/*.docx"))
    return candidates[0] if candidates else None


def verify_project_code_sorting(file_path: str) -> float:
    """Verify that the table containing the column header *Project Code*
    is sorted alphabetically (treating codes strictly as text).

    Progressive scoring (max 1.0):
        • 0.2  – Locate the correct table / column structure
        • 0.2  – Codes follow a letter+number text pattern (indicates text treatment)
        • 0.6  – Alphabetical A→Z ordering quality (full points if perfect, proportional otherwise)
    """
    print(f"Verifying project code sorting for file: {file_path}")

    max_score = 1.0
    score = 0.0

    # --------- Safety checks ---------
    if not file_path or not os.path.exists(file_path):
        print("✗ Document file not found. Cannot verify task.")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to open DOCX file: {e}")
        return 0.0

    # --------- Locate relevant table & column ---------
    target_table = None
    code_col_idx = None

    for tbl_idx, table in enumerate(doc.tables):
        if not table.rows:
            continue  # empty table guard
        header_cells = table.rows[0].cells
        header_texts = [cell.text.strip().lower() for cell in header_cells]
        for idx, header in enumerate(header_texts):
            if "project code" in header:
                target_table = table
                code_col_idx = idx
                break
        if target_table is not None:
            break

    if target_table is None:
        print("✗ No table found with a \"Project Code\" column header.")
        return 0.0

    print(
        f"✓ Located target table (index {tbl_idx}) with project code column at index {code_col_idx}."
    )
    score += 0.2  # structure found

    # --------- Extract project codes ---------
    codes = []
    for row in target_table.rows[1:]:  # skip header row
        if code_col_idx >= len(row.cells):
            continue  # uneven row safeguard
        txt = row.cells[code_col_idx].text.strip()
        if txt:
            codes.append(txt)

    if not codes:
        print("✗ No project codes found under the identified column.")
        return round(score, 4)  # can't continue without codes

    print("Extracted project codes:", codes)

    # --------- Verify codes are treated as text ---------
    text_pattern = re.compile(r"^[A-Za-z]+\d+$")
    pattern_matches = sum(1 for c in codes if text_pattern.match(c))
    pattern_ratio = pattern_matches / len(codes)

    if pattern_ratio == 1.0:
        print("✓ All codes adhere to letter+number pattern (treated as text).")
    else:
        print(
            f"✗ Only {pattern_matches}/{len(codes)} codes match the required text pattern."
        )
    score += 0.2 * pattern_ratio  # up to 0.2 based on adherence

    # --------- Check alphabetical ordering ---------
    codes_upper = [c.upper() for c in codes]  # normalise case
    expected_sorted = sorted(codes_upper)

    if codes_upper == expected_sorted:
        print("✓ Codes are perfectly sorted alphabetically A–Z.")
        score += 0.6  # full ordering credit
    else:
        # Progressive credit: proportion of adjacent in-order pairs
        if len(codes_upper) > 1:
            in_order_pairs = sum(
                1 for i in range(1, len(codes_upper)) if codes_upper[i - 1] <= codes_upper[i]
            )
            order_ratio = in_order_pairs / (len(codes_upper) - 1)
        else:
            order_ratio = 1.0  # trivially sorted if single item
        print(
            f"✗ Codes are not fully sorted (adjacent in-order ratio {order_ratio:.2f})."
        )
        score += 0.6 * order_ratio  # proportional ordering credit

    final_score = round(min(score, max_score), 4)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    document_path = locate_document()
    reward = verify_project_code_sorting(document_path)
    # Explicitly print in the required format
    print(f"REWARD: {reward}")

