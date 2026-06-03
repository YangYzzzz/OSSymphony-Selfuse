"""
Reward Script: Set PDF permissions (low-res print only, no extract, no modify)
Task ID: pdf_mbc_015
Domain: pdf
Scoring:
  Component 1 (0.25): Restricted file exists and is encrypted with owner password 'ownerCtrl99'
  Component 2 (0.25): Low-res printing allowed, high-res printing disallowed
  Component 3 (0.25): Content extraction disallowed and modification disallowed
  Component 4 (0.25): Content integrity — page count and text match original
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_015'
OWNER_PASSWORD = 'ownerCtrl99'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'shared_manual.pdf')
RESTRICTED_PATH = os.path.join(WORKDIR, 'Documents', 'shared_manual_restricted.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: restricted file must exist (task-introduced)
    if not os.path.exists(RESTRICTED_PATH):
        print(f"FAIL: Restricted file not found at {RESTRICTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted and owner password 'ownerCtrl99' works (0.25 points)
    try:
        import pikepdf
        # First, try opening with owner password — must succeed
        pdf = pikepdf.open(RESTRICTED_PATH, password=OWNER_PASSWORD)
        enc = pdf.encryption
        # Verify encryption is actually present (R >= 2 means some encryption)
        if enc.R >= 2:
            print(f"PASS: Component 1 — File is encrypted (R={enc.R}) and owner password works (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Encryption revision too low: R={enc.R}")
        pdf.close()
    except pikepdf.PasswordError:
        print(f"FAIL: Component 1 — Owner password 'ownerCtrl99' does not work")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Low-res printing allowed, high-res printing disallowed (0.25 points)
    try:
        import pikepdf
        pdf = pikepdf.open(RESTRICTED_PATH, password=OWNER_PASSWORD)
        allow = pdf.allow
        lowres_ok = allow.print_lowres
        highres_off = not allow.print_highres
        if lowres_ok and highres_off:
            print(f"PASS: Component 2 — print_lowres={allow.print_lowres}, print_highres={allow.print_highres} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — print_lowres={allow.print_lowres} (expect True), print_highres={allow.print_highres} (expect False)")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content extraction and modification disallowed (0.25 points)
    try:
        import pikepdf
        pdf = pikepdf.open(RESTRICTED_PATH, password=OWNER_PASSWORD)
        allow = pdf.allow
        extract_off = not allow.extract
        modify_off = not allow.modify_other
        if extract_off and modify_off:
            print(f"PASS: Component 3 — extract={allow.extract}, modify_other={allow.modify_other} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — extract={allow.extract} (expect False), modify_other={allow.modify_other} (expect False)")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content integrity — page count and text match original (0.25 points)
    # This checks that the restricted file has identical content to the original,
    # which is a task requirement ("Content identical"). Only awards points if the
    # restricted file exists (which is task-introduced), so this component is anchored
    # to the task change.
    try:
        import pymupdf
        if not os.path.exists(ORIGINAL_PATH):
            print(f"FAIL: Component 4 — Original file not found at {ORIGINAL_PATH}")
        else:
            doc_orig = pymupdf.open(ORIGINAL_PATH)
            doc_rest = pymupdf.open(RESTRICTED_PATH)
            # Authenticate if needed
            if doc_rest.is_encrypted:
                doc_rest.authenticate(OWNER_PASSWORD)

            pages_match = doc_orig.page_count == doc_rest.page_count
            # Compare text on first, middle, and last pages
            text_match = True
            sample_pages = [0, doc_orig.page_count // 2, doc_orig.page_count - 1]
            for pg in sample_pages:
                t1 = doc_orig[pg].get_text()
                t2 = doc_rest[pg].get_text()
                if t1 != t2:
                    text_match = False
                    print(f"  Text mismatch on page {pg}")
                    break

            if pages_match and text_match:
                print(f"PASS: Component 4 — Content intact: {doc_orig.page_count} pages, text matches on sampled pages (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — pages_match={pages_match}, text_match={text_match}")

            doc_orig.close()
            doc_rest.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
