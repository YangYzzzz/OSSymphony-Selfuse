"""
Reward Script: Format Y-axis of chart to display values in thousands with 'K' suffix
Task ID: calc_chart_axis_number_format_050
Domain: libreoffice_calc
Scoring:
  Component 1: Y-axis has a numFmt object (not None)                  — 0.3 pts
  Component 2: numFmt formatCode contains 'K' suffix (thousands fmt)  — 0.4 pts
  Component 3: numFmt sourceLinked is False                           — 0.3 pts
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_chart_axis_number_format_050'


def verify_task(file_path):
    """
    Verify task completion: Y-axis of the column chart on 'BigNumbers' sheet
    must have a custom number format showing values in thousands with a 'K' suffix.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'BigNumbers' sheet must exist
    if 'BigNumbers' not in wb.sheetnames:
        print("FAIL: Sheet 'BigNumbers' not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['BigNumbers']

    # Precondition: chart must exist
    if not hasattr(ws, '_charts') or len(ws._charts) == 0:
        print("FAIL: No charts found on 'BigNumbers' sheet")
        print("REWARD: 0.0")
        return 0.0

    chart = ws._charts[0]

    # Precondition: chart must have a y_axis
    if not hasattr(chart, 'y_axis') or chart.y_axis is None:
        print("FAIL: Chart has no y_axis")
        print("REWARD: 0.0")
        return 0.0

    y_axis = chart.y_axis

    # Component 1: Y-axis numFmt is set (not None) (0.3 points)
    # In the initial file, y_axis.numFmt is None.
    # After task completion, a NumFmt object must be present.
    try:
        num_fmt = y_axis.numFmt
        if num_fmt is not None:
            print(f"PASS: Component 1 — Y-axis numFmt is set: {num_fmt} (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — Y-axis numFmt is None (no custom format applied)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not access y_axis.numFmt: {e}")

    # Component 2: numFmt formatCode indicates thousands with 'K' suffix (0.4 points)
    # The golden file uses '#,##0,"K"' which divides by 1000 and appends "K".
    # We check that the formatCode contains '"K"' or 'K' in a way consistent with
    # a thousands display format (divide by 1000 and append K suffix).
    try:
        num_fmt = y_axis.numFmt
        if num_fmt is not None:
            format_code = num_fmt.formatCode if hasattr(num_fmt, 'formatCode') else str(num_fmt)
            format_code_upper = format_code.upper() if format_code else ''
            # Accept formats that contain K (case-insensitive) to handle variations
            # Common accepted formats: '#,##0,"K"', '0,"K"', '#,##0.0,"K"'
            # The key requirement: divide-by-1000 (comma after digit group) + K suffix
            has_k_suffix = 'K' in format_code_upper
            # Also check for the thousands-scaling comma pattern (e.g., #,##0,"K" or 0,"K")
            # In Excel/Calc format codes, a trailing comma after the number part divides by 1000
            has_thousands_scale = ',' in format_code and (
                format_code.strip().endswith(',"K"') or
                format_code.strip().endswith(',"k"') or
                ',"K"' in format_code or
                ',"k"' in format_code
            )
            if has_k_suffix and has_thousands_scale:
                print(f"PASS: Component 2 — Y-axis numFmt formatCode '{format_code}' has K-suffix thousands format (0.4 pts)")
                total_score += 0.4
            elif has_k_suffix:
                # Partial: has K but may not use thousands scaling properly
                print(f"PASS: Component 2 — Y-axis numFmt formatCode '{format_code}' contains 'K' suffix (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Y-axis numFmt formatCode '{format_code}' does not include 'K' suffix for thousands display")
        else:
            print("FAIL: Component 2 — Y-axis numFmt is None, cannot check formatCode")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check formatCode: {e}")

    # Component 3: numFmt sourceLinked is False (0.3 points)
    # sourceLinked=False means the format is custom (not linked to the source data format).
    # In the golden file, sourceLinked=False ensures the custom format is applied.
    try:
        num_fmt = y_axis.numFmt
        if num_fmt is not None:
            source_linked = num_fmt.sourceLinked if hasattr(num_fmt, 'sourceLinked') else None
            if source_linked is False:
                print(f"PASS: Component 3 — Y-axis numFmt sourceLinked=False (custom format not linked to source) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Y-axis numFmt sourceLinked={source_linked} (expected False for custom format)")
        else:
            print("FAIL: Component 3 — Y-axis numFmt is None, cannot check sourceLinked")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check sourceLinked: {e}")

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
