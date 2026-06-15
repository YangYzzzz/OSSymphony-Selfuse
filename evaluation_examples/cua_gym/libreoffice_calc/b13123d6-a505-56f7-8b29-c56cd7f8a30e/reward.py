"""
Reward Script: Fill DOI column for 6 ML papers in missing_dois.ods
Task ID: osworld_multi_apps_web_references_005
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: 3 or more DOI cells filled with valid DOI format (0.5 pts)
  - Component 2: All 6 DOI cells filled with valid DOI format (0.5 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
FILE_NAME = 'missing_dois.ods'
FILE_PATH = os.path.join(WORKDIR, FILE_NAME)

# Expected DOI patterns from CrossRef for these 6 papers
# These are the specific DOIs as verified in the golden state
EXPECTED_DOIS = {
    'Playing Atari with Deep Reinforcement Learning': '10.48550/arXiv.1312.5602',
    'Generative Adversarial Networks': '10.48550/arXiv.1406.2661',
    'Dropout': '10.5555/2627435.2670313',
    'Adam': '10.48550/arXiv.1412.6980',
    'Batch Normalization': '10.48550/arXiv.1502.03167',
    'ImageNet Classification': '10.1145/3065386',
}

def is_valid_doi(doi_str):
    """Check if a string looks like a valid DOI (starts with 10. followed by registrant/suffix)."""
    if not doi_str or not isinstance(doi_str, str):
        return False
    doi_str = doi_str.strip()
    # DOIs start with '10.' followed by registrant code and slash
    return bool(re.match(r'^10\.\d{4,}/', doi_str))

def read_ods_dois(file_path):
    """Read the DOI column from the ODS file, returns list of (title, doi) tuples."""
    import odf.opendocument
    import odf.table
    import odf.text

    doc = odf.opendocument.load(file_path)
    sheets = doc.spreadsheet.getElementsByType(odf.table.Table)
    if not sheets:
        raise ValueError("No sheets found in ODS file")

    sheet = sheets[0]
    rows = sheet.getElementsByType(odf.table.TableRow)

    results = []
    for i, row in enumerate(rows):
        if i == 0:
            continue  # Skip header row
        cells = row.getElementsByType(odf.table.TableCell)
        row_data = []
        for cell in cells:
            texts = cell.getElementsByType(odf.text.P)
            cell_text = ""
            for t in texts:
                if t.firstChild:
                    cell_text += str(t.firstChild)
            row_data.append(cell_text)

        # Ensure row has at least 5 columns (Title=0, Authors=1, Year=2, Venue=3, DOI=4)
        while len(row_data) < 5:
            row_data.append("")

        title = row_data[0] if row_data else ""
        doi = row_data[4] if len(row_data) > 4 else ""
        results.append((title, doi))

    return results


def verify_task(file_path):
    """
    Verify task completion: DOI column filled for all 6 ML papers.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        rows = read_ods_dois(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not rows:
        print("CRITICAL: No data rows found in file")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(rows)} data rows in the file")

    # Count DOIs that are valid
    valid_dois = []
    invalid_dois = []

    for title, doi in rows:
        doi_stripped = doi.strip() if doi else ""
        if is_valid_doi(doi_stripped):
            valid_dois.append((title, doi_stripped))
            print(f"PASS: Valid DOI found for '{title[:50]}': {doi_stripped}")
        else:
            invalid_dois.append((title, doi_stripped))
            print(f"FAIL: Missing/invalid DOI for '{title[:50]}': repr={repr(doi_stripped)}")

    total_filled = len(valid_dois)
    total_expected = len(rows)  # Should be 6

    print(f"\nSummary: {total_filled}/{total_expected} DOIs filled with valid format")

    # Component 1: At least half (3+) of the DOIs filled with valid format (0.5 points)
    try:
        if total_filled >= 3:
            print(f"PASS: Component 1 — {total_filled}/{total_expected} DOIs filled, meets threshold of 3 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — only {total_filled}/{total_expected} DOIs filled, need at least 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 6 DOIs filled with valid format (0.5 points)
    try:
        if total_filled == total_expected and total_expected == 6:
            print(f"PASS: Component 2 — All 6 DOIs filled with valid format (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — only {total_filled}/6 DOIs filled, need all 6")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify against canonical file path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
