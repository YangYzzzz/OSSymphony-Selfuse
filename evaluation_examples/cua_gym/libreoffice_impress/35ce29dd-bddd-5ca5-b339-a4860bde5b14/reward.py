"""
Reward Script: Convert 2D column chart to 3D column chart with perspective rotation
Task ID: impress_tct_049
Domain: libreoffice_impress
Scoring:
  Component 1: bar3DChart element present (barChart absent) — 0.4 pts
  Component 2: view3D element with perspective settings — 0.3 pts
  Component 3: Data integrity preserved in 3D chart (4 categories, 2 series) — 0.3 pts
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_049'

# XML namespaces used in chart XML
NS_C = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_MAP = {'c': NS_C, 'a': NS_A, 'r': NS_R}


def find_chart_xml_path(zf):
    """Find the chart XML file path inside the PPTX ZIP."""
    chart_files = [f for f in zf.namelist() if f.startswith('ppt/charts/chart') and f.endswith('.xml')]
    if chart_files:
        return chart_files[0]
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the chart XML
    chart_path = find_chart_xml_path(zf)
    if chart_path is None:
        print("CRITICAL: No chart XML found in presentation")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open(chart_path) as f:
            chart_xml = f.read()
        root = ET.fromstring(chart_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find the chart element (child of chartSpace)
    chart_elem = root.find('c:chart', NS_MAP)
    if chart_elem is None:
        print("CRITICAL: No c:chart element found")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    plot_area = chart_elem.find('c:plotArea', NS_MAP)
    if plot_area is None:
        print("CRITICAL: No plotArea element found")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: bar3DChart element present, barChart absent (0.4 points)
    # This is the core change — 2D uses barChart, 3D uses bar3DChart
    try:
        bar3d_chart = plot_area.find('c:bar3DChart', NS_MAP)
        bar2d_chart = plot_area.find('c:barChart', NS_MAP)

        has_3d = bar3d_chart is not None
        has_2d = bar2d_chart is not None

        if has_3d and not has_2d:
            print(f"PASS: Component 1 — bar3DChart present, barChart absent (0.4 pts)")
            total_score += 0.4
        elif has_3d and has_2d:
            print(f"PARTIAL: Component 1 — bar3DChart present but barChart also exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — bar3DChart not found (has_3d={has_3d}, has_2d={has_2d})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: view3D element with perspective rotation settings (0.3 points)
    # The 3D chart should have a view3D element with rotation and perspective values
    try:
        view3d = chart_elem.find('c:view3D', NS_MAP)
        if view3d is not None:
            rot_x = view3d.find('c:rotX', NS_MAP)
            rot_y = view3d.find('c:rotY', NS_MAP)
            perspective = view3d.find('c:perspective', NS_MAP)

            has_rot_x = rot_x is not None and rot_x.get('val') is not None
            has_rot_y = rot_y is not None and rot_y.get('val') is not None
            has_perspective = perspective is not None and perspective.get('val') is not None

            sub_score = 0.0
            details = []

            if has_rot_x:
                sub_score += 0.1
                details.append(f"rotX={rot_x.get('val')}")
            if has_rot_y:
                sub_score += 0.1
                details.append(f"rotY={rot_y.get('val')}")
            if has_perspective:
                sub_score += 0.1
                details.append(f"perspective={perspective.get('val')}")

            if sub_score > 0:
                print(f"PASS: Component 2 — view3D present with {', '.join(details)} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — view3D present but no rotation/perspective attributes")
        else:
            print(f"FAIL: Component 2 — No view3D element found in chart")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data integrity preserved in the 3D chart (0.3 points)
    # The 3D chart must have the same data: 4 categories (Q1-Q4), 2 series
    # This is anchored to the 3D chart — only scores if we're checking bar3DChart
    try:
        # Use bar3DChart if present, otherwise this component fails (no 3D chart = no data in 3D chart)
        chart_container = plot_area.find('c:bar3DChart', NS_MAP)
        if chart_container is None:
            print(f"FAIL: Component 3 — No bar3DChart to verify data integrity in")
        else:
            series_elements = chart_container.findall('c:ser', NS_MAP)
            num_series = len(series_elements)

            # Check categories count from first series
            num_categories = 0
            if num_series > 0:
                cat_ref = series_elements[0].find('.//c:cat/c:strRef/c:strCache/c:ptCount', NS_MAP)
                if cat_ref is not None:
                    num_categories = int(cat_ref.get('val', '0'))

            # Check bar direction is column
            bar_dir = chart_container.find('c:barDir', NS_MAP)
            is_column = bar_dir is not None and bar_dir.get('val') == 'col'

            sub_score = 0.0
            if num_series == 2:
                sub_score += 0.1
                print(f"  Data check: 2 series found")
            else:
                print(f"  Data check: Expected 2 series, found {num_series}")

            if num_categories == 4:
                sub_score += 0.1
                print(f"  Data check: 4 categories found")
            else:
                print(f"  Data check: Expected 4 categories, found {num_categories}")

            if is_column:
                sub_score += 0.1
                print(f"  Data check: Column direction confirmed")
            else:
                print(f"  Data check: Bar direction is not 'col'")

            if sub_score > 0:
                print(f"PASS: Component 3 — Data integrity in 3D chart ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — Data integrity issues in 3D chart")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
