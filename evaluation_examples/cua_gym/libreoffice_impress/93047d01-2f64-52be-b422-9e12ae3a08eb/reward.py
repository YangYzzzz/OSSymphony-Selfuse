"""
Reward Script: Insert a 3D pie chart on slide 7 showing market share data
Task ID: impress_tm_087
Domain: libreoffice_impress
Scoring:
  Component 1: Chart shape exists on slide 7 (0.20)
  Component 2: Chart is 3D pie type (0.20)
  Component 3: Correct categories and values (0.30)
  Component 4: Percentage data labels shown (0.15)
  Component 5: Legend present (0.15)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_087'

# Namespaces used in chart XML
NS_C = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_RELS = 'http://schemas.openxmlformats.org/package/2006/relationships'

EXPECTED_CATEGORIES = ['Company A', 'Company B', 'Company C', 'Others']
EXPECTED_VALUES = [42.0, 28.0, 18.0, 12.0]


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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


def find_chart_on_slide7(pptx_path):
    """Check if slide 7 has a chart relationship and return the chart XML path."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Check slide7 relationships for chart reference
        rels_path = 'ppt/slides/_rels/slide7.xml.rels'
        if rels_path not in zf.namelist():
            return None
        rels_xml = zf.read(rels_path).decode()
        rels_root = ET.fromstring(rels_xml)
        for rel in rels_root.findall(f'{{{NS_RELS}}}Relationship'):
            rel_type = rel.get('Type', '')
            if 'chart' in rel_type.lower():
                target = rel.get('Target', '')
                # Target is relative: ../charts/chart1.xml -> ppt/charts/chart1.xml
                chart_path = 'ppt/' + target.replace('../', '')
                if chart_path in zf.namelist():
                    return chart_path
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Chart shape exists on slide 7 (0.20 points)
    chart_path = None
    try:
        chart_path = find_chart_on_slide7(file_path)
        if chart_path:
            print(f"PASS: Component 1 — Chart found on slide 7 at {chart_path} (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 1 — No chart found on slide 7")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if not chart_path:
        # No chart means remaining checks cannot pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        zf.close()
        return final_score

    # Parse chart XML for remaining components
    try:
        chart_xml = zf.read(chart_path).decode()
        chart_root = ET.fromstring(chart_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse chart XML: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        zf.close()
        return final_score

    # Component 2: Chart is 3D pie type (0.20 points)
    try:
        # Look for pie3DChart element anywhere in chart XML
        pie3d = chart_root.find(f'.//{{{NS_C}}}pie3DChart')
        if pie3d is not None:
            print("PASS: Component 2 — Chart is pie3DChart (3D pie) (0.20 pts)")
            total_score += 0.20
        else:
            # Check if it's at least a regular pie chart
            pie = chart_root.find(f'.//{{{NS_C}}}pieChart')
            if pie is not None:
                print("FAIL: Component 2 — Chart is a pie chart but NOT 3D (pie3DChart expected)")
            else:
                print("FAIL: Component 2 — Chart is not a pie chart type")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct categories and values (0.30 points)
    # Sub-scored: 0.15 for categories, 0.15 for values
    try:
        pie3d = chart_root.find(f'.//{{{NS_C}}}pie3DChart')
        # Fall back to pieChart if pie3DChart not found
        chart_elem = pie3d if pie3d is not None else chart_root.find(f'.//{{{NS_C}}}pieChart')

        if chart_elem is None:
            print("FAIL: Component 3 — No pie chart element found to check data")
        else:
            ser = chart_elem.find(f'{{{NS_C}}}ser')
            if ser is None:
                print("FAIL: Component 3 — No series found in pie chart")
            else:
                # Extract categories
                cat_elem = ser.find(f'{{{NS_C}}}cat')
                actual_cats = []
                if cat_elem is not None:
                    str_cache = cat_elem.find(f'.//{{{NS_C}}}strCache')
                    if str_cache is not None:
                        for pt in str_cache.findall(f'{{{NS_C}}}pt'):
                            v = pt.find(f'{{{NS_C}}}v')
                            if v is not None and v.text:
                                actual_cats.append(v.text.strip())

                # Extract values
                val_elem = ser.find(f'{{{NS_C}}}val')
                actual_vals = []
                if val_elem is not None:
                    num_cache = val_elem.find(f'.//{{{NS_C}}}numCache')
                    if num_cache is not None:
                        for pt in num_cache.findall(f'{{{NS_C}}}pt'):
                            v = pt.find(f'{{{NS_C}}}v')
                            if v is not None and v.text:
                                actual_vals.append(float(v.text.strip()))

                print(f"  Categories found: {actual_cats}")
                print(f"  Values found: {actual_vals}")

                comp3_score = 0.0

                # Check categories (0.15)
                if actual_cats == EXPECTED_CATEGORIES:
                    print("  PASS: Categories match exactly")
                    comp3_score += 0.15
                elif len(actual_cats) == len(EXPECTED_CATEGORIES) and all(
                    a.lower() == e.lower() for a, e in zip(actual_cats, EXPECTED_CATEGORIES)
                ):
                    print("  PASS: Categories match (case-insensitive)")
                    comp3_score += 0.15
                else:
                    print(f"  FAIL: Categories mismatch. Expected {EXPECTED_CATEGORIES}")

                # Check values (0.15)
                if actual_vals == EXPECTED_VALUES:
                    print("  PASS: Values match exactly")
                    comp3_score += 0.15
                elif len(actual_vals) == len(EXPECTED_VALUES) and all(
                    abs(a - e) < 0.5 for a, e in zip(actual_vals, EXPECTED_VALUES)
                ):
                    print("  PASS: Values match (within tolerance)")
                    comp3_score += 0.15
                else:
                    print(f"  FAIL: Values mismatch. Expected {EXPECTED_VALUES}")

                if comp3_score > 0:
                    print(f"PASS: Component 3 — Data verification ({comp3_score} pts)")
                    total_score += comp3_score
                else:
                    print("FAIL: Component 3 — Both categories and values incorrect")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Percentage data labels shown (0.15 points)
    try:
        pie3d = chart_root.find(f'.//{{{NS_C}}}pie3DChart')
        chart_elem = pie3d if pie3d is not None else chart_root.find(f'.//{{{NS_C}}}pieChart')

        if chart_elem is not None:
            # Check dLbls (data labels) element
            dlbls = chart_elem.find(f'{{{NS_C}}}dLbls')
            if dlbls is None:
                # Also check at series level
                ser = chart_elem.find(f'{{{NS_C}}}ser')
                if ser is not None:
                    dlbls = ser.find(f'{{{NS_C}}}dLbls')

            if dlbls is not None:
                show_pct = dlbls.find(f'{{{NS_C}}}showPercent')
                if show_pct is not None and show_pct.get('val') == '1':
                    print("PASS: Component 4 — Percentage data labels enabled (0.15 pts)")
                    total_score += 0.15
                else:
                    pct_val = show_pct.get('val') if show_pct is not None else 'not found'
                    print(f"FAIL: Component 4 — showPercent is '{pct_val}', expected '1'")
            else:
                print("FAIL: Component 4 — No data labels element found")
        else:
            print("FAIL: Component 4 — No pie chart element found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Legend present (0.15 points)
    try:
        chart_node = chart_root.find(f'{{{NS_C}}}chart')
        if chart_node is not None:
            legend = chart_node.find(f'{{{NS_C}}}legend')
            if legend is not None:
                print("PASS: Component 5 — Legend is present (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 5 — No legend found in chart")
        else:
            print("FAIL: Component 5 — Cannot find chart node")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
