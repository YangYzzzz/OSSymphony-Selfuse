"""
Reward Script: Move chart legend from right to bottom on slide 2
Task ID: impress_tct_043
Domain: libreoffice_impress
Scoring:
  Component 1 (0.6): Legend position is 'b' (bottom)
  Component 2 (0.4): Legend is bottom AND chart data integrity preserved (4 series, barChart type)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_043'

# Namespace for chart XML
NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
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


def get_chart_xml(pptx_path, chart_name='ppt/charts/chart1.xml'):
    """Extract and parse chart XML from the pptx file."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(chart_name) as f:
            return ET.fromstring(f.read())


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx with chart
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = get_chart_xml(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Legend position is 'b' (bottom) — 0.6 points
    # This is the core task requirement: move legend from right to bottom
    try:
        legend = root.find('.//c:legend', NS)
        if legend is not None:
            legend_pos = legend.find('c:legendPos', NS)
            if legend_pos is not None:
                pos_val = legend_pos.get('val')
                if pos_val == 'b':
                    print(f"PASS: Component 1 -- Legend position is 'b' (bottom) (0.6 pts)")
                    total_score += 0.6
                else:
                    print(f"FAIL: Component 1 -- Legend position is '{pos_val}', expected 'b'")
            else:
                print("FAIL: Component 1 -- No legendPos element found in legend")
        else:
            print("FAIL: Component 1 -- No legend element found in chart")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Legend is bottom AND chart data integrity preserved — 0.4 points
    # Compound check: legend must be 'b' AND chart must still have 4 series in barChart
    # This ensures the task was done correctly without breaking the chart
    try:
        legend = root.find('.//c:legend', NS)
        legend_is_bottom = (
            legend is not None
            and legend.find('c:legendPos', NS) is not None
            and legend.find('c:legendPos', NS).get('val') == 'b'
        )

        bar_chart = root.find('.//c:barChart', NS)
        series_count = 0
        if bar_chart is not None:
            series_count = len(bar_chart.findall('c:ser', NS))

        if legend_is_bottom and bar_chart is not None and series_count == 4:
            print(f"PASS: Component 2 -- Legend is bottom AND chart has {series_count} series in barChart (0.4 pts)")
            total_score += 0.4
        else:
            reasons = []
            if not legend_is_bottom:
                reasons.append("legend not at bottom")
            if bar_chart is None:
                reasons.append("barChart element missing")
            if series_count != 4:
                reasons.append(f"expected 4 series, found {series_count}")
            print(f"FAIL: Component 2 -- {', '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

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
