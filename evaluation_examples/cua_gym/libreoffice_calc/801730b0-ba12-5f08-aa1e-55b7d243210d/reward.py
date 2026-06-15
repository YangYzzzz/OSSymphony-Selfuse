"""
Reward Script: Collect ML best paper award winners 2021-2024 across NeurIPS/ICML/ICLR
Task ID: osworld_multi_apps_web_conference_011
Domain: multi_apps (libreoffice_calc + libreoffice_writer)

Scoring Rubric:
  Component 1 (0.35): ml_best_papers.ods has correct structure with all required columns,
                       data covering all 3 conferences and years 2021-2024, and numeric
                       Citation_Count values.
  Component 2 (0.25): ml_best_papers.ods has an Institution Summary sheet identifying
                       the most-awarded institution.
  Component 3 (0.25): best_papers_summary.odt exists and contains a substantive summary
                       paragraph mentioning institutions and conferences.
  Component 4 (0.15): Semantic Scholar URLs present in the data rows.

Both files are on the Desktop (/home/user/Desktop/).
Initial state: Desktop is empty (no files). All points should fail on initial.
"""

import os
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
ODS_PATH = os.path.join(DESKTOP, 'ml_best_papers.ods')
ODT_PATH = os.path.join(DESKTOP, 'best_papers_summary.odt')

# Required column headers (case-insensitive matching)
REQUIRED_COLUMNS = ['Year', 'Conference', 'Award_Category', 'Title',
                    'First_Author', 'Affiliation', 'Citation_Count', 'Semantic_Scholar_URL']
REQUIRED_CONFERENCES = {'NeurIPS', 'ICML', 'ICLR'}
REQUIRED_YEARS = {'2021', '2022', '2023', '2024'}


def read_ods_content_xml(ods_path):
    """Read content.xml from an ODS file (ZIP-based ODF format)."""
    with zipfile.ZipFile(ods_path, 'r') as z:
        return z.read('content.xml').decode('utf-8')


