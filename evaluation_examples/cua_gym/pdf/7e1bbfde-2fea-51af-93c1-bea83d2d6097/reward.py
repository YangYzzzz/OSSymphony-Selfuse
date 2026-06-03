"""
Reward Script: PDF Password Protection
Task ID: pdf_mbc_004
Domain: pdf
Scoring:
  Component 1: Protected file exists and is encrypted (0.20 pts)
  Component 2: Password 'read2024' authenticates successfully (0.30 pts)
  Component 3: AES-256 encryption (R=6, V=5) (0.15 pts)
  Component 4: Wrong/no password is rejected (0.15 pts)
  Component 5: Content preserved - same page count as original (0.20 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_004'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'employee_handbook.pdf')
PROTECTED_PATH = os.path.join(WORKDIR, 'Documents', 'employee_handbook_protected.pdf')
EXPECTED_PASSWORD = 'read2024'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist (gate, not scored)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: protected file must exist (gate, not scored alone)
    if not os.path.exists(PROTECTED_PATH):
        print(f"FAIL: Protected file not found: {PROTECTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Protected file exists AND is encrypted (0.20 pts)
    # This is a compound check: file existence + encryption flag
    # On initial_env, the protected file does not exist, so we never reach here
    try:
        import pymupdf
        doc = pymupdf.open(PROTECTED_PATH)
        is_enc = doc.is_encrypted
        doc.close()
        if is_enc:
            print(f"PASS: Component 1 - Protected file exists and is encrypted (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Protected file exists but is NOT encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Password 'read2024' authenticates successfully (0.30 pts)
    try:
        import pymupdf
        doc = pymupdf.open(PROTECTED_PATH)
        if doc.is_encrypted:
            auth_result = doc.authenticate(EXPECTED_PASSWORD)
            doc.close()
            if auth_result > 0:
                print(f"PASS: Component 2 - Password '{EXPECTED_PASSWORD}' authenticates (auth_result={auth_result}) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - Password '{EXPECTED_PASSWORD}' failed authentication (auth_result={auth_result})")
        else:
            doc.close()
            print(f"FAIL: Component 2 - File is not encrypted, cannot test password")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: AES-256 encryption (R=6) (0.15 pts)
    try:
        import pikepdf
        pdf = pikepdf.open(PROTECTED_PATH, password=EXPECTED_PASSWORD)
        enc = pdf.encryption
        r_val = enc.R
        v_val = enc.V
        pdf.close()
        if r_val == 6 and v_val == 5:
            print(f"PASS: Component 3 - AES-256 encryption confirmed (R={r_val}, V={v_val}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Expected R=6, V=5 (AES-256), found R={r_val}, V={v_val}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Wrong/no password is rejected (0.15 pts)
    try:
        import pikepdf
        rejection_count = 0

        # Test wrong password
        try:
            pdf_bad = pikepdf.open(PROTECTED_PATH, password='wrongpassword')
            pdf_bad.close()
            print(f"FAIL: Component 4 - Wrong password was accepted")
        except Exception:
            rejection_count += 1  # wrong password correctly rejected

        # Test no password
        try:
            pdf_none = pikepdf.open(PROTECTED_PATH)
            pdf_none.close()
            print(f"FAIL: Component 4 - File opened without password")
        except Exception:
            rejection_count += 1  # no password correctly rejected

        if rejection_count == 2:
            print(f"PASS: Component 4 - Wrong and no password both correctly rejected (0.15 pts)")
            total_score += 0.15
        elif rejection_count == 1:
            print(f"PARTIAL: Component 4 - Only one rejection succeeded ({rejection_count}/2) (0.075 pts)")
            total_score += 0.075
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Content preserved - same page count as original (0.20 pts)
    try:
        import pymupdf
        doc_orig = pymupdf.open(ORIGINAL_PATH)
        orig_pages = doc_orig.page_count
        doc_orig.close()

        doc_prot = pymupdf.open(PROTECTED_PATH)
        if doc_prot.is_encrypted:
            doc_prot.authenticate(EXPECTED_PASSWORD)
        prot_pages = doc_prot.page_count
        doc_prot.close()

        if orig_pages == prot_pages:
            print(f"PASS: Component 5 - Page count preserved ({prot_pages} pages) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 - Page count mismatch: original={orig_pages}, protected={prot_pages}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
