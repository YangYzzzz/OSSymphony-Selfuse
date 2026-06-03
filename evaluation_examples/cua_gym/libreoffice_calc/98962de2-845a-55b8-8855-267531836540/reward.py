"""
Reward Script: Gender Diversity Analysis at ML Conferences
Task ID: osworld_multi_apps_web_conference_010
Domain: libreoffice_calc (ODS format)
Scoring:
  - Precondition gate: File conference_diversity.ods exists on Desktop
  - Component 1: Sheet 1 (AC_List) has correct columns: Name, Conference, Inferred_Gender (0.2 pts)
  - Component 2: Sheet 1 has data rows for BOTH NeurIPS 2023 and ICML 2023 (0.3 pts)
  - Component 3: Inferred_Gender column has valid values (M/F/Unknown) (0.2 pts)
  - Component 4: Sheet 2 (Summary) has correct columns and data for both conferences (0.3 pts)
Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_010'
FILE_PATH = '/home/user/Desktop/conference_diversity.ods'


def ensure_odfpy():
    """Ensure odfpy is available, installing quietly if needed."""
    try:
        import odf  # noqa: F401
        return True
    except ImportError:
        import pip
        try:
            pip.main(['install', 'odfpy', '-q'])
            return True
        except Exception:
            pass
        # fallback: try os.system
        ret = os.system(f"{sys.executable} -m pip install odfpy -q 2>/dev/null")
        return ret == 0


def get_cell_value(cell):
    """Extract text value from an ODF table cell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        return ''.join([str(p) for p in ps]) if ps else ''
    except Exception:
        return ''


