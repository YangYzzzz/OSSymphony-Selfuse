"""
Reward Script: Multi-app PDF workflow — fill cover letter, merge PDFs, encrypt
Task ID: pdf_cross_137
Domain: pdf
Scoring:
  Component 1 (0.35): ~/Documents/application_james_park.pdf exists with 3+ pages
  Component 2 (0.25): application_james_park.pdf contains 'James Park' and 'Senior Engineer'
  Component 3 (0.20): ~/Documents/application_james_park_encrypted.pdf exists and is encrypted
  Component 4 (0.20): encrypted PDF can be opened with 'apply2026' and contains correct content
"""

import os

# Try importing pymupdf (newer) or fitz (older)
try:
    import pymupdf
    open_pdf = pymupdf.open
except ImportError:
    import fitz as pymupdf
    open_pdf = pymupdf.open

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_137'

MERGED_PATH = os.path.join(WORKDIR, 'application_james_park.pdf')
ENCRYPTED_PATH = os.path.join(WORKDIR, 'application_james_park_encrypted.pdf')
ENCRYPT_PASSWORD = 'apply2026'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------
    # Component 1: Merged PDF exists with 3+ pages (0.35 points)
    # The task requires merging 1-page cover letter + 2-page resume = 3+ pages.
    # This file should NOT exist on initial_env (no merge performed yet).
    # -----------------------------------------------------------------
    try:
        if not os.path.exists(MERGED_PATH):
            print(f"FAIL: Component 1 — {MERGED_PATH} does not exist")
        else:
            doc = open_pdf(MERGED_PATH)
            page_count = doc.page_count
            doc.close()
            if page_count >= 3:
                print(f"PASS: Component 1 — application_james_park.pdf exists with {page_count} pages (>= 3) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — application_james_park.pdf has only {page_count} pages, expected 3+")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------
    # Component 2: Merged PDF contains 'James Park' and 'Senior Engineer' (0.25 points)
    # This verifies the cover letter had placeholders filled with correct values.
    # On initial_env, cover_letter.odt exists (template with unfilled placeholders)
    # but application_james_park.pdf does NOT exist, so this will fail on initial.
    # -----------------------------------------------------------------
    try:
        if not os.path.exists(MERGED_PATH):
            print(f"FAIL: Component 2 — {MERGED_PATH} does not exist (cannot check content)")
        else:
            doc = open_pdf(MERGED_PATH)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()

            has_name = 'James Park' in full_text
            has_position = 'Senior Engineer' in full_text

            if has_name and has_position:
                print(f"PASS: Component 2 — found 'James Park' and 'Senior Engineer' in merged PDF (0.25 pts)")
                total_score += 0.25
            elif has_name:
                print(f"FAIL: Component 2 — found 'James Park' but missing 'Senior Engineer'")
            elif has_position:
                print(f"FAIL: Component 2 — found 'Senior Engineer' but missing 'James Park'")
            else:
                print(f"FAIL: Component 2 — missing both 'James Park' and 'Senior Engineer' in merged PDF")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------
    # Component 3: Encrypted PDF exists and is encrypted (0.20 points)
    # application_james_park_encrypted.pdf should NOT exist on initial_env.
    # -----------------------------------------------------------------
    try:
        if not os.path.exists(ENCRYPTED_PATH):
            print(f"FAIL: Component 3 — {ENCRYPTED_PATH} does not exist")
        else:
            doc = open_pdf(ENCRYPTED_PATH)
            is_encrypted = doc.is_encrypted
            doc.close()
            if is_encrypted:
                print(f"PASS: Component 3 — application_james_park_encrypted.pdf exists and is encrypted (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — application_james_park_encrypted.pdf exists but is NOT encrypted")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------
    # Component 4: Encrypted PDF opens with password 'apply2026' and
    # contains correct content (James Park + Senior Engineer) (0.20 points)
    # Verifies both the password correctness and content integrity.
    # -----------------------------------------------------------------
    try:
        if not os.path.exists(ENCRYPTED_PATH):
            print(f"FAIL: Component 4 — {ENCRYPTED_PATH} does not exist (cannot check password)")
        else:
            doc = open_pdf(ENCRYPTED_PATH)
            if not doc.is_encrypted:
                doc.close()
                print(f"FAIL: Component 4 — encrypted PDF is not encrypted; cannot test password")
            else:
                auth_result = doc.authenticate(ENCRYPT_PASSWORD)
                if auth_result == 0:
                    doc.close()
                    print(f"FAIL: Component 4 — password '{ENCRYPT_PASSWORD}' did NOT open the encrypted PDF (auth={auth_result})")
                else:
                    # Password correct — now also verify content
                    full_text = ""
                    for page in doc:
                        full_text += page.get_text()
                    doc.close()

                    has_name = 'James Park' in full_text
                    has_position = 'Senior Engineer' in full_text

                    if has_name and has_position:
                        print(f"PASS: Component 4 — password 'apply2026' works and content intact (James Park + Senior Engineer) (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 4 — password works but content missing: has_name={has_name}, has_position={has_position}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
