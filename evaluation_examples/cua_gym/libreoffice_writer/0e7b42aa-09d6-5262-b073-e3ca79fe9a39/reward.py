"""
Reward script for writer_legal_025:
Verify that a two-column signature block table with no visible borders
exists at the end of the contract document, containing fields for
ABC Corporation and XYZ Industries.
"""

from docx import Document
from docx.oxml.ns import qn

DOC_PATH = "/home/user/writer_legal_025.docx"


def check_border_invisible(border_elem):
    """Check if a single border element is invisible (none, nil, or zero-width)."""
    if border_elem is None:
        return True
    val = border_elem.get(qn('w:val'))
    if val in ('none', 'nil'):
        return True
    sz = border_elem.get(qn('w:sz'))
    if sz is not None and sz == '0':
        return True
    return False


def check_table_borders_invisible(table):
    """Check if table borders are not visible."""
    tbl = table._tbl
    tbl_pr = tbl.find(qn('w:tblPr'))
    if tbl_pr is None:
        return True  # no properties means default (could be visible)

    tbl_borders = tbl_pr.find(qn('w:tblBorders'))
    if tbl_borders is None:
        # No explicit borders set at table level - check style
        # If no borders element, borders depend on style; we check cells too
        return True

    border_names = ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']
    for name in border_names:
        border_el = tbl_borders.find(qn(f'w:{name}'))
        if not check_border_invisible(border_el):
            return False
    return True


def check_cell_borders_invisible(table):
    """Check cell-level borders are invisible too."""
    for row in table.rows:
        for cell in row.cells:
            tc_pr = cell._tc.find(qn('w:tcPr'))
            if tc_pr is None:
                continue
            tc_borders = tc_pr.find(qn('w:tcBorders'))
            if tc_borders is None:
                continue
            for name in ['top', 'left', 'bottom', 'right']:
                border_el = tc_borders.find(qn(f'w:{name}'))
                if border_el is not None:
                    val = border_el.get(qn('w:val'))
                    if val not in (None, 'none', 'nil'):
                        sz = border_el.get(qn('w:sz'))
                        if sz is None or sz != '0':
                            return False
    return True


def check_column_content(cells_text, expected_party):
    """
    Check if a column contains the expected party name and fields.
    cells_text is a list of cell texts (one per row) for a single column.
    Returns a dict with individual check results.
    """
    # Combine all text from the column
    combined = "\n".join(cells_text).lower()

    results = {
        "party_name": False,
        "signature_line": False,
        "name_field": False,
        "title_field": False,
        "date_field": False,
    }

    # Check party name
    if expected_party.lower() in combined:
        results["party_name"] = True

    # Check for signature line - could be underscores, dashes, or the word "signature"
    if "___" in combined or "---" in combined or "signature" in combined or "sign" in combined:
        results["signature_line"] = True

    # Check fields
    if "name:" in combined or "name :" in combined or "printed name" in combined:
        results["name_field"] = True
    if "title:" in combined or "title :" in combined:
        results["title_field"] = True
    if "date:" in combined or "date :" in combined:
        results["date_field"] = True

    return results


def main():
    score = 0.0

    try:
        doc = Document(DOC_PATH)
    except Exception as e:
        print(f"ERROR: Cannot open document: {e}")
        print(f"REWARD: 0.0")
        return

    tables = doc.tables

    # --- Condition 1 (0.2): Table exists ---
    if len(tables) == 0:
        print("FAIL: No tables found in document.")
        print(f"REWARD: 0.0")
        return

    # Find the best candidate table (last table is most likely the signature block)
    target_table = None
    for t in reversed(tables):
        # Check if it has at least 2 columns
        if len(t.columns) >= 2:
            # Check if it mentions either party
            all_text = ""
            for row in t.rows:
                for cell in row.cells:
                    all_text += cell.text.lower() + " "
            if "abc" in all_text or "xyz" in all_text:
                target_table = t
                break

    if target_table is None:
        # Fall back to last table
        target_table = tables[-1]

    print(f"Found {len(tables)} table(s). Checking signature block table.")
    score += 0.2
    print(f"  +0.20 Table exists. Running score: {score:.2f}")

    # --- Condition 2 (0.15): Table has exactly 2 columns ---
    num_cols = len(target_table.columns)
    if num_cols == 2:
        score += 0.15
        print(f"  +0.15 Table has 2 columns. Running score: {score:.2f}")
    else:
        print(f"  +0.00 Table has {num_cols} columns (expected 2). Running score: {score:.2f}")

    # --- Condition 3 (0.15): No visible borders ---
    table_borders_ok = check_table_borders_invisible(target_table)
    cell_borders_ok = check_cell_borders_invisible(target_table)
    if table_borders_ok and cell_borders_ok:
        score += 0.15
        print(f"  +0.15 Table borders are invisible. Running score: {score:.2f}")
    elif table_borders_ok or cell_borders_ok:
        score += 0.075
        print(f"  +0.075 Table borders partially invisible. Running score: {score:.2f}")
    else:
        print(f"  +0.00 Table has visible borders. Running score: {score:.2f}")

    # --- Condition 4 (0.25): Left column has ABC Corporation content ---
    if num_cols >= 2:
        left_col_texts = []
        right_col_texts = []
        for row in target_table.rows:
            cells = row.cells
            left_col_texts.append(cells[0].text)
            right_col_texts.append(cells[1].text)

        # Determine which column has which party
        left_combined = "\n".join(left_col_texts).lower()
        right_combined = "\n".join(right_col_texts).lower()

        # ABC could be in either column; detect layout
        if "abc" in left_combined and "xyz" in right_combined:
            abc_texts = left_col_texts
            xyz_texts = right_col_texts
        elif "abc" in right_combined and "xyz" in left_combined:
            abc_texts = right_col_texts
            xyz_texts = left_col_texts
        else:
            # Try best guess - left=ABC, right=XYZ as specified in task
            abc_texts = left_col_texts
            xyz_texts = right_col_texts

        abc_results = check_column_content(abc_texts, "ABC Corporation")
        abc_checks = sum(abc_results.values())
        abc_score = 0.25 * (abc_checks / 5.0)
        score += abc_score
        print(f"  +{abc_score:.3f} ABC Corporation column: {abc_results}. Running score: {score:.2f}")

        # --- Condition 5 (0.25): Right column has XYZ Industries content ---
        xyz_results = check_column_content(xyz_texts, "XYZ Industries")
        xyz_checks = sum(xyz_results.values())
        xyz_score = 0.25 * (xyz_checks / 5.0)
        score += xyz_score
        print(f"  +{xyz_score:.3f} XYZ Industries column: {xyz_results}. Running score: {score:.2f}")
    else:
        print(f"  +0.00 Cannot check column content (not 2 columns). Running score: {score:.2f}")

    # Clamp score
    score = round(min(max(score, 0.0), 1.0), 2)
    # Handle floating point: if very close to 1.0, round up
    if score >= 0.99:
        score = 1.0
    print(f"REWARD: {score}")


if __name__ == "__main__":
    main()
