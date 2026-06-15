"""
Reward Script: Batch Conversion and Quality-Check Pipeline
Task ID: osworld_multi_apps_doc_batch_convert_012
Domain: multi_apps (libreoffice_calc + libreoffice_writer + os)
Scoring:
  - Component 1 (0.25): 12 PDF files exist in docs_input/ with non-zero size
  - Component 2 (0.35): qc_results.ods exists on Desktop with correct headers,
                         12 data rows, and all Status values = 'PASS'
  - Component 3 (0.40): qc_report.odt exists on Desktop with title heading,
                         summary paragraph mentioning 12/12 passed, results table
                         with 12 rows, and conclusion paragraph
"""

import os
import zipfile
import io
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
DOCS_INPUT = '/home/user/docs_input'
DESKTOP = '/home/user/Desktop'

# Expected filenames based on context
EXPECTED_ODTS = [
    'annual_report_2024.odt',
    'budget_proposal_2025.odt',
    'compliance_report_gdpr.odt',
    'contract_template_services.odt',
    'employee_handbook_v3.odt',
    'meeting_minutes_q1_review.odt',
    'policy_document_remote_work.odt',
    'product_specifications_v2.odt',
    'project_charter_alpha.odt',
    'research_summary_biotech.odt',
    'technical_guide_api_v4.odt',
    'training_materials_safety.odt',
]

EXPECTED_PDFS = [f.replace('.odt', '.pdf') for f in EXPECTED_ODTS]

QC_RESULTS_PATH = os.path.join(DESKTOP, 'qc_results.ods')
QC_REPORT_PATH = os.path.join(DESKTOP, 'qc_report.odt')

ODF_NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}


def parse_ods_rows(file_path):
    """Parse an ODS file and return list of rows (each row is a list of cell text strings)."""
    with open(file_path, 'rb') as f:
        data = f.read()
    zf = zipfile.ZipFile(io.BytesIO(data))
    content = zf.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)
    rows = root.findall('.//table:table-row', ODF_NS)
    result = []
    for row in rows:
        cells = row.findall('table:table-cell', ODF_NS)
        row_data = []
        for cell in cells:
            p = cell.find('text:p', ODF_NS)
            row_data.append(p.text.strip() if p is not None and p.text else '')
        result.append(row_data)
    return result


