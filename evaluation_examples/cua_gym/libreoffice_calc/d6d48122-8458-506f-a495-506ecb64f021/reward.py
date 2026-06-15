"""
Reward Script: DBLP researcher data entry, sorting, Career Length formula, alternating colors
Task ID: osworld_multi_apps_scholar_to_calc_012
Domain: libreoffice_calc
Scoring:
  Component 1: 4 data rows present with researcher names (0.25 pts)
  Component 2: Data sorted by First Year ascending (0.25 pts)
  Component 3: Career Length column has formula =2024-C_n style (0.25 pts)
  Component 4: Alternating row background colors (light blue / white) on data rows (0.25 pts)
"""

import os
import zipfile
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_012'
FILE_PATH = f'{WORKDIR}/researchers.ods'

# Namespaces used in ODS XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'calcext': 'urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0',
}


def parse_ods(file_path):
    """
    Parse an ODS file and return:
      - rows: list of lists of (value, style_name, formula) per non-empty row
      - style_bg: dict mapping style_name -> background_color hex (lower, e.g. '#add8e6')
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read()

    root = ET.fromstring(content)

    # --- Parse automatic styles for background colors ---
    style_bg = {}
    auto_styles = root.find('.//office:automatic-styles', NS)
    if auto_styles is not None:
        for style_elem in auto_styles.findall('style:style', NS):
            s_name = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name')
            s_family = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family')
            if s_family != 'table-cell':
                continue
            cell_props = style_elem.find('style:table-cell-properties', NS)
            if cell_props is not None:
                bg = cell_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}background-color')
                if bg:
                    style_bg[s_name] = bg.lower()

    # --- Parse spreadsheet rows ---
    spreadsheet = root.find('.//office:spreadsheet', NS)
    tables = spreadsheet.findall('table:table', NS)
    if not tables:
        return [], style_bg

    table = tables[0]  # first sheet
    raw_rows = []
    for row_elem in table.findall('table:table-row', NS):
        repeat_rows = int(row_elem.get(
            '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-rows-repeated', '1'))
        cells = []
        for cell_elem in row_elem.findall('table:table-cell', NS):
            repeat = int(cell_elem.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated', '1'))
            # Get text value
            p_elems = cell_elem.findall('text:p', NS)
            val = ' '.join(p.text or '' for p in p_elems) if p_elems else ''
            # Get formula
            formula = cell_elem.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}formula', '')
            # Get style
            style_name = cell_elem.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', '')
            # Numeric value (for sorting verification)
            num_val = cell_elem.get(
                '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value', '')
            for _ in range(repeat):
                cells.append((val, style_name, formula, num_val))
        for _ in range(repeat_rows):
            raw_rows.append(cells)

    # Trim trailing empty rows
    meaningful_rows = []
    for row_cells in raw_rows:
        non_empty = [(v, s, f, n) for v, s, f, n in row_cells if v or f]
        if non_empty:
            meaningful_rows.append(row_cells)

    return meaningful_rows, style_bg


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load ODS file
    try:
        rows, style_bg = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expect: row 0 = header, rows 1-4 = data
    if len(rows) < 2:
        print(f"FAIL: File has fewer than 2 rows (found {len(rows)}). No data rows present.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    header_row = rows[0]
    data_rows = rows[1:]

    # Get cell values for each data row (first 6 columns)
    def get_cell_value(row, col_idx):
        if col_idx < len(row):
            return row[col_idx][0]  # (val, style, formula, num_val)
        return ''

    def get_cell_style(row, col_idx):
        if col_idx < len(row):
            return row[col_idx][1]
        return ''

    def get_cell_formula(row, col_idx):
        if col_idx < len(row):
            return row[col_idx][2]
        return ''

    def get_cell_num(row, col_idx):
        if col_idx < len(row):
            return row[col_idx][3]
        return ''

    # -------------------------------------------------------------------
    # Component 1: 4 data rows with researcher names filled (0.25 points)
    # -------------------------------------------------------------------
    try:
        expected_researchers = {'Ellen Riloff', 'Rada Mihalcea', 'Diana Inkpen', 'Julia Sedoc'}
        found_names = set()
        for dr in data_rows:
            name = get_cell_value(dr, 0).strip()
            if name:
                found_names.add(name)

        # Check count and that all 4 researchers are present
        if len(data_rows) >= 4 and expected_researchers.issubset(found_names):
            print(f"PASS: Component 1 — 4 data rows present with all researcher names: {found_names} (0.25 pts)")
            total_score += 0.25
        elif len(data_rows) >= 4:
            print(f"FAIL: Component 1 — 4+ rows present but names don't match. Found: {found_names}, Expected: {expected_researchers}")
        else:
            print(f"FAIL: Component 1 — Expected 4 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: Data rows sorted by First Year ascending (0.25 points)
    # Task: sort by 'First Year' column (col index 2) ascending
    # Golden order: 1993, 1999, 2001, 2017
    # -------------------------------------------------------------------
    try:
        first_years = []
        for dr in data_rows[:4]:
            # Prefer numeric value attribute for accuracy
            num_str = get_cell_num(dr, 2)
            val_str = get_cell_value(dr, 2)
            year_str = num_str if num_str else val_str
            try:
                year = int(float(year_str))
                first_years.append(year)
            except (ValueError, TypeError):
                first_years.append(None)

        valid_years = [y for y in first_years if y is not None]
        is_sorted_ascending = (len(valid_years) == 4 and
                               valid_years == sorted(valid_years) and
                               valid_years[0] < valid_years[-1])
        if is_sorted_ascending:
            print(f"PASS: Component 2 — Data rows sorted by First Year ascending: {valid_years} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected ascending First Years, found: {first_years}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: Career Length column has formula =2024-C_n style (0.25 pts)
    # Formula in ODS format: "of:=2024-[.C2]" or similar
    # Check that at least the first data row's Career Length cell has a formula
    # referencing 2024 minus the First Year column
    # -------------------------------------------------------------------
    try:
        formula_count = 0
        for i, dr in enumerate(data_rows[:4]):
            formula = get_cell_formula(dr, 5)  # column F = index 5
            # ODS formula: "of:=2024-[.C2]" pattern
            # Accept variations: contains "2024" and references column C
            if formula and '2024' in formula and ('C' in formula or 'c' in formula):
                formula_count += 1

        if formula_count >= 4:
            print(f"PASS: Component 3 — All 4 Career Length cells have =2024-C_n formula ({formula_count}/4) (0.25 pts)")
            total_score += 0.25
        elif formula_count >= 2:
            # Partial: at least half have formulas
            print(f"PASS (partial): Component 3 — {formula_count}/4 Career Length cells have formula, awarding partial")
            total_score += 0.25  # Still award full as partial is enough signal
        else:
            # Check if values are at least correct (formula may have been hardcoded)
            correct_values = 0
            year_to_length = {1993: 31, 1999: 25, 2001: 23, 2017: 7}
            for dr in data_rows[:4]:
                num_str = get_cell_num(dr, 2)  # First Year
                career_val_str = get_cell_value(dr, 5)
                try:
                    year = int(float(num_str)) if num_str else None
                    career_len = int(float(career_val_str)) if career_val_str else None
                    if year and career_len and year_to_length.get(year) == career_len:
                        correct_values += 1
                except:
                    pass
            if correct_values >= 4:
                print(f"FAIL: Component 3 — No =2024-CX formula found in Career Length cells. Values are correct ({correct_values}/4) but formulas required.")
            else:
                print(f"FAIL: Component 3 — Career Length formula not found or incorrect. Formulas found: {formula_count}/4")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: Alternating row background colors (light blue / white) (0.25 pts)
    # Golden: row 2 = light blue (#add8e6), row 3 = white (#ffffff),
    #         row 4 = light blue (#add8e6), row 5 = white (#ffffff)
    # -------------------------------------------------------------------
    try:
        light_blue_variants = {'#add8e6', '#aad8e6', '#add8e7'}  # slight variation tolerance
        white_variants = {'#ffffff', '#fefefe', ''}  # empty background = white by default

        color_details = []
        mismatch_count = 0

        for i, dr in enumerate(data_rows[:4]):
            # Check first cell of each row (col A) for background color
            style_name = get_cell_style(dr, 0)
            bg_color = style_bg.get(style_name, '').lower()
            color_details.append((i + 2, style_name, bg_color))

            expected_blue = (i % 2 == 0)  # rows 1,3 (index 0,2) = light blue; rows 2,4 (index 1,3) = white
            if expected_blue:
                is_light_blue = (bg_color in light_blue_variants or
                                 'add8e6' in bg_color or
                                 'lightblue' in bg_color)
                if not is_light_blue:
                    mismatch_count += 1
            else:
                if bg_color not in white_variants:
                    mismatch_count += 1

        # Check that there are at least 2 distinct background colors across rows
        unique_colors = set(style_bg.get(get_cell_style(dr, 0), '').lower() for dr in data_rows[:4])

        print(f"DEBUG: Row colors: {color_details}")
        print(f"DEBUG: Unique colors: {unique_colors}")
        print(f"DEBUG: Style->BG map: {style_bg}")

        # Primary check: exact light blue / white alternation
        has_light_blue = any('add8e6' in c for c in unique_colors)
        has_white = any(c in {'#ffffff', ''} for c in unique_colors)

        if mismatch_count == 0 and len(unique_colors) >= 2:
            print(f"PASS: Component 4 — Alternating light blue/white background on data rows (0.25 pts)")
            total_score += 0.25
        elif has_light_blue and has_white and len(unique_colors) >= 2:
            print(f"PASS: Component 4 — Alternating light blue/white colors detected (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — No valid alternating light blue/white colors. mismatch={mismatch_count}, unique={unique_colors}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on this VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
