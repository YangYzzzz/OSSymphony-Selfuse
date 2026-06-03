"""
Reward Script: Competitive Analysis Report — Chrome browsing + LibreOffice Writer ODT
Task ID: osworld_multi_apps_sys_browser_os_009
Domain: multi_apps (os + libreoffice_writer + chrome)
Scoring:
  Component 1: 3 screenshot files exist on Desktop               (0.30 pts)
  Component 2: language_comparison.odt exists with a table       (0.15 pts)
  Component 3: Table has correct header row                       (0.10 pts)
  Component 4: Table has correct language/version data            (0.30 pts)
  Component 5: Table has correct screenshot paths                 (0.15 pts)
  Total: 1.00
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_sys_browser_os_009'

# Expected ground truth values from task context
EXPECTED_LANGUAGES = ['Python', 'Ruby', 'Go']
EXPECTED_VERSIONS = {
    'python': '3.13.2',
    'ruby': '3.4.1',
    'go': '1.24.0',
}
EXPECTED_SCREENSHOT_PATHS = [
    '/home/user/Desktop/screenshot_1.png',
    '/home/user/Desktop/screenshot_2.png',
    '/home/user/Desktop/screenshot_3.png',
]
EXPECTED_HEADERS = ['Language', 'Version', 'Screenshot Path']
ODT_PATH = f'{WORKDIR}/language_comparison.odt'


def get_all_text(element):
    """Recursively extract all text from an ODF element."""
    texts = []
    for child in element.childNodes:
        if child.nodeType == child.TEXT_NODE:
            texts.append(child.data)
        else:
            texts.append(get_all_text(child))
    return ''.join(texts)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: 3 screenshot files exist on Desktop (0.30 points)
    # These files must be created by the task (Desktop is empty in initial_env)
    try:
        screenshots_found = []
        for i in range(1, 4):
            path = f'{WORKDIR}/screenshot_{i}.png'
            if os.path.isfile(path) and os.path.getsize(path) > 0:
                screenshots_found.append(path)

        n_shots = len(screenshots_found)
        if n_shots == 3:
            print(f"PASS: Component 1 — all 3 screenshot files exist on Desktop (0.30 pts)")
            total_score += 0.30
        elif n_shots == 2:
            print(f"PARTIAL: Component 1 — 2/3 screenshot files found (0.20 pts): {screenshots_found}")
            total_score += 0.20
        elif n_shots == 1:
            print(f"PARTIAL: Component 1 — 1/3 screenshot files found (0.10 pts): {screenshots_found}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — no screenshot files found in {WORKDIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: language_comparison.odt exists and has exactly 1 table (0.15 points)
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        from odf.text import P

        if not os.path.isfile(ODT_PATH):
            print(f"FAIL: Component 2 — ODT file not found: {ODT_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {min(total_score, 1.0)}")
            return min(total_score, 1.0)

        doc = load(ODT_PATH)
        tables = doc.getElementsByType(Table)
        if len(tables) >= 1:
            print(f"PASS: Component 2 — language_comparison.odt exists and has {len(tables)} table(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — ODT file has no tables (found {len(tables)})")

    except Exception as e:
        print(f"ERROR: Component 2 — cannot load/parse ODT: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Extract all rows for subsequent components
    try:
        tables = doc.getElementsByType(Table)
        table = tables[0]
        rows = table.getElementsByType(TableRow)
        table_data = []
        for row in rows:
            cells = row.getElementsByType(TableCell)
            row_texts = [get_all_text(cell).strip() for cell in cells]
            table_data.append(row_texts)
    except Exception as e:
        print(f"ERROR: Could not extract table data: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 3: Table has correct header row (0.10 points)
    # Header row must contain Language, Version, Screenshot Path
    try:
        if len(table_data) >= 1:
            header_row = [cell.strip() for cell in table_data[0]]
            # Check that all three expected headers are present (case-insensitive)
            headers_lower = [h.lower() for h in header_row]
            expected_lower = [h.lower() for h in EXPECTED_HEADERS]
            if all(exp in headers_lower for exp in expected_lower):
                print(f"PASS: Component 3 — header row correct: {header_row} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — header row mismatch. Found: {header_row}, "
                      f"expected: {EXPECTED_HEADERS}")
        else:
            print(f"FAIL: Component 3 — table is empty (no rows)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Table has correct language/version data (0.30 points)
    # Check that Python/Ruby/Go rows have correct version numbers
    try:
        # Data rows are rows 1..3 (after header)
        data_rows = table_data[1:] if len(table_data) > 1 else []
        languages_found = {}
        for row in data_rows:
            if len(row) >= 2:
                lang = row[0].strip()
                version = row[1].strip()
                languages_found[lang.lower()] = version

        correct_count = 0
        for lang, expected_ver in EXPECTED_VERSIONS.items():
            found_ver = languages_found.get(lang)
            if found_ver == expected_ver:
                correct_count += 1
                print(f"PASS: Component 4 — {lang.capitalize()} version = '{found_ver}' (correct)")
            elif found_ver is not None:
                print(f"FAIL: Component 4 — {lang.capitalize()} version mismatch: "
                      f"found='{found_ver}', expected='{expected_ver}'")
            else:
                print(f"FAIL: Component 4 — {lang.capitalize()} row not found in table")

        if correct_count == 3:
            print(f"PASS: Component 4 — all 3 language/version entries correct (0.30 pts)")
            total_score += 0.30
        elif correct_count == 2:
            print(f"PARTIAL: Component 4 — 2/3 language/version entries correct (0.20 pts)")
            total_score += 0.20
        elif correct_count == 1:
            print(f"PARTIAL: Component 4 — 1/3 language/version entries correct (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — no correct language/version entries found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Table has correct screenshot paths (0.15 points)
    # Check that rows reference the correct screenshot paths
    try:
        data_rows = table_data[1:] if len(table_data) > 1 else []
        # Build expected language -> screenshot path mapping
        expected_screenshot_map = {
            'python': '/home/user/Desktop/screenshot_1.png',
            'ruby': '/home/user/Desktop/screenshot_2.png',
            'go': '/home/user/Desktop/screenshot_3.png',
        }
        correct_paths = 0
        for row in data_rows:
            if len(row) >= 3:
                lang = row[0].strip().lower()
                path = row[2].strip()
                expected_path = expected_screenshot_map.get(lang)
                if expected_path and path == expected_path:
                    correct_paths += 1
                    print(f"PASS: Component 5 — {lang} screenshot path = '{path}' (correct)")
                elif expected_path:
                    print(f"FAIL: Component 5 — {lang} screenshot path mismatch: "
                          f"found='{path}', expected='{expected_path}'")
                else:
                    print(f"INFO: Component 5 — unknown language '{lang}' in row, skipping path check")

        if correct_paths == 3:
            print(f"PASS: Component 5 — all 3 screenshot paths correct (0.15 pts)")
            total_score += 0.15
        elif correct_paths > 0:
            partial = round(0.05 * correct_paths, 2)
            print(f"PARTIAL: Component 5 — {correct_paths}/3 screenshot paths correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — no correct screenshot paths found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {round(final_score, 2)}")
    return final_score


verify_task()
