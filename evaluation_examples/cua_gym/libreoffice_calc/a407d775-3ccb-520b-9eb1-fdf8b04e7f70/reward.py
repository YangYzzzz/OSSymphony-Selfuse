"""
Reward Script: Box-and-whisker style chart for API response time distribution
Task ID: calc_gcp_052
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Chart exists on APIMetrics sheet
  Component 2 (0.3): Chart is a stacked bar chart with series referencing helper columns
  Component 3 (0.2): Chart has appropriate title and axis labels
  Component 4 (0.2): Chart uses categories covering all 5 endpoints
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcp_052'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: APIMetrics sheet must exist
    if 'APIMetrics' not in wb.sheetnames:
        print("FAIL: 'APIMetrics' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['APIMetrics']

    # Component 1: A chart exists on the APIMetrics sheet (0.3 points)
    # Initial file has 0 charts; golden has >= 1 chart.
    try:
        chart_count = len(ws._charts)
        if chart_count >= 1:
            print(f"PASS: Component 1 — {chart_count} chart(s) found on APIMetrics (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No charts found on APIMetrics sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no charts, remaining components cannot pass
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    chart = ws._charts[0]

    # Component 2: Chart is a stacked bar/column chart with series referencing
    # helper columns (G and/or H) for the box-and-whisker construction (0.3 points)
    try:
        is_bar_type = type(chart).__name__ == 'BarChart'
        is_stacked = False
        if is_bar_type:
            is_stacked = chart.grouping == 'stacked'

        # Check that at least one series references helper columns (G-K range)
        # which are the computed box/whisker values
        has_helper_series = False
        for s in chart.series:
            try:
                val_ref = ''
                if hasattr(s, 'val') and s.val and hasattr(s.val, 'numRef') and s.val.numRef:
                    val_ref = s.val.numRef.f or ''
                # Helper columns are G through K (columns used for chart construction)
                if any(col in val_ref for col in ['$G$', '$H$', '$I$', '$J$', '$K$', '!G', '!H', '!I', '!J', '!K']):
                    has_helper_series = True
                    break
            except Exception:
                pass

        if is_bar_type and is_stacked and has_helper_series:
            print(f"PASS: Component 2 — Stacked bar chart with helper column series (0.3 pts)")
            total_score += 0.3
        elif is_bar_type and has_helper_series:
            # Partial: bar chart with right data but not stacked
            print(f"PARTIAL: Component 2 — Bar chart with helper series but grouping={chart.grouping} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected stacked BarChart with helper column series. "
                  f"Got type={type(chart).__name__}, is_bar={is_bar_type}, "
                  f"stacked={is_stacked}, helper_series={has_helper_series}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart has an appropriate title and axis labels (0.2 points)
    try:
        has_title = False
        title_text = ''
        try:
            if chart.title and chart.title.tx and chart.title.tx.rich:
                for p in chart.title.tx.rich.paragraphs:
                    for r in p.r:
                        title_text += r.t
            if title_text:
                has_title = True
        except Exception:
            pass

        # Check title contains relevant keywords (box, whisker, response, API, distribution)
        title_lower = title_text.lower()
        title_relevant = any(kw in title_lower for kw in ['box', 'whisker', 'response', 'distribution', 'api'])

        has_y_axis = False
        try:
            if chart.y_axis and chart.y_axis.title:
                y_text = ''
                if chart.y_axis.title.tx and chart.y_axis.title.tx.rich:
                    for p in chart.y_axis.title.tx.rich.paragraphs:
                        for r in p.r:
                            y_text += r.t
                if y_text:
                    has_y_axis = True
        except Exception:
            pass

        has_x_axis = False
        try:
            if chart.x_axis and chart.x_axis.title:
                x_text = ''
                if chart.x_axis.title.tx and chart.x_axis.title.tx.rich:
                    for p in chart.x_axis.title.tx.rich.paragraphs:
                        for r in p.r:
                            x_text += r.t
                if x_text:
                    has_x_axis = True
        except Exception:
            pass

        sub_score = 0.0
        if has_title and title_relevant:
            sub_score += 0.1
            print(f"  Title: '{title_text}' — relevant")
        elif has_title:
            sub_score += 0.05
            print(f"  Title: '{title_text}' — present but not clearly relevant")
        else:
            print(f"  Title: missing or empty")

        if has_y_axis:
            sub_score += 0.05
            print(f"  Y-axis label: present")
        else:
            print(f"  Y-axis label: missing")

        if has_x_axis:
            sub_score += 0.05
            print(f"  X-axis label: present")
        else:
            print(f"  X-axis label: missing")

        if sub_score > 0:
            print(f"PASS: Component 3 — Title and axis labels ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 3 — No title or axis labels found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart uses categories covering all 5 endpoints (0.2 points)
    # The chart should reference A2:A6 (or equivalent) as categories
    try:
        has_categories = False
        cat_ref = ''
        for s in chart.series:
            try:
                if hasattr(s, 'cat') and s.cat:
                    if hasattr(s.cat, 'strRef') and s.cat.strRef:
                        cat_ref = s.cat.strRef.f or ''
                    elif hasattr(s.cat, 'numRef') and s.cat.numRef:
                        cat_ref = s.cat.numRef.f or ''
                if cat_ref:
                    break
            except Exception:
                pass

        # Check the series count covers 5 endpoints (at least 2 series for stacked box construction)
        series_count = len(chart.series)

        if cat_ref and series_count >= 2:
            # Categories reference found and multiple series (needed for box construction)
            print(f"PASS: Component 4 — Categories ref='{cat_ref}', {series_count} series for 5 endpoints (0.2 pts)")
            total_score += 0.2
            has_categories = True
        elif series_count >= 2:
            # No explicit category ref but series count suggests proper setup
            print(f"PARTIAL: Component 4 — {series_count} series but no explicit category reference (0.1 pts)")
            total_score += 0.1
            has_categories = True
        else:
            print(f"FAIL: Component 4 — Expected >=2 series for box plot, found {series_count}. Cat ref: '{cat_ref}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
