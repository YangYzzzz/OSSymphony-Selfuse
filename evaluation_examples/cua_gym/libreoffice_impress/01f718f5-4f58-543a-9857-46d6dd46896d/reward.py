"""
Reward Script: Set chart title and axis titles on slide 3
Task ID: impress_tct_042
Domain: libreoffice_impress
Scoring:
  Component 1: Chart title = "Annual Growth Rate (%)" (0.4 pts)
  Component 2: X-axis title = "Year" (0.3 pts)
  Component 3: Y-axis title = "Growth %" (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET


WORKDIR = '/home/user'
TASK_ID = 'impress_tct_042'

# XML namespaces used in chart XML
NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_chart_path_for_slide(pptx_path, slide_num):
    """Find the chart XML path linked from a given slide number."""
    rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        try:
            with zf.open(rels_path) as f:
                root = ET.parse(f).getroot()
                for rel in root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                    if 'chart' in rel.get('Type', ''):
                        target = rel.get('Target', '')
                        # Target is relative like ../charts/chart1.xml
                        chart_name = target.split('/')[-1]
                        return f'ppt/charts/{chart_name}'
        except KeyError:
            pass
    return None


def get_title_text(title_elem):
    """Extract text from a c:title element."""
    if title_elem is None:
        return None
    # Look for rich text: c:tx/c:rich/a:p/a:r/a:t
    texts = []
    for t in title_elem.findall('.//a:t', NS):
        if t.text:
            texts.append(t.text)
    return ''.join(texts) if texts else None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find chart XML path for slide 3
    chart_path = find_chart_path_for_slide(file_path, 3)
    if chart_path is None:
        print("CRITICAL: No chart found on slide 3")
        print("REWARD: 0.0")
        return 0.0

    # Parse chart XML
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open(chart_path) as f:
                chart_root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the c:chart element
    chart_elem = chart_root.find('c:chart', NS)
    if chart_elem is None:
        print("CRITICAL: No c:chart element found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Chart title = "Annual Growth Rate (%)" (0.4 points)
    try:
        chart_title_elem = chart_elem.find('c:title', NS)
        chart_title_text = get_title_text(chart_title_elem)

        # Also check autoTitleDeleted — if val="1", title is explicitly deleted
        auto_del = chart_elem.find('c:autoTitleDeleted', NS)
        auto_deleted = (auto_del is not None and auto_del.get('val') == '1')

        if auto_deleted:
            print("FAIL: Component 1 — chart title is explicitly deleted (autoTitleDeleted=1)")
        elif chart_title_text and chart_title_text.strip() == 'Annual Growth Rate (%)':
            print(f"PASS: Component 1 — chart title = '{chart_title_text.strip()}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected chart title 'Annual Growth Rate (%)', found: '{chart_title_text}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get plot area axes for axis title checks
    plot_area = chart_elem.find('c:plotArea', NS)
    if plot_area is None:
        print("CRITICAL: No plotArea found in chart")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: X-axis (category axis) title = "Year" (0.3 points)
    try:
        cat_ax = plot_area.find('c:catAx', NS)
        if cat_ax is None:
            print("FAIL: Component 2 — no category axis found")
        else:
            cat_title_elem = cat_ax.find('c:title', NS)
            cat_title_text = get_title_text(cat_title_elem)
            if cat_title_text and cat_title_text.strip() == 'Year':
                print(f"PASS: Component 2 — X-axis title = '{cat_title_text.strip()}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — expected X-axis title 'Year', found: '{cat_title_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Y-axis (value axis) title = "Growth %" (0.3 points)
    try:
        val_ax = plot_area.find('c:valAx', NS)
        if val_ax is None:
            print("FAIL: Component 3 — no value axis found")
        else:
            val_title_elem = val_ax.find('c:title', NS)
            val_title_text = get_title_text(val_title_elem)
            if val_title_text and val_title_text.strip() == 'Growth %':
                print(f"PASS: Component 3 — Y-axis title = '{val_title_text.strip()}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — expected Y-axis title 'Growth %', found: '{val_title_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — persist app state then verify
def persist_app_state(domain):
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


persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
