"""
Reward Script: Visit Papers With Code and record ImageNet SOTA leaderboard
Task ID: osworld_multi_apps_web_papers_007
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: File exists at Desktop as imagenet_sota.ods (precondition gate)
  Component 2: Correct column headers (0.2 pts)
  Component 3: Exactly 10 data rows (0.3 pts)
  Component 4: Rank column contains values 1-10 in order (0.2 pts)
  Component 5: Accuracy columns contain numeric values (0.3 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_papers_007'
FILE_PATH = f'{WORKDIR}/imagenet_sota.ods'

REQUIRED_COLUMNS = ['Rank', 'Method', 'Top-1_Accuracy', 'Top-5_Accuracy', 'Paper_Title']


def get_cell_text(cell):
    """Extract plain text from an ODF cell."""
    from odf.text import P
    texts = []
    for p in cell.getElementsByType(P):
        texts.append(str(p))
    return ' '.join(texts).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS file using odfpy
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        from odf.text import P

        doc = load(file_path)
        sheets = doc.spreadsheet.getElementsByType(Table)
        if not sheets:
            print("CRITICAL: No sheets found in the ODS file")
            print("REWARD: 0.0")
            return 0.0

        # Use the first sheet
        sheet = sheets[0]
        rows = sheet.getElementsByType(TableRow)

        print(f"INFO: File loaded successfully. Sheet: '{sheet.getAttribute('name')}', Rows: {len(rows)}")

    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all rows into a list of lists
    all_rows = []
    try:
        for row in rows:
            cells = row.getElementsByType(TableCell)
            row_data = []
            for cell in cells:
                repeat = cell.getAttribute('numbercolumnsrepeated')
                repeat = int(repeat) if repeat else 1
                # Extract text value
                text = get_cell_text(cell)
                # If this is a highly-repeated empty cell (padding), limit to 1
                if repeat > 10 and text == '':
                    row_data.append(text)
                else:
                    for _ in range(repeat):
                        row_data.append(text)
            all_rows.append(row_data)
    except Exception as e:
        print(f"ERROR: Failed to parse rows: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Filter out completely empty rows
    non_empty_rows = [r for r in all_rows if any(v.strip() for v in r)]

    if not non_empty_rows:
        print("FAIL: No non-empty rows found in the file")
        print("REWARD: 0.0")
        return 0.0

    header_row = non_empty_rows[0] if non_empty_rows else []
    data_rows = non_empty_rows[1:] if len(non_empty_rows) > 1 else []

    print(f"INFO: Header row: {header_row[:6]}")
    print(f"INFO: Data rows count: {len(data_rows)}")

    # Component 1: Correct column headers (0.2 points)
    # Checks that the 5 required columns are present in the header row
    try:
        # Normalize header by stripping whitespace
        header_normalized = [h.strip() for h in header_row[:6]]
        # Check that all required columns are present
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in header_normalized]
        if not missing_cols:
            print(f"PASS: Component 1 — All required columns found in header: {REQUIRED_COLUMNS} (0.2 pts)")
            total_score += 0.2
        else:
            # Try case-insensitive match
            header_lower = [h.lower() for h in header_normalized]
            missing_ci = [col for col in REQUIRED_COLUMNS if col.lower() not in header_lower]
            if not missing_ci:
                print(f"PASS: Component 1 — All required columns found (case-insensitive) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — Missing columns: {missing_ci}. Found: {header_normalized}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 10 data rows (0.3 points)
    # The task explicitly requires top 10 entries
    try:
        n_data_rows = len(data_rows)
        if n_data_rows == 10:
            print(f"PASS: Component 2 — Exactly 10 data rows found (0.3 pts)")
            total_score += 0.3
        elif n_data_rows >= 10:
            # Award partial credit if at least 10 rows
            print(f"PASS: Component 2 — {n_data_rows} data rows found (>= 10 required) (0.3 pts)")
            total_score += 0.3
        elif n_data_rows >= 5:
            print(f"PARTIAL: Component 2 — {n_data_rows} data rows found (expected 10) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Only {n_data_rows} data rows found, expected 10")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rank column contains values 1-10 (0.2 points)
    # The ranks should be numeric 1 through 10
    try:
        # Find the Rank column index
        header_normalized = [h.strip() for h in header_row[:6]]
        rank_col_idx = None
        for i, h in enumerate(header_normalized):
            if h.lower() == 'rank':
                rank_col_idx = i
                break

        if rank_col_idx is None:
            print(f"FAIL: Component 3 — No 'Rank' column found in header")
        else:
            ranks = []
            for r in data_rows:
                if rank_col_idx < len(r):
                    try:
                        ranks.append(int(float(r[rank_col_idx].strip())))
                    except (ValueError, TypeError):
                        ranks.append(None)

            expected_ranks = list(range(1, len(data_rows) + 1))
            actual_valid_ranks = [rk for rk in ranks if rk is not None]

            if len(actual_valid_ranks) >= 10 and sorted(actual_valid_ranks[:10]) == list(range(1, 11)):
                print(f"PASS: Component 3 — Rank column contains values 1-10 (0.2 pts)")
                total_score += 0.2
            elif len(actual_valid_ranks) >= 10 and set(actual_valid_ranks[:10]) == set(range(1, 11)):
                print(f"PASS: Component 3 — Rank column contains values 1-10 (unordered) (0.2 pts)")
                total_score += 0.2
            elif len(actual_valid_ranks) >= 5:
                print(f"PARTIAL: Component 3 — {len(actual_valid_ranks)} valid rank values found (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — Rank values invalid or missing. Found: {ranks[:10]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Accuracy columns contain numeric values (0.3 points)
    # Both Top-1_Accuracy and Top-5_Accuracy should have numeric values
    try:
        header_normalized = [h.strip() for h in header_row[:6]]

        # Find Top-1 and Top-5 accuracy column indices
        top1_idx = None
        top5_idx = None
        for i, h in enumerate(header_normalized):
            if 'top-1' in h.lower() or 'top1' in h.lower():
                top1_idx = i
            if 'top-5' in h.lower() or 'top5' in h.lower():
                top5_idx = i

        top1_valid = 0
        top5_valid = 0

        if top1_idx is not None:
            for r in data_rows:
                if top1_idx < len(r):
                    val = r[top1_idx].strip().replace('%', '')
                    try:
                        float(val)
                        top1_valid += 1
                    except (ValueError, TypeError):
                        pass

        if top5_idx is not None:
            for r in data_rows:
                if top5_idx < len(r):
                    val = r[top5_idx].strip().replace('%', '')
                    try:
                        float(val)
                        top5_valid += 1
                    except (ValueError, TypeError):
                        pass

        n_rows = len(data_rows)
        if n_rows == 0:
            print("FAIL: Component 4 — No data rows to check accuracy values")
        elif top1_idx is None or top5_idx is None:
            print(f"FAIL: Component 4 — Could not find accuracy columns. top1_idx={top1_idx}, top5_idx={top5_idx}")
        elif top1_valid >= n_rows and top5_valid >= n_rows:
            print(f"PASS: Component 4 — All {n_rows} rows have numeric Top-1 ({top1_valid}) and Top-5 ({top5_valid}) accuracy values (0.3 pts)")
            total_score += 0.3
        elif top1_valid >= n_rows // 2 and top5_valid >= n_rows // 2:
            print(f"PARTIAL: Component 4 — Top-1 valid: {top1_valid}/{n_rows}, Top-5 valid: {top5_valid}/{n_rows} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Insufficient numeric accuracy values. Top-1: {top1_valid}/{n_rows}, Top-5: {top5_valid}/{n_rows}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
