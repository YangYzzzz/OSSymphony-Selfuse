"""
Reward Script: Encrypt PDF with passwords and permission restrictions
Task ID: pdf_gf1_012
Domain: pdf
Scoring:
  1. Encrypted file exists (0.15)
  2. File is encrypted / requires password (0.15)
  3. User password 'user1234' authenticates (0.20)
  4. Owner password 'owner5678' authenticates (0.15)
  5. Printing is allowed (0.10)
  6. Copy/extract is restricted (0.10)
  7. Modification is restricted (0.10)
  8. Page count preserved at 6 (0.05)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_012'

ENCRYPTED_PATH = os.path.join(WORKDIR, 'Documents', 'confidential_report_encrypted.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: encrypted file must exist ----
    if not os.path.exists(ENCRYPTED_PATH):
        print(f"CRITICAL: Encrypted file not found at {ENCRYPTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Encrypted file exists and has non-zero size (0.15 points)
    try:
        fsize = os.path.getsize(ENCRYPTED_PATH)
        if fsize > 0:
            print(f"PASS: Component 1 — Encrypted file exists, size={fsize} bytes (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Encrypted file exists but is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File is encrypted (requires password) (0.15 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        is_enc = doc.is_encrypted
        needs = doc.needs_pass
        doc.close()
        if is_enc:
            print(f"PASS: Component 2 — File is encrypted, needs_pass={needs} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — File is NOT encrypted")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: User password 'user1234' authenticates (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        auth_result = doc.authenticate('user1234')
        doc.close()
        # authenticate returns: 0=failed, 1=no password needed,
        # 2=user password correct, 4=owner password correct, 6=both
        if auth_result > 0:
            print(f"PASS: Component 3 — User password 'user1234' accepted, auth_result={auth_result} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — User password 'user1234' rejected, auth_result={auth_result}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Owner password 'owner5678' authenticates (0.15 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        auth_result = doc.authenticate('owner5678')
        doc.close()
        if auth_result >= 4:
            print(f"PASS: Component 4 — Owner password 'owner5678' accepted with owner-level, auth_result={auth_result} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Owner password 'owner5678' did not grant owner-level access, auth_result={auth_result}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Components 5-7: Permission checks (using pikepdf with owner password for full access)
    try:
        import pikepdf
        pdf = pikepdf.open(ENCRYPTED_PATH, password='owner5678')
        allow = pdf.allow

        # Component 5: Printing is allowed (0.10 points)
        if allow.print_lowres or allow.print_highres:
            print(f"PASS: Component 5 — Printing allowed (lowres={allow.print_lowres}, highres={allow.print_highres}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Printing NOT allowed (lowres={allow.print_lowres}, highres={allow.print_highres})")

        # Component 6: Copy/extract is restricted (0.10 points)
        if not allow.extract:
            print(f"PASS: Component 6 — Extract/copy restricted (extract={allow.extract}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Extract/copy NOT restricted (extract={allow.extract})")

        # Component 7: Modification is restricted (0.10 points)
        if not allow.modify_other:
            print(f"PASS: Component 7 — Modification restricted (modify_other={allow.modify_other}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Modification NOT restricted (modify_other={allow.modify_other})")

        pdf.close()
    except Exception as e:
        print(f"ERROR: Components 5-7 — Could not check permissions: {e}")

    # Component 8: Page count preserved at 6 (0.05 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        # Need to authenticate to read pages
        doc.authenticate('user1234')
        pc = doc.page_count
        doc.close()
        if pc == 6:
            print(f"PASS: Component 8 — Page count is 6 (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 8 — Expected 6 pages, found {pc}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
