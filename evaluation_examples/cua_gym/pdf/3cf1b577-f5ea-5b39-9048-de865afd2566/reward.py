"""
Reward Script: Create a PDF with a formatted NLP benchmark table
Task ID: pdf_res_089
Domain: pdf
Scoring:
  Component 1 (0.2): Title text present in PDF
  Component 2 (0.2): Table exists with 5 columns and correct headers
  Component 3 (0.3): Table has at least 10 data rows
  Component 4 (0.3): Numeric columns contain plausible metric values
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_089'
FILE_PATH = os.path.join(WORKDIR, 'papers', 'supplementary_table.pdf')

EXPECTED_HEADERS = ['Rank', 'Method', 'BLEU', 'ROUGE-L', 'Human Eval']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have at least 1 page
    if doc.page_count < 1:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]
    text = page.get_text('text')

    # Component 1: Title text is present (0.2 points)
    # The PDF must contain "Supplementary Table S1: Full Benchmark Results"
    # This is a task-introduced change -- initial_env has no file at all.
    try:
        if 'Supplementary Table S1' in text and 'Benchmark Results' in text:
            print(f"PASS: Component 1 -- Title text found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Title text not found in page text")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Table exists with 5 columns and correct header names (0.2 points)
    # Extract tables from page 0
    try:
        tabs = page.find_tables()
        table_list = tabs.tables if hasattr(tabs, 'tables') else list(tabs)
        if len(table_list) == 0:
            print("FAIL: Component 2 -- No table found on page")
        else:
            # Use the first (or largest) table
            best_table = None
            best_rows = 0
            for t in table_list:
                rows = t.extract()
                if len(rows) > best_rows:
                    best_rows = len(rows)
                    best_table = rows

            if best_table is None or len(best_table) == 0:
                print("FAIL: Component 2 -- Table is empty")
            else:
                header_row = best_table[0]
                num_cols = len(header_row)
                # Check 5 columns
                if num_cols == 5:
                    # Check header names match expected (case-insensitive, strip whitespace)
                    headers_match = all(
                        actual.strip().lower() == expected.lower()
                        for actual, expected in zip(header_row, EXPECTED_HEADERS)
                    )
                    if headers_match:
                        print(f"PASS: Component 2 -- Table has 5 columns with correct headers: {header_row} (0.2 pts)")
                        total_score += 0.2
                    else:
                        print(f"FAIL: Component 2 -- Headers mismatch. Expected {EXPECTED_HEADERS}, got {header_row}")
                else:
                    print(f"FAIL: Component 2 -- Expected 5 columns, found {num_cols}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Table has at least 10 data rows (excluding header) (0.3 points)
    try:
        tabs = page.find_tables()
        table_list = tabs.tables if hasattr(tabs, 'tables') else list(tabs)
        best_table = None
        best_rows = 0
        for t in table_list:
            rows = t.extract()
            if len(rows) > best_rows:
                best_rows = len(rows)
                best_table = rows

        if best_table is not None:
            data_rows = best_table[1:]  # exclude header
            num_data_rows = len(data_rows)
            if num_data_rows >= 10:
                print(f"PASS: Component 3 -- Table has {num_data_rows} data rows (>= 10) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Only {num_data_rows} data rows, expected >= 10")
        else:
            print("FAIL: Component 3 -- No table found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Numeric columns contain plausible metric values (0.3 points)
    # BLEU (col 2): typically 0-100, ROUGE-L (col 3): typically 0-100,
    # Human Eval (col 4): typically 1-5 scale
    # Check that at least 8 out of 10 data rows have valid numeric values
    try:
        tabs = page.find_tables()
        table_list = tabs.tables if hasattr(tabs, 'tables') else list(tabs)
        best_table = None
        best_rows = 0
        for t in table_list:
            rows = t.extract()
            if len(rows) > best_rows:
                best_rows = len(rows)
                best_table = rows

        if best_table is not None and len(best_table) > 1:
            data_rows = best_table[1:]
            valid_rows = 0
            for row in data_rows:
                if len(row) >= 5:
                    try:
                        bleu = float(row[2])
                        rouge = float(row[3])
                        human_eval = float(row[4])
                        # Plausibility checks
                        if 0 <= bleu <= 100 and 0 <= rouge <= 100 and 0 <= human_eval <= 5.5:
                            valid_rows += 1
                    except (ValueError, TypeError):
                        pass
            if valid_rows >= 8:
                print(f"PASS: Component 4 -- {valid_rows}/{len(data_rows)} rows have plausible numeric values (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 -- Only {valid_rows}/{len(data_rows)} rows have plausible numeric values, need >= 8")
        else:
            print("FAIL: Component 4 -- No table data found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
