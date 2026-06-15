"""
Reward Script: Batch apply password protection to PDF files
Task ID: pdf_fin_086
Domain: pdf
Scoring:
  Component 1 (0.20): All 6 protected PDF files exist in output directory
  Component 2 (0.25): All 6 files are encrypted (require password to open)
  Component 3 (0.20): User password 'view_2024' works on all 6 files
  Component 4 (0.10): Owner password 'admin_2024' works on all 6 files
  Component 5 (0.10): AES-256 encryption (R=6) on all 6 files
  Component 6 (0.10): Printing restricted on all 6 files
  Component 7 (0.05): Copying (extract) restricted on all 6 files
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_086'

EXPECTED_FILES = [
    'payroll.pdf',
    'tax_ids.pdf',
    'bank_details.pdf',
    'ssn_list.pdf',
    'salary_schedule.pdf',
    'bonus_plan.pdf',
]

PROTECTED_DIR = os.path.join(WORKDIR, 'finance', 'sensitive', 'protected')
USER_PASSWORD = 'view_2024'
OWNER_PASSWORD = 'admin_2024'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 6 protected PDF files exist (0.20 points)
    try:
        existing_files = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(PROTECTED_DIR, fname)
            if os.path.isfile(fpath):
                existing_files.append(fname)
        ratio = len(existing_files) / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 1 — All 6 protected files exist (0.20 pts)")
            total_score += 0.20
        elif ratio > 0:
            partial = round(0.20 * ratio, 3)
            print(f"PARTIAL: Component 1 — {len(existing_files)}/6 files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No protected files found in {PROTECTED_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Early exit if no files exist
    if not existing_files:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All files are encrypted (require password to open) (0.25 points)
    try:
        import pikepdf
        encrypted_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath)
                # If it opens without password, it's not encrypted
                pdf.close()
                print(f"  FAIL: {fname} is NOT encrypted (opened without password)")
            except pikepdf.PasswordError:
                encrypted_count += 1
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = encrypted_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 2 — All 6 files are encrypted (0.25 pts)")
            total_score += 0.25
        elif ratio > 0:
            partial = round(0.25 * ratio, 3)
            print(f"PARTIAL: Component 2 — {encrypted_count}/6 files encrypted ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No files are encrypted")
    except ImportError:
        print(f"ERROR: Component 2 — pikepdf not available")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: User password 'view_2024' works on all files (0.20 points)
    try:
        import pikepdf
        user_pw_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath, password=USER_PASSWORD)
                user_pw_count += 1
                pdf.close()
            except pikepdf.PasswordError:
                print(f"  FAIL: {fname} — user password '{USER_PASSWORD}' rejected")
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = user_pw_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 3 — User password works on all 6 files (0.20 pts)")
            total_score += 0.20
        elif ratio > 0:
            partial = round(0.20 * ratio, 3)
            print(f"PARTIAL: Component 3 — User password works on {user_pw_count}/6 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — User password rejected on all files")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Owner password 'admin_2024' works on all files (0.10 points)
    try:
        import pikepdf
        owner_pw_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath, password=OWNER_PASSWORD)
                owner_pw_count += 1
                pdf.close()
            except pikepdf.PasswordError:
                print(f"  FAIL: {fname} — owner password '{OWNER_PASSWORD}' rejected")
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = owner_pw_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 4 — Owner password works on all 6 files (0.10 pts)")
            total_score += 0.10
        elif ratio > 0:
            partial = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 4 — Owner password works on {owner_pw_count}/6 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Owner password rejected on all files")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: AES-256 encryption (R=6) on all files (0.10 points)
    try:
        import pikepdf
        aes256_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath, password=OWNER_PASSWORD)
                enc = pdf.encryption
                if enc.R == 6:
                    aes256_count += 1
                else:
                    print(f"  FAIL: {fname} — encryption R={enc.R}, expected R=6 (AES-256)")
                pdf.close()
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = aes256_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 5 — AES-256 (R=6) on all 6 files (0.10 pts)")
            total_score += 0.10
        elif ratio > 0:
            partial = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 5 — AES-256 on {aes256_count}/6 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No files use AES-256 encryption")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Printing restricted on all files (0.10 points)
    try:
        import pikepdf
        print_restricted_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath, password=OWNER_PASSWORD)
                allow = pdf.allow
                if not allow.print_lowres and not allow.print_highres:
                    print_restricted_count += 1
                else:
                    print(f"  FAIL: {fname} — print_lowres={allow.print_lowres}, print_highres={allow.print_highres}")
                pdf.close()
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = print_restricted_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 6 — Printing restricted on all 6 files (0.10 pts)")
            total_score += 0.10
        elif ratio > 0:
            partial = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 6 — Printing restricted on {print_restricted_count}/6 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — No files have printing restricted")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Copying (extract) restricted on all files (0.05 points)
    try:
        import pikepdf
        copy_restricted_count = 0
        for fname in existing_files:
            fpath = os.path.join(PROTECTED_DIR, fname)
            try:
                pdf = pikepdf.open(fpath, password=OWNER_PASSWORD)
                allow = pdf.allow
                if not allow.extract:
                    copy_restricted_count += 1
                else:
                    print(f"  FAIL: {fname} — extract={allow.extract} (should be False)")
                pdf.close()
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        ratio = copy_restricted_count / len(EXPECTED_FILES)
        if ratio == 1.0:
            print(f"PASS: Component 7 — Copying restricted on all 6 files (0.05 pts)")
            total_score += 0.05
        elif ratio > 0:
            partial = round(0.05 * ratio, 3)
            print(f"PARTIAL: Component 7 — Copying restricted on {copy_restricted_count}/6 files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 7 — No files have copying restricted")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
