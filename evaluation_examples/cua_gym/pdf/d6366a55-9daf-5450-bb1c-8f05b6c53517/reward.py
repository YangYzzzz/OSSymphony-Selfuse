"""
Reward Script: Extract tables from financial.pdf to extracted_tables.txt
Task ID: pdf_cr_051
Domain: pdf
Scoring:
  - Component 1 (0.15): extracted_tables.txt exists
  - Component 2 (0.25): Contains page header markers for pages with tables (1, 3, 5)
  - Component 3 (0.20): Rows use pipe-delimited format
  - Component 4 (0.15): Page 1 table contains expected financial division data
  - Component 5 (0.15): Page 3 table contains expected expense category data
  - Component 6 (0.10): Page 5 table contains expected KPI metric data
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_051'
OUTPUT_FILE = os.path.join(WORKDIR, 'Desktop', 'extracted_tables.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (this IS a task-introduced change since
    # extracted_tables.txt does not exist in initial_env)
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(OUTPUT_FILE, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: Output file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File exists and is non-empty (0.15 points)
    # This fails on initial_env (file doesn't exist) and passes on golden_env
    if len(content.strip()) > 0:
        print(f"PASS: Component 1 — extracted_tables.txt exists and is non-empty ({len(content)} chars) (0.15 pts)")
        total_score += 0.15
    else:
        print(f"FAIL: Component 1 — file is empty")

    # Component 2: Contains page header markers for the correct pages (0.25 points)
    # The PDF has tables on pages 1, 3, and 5. Headers should be like "=== Table from Page X ==="
    try:
        # Look for page header pattern
        page_headers = re.findall(r'===\s*Table from Page (\d+)\s*===', content, re.IGNORECASE)
        page_numbers = sorted([int(p) for p in page_headers])
        expected_pages = [1, 3, 5]

        if not page_headers:
            # Try alternative patterns
            page_headers_alt = re.findall(r'(?:Table|Page)\s*(?:from\s+)?(?:Page\s+)?(\d+)', content, re.IGNORECASE)
            if page_headers_alt:
                print(f"FAIL: Component 2 — Found page references but not in expected '=== Table from Page X ===' format")
            else:
                print(f"FAIL: Component 2 — No page header markers found")
        else:
            # Check how many expected pages are present
            matched_pages = [p for p in expected_pages if p in page_numbers]
            if len(matched_pages) == len(expected_pages):
                print(f"PASS: Component 2 — All 3 expected page headers found: pages {page_numbers} (0.25 pts)")
                total_score += 0.25
            elif len(matched_pages) >= 2:
                partial = 0.15
                print(f"PARTIAL: Component 2 — {len(matched_pages)}/3 page headers found: {page_numbers} ({partial} pts)")
                total_score += partial
            elif len(matched_pages) >= 1:
                partial = 0.08
                print(f"PARTIAL: Component 2 — {len(matched_pages)}/3 page headers found: {page_numbers} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Page headers found for {page_numbers} but expected {expected_pages}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rows use pipe-delimited format (0.20 points)
    # Lines should contain "|" as cell separator
    try:
        lines = [l.strip() for l in content.strip().split('\n') if l.strip()]
        # Filter out header lines (=== ... ===) and blank lines
        data_lines = [l for l in lines if not l.startswith('===') and '|' in l]

        if len(data_lines) >= 15:
            # Golden has ~23 data rows (5 + header for table 1, 8 + header for table 2, 9 + header for table 3)
            print(f"PASS: Component 3 — {len(data_lines)} pipe-delimited data rows found (0.20 pts)")
            total_score += 0.20
        elif len(data_lines) >= 8:
            partial = 0.12
            print(f"PARTIAL: Component 3 — {len(data_lines)} pipe-delimited rows (expected >=15) ({partial} pts)")
            total_score += partial
        elif len(data_lines) >= 3:
            partial = 0.06
            print(f"PARTIAL: Component 3 — {len(data_lines)} pipe-delimited rows (expected >=15) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(data_lines)} pipe-delimited data rows found (expected >=15)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 1 table contains financial division data (0.15 points)
    # Expected: division names like "Technology Solutions", "Advisory Services", revenue columns
    try:
        content_lower = content.lower()
        page1_keywords = ['technology solutions', 'advisory services', 'wealth management',
                          'capital markets', 'insurance products']
        found_kw = [kw for kw in page1_keywords if kw in content_lower]

        if len(found_kw) >= 4:
            print(f"PASS: Component 4 — Page 1 table: {len(found_kw)}/5 division names found (0.15 pts)")
            total_score += 0.15
        elif len(found_kw) >= 2:
            partial = 0.08
            print(f"PARTIAL: Component 4 — Page 1 table: {len(found_kw)}/5 division names found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Page 1 table: only {len(found_kw)}/5 division names found: {found_kw}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 3 table contains expense category data (0.15 points)
    # Expected: "Personnel & Compensation", "Technology Infrastructure", etc.
    try:
        page3_keywords = ['personnel', 'technology infrastructure', 'office',
                          'professional services', 'marketing', 'regulatory']
        found_kw3 = [kw for kw in page3_keywords if kw in content_lower]

        if len(found_kw3) >= 5:
            print(f"PASS: Component 5 — Page 3 table: {len(found_kw3)}/6 expense categories found (0.15 pts)")
            total_score += 0.15
        elif len(found_kw3) >= 3:
            partial = 0.08
            print(f"PARTIAL: Component 5 — Page 3 table: {len(found_kw3)}/6 expense categories found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Page 3 table: only {len(found_kw3)}/6 expense categories found: {found_kw3}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Page 5 table contains KPI metric data (0.10 points)
    # Expected: "Revenue Growth", "Operating Margin", "Client Retention", etc.
    try:
        page5_keywords = ['revenue growth', 'operating margin', 'client retention',
                          'employee satisfaction', 'net promoter', 'digital adoption']
        found_kw5 = [kw for kw in page5_keywords if kw in content_lower]

        if len(found_kw5) >= 4:
            print(f"PASS: Component 6 — Page 5 table: {len(found_kw5)}/6 KPI metrics found (0.10 pts)")
            total_score += 0.10
        elif len(found_kw5) >= 2:
            partial = 0.05
            print(f"PARTIAL: Component 6 — Page 5 table: {len(found_kw5)}/6 KPI metrics found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — Page 5 table: only {len(found_kw5)}/6 KPI metrics found: {found_kw5}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
