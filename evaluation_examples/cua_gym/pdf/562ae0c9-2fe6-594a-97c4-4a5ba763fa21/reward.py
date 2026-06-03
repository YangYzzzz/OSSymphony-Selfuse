"""
Reward Script: Compare two financial policy PDFs and create a comparison report
Task ID: pdf_fin_013
Domain: pdf
Scoring:
  - Component 1 (0.15): Comparison PDF exists and is a valid PDF
  - Component 2 (0.10): Report has multiple pages (>=2)
  - Component 3 (0.30): All 8 text differences are documented
  - Component 4 (0.20): Page references are included for changes
  - Component 5 (0.25): Both original and revised text excerpts present
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_013'
COMPARISON_PATH = os.path.join(WORKDIR, 'finance', 'policy_comparison.pdf')

# Key identifiers for the 8 changes (unique keywords from each change)
CHANGE_IDENTIFIERS = [
    # Change 1: Expense approval threshold ($5,000 -> $10,000)
    {"keywords": ["expense", "approval"], "v1_marker": "5,000", "v2_marker": "10,000", "page": "2"},
    # Change 2: Travel reimbursement rate ($275 -> $325)
    {"keywords": ["travel", "reimbursement"], "v1_marker": "275", "v2_marker": "325", "page": "4"},
    # Change 3: Vendor payment terms (net-60 -> net-45)
    {"keywords": ["vendor", "invoice"], "v1_marker": "net-60", "v2_marker": "net-45", "page": "5"},
    # Change 4: Internal audit frequency (biannual -> quarterly)
    {"keywords": ["audit", "frequency"], "v1_marker": "biannual", "v2_marker": "quarterly", "page": "7"},
    # Change 5: Capital expenditure authorization ($50,000 -> $25,000)
    {"keywords": ["capital", "expenditure"], "v1_marker": "50,000", "v2_marker": "25,000", "page": "9"},
    # Change 6: Financial records retention (five years -> seven years)
    {"keywords": ["records", "retention"], "v1_marker": "five year", "v2_marker": "seven year", "page": "11"},
    # Change 7: Whistleblower protection
    {"keywords": ["whistleblower"], "v1_marker": "grievance policy", "v2_marker": "Whistleblower Protection Program", "page": "13"},
    # Change 8: Non-compliance penalties
    {"keywords": ["non-compliance", "violation"], "v1_marker": "termination of employment", "v2_marker": "regulatory authorities", "page": "14"},
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Component 1: Comparison PDF exists and is valid (0.15 pts) ----
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 — Comparison PDF exists and is valid, {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot load comparison PDF: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract all text from the comparison report
    full_text = ""
    for i in range(doc.page_count):
        page = doc[i]
        full_text += page.get_text() + "\n"
    doc.close()

    full_text_lower = full_text.lower()

    # ---- Component 2: Report has multiple pages (0.10 pts) ----
    try:
        if page_count >= 2:
            print(f"PASS: Component 2 — Report has {page_count} pages (>= 2) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Report only has {page_count} page, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: All 8 text differences documented (0.30 pts) ----
    # Award partial credit: 0.30 / 8 = 0.0375 per change found
    try:
        changes_found = 0
        for idx, change in enumerate(CHANGE_IDENTIFIERS):
            # A change is "documented" if at least one keyword AND either the v1 or v2 marker is present
            keyword_found = any(kw.lower() in full_text_lower for kw in change["keywords"])
            marker_found = (
                change["v1_marker"].lower() in full_text_lower or
                change["v2_marker"].lower() in full_text_lower
            )
            if keyword_found and marker_found:
                changes_found += 1
                print(f"  Change {idx+1}: FOUND (keywords + markers present)")
            else:
                print(f"  Change {idx+1}: NOT FOUND (keyword={keyword_found}, marker={marker_found})")

        change_score = (changes_found / 8) * 0.30
        if changes_found == 8:
            print(f"PASS: Component 3 — All 8 changes documented ({change_score:.4f} pts)")
            total_score += change_score
        elif changes_found > 0:
            print(f"PARTIAL: Component 3 — {changes_found}/8 changes documented ({change_score:.4f} pts)")
            total_score += change_score
        else:
            print(f"FAIL: Component 3 — No changes documented")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: Page references included (0.20 pts) ----
    # Each change should reference its source page number
    try:
        pages_referenced = 0
        for idx, change in enumerate(CHANGE_IDENTIFIERS):
            page_num = change["page"]
            # Look for the page number near the change context
            # Patterns like "Page: 2", "Page 2", "page 2", "p. 2", "p2"
            page_patterns = [
                rf'page[:\s]*{page_num}\b',
                rf'p\.\s*{page_num}\b',
            ]
            page_ref_found = any(
                re.search(pat, full_text_lower) for pat in page_patterns
            )
            if page_ref_found:
                pages_referenced += 1

        page_score = (pages_referenced / 8) * 0.20
        if pages_referenced == 8:
            print(f"PASS: Component 4 — All 8 page references found ({page_score:.4f} pts)")
            total_score += page_score
        elif pages_referenced > 0:
            print(f"PARTIAL: Component 4 — {pages_referenced}/8 page references found ({page_score:.4f} pts)")
            total_score += page_score
        else:
            print(f"FAIL: Component 4 — No page references found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Both original and revised text present (0.25 pts) ----
    # For each change, both the v1 marker AND v2 marker should appear
    try:
        both_present_count = 0
        for idx, change in enumerate(CHANGE_IDENTIFIERS):
            v1_found = change["v1_marker"].lower() in full_text_lower
            v2_found = change["v2_marker"].lower() in full_text_lower
            if v1_found and v2_found:
                both_present_count += 1
                print(f"  Change {idx+1}: Both original and revised text present")
            else:
                print(f"  Change {idx+1}: v1={v1_found}, v2={v2_found}")

        both_score = (both_present_count / 8) * 0.25
        if both_present_count == 8:
            print(f"PASS: Component 5 — All 8 changes have both original and revised text ({both_score:.4f} pts)")
            total_score += both_score
        elif both_present_count > 0:
            print(f"PARTIAL: Component 5 — {both_present_count}/8 have both texts ({both_score:.4f} pts)")
            total_score += both_score
        else:
            print(f"FAIL: Component 5 — No changes have both original and revised text")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMPARISON_PATH):
    print(f"File not found: {COMPARISON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(COMPARISON_PATH)