def parse_odt_structure(file_path):
    """Parse an ODT file and return (headings, paragraphs, table_rows)."""
    with open(file_path, 'rb') as f:
        data = f.read()
    zf = zipfile.ZipFile(io.BytesIO(data))
    content = zf.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)

    headings = []
    paragraphs = []
    table_rows = []

    body = root.find('.//office:text', ODF_NS)
    if body is None:
        return headings, paragraphs, table_rows

    for elem in body:
        tag = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
        text = ''.join(t for t in elem.itertext()).strip()
        if tag == 'h':
            headings.append(text)
        elif tag == 'p':
            if text:
                paragraphs.append(text)
        elif tag == 'table':
            for row_elem in elem.findall('.//table:table-row', ODF_NS):
                cells = row_elem.findall('table:table-cell', ODF_NS)
                row_data = []
                for cell in cells:
                    p = cell.find('text:p', ODF_NS)
                    row_data.append(p.text.strip() if p is not None and p.text else '')
                table_rows.append(row_data)

    return headings, paragraphs, table_rows


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ─── Component 1: 12 PDF files in docs_input/ with non-zero size (0.25 points) ───
    # Initial env has 0 PDFs in docs_input; golden env has 12 PDFs.
    try:
        if not os.path.isdir(DOCS_INPUT):
            print("FAIL: Component 1 — docs_input/ directory not found")
        else:
            existing_files = os.listdir(DOCS_INPUT)
            pdfs_nonempty = []
            for pdf_name in EXPECTED_PDFS:
                if pdf_name in existing_files:
                    pdf_path = os.path.join(DOCS_INPUT, pdf_name)
                    size = os.path.getsize(pdf_path)
                    if size > 0:
                        pdfs_nonempty.append(pdf_name)

            num_ok = len(pdfs_nonempty)
            if num_ok == 12:
                print(f"PASS: Component 1 — all 12 PDF files found non-empty (0.25 pts)")
                total_score += 0.25
            elif num_ok > 0:
                partial_c1 = round(0.25 * num_ok / 12, 4)
                total_score += partial_c1
                print(f"PARTIAL: Component 1 — {num_ok}/12 PDFs non-empty, awarding {partial_c1} pts")
            else:
                print("FAIL: Component 1 — no non-empty PDFs found in docs_input/")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ─── Component 2: qc_results.ods on Desktop with correct structure (0.35 points) ───
    # Initial env has no qc_results.ods; golden has it with 12 data rows all PASS.
    try:
        if not os.path.exists(QC_RESULTS_PATH):
            print(f"FAIL: Component 2 — qc_results.ods not found at {QC_RESULTS_PATH}")
        else:
            rows = parse_ods_rows(QC_RESULTS_PATH)
            expected_headers = ['Filename', 'Expected_Pages', 'Actual_Pages', 'File_Size_Bytes', 'Status']

            # Check headers (row 0)
            header_ok = (
                len(rows) > 0 and
                len(rows[0]) >= 5 and
                all(rows[0][i].strip() == expected_headers[i] for i in range(5))
            )

            data_rows = rows[1:] if len(rows) > 1 else []

            # Count rows with Status=PASS and positive file size
            pass_rows = sum(
                1 for r in data_rows
                if len(r) >= 5 and r[4].strip().upper() == 'PASS'
            )
            size_ok_rows = 0
            for r in data_rows:
                if len(r) >= 4:
                    try:
                        if int(r[3]) > 0:
                            size_ok_rows += 1
                    except (ValueError, TypeError):
                        pass

            if header_ok and len(data_rows) == 12 and pass_rows == 12 and size_ok_rows == 12:
                print("PASS: Component 2 — qc_results.ods: correct headers, 12 rows, "
                      "all Status=PASS, all sizes>0 (0.35 pts)")
                total_score += 0.35
            elif header_ok and len(data_rows) == 12 and pass_rows == 12:
                print(f"PARTIAL: Component 2 — qc_results.ods 12 rows all PASS, "
                      f"but only {size_ok_rows}/12 have positive file sizes (0.25 pts)")
                total_score += 0.25
            elif header_ok and len(data_rows) == 12:
                print(f"PARTIAL: Component 2 — qc_results.ods 12 rows but only "
                      f"{pass_rows}/12 Status=PASS (0.15 pts)")
                total_score += 0.15
            elif header_ok and len(data_rows) > 0:
                partial_c2 = round(0.35 * len(data_rows) / 12, 4)
                total_score += partial_c2
                print(f"PARTIAL: Component 2 — qc_results.ods has {len(data_rows)}/12 "
                      f"data rows ({partial_c2} pts)")
            elif len(data_rows) > 0:
                print(f"PARTIAL: Component 2 — qc_results.ods has data but header mismatch; "
                      f"expected {expected_headers}, got {rows[0] if rows else 'empty'} (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 2 — qc_results.ods is empty or has no data rows")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ─── Component 3: qc_report.odt on Desktop with correct content (0.40 points) ───
    # Initial env has no qc_report.odt; golden has it with title, summary, table, conclusion.
    try:
        if not os.path.exists(QC_REPORT_PATH):
            print(f"FAIL: Component 3 — qc_report.odt not found at {QC_REPORT_PATH}")
        else:
            headings, paragraphs, table_rows = parse_odt_structure(QC_REPORT_PATH)

            # Sub-check 3a: Has a title/heading with batch/quality/conversion (0.10 pts)
            has_title = any(
                any(kw in h.lower() for kw in ('batch', 'quality', 'conversion', 'report'))
                for h in headings
            )
            if has_title:
                print("PASS: Component 3a — report has a relevant title heading (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3a — no relevant heading found; headings={headings}")

            # Sub-check 3b: Summary paragraph mentions '12' + documents/pass (0.10 pts)
            all_para_text = ' '.join(paragraphs)
            has_summary_12 = (
                '12' in all_para_text and
                ('pass' in all_para_text.lower() or 'document' in all_para_text.lower())
            )
            if has_summary_12:
                print("PASS: Component 3b — summary paragraph mentions '12' documents (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3b — no summary mentioning 12; "
                      f"first paragraphs: {paragraphs[:2]}")

            # Sub-check 3c: Results table with 12 data rows (0.15 pts)
            data_table_rows = [r for r in table_rows if r and r[0] and r[0] != 'Filename']
            num_table_data = len(data_table_rows)
            if num_table_data >= 12:
                print(f"PASS: Component 3c — results table has {num_table_data} data rows (0.15 pts)")
                total_score += 0.15
            elif num_table_data > 0:
                partial_c3c = round(0.15 * num_table_data / 12, 4)
                total_score += partial_c3c
                print(f"PARTIAL: Component 3c — results table has {num_table_data}/12 rows "
                      f"({partial_c3c} pts)")
            else:
                print("FAIL: Component 3c — no results table data rows found in qc_report.odt")

            # Sub-check 3d: Conclusion/failure-list paragraph (0.05 pts)
            has_conclusion = any(
                any(kw in p.lower() for kw in ('fail', 'pass', 'all', 'document'))
                for p in paragraphs
            )
            if has_conclusion:
                print("PASS: Component 3d — report has conclusion/summary paragraph (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 3d — no conclusion paragraph found in qc_report.odt")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
