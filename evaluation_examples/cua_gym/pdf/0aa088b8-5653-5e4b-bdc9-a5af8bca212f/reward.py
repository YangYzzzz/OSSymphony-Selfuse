"""
Reward Script: Apply password protection to attorney-client memo PDF
Task ID: pdf_legal_007
Domain: pdf
Scoring:
  Component 1 (0.20): Protected file exists and is encrypted
  Component 2 (0.20): User password 'priv2024!' opens the file
  Component 3 (0.15): Owner password 'admin2024!' opens the file
  Component 4 (0.20): Printing restricted (lowres + highres disabled)
  Component 5 (0.15): Copying/extraction restricted
  Component 6 (0.10): Page count preserved (4 pages)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_007'
PROTECTED_PATH = os.path.join(WORKDIR, 'legal', 'attorney_client_memo_protected.pdf')
USER_PASSWORD = 'priv2024!'
OWNER_PASSWORD = 'admin2024!'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Protected file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    import pikepdf

    # Component 1: File is encrypted (0.20 points)
    try:
        is_encrypted = False
        try:
            pdf_test = pikepdf.open(file_path)
            pdf_test.close()
            # If we get here, file is NOT encrypted
        except pikepdf._core.PasswordError:
            is_encrypted = True

        if is_encrypted:
            print(f"PASS: Component 1 -- File is encrypted (requires password) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- File opened without password, not encrypted")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: User password 'priv2024!' opens the file (0.20 points)
    pdf_user = None
    try:
        user_pw_works = False
        try:
            pdf_user = pikepdf.open(file_path, password=USER_PASSWORD)
            user_pw_works = True
        except pikepdf._core.PasswordError:
            pass

        if user_pw_works:
            print(f"PASS: Component 2 -- User password '{USER_PASSWORD}' works (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- User password '{USER_PASSWORD}' rejected")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Owner password 'admin2024!' opens the file (0.15 points)
    pdf_owner = None
    try:
        owner_pw_works = False
        try:
            pdf_owner = pikepdf.open(file_path, password=OWNER_PASSWORD)
            owner_pw_works = True
        except pikepdf._core.PasswordError:
            pass

        if owner_pw_works:
            print(f"PASS: Component 3 -- Owner password '{OWNER_PASSWORD}' works (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Owner password '{OWNER_PASSWORD}' rejected")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Printing restricted -- both print_lowres and print_highres must be False (0.20 points)
    try:
        if pdf_user is not None:
            allow = pdf_user.allow
            print_low = allow.print_lowres
            print_high = allow.print_highres
            if not print_low and not print_high:
                print(f"PASS: Component 4 -- Printing restricted (lowres={print_low}, highres={print_high}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- Printing NOT fully restricted (lowres={print_low}, highres={print_high})")
        else:
            print(f"FAIL: Component 4 -- Cannot check permissions (user password failed)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Copying/extraction restricted -- extract must be False (0.15 points)
    try:
        if pdf_user is not None:
            allow = pdf_user.allow
            extract_allowed = allow.extract
            if not extract_allowed:
                print(f"PASS: Component 5 -- Copying/extraction restricted (extract={extract_allowed}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- Copying/extraction NOT restricted (extract={extract_allowed})")
        else:
            print(f"FAIL: Component 5 -- Cannot check permissions (user password failed)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Page count preserved (4 pages) (0.10 points)
    try:
        if pdf_user is not None:
            page_count = len(pdf_user.pages)
            if page_count == 4:
                print(f"PASS: Component 6 -- Page count correct ({page_count} pages) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- Expected 4 pages, found {page_count}")
        else:
            print(f"FAIL: Component 6 -- Cannot check pages (user password failed)")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Clean up
    try:
        if pdf_user is not None:
            pdf_user.close()
        if pdf_owner is not None:
            pdf_owner.close()
    except Exception:
        pass

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PROTECTED_PATH):
    print(f"File not found: {PROTECTED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PROTECTED_PATH)
