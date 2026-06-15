"""
Reward Script: Combination chart with bars (Revenue), line (Profit Margin %), area (Cost)
Task ID: calc_gcp_058
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on sheet (0.15)
  Component 2: Three chart sub-types present: barChart, lineChart, areaChart (0.30)
  Component 3: Correct series-to-chart-type mapping (0.25)
  Component 4: Secondary value axis for ProfitMargin% line series (0.15)
  Component 5: Legend present (0.15)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'calc_gcp_058'

NS = {'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be a valid xlsx (zip) with at least one chart XML
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print("CRITICAL: Cannot open {} as zip: {}".format(file_path, e))
        print("REWARD: 0.0")
        return 0.0

    chart_files = [f for f in zf.namelist() if f.startswith('xl/charts/') and f.endswith('.xml')]

    # ---------------------------------------------------------------
    # Component 1: At least one chart exists on the sheet (0.15 pts)
    # Initial env has 0 charts; golden has 1+.
    # ---------------------------------------------------------------
    try:
        if len(chart_files) >= 1:
            print("PASS: Component 1 — Chart file(s) found: {} (0.15 pts)".format(chart_files))
            total_score += 0.15
        else:
            print("FAIL: Component 1 — No chart XML files found in workbook")
    except Exception as e:
        print("ERROR: Component 1 — {}".format(e))

    if len(chart_files) == 0:
        # No chart at all; remaining checks meaningless
        final_score = min(total_score, 1.0)
        print("\nScore: {}/1.0".format(total_score))
        print("REWARD: {}".format(final_score))
        return final_score

    # Parse the first chart XML (combination charts live in a single chart file)
    try:
        chart_xml = zf.read(chart_files[0])
        root = etree.fromstring(chart_xml)
    except Exception as e:
        print("ERROR: Cannot parse chart XML: {}".format(e))
        final_score = min(total_score, 1.0)
        print("\nScore: {}/1.0".format(total_score))
        print("REWARD: {}".format(final_score))
        return final_score

    # Helper: find chart sub-types
    def find_chart_types():
        types_found = {}
        for tag in ['barChart', 'lineChart', 'areaChart', 'pieChart', 'scatterChart']:
            elems = root.findall('.//c:{}'.format(tag), NS)
            if elems:
                types_found[tag] = elems
        return types_found

    chart_types = find_chart_types()

    # ---------------------------------------------------------------
    # Component 2: Three chart sub-types present (0.30 pts)
    # Must have barChart, lineChart, and areaChart in same chart.
    # ---------------------------------------------------------------
    try:
        has_bar = 'barChart' in chart_types
        has_line = 'lineChart' in chart_types
        has_area = 'areaChart' in chart_types
        count_correct = sum([has_bar, has_line, has_area])

        if count_correct == 3:
            print("PASS: Component 2 — All three chart types found: barChart, lineChart, areaChart (0.30 pts)")
            total_score += 0.30
        else:
            missing = []
            if not has_bar:
                missing.append('barChart')
            if not has_line:
                missing.append('lineChart')
            if not has_area:
                missing.append('areaChart')
            print("FAIL: Component 2 — Missing chart types: {}. Found: {}".format(
                missing, list(chart_types.keys())))
    except Exception as e:
        print("ERROR: Component 2 — {}".format(e))

    # ---------------------------------------------------------------
    # Component 3: Correct series-to-chart-type mapping (0.25 pts)
    # Revenue (col B) -> barChart, Cost (col C) -> areaChart,
    # ProfitMargin% (col D) -> lineChart
    # ---------------------------------------------------------------
    try:
        def get_series_refs(chart_elem):
            """Return list of data reference strings for series in this chart element."""
            refs = []
            for ser in chart_elem.findall('c:ser', NS):
                # Check tx (title) strRef
                f_elem = ser.find('.//c:tx/c:strRef/c:f', NS)
                if f_elem is not None:
                    refs.append(f_elem.text)
                else:
                    # Fall back to val ref
                    val_f = ser.find('.//c:val/c:numRef/c:f', NS)
                    if val_f is not None:
                        refs.append(val_f.text)
            return refs

        mapping_score = 0.0
        checks_passed = 0

        # Check barChart has Revenue (column B)
        if has_bar:
            bar_refs = []
            for elem in chart_types['barChart']:
                bar_refs.extend(get_series_refs(elem))
            bar_has_revenue = any('B' in r.upper() for r in bar_refs)
            if bar_has_revenue:
                checks_passed += 1
                print("  Component 3a: barChart references Revenue (B) — correct")
            else:
                print("  Component 3a FAIL: barChart refs={}, expected Revenue (B)".format(bar_refs))

        # Check areaChart has Cost (column C)
        if has_area:
            area_refs = []
            for elem in chart_types['areaChart']:
                area_refs.extend(get_series_refs(elem))
            area_has_cost = any('C' in r.split('!')[-1].upper() for r in area_refs)
            if area_has_cost:
                checks_passed += 1
                print("  Component 3b: areaChart references Cost (C) — correct")
            else:
                print("  Component 3b FAIL: areaChart refs={}, expected Cost (C)".format(area_refs))

        # Check lineChart has ProfitMargin% (column D)
        if has_line:
            line_refs = []
            for elem in chart_types['lineChart']:
                line_refs.extend(get_series_refs(elem))
            line_has_margin = any('D' in r.split('!')[-1].upper() for r in line_refs)
            if line_has_margin:
                checks_passed += 1
                print("  Component 3c: lineChart references ProfitMargin% (D) — correct")
            else:
                print("  Component 3c FAIL: lineChart refs={}, expected ProfitMargin% (D)".format(line_refs))

        if checks_passed == 3:
            print("PASS: Component 3 — All series correctly mapped to chart types (0.25 pts)")
            total_score += 0.25
        elif checks_passed >= 1:
            partial = round(0.25 * checks_passed / 3.0, 2)
            print("PARTIAL: Component 3 — {}/3 mappings correct ({} pts)".format(checks_passed, partial))
            total_score += partial
        else:
            print("FAIL: Component 3 — No correct series-to-chart-type mappings")
    except Exception as e:
        print("ERROR: Component 3 — {}".format(e))

    # ---------------------------------------------------------------
    # Component 4: Secondary value axis for ProfitMargin% line (0.15 pts)
    # The lineChart must use a different valAx than barChart/areaChart.
    # ---------------------------------------------------------------
    try:
        def get_axis_ids(chart_elem):
            return [a.get('val') for a in chart_elem.findall('c:axId', NS)]

        if has_bar and has_line:
            bar_ax_ids = set()
            for elem in chart_types['barChart']:
                bar_ax_ids.update(get_axis_ids(elem))

            line_ax_ids = set()
            for elem in chart_types['lineChart']:
                line_ax_ids.update(get_axis_ids(elem))

            # Both share a catAx, but the valAx should differ
            # Get all valAx IDs
            all_val_axes = root.findall('.//c:valAx/c:axId', NS)
            val_ax_ids = set(a.get('val') for a in all_val_axes)

            # The line chart's value axis should be different from bar chart's value axis
            bar_val_axes = bar_ax_ids.intersection(val_ax_ids)
            line_val_axes = line_ax_ids.intersection(val_ax_ids)

            if len(val_ax_ids) >= 2 and line_val_axes != bar_val_axes:
                print("PASS: Component 4 — Secondary axis detected: bar uses {}, line uses {} (0.15 pts)".format(
                    bar_val_axes, line_val_axes))
                total_score += 0.15
            else:
                print("FAIL: Component 4 — No secondary axis. valAxes={}, bar={}, line={}".format(
                    val_ax_ids, bar_val_axes, line_val_axes))
        else:
            print("FAIL: Component 4 — Cannot check secondary axis (missing bar or line chart)")
    except Exception as e:
        print("ERROR: Component 4 — {}".format(e))

    # ---------------------------------------------------------------
    # Component 5: Legend present (0.15 pts)
    # ---------------------------------------------------------------
    try:
        legend = root.find('.//c:legend', NS)
        if legend is not None:
            print("PASS: Component 5 — Legend present (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 5 — No legend found in chart")
    except Exception as e:
        print("ERROR: Component 5 — {}".format(e))

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
    print("\nScore: {}/1.0".format(total_score))
    print("REWARD: {}".format(final_score))
    return final_score


# Persistence hook — save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
    except Exception as e:
        print("PERSIST_WARN: save hook failed: {}".format(e))


# Entry point
file_path = os.path.join(WORKDIR, '{}.xlsx'.format(TASK_ID))
if not os.path.exists(file_path):
    print("File not found: {}".format(file_path))
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
