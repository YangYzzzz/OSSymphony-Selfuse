"""
Reward Script: Set header distance to 1.5cm and footer distance to 1.0cm from edge
Task ID: calc_gfl_078
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Header margin is 1.5cm (0.5906 inches) from edge
  Component 2 (0.5): Footer margin is 1.0cm (0.3937 inches) from edge
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_078'

# Conversion: 1 inch = 2.54 cm
# 1.5 cm = 1.5 / 2.54 = 0.59055118... inches
# 1.0 cm = 1.0 / 2.54 = 0.39370079... inches
EXPECTED_HEADER_INCHES = 1.5 / 2.54  # ~0.5906
EXPECTED_FOOTER_INCHES = 1.0 / 2.54  # ~0.3937
TOLERANCE = 0.02  # Allow ~0.5mm tolerance


def verify_task(file_path):
    """
    Verify that header and footer margins are set correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Report' sheet must exist
    if 'Report' not in wb.sheetnames:
        print("FAIL: 'Report' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Report']
    pm = ws.page_margins

    # Component 1: Header margin is 1.5cm from edge (0.5 points)
    try:
        header_margin = pm.header
        diff = abs(header_margin - EXPECTED_HEADER_INCHES)
        if diff <= TOLERANCE:
            print(f"PASS: Component 1 - Header margin is {header_margin:.4f} inches "
                  f"(expected ~{EXPECTED_HEADER_INCHES:.4f}, diff={diff:.4f}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Header margin is {header_margin:.4f} inches, "
                  f"expected ~{EXPECTED_HEADER_INCHES:.4f} (1.5cm), diff={diff:.4f}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Footer margin is 1.0cm from edge (0.5 points)
    try:
        footer_margin = pm.footer
        diff = abs(footer_margin - EXPECTED_FOOTER_INCHES)
        if diff <= TOLERANCE:
            print(f"PASS: Component 2 - Footer margin is {footer_margin:.4f} inches "
                  f"(expected ~{EXPECTED_FOOTER_INCHES:.4f}, diff={diff:.4f}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - Footer margin is {footer_margin:.4f} inches, "
                  f"expected ~{EXPECTED_FOOTER_INCHES:.4f} (1.0cm), diff={diff:.4f}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
