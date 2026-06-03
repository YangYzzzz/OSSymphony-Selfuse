"""
Reward Script: Audit research paper bibliography and compile findings
Task ID: osworld_multi_apps_web_references_012
Domain: libreoffice_calc (multi-app: ODS + ODT)

Scoring Rubric:
  Component 1 (0.35): ref_audit.ods contains 15 data rows with audit data
  Component 2 (0.25): ref_audit.ods has a summary row at the bottom
  Component 3 (0.25): paper_draft.odt contains annotations for flagged references
  Component 4 (0.15): Flag column values are correct (Broken_Link, Not_Peer_Reviewed, Old, OK)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_012'

ODS_PATH = os.path.join(WORKDIR, 'Desktop', 'ref_audit.ods')
ODT_PATH = os.path.join(WORKDIR, 'Documents', 'paper_draft.odt')

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'dc': 'http://purl.org/dc/elements/1.1/',
}


def parse_ods_rows(ods_path):
    """Parse ODS content.xml and return list of row data (as lists of cell text)."""
    with zipfile.ZipFile(ods_path, 'r') as z:
        content_xml = z.read('content.xml')

    root = ET.fromstring(content_xml)
    spreadsheet = root.find('.//office:spreadsheet', NS)
    if spreadsheet is None:
        raise ValueError("No spreadsheet element found in ODS")

    table = spreadsheet.find('table:table', NS)
    if table is None:
        raise ValueError("No table found in spreadsheet")

    rows = []
    for row_elem in table.findall('table:table-row', NS):
        row_data = []
        for cell in row_elem.findall('table:table-cell', NS):
            # Get text content of cell
            texts = []
            for p in cell.findall('text:p', NS):
                texts.append(p.text or '')
            cell_text = ' '.join(texts).strip()
            row_data.append(cell_text)
        rows.append(row_data)

    return rows


def parse_odt_annotations(odt_path):
    """Parse ODT content.xml and return list of annotation text bodies."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        content_xml = z.read('content.xml')

    root = ET.fromstring(content_xml)
    annotations = []
    # office:annotation elements can appear anywhere in the document
    for ann in root.findall('.//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation'):
        texts = []
        for p in ann.findall('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
            if p.text:
                texts.append(p.text)
        annotations.append(' '.join(texts))

    return annotations


def verify_task():
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Precondition gate: Check that required files exist
    # -----------------------------------------------------------------------
    if not os.path.exists(ODS_PATH):
        print(f"CRITICAL: ODS file not found: {ODS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(ODT_PATH):
        print(f"CRITICAL: ODT file not found: {ODT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: ref_audit.ods has 15 data rows filled with audit data (0.35 pts)
    # The initial state only has a header row (no data rows).
    # The golden state has 15 data rows + the header row.
    # -----------------------------------------------------------------------
    try:
        rows = parse_ods_rows(ODS_PATH)
        # rows[0] = header, rows[1..15] = data rows, rows[16] = summary (if present)
        # Count rows that have a numeric Ref_Number in column 0
        data_rows = []
        for row in rows[1:]:  # skip header
            if row and row[0].strip().isdigit():
                data_rows.append(row)

        # Expect at least 15 data rows with Ref_Number, Title, DOI_Valid, Citation_Count, Age_Years, Peer_Reviewed, Flag
        fully_filled_rows = []
        for row in data_rows:
            # Must have at least 7 columns and none of the critical ones blank
            if (len(row) >= 7
                    and row[0].strip()  # Ref_Number
                    and row[1].strip()  # Title
                    and row[2].strip() in ('Yes', 'No')  # DOI_Valid
                    and row[4].strip().lstrip('-').isdigit()  # Age_Years
                    and row[5].strip() in ('Yes', 'No')  # Peer_Reviewed
                    and row[6].strip() in ('OK', 'Old', 'Broken_Link', 'Not_Peer_Reviewed')):  # Flag
                fully_filled_rows.append(row)

        if len(fully_filled_rows) >= 15:
            print(f"PASS: Component 1 — ref_audit.ods has {len(fully_filled_rows)} fully filled data rows (0.35 pts)")
            total_score += 0.35
        elif len(fully_filled_rows) >= 10:
            print(f"PARTIAL: Component 1 — ref_audit.ods has {len(fully_filled_rows)}/15 filled data rows (0.15 pts)")
            total_score += 0.15
        elif len(fully_filled_rows) >= 5:
            print(f"PARTIAL: Component 1 — ref_audit.ods has {len(fully_filled_rows)}/15 filled data rows (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — ref_audit.ods has {len(fully_filled_rows)}/15 filled data rows (expected >= 15)")

    except Exception as e:
        print(f"ERROR: Component 1 — Could not parse ODS: {e}")

    # -----------------------------------------------------------------------
    # Component 2: ref_audit.ods has a summary row at the bottom (0.25 pts)
    # The task requires a summary row with total refs, broken count,
    # non-peer-reviewed count, and old count.
    # -----------------------------------------------------------------------
    try:
        rows = parse_ods_rows(ODS_PATH)

        # Find the summary row - it should contain "SUMMARY" or similar keyword
        # or be on row index 16+ and have aggregated counts
        summary_found = False
        for row in rows:
            if not row:
                continue
            row_text = ' '.join(row).upper()
            if 'SUMMARY' in row_text or 'TOTAL' in row_text:
                # Check that there is count-like data (a number representing 15 total refs)
                # The summary row should have at least one cell with value "15" (total refs)
                has_total_count = False
                for cell in row:
                    if cell.strip() == '15' or '15' in cell:
                        has_total_count = True
                        break

                if has_total_count:
                    print(f"PASS: Component 2 — Summary row found with total count of 15 (0.25 pts)")
                    total_score += 0.25
                    summary_found = True
                    break
                else:
                    # Partial: summary row exists but may be missing expected totals
                    print(f"PARTIAL: Component 2 — Summary/Total row found but missing count=15 (0.10 pts)")
                    total_score += 0.10
                    summary_found = True
                    break

        if not summary_found:
            print(f"FAIL: Component 2 — No summary/total row found in ref_audit.ods")

    except Exception as e:
        print(f"ERROR: Component 2 — Could not parse ODS summary row: {e}")

    # -----------------------------------------------------------------------
    # Component 3: paper_draft.odt has annotations for flagged references (0.25 pts)
    # The initial ODT has no annotations. The golden ODT has annotations
    # on each flagged reference paragraph.
    # -----------------------------------------------------------------------
    try:
        annotations = parse_odt_annotations(ODT_PATH)

        # Count annotations that contain audit-related keywords
        audit_annotations = [a for a in annotations if any(kw in a.upper() for kw in
                             ('AUDIT FLAG', 'BROKEN', 'OLD', 'NOT PEER', 'PEER-REVIEWED', 'DOI'))]

        if len(audit_annotations) >= 8:
            print(f"PASS: Component 3 — paper_draft.odt has {len(audit_annotations)} audit annotations (0.25 pts)")
            total_score += 0.25
        elif len(audit_annotations) >= 4:
            print(f"PARTIAL: Component 3 — paper_draft.odt has {len(audit_annotations)} audit annotations (0.12 pts)")
            total_score += 0.12
        elif len(audit_annotations) >= 1:
            print(f"PARTIAL: Component 3 — paper_draft.odt has {len(audit_annotations)} audit annotations (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — paper_draft.odt has no audit annotations (expected >= 8)")

    except Exception as e:
        print(f"ERROR: Component 3 — Could not parse ODT annotations: {e}")

    # -----------------------------------------------------------------------
    # Component 4: Flag column values are correct (0.15 pts)
    # Verified flags in golden:
    #   - "Broken_Link" for refs 8 and 15 (DOI_Valid=No)
    #   - "Not_Peer_Reviewed" for refs 5 and 14 (Peer_Reviewed=No, DOI_Valid=Yes)
    #   - "Old" for refs 1,2,3,9,10,11,12,13 (Age_Years > 10)
    #   - "OK" for refs 4,6,7
    # -----------------------------------------------------------------------
    try:
        rows = parse_ods_rows(ODS_PATH)

        # Collect data rows and check flag consistency
        data_rows = [r for r in rows[1:] if r and r[0].strip().isdigit()]

        # Validate flag logic:
        # - If DOI_Valid == "No" → Flag should be "Broken_Link"
        # - If Peer_Reviewed == "No" and DOI_Valid == "Yes" → Flag should include "Not_Peer_Reviewed"
        # - If Age_Years > 10 (and not Broken_Link/Not_Peer_Reviewed) → Flag should be "Old"
        #   (some implementations may flag old as separate or combined)
        # - Otherwise → Flag should be "OK"

        broken_link_correct = 0
        not_peer_reviewed_correct = 0
        old_correct = 0
        ok_correct = 0

        for row in data_rows:
            if len(row) < 7:
                continue
            doi_valid = row[2].strip()
            age_years_str = row[4].strip()
            peer_reviewed = row[5].strip()
            flag = row[6].strip()

            try:
                age_years = int(age_years_str)
            except (ValueError, TypeError):
                age_years = 0

            if doi_valid == 'No' and flag == 'Broken_Link':
                broken_link_correct += 1
            elif doi_valid == 'Yes' and peer_reviewed == 'No' and flag == 'Not_Peer_Reviewed':
                not_peer_reviewed_correct += 1
            elif doi_valid == 'Yes' and peer_reviewed == 'Yes' and age_years >= 10 and flag == 'Old':
                # "Old" means >= 10 years (as implemented in golden)
                old_correct += 1
            elif doi_valid == 'Yes' and peer_reviewed == 'Yes' and age_years < 10 and flag == 'OK':
                ok_correct += 1

        total_correct = broken_link_correct + not_peer_reviewed_correct + old_correct + ok_correct
        print(f"  Flag breakdown: broken_link={broken_link_correct}, not_peer_reviewed={not_peer_reviewed_correct}, old={old_correct}, ok={ok_correct}")

        if total_correct >= 15:
            print(f"PASS: Component 4 — All 15 flags correct (0.15 pts)")
            total_score += 0.15
        elif total_correct >= 10:
            print(f"PARTIAL: Component 4 — {total_correct}/15 flags correct (0.10 pts)")
            total_score += 0.10
        elif total_correct >= 5:
            print(f"PARTIAL: Component 4 — {total_correct}/15 flags correct (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — Only {total_correct}/15 flags correct (expected 15)")

    except Exception as e:
        print(f"ERROR: Component 4 — Could not check flags: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == '__main__':
    verify_task()
