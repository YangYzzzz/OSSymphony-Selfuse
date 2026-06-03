"""
Reward Script: Dual-axis chart on slide 6 with bar + line series
Task ID: impress_stu_069
Domain: libreoffice_impress
Scoring:
  C1 (0.15) - Chart exists on slide 6
  C2 (0.10) - Chart title is 'Research Output Trends'
  C3 (0.25) - Bar chart series with correct 'Number of Papers Published' data
  C4 (0.25) - Line chart series with correct 'Average Citations per Paper' data
  C5 (0.10) - Bar fill color is blue (#3498DB)
  C6 (0.10) - Line color is red (#E74C3C) with markers
  C7 (0.05) - Secondary Y-axis (line plotted on right axis)
"""

import os
import xml.etree.ElementTree as ET
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'impress_stu_069'

# Expected data
EXPECTED_BAR_VALUES = [45.0, 52.0, 61.0, 78.0, 95.0, 110.0]
EXPECTED_LINE_VALUES = [3.2, 3.5, 4.1, 4.8, 5.2, 6.1]
EXPECTED_CATEGORIES = ['2020', '2021', '2022', '2023', '2024', '2025']

NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def parse_chart_xml_from_slide6(pptx_path):
    """Extract chart XML from slide 6 of the pptx file via ZIP."""
    # First, find chart references in slide6.xml
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Read slide6.xml.rels to find chart relationship
        rels_path = 'ppt/slides/_rels/slide6.xml.rels'
        try:
            with zf.open(rels_path) as f:
                rels_root = ET.parse(f).getroot()
        except KeyError:
            print("FAIL: slide6.xml.rels not found")
            return None, None

        chart_path = None
        for rel in rels_root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            if 'chart' in rel.get('Type', '').lower():
                target = rel.get('Target', '')
                # Target is relative like ../charts/chart1.xml
                chart_path = 'ppt/charts/' + target.split('/')[-1]
                break

        if not chart_path:
            print("FAIL: No chart relationship found in slide 6")
            return None, None

        try:
            with zf.open(chart_path) as f:
                chart_root = ET.parse(f).getroot()
            return chart_root, chart_path
        except KeyError:
            print(f"FAIL: Chart file {chart_path} not found in ZIP")
            return None, None


def get_series_values(ser_element):
    """Extract numeric values from a chart series element."""
    values = []
    val_elem = ser_element.find('.//c:val', NS)
    if val_elem is None:
        return values
    num_cache = val_elem.find('.//c:numCache', NS)
    if num_cache is None:
        return values
    for pt in num_cache.findall('c:pt', NS):
        v = pt.find('c:v', NS)
        if v is not None and v.text:
            values.append(float(v.text))
    return values


def get_series_name(ser_element):
    """Extract series name from tx element."""
    tx = ser_element.find('c:tx', NS)
    if tx is None:
        return ''
    # Check strCache
    str_cache = tx.find('.//c:strCache', NS)
    if str_cache is not None:
        pt = str_cache.find('.//c:pt/c:v', NS)
        if pt is not None and pt.text:
            return pt.text
    return ''


def get_series_categories(ser_element):
    """Extract category labels from a chart series."""
    cats = []
    cat_elem = ser_element.find('c:cat', NS)
    if cat_elem is None:
        return cats
    str_cache = cat_elem.find('.//c:strCache', NS)
    if str_cache is not None:
        for pt in str_cache.findall('c:pt', NS):
            v = pt.find('c:v', NS)
            if v is not None and v.text:
                cats.append(v.text)
    return cats


def get_fill_color(ser_element):
    """Extract solid fill color from series spPr."""
    sp_pr = ser_element.find('c:spPr', NS)
    if sp_pr is None:
        return None
    solid_fill = sp_pr.find('a:solidFill', NS)
    if solid_fill is None:
        return None
    srgb = solid_fill.find('a:srgbClr', NS)
    if srgb is not None:
        return srgb.get('val', '').upper()
    return None


def get_line_color(ser_element):
    """Extract line color from series spPr/ln."""
    sp_pr = ser_element.find('c:spPr', NS)
    if sp_pr is None:
        return None
    ln = sp_pr.find('a:ln', NS)
    if ln is None:
        return None
    solid_fill = ln.find('a:solidFill', NS)
    if solid_fill is None:
        return None
    srgb = solid_fill.find('a:srgbClr', NS)
    if srgb is not None:
        return srgb.get('val', '').upper()
    return None


def has_markers(ser_element):
    """Check if the series has markers configured."""
    marker = ser_element.find('c:marker', NS)
    if marker is None:
        return False
    symbol = marker.find('c:symbol', NS)
    if symbol is not None:
        val = symbol.get('val', 'none')
        return val != 'none'
    return False


def values_match(actual, expected, tolerance=0.01):
    """Check if two lists of numeric values match within tolerance."""
    if len(actual) != len(expected):
        return False
    return all(abs(a - e) < tolerance for a, e in zip(actual, expected))


