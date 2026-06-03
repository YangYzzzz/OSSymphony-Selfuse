"""
Reward Script: Password-protect discovery production PDF with AES-256 encryption
Task ID: pdf_legal_021
Domain: pdf
Scoring:
  - Component 1 (0.20): Encrypted file exists and is encrypted
  - Component 2 (0.20): User password 'disc0very2024' authenticates
  - Component 3 (0.15): Owner password 'admin_disc!' authenticates
  - Component 4 (0.15): AES-256 encryption (revision 6, 256-bit)
  - Component 5 (0.15): Printing is allowed (print_lowres and print_highres)
  - Component 6 (0.15): Editing and text extraction are restricted
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_021'

ENCRYPTED_PATH = os.path.join(WORKDIR, 'legal', 'discovery', 'production_001_encrypted.pdf')
USER_PASSWORD = 'disc0very2024'
OWNER_PASSWORD = 'admin_disc!'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Encrypted file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        is_enc = doc.is_encrypted
        doc.close()
        if is_enc:
            print(f"PASS: Component 1 — File is encrypted (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File is NOT encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: User password authenticates (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        auth_result = doc.authenticate(USER_PASSWORD)
        doc.close()
        if auth_result > 0:
            print(f"PASS: Component 2 — User password authenticates (auth={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — User password failed (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password authenticates (0.15 points)
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        auth_result = doc.authenticate(OWNER_PASSWORD)
        doc.close()
        if auth_result > 0:
            print(f"PASS: Component 3 — Owner password authenticates (auth={auth_result}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Owner password failed (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: AES-256 encryption — R=6, 256-bit (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password=OWNER_PASSWORD)
        enc = pdf.encryption
        r_val = enc.R
        bits = enc.bits
        pdf.close()
        if r_val == 6 and bits == 256:
            print(f"PASS: Component 4 — AES-256 confirmed (R={r_val}, bits={bits}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected R=6/256-bit, got R={r_val}/bits={bits}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Printing allowed (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password=OWNER_PASSWORD)
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

    # Component 6: Editing and text extraction restricted (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password=OWNER_PASSWORD)
        allow = pdf.allow
        modify = allow.modify_other
        extract = allow.extract
        pdf.close()
        if not modify and not extract:
            print(f"PASS: Component 6 — Editing({modify}) and extraction({extract}) restricted (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — modify_other={modify}, extract={extract} (both should be False)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(ENCRYPTED_PATH):
    print(f"File not found: {ENCRYPTED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ENCRYPTED_PATH)
