"""
Reward Script: Grade Analyzer - Python script completion + grade report + spreadsheet entry
Task ID: osworld_multi_apps_code_script_output_005
Domain: libreoffice_calc (multi-app: python script, text file, ods spreadsheet)

Scoring Rubric:
  Component 1: grade_report.txt exists and contains class average "78.77"     (0.35 pts)
  Component 2: grade_report.txt contains correct top students and failing list  (0.30 pts)
  Component 3: grades_summary.ods cell C1 contains the float class average 78.77 (0.35 pts)
  Total: 1.0

Ground truth from task context:
  - class average = 78.77 (rounded to 2 decimal places)
  - grade_report.txt must be created with the printed summary
  - Cell C1 of grades_summary.ods must contain the float 78.77
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_005'

REPORT_PATH = f'{WORKDIR}/data/grade_report.txt'
ODS_PATH = f'{WORKDIR}/data/grades_summary.ods'
CLASS_AVG = 78.77
AVG_TOLERANCE = 0.01


def read_ods_cell_c1(ods_path):
    """
    Read cell C1 (row 0, col 2) from grades_summary.ods using zipfile + XML parsing.
    ODS files are ZIP archives containing content.xml.
    Returns (value_type, value_str) or (None, None) on error.
    """
    try:
        with zipfile.ZipFile(ods_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')

        # Parse XML
        # Register namespaces to handle prefixed tags
        ns = {
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        }

        root = ET.fromstring(content_xml)

        # Navigate: document-content > body > spreadsheet > table > table-row[0] > table-cell[2]
        spreadsheet = root.find('.//office:spreadsheet', ns)
        if spreadsheet is None:
            return None, None

        # Find first table
        table = spreadsheet.find('table:table', ns)
        if table is None:
            return None, None

        rows = table.findall('table:table-row', ns)
        if not rows:
            return None, None

        # Row 0 = first row (row index 0 = spreadsheet row 1)
        first_row = rows[0]
        cells = first_row.findall('table:table-cell', ns)

        # C1 = column index 2 (0-based)
        if len(cells) < 3:
            return None, None

        cell_c1 = cells[2]
        val_type = cell_c1.get(
            '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value-type'
        )
        val_str = cell_c1.get(
            '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value'
        )
        # Also try to get the text content
        text_elem = cell_c1.find('text:p', ns)
        text_val = text_elem.text if text_elem is not None else None

        return val_type, val_str, text_val
    except Exception as e:
        print(f"ERROR reading ODS: {e}")
        return None, None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: grade_report.txt exists and contains class average (0.35 pts)
    # This FAILS on initial_env (file doesn't exist) → PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(REPORT_PATH):
            print(f"FAIL: Component 1 — grade_report.txt not found at {REPORT_PATH}")
        else:
            with open(REPORT_PATH, 'r') as f:
                report_content = f.read()

            # Check class average line exists with correct value
            if f"Class Average: {CLASS_AVG}" in report_content:
                print(f"PASS: Component 1 — grade_report.txt exists and contains 'Class Average: {CLASS_AVG}' (0.35 pts)")
                total_score += 0.35
            else:
                # Try to find any class average value to give partial feedback
                import re
                match = re.search(r'Class Average:\s*([\d.]+)', report_content)
                if match:
                    found_val = float(match.group(1))
                    print(f"FAIL: Component 1 — grade_report.txt exists but class average is {found_val}, expected {CLASS_AVG}")
                else:
                    print(f"FAIL: Component 1 — grade_report.txt exists but 'Class Average:' line not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2a: grade_report.txt contains correct top students (0.15 pts)
    # Checks for Grace Lee as the top student (highest avg 94.33)
    # This FAILS on initial_env (file doesn't exist) → PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(REPORT_PATH):
            print(f"FAIL: Component 2a — grade_report.txt not found, cannot check top students")
        else:
            with open(REPORT_PATH, 'r') as f:
                report_content_2a = f.read()
            if "Grace Lee" in report_content_2a and "Top 3 Students:" in report_content_2a:
                print(f"PASS: Component 2a — Top students section found with Grace Lee (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2a — Top students section missing or Grace Lee not found")
    except Exception as e:
        print(f"ERROR: Component 2a — {e}")

    # -----------------------------------------------------------------------
    # Component 2b: grade_report.txt contains correct failing students (0.15 pts)
    # Checks for Frank Wilson as the failing student (avg < 60)
    # This FAILS on initial_env (file doesn't exist) → PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(REPORT_PATH):
            print(f"FAIL: Component 2b — grade_report.txt not found, cannot check failing students")
        else:
            with open(REPORT_PATH, 'r') as f:
                report_content_2b = f.read()
            if "Frank Wilson" in report_content_2b and "Failing Students" in report_content_2b:
                print(f"PASS: Component 2b — Failing students section found with Frank Wilson (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2b — Failing students section missing or Frank Wilson not found")
    except Exception as e:
        print(f"ERROR: Component 2b — {e}")

    # -----------------------------------------------------------------------
    # Component 3: grades_summary.ods cell C1 contains float 78.77 (0.35 pts)
    # Initially C1 is a string "Class Average" header; after task it should be float 78.77
    # This FAILS on initial_env (C1 is string) → PASSES on golden_env (C1 is float 78.77)
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(ODS_PATH):
            print(f"FAIL: Component 3 — grades_summary.ods not found at {ODS_PATH}")
        else:
            result = read_ods_cell_c1(ODS_PATH)
            if result[0] is None and result[1] is None:
                print(f"FAIL: Component 3 — Could not read C1 from grades_summary.ods")
            else:
                val_type, val_str, text_val = result
                print(f"DEBUG: C1 value-type={val_type}, value={val_str}, text={text_val}")

                if val_type == 'float' and val_str is not None:
                    try:
                        c1_float = float(val_str)
                        if abs(c1_float - CLASS_AVG) <= AVG_TOLERANCE:
                            print(f"PASS: Component 3 — C1 is float {c1_float} ≈ {CLASS_AVG} (0.35 pts)")
                            total_score += 0.35
                        else:
                            print(f"FAIL: Component 3 — C1 is float {c1_float} but expected {CLASS_AVG}")
                    except ValueError:
                        print(f"FAIL: Component 3 — C1 value '{val_str}' cannot be parsed as float")
                elif val_type == 'string':
                    # Check if the text content is the numeric value as a string
                    if text_val is not None:
                        try:
                            c1_float = float(text_val)
                            if abs(c1_float - CLASS_AVG) <= AVG_TOLERANCE:
                                print(f"PASS: Component 3 — C1 text is '{text_val}' ≈ {CLASS_AVG} (0.35 pts)")
                                total_score += 0.35
                            else:
                                print(f"FAIL: Component 3 — C1 is string type with text '{text_val}', expected float {CLASS_AVG}")
                        except (ValueError, TypeError):
                            print(f"FAIL: Component 3 — C1 is string type with text '{text_val}', expected float {CLASS_AVG}")
                    else:
                        print(f"FAIL: Component 3 — C1 is string type (not a float)")
                else:
                    print(f"FAIL: Component 3 — C1 has unexpected type '{val_type}' with value '{val_str}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
