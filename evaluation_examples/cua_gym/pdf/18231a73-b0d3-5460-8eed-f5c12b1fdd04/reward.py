"""
Reward Script: Contract comparison report generation
Task ID: pdf_legal_023
Domain: pdf
Scoring:
  - Component 1 (0.10): Report file exists at correct path
  - Component 2 (0.10): Valid PDF with reasonable page count
  - Component 3 (0.10): Report header/title references contract comparison
  - Component 4 (0.15): Report states 12 total differences found
  - Component 5 (0.30): Report contains specific differences with old/new text (progressive)
  - Component 6 (0.15): Report includes page number references for differences
  - Component 7 (0.10): Report mentions new Section 17 (Audit Rights) in V2
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_023'
REPORT_PATH = os.path.join(WORKDIR, 'legal', 'contract_comparison_report.pdf')

# Key differences that should appear in the report (keywords from old->new changes)
EXPECTED_DIFFERENCES = [
    ("March 15, 2025", "April 1, 2025"),          # Diff 1: Effective date
    ("one (1) Business Day", "two (2) Business Day"),  # Diff 2: Response time
    ("thirty (30) days", "forty-five (45) days"),  # Diff 3: Payment terms
    ("1.5%", "1.0%"),                              # Diff 4: Late payment interest
    ("three (3) years", "two (2) years"),           # Diff 5: Initial term
    ("sixty (60) days", "forty-five (45) days"),    # Diff 6: Termination notice
    ("ninety (90) days", "one hundred twenty (120) days"),  # Diff 7: Warranty period
    ("2,000,000", "3,000,000"),                    # Diff 8: General liability
    ("3,000,000", "5,000,000"),                    # Diff 9: Cyber liability (per claim)
    ("seventy-two (72) hours", "forty-eight (48) hours"),  # Diff 10: Data breach notification
    ("ninety (90) consecutive days", "sixty (60) consecutive days"),  # Diff 11: Force majeure
    ("twelve (12) months", "eighteen (18) months"),  # Diff 12: Non-solicitation
]


def verify_task(report_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Report file exists (0.10 points)
    # This is a task-introduced change: file does NOT exist in initial_env
    try:
        if os.path.exists(report_path) and os.path.getsize(report_path) > 100:
            print(f"PASS: Component 1 — Report file exists at {report_path} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Report file not found or empty at {report_path}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        import fitz
        doc = fitz.open(report_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {report_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the report
    full_text = ""
    for i in range(doc.page_count):
        full_text += doc[i].get_text() + "\n"
    full_text_lower = full_text.lower()
    doc.close()

    # Component 2: Valid PDF with reasonable page count (0.10 points)
    try:
        doc_check = fitz.open(report_path)
        page_count = doc_check.page_count
        doc_check.close()
        if page_count >= 2:
            print(f"PASS: Component 2 — Valid PDF with {page_count} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — PDF has only {page_count} page(s), expected at least 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Report title/header references contract comparison (0.10 points)
    try:
        if ("comparison" in full_text_lower or "compare" in full_text_lower or "diff" in full_text_lower) and \
           ("contract" in full_text_lower):
            print(f"PASS: Component 3 — Report references contract comparison (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Report does not mention contract comparison")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Report states 12 total differences (0.15 points)
    try:
        # Look for "12" near "difference" or "change"
        has_12_count = bool(re.search(r'12\s*(total\s*)?(difference|change|modification)', full_text_lower))
        has_total_12 = bool(re.search(r'total\s*(difference|change|modification)s?\s*(\w+\s*)?:?\s*12', full_text_lower))
        if has_12_count or has_total_12:
            print(f"PASS: Component 4 — Report mentions 12 differences (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Could not find reference to 12 differences in report")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Report contains specific differences with old/new text (0.30 points, progressive)
    try:
        diffs_found = 0
        for i, (old_text, new_text) in enumerate(EXPECTED_DIFFERENCES):
            old_found = old_text.lower() in full_text_lower
            new_found = new_text.lower() in full_text_lower
            if old_found and new_found:
                diffs_found += 1

        # Progressive scoring: 0.30 * (diffs_found / 12), need at least 6 for any credit
        if diffs_found >= 6:
            pts = round(0.30 * (diffs_found / 12), 4)
            print(f"PASS: Component 5 — Found {diffs_found}/12 specific differences ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 5 — Only found {diffs_found}/12 specific differences (need >= 6)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Report includes page number references (0.15 points)
    try:
        # Look for patterns like "page 2", "page: 3", "Page 4", etc.
        page_refs = re.findall(r'page\s*:?\s*\d+', full_text_lower)
        if len(page_refs) >= 4:
            print(f"PASS: Component 6 — Found {len(page_refs)} page number references (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Found only {len(page_refs)} page references, expected >= 4")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Report mentions new Section 17 (Audit Rights) (0.10 points)
    try:
        has_audit = "audit" in full_text_lower
        has_section_17 = "section 17" in full_text_lower or "17" in full_text_lower
        has_new_section = "new" in full_text_lower or "additional" in full_text_lower or "added" in full_text_lower
        if has_audit and (has_section_17 or has_new_section):
            print(f"PASS: Component 7 — Report mentions Audit Rights / Section 17 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Missing reference to new Audit Rights section")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(REPORT_PATH)
