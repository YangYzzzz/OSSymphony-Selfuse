"""
Reward Script: Verify PDF margin check report
Task ID: pdf_cr_073
Domain: pdf (libreoffice_calc labeled but actually pdf analysis task)
Scoring:
  Component 1: File exists with page-level analysis lines (0.25)
  Component 2: Correct PASS/FAIL classification per page (0.35)
  Component 3: Margin values present and reasonable (0.25)
  Component 4: Summary line correct (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_073'
REPORT_PATH = os.path.join(WORKDIR, 'Desktop', 'margin_check.txt')


def verify_task():
    """
    Verify that margin_check.txt correctly reports margin analysis
    for printable.pdf. Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: file must exist (not scored alone — gates further checks)
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found: {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(REPORT_PATH).read().strip()
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Expected ground truth from golden_env exploration:
    # Page 1: PASS (Left=150.0, Right=155.2, Top=170.0, Bottom=348.4 — all >= 36)
    # Page 2: PASS (Left=72.0, Right=72.0, Top=40.7, Bottom=369.6 — all >= 36)
    # Page 3: FAIL (Left=10.0 < 36)
    # Page 4: FAIL (Bottom=2.6 < 36)
    # Page 5: PASS (Left=72.0, Right=83.9, Top=52.7, Bottom=87.7 — all >= 36)
    expected_verdicts = {1: 'PASS', 2: 'PASS', 3: 'FAIL', 4: 'FAIL', 5: 'PASS'}

    # Component 1: File has page-level analysis lines for all 5 pages (0.25 points)
    # Parse page lines using regex
    page_pattern = re.compile(
        r'Page\s+(\d+)\s*:\s*.*?(PASS|FAIL)',
        re.IGNORECASE
    )
    page_matches = {}
    for line in lines:
        m = page_pattern.search(line)
        if m:
            page_num = int(m.group(1))
            verdict = m.group(2).upper()
            page_matches[page_num] = {'verdict': verdict, 'line': line}

    try:
        found_pages = set(page_matches.keys())
        expected_pages = {1, 2, 3, 4, 5}
        if expected_pages.issubset(found_pages):
            print(f"PASS: Component 1 — All 5 page analysis lines found (0.25 pts)")
            total_score += 0.25
        else:
            missing = expected_pages - found_pages
            print(f"FAIL: Component 1 — Missing page lines for pages: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct PASS/FAIL classification per page (0.35 points)
    # Each correct classification earns 0.07 points (5 pages * 0.07 = 0.35)
    try:
        comp2_score = 0.0
        for page_num in range(1, 6):
            if page_num in page_matches:
                actual_verdict = page_matches[page_num]['verdict']
                expected_verdict = expected_verdicts[page_num]
                if actual_verdict == expected_verdict:
                    comp2_score += 0.07
                    print(f"PASS: Component 2 — Page {page_num} correctly classified as {actual_verdict}")
                else:
                    print(f"FAIL: Component 2 — Page {page_num} classified as {actual_verdict}, expected {expected_verdict}")
            else:
                print(f"FAIL: Component 2 — Page {page_num} not found in report")
        if comp2_score > 0:
            total_score += comp2_score
        print(f"  Component 2 subtotal: {comp2_score:.2f}/0.35")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Margin values present and reasonable (0.25 points)
    # Check that each page line contains Left, Right, Top, Bottom margin values
    margin_pattern = re.compile(
        r'Left\s*=\s*([\d.]+)\s*pt.*?Right\s*=\s*([\d.]+)\s*pt.*?Top\s*=\s*([\d.]+)\s*pt.*?Bottom\s*=\s*([\d.]+)\s*pt',
        re.IGNORECASE
    )
    # Expected approximate margins from golden (tolerance of 15pt for rounding differences)
    expected_margins = {
        1: {'left': 150.0, 'right': 155.2, 'top': 170.0, 'bottom': 348.4},
        2: {'left': 72.0, 'right': 72.0, 'top': 40.7, 'bottom': 369.6},
        3: {'left': 10.0, 'right': 232.0, 'top': 42.9, 'bottom': 449.4},
        4: {'left': 72.0, 'right': 77.6, 'top': 40.7, 'bottom': 2.6},
        5: {'left': 72.0, 'right': 83.9, 'top': 52.7, 'bottom': 87.7},
    }
    try:
        comp3_score = 0.0
        pages_with_margins = 0
        for page_num in range(1, 6):
            if page_num in page_matches:
                line = page_matches[page_num]['line']
                mm = margin_pattern.search(line)
                if mm:
                    left = float(mm.group(1))
                    right = float(mm.group(2))
                    top = float(mm.group(3))
                    bottom = float(mm.group(4))
                    exp = expected_margins[page_num]
                    # Check if values are within reasonable tolerance (20pt)
                    tolerance = 20.0
                    if (abs(left - exp['left']) < tolerance and
                        abs(right - exp['right']) < tolerance and
                        abs(top - exp['top']) < tolerance and
                        abs(bottom - exp['bottom']) < tolerance):
                        pages_with_margins += 1
                        print(f"PASS: Component 3 — Page {page_num} margins within tolerance "
                              f"(L={left}, R={right}, T={top}, B={bottom})")
                    else:
                        print(f"FAIL: Component 3 — Page {page_num} margins out of tolerance "
                              f"(L={left}, R={right}, T={top}, B={bottom}) "
                              f"expected ~(L={exp['left']}, R={exp['right']}, T={exp['top']}, B={exp['bottom']})")
                else:
                    print(f"FAIL: Component 3 — Page {page_num} missing margin values in line")
        # Award proportional score
        comp3_score = 0.05 * pages_with_margins  # 5 pages * 0.05 = 0.25
        if comp3_score > 0:
            total_score += comp3_score
        print(f"  Component 3 subtotal: {comp3_score:.2f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Summary line correct (0.15 points)
    # Expected: "3 of 5 pages have adequate print margins"
    try:
        summary_pattern = re.compile(r'(\d+)\s+of\s+(\d+)\s+pages?\s+have\s+adequate', re.IGNORECASE)
        summary_match = None
        for line in lines:
            sm = summary_pattern.search(line)
            if sm:
                summary_match = (int(sm.group(1)), int(sm.group(2)), line.strip())
                break
        if summary_match is not None:
            pass_count, total_count, matched_line = summary_match
            if pass_count == 3 and total_count == 5:
                print(f"PASS: Component 4 — Summary line correct: '{matched_line}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Summary says {pass_count} of {total_count}, expected 3 of 5")
        else:
            print(f"FAIL: Component 4 — No summary line found matching 'X of Y pages have adequate'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
