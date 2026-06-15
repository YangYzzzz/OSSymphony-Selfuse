"""
Reward Script: Embed bar chart from results.xlsx into slide 8 of acl2025_talk.odp
Task ID: impress_cross_acad_004
Domain: libreoffice_impress (ODP format)
Scoring:
  Component 1: Slide 8 contains an embedded OLE chart object (draw:object), replacing placeholder text (0.4 pts)
  Component 2: The embedded object is a bar chart (chart:class="chart:bar") (0.3 pts)
  Component 3: The chart data contains correct column headers matching results.xlsx (Baseline, OurModel/Our Model) (0.3 pts)
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_cross_acad_004'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. An embedded OLE chart object on slide 8 of acl2025_talk.odp (replacing the 'RESULTS CHART HERE' text box)
    2. The chart must be a bar chart
    3. The chart data must contain the correct series names from results.xlsx (Baseline, Our Model)
    """
    total_score = 0.0

    # Verify the file exists and is a valid zip (ODP format)
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            file_list = zf.namelist()
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path} as ZIP/ODP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read content.xml from the ODP
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('content.xml') as f:
                content = f.read().decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find slide 8 (index 7) using draw:page occurrences
    try:
        pages = [m.start() for m in re.finditer('<draw:page ', content)]
        if len(pages) < 8:
            print(f"FAIL: Presentation has fewer than 8 slides (found {len(pages)})")
            print("REWARD: 0.0")
            return 0.0

        start = pages[7]
        end = pages[8] if len(pages) > 8 else len(content)
        slide8_xml = content[start:end]
    except Exception as e:
        print(f"CRITICAL: Cannot parse slides: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Slide 8 contains an embedded OLE chart object (draw:object), replacing placeholder text (0.4 pts)
    # The golden state has <draw:object xlink:href="./Object 1" ...> on slide 8
    # The initial state has a text box with "RESULTS CHART HERE" only
    try:
        has_draw_object = '<draw:object ' in slide8_xml and 'xlink:href' in slide8_xml
        has_placeholder_text = 'RESULTS CHART HERE' in slide8_xml

        if has_draw_object:
            print(f"PASS: Component 1 — Slide 8 contains an embedded OLE object (draw:object with xlink:href) (0.4 pts)")
            total_score += 0.4
        else:
            if has_placeholder_text:
                print(f"FAIL: Component 1 — Slide 8 still has 'RESULTS CHART HERE' placeholder; no embedded object found")
            else:
                print(f"FAIL: Component 1 — No draw:object element found on slide 8")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The embedded object is a bar chart (0.3 pts)
    # Check if the Object 1/content.xml contains chart:class="chart:bar"
    try:
        has_object_dir = any(name.startswith('Object 1/') or name == 'Object 1/' for name in file_list)
        if not has_object_dir:
            print(f"FAIL: Component 2 — No 'Object 1/' directory found in ODP (no embedded chart object)")
        else:
            with zipfile.ZipFile(file_path, 'r') as zf:
                with zf.open('Object 1/content.xml') as f:
                    chart_content = f.read().decode('utf-8')

            # Check chart type: chart:bar
            is_bar_chart = 'chart:class="chart:bar"' in chart_content
            if is_bar_chart:
                print(f"PASS: Component 2 — Embedded object is a bar chart (chart:class='chart:bar') (0.3 pts)")
                total_score += 0.3
            else:
                chart_type_match = re.search(r'chart:class="([^"]+)"', chart_content)
                found_type = chart_type_match.group(1) if chart_type_match else 'unknown'
                print(f"FAIL: Component 2 — Expected bar chart (chart:bar), found: {found_type}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The chart data contains the correct column headers from results.xlsx (Baseline, Our Model) (0.3 pts)
    # The golden chart data has series headers "Baseline" and "Our Model" / "OurModel" derived from results.xlsx
    try:
        has_object_dir = any(name.startswith('Object 1/') or name == 'Object 1/' for name in file_list)
        if not has_object_dir:
            print(f"FAIL: Component 3 — No 'Object 1/' directory found in ODP (no embedded chart object)")
        else:
            with zipfile.ZipFile(file_path, 'r') as zf:
                with zf.open('Object 1/content.xml') as f:
                    chart_content = f.read().decode('utf-8')

            # Look for Baseline and Our Model / OurModel series names in the chart data
            has_baseline = bool(re.search(r'<text:p>\s*Baseline\s*</text:p>', chart_content))
            # Accept both "Our Model" and "OurModel" as the column header in results.xlsx
            has_ourmodel = bool(re.search(r'<text:p>\s*Our\s*Model\s*</text:p>', chart_content) or
                                re.search(r'<text:p>\s*OurModel\s*</text:p>', chart_content))

            if has_baseline and has_ourmodel:
                print(f"PASS: Component 3 — Chart data contains correct series headers 'Baseline' and 'Our Model'/'OurModel' from results.xlsx (0.3 pts)")
                total_score += 0.3
            elif has_baseline:
                print(f"FAIL: Component 3 — Found 'Baseline' series but missing 'Our Model'/'OurModel' series header")
            elif has_ourmodel:
                print(f"FAIL: Component 3 — Found 'Our Model'/'OurModel' series but missing 'Baseline' series header")
            else:
                print(f"FAIL: Component 3 — Neither 'Baseline' nor 'Our Model'/'OurModel' series headers found in chart data")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against the golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.odp'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
