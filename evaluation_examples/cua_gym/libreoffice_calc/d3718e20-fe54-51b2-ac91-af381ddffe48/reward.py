"""
Reward Script: NeurIPS Decade Analysis - Multi-Sheet Calc + Writer Essay
Task ID: osworld_multi_apps_web_conference_015
Domain: libreoffice_calc (multi-app: also libreoffice_writer)

Task: Compile a decade-long NeurIPS analysis (2015-2024) into:
  1. neurips_decade.ods - multi-sheet Calc workbook with Data sheet (9 columns),
     Chart sheet (line chart of acceptance rate trends)
  2. neurips_evolution_essay.odt in Documents - 500-word Writer essay with
     H1 title and 4 structured paragraphs

Scoring rubric (total = 1.0):
  Component 1: ODS file exists with 2 named sheets: 'Data' and 'Chart'   (0.25 pts)
  Component 2: Data sheet has 10 data rows (2015-2024) with required columns (0.25 pts)
  Component 3: Chart sheet has Year+Acceptance_Rate data (10 rows)        (0.20 pts)
  Component 4: ODT essay file exists in Documents                         (0.15 pts)
  Component 5: ODT has H1 heading + >= 4 paragraphs + >= 500 words        (0.15 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_conference_015'

ODS_PATH = f'{WORKDIR}/neurips_decade.ods'
ODT_PATH = f'{WORKDIR}/Documents/neurips_evolution_essay.odt'

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'chart': 'urn:oasis:names:tc:opendocument:xmlns:chart:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
}

REQUIRED_DATA_COLS = {
    'Year', 'City', 'Country', 'Submitted', 'Accepted',
    'Acceptance_Rate', 'Best_Paper_Title', 'Keynote_Speaker_1', 'Keynote_Speaker_2'
}

EXPECTED_YEARS = {str(y) for y in range(2015, 2025)}  # 2015-2024


def parse_ods_sheets(ods_path):
    """
    Parse an ODS file and return a dict of {sheet_name: [[row values], ...]}
    Only extracts visible cell values (not formulas).
    """
    zf = zipfile.ZipFile(ods_path, 'r')
    content = zf.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)

    body = root.find('.//office:spreadsheet', NS)
    tables = body.findall('table:table', NS)

    sheets = {}
    for t in tables:
        name = t.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name', '')
        rows_data = []
        rows = t.findall('table:table-row', NS)
        for row in rows:
            cells = row.findall('table:table-cell', NS)
            cell_vals = []
            for cell in cells:
                repeat_str = cell.get(
                    '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated', '1'
                )
                try:
                    repeat = int(repeat_str)
                except ValueError:
                    repeat = 1
                p = cell.find('text:p', NS)
                val = p.text if p is not None else None
                for _ in range(repeat):
                    cell_vals.append(val)
            rows_data.append(cell_vals)
        sheets[name] = rows_data
    return sheets


def get_nonempty_rows(rows_data):
    """Filter rows that have at least one non-None value."""
    return [r for r in rows_data if any(v is not None for v in r)]


def parse_odt_text(odt_path):
    """
    Parse an ODT file. Returns (headings, paragraphs, total_word_count).
    headings: list of (outline_level, text)
    paragraphs: list of text strings for body paragraphs (tag=p)
    """
    zf = zipfile.ZipFile(odt_path, 'r')
    content = zf.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)

    body = root.find('.//office:text', NS)
    headings = []
    paragraphs = []
    all_text_parts = []

    for elem in body:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        text_content = ''.join(elem.itertext()).strip()
        if not text_content:
            continue
        all_text_parts.append(text_content)
        if tag == 'h':
            level = elem.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}outline-level', '0')
            try:
                level = int(level)
            except ValueError:
                level = 0
            headings.append((level, text_content))
        elif tag == 'p':
            paragraphs.append(text_content)

    total_words = len(' '.join(all_text_parts).split())
    return headings, paragraphs, total_words


def verify_task():
    total_score = 0.0

    # ------------------------------------------------------------------
    # Component 1: ODS file exists with sheets named 'Data' and 'Chart'
    #              (0.25 points)
    # This FAILS on initial_env (no ODS file), PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 1 — ODS file not found at {ODS_PATH}")
        else:
            sheets = parse_ods_sheets(ODS_PATH)
            sheet_names = list(sheets.keys())
            has_data_sheet = 'Data' in sheet_names
            has_chart_sheet = 'Chart' in sheet_names

            if has_data_sheet and has_chart_sheet:
                print(f"PASS: Component 1 — ODS file found with sheets: {sheet_names} (0.25 pts)")
                total_score += 0.25
            else:
                missing = []
                if not has_data_sheet:
                    missing.append("'Data'")
                if not has_chart_sheet:
                    missing.append("'Chart'")
                print(f"FAIL: Component 1 — ODS missing sheets: {missing}; found: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Data sheet has all 9 required columns + 10 data rows
    #              covering years 2015-2024 (0.25 points)
    # This FAILS on initial_env (no ODS), PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print("FAIL: Component 2 — ODS file not found, skipping Data sheet check")
        else:
            if 'sheets' not in dir():
                sheets = parse_ods_sheets(ODS_PATH)
            if 'Data' not in sheets:
                print("FAIL: Component 2 — 'Data' sheet not present")
            else:
                data_rows = get_nonempty_rows(sheets['Data'])
                # First row should be headers
                if len(data_rows) < 2:
                    print(f"FAIL: Component 2 — Data sheet has only {len(data_rows)} non-empty rows (expected header + 10 data)")
                else:
                    header_row = [str(v).strip() if v is not None else '' for v in data_rows[0]]
                    # Check required columns
                    missing_cols = REQUIRED_DATA_COLS - set(header_row)
                    # Count data rows and check years
                    data_only_rows = data_rows[1:]
                    year_col_idx = None
                    for i, col in enumerate(header_row):
                        if col == 'Year':
                            year_col_idx = i
                            break

                    years_found = set()
                    if year_col_idx is not None:
                        for r in data_only_rows:
                            if year_col_idx < len(r) and r[year_col_idx] is not None:
                                years_found.add(str(r[year_col_idx]).strip())

                    missing_years = EXPECTED_YEARS - years_found
                    correct_row_count = len(data_only_rows) >= 10

                    if not missing_cols and correct_row_count and not missing_years:
                        print(f"PASS: Component 2 — Data sheet has {len(data_only_rows)} data rows, "
                              f"all required columns, years {sorted(years_found)} (0.25 pts)")
                        total_score += 0.25
                    else:
                        details = []
                        if missing_cols:
                            details.append(f"missing columns: {missing_cols}")
                        if not correct_row_count:
                            details.append(f"only {len(data_only_rows)} data rows (expected 10)")
                        if missing_years:
                            details.append(f"missing years: {sorted(missing_years)}")
                        print(f"FAIL: Component 2 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Chart sheet has Year + Acceptance_Rate data (10 rows)
    #              verifying the chart data source for acceptance rate trend
    #              (0.20 points)
    # This FAILS on initial_env (no ODS), PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print("FAIL: Component 3 — ODS file not found, skipping Chart sheet check")
        else:
            if 'sheets' not in dir():
                sheets = parse_ods_sheets(ODS_PATH)
            if 'Chart' not in sheets:
                print("FAIL: Component 3 — 'Chart' sheet not present")
            else:
                chart_rows = get_nonempty_rows(sheets['Chart'])
                if len(chart_rows) < 2:
                    print(f"FAIL: Component 3 — Chart sheet has {len(chart_rows)} non-empty rows (expected header + 10)")
                else:
                    header_row = [str(v).strip() if v is not None else '' for v in chart_rows[0]]
                    has_year_col = 'Year' in header_row
                    has_rate_col = 'Acceptance_Rate' in header_row
                    data_only_rows = chart_rows[1:]
                    has_ten_rows = len(data_only_rows) >= 10

                    if has_year_col and has_rate_col and has_ten_rows:
                        print(f"PASS: Component 3 — Chart sheet has Year+Acceptance_Rate columns "
                              f"and {len(data_only_rows)} data rows (0.20 pts)")
                        total_score += 0.20
                    else:
                        details = []
                        if not has_year_col:
                            details.append("missing 'Year' column")
                        if not has_rate_col:
                            details.append("missing 'Acceptance_Rate' column")
                        if not has_ten_rows:
                            details.append(f"only {len(data_only_rows)} data rows (expected 10)")
                        print(f"FAIL: Component 3 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: ODT essay file exists in Documents directory
    #              (0.15 points)
    # This FAILS on initial_env (no ODT file), PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        if os.path.exists(ODT_PATH):
            file_size = os.path.getsize(ODT_PATH)
            if file_size > 1000:  # must be a real file, not empty
                print(f"PASS: Component 4 — ODT essay file found at {ODT_PATH} "
                      f"({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — ODT file exists but appears empty ({file_size} bytes)")
        else:
            print(f"FAIL: Component 4 — ODT essay not found at {ODT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: ODT has H1 heading + at least 4 paragraphs + >= 500 words
    #              covering required topics (growth, thematic, geographic,
    #              acceptance rate) (0.15 points)
    # This FAILS on initial_env (no ODT), PASSES on golden_env.
    # ------------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print("FAIL: Component 5 — ODT essay not found, skipping structure check")
        else:
            headings, paragraphs, total_words = parse_odt_text(ODT_PATH)

            # Check H1 heading
            h1_headings = [h for level, h in headings if level == 1]
            has_h1 = len(h1_headings) >= 1

            # Check at least 4 body paragraphs
            has_four_paragraphs = len(paragraphs) >= 4

            # Check >= 500 words
            has_500_words = total_words >= 500

            # Check coverage of key topics (using keyword matching)
            all_body_text = ' '.join(paragraphs).lower()
            topic_keywords = {
                'growth': any(kw in all_body_text for kw in ['growth', 'submissions', 'accepted', 'exponential']),
                'thematic': any(kw in all_body_text for kw in ['thematic', 'theme', 'deep learning', 'theory', 'application']),
                'geographic': any(kw in all_body_text for kw in ['geographic', 'city', 'venue', 'montreal', 'vancouver', 'virtual']),
                'acceptance_rate': any(kw in all_body_text for kw in ['acceptance rate', 'acceptance_rate', 'percent', '%']),
            }
            topics_covered = sum(1 for v in topic_keywords.values() if v)

            if has_h1 and has_four_paragraphs and has_500_words:
                print(f"PASS: Component 5 — ODT has H1 heading ('{h1_headings[0][:60]}...'), "
                      f"{len(paragraphs)} paragraphs, {total_words} words, "
                      f"{topics_covered}/4 topics covered (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not has_h1:
                    details.append(f"no H1 heading found (headings: {headings})")
                if not has_four_paragraphs:
                    details.append(f"only {len(paragraphs)} paragraphs (expected >= 4)")
                if not has_500_words:
                    details.append(f"only {total_words} words (expected >= 500)")
                print(f"FAIL: Component 5 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == '__main__':
    verify_task()
