"""
Reward Script: Reformat academic JSON records into LibreOffice Writer report
Task ID: osworld_multi_apps_json_reformat_writer_012
Domain: libreoffice_writer
Scoring:
  Component 1: Raw JSON deleted from document (0.2 pts)
  Component 2: Document has tables (personal info + course tables, at least 10) (0.2 pts)
  Component 3: Course grade tables contain GPA rows (0.3 pts)
  Component 4: Final comparison table with 5 student rows (GPA, credits, highest course) (0.3 pts)
"""

import os
import re

FILE_PATH = '/home/user/Documents/academic_records.odt'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_012'


def get_all_text_nodes(elem):
    """Recursively collect all TEXT node data from an element."""
    results = []
    if elem.nodeType == elem.TEXT_NODE:
        results.append(elem.data)
    else:
        for child in elem.childNodes:
            results.extend(get_all_text_nodes(child))
    return results


def get_cell_text(cell):
    """Get concatenated text from a table cell."""
    texts = get_all_text_nodes(cell)
    return ' '.join(t for t in texts if t.strip()).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import P
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all paragraph texts from the document
    all_para_texts = []
    for para in doc.getElementsByType(P):
        texts = get_all_text_nodes(para)
        combined = ' '.join(texts).strip()
        if combined:
            all_para_texts.append(combined)

    full_doc_text = '\n'.join(all_para_texts)

    # Gather all tables
    tables = doc.getElementsByType(Table)
    num_tables = len(tables)

    # Component 1: Raw JSON deleted (no student_id JSON patterns remain)
    # Initial state has lines like: "student_id": "STU-2024-001" as plain text paragraphs
    # Golden state replaces those with structured tables
    try:
        json_patterns = [
            r'"student_id"',
            r'"name":',
            r'"major":',
            r'"courses":\s*\[',
            r'"grade":',
            r'"credits":',
        ]
        json_found = any(re.search(pat, full_doc_text) for pat in json_patterns)

        if not json_found:
            print(f"PASS: Component 1 — Raw JSON content deleted from document (0.2 pts)")
            total_score += 0.2
        else:
            # Find which pattern matched
            matched = [p for p in json_patterns if re.search(p, full_doc_text)]
            print(f"FAIL: Component 1 — Raw JSON still present in document. Patterns found: {matched}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tables present (at least 10 tables: 5 personal info + 5 course tables)
    # Task requires 1 personal info table + 1 course table per student = 10 min, plus final = 11
    try:
        if num_tables >= 10:
            print(f"PASS: Component 2 — Document has {num_tables} tables (expected >= 10) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected at least 10 tables, found {num_tables}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: GPA rows in course grade tables
    # Each course grade table should have a last row with GPA and Total Credits info
    # Expected GPA values from ground truth:
    #   Emily Hartman: 3.29, Marcus Okonkwo: 3.20, Sofia Reyes: 3.67
    #   James Thornton: 2.79, Aisha Nakamura: 3.60
    expected_gpas = ['3.29', '3.20', '3.67', '2.79', '3.60']
    try:
        gpa_rows_found = 0
        gpa_detail = []

        for table in tables:
            rows = table.getElementsByType(TableRow)
            if not rows:
                continue
            # Check the last row for GPA content
            last_row = rows[-1]
            cells = last_row.getElementsByType(TableCell)
            if not cells:
                continue
            first_cell_text = get_cell_text(cells[0])
            # Look for "GPA:" pattern in first cell
            if re.search(r'GPA\s*:', first_cell_text, re.IGNORECASE):
                gpa_rows_found += 1
                gpa_detail.append(first_cell_text)

        if gpa_rows_found >= 5:
            print(f"PASS: Component 3 — Found {gpa_rows_found} GPA rows in course tables: {gpa_detail} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected 5 GPA rows, found {gpa_rows_found}. Details: {gpa_detail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Final comparison table with 5 student rows
    # Table 11 (index 10) should have: header + 5 rows with student name, GPA, total credits, highest-grade course
    # Expected data from ground truth:
    #   Emily Hartman | 3.29 | 17 | Data Structures
    #   Marcus Okonkwo | 3.20 | 20 | Circuit Analysis
    #   Sofia Reyes | 3.67 | 18 | Organic Chemistry I
    #   James Thornton | 2.79 | 19 | International Trade
    #   Aisha Nakamura | 3.60 | 15 | Research Methods
    expected_comparison_rows = {
        'Emily Hartman': ('3.29', '17', 'Data Structures'),
        'Marcus Okonkwo': ('3.20', '20', 'Circuit Analysis'),
        'Sofia Reyes': ('3.67', '18', 'Organic Chemistry I'),
        'James Thornton': ('2.79', '19', 'International Trade'),
        'Aisha Nakamura': ('3.60', '15', 'Research Methods'),
    }
    try:
        # The comparison table should be the last table or have specific header columns
        comparison_table = None
        for table in tables:
            rows = table.getElementsByType(TableRow)
            if not rows:
                continue
            # Check the header row for "Student Name" and "GPA" columns
            header_cells = rows[0].getElementsByType(TableCell)
            header_texts = [get_cell_text(c) for c in header_cells]
            # Look for a table with "GPA" in header and at least 4 columns
            if len(header_texts) >= 4 and any('GPA' in t for t in header_texts):
                comparison_table = table
                break  # Use first match if multiple

        if comparison_table is None:
            # Try looking for 11th table (last table)
            if num_tables >= 11:
                comparison_table = tables[10]
            elif num_tables >= 1:
                comparison_table = tables[-1]

        if comparison_table is None:
            print(f"FAIL: Component 4 — No comparison table found in document")
        else:
            rows = comparison_table.getElementsByType(TableRow)
            # Find how many student rows match expected data
            matched_students = 0
            row_details = []

            for row in rows:
                cells = row.getElementsByType(TableCell)
                if len(cells) < 4:
                    continue
                cell_texts = [get_cell_text(cells[i]) for i in range(min(4, len(cells)))]
                student_name = cell_texts[0]
                if student_name in expected_comparison_rows:
                    exp_gpa, exp_credits, exp_course = expected_comparison_rows[student_name]
                    # Check GPA matches (allow some tolerance)
                    gpa_ok = exp_gpa in cell_texts[1] if len(cell_texts) > 1 else False
                    credits_ok = exp_credits in cell_texts[2] if len(cell_texts) > 2 else False
                    course_ok = exp_course.lower() in cell_texts[3].lower() if len(cell_texts) > 3 else False
                    if gpa_ok and credits_ok and course_ok:
                        matched_students += 1
                        row_details.append(f"{student_name}: OK")
                    else:
                        row_details.append(f"{student_name}: partial (gpa={gpa_ok}, credits={credits_ok}, course={course_ok}); got {cell_texts}")

            if matched_students == 5:
                print(f"PASS: Component 4 — Final comparison table has all 5 correct student rows: {row_details} (0.3 pts)")
                total_score += 0.3
            elif matched_students >= 3:
                partial = matched_students / 5 * 0.3
                print(f"PARTIAL: Component 4 — {matched_students}/5 student rows correct, awarding {partial:.2f} pts. Details: {row_details}")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Expected 5 correct comparison rows, found {matched_students}. Details: {row_details}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
