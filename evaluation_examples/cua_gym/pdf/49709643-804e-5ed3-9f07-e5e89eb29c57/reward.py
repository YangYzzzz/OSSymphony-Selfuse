"""
Reward Script: Set user/owner passwords on a PDF
Task ID: pdf_mbc_009
Domain: pdf
Scoring:
  Component 1 (0.20): nda_secured.pdf exists and is encrypted
  Component 2 (0.20): User password 'viewonly55' authenticates
  Component 3 (0.20): Owner password 'legaladmin' authenticates with full permissions
  Component 4 (0.15): Encryption uses AES (128 or 256)
  Component 5 (0.25): Content identical to original nda_template.pdf
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_009'
SECURED_PATH = os.path.join(WORKDIR, 'Legal', 'nda_secured.pdf')
TEMPLATE_PATH = os.path.join(WORKDIR, 'Legal', 'nda_template.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: template must exist (gate, not scored)
    if not os.path.exists(TEMPLATE_PATH):
        print(f"CRITICAL: Template file not found: {TEMPLATE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: secured file must exist (gate, not scored independently as a change-check)
    if not os.path.exists(SECURED_PATH):
        print(f"FAIL: Secured file not found: {SECURED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: nda_secured.pdf is encrypted (0.20 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        import pymupdf
        doc = pymupdf.open(SECURED_PATH)
        is_enc = doc.is_encrypted
        needs = doc.needs_pass
        doc.close()
        if is_enc and needs:
            print(f"PASS: Component 1 — nda_secured.pdf is encrypted and requires password (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — is_encrypted={is_enc}, needs_pass={needs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: User password 'viewonly55' authenticates (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(SECURED_PATH)
        auth_result = doc.authenticate('viewonly55')
        doc.close()
        if auth_result > 0:
            print(f"PASS: Component 2 — User password 'viewonly55' works (auth={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — User password 'viewonly55' failed (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password 'legaladmin' grants full permissions (0.20 points)
    try:
        import pikepdf
        pdf = pikepdf.open(SECURED_PATH, password='legaladmin')
        perms = pdf.allow
        all_perms = (
            perms.print_lowres and perms.print_highres and
            perms.extract and perms.modify_other and
            perms.modify_annotation and perms.modify_assembly and
            perms.modify_form
        )
        pdf.close()
        if all_perms:
            print(f"PASS: Component 3 — Owner password 'legaladmin' grants full permissions (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Owner password works but not all permissions granted: {perms}")
    except pikepdf.PasswordError:
        print(f"FAIL: Component 3 — Owner password 'legaladmin' rejected")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Encryption uses AES (AES-128 R=4 or AES-256 R=6) (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(SECURED_PATH, password='legaladmin')
        enc = pdf.encryption
        # R=4 means AES-128, R=6 means AES-256; both acceptable per task context
        r_val = enc.R
        is_aes = r_val in (4, 6)
        pdf.close()
        if is_aes:
            bits = 128 if r_val == 4 else 256
            print(f"PASS: Component 4 — AES-{bits} encryption (R={r_val}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Encryption R={r_val}, expected R=4 (AES-128) or R=6 (AES-256)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Content identical to original nda_template.pdf (0.25 points)
    try:
        import pymupdf
        doc_template = pymupdf.open(TEMPLATE_PATH)
        doc_secured = pymupdf.open(SECURED_PATH)
        doc_secured.authenticate('viewonly55')

        template_pages = len(doc_template)
        secured_pages = len(doc_secured)

        if template_pages != secured_pages:
            print(f"FAIL: Component 5 — Page count mismatch: template={template_pages}, secured={secured_pages}")
        else:
            mismatched_page = -1
            for i in range(template_pages):
                t_text = doc_template[i].get_text()
                s_text = doc_secured[i].get_text()
                if t_text != s_text:
                    mismatched_page = i
                    break
            if mismatched_page < 0:
                print(f"PASS: Component 5 — Content identical ({template_pages} pages, text matches) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 5 — Text mismatch on page {mismatched_page + 1}")

        doc_template.close()
        doc_secured.close()
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
