"""
Reward Script: Multi-source paper database with model efficiency topics
Task ID: osworld_multi_apps_web_papers_013
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.35): File exists with correct structure (7 columns, 15+ unique papers)
  Component 2 (0.25): All 3 topics covered with 5+ papers each (pruning, distillation, quantization)
  Component 3 (0.20): Papers sorted by Year descending, then Title alphabetically
  Component 4 (0.20): Each paper has a valid URL in arXiv_or_DOI_URL column
"""

import os

FILE_PATH = '/home/user/Desktop/efficiency_papers.ods'
WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_013'

REQUIRED_COLUMNS = ['Title', 'First_Author', 'Year', 'Venue', 'Topics', 'arXiv_or_DOI_URL', 'Notes']
REQUIRED_TOPICS = ['pruning', 'distillation', 'quantization']
MIN_PAPERS = 15
MIN_PAPERS_PER_TOPIC = 5


def read_ods_data(file_path):
    """Read ODS file and return list of rows as lists of strings."""
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    tables = doc.spreadsheet.getElementsByType(Table)
    if not tables:
        raise ValueError("No sheets found in ODS file")

    table = tables[0]
    rows = table.getElementsByType(TableRow)

    data = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            repeat = cell.getAttribute('numbercolumnsrepeated')
            text_nodes = cell.getElementsByType(P)
            value = ' '.join(str(p) for p in text_nodes) if text_nodes else ''
            if repeat and int(repeat) < 100:
                for _ in range(int(repeat)):
                    row_data.append(value)
            else:
                row_data.append(value)
        # Only include rows that have at least one non-empty cell
        if any(v.strip() for v in row_data):
            data.append(row_data)
    return data


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS file
    try:
        data = read_ods_data(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(data) < 2:
        print("CRITICAL: File has fewer than 2 rows (no data rows)")
        print("REWARD: 0.0")
        return 0.0

    header = [str(h).strip() for h in data[0]]
    papers = data[1:]

    # Remove completely empty rows from papers list
    papers = [[str(v).strip() for v in p] for p in papers if any(str(v).strip() for v in p)]

    # -------------------------------------------------------------------------
    # Component 1: File structure — correct columns and 15+ unique papers (0.35 pts)
    # -------------------------------------------------------------------------
    try:
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in header]
        col_ok = len(missing_cols) == 0

        col_title_idx = header.index('Title') if 'Title' in header else -1
        titles = [p[col_title_idx] for p in papers if col_title_idx >= 0 and len(p) > col_title_idx]
        unique_count = len(set(t.lower().strip() for t in titles if t.strip()))
        count_ok = unique_count >= MIN_PAPERS

        if col_ok and count_ok:
            print(f"PASS: Component 1 — {unique_count} unique papers with all {len(REQUIRED_COLUMNS)} required columns (0.35 pts)")
            total_score += 0.35
        elif not col_ok:
            print(f"FAIL: Component 1 — missing columns: {missing_cols}. Found: {header}")
        else:
            print(f"FAIL: Component 1 — only {unique_count} unique papers, need {MIN_PAPERS}+")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Topic coverage — all 3 topics with 5+ papers each (0.25 pts)
    # -------------------------------------------------------------------------
    try:
        topic_counts = {t: 0 for t in REQUIRED_TOPICS}
        col_topics_idx = header.index('Topics') if 'Topics' in header else -1

        if col_topics_idx >= 0:
            for paper in papers:
                if len(paper) > col_topics_idx:
                    paper_topics = paper[col_topics_idx].lower()
                    for topic in REQUIRED_TOPICS:
                        if topic in paper_topics:
                            topic_counts[topic] += 1

        under_threshold = {t: c for t, c in topic_counts.items() if c < MIN_PAPERS_PER_TOPIC}
        all_topics_ok = col_topics_idx >= 0 and len(under_threshold) == 0

        if all_topics_ok:
            print(f"PASS: Component 2 — all topics have {MIN_PAPERS_PER_TOPIC}+ papers: {topic_counts} (0.25 pts)")
            total_score += 0.25
        elif col_topics_idx < 0:
            print("FAIL: Component 2 — 'Topics' column not found")
        else:
            print(f"FAIL: Component 2 — topics with <{MIN_PAPERS_PER_TOPIC} papers: {under_threshold}. All counts: {topic_counts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Sorting — Year descending, then Title alphabetically (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        col_year_idx = header.index('Year') if 'Year' in header else -1
        col_title_idx2 = header.index('Title') if 'Title' in header else -1

        def sort_key(p):
            try:
                year = int(p[col_year_idx]) if col_year_idx >= 0 and len(p) > col_year_idx and p[col_year_idx].isdigit() else 0
            except (ValueError, IndexError):
                year = 0
            title = p[col_title_idx2].lower().strip() if col_title_idx2 >= 0 and len(p) > col_title_idx2 else ''
            return (-year, title)

        current_order = [sort_key(p) for p in papers]
        expected_order = sorted(current_order)
        sort_ok = col_year_idx >= 0 and col_title_idx2 >= 0 and current_order == expected_order

        if sort_ok:
            years_desc = [-key[0] for key in current_order]
            print(f"PASS: Component 3 — papers sorted by Year desc ({years_desc[0]}-{years_desc[-1]}) then Title alpha (0.20 pts)")
            total_score += 0.20
        elif col_year_idx < 0 or col_title_idx2 < 0:
            print("FAIL: Component 3 — 'Year' or 'Title' column not found")
        else:
            mismatches = [i for i, (c, e) in enumerate(zip(current_order, expected_order)) if c != e]
            print(f"FAIL: Component 3 — {len(mismatches)} rows out of sort order (first mismatch at row {mismatches[0]+1 if mismatches else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: URLs — each paper has a valid arXiv or DOI URL (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        col_url_idx = header.index('arXiv_or_DOI_URL') if 'arXiv_or_DOI_URL' in header else -1
        papers_with_url = 0
        papers_without_url = []

        if col_url_idx >= 0:
            for i, paper in enumerate(papers):
                if len(paper) > col_url_idx:
                    url = paper[col_url_idx].strip()
                    if url.startswith('http://') or url.startswith('https://'):
                        papers_with_url += 1
                    else:
                        papers_without_url.append(i + 1)
                else:
                    papers_without_url.append(i + 1)

        url_ratio = papers_with_url / len(papers) if papers and col_url_idx >= 0 else 0
        full_coverage = col_url_idx >= 0 and url_ratio >= 1.0
        partial_coverage = col_url_idx >= 0 and 0.8 <= url_ratio < 1.0

        if full_coverage:
            print(f"PASS: Component 4 — all {papers_with_url}/{len(papers)} papers have valid URLs (0.20 pts)")
            total_score += 0.20
        elif partial_coverage:
            partial_pts = round(0.20 * url_ratio, 2)
            print(f"PARTIAL: Component 4 — {papers_with_url}/{len(papers)} papers have URLs ({partial_pts} pts)")
            total_score += partial_pts
        elif col_url_idx < 0:
            print("FAIL: Component 4 — 'arXiv_or_DOI_URL' column not found")
        else:
            print(f"FAIL: Component 4 — only {papers_with_url}/{len(papers)} papers have valid URLs; missing rows: {papers_without_url[:10]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical file path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
