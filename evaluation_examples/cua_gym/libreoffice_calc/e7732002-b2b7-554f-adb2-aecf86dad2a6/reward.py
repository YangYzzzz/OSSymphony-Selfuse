"""
Reward Script: WEEKDAY-based conditional formatting for time tracking sheet
Task ID: osworld_calc_conditional_format_weekday_006
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4 pts): CF rule with WEEKDAY-based formula highlights weekend dates with green fill
  Component 2 (0.4 pts): CF rule with AND(hours>8, WEEKDAY-weekday) highlights weekday overtime with red fill
  Component 3 (0.2 pts): Both CF rules are applied to a range that covers the data area (col A through D, rows 2+)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_conditional_format_weekday_006'


def normalize_formula(f):
    """Normalize a formula string for loose comparison."""
    return f.upper().replace(' ', '').replace('"', "'")


def has_weekday_weekend_rule(rules):
    """
    Check if any rule is a formula-based rule whose formula uses WEEKDAY to identify weekends.
    Acceptable patterns:
      - WEEKDAY($A2,2)>=6  (Mon=1 mode, Sat=6, Sun=7)
      - WEEKDAY($A2,1)>=7  (Sun=1 mode, Sat=7)
      - WEEKDAY($A2,1)=1   (Sun=1, checking Sunday only, less likely)
      - OR(WEEKDAY(...), ...)
    We accept any formula that contains WEEKDAY and some form of >=6, =7, >=7, =6 etc.
    Primary check: formula contains WEEKDAY and (>=6 or >=7 or =6 or =7) to catch common variants.
    """
    for rule in rules:
        if rule.type != 'expression':
            continue
        for f in rule.formula:
            nf = normalize_formula(f)
            if 'WEEKDAY' not in nf:
                continue
            # Check for patterns that identify Saturday (6 in mode 2) or Sunday (7 in mode 2)
            # e.g., >=6, =6, =7, >=7, >5
            if re.search(r'(>=6|>=7|=6|=7|>5)', nf):
                return True
            # Also accept OR-based patterns
            if re.search(r'OR\(.*WEEKDAY.*\)', nf):
                return True
    return False


def get_weekend_rule_fill(rules):
    """Return the fgColor.rgb of the weekend-detection rule, or None if not found."""
    for rule in rules:
        if rule.type != 'expression':
            continue
        for f in rule.formula:
            nf = normalize_formula(f)
            if 'WEEKDAY' not in nf:
                continue
            if re.search(r'(>=6|>=7|=6|=7|>5)', nf):
                try:
                    return rule.dxf.fill.fgColor.rgb
                except Exception:
                    return None
    return None


def has_overtime_weekday_rule(rules):
    """
    Check if any rule is a formula-based rule that identifies weekday overtime:
    hours > 8 AND WEEKDAY-based condition indicating a weekday.
    Acceptable patterns:
      - AND($D2>8, WEEKDAY($A2,2)<6)
      - AND(WEEKDAY($A2,2)<6, $D2>8)
      - AND($D2>8, WEEKDAY($A2,1)>1, WEEKDAY($A2,1)<7)  (less likely)
    Primary check: formula contains both 'WEEKDAY' and 'D2>8' (or D2>=9) and some form of <6, <=5, <7
    """
    for rule in rules:
        if rule.type != 'expression':
            continue
        for f in rule.formula:
            nf = normalize_formula(f)
            if 'WEEKDAY' not in nf:
                continue
            # Must have some hours condition: D2>8 or D2>=9
            has_hours = bool(re.search(r'D\d*>8|D\d*>=9', nf))
            # Must have weekday condition: <6, <=5, <7 (for mode 2), or >1,<7 (for mode 1)
            has_weekday_cond = bool(re.search(r'(<6|<=5|<7|WEEKDAY.*<6|WEEKDAY.*<=5)', nf))
            if has_hours and has_weekday_cond:
                return True
    return False


def get_overtime_rule_fill(rules):
    """Return the fgColor.rgb of the overtime-on-weekday rule, or None."""
    for rule in rules:
        if rule.type != 'expression':
            continue
        for f in rule.formula:
            nf = normalize_formula(f)
            if 'WEEKDAY' not in nf:
                continue
            has_hours = bool(re.search(r'D\d*>8|D\d*>=9', nf))
            has_weekday_cond = bool(re.search(r'(<6|<=5|<7|WEEKDAY.*<6|WEEKDAY.*<=5)', nf))
            if has_hours and has_weekday_cond:
                try:
                    return rule.dxf.fill.fgColor.rgb
                except Exception:
                    return None
    return None


def is_green_color(rgb):
    """Return True if the color is green (or a shade of green)."""
    if not rgb or len(rgb) != 8:
        return False
    # Extract R, G, B from ARGB
    r = int(rgb[2:4], 16)
    g = int(rgb[4:6], 16)
    b = int(rgb[6:8], 16)
    # Pure green: 00FF00, or any green-dominant color
    # Minimum: G is the dominant channel and noticeably green
    return g > 100 and g > r and g > b


def is_red_color(rgb):
    """Return True if the color is red (or a shade of red)."""
    if not rgb or len(rgb) != 8:
        return False
    r = int(rgb[2:4], 16)
    g = int(rgb[4:6], 16)
    b = int(rgb[6:8], 16)
    # Red dominant
    return r > 100 and r > g and r > b


def covers_data_range(cf_range_str):
    """
    Check if the CF range string covers the data area: columns A-D, starting from row 2.
    Acceptable ranges include A2:D23, A2:D100, A:D, A2:D1048576, etc.
    We simply check that the range starts at or before row 2 and includes columns A and D.
    """
    if not cf_range_str:
        return False
    cf_str = str(cf_range_str).upper()
    # Must include column A (start) and column D (end)
    # Range like A2:D23, $A$2:$D$23, A2:D1048576
    # We strip $ signs for easier parsing
    cf_clean = cf_str.replace('$', '')
    # Match a range like A<num>:D<num> or A:D
    match = re.match(r'([A-Z]+)(\d*):([A-Z]+)(\d*)', cf_clean)
    if match:
        start_col, start_row, end_col, end_row = match.groups()
        # Check columns span A to at least D
        if start_col <= 'A' and end_col >= 'D':
            # Check starting row: must be 2 or earlier (row 1 is header, data starts at 2)
            if not start_row or int(start_row) <= 2:
                return True
    return False


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

    # Validate we have the expected sheet
    if 'Time Tracking' not in wb.sheetnames:
        print("CRITICAL: 'Time Tracking' sheet not found.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Time Tracking']

    # Gather all conditional formatting rules from all ranges
    all_rules = []
    cf_range_strs = []
    for cf_range in ws.conditional_formatting:
        # Use .sqref attribute if available, otherwise fall back to str representation
        try:
            cf_range_strs.append(str(cf_range.sqref))
        except AttributeError:
            # Fallback: extract range from repr like '<ConditionalFormatting A2:D23>'
            raw = str(cf_range)
            # strip class prefix if present
            parts = raw.split()
            cf_range_strs.append(parts[-1].rstrip('>') if len(parts) > 1 else raw)
        for rule in ws.conditional_formatting[cf_range]:
            all_rules.append(rule)

    if not all_rules:
        print("FAIL: No conditional formatting rules found.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # -------------------------------------------------------------------------
    # Component 1: WEEKDAY-based green fill for weekend rows (0.4 points)
    # -------------------------------------------------------------------------
    try:
        weekend_rule_found = has_weekday_weekend_rule(all_rules)
        if weekend_rule_found:
            weekend_fill = get_weekend_rule_fill(all_rules)
            green_fill_ok = is_green_color(weekend_fill) if weekend_fill else False
            if green_fill_ok:
                print(f"PASS: Component 1 — Weekend WEEKDAY rule found with green fill ({weekend_fill}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — Weekend WEEKDAY rule found but fill color is not green (got: {weekend_fill})")
        else:
            print("FAIL: Component 1 — No WEEKDAY-based formula rule to highlight weekend dates found.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: WEEKDAY + overtime (D>8) red fill rule (0.4 points)
    # -------------------------------------------------------------------------
    try:
        overtime_rule_found = has_overtime_weekday_rule(all_rules)
        if overtime_rule_found:
            overtime_fill = get_overtime_rule_fill(all_rules)
            red_fill_ok = is_red_color(overtime_fill) if overtime_fill else False
            if red_fill_ok:
                print(f"PASS: Component 2 — Weekday overtime rule found with red fill ({overtime_fill}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Weekday overtime rule found but fill color is not red (got: {overtime_fill})")
        else:
            print("FAIL: Component 2 — No weekday overtime (D>8 AND WEEKDAY) formula rule found.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: CF rules cover the data range (cols A-D, from row 2) (0.2 points)
    # -------------------------------------------------------------------------
    try:
        range_ok = any(covers_data_range(r) for r in cf_range_strs)
        if range_ok:
            print(f"PASS: Component 3 — CF range covers data area (found ranges: {cf_range_strs}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — CF ranges do not adequately cover data area (found: {cf_range_strs})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
