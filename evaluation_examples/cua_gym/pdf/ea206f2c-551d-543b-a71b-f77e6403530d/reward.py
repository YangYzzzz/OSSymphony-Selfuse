"""
Reward Script: Extract emails from PDF, deduplicate, sort, and save as JSON array
Task ID: pdf_cross_092
Domain: pdf (cross-domain: PDF + Python scripting + JSON)
Scoring:
  Component 1: Script ~/scripts/extract_emails.py exists (0.30 pts)
  Component 2: Output ~/Documents/emails.json exists and is valid JSON array with 28-36 emails (0.35 pts)
  Component 3: Emails are alphabetically sorted with no duplicates (0.20 pts)
  Component 4: Emails contain addresses from expected domains: company.com, gmail.com, outlook.com (0.15 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_092'

SCRIPT_PATH = f'{WORKDIR}/scripts/extract_emails.py'
JSON_PATH = f'{WORKDIR}/Documents/emails.json'
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script ~/scripts/extract_emails.py exists and uses pymupdf + regex (0.30 points)
    # This FAILS on initial_env (no script) and PASSES on golden_env
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 1 — script not found: {SCRIPT_PATH}")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()

            # Check script uses pymupdf or fitz
            uses_pymupdf = ('import pymupdf' in script_content or
                            'import fitz' in script_content or
                            'fitz as pymupdf' in script_content or
                            'pymupdf as fitz' in script_content)
            # Check script uses regex
            uses_regex = ('import re' in script_content or 're.compile' in script_content or
                          're.findall' in script_content or 're.search' in script_content)
            # Check script reads the correct PDF
            reads_pdf = ('contact_list.pdf' in script_content)

            if uses_pymupdf and uses_regex and reads_pdf:
                print(f"PASS: Component 1 — script exists, uses pymupdf+regex, reads contact_list.pdf (0.30 pts)")
                total_score += 0.30
            elif uses_pymupdf or uses_regex:
                # Partial: script exists but may be incomplete
                print(f"PARTIAL: Component 1 — script exists but missing requirements: pymupdf={uses_pymupdf}, regex={uses_regex}, reads_pdf={reads_pdf} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — script exists but does not use pymupdf/fitz or regex")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ~/Documents/emails.json exists and is valid JSON array with 28-36 emails (0.35 points)
    # This FAILS on initial_env (no emails.json) and PASSES on golden_env
    emails_data = None
    try:
        if not os.path.exists(JSON_PATH):
            print(f"FAIL: Component 2 — emails.json not found: {JSON_PATH}")
        else:
            with open(JSON_PATH, 'r') as f:
                content = f.read().strip()
            try:
                emails_data = json.loads(content)
            except json.JSONDecodeError as je:
                print(f"FAIL: Component 2 — emails.json is not valid JSON: {je}")
                emails_data = None

            if emails_data is not None:
                if not isinstance(emails_data, list):
                    print(f"FAIL: Component 2 — emails.json is not a JSON array, got {type(emails_data).__name__}")
                    emails_data = None
                else:
                    num_emails = len(emails_data)
                    # Validate each item looks like an email
                    valid_email_items = [e for e in emails_data if isinstance(e, str) and EMAIL_REGEX.match(e)]
                    if 28 <= num_emails <= 36 and len(valid_email_items) == num_emails:
                        print(f"PASS: Component 2 — emails.json is valid JSON array with {num_emails} email addresses (0.35 pts)")
                        total_score += 0.35
                    elif 20 <= num_emails <= 40 and len(valid_email_items) >= int(num_emails * 0.9):
                        # Nearby count range — partial credit
                        print(f"PARTIAL: Component 2 — emails.json has {num_emails} emails (expected 28-36), {len(valid_email_items)} look like valid emails (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 2 — emails.json has {num_emails} items, {len(valid_email_items)} valid emails; "
                              f"expected 28-36 email addresses")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Emails are alphabetically sorted with no duplicates (0.20 points)
    # This FAILS on initial_env (no emails.json) and PASSES on golden_env
    try:
        if emails_data is None:
            print(f"FAIL: Component 3 — emails.json not available (skipping sort/dedup check)")
        else:
            str_emails = [str(e).lower() for e in emails_data]
            is_sorted = str_emails == sorted(str_emails)
            has_no_dupes = len(str_emails) == len(set(str_emails))

            if is_sorted and has_no_dupes:
                print(f"PASS: Component 3 — emails are alphabetically sorted and deduplicated (0.20 pts)")
                total_score += 0.20
            elif is_sorted:
                print(f"PARTIAL: Component 3 — emails are sorted but have duplicates ({len(str_emails) - len(set(str_emails))} dupe(s)) (0.10 pts)")
                total_score += 0.10
            elif has_no_dupes:
                print(f"PARTIAL: Component 3 — emails are deduplicated but not alphabetically sorted (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — emails are neither sorted nor deduplicated")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Emails contain addresses from expected domains (company.com, gmail.com, outlook.com) (0.15 points)
    # This FAILS on initial_env (no emails.json) and PASSES on golden_env
    try:
        if emails_data is None:
            print(f"FAIL: Component 4 — emails.json not available (skipping domain check)")
        else:
            str_emails = [str(e).lower() for e in emails_data]
            has_company = any('@company.com' in e for e in str_emails)
            has_gmail = any('@gmail.com' in e for e in str_emails)
            has_outlook = any('@outlook.com' in e for e in str_emails)

            domains_found = sum([has_company, has_gmail, has_outlook])
            if domains_found == 3:
                print(f"PASS: Component 4 — emails include addresses from company.com, gmail.com, and outlook.com (0.15 pts)")
                total_score += 0.15
            elif domains_found == 2:
                print(f"PARTIAL: Component 4 — emails include addresses from {domains_found}/3 expected domains "
                      f"(company.com={has_company}, gmail.com={has_gmail}, outlook.com={has_outlook}) (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 — emails missing expected domains "
                      f"(company.com={has_company}, gmail.com={has_gmail}, outlook.com={has_outlook})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
