"""
Reward Script: Redact emails and encrypt PDF with password
Task ID: pdf_pw_006
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists and is encrypted
  Component 2 (0.20): Password 'depo2026' successfully authenticates
  Component 3 (0.30): No email addresses remain in extracted text
  Component 4 (0.15): Permissions — printing allowed, copy/edit restricted
  Component 5 (0.15): All 35 pages preserved
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_006'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'depositions_batch_secured.pdf')
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # ----------------------------------------------------------------
    # Component 1: File is encrypted (0.20 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    # ----------------------------------------------------------------
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
        is_encrypted = doc.is_encrypted
        doc.close()
        if is_encrypted:
            print(f"PASS: Component 1 — File is encrypted (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File is NOT encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Password 'depo2026' authenticates (0.20 points)
    # ----------------------------------------------------------------
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
        if doc.is_encrypted:
            auth_result = doc.authenticate('depo2026')
            doc.close()
            if auth_result > 0:
                print(f"PASS: Component 2 — Password 'depo2026' works (auth={auth_result}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Password 'depo2026' rejected (auth={auth_result})")
        else:
            doc.close()
            print(f"FAIL: Component 2 — File not encrypted, password check N/A")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: No email addresses in text (0.30 points)
    # Initial file has ~21 emails; golden must have 0
    # ----------------------------------------------------------------
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
        if doc.is_encrypted:
            doc.authenticate('depo2026')
        emails_found = []
        for page in doc:
            text = page.get_text()
            found = EMAIL_PATTERN.findall(text)
            emails_found.extend(found)
        doc.close()

        if len(emails_found) == 0:
            print(f"PASS: Component 3 — Zero email addresses found in text (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Found {len(emails_found)} email(s): {emails_found[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Permissions — print allowed, copy/edit restricted (0.15 points)
    # ----------------------------------------------------------------
    try:
        import pikepdf
        pdf = pikepdf.open(OUTPUT_PATH, password='depo2026')
        allow = pdf.allow
        print_ok = allow.print_lowres or allow.print_highres
        copy_restricted = not allow.extract
        edit_restricted = not allow.modify_other
        pdf.close()

        perm_pass = print_ok and copy_restricted and edit_restricted
        if perm_pass:
            print(f"PASS: Component 4 — Print=allowed, Copy=restricted, Edit=restricted (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — print_ok={print_ok}, copy_restricted={copy_restricted}, edit_restricted={edit_restricted}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: All 35 pages preserved (0.15 points)
    # ----------------------------------------------------------------
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
        if doc.is_encrypted:
            doc.authenticate('depo2026')
        page_count = len(doc)
        doc.close()

        if page_count == 35:
            print(f"PASS: Component 5 — Page count is 35 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected 35 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
