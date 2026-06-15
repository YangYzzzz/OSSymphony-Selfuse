"""
Reward Script: Check text formatting consistency in style_guide.pdf and verify style_check.txt
Task ID: pdf_cr_067
Domain: pdf (libreoffice_calc listed but task is PDF analysis)
Scoring:
  Component 1 (0.20): style_check.txt exists and is non-empty
  Component 2 (0.25): Heading font correctly identified (Helvetica-Bold, ~18pt)
  Component 3 (0.25): Body font correctly identified (Helvetica, ~11pt)
  Component 4 (0.30): Inconsistencies section lists real formatting deviations
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_067'
REPORT_PATH = os.path.join(WORKDIR, 'Desktop', 'style_check.txt')
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'style_guide.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist (not scored — it exists in both envs)
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: style_check.txt exists and is non-empty (0.20 points)
    # This file does NOT exist in initial_env, only in golden_env
    try:
        if os.path.exists(REPORT_PATH):
            content = open(REPORT_PATH, 'r').read()
            if len(content.strip()) > 20:
                print(f"PASS: Component 1 — style_check.txt exists and has {len(content)} chars (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — style_check.txt exists but too short ({len(content)} chars)")
        else:
            print(f"FAIL: Component 1 — style_check.txt does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If file doesn't exist, no further checks can pass
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the report content for further checks
    try:
        content = open(REPORT_PATH, 'r').read()
        content_lower = content.lower()
    except Exception as e:
        print(f"ERROR: Cannot read style_check.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Heading font correctly identified (0.25 points)
    # The golden report says: "Heading font: Helvetica-Bold, size: 18.0pt"
    # We check that the report identifies the heading font as some variant of Helvetica-Bold
    # and the size as approximately 18pt
    try:
        heading_found = False
        # Look for heading font identification line
        heading_pattern = re.search(
            r'heading\s+font[:\s]+([^\n,]+)',
            content, re.IGNORECASE
        )
        if heading_pattern:
            heading_info = heading_pattern.group(1).strip()
            # Check for Helvetica-Bold (or helv bold variant)
            has_helv_bold = bool(re.search(r'helvetica[\s\-_]*bold', heading_info, re.IGNORECASE))
            # Check for size ~18
            size_match = re.search(r'(\d+\.?\d*)\s*pt', content[heading_pattern.start():heading_pattern.start()+200], re.IGNORECASE)
            has_size_18 = False
            if size_match:
                size_val = float(size_match.group(1))
                has_size_18 = abs(size_val - 18.0) < 1.0

            if has_helv_bold and has_size_18:
                print(f"PASS: Component 2 — Heading font identified as Helvetica-Bold ~18pt (0.25 pts)")
                total_score += 0.25
                heading_found = True
            elif has_helv_bold:
                print(f"PARTIAL: Component 2 — Helvetica-Bold found but size not ~18pt (0.10 pts)")
                total_score += 0.10
                heading_found = True
            elif has_size_18:
                print(f"PARTIAL: Component 2 — Size ~18pt found but not Helvetica-Bold (0.10 pts)")
                total_score += 0.10
                heading_found = True

        if not heading_found:
            print(f"FAIL: Component 2 — Heading font not properly identified in report")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Body font correctly identified (0.25 points)
    # The golden report says: "Body font: Helvetica, size: 11.0pt"
    try:
        body_found = False
        body_pattern = re.search(
            r'body\s+font[:\s]+([^\n,]+)',
            content, re.IGNORECASE
        )
        if body_pattern:
            body_info = body_pattern.group(1).strip()
            # Check for Helvetica (but not Helvetica-Bold specifically)
            has_helv = bool(re.search(r'helvetica', body_info, re.IGNORECASE))
            # Check for size ~11
            size_match = re.search(r'(\d+\.?\d*)\s*pt', content[body_pattern.start():body_pattern.start()+200], re.IGNORECASE)
            has_size_11 = False
            if size_match:
                size_val = float(size_match.group(1))
                has_size_11 = abs(size_val - 11.0) < 1.0

            if has_helv and has_size_11:
                print(f"PASS: Component 3 — Body font identified as Helvetica ~11pt (0.25 pts)")
                total_score += 0.25
                body_found = True
            elif has_helv:
                print(f"PARTIAL: Component 3 — Helvetica found but size not ~11pt (0.10 pts)")
                total_score += 0.10
                body_found = True
            elif has_size_11:
                print(f"PARTIAL: Component 3 — Size ~11pt found but not Helvetica (0.10 pts)")
                total_score += 0.10
                body_found = True

        if not body_found:
            print(f"FAIL: Component 3 — Body font not properly identified in report")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Inconsistencies section with real formatting deviations (0.30 points)
    # The golden report lists:
    #   - Heading font mismatches (Times-Bold on pages 2, 3)
    #   - Body font mismatches (Courier on pages 2, 4)
    #   - Body size mismatches (13pt on page 3)
    # We award partial credit for identifying each category of inconsistency
    try:
        inconsistency_score = 0.0

        # Check that an "Inconsistencies" section exists
        has_inconsistencies_section = bool(re.search(
            r'inconsisten(cy|cies|t)', content, re.IGNORECASE
        ))

        if has_inconsistencies_section:
            # Sub-check 4a: Heading font inconsistencies mentioned (Times-Bold or wrong heading font)
            has_heading_issues = bool(re.search(
                r'(times|heading).*(inconsist|instead|mismatch|deviat|wrong|differ|unexpected)',
                content, re.IGNORECASE
            )) or bool(re.search(
                r'(inconsist|instead|mismatch|deviat|wrong|differ|unexpected).*(heading|times)',
                content, re.IGNORECASE
            ))
            if has_heading_issues:
                inconsistency_score += 0.10
                print(f"  Sub-check 4a: Heading inconsistencies reported (+0.10)")

            # Sub-check 4b: Body font inconsistencies mentioned (Courier or wrong body font)
            has_body_font_issues = bool(re.search(
                r'(courier|body\s+text).*(inconsist|instead|mismatch|deviat|wrong|differ|unexpected)',
                content, re.IGNORECASE
            )) or bool(re.search(
                r'(inconsist|instead|mismatch|deviat|wrong|differ|unexpected).*(courier|body\s+text)',
                content, re.IGNORECASE
            ))
            if has_body_font_issues:
                inconsistency_score += 0.10
                print(f"  Sub-check 4b: Body font inconsistencies reported (+0.10)")

            # Sub-check 4c: Body size inconsistencies mentioned (13pt or size deviation)
            has_size_issues = bool(re.search(
                r'(13\.?0?\s*pt|size).*(inconsist|instead|mismatch|deviat|wrong|differ|unexpected)',
                content, re.IGNORECASE
            )) or bool(re.search(
                r'(inconsist|instead|mismatch|deviat|wrong|differ|unexpected).*(13\.?0?\s*pt|size)',
                content, re.IGNORECASE
            ))
            if has_size_issues:
                inconsistency_score += 0.10
                print(f"  Sub-check 4c: Body size inconsistencies reported (+0.10)")

            if inconsistency_score > 0:
                print(f"PASS: Component 4 — Inconsistencies section with {inconsistency_score:.2f} sub-score ({inconsistency_score:.2f} pts)")
                total_score += inconsistency_score
            else:
                print(f"FAIL: Component 4 — Inconsistencies section exists but no specific issues identified")
        else:
            print(f"FAIL: Component 4 — No inconsistencies section found in report")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
