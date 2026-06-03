"""
Reward Script: Open survey_results.pdf, enter data into survey_analysis.ods,
               calculate statistics, and create a radar chart.
Task ID: pdf_cross_041
Domain: libreoffice_calc (cross-domain: pdf + calc)

Scoring Rubric:
  Component 1: survey_analysis.ods exists (precondition gate)
  Component 2: Survey Data sheet has 30 rows of ratings (1-5) for 5 categories — 0.25 pts
  Component 3: Statistics sheet has AVERAGE, MEDIAN, MODE, STDEV formulas/values for all 5 categories — 0.40 pts
  Component 4: A radar chart is embedded in the ODS file — 0.35 pts
  Total: 1.0

Ground truth (from context):
  - 30 participants, 5 categories: Usability, Performance, Design, Support, Value
  - Ratings are integers 1-5
  - Statistics: mean, median, mode, std deviation for each category
  - A radar chart comparing the 5 category means

Note: ODS is a ZIP archive; use zipfile + xml.etree.ElementTree to parse it.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_041'
ODS_PATH = f'{WORKDIR}/Documents/survey_analysis.ods'

# ODS XML namespaces
NS_TABLE = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
NS_CHART = 'urn:oasis:names:tc:opendocument:xmlns:chart:1.0'
NS_DRAW = 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'

CATEGORIES = ['Usability', 'Performance', 'Design', 'Support', 'Value']
STAT_FUNCTIONS = ['AVERAGE', 'MEDIAN', 'MODE', 'STDEV']
# Expected mean values (ground truth from context/golden file analysis)
EXPECTED_MEANS = {
    'Usability': 3.8,
    'Performance': 3.7,
    'Design': 3.9,
    'Support': 3.767,
    'Value': 3.9,
}
MEAN_TOLERANCE = 0.15  # allow rounding differences


def parse_ods_content(ods_path):
    """Parse ODS file and return root element and all tables."""
    with zipfile.ZipFile(ods_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)
    tables = root.findall('.//{' + NS_TABLE + '}table')
    return root, tables


def get_cell_info(cell):
    """Extract formula, value, and text content from an ODS table-cell."""
    formula = cell.get('{' + NS_TABLE + '}formula')
    val = cell.get('{' + NS_OFFICE + '}value')
    texts = []
    for p in cell.findall('{' + NS_TEXT + '}p'):
        texts.append(''.join(p.itertext()))
    text_val = ' '.join(texts).strip()
    return {'formula': formula, 'value': val, 'text': text_val}


def iter_table_rows(table):
    """
    Yield (row_index_1based, list_of_cell_info_dicts) for each logical row,
    expanding repeated rows/columns.
    """
    row_idx = 1
    for row in table.findall('{' + NS_TABLE + '}table-row'):
        repeat = int(row.get('{' + NS_TABLE + '}number-rows-repeated', 1))
        cells = row.findall('{' + NS_TABLE + '}table-cell')
        row_data = []
        for cell in cells:
            c_repeat = int(cell.get('{' + NS_TABLE + '}number-columns-repeated', 1))
            info = get_cell_info(cell)
            for _ in range(c_repeat):
                row_data.append(info)
        yield row_idx, row_data
        row_idx += repeat


def verify_task(ods_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: file must exist ---
    if not os.path.exists(ods_path):
        print(f"CRITICAL: survey_analysis.ods not found at {ods_path}")
        print("REWARD: 0.0")
        return 0.0

    # Try to open ODS as a ZIP archive
    try:
        root, tables = parse_ods_content(ods_path)
        print(f"INFO: Loaded ODS with {len(tables)} sheet(s): "
              f"{[t.get('{' + NS_TABLE + '}name') for t in tables]}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {ods_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build sheet name → table element map
    table_map = {}
    for t in tables:
        name = t.get('{' + NS_TABLE + '}name', '')
        table_map[name] = t

    # ---------------------------------------------------------------
    # Component 1: Survey Data sheet has 30 rows of integer ratings (0.25 pts)
    #
    # We look for a sheet with a name that includes "Survey Data" or
    # similar, check that it has a header row (Usability/Performance/etc.)
    # and at least 30 data rows with values in 1-5 range.
    # ---------------------------------------------------------------
    try:
        # Find the survey data sheet (flexible naming)
        survey_sheet = None
        for name, tbl in table_map.items():
            if 'survey' in name.lower() or 'data' in name.lower():
                # Check if it has category headers
                for row_idx, row_data in iter_table_rows(tbl):
                    if row_idx > 3:
                        break
                    texts = [c['text'].lower() for c in row_data if c['text']]
                    if any(cat.lower() in texts for cat in CATEGORIES):
                        survey_sheet = tbl
                        break
                if survey_sheet is not None:
                    break

        if survey_sheet is None:
            # Fall back to first sheet
            if tables:
                survey_sheet = tables[0]
                print("WARN: Could not find labeled Survey Data sheet; using first sheet")

        if survey_sheet is None:
            print("FAIL: Component 1 — No survey data sheet found")
        else:
            # Count valid data rows: rows with numeric values in range 1-5
            data_rows_found = 0
            header_row_idx = None
            for row_idx, row_data in iter_table_rows(survey_sheet):
                # Skip empty rows
                non_empty = [c for c in row_data if c['text'] or c['value']]
                if not non_empty:
                    continue

                # Detect header row (contains category names)
                texts_lower = [c['text'].lower() for c in non_empty if c['text']]
                if any(cat.lower() in texts_lower for cat in CATEGORIES):
                    header_row_idx = row_idx
                    print(f"INFO: Header row found at row {row_idx}")
                    continue

                # Count data rows after header
                if header_row_idx is not None:
                    # Check for numeric rating values in 1-5 range
                    numeric_vals = []
                    for c in row_data:
                        if c['value'] is not None:
                            try:
                                v = float(c['value'])
                                numeric_vals.append(v)
                            except ValueError:
                                pass
                        elif c['text']:
                            try:
                                v = float(c['text'])
                                numeric_vals.append(v)
                            except ValueError:
                                pass
                    # Valid data row: at least 5 numeric values in 1-5
                    rating_vals = [v for v in numeric_vals if 1 <= v <= 5]
                    if len(rating_vals) >= 5:
                        data_rows_found += 1

            if data_rows_found >= 30:
                print(f"PASS: Component 1 — Survey Data sheet has {data_rows_found} rows with 5-category ratings (0.25 pts)")
                total_score += 0.25
            elif data_rows_found >= 25:
                # Partial credit: close to 30
                print(f"PARTIAL: Component 1 — Survey Data sheet has {data_rows_found}/30 rows (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — Survey Data sheet has only {data_rows_found} valid data rows (expected 30)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Statistics sheet has AVERAGE, MEDIAN, MODE, STDEV
    #              formulas/values for all 5 categories (0.40 pts)
    #
    # Full credit: all 4 statistics present for all 5 categories (20 cells)
    # Partial: some stats present
    # ---------------------------------------------------------------
    try:
        stats_sheet = None
        for name, tbl in table_map.items():
            if 'stat' in name.lower():
                stats_sheet = tbl
                break

        if stats_sheet is None:
            # Fall back: search all sheets for AVERAGE formulas
            for name, tbl in table_map.items():
                for row_idx, row_data in iter_table_rows(tbl):
                    if row_idx > 15:
                        break
                    for c in row_data:
                        if c.get('formula') and 'AVERAGE' in c.get('formula', '').upper():
                            stats_sheet = tbl
                            break
                    if stats_sheet is not None:
                        break

        if stats_sheet is None:
            print("FAIL: Component 2 — No statistics sheet found with AVERAGE/MEDIAN/MODE/STDEV")
        else:
            # Count stat functions found
            stat_funcs_found = {f: 0 for f in STAT_FUNCTIONS}
            categories_covered = set()
            mean_values_correct = 0

            for row_idx, row_data in iter_table_rows(stats_sheet):
                for c in row_data:
                    formula = (c.get('formula') or '').upper()
                    for func in STAT_FUNCTIONS:
                        if func in formula:
                            stat_funcs_found[func] += 1

                # Check if row has a category name
                texts = [c['text'] for c in row_data if c['text']]
                for cat in CATEGORIES:
                    if cat in texts:
                        categories_covered.add(cat)
                        # Also check mean value correctness
                        for c in row_data:
                            if c.get('value') is not None and (c.get('formula') or '').upper().find('AVERAGE') >= 0:
                                try:
                                    actual_mean = float(c['value'])
                                    expected_mean = EXPECTED_MEANS.get(cat)
                                    if expected_mean is not None and abs(actual_mean - expected_mean) <= MEAN_TOLERANCE:
                                        mean_values_correct += 1
                                except (ValueError, TypeError):
                                    pass

            # Determine partial score
            funcs_present = sum(1 for f in STAT_FUNCTIONS if stat_funcs_found[f] >= 5)  # >= 5 = covers all categories
            cats_covered = len(categories_covered)

            print(f"INFO: Stat functions with >=5 occurrences: {stat_funcs_found}")
            print(f"INFO: Categories covered in stats sheet: {categories_covered}")
            print(f"INFO: Mean values matching expected: {mean_values_correct}/5")

            # Award points:
            # - 0.10 pts: at least 1 stat function with >= 5 occurrences (covers all categories)
            # - 0.20 pts: all 4 stat functions present with >= 5 occurrences each
            # - 0.30 pts: + correct mean values for all 5 categories
            # - 0.40 pts: + all 5 categories in stats sheet header/labels

            comp2_score = 0.0
            if funcs_present >= 1:
                comp2_score += 0.10
            if funcs_present >= 4:
                comp2_score += 0.10
            if cats_covered >= 5:
                comp2_score += 0.10
            if mean_values_correct >= 5:
                comp2_score += 0.10

            total_score += comp2_score
            if comp2_score >= 0.40:
                print(f"PASS: Component 2 — Statistics sheet has all required formulas and correct mean values ({comp2_score:.2f} pts)")
            elif comp2_score > 0:
                print(f"PARTIAL: Component 2 — Statistics partially complete ({comp2_score:.2f}/0.40 pts)")
            else:
                print("FAIL: Component 2 — No valid statistics found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: A radar chart is embedded in the ODS file (0.35 pts)
    #
    # ODS stores charts as embedded objects under "Object N/content.xml".
    # Look for chart:chart with class="chart:filled-radar" or "chart:radar"
    # or any radar-type chart.
    # Also check ObjectReplacements for the chart image.
    # ---------------------------------------------------------------
    try:
        chart_count = 0
        radar_chart_count = 0

        with zipfile.ZipFile(ods_path, 'r') as z:
            filelist = z.namelist()

            # Look for Object N/content.xml files (embedded charts)
            obj_content_files = [f for f in filelist if f.startswith('Object') and f.endswith('content.xml')]
            print(f"INFO: Found object files: {obj_content_files}")

            for obj_file in obj_content_files:
                try:
                    obj_content = z.read(obj_file).decode('utf-8')
                    obj_root = ET.fromstring(obj_content)

                    # Find chart elements
                    chart_els = obj_root.findall('.//{' + NS_CHART + '}chart')
                    chart_count += len(chart_els)

                    for chart_el in chart_els:
                        chart_class = chart_el.get('{' + NS_CHART + '}class', '').lower()
                        print(f"INFO: Found chart type: {chart_class}")

                        # Count series
                        series = obj_root.findall('.//{' + NS_CHART + '}series')
                        if series:
                            dp_count = len(series[0].findall('.//{' + NS_CHART + '}data-point'))
                            print(f"INFO: Series count: {len(series)}, data points in first: {dp_count}")

                        # Count radar charts specifically
                        radar_chart_count += 1 if 'radar' in chart_class else 0

                except Exception as e:
                    print(f"WARN: Could not parse {obj_file}: {e}")

        # Also check the main content.xml for embedded chart frames
        draw_frames = root.findall('.//{' + NS_DRAW + '}frame')
        draw_objects = root.findall('.//{' + NS_DRAW + '}object')
        frame_count = len(draw_frames) + len(draw_objects)
        if frame_count > 0:
            print(f"INFO: Found {frame_count} draw:frame/object element(s) in main sheet")
        # If no embedded objects found in zip but frames exist in content, count as chart
        if chart_count == 0 and frame_count > 0:
            chart_count = frame_count

        # Scoring for Component 3
        comp3_score = 0.0
        if chart_count >= 1:
            comp3_score += 0.20
        if radar_chart_count >= 1:
            comp3_score += 0.15

        total_score += comp3_score

        if comp3_score >= 0.35:
            print(f"PASS: Component 3 — Radar chart found and confirmed ({comp3_score:.2f} pts). "
                  f"Charts: {chart_count}, Radar: {radar_chart_count}")
        elif comp3_score > 0:
            print(f"PARTIAL: Component 3 — Chart found but not confirmed as radar ({comp3_score:.2f}/0.35 pts)")
        else:
            print("FAIL: Component 3 — No chart found in ODS file")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(ODS_PATH):
    print(f"File not found: {ODS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ODS_PATH)
