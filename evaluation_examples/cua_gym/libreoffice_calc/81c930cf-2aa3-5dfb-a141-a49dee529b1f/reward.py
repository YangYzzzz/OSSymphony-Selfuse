"""
Reward Script: ArXiv cs.CL Paper Deduplication Tracker
Task ID: osworld_multi_apps_arxiv_llms_calc_011
Domain: libreoffice_calc
Scoring:
  Component 1 (0.40): Data rows populated — at least 30 papers with all required fields
                      spanning all 3 dates (2024-01-15, 2024-01-16, 2024-01-17)
  Component 2 (0.35): Status column correctly populated with 'cross-posted'/'original'
                      and cross-posted papers present across all 3 dates
  Component 3 (0.25): Summary section has COUNTIF formulas in H2:H4 for per-day counts
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_011'

# ODF/ODS XML namespaces
NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':  'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'of':    'urn:oasis:names:tc:opendocument:xmlns:of:1.2',
}


def read_ods_sheet(ods_path, sheet_index=0):
    """
    Parse an .ods file using zipfile + xml.etree.
    Returns a 2D list of (row, col) -> cell_value (strings).
    Also returns raw_cells: list of rows, each row is a list of (value_str, formula_str).
    """
    with zipfile.ZipFile(ods_path, 'r') as z:
        content_xml = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content_xml)

    # Navigate: office:document-content > office:body > office:spreadsheet > table:table
    body = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body')
    spreadsheet = body.find('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}spreadsheet')
    tables = spreadsheet.findall('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table')

    if sheet_index >= len(tables):
        raise ValueError(f"Sheet index {sheet_index} not found (only {len(tables)} sheets)")

    table = tables[sheet_index]
    sheet_name = table.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name', '')

    rows_data = []  # list of rows; each row is list of (text_value, formula_str)

    TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
    TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

    for row_el in table.findall(f'{{{TABLE_NS}}}table-row'):
        # Handle table:number-rows-repeated
        rows_repeated = int(row_el.get(f'{{{TABLE_NS}}}number-rows-repeated', '1'))

        row_cells = []
        for cell_el in row_el.findall(f'{{{TABLE_NS}}}table-cell'):
            cols_repeated = int(cell_el.get(f'{{{TABLE_NS}}}number-columns-repeated', '1'))

            # Extract text value
            text_parts = []
            for p in cell_el.findall(f'.//{{{TEXT_NS}}}p'):
                text_parts.append(''.join(p.itertext()))
            cell_text = ''.join(text_parts) if text_parts else None

            # Extract formula
            formula = cell_el.get(f'{{{TABLE_NS}}}formula', None)

            for _ in range(cols_repeated):
                row_cells.append((cell_text, formula))

        # Only append non-repeated empty rows if they're not at the very end
        for _ in range(rows_repeated):
            rows_data.append(row_cells)

    return sheet_name, rows_data


def get_cell(rows_data, row_idx, col_idx):
    """Get (text_value, formula) for 1-indexed row/col. Returns (None, None) if out of range."""
    r = row_idx - 1
    c = col_idx - 1
    if r < 0 or r >= len(rows_data):
        return (None, None)
    row = rows_data[r]
    if c < 0 or c >= len(row):
        return (None, None)
    return row[c]


def verify_task(ods_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        sheet_name, rows_data = read_ods_sheet(ods_path, sheet_index=0)
        print(f"INFO: Sheet '{sheet_name}' loaded, {len(rows_data)} rows")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {ods_path}: {e}")
        import traceback
        traceback.print_exc()
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Check headers in row 1
    expected_headers = {1: 'arXiv ID', 2: 'Title', 3: 'Authors', 4: 'Date', 5: 'Status'}
    for col, expected in expected_headers.items():
        val, _ = get_cell(rows_data, 1, col)
        if val is None or str(val).strip().lower() != expected.lower():
            print(f"CRITICAL: Header col {col} = '{val}', expected '{expected}'")
            print("REWARD: 0.0")
            return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Data rows populated with at least 30 papers (0.40 points)
    # Initial env has 0 data rows; golden env has 39 papers spanning 3 dates
    # -----------------------------------------------------------------------
    try:
        papers = []
        EXPECTED_DATES = {'2024-01-15', '2024-01-16', '2024-01-17'}

        for row_idx in range(2, len(rows_data) + 1):
            arxiv_id_val, _ = get_cell(rows_data, row_idx, 1)
            title_val, _    = get_cell(rows_data, row_idx, 2)
            authors_val, _  = get_cell(rows_data, row_idx, 3)
            date_val, _     = get_cell(rows_data, row_idx, 4)
            status_val, _   = get_cell(rows_data, row_idx, 5)

            if arxiv_id_val is None:
                continue

            papers.append({
                'id': str(arxiv_id_val).strip(),
                'title': title_val,
                'authors': authors_val,
                'date': str(date_val).strip() if date_val else None,
                'status': str(status_val).strip().lower() if status_val else None,
            })

        total_papers = len(papers)
        papers_with_all_fields = [
            p for p in papers
            if p['id'] and p['title'] and p['authors'] and p['date'] and p['status']
        ]
        dates_present = set(p['date'] for p in papers)
        all_dates_covered = EXPECTED_DATES.issubset(dates_present)

        if total_papers >= 30 and len(papers_with_all_fields) >= 30 and all_dates_covered:
            print(f"PASS: Component 1 — {total_papers} papers found, all 3 dates covered, "
                  f"{len(papers_with_all_fields)} with complete fields (0.40 pts)")
            total_score += 0.40
        elif total_papers >= 15:
            print(f"PARTIAL: Component 1 — {total_papers} papers found (expected >=30), "
                  f"dates covered: {dates_present}. Awarding 0.20 pts")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — only {total_papers} data rows found (expected >=30), "
                  f"all_dates_covered={all_dates_covered}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        papers = []

    # -----------------------------------------------------------------------
    # Component 2: Status column correctly populated (0.35 points)
    # Initial env has no status values; golden env has 'cross-posted'/'original' on every row,
    # with cross-posted papers present on all 3 dates
    # -----------------------------------------------------------------------
    try:
        VALID_STATUSES = {'cross-posted', 'original'}

        if len(papers) > 0:
            valid_status_papers = [p for p in papers if p['status'] in VALID_STATUSES]
            cross_posted_papers = [p for p in papers if p['status'] == 'cross-posted']
            cross_dates = set(p['date'] for p in cross_posted_papers)
            cross_posted_all_dates = EXPECTED_DATES.issubset(cross_dates)
            status_ratio = len(valid_status_papers) / len(papers)

            if status_ratio >= 0.95 and len(cross_posted_papers) >= 5 and cross_posted_all_dates:
                print(f"PASS: Component 2 — {len(valid_status_papers)}/{len(papers)} valid status, "
                      f"{len(cross_posted_papers)} cross-posted across all 3 dates (0.35 pts)")
                total_score += 0.35
            elif status_ratio >= 0.80 and len(cross_posted_papers) >= 1:
                print(f"PARTIAL: Component 2 — {len(valid_status_papers)}/{len(papers)} valid status, "
                      f"{len(cross_posted_papers)} cross-posted. Awarding 0.15 pts")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — {len(valid_status_papers)}/{len(papers)} valid status, "
                      f"cross-posted: {len(cross_posted_papers)}, cross_dates: {cross_dates}")
        else:
            print("FAIL: Component 2 — no papers found, cannot verify status")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Summary section has COUNTIF formulas in H2:H4 (0.25 points)
    # Initial env has dates in G2:G4 but NO formulas in H2:H4
    # Golden env has COUNTIF formulas in H2:H4 referencing the Date column
    # -----------------------------------------------------------------------
    try:
        h2_val, h2_formula = get_cell(rows_data, 2, 8)
        h3_val, h3_formula = get_cell(rows_data, 3, 8)
        h4_val, h4_formula = get_cell(rows_data, 4, 8)

        def is_countif_formula(formula_str, value_str):
            """Check if cell contains a COUNTIF formula."""
            # In ODS, formulas are stored in table:formula attribute
            # They look like: "of:=COUNTIF($D$2:$D$40,G2)" or "=COUNTIF(...)"
            if formula_str:
                f = str(formula_str).upper()
                if 'COUNTIF' in f:
                    return True
            # Also check value field in case formula is stored as text
            if value_str:
                v = str(value_str).strip().upper()
                if v.startswith('=COUNTIF') or 'COUNTIF' in v:
                    return True
            return False

        h2_ok = is_countif_formula(h2_formula, h2_val)
        h3_ok = is_countif_formula(h3_formula, h3_val)
        h4_ok = is_countif_formula(h4_formula, h4_val)
        countif_count = sum([h2_ok, h3_ok, h4_ok])

        if countif_count == 3:
            print(f"PASS: Component 3 — COUNTIF formulas in H2, H3, H4 (0.25 pts)")
            total_score += 0.25
        elif countif_count >= 1:
            print(f"PARTIAL: Component 3 — only {countif_count}/3 COUNTIF formulas found. "
                  f"H2_formula={repr(h2_formula)}, H3_formula={repr(h3_formula)}, "
                  f"H4_formula={repr(h4_formula)}. Awarding 0.10 pts")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — no COUNTIF formulas in H2:H4. "
                  f"H2_formula={repr(h2_formula)}, H3_formula={repr(h3_formula)}, "
                  f"H4_formula={repr(h4_formula)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
ods_path = f'{WORKDIR}/dedup_tracker.ods'
if not os.path.exists(ods_path):
    print(f"File not found: {ods_path}")
    print("REWARD: 0.0")
else:
    verify_task(ods_path)
