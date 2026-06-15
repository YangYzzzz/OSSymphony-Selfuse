"""
Reward Script: Verify isbn_tracker.ods is filled with ISBN-13 and OpenLibrary URLs
Task ID: osworld_multi_apps_web_references_007
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: All 10 books have a valid ISBN_13 value (0.60 pts, 0.06 per book)
  - Component 2: All 10 books have a valid OpenLibrary_URL (0.40 pts, 0.04 per book)
  Total: 1.0

Task: Open Writer doc with 10 CS books, look up ISBN-13 on OpenLibrary, fill in isbn_tracker.ods
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_007'
ODS_PATH = f'{WORKDIR}/Desktop/isbn_tracker.ods'

# Expected book titles (for reference / logging)
EXPECTED_TITLES = [
    'The Art of Computer Programming',
    'Introduction to Algorithms',
    'Design Patterns',
    'Structure and Interpretation of Computer Programs',
    'Clean Code',
    'The Pragmatic Programmer',
    'Code Complete',
    'Algorithms',
    'Computer Networks',
    'Operating System Concepts',
]

ISBN13_RE = re.compile(r'^97[89]\d{10}$')
OPENLIBRARY_URL_RE = re.compile(r'^https?://openlibrary\.org/.+', re.IGNORECASE)


def get_cell_text(cell):
    """Extract text content from an ODF cell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        val = ''
        for p in ps:
            if p.firstChild:
                val += str(p.firstChild)
        return val.strip()
    except Exception:
        return ''


def load_ods_data(path):
    """
    Load ODS spreadsheet and return list of dicts with Title, Author, ISBN_13, OpenLibrary_URL.
    Returns None if file cannot be loaded.
    """
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        from odf.namespaces import TABLENS

        doc = load(path)
        sheets = doc.spreadsheet.getElementsByType(Table)
        if not sheets:
            print("CRITICAL: No sheets found in ODS file")
            return None

        sheet = sheets[0]
        rows = sheet.getElementsByType(TableRow)

        if not rows:
            print("CRITICAL: No rows found in sheet")
            return None

        # Parse header row
        header_cells = rows[0].getElementsByType(TableCell)
        headers = []
        for cell in header_cells:
            text = get_cell_text(cell)
            repeat = cell.attributes.get((TABLENS, 'number-columns-repeated'), '1')
            count = int(repeat)
            for _ in range(min(count, 10)):
                headers.append(text)

        print(f"Headers: {headers}")

        # Find column indices
        try:
            title_idx = next(i for i, h in enumerate(headers) if 'title' in h.lower())
            author_idx = next(i for i, h in enumerate(headers) if 'author' in h.lower())
            isbn_idx = next(i for i, h in enumerate(headers) if 'isbn' in h.lower())
            url_idx = next(i for i, h in enumerate(headers) if 'url' in h.lower() or 'openlibrary' in h.lower())
        except StopIteration as e:
            print(f"CRITICAL: Cannot find required column header: {e}")
            return None

        records = []
        for row in rows[1:]:
            cells = row.getElementsByType(TableCell)
            row_vals = []
            for cell in cells:
                text = get_cell_text(cell)
                repeat = cell.attributes.get((TABLENS, 'number-columns-repeated'), '1')
                count = int(repeat)
                for _ in range(min(count, 10)):
                    row_vals.append(text)

            # Pad to required length
            while len(row_vals) <= max(title_idx, author_idx, isbn_idx, url_idx):
                row_vals.append('')

            title = row_vals[title_idx] if title_idx < len(row_vals) else ''
            author = row_vals[author_idx] if author_idx < len(row_vals) else ''
            isbn = row_vals[isbn_idx] if isbn_idx < len(row_vals) else ''
            url = row_vals[url_idx] if url_idx < len(row_vals) else ''

            if title or author:
                records.append({
                    'title': title,
                    'author': author,
                    'isbn_13': isbn,
                    'openlibrary_url': url,
                })

        return records

    except ImportError:
        print("CRITICAL: odfpy not available; cannot read ODS file")
        return None
    except Exception as e:
        print(f"CRITICAL: Failed to load ODS file: {e}")
        return None


def verify_task(ods_path):
    """
    Verify that isbn_tracker.ods has been filled in with valid ISBN-13 and OpenLibrary URLs.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(ods_path):
        print(f"CRITICAL: File not found: {ods_path}")
        print("REWARD: 0.0")
        return 0.0

    records = load_ods_data(ods_path)
    if records is None:
        print("CRITICAL: Could not parse ODS file")
        print("REWARD: 0.0")
        return 0.0

    print(f"\nFound {len(records)} data rows (expected 10)\n")

    # Ensure we have the expected 10 books
    if len(records) < 10:
        print(f"WARN: Only {len(records)} rows found, expected 10")

    # Component 1: Valid ISBN_13 values (0.06 pts per book, 0.6 total)
    # An ISBN-13 must be exactly 13 digits starting with 978 or 979
    isbn_score = 0.0
    isbn_per_book = 0.06
    print("=== Component 1: ISBN_13 validation (0.06 pts each, 0.60 total) ===")
    for i, rec in enumerate(records[:10]):
        isbn = rec['isbn_13'].strip().replace('-', '').replace(' ', '')
        title_short = rec['title'][:40] if rec['title'] else f'Row {i+1}'
        if ISBN13_RE.match(isbn):
            print(f"  PASS: [{i+1}] {title_short!r} → ISBN-13: {isbn}")
            isbn_score += isbn_per_book
        else:
            print(f"  FAIL: [{i+1}] {title_short!r} → ISBN-13 invalid or missing: {repr(rec['isbn_13'])}")

    print(f"  ISBN score: {isbn_score:.2f}/0.60\n")

    # Component 2: Valid OpenLibrary URLs (0.04 pts per book, 0.40 total)
    url_score = 0.0
    url_per_book = 0.04
    print("=== Component 2: OpenLibrary_URL validation (0.04 pts each, 0.40 total) ===")
    for i, rec in enumerate(records[:10]):
        url = rec['openlibrary_url'].strip()
        title_short = rec['title'][:40] if rec['title'] else f'Row {i+1}'
        if OPENLIBRARY_URL_RE.match(url):
            print(f"  PASS: [{i+1}] {title_short!r} → URL: {url}")
            url_score += url_per_book
        else:
            print(f"  FAIL: [{i+1}] {title_short!r} → URL invalid or missing: {repr(rec['openlibrary_url'])}")

    print(f"  URL score: {url_score:.2f}/0.40\n")

    total_score = isbn_score + url_score
    final_score = round(min(total_score, 1.0), 2)

    print(f"Score breakdown: ISBN={isbn_score:.2f} + URL={url_score:.2f} = {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: run verification against the canonical file path on the VM
if not os.path.exists(ODS_PATH):
    print(f"File not found: {ODS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ODS_PATH)
