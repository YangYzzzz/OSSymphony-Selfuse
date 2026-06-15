"""
Reward Script: Monthly Budget Variance Report PDF
Task ID: pdf_fin_071
Domain: pdf
Scoring:
  Component 1: PDF exists and is valid with correct structure (0.15)
  Component 2: Table has all 7 category rows with correct names (0.15)
  Component 3: Correct budget and actual values for all categories (0.20)
  Component 4: Correct variance calculations (Budget-Actual for expenses, Actual-Budget for revenue) (0.25)
  Component 5: Color-coding — green for favorable variances, red for unfavorable (0.25)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_071'

# Expected data: (Category, Budget, Actual)
# Revenue: favorable when Actual > Budget
# Expenses (COGS, Salaries, Marketing, Rent, Utilities, Other): favorable when Actual < Budget
EXPECTED_DATA = {
    'Revenue':   (500000, 485000),
    'COGS':      (200000, 210000),
    'Salaries':  (150000, 148000),
    'Marketing': (40000,  52000),
    'Rent':      (25000,  25000),
    'Utilities': (8000,   9500),
    'Other':     (15000,  11000),
}

# Variance rules:
# Revenue: Actual - Budget (negative = unfavorable)
# Expenses: Budget - Actual (negative = unfavorable)
REVENUE_CATEGORIES = {'Revenue'}

def compute_variance(category, budget, actual):
    """Compute variance. Positive = favorable, negative = unfavorable."""
    if category in REVENUE_CATEGORIES:
        return actual - budget
    else:
        return budget - actual

def compute_variance_pct(variance, budget):
    if budget == 0:
        return 0.0
    return (variance / budget) * 100


def parse_dollar_value(text):
    """Parse dollar amounts like '$500,000', '-$15,000', '$0' to int."""
    text = text.strip().replace(',', '').replace('$', '')
    if not text or text == '0':
        return 0
    return int(float(text))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pymupdf

    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF exists and is valid with correct structure (0.15 points)
    # Check: single page, has table columns, produced by reportlab
    try:
        page_count = doc.page_count
        full_text = doc[0].get_text("text")
        has_columns = all(col in full_text for col in ["Category", "Budget", "Actual", "Variance"])
        has_title = "variance" in full_text.lower() and "report" in full_text.lower()

        if page_count >= 1 and has_columns and has_title:
            print(f"PASS: Component 1 — Valid PDF with table structure, {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Missing structure. pages={page_count}, has_columns={has_columns}, has_title={has_title}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Table has all 7 category rows (0.15 points)
    try:
        found_categories = []
        for cat in EXPECTED_DATA.keys():
            if cat in full_text:
                found_categories.append(cat)

        cat_ratio = len(found_categories) / len(EXPECTED_DATA)
        if cat_ratio == 1.0:
            print(f"PASS: Component 2 — All 7 categories found: {found_categories} (0.15 pts)")
            total_score += 0.15
        elif cat_ratio >= 0.5:
            partial = round(0.15 * cat_ratio, 3)
            print(f"PARTIAL: Component 2 — {len(found_categories)}/7 categories found: {found_categories} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {len(found_categories)}/7 categories found: {found_categories}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct budget and actual values (0.20 points)
    # Extract text spans and check the dollar values per row
    try:
        page = doc[0]
        data = page.get_text("dict")

        # Collect all text spans with positions, sorted by y then x
        all_spans = []
        for block in data["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        bbox = span["bbox"]
                        all_spans.append({
                            "text": text,
                            "x": bbox[0],
                            "y": bbox[1],
                            "color": span["color"],
                            "font": span["font"],
                        })

        # Group spans by approximate y-coordinate (rows)
        all_spans.sort(key=lambda s: (round(s["y"] / 5) * 5, s["x"]))

        # For each category, find its row and extract dollar values
        correct_values = 0
        total_checks = 0
        for cat, (exp_budget, exp_actual) in EXPECTED_DATA.items():
            # Find spans in the row containing this category name
            cat_spans = [s for s in all_spans if s["text"] == cat]
            if not cat_spans:
                total_checks += 2
                continue

            cat_y = cat_spans[0]["y"]
            # Get all spans on same row (within 5pt y tolerance)
            row_spans = [s for s in all_spans if abs(s["y"] - cat_y) < 5]
            row_spans.sort(key=lambda s: s["x"])

            # Extract dollar values from this row
            dollar_vals = []
            for s in row_spans:
                if '$' in s["text"] or (s["text"].replace(',', '').replace('-', '').replace('.', '').isdigit() and s["text"] != cat):
                    try:
                        dollar_vals.append(parse_dollar_value(s["text"]))
                    except (ValueError, TypeError):
                        pass

            # First two dollar values should be Budget and Actual
            total_checks += 2
            if len(dollar_vals) >= 2:
                if dollar_vals[0] == exp_budget:
                    correct_values += 1
                else:
                    print(f"  {cat} budget: expected {exp_budget}, found {dollar_vals[0]}")
                if dollar_vals[1] == exp_actual:
                    correct_values += 1
                else:
                    print(f"  {cat} actual: expected {exp_actual}, found {dollar_vals[1]}")
            else:
                print(f"  {cat}: could not extract budget/actual values from row (found {len(dollar_vals)} dollar values)")

        if total_checks > 0:
            ratio = correct_values / total_checks
            points = round(0.20 * ratio, 3)
            if ratio == 1.0:
                print(f"PASS: Component 3 — All {correct_values}/{total_checks} budget/actual values correct (0.20 pts)")
                total_score += 0.20
            elif ratio > 0:
                print(f"PARTIAL: Component 3 — {correct_values}/{total_checks} values correct ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 3 — No correct budget/actual values")
        else:
            print(f"FAIL: Component 3 — Could not extract any values")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct variance calculations (0.25 points)
    try:
        correct_variances = 0
        total_var_checks = 0

        for cat, (exp_budget, exp_actual) in EXPECTED_DATA.items():
            exp_variance = compute_variance(cat, exp_budget, exp_actual)

            # Find the category row again
            cat_spans = [s for s in all_spans if s["text"] == cat]
            if not cat_spans:
                total_var_checks += 1
                continue

            cat_y = cat_spans[0]["y"]
            row_spans = [s for s in all_spans if abs(s["y"] - cat_y) < 5]
            row_spans.sort(key=lambda s: s["x"])

            # Extract dollar values — third should be variance
            dollar_vals = []
            for s in row_spans:
                if '$' in s["text"]:
                    try:
                        dollar_vals.append(parse_dollar_value(s["text"]))
                    except (ValueError, TypeError):
                        pass

            total_var_checks += 1
            if len(dollar_vals) >= 3:
                actual_variance = dollar_vals[2]
                if actual_variance == exp_variance:
                    correct_variances += 1
                else:
                    print(f"  {cat} variance: expected {exp_variance}, found {actual_variance}")
            else:
                print(f"  {cat}: could not find variance value (found {len(dollar_vals)} dollar values)")

        if total_var_checks > 0:
            ratio = correct_variances / total_var_checks
            points = round(0.25 * ratio, 3)
            if ratio == 1.0:
                print(f"PASS: Component 4 — All {correct_variances}/{total_var_checks} variance calculations correct (0.25 pts)")
                total_score += 0.25
            elif ratio > 0:
                print(f"PARTIAL: Component 4 — {correct_variances}/{total_var_checks} variances correct ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 4 — No correct variance calculations")
        else:
            print(f"FAIL: Component 4 — Could not check variances")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Color-coding — green for favorable, red for unfavorable (0.25 points)
    # Red = (231,76,60) = 0xE74C3C, Green = (39,174,96) = 0x27AE60
    try:
        RED_THRESHOLD = 150  # R component high, G and B low
        GREEN_THRESHOLD = 100  # G component high

        correct_colors = 0
        total_color_checks = 0

        for cat, (exp_budget, exp_actual) in EXPECTED_DATA.items():
            exp_variance = compute_variance(cat, exp_budget, exp_actual)
            if exp_variance == 0:
                # Neutral variance — no color requirement
                continue

            # Find category row
            cat_spans_c = [s for s in all_spans if s["text"] == cat]
            if not cat_spans_c:
                total_color_checks += 1
                continue

            cat_y = cat_spans_c[0]["y"]
            row_spans = [s for s in all_spans if abs(s["y"] - cat_y) < 5]
            row_spans.sort(key=lambda s: s["x"])

            # Find the variance cell (should contain $ and be the 3rd dollar value)
            variance_spans = [s for s in row_spans if '$' in s["text"]]
            if len(variance_spans) >= 3:
                var_span = variance_spans[2]
                color_int = var_span["color"]
                r = (color_int >> 16) & 0xFF
                g = (color_int >> 8) & 0xFF
                b = color_int & 0xFF

                total_color_checks += 1
                if exp_variance > 0:
                    # Favorable — should be green
                    if g > RED_THRESHOLD and r < GREEN_THRESHOLD:
                        correct_colors += 1
                    else:
                        print(f"  {cat} variance color: expected green (favorable), found RGB({r},{g},{b})")
                else:
                    # Unfavorable — should be red
                    if r > RED_THRESHOLD and g < GREEN_THRESHOLD:
                        correct_colors += 1
                    else:
                        print(f"  {cat} variance color: expected red (unfavorable), found RGB({r},{g},{b})")
            else:
                total_color_checks += 1
                print(f"  {cat}: could not find variance span for color check")

        if total_color_checks > 0:
            ratio = correct_colors / total_color_checks
            points = round(0.25 * ratio, 3)
            if ratio == 1.0:
                print(f"PASS: Component 5 — All {correct_colors}/{total_color_checks} variance colors correct (0.25 pts)")
                total_score += 0.25
            elif ratio > 0:
                print(f"PARTIAL: Component 5 — {correct_colors}/{total_color_checks} colors correct ({points} pts)")
                total_score += points
            else:
                print(f"FAIL: Component 5 — No correct variance colors")
        else:
            print(f"FAIL: Component 5 — Could not check colors")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/finance/variance_report_march.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
