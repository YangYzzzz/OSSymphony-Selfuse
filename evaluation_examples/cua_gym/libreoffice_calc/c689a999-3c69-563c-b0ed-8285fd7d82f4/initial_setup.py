"""
Initial Setup: Survey Results ODS Dataset
Task ID: osworld_multi_apps_code_script_output_010
Domain: multi_apps (libreoffice_calc + terminal + vscode)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_010'
DATA_DIR = f'{WORKDIR}/data'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
DESKTOP_DIR = f'{WORKDIR}/Desktop'
ODS_OUTPUT = f'{DATA_DIR}/survey_results.ods'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    import random

    random.seed(42)

    # Create necessary directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DESKTOP_DIR, exist_ok=True)
    # Note: scripts/ directory intentionally NOT created — agent must create it

    # Build ODS file using Python odfpy
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties
    from odf.text import P
    from odf.table import Table, TableColumn, TableRow, TableCell

    doc = OpenDocumentSpreadsheet()

    # Define a style for headers
    header_style = Style(name="ColumnHeader", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(header_style)

    table = Table(name="Survey Results")

    # Define columns
    for _ in range(10):  # respondent_id, age, department, Q1-Q8 = 11 cols
        table.addElement(TableColumn())

    # --- Header row ---
    header_row = TableRow()
    headers = ["respondent_id", "age", "department", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
    for h in headers:
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=str(h)))
        header_row.addElement(cell)
    table.addElement(header_row)

    # --- Data rows: 50 respondents, some rows with missing values ---
    departments = [
        "Engineering", "Marketing", "Sales", "HR", "Finance",
        "Operations", "Research", "Legal", "Product", "Design"
    ]

    # Pre-define which rows have missing values (10% of rows have one missing score)
    missing_rows = {5: "Q3", 12: "Q7", 18: "Q1", 25: "Q5", 31: "Q2",
                    37: "Q8", 42: "Q4", 46: "Q6", 49: "Q3", 50: "Q7"}

    for i in range(1, 51):
        row = TableRow()

        # respondent_id
        cell_id = TableCell(valuetype="float", value=str(i))
        cell_id.addElement(P(text=str(i)))
        row.addElement(cell_id)

        # age (22-65)
        age = random.randint(22, 65)
        cell_age = TableCell(valuetype="float", value=str(age))
        cell_age.addElement(P(text=str(age)))
        row.addElement(cell_age)

        # department
        dept = departments[(i - 1) % len(departments)]
        cell_dept = TableCell(valuetype="string")
        cell_dept.addElement(P(text=dept))
        row.addElement(cell_dept)

        # Q1-Q8 Likert scale (1-5), with some missing
        question_cols = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
        for q in question_cols:
            if i in missing_rows and missing_rows[i] == q:
                # Missing value — empty cell
                cell_q = TableCell()
                row.addElement(cell_q)
            else:
                # Score 1-5, with bias toward different ranges per question
                q_num = int(q[1])
                if q_num in [2, 6]:  # Questions that tend to score below 3
                    score = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 25, 15, 10])[0]
                elif q_num in [1, 4, 8]:  # Questions that score well above 3
                    score = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
                else:
                    score = random.randint(1, 5)

                cell_q = TableCell(valuetype="float", value=str(score))
                cell_q.addElement(P(text=str(score)))
                row.addElement(cell_q)

        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(ODS_OUTPUT)
    print(f'Initial ODS file created: {ODS_OUTPUT}')

    # Verify file was created
    assert os.path.isfile(ODS_OUTPUT), f"ODS file not found at {ODS_OUTPUT}"
    print(f'File size: {os.path.getsize(ODS_OUTPUT)} bytes')

    # Open LibreOffice Calc with the ODS file for GUI context
    launch_gui(f'libreoffice --calc "{ODS_OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Calc with survey_results.ods on DISPLAY=:0')


create_initial()
