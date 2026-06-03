"""
Reward Script: Create pie chart with title and percentage labels
Task ID: calc_gg1_015
Domain: libreoffice_calc
Scoring:
  Component 1: Pie chart exists on 'Market Share' sheet (0.3)
  Component 2: Chart title is 'Market Share by Region' (0.3)
  Component 3: Data labels configured to show percentages (0.2)
  Component 4: Chart data references correct range with 5 categories (0.2)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_015'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Precondition: 'Market Share' sheet must exist
    if 'Market Share' not in wb.sheetnames:
        print("FAIL: 'Market Share' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Market Share']

    # Component 1: A pie chart exists on the 'Market Share' sheet (0.3 points)
    try:
        charts = ws._charts
        pie_chart = None
        if len(charts) > 0:
            for ch in charts:
                if type(ch).__name__ == 'PieChart':
                    pie_chart = ch
                    break
        if pie_chart is not None:
            print(f"PASS: Component 1 — PieChart found on 'Market Share' sheet (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No PieChart found. Charts present: {[type(c).__name__ for c in charts]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chart title is 'Market Share by Region' (0.3 points)
    try:
        if pie_chart is not None and pie_chart.title is not None:
            # Extract title text from the Title object
            title_text = None
            title_obj = pie_chart.title
            if hasattr(title_obj, 'tx') and title_obj.tx is not None:
                tx = title_obj.tx
                if hasattr(tx, 'rich') and tx.rich is not None:
                    # Extract text from rich text paragraphs
                    parts = []
                    for p in tx.rich.p:
                        for r in (p.r if p.r else []):
                            if hasattr(r, 't') and r.t:
                                parts.append(r.t)
                    if parts:
                        title_text = ''.join(parts)
                elif hasattr(tx, 'strRef') and tx.strRef is not None:
                    title_text = str(tx.strRef)
            # Fallback: try str representation
            if title_text is None:
                title_text = str(pie_chart.title)

            if title_text and title_text.strip() == 'Market Share by Region':
                print(f"PASS: Component 2 — Chart title is 'Market Share by Region' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Chart title is '{title_text}', expected 'Market Share by Region'")
        else:
            print(f"FAIL: Component 2 — No chart title found (pie_chart={'exists' if pie_chart else 'None'})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data labels show percentages (0.2 points)
    try:
        if pie_chart is not None:
            show_pct = False
            # Check chart-level dataLabels
            if hasattr(pie_chart, 'dataLabels') and pie_chart.dataLabels is not None:
                dl = pie_chart.dataLabels
                if hasattr(dl, 'showPercent') and dl.showPercent:
                    show_pct = True
            # Also check series-level dLbls
            if not show_pct and len(pie_chart.series) > 0:
                s = pie_chart.series[0]
                if hasattr(s, 'dLbls') and s.dLbls is not None:
                    if hasattr(s.dLbls, 'showPercent') and s.dLbls.showPercent:
                        show_pct = True
            if show_pct:
                print(f"PASS: Component 3 — Percentage labels enabled on pie chart (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — showPercent is not True on dataLabels")
        else:
            print(f"FAIL: Component 3 — No pie chart to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart references correct data and has categories for 5 regions (0.2 points)
    try:
        if pie_chart is not None and len(pie_chart.series) > 0:
            s = pie_chart.series[0]
            has_data_ref = False
            has_cat_ref = False

            # Check data reference includes B column values
            if hasattr(s, 'val') and s.val is not None:
                val_src = s.val
                if hasattr(val_src, 'numRef') and val_src.numRef is not None:
                    ref_str = val_src.numRef.f if hasattr(val_src.numRef, 'f') else ''
                    if 'B' in ref_str.upper():
                        has_data_ref = True
                        print(f"  Data ref: {ref_str}")

            # Check categories reference includes A column
            if hasattr(s, 'cat') and s.cat is not None:
                cat_src = s.cat
                if hasattr(cat_src, 'numRef') and cat_src.numRef is not None:
                    ref_str = cat_src.numRef.f if hasattr(cat_src.numRef, 'f') else ''
                    if 'A' in ref_str.upper():
                        has_cat_ref = True
                        print(f"  Cat ref: {ref_str}")
                elif hasattr(cat_src, 'strRef') and cat_src.strRef is not None:
                    ref_str = cat_src.strRef.f if hasattr(cat_src.strRef, 'f') else ''
                    if 'A' in ref_str.upper():
                        has_cat_ref = True
                        print(f"  Cat ref: {ref_str}")

            if has_data_ref and has_cat_ref:
                print(f"PASS: Component 4 — Chart references correct data range with categories (0.2 pts)")
                total_score += 0.2
            elif has_data_ref:
                print(f"PARTIAL: Component 4 — Data ref OK but categories ref missing (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — Chart data references not pointing to correct range")
        else:
            print(f"FAIL: Component 4 — No pie chart or no series")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
