"""
Reward Script: Add 4 Google Brain/DeepMind NLP researcher rows to LibreOffice Calc
               and create a bar chart on a new 'Chart' sheet.
Task ID: osworld_multi_apps_scholar_to_calc_015
Domain:  libreoffice_calc
Scoring:
  Component 1 (0.4): 4 researcher data rows present in 'Researchers' sheet
  Component 2 (0.3): A second sheet named 'Chart' exists
  Component 3 (0.3): The 'Chart' sheet contains a bar chart referencing Publications data
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_015'
FILE_PATH = f'{WORKDIR}/google_researchers.ods'

# Expected researchers (lowercase for case-insensitive matching)
EXPECTED_RESEARCHERS = [
    'oriol vinyals',
    'samy bengio',
    'quoc v. le',
    'tomas mikolov',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: file must exist and be readable ---
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pyexcel_ods3
    except ImportError:
        print("CRITICAL: pyexcel_ods3 not available")
        print("REWARD: 0.0")
        return 0.0

    # Load spreadsheet data
    try:
        data = pyexcel_ods3.get_data(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sheet_names = list(data.keys())
    print(f"INFO: Sheets found: {sheet_names}")

    # -------------------------------------------------------
    # Component 1: 4 researcher data rows in 'Researchers' sheet (0.4 points)
    # Initial env has only the header row; golden env has 4 data rows.
    # -------------------------------------------------------
    try:
        if 'Researchers' not in sheet_names:
            print("FAIL: Component 1 — 'Researchers' sheet not found")
        else:
            researchers_sheet = data['Researchers']
            # Data rows are after the header (row index 0)
            data_rows = [row for row in researchers_sheet[1:] if row and len(row) >= 1 and row[0]]

            # Count how many expected researcher names appear in data rows
            found_names = set()
            for row in data_rows:
                name_cell = str(row[0]).strip().lower() if row else ''
                for expected in EXPECTED_RESEARCHERS:
                    if expected in name_cell or name_cell in expected:
                        found_names.add(expected)

            print(f"INFO: Data rows found: {len(data_rows)}")
            print(f"INFO: Found researcher names: {[str(r[0]) for r in data_rows if r]}")
            print(f"INFO: Matched expected researchers: {len(found_names)}/4")

            # Full rows have all 4 columns: Name, Affiliation, Publications, Largest-Team Paper
            rows_with_full_data = [
                row for row in data_rows
                if len(row) >= 4 and row[0] and row[1] and row[2] is not None and row[3]
            ]

            if len(data_rows) >= 4 and len(found_names) >= 4:
                print("PASS: Component 1 — All 4 researchers found with data (0.4 pts)")
                total_score += 0.4
            elif len(rows_with_full_data) >= 4:
                print("PASS: Component 1 — 4 complete data rows found (0.4 pts)")
                total_score += 0.4
            elif len(data_rows) >= 2:
                print(f"PARTIAL: Component 1 — {len(data_rows)} data rows found, expected 4 (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — Expected 4 researcher rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------
    # Component 2: Second sheet named 'Chart' exists (0.3 points)
    # Initial env has only 'Researchers' sheet; golden env adds a 'Chart' sheet.
    # -------------------------------------------------------
    try:
        if 'Chart' in sheet_names:
            chart_position = sheet_names.index('Chart')
            print(f"PASS: Component 2 — 'Chart' sheet exists at position {chart_position} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 'Chart' sheet not found; sheets: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------
    # Component 3: Bar chart present in the ODS, referencing Publications data (0.3 points)
    # The initial env has no embedded chart object; golden env has an embedded bar chart.
    # We inspect the ODS zip archive for a chart object referencing Researchers.C (Publications column).
    # -------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            namelist = z.namelist()

            # Find embedded chart object content files (exclude main content.xml)
            chart_content_files = [
                n for n in namelist
                if n.endswith('content.xml') and n != 'content.xml'
            ]
            print(f"INFO: Chart content files: {chart_content_files}")

            # Verify main content.xml references an embedded chart object
            main_content = z.read('content.xml').decode('utf-8')
            has_draw_object = 'draw:object' in main_content
            if has_draw_object:
                print("INFO: Embedded draw:object found in content.xml")
            else:
                print("INFO: No draw:object found in content.xml")

            # Inspect each chart content XML for bar type and publications reference
            bar_chart_count = sum(
                1 for cf in chart_content_files
                if ('chart:class="chart:bar"' in z.read(cf).decode('utf-8')
                    or "chart:class='chart:bar'" in z.read(cf).decode('utf-8'))
            )

            pubs_ref_count = sum(
                1 for cf in chart_content_files
                if re.search(r'Researchers\.C\d', z.read(cf).decode('utf-8'))
            )

            print(f"INFO: Bar chart objects found: {bar_chart_count}")
            print(f"INFO: Charts referencing Publications column: {pubs_ref_count}")

            if has_draw_object and bar_chart_count >= 1 and pubs_ref_count >= 1:
                print("PASS: Component 3 — Bar chart found, references Publications data (0.3 pts)")
                total_score += 0.3
            elif has_draw_object and bar_chart_count >= 1:
                print("PARTIAL: Component 3 — Bar chart found but publications ref not confirmed (0.2 pts)")
                total_score += 0.2
            elif has_draw_object:
                print("PARTIAL: Component 3 — Chart object found but not confirmed as bar chart (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 3 — No embedded chart found in ODS file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
