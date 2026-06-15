"""
Reward Script: Create a combination chart (bar + line) for monthly sales and profit margin
Task ID: calc_chart_combo_bar_line_015
Domain: libreoffice_calc

Scoring rubric:
  Component 1: Combo chart exists on 'Performance' sheet (both barChart and lineChart) — 0.30 pts
  Component 2: Correct data series — bar uses Sales (B2:B7), line uses Profit Margin (C2:C7) — 0.30 pts
  Component 3: Chart title is 'Monthly Sales and Profit Margin' — 0.20 pts
  Component 4: Legend is present in the chart — 0.20 pts
  Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'calc_chart_combo_bar_line_015'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid xlsx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load workbook {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Performance' sheet must exist
    if 'Performance' not in wb.sheetnames:
        print("CRITICAL: 'Performance' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Performance']

    # Read the raw XML from the xlsx zip to accurately inspect chart structure
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            chart_files = [f for f in zf.namelist() if f.startswith('xl/charts/') and f.endswith('.xml')]
            if not chart_files:
                chart_xml_map = {}
            else:
                chart_xml_map = {cf: zf.read(cf).decode('utf-8') for cf in chart_files}
    except Exception as e:
        print(f"ERROR: Cannot read xlsx zip contents: {e}")
        chart_xml_map = {}

    # Combine all chart XMLs for multi-chart files
    all_chart_xml = ' '.join(chart_xml_map.values())

    # --------------------------------------------------------------------------
    # Component 1: Combo chart exists — both barChart AND lineChart present (0.30 pts)
    # This FAILS on initial (0 charts) and PASSES on golden (combo chart with both types)
    # --------------------------------------------------------------------------
    try:
        # Check via openpyxl that at least one chart exists on the sheet
        num_charts = len(ws._charts)
        has_bar_element = '<barChart>' in all_chart_xml
        has_line_element = '<lineChart>' in all_chart_xml

        if num_charts >= 1 and has_bar_element and has_line_element:
            print(f"PASS: Component 1 — Combo chart found with barChart and lineChart (0.30 pts)")
            total_score += 0.30
        elif num_charts == 0:
            print(f"FAIL: Component 1 — No charts found on 'Performance' sheet")
        elif not has_bar_element:
            print(f"FAIL: Component 1 — Chart exists but no barChart element found (not a combo chart)")
        elif not has_line_element:
            print(f"FAIL: Component 1 — Chart has barChart but no lineChart element (not a combo chart)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --------------------------------------------------------------------------
    # Component 2: Correct data series — bar uses Sales data, line uses Profit Margin data (0.30 pts)
    # Bar series should reference B column (Sales), line series should reference C column (Profit Margin)
    # Category axis should reference A2:A7 (months)
    # --------------------------------------------------------------------------
    try:
        # Extract barChart and lineChart sections from XML
        if '<barChart>' in all_chart_xml and '<lineChart>' in all_chart_xml:
            bar_section = all_chart_xml.split('<barChart>')[1].split('</barChart>')[0]
            line_section = all_chart_xml.split('<lineChart>')[1].split('</lineChart>')[0]

            # Bar chart: should reference Sales data in column B (rows 2-7)
            # Accept both $B$2:$B$7 and B2:B7 style references
            bar_has_sales = ('$B$2:$B$7' in bar_section or "'Performance'!B2:B7" in bar_section)
            # Line chart: should reference Profit Margin data in column C (rows 2-7)
            line_has_margin = ('$C$2:$C$7' in line_section or "'Performance'!C2:C7" in line_section)
            # Either section should reference months in column A (rows 2-7) as categories
            cat_has_months = ('$A$2:$A$7' in all_chart_xml or "'Performance'!A2:A7" in all_chart_xml)

            if bar_has_sales and line_has_margin and cat_has_months:
                print(f"PASS: Component 2 — Bar series references Sales (B2:B7), Line series references Profit Margin (C2:C7), categories reference months (A2:A7) (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not bar_has_sales:
                    missing.append("bar series does not reference Sales column B (rows 2-7)")
                if not line_has_margin:
                    missing.append("line series does not reference Profit Margin column C (rows 2-7)")
                if not cat_has_months:
                    missing.append("categories do not reference Month column A (rows 2-7)")
                print(f"FAIL: Component 2 — {'; '.join(missing)}")
        else:
            print(f"FAIL: Component 2 — Cannot verify series data (missing barChart or lineChart element)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --------------------------------------------------------------------------
    # Component 3: Chart title is 'Monthly Sales and Profit Margin' (0.20 pts)
    # --------------------------------------------------------------------------
    try:
        expected_title = 'Monthly Sales and Profit Margin'
        if expected_title in all_chart_xml:
            print(f"PASS: Component 3 — Chart title '{expected_title}' found (0.20 pts)")
            total_score += 0.20
        else:
            # Try openpyxl chart title extraction
            title_found = False
            for chart in ws._charts:
                try:
                    title_text = chart.title.tx.rich.p[0].r[0].t
                    if title_text and expected_title.lower() in title_text.lower():
                        title_found = True
                        break
                except Exception:
                    pass
            if title_found:
                print(f"PASS: Component 3 — Chart title '{expected_title}' found via openpyxl (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Expected chart title '{expected_title}' not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --------------------------------------------------------------------------
    # Component 4: Legend is present (0.20 pts)
    # --------------------------------------------------------------------------
    try:
        has_legend = '<legend>' in all_chart_xml

        if has_legend:
            print(f"PASS: Component 4 — Legend is present in the chart (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No legend found in the chart")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
