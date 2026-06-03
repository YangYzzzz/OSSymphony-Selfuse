"""
Reward Script: Create a 3D pie chart showing the breakdown of customer complaints by category.
Task ID: calc_chart_pie_3d_066
Domain: libreoffice_calc
Scoring:
  - Component 1: A 3D pie chart (PieChart3D) exists on the 'Complaints' sheet — 0.4 pts
  - Component 2: Chart title is 'Customer Complaints by Category' — 0.3 pts
  - Component 3: Chart data range covers all 6 categories (B2:B7 with cats A2:A7) — 0.3 pts
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_pie_3d_066'


def get_title_text(chart):
    """Extract plain text from a chart title object."""
    try:
        title = chart.title
        if title is None:
            return None
        if hasattr(title, 'tx') and title.tx:
            tx = title.tx
            if hasattr(tx, 'rich') and tx.rich:
                texts = []
                for p in tx.rich.p:
                    if hasattr(p, 'r') and p.r:
                        for r in p.r:
                            if hasattr(r, 't') and r.t:
                                texts.append(r.t)
                return ''.join(texts) if texts else None
        # Sometimes title is a plain string
        if isinstance(title, str):
            return title
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the workbook — precondition gate
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: 'Complaints' sheet must exist
    if 'Complaints' not in wb.sheetnames:
        print("FAIL: 'Complaints' sheet not found in workbook")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    ws = wb['Complaints']

    # Gate: at least one chart must exist
    charts = ws._charts
    if not charts:
        print("FAIL: No charts found on 'Complaints' sheet")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    chart = charts[0]

    # Component 1: Chart is a 3D pie chart — PieChart3D type (0.4 points)
    # The initial file has NO charts, so this check always fails on initial.
    try:
        chart_type_name = type(chart).__name__
        if chart_type_name == 'PieChart3D':
            print(f"PASS: Component 1 — Chart is PieChart3D (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected PieChart3D, found {chart_type_name}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Customer Complaints by Category' (0.3 points)
    # The initial file has no chart, so no title to check — fails on initial.
    try:
        title_text = get_title_text(chart)
        expected_title = 'Customer Complaints by Category'
        if title_text and title_text.strip() == expected_title:
            print(f"PASS: Component 2 — Chart title is '{title_text}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected title '{expected_title}', found: {repr(title_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart data covers all 6 categories (B2:B7 values, A2:A7 categories) (0.3 points)
    # The initial file has no chart — fails on initial.
    try:
        data_ref_found = None
        cat_ref_found = None

        # Check the value data reference covers rows 2 through 7 (6 categories)
        if chart.series:
            series = chart.series[0]
            # Check values reference
            if hasattr(series, 'val') and series.val:
                val = series.val
                if hasattr(val, 'numRef') and val.numRef:
                    data_ref_found = val.numRef.ref
                else:
                    print("  Could not find numRef for series values")
            else:
                print("  Series has no val attribute")

            # Check categories reference
            if hasattr(series, 'cat') and series.cat:
                cat = series.cat
                if hasattr(cat, 'strRef') and cat.strRef:
                    cat_ref_found = cat.strRef.ref
                elif hasattr(cat, 'numRef') and cat.numRef:
                    cat_ref_found = cat.numRef.ref
                else:
                    print("  No category reference found")
            else:
                print("  Series has no cat attribute")
        else:
            print("  Chart has no series")

        # Normalize references (strip absolute $ and sheet prefix) for comparison
        data_covers_range = (
            data_ref_found is not None and
            'B2' in data_ref_found.replace('$', '').replace("'Complaints'!", '').replace('Complaints!', '') and
            'B7' in data_ref_found.replace('$', '').replace("'Complaints'!", '').replace('Complaints!', '')
        )
        cats_covers_range = (
            cat_ref_found is not None and
            'A2' in cat_ref_found.replace('$', '').replace("'Complaints'!", '').replace('Complaints!', '') and
            'A7' in cat_ref_found.replace('$', '').replace("'Complaints'!", '').replace('Complaints!', '')
        )

        if data_ref_found:
            print(f"  Data ref: {data_ref_found} — covers B2:B7: {data_covers_range}")
        if cat_ref_found:
            print(f"  Cat ref: {cat_ref_found} — covers A2:A7: {cats_covers_range}")

        if data_covers_range and cats_covers_range:
            print(f"PASS: Component 3 — Data range covers all 6 categories (B2:B7, A2:A7) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Data range incomplete (data_covers_range={data_covers_range}, cats_covers_range={cats_covers_range})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
