"""
Reward Script: Research top 15 global restaurant chains and build ODS database + ODT article
Task ID: osworld_multi_apps_web_location_015
Domain: libreoffice_calc (multi-app: Calc + Writer)

Scoring Rubric:
  Component 1: ODS file has 15 data rows + required 11 columns          — 0.25 pts
  Component 2: ODS US_Pct column contains formulas (=Fx/Ex pattern)    — 0.25 pts
  Component 3: ODS rows sorted by Total_Locations descending            — 0.15 pts
  Component 4: ODT file exists with H1 heading + 3 body paragraphs     — 0.20 pts
  Component 5: ODT has >= 300 words and references specific numbers     — 0.15 pts
  Total:                                                                  1.00 pts
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_015'

# Canonical file paths
ODS_PATH = f'{WORKDIR}/restaurant_chains_global.ods'
ODT_PATH = f'{WORKDIR}/Documents/fast_food_dominance.odt'

# Required columns for the ODS database
REQUIRED_COLUMNS = [
    'Rank', 'Chain', 'Founded_Year', 'Headquarters', 'Total_Locations',
    'US_Locations', 'International_Locations', 'US_Pct',
    'Est_Annual_Revenue_B_USD', 'Primary_Cuisine', 'Parent_Company'
]

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}


def parse_ods(ods_path):
    """Parse ODS file and return (header_row, data_rows, formulas_by_row_col).
    formulas_by_row_col: dict {(row_idx, col_idx): formula_string}
    """
    with zipfile.ZipFile(ods_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    tree = ET.fromstring(content)
    body = tree.find('.//office:spreadsheet', NS)
    sheets = body.findall('table:table', NS)
    if not sheets:
        return None, [], {}

    sheet = sheets[0]
    rows = sheet.findall('table:table-row', NS)
    header = None
    data_rows = []
    formulas = {}

    for i, row in enumerate(rows):
        cells = row.findall('table:table-cell', NS)
        row_data = []
        for j, cell in enumerate(cells):
            formula = cell.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}formula')
            if formula:
                formulas[(i, j)] = formula
            texts = cell.findall('.//text:p', NS)
            val = ' '.join(t.text or '' for t in texts if t.text).strip()
            row_data.append(val)
        if i == 0:
            header = row_data
        else:
            if any(row_data):
                data_rows.append(row_data)

    return header, data_rows, formulas


def parse_odt_text(odt_path):
    """Parse ODT file and return (headings, paragraphs, word_count)."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    tree = ET.fromstring(content)
    headings = []
    paragraphs = []

    # Collect headings (H1, H2, etc.)
    for elem in tree.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h'):
        text = ''.join(elem.itertext()).strip()
        if text:
            headings.append(text)

    # Collect body paragraphs
    for elem in tree.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
        text = ''.join(elem.itertext()).strip()
        if text:
            paragraphs.append(text)

    full_text = ' '.join(headings + paragraphs)
    words = re.findall(r'\b\w+\b', full_text)
    return headings, paragraphs, len(words)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: ODS file must exist ---
    if not os.path.exists(ODS_PATH):
        print(f"CRITICAL: ODS file not found at {ODS_PATH}")
        print(f"REWARD: 0.0")
        return 0.0

    # Parse ODS file
    try:
        header, data_rows, formulas = parse_ods(ODS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: ODS has 15 data rows and all 11 required columns (0.25 pts)
    # -----------------------------------------------------------------------
    try:
        has_15_rows = len(data_rows) == 15
        # Normalize column names for comparison (case-insensitive, strip)
        header_normalized = [h.strip() for h in (header or [])]
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in header_normalized]
        has_all_cols = len(missing_cols) == 0

        if has_15_rows and has_all_cols:
            print(f"PASS: Component 1 — ODS has 15 data rows and all 11 required columns (0.25 pts)")
            total_score += 0.25
        else:
            if not has_15_rows:
                print(f"FAIL: Component 1 — Expected 15 data rows, found {len(data_rows)}")
            if not has_all_cols:
                print(f"FAIL: Component 1 — Missing columns: {missing_cols}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: US_Pct column contains formulas (0.25 pts)
    # -----------------------------------------------------------------------
    try:
        # US_Pct is column index 7 (0-based), data rows start at row index 1
        us_pct_col = 7
        formula_count = 0
        formula_pattern = re.compile(r'\[\.F\d+\]/\[\.E\d+\]', re.IGNORECASE)

        for row_idx in range(1, 16):  # rows 1-15 are data rows
            formula = formulas.get((row_idx, us_pct_col), '')
            if formula and formula_pattern.search(formula):
                formula_count += 1

        if formula_count >= 14:
            print(f"PASS: Component 2 — US_Pct column has formulas in {formula_count}/15 data rows (0.25 pts)")
            total_score += 0.25
        elif formula_count >= 7:
            # Partial: at least half have formulas
            print(f"PARTIAL: Component 2 — US_Pct column has formulas in only {formula_count}/15 rows (0.12 pts)")
            total_score += 0.12
        else:
            print(f"FAIL: Component 2 — US_Pct column formulas found in only {formula_count}/15 rows (expected formula like =F2/E2)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Rows sorted by Total_Locations descending (0.15 pts)
    # -----------------------------------------------------------------------
    try:
        # Total_Locations is column index 4 (0-based)
        total_locations_col = 4
        location_values = []
        for row in data_rows:
            if len(row) > total_locations_col:
                val_str = row[total_locations_col].replace(',', '').replace('.', '').strip()
                try:
                    location_values.append(int(float(val_str)))
                except (ValueError, TypeError):
                    location_values.append(None)

        # Check that valid values are in descending order
        valid_vals = [v for v in location_values if v is not None]
        is_sorted = all(valid_vals[i] >= valid_vals[i + 1]
                        for i in range(len(valid_vals) - 1))

        if is_sorted and len(valid_vals) >= 14:
            print(f"PASS: Component 3 — Rows sorted by Total_Locations descending, top: {valid_vals[:5]} (0.15 pts)")
            total_score += 0.15
        else:
            if not is_sorted:
                print(f"FAIL: Component 3 — Rows NOT sorted by Total_Locations descending: {valid_vals[:5]}")
            else:
                print(f"FAIL: Component 3 — Only {len(valid_vals)} valid Total_Locations values found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: ODT file with H1 heading + at least 3 body paragraphs (0.20 pts)
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 4 — ODT file not found at {ODT_PATH}")
        else:
            headings, paragraphs, word_count = parse_odt_text(ODT_PATH)
            has_h1 = len(headings) >= 1
            has_3_paras = len(paragraphs) >= 3

            if has_h1 and has_3_paras:
                print(f"PASS: Component 4 — ODT has H1 heading ('{headings[0][:60]}') "
                      f"and {len(paragraphs)} body paragraphs (0.20 pts)")
                total_score += 0.20
            else:
                if not has_h1:
                    print(f"FAIL: Component 4 — ODT has no H1 heading (found {len(headings)} headings)")
                if not has_3_paras:
                    print(f"FAIL: Component 4 — ODT has only {len(paragraphs)} paragraphs, need >= 3")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: ODT >= 300 words and references specific numbers (0.15 pts)
    # -----------------------------------------------------------------------
    try:
        if os.path.exists(ODT_PATH):
            headings, paragraphs, word_count = parse_odt_text(ODT_PATH)
            full_text = ' '.join(headings + paragraphs)

            has_min_words = word_count >= 300
            # Check that the article references specific chain names from the spreadsheet
            # (at least 3 different chain names must appear)
            chain_names = ["McDonald", "Subway", "Starbucks", "KFC", "Burger King",
                           "Domino", "Pizza Hut", "Dunkin", "Taco Bell", "Wendy"]
            found_chains = [c for c in chain_names if c in full_text]
            references_chains = len(found_chains) >= 3

            # Check that the article references at least some numbers from the ODS
            # (numbers that appear in spreadsheet data like location counts or revenue)
            # Allow numbers in formats like "40,275" or "40275" or "26.5"
            has_numbers = bool(re.search(r'\b\d{1,3}(?:,\d{3})+\b', full_text))  # comma-formatted e.g. 40,275

            if has_min_words and references_chains and has_numbers:
                print(f"PASS: Component 5 — ODT has {word_count} words, references chains: {found_chains[:5]}, "
                      f"includes specific numbers (0.15 pts)")
                total_score += 0.15
            else:
                if not has_min_words:
                    print(f"FAIL: Component 5 — ODT word count {word_count} < 300 words required")
                if not references_chains:
                    print(f"FAIL: Component 5 — ODT references only {len(found_chains)} chains: {found_chains}")
                if not has_numbers:
                    print(f"FAIL: Component 5 — ODT does not reference specific numbers from spreadsheet")
        else:
            print(f"FAIL: Component 5 — ODT file not found, skipping word/content check")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
