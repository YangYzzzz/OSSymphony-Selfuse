"""
Reward Script: Organize 5 SF restaurants into LibreOffice Calc ODS table
Task ID: osworld_multi_apps_web_location_001
Domain: libreoffice_calc
Scoring:
  Component 1: Correct column headers (Name, Rating, Address, Cuisine, Price_Range) — 0.3 pts
  Component 2: Rows sorted by Rating descending (La Taqueria 4.7 first) — 0.3 pts
  Component 3: All 5 restaurants present with correct data — 0.2 pts
  Component 4: Header row is bold (HeaderStyle with font-weight=bold) — 0.2 pts
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_001'
FILE_PATH = '/home/user/Desktop/sf_restaurants.ods'

# ODS XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

# Expected restaurant data sorted by Rating descending
EXPECTED_RESTAURANTS = [
    {'name': 'La Taqueria', 'rating': 4.7},
    {'name': 'State Bird Provisions', 'rating': 4.6},
    {'name': 'Tartine Bakery', 'rating': 4.5},
    {'name': 'Nopa', 'rating': 4.4},
    # Zuni Café may have encoding variants
]
EXPECTED_HEADERS = ['Name', 'Rating', 'Address', 'Cuisine', 'Price_Range']
EXPECTED_ALL_NAMES = {
    'La Taqueria', 'State Bird Provisions', 'Tartine Bakery', 'Nopa'
}
# Zuni Café may have accent variation, handled with partial match
ZUNI_PARTIAL = 'Zuni'


def parse_ods(filepath):
    """
    Parse ODS file and return:
      - rows: list of lists of cell text values
      - header_styles: list of style names from row 0
      - bold_style_names: set of style names that have fo:font-weight=bold
    """
    with zipfile.ZipFile(filepath) as z:
        with z.open('content.xml') as f:
            content_xml = f.read().decode('utf-8')
        with z.open('styles.xml') as f:
            styles_xml = f.read().decode('utf-8')

    # Parse content
    content_root = ET.fromstring(content_xml)
    spreadsheet = content_root.find('.//office:spreadsheet', NS)
    table = spreadsheet.find('table:table', NS)
    table_rows = table.findall('table:table-row', NS)

    rows = []
    header_styles = []
    for i, row_el in enumerate(table_rows):
        cells = row_el.findall('table:table-cell', NS)
        row_data = []
        for cell in cells:
            p = cell.find('text:p', NS)
            row_data.append(p.text if p is not None else None)
        rows.append(row_data)
        if i == 0:
            for cell in cells:
                style_name = cell.get(
                    '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', '')
                header_styles.append(style_name)

    # Parse styles.xml to find bold style names
    styles_root = ET.fromstring(styles_xml)
    bold_style_names = set()
    for style_el in styles_root.findall('.//style:style', NS):
        text_props = style_el.find('style:text-properties', NS)
        if text_props is not None:
            fw = text_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-weight', '')
            if fw.lower() == 'bold':
                bold_style_names.add(style_el.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', ''))

    return rows, header_styles, bold_style_names


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid ODS
    if not os.path.exists(file_path):
        print(f"FAIL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        rows, header_styles, bold_style_names = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not rows:
        print("CRITICAL: ODS file has no rows")
        print("REWARD: 0.0")
        return 0.0

    header_row = rows[0] if rows else []
    data_rows = rows[1:] if len(rows) > 1 else []

    # Component 1: Correct column headers (0.3 points)
    # Expected: Name, Rating, Address, Cuisine, Price_Range
    try:
        if len(header_row) >= 5:
            found_headers = [str(h).strip() if h else '' for h in header_row[:5]]
            if found_headers == EXPECTED_HEADERS:
                print(f"PASS: Component 1 — correct headers {found_headers} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — expected headers {EXPECTED_HEADERS}, found {found_headers}")
        else:
            print(f"FAIL: Component 1 — expected 5 columns, found {len(header_row)}: {header_row}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rows sorted by Rating descending, La Taqueria (4.7) first (0.3 points)
    # Check first 4 rows match descending rating order
    try:
        if len(data_rows) >= 1:
            first_name = str(data_rows[0][0]).strip() if data_rows[0] and len(data_rows[0]) > 0 else ''
            first_rating_raw = data_rows[0][1] if len(data_rows[0]) > 1 else None
            first_rating = float(first_rating_raw) if first_rating_raw is not None else None

            if first_name == 'La Taqueria' and first_rating is not None and abs(first_rating - 4.7) < 0.01:
                # Also verify descending order for all rows
                ratings = []
                for dr in data_rows:
                    try:
                        r = float(dr[1]) if dr and len(dr) > 1 and dr[1] is not None else None
                        if r is not None:
                            ratings.append(r)
                    except (ValueError, TypeError):
                        pass

                is_desc = all(ratings[i] >= ratings[i+1] for i in range(len(ratings)-1))
                if is_desc and len(ratings) == 5:
                    print(f"PASS: Component 2 — sorted by Rating descending, La Taqueria first (4.7), ratings: {ratings} (0.3 pts)")
                    total_score += 0.3
                elif first_name == 'La Taqueria':
                    print(f"PARTIAL FAIL: Component 2 — La Taqueria is first but sort order not fully correct, ratings: {ratings}")
                else:
                    print(f"FAIL: Component 2 — first row is {first_name} with rating {first_rating}, expected La Taqueria (4.7)")
            else:
                print(f"FAIL: Component 2 — first row is '{first_name}' with rating {first_rating}, expected 'La Taqueria' (4.7)")
        else:
            print("FAIL: Component 2 — no data rows found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 restaurants present with correct ratings (0.2 points)
    try:
        if len(data_rows) == 5:
            names_found = set()
            zuni_count = 0  # count of rows where name contains 'Zuni'
            rating_correct = 0
            expected_rating_map = {
                'La Taqueria': 4.7,
                'State Bird Provisions': 4.6,
                'Tartine Bakery': 4.5,
                'Nopa': 4.4,
            }

            for dr in data_rows:
                name = str(dr[0]).strip() if dr and len(dr) > 0 and dr[0] else ''
                rating_raw = dr[1] if len(dr) > 1 else None
                try:
                    rating = float(rating_raw) if rating_raw is not None else None
                except (ValueError, TypeError):
                    rating = None

                if name in EXPECTED_ALL_NAMES:
                    names_found.add(name)
                    if rating is not None and abs(rating - expected_rating_map[name]) < 0.01:
                        rating_correct += 1

                if ZUNI_PARTIAL in name:
                    zuni_count += 1
                    if rating is not None and abs(rating - 4.3) < 0.01:
                        rating_correct += 1

            all_4_expected_found = names_found == EXPECTED_ALL_NAMES
            all_5_present = all_4_expected_found and (zuni_count >= 1)

            if all_5_present and rating_correct == 5:
                print(f"PASS: Component 3 — all 5 restaurants present with correct ratings (0.2 pts)")
                total_score += 0.2
            else:
                missing = EXPECTED_ALL_NAMES - names_found
                print(f"FAIL: Component 3 — found {len(names_found)+min(zuni_count, 1)}/5 restaurants, "
                      f"correct ratings: {rating_correct}/5, missing: {missing}, zuni_count: {zuni_count}")
        else:
            print(f"FAIL: Component 3 — expected 5 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Header row cells use a bold style (0.2 points)
    # Verify that header cells are styled with a style that has font-weight=bold
    try:
        if header_styles and bold_style_names:
            headers_are_bold = all(s in bold_style_names for s in header_styles if s)
            if headers_are_bold and len(header_styles) >= 5:
                print(f"PASS: Component 4 — header row uses bold style(s): {set(header_styles)}, "
                      f"bold styles defined: {bold_style_names} (0.2 pts)")
                total_score += 0.2
            else:
                non_bold = [s for s in header_styles if s and s not in bold_style_names]
                print(f"FAIL: Component 4 — not all header cells bold. "
                      f"Styles used: {header_styles}, bold styles: {bold_style_names}, "
                      f"non-bold styles in header: {non_bold}")
        else:
            print(f"FAIL: Component 4 — no header styles found or no bold styles defined. "
                  f"header_styles={header_styles}, bold_style_names={bold_style_names}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
