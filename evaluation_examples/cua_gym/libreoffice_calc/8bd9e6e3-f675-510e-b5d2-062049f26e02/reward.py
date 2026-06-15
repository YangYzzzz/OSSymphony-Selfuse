"""
Reward Script: Create a scatter plot with linear regression trendline and formatting
Task ID: calc_chart_scatter_regression_080
Domain: libreoffice_calc
Scoring:
  - Component 1: Scatter chart exists on StudyData sheet (0.25 pts)
  - Component 2: Chart title is 'Study Hours vs Exam Score' AND axis titles present (0.20 pts)
  - Component 3: Linear trendline with equation displayed (dispEq=True) (0.25 pts)
  - Component 4: Data point marker color is #1565C0 (dark blue) (0.15 pts)
  - Component 5: White background (#FFFFFF) in chart area (0.15 pts)
"""

import os
import zipfile
import lxml.etree as ET
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_scatter_regression_080'

# XML namespace used in chart XML
C_NS = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_chart_xml_root(file_path):
    """Extract chart XML from xlsx and return parsed root element."""
    with zipfile.ZipFile(file_path, 'r') as z:
        chart_files = [f for f in z.namelist() if f.startswith('xl/charts/') and f.endswith('.xml')]
        if not chart_files:
            return None
        # Return first chart
        xml_data = z.read(chart_files[0])
        return ET.fromstring(xml_data)


