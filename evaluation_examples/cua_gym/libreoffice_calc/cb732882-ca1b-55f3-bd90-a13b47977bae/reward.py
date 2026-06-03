"""
Reward Script: Create a step-line chart showing price changes over time
Task ID: calc_chart_line_step_075
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on 'PriceHistory' sheet (0.3 pts)
  Component 2: Chart is a LineChart type (0.2 pts)
  Component 3: Chart title is 'Product Price History' (0.2 pts)
  Component 4: Data range covers correct cells (A2:A9 for cats, B2:B9 for vals) (0.2 pts)
  Component 5: Line is non-smooth (smooth=0, step-like) (0.1 pts)
  Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_line_step_075'


def get_chart_xml_content(file_path):
    """Extract chart XML from XLSX ZIP container. Returns None if not found."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            chart_files = [f for f in z.namelist() if f.startswith('xl/charts/') and f.endswith('.xml')]
            if not chart_files:
                return None
            return z.read(chart_files[0]).decode('utf-8')
    except Exception as e:
        print(f"ERROR reading chart XML: {e}")
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition: file must be loadable
    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Pre-condition: 'PriceHistory' sheet must exist
    if 'PriceHistory' not in wb.sheetnames:
        print("CRITICAL: Sheet 'PriceHistory' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['PriceHistory']

    # Component 1: Chart exists on 'PriceHistory' sheet (0.3 points)
    # Initial file has 0 charts; golden file has 1 chart.
    try:
        charts = ws._charts
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists on PriceHistory sheet (found {len(charts)} chart(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No chart found on PriceHistory sheet (expected >= 1, found 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check charts: {e}")

    # Component 2: Chart is a LineChart type (0.2 points)
    # Initial file has no chart at all; golden file has a LineChart.
    try:
        from openpyxl.chart import LineChart
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            if isinstance(chart, LineChart):
                print(f"PASS: Component 2 — Chart is a LineChart type (0.2 pts)")
                total_score += 0.2
            else:
                chart_type = type(chart).__name__
                print(f"FAIL: Component 2 — Expected LineChart, found {chart_type}")
        else:
            print(f"FAIL: Component 2 — No chart to check type (no charts in sheet)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check chart type: {e}")

    # Component 3: Chart title is 'Product Price History' (0.2 points)
    # Initial file has no chart, hence no title; golden file has the correct title.
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            # Extract title from rich text structure
            title_text = None
            try:
                # Try the rich text path: chart.title.tx.rich.p[0].r[0].t
                title_text = chart.title.tx.rich.p[0].r[0].t
            except Exception:
                pass
            if title_text is None:
                try:
                    # Try alternative: chart.title as string
                    title_text = str(chart.title)
                except Exception:
                    pass

            expected_title = 'Product Price History'
            if title_text and title_text.strip() == expected_title:
                print(f"PASS: Component 3 — Chart title is '{expected_title}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected title '{expected_title}', found: {repr(title_text)}")
        else:
            print(f"FAIL: Component 3 — No chart to check title (no charts in sheet)")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check chart title: {e}")

    # Component 4: Data range covers correct cells (B2:B9 for values, A2:A9 for categories) (0.2 points)
    # This verifies the chart plots all 8 data rows (rows 2-9) from the PriceHistory sheet.
    # Initial file has no chart, so data range check will fail.
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart = charts[0]
            val_ref = None
            cat_ref = None
            if len(chart.series) >= 1:
                ser = chart.series[0]
                # Values reference
                if hasattr(ser, 'val') and ser.val and hasattr(ser.val, 'numRef') and ser.val.numRef:
                    val_ref = ser.val.numRef.ref
                # Categories reference
                if hasattr(ser, 'cat') and ser.cat:
                    if hasattr(ser.cat, 'numRef') and ser.cat.numRef:
                        cat_ref = ser.cat.numRef.ref
                    elif hasattr(ser.cat, 'strRef') and ser.cat.strRef:
                        cat_ref = ser.cat.strRef.ref

            # Normalize references for comparison (remove $ signs and quotes)
            def normalize_ref(ref):
                if ref is None:
                    return None
                return ref.replace('$', '').replace("'", '').replace('"', '').strip()

            val_ref_norm = normalize_ref(val_ref)
            cat_ref_norm = normalize_ref(cat_ref)

            # Expected: B2:B9 for values, A2:A9 for categories (sheet prefix optional)
            val_ok = val_ref_norm is not None and 'B2:B9' in val_ref_norm
            cat_ok = cat_ref_norm is not None and 'A2:A9' in cat_ref_norm

            if val_ok and cat_ok:
                print(f"PASS: Component 4 — Data range correct: values={val_ref}, cats={cat_ref} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Data range incorrect. values={val_ref} (expected B2:B9), cats={cat_ref} (expected A2:A9)")
        else:
            print(f"FAIL: Component 4 — No chart to check data range (no charts in sheet)")
    except Exception as e:
        print(f"ERROR: Component 4 — Could not check data range: {e}")

    # Component 5: Line is non-smooth (step-like, smooth=0) (0.1 points)
    # The step-line effect requires smooth=False (no interpolation between points).
    # Initial file has no chart; golden file has smooth=False.
    # We check the XML directly since openpyxl's smooth attribute may be unreliable.
    try:
        charts = ws._charts
        if len(charts) >= 1:
            chart_xml = get_chart_xml_content(file_path)
            if chart_xml is not None:
                # A non-smooth line chart has <smooth val="0"/> or no smooth element
                # (defaults to 0). A smooth line has <smooth val="1"/>.
                import re
                # Check that there is no smooth=1 (which would be a smooth/curved line)
                smooth_1_match = re.search(r'<[^:]*:?smooth\s+val=["\']1["\']', chart_xml)
                if smooth_1_match:
                    print(f"FAIL: Component 5 — Chart line is smooth (val=1), expected non-smooth step line")
                else:
                    # Check if smooth=0 is explicitly set (preferred for step-line)
                    # No smooth element also means non-smooth (default 0), which is acceptable.
                    smooth_0_match = re.search(r'<[^:]*:?smooth\s+val=["\']0["\']', chart_xml)
                    non_smooth_confirmed = smooth_0_match is not None
                    non_smooth_default = (not non_smooth_confirmed)  # no smooth element = default 0
                    if non_smooth_confirmed:
                        print(f"PASS: Component 5 — Line is non-smooth (smooth=0, step-like behavior) (0.1 pts)")
                        total_score += 0.1
                    elif non_smooth_default:
                        print(f"PASS: Component 5 — Line has no smooth attribute (defaults to non-smooth/step-like) (0.1 pts)")
                        total_score += 0.1
            else:
                print(f"FAIL: Component 5 — Could not read chart XML to verify smooth property")
        else:
            print(f"FAIL: Component 5 — No chart to check smooth property (no charts in sheet)")
    except Exception as e:
        print(f"ERROR: Component 5 — Could not check smooth property: {e}")

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
