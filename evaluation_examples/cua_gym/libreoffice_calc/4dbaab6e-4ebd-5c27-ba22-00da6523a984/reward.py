"""
Reward Script: Research Workflow Automation
Task ID: osworld_multi_apps_multi_simple_012
Domain: multi_apps (libreoffice_calc + libreoffice_writer + os)

Task: Automate a research workflow:
  1. For each of 4 queries in queries.ods: search and fill in result titles (col C) and links (col D)
  2. Write a Python script format_results.py that reads the Calc file and generates a Writer report
  3. Generate results_report.odt with 4 formatted citations

Scoring:
  - Component 1: queries.ods has result titles in column C for all 4 rows  (0.35 pts)
  - Component 2: queries.ods has result links in column D for all 4 rows   (0.25 pts)
  - Component 3: format_results.py script exists                           (0.20 pts)
  - Component 4: results_report.odt exists with >= 4 citation headings     (0.20 pts)
  Total: 1.0
"""

import os

RESEARCH_DIR = '/home/user/research'
ODS_PATH = os.path.join(RESEARCH_DIR, 'queries.ods')
SCRIPT_PATH = os.path.join(RESEARCH_DIR, 'format_results.py')
REPORT_PATH = os.path.join(RESEARCH_DIR, 'results_report.odt')


def get_ods_rows(ods_path):
    """Read rows from the ODS file using odfpy. Returns list of rows as lists of strings."""
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(ods_path)
    tables = doc.getElementsByType(Table)
    if not tables:
        return []

    table = tables[0]
    rows = table.getElementsByType(TableRow)
    result = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            # Get repeat count to handle repeated empty cells
            repeat = cell.getAttribute('numbercolumnsrepeated')
            try:
                repeat = int(repeat) if repeat else 1
            except (ValueError, TypeError):
                repeat = 1
            paras = cell.getElementsByType(P)
            text = str(paras[0]) if paras else ''
            for _ in range(repeat):
                row_data.append(text)
        result.append(row_data)
    return result


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: queries.ods must exist
    if not os.path.exists(ODS_PATH):
        print(f"CRITICAL: queries.ods not found at {ODS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODS rows
    try:
        rows = get_ods_rows(ODS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot read ODS file {ODS_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expect header row + 4 data rows
    # Row format: [Query(A), TargetURL(B), ResultTitle(C), ResultLink(D)]
    if len(rows) < 2:
        print(f"CRITICAL: Expected at least 2 rows (header + data), got {len(rows)}")
        print("REWARD: 0.0")
        return 0.0

    data_rows = rows[1:]  # skip header row
    print(f"INFO: Found {len(data_rows)} data rows in queries.ods")

    # Component 1: All 4 data rows have non-empty Result Titles in column C (0.35 points)
    try:
        titles_filled = 0
        for i, row in enumerate(data_rows):
            title = row[2].strip() if len(row) > 2 else ''
            if title:
                titles_filled += 1
                print(f"  Row {i+1} Title: {title[:60]}")
            else:
                print(f"  Row {i+1} Title: EMPTY")

        if titles_filled == 4:
            print(f"PASS: Component 1 — All 4 rows have Result Titles in column C (0.35 pts)")
            total_score += 0.35
        elif titles_filled >= 2:
            partial = round(0.35 * titles_filled / 4, 4)
            print(f"PARTIAL: Component 1 — {titles_filled}/4 rows have Result Titles ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {titles_filled}/4 rows have Result Titles in column C")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 data rows have non-empty Result Links in column D (0.25 points)
    try:
        links_filled = 0
        for i, row in enumerate(data_rows):
            link = row[3].strip() if len(row) > 3 else ''
            if link:
                links_filled += 1
                print(f"  Row {i+1} Link: {link[:80]}")
            else:
                print(f"  Row {i+1} Link: EMPTY")

        if links_filled == 4:
            print(f"PASS: Component 2 — All 4 rows have Result Links in column D (0.25 pts)")
            total_score += 0.25
        elif links_filled >= 2:
            partial = round(0.25 * links_filled / 4, 4)
            print(f"PARTIAL: Component 2 — {links_filled}/4 rows have Result Links ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {links_filled}/4 rows have Result Links in column D")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: format_results.py exists (0.20 points)
    try:
        if os.path.isfile(SCRIPT_PATH):
            # Also verify it has some content (is a real script, not empty)
            size = os.path.getsize(SCRIPT_PATH)
            if size > 100:
                print(f"PASS: Component 3 — format_results.py exists and has content ({size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — format_results.py exists but is nearly empty ({size} bytes)")
        else:
            print(f"FAIL: Component 3 — format_results.py not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: results_report.odt exists with >= 4 citation headings (0.20 points)
    try:
        if not os.path.isfile(REPORT_PATH):
            print(f"FAIL: Component 4 — results_report.odt not found at {REPORT_PATH}")
        else:
            # Check the ODT contains citation headings
            from odf.opendocument import load as odt_load
            from odf.text import H

            report_doc = odt_load(REPORT_PATH)
            headings = report_doc.getElementsByType(H)
            citation_headings = [str(h) for h in headings if 'Citation' in str(h) or 'citation' in str(h)]

            print(f"  ODT headings found: {[str(h) for h in headings]}")
            print(f"  Citation headings: {citation_headings}")

            if len(citation_headings) >= 4:
                print(f"PASS: Component 4 — results_report.odt has {len(citation_headings)} citation headings (0.20 pts)")
                total_score += 0.20
            elif len(citation_headings) >= 1:
                partial = round(0.20 * len(citation_headings) / 4, 4)
                print(f"PARTIAL: Component 4 — results_report.odt has {len(citation_headings)}/4 citations ({partial} pts)")
                total_score += partial
            else:
                # ODT exists but no citation headings — check if it at least has content
                from odf.text import P
                paras = report_doc.getElementsByType(P)
                para_texts = [str(p) for p in paras if str(p).strip()]
                citation_paras = [t for t in para_texts if 'Citation' in t or 'citation' in t or 'Result' in t]
                if len(citation_paras) >= 4:
                    print(f"PARTIAL: Component 4 — ODT has content (no heading markup, {len(citation_paras)} citation paras) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 4 — results_report.odt exists but has insufficient citation content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
