"""
Reward Script: Set chart font on slide 4 to 10pt Calibri for all text elements
Task ID: impress_tct_065
Domain: libreoffice_impress
Scoring:
  - Component 1: Chart title font (0.2)
  - Component 2: Category axis title font (0.2)
  - Component 3: Value axis title font (0.2)
  - Component 4: Axis tick label fonts (0.2)
  - Component 5: Data label font (0.1)
  - Component 6: Legend font (0.1)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_065'
TARGET_SIZE = '1000'       # 10pt in hundredths-of-a-point
TARGET_TYPEFACE = 'Calibri'

NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def check_txpr_font(element, ns, label):
    """Check a c:txPr element for defRPr sz and latin typeface.
    Returns (size_ok, font_ok, details_str)."""
    if element is None:
        return False, False, f"{label}: txPr element not found"
    defRPr = element.find('.//a:defRPr', ns)
    if defRPr is None:
        return False, False, f"{label}: defRPr not found"
    sz = defRPr.get('sz', '')
    latin = defRPr.find('a:latin', ns)
    tf = latin.get('typeface', '') if latin is not None else ''
    size_ok = (sz == TARGET_SIZE)
    font_ok = (tf == TARGET_TYPEFACE)
    details = f"{label}: sz={sz} (want {TARGET_SIZE}), typeface={tf} (want {TARGET_TYPEFACE})"
    return size_ok, font_ok, details


def check_rich_font(rich_elem, ns, label):
    """Check a c:rich element (used for titles). Checks both defRPr and rPr."""
    if rich_elem is None:
        return False, False, f"{label}: rich element not found"

    # Check defRPr
    defRPr = rich_elem.find('.//a:defRPr', ns)
    if defRPr is None:
        return False, False, f"{label}: defRPr not found in rich"
    sz_def = defRPr.get('sz', '')
    latin_def = defRPr.find('a:latin', ns)
    tf_def = latin_def.get('typeface', '') if latin_def is not None else ''

    # Also check rPr on runs (if present)
    rPr_list = rich_elem.findall('.//a:rPr', ns)
    rpr_bad = []
    for rPr in rPr_list:
        sz_r = rPr.get('sz', sz_def)
        latin_r = rPr.find('a:latin', ns)
        tf_r = latin_r.get('typeface', tf_def) if latin_r is not None else tf_def
        if sz_r != TARGET_SIZE or tf_r != TARGET_TYPEFACE:
            rpr_bad.append(f"rPr sz={sz_r}, typeface={tf_r}")

    size_ok = (sz_def == TARGET_SIZE) and len(rpr_bad) == 0
    font_ok = (tf_def == TARGET_TYPEFACE) and len(rpr_bad) == 0
    details = f"{label}: defRPr sz={sz_def}, typeface={tf_def}"
    if rpr_bad:
        details += f"; rPr issues: {'; '.join(rpr_bad)}"
    return size_ok, font_ok, details


def verify_task(file_path):
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find chart XML - chart is on slide 4, embedded as chart1.xml
    chart_xml_path = None
    for name in zf.namelist():
        if name.startswith('ppt/charts/chart') and name.endswith('.xml'):
            chart_xml_path = name
            break

    if chart_xml_path is None:
        print("CRITICAL: No chart XML found in pptx")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open(chart_xml_path) as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    chart = root.find('c:chart', NS)
    if chart is None:
        print("CRITICAL: No c:chart element found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Chart title font — 10pt Calibri (0.2 points)
    try:
        title_elem = chart.find('c:title', NS)
        if title_elem is not None:
            rich = title_elem.find('.//c:rich', NS)
            size_ok, font_ok, details = check_rich_font(rich, NS, "Chart title")
            if size_ok and font_ok:
                print(f"PASS: Component 1 — Chart title is 10pt Calibri (0.2 pts). {details}")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — {details}")
        else:
            print("FAIL: Component 1 — Chart title element not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Category axis title font — 10pt Calibri (0.2 points)
    try:
        plot_area = chart.find('c:plotArea', NS)
        cat_ax = plot_area.find('c:catAx', NS) if plot_area is not None else None
        if cat_ax is not None:
            cat_title = cat_ax.find('c:title', NS)
            if cat_title is not None:
                rich = cat_title.find('.//c:rich', NS)
                size_ok, font_ok, details = check_rich_font(rich, NS, "CatAx title")
                if size_ok and font_ok:
                    print(f"PASS: Component 2 — Category axis title is 10pt Calibri (0.2 pts). {details}")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 2 — {details}")
            else:
                print("FAIL: Component 2 — Category axis title not found")
        else:
            print("FAIL: Component 2 — catAx not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Value axis title font — 10pt Calibri (0.2 points)
    try:
        val_ax = plot_area.find('c:valAx', NS) if plot_area is not None else None
        if val_ax is not None:
            val_title = val_ax.find('c:title', NS)
            if val_title is not None:
                rich = val_title.find('.//c:rich', NS)
                size_ok, font_ok, details = check_rich_font(rich, NS, "ValAx title")
                if size_ok and font_ok:
                    print(f"PASS: Component 3 — Value axis title is 10pt Calibri (0.2 pts). {details}")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — {details}")
            else:
                print("FAIL: Component 3 — Value axis title not found")
        else:
            print("FAIL: Component 3 — valAx not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Axis tick label fonts — both catAx and valAx txPr (0.2 points)
    try:
        cat_tick_ok = False
        val_tick_ok = False

        # Category axis tick labels
        if cat_ax is not None:
            cat_txPr = cat_ax.find('c:txPr', NS)
            s_ok, f_ok, details = check_txpr_font(cat_txPr, NS, "CatAx tick labels")
            cat_tick_ok = s_ok and f_ok
            if not cat_tick_ok:
                print(f"FAIL: Component 4a — {details}")
            else:
                print(f"PASS: Component 4a — {details}")

        # Value axis tick labels
        if val_ax is not None:
            val_txPr = val_ax.find('c:txPr', NS)
            s_ok, f_ok, details = check_txpr_font(val_txPr, NS, "ValAx tick labels")
            val_tick_ok = s_ok and f_ok
            if not val_tick_ok:
                print(f"FAIL: Component 4b — {details}")
            else:
                print(f"PASS: Component 4b — {details}")

        if cat_tick_ok and val_tick_ok:
            print(f"PASS: Component 4 — Both axis tick labels are 10pt Calibri (0.2 pts)")
            total_score += 0.2
        elif cat_tick_ok or val_tick_ok:
            print(f"PARTIAL: Component 4 — One of two axis tick labels correct (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Neither axis tick label is correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data labels font — 10pt Calibri (0.1 points)
    try:
        bar_chart = plot_area.find('c:barChart', NS) if plot_area is not None else None
        if bar_chart is not None:
            dLbls = bar_chart.find('c:dLbls', NS)
            if dLbls is not None:
                dLbls_txPr = dLbls.find('c:txPr', NS)
                s_ok, f_ok, details = check_txpr_font(dLbls_txPr, NS, "Data labels")
                if s_ok and f_ok:
                    print(f"PASS: Component 5 — Data labels are 10pt Calibri (0.1 pts). {details}")
                    total_score += 0.1
                else:
                    print(f"FAIL: Component 5 — {details}")
            else:
                print("FAIL: Component 5 — dLbls element not found")
        else:
            print("FAIL: Component 5 — barChart element not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Legend font — 10pt Calibri (0.1 points)
    try:
        legend = chart.find('c:legend', NS)
        if legend is not None:
            legend_txPr = legend.find('c:txPr', NS)
            s_ok, f_ok, details = check_txpr_font(legend_txPr, NS, "Legend")
            if s_ok and f_ok:
                print(f"PASS: Component 6 — Legend is 10pt Calibri (0.1 pts). {details}")
                total_score += 0.1
            else:
                print(f"FAIL: Component 6 — {details}")
        else:
            print("FAIL: Component 6 — Legend element not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

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
