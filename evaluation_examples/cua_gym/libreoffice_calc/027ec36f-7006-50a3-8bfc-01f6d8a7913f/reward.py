"""
Reward Script: Decrypt and re-encrypt PDF with new password and AES-128
Task ID: pdf_mbc_029
Domain: pdf
Scoring:
  Component 1 (0.25): New file exists and is a valid encrypted PDF
  Component 2 (0.25): New file opens with new password 'newArch2025!'
  Component 3 (0.20): Old password 'arch1ve2020' does NOT open the new file
  Component 4 (0.15): Encryption uses AES-128 (AESV2)
  Component 5 (0.15): Content preserved (page count + text match with original)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_029'

NEW_FILE = os.path.join(WORKDIR, 'Secure', 'archived_records_new.pdf')
ORIG_FILE = os.path.join(WORKDIR, 'Secure', 'archived_records.pdf')
NEW_PASSWORD = 'newArch2025!'
OLD_PASSWORD = 'arch1ve2020'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: New file exists and is a valid encrypted PDF (0.25 points)
    try:
        import pymupdf
        if not os.path.exists(NEW_FILE):
            print(f"FAIL: Component 1 -- {NEW_FILE} does not exist")
        else:
            doc = pymupdf.open(NEW_FILE)
            if doc.is_encrypted:
                print(f"PASS: Component 1 -- {NEW_FILE} exists and is encrypted (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- {NEW_FILE} exists but is NOT encrypted")
            doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: New file opens with new password 'newArch2025!' (0.25 points)
    try:
        import pymupdf
        doc = pymupdf.open(NEW_FILE)
        auth_result = doc.authenticate(NEW_PASSWORD)
        if auth_result > 0:
            print(f"PASS: Component 2 -- New password authenticates (auth={auth_result}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- New password 'newArch2025!' failed to authenticate (auth={auth_result})")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Old password 'arch1ve2020' does NOT open the new file (0.20 points)
    try:
        import pymupdf
        doc = pymupdf.open(NEW_FILE)
        auth_result = doc.authenticate(OLD_PASSWORD)
        if auth_result == 0:
            print(f"PASS: Component 3 -- Old password correctly rejected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Old password 'arch1ve2020' still opens the new file (auth={auth_result})")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Encryption uses AES-128 (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(NEW_FILE, password=NEW_PASSWORD)
        enc = pdf.encryption
        stream_method = str(enc.stream_method)
        # Check for AES encryption method
        is_aes = 'aes' in stream_method.lower()
        # Check encrypt dict for AESV2 and key length 128
        aesv2_found = ('AESV2' in str(pdf.trailer.get('/Encrypt', {}).get('/CF', {}).get('/StdCF', {}).get('/CFM', '')))
        length_128 = (int(pdf.trailer.get('/Encrypt', {}).get('/Length', 0)) == 128)

        if is_aes and (aesv2_found or length_128):
            print(f"PASS: Component 4 -- AES-128 encryption confirmed (stream={stream_method}, AESV2={aesv2_found}, len128={length_128}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Expected AES-128, got stream={stream_method}, AESV2={aesv2_found}, len128={length_128}")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Content preserved - page count and text match (0.15 points)
    try:
        import pymupdf
        # Open original with old password
        doc_orig = pymupdf.open(ORIG_FILE)
        doc_orig.authenticate(OLD_PASSWORD)

        # Open new with new password
        doc_new = pymupdf.open(NEW_FILE)
        doc_new.authenticate(NEW_PASSWORD)

        orig_pages = len(doc_orig)
        new_pages = len(doc_new)

        if orig_pages != new_pages:
            print(f"FAIL: Component 5 -- Page count mismatch: original={orig_pages}, new={new_pages}")
        else:
            # Sample pages for text comparison
            pages_to_check = [0, orig_pages // 2, orig_pages - 1]
            mismatched = [pi for pi in pages_to_check if doc_orig[pi].get_text('text') != doc_new[pi].get_text('text')]
            if len(mismatched) == 0:
                print(f"PASS: Component 5 -- Content preserved ({new_pages} pages, sampled text matches) (0.15 pts)")
                total_score += 0.15

        doc_orig.close()
        doc_new.close()
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(NEW_FILE):
    print(f"File not found: {NEW_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()
