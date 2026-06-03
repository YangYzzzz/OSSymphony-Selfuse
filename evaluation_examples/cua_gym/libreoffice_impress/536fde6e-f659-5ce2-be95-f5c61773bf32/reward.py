"""
Reward Script: Set bar chart series colors on slide 2
Task ID: impress_tct_046
Domain: libreoffice_impress
Scoring:
  Component 1: Series 1 (idx=0) fill color == #1565C0  (0.34 pts)
  Component 2: Series 2 (idx=1) fill color == #EF6C00  (0.33 pts)
  Component 3: Series 3 (idx=2) fill color == #2E7D32  (0.33 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_046'

# Expected colors per series index (uppercase hex, no '#')
EXPECTED_COLORS = {
    '0': '1565C0',
    '1': 'EF6C00',
    '2': '2E7D32',
}

SERIES_WEIGHTS = {
    '0': 0.34,
    '1': 0.33,
    '2': 0.33,
}


def get_chart_series_colors(pptx_path):
    """Extract solidFill srgbClr from each bar chart series in chart1.xml.
    Returns dict: { series_idx_str: color_hex_upper | None }
    """
    ns = {
        'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }
    colors = {}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/charts/chart1.xml') as f:
                root = ET.parse(f).getroot()

            for tag in ['c:barChart', 'c:bar3DChart']:
                bar_chart = root.find('.//' + tag, ns)
                if bar_chart is not None:
                    for ser in bar_chart.findall('c:ser', ns):
                        idx_el = ser.find('c:idx', ns)
                        if idx_el is None:
                            continue
                        idx = idx_el.get('val')
                        color = None
                        spPr = ser.find('c:spPr', ns)
                        if spPr is not None:
                            solid = spPr.find('a:solidFill', ns)
                            if solid is not None:
                                srgb = solid.find('a:srgbClr', ns)
                                if srgb is not None:
                                    color = srgb.get('val', '').upper()
                        colors[idx] = color
                    break
    except Exception as e:
        print('ERROR: Could not parse chart XML: %s' % e)
    return colors


def verify_task(file_path):
    """Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip/pptx
    if not os.path.exists(file_path):
        print('CRITICAL: File not found: %s' % file_path)
        print('REWARD: 0.0')
        return 0.0

    # Precondition: chart1.xml must exist
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            if 'ppt/charts/chart1.xml' not in zf.namelist():
                print('CRITICAL: No chart found in presentation')
                print('REWARD: 0.0')
                return 0.0
    except Exception as e:
        print('CRITICAL: Cannot open pptx as zip: %s' % e)
        print('REWARD: 0.0')
        return 0.0

    # Extract actual series colors
    actual_colors = get_chart_series_colors(file_path)
    if not actual_colors:
        print('CRITICAL: Could not extract any series from chart')
        print('REWARD: 0.0')
        return 0.0

    # Component 1: Series 1 (idx=0) color is #1565C0 (0.34 points)
    try:
        actual = actual_colors.get('0')
        expected = EXPECTED_COLORS['0']
        if actual is not None and actual.upper() == expected:
            print('PASS: Component 1 -- Series 1 color is #%s (0.34 pts)' % actual)
            total_score += 0.34
        else:
            print('FAIL: Component 1 -- Series 1 color expected #%s, found %s' % (expected, actual))
    except Exception as e:
        print('ERROR: Component 1 -- %s' % e)

    # Component 2: Series 2 (idx=1) color is #EF6C00 (0.33 points)
    try:
        actual = actual_colors.get('1')
        expected = EXPECTED_COLORS['1']
        if actual is not None and actual.upper() == expected:
            print('PASS: Component 2 -- Series 2 color is #%s (0.33 pts)' % actual)
            total_score += 0.33
        else:
            print('FAIL: Component 2 -- Series 2 color expected #%s, found %s' % (expected, actual))
    except Exception as e:
        print('ERROR: Component 2 -- %s' % e)

    # Component 3: Series 3 (idx=2) color is #2E7D32 (0.33 points)
    try:
        actual = actual_colors.get('2')
        expected = EXPECTED_COLORS['2']
        if actual is not None and actual.upper() == expected:
            print('PASS: Component 3 -- Series 3 color is #%s (0.33 pts)' % actual)
            total_score += 0.33
        else:
            print('FAIL: Component 3 -- Series 3 color expected #%s, found %s' % (expected, actual))
    except Exception as e:
        print('ERROR: Component 3 -- %s' % e)

    final_score = min(round(total_score, 2), 1.0)
    print('')
    print('Score: %s/1.0' % final_score)
    print('REWARD: %s' % final_score)
    return final_score


# Persistence hook: save any unsaved GUI state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print("PERSIST_WARN: save hook failed: %s" % e)


# Entry point
persist_app_state()

file_path = '%s/%s.pptx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print('File not found: %s' % file_path)
    print('REWARD: 0.0')
else:
    verify_task(file_path)
