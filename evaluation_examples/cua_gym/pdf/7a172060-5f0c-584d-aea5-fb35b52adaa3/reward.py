"""
Reward Script: Multi-page financial summary report verification
Task ID: pdf_fin_016
Domain: pdf
Scoring:
  - Component 1 (0.15): PDF exists and has exactly 3 pages
  - Component 2 (0.20): Page 1 title text present
  - Component 3 (0.30): Page 2 table with correct structure and data
  - Component 4 (0.20): Page 3 summary with correct financial figures
  - Component 5 (0.15): Page 3 margin percentage present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_016'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'summary_report.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has exactly 3 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 3:
            print(f"PASS: Component 1 — PDF has exactly 3 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 1 has title 'Q4 2024 Financial Summary' and 'Meridian Corp' (0.20 points)
    try:
        page1_text = doc[0].get_text().lower()
        has_q4 = 'q4 2024 financial summary' in page1_text
        has_meridian = 'meridian corp' in page1_text
        if has_q4 and has_meridian:
            print(f"PASS: Component 2 — Page 1 has title with Q4 2024 Financial Summary and Meridian Corp (0.20 pts)")
            total_score += 0.20
        elif has_q4 or has_meridian:
            print(f"PARTIAL: Component 2 — Found {'Q4 title' if has_q4 else 'Meridian Corp'} but missing {'Meridian Corp' if has_q4 else 'Q4 title'} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Page 1 missing title text. Found: {page1_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 2 has revenue table with correct structure and data (0.30 points)
    try:
        page2_text = doc[1].get_text()
        page2_lower = page2_text.lower()

        # Check table headers
        has_month = 'month' in page2_lower
        has_revenue = 'revenue' in page2_lower
        has_expenses = 'expenses' in page2_lower
        has_net = 'net' in page2_lower
        headers_ok = has_month and has_revenue and has_expenses and has_net

        # Check data rows - key financial figures
        has_oct = 'october' in page2_lower or 'oct' in page2_lower
        has_nov = 'november' in page2_lower or 'nov' in page2_lower
        has_dec = 'december' in page2_lower or 'dec' in page2_lower
        months_ok = has_oct and has_nov and has_dec

        # Check specific dollar amounts (flexible matching)
        has_1200 = '1,200,000' in page2_text or '1200000' in page2_text or '1.2m' in page2_lower or '$1.2m' in page2_lower
        has_800 = '800,000' in page2_text or '800000' in page2_text
        has_400 = '400,000' in page2_text or '400000' in page2_text
        has_1500 = '1,500,000' in page2_text or '1500000' in page2_text or '1.5m' in page2_lower
        has_950 = '950,000' in page2_text or '950000' in page2_text
        has_550 = '550,000' in page2_text or '550000' in page2_text
        has_1800 = '1,800,000' in page2_text or '1800000' in page2_text or '1.8m' in page2_lower
        has_1100 = '1,100,000' in page2_text or '1100000' in page2_text
        has_700 = '700,000' in page2_text or '700000' in page2_text

        # Count how many key values are present
        key_values = [has_1200, has_800, has_400, has_1500, has_950, has_550, has_1800, has_1100, has_700]
        values_present = sum(key_values)

        comp3_score = 0.0
        if headers_ok:
            comp3_score += 0.05
        if months_ok:
            comp3_score += 0.05
        if values_present >= 7:
            comp3_score += 0.20
        elif values_present >= 4:
            comp3_score += 0.10
        elif values_present >= 1:
            comp3_score += 0.05

        if comp3_score > 0:
            print(f"PASS: Component 3 — Table headers={'OK' if headers_ok else 'MISSING'}, months={'OK' if months_ok else 'MISSING'}, values={values_present}/9 ({comp3_score} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — Page 2 table missing. Headers: {headers_ok}, Months: {months_ok}, Values: {values_present}/9")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 3 has summary with correct financial totals (0.20 points)
    try:
        page3_text = doc[2].get_text()
        page3_lower = page3_text.lower()

        has_total_rev = '4.5m' in page3_lower or '4,500,000' in page3_text or '4500000' in page3_text
        has_total_exp = '2.85m' in page3_lower or '2,850,000' in page3_text or '2850000' in page3_text
        has_net_income = '1.65m' in page3_lower or '1,650,000' in page3_text or '1650000' in page3_text

        figures_found = sum([has_total_rev, has_total_exp, has_net_income])

        if figures_found == 3:
            print(f"PASS: Component 4 — All 3 financial totals present on page 3 (0.20 pts)")
            total_score += 0.20
        elif figures_found >= 1:
            partial = round(0.20 * figures_found / 3, 2)
            print(f"PARTIAL: Component 4 — {figures_found}/3 financial totals found (rev={has_total_rev}, exp={has_total_exp}, net={has_net_income}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No financial totals found on page 3. Text: {page3_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 3 has 36.7% margin (0.15 points)
    try:
        page3_text = doc[2].get_text()
        if '36.7%' in page3_text or '36.7 %' in page3_text:
            print(f"PASS: Component 5 — 36.7% margin found on page 3 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — 36.7% margin not found on page 3")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
