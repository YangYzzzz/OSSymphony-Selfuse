"""
Initial Setup: Shipping manifest template - blank ShipManifest sheet
Task ID: calc_ops_warehouse_shipping_manifest_019
Domain: libreoffice_calc

Creates a workbook with a single blank 'ShipManifest' sheet (the pre-task state).
"""

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ops_warehouse_shipping_manifest_019'
OUTPUT = f'{WORKDIR}/{TASK_ID}_initial.xlsx'


def create_initial():
    wb = openpyxl.Workbook()

    # Rename the default sheet to 'ShipManifest'
    ws = wb.active
    ws.title = 'ShipManifest'

    # The sheet is intentionally blank (per task context:
    # "Sheet 'ShipManifest' is currently blank")
    # No merged cells, no headers, no formulas, no print settings

    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')


create_initial()
