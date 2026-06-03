"""
Reward Script: Create a column chart and apply a professional dark theme
Task ID: calc_chart_copy_format_061
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on DarkTheme sheet (column/bar type)             — 0.20 pts
  Component 2: Chart title is 'Year-over-Year Comparison' with white text    — 0.20 pts
  Component 3: Chart outer background (chartSpace) is #2D2D2D dark gray      — 0.20 pts
  Component 4: Series colors: 'This Year'=#4FC3F7, 'Last Year'=#81C784       — 0.20 pts
  Component 5: White text (#FFFFFF) for axis labels and legend                — 0.20 pts
Total: 1.0
"""

import os
import re
import zipfile

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_copy_format_061'


def get_chart_xml(file_path):
    """Extract chart1.xml content from xlsx zip. Returns None if no chart found."""
    try:
        with zipfile.ZipFile(file_path) as z:
            chart_files = [n for n in z.namelist()
                           if re.search(r'xl/charts/chart\d+\.xml', n)]
            if not chart_files:
                return None
            # Return content of first chart
            return z.read(chart_files[0]).decode('utf-8')
    except Exception as e:
        print(f"ERROR: Cannot read chart XML from {file_path}: {e}")
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load workbook {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: DarkTheme sheet must exist
    if 'DarkTheme' not in wb.sheetnames:
        print("CRITICAL: 'DarkTheme' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['DarkTheme']

    # -------------------------------------------------------------------------
    # Component 1: Chart exists on DarkTheme sheet and is a column/bar chart (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        charts = ws._charts
        chart_count = len(charts)
        chart_type_name = type(charts[0]).__name__ if chart_count >= 1 else ''
        bar_dir_val = getattr(charts[0], 'barDir', None) if chart_count >= 1 else None

        if chart_count >= 1 and chart_type_name == 'BarChart' and bar_dir_val == 'col':
            print(f"PASS: Component 1 — Column chart found on DarkTheme sheet "
                  f"(type={chart_type_name}, barDir={bar_dir_val}) (0.20 pts)")
            total_score += 0.20
        elif chart_count >= 1:
            print(f"FAIL: Component 1 — Chart found but not a column chart "
                  f"(type={chart_type_name}, barDir={bar_dir_val})")
        else:
            print("FAIL: Component 1 — No chart found on DarkTheme sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For all remaining components, work directly with the chart XML
    chart_xml = get_chart_xml(file_path)
    if chart_xml is None:
        print("FAIL: Components 2-5 — No chart XML available in file")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # -------------------------------------------------------------------------
    # Component 2: Chart title is 'Year-over-Year Comparison' with white text (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        # Check title text
        title_match = re.search(r'<a:t>Year-over-Year Comparison</a:t>', chart_xml)
        # Check title text has white fill (srgbClr val="FFFFFF") in the title section
        # We look for the title block and verify white color inside it
        title_block = re.search(
            r'<title>(.*?)</title>', chart_xml, re.DOTALL)
        title_has_white = False
        if title_block:
            title_content = title_block.group(1)
            title_has_white = bool(re.search(
                r'<a:srgbClr val="FFFFFF"/>', title_content))

        if title_match and title_has_white:
            print("PASS: Component 2 — Chart title is 'Year-over-Year Comparison' "
                  "with white text (#FFFFFF) (0.20 pts)")
            total_score += 0.20
        elif title_match:
            print("FAIL: Component 2 — Chart title text is correct but white color not found in title")
        else:
            # Check if any title text is found at all
            any_title = re.search(r'<a:t>(.*?)</a:t>', chart_xml)
            if any_title:
                print(f"FAIL: Component 2 — Chart title found but wrong text: "
                      f"'{any_title.group(1)}'")
            else:
                print("FAIL: Component 2 — No chart title text found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Chart outer background (chartSpace spPr) is #2D2D2D (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        # The chartSpace-level spPr is the outermost background
        # Pattern: </chart><spPr>...<a:srgbClr val="2D2D2D"/>...
        # We look for spPr after the </chart> closing tag (chartSpace level)
        # Split on </chart> and check the spPr in the remaining content
        chart_space_part = chart_xml.split('</chart>')
        outer_section = chart_space_part[-1] if len(chart_space_part) >= 2 else ''
        outer_bg_correct = bool(re.search(
            r'<spPr>.*?<a:srgbClr val="2D2D2D"/>.*?</spPr>',
            outer_section, re.DOTALL))

        if outer_bg_correct:
            print("PASS: Component 3 — Chart outer background (chartSpace) "
                  "is #2D2D2D dark gray (0.20 pts)")
            total_score += 0.20
        else:
            # Try to extract actual color
            outer_color_match = re.search(
                r'<a:srgbClr val="([0-9A-Fa-f]{6})"/>',
                chart_space_part[-1] if len(chart_space_part) >= 2 else '')
            actual_color = outer_color_match.group(1) if outer_color_match else 'not found'
            print(f"FAIL: Component 3 — Chart outer background not #2D2D2D "
                  f"(found: #{actual_color})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Series colors: Series 0 = #4FC3F7, Series 1 = #81C784 (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        # Find all <ser> blocks and check their spPr fill colors
        ser_blocks = re.findall(r'<ser>(.*?)</ser>', chart_xml, re.DOTALL)

        def extract_series_color(ser_content):
            """Extract the srgbClr hex value from a series spPr block."""
            m = re.search(r'<spPr>.*?<a:srgbClr val="([0-9A-Fa-f]{6})"/>',
                          ser_content, re.DOTALL)
            return m.group(1).upper() if m else None

        if len(ser_blocks) >= 2:
            color_0 = extract_series_color(ser_blocks[0])
            color_1 = extract_series_color(ser_blocks[1])

            if color_0 == '4FC3F7' and color_1 == '81C784':
                total_score += 0.20
                print(f"PASS: Component 4 — Series colors correct: "
                      f"Series 0=#{color_0} (This Year/light blue), "
                      f"Series 1=#{color_1} (Last Year/green) (0.20 pts)")
            else:
                print(f"FAIL: Component 4 — Series colors incorrect: "
                      f"Series 0=#{color_0} (expected #4FC3F7), "
                      f"Series 1=#{color_1} (expected #81C784)")
        else:
            print(f"FAIL: Component 4 — Expected 2 series, found {len(ser_blocks)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    # Component 5: White text (#FFFFFF) for axis labels and legend (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        # Check catAx (category axis) txPr for white text
        # Check valAx (value axis) txPr for white text
        # Check legend txPr for white text

        def has_white_text_in_block(xml_content, block_tag):
            """Find block_tag and check if it contains white srgbClr."""
            block_match = re.search(
                rf'<{block_tag}>(.*?)</{block_tag}>', xml_content, re.DOTALL)
            if not block_match:
                return False, None
            block_content = block_match.group(1)
            # Look for txPr section with white fill
            txpr_match = re.search(r'<txPr>(.*?)</txPr>', block_content, re.DOTALL)
            if not txpr_match:
                return False, 'no txPr'
            txpr_content = txpr_match.group(1)
            has_white = bool(re.search(r'<a:srgbClr val="FFFFFF"/>', txpr_content))
            return has_white, txpr_content if not has_white else None

        catax_white, catax_info = has_white_text_in_block(chart_xml, 'catAx')
        valax_white, valax_info = has_white_text_in_block(chart_xml, 'valAx')
        legend_white, legend_info = has_white_text_in_block(chart_xml, 'legend')

        all_axes_white = catax_white and valax_white and legend_white

        if all_axes_white:
            print("PASS: Component 5 — White text (#FFFFFF) for catAx, valAx, "
                  "and legend (0.20 pts)")
            total_score += 0.20
        else:
            issues = []
            if not catax_white:
                issues.append(f"catAx axis labels not white (info: {catax_info})")
            if not valax_white:
                issues.append(f"valAx axis labels not white (info: {valax_info})")
            if not legend_white:
                issues.append(f"legend text not white (info: {legend_info})")
            print(f"FAIL: Component 5 — Not all text is white: {'; '.join(issues)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
