"""
Reward Script: Configure header/footer with multiple sections and set top margin
Task ID: calc_mcp_092
Domain: libreoffice_calc
Scoring:
  Component 1: Header left section = 'Department: Finance' (0.2 pts)
  Component 2: Header right section = 'DRAFT' (0.15 pts)
  Component 3: Footer left section = 'Prepared by: Controller' (0.15 pts)
  Component 4: Footer center section = 'Page &P' (0.15 pts)
  Component 5: Footer right section = '&D &T' (0.15 pts)
  Component 6: Top margin = 1.2 inches (0.2 pts)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_092'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Audit Trail' sheet must exist
    if 'Audit Trail' not in wb.sheetnames:
        print("FAIL: 'Audit Trail' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Audit Trail']
    hf = ws.HeaderFooter

    # Component 1: Header left section = 'Department: Finance' (0.2 points)
    try:
        header_left = hf.oddHeader.left.text if hf.oddHeader and hf.oddHeader.left else None
        if header_left and header_left.strip() == 'Department: Finance':
            print(f"PASS: Component 1 — Header left = '{header_left}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected header left 'Department: Finance', found: {repr(header_left)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header right section = 'DRAFT' (0.15 points)
    try:
        header_right = hf.oddHeader.right.text if hf.oddHeader and hf.oddHeader.right else None
        if header_right and header_right.strip() == 'DRAFT':
            print(f"PASS: Component 2 — Header right = '{header_right}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected header right 'DRAFT', found: {repr(header_right)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer left section = 'Prepared by: Controller' (0.15 points)
    try:
        footer_left = hf.oddFooter.left.text if hf.oddFooter and hf.oddFooter.left else None
        if footer_left and footer_left.strip() == 'Prepared by: Controller':
            print(f"PASS: Component 3 — Footer left = '{footer_left}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected footer left 'Prepared by: Controller', found: {repr(footer_left)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Footer center section = 'Page &P' (0.15 points)
    try:
        footer_center = hf.oddFooter.center.text if hf.oddFooter and hf.oddFooter.center else None
        if footer_center and footer_center.strip() == 'Page &P':
            print(f"PASS: Component 4 — Footer center = '{footer_center}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected footer center 'Page &P', found: {repr(footer_center)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Footer right section = '&D &T' (0.15 points)
    try:
        footer_right = hf.oddFooter.right.text if hf.oddFooter and hf.oddFooter.right else None
        if footer_right and footer_right.strip() == '&D &T':
            print(f"PASS: Component 5 — Footer right = '{footer_right}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected footer right '&D &T', found: {repr(footer_right)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Top margin = 1.2 inches (0.2 points)
    try:
        top_margin = ws.page_margins.top
        if top_margin is not None and abs(float(top_margin) - 1.2) < 0.05:
            print(f"PASS: Component 6 — Top margin = {top_margin} inches (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 6 — Expected top margin ~1.2, found: {top_margin}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
