"""
Reward Script: Multi-file document processing workflow automation
Task ID: osworld_multi_apps_doc_follow_instructions_012
Domain: libreoffice_calc (multi-apps: Calc + Writer + PDFs + log)
Scoring:
  Component 1 (0.25): consolidated.ods exists with merged data (3 sheets, 33 data rows, correct columns + Source column)
  Component 2 (0.25): consolidated.ods Summary sheet has correct aggregation values (Grand Total=1242280.0, 33 records)
  Component 3 (0.15): summary_report.odt exists and contains real data values (not template placeholders)
  Component 4 (0.20): Both PDF exports exist (consolidated.pdf + summary_report.pdf, non-trivial size)
  Component 5 (0.15): completion_log.txt exists on Desktop with timestamp, file sizes, and discrepancy info
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_follow_instructions_012'

CONSOLIDATED_ODS = f'{WORKDIR}/Documents/consolidated.ods'
SUMMARY_REPORT_ODT = f'{WORKDIR}/Documents/summary_report.odt'
CONSOLIDATED_PDF = f'{WORKDIR}/Documents/consolidated.pdf'
SUMMARY_REPORT_PDF = f'{WORKDIR}/Documents/summary_report.pdf'
COMPLETION_LOG = f'{WORKDIR}/Desktop/completion_log.txt'

# Expected golden values from task context
EXPECTED_GRAND_TOTAL = 1242280.0
EXPECTED_TOTAL_RECORDS = 33


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: consolidated.ods exists with merged data structure (0.25 pts)
    # Must have: Data sheet with 33+ data rows and a 'Source' column,
    # plus a 'Summary' sheet for aggregation
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(CONSOLIDATED_ODS):
            print("FAIL: Component 1 — consolidated.ods does not exist")
        else:
            from odf.opendocument import load
            import odf.table as odf_table
            from odf.text import P

            doc = load(CONSOLIDATED_ODS)
            sheets = doc.spreadsheet.getElementsByType(odf_table.Table)
            sheet_names = [s.getAttribute('name') for s in sheets]
            print(f"INFO: consolidated.ods sheet names: {sheet_names}")

            has_data_sheet = 'Data' in sheet_names
            has_summary_sheet = 'Summary' in sheet_names

            if not has_data_sheet:
                print(f"FAIL: Component 1 — No 'Data' sheet found (sheets: {sheet_names})")
            else:
                # Count data rows on Data sheet (excluding header)
                data_sheet = next((s for s in sheets if s.getAttribute('name') == 'Data'), None)
                rows = data_sheet.getElementsByType(odf_table.TableRow)

                # Check header row for standard columns
                header_cells = rows[0].getElementsByType(odf_table.TableCell) if rows else []
                header_vals = []
                for cell in header_cells:
                    val = ''
                    for p in cell.getElementsByType(P):
                        val += p.firstChild.data if p.firstChild else ''
                    header_vals.append(val)

                print(f"INFO: Data sheet header: {header_vals}")

                # Check 'Source' column in header (indicates merge provenance)
                has_source_col = any('source' in h.lower() for h in header_vals if h)
                data_row_count = len(rows) - 1  # subtract header row

                if data_row_count >= EXPECTED_TOTAL_RECORDS and has_source_col and has_summary_sheet:
                    print(f"PASS: Component 1 — consolidated.ods has {len(sheet_names)} sheets, "
                          f"{data_row_count} data rows, 'Source' column present (0.25 pts)")
                    total_score += 0.25
                else:
                    details = []
                    if data_row_count < EXPECTED_TOTAL_RECORDS:
                        details.append(f"only {data_row_count} data rows (expected {EXPECTED_TOTAL_RECORDS})")
                    if not has_source_col:
                        details.append("missing 'Source' column in Data sheet")
                    if not has_summary_sheet:
                        details.append("missing 'Summary' sheet")
                    print(f"FAIL: Component 1 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Summary sheet has correct aggregation values (0.25 pts)
    # Grand Total = 1242280.0, Total Records = 33
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(CONSOLIDATED_ODS):
            print("FAIL: Component 2 — consolidated.ods does not exist")
        else:
            from odf.opendocument import load
            import odf.table as odf_table
            from odf.text import P

            doc = load(CONSOLIDATED_ODS)
            sheets = doc.spreadsheet.getElementsByType(odf_table.Table)
            summary_sheet = next((s for s in sheets if s.getAttribute('name') == 'Summary'), None)

            if summary_sheet is None:
                print("FAIL: Component 2 — 'Summary' sheet not found in consolidated.ods")
            else:
                rows = summary_sheet.getElementsByType(odf_table.TableRow)

                # Read all label-value pairs from Summary sheet
                summary_data = {}
                for row in rows:
                    cells = row.getElementsByType(odf_table.TableCell)
                    cell_vals = []
                    for cell in cells:
                        val = ''
                        for p in cell.getElementsByType(P):
                            val += p.firstChild.data if p.firstChild else ''
                        cell_vals.append(val.strip())
                    if len(cell_vals) >= 2 and cell_vals[0] and cell_vals[1]:
                        summary_data[cell_vals[0]] = cell_vals[1]

                print(f"INFO: Summary sheet data: {summary_data}")

                # Check Grand Total Amount and Total Records
                grand_total_matches = any(
                    'grand total' in label.lower() and
                    abs(float(value) - EXPECTED_GRAND_TOTAL) < 1.0
                    for label, value in summary_data.items()
                    if value.replace('.', '').replace('-', '').isdigit() or
                    (value.count('.') <= 1 and value.replace('.', '').isdigit())
                )
                total_records_matches = any(
                    'total record' in label.lower() and
                    int(float(value)) == EXPECTED_TOTAL_RECORDS
                    for label, value in summary_data.items()
                    if value.replace('.', '').isdigit()
                )

                if grand_total_matches and total_records_matches:
                    print(f"PASS: Component 2 — Summary sheet Grand Total={EXPECTED_GRAND_TOTAL}, "
                          f"Total Records={EXPECTED_TOTAL_RECORDS} (0.25 pts)")
                    total_score += 0.25
                else:
                    details = []
                    if not grand_total_matches:
                        details.append(f"Grand Total not found or incorrect (expected {EXPECTED_GRAND_TOTAL})")
                    if not total_records_matches:
                        details.append(f"Total Records not found or incorrect (expected {EXPECTED_TOTAL_RECORDS})")
                    print(f"FAIL: Component 2 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: summary_report.odt exists and contains real data values (0.15 pts)
    # Must contain actual numeric values from consolidated data, not template placeholders
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(SUMMARY_REPORT_ODT):
            print("FAIL: Component 3 — summary_report.odt does not exist")
        else:
            from odf.opendocument import load
            from odf.text import P

            doc = load(SUMMARY_REPORT_ODT)
            all_text = ''
            for para in doc.getElementsByType(P):
                for node in para.childNodes:
                    if node.nodeType == node.TEXT_NODE:
                        all_text += node.data
                    elif hasattr(node, 'childNodes'):
                        for child in node.childNodes:
                            if child.nodeType == child.TEXT_NODE:
                                all_text += child.data

            print(f"INFO: summary_report.odt text (first 500 chars): {all_text[:500]}")

            # Check for actual data values from the consolidated data
            has_grand_total = str(int(EXPECTED_GRAND_TOTAL)) in all_text
            has_record_count = str(EXPECTED_TOTAL_RECORDS) in all_text
            # Check it's not just a template (no PLACEHOLDER-style content)
            has_placeholder = '{{' in all_text or '[[' in all_text or 'PLACEHOLDER' in all_text.upper()

            if has_grand_total and has_record_count and not has_placeholder:
                print(f"PASS: Component 3 — summary_report.odt contains real data values "
                      f"(Grand Total found, record count found) (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not has_grand_total:
                    details.append(f"Grand Total value {int(EXPECTED_GRAND_TOTAL)} not found in report")
                if not has_record_count:
                    details.append(f"Total record count '{EXPECTED_TOTAL_RECORDS}' not found in report")
                if has_placeholder:
                    details.append("Report contains template placeholders (not filled)")
                print(f"FAIL: Component 3 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Both PDF exports exist and have non-trivial size (0.20 pts)
    # consolidated.pdf and summary_report.pdf must both exist with size > 5KB
    # -----------------------------------------------------------------------
    try:
        MIN_PDF_SIZE = 5000  # 5KB minimum for a real PDF

        consolidated_pdf_size = os.path.getsize(CONSOLIDATED_PDF) if os.path.exists(CONSOLIDATED_PDF) else 0
        summary_report_pdf_size = os.path.getsize(SUMMARY_REPORT_PDF) if os.path.exists(SUMMARY_REPORT_PDF) else 0

        if consolidated_pdf_size > MIN_PDF_SIZE:
            print(f"PASS: consolidated.pdf exists, size={consolidated_pdf_size} bytes")
        elif consolidated_pdf_size > 0:
            print(f"FAIL: consolidated.pdf too small: {consolidated_pdf_size} bytes (min {MIN_PDF_SIZE})")
        else:
            print("FAIL: consolidated.pdf does not exist")

        if summary_report_pdf_size > MIN_PDF_SIZE:
            print(f"PASS: summary_report.pdf exists, size={summary_report_pdf_size} bytes")
        elif summary_report_pdf_size > 0:
            print(f"FAIL: summary_report.pdf too small: {summary_report_pdf_size} bytes (min {MIN_PDF_SIZE})")
        else:
            print("FAIL: summary_report.pdf does not exist")

        if consolidated_pdf_size > MIN_PDF_SIZE and summary_report_pdf_size > MIN_PDF_SIZE:
            print(f"PASS: Component 4 — both PDF exports exist with adequate size (0.20 pts)")
            total_score += 0.20
        elif consolidated_pdf_size > MIN_PDF_SIZE or summary_report_pdf_size > MIN_PDF_SIZE:
            print(f"PARTIAL: Component 4 — only one PDF export found/valid (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 4 — no valid PDF exports found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: completion_log.txt on Desktop with required content (0.15 pts)
    # Must contain: timestamp, file sizes of output files, discrepancy report
    # Partial credit: 0.05 per sub-check (timestamp, file info, discrepancy/status)
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(COMPLETION_LOG):
            print("FAIL: Component 5 — completion_log.txt not found on Desktop")
        else:
            with open(COMPLETION_LOG, 'r') as f:
                log_content = f.read()

            print(f"INFO: completion_log.txt content:\n{log_content}")

            # Required elements in the log
            has_timestamp = ('timestamp' in log_content.lower() or
                             '2025' in log_content or '2026' in log_content)
            has_file_info = ('bytes' in log_content.lower() or
                             'consolidated.ods' in log_content or
                             'summary_report' in log_content)
            has_validation_info = ('discrepanc' in log_content.lower() or
                                   'validation' in log_content.lower() or
                                   'complete' in log_content.lower() or
                                   'pass' in log_content.lower())

            score_comp5 = 0.0
            if has_timestamp:
                score_comp5 += 0.05
                print("PASS: completion_log.txt has timestamp")
            else:
                print("FAIL: completion_log.txt missing timestamp")

            if has_file_info:
                score_comp5 += 0.05
                print("PASS: completion_log.txt references output files/sizes")
            else:
                print("FAIL: completion_log.txt missing output file information")

            if has_validation_info:
                score_comp5 += 0.05
                print("PASS: completion_log.txt contains discrepancy/completion info")
            else:
                print("FAIL: completion_log.txt missing discrepancy/completion info")

            if score_comp5 > 0:
                print(f"PASS: Component 5 — completion_log.txt: {score_comp5:.2f} pts")
                total_score += score_comp5
            else:
                print("FAIL: Component 5 — completion_log.txt missing all required content")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Run the verification
verify_task()
