"""
Reward Script: Population Pyramid Chart
Task ID: calc_gcp_049
Domain: libreoffice_calc
Scoring:
  Component 1: Chart exists on Demographics sheet (0.20)
  Component 2: Chart is horizontal bar type (0.20)
  Component 3: Chart has 2 series covering Males and Females data (0.25)
  Component 4: Chart title references population pyramid (0.15)
  Component 5: Chart has axis titles for age group and population (0.20)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gcp_049'


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def extract_title_text(title_obj):
    """Extract plain text from an openpyxl chart Title object."""
    if title_obj is None:
        return None
    # Try direct .text property first
    try:
        txt = title_obj.text
        if isinstance(txt, str):
            return txt
    except Exception:
        pass
    # Try rich text extraction
    try:
        for p in title_obj.tx.rich.paragraphs:
            for r in p.r:
                if r.t:
                    return r.t
    except Exception:
        pass
    return None


def verify_task(file_path):
    """
    Verify population pyramid chart creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Demographics sheet must exist
    if 'Demographics' not in wb.sheetnames:
        print("CRITICAL: 'Demographics' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Demographics']

    # Component 1: Chart exists on Demographics sheet (0.20 points)
    # Initial has 0 charts; golden has >= 1
    try:
        chart_count = len(ws._charts)
        if chart_count >= 1:
            print(f"PASS: Component 1 -- Chart exists on Demographics ({chart_count} chart(s)) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- No charts found on Demographics sheet (count={chart_count})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If no charts, remaining components cannot pass
    if len(ws._charts) < 1:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    chart = ws._charts[0]

    # Component 2: Chart is horizontal bar type (0.20 points)
    # A population pyramid uses horizontal bars (type="bar" in openpyxl)
    try:
        chart_type = chart.type
        if chart_type == "bar":
            print(f"PASS: Component 2 -- Chart is horizontal bar type (type={chart_type}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- Expected bar (horizontal), found type={chart_type}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Chart has 2 series referencing Males and Females (0.25 points)
    # We check: exactly 2 series, one references column B (Males), one references column C (Females)
    try:
        series_count = len(chart.series)
        if series_count >= 2:
            # Check that series reference columns B and C from Demographics
            refs_found = set()
            for s in chart.series:
                val_ref = None
                try:
                    val_ref = s.val.numRef.f
                except Exception:
                    pass
                if val_ref:
                    val_ref_upper = val_ref.upper()
                    if '$B$' in val_ref_upper or '!B' in val_ref_upper:
                        refs_found.add('B')
                    if '$C$' in val_ref_upper or '!C' in val_ref_upper:
                        refs_found.add('C')
            if 'B' in refs_found and 'C' in refs_found:
                print(f"PASS: Component 3 -- 2 series referencing Males (B) and Females (C) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Series refs found: {refs_found}, expected B and C")
        else:
            print(f"FAIL: Component 3 -- Expected >= 2 series, found {series_count}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Chart title references population pyramid (0.15 points)
    try:
        title_text = extract_title_text(chart.title)
        if title_text and 'pyramid' in title_text.lower():
            print(f"PASS: Component 4 -- Chart title contains 'pyramid' (title='{title_text}') (0.15 pts)")
            total_score += 0.15
        elif title_text and 'population' in title_text.lower():
            # Partial: has population but not pyramid
            print(f"PARTIAL: Component 4 -- Title has 'population' but not 'pyramid' (title='{title_text}') (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 -- Expected title with 'pyramid', found: '{title_text}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Chart has axis titles for age group and population (0.20 points)
    # y_axis should mention age, x_axis should mention population/count
    try:
        y_title = extract_title_text(chart.y_axis.title)
        x_title = extract_title_text(chart.x_axis.title)
        axis_score = 0.0

        # Check y-axis title (age group)
        if y_title and 'age' in y_title.lower():
            axis_score += 0.10
            print(f"  PASS: Y-axis title contains 'age' (y_title='{y_title}')")
        else:
            print(f"  FAIL: Y-axis title expected 'age', found: '{y_title}'")

        # Check x-axis title (population/count)
        if x_title and ('population' in x_title.lower() or 'count' in x_title.lower() or 'number' in x_title.lower()):
            axis_score += 0.10
            print(f"  PASS: X-axis title contains population/count (x_title='{x_title}')")
        else:
            print(f"  FAIL: X-axis title expected 'population'/'count', found: '{x_title}'")

        if axis_score > 0:
            print(f"PASS: Component 5 -- Axis titles ({axis_score} pts)")
            total_score += axis_score
        else:
            print(f"FAIL: Component 5 -- No matching axis titles found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
