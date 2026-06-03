"""
Reward Script: NSF ML Grant Research Task
Task ID: osworld_multi_apps_web_faculty_014
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.4): File contains required columns AND at least 15 data rows
  Component 2 (0.3): Grant data references target institutions (MIT, Stanford, Berkeley)
  Component 3 (0.3): Summary section with average award amounts by institution
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_FILE = '/home/user/Desktop/nsf_ml_grants.ods'

# ODS XML namespaces
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'

REQUIRED_COLUMNS = {'PI_Name', 'Institution', 'Award_Amount', 'Project_Title',
                    'Start_Date', 'End_Date', 'Award_Number'}

TARGET_INSTITUTIONS = {'MIT', 'Stanford', 'Berkeley'}


def get_cell_text(cell):
    """Extract text or numeric value from an ODS table-cell element."""
    value_type = cell.get(f'{{{OFFICE_NS}}}value-type')
    value = cell.get(f'{{{OFFICE_NS}}}value')
    # For numeric/currency/percentage cells, use the numeric value attribute
    if value is not None and value_type in ('float', 'currency', 'percentage'):
        return value
    # For text/date cells, extract text content
    texts = []
    for t in cell.findall(f'.//{{{TEXT_NS}}}p'):
        if t.text:
            texts.append(t.text)
        for span in t:
            if span.text:
                texts.append(span.text)
            if span.tail:
                texts.append(span.tail)
        if t.tail:
            texts.append(t.tail)
    return ' '.join(texts).strip()


def parse_ods(file_path):
    """
    Parse an ODS file and return list of sheets, each as list of rows (list of strings).
    Returns None on error.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            with z.open('content.xml') as f:
                content = f.read().decode('utf-8')
    except Exception as e:
        print(f"ERROR: Cannot open ODS file {file_path}: {e}")
        return None

    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"ERROR: Cannot parse ODS XML: {e}")
        return None

    sheets = {}
    for sheet in root.findall(f'.//{{{TABLE_NS}}}table'):
        name = sheet.get(f'{{{TABLE_NS}}}name', 'Sheet')
        rows_data = []
        for row in sheet.findall(f'{{{TABLE_NS}}}table-row'):
            cells = (row.findall(f'{{{TABLE_NS}}}table-cell') +
                     row.findall(f'{{{TABLE_NS}}}covered-table-cell'))
            row_vals = []
            for cell in cells:
                repeat = int(cell.get(f'{{{TABLE_NS}}}number-columns-repeated', 1))
                val = get_cell_text(cell)
                # Cap repeat to avoid huge empty expansions
                for _ in range(min(repeat, 50)):
                    row_vals.append(val)
            # Trim trailing empty cells
            while row_vals and row_vals[-1] == '':
                row_vals.pop()
            rows_data.append(row_vals)
        # Trim trailing empty rows
        while rows_data and not rows_data[-1]:
            rows_data.pop()
        sheets[name] = rows_data
    return sheets


