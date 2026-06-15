"""
Reward Script: Create quota progress visualization chart in LibreOffice Calc
Task ID: calc_sales_quota_progress_chart_034
Domain: libreoffice_calc

Scoring rubric:
  Component 1: Chart exists in QuotaViz sheet (0.3 pts)
  Component 2: Chart title = 'Sales Quota vs Actual by Rep' AND has >= 2 series (0.3 pts)
  Component 3: First/Actual-Sales series has data labels with percentage format (0.2 pts)
  Component 4: Both series reference the correct data (Actual Sales + Quota columns) (0.2 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_sales_quota_progress_chart_034'


def get_chart_title_text(chart):
    """Extract plain text title from a chart object."""
    try:
        title = chart.title
        if title is None:
            return None
        tx = title.tx
        if tx is None:
            return None
        rich = tx.rich
        if rich is None:
            return None
        texts = []
        for para in rich.p:
            for run in para.r:
                texts.append(run.t)
        return ''.join(texts).strip()
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: QuotaViz sheet must exist
    if 'QuotaViz' not in wb.sheetnames:
        print("CRITICAL: Sheet 'QuotaViz' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['QuotaViz']
    charts = ws._charts

    # Component 1: A chart exists in the QuotaViz sheet (0.3 points)
    # FAILS on initial (0 charts), PASSES on golden (1 chart)
    try:
        if len(charts) >= 1:
            print(f"PASS: Component 1 — Chart exists in QuotaViz sheet ({len(charts)} chart(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No chart found in QuotaViz sheet")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Sales Quota vs Actual by Rep' AND has >= 2 series (0.3 points)
    # FAILS on initial (no chart), PASSES on golden
    try:
        if len(charts) >= 1:
            chart = charts[0]
            title_text = get_chart_title_text(chart)
            num_series = len(chart.series)
            title_ok = title_text is not None and 'Sales Quota vs Actual' in title_text
            series_ok = num_series >= 2

            if title_ok and series_ok:
                print(f"PASS: Component 2 — Chart title='{title_text}' and {num_series} series found (0.3 pts)")
                total_score += 0.3
            elif title_ok and not series_ok:
                print(f"FAIL: Component 2 — Title OK ('{title_text}') but only {num_series} series (expected >= 2)")
            elif not title_ok and series_ok:
                print(f"FAIL: Component 2 — {num_series} series OK but title='{title_text}' (expected 'Sales Quota vs Actual by Rep')")
            else:
                print(f"FAIL: Component 2 — title='{title_text}', {num_series} series")
        else:
            print("FAIL: Component 2 — No chart to check title/series")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Actual Sales series has data labels with percentage format (0.2 points)
    # The task requires attainment % as data labels on the Actual bars.
    # FAILS on initial (no chart), PASSES on golden (Series 0 has dLbls with showVal=True and percentage numFmt)
    try:
        if len(charts) >= 1:
            chart = charts[0]
            if len(chart.series) >= 1:
                # Find any series with data labels set to percentage format
                pct_label_series_idx = -1
                pct_label_fmt = None
                for s_idx, series in enumerate(chart.series):
                    if series.dLbls is not None:
                        dl = series.dLbls
                        # Check if labels are shown (showVal=True or showPercent=True)
                        shows_value = dl.showVal is True or dl.showPercent is True
                        # Check for percentage-style numFmt (e.g., '0.0%', '0%', '0.00%')
                        has_pct_fmt = (dl.numFmt is not None and '%' in str(dl.numFmt))
                        if shows_value and has_pct_fmt:
                            pct_label_series_idx = s_idx
                            pct_label_fmt = dl.numFmt
                            break
                        elif shows_value:
                            # Partial: labels shown but not in % format
                            print(f"INFO: Series {s_idx} has data labels (showVal={dl.showVal}) but numFmt='{dl.numFmt}' is not percentage format")
                if pct_label_series_idx >= 0:
                    print(f"PASS: Component 3 — Series {pct_label_series_idx} has data labels with percentage format (numFmt='{pct_label_fmt}') (0.2 pts)")
                    total_score += 0.2
                else:
                    print("FAIL: Component 3 — No series has data labels with percentage number format")
            else:
                print("FAIL: Component 3 — No series found in chart")
        else:
            print("FAIL: Component 3 — No chart to check data labels")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Both Actual Sales and Quota series reference correct data columns (0.2 points)
    # Actual Sales should reference column C ($C$2:$C$12 or similar),
    # Quota should reference column B ($B$2:$B$12 or similar).
    # Categories should reference column A (rep names: $A$2:$A$12).
    # FAILS on initial (no chart), PASSES on golden
    try:
        if len(charts) >= 1:
            chart = charts[0]
            if len(chart.series) >= 2:
                # Check that series reference both columns B and C
                series_refs = []
                for series in chart.series:
                    try:
                        if series.val and series.val.numRef:
                            series_refs.append(series.val.numRef.f)
                    except Exception:
                        pass

                # Check category reference covers column A (rep names)
                cat_refs = []
                for series in chart.series:
                    try:
                        if series.cat:
                            if series.cat.numRef:
                                cat_refs.append(series.cat.numRef.f)
                            elif series.cat.strRef:
                                cat_refs.append(series.cat.strRef.f)
                    except Exception:
                        pass

                # Check that series cover both B (Quota) and C (Actual Sales)
                has_col_b = any('$B$' in ref or '!B' in ref for ref in series_refs)
                has_col_c = any('$C$' in ref or '!C' in ref for ref in series_refs)
                has_col_a_cats = any('$A$' in ref or '!A' in ref or 'A2' in ref for ref in cat_refs)

                if has_col_b and has_col_c:
                    print(f"PASS: Component 4 — Series reference both Quota (col B) and Actual Sales (col C). Refs: {series_refs} (0.2 pts)")
                    total_score += 0.2
                elif has_col_c and not has_col_b:
                    print(f"FAIL: Component 4 — Actual Sales series found (col C) but no Quota series (col B). Refs: {series_refs}")
                elif has_col_b and not has_col_c:
                    print(f"FAIL: Component 4 — Quota series found (col B) but no Actual Sales series (col C). Refs: {series_refs}")
                else:
                    print(f"FAIL: Component 4 — Neither Quota (col B) nor Actual Sales (col C) reference found. Refs: {series_refs}")
            else:
                print(f"FAIL: Component 4 — Need >= 2 series to check data references, found {len(chart.series)}")
        else:
            print("FAIL: Component 4 — No chart to check series data references")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
