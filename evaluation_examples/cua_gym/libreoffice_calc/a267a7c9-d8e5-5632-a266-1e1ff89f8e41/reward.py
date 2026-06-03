"""
Reward Script: Find ICLR 2024 spotlight papers about transformers/attention and add to ODS file
Task ID: osworld_multi_apps_web_papers_009
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.4): At least one new transformer/attention spotlight paper row was added
  Component 2 (0.3): All newly added rows have Track='Spotlight' and a numerical rating
  Component 3 (0.3): At least 3 distinct transformer/attention papers were appended with
                     non-empty Title, Authors, and numerical Rating
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_009'
FILE_PATH = '/home/user/Desktop/iclr_spotlights.ods'

# Known initial rows (from initial_env): titles that were pre-existing before the task.
# These are NOT new additions — we exclude them from scoring.
INITIAL_TITLES = {
    'Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model',
    'Diffusion-based Image Translation with Label Guidance for Domain Adaptive Semantic Segmentation',
    'FedAvg with Fine Tuning: Local Updates Lead to Representation Learning',
    'Flow Matching on General Geometries',
    'LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models',
    'Contrastive Preference Learning: Learning from Human Feedback without RL',
    'Generalization in diffusion models arises from geometry-adaptive harmonic representations',
}

# Keywords that indicate transformer/attention relevance (case-insensitive)
TRANSFORMER_KEYWORDS = [
    'transformer', 'transformers', 'attention', 'self-attention',
    'multihead', 'multi-head', 'multi-query'
]


def parse_ods_rows(file_path):
    """
    Parse an ODS file and return a list of rows as lists of cell string values.
    Returns (rows, error_message). rows is a list of lists.
    Row 0 is the header if it exists.
    """
    ns = {
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    }
    TABLE_NAME_ATTR = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name'

    try:
        with zipfile.ZipFile(file_path) as z:
            content = z.read('content.xml').decode('utf-8')
    except Exception as e:
        return None, f"Cannot open ODS file: {e}"

    try:
        root = ET.fromstring(content)
    except Exception as e:
        return None, f"Cannot parse ODS XML: {e}"

    tables = root.findall('.//table:table', ns)
    if not tables:
        return [], "No tables found in ODS"

    # Use first table
    table = tables[0]
    rows = []
    for row_el in table.findall('table:table-row', ns):
        cells = row_el.findall('table:table-cell', ns)
        cell_vals = []
        for cell in cells:
            p = cell.find('text:p', ns)
            cell_vals.append(p.text.strip() if p is not None and p.text else '')
        rows.append(cell_vals)

    return rows, None


def is_transformer_or_attention(title):
    """Check if a paper title is related to transformers or attention mechanisms."""
    title_lower = title.lower()
    return any(kw in title_lower for kw in TRANSFORMER_KEYWORDS)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: file must exist ---
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    rows, error = parse_ods_rows(file_path)
    if rows is None:
        print(f"CRITICAL: Cannot parse ODS file: {error}")
        print("REWARD: 0.0")
        return 0.0

    # Skip header row (row 0)
    data_rows = rows[1:] if len(rows) > 0 else []

    print(f"INFO: Total rows (including header): {len(rows)}")
    print(f"INFO: Data rows: {len(data_rows)}")

    # Identify newly added rows (not in initial set)
    new_rows = []
    for row in data_rows:
        title = row[0] if len(row) > 0 else ''
        if title and title not in INITIAL_TITLES:
            new_rows.append(row)

    print(f"INFO: New rows added: {len(new_rows)}")

    # Identify new transformer/attention rows among new additions
    new_transformer_rows = []
    for row in new_rows:
        title = row[0] if len(row) > 0 else ''
        if is_transformer_or_attention(title):
            new_transformer_rows.append(row)

    print(f"INFO: New transformer/attention rows: {len(new_transformer_rows)}")
    for row in new_transformer_rows:
        title = row[0] if len(row) > 0 else ''
        rating = row[2] if len(row) > 2 else ''
        track = row[3] if len(row) > 3 else ''
        print(f"  - {title[:60]} | Rating={rating} | Track={track}")

    # -------------------------------------------------------------------------
    # Component 1: At least one new transformer/attention paper was added (0.4 pts)
    # This FAILS on initial_env (0 new rows) and PASSES on golden_env (>=1 new row).
    # -------------------------------------------------------------------------
    try:
        if len(new_transformer_rows) >= 1:
            print(f"PASS: Component 1 — {len(new_transformer_rows)} new transformer/attention paper(s) added (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No new transformer/attention papers found in the file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: All new rows have Track='Spotlight' and a numerical Rating (0.3 pts)
    # Checks that newly added rows are correctly categorized with proper metadata.
    # FAILS on initial (no new rows to pass), PASSES on golden.
    # -------------------------------------------------------------------------
    try:
        if len(new_transformer_rows) == 0:
            print("FAIL: Component 2 — No new transformer rows to verify Track/Rating")
        else:
            bad_track_count = 0
            bad_rating_count = 0
            issues = []
            for row in new_transformer_rows:
                title = row[0] if len(row) > 0 else ''
                rating = row[2] if len(row) > 2 else ''
                track = row[3] if len(row) > 3 else ''

                if track.strip() != 'Spotlight':
                    bad_track_count += 1
                    issues.append(f"  Track mismatch: '{title[:50]}' has Track='{track}'")

                try:
                    float(rating)
                except (ValueError, TypeError):
                    bad_rating_count += 1
                    issues.append(f"  Non-numeric rating: '{title[:50]}' has Rating='{rating}'")

            if bad_track_count == 0 and bad_rating_count == 0:
                print(f"PASS: Component 2 — All {len(new_transformer_rows)} new rows have Track='Spotlight' and numerical Rating (0.3 pts)")
                total_score += 0.3
            else:
                print("FAIL: Component 2 — Track/Rating issues in new rows:")
                for issue in issues:
                    print(issue)
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: At least 3 distinct transformer/attention papers added with
    #              non-empty Title and Authors (0.3 pts)
    # Verifies breadth — more than a token addition — and data completeness.
    # FAILS on initial, PASSES on golden.
    # -------------------------------------------------------------------------
    try:
        complete_rows = []
        for row in new_transformer_rows:
            title = row[0] if len(row) > 0 else ''
            authors = row[1] if len(row) > 1 else ''
            if title.strip() and authors.strip():
                complete_rows.append(row)

        if len(complete_rows) >= 3:
            print(f"PASS: Component 3 — {len(complete_rows)} complete transformer/attention papers added (Title+Authors non-empty) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Only {len(complete_rows)} complete transformer/attention paper(s) with Title+Authors; need at least 3")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical task file path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
