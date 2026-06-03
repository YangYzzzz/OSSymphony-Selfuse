"""
Reward Script: Add 10 LLM papers from arXiv cs.CL January 2024 to LibreOffice Calc
Task ID: osworld_multi_apps_arxiv_llms_calc_005
Domain: libreoffice_calc
Scoring:
  - Component 1 (0.5): At least 10 data rows present in the spreadsheet (rows 2-11+)
  - Component 2 (0.3): All data row arXiv IDs start with '2401.' (correct January 2024)
  - Component 3 (0.2): Titles contain LLM/language model/GPT/foundation model keywords
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_005'
FILE_PATH = f'{WORKDIR}/llm_jan2024.ods'

# Keywords to check in titles (case-insensitive)
LLM_KEYWORDS = [
    'llm', 'llms',
    'language model', 'language models',
    'gpt',
    'foundation model', 'foundation models',
    'large model',
    'conversational',
    'instruction tuning',
    'fine-tuning', 'finetuning',
    'unlearning',
    'vision-language',
    'multimodal',
    'mixture of experts',
]


def read_ods_rows(filepath):
    """
    Read rows from ODS file (actually XLSX format internally with inlineStr cells).
    Returns list of (arxiv_id, title, authors) tuples for data rows (row 2 onwards).
    Row 1 is the header row and is skipped.
    Returns None if file cannot be read.
    """
    try:
        with zipfile.ZipFile(filepath, 'r') as zf:
            with zf.open('xl/worksheets/sheet1.xml') as f:
                content = f.read().decode('utf-8')
    except Exception as e:
        print(f"ERROR: Cannot open file {filepath}: {e}")
        return None

    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"ERROR: Cannot parse XML: {e}")
        return None

    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    data_rows = []

    for row_elem in root.findall(f'.//{{{ns}}}row'):
        row_idx = int(row_elem.get('r', 0))
        # Skip header row (row 1)
        if row_idx < 2:
            continue

        row_cells = {}
        for cell in row_elem.findall(f'{{{ns}}}c'):
            cell_ref = cell.get('r', '')
            col = ''.join(c for c in cell_ref if c.isalpha())

            # Handle inlineStr type (t="inlineStr")
            cell_type = cell.get('t', '')
            if cell_type == 'inlineStr':
                is_elem = cell.find(f'{{{ns}}}is')
                if is_elem is not None:
                    t_elem = is_elem.find(f'{{{ns}}}t')
                    if t_elem is not None and t_elem.text:
                        row_cells[col] = t_elem.text
                    else:
                        row_cells[col] = ''
                else:
                    row_cells[col] = ''
            # Handle shared strings (t="s")
            elif cell_type == 's':
                v_elem = cell.find(f'{{{ns}}}v')
                row_cells[col] = v_elem.text if v_elem is not None else ''
            # Handle plain values
            else:
                v_elem = cell.find(f'{{{ns}}}v')
                row_cells[col] = v_elem.text if v_elem is not None else ''

        arxiv_id = row_cells.get('A', '').strip()
        title = row_cells.get('B', '').strip()
        authors = row_cells.get('C', '').strip()

        # Only count rows that have at least arXiv ID or title populated
        if arxiv_id or title:
            data_rows.append((arxiv_id, title, authors))

    return data_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read data rows
    data_rows = read_ods_rows(file_path)
    if data_rows is None:
        print("CRITICAL: Cannot read file content")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(data_rows)} data rows (excluding header)")
    for i, (arxiv_id, title, authors) in enumerate(data_rows[:5], 1):
        print(f"  Row {i}: [{arxiv_id}] {title[:60]}...")

    # Component 1: At least 10 data rows present (0.5 points)
    # This is the primary task - adding 10 papers as rows
    try:
        num_data_rows = len(data_rows)
        if num_data_rows >= 10:
            print(f"PASS: Component 1 — {num_data_rows} data rows found (need >= 10) (0.5 pts)")
            total_score += 0.5
        elif num_data_rows >= 5:
            # Partial credit: at least 5 rows
            partial = 0.25
            print(f"PARTIAL: Component 1 — {num_data_rows} data rows found (need >= 10), partial credit ({partial} pts)")
            total_score += partial
        elif num_data_rows >= 1:
            # Minimal partial credit: at least 1 row
            partial = 0.1
            print(f"PARTIAL: Component 1 — {num_data_rows} data rows found (need >= 10), minimal credit ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No data rows found, expected >= 10")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All data row arXiv IDs start with '2401.' (0.3 points)
    # This verifies papers are from January 2024 cs.CL listing as required
    try:
        if len(data_rows) >= 10:
            arxiv_ids = [row[0] for row in data_rows]
            valid_ids = [aid for aid in arxiv_ids if aid.startswith('2401.')]
            if len(valid_ids) >= 10:
                print(f"PASS: Component 2 — All {len(valid_ids)} arXiv IDs start with '2401.' (0.3 pts)")
                total_score += 0.3
            elif len(valid_ids) >= 5:
                partial = 0.15
                print(f"PARTIAL: Component 2 — {len(valid_ids)}/10 arXiv IDs start with '2401.', partial ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {len(valid_ids)}/10 arXiv IDs start with '2401.'")
                print(f"  Found IDs: {arxiv_ids[:5]}")
        else:
            print(f"SKIP: Component 2 — Insufficient data rows for arXiv ID check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Titles contain LLM/language model/GPT/foundation model keywords (0.2 points)
    # This verifies the papers are actually about large language models/foundation models
    try:
        if len(data_rows) >= 10:
            titles = [row[1].lower() for row in data_rows]
            matching_titles = 0
            for title in titles:
                if any(kw in title for kw in LLM_KEYWORDS):
                    matching_titles += 1

            ratio = matching_titles / len(titles)
            if matching_titles >= 8:
                print(f"PASS: Component 3 — {matching_titles}/{len(titles)} titles contain LLM keywords (0.2 pts)")
                total_score += 0.2
            elif matching_titles >= 5:
                partial = 0.1
                print(f"PARTIAL: Component 3 — {matching_titles}/{len(titles)} titles contain LLM keywords ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {matching_titles}/{len(titles)} titles contain LLM keywords")
                print(f"  Example titles: {[row[1][:50] for row in data_rows[:3]]}")
        else:
            print(f"SKIP: Component 3 — Insufficient data rows for keyword check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
