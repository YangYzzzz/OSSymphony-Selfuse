"""
FINAL REWARD SCRIPT - SUCCESS
Task: In the first table of my document, I need the header to stretch across both the second and third columns. How do I merge cells B2 and C2 in Table 1 in LibreOffice Writer?
Generated: 2025-09-10 18:04:42
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import xml.etree.ElementTree as ET
from docx import Document


def verify_task(file_path: str) -> float:
    """Verify that in the first table of the document cells B2 and C2 are merged
    (i.e., cell B2 spans two columns). Returns a progressive score between 0.0 and 1.0.
    """

    print(f"Checking document: {file_path}")

    # ---- Basic file checks (no points for these) ----
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading document: {e}")
        return 0.0

    tables = doc.tables
    if not tables:
        print("✗ No tables found in document")
        return 0.0

    # ---- Verification & Scoring ----
    total_score = 0.0      # progressive score
    max_score   = 1.0

    # 1) Table structure present (0.3 points)
    first_table = tables[0]
    num_rows    = len(first_table.rows)
    num_cols    = len(first_table.columns) if num_rows else 0
    print(f"✓ Found {len(tables)} table(s) | First table size: {num_rows} rows x {num_cols} columns")

    if num_rows >= 2 and num_cols >= 3:
        total_score += 0.3
        print("✓ Table structure sufficient (0.3 points)")
    else:
        print("✗ First table does not have the required size (need ≥2 rows & ≥3 cols)")
        return total_score  # cannot proceed without correct structure

    # 2) Cell B2 spans two columns (0.7 points)
    #    In python-docx, this corresponds to the second row (index 1) & second column (index 1)
    target_cell = first_table.rows[1].cells[1]

    # Extract <w:gridSpan w:val="2"/> from cell XML
    ns   = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    root = ET.fromstring(target_cell._tc.xml)
    grid_span_el = root.find('.//w:gridSpan', ns)

    if grid_span_el is not None:
        span_val = grid_span_el.attrib.get(f"{{{ns['w']}}}val") or grid_span_el.attrib.get('w:val')
        print(f"gridSpan value detected: {span_val}")
        if str(span_val) == '2':
            total_score += 0.7
            print("✓ Cell B2 correctly merged across 2 columns (0.7 points)")
        else:
            print("✗ gridSpan present but value ≠ 2 (cell not merged over exactly two columns)")
    else:
        print("✗ No gridSpan element found – cells B2 & C2 are not merged")

    # ---- Final score ----
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path to the document inside the VM
    FILE_PATH = \
        "/home/user/in_the_first_table_of_my_document_i_need_the_header_to_stretch_across_both_the_second_and_third_colu.docx"

    reward = verify_task(FILE_PATH)
    print(f"REWARD: {reward}")

