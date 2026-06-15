"""
Reward Script: PDF Encryption Verification
Task ID: pdf_mbc_022
Domain: pdf
Scoring:
  C1 (0.15) - Secure file exists and is password-protected
  C2 (0.20) - User password 'mytax$2024' opens the file
  C3 (0.15) - Owner password 'admin#tax' opens the file
  C4 (0.20) - AES-256 encryption (R=6, V=5, AESV3 cipher)
  C5 (0.15) - Printing is allowed (lowres + highres)
  C6 (0.15) - Copy/edit/annotation are disabled
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_022'
SECURE_FILE = os.path.join(WORKDIR, 'Documents', 'tax_return_2024_secure.pdf')
USER_PASSWORD = 'mytax$2024'
OWNER_PASSWORD = 'admin#tax'


def verify_task():
    """
    Verify PDF encryption task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: secure file must exist
    if not os.path.exists(SECURE_FILE):
        print(f"CRITICAL: Secure file not found: {SECURE_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is password-protected (0.15 points)
    # It should NOT open without a password
    try:
        import pikepdf
        needs_password = False
        try:
            pdf = pikepdf.open(SECURE_FILE)
            # If it opens without password, it's not protected
            pdf.close()
            print("FAIL: Component 1 - File opens without password (not encrypted)")
        except pikepdf.PasswordError:
            needs_password = True
            print(f"PASS: Component 1 - File requires password to open (0.15 pts)")
            total_score += 0.15
        except Exception as e:
            print(f"ERROR: Component 1 - Unexpected error: {e}")
    except ImportError:
        print("ERROR: Component 1 - pikepdf not available")

    if not needs_password:
        # If file doesn't need password, remaining checks are moot
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: User password works (0.20 points)
    user_pdf = None
    try:
        import pikepdf
        user_pdf = pikepdf.open(SECURE_FILE, password=USER_PASSWORD)
        print(f"PASS: Component 2 - User password 'mytax$2024' opens file (0.20 pts)")
        total_score += 0.20
    except pikepdf.PasswordError:
        print(f"FAIL: Component 2 - User password 'mytax$2024' does not open file")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Owner password works (0.15 points)
    try:
        import pikepdf
        owner_pdf = pikepdf.open(SECURE_FILE, password=OWNER_PASSWORD)
        print(f"PASS: Component 3 - Owner password 'admin#tax' opens file (0.15 pts)")
        total_score += 0.15
        owner_pdf.close()
    except pikepdf.PasswordError:
        print(f"FAIL: Component 3 - Owner password 'admin#tax' does not open file")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: AES-256 encryption (R=6, V=5, AESV3) (0.20 points)
    try:
        if user_pdf is not None:
            trailer = user_pdf.trailer
            enc = trailer.get('/Encrypt')
            if enc:
                v_val = int(enc.get('/V', 0))
                r_val = int(enc.get('/R', 0))
                cf = enc.get('/CF')
                cfm_name = ''
                if cf:
                    std_cf = cf.get('/StdCF')
                    if std_cf:
                        cfm_name = str(std_cf.get('/CFM', ''))

                is_aes256 = (v_val == 5 and r_val == 6 and 'AESV3' in cfm_name)
                if is_aes256:
                    print(f"PASS: Component 4 - AES-256 encryption (V={v_val}, R={r_val}, CFM={cfm_name}) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 - Not AES-256. V={v_val}, R={r_val}, CFM={cfm_name}")
            else:
                print("FAIL: Component 4 - No /Encrypt dictionary found")
        else:
            print("SKIP: Component 4 - Could not open file with user password")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Printing allowed (0.15 points)
    try:
        if user_pdf is not None:
            allow = user_pdf.allow
            if allow.print_lowres and allow.print_highres:
                print(f"PASS: Component 5 - Printing allowed (lowres={allow.print_lowres}, highres={allow.print_highres}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - Printing not fully allowed (lowres={allow.print_lowres}, highres={allow.print_highres})")
        else:
            print("SKIP: Component 5 - Could not open file with user password")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Copy/edit/annotation disabled (0.15 points)
    try:
        if user_pdf is not None:
            allow = user_pdf.allow
            restricted = (
                not allow.extract
                and not allow.modify_other
                and not allow.modify_annotation
                and not allow.modify_form
                and not allow.modify_assembly
            )
            if restricted:
                print(f"PASS: Component 6 - All restricted permissions disabled (extract={allow.extract}, modify_other={allow.modify_other}, modify_annotation={allow.modify_annotation}, modify_form={allow.modify_form}, modify_assembly={allow.modify_assembly}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 - Some restricted permissions still allowed: extract={allow.extract}, modify_other={allow.modify_other}, modify_annotation={allow.modify_annotation}, modify_form={allow.modify_form}, modify_assembly={allow.modify_assembly}")
        else:
            print("SKIP: Component 6 - Could not open file with user password")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Cleanup
    if user_pdf is not None:
        try:
            user_pdf.close()
        except Exception:
            pass

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
