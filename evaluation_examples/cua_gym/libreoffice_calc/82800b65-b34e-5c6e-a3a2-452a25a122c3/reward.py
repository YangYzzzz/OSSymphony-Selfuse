"""
Reward Script: Verify redaction check report for a PDF
Task ID: pdf_cr_069
Domain: pdf (libreoffice_calc domain label, but actual task is PDF verification)
Scoring:
  Component 1 (0.15): redaction_check.txt exists and is non-empty
  Component 2 (0.25): Correct per-page redaction box counts (Page 1: 3, Page 2: 2, Page 3: 2)
  Component 3 (0.25): Correct CLEAN/EXPOSED classification for each region
  Component 4 (0.20): Summary with correct totals (7 total, 3 proper, 4 improper)
  Component 5 (0.15): Report structure includes header, per-page sections, and summary
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_069'
REPORT_PATH = f'{WORKDIR}/Desktop/redaction_check.txt'

# Ground truth from VM exploration:
# Page 1: 3 black rects - Box1: CLEAN, Box2: EXPOSED, Box3: CLEAN
# Page 2: 2 black rects - Box1: EXPOSED, Box2: EXPOSED
# Page 3: 2 black rects - Box1: CLEAN, Box2: EXPOSED
# Total: 7 boxes, 3 properly redacted (CLEAN), 4 improperly redacted (EXPOSED)

EXPECTED_BOX_COUNTS = {1: 3, 2: 2, 3: 2}
EXPECTED_TOTAL_BOXES = 7
EXPECTED_PROPER = 3
EXPECTED_IMPROPER = 4


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: redaction_check.txt exists and is non-empty (0.15 points)
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 1 -- {REPORT_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0  # Early exit: nothing else to check
        content = open(REPORT_PATH, 'r').read()
        if len(content.strip()) < 50:
            print(f"FAIL: Component 1 -- File exists but too short ({len(content)} chars)")
            print("REWARD: 0.0")
            return 0.0
        print(f"PASS: Component 1 -- redaction_check.txt exists, {len(content)} chars (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Correct per-page redaction box counts (0.25 points)
    # Look for patterns like "Page X: Y redaction box" (case insensitive)
    try:
        page_box_pattern = re.compile(
            r'[Pp]age\s+(\d+)\s*:\s*(\d+)\s*redaction\s*box',
            re.IGNORECASE
        )
        found_counts = {}
        for match in page_box_pattern.finditer(content):
            page_num = int(match.group(1))
            box_count = int(match.group(2))
            found_counts[page_num] = box_count

        if not found_counts:
            print(f"FAIL: Component 2 -- No page box count patterns found in report")
        else:
            # Award partial credit: per-page correctness
            pages_correct = 0
            total_pages = len(EXPECTED_BOX_COUNTS)
            for page, expected_count in EXPECTED_BOX_COUNTS.items():
                actual = found_counts.get(page)
                if actual == expected_count:
                    pages_correct += 1
                    print(f"  Page {page}: correct ({expected_count} boxes)")
                else:
                    print(f"  Page {page}: expected {expected_count} boxes, found {actual}")

            if pages_correct == total_pages:
                print(f"PASS: Component 2 -- All page box counts correct (0.25 pts)")
                total_score += 0.25
            elif pages_correct > 0:
                partial = 0.25 * (pages_correct / total_pages)
                print(f"PARTIAL: Component 2 -- {pages_correct}/{total_pages} pages correct ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- No page box counts correct")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct CLEAN/EXPOSED classification (0.25 points)
    # The report should identify which redaction areas are CLEAN vs EXPOSED
    try:
        clean_count = len(re.findall(r'CLEAN', content, re.IGNORECASE))
        exposed_count = len(re.findall(r'EXPOSED', content, re.IGNORECASE))

        # We expect exactly 3 CLEAN and 4 EXPOSED mentions in the per-box details
        # (The summary might also mention counts, but the per-box markers are key)
        comp3_score = 0.0

        # Check that CLEAN appears at least 3 times (per-box level)
        if clean_count >= EXPECTED_PROPER:
            comp3_score += 0.125
            print(f"  CLEAN mentions: {clean_count} (expected >= {EXPECTED_PROPER})")
        else:
            print(f"  CLEAN mentions: {clean_count} (expected >= {EXPECTED_PROPER}) -- insufficient")

        # Check that EXPOSED appears at least 4 times (per-box level)
        if exposed_count >= EXPECTED_IMPROPER:
            comp3_score += 0.125
            print(f"  EXPOSED mentions: {exposed_count} (expected >= {EXPECTED_IMPROPER})")
        else:
            print(f"  EXPOSED mentions: {exposed_count} (expected >= {EXPECTED_IMPROPER}) -- insufficient")

        if comp3_score > 0:
            print(f"{'PASS' if comp3_score == 0.25 else 'PARTIAL'}: Component 3 -- CLEAN/EXPOSED classification ({comp3_score:.2f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- Missing CLEAN/EXPOSED classifications")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Summary with correct totals (0.20 points)
    # Expect: total boxes = 7, properly redacted = 3, improperly redacted = 4
    try:
        comp4_score = 0.0

        # Check for total box count in summary
        total_match = re.search(
            r'[Tt]otal\s*(?:redaction\s*)?box(?:es)?\s*:\s*(\d+)',
            content
        )
        if total_match and int(total_match.group(1)) == EXPECTED_TOTAL_BOXES:
            comp4_score += 0.07
            print(f"  Total boxes: {total_match.group(1)} (correct)")
        else:
            found_val = total_match.group(1) if total_match else 'not found'
            print(f"  Total boxes: {found_val} (expected {EXPECTED_TOTAL_BOXES})")

        # Check for properly redacted count
        proper_match = re.search(
            r'[Pp]roperly\s*redacted\s*:\s*(\d+)',
            content
        )
        if proper_match and int(proper_match.group(1)) == EXPECTED_PROPER:
            comp4_score += 0.07
            print(f"  Properly redacted: {proper_match.group(1)} (correct)")
        else:
            found_val = proper_match.group(1) if proper_match else 'not found'
            print(f"  Properly redacted: {found_val} (expected {EXPECTED_PROPER})")

        # Check for improperly redacted count
        improper_match = re.search(
            r'[Ii]mproperly\s*redacted\s*:\s*(\d+)',
            content
        )
        if improper_match and int(improper_match.group(1)) == EXPECTED_IMPROPER:
            comp4_score += 0.06
            print(f"  Improperly redacted: {improper_match.group(1)} (correct)")
        else:
            found_val = improper_match.group(1) if improper_match else 'not found'
            print(f"  Improperly redacted: {found_val} (expected {EXPECTED_IMPROPER})")

        if comp4_score > 0:
            print(f"{'PASS' if comp4_score >= 0.19 else 'PARTIAL'}: Component 4 -- Summary totals ({comp4_score:.2f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 -- No correct summary totals found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Report structure (0.15 points)
    # Should have: header/title, per-page sections, summary section
    try:
        comp5_score = 0.0

        # Check for a header or title mentioning "redact"
        has_header = bool(re.search(r'[Rr]edact', content[:200]))
        if has_header:
            comp5_score += 0.05
            print(f"  Header: found reference to redaction in first 200 chars")
        else:
            print(f"  Header: no redaction reference in first 200 chars")

        # Check for per-page sections (at least 3 pages mentioned)
        page_mentions = set(re.findall(r'[Pp]age\s+(\d+)', content))
        if len(page_mentions) >= 3:
            comp5_score += 0.05
            print(f"  Per-page sections: {len(page_mentions)} pages mentioned")
        else:
            print(f"  Per-page sections: only {len(page_mentions)} pages mentioned (expected >= 3)")

        # Check for summary section
        has_summary = bool(re.search(r'[Ss]ummary', content))
        if has_summary:
            comp5_score += 0.05
            print(f"  Summary section: found")
        else:
            print(f"  Summary section: not found")

        if comp5_score > 0:
            print(f"{'PASS' if comp5_score >= 0.14 else 'PARTIAL'}: Component 5 -- Report structure ({comp5_score:.2f} pts)")
            total_score += comp5_score
        else:
            print(f"FAIL: Component 5 -- Report structure insufficient")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
