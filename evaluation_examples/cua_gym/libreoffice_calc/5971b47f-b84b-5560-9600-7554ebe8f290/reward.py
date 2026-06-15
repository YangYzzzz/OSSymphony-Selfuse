"""
Reward Script: Add secondary Y-axis to embedded chart, assign 'Units Sold' to it
Task ID: calc_gg2_002
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): LineChart references a DIFFERENT Y-axis than BarChart (secondary axis)
  Component 2 (0.3): A second valAx exists in chart XML with title containing 'Units Sold'
  Component 3 (0.3): BarChart still uses the original primary Y-axis (Revenue USD unchanged)
"""

import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile

WORKDIR = '/home/user'
TASK_ID = 'calc_gg2_002'

# XML namespace for chart elements
CHART_NS = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
DRAW_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_chart_xml(file_path):
    """Extract chart1.xml content from the xlsx archive."""
    with ZipFile(file_path, 'r') as z:
        chart_files = [f for f in z.namelist() if f.startswith('xl/charts/chart') and f.endswith('.xml')]
        if not chart_files:
            return None
        return z.read(chart_files[0]).decode()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and has a chart
    chart_xml = None
    try:
        chart_xml = get_chart_xml(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read chart from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if chart_xml is None:
        print("CRITICAL: No chart XML found in file")
        print("REWARD: 0.0")
        return 0.0

    # Parse the chart XML
    try:
        root = ET.fromstring(chart_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: find all elements by local name (ignoring namespace)
    def find_all_by_local(element, local_name):
        return [el for el in element.iter() if el.tag.endswith('}' + local_name) or el.tag == local_name]

    # Locate plotArea
    plot_areas = find_all_by_local(root, 'plotArea')
    if not plot_areas:
        print("CRITICAL: No plotArea found in chart")
        print("REWARD: 0.0")
        return 0.0
    plot_area = plot_areas[0]

    # Extract barChart and lineChart axId references
    bar_charts = find_all_by_local(plot_area, 'barChart')
    line_charts = find_all_by_local(plot_area, 'lineChart')

    if not bar_charts:
        print("CRITICAL: No barChart found in plotArea")
        print("REWARD: 0.0")
        return 0.0
    if not line_charts:
        print("CRITICAL: No lineChart found in plotArea")
        print("REWARD: 0.0")
        return 0.0

    # Get axId values for barChart and lineChart
    def get_ax_ids(chart_element):
        """Get all axId values directly under a chart element."""
        ax_ids = []
        for child in chart_element:
            if child.tag.endswith('}axId') or child.tag == 'axId':
                val = child.get('val')
                if val:
                    ax_ids.append(val)
        return ax_ids

    bar_ax_ids = get_ax_ids(bar_charts[0])
    line_ax_ids = get_ax_ids(line_charts[0])

    print(f"INFO: barChart axIds = {bar_ax_ids}")
    print(f"INFO: lineChart axIds = {line_ax_ids}")

    # Get all valAx elements in plotArea
    val_axes = find_all_by_local(plot_area, 'valAx')
    val_ax_info = []
    for vax in val_axes:
        ax_id_els = find_all_by_local(vax, 'axId')
        ax_id = ax_id_els[0].get('val') if ax_id_els else None
        # Get title text
        title_text = ''
        title_els = find_all_by_local(vax, 'title')
        if title_els:
            t_els = find_all_by_local(title_els[0], 't')
            if t_els:
                title_text = t_els[0].text or ''
        val_ax_info.append({'axId': ax_id, 'title': title_text})

    print(f"INFO: valAx elements: {val_ax_info}")

    # ---- Component 1 (0.4 pts): LineChart references a DIFFERENT Y-axis than BarChart ----
    # In initial: both barChart and lineChart share the same valAx (axId=100).
    # In golden: lineChart uses a new axId (200) different from barChart's valAx.
    try:
        # The barChart should have a catAx and a valAx reference.
        # The lineChart should have the SAME catAx but a DIFFERENT valAx.
        # We compare the valAx references (non-catAx axId) between bar and line.
        # The catAx is typically the lower-valued axId shared by both.
        # We look for the axId that differs.
        bar_set = set(bar_ax_ids)
        line_set = set(line_ax_ids)

        # Both should share the catAx. The valAx should differ.
        shared = bar_set & line_set
        bar_only = bar_set - line_set
        line_only = line_set - bar_set

        if line_only and bar_only:
            # They have at least one different axId each -> secondary axis exists
            print(f"PASS: Component 1 -- lineChart has unique axId(s) {line_only} vs barChart {bar_only} (0.4 pts)")
            total_score += 0.4
        elif line_only:
            # Line has extra axId not in bar
            print(f"PASS: Component 1 -- lineChart references different axId {line_only} (0.4 pts)")
            total_score += 0.4
        else:
            # Both share all axIds - no secondary axis
            print(f"FAIL: Component 1 -- barChart and lineChart share identical axIds {bar_set}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ---- Component 2 (0.3 pts): A second valAx exists with title containing 'Units Sold' ----
    try:
        # In initial: only 1 valAx. In golden: 2 valAx elements, one titled 'Units Sold'.
        units_sold_axes = [vax for vax in val_ax_info if 'units sold' in vax['title'].lower()]

        if len(val_ax_info) >= 2 and len(units_sold_axes) >= 1:
            print(f"PASS: Component 2 -- Found {len(val_ax_info)} valAx elements, secondary titled '{units_sold_axes[0]['title']}' (0.3 pts)")
            total_score += 0.3
        elif len(val_ax_info) >= 2:
            # Two axes but no 'Units Sold' title -> partial (0.15)
            print(f"PARTIAL: Component 2 -- Found {len(val_ax_info)} valAx elements but none titled 'Units Sold' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Only {len(val_ax_info)} valAx element(s) found, expected 2")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---- Component 3 (0.3 pts): BarChart still uses original primary Y-axis ----
    # The barChart should still reference the original primary valAx (the one titled 'Revenue (USD)')
    try:
        # Find the valAx with 'Revenue' in its title
        revenue_axes = [vax for vax in val_ax_info if 'revenue' in vax['title'].lower()]

        if revenue_axes:
            revenue_ax_id = revenue_axes[0]['axId']
            # Check that barChart references this axId
            if revenue_ax_id in bar_ax_ids:
                # Additionally confirm barChart does NOT reference the secondary axis
                # (barChart should not have been moved to secondary)
                if units_sold_axes := [vax for vax in val_ax_info if 'units sold' in vax['title'].lower()]:
                    secondary_id = units_sold_axes[0]['axId']
                    if secondary_id not in bar_ax_ids:
                        print(f"PASS: Component 3 -- barChart uses primary axis '{revenue_axes[0]['title']}' (axId={revenue_ax_id}), not secondary (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 3 -- barChart also references secondary axis {secondary_id}")
                else:
                    # No secondary axis found but barChart still on revenue axis
                    # This is a partial pass since bar is on correct axis
                    print(f"FAIL: Component 3 -- No secondary axis to compare against")
            else:
                print(f"FAIL: Component 3 -- barChart does not reference Revenue axis (axId={revenue_ax_id})")
        else:
            print(f"FAIL: Component 3 -- No valAx with 'Revenue' title found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_calc")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