def get_sheet_data(sheet):
    """Extract all rows from an ODF sheet as list of lists of strings."""
    from odf.table import TableRow, TableCell
    rows = sheet.getElementsByType(TableRow)
    data = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        row_vals = [get_cell_value(c).strip() for c in cells]
        data.append(row_vals)
    return data


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Ensure odfpy library is available
    if not ensure_odfpy():
        print("CRITICAL: odfpy library not available and could not be installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        from odf.opendocument import load
        from odf.table import Table
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get sheets
    try:
        sheets = doc.spreadsheet.getElementsByType(Table)
        sheet_names = [s.getAttribute("name") for s in sheets]
        print(f"INFO: Found {len(sheets)} sheet(s): {sheet_names}")
    except Exception as e:
        print(f"CRITICAL: Cannot get sheets: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: need at least 2 sheets
    if len(sheets) < 2:
        print(f"FAIL: Expected at least 2 sheets, found {len(sheets)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Sheet 1 (AC_List) has correct headers (0.2 points)
    # Headers must include Name, Conference, Inferred_Gender columns
    try:
        sheet1_data = get_sheet_data(sheets[0])
        comp1_passed = False
        if sheet1_data:
            header_row = [h.strip() for h in sheet1_data[0]]
            header_lower = [h.lower() for h in header_row]
            has_name = any('name' in h for h in header_lower)
            has_conference = any('conference' in h for h in header_lower)
            has_gender = any('gender' in h for h in header_lower)
            comp1_passed = has_name and has_conference and has_gender

        if comp1_passed:
            print(f"PASS: Component 1 — AC_List sheet has required columns (Name, Conference, Inferred_Gender): {header_row[:4]} (0.2 pts)")
            total_score += 0.2
        else:
            header_show = header_row[:6] if sheet1_data else "none"
            print(f"FAIL: Component 1 — AC_List sheet missing required columns. Found: {header_show}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Sheet 1 has data rows for BOTH NeurIPS 2023 and ICML 2023 (0.3 points)
    # Must have entries for both conferences with non-trivial data (at least 5 rows each)
    try:
        sheet1_data = get_sheet_data(sheets[0])
        neurips_rows = []
        icml_rows = []
        for row in sheet1_data[1:]:  # skip header
            if len(row) >= 2 and row[0]:  # non-empty name
                conf = row[1].strip()
                if 'neurips' in conf.lower() or 'nips' in conf.lower():
                    neurips_rows.append(row)
                elif 'icml' in conf.lower():
                    icml_rows.append(row)

        both_have_many = len(neurips_rows) >= 5 and len(icml_rows) >= 5
        both_have_some = len(neurips_rows) >= 1 and len(icml_rows) >= 1
        one_has_many = len(neurips_rows) >= 5 or len(icml_rows) >= 5

        if both_have_many:
            print(f"PASS: Component 2 — Data for both conferences: NeurIPS ({len(neurips_rows)} rows), ICML ({len(icml_rows)} rows) (0.3 pts)")
            total_score += 0.3
        elif both_have_some:
            print(f"PARTIAL: Component 2 — Some data for both conferences but sparse: NeurIPS ({len(neurips_rows)} rows), ICML ({len(icml_rows)} rows) (0.15 pts)")
            total_score += 0.15
        elif one_has_many:
            print(f"PARTIAL: Component 2 — Data for only one conference: NeurIPS ({len(neurips_rows)} rows), ICML ({len(icml_rows)} rows) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — Insufficient data: NeurIPS ({len(neurips_rows)} rows), ICML ({len(icml_rows)} rows)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Inferred_Gender column has valid values M/F/Unknown (0.2 points)
    # At least 90% of data rows should have M, F, or Unknown
    try:
        sheet1_data = get_sheet_data(sheets[0])
        comp3_passed = False
        comp3_partial = False
        valid_count = 0
        total_data_rows = 0
        ratio = 0.0

        if sheet1_data and len(sheet1_data) > 1:
            header_lower = [h.strip().lower() for h in sheet1_data[0]]
            gender_col = -1
            for i, h in enumerate(header_lower):
                if 'gender' in h:
                    gender_col = i
                    break

            if gender_col >= 0:
                valid_gender_values = {'m', 'f', 'unknown', 'male', 'female'}
                for row in sheet1_data[1:]:
                    if len(row) > 0 and row[0]:  # non-empty name
                        total_data_rows += 1
                        if len(row) > gender_col:
                            g = row[gender_col].strip().lower()
                            if g in valid_gender_values:
                                valid_count += 1

                if total_data_rows > 0:
                    ratio = valid_count / total_data_rows
                    comp3_passed = ratio >= 0.9
                    comp3_partial = ratio >= 0.5

        if comp3_passed:
            print(f"PASS: Component 3 — Gender column has valid values in {valid_count}/{total_data_rows} rows ({ratio:.1%}) (0.2 pts)")
            total_score += 0.2
        elif comp3_partial:
            print(f"PARTIAL: Component 3 — Gender column partially valid: {valid_count}/{total_data_rows} rows ({ratio:.1%}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — Gender column has too many invalid values or column not found: {valid_count}/{total_data_rows} rows")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sheet 2 (Summary) has correct columns and data for both conferences (0.3 points)
    # Required columns: Conference, Total_ACs, Male_Count, Female_Count, Unknown_Count, Female_Pct
    # Must have data rows for both NeurIPS 2023 and ICML 2023
    try:
        sheet2_data = get_sheet_data(sheets[1])
        comp4_full = False
        comp4_partial_headers = False
        comp4_partial_data = False
        neurips_summary = None
        icml_summary = None
        header_row2 = []

        if sheet2_data:
            header_row2 = [h.strip() for h in sheet2_data[0]]
            header_lower2 = [h.lower() for h in header_row2]

            has_conference2 = any('conference' in h for h in header_lower2)
            has_total = any('total' in h for h in header_lower2)
            has_male = any('male' in h for h in header_lower2)
            has_female = any('female' in h for h in header_lower2)
            headers_ok = has_conference2 and has_total and has_male and has_female

            for row in sheet2_data[1:]:
                if len(row) >= 2 and row[0]:
                    conf = row[0].strip()
                    if 'neurips' in conf.lower() or 'nips' in conf.lower():
                        neurips_summary = row
                    elif 'icml' in conf.lower():
                        icml_summary = row

            data_ok = neurips_summary is not None and icml_summary is not None
            comp4_full = headers_ok and data_ok
            comp4_partial_headers = headers_ok and not data_ok
            comp4_partial_data = not headers_ok and data_ok

        if comp4_full:
            total_score += 0.3
            print(f"PASS: Component 4 — Summary sheet has correct columns and data for both conferences (0.3 pts)")
            print(f"  NeurIPS summary: {neurips_summary[:6]}")
            print(f"  ICML summary: {icml_summary[:6]}")
        elif comp4_partial_headers:
            print(f"PARTIAL: Component 4 — Summary sheet has correct columns but missing conference data: NeurIPS={'found' if neurips_summary else 'missing'}, ICML={'found' if icml_summary else 'missing'} (0.15 pts)")
            total_score += 0.15
        elif comp4_partial_data:
            print(f"PARTIAL: Component 4 — Summary sheet has data but incomplete columns. Found: {header_row2[:6]} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Summary sheet incomplete. Headers found: {header_row2[:6]}, NeurIPS={'found' if neurips_summary else 'missing'}, ICML={'found' if icml_summary else 'missing'}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
