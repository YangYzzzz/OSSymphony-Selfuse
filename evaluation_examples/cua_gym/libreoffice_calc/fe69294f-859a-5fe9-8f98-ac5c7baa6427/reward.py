"""
Reward Script: ArXiv paper collection and keyword frequency analysis
Task ID: osworld_multi_apps_arxiv_llms_calc_012
Domain: libreoffice_calc
Scoring:
  Component 1: Sheet1 contains 5+ data rows (papers added)          — 0.35 pts
  Component 2: Each paper row has all 5 required columns filled      — 0.25 pts
  Component 3: arXiv IDs look like valid 2024 paper IDs             — 0.10 pts
  Component 4: Keyword Frequency sheet has 10+ entries sorted desc  — 0.30 pts
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_012'
FILE_PATH = f'{WORKDIR}/weekly_arxiv.ods'

# ODS XML namespaces
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def get_cell_text(cell):
    """Extract text content from an ODS table-cell element."""
    parts = []
    for p in cell.findall('.//{%s}p' % TEXT_NS):
        if p.text:
            parts.append(p.text)
        # Also grab tail text from child elements
        for child in p:
            if child.tail:
                parts.append(child.tail)
            if child.text:
                parts.append(child.text)
    return ' '.join(parts).strip() if parts else None


def parse_ods(file_path):
    """
    Parse an ODS file and return dict of {sheet_name: list_of_rows}.
    Each row is a list of cell values (strings or None).
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    spreadsheet = root.find('.//{%s}spreadsheet' % OFFICE_NS)
    tables = spreadsheet.findall('{%s}table' % TABLE_NS)

    sheets = {}
    for table in tables:
        sheet_name = table.get('{%s}name' % TABLE_NS)
        sheet_rows = []
        rows = table.findall('{%s}table-row' % TABLE_NS)
        for row in rows:
            cells = row.findall('{%s}table-cell' % TABLE_NS)
            row_values = []
            for cell in cells:
                # Handle repeated columns
                repeat = cell.get('{%s}number-columns-repeated' % TABLE_NS)
                val = get_cell_text(cell)
                if repeat:
                    row_values.extend([val] * int(repeat))
                else:
                    row_values.append(val)
            sheet_rows.append(row_values)
        sheets[sheet_name] = sheet_rows
    return sheets


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS file
    try:
        sheets = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify expected sheets exist
    if 'Sheet1' not in sheets:
        print("CRITICAL: 'Sheet1' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    if 'Keyword Frequency' not in sheets:
        print("CRITICAL: 'Keyword Frequency' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    sheet1_rows = sheets['Sheet1']
    kf_rows = sheets['Keyword Frequency']

    # --- Component 1: Sheet1 has 5+ data rows (papers added) — 0.35 points ---
    # Task: collect all papers from Feb 1-7, 2024 (at least 5 expected)
    # Header row is row 0, data starts from row 1
    try:
        # Find data rows (non-empty rows after header)
        data_rows = []
        for ri, row in enumerate(sheet1_rows):
            if ri == 0:
                continue  # skip header
            # A data row must have at least arXiv ID (col 0) and Title (col 1)
            arxiv_id = row[0] if len(row) > 0 else None
            title = row[1] if len(row) > 1 else None
            if arxiv_id or title:
                data_rows.append(row)

        paper_count = len(data_rows)
        if paper_count >= 5:
            print(f"PASS: Component 1 — Sheet1 has {paper_count} paper rows (>= 5 required) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Sheet1 has only {paper_count} paper rows; expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Each paper row has all 5 columns filled — 0.25 points ---
    # Required columns: arXiv ID (0), Title (1), Authors (2), Abstract (3), Keywords (4)
    try:
        if not data_rows:
            print("FAIL: Component 2 — No data rows to evaluate")
        else:
            fully_filled = 0
            for row in data_rows:
                cols = [row[i] if i < len(row) else None for i in range(5)]
                if all(c for c in cols):
                    fully_filled += 1

            ratio = fully_filled / len(data_rows)
            if ratio >= 0.8:
                print(f"PASS: Component 2 — {fully_filled}/{len(data_rows)} papers have all 5 columns filled (0.25 pts)")
                total_score += 0.25
            elif ratio >= 0.5:
                partial = 0.15
                print(f"PARTIAL: Component 2 — {fully_filled}/{len(data_rows)} papers fully filled; awarding partial credit (0.15 pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {fully_filled}/{len(data_rows)} papers have all 5 columns; expected >= 80%")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: arXiv IDs look like valid 2024 cs.CL paper IDs — 0.10 points ---
    # Expected format: YYMM.NNNNN where YY=24, MM=01 or 02 (Feb 2024 papers)
    try:
        if not data_rows:
            print("FAIL: Component 3 — No data rows to check IDs")
        else:
            arxiv_pattern = re.compile(r'^24\d{2}\.\d{4,5}$')
            valid_ids = 0
            for row in data_rows:
                arxiv_id = row[0] if len(row) > 0 else None
                if arxiv_id and arxiv_pattern.match(str(arxiv_id).strip()):
                    valid_ids += 1

            ratio = valid_ids / len(data_rows) if data_rows else 0
            if ratio >= 0.8:
                print(f"PASS: Component 3 — {valid_ids}/{len(data_rows)} papers have valid 2024 arXiv IDs (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Only {valid_ids}/{len(data_rows)} papers have valid 2024 arXiv IDs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Keyword Frequency sheet has 10+ entries, sorted descending — 0.30 points ---
    try:
        # Find keyword data rows (non-empty rows after header)
        kf_data = []
        for ri, row in enumerate(kf_rows):
            if ri == 0:
                continue  # skip header
            keyword = row[0] if len(row) > 0 else None
            count_str = row[1] if len(row) > 1 else None
            if keyword:
                try:
                    count_val = int(count_str) if count_str else 0
                except (ValueError, TypeError):
                    count_val = 0
                kf_data.append((keyword, count_val))

        keyword_count = len(kf_data)
        if keyword_count < 10:
            print(f"FAIL: Component 4 — Keyword Frequency sheet has only {keyword_count} entries; expected >= 10")
        else:
            # Check if sorted by count descending
            counts = [c for _, c in kf_data]
            is_sorted_desc = all(counts[i] >= counts[i+1] for i in range(len(counts)-1))
            comp4_pts = 0.30 if is_sorted_desc else 0.15
            if is_sorted_desc:
                print(f"PASS: Component 4 — Keyword Frequency has {keyword_count} keywords, sorted descending ({comp4_pts} pts)")
                total_score += comp4_pts
            elif comp4_pts > 0:
                # Partial: has keywords but not properly sorted
                print(f"PARTIAL: Component 4 — Keyword Frequency has {keyword_count} keywords but NOT sorted descending ({comp4_pts} pts)")
                total_score += comp4_pts
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in VM env
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
