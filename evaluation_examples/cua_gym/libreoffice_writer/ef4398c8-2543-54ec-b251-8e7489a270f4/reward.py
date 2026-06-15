"""
Reward Script: Convert JSON to Writer table sorted by response_time_ms descending
Task ID: osworld_multi_apps_json_reformat_writer_007
Domain: libreoffice_writer
Scoring:
  - Component 1: Header note present above table (0.3 pts)
  - Component 2: Table exists with 5 columns and 11 rows (1 header + 10 data) (0.3 pts)
  - Component 3: Table data sorted by response_time_ms descending (0.4 pts)
"""

import os

FILE_PATH = '/home/user/Documents/api_response.odt'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_007'

EXPECTED_HEADER = 'API Performance Log \u2014 sorted by response time'
EXPECTED_SORTED_TIMES = [2300, 1850, 980, 640, 490, 310, 220, 185, 120, 45]
EXPECTED_COLUMNS = ['timestamp', 'endpoint', 'method', 'status_code', 'response_time_ms']


def get_cell_text(cell):
    """Extract text from a table cell."""
    from odf.text import P
    txt = ''
    for para in cell.getElementsByType(P):
        for node in para.childNodes:
            if node.nodeType == node.TEXT_NODE:
                txt += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        txt += child.data
    return txt.strip()


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

        doc = load(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file ' + file_path + ': ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    # Component 1: Header note present above table (0.3 points)
    # The header note "API Performance Log — sorted by response time" should be the first paragraph
    try:
        paras = doc.getElementsByType(P)
        header_found = False

        if paras:
            first_para = paras[0]
            # Extract all text from the first paragraph (including spans)
            para_text = ''
            for node in first_para.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    para_text += node.data
                elif hasattr(node, 'childNodes'):
                    for child in node.childNodes:
                        if child.nodeType == child.TEXT_NODE:
                            para_text += child.data
            para_text = para_text.strip()

            if para_text == EXPECTED_HEADER:
                header_found = True
                print('PASS: Component 1 - Header note found: ' + repr(para_text) + ' (0.3 pts)')
                total_score += 0.3
            else:
                # Check if it exists anywhere in the document paragraphs
                for para in paras:
                    ptxt = ''
                    for node in para.childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            ptxt += node.data
                        elif hasattr(node, 'childNodes'):
                            for child in node.childNodes:
                                if child.nodeType == child.TEXT_NODE:
                                    ptxt += child.data
                    ptxt = ptxt.strip()
                    if ptxt == EXPECTED_HEADER:
                        header_found = True
                        print('PASS: Component 1 - Header note found (not first para): ' + repr(ptxt) + ' (0.3 pts)')
                        total_score += 0.3
                        break

                if not header_found:
                    print('FAIL: Component 1 - Expected header: ' + repr(EXPECTED_HEADER) + ', found first para: ' + repr(para_text))
    except Exception as e:
        print('ERROR: Component 1 - ' + str(e))

    # Component 2: Table exists with correct structure (5 columns, 11 rows) (0.3 points)
    # Table should have 1 header row + 10 data rows = 11 rows
    try:
        tables = doc.getElementsByType(Table)

        if not tables:
            print('FAIL: Component 2 - No table found in document')
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)
            num_rows = len(rows)

            if num_rows == 0:
                print('FAIL: Component 2 - Table has no rows')
            else:
                # Check header row columns
                header_row = rows[0]
                header_cells = header_row.getElementsByType(TableCell)
                num_cols = len(header_cells)

                if num_cols == 5 and num_rows == 11:
                    # Check column names
                    col_texts = [get_cell_text(c) for c in header_cells]
                    cols_match = all(col_texts[i] == EXPECTED_COLUMNS[i] for i in range(5))
                    if cols_match:
                        print('PASS: Component 2 - Table structure correct: 11 rows x 5 cols, correct headers (0.3 pts)')
                        total_score += 0.3
                    else:
                        # Partial: right shape but wrong column names
                        print('FAIL: Component 2 - Table shape OK (11x5) but columns wrong: ' + str(col_texts) + ' expected: ' + str(EXPECTED_COLUMNS))
                else:
                    print('FAIL: Component 2 - Expected 11 rows x 5 cols, found ' + str(num_rows) + ' rows x ' + str(num_cols) + ' cols')
    except Exception as e:
        print('ERROR: Component 2 - ' + str(e))

    # Component 3: Table sorted by response_time_ms descending (0.4 points)
    # First data row should have 2300ms, last data row should have 45ms
    # All rows should be in descending order
    try:
        tables = doc.getElementsByType(Table)

        if not tables:
            print('FAIL: Component 3 - No table found, cannot check sort order')
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)

            if len(rows) < 2:
                print('FAIL: Component 3 - Not enough rows to check sort order')
            else:
                # response_time_ms is in column index 4 (0-based)
                data_rows = rows[1:]  # skip header row
                response_times = []
                valid = True

                for row in data_rows:
                    cells = row.getElementsByType(TableCell)
                    if len(cells) >= 5:
                        rt_text = get_cell_text(cells[4])
                        try:
                            rt_val = int(rt_text)
                            response_times.append(rt_val)
                        except ValueError:
                            print('FAIL: Component 3 - Invalid response_time_ms value: ' + repr(rt_text))
                            valid = False
                            break
                    else:
                        print('FAIL: Component 3 - Row has fewer than 5 cells')
                        valid = False
                        break

                if valid and len(response_times) == 10:
                    is_sorted = all(response_times[i] >= response_times[i+1] for i in range(len(response_times)-1))
                    matches_expected = response_times == EXPECTED_SORTED_TIMES

                    if matches_expected:
                        print('PASS: Component 3 - Table correctly sorted by response_time_ms descending: ' + str(response_times) + ' (0.4 pts)')
                        total_score += 0.4
                    elif is_sorted:
                        # Sorted but not exact expected order (maybe same values)
                        print('PASS: Component 3 - Table is sorted descending (times: ' + str(response_times) + ') (0.4 pts)')
                        total_score += 0.4
                    else:
                        print('FAIL: Component 3 - Table NOT sorted by response_time_ms descending. Got: ' + str(response_times) + ', expected: ' + str(EXPECTED_SORTED_TIMES))
                elif valid:
                    print('FAIL: Component 3 - Expected 10 data rows, found ' + str(len(response_times)))
    except Exception as e:
        print('ERROR: Component 3 - ' + str(e))

    final_score = min(total_score, 1.0)
    print('')
    print('Score: ' + str(total_score) + '/1.0')
    print('REWARD: ' + str(final_score))
    return final_score


if not os.path.exists(FILE_PATH):
    print('File not found: ' + FILE_PATH)
    print('REWARD: 0.0')
else:
    verify_task(FILE_PATH)
