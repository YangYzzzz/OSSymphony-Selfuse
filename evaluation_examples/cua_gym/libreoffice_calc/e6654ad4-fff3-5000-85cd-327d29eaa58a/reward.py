"""
Reward Script: Cross-category arXiv paper collection with duplicate detection
Task ID: osworld_multi_apps_arxiv_llms_calc_009
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.40): At least 10 data rows added with arXiv IDs from both cs.CL and cs.LG categories
  Component 2 (0.35): Duplicate column (E) contains IF+COUNTIF formula or correct Yes/No values detecting duplicates
  Component 3 (0.25): Summary cell I1 contains COUNTIF formula or numeric count of duplicate papers
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_009'

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'of':     'urn:oasis:names:tc:opendocument:xmlns:of:1.2',
}


def get_cell_text(cell_elem):
    """Extract text content from an ODS table:table-cell element."""
    texts = []
    for p in cell_elem.findall('.//text:p', NS):
        for node in p.iter():
            if node.text:
                texts.append(node.text)
            if node.tail:
                texts.append(node.tail)
    return ''.join(texts).strip()


def get_cell_formula(cell_elem):
    """Return the formula attribute if present, else None."""
    return cell_elem.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}formula') or \
           cell_elem.get('{urn:oasis:names:tc:opendocument:xmlns:of:1.2}formula')


def parse_ods(file_path):
    """Parse ODS file and return list of sheets as list of rows (each row = list of (text, formula))."""
    with zipfile.ZipFile(file_path) as z:
        content_xml = z.read('content.xml')
    root = ET.fromstring(content_xml)
    sheets = {}
    for table in root.findall('.//table:table', NS):
        sheet_name = table.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name')
        rows = []
        for row in table.findall('table:table-row', NS):
            cells = row.findall('table:table-cell', NS)
            row_data = []
            for cell in cells:
                text = get_cell_text(cell)
                formula = get_cell_formula(cell)
                repeat = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated')
                row_data.append((text, formula))
                # For repeated empty cells, just add once (they are trailing empties)
                if repeat and int(repeat) > 1:
                    break
            rows.append(row_data)
        sheets[sheet_name] = rows
    return sheets


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse the ODS file
    try:
        sheets = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Papers' sheet must exist
    if 'Papers' not in sheets:
        print("CRITICAL: 'Papers' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    rows = sheets['Papers']
    print(f"INFO: Found {len(rows)} rows in 'Papers' sheet (including header)")

    # -----------------------------------------------------------------------
    # Component 1 (0.40): At least 10 data rows with arXiv IDs from BOTH
    #   cs.CL and cs.LG source categories
    # -----------------------------------------------------------------------
    try:
        # Row 0 is the header. Data rows start at index 1.
        data_rows = rows[1:] if len(rows) > 1 else []

        # Count rows that have a non-empty arXiv ID (column A = index 0)
        arxiv_ids = []
        categories = []
        for row in data_rows:
            arxiv_id = row[0][0] if len(row) > 0 else ''
            category = row[3][0] if len(row) > 3 else ''
            if arxiv_id:
                arxiv_ids.append(arxiv_id)
                categories.append(category)

        has_cscl = any(c.strip() == 'cs.CL' for c in categories)
        has_cslg = any(c.strip() == 'cs.LG' for c in categories)
        row_count = len(arxiv_ids)

        print(f"  Data rows with arXiv ID: {row_count}")
        print(f"  Has cs.CL: {has_cscl}, Has cs.LG: {has_cslg}")
        print(f"  Categories: {categories}")

        if row_count >= 10 and has_cscl and has_cslg:
            print(f"PASS: Component 1 — {row_count} rows from both cs.CL and cs.LG (0.40 pts)")
            total_score += 0.40
        elif row_count >= 5 and (has_cscl or has_cslg):
            print(f"PARTIAL: Component 1 — {row_count} rows but missing one category (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Only {row_count} data rows, expected >=10 from both categories")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2 (0.35): Duplicate column (E = index 4) correctly identifies
    #   duplicate arXiv IDs using IF+COUNTIF formula or correct Yes/No values
    # -----------------------------------------------------------------------
    try:
        # Find rows where duplicate arXiv IDs appear more than once
        from collections import Counter
        id_counts = Counter(arxiv_ids)
        duplicates_expected = {arxiv_id for arxiv_id, cnt in id_counts.items() if cnt > 1}
        print(f"  Expected duplicate IDs: {duplicates_expected}")

        # Check each data row's Duplicate column (index 4)
        formula_found = False
        correct_values = True
        has_yes_for_duplicate = False
        has_no_for_non_duplicate = False

        for i, row in enumerate(data_rows):
            if not (len(row) > 0 and row[0][0]):
                continue  # skip empty rows
            arxiv_id = row[0][0]
            dup_cell_text = row[4][0] if len(row) > 4 else ''
            dup_cell_formula = row[4][1] if len(row) > 4 else None

            if dup_cell_formula and ('COUNTIF' in dup_cell_formula.upper() or 'IF' in dup_cell_formula.upper()):
                formula_found = True

            # Check value correctness
            expected_val = 'Yes' if arxiv_id in duplicates_expected else 'No'
            if dup_cell_text.strip() not in ('Yes', 'No', ''):
                correct_values = False
            elif dup_cell_text.strip() == 'Yes' and arxiv_id in duplicates_expected:
                has_yes_for_duplicate = True
            elif dup_cell_text.strip() == 'No' and arxiv_id not in duplicates_expected:
                has_no_for_non_duplicate = True
            elif dup_cell_text.strip() != '' and dup_cell_text.strip() != expected_val:
                correct_values = False

            print(f"  Row {i+2}: ID={arxiv_id}, Dup={repr(dup_cell_text)}, "
                  f"Formula={repr(dup_cell_formula)}, Expected={expected_val}")

        print(f"  formula_found={formula_found}, correct_values={correct_values}, "
              f"has_yes={has_yes_for_duplicate}, has_no={has_no_for_non_duplicate}")

        # Require that there are actual data rows with content to score this component
        has_any_data = len(arxiv_ids) >= 10

        if has_any_data and formula_found and (has_yes_for_duplicate or correct_values):
            print(f"PASS: Component 2 — IF+COUNTIF formula in Duplicate column with correct values (0.35 pts)")
            total_score += 0.35
        elif has_any_data and (has_yes_for_duplicate and has_no_for_non_duplicate):
            print(f"PASS: Component 2 — Duplicate column has correct Yes/No values (0.35 pts)")
            total_score += 0.35
        elif has_any_data and (has_yes_for_duplicate or has_no_for_non_duplicate):
            print(f"PARTIAL: Component 2 — Some correct Yes/No values in Duplicate column (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — No data rows or Duplicate column empty/incorrect")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3 (0.25): Summary cell I1 contains COUNTIF formula or a
    #   numeric value representing count of duplicate papers
    # -----------------------------------------------------------------------
    try:
        # Row 0 is header. Column I = index 8 (0-indexed).
        header_row = rows[0] if rows else []
        # I1 is the 9th column (index 8)
        summary_text = header_row[8][0] if len(header_row) > 8 else ''
        summary_formula = header_row[8][1] if len(header_row) > 8 else None

        print(f"  I1 text: {repr(summary_text)}, I1 formula: {repr(summary_formula)}")

        has_countif_formula = (
            summary_formula is not None and
            'COUNTIF' in summary_formula.upper()
        )
        has_numeric_count = False
        try:
            val = float(summary_text)
            has_numeric_count = val >= 0
        except (ValueError, TypeError):
            pass

        # Verify H1 label (index 7) says "Duplicate Count"
        h1_text = header_row[7][0] if len(header_row) > 7 else ''
        print(f"  H1 text: {repr(h1_text)}")

        if has_countif_formula and 'E' in (summary_formula or '').upper():
            print(f"PASS: Component 3 — I1 contains COUNTIF formula on Duplicate column: "
                  f"{summary_formula} = {summary_text} (0.25 pts)")
            total_score += 0.25
        elif has_countif_formula:
            print(f"PASS: Component 3 — I1 contains COUNTIF formula: {summary_formula} (0.25 pts)")
            total_score += 0.25
        elif has_numeric_count and summary_text != '':
            print(f"PASS: Component 3 — I1 has numeric duplicate count: {summary_text} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — I1 empty or no valid summary. text={repr(summary_text)}, "
                  f"formula={repr(summary_formula)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Final score
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/cross_category.ods'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
