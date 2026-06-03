"""
Reward Script: Change PDF owner password
Task ID: pdf_mbc_013
Domain: pdf
Scoring:
  Component 1 (0.4): New owner password 'newSecure!456' authenticates
  Component 2 (0.3): Old owner password 'oldpass123' no longer authenticates
  Component 3 (0.2): Permissions preserved (no editing, no copying) with new password
  Component 4 (0.1): Content unchanged (page count and text) with new password
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_013'
FILE_PATH = os.path.join(WORKDIR, 'Secure', 'classified.pdf')

NEW_OWNER_PASS = 'newSecure!456'
OLD_OWNER_PASS = 'oldpass123'


def try_open_with_password(file_path, password):
    """Try to open PDF with given password. Returns pikepdf object or None."""
    import pikepdf
    try:
        return pikepdf.open(file_path, password=password)
    except Exception:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file exists and is a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # We use pikepdf for password/encryption verification and pymupdf for content checks
    try:
        import pikepdf
    except ImportError:
        print("CRITICAL: pikepdf not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        print("CRITICAL: pymupdf not available")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: New owner password 'newSecure!456' authenticates (0.4 points)
    # This FAILS on initial (oldpass123 is the owner password, not newSecure!456)
    # This PASSES on golden (owner password changed to newSecure!456)
    try:
        pdf_new = try_open_with_password(file_path, NEW_OWNER_PASS)
        if pdf_new is not None:
            pdf_new.close()
            print(f"PASS: Component 1 — new owner password '{NEW_OWNER_PASS}' authenticates (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — new owner password '{NEW_OWNER_PASS}' does not authenticate")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Old owner password 'oldpass123' no longer authenticates (0.3 points)
    # This FAILS on initial (oldpass123 works fine on initial)
    # This PASSES on golden (oldpass123 no longer works)
    try:
        pdf_old = try_open_with_password(file_path, OLD_OWNER_PASS)
        if pdf_old is None:
            print(f"PASS: Component 2 — old owner password '{OLD_OWNER_PASS}' no longer works (0.3 pts)")
            total_score += 0.3
        else:
            pdf_old.close()
            print(f"FAIL: Component 2 — old owner password '{OLD_OWNER_PASS}' still authenticates")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Permissions preserved with new password (0.2 points)
    # Gated on new password working — if new password doesn't work, skip
    # Expected permissions: extract=False, modify_other=False (no editing, no copying)
    # This component only awards points when new password works AND permissions match
    try:
        pdf_perms = try_open_with_password(file_path, NEW_OWNER_PASS)
        if pdf_perms is None:
            print("FAIL: Component 3 — skipped (new owner password does not work)")
        else:
            allow = pdf_perms.allow
            pdf_perms.close()

            extract_blocked = not allow.extract
            modify_blocked = not allow.modify_other
            modify_annot_blocked = not allow.modify_annotation
            modify_form_blocked = not allow.modify_form
            modify_assembly_blocked = not allow.modify_assembly

            if extract_blocked and modify_blocked and modify_annot_blocked \
                    and modify_form_blocked and modify_assembly_blocked:
                print(f"PASS: Component 3 — restrictions preserved: extract={allow.extract}, "
                      f"modify_other={allow.modify_other}, modify_annotation={allow.modify_annotation}, "
                      f"modify_form={allow.modify_form}, modify_assembly={allow.modify_assembly} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — permissions mismatch: extract={allow.extract}, "
                      f"modify_other={allow.modify_other}, modify_annotation={allow.modify_annotation}, "
                      f"modify_form={allow.modify_form}, modify_assembly={allow.modify_assembly}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content unchanged with new password (0.1 points)
    # Gated on new password working — if new password doesn't work, skip
    # Check page count == 3 and first page contains expected text
    try:
        doc = pymupdf.open(file_path)
        auth_result = doc.authenticate(NEW_OWNER_PASS)
        if auth_result == 0:
            doc.close()
            print("FAIL: Component 4 — skipped (new owner password does not authenticate via pymupdf)")
        else:
            page_count = doc.page_count
            page_text = doc[0].get_text()
            doc.close()

            if page_count == 3 and 'CLASSIFIED' in page_text and 'Project Meridian' in page_text:
                print(f"PASS: Component 4 — content unchanged: {page_count} pages, "
                      f"expected text found (0.1 pts)")
                total_score += 0.1
            else:
                has_classified = 'CLASSIFIED' in page_text
                has_meridian = 'Project Meridian' in page_text
                print(f"FAIL: Component 4 — page_count={page_count} (exp 3), "
                      f"CLASSIFIED={has_classified}, Project Meridian={has_meridian}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
