"""
Reward Script: Open 'product_data.odt', reformat JSON as a two-column table (Key|Value), delete original JSON text, save.
Task ID: osworld_multi_apps_json_reformat_writer_001
Domain: libreoffice_writer
Scoring:
  Component 1: Table exists with 2 columns (0.3 pts)
  Component 2: Header row contains 'Key' and 'Value' (0.3 pts)
  Component 3: All 5 data rows present with correct key-value pairs (0.3 pts)
  Component 4: Original JSON text is absent from document body (0.1 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_001'

# Expected table data (ground truth from task context)
EXPECTED_HEADER = ('Key', 'Value')
EXPECTED_DATA_ROWS = [
    ('name', 'Widget Pro'),
    ('price', '29.99'),
    ('category', 'Tools'),
    ('stock', '150'),
    ('sku', 'WP-001'),
]
JSON_SNIPPET = '"name"'  # substring that only appears in the original JSON text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P
        from odf.table import Table, TableRow, TableCell
    except ImportError as e:
        print(f"CRITICAL: Cannot import odf library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts (including those inside table cells)
    def get_cell_text(cell):
        text = ''
        for p in cell.getElementsByType(P):
            for node in p.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text += node.data
        return text.strip()

    # Gather top-level paragraph texts (outside tables)
    body_paragraphs = []
    try:
        for p in doc.getElementsByType(P):
            text = ''
            for node in p.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text += node.data
            body_paragraphs.append(text)
    except Exception as e:
        print(f"ERROR: Could not read paragraphs: {e}")

    # Component 1: Table with 2 columns exists (0.3 points)
    # On initial_env: no tables → FAIL. On golden_env: 1 table with 2 cols → PASS.
    try:
        tables = doc.getElementsByType(Table)
        valid_table = None
        for table in tables:
            rows = table.getElementsByType(TableRow)
            if len(rows) >= 1:
                first_row = rows[0]
                cells = first_row.getElementsByType(TableCell)
                if len(cells) == 2:
                    valid_table = table
                    break

        if valid_table is not None:
            print(f"PASS: Component 1 — Table with 2 columns found (0.3 pts)")
            total_score += 0.3
        else:
            num_tables = len(doc.getElementsByType(Table))
            print(f"FAIL: Component 1 — Expected a table with 2 columns, found {num_tables} table(s) with no valid 2-column table")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header row is 'Key' | 'Value' (0.3 points)
    # On initial_env: no tables → FAIL. On golden_env: header row present → PASS.
    try:
        if valid_table is not None:
            rows = valid_table.getElementsByType(TableRow)
            header_row = rows[0]
            header_cells = header_row.getElementsByType(TableCell)
            col0_text = get_cell_text(header_cells[0])
            col1_text = get_cell_text(header_cells[1])

            if col0_text.lower() == 'key' and col1_text.lower() == 'value':
                print(f"PASS: Component 2 — Header row is '{col0_text}' | '{col1_text}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Header expected 'Key'|'Value', found '{col0_text}'|'{col1_text}'")
        else:
            print("FAIL: Component 2 — No valid table found to check header")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 data rows with correct key-value pairs (0.3 points)
    # On initial_env: no tables → FAIL. On golden_env: all 5 pairs → PASS.
    try:
        if valid_table is not None:
            rows = valid_table.getElementsByType(TableRow)
            data_rows = rows[1:]  # skip header
            found_pairs = []
            for row in data_rows:
                cells = row.getElementsByType(TableCell)
                if len(cells) == 2:
                    k = get_cell_text(cells[0])
                    v = get_cell_text(cells[1])
                    found_pairs.append((k, v))

            matches = 0
            for expected_k, expected_v in EXPECTED_DATA_ROWS:
                # Match key exactly; value can be string-equal (numbers may be stored as strings)
                for fk, fv in found_pairs:
                    if fk.strip().lower() == expected_k.lower() and fv.strip() == expected_v:
                        matches += 1
                        break

            if matches == len(EXPECTED_DATA_ROWS):
                print(f"PASS: Component 3 — All {matches}/{len(EXPECTED_DATA_ROWS)} data rows correct (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Only {matches}/{len(EXPECTED_DATA_ROWS)} data rows matched. Found: {found_pairs}")
        else:
            print("FAIL: Component 3 — No valid table found to check data rows")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original JSON text removed from document body (0.1 points)
    # On initial_env: JSON text present → FAIL. On golden_env: no JSON text → PASS.
    try:
        # Check all paragraph texts for JSON-like content (curly brace with key-value pattern)
        all_doc_text = ' '.join(body_paragraphs)
        json_still_present = ('{' in all_doc_text and '"name"' in all_doc_text)

        if not json_still_present:
            print(f"PASS: Component 4 — JSON text has been removed from the document (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — JSON text still present in document body")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/product_data.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
