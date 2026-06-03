"""
Reward Script: Faculty hiring trend analysis - new_faculty_analysis.ods
Task ID: osworld_multi_apps_web_faculty_013
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: File exists as new_faculty_analysis.ods (precondition gate)
  Component 2: Sheet structure - 3 required sheets with correct names (0.25 pts)
  Component 3: Faculty_Data sheet has required columns and >= 20 data rows (0.35 pts)
  Component 4: PhD_Feeder_Analysis sheet has required columns and data (0.20 pts)
  Component 5: Research_Area_Frequency sheet has required columns and data (0.20 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_013'
FILE_PATH = f'{WORKDIR}/new_faculty_analysis.ods'

# XML namespaces used in ODS files
NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


def parse_ods(file_path):
    """
    Parse ODS file using zipfile + XML parsing (no external ODS library needed).
    Returns a dict: {sheet_name: [[row values], ...]}
    """
    sheets = {}
    with zipfile.ZipFile(file_path) as z:
        with z.open("content.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()
            body = root.find(".//office:spreadsheet", NS)
            if body is None:
                return sheets
            for tbl in body.findall(".//table:table", NS):
                tname = tbl.get("{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name")
                rows_data = []
                rows = tbl.findall(".//table:table-row", NS)
                for row in rows:
                    cells = row.findall(".//table:table-cell", NS)
                    row_vals = []
                    has_data = False
                    for cell in cells:
                        p = cell.find(".//text:p", NS)
                        if p is not None and p.text:
                            row_vals.append(p.text.strip())
                            has_data = True
                        else:
                            row_vals.append(None)
                    if has_data:
                        rows_data.append(row_vals)
                sheets[tname] = rows_data
    return sheets


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODS file
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    if not file_path.endswith('.ods'):
        print(f"CRITICAL: File is not .ods format: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sheets = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"ODS file loaded successfully. Sheets found: {list(sheets.keys())}")

    # Component 1: Sheet structure - 3 required sheets with correct names (0.25 pts)
    # Checks that all 3 required sheets exist by name
    try:
        required_sheets = ["Faculty_Data", "PhD_Feeder_Analysis", "Research_Area_Frequency"]
        sheets_present = [s for s in required_sheets if s in sheets]
        if len(sheets_present) == 3:
            print(f"PASS: Component 1 — All 3 required sheets present: {required_sheets} (0.25 pts)")
            total_score += 0.25
        else:
            missing = [s for s in required_sheets if s not in sheets]
            print(f"FAIL: Component 1 — Missing sheets: {missing}. Found sheets: {list(sheets.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Faculty_Data sheet has required columns and >= 20 data rows (0.35 pts)
    # This verifies the main data collection task was completed
    try:
        if "Faculty_Data" not in sheets:
            print("FAIL: Component 2 — Faculty_Data sheet not found")
        else:
            faculty_rows = sheets["Faculty_Data"]
            if not faculty_rows:
                print("FAIL: Component 2 — Faculty_Data sheet is empty")
            else:
                # Check header row
                header_row = faculty_rows[0]
                required_cols = ["Name", "Hired_By", "Joined_Year", "PhD_Institution", "Research_Area"]
                # Normalize: check case-insensitively
                header_lower = [str(v).strip().lower() if v else "" for v in header_row]
                required_lower = [c.lower() for c in required_cols]
                cols_present = [c for c in required_lower if c in header_lower]

                # Count data rows (rows with non-empty Name)
                data_rows = []
                for row in faculty_rows[1:]:  # skip header
                    if row and row[0] and str(row[0]).strip():
                        data_rows.append(row)

                # Verify institutions (Hired_By) contain at least 3 of 4 expected institutions
                hired_by_idx = header_lower.index("hired_by") if "hired_by" in header_lower else -1
                institutions_present = set()
                if hired_by_idx >= 0:
                    for row in data_rows:
                        if len(row) > hired_by_idx and row[hired_by_idx]:
                            institutions_present.add(str(row[hired_by_idx]).strip())

                expected_institutions = {"MIT", "Stanford", "CMU", "Berkeley"}
                institutions_matched = institutions_present & expected_institutions

                cols_ok = len(cols_present) >= 4  # at least 4 of 5 required columns
                rows_ok = len(data_rows) >= 20  # at least 20 faculty entries
                institutions_ok = len(institutions_matched) >= 3  # at least 3 of 4 institutions

                if cols_ok and rows_ok and institutions_ok:
                    print(f"PASS: Component 2 — Faculty_Data has {len(cols_present)}/5 required columns, "
                          f"{len(data_rows)} data rows, institutions: {institutions_matched} (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — cols_ok={cols_ok} ({len(cols_present)}/5 cols found), "
                          f"rows_ok={rows_ok} ({len(data_rows)} rows, need >=20), "
                          f"institutions_ok={institutions_ok} ({institutions_matched})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PhD_Feeder_Analysis sheet has required structure and data (0.20 pts)
    # This verifies the aggregation/analysis was performed
    try:
        if "PhD_Feeder_Analysis" not in sheets:
            print("FAIL: Component 3 — PhD_Feeder_Analysis sheet not found")
        else:
            feeder_rows = sheets["PhD_Feeder_Analysis"]
            if not feeder_rows:
                print("FAIL: Component 3 — PhD_Feeder_Analysis sheet is empty")
            else:
                # Check header
                header_row = feeder_rows[0]
                header_lower = [str(v).strip().lower() if v else "" for v in header_row]
                required_feeder_cols = ["phd_institution", "count"]
                feeder_cols_ok = all(c in header_lower for c in required_feeder_cols)

                # Count data rows
                data_rows = []
                for row in feeder_rows[1:]:
                    if row and row[0] and str(row[0]).strip():
                        data_rows.append(row)

                # Check Percentage column exists as well
                has_percentage = "percentage" in header_lower

                # Need at least 5 institutions listed
                data_rows_ok = len(data_rows) >= 5

                if feeder_cols_ok and data_rows_ok:
                    print(f"PASS: Component 3 — PhD_Feeder_Analysis has required columns "
                          f"(percentage col: {has_percentage}), {len(data_rows)} institution entries (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 — feeder_cols_ok={feeder_cols_ok} (header: {header_row}), "
                          f"data_rows_ok={data_rows_ok} ({len(data_rows)} rows, need >=5)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Research_Area_Frequency sheet has required structure and data (0.20 pts)
    # This verifies the research area frequency analysis was performed
    try:
        if "Research_Area_Frequency" not in sheets:
            print("FAIL: Component 4 — Research_Area_Frequency sheet not found")
        else:
            freq_rows = sheets["Research_Area_Frequency"]
            if not freq_rows:
                print("FAIL: Component 4 — Research_Area_Frequency sheet is empty")
            else:
                # Check header
                header_row = freq_rows[0]
                header_lower = [str(v).strip().lower() if v else "" for v in header_row]
                required_freq_cols = ["research_area", "count"]
                freq_cols_ok = all(c in header_lower for c in required_freq_cols)

                # Count data rows
                data_rows = []
                for row in freq_rows[1:]:
                    if row and row[0] and str(row[0]).strip():
                        data_rows.append(row)

                # Need at least 5 distinct research areas
                data_rows_ok = len(data_rows) >= 5

                if freq_cols_ok and data_rows_ok:
                    print(f"PASS: Component 4 — Research_Area_Frequency has required columns, "
                          f"{len(data_rows)} research area entries (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — freq_cols_ok={freq_cols_ok} (header: {header_row}), "
                          f"data_rows_ok={data_rows_ok} ({len(data_rows)} rows, need >=5)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
