"""
Reward Script: Verify PDF digital signature extraction and report generation
Task ID: pdf_gf2_041
Domain: pdf
Scoring:
  - Component 1: Report file exists and is non-empty (0.15)
  - Component 2: Reports correct number of signature fields (3) (0.20)
  - Component 3: Lists all 3 signature field names (0.20)
  - Component 4: Reports signer names for signed fields (0.20)
  - Component 5: Reports signing dates for signed fields (0.10)
  - Component 6: Correctly identifies unsigned/empty witness field (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_041'

def verify_task():
    """
    Verify that signature_verification.txt was created with correct content.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    report_path = os.path.join(WORKDIR, 'Documents', 'signature_verification.txt')

    # Component 1: Report file exists and is non-empty (0.15 points)
    try:
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                content = f.read()
            if len(content.strip()) > 50:
                print(f"PASS: Component 1 — Report file exists and is non-empty ({len(content)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Report file exists but too short ({len(content)} chars)")
                # Can't proceed without content
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
        else:
            print(f"FAIL: Component 1 — Report file not found at {report_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    content_lower = content.lower()

    # Component 2: Reports correct number of signature fields (3) (0.20 points)
    try:
        # Check if the report mentions 3 signature fields
        found_three = False
        # Look for patterns like "3 signature", "3 fields", "Total Signature Fields Found: 3"
        patterns_three = [
            r'3\s+signature',
            r'signature.*3',
            r'total.*3',
            r'found.*3',
            r'3\s+field',
            r'field.*3',
        ]
        for pat in patterns_three:
            if re.search(pat, content_lower):
                found_three = True
                break

        # Also accept if exactly 3 distinct signature field sections are described
        if not found_three:
            # Count occurrences of field/signature section headers
            field_sections = re.findall(r'(?:signature\s+field|field\s*#?\s*\d)', content_lower)
            if len(field_sections) >= 3:
                found_three = True

        if found_three:
            print(f"PASS: Component 2 — Report mentions 3 signature fields (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Report does not clearly indicate 3 signature fields")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Lists all 3 signature field names (0.20 points)
    try:
        field_names = ['signature_client', 'signature_consultant', 'signature_witness']
        found_fields = []
        for fname in field_names:
            if fname in content_lower or fname.replace('_', ' ') in content_lower:
                found_fields.append(fname)

        if len(found_fields) == 3:
            print(f"PASS: Component 3 — All 3 field names found: {found_fields} (0.20 pts)")
            total_score += 0.20
        elif len(found_fields) >= 2:
            partial = round(0.20 * len(found_fields) / 3, 2)
            print(f"PARTIAL: Component 3 — {len(found_fields)}/3 field names found: {found_fields} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(found_fields)}/3 field names found: {found_fields}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Reports signer names for signed fields (0.20 points)
    try:
        signers = ['harrington', 'nakamura']
        found_signers = []
        for signer in signers:
            if signer in content_lower:
                found_signers.append(signer)

        if len(found_signers) == 2:
            print(f"PASS: Component 4 — Both signer names found: {found_signers} (0.20 pts)")
            total_score += 0.20
        elif len(found_signers) == 1:
            print(f"PARTIAL: Component 4 — 1/2 signer names found: {found_signers} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No signer names found (expected Harrington and Nakamura)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Reports signing dates for signed fields (0.10 points)
    try:
        # Look for date patterns like 2025-03-15 or March 15, 2025 etc.
        date_patterns = [
            r'2025[-/.]03[-/.]15',
            r'march\s+15.*2025',
            r'2025.*march.*15',
            r'15[-/.]03[-/.]2025',
            r'03[-/.]15[-/.]2025',
        ]
        found_dates = False
        for pat in date_patterns:
            matches = re.findall(pat, content_lower)
            if len(matches) >= 1:
                found_dates = True
                break

        if found_dates:
            print(f"PASS: Component 5 — Signing date(s) found in report (0.10 pts)")
            total_score += 0.10
        else:
            # Also accept any date mention as partial credit
            any_date = re.search(r'\d{4}[-/.]\d{2}[-/.]\d{2}', content)
            if any_date:
                print(f"PARTIAL: Component 5 — Some date found ({any_date.group()}) but not expected 2025-03-15 (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — No signing dates found in report")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Correctly identifies unsigned/empty witness field (0.15 points)
    try:
        # The witness field should be identified as empty/unsigned
        witness_mentioned = 'witness' in content_lower
        unsigned_indicators = ['unsigned', 'empty', 'not signed', 'n/a', 'none', 'no signature']
        has_unsigned = any(ind in content_lower for ind in unsigned_indicators)

        if witness_mentioned and has_unsigned:
            print(f"PASS: Component 6 — Witness field correctly identified as unsigned/empty (0.15 pts)")
            total_score += 0.15
        elif witness_mentioned:
            print(f"PARTIAL: Component 6 — Witness mentioned but unsigned status not clear (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — Witness field unsigned status not reported")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {round(final_score, 2)}")
    return final_score


# Entry point
verify_task()
