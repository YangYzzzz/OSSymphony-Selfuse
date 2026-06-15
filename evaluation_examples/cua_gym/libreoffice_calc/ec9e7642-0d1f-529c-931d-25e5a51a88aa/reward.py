"""
Reward Script: Search Semantic Scholar for RAG papers and record in Calc file
Task ID: osworld_multi_apps_web_papers_010
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: File exists at Desktop/rag_papers.ods with required columns (0.25)
  Component 2: Has exactly 8 data rows (0.25)
  Component 3: Citation_Count column is numeric and sorted descending (0.25)
  Component 4: File content is RAG-related (title keywords check) (0.25)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
FILE_PATH = '/home/user/Desktop/rag_papers.ods'

REQUIRED_COLUMNS = ['Title', 'Authors', 'Year', 'Venue', 'Citation_Count', 'Semantic_Scholar_URL']
REQUIRED_ROW_COUNT = 8  # data rows excluding header

# RAG-related keywords that should appear in paper titles
RAG_KEYWORDS = [
    'retrieval', 'augmented', 'generation', 'rag', 'dense retrieval',
    'language model', 'retrieve', 'knowledge'
]


def parse_ods(file_path):
    """
    Parse an ODS file using zipfile + xml.etree.ElementTree (stdlib only).
    Returns a list of rows, where each row is a list of cell string values.
    """
    NS = {
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    }
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    # Navigate to the first sheet
    body = root.find('office:body', NS)
    spreadsheet = body.find('office:spreadsheet', NS)
    table = spreadsheet.find('table:table', NS)

    rows = []
    for tr in table.findall('table:table-row', NS):
        row = []
        for tc in tr.findall('table:table-cell', NS):
            # Get text value from <text:p> child elements
            texts = tc.findall('text:p', NS)
            if texts:
                val = ''.join(t.text or '' for t in texts)
            else:
                val = ''
            row.append(val)
        # Trim trailing empty cells
        while row and row[-1] == '':
            row.pop()
        if row:  # skip completely empty rows
            rows.append(row)
    return rows


def verify_task(file_path):
    """
    Verify that the rag_papers.ods file satisfies task requirements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse file
    try:
        rows = parse_ods(file_path)
        print(f"INFO: Parsed {len(rows)} rows (including header)")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) == 0:
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: Correct column headers (0.25 points) ---
    # The file must have the required columns in the header row
    try:
        header = rows[0]
        print(f"INFO: Header row: {header}")
        # Check all required columns are present (case-sensitive, exact match)
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in header]
        if not missing_cols:
            print(f"PASS: Component 1 — All required columns present: {REQUIRED_COLUMNS} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Missing columns: {missing_cols}. Found: {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Has exactly 8 data rows (0.25 points) ---
    # data rows = total rows minus header
    try:
        data_rows = rows[1:]  # exclude header
        actual_count = len(data_rows)
        if actual_count == REQUIRED_ROW_COUNT:
            print(f"PASS: Component 2 — Exactly {REQUIRED_ROW_COUNT} data rows found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected {REQUIRED_ROW_COUNT} data rows, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Citation_Count column is numeric and sorted descending (0.25 points) ---
    # Citation counts must be integers, and sorted largest first
    try:
        header = rows[0]
        if 'Citation_Count' in header:
            citation_col_idx = header.index('Citation_Count')
            data_rows = rows[1:]
            citation_vals = []
            for row in data_rows:
                if citation_col_idx < len(row):
                    raw = row[citation_col_idx].strip()
                    # Accept float strings like '12800.0' or int strings like '12800'
                    try:
                        citation_vals.append(float(raw))
                    except ValueError:
                        citation_vals.append(None)
                else:
                    citation_vals.append(None)

            all_numeric = all(v is not None for v in citation_vals)
            if all_numeric and len(citation_vals) > 0:
                # Check descending order
                is_sorted_desc = all(
                    citation_vals[i] >= citation_vals[i + 1]
                    for i in range(len(citation_vals) - 1)
                )
                if is_sorted_desc:
                    print(f"PASS: Component 3 — Citation_Count is numeric and sorted descending: {[int(v) for v in citation_vals]} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — Citation_Count is numeric but NOT sorted descending: {citation_vals}")
            else:
                print(f"FAIL: Component 3 — Some Citation_Count values are non-numeric: {citation_vals}")
        else:
            print(f"FAIL: Component 3 — No 'Citation_Count' column in header: {header}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Content is RAG-related (0.25 points) ---
    # At least 6 of the 8 paper titles must contain RAG-related keywords
    try:
        header = rows[0]
        if 'Title' in header:
            title_col_idx = header.index('Title')
            data_rows = rows[1:]
            rag_count = 0
            for row in data_rows:
                if title_col_idx < len(row):
                    title_lower = row[title_col_idx].lower()
                    if any(kw in title_lower for kw in RAG_KEYWORDS):
                        rag_count += 1
            # At least 6 out of 8 papers should mention RAG-related concepts
            rag_threshold = 6
            if rag_count >= rag_threshold:
                print(f"PASS: Component 4 — {rag_count}/{len(data_rows)} paper titles contain RAG-related keywords (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Only {rag_count}/{len(data_rows)} paper titles contain RAG-related keywords (need >= {rag_threshold})")
        else:
            print(f"FAIL: Component 4 — No 'Title' column in header: {header}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the rag_papers.ods file
verify_task(FILE_PATH)