def verify_task(file_path):
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Parse chart XML from slide 6
    chart_root, chart_path = parse_chart_xml_from_slide6(file_path)

    # Component 1: Chart exists on slide 6 (0.15 points)
    try:
        if chart_root is not None:
            print(f"PASS: Component 1 -- Chart found on slide 6 at {chart_path} (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 -- No chart found on slide 6")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find chart sub-elements
    chart_elem = chart_root.find('c:chart', NS)
    plot_area = chart_elem.find('c:plotArea', NS) if chart_elem is not None else None

    # Component 2: Chart title is 'Research Output Trends' (0.10 points)
    try:
        title_elem = chart_elem.find('c:title', NS) if chart_elem is not None else None
        title_text = ''
        if title_elem is not None:
            # Gather all text runs in the title
            for t in title_elem.findall('.//a:t', NS):
                if t.text:
                    title_text += t.text
        title_text = title_text.strip()
        if 'research output trends' in title_text.lower():
            print(f"PASS: Component 2 -- Chart title is '{title_text}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Expected title 'Research Output Trends', found '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Find bar chart and line chart elements
    bar_chart = plot_area.find('c:barChart', NS) if plot_area is not None else None
    line_chart = plot_area.find('c:lineChart', NS) if plot_area is not None else None

    bar_ser = bar_chart.find('c:ser', NS) if bar_chart is not None else None
    line_ser = line_chart.find('c:ser', NS) if line_chart is not None else None

    # Component 3: Bar chart series with correct data (0.25 points)
    try:
        if bar_ser is not None:
            bar_name = get_series_name(bar_ser)
            bar_values = get_series_values(bar_ser)
            bar_cats = get_series_categories(bar_ser)

            name_ok = 'paper' in bar_name.lower() and 'published' in bar_name.lower()
            values_ok = values_match(bar_values, EXPECTED_BAR_VALUES)
            cats_ok = bar_cats == EXPECTED_CATEGORIES or len(bar_cats) == 0  # cats might be shared

            if values_ok and name_ok:
                print(f"PASS: Component 3 -- Bar series '{bar_name}' with values {bar_values} (0.25 pts)")
                total_score += 0.25
            elif values_ok:
                # Partial: values correct but name missing/wrong
                print(f"PARTIAL: Component 3 -- Bar values correct {bar_values} but name '{bar_name}' unexpected (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Bar values {bar_values} != expected {EXPECTED_BAR_VALUES}, name='{bar_name}'")
        else:
            print("FAIL: Component 3 -- No bar chart series found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Line chart series with correct data (0.25 points)
    try:
        if line_ser is not None:
            line_name = get_series_name(line_ser)
            line_values = get_series_values(line_ser)

            name_ok = 'citation' in line_name.lower()
            values_ok = values_match(line_values, EXPECTED_LINE_VALUES)

            if values_ok and name_ok:
                print(f"PASS: Component 4 -- Line series '{line_name}' with values {line_values} (0.25 pts)")
                total_score += 0.25
            elif values_ok:
                print(f"PARTIAL: Component 4 -- Line values correct {line_values} but name '{line_name}' unexpected (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- Line values {line_values} != expected {EXPECTED_LINE_VALUES}, name='{line_name}'")
        else:
            print("FAIL: Component 4 -- No line chart series found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Bar fill color is blue #3498DB (0.10 points)
    try:
        if bar_ser is not None:
            bar_color = get_fill_color(bar_ser)
            if bar_color and bar_color == '3498DB':
                print(f"PASS: Component 5 -- Bar fill color is #{bar_color} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- Expected bar fill color #3498DB, found #{bar_color}")
        else:
            print("FAIL: Component 5 -- No bar series to check color")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Line color is red #E74C3C with markers (0.10 points)
    try:
        if line_ser is not None:
            line_color = get_line_color(line_ser)
            markers = has_markers(line_ser)

            if line_color == 'E74C3C' and markers:
                print(f"PASS: Component 6 -- Line color #{line_color} with markers (0.10 pts)")
                total_score += 0.10
            elif line_color == 'E74C3C':
                print(f"PARTIAL: Component 6 -- Line color correct #{line_color} but no markers (0.05 pts)")
                total_score += 0.05
            elif markers:
                print(f"PARTIAL: Component 6 -- Markers present but line color #{line_color} != #E74C3C (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 -- Line color #{line_color}, markers={markers}")
        else:
            print("FAIL: Component 6 -- No line series to check styling")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: Secondary Y-axis (line on right axis) (0.05 points)
    try:
        if plot_area is not None:
            # Look for a valAx with axPos='r' (right side)
            val_axes = plot_area.findall('c:valAx', NS)
            has_right_axis = False
            for vax in val_axes:
                ax_pos = vax.find('c:axPos', NS)
                if ax_pos is not None and ax_pos.get('val') == 'r':
                    # Also check it's not deleted
                    delete = vax.find('c:delete', NS)
                    if delete is None or delete.get('val') != '1':
                        has_right_axis = True
                        break

            if has_right_axis:
                print(f"PASS: Component 7 -- Secondary Y-axis (right) found (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 7 -- No secondary Y-axis on right side")
        else:
            print("FAIL: Component 7 -- No plot area found")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Impress
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
