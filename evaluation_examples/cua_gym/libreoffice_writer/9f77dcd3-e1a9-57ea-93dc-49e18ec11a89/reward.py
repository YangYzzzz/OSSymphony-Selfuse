"""
Reward Script: Export Writer document as PDF with specific metadata title
Task ID: writer_biz_041
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): PDF file exists at expected path
  Component 2 (0.5): PDF metadata title matches 'Meridian Solutions - Partnership Proposal 2025'
  Component 3 (0.2): PDF has substantive content (multiple pages from the business proposal)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_041'
EXPECTED_TITLE = 'Meridian Solutions - Partnership Proposal 2025'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    pdf_path = os.path.join(WORKDIR, f'{TASK_ID}.pdf')

    # Component 1: PDF file exists (0.3 points)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        if os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"PASS: Component 1 — PDF file exists at {pdf_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — PDF file not found or empty at {pdf_path}")
            # No PDF means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF metadata title matches expected value (0.5 points)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        actual_title = meta.get('title', '') or ''
        doc.close()

        if actual_title.strip() == EXPECTED_TITLE:
            print(f"PASS: Component 2 — PDF title matches exactly: '{actual_title}' (0.5 pts)")
            total_score += 0.5
        elif EXPECTED_TITLE.lower() in actual_title.lower():
            # Partial credit for case-insensitive match
            print(f"PARTIAL: Component 2 — PDF title case mismatch: '{actual_title}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected title '{EXPECTED_TITLE}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF has substantive content (0.2 points)
    # Verifies the PDF is a real export of the business proposal, not an empty file
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        import fitz
        doc = fitz.open(pdf_path)
        page_count = doc.page_count

        # The business proposal should have multiple pages
        if page_count >= 2:
            # Check that first page has some text content
            first_page_text = doc.load_page(0).get_text().strip()
            doc.close()
            if len(first_page_text) > 50:
                print(f"PASS: Component 3 — PDF has {page_count} pages with content (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — PDF first page has insufficient text ({len(first_page_text)} chars)")
        else:
            doc.close()
            print(f"FAIL: Component 3 — PDF has only {page_count} page(s), expected multi-page proposal")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()
verify_task()
