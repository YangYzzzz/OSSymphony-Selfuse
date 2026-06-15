"""
Reward Script: Create separate column charts for Inbound and Outbound shipment tables
Task ID: osworld_calc_dual_chart_separate_tables_005
Domain: libreoffice_calc
Scoring:
  Component 1: Two charts exist in the spreadsheet (0.2 pts)
  Component 2: Inbound chart has correct title (0.3 pts)
  Component 3: Inbound chart references inbound data range (rows 2-10, col B) (0.1 pts)
  Component 4: Outbound chart has correct title (0.3 pts)
  Component 5: Outbound chart references outbound data range (rows 13-21, col E) (0.1 pts)
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_dual_chart_separate_tables_005'


def extract_chart_title(chart):
    """Safely extract title text from a chart object."""
    try:
        return chart.title.tx.rich.p[0].r[0].t
    except Exception:
        pass
    try:
        return str(chart.title)
    except Exception:
        return None


def check_series_ref_contains(series, substring):
    """Check if the series value reference formula contains a given substring."""
    try:
        ref_formula = series.val.numRef.f
        return substring.lower() in ref_formula.lower()
    except Exception:
        return False


def check_cat_ref_contains(series, substring):
    """Check if the series category reference formula contains a given substring."""
    try:
        ref_formula = series.cat.numRef.f
        return substring.lower() in ref_formula.lower()
    except Exception:
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook
    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the active/only sheet — expected to be 'Shipments'
    try:
        ws = wb['Shipments']
    except KeyError:
        # Fall back to first sheet if sheet name differs
        ws = wb.worksheets[0]
        print(f"WARN: Sheet 'Shipments' not found, using first sheet: {ws.title}")

    # Collect all charts in this sheet
    charts = ws._charts

    # -----------------------------------------------------------------------
    # Component 1: Two charts exist in the spreadsheet (0.2 points)
    # The initial file has 0 charts; the agent must add 2 charts.
    # -----------------------------------------------------------------------
    try:
        num_charts = len(charts)
        if num_charts >= 2:
            print(f"PASS: Component 1 — {num_charts} charts found in sheet (expected >= 2) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected >= 2 charts, found {num_charts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Identify inbound and outbound charts by title
    inbound_chart = None
    outbound_chart = None
    for chart in charts:
        title = extract_chart_title(chart)
        if title is not None:
            title_lower = title.lower()
            if 'inbound' in title_lower:
                inbound_chart = chart
            elif 'outbound' in title_lower:
                outbound_chart = chart

    # -----------------------------------------------------------------------
    # Component 2: Inbound chart has correct title (0.3 points)
    # Expected title: 'Inbound Shipment Volume by Route'
    # -----------------------------------------------------------------------
    try:
        if inbound_chart is not None:
            title = extract_chart_title(inbound_chart)
            expected_title = 'Inbound Shipment Volume by Route'
            if title and title.strip() == expected_title:
                print(f"PASS: Component 2 — Inbound chart title is '{title}' (0.3 pts)")
                total_score += 0.3
            else:
                # Partial: title at least contains 'inbound'
                if title and 'inbound' in title.lower():
                    print(f"PARTIAL: Component 2 — Inbound chart found but title is '{title}', expected '{expected_title}' (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — Inbound chart title is '{title}', expected '{expected_title}'")
        else:
            print(f"FAIL: Component 2 — No chart with 'inbound' in title found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Inbound chart references correct data range (0.1 points)
    # Expected: data from B2:B10 (Inbound Volume column), cats from A2:A10
    # -----------------------------------------------------------------------
    try:
        if inbound_chart is not None and len(inbound_chart.series) > 0:
            series = inbound_chart.series[0]
            # Check that value reference is from column B, rows 2-10
            val_ok = check_series_ref_contains(series, '$B$2:$B$10') or check_series_ref_contains(series, 'B2:B10')
            cat_ok = check_cat_ref_contains(series, '$A$2:$A$10') or check_cat_ref_contains(series, 'A2:A10')
            if val_ok and cat_ok:
                print(f"PASS: Component 3 — Inbound chart data references correct inbound range (B2:B10/A2:A10) (0.1 pts)")
                total_score += 0.1
            elif val_ok or cat_ok:
                # One of the two references is correct — partial credit
                try:
                    val_ref = series.val.numRef.f
                except Exception:
                    val_ref = 'unknown'
                try:
                    cat_ref = series.cat.numRef.f
                except Exception:
                    cat_ref = 'unknown'
                inbound_partial_ref_match = val_ok or cat_ok
                if inbound_partial_ref_match:
                    print(f"PARTIAL: Component 3 — Inbound chart partial ref match: val={val_ref}, cat={cat_ref} (0.05 pts)")
                    total_score += 0.05
            else:
                try:
                    val_ref = series.val.numRef.f
                except Exception:
                    val_ref = 'unknown'
                print(f"FAIL: Component 3 — Inbound chart data ref is '{val_ref}', expected col B rows 2-10")
        else:
            print(f"FAIL: Component 3 — No inbound chart or no series found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Outbound chart has correct title (0.3 points)
    # Expected title: 'Outbound Shipment Volume by Route'
    # -----------------------------------------------------------------------
    try:
        if outbound_chart is not None:
            title = extract_chart_title(outbound_chart)
            expected_title = 'Outbound Shipment Volume by Route'
            if title and title.strip() == expected_title:
                print(f"PASS: Component 4 — Outbound chart title is '{title}' (0.3 pts)")
                total_score += 0.3
            else:
                if title and 'outbound' in title.lower():
                    print(f"PARTIAL: Component 4 — Outbound chart found but title is '{title}', expected '{expected_title}' (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — Outbound chart title is '{title}', expected '{expected_title}'")
        else:
            print(f"FAIL: Component 4 — No chart with 'outbound' in title found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Outbound chart references correct data range (0.1 points)
    # Expected: data from E13:E21 (Outbound Volume column), cats from D13:D21
    # -----------------------------------------------------------------------
    try:
        if outbound_chart is not None and len(outbound_chart.series) > 0:
            series = outbound_chart.series[0]
            # Check value reference is from column E, rows 13-21
            val_ok = check_series_ref_contains(series, '$E$13:$E$21') or check_series_ref_contains(series, 'E13:E21')
            cat_ok = check_cat_ref_contains(series, '$D$13:$D$21') or check_cat_ref_contains(series, 'D13:D21')
            if val_ok and cat_ok:
                print(f"PASS: Component 5 — Outbound chart data references correct outbound range (E13:E21/D13:D21) (0.1 pts)")
                total_score += 0.1
            elif val_ok or cat_ok:
                # One of the two references is correct — partial credit
                try:
                    val_ref = series.val.numRef.f
                except Exception:
                    val_ref = 'unknown'
                try:
                    cat_ref = series.cat.numRef.f
                except Exception:
                    cat_ref = 'unknown'
                outbound_partial_ref_match = val_ok or cat_ok
                if outbound_partial_ref_match:
                    print(f"PARTIAL: Component 5 — Outbound chart partial ref match: val={val_ref}, cat={cat_ref} (0.05 pts)")
                    total_score += 0.05
            else:
                try:
                    val_ref = series.val.numRef.f
                except Exception:
                    val_ref = 'unknown'
                print(f"FAIL: Component 5 — Outbound chart data ref is '{val_ref}', expected col E rows 13-21")
        else:
            print(f"FAIL: Component 5 — No outbound chart or no series found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
