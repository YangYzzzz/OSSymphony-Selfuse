"""
Reward Script: Encrypt PDF with user/owner passwords and specific permissions
Task ID: pdf_res_047
Domain: pdf
Scoring:
  Component 1 (0.20): Encrypted file exists and requires password
  Component 2 (0.20): User password 'read2026' authenticates
  Component 3 (0.10): Owner password 'admin2026' authenticates
  Component 4 (0.20): Printing is allowed (lowres + highres)
  Component 5 (0.15): Editing/modification is restricted
  Component 6 (0.15): Copying/extraction is restricted
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_047'

ENCRYPTED_PATH = os.path.join(WORKDIR, 'thesis', 'confidential_results_encrypted.pdf')
USER_PASSWORD = 'read2026'
OWNER_PASSWORD = 'admin2026'


def check_encryption():
    """Check if the file is encrypted (requires password). Returns bool."""
    import pikepdf
    try:
        pdf = pikepdf.open(ENCRYPTED_PATH)
        pdf.close()
        return False  # opened without password = not encrypted
    except pikepdf._core.PasswordError:
        return True  # password required = encrypted


def check_password(password):
    """Check if a given password can open the encrypted file. Returns bool."""
    import pikepdf
    try:
        pdf = pikepdf.open(ENCRYPTED_PATH, password=password)
        pdf.close()
        return True
    except pikepdf._core.PasswordError:
        return False


def get_permissions(password):
    """Open with password and return the allow (permissions) object, or None."""
    import pikepdf
    try:
        pdf = pikepdf.open(ENCRYPTED_PATH, password=password)
        allow = pdf.allow
        perms = {
            'print_lowres': allow.print_lowres,
            'print_highres': allow.print_highres,
            'modify_other': allow.modify_other,
            'modify_annotation': allow.modify_annotation,
            'modify_assembly': allow.modify_assembly,
            'modify_form': allow.modify_form,
            'extract': allow.extract,
        }
        pdf.close()
        return perms
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: encrypted file must exist
    if not os.path.exists(ENCRYPTED_PATH):
        print(f"CRITICAL: Encrypted file not found: {ENCRYPTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted (requires password to open) (0.20 points)
    try:
        if check_encryption():
            print(f"PASS: Component 1 — File is encrypted, requires password (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — File opened without password (not encrypted)")
            # Not encrypted => no point checking passwords/permissions
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: User password 'read2026' works (0.20 points)
    try:
        if check_password(USER_PASSWORD):
            print(f"PASS: Component 2 — User password '{USER_PASSWORD}' authenticates (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — User password '{USER_PASSWORD}' rejected")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password 'admin2026' works (0.10 points)
    try:
        if check_password(OWNER_PASSWORD):
            print(f"PASS: Component 3 — Owner password '{OWNER_PASSWORD}' authenticates (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Owner password '{OWNER_PASSWORD}' rejected")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Get permissions for components 4-6
    perms = get_permissions(USER_PASSWORD)
    if perms is None:
        perms = get_permissions(OWNER_PASSWORD)
    if perms is None:
        print("ERROR: Cannot read permissions with either password")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 4: Printing is allowed (0.20 points)
    try:
        if perms['print_lowres'] and perms['print_highres']:
            print(f"PASS: Component 4 — Printing allowed (lowres={perms['print_lowres']}, "
                  f"highres={perms['print_highres']}) (0.20 pts)")
            total_score += 0.20
        elif perms['print_lowres'] or perms['print_highres']:
            print(f"PARTIAL: Component 4 — Partial print (lowres={perms['print_lowres']}, "
                  f"highres={perms['print_highres']}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Printing not allowed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Editing/modification is restricted (0.15 points)
    try:
        edit_flags = [perms['modify_other'], perms['modify_annotation'],
                      perms['modify_assembly'], perms['modify_form']]
        if all(not flag for flag in edit_flags):
            total_score += 0.15
            print(f"PASS: Component 5 — All editing restricted (modify_other={perms['modify_other']}, "
                  f"modify_annotation={perms['modify_annotation']}, modify_assembly={perms['modify_assembly']}, "
                  f"modify_form={perms['modify_form']}) (0.15 pts)")
        else:
            restricted_count = sum(1 for f in edit_flags if not f)
            if restricted_count >= 2:
                print(f"PARTIAL: Component 5 — {restricted_count}/4 edit perms restricted (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 5 — Editing not restricted")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Copying/extraction is restricted (0.15 points)
    try:
        if not perms['extract']:
            print(f"PASS: Component 6 — Extraction/copying restricted (extract={perms['extract']}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Extraction/copying allowed (extract={perms['extract']})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
