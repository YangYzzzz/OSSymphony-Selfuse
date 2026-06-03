"""
Reward Script: Add error bars to chart on slide 3 with fixed value +/-5
Task ID: impress_tct_066
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): errBars element exists in chart series XML
  Component 2 (0.2): errBarType is "both" (plus and minus)
  Component 3 (0.2): errValType is "fixedVal" (fixed value type)
  Component 4 (0.3): fixed value is 5.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_066'

# Chart XML namespace
NS = {'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}


def verify_task(file_path):
    """
    Verify that error bars have been added to the chart on slide 3
    with a fixed value of +/-5.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx (zip)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find chart XML file (the chart on slide 3)
    chart_xml_path = None
    try:
        chart_files = [f for f in zf.namelist() if f.startswith('ppt/charts/') and f.endswith('.xml') and not '_rels' in f]
        if chart_files:
            chart_xml_path = chart_files[0]  # chart1.xml
            print(f"INFO: Found chart at {chart_xml_path}")
        else:
            print("CRITICAL: No chart XML found in pptx")
            print("REWARD: 0.0")
            zf.close()
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Error listing chart files: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    # Parse chart XML
    try:
        with zf.open(chart_xml_path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        print("REWARD: 0.0")
        zf.close()
        return 0.0

    # Find errBars element within the series
    err_bars = root.findall('.//c:errBars', NS)

    # Component 1: errBars element exists (0.3 points)
    try:
        if len(err_bars) > 0:
            print(f"PASS: Component 1 — errBars element found ({len(err_bars)} instance(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No errBars element found in chart XML")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(err_bars) == 0:
        # No error bars at all, remaining checks will fail
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        zf.close()
        return final_score

    eb = err_bars[0]

    # Component 2: errBarType is "both" (plus and minus) (0.2 points)
    try:
        bar_type_el = eb.find('c:errBarType', NS)
        if bar_type_el is not None:
            bar_type_val = bar_type_el.get('val', '')
            if bar_type_val == 'both':
                print(f"PASS: Component 2 — errBarType is 'both' (plus/minus) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — errBarType is '{bar_type_val}', expected 'both'")
        else:
            print("FAIL: Component 2 — errBarType element not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: errValType is "fixedVal" (0.2 points)
    try:
        val_type_el = eb.find('c:errValType', NS)
        if val_type_el is not None:
            val_type_val = val_type_el.get('val', '')
            if val_type_val == 'fixedVal':
                print(f"PASS: Component 3 — errValType is 'fixedVal' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — errValType is '{val_type_val}', expected 'fixedVal'")
        else:
            print("FAIL: Component 3 — errValType element not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: fixed value is 5.0 (0.3 points)
    try:
        val_el = eb.find('c:val', NS)
        if val_el is not None:
            val_str = val_el.get('val', '')
            try:
                val_num = float(val_str)
                if abs(val_num - 5.0) < 0.01:
                    print(f"PASS: Component 4 — error bar value is {val_num} (expected 5.0) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 4 — error bar value is {val_num}, expected 5.0")
            except ValueError:
                print(f"FAIL: Component 4 — error bar value '{val_str}' is not numeric")
        else:
            print("FAIL: Component 4 — val element not found in errBars")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
