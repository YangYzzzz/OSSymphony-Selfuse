"""
Reward Script: Add trend line with R-squared value to scatter chart on slide 4
Task ID: impress_tct_057
Domain: libreoffice_impress
Scoring:
  Component 1 — Trendline exists on chart data series (0.4 pts)
  Component 2 — Trendline type is linear (0.3 pts)
  Component 3 — R-squared value is displayed (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_057'


def persist_app_state(domain):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid zip (pptx)
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: chart1.xml must exist (the chart on slide 4)
    chart_xml_path = 'ppt/charts/chart1.xml'
    if chart_xml_path not in zf.namelist():
        print(f"CRITICAL: No chart XML found at {chart_xml_path}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Parse chart XML
    try:
        with zf.open(chart_xml_path) as f:
            chart_content = f.read().decode('utf-8')
        root = ET.fromstring(chart_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Namespace for chart XML
    ns_c = 'http://schemas.openxmlformats.org/drawingml/2006/chart'

    # Find all trendline elements anywhere in the chart
    trendlines = root.findall(f'.//{{{ns_c}}}trendline')

    # Component 1: Trendline exists on chart data series (0.4 points)
    try:
        if len(trendlines) > 0:
            print(f"PASS: Component 1 — Trendline found ({len(trendlines)} trendline(s)) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No trendline found in chart")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Trendline type is linear (0.3 points)
    try:
        if len(trendlines) > 0:
            trendline = trendlines[0]
            type_elem = trendline.find(f'{{{ns_c}}}trendlineType')
            if type_elem is not None:
                ttype = type_elem.get('val', '')
                if ttype == 'linear':
                    print(f"PASS: Component 2 — Trendline type is 'linear' (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Trendline type is '{ttype}', expected 'linear'")
            else:
                # No explicit type element; in OOXML, default trendline type is linear
                print("PASS: Component 2 — No explicit type (defaults to linear) (0.3 pts)")
                total_score += 0.3
        else:
            print("FAIL: Component 2 — No trendline to check type on")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: R-squared value is displayed on chart (0.3 points)
    try:
        if len(trendlines) > 0:
            trendline = trendlines[0]
            disp_rsqr = trendline.find(f'{{{ns_c}}}dispRSqr')
            if disp_rsqr is not None:
                val = disp_rsqr.get('val', '0')
                if val == '1':
                    print(f"PASS: Component 3 — R-squared display enabled (dispRSqr=1) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — dispRSqr val='{val}', expected '1'")
            else:
                print("FAIL: Component 3 — No dispRSqr element found in trendline")
        else:
            print("FAIL: Component 3 — No trendline to check R-squared display on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
