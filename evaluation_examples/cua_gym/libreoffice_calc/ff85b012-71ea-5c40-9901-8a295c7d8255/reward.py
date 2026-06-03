"""
Reward Script: Process 3 paper submissions — fill editorial_db.ods reference database and produce editorial_report.odt
Task ID: osworld_multi_apps_web_references_014
Domain: libreoffice_calc (+ libreoffice_writer)

Scoring rubric:
  Component 1 (0.40): editorial_db.ods has data rows for all 3 papers with all required columns populated
  Component 2 (0.30): editorial_report.odt exists in Documents with 3 submission sections (one per paper)
  Component 3 (0.30): editorial_report.odt contains required editorial content (recommendations, self-citation flags, ref counts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_014'

ODS_PATH = f'{WORKDIR}/Desktop/editorial_db.ods'
ODT_PATH = f'{WORKDIR}/Documents/editorial_report.odt'

REQUIRED_COLUMNS = ['Paper_ID', 'Ref_Number', 'Title', 'DOI', 'Citation_Count', 'Self_Citation', 'DOI_Valid']
REQUIRED_PAPERS = ['submission1', 'submission2', 'submission3']
MIN_REFS_PER_PAPER = 5   # each paper should have at least 5 references (task says 10-15 each)
REQUIRED_RECOMMENDATION_KEYWORDS = ['Accept', 'Revise', 'Reject']


def parse_ods_rows(ods_path):
    """
    Parse an ODS file and return (headers, data_rows).
    data_rows is a list of dicts mapping column name to cell value.
    Returns (None, None) on failure.
    """
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    }
    try:
        with zipfile.ZipFile(ods_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8').lstrip()
        root = ET.fromstring(content)
        rows = root.findall('.//table:table-row', ns)
        if not rows:
            return None, None

        # Extract headers from first row
        header_cells = rows[0].findall('.//table:table-cell', ns)
        headers = []
        for cell in header_cells:
            p = cell.find('.//text:p', ns)
            headers.append(p.text if p is not None and p.text else '')

        # Extract data rows
        data_rows = []
        for row in rows[1:]:
            cells = row.findall('.//table:table-cell', ns)
            values = []
            for cell in cells:
                p = cell.find('.//text:p', ns)
                values.append(p.text if p is not None and p.text else '')
            if any(v.strip() for v in values):  # skip completely empty rows
                row_dict = {}
                for i, h in enumerate(headers):
                    row_dict[h] = values[i] if i < len(values) else ''
                data_rows.append(row_dict)
        return headers, data_rows
    except Exception as e:
        print(f"ERROR: parse_ods_rows failed: {e}")
        return None, None


def parse_odt_text(odt_path):
    """
    Extract all text content (paragraphs and headings) from an ODT file.
    Returns a list of text strings (one per para/heading), or None on failure.
    """
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    }
    try:
        with zipfile.ZipFile(odt_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8').lstrip()
        root = ET.fromstring(content)
        texts = []
        for elem in root.findall('.//text:h', ns):
            t = ''.join(elem.itertext()).strip()
            if t:
                texts.append(t)
        for elem in root.findall('.//text:p', ns):
            t = ''.join(elem.itertext()).strip()
            if t:
                texts.append(t)
        return texts
    except Exception as e:
        print(f"ERROR: parse_odt_text failed: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: editorial_db.ods has reference data for all 3 papers (0.40)
    # All 3 papers must have >= MIN_REFS_PER_PAPER rows, with required columns
    # populated and Self_Citation / DOI_Valid using Yes/No values.
    # =========================================================================
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 1 — ODS file not found at {ODS_PATH}")
        else:
            headers, data_rows = parse_ods_rows(ODS_PATH)
            if headers is None:
                print("FAIL: Component 1 — Could not parse ODS file")
            else:
                # Check required columns exist
                missing_cols = [c for c in REQUIRED_COLUMNS if c not in headers]
                if missing_cols:
                    print(f"FAIL: Component 1 — Missing columns: {missing_cols}")
                else:
                    # Count rows per paper
                    paper_counts = {p: 0 for p in REQUIRED_PAPERS}
                    valid_data_counts = {p: 0 for p in REQUIRED_PAPERS}
                    for row in data_rows:
                        pid = row.get('Paper_ID', '').strip()
                        if pid in paper_counts:
                            paper_counts[pid] += 1
                            # Check that key fields are populated
                            doi_valid_val = row.get('DOI_Valid', '').strip()
                            self_cit_val = row.get('Self_Citation', '').strip()
                            title_val = row.get('Title', '').strip()
                            doi_val = row.get('DOI', '').strip()
                            cit_val = row.get('Citation_Count', '').strip()
                            has_doi_valid = doi_valid_val in ('Yes', 'No')
                            has_self_cit = self_cit_val in ('Yes', 'No')
                            if title_val and doi_val and cit_val and has_doi_valid and has_self_cit:
                                valid_data_counts[pid] += 1

                    # Award points if ALL 3 papers have sufficient rows with complete data
                    papers_with_enough_refs = sum(1 for p in REQUIRED_PAPERS if paper_counts[p] >= MIN_REFS_PER_PAPER)
                    papers_with_valid_data = sum(1 for p in REQUIRED_PAPERS if valid_data_counts[p] >= MIN_REFS_PER_PAPER)

                    print(f"INFO: Row counts per paper: {paper_counts}")
                    print(f"INFO: Valid-data rows per paper: {valid_data_counts}")

                    if papers_with_enough_refs == 3 and papers_with_valid_data == 3:
                        print(f"PASS: Component 1 — All 3 papers have >= {MIN_REFS_PER_PAPER} filled rows (0.40 pts)")
                        total_score += 0.40
                    elif papers_with_enough_refs >= 2 and papers_with_valid_data >= 2:
                        print(f"PARTIAL: Component 1 — {papers_with_enough_refs}/3 papers have sufficient data (0.20 pts)")
                        total_score += 0.20
                    elif papers_with_enough_refs >= 1:
                        print(f"PARTIAL: Component 1 — Only {papers_with_enough_refs}/3 papers have data (0.10 pts)")
                        total_score += 0.10
                    else:
                        print(f"FAIL: Component 1 — No paper has sufficient rows. Counts: {paper_counts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: editorial_report.odt exists in Documents with 3 sections (0.30)
    # The file must be present and contain section headings for all 3 submissions.
    # =========================================================================
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 2 — editorial_report.odt not found at {ODT_PATH}")
        else:
            odt_texts = parse_odt_text(ODT_PATH)
            if odt_texts is None:
                print("FAIL: Component 2 — Could not parse ODT file")
            else:
                # Check for 3 submission section references
                all_texts = '\n'.join(odt_texts)
                sections_found = sum(1 for p in REQUIRED_PAPERS if p in all_texts)
                if sections_found == 3:
                    print(f"PASS: Component 2 — editorial_report.odt found with all 3 submission sections (0.30 pts)")
                    total_score += 0.30
                elif sections_found >= 2:
                    print(f"PARTIAL: Component 2 — {sections_found}/3 submission sections found (0.15 pts)")
                    total_score += 0.15
                elif sections_found >= 1:
                    print(f"PARTIAL: Component 2 — Only {sections_found}/3 submission sections found (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 2 — No submission sections found in editorial_report.odt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: editorial_report.odt has required editorial content (0.30)
    # Must contain at least one recommendation (Accept/Revise/Reject),
    # self-citation information, and reference count information for each paper.
    # =========================================================================
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 3 — editorial_report.odt not found")
        else:
            odt_texts = parse_odt_text(ODT_PATH)
            if odt_texts is None:
                print("FAIL: Component 3 — Could not parse ODT file")
            else:
                all_texts = '\n'.join(odt_texts)

                # Check for at least one recommendation keyword
                has_recommendation = any(kw in all_texts for kw in REQUIRED_RECOMMENDATION_KEYWORDS)

                # Check for self-citation content
                has_self_citation_info = ('Self-Citation' in all_texts or 'self-citation' in all_texts
                                          or 'Self_Citation' in all_texts or '20%' in all_texts)

                # Check for reference count info
                has_ref_count = ('Reference' in all_texts or 'Ref' in all_texts)

                checks_passed = sum([has_recommendation, has_self_citation_info, has_ref_count])
                print(f"INFO: Editorial content checks: recommendation={has_recommendation}, "
                      f"self_citation_info={has_self_citation_info}, ref_count={has_ref_count}")

                if checks_passed == 3:
                    print(f"PASS: Component 3 — All editorial content checks pass (0.30 pts)")
                    total_score += 0.30
                elif checks_passed == 2:
                    print(f"PARTIAL: Component 3 — {checks_passed}/3 content checks pass (0.15 pts)")
                    total_score += 0.15
                elif checks_passed == 1:
                    print(f"PARTIAL: Component 3 — Only {checks_passed}/3 content checks pass (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 — No required editorial content found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
