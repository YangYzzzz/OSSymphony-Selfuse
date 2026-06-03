"""
Reward Script: Conditional formatting on Sales sheet for profit analysis
Task ID: calc_ggf_044
Domain: libreoffice_calc
Scoring:
  Component 1 (0.20): Conditional formatting rules exist on Sales sheet
  Component 2 (0.30): Rule for negative profit ($F2<0) with red-ish fill on A2:F51
  Component 3 (0.30): Rule for high profit ($F2>5000) with green-ish fill on A2:F51
  Component 4 (0.20): Both rules cover the full 6-column range A2:F51
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_044'


def normalize_formula(f):
    """Normalize a formula string for comparison."""
    if f is None:
        return ''
    return str(f).strip().upper().replace(' ', '').replace('=', '')


def is_reddish(rgb_str):
    """Check if an ARGB hex string represents a reddish/light-red color."""
    if not rgb_str or len(rgb_str) < 6:
        return False
    # Extract RGB components (last 6 chars)
    hex_rgb = rgb_str[-6:]
    try:
        r = int(hex_rgb[0:2], 16)
        g = int(hex_rgb[2:4], 16)
        b = int(hex_rgb[4:6], 16)
    except ValueError:
        return False
    # Light red: R is dominant, high overall brightness
    # Known good values: FFC7CE (255, 199, 206), FF0000, etc.
    return r > 180 and r > g and r > b


def is_greenish(rgb_str):
    """Check if an ARGB hex string represents a greenish/light-green color."""
    if not rgb_str or len(rgb_str) < 6:
        return False
    hex_rgb = rgb_str[-6:]
    try:
        r = int(hex_rgb[0:2], 16)
        g = int(hex_rgb[2:4], 16)
        b = int(hex_rgb[4:6], 16)
    except ValueError:
        return False
    # Light green: G is dominant
    # Known good values: C6EFCE (198, 239, 206), 00FF00, etc.
    return g > 180 and g > r and g > b


def range_covers_a2_f51(range_str):
    """Check if a conditional formatting range covers A2:F51 (all 6 columns, rows 2-51)."""
    range_str = str(range_str).upper().replace(' ', '')
    # The range could be exactly A2:F51 or contain it
    # Check for common representations
    if 'A2:F51' in range_str:
        return True
    # Also accept if it covers at least columns A-F and rows 2-51
    # Parse the range to check coverage
    try:
        from openpyxl.utils import range_boundaries
        parts = range_str.split(':')
        if len(parts) == 2:
            min_col, min_row, max_col, max_row = range_boundaries(range_str)
            if min_col <= 1 and max_col >= 6 and min_row <= 2 and max_row >= 51:
                return True
    except Exception:
        pass
    return False


def verify_task(file_path):
    """
    Verify conditional formatting task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check Sales sheet exists
    if 'Sales' not in wb.sheetnames:
        print("FAIL: 'Sales' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Sales']

    # Collect all conditional formatting rules
    all_rules = []
    for cf in ws.conditional_formatting:
        cf_range = str(cf)
        for rule in cf.rules:
            all_rules.append({
                'range': cf_range,
                'type': rule.type,
                'formula': rule.formula,
                'dxf': rule.dxf,
            })

    print(f"Found {len(all_rules)} conditional formatting rule(s)")
    for i, r in enumerate(all_rules):
        formulas_str = ', '.join(str(f) for f in r['formula']) if r['formula'] else 'none'
        print(f"  Rule {i}: range={r['range']}, type={r['type']}, formula=[{formulas_str}]")

    # Component 1: At least 2 conditional formatting rules exist (0.20 points)
    try:
        if len(all_rules) >= 2:
            print(f"PASS: Component 1 - Found {len(all_rules)} CF rules (>= 2 required) (0.20 pts)")
            total_score += 0.20
        elif len(all_rules) == 1:
            print(f"PARTIAL: Component 1 - Found 1 CF rule, expected at least 2 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 - No conditional formatting rules found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Rule for negative profit with red fill (0.30 points)
    try:
        found_neg_rule = False
        for r in all_rules:
            if r['formula']:
                for f in r['formula']:
                    nf = normalize_formula(f)
                    # Check for $F2<0 or F2<0 patterns
                    if ('F2<0' in nf or 'F$2<0' in nf) and '>' not in nf:
                        # Check for red fill
                        has_red = False
                        if r['dxf'] and r['dxf'].fill:
                            fill = r['dxf'].fill
                            if fill.fgColor and fill.fgColor.rgb:
                                has_red = is_reddish(str(fill.fgColor.rgb))
                            if not has_red and fill.bgColor and fill.bgColor.rgb:
                                has_red = is_reddish(str(fill.bgColor.rgb))
                        if has_red:
                            print(f"PASS: Component 2 - Negative profit rule found with red fill (0.30 pts)")
                            total_score += 0.30
                            found_neg_rule = True
                            break
                        else:
                            # Formula matches but fill color doesn't - partial credit
                            print(f"PARTIAL: Component 2 - Formula matches but fill is not reddish (0.15 pts)")
                            total_score += 0.15
                            found_neg_rule = True
                            break
            if found_neg_rule:
                break
        if not found_neg_rule:
            print(f"FAIL: Component 2 - No rule with formula $F2<0 found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Rule for high profit with green fill (0.30 points)
    try:
        found_high_rule = False
        for r in all_rules:
            if r['formula']:
                for f in r['formula']:
                    nf = normalize_formula(f)
                    # Check for $F2>5000 or F2>5000 patterns
                    if ('F2>5000' in nf or 'F$2>5000' in nf) and '<' not in nf:
                        # Check for green fill
                        has_green = False
                        if r['dxf'] and r['dxf'].fill:
                            fill = r['dxf'].fill
                            if fill.fgColor and fill.fgColor.rgb:
                                has_green = is_greenish(str(fill.fgColor.rgb))
                            if not has_green and fill.bgColor and fill.bgColor.rgb:
                                has_green = is_greenish(str(fill.bgColor.rgb))
                        if has_green:
                            print(f"PASS: Component 3 - High profit rule found with green fill (0.30 pts)")
                            total_score += 0.30
                            found_high_rule = True
                            break
                        else:
                            print(f"PARTIAL: Component 3 - Formula matches but fill is not greenish (0.15 pts)")
                            total_score += 0.15
                            found_high_rule = True
                            break
            if found_high_rule:
                break
        if not found_high_rule:
            print(f"FAIL: Component 3 - No rule with formula $F2>5000 found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Both rules cover the correct range A2:F51 (0.20 points)
    try:
        neg_range_ok = False
        high_range_ok = False
        for r in all_rules:
            if r['formula']:
                for f in r['formula']:
                    nf = normalize_formula(f)
                    if ('F2<0' in nf or 'F$2<0' in nf) and '>' not in nf:
                        if range_covers_a2_f51(r['range']):
                            neg_range_ok = True
                    if ('F2>5000' in nf or 'F$2>5000' in nf) and '<' not in nf:
                        if range_covers_a2_f51(r['range']):
                            high_range_ok = True
        if neg_range_ok and high_range_ok:
            print(f"PASS: Component 4 - Both rules cover A2:F51 range (0.20 pts)")
            total_score += 0.20
        elif neg_range_ok or high_range_ok:
            print(f"PARTIAL: Component 4 - Only one rule has correct range A2:F51 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - Neither rule covers A2:F51")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
