"""
Reward Script: Compile CV conference history into a sorted ODS spreadsheet
Task ID: osworld_multi_apps_web_conference_008
Domain: libreoffice_calc (ODS format)

Scoring Rubric:
  Component 1: Required columns present (Conference, Year, Location, Papers_Count, Notes) — 0.2 pts
  Component 2: All 3 conferences (CVPR, ICCV, ECCV) represented with substantial data — 0.3 pts
  Component 3: Data sorted by Conference then Year ascending — 0.3 pts
  Component 4: Papers_Count populated for at least some entries — 0.2 pts
  Total: 1.0

Note: File is .ods format; we parse it via zipfile + XML (ODS = ZIP of XML files).
The file is expected at /home/user/Desktop/cv_conferences_history.ods.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

FILE_PATH = '/home/user/Desktop/cv_conferences_history.ods'

# ODS XML namespaces
NS_TABLE = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'


def parse_ods(path):
    """
    Parse an ODS file and return a list of rows (list of lists of strings).
    Each row is a list of cell string values.
    """
    with zipfile.ZipFile(path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    tables = root.findall(f'.//{{{NS_TABLE}}}table')
    if not tables:
        return []

    # Use the first sheet
    table = tables[0]
    rows = table.findall(f'.//{{{NS_TABLE}}}table-row')

    result = []
    for row in rows:
        cells = row.findall(f'.//{{{NS_TABLE}}}table-cell')
        values = []
        for cell in cells:
            text_nodes = cell.findall(f'.//{{{NS_TEXT}}}p')
            val = ' '.join((t.text or '') for t in text_nodes) if text_nodes else ''
            values.append(val.strip())
        # Remove trailing empty cells
        while values and not values[-1]:
            values.pop()
        result.append(values)

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODS
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        rows = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) < 2:
        print(f"CRITICAL: File has fewer than 2 rows (header + data), got {len(rows)}")
        print("REWARD: 0.0")
        return 0.0

    header = [v.strip().lower() for v in rows[0]] if rows else []
    data_rows = [r for r in rows[1:] if any(v.strip() for v in r)]

    print(f"INFO: Parsed {len(rows)} rows total, {len(data_rows)} data rows")
    print(f"INFO: Header: {rows[0] if rows else 'N/A'}")

    # -------------------------------------------------------------------------
    # Component 1: Required columns present (0.2 points)
    # The task specifies columns: Conference, Year, Location, Papers_Count, Notes
    # -------------------------------------------------------------------------
    try:
        required_cols = ['conference', 'year', 'location', 'papers_count']
        missing_cols = [col for col in required_cols if col not in header]
        if not missing_cols:
            print(f"PASS: Component 1 — All required columns present: {rows[0][:5]} (0.2 pts)")
            total_score += 0.2
        else:
            # Allow partial header match with fuzzy check
            header_str = ' '.join(header).lower()
            partial_found = sum(1 for col in required_cols if col.replace('_', '') in header_str.replace('_', '').replace(' ', ''))
            if partial_found >= 3:
                print(f"PASS (partial): Component 1 — {partial_found}/4 required columns found in header (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — Missing required columns: {missing_cols}. Header found: {rows[0]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: All 3 conferences present with substantial data (0.3 points)
    # CVPR, ICCV, ECCV must each have at least 5 rows
    # -------------------------------------------------------------------------
    try:
        # Determine column index for Conference (column 0 by default)
        conf_col = 0
        if 'conference' in header:
            conf_col = header.index('conference')

        conferences_found = {}
        for row in data_rows:
            if len(row) > conf_col:
                conf = row[conf_col].strip().upper()
                if conf in ('CVPR', 'ICCV', 'ECCV'):
                    conferences_found[conf] = conferences_found.get(conf, 0) + 1

        required_conferences = {'CVPR', 'ICCV', 'ECCV'}
        present_conferences = set(conferences_found.keys())
        all_present = required_conferences <= present_conferences
        has_substantial = all(conferences_found.get(c, 0) >= 5 for c in required_conferences)

        detail = (f"CVPR={conferences_found.get('CVPR', 0)}, "
                  f"ICCV={conferences_found.get('ICCV', 0)}, "
                  f"ECCV={conferences_found.get('ECCV', 0)}")
        if all_present and has_substantial:
            print(f"PASS: Component 2 — All 3 conferences present with substantial data: {detail} (0.3 pts)")
            total_score += 0.3
        elif all_present:
            print(f"PASS (partial): Component 2 — All 3 conferences present but limited data: "
                  f"{conferences_found} (0.15 pts)")
            total_score += 0.15
        elif len(present_conferences) >= 2:
            print(f"PASS (partial): Component 2 — Only {present_conferences} found, "
                  f"missing {required_conferences - present_conferences} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — Missing conferences. Found: {conferences_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Data sorted by Conference then Year ascending (0.3 points)
    # -------------------------------------------------------------------------
    try:
        conf_col = 0
        year_col = 1
        if 'conference' in header:
            conf_col = header.index('conference')
        if 'year' in header:
            year_col = header.index('year')

        valid_rows = []
        for row in data_rows:
            if len(row) > max(conf_col, year_col):
                conf = row[conf_col].strip().upper()
                year_str = row[year_col].strip()
                if conf in ('CVPR', 'ICCV', 'ECCV') and year_str.isdigit():
                    valid_rows.append((conf, int(year_str)))

        sort_violations = sum(
            1 for i in range(1, len(valid_rows)) if valid_rows[i] < valid_rows[i - 1]
        )
        # Log first few violations for debugging
        for i in range(1, len(valid_rows)):
            if valid_rows[i] < valid_rows[i - 1] and sort_violations <= 3:
                print(f"  Sort violation at position {i}: {valid_rows[i-1]} -> {valid_rows[i]}")

        if sort_violations == 0 and len(valid_rows) > 10:
            print(f"PASS: Component 3 — Data correctly sorted by Conference then Year "
                  f"({len(valid_rows)} valid rows checked) (0.3 pts)")
            total_score += 0.3
        elif sort_violations <= 2 and len(valid_rows) > 10:
            print(f"PASS (partial): Component 3 — Mostly sorted, {sort_violations} violations "
                  f"among {len(valid_rows)} rows (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Data not properly sorted. Violations: {sort_violations}, "
                  f"valid rows checked: {len(valid_rows)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Papers_Count populated for some entries (0.2 points)
    # The task says "collect paper counts if available" — Wikipedia has this for recent years
    # -------------------------------------------------------------------------
    try:
        papers_col = -1
        if 'papers_count' in header:
            papers_col = header.index('papers_count')
        elif 'papers count' in header:
            papers_col = header.index('papers count')
        else:
            # Try to find a numeric-looking column that's not Year
            for idx, h in enumerate(header):
                if 'paper' in h.lower() or 'count' in h.lower():
                    papers_col = idx
                    break

        if papers_col >= 0:
            rows_with_papers = 0
            for row in data_rows:
                if len(row) > papers_col:
                    val = row[papers_col].strip()
                    if val and val.isdigit() and int(val) > 0:
                        rows_with_papers += 1

            if rows_with_papers >= 10:
                print(f"PASS: Component 4 — Papers_Count populated for {rows_with_papers} entries (0.2 pts)")
                total_score += 0.2
            elif rows_with_papers >= 3:
                print(f"PASS (partial): Component 4 — Papers_Count populated for {rows_with_papers} entries (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — Papers_Count found in column {papers_col} "
                      f"but only {rows_with_papers} non-empty numeric values")
        else:
            print(f"FAIL: Component 4 — Could not find Papers_Count column. Header: {rows[0]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
