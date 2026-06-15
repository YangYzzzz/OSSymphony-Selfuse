"""
Reward Script: Audit a vendor's billing accuracy — ODS audit log + ODT report
Task ID: osworld_multi_apps_doc_pdf_calc_010
Domain: libreoffice_calc + libreoffice_writer (multi-app)
Scoring Rubric:
  Component 1: audit_log.ods has all 7 months filled with numeric data       (0.30 pts)
  Component 2: Exactly 3 ERROR rows identified + red highlight on error rows  (0.20 pts)
  Component 3: Summary row has correct total discrepancy (~826.65)            (0.20 pts)
  Component 4: audit_report.odt exists in Documents/                         (0.15 pts)
  Component 5: audit_report.odt mentions total overbilling ~826.65           (0.15 pts)
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_pdf_calc_010'

AUDIT_LOG_PATH = f'{WORKDIR}/Desktop/audit_log.ods'
AUDIT_REPORT_PATH = f'{WORKDIR}/Documents/audit_report.odt'

# ODS/ODT XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

def read_ods_content_xml(path):
    """Read and return the content.xml from an ODS/ODT file."""
    with zipfile.ZipFile(path, 'r') as z:
        return z.read('content.xml').decode('utf-8')

def parse_ods_rows(content_xml_str):
    """
    Parse ODS content.xml and return list of rows.
    Each row is a list of (cell_value, style_name) tuples.
    """
    root = ET.fromstring(content_xml_str)
    rows = []
    # Find the table
    spreadsheet = root.find('.//office:spreadsheet', NS)
    if spreadsheet is None:
        return rows
    table = spreadsheet.find('table:table', NS)
    if table is None:
        return rows
    for row_el in table.findall('table:table-row', NS):
        row = []
        for cell_el in row_el.findall('table:table-cell', NS):
            style = cell_el.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', '')
            # Get cell value
            val_type = cell_el.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value-type', '')
            val = cell_el.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value', None)
            text_el = cell_el.find('text:p', NS)
            text_val = text_el.text if text_el is not None and text_el.text else ''
            if val is not None:
                try:
                    cell_value = float(val)
                except ValueError:
                    cell_value = text_val
            elif text_val:
                cell_value = text_val
            else:
                cell_value = None
            row.append((cell_value, style))
        rows.append(row)
    return rows

def get_style_bgcolor(content_xml_str, style_name):
    """Extract background color for a given style name from ODS content.xml."""
    root = ET.fromstring(content_xml_str)
    auto_styles = root.find('office:automatic-styles', NS)
    if auto_styles is None:
        return None
    for style_el in auto_styles.findall('style:style', NS):
        sn = style_el.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', '')
        if sn == style_name:
            tc_props = style_el.find('style:table-cell-properties', NS)
            if tc_props is not None:
                return tc_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}background-color', None)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: audit_log.ods must exist ----
    if not os.path.exists(AUDIT_LOG_PATH):
        print(f"CRITICAL: audit_log.ods not found at {AUDIT_LOG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ods_content = read_ods_content_xml(AUDIT_LOG_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot read audit_log.ods: {e}")
        print("REWARD: 0.0")
        return 0.0

    rows = parse_ods_rows(ods_content)
    # rows[0] = header, rows[1..7] = Jan-Jul, rows[8] = summary
    print(f"INFO: audit_log.ods has {len(rows)} rows (expected 9: 1 header + 7 months + 1 summary)")

    # ---- Component 1: All 7 month rows filled with numeric data (0.30 points) ----
    # The initial log has all month rows with only the month-name text, all numeric cells empty.
    # In the golden log, rows 1-7 (0-indexed) have numeric data in columns 2-10 (Units, prices, etc.)
    try:
        data_rows = rows[1:8]  # rows for Jan through Jul (7 rows)
        filled_count = 0
        for row in data_rows:
            # Check that at least columns 1 (Units) and 7 (Expected_Total) have numeric values
            # row indices: 0=Invoice_Month, 1=Units, 2=Unit_Price, 3=Exp_Sub, 4=Inv_Sub,
            #              5=Exp_Tax, 6=Inv_Tax, 7=Exp_Total, 8=Inv_Total, 9=Disc, 10=Status
            has_units = len(row) > 1 and row[1][0] is not None and isinstance(row[1][0], (int, float))
            has_exp_total = len(row) > 7 and row[7][0] is not None and isinstance(row[7][0], (int, float))
            has_status = len(row) > 10 and row[10][0] is not None and str(row[10][0]).strip() in ('OK', 'ERROR')
            if has_units and has_exp_total and has_status:
                filled_count += 1
        if filled_count == 7:
            print(f"PASS: Component 1 — All 7 month rows filled with numeric data and status (0.30 pts)")
            total_score += 0.30
        elif filled_count >= 4:
            print(f"PARTIAL: Component 1 — Only {filled_count}/7 rows fully filled (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Only {filled_count}/7 rows filled; expected 7")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Exactly 3 ERROR rows with red background (0.20 points) ----
    # The initial log has no ERROR status rows. The golden log has 3 ERROR rows (Feb, May, Jun)
    # with red background highlight.
    try:
        error_rows = []
        error_row_months = []
        expected_error_months = {'February 2025', 'May 2025', 'June 2025'}
        for row in data_rows:
            if len(row) > 10 and row[10][0] is not None and str(row[10][0]).strip() == 'ERROR':
                month_name = str(row[0][0]).strip() if row[0][0] else ''
                error_rows.append(row)
                error_row_months.append(month_name)

        # Check red highlight on error rows
        red_highlight_count = 0
        for row in error_rows:
            # Check if any numeric cell in the row has a style that maps to red background
            for cell_val, style_name in row[1:]:  # skip month-name cell (col 0)
                bg_color = get_style_bgcolor(ods_content, style_name)
                if bg_color and bg_color.lower() in ('#ff0000', '#ff0000'):
                    red_highlight_count += 1
                    break  # at least one red cell in this row — count the row

        found_error_months = set(error_row_months)
        correct_months = found_error_months == expected_error_months
        correct_count = len(error_rows) == 3

        if correct_count and correct_months and red_highlight_count >= 3:
            print(f"PASS: Component 2 — 3 ERROR rows (Feb, May, Jun) with red highlighting (0.20 pts)")
            total_score += 0.20
        elif correct_count and correct_months:
            print(f"PARTIAL: Component 2 — 3 correct ERROR rows but red highlighting missing/partial ({red_highlight_count}/3) (0.10 pts)")
            total_score += 0.10
        elif len(error_rows) == 3:
            print(f"PARTIAL: Component 2 — 3 ERROR rows found but months are {found_error_months} vs expected {expected_error_months} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Found {len(error_rows)} ERROR rows (expected 3), months: {found_error_months}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: Summary row with correct total discrepancy ~826.65 (0.20 points) ----
    # The initial log has a TOTAL row with all empty cells.
    # The golden log has a "TOTAL DISCREPANCY" row with 826.65 in the Discrepancy_Amount column.
    # Note: the summary row may have 12 cells (with an extra cell), so we scan all cells for
    # the value 826.65 rather than relying on a fixed column index.
    try:
        summary_row = rows[8] if len(rows) > 8 else None
        if summary_row is None:
            print("FAIL: Component 3 — No summary row found (row index 8)")
        else:
            month_label = str(summary_row[0][0]).strip() if summary_row[0][0] else ''
            has_total_label = 'TOTAL' in month_label.upper()

            # Scan all cells in the summary row for a numeric value ~826.65
            total_disc = None
            for cell_val, cell_style in summary_row:
                if cell_val is not None:
                    try:
                        fval = float(cell_val)
                        if abs(fval - 826.65) < 0.10:
                            total_disc = fval
                            break
                    except (ValueError, TypeError):
                        pass

            if has_total_label and total_disc is not None:
                print(f"PASS: Component 3 — Summary row found with total discrepancy {total_disc} (~826.65) (0.20 pts)")
                total_score += 0.20
            elif has_total_label:
                # Also check if any cell contains the text "826.65"
                text_match = any(str(cell_val) == '826.65' for cell_val, _ in summary_row if cell_val is not None)
                if text_match:
                    print(f"PASS: Component 3 — Summary row found with text '826.65' (0.20 pts)")
                    total_score += 0.20
                else:
                    all_vals = [(v, s) for v, s in summary_row if v is not None]
                    print(f"FAIL: Component 3 — Summary row has TOTAL label but no 826.65 value. Values: {all_vals}")
            else:
                print(f"FAIL: Component 3 — Summary row label='{month_label}', no TOTAL label found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: audit_report.odt exists in Documents/ (0.15 points) ----
    # The initial state has no audit_report.odt in Documents.
    # The golden state has /home/user/Documents/audit_report.odt.
    try:
        if os.path.exists(AUDIT_REPORT_PATH) and os.path.getsize(AUDIT_REPORT_PATH) > 500:
            print(f"PASS: Component 4 — audit_report.odt exists at {AUDIT_REPORT_PATH} (0.15 pts)")
            total_score += 0.15
        elif os.path.exists(AUDIT_REPORT_PATH):
            print(f"FAIL: Component 4 — audit_report.odt exists but is too small ({os.path.getsize(AUDIT_REPORT_PATH)} bytes)")
        else:
            print(f"FAIL: Component 4 — audit_report.odt not found at {AUDIT_REPORT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: audit_report.odt mentions total overbilling ~826.65 (0.15 points) ----
    # The initial state has no audit_report.odt.
    # The golden report mentions "826.65" in the findings summary and recommendations.
    try:
        if os.path.exists(AUDIT_REPORT_PATH):
            odt_content = read_ods_content_xml(AUDIT_REPORT_PATH)
            # Check for key content: total amount and recommendation to dispute
            has_total_amount = '826.65' in odt_content
            has_recommendation = any(kw in odt_content.lower() for kw in ['dispute', 'recommend', 'credit note', 'refund'])
            has_executive_summary = any(kw in odt_content.lower() for kw in ['executive', 'summary', 'findings'])
            has_error_count = '3' in odt_content and any(kw in odt_content.lower() for kw in ['error', 'discrepan'])

            passes = sum([has_total_amount, has_recommendation, has_executive_summary, has_error_count])
            if has_total_amount and has_recommendation and has_executive_summary:
                print(f"PASS: Component 5 — audit_report.odt contains overbilling amount 826.65, recommendations, and exec summary (0.15 pts)")
                total_score += 0.15
            elif has_total_amount:
                print(f"PARTIAL: Component 5 — audit_report.odt contains 826.65 but missing some content (passes={passes}/4) (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 5 — audit_report.odt does not mention 826.65 or key audit content (passes={passes}/4)")
        else:
            print(f"FAIL: Component 5 — audit_report.odt not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
