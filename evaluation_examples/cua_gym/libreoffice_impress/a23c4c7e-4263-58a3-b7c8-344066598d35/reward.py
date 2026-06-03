"""
Reward Script: Set Y-axis min to 0, max to 500, major gridline intervals of 100
Task ID: impress_tct_058
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Y-axis minimum is 0
  Component 2 (0.3): Y-axis maximum is 500
  Component 3 (0.4): Major gridline interval (majorUnit) is 100
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_058'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse chart XML from the pptx ZIP
    ns_c = 'http://schemas.openxmlformats.org/drawingml/2006/chart'

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Find chart XML - we know it's chart1.xml on slide 2
            chart_path = 'ppt/charts/chart1.xml'
            if chart_path not in zf.namelist():
                print(f"CRITICAL: Chart file {chart_path} not found in pptx")
                print("REWARD: 0.0")
                return 0.0

            with zf.open(chart_path) as f:
                tree = ET.parse(f)
                root = tree.getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the valAx (value axis) element
    valAx = root.find(f'.//{{{ns_c}}}valAx')
    if valAx is None:
        print("CRITICAL: No value axis (valAx) found in chart")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Y-axis minimum is 0 (0.3 points)
    try:
        scaling = valAx.find(f'{{{ns_c}}}scaling')
        min_elem = scaling.find(f'{{{ns_c}}}min') if scaling is not None else None
        if min_elem is not None:
            min_val = float(min_elem.get('val'))
            if abs(min_val - 0.0) < 0.01:
                print(f"PASS: Component 1 - Y-axis minimum is {min_val} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 - Y-axis minimum is {min_val}, expected 0")
        else:
            print("FAIL: Component 1 - No explicit minimum set on Y-axis (auto-scaling)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Y-axis maximum is 500 (0.3 points)
    try:
        scaling = valAx.find(f'{{{ns_c}}}scaling')
        max_elem = scaling.find(f'{{{ns_c}}}max') if scaling is not None else None
        if max_elem is not None:
            max_val = float(max_elem.get('val'))
            if abs(max_val - 500.0) < 0.01:
                print(f"PASS: Component 2 - Y-axis maximum is {max_val} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Y-axis maximum is {max_val}, expected 500")
        else:
            print("FAIL: Component 2 - No explicit maximum set on Y-axis (auto-scaling)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Major gridline interval is 100 (0.4 points)
    try:
        major_unit = valAx.find(f'{{{ns_c}}}majorUnit')
        if major_unit is not None:
            unit_val = float(major_unit.get('val'))
            if abs(unit_val - 100.0) < 0.01:
                print(f"PASS: Component 3 - Major unit interval is {unit_val} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 - Major unit interval is {unit_val}, expected 100")
        else:
            print("FAIL: Component 3 - No explicit majorUnit set on Y-axis (auto intervals)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
