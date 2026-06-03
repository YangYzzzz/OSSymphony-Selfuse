"""
Reward Script: Change the chart background to light gray (#F5F5F5) and add a thin border
               (#BDBDBD, 1pt) around the chart plot area on slide 2.
Task ID: impress_tct_055
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): Chart background fill is solid #F5F5F5
  Component 2 (0.5): Plot area border is solid #BDBDBD, ~1pt (12700 EMU)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_055'

# XML namespaces used in OOXML chart files
NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def find_chart_xml_name(zf):
    """Find chart XML files inside the pptx archive."""
    return [n for n in zf.namelist() if n.startswith('ppt/charts/chart') and n.endswith('.xml')]


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

    # Locate chart XML (we expect chart1.xml for the chart on slide 2)
    chart_files = find_chart_xml_name(zf)
    if not chart_files:
        print("FAIL: No chart XML found in the presentation.")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Use the first chart file (chart on slide 2)
    chart_xml_path = chart_files[0]
    try:
        chart_content = zf.read(chart_xml_path).decode('utf-8')
        root = ET.fromstring(chart_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse {chart_xml_path}: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: Chart background fill is solid #F5F5F5 (0.5 points)
    # The chart background is set via <c:spPr> directly under <c:chartSpace>.
    # We check for <a:solidFill><a:srgbClr val="F5F5F5"/></a:solidFill>.
    # ---------------------------------------------------------------
    try:
        # Find c:spPr that is a direct child of c:chartSpace (the root)
        chart_spPr = root.find('c:spPr', NS)
        if chart_spPr is not None:
            solid_fill = chart_spPr.find('a:solidFill', NS)
            if solid_fill is not None:
                srgb = solid_fill.find('a:srgbClr', NS)
                if srgb is not None:
                    bg_color = srgb.get('val', '').upper()
                    if bg_color == 'F5F5F5':
                        print(f"PASS: Component 1 — Chart background fill is #F5F5F5 (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 1 — Chart background color is #{bg_color}, expected #F5F5F5")
                else:
                    print("FAIL: Component 1 — Chart background fill is not srgbClr type")
            else:
                print("FAIL: Component 1 — No solidFill in chart spPr")
        else:
            print("FAIL: Component 1 — No spPr element on chartSpace (no background fill set)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Plot area border is solid #BDBDBD, ~1pt/12700 EMU (0.5 points)
    # The plot area border is set via <c:spPr><a:ln> under <c:plotArea>.
    # We check for <a:ln w="12700"><a:solidFill><a:srgbClr val="BDBDBD"/></a:solidFill></a:ln>.
    # We allow some tolerance on width: between 10000 and 15000 EMU (~0.8pt to 1.2pt).
    # ---------------------------------------------------------------
    try:
        chart_elem = root.find('c:chart', NS)
        if chart_elem is None:
            print("FAIL: Component 2 — No c:chart element found")
        else:
            plot_area = chart_elem.find('c:plotArea', NS)
            if plot_area is None:
                print("FAIL: Component 2 — No c:plotArea element found")
            else:
                plot_spPr = plot_area.find('c:spPr', NS)
                if plot_spPr is None:
                    print("FAIL: Component 2 — No spPr on plotArea (no border set)")
                else:
                    ln = plot_spPr.find('a:ln', NS)
                    if ln is None:
                        print("FAIL: Component 2 — No a:ln element on plotArea spPr (no border)")
                    else:
                        # Check border width
                        width_str = ln.get('w', '0')
                        width = int(width_str)
                        width_ok = 10000 <= width <= 15000

                        # Check border color
                        border_fill = ln.find('a:solidFill', NS)
                        color_ok = False
                        actual_color = None
                        if border_fill is not None:
                            border_srgb = border_fill.find('a:srgbClr', NS)
                            if border_srgb is not None:
                                actual_color = border_srgb.get('val', '').upper()
                                color_ok = (actual_color == 'BDBDBD')

                        if width_ok and color_ok:
                            print(f"PASS: Component 2 — Plot area border: #{actual_color}, width={width} EMU (0.5 pts)")
                            total_score += 0.5
                        else:
                            details = []
                            if not width_ok:
                                details.append(f"width={width} EMU (expected ~12700)")
                            if not color_ok:
                                details.append(f"color=#{actual_color} (expected #BDBDBD)")
                            print(f"FAIL: Component 2 — Plot area border issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    zf.close()

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
