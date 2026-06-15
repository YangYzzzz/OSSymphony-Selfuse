"""
Reward Script: Remove password from locked_report.pdf and save as unlocked_report.pdf
Task ID: pdf_fm_065
Domain: pdf
Scoring:
  Component 1: unlocked_report.pdf exists and is openable (0.2)
  Component 2: unlocked_report.pdf is NOT encrypted / password-protected (0.3)
  Component 3: Page count matches original locked_report.pdf (0.2)
  Component 4: Text content matches original locked_report.pdf (0.3)
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_065'

LOCKED_PATH = os.path.join(WORKDIR, 'Documents', 'locked_report.pdf')
UNLOCKED_PATH = os.path.join(WORKDIR, 'Documents', 'unlocked_report.pdf')
LOCKED_PASSWORD = 'OldPass123'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: locked_report.pdf must exist (gate, no points)
    if not os.path.exists(LOCKED_PATH):
        print(f"CRITICAL: Source file not found: {LOCKED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: unlocked_report.pdf exists and is a valid PDF (0.2 points)
    # This is task-introduced: the file does NOT exist before the agent acts.
    try:
        if not os.path.exists(UNLOCKED_PATH):
            print(f"FAIL: Component 1 — unlocked_report.pdf does not exist at {UNLOCKED_PATH}")
        else:
            doc_test = pymupdf.open(UNLOCKED_PATH)
            if doc_test.page_count > 0:
                print(f"PASS: Component 1 — unlocked_report.pdf exists and is a valid PDF ({doc_test.page_count} pages) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — unlocked_report.pdf has 0 pages")
            doc_test.close()
    except Exception as e:
        print(f"ERROR: Component 1 — cannot open unlocked_report.pdf: {e}")

    # Early exit if the file doesn't exist or can't be opened
    if total_score < 0.2:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: unlocked_report.pdf is NOT encrypted (0.3 points)
    # The task is to remove the password, so the output must not be encrypted.
    try:
        doc_unlocked = pymupdf.open(UNLOCKED_PATH)
        if not doc_unlocked.is_encrypted and doc_unlocked.needs_pass == 0:
            print(f"PASS: Component 2 — unlocked_report.pdf is NOT encrypted (is_encrypted={doc_unlocked.is_encrypted}, needs_pass={doc_unlocked.needs_pass}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — unlocked_report.pdf is still encrypted (is_encrypted={doc_unlocked.is_encrypted}, needs_pass={doc_unlocked.needs_pass})")
        doc_unlocked.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Open locked PDF with password for comparison
    try:
        doc_locked = pymupdf.open(LOCKED_PATH)
        auth_result = doc_locked.authenticate(LOCKED_PASSWORD)
        if auth_result == 0:
            print(f"WARNING: Could not authenticate locked_report.pdf with password '{LOCKED_PASSWORD}'")
            doc_locked.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Cannot open locked_report.pdf: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Page count matches (0.2 points)
    try:
        doc_unlocked = pymupdf.open(UNLOCKED_PATH)
        locked_pages = doc_locked.page_count
        unlocked_pages = doc_unlocked.page_count
        if locked_pages == unlocked_pages:
            print(f"PASS: Component 3 — page count matches (locked={locked_pages}, unlocked={unlocked_pages}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — page count mismatch (locked={locked_pages}, unlocked={unlocked_pages})")
        doc_unlocked.close()
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text content matches across all pages (0.3 points)
    try:
        doc_unlocked = pymupdf.open(UNLOCKED_PATH)
        pages_match = 0
        pages_total = min(doc_locked.page_count, doc_unlocked.page_count)

        if pages_total == 0:
            print(f"FAIL: Component 4 — no pages to compare")
        else:
            for i in range(pages_total):
                text_locked = doc_locked[i].get_text()
                text_unlocked = doc_unlocked[i].get_text()
                if text_locked == text_unlocked:
                    pages_match += 1
                else:
                    print(f"  Page {i}: text differs (locked has {len(text_locked)} chars, unlocked has {len(text_unlocked)} chars)")

            match_ratio = pages_match / pages_total
            if match_ratio == 1.0:
                print(f"PASS: Component 4 — all {pages_total} pages have matching text content (0.3 pts)")
                total_score += 0.3
            elif match_ratio >= 0.8:
                partial = round(0.3 * match_ratio, 2)
                print(f"PARTIAL: Component 4 — {pages_match}/{pages_total} pages match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — only {pages_match}/{pages_total} pages match")

        doc_unlocked.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc_locked.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
