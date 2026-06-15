"""
Reward Script: Print settings for charts only on the 'Charts' sheet
Task ID: calc_mcp_085
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Print area is set on Charts sheet and excludes data columns (A-E)
  Component 2 (0.3): Print area covers chart region (col F+ where charts are anchored)
  Component 3 (0.2): Page setup scale is 100 (charts at displayed/screen size)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_085'


def parse_print_area(print_area_str):
    """Parse a print area string like "'Charts'!$F$1:$W$34" into components."""
    if not print_area_str:
        return None
    # Remove sheet name prefix
    match = re.search(r'\$([A-Z]+)\$(\d+):\$([A-Z]+)\$(\d+)', str(print_area_str))
    if not match:
        return None
    return {
        'start_col': match.group(1),
        'start_row': int(match.group(2)),
        'end_col': match.group(3),
        'end_row': int(match.group(4)),
    }


def col_to_num(col_letter):
    """Convert column letter(s) to number. A=1, B=2, ..., Z=26, AA=27."""
    num = 0
    for ch in col_letter:
        num = num * 26 + (ord(ch) - ord('A') + 1)
    return num


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Charts' sheet must exist
    if 'Charts' not in wb.sheetnames:
        print("FAIL: 'Charts' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Charts']

    # Precondition: Charts sheet must have charts (data integrity)
    if len(ws._charts) < 1:
        print("FAIL: No charts found in 'Charts' sheet — data integrity issue")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Print area is set on Charts sheet AND excludes data columns A-E (0.5 points)
    # The task says "print charts only, not the cell data". Data is in columns A-D.
    # So the print area must be set and must NOT include columns A through E.
    try:
        print_area = ws.print_area
        if print_area:
            # print_area can be a string or list; normalize
            pa_str = str(print_area)
            parsed = parse_print_area(pa_str)
            if parsed:
                start_col_num = col_to_num(parsed['start_col'])
                # Data is in columns A-D (1-4). Print area must start at E(5) or later
                # to exclude data.
                if start_col_num >= 5:
                    print(f"PASS: Component 1 — Print area '{pa_str}' is set and excludes data columns A-D (start col={parsed['start_col']}) (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 — Print area starts at column {parsed['start_col']} which includes data columns")
            else:
                print(f"FAIL: Component 1 — Print area '{pa_str}' could not be parsed")
        else:
            print("FAIL: Component 1 — No print area set on Charts sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Print area covers the chart region (0.3 points)
    # Charts are anchored at col=5 (F), rows 1 and 17. The print area should
    # encompass this chart region — starting no later than col F row 1, and
    # extending to cover both charts (at least through ~row 30).
    try:
        print_area = ws.print_area
        if print_area:
            pa_str = str(print_area)
            parsed = parse_print_area(pa_str)
            if parsed:
                start_col_num = col_to_num(parsed['start_col'])
                end_col_num = col_to_num(parsed['end_col'])
                # Charts at col 5 (F). Print area must include col F (6) at minimum.
                # Start col should be <= F(6) and end col should be >= some reasonable width.
                # Start row should be <= 1, end row should be >= 30 to cover both charts.
                covers_charts = (
                    start_col_num <= 6 and  # starts at or before column F
                    end_col_num >= 10 and   # extends at least to column J (reasonable chart width)
                    parsed['start_row'] <= 2 and  # starts at or near top
                    parsed['end_row'] >= 28  # covers both charts (chart 2 starts at row 17)
                )
                if covers_charts:
                    print(f"PASS: Component 2 — Print area covers chart region ({parsed['start_col']}{parsed['start_row']}:{parsed['end_col']}{parsed['end_row']}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Print area {pa_str} does not adequately cover chart region")
            else:
                print(f"FAIL: Component 2 — Could not parse print area")
        else:
            print("FAIL: Component 2 — No print area set")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page setup scale is 100 — charts at displayed/screen size (0.2 points)
    # The task says "Charts should print at their displayed size", meaning scale=100%.
    try:
        ps = ws.page_setup
        scale = ps.scale
        if scale is not None and int(scale) == 100:
            print(f"PASS: Component 3 — Page setup scale is 100% (displayed size) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Page setup scale is {scale}, expected 100")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
