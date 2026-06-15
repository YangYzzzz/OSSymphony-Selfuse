"""
Reward Script: Create a summary PDF listing metadata of 10 source PDFs
Task ID: pdf_pw_045
Domain: pdf
Scoring:
  Component 1 (0.20): Table with correct 6-column header row
  Component 2 (0.30): All 10 source filenames present in table
  Component 3 (0.25): Author and page count values match source metadata
  Component 4 (0.25): File size and creation date values present for all files
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_045'
REPORT_PATH = os.path.join(WORKDIR, 'reports', 'metadata_report.pdf')
SOURCE_DIR = os.path.join(WORKDIR, 'reports', 'source_docs')

# Expected column headers
EXPECTED_HEADERS = ['Filename', 'Title', 'Author', 'Pages', 'File Size', 'Creation Date']


def get_source_metadata():
    """Read actual metadata from all source PDFs."""
    metadata = {}
    if not os.path.isdir(SOURCE_DIR):
        return metadata
    for fname in sorted(os.listdir(SOURCE_DIR)):
        if not fname.lower().endswith('.pdf'):
            continue
        fpath = os.path.join(SOURCE_DIR, fname)
        try:
            doc = pymupdf.open(fpath)
            meta = doc.metadata
            info = {
                'title': meta.get('title', ''),
                'author': meta.get('author', ''),
                'pages': doc.page_count,
                'size': os.path.getsize(fpath),
                'creationDate': meta.get('creationDate', ''),
            }
            doc.close()
            metadata[fname] = info
        except Exception:
            pass
    return metadata


def extract_all_text(pdf_path):
    """Extract full text from the report PDF."""
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text('text')
    doc.close()
    return full_text


def extract_table_rows(pdf_path):
    """Extract table rows from the report PDF using find_tables."""
    doc = pymupdf.open(pdf_path)
    all_rows = []
    for page in doc:
        tables = page.find_tables()
        for table in tables:
            rows = table.extract()
            all_rows.extend(rows)
    doc.close()
    return all_rows


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: report file must exist
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found: {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: must be a valid PDF
    try:
        doc = pymupdf.open(REPORT_PATH)
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot open report PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read source metadata for verification
    source_meta = get_source_metadata()
    if len(source_meta) == 0:
        print("CRITICAL: Cannot read source PDFs for comparison")
        print("REWARD: 0.0")
        return 0.0

    source_filenames = sorted(source_meta.keys())
    print(f"INFO: Found {len(source_meta)} source PDFs to verify against")

    # Extract table data from report
    try:
        table_rows = extract_table_rows(REPORT_PATH)
    except Exception as e:
        print(f"ERROR: Failed to extract tables: {e}")
        table_rows = []

    # Also extract full text as fallback
    try:
        full_text = extract_all_text(REPORT_PATH)
    except Exception as e:
        print(f"ERROR: Failed to extract text: {e}")
        full_text = ""

    # Component 1: Table with correct 6-column header row (0.20 points)
    try:
        header_ok = 0  # 1 if header passes, 0 otherwise
        if len(table_rows) > 0:
            header_row = table_rows[0]
            # Clean header cells
            clean_headers = [str(c).strip().replace('\n', ' ') if c else '' for c in header_row]
            # Check that all expected headers are present (case-insensitive)
            matched_headers = 0
            for expected in EXPECTED_HEADERS:
                for actual in clean_headers:
                    if expected.lower() in actual.lower():
                        matched_headers += 1
                        break
            if matched_headers >= 5 and len(clean_headers) >= 5:
                header_ok = 1
                print(f"PASS: Component 1 -- Table header found with {matched_headers}/6 expected columns (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- Only {matched_headers}/6 expected headers found in {clean_headers}")
        else:
            # Fallback: check if headers appear in text
            headers_in_text = sum(1 for h in EXPECTED_HEADERS if h.lower() in full_text.lower())
            if headers_in_text >= 5:
                header_ok = 1
                print(f"PASS: Component 1 -- Headers found in text ({headers_in_text}/6) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- Only {headers_in_text}/6 headers found in text")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 10 source filenames present in table/text (0.30 points)
    try:
        filenames_found = 0
        for fname in source_filenames:
            # Check in table rows (filenames may have underscores replaced or be split across lines)
            fname_base = fname.replace('.pdf', '').replace('_', ' ')
            match_count = 0
            for row in table_rows[1:] if len(table_rows) > 1 else []:
                row_text = ' '.join(str(c).replace('\n', ' ') if c else '' for c in row)
                if fname in row_text or fname_base.lower() in row_text.lower():
                    match_count = 1
                    break
            # Fallback: check in full text
            if match_count == 0:
                fname_no_ext = fname.replace('.pdf', '')
                if fname_no_ext in full_text or fname in full_text:
                    match_count = 1
            filenames_found += match_count

        if filenames_found == 10:
            print(f"PASS: Component 2 -- All 10 source filenames found in report (0.30 pts)")
            total_score += 0.30
        elif filenames_found >= 7:
            partial = round(0.30 * filenames_found / 10, 2)
            print(f"PARTIAL: Component 2 -- {filenames_found}/10 filenames found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Only {filenames_found}/10 filenames found in report")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Author and page count values match source metadata (0.25 points)
    try:
        matches = 0
        total_checks = 0
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        for fname, meta in source_meta.items():
            expected_author = meta['author']
            expected_pages = str(meta['pages'])
            fname_base = fname.replace('.pdf', '').replace('_', ' ')

            # Find the matching row
            for row in data_rows:
                row_text = ' '.join(str(c).replace('\n', ' ') if c else '' for c in row)
                if fname.replace('.pdf', '').replace('_', ' ').lower() in row_text.lower() or fname in row_text:
                    # Check author
                    total_checks += 1
                    if expected_author.lower() in row_text.lower():
                        matches += 1
                    # Check page count
                    total_checks += 1
                    if expected_pages in row_text:
                        matches += 1
                    break

        if total_checks > 0:
            ratio = matches / total_checks
            if ratio >= 0.9:
                print(f"PASS: Component 3 -- {matches}/{total_checks} author/page checks match (0.25 pts)")
                total_score += 0.25
            elif ratio >= 0.5:
                partial = round(0.25 * ratio, 2)
                print(f"PARTIAL: Component 3 -- {matches}/{total_checks} author/page checks match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Only {matches}/{total_checks} author/page checks match")
        else:
            # Fallback: check in full text
            text_matches = 0
            for fname, meta in source_meta.items():
                if meta['author'] in full_text:
                    text_matches += 1
            if text_matches >= 8:
                print(f"PASS: Component 3 -- {text_matches}/10 authors found in text (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Only {text_matches}/10 authors found in text")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: File size and creation date values present (0.25 points)
    try:
        size_found = 0
        date_found = 0

        for fname, meta in source_meta.items():
            raw_size = meta['size']
            # The report likely shows human-readable size (e.g., "2.7 KB")
            # Check if any reasonable representation of the size is in the text
            size_kb = raw_size / 1024
            # Possible formats: "2.7 KB", "2753", "2.69 KB", etc.
            size_representations = [
                f"{size_kb:.1f}",  # e.g., "2.7"
                f"{size_kb:.0f}",  # e.g., "3"
                str(raw_size),      # raw bytes
            ]

            fname_base = fname.replace('.pdf', '').replace('_', ' ')
            # Find matching row in table
            matched_row_text = ""
            for row in data_rows:
                row_text = ' '.join(str(c).replace('\n', ' ') if c else '' for c in row)
                if fname_base.lower() in row_text.lower() or fname in row_text:
                    matched_row_text = row_text
                    break

            if not matched_row_text:
                continue

            # Check file size
            for sr in size_representations:
                if sr in matched_row_text:
                    size_found += 1
                    break

            # Check creation date: could be in various formats
            raw_date = meta['creationDate']  # e.g., "D:20250228170000"
            if raw_date.startswith('D:'):
                date_str = raw_date[2:]
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                # Check for date representations like "2025-02-28", "02/28/2025", "2025", etc.
                date_formats = [
                    f"{year}-{month}-{day}",
                    f"{month}/{day}/{year}",
                    f"{month}-{day}-{year}",
                    f"{year}/{month}/{day}",
                ]
                for df in date_formats:
                    if df in matched_row_text:
                        date_found += 1
                        break

        total_items = len(source_meta)
        size_ratio = size_found / total_items if total_items > 0 else 0
        date_ratio = date_found / total_items if total_items > 0 else 0
        combined_ratio = (size_ratio + date_ratio) / 2

        if combined_ratio >= 0.8:
            print(f"PASS: Component 4 -- Sizes: {size_found}/{total_items}, Dates: {date_found}/{total_items} (0.25 pts)")
            total_score += 0.25
        elif combined_ratio >= 0.4:
            partial = round(0.25 * combined_ratio, 2)
            print(f"PARTIAL: Component 4 -- Sizes: {size_found}/{total_items}, Dates: {date_found}/{total_items} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Sizes: {size_found}/{total_items}, Dates: {date_found}/{total_items}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
