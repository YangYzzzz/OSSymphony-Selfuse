"""
Reward Script: Export presentation as password-protected PDF
Task ID: impress_el_019
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.35): PDF exists and is encrypted (requires password)
  - Component 2 (0.35): PDF opens with password 'SecureDoc2025'
  - Component 3 (0.30): PDF contains exactly 15 pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_el_019'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: PDF file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    import pikepdf

    # Component 1: PDF is encrypted / requires password to open (0.35 points)
    try:
        encryption_check = "unknown"
        try:
            pdf_no_pass = pikepdf.open(file_path)
            # If we get here, the PDF opened without a password — NOT encrypted
            pdf_no_pass.close()
            encryption_check = "not_encrypted"
        except pikepdf.PasswordError:
            # Good — password is required, meaning the PDF is encrypted
            encryption_check = "encrypted"

        if encryption_check == "encrypted":
            print("PASS: Component 1 — PDF is encrypted and requires a password (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — PDF opened without password, not encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF opens with the specific password 'SecureDoc2025' (0.35 points)
    pdf = None
    try:
        pdf = pikepdf.open(file_path, password='SecureDoc2025')
        correct_password = pdf.is_encrypted  # verify it was actually encrypted
        if correct_password:
            print("PASS: Component 2 — PDF opens with password 'SecureDoc2025' (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — PDF opened but is_encrypted is False")
    except pikepdf.PasswordError:
        print("FAIL: Component 2 — PDF does NOT open with password 'SecureDoc2025'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF contains exactly 15 pages (0.30 points)
    if pdf is not None:
        try:
            page_count = len(pdf.pages)
            if page_count == 15:
                print(f"PASS: Component 3 — PDF has 15 pages as expected (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Expected 15 pages, found {page_count}")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
        finally:
            pdf.close()
    else:
        print("SKIP: Component 3 — Could not open PDF (no valid handle)")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    # Also check common alternative names
    alt_names = [
        f'{WORKDIR}/Confidential_Report.pdf',
        f'{WORKDIR}/impress_el_019_initial.pdf',
    ]
    file_path = None
    for alt in alt_names:
        if os.path.exists(alt):
            print(f"Found PDF at alternative path: {alt}")
            file_path = alt
            break
    if file_path is None:
        print(f"File not found: {WORKDIR}/{TASK_ID}.pdf (also checked alternatives)")
        print("REWARD: 0.0")
    else:
        verify_task(file_path)
else:
    verify_task(file_path)
