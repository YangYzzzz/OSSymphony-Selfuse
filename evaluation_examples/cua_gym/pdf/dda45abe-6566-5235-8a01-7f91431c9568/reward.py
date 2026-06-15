"""
Reward Script: Remove existing password protection and re-encrypt with new credentials
Task ID: pdf_legal_050
Domain: pdf
Scoring:
  - Component 1 (0.35): File is encrypted and opens with new user password 'archive2024secure'
  - Component 2 (0.25): Old password 'oldpass123' does NOT open the file
  - Component 3 (0.20): Owner password 'firmadmin2024' opens the file
  - Component 4 (0.20): Document content is preserved (4 pages, expected text present)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_050'
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'archived', 'case_2020_reencrypted.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted and opens with new user password 'archive2024secure' (0.35 points)
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        if doc.is_encrypted:
            auth_result = doc.authenticate('archive2024secure')
            if auth_result > 0:
                print(f"PASS: Component 1 — File is encrypted and opens with new user password (auth={auth_result}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — File is encrypted but new user password 'archive2024secure' did not work (auth={auth_result})")
            doc.close()
        else:
            print("FAIL: Component 1 — File is NOT encrypted")
            doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Old password 'oldpass123' does NOT open the file (0.25 points)
    try:
        import pymupdf
        doc2 = pymupdf.open(file_path)
        if doc2.is_encrypted:
            auth_old = doc2.authenticate('oldpass123')
            if auth_old == 0:
                print(f"PASS: Component 2 — Old password 'oldpass123' correctly rejected (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Old password 'oldpass123' still works (auth={auth_old})")
            doc2.close()
        else:
            print("FAIL: Component 2 — File is not encrypted, cannot test old password rejection")
            doc2.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Owner password 'firmadmin2024' works (0.20 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='firmadmin2024')
        page_count = len(pdf.pages)
        if page_count > 0:
            print(f"PASS: Component 3 — Owner password 'firmadmin2024' opens the file ({page_count} pages) (0.20 pts)")
            total_score += 0.20
        pdf.close()
    except pikepdf.PasswordError:
        print("FAIL: Component 3 — Owner password 'firmadmin2024' was rejected")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Document content is preserved (0.20 points)
    # The original document has 4 pages and contains specific legal text
    try:
        import pymupdf
        doc3 = pymupdf.open(file_path)
        if doc3.is_encrypted:
            doc3.authenticate('archive2024secure')

        content_score = 0.0

        # Check page count (should be 4)
        if doc3.page_count == 4:
            content_score += 0.10
            print(f"PASS: Component 4a — Page count is 4 as expected")
        else:
            print(f"FAIL: Component 4a — Expected 4 pages, found {doc3.page_count}")

        # Check that key text content is preserved
        page0_text = doc3[0].get_text()
        if "GREENFIELD PROPERTIES" in page0_text and "PACIFIC RIM DEVELOPMENT" in page0_text and "BC-2020-04587" in page0_text:
            content_score += 0.10
            print(f"PASS: Component 4b — Key legal text content preserved on page 1")
        else:
            print(f"FAIL: Component 4b — Key legal text content missing from page 1")

        if content_score > 0:
            total_score += content_score
        doc3.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
