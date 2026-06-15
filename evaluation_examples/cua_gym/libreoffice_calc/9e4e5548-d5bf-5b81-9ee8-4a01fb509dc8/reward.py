"""
Reward Script: Organize research paper PDFs into year-based folders and create catalog
Task ID: osworld_multi_apps_doc_desktop_organize_006
Domain: multi_apps / libreoffice_calc + os
Scoring:
  Component 1: Year folders exist and all 15 PDFs moved to correct year folders (0.4 pts)
  Component 2: papers_catalog.ods exists with correct headers and 15 data rows (0.3 pts)
  Component 3: Catalog data is sorted by Year then Filename, paths match actual locations (0.3 pts)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_desktop_organize_006'

# Ground truth: 15 PDFs mapped to their year folders
EXPECTED_PDF_LOCATIONS = {
    'brown2020language.pdf':    '2020',
    'dosovitskiy2020image.pdf': '2020',
    'raffel2020exploring.pdf':  '2020',
    'jones2021transformer.pdf': '2021',
    'loshchilov2021decoupled.pdf': '2021',
    'radford2021learning.pdf':  '2021',
    'ouyang2022training.pdf':   '2022',
    'smith2022attention.pdf':   '2022',
    'wei2022chain.pdf':         '2022',
    'achiam2023gpt.pdf':        '2023',
    'touvron2023llama.pdf':     '2023',
    'wang2023llm.pdf':          '2023',
    'bai2024longalign.pdf':     '2024',
    'dubey2024llama.pdf':       '2024',
    'yang2024qwen.pdf':         '2024',
}

EXPECTED_YEARS = ['2020', '2021', '2022', '2023', '2024']
CATALOG_PATH = os.path.join(WORKDIR, 'papers_catalog.ods')


def read_ods_rows(path):
    """Read all rows from the first sheet of an ODS file using the odf library."""
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(path)
    tables = doc.spreadsheet.getElementsByType(Table)
    if not tables:
        return []
    sheet = tables[0]
    rows_data = []
    for row in sheet.getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        row_vals = []
        for cell in cells:
            repeated = int(cell.getAttribute('numbercolumnsrepeated') or 1)
            ps = cell.getElementsByType(P)
            val = str(ps[0]) if ps else ''
            for _ in range(repeated):
                row_vals.append(val)
        # Strip trailing empty cells
        while row_vals and row_vals[-1] == '':
            row_vals.pop()
        if row_vals:
            rows_data.append(row_vals)
    return rows_data


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Year folders exist AND all 15 PDFs are in the correct year folder (0.4 pts)
    # This FAILS on initial (no folders, PDFs on desktop) and PASSES on golden (PDFs moved)
    try:
        folders_ok = True
        pdfs_ok = True
        missing_folders = []
        wrong_location_pdfs = []

        # Check year folders exist
        for year in EXPECTED_YEARS:
            folder_path = os.path.join(WORKDIR, year)
            if not os.path.isdir(folder_path):
                folders_ok = False
                missing_folders.append(year)

        # Check each PDF is in the correct year folder
        for pdf_name, expected_year in EXPECTED_PDF_LOCATIONS.items():
            expected_path = os.path.join(WORKDIR, expected_year, pdf_name)
            if not os.path.isfile(expected_path):
                pdfs_ok = False
                wrong_location_pdfs.append(f"{pdf_name} -> {expected_year}/")

        if folders_ok and pdfs_ok:
            print(f"PASS: Component 1 — All 5 year folders exist and all 15 PDFs are in correct year folders (0.4 pts)")
            total_score += 0.4
        else:
            if missing_folders:
                print(f"FAIL: Component 1 — Missing year folders: {missing_folders}")
            if wrong_location_pdfs:
                print(f"FAIL: Component 1 — PDFs not in expected year folder: {wrong_location_pdfs[:5]}{'...' if len(wrong_location_pdfs)>5 else ''}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: papers_catalog.ods exists with correct headers and 15 data rows (0.3 pts)
    # This FAILS on initial (no catalog file) and PASSES on golden
    try:
        if not os.path.isfile(CATALOG_PATH):
            print(f"FAIL: Component 2 — papers_catalog.ods not found at {CATALOG_PATH}")
        else:
            rows = read_ods_rows(CATALOG_PATH)
            if not rows:
                print(f"FAIL: Component 2 — papers_catalog.ods is empty")
            else:
                # Check header row
                header = [str(v).strip() for v in rows[0]]
                expected_headers = ['Filename', 'Year', 'New_Path']
                headers_ok = all(h in header for h in expected_headers)

                # Check 15 data rows (row 0 = header, rows 1-15 = data)
                data_rows = rows[1:]
                row_count_ok = len(data_rows) == 15

                if headers_ok and row_count_ok:
                    print(f"PASS: Component 2 — papers_catalog.ods found with correct headers {header[:3]} and {len(data_rows)} data rows (0.3 pts)")
                    total_score += 0.3
                else:
                    if not headers_ok:
                        print(f"FAIL: Component 2 — Headers incorrect: expected {expected_headers}, found {header[:3]}")
                    if not row_count_ok:
                        print(f"FAIL: Component 2 — Expected 15 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Catalog is sorted by Year then Filename AND paths match actual file locations (0.3 pts)
    # This FAILS on initial (no catalog) and PASSES on golden
    try:
        if not os.path.isfile(CATALOG_PATH):
            print(f"FAIL: Component 3 — papers_catalog.ods not found, cannot check content")
        else:
            rows = read_ods_rows(CATALOG_PATH)
            data_rows = rows[1:] if rows else []

            if len(data_rows) != 15:
                print(f"FAIL: Component 3 — Need 15 data rows to verify sorting/content, found {len(data_rows)}")
            else:
                # Check sorting by Year then Filename
                sort_ok = True
                path_ok = True
                path_errors = []

                # Extract (filename, year, path) tuples
                parsed = []
                for row in data_rows:
                    fname = str(row[0]).strip() if len(row) > 0 else ''
                    year  = str(row[1]).strip() if len(row) > 1 else ''
                    path  = str(row[2]).strip() if len(row) > 2 else ''
                    parsed.append((fname, year, path))

                # Check sort order: by Year ascending, then Filename ascending
                sort_keys = [(p[1], p[0]) for p in parsed]
                expected_sort = sorted(sort_keys)
                if sort_keys != expected_sort:
                    sort_ok = False
                    print(f"FAIL: Component 3 — Catalog not sorted by Year then Filename. First mismatch at index {next(i for i,(a,b) in enumerate(zip(sort_keys,expected_sort)) if a!=b)}")

                # Check paths match expected locations (Year/Filename pattern)
                for fname, year, path in parsed:
                    if fname in EXPECTED_PDF_LOCATIONS:
                        expected_year = EXPECTED_PDF_LOCATIONS[fname]
                        expected_path = f'/home/user/Desktop/{expected_year}/{fname}'
                        if path != expected_path:
                            path_ok = False
                            path_errors.append(f"{fname}: expected path '{expected_path}', got '{path}'")
                    else:
                        path_ok = False
                        path_errors.append(f"Unexpected filename in catalog: {fname}")

                if sort_ok and path_ok:
                    print(f"PASS: Component 3 — Catalog sorted correctly and all 15 paths match expected locations (0.3 pts)")
                    total_score += 0.3
                else:
                    if path_errors:
                        print(f"FAIL: Component 3 — Path errors: {path_errors[:3]}{'...' if len(path_errors)>3 else ''}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
