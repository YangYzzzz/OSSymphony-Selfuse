"""
Reward Script: Financial Ratio Analysis PDF creation
Task ID: pdf_fin_081
Domain: pdf
Scoring:
  Component 1 (0.15): PDF file exists at correct path
  Component 2 (0.20): All 4 ratio category section headings present
  Component 3 (0.30): All 13 individual ratio values present and correct
  Component 4 (0.15): Benchmark values present for comparison
  Component 5 (0.20): Color-coded status indicators present (non-black colored text)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_081'
PDF_PATH = os.path.join(WORKDIR, 'finance', 'ratio_analysis_2023.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists at the correct path (0.15 points)
    # Task asks to CREATE this file, so it does not exist in initial_env
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — PDF not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0
        file_size = os.path.getsize(file_path)
        if file_size > 100:
            print(f"PASS: Component 1 — PDF exists at {file_path} ({file_size} bytes) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF too small ({file_size} bytes), likely empty/corrupt")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF and extract all text
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        all_text = ""
        for page in doc:
            all_text += page.get_text("text") + "\n"
        page_count = doc.page_count
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize text for searching
    text_lower = all_text.lower()

    # Component 2: All 4 ratio category section headings (0.20 points)
    # Task requires Liquidity, Profitability, Leverage, and Efficiency sections
    try:
        sections = {
            "Liquidity": "liquidity" in text_lower and "ratio" in text_lower,
            "Profitability": "profitability" in text_lower or "profit" in text_lower,
            "Leverage": "leverage" in text_lower,
            "Efficiency": "efficiency" in text_lower,
        }
        sections_found = sum(1 for v in sections.values() if v)
        if sections_found == 4:
            print(f"PASS: Component 2 — All 4 ratio categories found (0.20 pts)")
            total_score += 0.20
        elif sections_found >= 2:
            partial = round(0.20 * sections_found / 4, 2)
            missing = [k for k, v in sections.items() if not v]
            print(f"PARTIAL: Component 2 — {sections_found}/4 categories found, missing: {missing} ({partial} pts)")
            total_score += partial
        else:
            missing = [k for k, v in sections.items() if not v]
            print(f"FAIL: Component 2 — Only {sections_found}/4 categories found, missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 13 individual ratio values present (0.30 points)
    # Each ratio is worth ~0.023 points (0.30 / 13)
    try:
        # Define expected ratios with their names and values to search for
        ratios = [
            ("Current Ratio", ["2.10", "2.1"]),
            ("Quick Ratio", ["1.50", "1.5"]),
            ("Cash Ratio", ["0.80", "0.8"]),
            ("Gross Margin", ["42", "42.00%", "42%"]),
            ("Operating Margin", ["18", "18.00%", "18%"]),
            ("Net Margin", ["12", "12.00%", "12%"]),
            ("ROE", ["15", "15.00%", "15%"]),
            ("ROA", ["8", "8.00%", "8%"]),
            ("Debt-to-Equity", ["0.65"]),
            ("Interest Coverage", ["8.20", "8.2"]),
            ("Inventory Turnover", ["6.50", "6.5"]),
            ("AR Turnover", ["9.20", "9.2"]),
            ("AP Turnover", ["7.80", "7.8"]),
        ]
        ratios_found = 0
        for name, values in ratios:
            # Check if the ratio name (or close variant) appears in text
            name_found = name.lower().replace("-", "") in text_lower.replace("-", "") or \
                         name.lower().split()[0] in text_lower
            # Check if any of the expected values appear
            value_found = any(v in all_text for v in values)
            if name_found and value_found:
                ratios_found += 1
            else:
                print(f"  DETAIL: Ratio '{name}' — name_found={name_found}, value_found={value_found}")

        points_per_ratio = 0.30 / 13
        comp3_score = round(ratios_found * points_per_ratio, 4)
        if ratios_found == 13:
            print(f"PASS: Component 3 — All 13 ratios found with correct values (0.30 pts)")
            total_score += 0.30
        elif ratios_found > 0:
            print(f"PARTIAL: Component 3 — {ratios_found}/13 ratios found ({comp3_score:.2f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No ratios found with matching values")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Benchmark values present (0.15 points)
    # The golden PDF includes a Benchmark column with comparison values
    try:
        benchmark_present = "benchmark" in text_lower
        # Check for specific benchmark values that appear in the golden PDF
        benchmark_values = ["1.80", "1.20", "0.50", "38.00", "15.00", "10.00",
                           "14.00", "7.00", "0.80", "6.00", "5.50", "8.00", "7.00"]
        benchmarks_found = sum(1 for v in benchmark_values if v in all_text)
        if benchmark_present and benchmarks_found >= 8:
            print(f"PASS: Component 4 — Benchmark data present ({benchmarks_found} benchmark values found) (0.15 pts)")
            total_score += 0.15
        elif benchmark_present and benchmarks_found >= 4:
            partial = round(0.15 * benchmarks_found / 10, 2)
            print(f"PARTIAL: Component 4 — Benchmark label present but only {benchmarks_found} values found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Benchmark data insufficient (label={benchmark_present}, values={benchmarks_found})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Color-coded status indicators (0.20 points)
    # Task requires color-coded indicators (green for above benchmark, red for below)
    # We check for non-black colored text spans that serve as status indicators
    try:
        GREEN_INT = 2600544   # RGB(39,174,96) — "Above Benchmark" color in golden
        ORANGE_INT = 15965202  # RGB(243,156,18) — "Near Benchmark"
        RED_INT = 15158332     # RGB(231,76,60) — "Below Benchmark"
        INDICATOR_COLORS = {GREEN_INT, ORANGE_INT, RED_INT}

        green_count = 0
        other_indicator_count = 0

        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" not in b:
                    continue
                for line in b["lines"]:
                    for span in line["spans"]:
                        color_int = span.get("color", 0)
                        text = span.get("text", "").strip()
                        # Count exact-match indicator colors
                        if color_int == GREEN_INT:
                            green_count += 1
                        elif color_int in INDICATOR_COLORS:
                            other_indicator_count += 1
                        # Also accept other green-ish or red-ish colors
                        elif color_int != 0:
                            r = (color_int >> 16) & 0xFF
                            g = (color_int >> 8) & 0xFF
                            bl = color_int & 0xFF
                            if g > 120 and r < 100 and bl < 120 and len(text) <= 3:
                                green_count += 1
                            elif r > 180 and g < 120 and bl < 120 and len(text) <= 3:
                                other_indicator_count += 1

        total_indicators = green_count + other_indicator_count
        if green_count > 0 and total_indicators >= 5:
            print(f"PASS: Component 5 — Color-coded indicators present (green={green_count}, other={other_indicator_count}, total={total_indicators}) (0.20 pts)")
            total_score += 0.20
        elif green_count > 0 or total_indicators >= 3:
            print(f"PARTIAL: Component 5 — Some color indicators found (green={green_count}, total={total_indicators}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No color-coded indicators found (green={green_count}, total={total_indicators})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.isfile(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
