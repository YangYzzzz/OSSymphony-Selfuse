"""
Reward Script: Detect multilingual text in a PDF and write a language report
Task ID: pdf_cr_075
Domain: pdf
Scoring:
  - Component 1 (0.15): Report file exists with correct header referencing bilingual.pdf
  - Component 2 (0.20): Per-page analysis section with correct page count (4 pages)
  - Component 3 (0.30): Scripts correctly detected per page (CJK on pages 1-4, Latin on pages 1-4)
  - Component 4 (0.20): Summary lists all detected scripts (must include CJK and Latin)
  - Component 5 (0.15): Primary script identified as Latin with a percentage
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_075'
REPORT_PATH = os.path.join(WORKDIR, 'Desktop', 'language_report.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: report file must exist
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found at {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(REPORT_PATH, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()
    lines = content.strip().split('\n')

    # Component 1: Report has header referencing bilingual.pdf (0.15 pts)
    # The report should reference the source PDF file
    try:
        if 'bilingual.pdf' in content:
            print(f"PASS: Component 1 -- Report references bilingual.pdf (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Report does not reference bilingual.pdf")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Per-page analysis with correct page count of 4 (0.20 pts)
    # The report must contain per-page breakdown and mention 4 pages
    try:
        # Check for page references - must have Page 1 through Page 4
        page_refs = set()
        for match in re.finditer(r'page\s+(\d+)', content_lower):
            page_refs.add(int(match.group(1)))

        has_pages_1_to_4 = {1, 2, 3, 4}.issubset(page_refs)
        # Also check that total pages is mentioned as 4
        has_total_4 = bool(re.search(r'(total\s+pages|pages)\s*[:\s]*4', content_lower))

        if has_pages_1_to_4 and has_total_4:
            print(f"PASS: Component 2 -- Per-page analysis for 4 pages found (0.20 pts)")
            total_score += 0.20
        elif has_pages_1_to_4:
            print(f"PARTIAL: Component 2 -- Pages 1-4 referenced but total not stated (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Missing per-page analysis. Found page refs: {page_refs}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct scripts detected per page (0.30 pts)
    # Golden truth: CJK on all 4 pages, Latin on all 4 pages
    # Each correctly detected page-script pair earns partial credit
    try:
        # We check that the report identifies both CJK and Latin for pages 1-4
        cjk_pages = set()
        latin_pages = set()
        for line in lines:
            line_lower = line.lower()
            page_match = re.search(r'page\s+(\d+)', line_lower)
            if page_match:
                page_num = int(page_match.group(1))
                if 'cjk' in line_lower:
                    cjk_pages.add(page_num)
                if 'latin' in line_lower:
                    latin_pages.add(page_num)

        # CJK should be on pages 1-4, Latin on pages 1-4
        expected_cjk = {1, 2, 3, 4}
        expected_latin = {1, 2, 3, 4}

        cjk_correct = len(expected_cjk.intersection(cjk_pages))
        latin_correct = len(expected_latin.intersection(latin_pages))
        total_correct = cjk_correct + latin_correct  # out of 8

        # Score proportionally: 0.30 * (correct / 8)
        comp3_score = round(0.30 * (total_correct / 8), 4)
        if comp3_score > 0:
            print(f"PASS: Component 3 -- {total_correct}/8 page-script pairs correct ({comp3_score} pts)")
            print(f"  CJK pages detected: {sorted(cjk_pages)}, Latin pages detected: {sorted(latin_pages)}")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- No correct page-script pairs found")
            print(f"  CJK pages: {sorted(cjk_pages)}, Latin pages: {sorted(latin_pages)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Summary lists detected scripts including CJK and Latin (0.20 pts)
    # The summary section should list all scripts found
    try:
        # Find the summary section and check if it lists both CJK and Latin
        summary_idx = -1
        for idx, line in enumerate(lines):
            if 'summary' in line.lower() or 'scripts detected' in line.lower():
                summary_idx = idx
                break

        # Check lines from summary onward for both CJK and Latin mention
        summary_text = '\n'.join(lines[summary_idx:]).lower() if summary_idx >= 0 else ''
        scripts_in_summary = ('cjk' in summary_text and 'latin' in summary_text)

        # Fallback: check if "scripts detected" line anywhere lists both
        if not scripts_in_summary:
            scripts_in_summary = bool(
                re.search(r'scripts?\s+detected.*cjk', content_lower) and
                re.search(r'scripts?\s+detected.*latin', content_lower)
            ) or bool(
                re.search(r'scripts?\s+detected.*latin.*cjk', content_lower)
            )

        if scripts_in_summary:
            print(f"PASS: Component 4 -- Summary lists CJK and Latin as detected scripts (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Summary missing or does not list both CJK and Latin")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Primary script identified as Latin with percentage (0.15 pts)
    # Golden truth: "Primary script: Latin (94%)" or similar
    try:
        primary_match = re.search(r'primary\s+script\s*[:\s]+latin', content_lower)
        has_percentage = bool(re.search(r'primary\s+script.*\d+\s*%', content_lower))

        if primary_match and has_percentage:
            print(f"PASS: Component 5 -- Primary script is Latin with percentage (0.15 pts)")
            total_score += 0.15
        elif primary_match:
            print(f"PARTIAL: Component 5 -- Primary script is Latin but no percentage (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 -- Primary script not identified as Latin")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
