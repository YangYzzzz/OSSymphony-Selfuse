"""
Reward Script: Create acl2023_llm_papers.ods with LLM papers from ACL 2023
Task ID: osworld_multi_apps_web_papers_006
Domain: libreoffice_calc
Scoring:
  Component 1: File 'acl2023_llm_papers.ods' exists in Documents (0.2 pts)
  Component 2: Correct header columns (Title, Authors, Anthology_URL) (0.2 pts)
  Component 3: At least 8 data rows present (0.3 pts)
  Component 4: Papers are LLM-related from ACL 2023 (URL and title checks) (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_006'
FILE_PATH = '/home/user/Documents/acl2023_llm_papers.ods'


def get_cell_text(cell):
    """Extract text from an ODF TableCell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        return ' '.join([str(p) for p in ps]) if ps else ''
    except Exception:
        return ''


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists at correct location (0.2 points)
    # This FAILS on initial_env (no file), PASSES on golden_env (file created)
    try:
        file_exists = os.path.exists(file_path)
        if file_exists:
            print(f"PASS: Component 1 — File exists at {file_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — File not found at {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Load the ODS file using odfpy
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except ImportError:
        print("CRITICAL: odfpy not available — cannot parse .ods file")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Get the first (and expected only) sheet
    try:
        sheets = doc.spreadsheet.getElementsByType(Table)
        if len(sheets) == 0:
            print("FAIL: No sheets found in ODS file")
            print(f"REWARD: {total_score}")
            return total_score
        ws = sheets[0]
        rows = ws.getElementsByType(TableRow)
        print(f"INFO: Sheet name: '{ws.getAttribute('name')}', Row count: {len(rows)}")
    except Exception as e:
        print(f"CRITICAL: Cannot access sheet structure: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct header columns (Title, Authors, Anthology_URL) (0.2 points)
    # This FAILS on initial_env (no file), PASSES on golden_env
    try:
        if len(rows) == 0:
            print("FAIL: Component 2 — No rows found in sheet")
        else:
            from odf.table import TableCell
            header_row = rows[0]
            header_cells = header_row.getElementsByType(TableCell)
            header_values = [get_cell_text(cell).strip() for cell in header_cells]

            expected_headers = ['Title', 'Authors', 'Anthology_URL']
            # Check if all expected headers are present (case-insensitive comparison)
            header_values_lower = [h.lower() for h in header_values]
            headers_found = all(h.lower() in header_values_lower for h in expected_headers)

            if headers_found:
                print(f"PASS: Component 2 — Headers correct: {header_values[:3]} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected headers {expected_headers}, found: {header_values[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: At least 8 data rows (0.3 points)
    # This FAILS on initial_env (no file), PASSES on golden_env (8 paper rows)
    try:
        data_rows = rows[1:]  # skip header
        num_data_rows = len(data_rows)

        # Count non-empty rows (rows with at least one non-empty cell)
        non_empty_count = 0
        for row in data_rows:
            cells = row.getElementsByType(TableCell)
            row_texts = [get_cell_text(c).strip() for c in cells]
            if any(t for t in row_texts):
                non_empty_count += 1

        if non_empty_count >= 8:
            print(f"PASS: Component 3 — Found {non_empty_count} non-empty data rows (>= 8 required) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Only {non_empty_count} non-empty data rows, need at least 8")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Papers are LLM-related from ACL 2023 (0.3 points)
    # Check that URLs contain 'aclanthology.org/2023' and titles contain LLM-related keywords
    # This FAILS on initial_env (no file), PASSES on golden_env
    try:
        llm_keywords = [
            'large language model', 'llm', 'language model', 'gpt', 'chatgpt',
            'instruction tuning', 'in-context learning', 'prompt', 'foundation model'
        ]
        acl2023_url_pattern = 'aclanthology.org/2023'

        llm_paper_count = 0
        valid_url_count = 0

        for row in data_rows:
            cells = row.getElementsByType(TableCell)
            cell_texts = [get_cell_text(c).strip() for c in cells]

            if len(cell_texts) < 3 or not any(cell_texts):
                continue

            title = cell_texts[0].lower() if len(cell_texts) > 0 else ''
            url = cell_texts[2] if len(cell_texts) > 2 else ''

            # Check URL is from ACL 2023 anthology
            if acl2023_url_pattern in url:
                valid_url_count += 1

            # Check title contains LLM-related keyword
            if any(kw in title for kw in llm_keywords):
                llm_paper_count += 1

        # Require at least 6 out of 8 papers to have valid ACL 2023 URLs and LLM-related titles
        url_ok = valid_url_count >= 6
        llm_ok = llm_paper_count >= 6

        if url_ok and llm_ok:
            print(f"PASS: Component 4 — {valid_url_count} valid ACL 2023 URLs, {llm_paper_count} LLM-related titles (0.3 pts)")
            total_score += 0.3
        else:
            if not url_ok:
                print(f"FAIL: Component 4 — Only {valid_url_count}/8 papers have valid ACL 2023 Anthology URLs (need >= 6)")
            if not llm_ok:
                print(f"FAIL: Component 4 — Only {llm_paper_count}/8 papers have LLM-related titles (need >= 6)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Main entry point
if not os.path.exists(FILE_PATH):
    print(f"FAIL: Component 1 — File not found at {FILE_PATH}")
    print("\nScore: 0.0/1.0")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
