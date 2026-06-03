"""
Reward Script: Reformat event_log.odt from raw JSON to structured Writer document
Task ID: osworld_multi_apps_json_reformat_writer_011
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Statistics summary block at top with correct counts
  Component 2 (0.35): Main log table with 20 rows and correct flat fields
  Component 3 (0.30): 4 ERROR metadata sub-tables (one per ERROR event)
  Component 4 (0.10): Raw JSON array deleted from document
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_011'
FILE_PATH = f'{WORKDIR}/event_log.odt'


def persist_app_state():
    """Send Ctrl+S to save any unsaved LibreOffice edits."""
    try:
        import time
        os.environ['DISPLAY'] = ':0'
        import pyautogui
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1.0)
        print('PERSIST: ctrl+s sent for libreoffice_writer')
    except Exception as e:
        print(f'PERSIST_WARN: save hook failed: {e}')


def get_all_paragraph_text(doc):
    """Extract all paragraph text from an ODF document."""
    from odf.text import P
    texts = []
    for elem in doc.body.getElementsByType(P):
        text = ''
        for node in elem.childNodes:
            if hasattr(node, 'data'):
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        text += child.data
        texts.append(text)
    return texts


def get_table_cell_text(cell):
    """Get all text from a table cell."""
    from odf.text import P
    text = ''
    for p in cell.getElementsByType(P):
        for node in p.childNodes:
            if hasattr(node, 'data'):
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        text += child.data
    return text.strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f'CRITICAL: Cannot load file {file_path}: {e}')
        print('REWARD: 0.0')
        return 0.0

    # Get all paragraph text for searching
    all_para_texts = get_all_paragraph_text(doc)
    full_text = '\n'.join(all_para_texts)

    # Get all tables
    try:
        from odf.table import Table, TableRow, TableCell
        tables = doc.body.getElementsByType(Table)
    except Exception as e:
        print(f'ERROR: Cannot get tables: {e}')
        tables = []

    # -------------------------------------------------------------------------
    # Component 4: Raw JSON deleted (0.10 points)
    # Check that no raw JSON array is present in the document
    # This FAILS on initial (has JSON) and PASSES on golden (JSON removed)
    # -------------------------------------------------------------------------
    try:
        has_json_array = bool(re.search(r'\{\s*"event_id"', full_text, re.DOTALL))
        has_json_open_bracket = bool(re.search(r'^\s*\[\s*$', full_text, re.MULTILINE) and
                                     re.search(r'"event_id".*"timestamp"', full_text, re.DOTALL))
        json_present = has_json_array or has_json_open_bracket

        if not json_present:
            print('PASS: Component 4 — Raw JSON array deleted from document (0.10 pts)')
            total_score += 0.10
        else:
            print('FAIL: Component 4 — Raw JSON array still present in document')
    except Exception as e:
        print(f'ERROR: Component 4 — {e}')

    # -------------------------------------------------------------------------
    # Component 1: Statistics summary block (0.25 points)
    # Must contain: Total Events: 20, INFO: 10, WARN: 6, ERROR: 4,
    # plus per-component counts
    # This FAILS on initial (no stats block) and PASSES on golden (has stats)
    # -------------------------------------------------------------------------
    try:
        stats_checks = {
            'Total Events: 20': bool(re.search(r'Total\s+Events:\s*20', full_text, re.IGNORECASE)),
            'INFO: 10': bool(re.search(r'INFO:\s*10', full_text)),
            'WARN: 6': bool(re.search(r'WARN:\s*6', full_text)),
            'ERROR: 4': bool(re.search(r'ERROR:\s*4', full_text)),
            'AuthService: 5': bool(re.search(r'AuthService:\s*5', full_text)),
            'DataPipeline: 5': bool(re.search(r'DataPipeline:\s*5', full_text)),
        }

        stats_passed = sum(1 for v in stats_checks.values() if v)
        stats_total = len(stats_checks)

        if stats_passed == stats_total:
            print(f'PASS: Component 1 — Statistics block complete ({stats_passed}/{stats_total} checks) (0.25 pts)')
            total_score += 0.25
        elif stats_passed >= 3:
            print(f'PARTIAL: Component 1 — Statistics block partially complete ({stats_passed}/{stats_total} checks) (0.12 pts)')
            total_score += 0.12
        else:
            print(f'FAIL: Component 1 — Statistics block missing or incomplete ({stats_passed}/{stats_total} checks passed)')
            for k, v in stats_checks.items():
                print(f'  {"PASS" if v else "FAIL"}: {k}')
    except Exception as e:
        print(f'ERROR: Component 1 — {e}')

    # -------------------------------------------------------------------------
    # Component 2: Main log table with 20 rows and flat fields (0.35 points)
    # Table must have header row + 20 data rows (21 total)
    # Headers: Event ID, Timestamp, Level, Component, Message
    # All 20 events must be present
    # This FAILS on initial (no table) and PASSES on golden (has 21-row table)
    # -------------------------------------------------------------------------
    try:
        main_table_found = False
        main_table_row_count = 0
        has_correct_headers = False
        event_ids_found = 0

        for t in tables:
            rows = t.getElementsByType(TableRow)
            if len(rows) >= 21:
                # Check headers
                if rows:
                    cells = rows[0].getElementsByType(TableCell)
                    header_texts = [get_table_cell_text(c) for c in cells]
                    # Check for expected header columns
                    header_str = ' '.join(header_texts).lower()
                    if 'event' in header_str and 'timestamp' in header_str and 'level' in header_str:
                        has_correct_headers = True

                # Count EVT- entries in the table
                evt_count = 0
                for row in rows[1:]:
                    cells = row.getElementsByType(TableCell)
                    for cell in cells:
                        cell_text = get_table_cell_text(cell)
                        if re.match(r'EVT-\d+', cell_text):
                            evt_count += 1
                            break

                if has_correct_headers and evt_count >= 18:
                    main_table_found = True
                    main_table_row_count = len(rows)
                    event_ids_found = evt_count
                    break

        if main_table_found and event_ids_found == 20:
            print(f'PASS: Component 2 — Main log table with {main_table_row_count} rows, {event_ids_found}/20 events (0.35 pts)')
            total_score += 0.35
        elif main_table_found and event_ids_found >= 18:
            print(f'PARTIAL: Component 2 — Main log table found but only {event_ids_found}/20 events (0.20 pts)')
            total_score += 0.20
        elif has_correct_headers:
            print(f'PARTIAL: Component 2 — Table with correct headers found but <18 event rows (0.10 pts)')
            total_score += 0.10
        else:
            print(f'FAIL: Component 2 — No main log table with 20+ event rows found')
            print(f'  Tables found: {len(tables)}, largest: {max((len(t.getElementsByType(TableRow)) for t in tables), default=0)} rows')
    except Exception as e:
        print(f'ERROR: Component 2 — {e}')

    # -------------------------------------------------------------------------
    # Component 3: 4 ERROR metadata sub-tables (0.30 points)
    # One sub-table for each ERROR event (EVT-017, EVT-018, EVT-019, EVT-020)
    # Each sub-table has 'Metadata Key' / 'Value' header and key-value rows
    # This FAILS on initial (no metadata tables) and PASSES on golden (has 4)
    # -------------------------------------------------------------------------
    try:
        metadata_tables_found = 0
        error_event_refs_found = 0

        # Check for metadata table references in text
        error_evt_refs = ['EVT-017', 'EVT-018', 'EVT-019', 'EVT-020']
        for evt_id in error_evt_refs:
            if any(evt_id in t for t in all_para_texts):
                error_event_refs_found += 1

        # Check for tables with 'Metadata Key' / 'Value' headers
        for t in tables:
            rows = t.getElementsByType(TableRow)
            if rows:
                cells = rows[0].getElementsByType(TableCell)
                header_texts = [get_table_cell_text(c) for c in cells]
                header_str = ' '.join(header_texts)
                if 'Metadata Key' in header_str and 'Value' in header_str:
                    metadata_tables_found += 1

        # Also check: each metadata table has at least 2 data rows (key-value pairs)
        valid_metadata_tables = 0
        for t in tables:
            rows = t.getElementsByType(TableRow)
            if len(rows) >= 3:  # header + at least 2 data rows
                cells_h = rows[0].getElementsByType(TableCell)
                header_texts = [get_table_cell_text(c) for c in cells_h]
                header_str = ' '.join(header_texts)
                if 'Metadata Key' in header_str or ('Key' in header_str and 'Value' in header_str):
                    # Check for metadata keys like error_code
                    has_error_code = False
                    for row in rows[1:]:
                        cells = row.getElementsByType(TableCell)
                        for cell in cells:
                            ct = get_table_cell_text(cell)
                            if ct in ('error_code', 'stack_trace', 'retry_count', 'host', 'template_path',
                                      'query_id', 'timeout_ms', 'sku', 'affected_user', 'port'):
                                has_error_code = True
                                break
                    if has_error_code:
                        valid_metadata_tables += 1

        if valid_metadata_tables >= 4:
            print(f'PASS: Component 3 — {valid_metadata_tables}/4 ERROR metadata sub-tables found (0.30 pts)')
            total_score += 0.30
        elif valid_metadata_tables == 3:
            print(f'PARTIAL: Component 3 — {valid_metadata_tables}/4 ERROR metadata sub-tables found (0.22 pts)')
            total_score += 0.22
        elif valid_metadata_tables == 2:
            print(f'PARTIAL: Component 3 — {valid_metadata_tables}/4 ERROR metadata sub-tables found (0.15 pts)')
            total_score += 0.15
        elif valid_metadata_tables == 1:
            print(f'PARTIAL: Component 3 — {valid_metadata_tables}/4 ERROR metadata sub-tables found (0.08 pts)')
            total_score += 0.08
        else:
            print(f'FAIL: Component 3 — No valid ERROR metadata sub-tables found')
            print(f'  Metadata-like tables found: {metadata_tables_found}, error event refs in text: {error_event_refs_found}/4')
    except Exception as e:
        print(f'ERROR: Component 3 — {e}')

    final_score = min(round(total_score, 2), 1.0)
    print(f'\nScore: {total_score}/1.0')
    print(f'REWARD: {final_score}')
    return final_score


# Run verification
if not os.path.exists(FILE_PATH):
    print(f'File not found: {FILE_PATH}')
    print('REWARD: 0.0')
else:
    persist_app_state()
    verify_task(FILE_PATH)