def read_odt_content_xml(odt_path):
    """Read content.xml from an ODT file (ZIP-based ODF format)."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        return z.read('content.xml').decode('utf-8')


def parse_ods_sheets(content_xml):
    """Parse ODS content.xml; return list of (sheet_name, list_of_rows) tuples.
    Each row is a list of cell text strings."""
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    }
    root = ET.fromstring(content_xml)
    spreadsheet = root.find('.//office:spreadsheet', ns)
    if spreadsheet is None:
        return []
    tables = spreadsheet.findall('.//table:table', ns)
    sheets = []
    for tbl in tables:
        name = tbl.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name', '')
        rows_data = []
        for row in tbl.findall('table:table-row', ns):
            cells = row.findall('table:table-cell', ns)
            row_vals = []
            for cell in cells:
                # Handle repeated columns
                reps_str = cell.get(
                    '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated', '1')
                try:
                    reps = int(reps_str)
                except ValueError:
                    reps = 1
                # Extract text from cell
                texts = []
                for tp in cell.findall('.//text:p', ns):
                    t = ''.join(tp.itertext())
                    texts.append(t)
                cell_val = ' '.join(texts).strip()
                # Limit repeated empty cells to avoid massive lists
                if reps > 10 and not cell_val:
                    reps = 1
                for _ in range(reps):
                    row_vals.append(cell_val)
            rows_data.append(row_vals)
        sheets.append((name, rows_data))
    return sheets


def parse_odt_text(content_xml):
    """Parse ODT content.xml; return list of paragraph text strings."""
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    }
    root = ET.fromstring(content_xml)
    body = root.find('.//office:body', ns)
    if body is None:
        return []
    text_body = body.find('.//office:text', ns)
    if text_body is None:
        return []
    paras = text_body.findall('text:p', ns)
    texts = []
    for p in paras:
        t = ''.join(p.itertext()).strip()
        if t:
            texts.append(t)
    return texts


def verify_task():
    total_score = 0.0

    # ---- Precondition gates: files must exist ----
    if not os.path.exists(ODS_PATH):
        print(f"CRITICAL: {ODS_PATH} not found — task not completed")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(ODT_PATH):
        print(f"CRITICAL: {ODT_PATH} not found — task not completed")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Both files found on Desktop")

    # ---- Component 1: ODS structure and data coverage (0.35 points) ----
    # Checks: correct column headers present, data rows for all 3 conferences
    # and all 4 years (2021-2024), and Citation_Count contains numeric values.
    # This FAILS on initial (no file) and PASSES on golden.
    try:
        ods_xml = read_ods_content_xml(ODS_PATH)
        sheets = parse_ods_sheets(ods_xml)

        # Find the "Best Papers" sheet (first sheet)
        best_papers_sheet = None
        for sname, srows in sheets:
            if srows and len(srows) > 1:
                best_papers_sheet = (sname, srows)
                break

        if best_papers_sheet is None:
            print("FAIL: Component 1 — No data sheet found in ODS file")
        else:
            sname, srows = best_papers_sheet
            print(f"INFO: Found sheet '{sname}' with {len(srows)} rows")

            # Check header row
            header_row = [v.strip() for v in srows[0] if v.strip()]
            header_upper = [h.upper() for h in header_row]

            required_upper = [c.upper() for c in REQUIRED_COLUMNS]
            missing_cols = [c for c in required_upper if c not in header_upper]

            if missing_cols:
                print(f"FAIL: Component 1 — Missing columns: {missing_cols} (found: {header_row})")
            else:
                print(f"PASS: All {len(REQUIRED_COLUMNS)} required columns present")

                # Find column indices
                conf_idx = header_upper.index('CONFERENCE')
                year_idx = header_upper.index('YEAR')
                cit_idx = header_upper.index('CITATION_COUNT')

                # Collect conferences and years from data rows
                found_conferences = set()
                found_years = set()
                numeric_citation_count = 0
                data_row_count = 0

                for row in srows[1:]:
                    if len(row) > max(conf_idx, year_idx, cit_idx):
                        conf_val = row[conf_idx].strip()
                        year_val = row[year_idx].strip()
                        cit_val = row[cit_idx].strip()
                        if conf_val:
                            found_conferences.add(conf_val)
                        if year_val:
                            found_years.add(year_val)
                        if cit_val:
                            try:
                                float(cit_val)
                                numeric_citation_count += 1
                            except ValueError:
                                pass
                            data_row_count += 1

                missing_conferences = REQUIRED_CONFERENCES - found_conferences
                missing_years = REQUIRED_YEARS - found_years

                if missing_conferences:
                    print(f"FAIL: Component 1 — Missing conference data: {missing_conferences}")
                elif missing_years:
                    print(f"FAIL: Component 1 — Missing year data: {missing_years}")
                elif data_row_count < 10:
                    print(f"FAIL: Component 1 — Too few data rows: {data_row_count} (need >= 10)")
                elif numeric_citation_count < 5:
                    print(f"FAIL: Component 1 — Too few numeric citation counts: {numeric_citation_count}")
                else:
                    print(f"PASS: Component 1 — All 3 conferences, all 4 years covered, "
                          f"{data_row_count} data rows, {numeric_citation_count} citation counts (0.35 pts)")
                    total_score += 0.35

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Institution Summary sheet (0.25 points) ----
    # Checks: ODS has a second sheet with institution tallies, with at least one
    # institution having count >= 2, identifying the dominant institution.
    # This FAILS on initial and PASSES on golden.
    try:
        ods_xml = read_ods_content_xml(ODS_PATH)
        sheets = parse_ods_sheets(ods_xml)

        if len(sheets) < 2:
            print(f"FAIL: Component 2 — Only {len(sheets)} sheet(s) in ODS; "
                  "need Institution Summary sheet")
        else:
            # Look for any sheet with "Institution" in headers
            inst_sheet = None
            for sname, srows in sheets[1:]:
                if srows:
                    first_row_vals = [v.strip().lower() for v in srows[0] if v.strip()]
                    if any('institution' in v or 'award' in v or 'count' in v for v in first_row_vals):
                        inst_sheet = (sname, srows)
                        break

            if inst_sheet is None:
                # Fall back: use 2nd sheet regardless
                inst_sheet = sheets[1]
                print(f"INFO: Using 2nd sheet '{inst_sheet[0]}' as institution summary")

            iname, irows = inst_sheet
            print(f"INFO: Institution sheet '{iname}' has {len(irows)} rows")

            # Find max count value
            max_count = 0
            institutions_with_count = 0
            for row in irows[1:]:
                vals = [v.strip() for v in row if v.strip()]
                if len(vals) >= 2:
                    institutions_with_count += 1
                    try:
                        cnt = int(vals[1])
                        if cnt > max_count:
                            max_count = cnt
                    except (ValueError, IndexError):
                        pass

            if institutions_with_count < 2:
                print(f"FAIL: Component 2 — Institution summary has too few entries: "
                      f"{institutions_with_count}")
            elif max_count < 2:
                print(f"FAIL: Component 2 — No institution has award count >= 2 "
                      f"(max found: {max_count}); summary seems incomplete")
            else:
                print(f"PASS: Component 2 — Institution summary with {institutions_with_count} "
                      f"institutions, max count={max_count} (0.25 pts)")
                total_score += 0.25

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: ODT summary paragraph content (0.25 points) ----
    # Checks: summary document has at least one substantive paragraph (>= 100 chars)
    # mentioning at least 2 of the 3 conferences and referencing institutions.
    # This FAILS on initial and PASSES on golden.
    try:
        odt_xml = read_odt_content_xml(ODT_PATH)
        paragraphs = parse_odt_text(odt_xml)

        if not paragraphs:
            print("FAIL: Component 3 — ODT file has no text content")
        else:
            # Check for substantive paragraph mentioning conferences and institutions
            all_text = ' '.join(paragraphs).lower()
            total_text_len = sum(len(p) for p in paragraphs)

            # Count conference mentions
            conference_mentions = sum(
                1 for c in ['neurips', 'icml', 'iclr'] if c in all_text
            )
            # Check for institution-related keywords
            institution_keywords = ['institution', 'university', 'google', 'stanford',
                                    'research', 'lab', 'institute']
            has_institution_ref = any(kw in all_text for kw in institution_keywords)

            # Check for award/citation discussion
            has_award_discussion = any(kw in all_text
                                       for kw in ['award', 'citation', 'paper', 'best paper'])

            if total_text_len < 100:
                print(f"FAIL: Component 3 — Summary text too short: {total_text_len} chars")
            elif conference_mentions < 2:
                print(f"FAIL: Component 3 — Only {conference_mentions}/3 conferences mentioned")
            elif not has_institution_ref:
                print("FAIL: Component 3 — No institution references in summary")
            elif not has_award_discussion:
                print("FAIL: Component 3 — No award/citation discussion in summary")
            else:
                print(f"PASS: Component 3 — ODT summary has {total_text_len} chars, "
                      f"{conference_mentions}/3 conferences, institution refs present (0.25 pts)")
                total_score += 0.25

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: Semantic Scholar URLs present (0.15 points) ----
    # Checks: ODS data rows contain semanticscholar.org URLs.
    # This FAILS on initial and PASSES on golden.
    try:
        ods_xml = read_ods_content_xml(ODS_PATH)
        sheets = parse_ods_sheets(ods_xml)

        best_papers_sheet = None
        for sname, srows in sheets:
            if srows and len(srows) > 1:
                best_papers_sheet = (sname, srows)
                break

        if best_papers_sheet is None:
            print("FAIL: Component 4 — No data sheet found")
        else:
            sname, srows = best_papers_sheet
            header_row = [v.strip().upper() for v in srows[0] if v.strip()]

            if 'SEMANTIC_SCHOLAR_URL' not in header_row:
                print("FAIL: Component 4 — No Semantic_Scholar_URL column found")
            else:
                url_idx = header_row.index('SEMANTIC_SCHOLAR_URL')
                url_count = 0
                valid_url_count = 0

                for row in srows[1:]:
                    if len(row) > url_idx:
                        url_val = row[url_idx].strip()
                        if url_val:
                            url_count += 1
                            if 'semanticscholar.org' in url_val.lower():
                                valid_url_count += 1

                if valid_url_count < 5:
                    print(f"FAIL: Component 4 — Too few Semantic Scholar URLs: "
                          f"{valid_url_count} valid out of {url_count} URL entries")
                else:
                    print(f"PASS: Component 4 — {valid_url_count} Semantic Scholar URLs present (0.15 pts)")
                    total_score += 0.15

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
