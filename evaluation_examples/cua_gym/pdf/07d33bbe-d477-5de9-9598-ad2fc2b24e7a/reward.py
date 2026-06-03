"""
Reward Script: Contract Diff Report Generation
Task ID: pdf_pw_015
Domain: pdf
Scoring:
  Component 1 (0.15): Diff report PDF exists and is readable
  Component 2 (0.25): Report documents at least 8 differences
  Component 3 (0.30): Report references all correct page numbers (2, 4, 5, 7, 9)
  Component 4 (0.30): Report contains specific known change text pairs
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_015'
REPORT_PATH = os.path.join(WORKDIR, 'legal', 'contract_diff_report.pdf')

# Known changes from the task context (ground truth)
EXPECTED_PAGE_NUMBERS = {2, 4, 5, 7, 9}

# Key text fragments that should appear in the diff report for each change
# Each tuple: (original_fragment, modified_fragment)
KNOWN_CHANGES = [
    ("Amazon Web Services", "Microsoft Azure"),
    ("eight (8) qualified engineers", "twelve (12) qualified engineers"),
    ("three (3) years", "five (5) years"),
    ("TLS 1.2", "TLS 1.3"),
    ("$5,000,000", "$10,000,000"),
    ("twelve (12) month period", "twenty-four (24) month period"),
    ("fifteen (15) business days", "ten (10) business days"),
    ("failure of third-party telecommunications.", "failure of third-party telecommunications or power"),
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: report file must exist and be a valid PDF
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Diff report not found at {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(REPORT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {REPORT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the report
    full_text = ""
    try:
        for page in doc:
            full_text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from report: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    full_text_lower = full_text.lower()

    # Component 1: Report PDF exists and has content (0.15 points)
    # This checks that the file is not just empty/blank but actually has report content
    try:
        if len(full_text.strip()) > 100 and doc.page_count >= 1:
            print(f"PASS: Component 1 -- Report PDF exists with {doc.page_count} pages, {len(full_text)} chars (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Report has insufficient content: {len(full_text)} chars, {doc.page_count} pages")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Report documents at least 8 differences (0.25 points)
    # Count how many of the known change pairs are documented
    try:
        changes_documented = 0
        for orig_frag, mod_frag in KNOWN_CHANGES:
            orig_found = orig_frag.lower() in full_text_lower
            mod_found = mod_frag.lower() in full_text_lower
            if orig_found and mod_found:
                changes_documented += 1

        if changes_documented >= 8:
            print(f"PASS: Component 2 -- All 8 differences documented ({changes_documented}/8) (0.25 pts)")
            total_score += 0.25
        elif changes_documented >= 6:
            partial = 0.25 * (changes_documented / 8)
            print(f"PARTIAL: Component 2 -- {changes_documented}/8 differences documented ({partial:.2f} pts)")
            total_score += partial
        elif changes_documented >= 4:
            partial = 0.25 * (changes_documented / 8)
            print(f"PARTIAL: Component 2 -- {changes_documented}/8 differences documented ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Only {changes_documented}/8 differences documented")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Report references all correct page numbers (0.30 points)
    # The report should mention pages 2, 4, 5, 7, and 9
    try:
        pages_found = set()
        for pn in EXPECTED_PAGE_NUMBERS:
            # Look for references like "Page 2", "page 2", "Page: 2", etc.
            import re
            pattern = rf'\bpage\s*:?\s*{pn}\b'
            if re.search(pattern, full_text_lower):
                pages_found.add(pn)

        if pages_found == EXPECTED_PAGE_NUMBERS:
            print(f"PASS: Component 3 -- All 5 page numbers referenced: {sorted(pages_found)} (0.30 pts)")
            total_score += 0.30
        elif len(pages_found) >= 3:
            partial = 0.30 * (len(pages_found) / len(EXPECTED_PAGE_NUMBERS))
            missing = EXPECTED_PAGE_NUMBERS - pages_found
            print(f"PARTIAL: Component 3 -- {len(pages_found)}/5 page numbers found, missing: {sorted(missing)} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Only {len(pages_found)}/5 page numbers found: {sorted(pages_found)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Report contains specific original/modified text pairs (0.30 points)
    # Each change should have both original and modified text identifiable
    try:
        verified_pairs = 0
        for i, (orig_frag, mod_frag) in enumerate(KNOWN_CHANGES):
            orig_present = orig_frag.lower() in full_text_lower
            mod_present = mod_frag.lower() in full_text_lower
            if orig_present and mod_present:
                verified_pairs += 1
                print(f"  Change {i+1}: FOUND -- '{orig_frag[:40]}' -> '{mod_frag[:40]}'")
            else:
                print(f"  Change {i+1}: MISSING -- orig={'found' if orig_present else 'NOT found'}, mod={'found' if mod_present else 'NOT found'}")

        if verified_pairs >= 8:
            print(f"PASS: Component 4 -- All 8 change text pairs verified (0.30 pts)")
            total_score += 0.30
        elif verified_pairs >= 5:
            partial = 0.30 * (verified_pairs / 8)
            print(f"PARTIAL: Component 4 -- {verified_pairs}/8 pairs verified ({partial:.2f} pts)")
            total_score += partial
        elif verified_pairs >= 3:
            partial = 0.30 * (verified_pairs / 8)
            print(f"PARTIAL: Component 4 -- {verified_pairs}/8 pairs verified ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Only {verified_pairs}/8 pairs verified")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
