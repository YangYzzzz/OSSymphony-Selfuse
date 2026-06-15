"""
Reward Script: Encrypt PDF with passwords and restricted permissions
Task ID: pdf_ro_008
Domain: pdf
Scoring:
  Component 1 (0.20): Encrypted file exists and is encrypted
  Component 2 (0.20): User password 'read2026' authenticates
  Component 3 (0.15): Owner password 'admin2026' authenticates
  Component 4 (0.25): Permissions correct (print allowed, extract/modify disallowed)
  Component 5 (0.10): AES-256 encryption (R=6, V=5, CFM=AESV3)
  Component 6 (0.10): Page count preserved (8 pages)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_008'
ENCRYPTED_PATH = os.path.join(WORKDIR, 'Documents', 'confidential_encrypted.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: encrypted file must exist
    if not os.path.exists(ENCRYPTED_PATH):
        print(f"CRITICAL: Encrypted file not found at {ENCRYPTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        if doc.is_encrypted:
            print(f"PASS: Component 1 -- File is encrypted (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- File is not encrypted")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: User password 'read2026' opens the file (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        auth_result = doc.authenticate('read2026')
        if auth_result > 0:
            print(f"PASS: Component 2 -- User password 'read2026' authenticates (auth_result={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- User password 'read2026' does not authenticate (auth_result={auth_result})")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Owner password 'admin2026' opens the file (0.15 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        auth_result = doc.authenticate('admin2026')
        # Owner password should return 2 (or higher) in pymupdf
        if auth_result > 0:
            print(f"PASS: Component 3 -- Owner password 'admin2026' authenticates (auth_result={auth_result}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Owner password 'admin2026' does not authenticate (auth_result={auth_result})")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Permissions correct (0.25 points)
    # Print allowed, extract/copy disallowed, modify disallowed
    try:
        import pikepdf
        pdf = pikepdf.open(ENCRYPTED_PATH, password='read2026')
        allow = pdf.allow

        perm_score = 0.0
        perm_checks = 0

        # Printing should be allowed
        if allow.print_lowres or allow.print_highres:
            print(f"  PASS: Printing allowed (print_lowres={allow.print_lowres}, print_highres={allow.print_highres})")
            perm_score += 1.0
            perm_checks += 1
        else:
            print(f"  FAIL: Printing not allowed")
            perm_checks += 1

        # Extract/copy should be disallowed
        if not allow.extract:
            print(f"  PASS: Text extraction/copying disallowed (extract={allow.extract})")
            perm_score += 1.0
            perm_checks += 1
        else:
            print(f"  FAIL: Text extraction/copying is allowed (extract={allow.extract})")
            perm_checks += 1

        # Modification should be disallowed
        if not allow.modify_other:
            print(f"  PASS: Modification disallowed (modify_other={allow.modify_other})")
            perm_score += 1.0
            perm_checks += 1
        else:
            print(f"  FAIL: Modification is allowed (modify_other={allow.modify_other})")
            perm_checks += 1

        if perm_checks > 0:
            component4_score = 0.25 * (perm_score / perm_checks)
            total_score += component4_score
            if perm_score == perm_checks:
                print(f"PASS: Component 4 -- All permissions correct ({component4_score:.2f} pts)")
            else:
                print(f"PARTIAL: Component 4 -- {int(perm_score)}/{perm_checks} permission checks passed ({component4_score:.2f} pts)")

        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: AES-256 encryption (R=6, V=5) (0.10 points)
    try:
        import pikepdf
        pdf = pikepdf.open(ENCRYPTED_PATH, password='admin2026')
        trailer = pdf.trailer
        if '/Encrypt' in trailer:
            enc = trailer['/Encrypt']
            v_val = int(enc.get('/V', 0))
            r_val = int(enc.get('/R', 0))
            # Check for AES-256: V=5, R=6
            if v_val == 5 and r_val == 6:
                print(f"PASS: Component 5 -- AES-256 encryption confirmed (V={v_val}, R={r_val}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- Expected V=5, R=6 for AES-256, got V={v_val}, R={r_val}")
        else:
            print(f"FAIL: Component 5 -- No /Encrypt dictionary in trailer")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Page count preserved (8 pages) (0.10 points)
    try:
        import pymupdf
        doc = pymupdf.open(ENCRYPTED_PATH)
        doc.authenticate('read2026')
        page_count = doc.page_count
        if page_count == 8:
            print(f"PASS: Component 6 -- Page count is 8 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- Expected 8 pages, found {page_count}")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
