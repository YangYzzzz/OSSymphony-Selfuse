"""
Reward Script: Comprehensive Expense Audit
Task ID: osworld_multi_apps_doc_pdf_calc_008
Domain: libreoffice_calc + libreoffice_writer (multi-app)

Task: Process 6 PDF receipts, fill expense_budget.ods with actual data,
categorize and flag over-budget categories in red, and write a financial
summary report in expense_audit_report.odt.

Scoring rubric:
  Component 1: ODS Actual column filled with correct values      (0.35 pts)
  Component 2: ODS Variance column correct                       (0.15 pts)
  Component 3: ODS Over_Budget column correct (YES/NO + red)     (0.20 pts)
  Component 4: ODT report exists with title                      (0.10 pts)
  Component 5: ODT report has comparison table with data         (0.15 pts)
  Component 6: ODT report mentions over-budget categories        (0.05 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_pdf_calc_008'

# Ground truth from task context
EXPECTED_ACTUALS = {
    'Travel': 1875,
    'Software': 625,
    'Office': 287,
    'Food': 445,
    'Marketing': 1820,
    'Training': 540,
}

EXPECTED_BUDGETS = {
    'Travel': 2000,
    'Software': 500,
    'Office': 300,
    'Food': 400,
    'Marketing': 1500,
    'Training': 600,
}

# Over-budget categories (actual > budget)
OVER_BUDGET_CATS = {'Software', 'Food', 'Marketing'}
UNDER_BUDGET_CATS = {'Travel', 'Office', 'Training'}

ODS_PATH = f'{WORKDIR}/Desktop/expense_budget.ods'
ODT_PATH = f'{WORKDIR}/Documents/expense_audit_report.odt'

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def get_cell_text(cell):
    """Extract visible text from an ODS/ODT table cell."""
    parts = []
    for p in cell.findall('.//text:p', NS):
        txt = ''.join(p.itertext()).strip()
        if txt:
            parts.append(txt)
    return ' '.join(parts).strip()


def get_cell_value(cell):
    """Extract numeric value from an ODS table cell (office:value attribute)."""
    val = cell.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value')
    if val is not None:
        try:
            return float(val)
        except ValueError:
            pass
    # Fallback: parse text
    txt = get_cell_text(cell)
    try:
        return float(txt.replace(',', ''))
    except ValueError:
        return None


def get_cell_style(cell):
    """Return the style name of an ODS table cell."""
    return cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', '')


def parse_ods(path):
    """Parse ODS file, return list of rows (each row is list of cells as dicts)."""
    with zipfile.ZipFile(path, 'r') as z:
        content = z.read('content.xml')
    root = ET.fromstring(content)

    spreadsheet = root.find('.//office:spreadsheet', NS)
    tables = spreadsheet.findall('table:table', NS)
    if not tables:
        return None, None

    table = tables[0]
    rows_data = []
    for row in table.findall('table:table-row', NS):
        cells = row.findall('table:table-cell', NS)
        row_data = []
        for cell in cells:
            row_data.append({
                'text': get_cell_text(cell),
                'value': get_cell_value(cell),
                'style': get_cell_style(cell),
            })
        rows_data.append(row_data)
    return root, rows_data


def get_auto_styles(root):
    """Return dict of style_name -> dict of properties."""
    styles = {}
    for style_el in root.findall('.//office:automatic-styles/style:style', NS):
        name = style_el.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', '')
        props = {}
        for tp in style_el.findall('style:text-properties', NS):
            color = tp.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}color')
            fw = tp.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-weight')
            if color:
                props['color'] = color.upper()
            if fw:
                props['font-weight'] = fw
        styles[name] = props
    return styles


def verify_task():
    total_score = 0.0

    # ===== COMPONENT 1: ODS Actual column filled with correct values (0.35 pts) =====
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: expense_budget.ods not found at {ODS_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        root_ods, rows = parse_ods(ODS_PATH)
        if rows is None or len(rows) < 2:
            print("FAIL: ODS has no data rows")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        # Build category->row mapping (skip header row 0)
        cat_rows = {}
        for row in rows[1:]:
            if len(row) >= 1 and row[0]['text']:
                cat = row[0]['text'].strip()
                cat_rows[cat] = row

        # Check Actual column (index 2) values
        actual_correct_count = 0
        for cat, expected_actual in EXPECTED_ACTUALS.items():
            row = cat_rows.get(cat)
            if row is None:
                print(f"FAIL Component 1: Category '{cat}' not found in ODS")
                continue
            if len(row) < 3:
                print(f"FAIL Component 1: Row for '{cat}' has fewer than 3 columns")
                continue
            actual_val = row[2]['value']
            if actual_val is not None and abs(actual_val - expected_actual) < 1.0:
                actual_correct_count += 1
                print(f"PASS Component 1 ({cat}): Actual={actual_val} (expected {expected_actual})")
            else:
                print(f"FAIL Component 1 ({cat}): Actual={actual_val} (expected {expected_actual})")

        if actual_correct_count == len(EXPECTED_ACTUALS):
            print(f"PASS: Component 1 — All {len(EXPECTED_ACTUALS)} Actual values correct (0.35 pts)")
            total_score += 0.35
        elif actual_correct_count >= 4:
            print(f"PARTIAL: Component 1 — {actual_correct_count}/{len(EXPECTED_ACTUALS)} Actual values correct (0.20 pts)")
            total_score += 0.20
        elif actual_correct_count >= 2:
            print(f"PARTIAL: Component 1 — {actual_correct_count}/{len(EXPECTED_ACTUALS)} Actual values correct (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Only {actual_correct_count}/{len(EXPECTED_ACTUALS)} Actual values correct")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ===== COMPONENT 2: ODS Variance column correct (0.15 pts) =====
    try:
        # Expected variance = budget - actual (positive = under budget, negative = over)
        EXPECTED_VARIANCES = {
            cat: EXPECTED_BUDGETS[cat] - EXPECTED_ACTUALS[cat]
            for cat in EXPECTED_ACTUALS
        }
        variance_correct_count = 0
        for cat, expected_var in EXPECTED_VARIANCES.items():
            row = cat_rows.get(cat)
            if row is None or len(row) < 4:
                continue
            var_val = row[3]['value']
            if var_val is not None and abs(var_val - expected_var) < 1.0:
                variance_correct_count += 1
                print(f"PASS Component 2 ({cat}): Variance={var_val} (expected {expected_var})")
            else:
                print(f"FAIL Component 2 ({cat}): Variance={var_val} (expected {expected_var})")

        if variance_correct_count == len(EXPECTED_VARIANCES):
            print(f"PASS: Component 2 — All {len(EXPECTED_VARIANCES)} Variance values correct (0.15 pts)")
            total_score += 0.15
        elif variance_correct_count >= 4:
            print(f"PARTIAL: Component 2 — {variance_correct_count}/{len(EXPECTED_VARIANCES)} Variance values correct (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 2 — Only {variance_correct_count}/{len(EXPECTED_VARIANCES)} Variance values correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ===== COMPONENT 3: ODS Over_Budget column correct with YES/NO + red styling (0.20 pts) =====
    try:
        auto_styles = get_auto_styles(root_ods)

        over_budget_correct_count = 0
        red_correct_count = 0
        for cat in EXPECTED_ACTUALS:
            row = cat_rows.get(cat)
            if row is None or len(row) < 5:
                continue
            ob_cell = row[4]
            ob_text = ob_cell['text'].strip().upper()
            ob_style = ob_cell['style']

            is_over = cat in OVER_BUDGET_CATS
            expected_text = 'YES' if is_over else 'NO'

            if ob_text == expected_text:
                over_budget_correct_count += 1
                print(f"PASS Component 3 ({cat}): Over_Budget='{ob_text}' (expected '{expected_text}')")

                # Check red styling for YES cells
                if is_over:
                    style_props = auto_styles.get(ob_style, {})
                    color = style_props.get('color', '')
                    if '#FF0000' in color or 'FF0000' in color:
                        red_correct_count += 1
                        print(f"PASS Component 3 ({cat}): Red styling confirmed for YES cell")
                    else:
                        print(f"FAIL Component 3 ({cat}): YES cell lacks red styling (style='{ob_style}', color='{color}')")
            else:
                print(f"FAIL Component 3 ({cat}): Over_Budget='{ob_text}' (expected '{expected_text}')")

        all_cats = len(EXPECTED_ACTUALS)
        if over_budget_correct_count == all_cats and red_correct_count == len(OVER_BUDGET_CATS):
            print(f"PASS: Component 3 — All Over_Budget values correct with red styling (0.20 pts)")
            total_score += 0.20
        elif over_budget_correct_count == all_cats:
            print(f"PARTIAL: Component 3 — All YES/NO correct but {red_correct_count}/{len(OVER_BUDGET_CATS)} red styling (0.12 pts)")
            total_score += 0.12
        elif over_budget_correct_count >= 4:
            print(f"PARTIAL: Component 3 — {over_budget_correct_count}/{all_cats} Over_Budget values correct (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 3 — Only {over_budget_correct_count}/{all_cats} Over_Budget values correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ===== COMPONENT 4: ODT report exists with title (0.10 pts) =====
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 4 — expense_audit_report.odt not found at {ODT_PATH}")
        else:
            with zipfile.ZipFile(ODT_PATH, 'r') as z:
                odt_content = z.read('content.xml').decode('utf-8')

            # Check for title-like content (case-insensitive)
            odt_lower = odt_content.lower()
            has_report_title = 'expense' in odt_lower and ('audit' in odt_lower or 'report' in odt_lower)
            if has_report_title:
                print(f"PASS: Component 4 — ODT report exists with expense audit title (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — ODT report exists but lacks 'expense audit/report' title content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ===== COMPONENT 5: ODT report has comparison table with correct data (0.15 pts) =====
    try:
        if os.path.exists(ODT_PATH):
            with zipfile.ZipFile(ODT_PATH, 'r') as z:
                odt_content_bytes = z.read('content.xml')
            odt_root = ET.fromstring(odt_content_bytes)

            # Find all tables in ODT
            tables = odt_root.findall('.//table:table', NS)
            if not tables:
                print("FAIL: Component 5 — No table found in ODT report")
            else:
                # Check table has at least 6 data rows (one per category)
                table = tables[0]
                table_rows = table.findall('table:table-row', NS)
                row_count = len(table_rows)

                # Extract all text from the table
                table_text = ' '.join(
                    ' '.join(cell.itertext())
                    for row in table_rows
                    for cell in row.findall('table:table-cell', NS)
                ).lower()

                # Check for key categories present in table
                cats_found = sum(1 for cat in EXPECTED_ACTUALS if cat.lower() in table_text)

                # Check for key actual values in table
                vals_found = sum(1 for val in EXPECTED_ACTUALS.values() if str(val) in table_text)

                if row_count >= 7 and cats_found >= 5 and vals_found >= 4:
                    print(f"PASS: Component 5 — ODT comparison table: {row_count} rows, {cats_found}/6 categories, {vals_found}/6 values (0.15 pts)")
                    total_score += 0.15
                elif cats_found >= 4 and vals_found >= 3:
                    print(f"PARTIAL: Component 5 — ODT table partial: {row_count} rows, {cats_found}/6 cats, {vals_found}/6 vals (0.08 pts)")
                    total_score += 0.08
                else:
                    print(f"FAIL: Component 5 — ODT table incomplete: {row_count} rows, {cats_found}/6 cats, {vals_found}/6 vals")
        else:
            print("FAIL: Component 5 — ODT file not found, skipping table check")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ===== COMPONENT 6: ODT report mentions over-budget categories (0.05 pts) =====
    try:
        if os.path.exists(ODT_PATH):
            with zipfile.ZipFile(ODT_PATH, 'r') as z:
                odt_text = z.read('content.xml').decode('utf-8').lower()

            # Check that the over-budget categories are mentioned in audit text
            over_budget_mentioned = sum(
                1 for cat in OVER_BUDGET_CATS if cat.lower() in odt_text
            )
            # Also check for recommendation keywords
            has_recommendations = any(
                kw in odt_text for kw in ['recommend', 'action', 'corrective', 'review', 'limit']
            )

            if over_budget_mentioned == len(OVER_BUDGET_CATS) and has_recommendations:
                print(f"PASS: Component 6 — All {len(OVER_BUDGET_CATS)} over-budget categories mentioned + recommendations (0.05 pts)")
                total_score += 0.05
            elif over_budget_mentioned >= 2:
                print(f"PARTIAL: Component 6 — {over_budget_mentioned}/{len(OVER_BUDGET_CATS)} over-budget categories mentioned (0.03 pts)")
                total_score += 0.03
            else:
                print(f"FAIL: Component 6 — Only {over_budget_mentioned}/{len(OVER_BUDGET_CATS)} over-budget categories mentioned")
        else:
            print("FAIL: Component 6 — ODT file not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
