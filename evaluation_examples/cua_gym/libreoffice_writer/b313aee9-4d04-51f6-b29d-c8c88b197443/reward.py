"""
Reward Script: Copy project data from 'projects.ods' into a formatted Writer table with
bold headers and add a caption 'Table 1: Active Projects Q4 2024' above the table.
Task ID: osworld_multi_apps_doc_calc_to_writer_005
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): status_report.odt exists and contains a table with correct shape (9 rows x 6 cols)
  Component 2 (0.40): Header row (row 0) has bold formatting on all 6 cells
  Component 3 (0.30): Caption text "Table 1: Active Projects Q4 2024" appears in a caption-style paragraph
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_005'
FILE_PATH = os.path.join(WORKDIR, 'status_report.odt')

EXPECTED_HEADERS = ['Project Name', 'Owner', 'Status', 'Due Date', 'Budget', 'Completion %']
CAPTION_TEXT = 'Table 1: Active Projects Q4 2024'
EXPECTED_ROWS = 9   # 1 header + 8 data rows
EXPECTED_COLS = 6


def get_cell_text(cell, para_type):
    """Extract text from an ODT table cell."""
    paras = cell.getElementsByType(para_type)
    text = ''
    for para in paras:
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        text += child.data
    return text.strip()


def is_span_bold(span, auto_styles):
    """Check if a text span has bold font-weight in automatic styles."""
    span_style = None
    try:
        span_style = span.getAttribute('stylename')
    except Exception:
        pass
    if not span_style:
        return False
    for s in auto_styles.childNodes:
        try:
            s_attrs = dict(s.attributes)
            s_name = None
            for k, v in s_attrs.items():
                if 'name' in k:
                    s_name = v
                    break
            if s_name == span_style:
                for prop in s.childNodes:
                    p_attrs = dict(prop.attributes)
                    for k, v in p_attrs.items():
                        if 'font-weight' in str(k) and v == 'bold':
                            return True
        except Exception:
            pass
    return False


def para_is_caption_style(para, auto_styles):
    """
    Return True if the paragraph uses a style whose parent-style-name is 'caption'
    (case-insensitive), or whose style name contains 'caption'.

    ODT attribute keys are (namespace_uri, local_name) tuples.
    We match by checking if the local_name part of the tuple contains the expected string.
    """
    try:
        style_name = para.getAttribute('stylename')
    except Exception:
        return False
    if not style_name:
        return False
    # Also accept if style name itself contains 'caption'
    if 'caption' in str(style_name).lower():
        return True
    # Check automatic styles: find the style with this name and check parent-style-name
    for s in auto_styles.childNodes:
        try:
            s_attrs = dict(s.attributes)
            # Extract the 'name' attribute value
            s_name = None
            for (ns, local), v in s_attrs.items():
                if local == 'name' and 'parent' not in local:
                    s_name = v
                    break
            if s_name != style_name:
                continue
            # Now check for parent-style-name containing 'caption'
            for (ns, local), v in s_attrs.items():
                if local == 'parent-style-name' and 'caption' in str(v).lower():
                    return True
        except Exception:
            pass
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"FAIL: status_report.odt not found at {file_path}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODT document
    try:
        from odf.opendocument import load
        from odf.text import P
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: status_report.odt contains a table with correct shape (0.30 points)
    # Checks: at least 1 table, 9 rows, 6 columns
    try:
        tables = doc.getElementsByType(Table)
        if len(tables) == 0:
            print(f"FAIL: Component 1 — No tables found in status_report.odt")
        else:
            tbl = tables[0]
            rows = tbl.getElementsByType(TableRow)
            num_rows = len(rows)

            if num_rows != EXPECTED_ROWS:
                print(f"FAIL: Component 1 — Expected {EXPECTED_ROWS} rows, found {num_rows}")
            else:
                # Check column count in first row
                first_row_cells = rows[0].getElementsByType(TableCell)
                num_cols = len(first_row_cells)
                if num_cols != EXPECTED_COLS:
                    print(f"FAIL: Component 1 — Expected {EXPECTED_COLS} columns in header row, found {num_cols}")
                else:
                    print(f"PASS: Component 1 — Table found with {num_rows} rows x {num_cols} cols (0.30 pts)")
                    total_score += 0.30
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header row has bold formatting on all cells (0.40 points)
    # The header row cells should have spans with bold font-weight
    try:
        from odf.text import Span
        tables = doc.getElementsByType(Table)
        if len(tables) == 0:
            print("FAIL: Component 2 — No tables found, cannot check header bold")
        else:
            tbl = tables[0]
            rows = tbl.getElementsByType(TableRow)
            if len(rows) == 0:
                print("FAIL: Component 2 — No rows found in table")
            else:
                first_row = rows[0]
                cells = first_row.getElementsByType(TableCell)
                bold_count = 0
                total_header_cells = len(cells)
                for cell in cells:
                    paras = cell.getElementsByType(P)
                    cell_is_bold = False
                    for para in paras:
                        for node in para.childNodes:
                            # Check spans with bold style
                            if hasattr(node, 'tagName') and 'span' in str(node.tagName).lower():
                                if is_span_bold(node, doc.automaticstyles):
                                    cell_is_bold = True
                    if cell_is_bold:
                        bold_count += 1

                if bold_count == total_header_cells and total_header_cells == EXPECTED_COLS:
                    print(f"PASS: Component 2 — All {EXPECTED_COLS} header cells are bold (0.40 pts)")
                    total_score += 0.40
                elif bold_count > 0:
                    print(f"FAIL: Component 2 — Only {bold_count}/{total_header_cells} header cells are bold")
                else:
                    print(f"FAIL: Component 2 — No bold header cells found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Caption "Table 1: Active Projects Q4 2024" appears above the table (0.30 points)
    # The caption should be in a paragraph using a 'caption' style (or parent caption)
    try:
        paras = doc.getElementsByType(P)
        caption_found = False
        caption_in_caption_style = False

        for para in paras:
            # Get full text of this paragraph
            text = ''
            for node in para.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text += node.data
                elif hasattr(node, 'childNodes'):
                    for child in node.childNodes:
                        if child.nodeType == child.TEXT_NODE:
                            text += child.data
            text = text.strip()

            if CAPTION_TEXT in text:
                caption_found = True
                # Check if it's in caption style
                if para_is_caption_style(para, doc.automaticstyles):
                    caption_in_caption_style = True
                    break

        if caption_found and caption_in_caption_style:
            print(f"PASS: Component 3 — Caption '{CAPTION_TEXT}' found in caption style (0.30 pts)")
            total_score += 0.30
        elif caption_found:
            # Caption text exists but not in caption style — partial credit considered,
            # but since the task specifically requires Caption style, no points
            print(f"FAIL: Component 3 — Caption text found but NOT in caption style")
        else:
            print(f"FAIL: Component 3 — Caption text '{CAPTION_TEXT}' NOT found in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
