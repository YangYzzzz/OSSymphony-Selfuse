"""
Reward Script: Insert horizontal bar chart in Sales_Report.docx
Task ID: writer_pd_037
Domain: libreoffice_writer
Scoring:
  Component 1: Chart object exists in document (0.20)
  Component 2: Chart is horizontal bar type (0.20)
  Component 3: Chart title is 'H1 2026 Sales Performance' (0.20)
  Component 4: Chart has 6 categories (Jan-Jun) (0.15)
  Component 5: Blue color scheme on bars (0.10)
  Component 6: Data labels showing values enabled (0.15)
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_037'


def persist_app_state(domain: str):
    """Save any unsaved edits in LibreOffice before verification."""
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

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read chart XML from the docx zip
    chart_xml = None
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            chart_files = [f for f in z.namelist() if re.match(r'word/charts/chart\d+\.xml', f)]
            if chart_files:
                chart_xml = z.read(chart_files[0]).decode('utf-8', errors='replace')
                print(f"INFO: Found chart file: {chart_files[0]}")
            else:
                print(f"INFO: No chart files found in docx. Files: {[f for f in z.namelist() if 'chart' in f.lower()]}")
    except Exception as e:
        print(f"CRITICAL: Cannot read docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Also check for chart relationship via python-docx
    has_chart_rel = False
    try:
        from docx import Document
        doc = Document(file_path)
        for rel in doc.part.rels.values():
            if 'chart' in str(rel.reltype).lower():
                has_chart_rel = True
                break
    except Exception as e:
        print(f"WARN: Could not check rels via python-docx: {e}")

    # Component 1: Chart object exists in document (0.20 points)
    try:
        if chart_xml is not None or has_chart_rel:
            print(f"PASS: Component 1 — Chart object exists in document (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No chart object found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no chart XML, remaining components cannot pass
    if chart_xml is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Chart is horizontal bar type (0.20 points)
    # A horizontal bar chart in OOXML uses <c:barChart> with <c:barDir val="bar"/>
    # (vertical/column uses val="col")
    try:
        has_bar_chart = '<c:barChart>' in chart_xml or '<c:barChart ' in chart_xml
        bar_dir_match = re.search(r'<c:barDir\s+val="(\w+)"', chart_xml)
        bar_dir = bar_dir_match.group(1) if bar_dir_match else None

        if has_bar_chart and bar_dir == 'bar':
            print(f"PASS: Component 2 — Chart is horizontal bar type (barDir=bar) (0.20 pts)")
            total_score += 0.20
        elif has_bar_chart and bar_dir == 'col':
            print(f"FAIL: Component 2 — Chart is column (vertical bar), not horizontal bar. barDir={bar_dir}")
        elif has_bar_chart:
            print(f"FAIL: Component 2 — barChart found but barDir={bar_dir}, expected 'bar'")
        else:
            print(f"FAIL: Component 2 — No barChart element found in chart XML")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart title is 'H1 2026 Sales Performance' (0.20 points)
    try:
        # Extract title text from <c:title>...<a:t>TITLE</a:t>...</c:title>
        title_section = re.search(r'<c:title>(.*?)</c:title>', chart_xml, re.DOTALL)
        if title_section:
            title_text_matches = re.findall(r'<a:t>(.*?)</a:t>', title_section.group(1))
            title_text = ''.join(title_text_matches).strip()
            expected_title = 'H1 2026 Sales Performance'
            if title_text == expected_title:
                print(f"PASS: Component 3 — Chart title is '{title_text}' (0.20 pts)")
                total_score += 0.20
            elif title_text.lower() == expected_title.lower():
                # Close enough — case difference only
                print(f"PASS: Component 3 — Chart title is '{title_text}' (case-insensitive match) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Chart title is '{title_text}', expected '{expected_title}'")
        else:
            # Check if autoTitleDeleted
            auto_del = re.search(r'<c:autoTitleDeleted\s+val="(\d)"', chart_xml)
            print(f"FAIL: Component 3 — No chart title element found (autoTitleDeleted={auto_del.group(1) if auto_del else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chart has 6 categories for Jan-Jun (0.15 points)
    try:
        # Look for category count in strCache
        cat_section = re.search(r'<c:cat>(.*?)</c:cat>', chart_xml, re.DOTALL)
        if cat_section:
            cat_content = cat_section.group(1)
            pt_count_match = re.search(r'<c:ptCount\s+val="(\d+)"', cat_content)
            cat_values = re.findall(r'<c:v>(.*?)</c:v>', cat_content)
            pt_count = int(pt_count_match.group(1)) if pt_count_match else len(cat_values)

            expected_months = ['January', 'February', 'March', 'April', 'May', 'June']
            if pt_count == 6 and len(cat_values) >= 6:
                # Check that months are present (any order is fine, but should include Jan-Jun)
                months_found = [v.strip() for v in cat_values[:6]]
                if all(m in months_found for m in expected_months):
                    print(f"PASS: Component 4 — 6 categories found: {months_found} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — 6 categories but values are {months_found}, expected {expected_months}")
            else:
                print(f"FAIL: Component 4 — Expected 6 categories, found ptCount={pt_count}, values={cat_values}")
        else:
            print(f"FAIL: Component 4 — No <c:cat> element found in chart")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Blue color scheme on bars (0.10 points)
    # Check for a solidFill with a blue-ish srgbClr in the series spPr
    try:
        # Find fill color in series shape properties
        ser_section = re.search(r'<c:ser>(.*?)</c:ser>', chart_xml, re.DOTALL)
        if ser_section:
            ser_content = ser_section.group(1)
            color_match = re.search(r'<a:srgbClr\s+val="([A-Fa-f0-9]{6})"', ser_content)
            if color_match:
                color_hex = color_match.group(1).upper()
                r_val = int(color_hex[0:2], 16)
                g_val = int(color_hex[2:4], 16)
                b_val = int(color_hex[4:6], 16)
                # Blue means blue channel is dominant (significantly higher than red and green)
                is_blue = b_val > r_val and b_val > g_val and b_val >= 100
                if is_blue:
                    print(f"PASS: Component 5 — Blue color scheme: #{color_hex} (R={r_val},G={g_val},B={b_val}) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — Bar color #{color_hex} (R={r_val},G={g_val},B={b_val}) is not blue")
            else:
                # Check for theme color references that might be blue
                theme_match = re.search(r'<a:schemeClr\s+val="(\w+)"', ser_content)
                if theme_match:
                    scheme = theme_match.group(1)
                    # Common blue schemes: accent1, dk2
                    if scheme in ('accent1', 'dk2', 'accent5'):
                        print(f"PASS: Component 5 — Blue scheme color: {scheme} (0.10 pts)")
                        total_score += 0.10
                    else:
                        print(f"FAIL: Component 5 — Scheme color '{scheme}' may not be blue")
                else:
                    print(f"FAIL: Component 5 — No fill color found in series")
        else:
            print(f"FAIL: Component 5 — No series element found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Data labels showing values enabled (0.15 points)
    try:
        # Look for <c:dLbls> with <c:showVal val="1"/>
        dlbls_section = re.search(r'<c:dLbls>(.*?)</c:dLbls>', chart_xml, re.DOTALL)
        if dlbls_section:
            dlbls_content = dlbls_section.group(1)
            show_val_match = re.search(r'<c:showVal\s+val="(\d)"', dlbls_content)
            if show_val_match and show_val_match.group(1) == '1':
                print(f"PASS: Component 6 — Data labels showing values enabled (showVal=1) (0.15 pts)")
                total_score += 0.15
            elif show_val_match:
                print(f"FAIL: Component 6 — showVal={show_val_match.group(1)}, expected 1")
            else:
                print(f"FAIL: Component 6 — No showVal attribute found in dLbls")
        else:
            print(f"FAIL: Component 6 — No <c:dLbls> element found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
