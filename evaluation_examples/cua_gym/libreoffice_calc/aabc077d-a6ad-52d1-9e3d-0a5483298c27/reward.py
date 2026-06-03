"""
Reward Script: Create a combination chart with revenue as filled area and customer count as line
Task ID: calc_chart_combo_area_line_049
Domain: libreoffice_calc
Scoring:
  Component 1: A chart exists on the CustomerRevenue sheet (0.2 pts)
  Component 2: Chart contains both an areaChart and a lineChart (combination chart) (0.3 pts)
  Component 3: Revenue series references column B data (area) and Customers series references column C data (line) (0.3 pts)
  Component 4: Chart title is 'Monthly Revenue and Customer Count' (0.1 pts)
  Component 5: Secondary axis exists for Customers (0.1 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_combo_area_line_049'

# XML namespace for chart elements
CHART_NS = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
DRAWINGML_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_chart_xml(file_path):
    """Extract chart XML from the xlsx file (which is a ZIP archive)."""
    chart_contents = []
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            chart_files = [f for f in z.namelist() if f.startswith('xl/charts/') and f.endswith('.xml')]
            for cf in chart_files:
                content = z.read(cf).decode('utf-8', errors='replace')
                chart_contents.append((cf, content))
    except Exception as e:
        print(f"ERROR: Cannot read chart XML from {file_path}: {e}")
    return chart_contents


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid xlsx
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

    # Precondition: CustomerRevenue sheet must exist
    if 'CustomerRevenue' not in wb.sheetnames:
        print("CRITICAL: Sheet 'CustomerRevenue' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['CustomerRevenue']

    # Component 1: A chart exists on the CustomerRevenue sheet (0.2 points)
    # This FAILS on initial (0 charts) and PASSES on golden (1+ charts)
    try:
        chart_count = len(ws._charts)
        if chart_count >= 1:
            print(f"PASS: Component 1 — {chart_count} chart(s) exist on CustomerRevenue sheet (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — No charts found on CustomerRevenue sheet (expected at least 1)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract chart XML for deeper inspection
    chart_contents = get_chart_xml(file_path)
    if not chart_contents:
        print("FAIL: No chart XML found in the workbook file")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Parse the chart XML — look for combination of areaChart and lineChart
    combined_xml = "\n".join(content for _, content in chart_contents)

    # Component 2: Chart contains both areaChart and lineChart (combination chart) (0.3 points)
    # Initial file has no chart at all — this FAILS on initial, PASSES on golden
    try:
        has_area_chart = '<areaChart>' in combined_xml or f'<areaChart ' in combined_xml
        has_line_chart = '<lineChart>' in combined_xml or f'<lineChart ' in combined_xml

        if has_area_chart and has_line_chart:
            print(f"PASS: Component 2 — Chart is a combination chart with both areaChart and lineChart (0.3 pts)")
            total_score += 0.3
        elif has_area_chart:
            print(f"FAIL: Component 2 — Only areaChart found; missing lineChart for Customers series")
        elif has_line_chart:
            print(f"FAIL: Component 2 — Only lineChart found; missing areaChart for Revenue series")
        else:
            print(f"FAIL: Component 2 — Neither areaChart nor lineChart found in chart XML")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Revenue (column B) references area chart series, Customers (column C) references line chart series (0.3 points)
    # This verifies correct data binding: Revenue in areaChart, Customers in lineChart
    # FAILS on initial (no chart), PASSES on golden
    try:
        # Parse the XML to check series references within each chart type
        all_passed = False
        revenue_in_area = False
        customers_in_line = False

        for _, xml_content in chart_contents:
            root = ET.fromstring(xml_content)
            ns = {'c': CHART_NS, 'a': DRAWINGML_NS}

            # Find areaChart elements and check series references
            for area_chart in root.iter(f'{{{CHART_NS}}}areaChart'):
                for ser in area_chart.findall(f'{{{CHART_NS}}}ser'):
                    val_elem = ser.find(f'.//{{{CHART_NS}}}val')
                    if val_elem is not None:
                        num_ref = val_elem.find(f'{{{CHART_NS}}}numRef')
                        if num_ref is not None:
                            f_elem = num_ref.find(f'{{{CHART_NS}}}f')
                            if f_elem is not None and '$B$' in (f_elem.text or ''):
                                revenue_in_area = True

            # Find lineChart elements and check series references
            for line_chart in root.iter(f'{{{CHART_NS}}}lineChart'):
                for ser in line_chart.findall(f'{{{CHART_NS}}}ser'):
                    val_elem = ser.find(f'.//{{{CHART_NS}}}val')
                    if val_elem is not None:
                        num_ref = val_elem.find(f'{{{CHART_NS}}}numRef')
                        if num_ref is not None:
                            f_elem = num_ref.find(f'{{{CHART_NS}}}f')
                            if f_elem is not None and '$C$' in (f_elem.text or ''):
                                customers_in_line = True

        if revenue_in_area and customers_in_line:
            print(f"PASS: Component 3 — Revenue ($000) in areaChart (col B), Customers in lineChart (col C) (0.3 pts)")
            total_score += 0.3
        elif revenue_in_area:
            print(f"FAIL: Component 3 — Revenue is in areaChart but Customers series not found in lineChart (col C)")
        elif customers_in_line:
            print(f"FAIL: Component 3 — Customers is in lineChart but Revenue series not found in areaChart (col B)")
        else:
            print(f"FAIL: Component 3 — Correct series-to-chart-type mapping not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart title is 'Monthly Revenue and Customer Count' (0.1 points)
    # FAILS on initial (no chart), PASSES on golden
    try:
        expected_title = 'Monthly Revenue and Customer Count'
        title_found = False

        for _, xml_content in chart_contents:
            # Check for the title text in the chart XML
            if expected_title in xml_content:
                title_found = True
                break

        if title_found:
            print(f"PASS: Component 4 — Chart title is '{expected_title}' (0.1 pts)")
            total_score += 0.1
        else:
            # Try case-insensitive check
            for _, xml_content in chart_contents:
                if expected_title.lower() in xml_content.lower():
                    title_found = True
                    break
            if title_found:
                print(f"PASS: Component 4 — Chart title matches '{expected_title}' (case-insensitive) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — Chart title '{expected_title}' not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Secondary axis exists for Customers series (0.1 points)
    # Task requires two Y-axes: primary for Revenue, secondary for Customers
    # FAILS on initial (no chart), PASSES on golden
    try:
        secondary_axis_found = False

        for _, xml_content in chart_contents:
            root = ET.fromstring(xml_content)
            # Check for valAx with crosses="max" which indicates secondary (right) axis
            for val_ax in root.iter(f'{{{CHART_NS}}}valAx'):
                crosses_elem = val_ax.find(f'{{{CHART_NS}}}crosses')
                if crosses_elem is not None and crosses_elem.get('val') == 'max':
                    secondary_axis_found = True
                    break

            if secondary_axis_found:
                break

        if secondary_axis_found:
            print(f"PASS: Component 5 — Secondary Y-axis exists for Customers series (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — Secondary Y-axis (crosses='max') not found; expected two Y-axes")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