def verify_task(file_path):
    """
    Verify task completion for NSF ML Grants research task.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be parseable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    sheets = parse_ods(file_path)
    if sheets is None:
        print("CRITICAL: Could not parse ODS file")
        print("REWARD: 0.0")
        return 0.0

    if not sheets:
        print("CRITICAL: ODS file has no sheets")
        print("REWARD: 0.0")
        return 0.0

    # Use the first sheet (or named sheet if present)
    sheet_name = list(sheets.keys())[0]
    rows = sheets[sheet_name]
    print(f"INFO: Using sheet '{sheet_name}' with {len(rows)} non-empty rows")

    # -------------------------------------------------------------------------
    # Component 1: Required columns present AND at least 15 data rows (0.4 pts)
    # This verifies the core data collection task was performed.
    # FAILS on initial_env (no file exists), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        # Find header row (must contain required column names)
        header_row_idx = None
        header = []
        for ridx, row in enumerate(rows):
            row_upper = [str(v).strip() for v in row]
            if 'PI_Name' in row_upper or 'pi_name' in [v.lower() for v in row_upper]:
                header_row_idx = ridx
                header = row_upper
                break

        if header_row_idx is None:
            print("FAIL: Component 1 — No header row with 'PI_Name' column found")
        else:
            # Check required columns (case-insensitive)
            header_lower = {v.lower() for v in header}
            required_lower = {c.lower() for c in REQUIRED_COLUMNS}
            missing_cols = required_lower - header_lower
            if missing_cols:
                print(f"FAIL: Component 1 — Missing required columns: {missing_cols}")
            else:
                # Count data rows after the header
                data_rows = []
                for row in rows[header_row_idx + 1:]:
                    if row and row[0] and str(row[0]).strip():
                        # Stop at summary section markers
                        first_cell = str(row[0]).strip()
                        if first_cell.lower().startswith('summary') or first_cell.lower() == 'institution':
                            break
                        data_rows.append(row)

                num_data_rows = len(data_rows)
                if num_data_rows >= 15:
                    print(f"PASS: Component 1 — All required columns present, {num_data_rows} data rows (>= 15)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — Only {num_data_rows} data rows found (need >= 15)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Grant data covers target institutions (MIT, Stanford, Berkeley)
    # This verifies that the agent actually searched the NSF database for the
    # specified institutions, not just generic data.
    # FAILS on initial_env (no file), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        if header_row_idx is None:
            print("FAIL: Component 2 — Cannot check institutions (no header found)")
        else:
            # Find Institution column index
            inst_col_idx = None
            for cidx, col_name in enumerate(header):
                if col_name.lower() == 'institution':
                    inst_col_idx = cidx
                    break

            if inst_col_idx is None:
                print("FAIL: Component 2 — 'Institution' column not found")
            else:
                # Collect all institution values from data rows
                found_institutions = set()
                for row in rows[header_row_idx + 1:]:
                    if row and row[0] and str(row[0]).strip():
                        first_cell = str(row[0]).strip()
                        if first_cell.lower().startswith('summary') or first_cell.lower() == 'institution':
                            break
                        if inst_col_idx < len(row):
                            inst_val = str(row[inst_col_idx]).strip()
                            if inst_val:
                                found_institutions.add(inst_val)

                institutions_found = TARGET_INSTITUTIONS & found_institutions
                if len(institutions_found) == len(TARGET_INSTITUTIONS):
                    print(f"PASS: Component 2 — All 3 target institutions found: {institutions_found}")
                    total_score += 0.3
                elif len(institutions_found) >= 2:
                    print(f"PARTIAL: Component 2 — {len(institutions_found)}/3 institutions found: {institutions_found}")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — Only {len(institutions_found)}/3 target institutions found: {found_institutions}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Summary section with average award by institution (0.3 pts)
    # This verifies the computation step: averages are calculated and present.
    # FAILS on initial_env (no file), PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        # Look for a summary section in all rows
        summary_found = False
        avg_institutions_found = set()

        all_text = []
        for row in rows:
            for cell in row:
                all_text.append(str(cell).strip().lower())

        # Look for "summary" label and institution averages
        summary_row_idx = None
        for ridx, row in enumerate(rows):
            row_text = ' '.join(str(v).lower() for v in row)
            if 'summary' in row_text or 'average' in row_text:
                summary_row_idx = ridx
                break

        if summary_row_idx is None:
            print("FAIL: Component 3 — No summary/average section found in the spreadsheet")
        else:
            # Check for institution averages after summary header
            for row in rows[summary_row_idx:]:
                row_text = ' '.join(str(v).strip() for v in row)
                for inst in TARGET_INSTITUTIONS:
                    if inst in row_text:
                        # Check that a numeric value is present in this row (the average amount)
                        # Use any() to avoid mutable flag pattern
                        def _has_large_numeric(row_cells):
                            for cell in row_cells:
                                try:
                                    val = float(str(cell).strip().replace(',', ''))
                                    if val > 10000:  # reasonable grant amount threshold
                                        return True
                                except (ValueError, TypeError):
                                    pass
                            return False
                        if _has_large_numeric(row):
                            avg_institutions_found.add(inst)

            if len(avg_institutions_found) == len(TARGET_INSTITUTIONS):
                print(f"PASS: Component 3 — Summary with average amounts found for all 3 institutions: {avg_institutions_found}")
                total_score += 0.3
            elif len(avg_institutions_found) >= 2:
                print(f"PARTIAL: Component 3 — Average amounts found for {len(avg_institutions_found)}/3 institutions: {avg_institutions_found}")
                total_score += 0.15
            elif len(avg_institutions_found) == 1:
                print(f"PARTIAL: Component 3 — Average amounts found for only 1/3 institutions: {avg_institutions_found}")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — No institution average amounts found in summary section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify on the VM file path
if not os.path.exists(TASK_FILE):
    print(f"File not found: {TASK_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TASK_FILE)
