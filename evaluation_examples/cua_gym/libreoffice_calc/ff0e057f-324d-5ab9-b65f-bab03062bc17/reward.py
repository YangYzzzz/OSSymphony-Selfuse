"""
Reward Script: Batch convert .docx to PDF, merge PDFs, rename with date, log to ODS
Task ID: osworld_multi_apps_doc_batch_convert_008
Domain: libreoffice_calc (ODS file)
Scoring:
  - Component 1: ODS conversion_log sheet has 6 data rows (0.30 pts)
  - Component 2: All 6 rows have Status='Success' (0.25 pts)
  - Component 3: 6 date-stamped PDF files exist in batch_docs/ (0.25 pts)
  - Component 4: combined.pdf exists in batch_docs/ (0.20 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_batch_convert_008'
BATCH_DOCS_DIR = '/home/user/Desktop/batch_docs'
ODS_FILE = f'{WORKDIR}/{TASK_ID}.ods'

# Expected docx basenames (without .docx extension)
EXPECTED_DOCX_BASENAMES = [
    'hr_policy_remote_work',
    'meeting_minutes_2025_03',
    'project_proposal_webapp',
    'quarterly_report_q1',
    'technical_spec_api_v2',
    'training_guide_onboarding',
]


def read_ods_sheet(file_path):
    """
    Read the conversion_log sheet from an ODS file using odfpy.
    Returns: (sheet_name, list_of_row_lists) or raises exception.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        raise ValueError("No sheets found in ODS file")

    result = []
    for sheet in sheets:
        name = sheet.getAttribute("name")
        rows_data = []
        for row in sheet.getElementsByType(TableRow):
            cells = row.getElementsByType(TableCell)
            row_vals = []
            for cell in cells:
                texts = cell.getElementsByType(P)
                row_vals.append(str(texts[0]) if texts else '')
            rows_data.append(row_vals)
        result.append((name, rows_data))
    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: ODS file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS file
    try:
        sheets = read_ods_sheet(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the conversion_log sheet (or first sheet)
    log_sheet = None
    for (name, rows) in sheets:
        name_lower = name.lower().replace(' ', '_').replace('-', '_')
        if 'conversion' in name_lower or 'log' in name_lower:
            log_sheet = (name, rows)
            break
    if log_sheet is None and sheets:
        log_sheet = sheets[0]

    if log_sheet is None:
        print("CRITICAL: No sheets found in ODS file")
        print("REWARD: 0.0")
        return 0.0

    sheet_name, rows = log_sheet
    print(f"INFO: Using sheet '{sheet_name}' with {len(rows)} rows")

    # Identify header row and data rows
    # Skip header row (first row with 'Filename' or similar)
    data_rows = []
    header_found = False
    for row in rows:
        if not header_found:
            # Check if this is a header row
            non_empty = [c for c in row if c.strip()]
            if non_empty:
                col_values = [c.strip().lower() for c in row if c.strip()]
                if any(v in ('filename', 'file', 'name') for v in col_values):
                    header_found = True
                    # Find column indices from header
                    header = [c.strip().lower() for c in row]
                    print(f"INFO: Header row: {[c.strip() for c in row if c.strip()]}")
                    continue
                else:
                    # No recognizable header — treat all rows as data
                    header_found = True
                    data_rows.append(row)
        else:
            # Check if row has at least one non-empty cell
            if any(c.strip() for c in row):
                data_rows.append(row)

    print(f"INFO: Data rows found: {len(data_rows)}")

    # ------------------------------------------------------------------
    # Component 1: Conversion log has exactly 6 data rows (0.30 points)
    # The initial_env has 0 data rows; golden_env has 6.
    # ------------------------------------------------------------------
    try:
        if len(data_rows) == 6:
            print(f"PASS: Component 1 — conversion_log has exactly 6 data rows (0.30 pts)")
            total_score += 0.30
        elif len(data_rows) > 0:
            partial = round(0.30 * len(data_rows) / 6, 4)
            print(f"PARTIAL: Component 1 — conversion_log has {len(data_rows)}/6 data rows ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — conversion_log has 0 data rows (expected 6)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: All 6 data rows have Status='Success' (0.25 points)
    # Status is in column index 3 (0-based): Filename, Original_Size, PDF_Size, Status, Timestamp
    # ------------------------------------------------------------------
    try:
        if data_rows:
            # Determine Status column index
            status_col = 3  # default (0-indexed)
            if header_found and 'header' in dir():
                pass  # Use default
            # Try to find status column from header
            try:
                for i, h in enumerate([c.strip().lower() for c in rows[0] if c.strip()]):
                    if h == 'status':
                        status_col = i
                        break
            except Exception:
                pass

            success_rows = 0
            for row in data_rows:
                if len(row) > status_col:
                    status_val = row[status_col].strip()
                    if status_val.lower() == 'success':
                        success_rows += 1
                    else:
                        print(f"  INFO: Row status = '{status_val}' (not 'Success')")
                else:
                    print(f"  INFO: Row too short (len={len(row)}), cannot get status")

            if success_rows == 6:
                print(f"PASS: Component 2 — all 6 rows have Status='Success' (0.25 pts)")
                total_score += 0.25
            elif success_rows > 0:
                partial = round(0.25 * success_rows / 6, 4)
                print(f"PARTIAL: Component 2 — {success_rows}/6 rows have Status='Success' ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — 0 rows have Status='Success'")
        else:
            print(f"FAIL: Component 2 — no data rows to check Status")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: 6 date-stamped PDF files exist in batch_docs/ (0.25 pts)
    # e.g. hr_policy_remote_work_20260306.pdf
    # Pattern: <basename>_<YYYYMMDD>.pdf
    # ------------------------------------------------------------------
    try:
        if os.path.isdir(BATCH_DOCS_DIR):
            all_files = os.listdir(BATCH_DOCS_DIR)
            # Date-stamped PDF pattern: ends with _YYYYMMDD.pdf
            date_pdf_pattern = re.compile(r'^.+_\d{8}\.pdf$')
            date_stamped_pdfs = [f for f in all_files if date_pdf_pattern.match(f)]
            print(f"INFO: Date-stamped PDFs found in batch_docs: {sorted(date_stamped_pdfs)}")

            if len(date_stamped_pdfs) == 6:
                print(f"PASS: Component 3 — 6 date-stamped PDF files found (0.25 pts)")
                total_score += 0.25
            elif len(date_stamped_pdfs) > 0:
                partial = round(0.25 * len(date_stamped_pdfs) / 6, 4)
                print(f"PARTIAL: Component 3 — {len(date_stamped_pdfs)}/6 date-stamped PDFs ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — no date-stamped PDFs found in {BATCH_DOCS_DIR}")
        else:
            print(f"FAIL: Component 3 — batch_docs directory not found at {BATCH_DOCS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: combined.pdf exists in batch_docs/ (0.20 points)
    # This is the merged PDF of the first 3 individual PDFs.
    # ------------------------------------------------------------------
    try:
        combined_path = os.path.join(BATCH_DOCS_DIR, 'combined.pdf')
        if os.path.exists(combined_path):
            size = os.path.getsize(combined_path)
            if size > 0:
                print(f"PASS: Component 4 — combined.pdf exists and is non-empty ({size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — combined.pdf exists but is empty")
        else:
            print(f"FAIL: Component 4 — combined.pdf not found in {BATCH_DOCS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(ODS_FILE):
    print(f"File not found: {ODS_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(ODS_FILE)
