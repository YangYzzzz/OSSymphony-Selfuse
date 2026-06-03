"""
Reward Script: Add data labels to pie chart showing category name and percentage
Task ID: calc_chart_data_labels_category_022
Domain: libreoffice_calc
Scoring:
  - Component 1: Data labels exist on pie chart (0.4 pts)
  - Component 2: Category name is shown in data labels (0.3 pts)
  - Component 3: Percentage is shown in data labels (0.3 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_data_labels_category_022'

# XML namespace used in OOXML chart files
CHART_NS = 'http://schemas.openxmlformats.org/drawingml/2006/chart'


def get_chart_xml(file_path):
    """Extract and parse chart XML from xlsx file. Returns parsed XML root or None."""
    with zipfile.ZipFile(file_path, 'r') as z:
        chart_files = [n for n in z.namelist() if 'charts/chart' in n.lower()]
        if not chart_files:
            return None
        with z.open(chart_files[0]) as f:
            content = f.read()
    return ET.fromstring(content)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Add data labels to the pie chart showing both the category name and percentage.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = get_chart_xml(file_path)
        if root is None:
            print("CRITICAL: No chart files found in workbook")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the pieChart element
    try:
        pie_chart_elem = root.find(f'.//{{{CHART_NS}}}pieChart')
        if pie_chart_elem is None:
            print("CRITICAL: No pieChart element found in chart XML")
            print("REWARD: 0.0")
            return 0.0
        print("INFO: Found pieChart element")
    except Exception as e:
        print(f"CRITICAL: Error finding pieChart: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Data labels element exists on the pie chart (0.4 points)
    # The task requires adding data labels — this checks that the <dLbls> element
    # is present on the pieChart (not just on individual series), which is absent
    # in the initial file.
    dLbls_elem = None
    try:
        # Check for dLbls at the pieChart level (applies to all slices)
        dLbls_elem = pie_chart_elem.find(f'{{{CHART_NS}}}dLbls')
        if dLbls_elem is not None:
            print(f"PASS: Component 1 — Data labels element (<dLbls>) found on pieChart (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No <dLbls> element found on pieChart. "
                  f"Expected data labels to be added to the chart.")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check dLbls element: {e}")

    # Component 2: Category name is shown in data labels (0.3 points)
    # The task requires showing the category name (e.g., 'Stocks', 'Bonds') on each slice.
    # This checks that showCatName is enabled in the dLbls element.
    try:
        if dLbls_elem is not None:
            show_cat = dLbls_elem.find(f'{{{CHART_NS}}}showCatName')
            if show_cat is not None and show_cat.get('val', '0') in ('1', 'true'):
                print(f"PASS: Component 2 — showCatName=1 found; category names will appear in labels (0.3 pts)")
                total_score += 0.3
            else:
                cat_val = show_cat.get('val', 'missing') if show_cat is not None else 'element not present'
                print(f"FAIL: Component 2 — showCatName not enabled. "
                      f"Expected showCatName val='1', found: {cat_val}")
        else:
            print(f"FAIL: Component 2 — Cannot check showCatName (no dLbls element)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check showCatName: {e}")

    # Component 3: Percentage is shown in data labels (0.3 points)
    # The task requires showing the percentage for each slice.
    # This checks that showPercent is enabled in the dLbls element.
    try:
        if dLbls_elem is not None:
            show_pct = dLbls_elem.find(f'{{{CHART_NS}}}showPercent')
            if show_pct is not None and show_pct.get('val', '0') in ('1', 'true'):
                print(f"PASS: Component 3 — showPercent=1 found; percentages will appear in labels (0.3 pts)")
                total_score += 0.3
            else:
                pct_val = show_pct.get('val', 'missing') if show_pct is not None else 'element not present'
                print(f"FAIL: Component 3 — showPercent not enabled. "
                      f"Expected showPercent val='1', found: {pct_val}")
        else:
            print(f"FAIL: Component 3 — Cannot check showPercent (no dLbls element)")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check showPercent: {e}")

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
