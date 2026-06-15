"""
Reward Script: Encrypt PDF with user/owner passwords and permission restrictions
Task ID: pdf_gf3_010
Domain: pdf
Scoring:
  - Component 1 (0.25): File exists, is encrypted, and requires a password to open
  - Component 2 (0.20): User password 'View2024!' successfully opens the file
  - Component 3 (0.20): Owner password 'Admin2024!' opens the file with owner-level access
  - Component 4 (0.15): Printing is allowed (print_lowres and print_highres both True)
  - Component 5 (0.20): Text extraction/copying is disallowed (extract is False)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_010'

def verify_task():
    """
    Verify PDF encryption task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    encrypted_path = f'{WORKDIR}/private/tax_return_encrypted.pdf'
    original_path = f'{WORKDIR}/private/tax_return.pdf'

    # Precondition: encrypted file must exist
    if not os.path.exists(encrypted_path):
        print(f"CRITICAL: Encrypted file not found at {encrypted_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: original file must still exist (task says it should be unchanged)
    if not os.path.exists(original_path):
        print(f"CRITICAL: Original file missing at {original_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted and requires a password to open (0.25 points)
    try:
        import pymupdf
        doc = pymupdf.open(encrypted_path)
        is_encrypted = doc.is_encrypted
        needs_pass = doc.needs_pass
        doc.close()

        if is_encrypted and needs_pass:
            print(f"PASS: Component 1 — File is encrypted and requires password (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — is_encrypted={is_encrypted}, needs_pass={needs_pass}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: User password 'View2024!' opens the file (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(encrypted_path)
        auth_result = doc.authenticate('View2024!')
        doc.close()

        # authenticate returns: 0=failed, 1=user-level, 2=owner-level (if user==owner)
        if auth_result > 0:
            print(f"PASS: Component 2 — User password 'View2024!' accepted (auth={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — User password 'View2024!' rejected (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password 'Admin2024!' opens with owner-level access (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(encrypted_path)
        auth_result = doc.authenticate('Admin2024!')
        doc.close()

        # Owner password should return 4 or 6 (owner-level access)
        # PyMuPDF authenticate returns bitmask: 1=user, 2=owner => combinations: 1,2,4,6
        # Actually: returns int where & 4 means owner access
        if auth_result >= 4:
            print(f"PASS: Component 3 — Owner password 'Admin2024!' accepted with owner access (auth={auth_result}) (0.20 pts)")
            total_score += 0.20
        elif auth_result > 0:
            print(f"PARTIAL: Component 3 — Password accepted but only user-level (auth={auth_result})")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Owner password 'Admin2024!' rejected (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Printing is allowed (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(encrypted_path, password='Admin2024!')
        allow = pdf.allow
        print_lowres = allow.print_lowres
        print_highres = allow.print_highres
        pdf.close()

        if print_lowres and print_highres:
            print(f"PASS: Component 4 — Printing allowed (lowres={print_lowres}, highres={print_highres}) (0.15 pts)")
            total_score += 0.15
        elif print_lowres or print_highres:
            print(f"PARTIAL: Component 4 — Only partial print (lowres={print_lowres}, highres={print_highres})")
            total_score += 0.075
        else:
            print(f"FAIL: Component 4 — Printing disallowed (lowres={print_lowres}, highres={print_highres})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Text extraction/copying is disallowed (0.20 points)
    try:
        import pikepdf
        pdf = pikepdf.open(encrypted_path, password='Admin2024!')
        allow = pdf.allow
        extract = allow.extract
        pdf.close()

        if not extract:
            print(f"PASS: Component 5 — Text extraction disallowed (extract={extract}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Text extraction is allowed (extract={extract})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
