"""
Initial Setup: Personal Monthly Budget Tracker
Task ID: calc_gen_personal_026
Domain: libreoffice_calc

Creates a blank 'Budget' spreadsheet — the starting state before the agent
builds the budget tracker. The sheet is intentionally empty (no formulas,
no formatting, no charts) so the agent must set everything up from scratch.
"""

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gen_personal_026'
OUTPUT = f'{WORKDIR}/{TASK_ID}_initial.xlsx'


def create_initial():
    wb = openpyxl.Workbook()

    # Single blank sheet named 'Budget'
    ws = wb.active
    ws.title = 'Budget'

    # Intentionally blank — no formulas, no formatting, no charts
    # The agent must build the entire budget tracker from scratch

    wb.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print('Content: Single blank sheet named "Budget" (no data, no formulas, no charts)')


create_initial()
