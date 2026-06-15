"""
Reward Script: Reformat JSON org chart to structured Writer report
Task ID: osworld_multi_apps_json_reformat_writer_009
Domain: libreoffice_writer
Scoring:
  Component 1: 4 bold department headings (Engineering, Marketing, Sales, HR) — 0.25 pts
  Component 2: 4 manager mini-tables (2 cols: name, title) — 0.30 pts
  Component 3: Employee listing per department (at least one employee per dept) — 0.20 pts
  Component 4: Summary table (3 cols, 4 data rows: dept, manager, count) — 0.25 pts
  Total: 1.0
"""

import os

# Use odf library to load .odt files
from odf.opendocument import load
from odf.text import P, H, List, ListItem
from odf.table import Table, TableRow, TableCell

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_009'
FILE_PATH = '/home/user/Documents/org_structure.odt'

EXPECTED_DEPARTMENTS = ['Engineering', 'Marketing', 'Sales', 'HR']
EXPECTED_MANAGERS = {
    'Engineering': ('Diana Foster', 'VP of Engineering'),
    'Marketing': ('Samuel Okonkwo', 'Head of Marketing'),
    'Sales': ('Rachel Kim', 'Director of Sales'),
    'HR': ('Karen Walsh', 'HR Manager'),
}
EXPECTED_EMPLOYEE_COUNTS = {
    'Engineering': 5,
    'Marketing': 3,
    'Sales': 4,
    'HR': 6,
}


def get_para_text(para):
    """Extract plain text from an ODT paragraph element."""
    parts = []
    for node in para.childNodes:
        if node.nodeType == node.TEXT_NODE:
            parts.append(node.data)
        elif node.qname and node.qname[1] == 'span':
            # Text within a span element
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    parts.append(child.data)
    return ''.join(parts).strip()


def get_cell_text(cell):
    """Extract plain text from a table cell."""
    parts = []
    for cp in cell.getElementsByType(P):
        parts.append(get_para_text(cp))
    return '\n'.join(p for p in parts if p).strip()


