"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need all numbers formatted with a comma (,) as the decimal separator for clarity in visualization. Please update the sheet and preserve decimal precision.
Generated: 2025-11-24 07:30:16
Status: success
Model: o3
Total Steps: 10
"""

import openpyxl
import math

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def is_comma_decimal_format(fmt: str) -> bool:
    """Return True if the Excel number-format string uses a comma (",")
    as the decimal separator and provides at least one digit placeholder
    after that comma.
    """
    if not isinstance(fmt, str):
        return False

    last_dot = fmt.rfind('.')
    last_comma = fmt.rfind(',')

    # There must be a comma and the comma must appear *after* the last dot
    if last_comma == -1 or last_comma < last_dot:
        return False

    # At least one digit placeholder (0 or #) must follow the comma
    return any(ch in '0#' for ch in fmt[last_comma + 1:])


def decimal_digits_needed(value) -> int:
    """How many decimal digits are logically part of this value?  For ints
    return 0.  For floats we use a safe string conversion that avoids
    binary floating point noise for user-typed numbers such as 123.45.
    """
    if isinstance(value, int):
        return 0

    s = str(value)
    if 'e' in s or 'E' in s:                 # scientific notation – expand
        s = ('%.15f' % value).rstrip('0')
    return len(s.split('.')[-1]) if '.' in s else 0


def placeholders_after_comma(fmt: str) -> int:
    """Count how many 0/# placeholders exist after the decimal comma."""
    if not isinstance(fmt, str):
        return 0
    last_comma = fmt.rfind(',')
    if last_comma == -1:
        return 0
    return sum(1 for ch in fmt[last_comma + 1:] if ch in '0#')

# ------------------------------------------------------------
# Verification function
# ------------------------------------------------------------

def verify_task(file_path: str) -> float:
    print(f"Starting verification for file: {file_path}")

    try:
        wb = openpyxl.load_workbook(file_path)
        print("✓ Workbook loaded successfully")
    except Exception as e:
        print(f"✗ Unable to load workbook: {e}")
        return 0.0

    numeric_cells = 0
    comma_ok = 0
    precision_ok = 0

    # --------------------------------------------------------
    # Iterate through every worksheet and every cell
    # --------------------------------------------------------
    for ws in wb.worksheets:
        print(f"Checking worksheet: {ws.title}")
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, (int, float)):
                    numeric_cells += 1
                    fmt = cell.number_format or ''

                    # Requirement 1 – comma as decimal separator
                    if is_comma_decimal_format(fmt):
                        comma_ok += 1
                    else:
                        print(f"  ✗ {cell.coordinate}: format '{fmt}' does not use comma decimal separator")

                    # Requirement 2 – preserve decimal precision
                    needed = decimal_digits_needed(cell.value)
                    shown  = placeholders_after_comma(fmt)
                    if shown >= needed:
                        precision_ok += 1
                    else:
                        print(f"  ✗ {cell.coordinate}: needs {needed} decimals, format shows {shown}")

    print(f"Total numeric cells analysed: {numeric_cells}")

    if numeric_cells == 0:
        print("✗ No numeric cells found – cannot award any points")
        return 0.0

    # --------------------------------------------------------
    # Scoring
    # --------------------------------------------------------
    score = 0.0

    # Primary objective (0.7): every numeric cell uses comma decimal separator
    if comma_ok == numeric_cells:
        print("✓ All numeric cells use comma as decimal separator (0.7 points)")
        score += 0.7
    else:
        print(f"✗ {numeric_cells - comma_ok} cells without correct decimal-comma formatting")

    # Secondary objective (0.3): decimal precision preserved everywhere
    if precision_ok == numeric_cells:
        print("✓ Decimal precision preserved for all numeric cells (0.3 points)")
        score += 0.3
    else:
        print(f"✗ {numeric_cells - precision_ok} cells lose decimal precision in their format")

    final_score = round(min(score, 1.0), 3)
    print(f"Final score: {final_score}")
    return final_score

# ------------------------------------------------------------
# Script entry point – executes verification and prints reward
# ------------------------------------------------------------
if __name__ == "__main__":
    FILE = "/home/user/i_need_all_numbers_formatted_with_a_comma_as_the_decimal_separator_for_clarity_in_visualization_plea.xlsx"
    reward = verify_task(FILE)
    print(f"REWARD: {reward}")
