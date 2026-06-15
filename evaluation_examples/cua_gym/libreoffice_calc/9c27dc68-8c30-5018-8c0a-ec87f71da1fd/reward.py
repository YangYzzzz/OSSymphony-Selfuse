"""
Reward Script: Create a pie chart with revenue distribution and data labels
Task ID: calc_sales_087
Domain: libreoffice_calc
Scoring:
  - Component 1: Pie chart exists on ProductRev sheet (0.3 pts)
  - Component 2: Chart title is 'Revenue by Product Line' (0.2 pts)
  - Component 3: Data labels show category names (0.25 pts)
  - Component 4: Data labels show percentages (0.25 pts)
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'calc_sales_087'


def persist_app_state(domain: str):
    """Send Ctrl+S to save any unsaved GUI edits."""
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
    import openpyxl
    from openpyxl.chart import PieChart

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the ProductRev sheet
    if 'ProductRev' not in wb.sheetnames:
        print("FAIL: Sheet 'ProductRev' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ProductRev']

    # Component 1: A pie chart exists on the ProductRev sheet (0.3 points)
    try:
        charts = ws._charts
        pie_charts = [c for c in charts if isinstance(c, PieChart)]
        if len(pie_charts) > 0:
            print(f"PASS: Component 1 — Found {len(pie_charts)} pie chart(s) on ProductRev (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No pie charts found. Total charts: {len(charts)}, types: {[type(c).__name__ for c in charts]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no pie chart, remaining checks are moot
    if total_score < 0.1:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    pie = pie_charts[0]

    # Component 2: Chart title is 'Revenue by Product Line' (0.2 points)
    try:
        title_text = None
        if pie.title is not None:
            # Extract title text from the rich text structure
            if hasattr(pie.title, 'tx') and pie.title.tx is not None:
                tx = pie.title.tx
                if hasattr(tx, 'rich') and tx.rich is not None:
                    for p in tx.rich.p:
                        for r in (p.r or []):
                            if r.t:
                                title_text = r.t
                elif hasattr(tx, 'strRef') and tx.strRef is not None:
                    title_text = str(tx.strRef)
            # Fallback: try direct text attribute
            if title_text is None and hasattr(pie.title, 'text'):
                title_text = pie.title.text

        if title_text and title_text.strip() == 'Revenue by Product Line':
            print(f"PASS: Component 2 — Chart title is 'Revenue by Product Line' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected title 'Revenue by Product Line', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data labels show category names (0.25 points)
    try:
        dl = pie.dataLabels
        if dl is not None and dl.showCatName:
            print(f"PASS: Component 3 — Data labels show category names (showCatName=True) (0.25 pts)")
            total_score += 0.25
        else:
            show_cat = dl.showCatName if dl else None
            print(f"FAIL: Component 3 — showCatName={show_cat}, expected True")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data labels show percentages (0.25 points)
    try:
        dl = pie.dataLabels
        if dl is not None and dl.showPercent:
            print(f"PASS: Component 4 — Data labels show percentages (showPercent=True) (0.25 pts)")
            total_score += 0.25
        else:
            show_pct = dl.showPercent if dl else None
            print(f"FAIL: Component 4 — showPercent={show_pct}, expected True")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
