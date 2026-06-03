"""
Reward Script: Fill in DOI, Citation_Count, and SS_URL for 7 arXiv papers in lab_refs.ods
Task ID: osworld_multi_apps_web_references_008
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: DOI column filled with valid DOI strings for all 7 papers (0.4 pts)
  - Component 2: Citation_Count column filled with non-empty numeric values for all 7 papers (0.3 pts)
  - Component 3: SS_URL column filled with Semantic Scholar URLs for all 7 papers (0.3 pts)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_references_008'
FILE_PATH = f'{WORKDIR}/lab_refs.ods'

# Expected arXiv IDs (row index -> arXiv ID)
EXPECTED_ARXIV_IDS = [
    '1706.03762',  # Attention Is All You Need
    '1810.04805',  # BERT
    '2005.14165',  # GPT-3
    '2010.11929',  # ViT
    '1512.03385',  # ResNet
    '1406.2661',   # GAN
    '1511.06434',  # DCGAN
]

# Expected DOIs (stable identifiers — should match exactly)
EXPECTED_DOIS = {
    '1706.03762': '10.48550/arXiv.1706.03762',
    '1810.04805': '10.18653/v1/N19-1423',
    '2005.14165': '10.48550/arXiv.2005.14165',
    '2010.11929': '10.48550/arXiv.2010.11929',
    '1512.03385': '10.1109/CVPR.2016.90',
    '1406.2661':  '10.48550/arXiv.1406.2661',
    '1511.06434': '10.48550/arXiv.1511.06434',
}


def get_cell_text(cell):
    """Extract text from an ODF table cell."""
    try:
        import odf.text
        paras = cell.getElementsByType(odf.text.P)
        if paras and paras[0].firstChild:
            return str(paras[0].firstChild.data).strip()
        return ''
    except Exception:
        return ''


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS file
    try:
        import odf.opendocument
        import odf.table
        import odf.text
        doc = odf.opendocument.load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the first sheet (References)
    try:
        sheets = doc.spreadsheet.getElementsByType(odf.table.Table)
        if not sheets:
            print("CRITICAL: No sheets found in the ODS file")
            print("REWARD: 0.0")
            return 0.0
        ws = sheets[0]
        rows = ws.getElementsByType(odf.table.TableRow)
    except Exception as e:
        print(f"CRITICAL: Cannot access sheet data: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all data rows (skip header row 0)
    # Columns: Title(0), arXiv_ID(1), DOI(2), Citation_Count(3), SS_URL(4)
    data_rows = []
    try:
        for i, row in enumerate(rows):
            if i == 0:
                continue  # skip header
            cells = row.getElementsByType(odf.table.TableCell)
            row_data = [get_cell_text(c) for c in cells]
            # Pad to at least 5 columns
            while len(row_data) < 5:
                row_data.append('')
            data_rows.append(row_data)
    except Exception as e:
        print(f"CRITICAL: Cannot parse rows: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify we have 7 data rows
    if len(data_rows) < 7:
        print(f"FAIL: Expected 7 data rows, found {len(data_rows)}")
        print("REWARD: 0.0")
        return 0.0

    # Build a mapping from arXiv ID -> row data for easier lookup
    arxiv_to_row = {}
    for row in data_rows:
        arxiv_id = row[1].strip() if len(row) > 1 else ''
        if arxiv_id:
            arxiv_to_row[arxiv_id] = row

    # -----------------------------------------------------------------
    # Component 1: DOI column filled with valid DOIs for all 7 papers (0.4 points)
    # Verifies that each paper has a non-empty DOI that matches the expected value
    # (DOIs are stable identifiers, so exact matching is appropriate)
    # -----------------------------------------------------------------
    try:
        doi_pass_count = 0
        doi_total = 0
        for arxiv_id, expected_doi in EXPECTED_DOIS.items():
            doi_total += 1
            row = arxiv_to_row.get(arxiv_id)
            if row is None:
                print(f"FAIL: DOI check — arXiv ID {arxiv_id} not found in file")
                continue
            actual_doi = row[2].strip() if len(row) > 2 else ''
            if actual_doi == expected_doi:
                doi_pass_count += 1
                print(f"PASS: DOI for {arxiv_id}: '{actual_doi}'")
            else:
                print(f"FAIL: DOI for {arxiv_id}: expected '{expected_doi}', found '{actual_doi}'")

        if doi_pass_count == doi_total:
            print(f"PASS: Component 1 — All {doi_total} DOIs correct (0.4 pts)")
            total_score += 0.4
        elif doi_pass_count >= 5:
            # Partial credit: at least 5/7 DOIs correct
            partial = round(0.4 * doi_pass_count / doi_total, 4)
            print(f"PARTIAL: Component 1 — {doi_pass_count}/{doi_total} DOIs correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {doi_pass_count}/{doi_total} DOIs correct (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 (DOI check) — {e}")

    # -----------------------------------------------------------------
    # Component 2: Citation_Count column filled with numeric values for all 7 papers (0.3 points)
    # Citation counts change over time, so we verify they are non-empty integers > 0
    # -----------------------------------------------------------------
    try:
        citation_pass_count = 0
        citation_total = 0
        for arxiv_id in EXPECTED_ARXIV_IDS:
            citation_total += 1
            row = arxiv_to_row.get(arxiv_id)
            if row is None:
                print(f"FAIL: Citation check — arXiv ID {arxiv_id} not found in file")
                continue
            actual_count = row[3].strip() if len(row) > 3 else ''
            if actual_count:
                try:
                    count_val = int(float(actual_count.replace(',', '')))
                    if count_val > 0:
                        citation_pass_count += 1
                        print(f"PASS: Citation_Count for {arxiv_id}: {count_val}")
                    else:
                        print(f"FAIL: Citation_Count for {arxiv_id}: value is 0 or negative: {actual_count}")
                except (ValueError, TypeError):
                    print(f"FAIL: Citation_Count for {arxiv_id}: non-numeric value: '{actual_count}'")
            else:
                print(f"FAIL: Citation_Count for {arxiv_id}: empty")

        if citation_pass_count == citation_total:
            print(f"PASS: Component 2 — All {citation_total} citation counts filled (0.3 pts)")
            total_score += 0.3
        elif citation_pass_count > 0:
            partial = round(0.3 * citation_pass_count / citation_total, 4)
            print(f"PARTIAL: Component 2 — {citation_pass_count}/{citation_total} citation counts filled ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No citation counts filled (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 (Citation_Count check) — {e}")

    # -----------------------------------------------------------------
    # Component 3: SS_URL column filled with Semantic Scholar URLs for all 7 papers (0.3 points)
    # Verifies that each paper has a non-empty URL pointing to semanticscholar.org
    # -----------------------------------------------------------------
    try:
        url_pass_count = 0
        url_total = 0
        for arxiv_id in EXPECTED_ARXIV_IDS:
            url_total += 1
            row = arxiv_to_row.get(arxiv_id)
            if row is None:
                print(f"FAIL: SS_URL check — arXiv ID {arxiv_id} not found in file")
                continue
            actual_url = row[4].strip() if len(row) > 4 else ''
            if actual_url and 'semanticscholar.org' in actual_url:
                url_pass_count += 1
                print(f"PASS: SS_URL for {arxiv_id}: '{actual_url}'")
            elif actual_url:
                print(f"FAIL: SS_URL for {arxiv_id}: URL does not point to semanticscholar.org: '{actual_url}'")
            else:
                print(f"FAIL: SS_URL for {arxiv_id}: empty")

        if url_pass_count == url_total:
            print(f"PASS: Component 3 — All {url_total} SS_URLs filled (0.3 pts)")
            total_score += 0.3
        elif url_pass_count > 0:
            partial = round(0.3 * url_pass_count / url_total, 4)
            print(f"PARTIAL: Component 3 — {url_pass_count}/{url_total} SS_URLs filled ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No SS_URLs filled (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 (SS_URL check) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {round(final_score, 4)}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
