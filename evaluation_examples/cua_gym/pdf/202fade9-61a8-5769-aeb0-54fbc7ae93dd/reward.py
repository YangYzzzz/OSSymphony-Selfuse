"""
Reward Script: PDF encryption with owner password and permission restrictions
Task ID: pdf_mbc_006
Domain: pdf
Scoring:
  Component 1 (0.25): PDF is encrypted (was unencrypted initially)
  Component 2 (0.25): Owner password 'admin9876' works
  Component 3 (0.20): Printing is disabled (both lowres and highres)
  Component 4 (0.20): Content extraction/copying is disabled
  Component 5 (0.10): Document content preserved (page count == 28)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_006'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'design_spec.pdf')


def verify_task(file_path):
    """
    Verify PDF encryption task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    import pikepdf

    # First, try opening without any password to check basic accessibility
    try:
        pdf_no_pw = pikepdf.open(file_path)
    except pikepdf.PasswordError:
        # If we can't open without password, user password was set (wrong behavior)
        print("FAIL: PDF requires a user password to open — task says users should view without a password")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF is encrypted (0.25 points)
    # This FAILS on initial (unencrypted) and PASSES on golden (encrypted)
    try:
        if pdf_no_pw.is_encrypted:
            print(f"PASS: Component 1 — PDF is encrypted (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — PDF is not encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Owner password 'admin9876' works (0.25 points)
    # Gated on encryption: if the PDF is not encrypted, owner password is meaningless
    # This FAILS on initial (not encrypted) and PASSES on golden
    try:
        if pdf_no_pw.is_encrypted:
            pdf_no_pw.close()
            try:
                pdf_owner = pikepdf.open(file_path, password='admin9876')
                print(f"PASS: Component 2 — Owner password 'admin9876' accepted on encrypted PDF (0.25 pts)")
                total_score += 0.25
                pdf_owner.close()
            except pikepdf.PasswordError:
                print(f"FAIL: Component 2 — Owner password 'admin9876' rejected")
            except Exception as e:
                print(f"ERROR: Component 2 — {e}")
        else:
            pdf_no_pw.close()
            print(f"FAIL: Component 2 — PDF not encrypted, owner password check not applicable")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Reopen for permission checks
    try:
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"ERROR: Cannot reopen PDF for permission checks: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Printing disabled (0.20 points)
    # Both print_lowres and print_highres should be False
    # This FAILS on initial (not encrypted, no restrictions) and PASSES on golden
    try:
        if pdf.is_encrypted:
            allow = pdf.allow
            lowres_disabled = not allow.print_lowres
            highres_disabled = not allow.print_highres
            if lowres_disabled and highres_disabled:
                print(f"PASS: Component 3 — Printing disabled (lowres={allow.print_lowres}, highres={allow.print_highres}) (0.20 pts)")
                total_score += 0.20
            elif lowres_disabled or highres_disabled:
                print(f"PARTIAL: Component 3 — Only partial print restriction (lowres={allow.print_lowres}, highres={allow.print_highres}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Printing not disabled (lowres={allow.print_lowres}, highres={allow.print_highres})")
        else:
            print(f"FAIL: Component 3 — PDF not encrypted, cannot check print permissions")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content extraction/copying disabled (0.20 points)
    # extract should be False
    # This FAILS on initial (not encrypted) and PASSES on golden
    try:
        if pdf.is_encrypted:
            allow = pdf.allow
            if not allow.extract:
                print(f"PASS: Component 4 — Content extraction disabled (extract={allow.extract}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Content extraction still allowed (extract={allow.extract})")
        else:
            print(f"FAIL: Component 4 — PDF not encrypted, cannot check extract permissions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Document content preserved — page count == 28 (0.10 points)
    # This check is anchored to encryption: only awards points if the PDF is encrypted AND has 28 pages
    # On initial_env (unencrypted), Component 1 gate prevents this from being a free point
    try:
        if pdf.is_encrypted:
            page_count = len(pdf.pages)
            if page_count == 28:
                print(f"PASS: Component 5 — Page count preserved ({page_count} pages) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Expected 28 pages, found {page_count}")
        else:
            print(f"FAIL: Component 5 — PDF not encrypted, skipping content preservation check")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    pdf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
