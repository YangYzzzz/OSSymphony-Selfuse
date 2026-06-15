"""
Reward Script: Password-protect salary_data.pdf with qpdf
Task ID: pdf_fm_064
Domain: pdf (libreoffice_calc listed but actual domain is pdf)
Scoring:
  Component 1 (0.4): Protected file exists and is encrypted (requires password)
  Component 2 (0.3): Password 'Finance2025!' successfully authenticates
  Component 3 (0.3): Content identical to original (5 pages, same text)
"""

import os
import pymupdf  # PyMuPDF / fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_064'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'confidential', 'salary_data.pdf')
PROTECTED_PATH = os.path.join(WORKDIR, 'Documents', 'confidential', 'salary_data_protected.pdf')
PASSWORD = 'Finance2025!'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist (not scored)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Protected file exists AND is encrypted (0.4 points)
    # This fails on initial_env (file doesn't exist) and passes on golden_env
    try:
        if not os.path.exists(PROTECTED_PATH):
            print(f"FAIL: Component 1 — Protected file not found: {PROTECTED_PATH}")
        else:
            doc = pymupdf.open(PROTECTED_PATH)
            is_enc = doc.is_encrypted
            needs_pw = doc.needs_pass
            doc.close()
            if is_enc and needs_pw:
                print(f"PASS: Component 1 — Protected file exists and is encrypted (needs_pass={needs_pw}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — File exists but is_encrypted={is_enc}, needs_pass={needs_pw}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Password 'Finance2025!' authenticates successfully (0.3 points)
    # This fails on initial_env (file doesn't exist) and passes on golden_env
    try:
        if not os.path.exists(PROTECTED_PATH):
            print(f"FAIL: Component 2 — Protected file not found")
        else:
            doc = pymupdf.open(PROTECTED_PATH)
            if not doc.is_encrypted:
                print(f"FAIL: Component 2 — File is not encrypted, cannot test password")
                doc.close()
            else:
                auth_result = doc.authenticate(PASSWORD)
                doc.close()
                if auth_result > 0:
                    print(f"PASS: Component 2 — Password '{PASSWORD}' authenticates (auth_result={auth_result}) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Password '{PASSWORD}' rejected (auth_result={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content matches original (5 pages, same text on all pages) (0.3 points)
    # This fails on initial_env (file doesn't exist) and passes on golden_env
    try:
        if not os.path.exists(PROTECTED_PATH):
            print(f"FAIL: Component 3 — Protected file not found")
        else:
            doc_orig = pymupdf.open(ORIGINAL_PATH)
            doc_prot = pymupdf.open(PROTECTED_PATH)

            # Authenticate if needed
            if doc_prot.is_encrypted:
                doc_prot.authenticate(PASSWORD)

            orig_pages = len(doc_orig)
            prot_pages = len(doc_prot)

            if orig_pages != prot_pages:
                print(f"FAIL: Component 3 — Page count mismatch: original={orig_pages}, protected={prot_pages}")
                doc_orig.close()
                doc_prot.close()
            else:
                # Compare text content of all pages
                mismatched_page = -1
                for i in range(orig_pages):
                    t_orig = doc_orig[i].get_text()
                    t_prot = doc_prot[i].get_text()
                    if t_orig != t_prot:
                        mismatched_page = i
                        print(f"FAIL: Component 3 — Page {i} text differs (orig_len={len(t_orig)}, prot_len={len(t_prot)})")
                        break

                doc_orig.close()
                doc_prot.close()

                if mismatched_page < 0:
                    print(f"PASS: Component 3 — Content matches original ({orig_pages} pages, all text identical) (0.3 pts)")
                    total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