def get_text_from_title(title_obj):
    """Extract plain text string from openpyxl Title object."""
    try:
        if title_obj is None:
            return None
        # Try getting text from rich text paragraph runs
        paragraphs = title_obj.tx.rich.p
        texts = []
        for p in paragraphs:
            if p.r:
                for run in p.r:
                    texts.append(run.t)
        return ''.join(texts)
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: StudyData sheet must exist
    if 'StudyData' not in wb.sheetnames:
        print("CRITICAL: Sheet 'StudyData' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['StudyData']

    # Component 1: Scatter chart exists on StudyData sheet (0.25 points)
    # The initial file has 0 charts; golden file has 1 ScatterChart
    try:
        charts = ws._charts
        scatter_chart = None
        for c in charts:
            if isinstance(c, openpyxl.chart.ScatterChart):
                scatter_chart = c
                break

        if scatter_chart is not None:
            print(f"PASS: Component 1 — ScatterChart found on 'StudyData' sheet (0.25 pts)")
            total_score += 0.25
        else:
            chart_types = [type(c).__name__ for c in charts]
            print(f"FAIL: Component 1 — No ScatterChart found. Charts present: {chart_types}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        scatter_chart = None

    # If no scatter chart, remaining components cannot pass
    if scatter_chart is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Chart title is 'Study Hours vs Exam Score' AND axis titles contain
    # 'Study Hours' and 'Exam Score' (0.20 points)
    try:
        title_text = get_text_from_title(scatter_chart.title)
        x_axis_title = get_text_from_title(scatter_chart.x_axis.title)
        y_axis_title = get_text_from_title(scatter_chart.y_axis.title)

        print(f"  Chart title: {repr(title_text)}")
        print(f"  X axis title: {repr(x_axis_title)}")
        print(f"  Y axis title: {repr(y_axis_title)}")

        # Check chart title
        title_ok = (title_text is not None and
                    'study hours' in title_text.lower() and
                    'exam score' in title_text.lower())

        # Check axis titles (flexible: accept either axis containing 'Study Hours' or 'Exam Score')
        # The golden file has them set; the initial file has no chart, so no axis titles
        all_axis_texts = []
        if x_axis_title:
            all_axis_texts.append(x_axis_title.lower())
        if y_axis_title:
            all_axis_texts.append(y_axis_title.lower())

        has_study_hours_axis = any('study hours' in t for t in all_axis_texts)
        has_exam_score_axis = any('exam score' in t for t in all_axis_texts)

        if title_ok and has_study_hours_axis and has_exam_score_axis:
            print(f"PASS: Component 2 — Chart title and axis titles correct (0.20 pts)")
            total_score += 0.20
        elif title_ok:
            print(f"FAIL: Component 2 — Chart title OK but axis titles incomplete: "
                  f"study_hours={has_study_hours_axis}, exam_score={has_exam_score_axis}")
        else:
            print(f"FAIL: Component 2 — Chart title incorrect: {repr(title_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Linear trendline with equation displayed (0.25 points)
    # golden: trendlineType='linear', dispEq=True
    try:
        trendline = None
        if scatter_chart.series:
            ser = scatter_chart.series[0]
            trendline = getattr(ser, 'trendline', None)

        if trendline is not None:
            is_linear = (trendline.trendlineType == 'linear')
            disp_eq = (trendline.dispEq is True)
            print(f"  Trendline type: {trendline.trendlineType}, dispEq: {trendline.dispEq}")

            if is_linear and disp_eq:
                print(f"PASS: Component 3 — Linear trendline with equation displayed (0.25 pts)")
                total_score += 0.25
            elif is_linear:
                print(f"FAIL: Component 3 — Trendline is linear but equation not displayed (dispEq={trendline.dispEq})")
            else:
                print(f"FAIL: Component 3 — Trendline type is {trendline.trendlineType}, expected 'linear'")
        else:
            print(f"FAIL: Component 3 — No trendline found in series")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data point marker color is #1565C0 (dark blue) (0.15 points)
    # Check marker spPr solidFill srgbClr == '1565C0'
    try:
        marker_color_ok = False
        if scatter_chart.series:
            ser = scatter_chart.series[0]
            marker = getattr(ser, 'marker', None)
            if marker and marker.spPr and marker.spPr.solidFill:
                fill = marker.spPr.solidFill
                if hasattr(fill, 'srgbClr') and fill.srgbClr:
                    color_val = fill.srgbClr.upper()
                    print(f"  Marker color: #{color_val}")
                    if color_val == '1565C0':
                        marker_color_ok = True
                    else:
                        print(f"FAIL: Component 4 — Expected #1565C0, found #{color_val}")
                else:
                    print(f"FAIL: Component 4 — Marker solidFill has no srgbClr: {fill}")
            else:
                print(f"FAIL: Component 4 — Marker or spPr or solidFill not found")

        if marker_color_ok:
            print(f"PASS: Component 4 — Data point marker color is #1565C0 (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: White background (#FFFFFF) on chart area or plot area (0.15 points)
    # Read directly from chart XML since openpyxl doesn't expose chartSpace.spPr cleanly
    try:
        chart_root = get_chart_xml_root(file_path)
        white_bg_found = False

        if chart_root is not None:
            # chartSpace is root element (C_NS namespace).
            # spPr is a direct child of chartSpace, also in C_NS.
            # Inside spPr, solidFill/srgbClr are in A_NS.

            # Check chartSpace/spPr (root's direct child)
            cs_spPr = chart_root.find(f'{{{C_NS}}}spPr')
            if cs_spPr is not None:
                solid_fills = cs_spPr.findall(f'.//{{{A_NS}}}srgbClr')
                for sf in solid_fills:
                    val = sf.get('val', '').upper()
                    print(f"  chartSpace background: #{val}")
                    if val == 'FFFFFF':
                        white_bg_found = True

            if not white_bg_found:
                # Also check plotArea/spPr
                # plotArea is under chart, both in C_NS
                plot_area_list = chart_root.findall(f'.//{{{C_NS}}}plotArea')
                for pa in plot_area_list:
                    pa_spPr = pa.find(f'{{{C_NS}}}spPr')
                    if pa_spPr is not None:
                        solid_fills = pa_spPr.findall(f'.//{{{A_NS}}}srgbClr')
                        for sf in solid_fills:
                            val = sf.get('val', '').upper()
                            print(f"  plotArea background: #{val}")
                            if val == 'FFFFFF':
                                white_bg_found = True

        if white_bg_found:
            print(f"PASS: Component 5 — Chart background is white (#FFFFFF) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — White background (#FFFFFF) not found in chart area")
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