def verify_task(file_path):
    """
    Verify task completion: JSON org chart reformatted to structured Writer report.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition: Load the ODT document
    try:
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Pre-condition: File should no longer be raw JSON (check initial state detection)
    paras = doc.getElementsByType(P)
    para_texts = [get_para_text(p) for p in paras]
    para_styles = [p.getAttribute('stylename') or '' for p in paras]

    if any(t.strip() == '{' for t in para_texts) and not any(s == 'DeptHeading' for s in para_styles):
        print("FAIL: File appears to still contain raw JSON content — not reformatted")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 4 bold department headings (0.25 points)
    # Task requires: bold department headings for Engineering, Marketing, Sales, HR
    # In golden file: paragraphs with style 'DeptHeading' (which has font-weight: bold)
    # Also accept headings by content match regardless of exact style name,
    # but require them to appear as visually distinct (non-normal) styled paragraphs
    try:
        # Find department heading paragraphs — look for DeptHeading style or H-type headings
        dept_heading_paras = []
        for p, style in zip(paras, para_styles):
            txt = get_para_text(p)
            if txt in EXPECTED_DEPARTMENTS:
                # Check if it has a bold/heading style (DeptHeading, Heading*, or has bold attribute)
                if 'heading' in style.lower() or 'dept' in style.lower() or style.startswith('H'):
                    dept_heading_paras.append(txt)
                else:
                    # Even if style name doesn't match, check if the paragraph is bold via auto-styles
                    # by checking if it uses a bold-marked auto-style
                    bold_styles = set()
                    for auto_style in doc.automaticstyles.childNodes:
                        try:
                            sname = auto_style.getAttribute('name')
                            sfamily = auto_style.getAttribute('family')
                            for child in auto_style.childNodes:
                                try:
                                    fw = child.getAttribute('fontweight')
                                    if fw == 'bold':
                                        bold_styles.add(sname)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                    if style in bold_styles:
                        dept_heading_paras.append(txt)

        found_depts = set(dept_heading_paras)
        missing_depts = [d for d in EXPECTED_DEPARTMENTS if d not in found_depts]

        if len(found_depts) >= 4 and not missing_depts:
            print(f"PASS: Component 1 — All 4 bold department headings found: {sorted(found_depts)} (0.25 pts)")
            total_score += 0.25
        elif len(found_depts) >= 2:
            print(f"PARTIAL: Component 1 — Only {len(found_depts)}/4 dept headings found: {sorted(found_depts)} (partial 0.10 pts)")
            print(f"  Missing: {missing_depts}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected 4 bold dept headings, found {len(found_depts)}: {sorted(found_depts)}")
            print(f"  Missing: {missing_depts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 4 manager mini-tables (2-column: Manager Name | Title) (0.30 points)
    # Each department should have a mini-table with manager's name and title
    try:
        tables = doc.getElementsByType(Table)
        # Filter to 2-column tables (manager tables) vs 3-column (summary table)
        manager_tables = []
        summary_tables = []
        for table in tables:
            rows = table.getElementsByType(TableRow)
            if rows:
                cells = rows[0].getElementsByType(TableCell)
                col_count = len(cells)
                if col_count == 2:
                    manager_tables.append(table)
                elif col_count == 3:
                    summary_tables.append(table)

        # Verify each manager table contains manager name + title
        manager_table_score = 0.0
        verified_managers = []
        for dept, (mgr_name, mgr_title) in EXPECTED_MANAGERS.items():
            for table in manager_tables:
                rows = table.getElementsByType(TableRow)
                all_cell_texts = []
                for row in rows:
                    cells = row.getElementsByType(TableCell)
                    for cell in cells:
                        ct = get_cell_text(cell)
                        if ct:
                            all_cell_texts.append(ct)
                if mgr_name in all_cell_texts or any(mgr_name in ct for ct in all_cell_texts):
                    if mgr_title in all_cell_texts or any(mgr_title in ct for ct in all_cell_texts):
                        verified_managers.append(dept)
                        break

        if len(verified_managers) >= 4:
            print(f"PASS: Component 2 — All 4 manager tables verified: {verified_managers} (0.30 pts)")
            total_score += 0.30
        elif len(verified_managers) >= 2:
            print(f"PARTIAL: Component 2 — {len(verified_managers)}/4 manager tables verified: {verified_managers} (partial 0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 4 manager tables, verified {len(verified_managers)}: {verified_managers}")
            print(f"  Found {len(manager_tables)} 2-column tables total")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Employee listing per department (0.20 points)
    # Each department section should be followed by a list of employees
    # We check that key employee names appear in the document text
    try:
        all_para_text = '\n'.join(para_texts)

        # Key employees per department (checking a representative sample)
        sample_employees = [
            'Alex Rivera',       # Engineering
            'Samuel Okonkwo',    # Marketing manager - also serves as check
            'Chloe Bennett',     # Marketing employee
            'Marco Delgado',     # Sales employee
            'Ben Nakamura',      # HR employee
        ]
        found_employees = [e for e in sample_employees if e in all_para_text]

        # Also check if "Employees:" label appears at least once (indicating structured listing)
        has_employees_label = any('Employees' in t or 'employees' in t for t in para_texts)

        if len(found_employees) >= 4 and has_employees_label:
            print(f"PASS: Component 3 — Employee listings present ({len(found_employees)}/5 sample employees found, 'Employees:' label present) (0.20 pts)")
            total_score += 0.20
        elif len(found_employees) >= 2:
            print(f"PARTIAL: Component 3 — {len(found_employees)}/5 sample employees found (partial 0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Too few employees found ({len(found_employees)}/5 checked)")
            print(f"  Found: {found_employees}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Summary table (3 columns: Department | Manager | Employee Count) (0.25 points)
    # The last table should be a 3-column summary with 4 data rows
    try:
        tables = doc.getElementsByType(Table)

        # Find 3-column tables
        three_col_tables = []
        for table in tables:
            rows = table.getElementsByType(TableRow)
            if rows:
                cells = rows[0].getElementsByType(TableCell)
                if len(cells) == 3:
                    three_col_tables.append(table)

        summary_verified = False
        if three_col_tables:
            # Check the last 3-col table for dept/manager/count data
            summary_table = three_col_tables[-1]
            rows = summary_table.getElementsByType(TableRow)
            # Collect all cell text
            all_summary_cells = []
            for row in rows:
                cells = row.getElementsByType(TableCell)
                row_data = [get_cell_text(c) for c in cells]
                all_summary_cells.append(row_data)

            # Verify 4 departments with correct counts
            found_count_data = {}
            for row in all_summary_cells:
                if len(row) >= 3:
                    dept_cell = row[0].strip()
                    count_cell = row[2].strip()
                    if dept_cell in EXPECTED_EMPLOYEE_COUNTS:
                        try:
                            count_val = int(count_cell)
                            found_count_data[dept_cell] = count_val
                        except (ValueError, TypeError):
                            pass

            correct_counts = {
                dept: count
                for dept, count in found_count_data.items()
                if EXPECTED_EMPLOYEE_COUNTS.get(dept) == count
            }

            total_rows_in_table = len(rows)

            if len(correct_counts) >= 4:
                print(f"PASS: Component 4 — Summary table verified: {correct_counts} (0.25 pts)")
                total_score += 0.25
            elif len(correct_counts) >= 2:
                partial = 0.12
                print(f"PARTIAL: Component 4 — Summary table has {len(correct_counts)}/4 correct rows: {correct_counts} (partial {partial} pts)")
                total_score += partial
            else:
                # Check if table exists with 4+ data rows at least (structure check)
                if total_rows_in_table >= 4:
                    print(f"PARTIAL: Component 4 — Summary table exists with {total_rows_in_table} rows but counts unverified (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 4 — Summary table verification failed. Data found: {found_count_data}")
                    print(f"  Expected: {EXPECTED_EMPLOYEE_COUNTS}")
        else:
            print("FAIL: Component 4 — No 3-column summary table found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
