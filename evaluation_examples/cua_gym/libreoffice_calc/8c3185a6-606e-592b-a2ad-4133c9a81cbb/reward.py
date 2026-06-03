"""
Reward Script: Extract Product Roadmap section from PDF and save as Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_007
Domain: multi_apps (Chrome + PDF)
Scoring:
  Component 1: product_roadmap_extract file exists in /home/user/strategy_docs/ (0.40 pts)
  Component 2: File contains the Product Roadmap section heading (0.30 pts)
  Component 3: File contains substantive Product Roadmap content (key sections/KPIs) (0.30 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_007'

# Expected output location (Google Drive /strategy_docs folder modeled as local directory)
STRATEGY_DOCS_DIR = os.path.join(WORKDIR, 'strategy_docs')
EXTRACT_FILE = os.path.join(STRATEGY_DOCS_DIR, 'product_roadmap_extract')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: product_roadmap_extract file exists in /home/user/strategy_docs/ (0.40 points)
    # This checks the primary task deliverable — file must exist in the correct location with content.
    try:
        folder_exists = os.path.isdir(STRATEGY_DOCS_DIR)
        file_exists = os.path.isfile(EXTRACT_FILE)
        file_nonempty = file_exists and os.path.getsize(EXTRACT_FILE) > 0

        if not folder_exists:
            print(f"FAIL: Component 1 — strategy_docs directory not found at {STRATEGY_DOCS_DIR}")
        elif not file_exists:
            print(f"FAIL: Component 1 — product_roadmap_extract not found in {STRATEGY_DOCS_DIR}")
            print(f"  INFO: strategy_docs contains: {os.listdir(STRATEGY_DOCS_DIR)}")
        elif not file_nonempty:
            print(f"FAIL: Component 1 — product_roadmap_extract exists but is empty")
        elif file_nonempty:
            file_size = os.path.getsize(EXTRACT_FILE)
            print(f"PASS: Component 1 — product_roadmap_extract exists in strategy_docs ({file_size} bytes) (+0.40 pts)")
            total_score += 0.40
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains the Product Roadmap section heading (0.30 points)
    # The extracted document should start with or clearly contain the "Product Roadmap" section header.
    try:
        if not os.path.isfile(EXTRACT_FILE):
            print(f"FAIL: Component 2 — file not found, cannot check section heading")
        else:
            with open(EXTRACT_FILE, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Check for Product Roadmap section heading (case-insensitive)
            content_lower = content.lower()
            has_heading = 'product roadmap' in content_lower

            if not has_heading:
                print(f"FAIL: Component 2 — 'Product Roadmap' heading not found in file content")
                print(f"  INFO: File starts with: {content[:200]!r}")
            elif has_heading:
                # Also note if the file contains unrelated sections from the PDF
                unrelated = [s for s in ['market analysis', 'financial projections', 'executive summary']
                             if s in content_lower]
                extra_note = f" (note: also contains {unrelated})" if unrelated else " (section appears isolated)"
                print(f"PASS: Component 2 — Product Roadmap heading found{extra_note} (+0.30 pts)")
                total_score += 0.30
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File contains substantive Product Roadmap content (0.30 points)
    # The extracted section should include key sub-sections from the Product Roadmap:
    # Q1-Q2 2025, Q3-Q4 2025, 2026, 2027, Vision Statement, Key Product Metrics/KPIs, etc.
    try:
        if not os.path.isfile(EXTRACT_FILE):
            print(f"FAIL: Component 3 — file not found, cannot check content")
        else:
            with open(EXTRACT_FILE, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            content_lower = content.lower()

            # Key content markers that should be present in the Product Roadmap section
            content_checks = {
                'vision_statement': 'vision statement' in content_lower or 'vision:' in content_lower,
                'quarterly_phases': ('q1' in content_lower or 'q1-q2' in content_lower) and '2025' in content,
                'year_2026': '2026' in content,
                'year_2027': '2027' in content,
                'product_metrics': (
                    'metrics' in content_lower or 'kpi' in content_lower or
                    'success criteria' in content_lower or 'nps' in content_lower or
                    'net promoter' in content_lower
                ),
            }

            passed_checks = [k for k, v in content_checks.items() if v]
            failed_checks = [k for k, v in content_checks.items() if not v]
            # Need at least 3 of 5 key content markers to qualify
            sufficient_content = len(passed_checks) >= 3

            if sufficient_content:
                print(f"PASS: Component 3 — Substantive Product Roadmap content present "
                      f"({len(passed_checks)}/{len(content_checks)} checks passed: {passed_checks}) (+0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Insufficient Product Roadmap content "
                      f"({len(passed_checks)}/{len(content_checks)} checks passed)")
                print(f"  Passed: {passed_checks}")
                print(f"  Failed: {failed_checks}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the task
verify_task()
