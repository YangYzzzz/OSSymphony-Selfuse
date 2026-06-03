"""
Reward Script: Password-protect a mediation brief PDF
Task ID: pdf_legal_063
Domain: pdf
Scoring:
  Component 1 (0.35): Protected file exists and is encrypted
  Component 2 (0.35): Correct password 'mediation2024' authenticates; wrong password fails
  Component 3 (0.30): All permissions allowed after auth + content integrity (12 pages)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_063'
PROTECTED_PATH = os.path.join(WORKDIR, 'legal', 'mediation', 'brief_protected.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'legal', 'mediation', 'brief.pdf')
EXPECTED_PASSWORD = 'mediation2024'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: protected file must exist
    if not os.path.exists(PROTECTED_PATH):
        print(f"CRITICAL: Protected file not found at {PROTECTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Protected file is encrypted (0.35 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        import pymupdf
        doc = pymupdf.open(PROTECTED_PATH)
        is_encrypted = doc.is_encrypted
        needs_pass = doc.needs_pass
        doc.close()

        if is_encrypted and needs_pass:
            print(f"PASS: Component 1 — brief_protected.pdf is encrypted and requires password (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — is_encrypted={is_encrypted}, needs_pass={needs_pass}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct password authenticates, wrong password fails (0.35 points)
    # Verifies the specific password 'mediation2024' works
    try:
        import pymupdf
        # Test correct password
        doc = pymupdf.open(PROTECTED_PATH)
        auth_result = doc.authenticate(EXPECTED_PASSWORD)
        doc.close()

        correct_pass_works = auth_result > 0

        # Test wrong password is rejected
        doc2 = pymupdf.open(PROTECTED_PATH)
        wrong_auth = doc2.authenticate('wrongpassword123')
        doc2.close()

        wrong_pass_rejected = wrong_auth == 0

        if correct_pass_works and wrong_pass_rejected:
            print(f"PASS: Component 2 — password 'mediation2024' authenticates (auth={auth_result}), wrong password rejected (0.35 pts)")
            total_score += 0.35
        elif correct_pass_works:
            print(f"PARTIAL: Component 2 — correct password works but wrong password also accepted (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — correct password failed (auth_result={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Full permissions after auth + content integrity (0.30 points)
    # Task says "Allow full access once the user password is entered"
    try:
        import pikepdf
        pdf = pikepdf.open(PROTECTED_PATH, password=EXPECTED_PASSWORD)
        allow = pdf.allow
        page_count = len(pdf.pages)
        pdf.close()

        # Check all permissions are True (full access)
        perms_to_check = [
            ('print_lowres', allow.print_lowres),
            ('print_highres', allow.print_highres),
            ('modify_annotation', allow.modify_annotation),
            ('modify_other', allow.modify_other),
            ('extract', allow.extract),
            ('accessibility', allow.accessibility),
        ]

        all_perms_ok = all(val for _, val in perms_to_check)
        failed_perms = [name for name, val in perms_to_check if not val]

        # Content integrity: should have same 12 pages as original
        pages_ok = page_count == 12

        if all_perms_ok and pages_ok:
            print(f"PASS: Component 3 — all permissions allowed, page count correct ({page_count}) (0.30 pts)")
            total_score += 0.30
        elif all_perms_ok and not pages_ok:
            print(f"PARTIAL: Component 3 — permissions OK but page count wrong ({page_count} != 12) (0.15 pts)")
            total_score += 0.15
        elif not all_perms_ok and pages_ok:
            print(f"PARTIAL: Component 3 — page count OK but permissions restricted: {failed_perms} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — permissions restricted ({failed_perms}), pages wrong ({page_count})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
