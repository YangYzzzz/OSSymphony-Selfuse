"""
Reward Script: Validate PDF page numbering and write results report
Task ID: pdf_res_093
Domain: pdf
Scoring:
  Component 1 (0.20): page_check.txt exists and has report structure (header + 50 pages mentioned)
  Component 2 (0.25): Report covers all 50 pages individually
  Component 3 (0.25): Correctly identifies OK/correct pages (at least 40 of 44)
  Component 4 (0.30): Correctly identifies the 6 discrepancy pages (7, 23, 31, 38, 45, 50)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_093'
REPORT_PATH = os.path.join(WORKDIR, 'thesis', 'page_check.txt')

# Ground truth from golden exploration:
# Pages with issues: 7 (incorrect, shows 9), 23 (missing), 31 (incorrect, shows 30),
#                    38 (incorrect, shows 40), 45 (missing), 50 (incorrect, shows 49)
# Page 1 is title page (no number expected) - OK
# All other pages are OK
DISCREPANCY_PAGES = {7, 23, 31, 38, 45, 50}
TOTAL_PAGES = 50
CORRECT_PAGES = set(range(1, TOTAL_PAGES + 1)) - DISCREPANCY_PAGES


def verify_task():
    """
    Verify that page_check.txt exists with a proper validation report.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist (not scored alone - combined with structure check)
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found: {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(REPORT_PATH, 'r').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()
    lines = content.strip().split('\n')

    # Component 1: Report structure - has header and mentions 50 pages (0.20 points)
    # This checks that the file is a proper report, not just random text.
    # FAILS on initial_env (file doesn't exist, gate above returns 0.0).
    try:
        # Check for some kind of report header (title/header line about page validation)
        header_found = any(
            'page' in line.lower() and any(kw in line.lower() for kw in ['valid', 'check', 'number', 'report'])
            for line in lines[:5]
        )

        # Check that the report mentions 50 total pages somewhere
        fifty_found = bool(re.search(r'(?:total\s*(?:pages)?|pages)\s*[:\s]*50', content_lower) or '50' in content)

        if header_found and fifty_found:
            print(f"PASS: Component 1 - Report has header and mentions 50 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - header={header_found}, fifty={fifty_found}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Report covers all 50 pages (0.25 points)
    # Check that each page from 1 to 50 is referenced in the report.
    try:
        pages_found = set()
        for line in lines:
            # Match patterns like "Page  7:", "Page 7:", "page 7 ", etc.
            matches = re.findall(r'(?:page)\s*(\d+)', line, re.IGNORECASE)
            for m in matches:
                pg = int(m)
                if 1 <= pg <= 50:
                    pages_found.add(pg)

        coverage = len(pages_found)
        if coverage >= 48:
            # At least 48 of 50 pages mentioned (allowing minor formatting differences)
            print(f"PASS: Component 2 - Report covers {coverage}/50 pages (0.25 pts)")
            total_score += 0.25
        elif coverage >= 40:
            partial = 0.25 * (coverage - 40) / 10.0
            print(f"PARTIAL: Component 2 - Report covers {coverage}/50 pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Report only covers {coverage}/50 pages")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Correctly identifies OK/correct pages (0.25 points)
    # At least 40 of the 44 correct pages should be marked OK/correct.
    try:
        ok_pages = set()
        for line in lines:
            # Match patterns like "Page  2: OK", "Page 10: OK", "Page 1: OK (title..."
            match = re.match(r'.*?page\s+(\d+)\s*:\s*ok\b', line, re.IGNORECASE)
            if match:
                pg = int(match.group(1))
                if 1 <= pg <= 50:
                    ok_pages.add(pg)
            # Also match "correct" instead of "OK"
            match2 = re.match(r'.*?page\s+(\d+)\s*:\s*correct\b', line, re.IGNORECASE)
            if match2:
                pg = int(match2.group(1))
                if 1 <= pg <= 50:
                    ok_pages.add(pg)

        # Count how many of the truly correct pages are marked OK
        correctly_identified_ok = len(ok_pages & CORRECT_PAGES)
        # Also check no discrepancy pages are falsely marked OK
        false_ok = len(ok_pages & DISCREPANCY_PAGES)

        if correctly_identified_ok >= 40 and false_ok == 0:
            print(f"PASS: Component 3 - {correctly_identified_ok}/44 correct pages identified as OK, 0 false OKs (0.25 pts)")
            total_score += 0.25
        elif correctly_identified_ok >= 40:
            # Slight deduction for false OKs
            partial = 0.25 * (1 - false_ok / 6.0)
            print(f"PARTIAL: Component 3 - {correctly_identified_ok} OK but {false_ok} false OKs ({partial:.2f} pts)")
            if partial > 0:
                total_score += partial
        elif correctly_identified_ok >= 30:
            partial = 0.25 * (correctly_identified_ok - 30) / 14.0
            print(f"PARTIAL: Component 3 - Only {correctly_identified_ok}/44 correct pages identified ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Only {correctly_identified_ok}/44 correct pages identified as OK")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Correctly identifies the 6 discrepancy pages (0.30 points)
    # Pages 7 (incorrect/9), 23 (missing), 31 (incorrect/30), 38 (incorrect/40), 45 (missing), 50 (incorrect/49)
    try:
        discrepancies_found = set()
        for line in lines:
            ll = line.lower()
            # Match lines indicating issues: INCORRECT, MISSING, wrong, error, discrepancy
            if any(kw in ll for kw in ['incorrect', 'missing', 'wrong', 'error', 'discrepan', 'mismatch', 'fail']):
                matches = re.findall(r'page\s+(\d+)', line, re.IGNORECASE)
                for m in matches:
                    pg = int(m)
                    if pg in DISCREPANCY_PAGES:
                        discrepancies_found.add(pg)

        found_count = len(discrepancies_found)
        # Award partial credit per discrepancy found
        points_per = 0.30 / 6.0  # 0.05 per discrepancy
        comp4_score = found_count * points_per

        if found_count == 6:
            print(f"PASS: Component 4 - All 6 discrepancies identified: {sorted(discrepancies_found)} (0.30 pts)")
            total_score += 0.30
        elif found_count > 0:
            print(f"PARTIAL: Component 4 - {found_count}/6 discrepancies found: {sorted(discrepancies_found)} ({comp4_score:.2f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 - No discrepancies identified")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
