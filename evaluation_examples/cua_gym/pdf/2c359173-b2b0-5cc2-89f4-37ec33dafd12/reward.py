"""
Reward Script: Encrypt board_minutes.pdf with owner/user passwords and restricted permissions
Task ID: pdf_fm_080
Domain: pdf
Scoring:
  Component 1: File exists and is encrypted (0.20)
  Component 2: User password 'Read0nly!' authenticates (0.20)
  Component 3: Owner password 'Admin#2025' authenticates with full access (0.20)
  Component 4: AES-256 encryption (R=6, 256-bit) (0.15)
  Component 5: Printing allowed (print_lowres + print_highres) (0.15)
  Component 6: Copy and edit disabled (extract=False, modify_other=False) (0.10)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_080'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'board_minutes_secure.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted — requires a password to open (0.20 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        is_encrypted = doc.is_encrypted
        needs_pass = doc.needs_pass
        doc.close()
        if is_encrypted:
            print(f"PASS: Component 1 — File is encrypted (is_encrypted={is_encrypted}, needs_pass={needs_pass}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File is NOT encrypted (is_encrypted={is_encrypted})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: User password 'Read0nly!' authenticates successfully (0.20 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        auth_result = doc.authenticate('Read0nly!')
        doc.close()
        # authenticate returns: 0=failed, 1=no password needed, 2=user level, 4=owner level
        if auth_result >= 2:
            print(f"PASS: Component 2 — User password 'Read0nly!' authenticates (auth_result={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — User password 'Read0nly!' failed (auth_result={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password 'Admin#2025' authenticates with owner-level access (0.20 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        auth_result = doc.authenticate('Admin#2025')
        doc.close()
        # auth_result 4 = owner level
        if auth_result >= 4:
            print(f"PASS: Component 3 — Owner password 'Admin#2025' authenticates at owner level (auth_result={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Owner password 'Admin#2025' did not get owner-level access (auth_result={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: AES-256 encryption (R=6, 256-bit key) (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='Admin#2025')
        enc = pdf.encryption
        r_value = enc.R
        bits = enc.bits
        pdf.close()
        if r_value == 6 and bits == 256:
            print(f"PASS: Component 4 — AES-256 encryption confirmed (R={r_value}, bits={bits}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected R=6/256-bit, found R={r_value}/bits={bits}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Printing is allowed (print_lowres=True AND print_highres=True) (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='Read0nly!')
        allow = pdf.allow
        print_low = allow.print_lowres
        print_high = allow.print_highres
        pdf.close()
        if print_low and print_high:
            print(f"PASS: Component 5 — Printing allowed (lowres={print_low}, highres={print_high}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Printing not fully allowed (lowres={print_low}, highres={print_high})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Copy and edit disabled (extract=False, modify_other=False) (0.10 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='Read0nly!')
        allow = pdf.allow
        extract = allow.extract
        modify_other = allow.modify_other
        pdf.close()
        if not extract and not modify_other:
            print(f"PASS: Component 6 — Copy/edit disabled (extract={extract}, modify_other={modify_other}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Copy/edit not fully disabled (extract={extract}, modify_other={modify_other})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
