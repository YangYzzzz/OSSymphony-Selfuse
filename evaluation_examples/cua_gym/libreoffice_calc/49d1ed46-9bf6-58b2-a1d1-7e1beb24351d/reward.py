"""
Reward Script: Export spreadsheet to CSV with pipe delimiters, double-quote text delimiters, ISO-8859-1 encoding
Task ID: calc_gsi_043
Domain: libreoffice_calc
Scoring:
  - Component 1: CSV file exists with correct name (0.15 pts)
  - Component 2: Pipe (|) field delimiter used correctly (0.30 pts)
  - Component 3: Double quotes as text delimiter on all fields (0.25 pts)
  - Component 4: Correct data content — 7 columns, header + 18 rows (0.20 pts)
  - Component 5: File is valid ISO-8859-1 encoding (0.10 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_043'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    csv_path = os.path.join(WORKDIR, f'{TASK_ID}.csv')

    # Precondition gate: CSV file must exist
    if not os.path.exists(csv_path):
        print(f"CRITICAL: CSV file not found at {csv_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read raw bytes for encoding and delimiter checks
    try:
        with open(csv_path, 'rb') as f:
            raw = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read CSV file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(raw) == 0:
        print("CRITICAL: CSV file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: CSV file exists and has substantial content (0.15 pts)
    # The file must have reasonable size (at least header + some data rows)
    try:
        # Decode as iso-8859-1 (always succeeds for any byte sequence, but we check content)
        text = raw.decode('iso-8859-1')
        # Split by common line endings
        if '\r\n' in text:
            lines = text.strip().split('\r\n')
        else:
            lines = text.strip().split('\n')

        if len(lines) >= 2:
            print(f"PASS: Component 1 — CSV file exists with {len(lines)} lines (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — CSV file has only {len(lines)} lines, expected at least 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Pipe (|) field delimiter used correctly (0.30 pts)
    # Every data line should use pipe as the field separator
    try:
        pipe_delimited_count = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            pipe_count = stripped.count('|')
            comma_count = stripped.count(',')
            # With 7 columns, we expect 6 pipe delimiters per line
            if pipe_count < 5:
                break
            pipe_delimited_count += 1
            # Check we're not using comma as delimiter (default CSV)
            # Commas might appear in data content, so check if pipe is the primary structure

        # Also check that the header line splits correctly by pipe
        header_fields = lines[0].split('|')

        if pipe_delimited_count == len(lines) and len(header_fields) >= 6:
            print(f"PASS: Component 2 — Pipe delimiter detected, header has {len(header_fields)} fields (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected pipe (|) delimiter with 7 fields. "
                  f"Pipe delimited lines: {pipe_delimited_count}/{len(lines)}, header fields by pipe: {len(header_fields)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Double quotes as text delimiter on all fields (0.25 pts)
    # Each field should be wrapped in double quotes
    try:
        quoted_line_count = 0
        checked_lines = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            fields = stripped.split('|')
            line_all_quoted = all(
                fld.strip().startswith('"') and fld.strip().endswith('"')
                for fld in fields
            )
            if not line_all_quoted:
                break
            quoted_line_count += 1
            checked_lines += 1

        if quoted_line_count == len(lines) and checked_lines >= 2:
            print(f"PASS: Component 3 — All fields in {checked_lines} lines are double-quoted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Not all fields are double-quoted. "
                  f"quoted_lines={quoted_line_count}/{len(lines)}, checked_lines={checked_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct data content — header + 18 data rows, 7 columns (0.20 pts)
    # Verify that the data was exported correctly
    try:
        expected_headers = ['Transaction ID', 'Date', 'Customer', 'Description', 'Amount', 'Category', 'Status']

        # Parse header
        header_fields = lines[0].split('|')
        # Strip quotes and whitespace
        parsed_headers = [f.strip().strip('"') for f in header_fields]

        headers_match = parsed_headers == expected_headers
        row_count_correct = len(lines) >= 19  # 1 header + 18 data rows
        col_count_correct = len(header_fields) == 7

        sub_score = 0.0
        if headers_match:
            sub_score += 0.10
        if row_count_correct and col_count_correct:
            sub_score += 0.10

        if sub_score > 0:
            print(f"PASS: Component 4 — headers_match={headers_match}, "
                  f"rows={len(lines)} (expected >=19), cols={len(header_fields)} (expected 7) ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 4 — headers_match={headers_match}, "
                  f"rows={len(lines)}, cols={len(header_fields)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: File is valid ISO-8859-1 encoded (not UTF-8 BOM) (0.10 pts)
    # Check that there is no UTF-8 BOM and the file is decodable as ISO-8859-1
    try:
        has_utf8_bom = raw[:3] == b'\xef\xbb\xbf'
        has_utf16_bom = raw[:2] in (b'\xff\xfe', b'\xfe\xff')

        # ISO-8859-1 can decode any byte, so we check for absence of UTF markers
        # and verify the content is valid when decoded as ISO-8859-1
        is_valid_iso = not has_utf8_bom and not has_utf16_bom

        # Also verify content makes sense when decoded as ISO-8859-1
        decoded = raw.decode('iso-8859-1')
        content_valid = 'Transaction ID' in decoded

        if is_valid_iso and content_valid:
            print(f"PASS: Component 5 — No BOM markers, valid ISO-8859-1 encoding (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — UTF-8 BOM: {has_utf8_bom}, UTF-16 BOM: {has_utf16_bom}, "
                  f"content_valid: {content_valid}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
