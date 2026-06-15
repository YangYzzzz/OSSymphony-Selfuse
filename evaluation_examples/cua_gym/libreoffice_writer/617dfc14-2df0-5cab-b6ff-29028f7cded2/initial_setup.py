"""
Initial Setup: Create experiment_results.ods with 3 sheets of experiment data on Desktop
Task ID: osworld_multi_apps_doc_calc_to_writer_012
Domain: libreoffice_writer (multi-app: calc source + writer target)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_012'
ODS_FILE = f'{DESKTOP}/experiment_results.ods'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)
    # Ensure Documents directory exists (agent will save there)
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    # Use pyexcel-ods3 or openpyxl - but for ODS we use odfpy
    # Use subprocess to create via python with odfpy
    # Build ODS content using odfpy
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TextProperties, TableCellProperties
    from odf.namespaces import OFFICENS

    doc = OpenDocumentSpreadsheet()

    def make_text_cell(value):
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=str(value)))
        return cell

    def make_float_cell(value):
        cell = TableCell(valuetype="float", value=str(value))
        cell.addElement(P(text=str(value)))
        return cell

    def make_string_cell(value):
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=str(value)))
        return cell

    # --- Treatment A data (20 rows) ---
    treatment_a_data = [
        ('TA-001', 3.42, 128.5, 0.003, '*'),
        ('TA-002', 2.87, 115.2, 0.041, '*'),
        ('TA-003', 4.15, 142.8, 0.001, '*'),
        ('TA-004', 1.95, 98.3,  0.182, ''),
        ('TA-005', 3.76, 133.1, 0.012, '*'),
        ('TA-006', 2.34, 109.7, 0.087, ''),
        ('TA-007', 4.58, 156.4, 0.000, '*'),
        ('TA-008', 3.11, 121.9, 0.028, '*'),
        ('TA-009', 1.72, 94.6,  0.234, ''),
        ('TA-010', 3.95, 138.2, 0.007, '*'),
        ('TA-011', 2.63, 112.5, 0.063, ''),
        ('TA-012', 4.29, 147.3, 0.002, '*'),
        ('TA-013', 3.54, 129.8, 0.019, '*'),
        ('TA-014', 1.88, 96.4,  0.198, ''),
        ('TA-015', 4.07, 140.6, 0.004, '*'),
        ('TA-016', 2.45, 111.3, 0.075, ''),
        ('TA-017', 3.83, 135.7, 0.009, '*'),
        ('TA-018', 4.71, 159.2, 0.000, '*'),
        ('TA-019', 2.98, 118.4, 0.047, '*'),
        ('TA-020', 1.64, 91.7,  0.267, ''),
    ]

    # --- Treatment B data (20 rows) ---
    treatment_b_data = [
        ('TB-001', 2.18, 105.4, 0.058, ''),
        ('TB-002', 3.67, 131.2, 0.015, '*'),
        ('TB-003', 1.43, 87.9,  0.312, ''),
        ('TB-004', 4.02, 139.5, 0.005, '*'),
        ('TB-005', 2.79, 114.8, 0.039, '*'),
        ('TB-006', 3.34, 124.6, 0.023, '*'),
        ('TB-007', 1.91, 97.1,  0.175, ''),
        ('TB-008', 4.48, 153.7, 0.001, '*'),
        ('TB-009', 2.56, 110.3, 0.069, ''),
        ('TB-010', 3.89, 136.9, 0.008, '*'),
        ('TB-011', 1.67, 92.5,  0.241, ''),
        ('TB-012', 4.23, 145.8, 0.002, '*'),
        ('TB-013', 2.95, 117.6, 0.044, '*'),
        ('TB-014', 3.51, 128.4, 0.017, '*'),
        ('TB-015', 1.78, 95.2,  0.208, ''),
        ('TB-016', 4.36, 149.1, 0.003, '*'),
        ('TB-017', 2.41, 108.9, 0.083, ''),
        ('TB-018', 3.74, 133.8, 0.011, '*'),
        ('TB-019', 1.55, 89.4,  0.289, ''),
        ('TB-020', 4.61, 157.3, 0.000, '*'),
    ]

    # --- Control data (10 rows) ---
    control_data = [
        ('CT-001', 1.23, 78.4,  0.543, ''),
        ('CT-002', 1.45, 82.1,  0.489, ''),
        ('CT-003', 1.17, 75.6,  0.612, ''),
        ('CT-004', 1.38, 80.3,  0.521, ''),
        ('CT-005', 1.52, 84.7,  0.467, ''),
        ('CT-006', 1.29, 79.2,  0.558, ''),
        ('CT-007', 1.41, 81.5,  0.502, ''),
        ('CT-008', 1.19, 76.8,  0.594, ''),
        ('CT-009', 1.47, 83.2,  0.478, ''),
        ('CT-010', 1.33, 79.9,  0.534, ''),
    ]

    headers = ['Sample_ID', 'Measurement_1 (mg/mL)', 'Measurement_2 (units)', 'p_value', 'Significant (*p<0.05)']

    def build_sheet(doc, name, data):
        sheet = Table(name=name)
        # Header row
        hrow = TableRow()
        for h in headers:
            hrow.addElement(make_text_cell(h))
        sheet.addElement(hrow)
        # Data rows
        for row_data in data:
            drow = TableRow()
            drow.addElement(make_text_cell(row_data[0]))   # Sample_ID
            drow.addElement(make_float_cell(row_data[1]))  # Measurement_1
            drow.addElement(make_float_cell(row_data[2]))  # Measurement_2
            drow.addElement(make_float_cell(row_data[3]))  # p_value
            drow.addElement(make_text_cell(row_data[4]))   # Significant
            sheet.addElement(drow)
        doc.spreadsheet.addElement(sheet)

    build_sheet(doc, 'Treatment_A', treatment_a_data)
    build_sheet(doc, 'Treatment_B', treatment_b_data)
    build_sheet(doc, 'Control', control_data)

    doc.save(ODS_FILE)
    print(f'Initial ODS file created: {ODS_FILE}')

    # GUI-ready startup: open experiment_results.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{ODS_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with experiment_results.ods on DISPLAY=:0')


create_initial()
