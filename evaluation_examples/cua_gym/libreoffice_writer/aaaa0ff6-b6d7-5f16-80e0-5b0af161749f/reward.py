"""
FINAL REWARD SCRIPT - SUCCESS
Task: Table 1 is framed by a thick border that makes the page look cramped. I just want the inner gridlines (all the row and column dividers) to stay, but the outer box around the table has to go. How do I strip off those outside edges in LibreOffice Writer without losing the internal lines?
Generated: 2025-09-10 16:00:05
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree


def verify_table_borders(file_path: str) -> float:
    """Reward script to verify that the outer borders of a table were removed
    while the inner gridlines (insideH / insideV) remain present.

    Scoring (progressive):
    • 0.2  – Document contains at least one table (task revolves around a table)
    • 0.4  – Outer borders (top/left/bottom/right) removed (val == nil or element absent)
    • 0.4  – Inner borders (insideH / insideV) present (val not nil)
    → 1.0  – All of the above satisfied on at least one table
    Partial points awarded if only some conditions are met.
    """

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    if not file_path.lower().endswith('.docx'):
        print("✗ Provided file is not a DOCX document")
        return 0.0

    # ------------------------------------------------------------------
    # Load the main document XML from the DOCX package
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, 'r') as docx_zip:
            if 'word/document.xml' not in docx_zip.namelist():
                print("✗ 'word/document.xml' part missing – invalid DOCX")
                return 0.0
            document_xml = docx_zip.read('word/document.xml')
    except Exception as e:
        print(f"✗ Error opening DOCX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # Parse XML and locate tables
    # ------------------------------------------------------------------
    try:
        root = etree.fromstring(document_xml)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        tables = root.xpath('//w:tbl', namespaces=ns)
    except Exception as e:
        print(f"✗ XML parsing error: {e}")
        return 0.0

    table_count = len(tables)
    print(f"Found {table_count} table(s) in document")

    if table_count == 0:
        print("✗ No tables to verify – task incomplete")
        return 0.0

    # At least one table present → 0.2 points
    total_score = 0.2

    # ------------------------------------------------------------------
    # Evaluate each table's border configuration
    # ------------------------------------------------------------------
    qualifying_tables = 0
    outer_removed_tables = 0
    inner_kept_tables = 0

    for idx, tbl in enumerate(tables, start=1):
        tbl_borders = tbl.xpath('.//w:tblBorders', namespaces=ns)
        if not tbl_borders:
            print(f"  Table {idx}: no <w:tblBorders> element – skipping")
            continue

        borders_elem = tbl_borders[0]

        def get_border_val(name: str):
            el = borders_elem.find(f'{{{ns["w"]}}}{name}')
            return None if el is None else el.get(f'{{{ns["w"]}}}val')

        # Outer borders should be nil or absent
        outer_ok = all(get_border_val(n) in (None, 'nil') for n in ['top', 'left', 'bottom', 'right'])
        # Inner borders should be explicitly present and not nil
        inner_ok = all(get_border_val(n) not in (None, 'nil') for n in ['insideH', 'insideV'])

        print(f"  Table {idx}: outer_ok={outer_ok}, inner_ok={inner_ok}")

        if outer_ok:
            outer_removed_tables += 1
        if inner_ok:
            inner_kept_tables += 1
        if outer_ok and inner_ok:
            qualifying_tables += 1

    # ------------------------------------------------------------------
    # Scoring logic
    # ------------------------------------------------------------------
    if qualifying_tables > 0:
        # Perfect fulfilment on at least one table → full remaining 0.8 pts
        total_score += 0.8
        print(f"✓ {qualifying_tables} table(s) meet all criteria (inner gridlines kept, outer borders removed)")
    else:
        # Partial fulfilment cases
        if outer_removed_tables > 0:
            total_score += 0.4  # Outer borders removed but inner not guaranteed
            print(f"• {outer_removed_tables} table(s) have outer borders removed (partial credit 0.4)")
        if inner_kept_tables > 0:
            total_score += 0.4  # Inner borders kept but outer not removed
            print(f"• {inner_kept_tables} table(s) keep inner gridlines (partial credit 0.4)")

    final_score = min(total_score, 1.0)
    print(f"Final Score: {final_score}")
    return final_score


if __name__ == "__main__":
    test_file = "/home/user/table_1_is_framed_by_a_thick_border_that_makes_the_page_look_cramped_i_just_want_the_inner_gridlines.docx"
    reward = verify_table_borders(test_file)
    print(f"REWARD: {reward}")
